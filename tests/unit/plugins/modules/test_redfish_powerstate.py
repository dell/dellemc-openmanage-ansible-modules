# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.3
# Copyright (C) 2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import redfish_powerstate
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text

tarrget_error_msg = "The target device does not support the system reset" \
                    " feature using Redfish API."
MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


@pytest.fixture
def redfish_connection_mock_for_powerstate(mocker, redfish_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'redfish_powerstate.Redfish')
    redfish_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    redfish_connection_mock_obj.invoke_request.return_value = redfish_response_mock
    return redfish_connection_mock_obj


class TestRedfishPowerstate(FakeAnsibleModule):
    module = redfish_powerstate

    def test_fetch_powerstate_resource_success_case_01(self, redfish_connection_mock_for_powerstate,
                                                       redfish_response_mock):
        """dynamically fetch the computer system id if one member exists in system"""
        f_module = self.get_module_mock()
        redfish_response_mock.json_data = {
            "Systems": {
                "@odata.id": "/redfish/v1/Systems"
            },
            "Members": [
                {
                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1"
                }
            ],
            "Actions": {
                "#ComputerSystem.Reset": {
                    "target": "/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset",
                    "ResetType@Redfish.AllowableValues": [
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
        redfish_connection_mock_for_powerstate.root_uri = "/redfish/v1/"
        self.module.fetch_power_uri_resource(f_module, redfish_connection_mock_for_powerstate)
        assert self.module.powerstate_map["allowable_enums"] == [
            "On",
            "ForceOff",
            "ForceRestart",
            "GracefulShutdown",
            "PushPowerButton",
            "Nmi",
            "PowerCycle"
        ]
        assert self.module.powerstate_map['power_uri'] == '/redfish/v1/Systems/System.Embedded.1/Actions' \
                                                          '/ComputerSystem.Reset'
        assert self.module.powerstate_map['current_state'] == 'On'

    def test_fetch_powerstate_resource_resource_id_given_success_case(self,
                                                                      redfish_connection_mock_for_powerstate,
                                                                      redfish_response_mock):
        """case when system id is explicitly provided"""
        f_module = self.get_module_mock(params={"resource_id": "System.Embedded.2"})
        redfish_response_mock.json_data = {
            "Systems": {
                "@odata.id": "/redfish/v1/Systems"
            },
            "Members": [
                {
                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1"
                },
                {
                    "@odata.id": "/redfish/v1/Systems/System.Embedded.2"
                }
            ],
            "Actions": {
                "#ComputerSystem.Reset": {
                    "target": "/redfish/v1/Systems/System.Embedded.2/Actions/ComputerSystem.Reset",
                    "ResetType@Redfish.AllowableValues": [
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
        redfish_connection_mock_for_powerstate.root_uri = "/redfish/v1/"
        self.module.fetch_power_uri_resource(f_module, redfish_connection_mock_for_powerstate)
        assert self.module.powerstate_map["allowable_enums"] == [
            "On",
            "ForceOff",
            "ForceRestart",
            "GracefulShutdown",
            "PushPowerButton",
            "Nmi",
            "PowerCycle"
        ]
        assert self.module.powerstate_map['power_uri'] == '/redfish/v1/Systems/System.Embedded.2/Actions' \
                                                          '/ComputerSystem.Reset'
        assert self.module.powerstate_map['current_state'] == 'On'

    def test_fetch_powerstate_resource_resource_id_not_given_failure_case(self,
                                                                          redfish_connection_mock_for_powerstate,
                                                                          redfish_response_mock):
        """case when system id not provided but multipble resource exists"""
        f_module = self.get_module_mock()
        redfish_response_mock.json_data = {
            "Systems": {
                "@odata.id": "/redfish/v1/Systems"
            },
            "Members": [
                {
                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1"
                },
                {
                    "@odata.id": "/redfish/v1/Systems/System.Embedded.2"
                }
            ],
            "Actions": {
                "#ComputerSystem.Reset": {
                    "target": "/redfish/v1/Systems/System.Embedded.2/Actions/ComputerSystem.Reset",
                    "ResetType@Redfish.AllowableValues": [
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
        redfish_connection_mock_for_powerstate.root_uri = "/redfish/v1/"
        with pytest.raises(Exception) as exc:
            self.module.fetch_power_uri_resource(f_module, redfish_connection_mock_for_powerstate)
        assert exc.value.args[0] == "Multiple devices exists in the system, but option 'resource_id' is not specified."

    def test_fetch_powerstate_resource_resource_id_invalid_failure_case(self,
                                                                        redfish_connection_mock_for_powerstate,
                                                                        redfish_response_mock):
        """failure case when system id is explicitly provided but which is not valid"""
        f_module = self.get_module_mock(params={"resource_id": "System.Embedded.3"})
        redfish_response_mock.json_data = {
            "Systems": {
                "@odata.id": "/redfish/v1/Systems"
            },
            "Members":
            [
                {
                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1"
                },
                {
                    "@odata.id": "/redfish/v1/Systems/System.Embedded.2"
                }
            ],
            "Actions": {
                "#ComputerSystem.Reset": {
                    "target": "/redfish/v1/Systems/System.Embedded.2/Actions/ComputerSystem.Reset",
                    "ResetType@Redfish.AllowableValues": [
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
        redfish_connection_mock_for_powerstate.root_uri = "/redfish/v1/"
        with pytest.raises(Exception) as exc:
            self.module.fetch_power_uri_resource(f_module, redfish_connection_mock_for_powerstate)
        assert exc.value.args[0] == "Invalid device Id 'System.Embedded.3' is provided"

    def test_fetch_powerstate_resource_error_case_01(self, redfish_connection_mock_for_powerstate,
                                                     redfish_response_mock):
        """failure case when system does not supports redfish computer system in schema"""
        f_module = self.get_module_mock()
        redfish_response_mock.json_data = {
            "@odata.id": "/redfish/v1/Systems",
            "Members": [
            ],
        }

        redfish_connection_mock_for_powerstate.root_uri = "/redfish/v1/"
        with pytest.raises(Exception) as exc:
            self.module.fetch_power_uri_resource(f_module, redfish_connection_mock_for_powerstate)
        assert exc.value.args[0] == tarrget_error_msg

    def test_fetch_powerstate_resource_error_case_02(self, redfish_connection_mock_for_powerstate,
                                                     redfish_response_mock):
        """failuere case when system does not supports redfish computer system action in schema"""
        f_module = self.get_module_mock()
        redfish_response_mock.json_data = {
            "Systems": {
                "@odata.id": "/redfish/v1/Systems"
            },
            "Members": [
                {
                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1"
                }
            ],
            "Actions": {

            }}
        redfish_connection_mock_for_powerstate.root_uri = "/redfish/v1/"
        with pytest.raises(Exception) as exc:
            self.module.fetch_power_uri_resource(f_module, redfish_connection_mock_for_powerstate)
        assert exc.value.args[0] == tarrget_error_msg

    def test_fetch_powerstate_resource_error_case_03(self, redfish_connection_mock_for_powerstate,
                                                     redfish_response_mock):
        """failuere case when system does not supports and throws http error not found"""
        f_module = self.get_module_mock()
        redfish_connection_mock_for_powerstate.root_uri = "/redfish/v1/"
        redfish_connection_mock_for_powerstate.invoke_request.side_effect = HTTPError('http://testhost.com', 404,
                                                                                      json.dumps(tarrget_error_msg), {},
                                                                                      None)
        with pytest.raises(Exception) as exc:
            self.module.fetch_power_uri_resource(f_module, redfish_connection_mock_for_powerstate)

    def test_fetch_powerstate_resource_error_case_04(self, redfish_connection_mock_for_powerstate,
                                                     redfish_response_mock):
        """failuere case when system does not supports and throws http error 400 bad request"""
        f_module = self.get_module_mock()
        redfish_connection_mock_for_powerstate.root_uri = "/redfish/v1/"
        redfish_connection_mock_for_powerstate.invoke_request.side_effect = HTTPError('http://testhost.com', 400,
                                                                                      tarrget_error_msg,
                                                                                      {}, None)
        with pytest.raises(Exception, match=tarrget_error_msg) as exc:
            self.module.fetch_power_uri_resource(f_module, redfish_connection_mock_for_powerstate)

    def test_fetch_powerstate_resource_error_case_05(self, redfish_connection_mock_for_powerstate,
                                                     redfish_response_mock):
        f_module = self.get_module_mock()
        msg = "connection error"
        redfish_connection_mock_for_powerstate.root_uri = "/redfish/v1/"
        redfish_connection_mock_for_powerstate.invoke_request.side_effect = URLError(msg)
        with pytest.raises(Exception, match=msg) as exc:
            self.module.fetch_power_uri_resource(f_module, redfish_connection_mock_for_powerstate)

    def test_fetch_powerstate_resource_error_case_06(self, redfish_connection_mock_for_powerstate,
                                                     redfish_response_mock):
        """when both system id and mebers of id not provided"""
        f_module = self.get_module_mock()
        redfish_response_mock.json_data = {
            "Systems": {
                "@odata.id": "/redfish/v1/Systems"
            },
            "Members": [
            ],
            "Actions": {

            }}
        redfish_connection_mock_for_powerstate.root_uri = "/redfish/v1/"
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
        f_module = self.get_module_mock()
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
        error_msg = "The target device does not support a" \
                    " graceful restart operation.The acceptable values for device reset types" \
                    " are {0}.".format(", ".join(allowable_enum))
        with pytest.raises(Exception) as exc:
            self.module.is_valid_reset_type(reset_type, allowable_enum, f_module)
        assert exc.value.args[0] == error_msg

    def test_is_valid_reset_type_case2(self):
        f_module = self.get_module_mock()
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

        mocker.patch(MODULE_PATH + 'redfish_powerstate.fetch_power_uri_resource',
                     return_value=None)
        mocker.patch(MODULE_PATH + 'redfish_powerstate.is_valid_reset_type',
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
        mocker.patch(MODULE_PATH + 'redfish_powerstate.fetch_power_uri_resource',
                     return_value=None)
        mocker.patch(MODULE_PATH + 'redfish_powerstate.is_valid_reset_type',
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
            result = self._run_module_with_fail_json(redfish_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'redfish_powerstate.run_change_power_state',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(redfish_default_args)
            assert result['failed'] is True
        assert 'msg' in result
