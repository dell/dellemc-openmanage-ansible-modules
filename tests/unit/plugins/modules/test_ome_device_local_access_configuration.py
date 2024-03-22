# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.1.0
# Copyright (C) 2022-2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
from io import StringIO
from ssl import SSLError

import pytest
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import ome_device_local_access_configuration
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_device_local_access_configuration.'

CONFIG_FAIL_MSG = "one of the following is required: enable_kvm_access, enable_chassis_direct_access, " \
                  "chassis_power_button, quick_sync, lcd"
DOMAIN_FAIL_MSG = "The operation to configure the local access is supported only on " \
                  "OpenManage Enterprise Modular."
FETCH_FAIL_MSG = "Unable to retrieve the device information."
DEVICE_FAIL_MSG = "Unable to complete the operation because the entered target device {0} '{1}' is invalid."
LAC_FAIL_MSG = "Unable to complete the operation because the local access configuration settings " \
               "are not supported on the specified device."
CHANGES_FOUND = "Changes found to be applied."
NO_CHANGES_FOUND = "No changes found to be applied."
SUCCESS_MSG = "Successfully updated the local access settings."
HTTPS_ADDRESS = 'https://testhost.com'
HTTP_ERROR_MSG = 'http error message'


@pytest.fixture
def ome_conn_mock_lac(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOMEMDevicePower(FakeAnsibleModule):
    module = ome_device_local_access_configuration

    @pytest.mark.parametrize("params", [
        {"json_data": {"value": [
            {'Id': 1234, 'PublicAddress': "XX.XX.XX.XX",
             'DeviceServiceTag': 'ABCD123', "Type": 1000},
            {'PublicAddress': "YY.YY.YY.YY", 'DeviceId': 1235, "Type": 1000}],
            "SettingType": "LocalAccessConfiguration", "EnableChassisDirect": False,
            "EnableChassisPowerButton": False, "EnableKvmAccess": True, "EnableLcdOverridePin": False,
            "LcdAccess": "VIEW_ONLY", "LcdCustomString": "LCD Text", "LcdLanguage": "en",
            "LcdPresence": "Present", "LcdPinLength": 6, "LedPresence": "Absent", "LcdOverridePin": "123456",
            "QuickSync": {"QuickSyncAccess": True, "TimeoutLimit": 10, "EnableInactivityTimeout": True,
                          "TimeoutLimitUnit": "MINUTES", "EnableReadAuthentication": True,
                          "EnableQuickSyncWifi": True, "QuickSyncHardware": "Present"}},
            'message': "Successfully updated the local access settings.",
            'mparams': {"hostname": "XX.XX.XX.XX",
                        "device_service_tag": 'ABCD123',
                        'enable_kvm_access': True, 'enable_chassis_direct_access': False,
                        'chassis_power_button':
                            {'enable_chassis_power_button': False, 'enable_lcd_override_pin': True,
                             'disabled_button_lcd_override_pin': "123456"
                             },
                        'lcd':
                            {'lcd_access': 'VIEW_AND_MODIFY',
                             'user_defined': 'LCD Text', 'lcd_language': 'en'},
                        'quick_sync': {'enable_quick_sync_wifi': True, 'enable_inactivity_timeout': True,
                                       'timeout_limit': 10, 'timeout_limit_unit': 'MINUTES',
                                       'enable_read_authentication': True,
                                       'quick_sync_access': 'READ_WRITE'}
                        }},
        {"json_data": {"value": [
            {'Id': 1234, 'PublicAddress': "dummyhostname_shouldnotexist",
             'DeviceId': 1234, "Type": 1000},
            {'PublicAddress': "YY.YY.YY.YY", 'DeviceId': 1235, "Type": 1000}],
            "SettingType": "LocalAccessConfiguration", "EnableChassisDirect": False,
            "EnableChassisPowerButton": False, "EnableKvmAccess": True, "EnableLcdOverridePin": False,
            "LcdAccess": "VIEW_ONLY", "LcdCustomString": "LCD Text", "LcdLanguage": "en",
            "LcdPresence": "Present", "LcdPinLength": 6, "LedPresence": "Absent", "LcdOverridePin": "123456",
            "QuickSync": {"QuickSyncAccess": True, "TimeoutLimit": 10, "EnableInactivityTimeout": True,
                          "TimeoutLimitUnit": "MINUTES", "EnableReadAuthentication": True,
                          "EnableQuickSyncWifi": True, "QuickSyncHardware": "Present"}},
            'message': "Successfully updated the local access settings.",
            'mparams': {"hostname": "dummyhostname_shouldnotexist",
                        'enable_kvm_access': True, 'enable_chassis_direct_access': False,
                        'chassis_power_button':
                            {'enable_chassis_power_button': False, 'enable_lcd_override_pin': True,
                             'disabled_button_lcd_override_pin': "123456"
                             },
                        'lcd':
                            {'lcd_access': 'VIEW_AND_MODIFY',
                             'user_defined': 'LCD Text', 'lcd_language': 'en'},
                        'quick_sync': {'enable_quick_sync_wifi': True, 'enable_inactivity_timeout': True,
                                       'timeout_limit': 10, 'timeout_limit_unit': 'MINUTES',
                                       'enable_read_authentication': True,
                                       'quick_sync_access': 'READ_WRITE'}
                        }}
    ])
    def test_ome_devices_lac_success(self, params, ome_conn_mock_lac, ome_response_mock,
                                     ome_default_args, module_mock, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['json_data']
        ome_default_args.update(params['mparams'])
        result = self._run_module(
            ome_default_args, check_mode=params.get('check_mode', False))
        assert result['msg'] == params['message']

    @pytest.mark.parametrize("params", [
        {"json_data": {"value": [
            {'Id': 1234, 'PublicAddress': "XX.XX.XX.XX",
             'DeviceId': 1234, "Type": 1000},
            {'PublicAddress': "YY.YY.YY.YY", 'DeviceId': 1235, "Type": 1000}]},
            'message': DOMAIN_FAIL_MSG,
            'http_error_json': {
                "error": {
                    "code": "Base.1.0.GeneralError",
                    "message": "A general error has occurred. See ExtendedInfo for more information.",
                    "@Message.ExtendedInfo": [
                        {
                            "MessageId": "CGEN1006",
                            "RelatedProperties": [],
                            "Message": "Unable to process the request because an error occurred.",
                            "MessageArgs": [],
                            "Severity": "Critical",
                            "Resolution": "Retry the operation. If the issue persists, contact your system administrator."
                        }
                    ]
                }},
            'mparams': {"hostname": "XX.XX.XX.XX",
                        "device_service_tag": 'ABCD123',
                        'enable_kvm_access': True, 'enable_chassis_direct_access': False,
                        'chassis_power_button':
                            {'enable_chassis_power_button': False, 'enable_lcd_override_pin': True,
                             'disabled_button_lcd_override_pin': "123456"
                             },
                        'lcd':
                            {'lcd_access': 'VIEW_AND_MODIFY',
                             'user_defined': 'LCD Text', 'lcd_language': 'en'},
                        'quick_sync': {'enable_quick_sync_wifi': True, 'enable_inactivity_timeout': True,
                                       'timeout_limit': 10, 'timeout_limit_unit': 'MINUTES',
                                       'enable_read_authentication': True,
                                       'quick_sync_access': 'READ_WRITE'}
                        }},
        {"json_data": {"value": [
            {'Id': 1234, 'PublicAddress': "XX.XX.XX.XX",
             'DeviceId': 1234, "Type": 1000},
            {'PublicAddress': "YY.YY.YY.YY", 'DeviceId': 1235, "Type": 1000}]},
            'message': LAC_FAIL_MSG,
            'http_error_json': {
                "error": {
                    "code": "Base.1.0.GeneralError",
                    "message": "A general error has occurred. See ExtendedInfo for more information.",
                    "@Message.ExtendedInfo": [
                        {
                            "MessageId": "CGEN1004",
                            "RelatedProperties": [],
                            "Message": "Unable to process the request because an error occurred.",
                            "MessageArgs": [],
                            "Severity": "Critical",
                            "Resolution": "Retry the operation. If the issue persists, contact your system administrator."
                        }
                    ]
                }},
            'check_domain_service': 'mocked_check_domain_service',
            'get_chassis_device': ('Id', 1234),
            'mparams': {"hostname": "XX.XX.XX.XX",
                        'enable_kvm_access': True, 'enable_chassis_direct_access': False,
                        'chassis_power_button':
                            {'enable_chassis_power_button': False, 'enable_lcd_override_pin': True,
                             'disabled_button_lcd_override_pin': "123456"
                             },
                        'lcd':
                            {'lcd_access': 'VIEW_AND_MODIFY',
                             'user_defined': 'LCD Text', 'lcd_language': 'en'},
                        'quick_sync': {'enable_quick_sync_wifi': True, 'enable_inactivity_timeout': True,
                                       'timeout_limit': 10, 'timeout_limit_unit': 'MINUTES',
                                       'enable_read_authentication': True,
                                       'quick_sync_access': 'READ_WRITE'}
                        }},
        {"json_data": {"value": [
            {'Id': 1234, 'PublicAddress': "XX.XX.XX.XX",
             'DeviceId': 1234, "Type": 1000},
            {'PublicAddress': "YY.YY.YY.YY", 'DeviceId': 1235, "Type": 1000}]},
            'message': "Unable to complete the operation because the entered target device id '123' is invalid.",
            'mparams': {"hostname": "XX.XX.XX.XX", "device_id": 123,
                        'enable_kvm_access': True, 'enable_chassis_direct_access': False,
                        'chassis_power_button':
                            {'enable_chassis_power_button': False, 'enable_lcd_override_pin': True,
                             'disabled_button_lcd_override_pin': "123456"
                             },
                        'lcd':
                            {'lcd_access': 'VIEW_AND_MODIFY',
                             'user_defined': 'LCD Text', 'lcd_language': 'en'},
                        'quick_sync': {'enable_quick_sync_wifi': True, 'enable_inactivity_timeout': True,
                                       'timeout_limit': 10, 'timeout_limit_unit': 'MINUTES',
                                       'enable_read_authentication': True,
                                       'quick_sync_access': 'READ_WRITE'}
                        }},
        {"json_data": {"value": [
            {'Id': 1234, 'PublicAddress': "XX.XX.XX.XX",
             'DeviceId': 1234, "Type": 1000},
            {'PublicAddress': "YY.YY.YY.YY", 'DeviceId': 1235, "Type": 1000}]},
            'message': CONFIG_FAIL_MSG,
            'mparams': {"hostname": "XX.XX.XX.XX", "device_id": 123}}
    ])
    def test_ome_devices_lac_failure(self, params, ome_conn_mock_lac, ome_response_mock,
                                     ome_default_args, module_mock, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['json_data']
        mocks = ["check_domain_service", 'get_chassis_device']
        for m in mocks:
            if m in params:
                mocker.patch(MODULE_PATH + m, return_value=params.get(m, {}))
        if 'http_error_json' in params:
            json_str = to_text(json.dumps(params.get('http_error_json', {})))
            ome_conn_mock_lac.invoke_request.side_effect = HTTPError(
                HTTPS_ADDRESS, 401, HTTP_ERROR_MSG, {
                    "accept-type": "application/json"},
                StringIO(json_str))
        ome_default_args.update(params['mparams'])
        result = self._run_module_with_fail_json(ome_default_args)
        assert result['msg'] == params['message']

    def test_check_domain_service(self, ome_conn_mock_lac, ome_default_args):
        f_module = self.get_module_mock()
        result = self.module.check_domain_service(f_module, ome_conn_mock_lac)
        assert result is None

    def test_get_chassis_device(self, ome_conn_mock_lac, ome_default_args, mocker, ome_response_mock):
        mocker.patch(MODULE_PATH + "get_ip_from_host",
                     return_value="X.X.X.X")
        ome_response_mock.json_data = {"value": [{"DeviceId": 25011, "DomainRoleTypeValue": "LEAD",
                                                  "PublicAddress": ["XX.XX.XX.XX"]},
                                                 {"DeviceId": 25012, "DomainRoleTypeValue": "STANDALONE",
                                                  "PublicAddress": ["YY.YY.YY.YY"]}]}
        param = {"device_id": 25012, "hostname": "XX.XX.XX.XX",
                 "enable_kvm_access": True}
        f_module = self.get_module_mock(params=param)
        with pytest.raises(Exception) as err:
            self.module.get_chassis_device(f_module, ome_conn_mock_lac)
        assert err.value.args[0] == "Unable to retrieve the device information."

    def test_get_ip_from_host(self, ome_conn_mock_lac, ome_default_args, ome_response_mock):
        result = self.module.get_ip_from_host("XX.XX.XX.XX")
        assert result == "XX.XX.XX.XX"

    def test_get_device_details(self, ome_conn_mock_lac, ome_default_args, ome_response_mock, mocker):
        param = {"device_id": 25012, "hostname": "XX.XX.XX.XX",
                 "enable_kvm_access": True}
        f_module = self.get_module_mock(params=param)
        ome_response_mock.status_code = 200
        ome_response_mock.success = True
        ome_response_mock.json_data = {
            "value": [], "SettingType": "LocalAccessConfiguration", "EnableChassisDirect": False,
            "EnableChassisPowerButton": False, "EnableKvmAccess": True, "EnableLcdOverridePin": False,
            "LcdAccess": "VIEW_ONLY", "LcdCustomString": "LCD Text", "LcdLanguage": "en", }
        with pytest.raises(Exception) as err:
            self.module.get_device_details(ome_conn_mock_lac, f_module)
        assert err.value.args[0] == "Unable to complete the operation because the entered target " \
                                    "device id '25012' is invalid."
        param = {"device_id": 25012, "hostname": "XX.XX.XX.XX",
                 "enable_kvm_access": True}
        f_module = self.get_module_mock(params=param)
        ome_response_mock.json_data = {"value": [
            {"Id": 25012, "DeviceServiceTag": "GHRT2RL"}], "EnableKvmAccess": True}
        mocker.patch(MODULE_PATH + 'check_mode_validation',
                     return_value={"EnableKvmAccess": True})
        resp = self.module.get_device_details(ome_conn_mock_lac, f_module)
        assert resp.json_data["EnableKvmAccess"] is True
        param = {"hostname": "XX.XX.XX.XX", "enable_kvm_access": True}
        f_module = self.get_module_mock(params=param)
        mocker.patch(MODULE_PATH + 'get_chassis_device',
                     return_value=("Id", 25011))
        resp = self.module.get_device_details(ome_conn_mock_lac, f_module)
        assert resp.json_data["EnableKvmAccess"] is True

    def test_check_mode_validation(self, ome_conn_mock_lac, ome_default_args, ome_response_mock, mocker):
        loc_data = {"EnableKvmAccess": True, "EnableChassisDirect": True, "EnableChassisPowerButton": True,
                    "EnableLcdOverridePin": True, "LcdAccess": True, "LcdCustomString": "LCD Text",
                    "LcdLanguage": "en", "LcdPresence": "Present", "LcdPinLength": 6, "LedPresence": "Absent", "LcdOverridePin": "123456",
                    "QuickSync": {"QuickSyncAccess": True, "TimeoutLimit": 10, "EnableInactivityTimeout": True,
                                  "TimeoutLimitUnit": "MINUTES", "EnableReadAuthentication": True,
                                  "EnableQuickSyncWifi": True, "QuickSyncHardware": "Present"}, }
        param = {"device_id": 25012, "hostname": "XX.XX.XX.XX",
                 "enable_kvm_access": True}
        f_module = self.get_module_mock(params=param)
        with pytest.raises(Exception) as err:
            self.module.check_mode_validation(f_module, loc_data)
        assert err.value.args[0] == "No changes found to be applied."
        f_module.check_mode = True
        with pytest.raises(Exception) as err:
            self.module.check_mode_validation(f_module, loc_data)
        assert err.value.args[0] == "No changes found to be applied."
        param = {"device_id": 25012, "hostname": "XX.XX.XX.XX",
                 "enable_kvm_access": False}
        f_module = self.get_module_mock(params=param)
        f_module.check_mode = True
        with pytest.raises(Exception) as err:
            self.module.check_mode_validation(f_module, loc_data)
        assert err.value.args[0] == "Changes found to be applied."
        f_module.check_mode = False
        result = self.module.check_mode_validation(f_module, loc_data)
        assert result["EnableKvmAccess"] is False

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_device_power_main_exception_case(self, exc_type, mocker, ome_default_args,
                                                  ome_conn_mock_lac, ome_response_mock):
        ome_default_args.update(
            {"device_id": 25011, "enable_kvm_access": True})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'check_domain_service',
                         side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'check_domain_service',
                         side_effect=exc_type("exception message"))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'check_domain_service',
                         side_effect=exc_type(HTTPS_ADDRESS, 400, HTTP_ERROR_MSG,
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result
