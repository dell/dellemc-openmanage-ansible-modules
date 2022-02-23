# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.1.0
# Copyright (C) 2022 Dell Inc. or its subsidiaries. All Rights Reserved.

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
from ansible_collections.dellemc.openmanage.plugins.modules import ome_server_interface_profile_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_server_interface_profile_info.'


@pytest.fixture
def ome_conn_mock_sip(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOMEMSIP(FakeAnsibleModule):

    module = ome_server_interface_profile_info

    def test_check_domain_service(self, ome_conn_mock_sip, ome_default_args):
        f_module = self.get_module_mock()
        result = self.module.check_domain_service(f_module, ome_conn_mock_sip)
        assert result is None

    def test_get_sip_info(self, ome_conn_mock_sip, ome_response_mock):
        f_module = self.get_module_mock(params={"device_id": [25011]})
        ome_conn_mock_sip.get_all_report_details.return_value = {
            "resp_obj": ome_response_mock, "report_list": [{"Id": 25012, "DeviceServiceTag": "HKRF20"}]
        }
        with pytest.raises(Exception) as err:
            self.module.get_sip_info(f_module, ome_conn_mock_sip)
        assert err.value.args[0] == "Unable to complete the operation because the entered target " \
                                    "device id(s) '25011' are invalid."
        f_module = self.get_module_mock(params={"device_id": [25012]})
        ome_response_mock.json_data = {"Id": "HKRF20", "ServerServiceTag": "HKRF20", "value": [{"Network": []}]}
        ome_conn_mock_sip.json_data = [{"Id": "HKRF20", "ServerServiceTag": "HKRF20"}]
        ome_conn_mock_sip.strip_substr_dict.return_value = {"Id": "HKRF20", "ServerServiceTag": "HKRF20",
                                                            "Networks": [{"Id": 10001}]}
        result = self.module.get_sip_info(f_module, ome_conn_mock_sip)
        assert result[0]["Id"] == "HKRF20"

    def test_main_case(self, ome_conn_mock_sip, ome_response_mock, ome_default_args, mocker):
        ome_default_args.update({"device_id": None, "validate_certs": False})
        with pytest.raises(Exception) as err:
            self._run_module(ome_default_args)
        assert err.value.args[0]['msg'] == "one of the following is required: device_id, device_service_tag."
        ome_default_args.update({"device_id": [25011], "validate_certs": False})
        mocker.patch(MODULE_PATH + 'check_domain_service')
        mocker.patch(MODULE_PATH + 'get_sip_info', return_value={"server_profiles": [{"Id": 25011}]})
        result = self._run_module(ome_default_args)
        assert result["msg"] == "Successfully retrieved the server interface profile information."

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_sip_power_main_exception_case(self, exc_type, mocker, ome_default_args,
                                               ome_conn_mock_sip, ome_response_mock):
        ome_default_args.update({"device_id": [25011], "validate_certs": False})
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
