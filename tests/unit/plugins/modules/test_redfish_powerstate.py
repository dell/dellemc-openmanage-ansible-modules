# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.0.0
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import redfish_powerstate
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from unittest.mock import MagicMock
from ansible.module_utils._text import to_text

tarrget_error_msg = "The target device does not support the system reset" \
                    " feature using Redfish API."
MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
HTTPS_ADDRESS = 'https://testhost.com'
INVALID_RESET_TYPE = "The target device does not support a {0} operation.The acceptable values for device reset types are {1}."
INVALID_RESET_TYPE_OEM = "'{option}' is not supported. The supported values" \
    " are {supported_oem_reset_type_values}. Enter the valid values and retry" \
    " the operation."
MODULE_PATH_COMP = 'ansible_collections.dellemc.openmanage.plugins.modules.redfish_powerstate.'
VENDOR_NOT_SPECIFIED = "The vendor is not specified. Enter the valid vendor and retry the operation."
VALIDATE_FINAL_PWR_STATE = 'redfish_powerstate.is_valid_final_pwr_state'
VALIDATE_VENDOR = 'redfish_powerstate.is_valid_vendor'
CHECK_FIRMWARE_VERSION = 'redfish_powerstate.check_firmware_version'
VALIDATE_RESET_TYPE = 'redfish_powerstate.is_valid_reset_type'
FETCH_PWR_URI = 'redfish_powerstate.fetch_power_uri_resource'
TARGET_URI = "/redfish/v1/Chassis/System.Embedded.1/Actions/Oem/DellOemChassis.ExtendedReset"
RESET_URI = '/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset'
ROOT_URI = "/redfish/v1/"
RESET_ALLOWED_KEY = "ResetType@Redfish.AllowableValues"
ODATA_KEY = "@odata.id"
RESOURCE_URI = "/redfish/v1/Systems"
SPECIFIC_RESOURCE_URI_ONE = "/redfish/v1/Systems/System.Embedded.1"
SPECIFIC_RESOURCE_URI_TWO = "/redfish/v1/Systems/System.Embedded.2"


@pytest.fixture
def redfish_connection_mock_for_powerstate(mocker, redfish_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'redfish_powerstate.Redfish')
    redfish_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    redfish_connection_mock_obj.invoke_request.return_value = redfish_response_mock
    return redfish_connection_mock_obj


class TestRedfishPowerstate(FakeAnsibleModule):
    module = redfish_powerstate

    arg_list1 = [{"resource_id": "System.Embedded.1", "reset_type": "ForceOff"}]
    resource_uri_output = {
        "Systems": {
            ODATA_KEY: RESOURCE_URI
        },
        "Members": [
            {
                ODATA_KEY: SPECIFIC_RESOURCE_URI_ONE
            },
            {
                ODATA_KEY: SPECIFIC_RESOURCE_URI_TWO
            }
        ],
        "Actions": {
            "#ComputerSystem.Reset": {
                "target": RESET_URI,
                RESET_ALLOWED_KEY: [
                    "On",
                    "ForceOff",
                    "ForceRestart",
                    "GracefulShutdown",
                    "PushPowerButton",
                    "Nmi",
                    "PowerCycle"
                ]
            }
        },
        "PowerState": "On"
    }

    def test_fetch_powerstate_resource_success_case_01(self, mocker, redfish_connection_mock_for_powerstate, redfish_default_args,
                                                       redfish_response_mock):
        """dynamically fetch the computer system id if one member exists in system"""
        f_module = self.get_module_mock(params={"reset_type": "ForceOff"})

        redfish_response_mock.json_data = self.resource_uri_output
        redfish_connection_mock_for_powerstate.root_uri = ROOT_URI
        self.module.fetch_power_uri_resource(f_module, redfish_connection_mock_for_powerstate, "Systems")
        # self.module.fetch_powerstate_details(f_module, redfish_connection_mock_for_powerstate)
        assert self.module.powerstate_map["allowable_enums"] == [
            "On",
            "ForceOff",
            "ForceRestart",
            "GracefulShutdown",
            "PushPowerButton",
            "Nmi",
            "PowerCycle"
        ]
        assert self.module.powerstate_map['power_uri'] == RESET_URI
        assert self.module.powerstate_map['current_state'] == 'On'

    def test_fetch_powerstate_resource_success_case_02(self, mocker, redfish_connection_mock_for_powerstate, redfish_default_args,
                                                       redfish_response_mock):
        """dynamically fetch the computer system id if one member exists in system"""
        f_module = self.get_module_mock(params={"oem_reset_type": {"dell": {"reset_type": "PowerCycle"}}})

        redfish_response_mock.json_data = {
            "Chassis": {
                ODATA_KEY: "/redfish/v1/Chassis"
            },
            "Members": [
                {
                    ODATA_KEY: "/redfish/v1/Chassis/System.Embedded.1"
                }
            ],
            "Actions": {
                "Oem": {
                    "#DellOemChassis.ExtendedReset": {
                        "FinalPowerState@Redfish.AllowableValues": [
                            "On",
                            "Off"
                        ],
                        RESET_ALLOWED_KEY: [
                            "PowerCycle"
                        ],
                        "target": TARGET_URI
                    }
                }
            },
            "PowerState": "Off"
        }
        redfish_connection_mock_for_powerstate.root_uri = ROOT_URI
        self.module.fetch_power_uri_resource(f_module, redfish_connection_mock_for_powerstate, "Chassis")
        # self.module.fetch_powerstate_details(f_module, redfish_connection_mock_for_powerstate)
        assert self.module.powerstate_map["allowable_enums"] == [
            "PowerCycle"
        ]
        assert self.module.powerstate_map['power_uri'] == '/redfish/v1/Chassis/System.Embedded.1/Actions/Oem/DellOemChassis.ExtendedReset'
        assert self.module.powerstate_map['current_state'] == 'Off'

    def test_fetch_powerstate_resource_resource_id_given_success_case(self,
                                                                      redfish_connection_mock_for_powerstate,
                                                                      redfish_response_mock):
        """case when system id is explicitly provided"""
        f_module = self.get_module_mock(params={"resource_id": "System.Embedded.1", "reset_type": "ForceOff"})
        redfish_response_mock.json_data = self.resource_uri_output
        redfish_connection_mock_for_powerstate.root_uri = ROOT_URI
        self.module.fetch_power_uri_resource(f_module, redfish_connection_mock_for_powerstate, "Systems")
        assert self.module.powerstate_map["allowable_enums"] == [
            "On",
            "ForceOff",
            "ForceRestart",
            "GracefulShutdown",
            "PushPowerButton",
            "Nmi",
            "PowerCycle"
        ]
        assert self.module.powerstate_map['power_uri'] == RESET_URI
        assert self.module.powerstate_map['current_state'] == 'On'

    def test_fetch_powerstate_resource_resource_id_not_given_success_case(self,
                                                                          redfish_connection_mock_for_powerstate,
                                                                          redfish_response_mock):
        """case when system id not provided but multipble resource exists"""
        f_module = self.get_module_mock(params={"reset_type": "ForceOff"})
        redfish_response_mock.json_data = self.resource_uri_output
        redfish_connection_mock_for_powerstate.root_uri = ROOT_URI
        self.module.fetch_power_uri_resource(f_module, redfish_connection_mock_for_powerstate, "Systems")
        assert self.module.powerstate_map["allowable_enums"] == [
            "On",
            "ForceOff",
            "ForceRestart",
            "GracefulShutdown",
            "PushPowerButton",
            "Nmi",
            "PowerCycle"
        ]
        assert self.module.powerstate_map['power_uri'] == RESET_URI
        assert self.module.powerstate_map['current_state'] == 'On'

    def test_fetch_powerstate_resource_resource_id_invalid_failure_case(self,
                                                                        redfish_connection_mock_for_powerstate,
                                                                        redfish_response_mock):
        """failure case when system id is explicitly provided but which is not valid"""
        f_module = self.get_module_mock(params={"resource_id": "System.Embedded.3", "reset_type": "ForceOff"})
        redfish_response_mock.json_data = {
            "Systems": {
                ODATA_KEY: RESOURCE_URI
            },
            "Members":
            [
                {
                    ODATA_KEY: SPECIFIC_RESOURCE_URI_ONE
                },
                {
                    ODATA_KEY: SPECIFIC_RESOURCE_URI_TWO
                }
            ],
            "Actions": {
                "#ComputerSystem.Reset": {
                    "target": "/redfish/v1/Systems/System.Embedded.2/Actions/ComputerSystem.Reset",
                    RESET_ALLOWED_KEY: [
                        "On",
                        "ForceOff",
                        "ForceRestart",
                        "GracefulShutdown",
                        "PushPowerButton",
                        "Nmi",
                        "PowerCycle"
                    ]
                }
            },
            "PowerState": "On"
        }
        redfish_connection_mock_for_powerstate.root_uri = ROOT_URI
        with pytest.raises(Exception) as exc:
            self.module.fetch_power_uri_resource(f_module, redfish_connection_mock_for_powerstate, "Systems")
        assert exc.value.args[0] == "Invalid device Id 'System.Embedded.3' is provided"

    def test_fetch_powerstate_resource_error_case_01(self, redfish_connection_mock_for_powerstate,
                                                     redfish_response_mock):
        """failure case when system does not supports redfish computer system in schema"""
        f_module = self.get_module_mock()
        redfish_response_mock.json_data = {
            ODATA_KEY: RESOURCE_URI,
            "Members": [
            ],
        }

        redfish_connection_mock_for_powerstate.root_uri = ROOT_URI
        with pytest.raises(Exception) as exc:
            self.module.fetch_power_uri_resource(f_module, redfish_connection_mock_for_powerstate)
        assert exc.value.args[0] == tarrget_error_msg

    def test_fetch_powerstate_resource_error_case_02(self, redfish_connection_mock_for_powerstate,
                                                     redfish_response_mock):
        """failuere case when system does not supports redfish computer system action in schema"""
        f_module = self.get_module_mock()
        redfish_response_mock.json_data = {
            "Systems": {
                ODATA_KEY: RESOURCE_URI
            },
            "Members": [
                {
                    ODATA_KEY: SPECIFIC_RESOURCE_URI_ONE
                }
            ],
            "Actions": {

            }}
        redfish_connection_mock_for_powerstate.root_uri = ROOT_URI
        with pytest.raises(Exception) as exc:
            self.module.fetch_power_uri_resource(f_module, redfish_connection_mock_for_powerstate)
        assert exc.value.args[0] == tarrget_error_msg

    def test_fetch_powerstate_resource_error_case_03(self, redfish_connection_mock_for_powerstate,
                                                     redfish_response_mock):
        """failuere case when system does not supports and throws http error not found"""
        f_module = self.get_module_mock()
        redfish_connection_mock_for_powerstate.root_uri = ROOT_URI
        redfish_connection_mock_for_powerstate.invoke_request.side_effect = HTTPError(HTTPS_ADDRESS, 404,
                                                                                      json.dumps(tarrget_error_msg), {},
                                                                                      None)
        with pytest.raises(Exception) as exc:
            self.module.fetch_power_uri_resource(f_module, redfish_connection_mock_for_powerstate)

    def test_fetch_powerstate_resource_error_case_04(self, redfish_connection_mock_for_powerstate,
                                                     redfish_response_mock):
        """failure case when system does not supports and throws http error 400 bad request"""
        f_module = self.get_module_mock()
        redfish_connection_mock_for_powerstate.root_uri = ROOT_URI
        redfish_connection_mock_for_powerstate.invoke_request.side_effect = HTTPError(HTTPS_ADDRESS, 400,
                                                                                      tarrget_error_msg,
                                                                                      {}, None)
        with pytest.raises(Exception, match=tarrget_error_msg) as exc:
            self.module.fetch_power_uri_resource(f_module, redfish_connection_mock_for_powerstate)

    def test_fetch_powerstate_resource_error_case_05(self, redfish_connection_mock_for_powerstate,
                                                     redfish_response_mock):
        f_module = self.get_module_mock()
        msg = "connection error"
        redfish_connection_mock_for_powerstate.root_uri = ROOT_URI
        redfish_connection_mock_for_powerstate.invoke_request.side_effect = URLError(msg)
        with pytest.raises(Exception, match=msg) as exc:
            self.module.fetch_power_uri_resource(f_module, redfish_connection_mock_for_powerstate)

    def test_fetch_powerstate_resource_error_case_06(self, redfish_connection_mock_for_powerstate,
                                                     redfish_response_mock):
        """when both system id and mebers of id not provided"""
        f_module = self.get_module_mock()
        redfish_response_mock.json_data = {
            "Systems": {
                ODATA_KEY: RESOURCE_URI
            },
            "Members": [
            ],
            "Actions": {

            }}
        redfish_connection_mock_for_powerstate.root_uri = ROOT_URI
        with pytest.raises(Exception) as exc:
            self.module.fetch_power_uri_resource(f_module, redfish_connection_mock_for_powerstate)
        assert exc.value.args[0] == tarrget_error_msg

    power_vals = [{"apply": "On", "current": "On", "result": False},
                  {"apply": "On", "current": "PoweringOn", "result": False},
                  {"apply": "On", "current": "Off", "result": True},
                  {"apply": "On", "current": "PoweringOff", "result": True},
                  {"apply": "ForceOn", "current": "On", "result": False},
                  {"apply": "ForceOn", "current": "PoweringOn", "result": False},
                  {"apply": "ForceOn", "current": "Off", "result": True},
                  {"apply": "ForceOn", "current": "PoweringOff", "result": True},
                  {"apply": "PushPowerButton", "current": "On", "result": True},
                  {"apply": "PushPowerButton", "current": "PoweringOn", "result": True},
                  {"apply": "PushPowerButton", "current": "Off", "result": True},
                  {"apply": "PushPowerButton", "current": "PoweringOff", "result": True},
                  {"apply": "ForceOff", "current": "On", "result": True},
                  {"apply": "ForceOff", "current": "PoweringOn", "result": True},
                  {"apply": "ForceOff", "current": "Off", "result": False},
                  {"apply": "ForceOff", "current": "PoweringOff", "result": False},
                  {"apply": "ForceRestart", "current": "On", "result": True},
                  {"apply": "ForceRestart", "current": "PoweringOn", "result": True},
                  {"apply": "ForceRestart", "current": "Off", "result": False},
                  {"apply": "ForceRestart", "current": "PoweringOff", "result": False},
                  {"apply": "GracefulRestart", "current": "On", "result": True},
                  {"apply": "GracefulRestart", "current": "PoweringOn", "result": True},
                  {"apply": "GracefulRestart", "current": "Off", "result": False},
                  {"apply": "GracefulRestart", "current": "PoweringOff", "result": False},
                  {"apply": "GracefulShutdown", "current": "On", "result": True},
                  {"apply": "GracefulShutdown", "current": "PoweringOn", "result": True},
                  {"apply": "GracefulShutdown", "current": "Off", "result": False},
                  {"apply": "GracefulShutdown", "current": "PoweringOff", "result": False},
                  {"apply": "Nmi", "current": "On", "result": True},
                  {"apply": "Nmi", "current": "PoweringOn", "result": True},
                  {"apply": "Nmi", "current": "Off", "result": False},
                  {"apply": "Nmi", "current": "PoweringOff", "result": False},
                  {"apply": "PowerCycle", "current": "On", "result": True},
                  {"apply": "PowerCycle", "current": "PoweringOn", "result": True},
                  {"apply": "PowerCycle", "current": "Off", "result": False},
                  {"apply": "PowerCycle", "current": "PoweringOff", "result": False},

                  ]

    @pytest.mark.parametrize("power_map", power_vals)
    def test_is_change_applicable_for_power_state(self, power_map):
        apply_state = power_map["apply"]
        current_state = power_map["current"]
        result = power_map["result"]
        res = self.module.is_change_applicable_for_power_state(current_state, apply_state)
        assert res is result

    def test_is_change_applicable_for_power_state_case_02(self):
        apply_state = "xyz"
        current_state = "On"
        result = False
        res = self.module.is_change_applicable_for_power_state(current_state, apply_state)
        assert res is result

    def test_is_valid_reset_type(self):
        # Scenario: when reset_type is passed and invalid value
        f_module = self.get_module_mock({"reset_type": "ForceOn"})
        reset_type = "GracefulRestart"
        allowable_enum = [
            "On",
            "ForceOff",
            "ForceRestart",
            "GracefulShutdown",
            "PushPowerButton",
            "Nmi",
            "PowerCycle"
        ]
        error_msg = INVALID_RESET_TYPE.format("graceful restart", ", ".join(allowable_enum))
        with pytest.raises(Exception) as exc:
            self.module.is_valid_reset_type(reset_type, allowable_enum, f_module)
        assert exc.value.args[0] == error_msg

        # Scenario: when oem_reset_type is passed and invalid value
        f_module = self.get_module_mock({"oem_reset_type": {"dell": {"reset_type": "GracefulRestart"}}})
        allowable_enum = [
            "PowerCycle"
        ]
        error_msg = INVALID_RESET_TYPE_OEM.format(option=reset_type,
                                                  supported_oem_reset_type_values=", ".join(allowable_enum))
        with pytest.raises(Exception) as exc:
            self.module.is_valid_reset_type(reset_type, allowable_enum, f_module)
        assert exc.value.args[0] == error_msg

    def test_is_valid_reset_type_case2(self):
        f_module = self.get_module_mock({"reset_type": "On"})
        reset_type = "ForceOff"
        allowable_enum = [
            "On",
            "ForceOff",
            "ForceRestart",
            "GracefulShutdown",
            "PushPowerButton",
            "Nmi",
            "PowerCycle"
        ]
        self.module.is_valid_reset_type(reset_type, allowable_enum, f_module)

    @pytest.mark.parametrize("val", [{"change_applicable": True, "check_mode_msg": "Changes found to be applied."},
                                     {"change_applicable": False, "check_mode_msg": "No Changes found to be applied."}])
    def test_run_change_power_state_case_with_checkmode(self, mocker, val):
        change_applicable = val["change_applicable"]
        message = val["check_mode_msg"]
        f_module = self.get_module_mock(params={"reset_type": "On"}, check_mode=True)
        self.module.powerstate_map.update({"allowable_enums": [
            "On",
            "ForceOff",
            "ForceRestart",
            "GracefulShutdown",
            "PushPowerButton",
            "Nmi",
            "PowerCycle"
        ]})
        self.module.powerstate_map.update({'power_uri': '/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem'
                                                        '.Reset'})
        self.module.powerstate_map.update({'current_state': 'On'})

        mocker.patch(MODULE_PATH + FETCH_PWR_URI,
                     return_value=None)
        mocker.patch(MODULE_PATH + VALIDATE_RESET_TYPE,
                     return_value=None)
        mocker.patch(MODULE_PATH + 'redfish_powerstate.is_change_applicable_for_power_state',
                     return_value=change_applicable)

        with pytest.raises(Exception, match=message):
            self.module.run_change_power_state(redfish_connection_mock_for_powerstate, f_module)

    @pytest.mark.parametrize("val", [{"change_applicable": True, "status_code": 204},
                                     {"change_applicable": False, "status_code": 200},
                                     {"change_applicable": True, "status_code": 200}])
    def test_run_change_power_state_case_without_checkmode(self, mocker, val, redfish_connection_mock_for_powerstate,
                                                           redfish_response_mock):
        redfish_response_mock.status_code = val["status_code"]
        change_applicable = val["change_applicable"]
        f_module = self.get_module_mock(params={"reset_type": "On"})
        self.module.powerstate_map.update({"allowable_enums": [
            "On",
            "ForceOff",
            "ForceRestart",
            "GracefulShutdown",
            "PushPowerButton",
            "Nmi",
            "PowerCycle"
        ]})
        self.module.powerstate_map.update({'power_uri': '/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem'
                                                        '.Reset'})
        self.module.powerstate_map.update({'current_state': 'On'})
        if change_applicable is True:
            if val["status_code"] == 204:
                redfish_response_mock.success = True
                message = "Successfully performed the reset type operation 'On'."
            else:
                redfish_response_mock.success = False
                message = "Unable to perform the reset type operation 'On'."
        else:
            message = "The device is already powered on."
        mocker.patch(MODULE_PATH + FETCH_PWR_URI,
                     return_value=None)
        mocker.patch(MODULE_PATH + VALIDATE_RESET_TYPE,
                     return_value=None)
        mocker.patch(MODULE_PATH + 'redfish_powerstate.is_change_applicable_for_power_state',
                     return_value=change_applicable)

        with pytest.raises(Exception, match=message):
            self.module.run_change_power_state(redfish_connection_mock_for_powerstate, f_module)

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError,
                              Exception])
    def test_main_redfish_powerstate_exception_handling_case(self, exc_type, redfish_default_args,
                                                             redfish_connection_mock_for_powerstate,
                                                             redfish_response_mock, mocker):
        redfish_default_args.update({"reset_type": "On"})
        redfish_response_mock.status_code = 400
        redfish_response_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'redfish_powerstate.run_change_power_state',
                         side_effect=exc_type("url open error"))
            result = self._run_module(redfish_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'redfish_powerstate.run_change_power_state',
                         side_effect=exc_type("exception message"))
            result = self._run_module(redfish_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'redfish_powerstate.run_change_power_state',
                         side_effect=exc_type(HTTPS_ADDRESS, 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module(redfish_default_args)
            assert result['failed'] is True
        assert 'msg' in result

    def test_run_change_ac_power_cycle(self, redfish_default_args, redfish_connection_mock_for_powerstate, mocker):
        # Scenario - When firmware version is not supported
        obj1 = MagicMock()
        obj1.json_data = {"FirmwareVersion": "6.10.00"}
        redfish_default_args.update({"oem_reset_type": {"dell": {"reset_type": "PowerCycle"}}})
        redfish_connection_mock_for_powerstate.invoke_request.return_value = obj1
        f_module = self.get_module_mock(params=redfish_default_args)
        with pytest.raises(Exception) as exc:
            self.module.run_change_ac_power_cycle(redfish_connection_mock_for_powerstate, f_module)
        assert exc.value.args[0] == "Unable to perform the Virtual AC power-cycle operation because the firmware version is not supported." \
            " The minimum supported firmware version is '7.00.60'."

        # Scenario - When vendor provided but not valid
        obj1.json_data = {"Vendor": "Dell"}
        redfish_default_args.update({})
        redfish_default_args.update({"oem_reset_type": {"Invalid": {}}})
        f_module = self.get_module_mock(params=redfish_default_args)
        redfish_connection_mock_for_powerstate.invoke_request.return_value = obj1
        mocker.patch(MODULE_PATH + CHECK_FIRMWARE_VERSION, return_value=None)
        with pytest.raises(Exception) as exc:
            self.module.run_change_ac_power_cycle(redfish_connection_mock_for_powerstate, f_module)
        assert exc.value.args[0] == "The vendor is not supported. The supported vendors" \
            " are 'Dell'. Enter the valid vendor and retry the operation."

        # Scenario - When operation is not defined
        redfish_default_args.update({})
        redfish_default_args.update({"oem_reset_type": {"Dell": {"final_power_state": "Off"}}})
        f_module = self.get_module_mock(params=redfish_default_args)
        mocker.patch(MODULE_PATH + CHECK_FIRMWARE_VERSION, return_value=None)
        mocker.patch(MODULE_PATH + VALIDATE_VENDOR, return_value=None)
        with pytest.raises(Exception) as exc:
            self.module.run_change_ac_power_cycle(redfish_connection_mock_for_powerstate, f_module)
        assert exc.value.args[0] == "No reset type is specified for the target device. Enter the valid value and retry the operation."

        # Scenario - When final_power_state is invalid
        redfish_default_args.update({})
        self.module.powerstate_map["allowable_enums"] = ["PowerCycle"]
        self.module.powerstate_map["power_uri"] = TARGET_URI
        self.module.powerstate_map["current_state"] = "Off"
        self.module.powerstate_map["allowable_power_state"] = ["On", "Off"]
        redfish_default_args.update({"oem_reset_type": {"Dell": {"final_power_state": "Invalid", "reset_type": "PowerCycle"}}})
        f_module = self.get_module_mock(params=redfish_default_args)
        mocker.patch(MODULE_PATH + CHECK_FIRMWARE_VERSION, return_value=None)
        mocker.patch(MODULE_PATH + VALIDATE_VENDOR, return_value=None)
        mocker.patch(MODULE_PATH + FETCH_PWR_URI, return_value=None)
        with pytest.raises(Exception) as exc:
            self.module.run_change_ac_power_cycle(redfish_connection_mock_for_powerstate, f_module)
        assert exc.value.args[0] == "The target device does not support 'Invalid' operation. The valid values of final power states for device are 'On, Off'."

    def setup_mocker(self, mocker):
        mocker.patch(MODULE_PATH + CHECK_FIRMWARE_VERSION, return_value=None)
        mocker.patch(MODULE_PATH + VALIDATE_VENDOR, return_value=None)
        mocker.patch(MODULE_PATH + VALIDATE_RESET_TYPE, return_value=None)
        mocker.patch(MODULE_PATH + VALIDATE_FINAL_PWR_STATE, return_value=None)
        mocker.patch(MODULE_PATH + FETCH_PWR_URI, return_value=None)

    def test_run_change_ac_power_cycle_case02(self, redfish_default_args, redfish_connection_mock_for_powerstate, mocker):
        # Scenario - Check Mode when server is powered off
        redfish_default_args.update({})
        self.module.powerstate_map["allowable_enums"] = ["PowerCycle"]
        self.module.powerstate_map["power_uri"] = TARGET_URI
        self.module.powerstate_map["current_state"] = "Off"
        self.module.powerstate_map["allowable_power_state"] = ["On", "Off"]
        redfish_default_args.update({"oem_reset_type": {"Dell": {"final_power_state": "On", "reset_type": "PowerCycle"}}})
        f_module = self.get_module_mock(params=redfish_default_args, check_mode=True)
        self.setup_mocker(mocker)
        with pytest.raises(Exception) as exc:
            self.module.run_change_ac_power_cycle(redfish_connection_mock_for_powerstate, f_module)
        assert exc.value.args[0] == "Changes found to be applied."

        # Scenario - Check Mode when server is powered On
        self.module.powerstate_map["current_state"] = "On"
        f_module = self.get_module_mock(params=redfish_default_args, check_mode=True)
        self.setup_mocker(mocker)
        with pytest.raises(Exception) as exc:
            self.module.run_change_ac_power_cycle(redfish_connection_mock_for_powerstate, f_module)
        assert exc.value.args[0] == "No changes found to be applied because system is in power ON state."

        # Scenario - Success case when currently server is powered off and final power state is On
        redfish_default_args.update({})
        obj = MagicMock()
        obj.status_code = 204
        self.module.powerstate_map["current_state"] = "Off"
        redfish_default_args.update({"oem_reset_type": {"Dell": {"final_power_state": "On", "reset_type": "PowerCycle"}}})
        f_module = self.get_module_mock(params=redfish_default_args)
        redfish_connection_mock_for_powerstate.invoke_request.return_value = obj
        self.setup_mocker(mocker)
        with pytest.raises(Exception) as exc:
            self.module.run_change_ac_power_cycle(redfish_connection_mock_for_powerstate, f_module)
        assert exc.value.args[0] == "Successfully performed the full virtual server AC power-cycle operation."\
            " Please wait a few minutes, the server will automatically power on."

        # Scenario - Success case when currently server is powered off and final power state is off which is a default value
        redfish_default_args.update({})
        obj = MagicMock()
        obj.status_code = 204
        self.module.powerstate_map["current_state"] = "Off"
        redfish_default_args.update({"oem_reset_type": {"Dell": {"reset_type": "PowerCycle"}}})
        f_module = self.get_module_mock(params=redfish_default_args)
        redfish_connection_mock_for_powerstate.invoke_request.return_value = obj
        self.setup_mocker(mocker)
        with pytest.raises(Exception) as exc:
            self.module.run_change_ac_power_cycle(redfish_connection_mock_for_powerstate, f_module)
        assert exc.value.args[0] == "Successfully performed the full virtual server AC power-cycle operation."

        # Scenario - Idrac gives error when system in in power ON state
        redfish_default_args.update({})
        obj = MagicMock()
        obj.status_code = 409
        obj_str = {
            "error":
                {
                    "@Message.ExtendedInfo": [
                        {
                            "Message": "Unable to perform the Virtual AC power-cycle operation because the server is powered on.",
                            "MessageId": "IDRAC.2.9.PSU507",
                        }
                    ],
                }
        }
        json_str = to_text(json.dumps(obj_str))
        self.module.powerstate_map["current_state"] = "Off"
        redfish_default_args.update({"oem_reset_type": {"Dell": {"reset_type": "PowerCycle"}}})
        f_module = self.get_module_mock(params=redfish_default_args)
        redfish_connection_mock_for_powerstate.invoke_request.side_effect = HTTPError("https://test.com",
                                                                                      409, "obj", {"accept-type": "application/json"},
                                                                                      StringIO(json_str))
        self.setup_mocker(mocker)
        with pytest.raises(Exception) as exc:
            self.module.run_change_ac_power_cycle(redfish_connection_mock_for_powerstate, f_module)
        assert exc.value.args[0] == "Unable to perform the Virtual AC power-cycle operation because the server is powered on."
