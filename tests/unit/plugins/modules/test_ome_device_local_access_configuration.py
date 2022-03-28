# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.2.0
# Copyright (C) 2021-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
import pytest
from ssl import SSLError
from io import StringIO
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils._text import to_text
from ansible_collections.dellemc.openmanage.plugins.modules import ome_device_local_access_configuration
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from mock import MagicMock, patch, Mock

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_device_local_access_configuration.'


@pytest.fixture
def ome_conn_mock_lac(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOMEMDevicePower(FakeAnsibleModule):

    module = ome_device_local_access_configuration

    def test_check_domain_service(self, ome_conn_mock_lac, ome_default_args):
        f_module = self.get_module_mock()
        result = self.module.check_domain_service(f_module, ome_conn_mock_lac)
        assert result is None

    def test_get_chassis_device(self, ome_conn_mock_lac, ome_default_args, mocker, ome_response_mock):
        mocker.patch(MODULE_PATH + "get_ip_from_host", return_value="192.18.1.1")
        ome_response_mock.json_data = {"value": [{"DeviceId": 25011, "DomainRoleTypeValue": "LEAD",
                                                  "PublicAddress": ["192.168.1.1"]},
                                                 {"DeviceId": 25012, "DomainRoleTypeValue": "STANDALONE",
                                                  "PublicAddress": ["192.168.1.2"]}]}
        param = {"device_id": 25012, "hostname": "192.168.1.6", "enable_kvm_access": True}
        f_module = self.get_module_mock(params=param)
        with pytest.raises(Exception) as err:
            self.module.get_chassis_device(f_module, ome_conn_mock_lac)
        assert err.value.args[0] == "Unable to retrieve the device information."

    def test_get_ip_from_host(self, ome_conn_mock_lac, ome_default_args, ome_response_mock):
        result = self.module.get_ip_from_host("192.168.0.1")
        assert result == "192.168.0.1"

    def test_get_device_details(self, ome_conn_mock_lac, ome_default_args, ome_response_mock, mocker):
        param = {"device_id": 25012, "hostname": "192.168.1.6", "enable_kvm_access": True}
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
        param = {"device_id": 25012, "hostname": "192.168.1.6", "enable_kvm_access": True}
        f_module = self.get_module_mock(params=param)
        ome_response_mock.json_data = {"value": [{"Id": 25012, "DeviceServiceTag": "GHRT2RL"}], "EnableKvmAccess": True}
        mocker.patch(MODULE_PATH + 'check_mode_validation', return_value={"EnableKvmAccess": True})
        resp = self.module.get_device_details(ome_conn_mock_lac, f_module)
        assert resp.json_data["EnableKvmAccess"] is True
        param = {"hostname": "192.168.1.6", "enable_kvm_access": True}
        f_module = self.get_module_mock(params=param)
        mocker.patch(MODULE_PATH + 'get_chassis_device', return_value=("Id", 25011))
        resp = self.module.get_device_details(ome_conn_mock_lac, f_module)
        assert resp.json_data["EnableKvmAccess"] is True

    def test_check_mode_validation(self, ome_conn_mock_lac, ome_default_args, ome_response_mock, mocker):
        loc_data = {"EnableKvmAccess": True, "EnableChassisDirect": True, "EnableChassisPowerButton": True,
                    "EnableLcdOverridePin": True, "LcdAccess": True, "LcdCustomString": "LCD Text",
                    "LcdLanguage": "en", "LcdOverridePin": 123456, "LcdPresence": "Present",
                    "QuickSync": {"QuickSyncAccess": True, "TimeoutLimit": 10, "EnableInactivityTimeout": True,
                                  "TimeoutLimitUnit": "MINUTES", "EnableReadAuthentication": True,
                                  "EnableQuickSyncWifi": True, "QuickSyncHardware": "Present"}, }
        param = {"device_id": 25012, "hostname": "192.168.1.6", "enable_kvm_access": True}
        f_module = self.get_module_mock(params=param)
        with pytest.raises(Exception) as err:
            self.module.check_mode_validation(f_module, loc_data)
        assert err.value.args[0] == "No changes found to be applied."
        f_module.check_mode = True
        with pytest.raises(Exception) as err:
            self.module.check_mode_validation(f_module, loc_data)
        assert err.value.args[0] == "No changes found to be applied."
        param = {"device_id": 25012, "hostname": "192.168.1.6", "enable_kvm_access": False}
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
        ome_default_args.update({"device_id": 25011, "enable_kvm_access": True})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'check_domain_service', side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'check_domain_service', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'check_domain_service',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result
