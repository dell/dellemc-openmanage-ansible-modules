# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.0.0
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
import pytest
from ansible_collections.dellemc.openmanage.plugins.modules import ome_user
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from io import StringIO
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


@pytest.fixture
def ome_connection_for_user(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'ome_user.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeUser(FakeAnsibleModule):
    module = ome_user

    def test__validate_inputs_fail_case(self, ome_connection_for_user):
        f_module = self.get_module_mock(params={"state": "absent", "user_id": None})
        with pytest.raises(Exception) as exc:
            self.module._validate_inputs(f_module)
        assert exc.value.args[0] == "One of the following 'user_id' or 'name' " \
                                    "option is required for state 'absent'"

    def test__validate_inputs_user_pass_case(self, mocker):
        f_module = self.get_module_mock(params={"state": "absent", "user_id": 123})
        fail_module_mock = mocker.patch(MODULE_PATH + 'ome_user.fail_module')
        self.module._validate_inputs(f_module)
        fail_module_mock.assert_not_called()

    def test_get_user_id_from_name(self, ome_response_mock, ome_connection_for_user):
        ome_response_mock.success = True
        ome_response_mock.json_data = {'value': [{"UserName": "Testname", "Id": 24}]}
        ome_response_mock.status_code = 200
        data = self.module.get_user_id_from_name(ome_connection_for_user, "Testname")
        assert data == 24

    def test_get_user_id_from_name01(self, ome_response_mock, ome_connection_for_user):
        ome_response_mock.success = True
        val = None
        ome_response_mock.json_data = {'value': [{"UserName": "Testname", "Id": 24}]}
        ome_response_mock.status_code = 200
        data = self.module.get_user_id_from_name(ome_connection_for_user, "Test")
        assert data == val

    def test_get_user_id_from_name_case02(self, ome_connection_for_user):
        val = None
        data = self.module.get_user_id_from_name(ome_connection_for_user, None)
        assert data == val

    def test__get_resource_parameters_present_success_case01(self, ome_response_mock, ome_connection_for_user, mocker):
        ome_response_mock.status_code = 200
        ome_response_mock.success = True
        ome_response_mock.json_date = {'value': []}
        f_module = self.get_module_mock(params={"state": "present",
                                                "user_id": 23,
                                                "attributes": {"UserName": "user1", "Password": "UserPassword",
                                                               "RoleId": "10", "Enabled": True}})
        mocker.patch(MODULE_PATH + 'ome_user.get_user_id_from_name', return_value=23)
        data = self.module._get_resource_parameters(f_module, ome_response_mock)
        assert data == ('PUT', "AccountService/Accounts('23')",
                        {'Enabled': True, 'Id': 23, 'Password': 'UserPassword', 'RoleId': '10', 'UserName': 'user1'})

    def test__get_resource_parameters_absent_success_case02(self, ome_response_mock, mocker, ome_connection_for_user,
                                                            ome_default_args):
        ome_response_mock.status_code = 200
        ome_response_mock.success = True
        ome_response_mock.json_date = {'value': []}
        f_module = self.get_module_mock(params={"state": "absent", "user_id": 23})
        mocker.patch(MODULE_PATH + 'ome_user.get_user_id_from_name', return_value=23)
        data = self.module._get_resource_parameters(f_module, ome_response_mock)
        assert data == ('DELETE', "AccountService/Accounts('23')", None)

    def test__get_resource_parameters_case03(self, ome_response_mock, mocker, ome_default_args):
        ome_response_mock.status_code = 200
        ome_response_mock.success = True
        ome_response_mock.json_date = {'value': []}
        f_module = self.get_module_mock(params={"state": "present",
                                                "user_id": None,
                                                "attributes": {"UserName": "user1", "Password": "UserPassword",
                                                               "RoleId": "10", "Enabled": True}})
        mocker.patch(MODULE_PATH + 'ome_user.get_user_id_from_name', return_value=None)
        data = self.module._get_resource_parameters(f_module, ome_response_mock)
        assert data == ('POST', "AccountService/Accounts",
                        {'Enabled': True, 'Password': 'UserPassword', 'RoleId': '10', 'UserName': 'user1'})

    def test__get_resource_parameters_fail_case(self, ome_response_mock, mocker):
        ome_response_mock.status_code = 200
        ome_response_mock.success = True
        ome_response_mock.json_date = {'value': []}
        f_module = self.get_module_mock(params={"state": "absent", "user_id": None})
        mocker.patch(MODULE_PATH + 'ome_user.get_user_id_from_name', return_value=None)
        with pytest.raises(Exception) as exc:
            self.module._get_resource_parameters(f_module, ome_response_mock)
        assert exc.value.args[0] == "Unable to get the account because the specified account " \
                                    "does not exist in the system."

    def test__get_resource_parameters_fail_case_02(self, ome_response_mock, mocker):
        fail_module_mock = mocker.patch(MODULE_PATH + 'ome_user.fail_module')
        f_module = self.get_module_mock(params={"state": "absent", "user_id": None})
        mocker.patch(MODULE_PATH + 'ome_user.get_user_id_from_name', return_value=None)
        res = self.module._get_resource_parameters(f_module, ome_response_mock)
        assert (res[0], res[1], res[2]) == ('DELETE', "AccountService/Accounts('None')", None)
        assert fail_module_mock.assert_not_called

    def test_main_user_success_case01(self, ome_default_args, mocker, ome_connection_for_user, ome_response_mock):
        ome_default_args.update({"state": "absent", "user_id": 23})
        mocker.patch(MODULE_PATH + 'ome_user._validate_inputs')
        mocker.patch(MODULE_PATH + 'ome_user._get_resource_parameters',
                     return_value=["DELETE", "ACCOUNT_RESOURCE", {"user_id": 23}])
        result = self._run_module(ome_default_args)
        message_success = [
            "Successfully deleted the User", "Successfully modified a User", "Successfully created a User"]
        assert result['changed'] is True
        assert result['msg'] in message_success

    def test_main_user_success_case02(self, ome_default_args, mocker, ome_connection_for_user, ome_response_mock):
        ome_default_args.update({"state": "present",
                                 "user_id": 23,
                                 "attributes": {"UserName": "user1", "Password": "UserPassword",
                                                "RoleId": "10", "Enabled": True}})
        mocker.patch(MODULE_PATH + 'ome_user._validate_inputs')
        mocker.patch(MODULE_PATH + 'ome_user._get_resource_parameters',
                     return_value=["PUT", "ACCOUNT_RESOURCE", {"user_id": 23}])
        result = self._run_module(ome_default_args)
        message_success = [
            "Successfully deleted the User", "Successfully modified a User", "Successfully created a User"]
        assert result['changed'] is True
        assert result['msg'] in message_success

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_main_user_exception_case(self, exc_type, mocker, ome_default_args, ome_connection_for_user,
                                      ome_response_mock):
        ome_default_args.update({"state": "present",
                                 "user_id": 23,
                                 "attributes": {"UserName": "user1", "Password": "UserPassword",
                                                "RoleId": "10", "Enabled": True}})
        mocker.patch(MODULE_PATH + 'ome_user._validate_inputs')
        mocker.patch(
            MODULE_PATH + 'ome_user._get_resource_parameters', return_value=("method",
                                                                             "path",
                                                                             "payload"))
        ome_response_mock.json_data = {"value": []}
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            ome_connection_for_user.invoke_request.side_effect = exc_type('test')
        else:
            mocker.patch(
                MODULE_PATH + 'ome_user._get_resource_parameters',
                side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                     {"accept-type": "application/json"}, StringIO(json_str)))
        result = self._run_module_with_fail_json(ome_default_args)
        assert 'msg' in result
        assert result['failed'] is True

    @pytest.mark.parametrize("http_method, status_code", [('POST', 200), ('PUT', 200), ('DELETE', 204)])
    def test_exit_module_user_success_case(self, http_method, status_code, ome_response_mock):
        ome_response_mock.status_code = status_code
        ome_response_mock.success = True
        ome_response_mock.json_date = {'value': []}
        f_module = self.get_module_mock()
        msg_dict = {'POST': "Successfully created a User",
                    'PUT': "Successfully modified a User",
                    'DELETE': "Successfully deleted the User"}
        with pytest.raises(Exception) as exc:
            self.module.exit_module(f_module, ome_response_mock, http_method)
        assert exc.value.args[0] == msg_dict[http_method]
