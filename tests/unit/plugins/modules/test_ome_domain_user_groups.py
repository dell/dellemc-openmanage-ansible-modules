# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 4.0.0
# Copyright (C) 2021 Dell Inc. or its subsidiaries. All Rights Reserved.

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
from ansible_collections.dellemc.openmanage.plugins.modules import ome_domain_user_groups
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_domain_user_groups.'
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."


@pytest.fixture
def ome_conn_mock_ad(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOMEADUser(FakeAnsibleModule):

    module = ome_domain_user_groups

    def test_get_directory_user(self, ome_conn_mock_ad, ome_response_mock, ome_default_args, mocker):
        f_module = self.get_module_mock(params={"state": "absent", "group_name": "Administrator"})
        ome_response_mock.json_data = {"value": [{"UserName": "Administrator", "RoleId": "10", "UserTypeId": 2}]}
        result = self.module.get_directory_user(f_module, ome_conn_mock_ad)
        assert result["UserName"] == "Administrator"

        f_module = self.get_module_mock(params={"state": "absent"})
        ome_response_mock.json_data = {"value": [{"UserName": "Administrator", "RoleId": "10", "UserTypeId": 2}]}
        with pytest.raises(Exception) as err:
            self.module.get_directory_user(f_module, ome_conn_mock_ad)
        assert err.value.args[0] == "missing required arguments: group_name"

        f_module = self.get_module_mock(params={"state": "absent", "group_name": "Administrator"})
        f_module.check_mode = True
        ome_response_mock.json_data = {"value": [{"UserName": "Administrator", "RoleId": "10", "UserTypeId": 2}]}
        with pytest.raises(Exception) as err:
            self.module.get_directory_user(f_module, ome_conn_mock_ad)
        assert err.value.args[0] == "Changes found to be applied."

        f_module = self.get_module_mock(params={"state": "absent", "group_name": "Administrator"})
        f_module.check_mode = True
        ome_response_mock.json_data = {"value": []}
        with pytest.raises(Exception) as err:
            self.module.get_directory_user(f_module, ome_conn_mock_ad)
        assert err.value.args[0] == "No changes found to be applied."

        f_module = self.get_module_mock(params={"state": "absent", "group_name": "Administrator"})
        ome_response_mock.json_data = {"value": []}
        with pytest.raises(Exception) as err:
            self.module.get_directory_user(f_module, ome_conn_mock_ad)
        assert err.value.args[0] == NO_CHANGES_MSG

    def test_delete_directory_user(self, ome_conn_mock_ad, ome_response_mock, ome_default_args, mocker):
        ome_response_mock.status_code = 204
        msg, changed = self.module.delete_directory_user(ome_conn_mock_ad, 15011)
        assert msg == "Successfully deleted the active directory user group."
        assert changed is True

    def test_get_role(self, ome_conn_mock_ad, ome_response_mock, ome_default_args, mocker):
        f_module = self.get_module_mock(params={"state": "present", "group_name": "Administrator",
                                                "role": "Administrator"})
        ome_response_mock.json_data = {"value": [{"Name": "ADMINISTRATOR", "Id": 10}]}
        result = self.module.get_role(f_module, ome_conn_mock_ad)
        assert result == 10

        f_module = self.get_module_mock(params={"state": "present", "group_name": "Administrator",
                                                "role": "Administrator"})
        ome_response_mock.json_data = {"value": [{"Name": "ADMIN", "Id": 10}]}
        with pytest.raises(Exception) as err:
            self.module.get_role(f_module, ome_conn_mock_ad)
        assert err.value.args[0] == "Unable to complete the operation because the entered " \
                                    "role name 'Administrator' does not exist."

        f_module = self.get_module_mock(params={"state": "present", "group_name": "Administrator"})
        ome_response_mock.json_data = {"value": [{"Name": "ADMIN", "Id": 10}]}
        with pytest.raises(Exception) as err:
            self.module.get_role(f_module, ome_conn_mock_ad)
        assert err.value.args[0] == "missing required arguments: role"

    def test_search_directory(self, ome_conn_mock_ad, ome_response_mock, ome_default_args, mocker):
        f_module = self.get_module_mock(params={"state": "present", "group_name": "Administrator",
                                                "domain_username": "admin@dev0", "domain_password": "password"})
        ome_response_mock.json_data = [{"CommonName": "Administrator", "ObjectGuid": "object_id"}]
        obj_id, name = self.module.search_directory(f_module, ome_conn_mock_ad, 16011)
        assert obj_id == "object_id"

        f_module = self.get_module_mock(params={"state": "present", "group_name": "Admin",
                                                "domain_username": "admin@dev0", "domain_password": "password"})
        with pytest.raises(Exception) as err:
            self.module.search_directory(f_module, ome_conn_mock_ad, 16011)
        assert err.value.args[0] == "Unable to complete the operation because the entered " \
                                    "group name 'Admin' does not exist."

    def test_get_directory(self, ome_conn_mock_ad, ome_response_mock, ome_default_args, mocker):
        f_module = self.get_module_mock()
        with pytest.raises(Exception) as err:
            self.module.get_directory(f_module, ome_conn_mock_ad)
        assert err.value.args[0] == "missing required arguments: directory_name or directory_id"

        f_module = self.get_module_mock(params={"directory_name": "test_directory"})
        ome_response_mock.json_data = {'value': [{"Name": "test_directory", "Id": 1}]}
        result = self.module.get_directory(f_module, ome_conn_mock_ad)
        assert result == 1

        f_module = self.get_module_mock(params={"directory_id": 2})
        ome_response_mock.json_data = {'value': [{"Name": "test_directory", "Id": 2}]}
        result = self.module.get_directory(f_module, ome_conn_mock_ad)
        assert result == 2

        f_module = self.get_module_mock(params={"directory_id": 3})
        with pytest.raises(Exception) as err:
            self.module.get_directory(f_module, ome_conn_mock_ad)
        assert err.value.args[0] == "Unable to complete the operation because the entered " \
                                    "directory id '3' does not exist."

    def test_directory_user(self, ome_conn_mock_ad, ome_response_mock, ome_default_args, mocker):
        f_module = self.get_module_mock(params={"group_name": "Administrator", "role": "administrator"})
        mocker.patch(MODULE_PATH + "get_directory_user", return_value={"UserName": "Administrator", "Id": 15011,
                                                                       "RoleId": "10", "Enabled": True})
        mocker.patch(MODULE_PATH + "get_role", return_value=16)
        mocker.patch(MODULE_PATH + "get_directory", return_value=10612)
        mocker.patch(MODULE_PATH + "search_directory", return_value=("obj_gui_id", "administrator"))
        ome_response_mock.json_data = [{"Name": "Account Operators", "Id": "16617", "ObjectGuid": "a491859c"}]
        resp, msg = self.module.directory_user(f_module, ome_conn_mock_ad)
        assert msg == 'updated'

        f_module.check_mode = True
        with pytest.raises(Exception) as err:
            self.module.directory_user(f_module, ome_conn_mock_ad)
        assert err.value.args[0] == "Changes found to be applied."

        mocker.patch(MODULE_PATH + "get_directory_user", return_value={"UserName": "Administrator", "Id": 15011,
                                                                       "RoleId": "16", "Enabled": True})
        with pytest.raises(Exception) as err:
            self.module.directory_user(f_module, ome_conn_mock_ad)
        assert err.value.args[0] == "No changes found to be applied."

        f_module.check_mode = False
        mocker.patch(MODULE_PATH + "get_directory_user", return_value={"UserName": "Administrator", "Id": 15011,
                                                                       "RoleId": "16", "Enabled": True})
        with pytest.raises(Exception) as err:
            self.module.directory_user(f_module, ome_conn_mock_ad)
        assert err.value.args[0] == NO_CHANGES_MSG

        mocker.patch(MODULE_PATH + "get_directory_user", return_value=None)
        f_module.check_mode = True
        with pytest.raises(Exception) as err:
            self.module.directory_user(f_module, ome_conn_mock_ad)
        assert err.value.args[0] == "Changes found to be applied."

        f_module.check_mode = False
        resp, msg = self.module.directory_user(f_module, ome_conn_mock_ad)
        assert msg == "imported"

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_domain_exception(self, exc_type, mocker, ome_default_args,
                                  ome_conn_mock_ad, ome_response_mock):
        ome_default_args.update({"state": "absent"})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'get_directory_user', side_effect=exc_type("url open error"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result["failed"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'get_directory_user', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'get_directory_user',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result
