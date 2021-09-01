# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.5.0
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
from ansible_collections.dellemc.openmanage.plugins.modules import ome_groups
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants

MULTIPLE_GROUPS_MSG = "Provide only one unique device group when state is present."
NONEXIST_GROUP_ID = "A device group with the provided ID does not exist."
NONEXIST_PARENT_ID = "A parent device group with the provided ID does not exist."
INVALID_PARENT = "The provided parent device group is not a valid user-defined static device group."
INVALID_GROUPS_DELETE = "Provide valid static device group(s) for deletion."
INVALID_GROUPS_MODIFY = "Provide valid static device group for modification."
PARENT_CREATION_FAILED = "Unable to create a parent device group with the name {pname}."
PARENT_IN_SUBTREE = "The parent group is already under the provided group."
CREATE_SUCCESS = "Successfully {op}d the device group."
GROUP_PARENT_SAME = "Provided parent and the device group cannot be the same."
DELETE_SUCCESS = "Successfully deleted the device group(s)."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
STATIC_ROOT = 'Static Groups'
SETTLING_TIME = 2

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_groups.'


@pytest.fixture
def ome_connection_mock_for_groups(mocker, ome_response_mock):
    connection_class_mock = mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.ome_groups.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeGroups(FakeAnsibleModule):
    module = ome_groups

    @pytest.mark.parametrize("params", [
        {"json_data": {"value": [{'Name': 'g1', 'Id': 24, 'TypeId': 3000, 'MembershipTypeId': 12}]},
         'message': DELETE_SUCCESS, "success": True, 'mparams': {'name': 'g1', 'state': 'absent'}},
        {"json_data": {"value": [{'Name': 'g1', 'Id': 24, 'TypeId': 3000, 'MembershipTypeId': 12}]},
         'message': DELETE_SUCCESS, "success": True, 'mparams': {'name': 'g1', 'state': 'absent'}},
        {"json_data": {"value": [{'Name': 'g1', 'Id': 24, 'TypeId': 3000, 'MembershipTypeId': 12}]},
         'message': CHANGES_FOUND, "success": True, 'mparams': {'group_id': 24, 'state': 'absent'}, 'check_mode': True},
        {"json_data": {"value": [{'Name': 'g1', 'Id': 24, 'TypeId': 3000, 'MembershipTypeId': 12}]},
         'message': NO_CHANGES_MSG, "success": True, 'mparams': {'name': 'g2', 'state': 'absent'}},
        {"json_data": {"value": [{'Name': 'g1', 'Id': 24, 'TypeId': 3000, 'MembershipTypeId': 12}]},
         'message': NO_CHANGES_MSG, "success": True, 'mparams': {'name': 'g2', 'state': 'absent'}, 'check_mode': True}])
    def test_ome_groups_delete(self, params, ome_connection_mock_for_groups, ome_response_mock, ome_default_args,
                               module_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['json_data']
        ome_connection_mock_for_groups.get_all_items_with_pagination.return_value = params['json_data']
        ome_default_args.update(params['mparams'])
        result = self._run_module(ome_default_args, check_mode=params.get('check_mode', False))
        assert result['msg'] == params['message']

    @pytest.mark.parametrize("params", [{"json_data": {
        "value": [{'Name': 'g2', 'Id': 24, 'TypeId': 3000, 'MembershipTypeId': 12},
                  {'Name': 'gp1', 'Id': 25, 'TypeId': 3000, 'MembershipTypeId': 12},
                  {'Name': 'Static Groups', 'Id': 1, 'TypeId': 2000, 'MembershipTypeId': 12}]},
        'message': CREATE_SUCCESS, "success": True,
        'mparams': {'name': 'g1', 'parent_group_name': 'gp1', 'description': 'My group described'},
        'return_data': 22, 'created_group': {'Name': 'g1', 'Id': 26, 'ParentId': 25, 'MembershipTypeId': 12}},
        {"json_data": {'value': [{'Name': 'g2', 'Id': 24, 'TypeId': 3000, 'MembershipTypeId': 12},
                                 {'Name': 'gp1', 'Id': 25, 'TypeId': 3000, 'MembershipTypeId': 12},
                                 {'Name': 'Static Groups', 'Id': 1, 'TypeId': 2000, 'MembershipTypeId': 12}]},
         'message': CREATE_SUCCESS, "success": True,
         'mparams': {'name': 'g1', 'parent_group_name': 'gp21', 'description': 'My group described'}, 'return_data': 22,
         'created_group': {'Name': 'g1', 'Id': 26, 'ParentId': 25, 'MembershipTypeId': 12}},
        {"json_data": {'value': [{'Name': 'g2', 'Id': 24, 'TypeId': 3000, 'MembershipTypeId': 12},
                                 {'Name': 'gp1', 'Id': 25, 'TypeId': 3000, 'MembershipTypeId': 12},
                                 {'Name': 'Static Groups', 'Id': 1, 'TypeId': 2000, 'MembershipTypeId': 12}]},
         'message': CREATE_SUCCESS, "success": True,
         'mparams': {'name': 'g1', 'parent_group_id': 25, 'description': 'My group described'}, 'return_data': 22,
         'created_group': {'Name': 'g1', 'Id': 26, 'ParentId': 25, 'MembershipTypeId': 12}},
        {"json_data": {'value': [{'Name': 'g2', 'Id': 24, 'TypeId': 3000, 'MembershipTypeId': 12},
                                 {'Name': 'gp1', 'Id': 25, 'TypeId': 3000, 'MembershipTypeId': 12},
                                 {'Name': 'Static Groups', 'Id': 1, 'TypeId': 2000, 'MembershipTypeId': 12}]},
         'message': CREATE_SUCCESS, "success": True,
         'mparams': {'name': 'g1', 'parent_group_name': 'Static Groups', 'description': 'My group described'},
         'return_data': 22, 'created_group': {'Name': 'g1', 'Id': 26, 'ParentId': 1, 'MembershipTypeId': 12}},
        {"json_data": {'value': [{'Name': 'g2', 'Id': 24, 'TypeId': 3000, 'MembershipTypeId': 12},
                                 {'Name': 'gp1', 'Id': 25, 'TypeId': 3000, 'MembershipTypeId': 12},
                                 {'Name': 'Static Groups', 'Id': 1, 'TypeId': 2000, 'MembershipTypeId': 12}]},
         'message': CREATE_SUCCESS, "success": True,
         'mparams': {'name': 'g1', 'parent_group_id': 1, 'description': 'My group described'}, 'return_data': 22,
         'created_group': {'Name': 'g1', 'Id': 26, 'ParentId': 1, 'MembershipTypeId': 12}},
        {"json_data": {'value': [{'Name': 'g2', 'Id': 24, 'TypeId': 3000, 'MembershipTypeId': 12},
                                 {'Name': 'gp1', 'Id': 25, 'TypeId': 3000, 'MembershipTypeId': 12},
                                 {'Name': 'Static Groups', 'Id': 1, 'TypeId': 2000, 'MembershipTypeId': 12}]},
         'message': CHANGES_FOUND, "success": True,
         'mparams': {'name': 'g1', 'parent_group_name': 'gp21', 'description': 'My group described'}, 'return_data': 22,
         'created_group': {'Name': 'g1', 'Id': 26, 'ParentId': 25, 'MembershipTypeId': 12}, 'check_mode': True}])
    def test_ome_groups_create(self, params, ome_connection_mock_for_groups, ome_response_mock, ome_default_args,
                               module_mock, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['return_data']
        ome_connection_mock_for_groups.get_all_items_with_pagination.return_value = params['json_data']
        ome_connection_mock_for_groups.strip_substr_dict.return_value = params.get('created_group', {})
        mocker.patch(MODULE_PATH + 'get_ome_group_by_id', return_value=params.get('created_group', {}))
        mocker.patch(MODULE_PATH + 'create_parent', return_value=params['created_group'].get('ParentId'))
        ome_default_args.update(params['mparams'])
        result = self._run_module(ome_default_args, check_mode=params.get('check_mode', False))
        assert result['msg'] == (params['message']).format(op='create')

    @pytest.mark.parametrize("params", [{"json_data": {
        'value': [{'Name': 'g1', 'Id': 24, 'TypeId': 3000, 'MembershipTypeId': 12, 'description': 'My group described'},
                  {'Name': 'gp1', 'Id': 25, 'TypeId': 3000, 'MembershipTypeId': 12},
                  {'Name': 'Static Groups', 'Id': 1, 'TypeId': 2000, 'MembershipTypeId': 12}]},
        'message': CREATE_SUCCESS, "success": True,
        'mparams': {'name': 'g1', 'new_name': 'j1', 'parent_group_name': 'gp1', 'description': 'description modified'},
        'return_data': 22, 'created_group': {'Name': 'g1', 'Id': 26, 'ParentId': 25, 'MembershipTypeId': 12}}, {
        "json_data": {'value': [{'Name': 'g1', 'Id': 24, 'TypeId': 3000, 'ParentId': 25, 'MembershipTypeId': 12,
                                 'description': 'My group described'},
                                {'Name': 'gp1', 'Id': 25, 'TypeId': 3000, 'MembershipTypeId': 12},
                                {'Name': 'Static Groups', 'Id': 1, 'TypeId': 2000, 'MembershipTypeId': 12}]},
        'message': CHANGES_FOUND, "success": True,
        'mparams': {'name': 'g1', 'parent_group_name': 'gp1', 'description': 'description modified'}, 'return_data': 22,
        'created_group': {'Name': 'g1', 'Id': 26, 'ParentId': 25, 'MembershipTypeId': 12}, 'check_mode': True}, {
        "json_data": {'value': [{'Name': 'g1', 'Id': 24, 'TypeId': 3000, 'ParentId': 25, 'MembershipTypeId': 12,
                                 'Description': 'My group described'},
                                {'Name': 'gp1', 'Id': 25, 'TypeId': 3000, 'MembershipTypeId': 12},
                                {'Name': 'Static Groups', 'Id': 1, 'TypeId': 2000, 'MembershipTypeId': 12}]},
        'message': NO_CHANGES_MSG, "success": True,
        'mparams': {'name': 'g1', 'new_name': 'g1', 'parent_group_name': 'gp1', 'description': 'My group described'},
        'return_data': 22, 'created_group': {'Name': 'g1', 'Id': 24, 'ParentId': 25, 'MembershipTypeId': 12},
        'check_mode': True}, ])
    def test_ome_groups_modify(self, params, ome_connection_mock_for_groups, ome_response_mock, ome_default_args,
                               module_mock, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['return_data']
        ome_connection_mock_for_groups.get_all_items_with_pagination.return_value = params['json_data']
        ome_connection_mock_for_groups.strip_substr_dict.return_value = params.get('created_group', {})
        mocker.patch(MODULE_PATH + 'get_ome_group_by_id', return_value=params.get('created_group', {}))
        mocker.patch(MODULE_PATH + 'create_parent', return_value=params['created_group'].get('ParentId'))
        # mocker.patch(MODULE_PATH + 'is_parent_in_subtree', return_value=False)
        ome_default_args.update(params['mparams'])
        result = self._run_module(ome_default_args, check_mode=params.get('check_mode', False))
        assert result['msg'] == (params['message']).format(op='update')

    @pytest.mark.parametrize("params", [{"json_data": {
        'value': [{'Name': 'g2', 'Id': 24, 'TypeId': 3000, 'MembershipTypeId': 12},
                  {'Name': 'g3', 'Id': 12, 'TypeId': 2000, 'MembershipTypeId': 24},
                  {'Name': 'gp1', 'Id': 25, 'TypeId': 3000, 'MembershipTypeId': 12},
                  {'Name': 'Static Groups', 'Id': 1, 'TypeId': 2000, 'MembershipTypeId': 12}]},
        'message': MULTIPLE_GROUPS_MSG, "success": True, 'mparams': {'name': ['g1', 'g3'], 'parent_group_name': 'gp1',
                                                                     'description': 'State present and multiple groups'},
        'return_data': 22, 'created_group': {'Name': 'g1', 'Id': 26, 'ParentId': 25, 'MembershipTypeId': 12}}, {
        "json_data": {'value': [{'Name': 'g2', 'Id': 24, 'TypeId': 3000, 'MembershipTypeId': 12},
                                {'Name': 'g3', 'Id': 12, 'TypeId': 2000, 'MembershipTypeId': 24},
                                {'Name': 'gp1', 'Id': 25, 'TypeId': 3000, 'MembershipTypeId': 12},
                                {'Name': 'Static Groups', 'Id': 1, 'TypeId': 2000, 'MembershipTypeId': 12}]},
        'message': NONEXIST_GROUP_ID, "success": True,
        'mparams': {'group_id': 13, 'parent_group_name': 'gp1', 'description': 'State present and no group_id'},
        'return_data': 22, 'created_group': {'Name': 'g1', 'Id': 26, 'ParentId': 25, 'MembershipTypeId': 12}}, {
        "json_data": {'value': [{'Name': 'g2', 'Id': 24, 'TypeId': 3000, 'MembershipTypeId': 12},
                                {'Name': 'g3', 'Id': 12, 'TypeId': 2000, 'MembershipTypeId': 24},
                                {'Name': 'gp1', 'Id': 25, 'TypeId': 3000, 'MembershipTypeId': 12},
                                {'Name': 'Static Groups', 'Id': 1, 'TypeId': 2000, 'MembershipTypeId': 12}]},
        'message': INVALID_PARENT, "success": True,
        'mparams': {'name': 'g1', 'parent_group_name': 'g3', 'description': 'State present and invalid parent'},
        'return_data': 22, 'created_group': {'Name': 'g1', 'Id': 26, 'ParentId': 25, 'MembershipTypeId': 12}}, {
        "json_data": {'value': [{'Name': 'g2', 'Id': 24, 'TypeId': 3000, 'MembershipTypeId': 12},
                                {'Name': 'g3', 'Id': 12, 'TypeId': 2000, 'MembershipTypeId': 24},
                                {'Name': 'gp1', 'Id': 25, 'TypeId': 3000, 'MembershipTypeId': 12},
                                {'Name': 'Static Groups', 'Id': 1, 'TypeId': 2000, 'MembershipTypeId': 12}]},
        'message': INVALID_GROUPS_DELETE, "success": True,
        'mparams': {'name': ['g1', 'g3'], 'state': 'absent', 'description': 'State absent and invalid group'},
        'return_data': 22, 'created_group': {'Name': 'g1', 'Id': 26, 'ParentId': 25, 'MembershipTypeId': 12}}, {
        "json_data": {'value': [{'Name': 'g2', 'Id': 24, 'TypeId': 3000, 'MembershipTypeId': 12},
                                {'Name': 'gp1', 'Id': 25, 'TypeId': 3000, 'MembershipTypeId': 12},
                                {'Name': 'Static Groups', 'Id': 1, 'TypeId': 2000, 'MembershipTypeId': 12}]},
        'message': NONEXIST_PARENT_ID, "success": True,
        'mparams': {'name': 'g1', 'parent_group_id': 26, 'description': 'create with non exist parent id'},
        'return_data': 22, 'created_group': {'Name': 'g1', 'Id': 26, 'ParentId': 25, 'MembershipTypeId': 12}}, {
        "json_data": {'value': [{'Name': 'g2', 'Id': 24, 'TypeId': 2000, 'MembershipTypeId': 24},
                                {'Name': 'gp1', 'Id': 25, 'TypeId': 3000, 'MembershipTypeId': 12},
                                {'Name': 'Static Groups', 'Id': 1, 'TypeId': 2000, 'MembershipTypeId': 12}]},
        'message': INVALID_PARENT, "success": True,
        'mparams': {'name': 'g1', 'parent_group_id': 24, 'description': 'create with non exist parent id'},
        'return_data': 22, 'created_group': {'Name': 'g1', 'Id': 26, 'ParentId': 25, 'MembershipTypeId': 12}}, {
        "json_data": {'value': [{'Name': 'g1', 'Id': 24, 'TypeId': 2000, 'ParentId': 25, 'MembershipTypeId': 24,
                                 'Description': 'My group described'},
                                {'Name': 'gp1', 'Id': 25, 'TypeId': 3000, 'MembershipTypeId': 12},
                                {'Name': 'Static Groups', 'Id': 1, 'TypeId': 2000, 'MembershipTypeId': 12}]},
        'message': INVALID_GROUPS_MODIFY, "success": True,
        'mparams': {'name': 'g1', 'new_name': 'g1', 'parent_group_name': 'gp1', 'description': 'My group described'},
        'return_data': 22, 'created_group': {'Name': 'g1', 'Id': 24, 'ParentId': 25, 'MembershipTypeId': 12},
        'check_mode': True},
        {"json_data": {'value': [{'Name': 'g1', 'Id': 24, 'TypeId': 3000, 'ParentId': 25, 'MembershipTypeId': 12,
         'Description': 'My group described'}, {'Name': 'gp1', 'Id': 24, 'TypeId': 3000, 'MembershipTypeId': 12},
                                 {'Name': 'Static Groups', 'Id': 1, 'TypeId': 2000, 'MembershipTypeId': 12}]},
         'message': GROUP_PARENT_SAME, "success": True,
         'mparams': {'name': 'g1', 'new_name': 'g1', 'parent_group_name': 'gp1', 'description': 'My group described'},
         'return_data': 22, 'created_group': {'Name': 'g1', 'Id': 24, 'ParentId': 25, 'MembershipTypeId': 12},
         'check_mode': True},
        {"json_data": {'value': [{'Name': 'x1', 'Id': 24, 'TypeId': 3000, 'ParentId': 25, 'MembershipTypeId': 12,
                                  'Description': 'My group described'},
                                 {'Name': 'g2', 'Id': 24, 'TypeId': 3000, 'MembershipTypeId': 12},
                                 {'Name': 'Static Groups', 'Id': 1, 'TypeId': 2000, 'MembershipTypeId': 12}]},
         'message': GROUP_PARENT_SAME, "success": True,
         'mparams': {'name': 'g1', 'parent_group_name': 'g1', 'description': 'My group described'},
         'return_data': 22, 'created_group': {'Name': 'g1', 'Id': 24, 'ParentId': 25, 'MembershipTypeId': 12},
         'check_mode': True}])
    def test_ome_groups_fail_jsons(self, params, ome_connection_mock_for_groups, ome_response_mock, ome_default_args,
                                   module_mock, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['return_data']
        ome_connection_mock_for_groups.get_all_items_with_pagination.return_value = params['json_data']
        ome_connection_mock_for_groups.strip_substr_dict.return_value = params.get('created_group', {})
        mocker.patch(MODULE_PATH + 'get_ome_group_by_id', return_value=params.get('created_group', {}))
        mocker.patch(MODULE_PATH + 'create_parent', return_value=params['created_group'].get('ParentId'))
        ome_default_args.update(params['mparams'])
        result = self._run_module_with_fail_json(ome_default_args)
        assert result['msg'] == params['message']

    @pytest.mark.parametrize("params", [{"json_data": 12, "mparams": {'name': 'g1', 'parent_group_name': 'gp21'}}])
    def test_create_parent(self, params, ome_connection_mock_for_groups, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params['mparams'])
        static_root = {'Name': 'Static Groups', 'Id': 1, 'TypeId': 2000, 'MembershipTypeId': 12}
        group_id = self.module.create_parent(ome_connection_mock_for_groups, f_module, static_root)
        assert group_id == params['json_data']

    @pytest.mark.parametrize("params",
                             [{"json_data": {'Name': 'g2', 'Id': 24, 'TypeId': 3000, 'MembershipTypeId': 12}}])
    def test_get_ome_group_by_id(self, params, ome_connection_mock_for_groups, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        group = self.module.get_ome_group_by_id(ome_connection_mock_for_groups, 24)
        assert group == params['json_data']

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_groups_main_exception_failure_case(self, exc_type, mocker, ome_default_args,
                                                    ome_connection_mock_for_groups, ome_response_mock):
        ome_default_args.update({"state": "absent", "name": "t1"})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'get_valid_groups', side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'get_valid_groups', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'get_valid_groups',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result
