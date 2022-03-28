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
from ansible_collections.dellemc.openmanage.plugins.modules import ome_device_power_settings
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from mock import MagicMock, patch, Mock

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_device_power_settings.'


@pytest.fixture
def ome_conn_mock_power(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOMEMDevicePower(FakeAnsibleModule):

    module = ome_device_power_settings

    def test_check_domain_service(self, ome_conn_mock_power, ome_default_args):
        f_module = self.get_module_mock()
        result = self.module.check_domain_service(f_module, ome_conn_mock_power)
        assert result is None

    def test_get_chassis_device(self, ome_conn_mock_power, ome_default_args, mocker, ome_response_mock):
        mocker.patch(MODULE_PATH + "get_ip_from_host", return_value="192.18.1.1")
        ome_response_mock.json_data = {"value": [{"DeviceId": 25011, "DomainRoleTypeValue": "LEAD",
                                                  "PublicAddress": ["192.168.1.1"]},
                                                 {"DeviceId": 25012, "DomainRoleTypeValue": "STANDALONE",
                                                  "PublicAddress": ["192.168.1.2"]}]}
        param = {"device_id": 25012, "hostname": "192.168.1.6",
                 "power_configuration": {"enable_power_cap": True, "power_cap": 3424}}
        f_module = self.get_module_mock(params=param)
        with pytest.raises(Exception) as err:
            self.module.get_chassis_device(f_module, ome_conn_mock_power)
        assert err.value.args[0] == "Failed to fetch the device information."

    def test_check_mode_validation(self, ome_conn_mock_power, ome_default_args, ome_response_mock):
        loc_data = {"PowerCap": "3424", "MinPowerCap": "3291", "MaxPowerCap": "3424",
                    "RedundancyPolicy": "NO_REDUNDANCY", "EnablePowerCapSettings": True,
                    "EnableHotSpare": True, "PrimaryGrid": "GRID_1", "PowerBudgetOverride": False}
        param = {"power_configuration": {"enable_power_cap": True, "power_cap": 3424}}
        f_module = self.get_module_mock(params=param)
        with pytest.raises(Exception) as err:
            self.module.check_mode_validation(f_module, loc_data)
        param = {"hot_spare_configuration": {"enable_hot_spare": False}}
        f_module = self.get_module_mock(params=param)
        f_module.check_mode = True
        with pytest.raises(Exception) as err:
            self.module.check_mode_validation(f_module, loc_data)
        assert err.value.args[0] == "Changes found to be applied."
        param = {"redundancy_configuration": {"redundancy_policy": "NO_REDUNDANCY"}}
        f_module = self.get_module_mock(params=param)
        f_module.check_mode = True
        with pytest.raises(Exception) as err:
            self.module.check_mode_validation(f_module, loc_data)
        assert err.value.args[0] == "No changes found to be applied."

    def test_fetch_device_details(self, ome_conn_mock_power, ome_default_args, ome_response_mock):
        param = {"device_id": 25012, "hostname": "192.168.1.6",
                 "power_configuration": {"enable_power_cap": True, "power_cap": 3424}}
        f_module = self.get_module_mock(params=param)
        ome_response_mock.status_code = 200
        ome_response_mock.success = True
        ome_response_mock.json_data = {"value": [], "PowerCap": "3424", "MinPowerCap": "3291",
                                       "MaxPowerCap": "3424", "RedundancyPolicy": "NO_REDUNDANCY",
                                       "EnablePowerCapSettings": True, "EnableHotSpare": True,
                                       "PrimaryGrid": "GRID_1", "PowerBudgetOverride": False}
        with pytest.raises(Exception) as err:
            self.module.fetch_device_details(f_module, ome_conn_mock_power)
        assert err.value.args[0] == "Unable to complete the operation because the entered target " \
                                    "device id '25012' is invalid."

    def test_get_ip_from_host(self, ome_conn_mock_power, ome_default_args, ome_response_mock):
        result = self.module.get_ip_from_host("192.168.0.1")
        assert result == "192.168.0.1"

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_device_power_main_exception_case(self, exc_type, mocker, ome_default_args,
                                                  ome_conn_mock_power, ome_response_mock):
        ome_default_args.update({"device_id": 25011, "power_configuration": {"enable_power_cap": True,
                                                                             "power_cap": 3424}})
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
