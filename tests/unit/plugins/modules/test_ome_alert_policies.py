# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.3.0
# Copyright (C) 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
from io import StringIO

import pytest
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import ome_alert_policies
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_alert_policies.'

SUCCESS_MSG = "Successfully completed the {0} alert policy operation."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_MSG = "Changes found to be applied."


@pytest.fixture
def ome_connection_mock_for_alert_policies(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeAlertPolicies(FakeAnsibleModule):
    module = ome_alert_policies

    @pytest.mark.parametrize("params", [
        {"message": SUCCESS_MSG.format("toggle enable"), "success": True,
         "json_data": {"value": [{'Name': "new alert policy", "Id": 12, "Enabled": False}]},
         "mparams": {"name": "new alert policy", "enable": True}},
        {"message": CHANGES_MSG, "success": True, "check_mode": True,
         "json_data": {"value": [{'Name': "new alert policy", "Id": 12, "Enabled": False}]},
         "mparams": {"name": "new alert policy", "enable": True}},
        {"message": "More than one policy name provided for update.", "success": True,
         "json_data": {"value": [{'Name': "alert policy1", "Id": 12, "Enabled": True},
                                 {'Name': "alert policy2", "Id": 13, "Enabled": True}]},
         "mparams": {"name": ["alert policy1", "alert policy2"], "enable": False, "description": 'Update case failed'}},
        {"message": "Policies alert policy3 are invalid for enable.", "success": True,
         "json_data": {"value": [{'Name': "alert policy1", "Id": 12, "Enabled": True},
                                 {'Name': "alert policy2", "Id": 13, "Enabled": True}]},
         "mparams": {"name": ["alert policy3", "alert policy2"], "enable": False}},
        {"message": NO_CHANGES_MSG, "success": True, "check_mode": True,
         "json_data": {"value": [{'Name': "new alert policy", "Id": 12, "Enabled": False}]},
         "mparams": {"name": "new alert policy", "enable": False}}
    ])
    def test_ome_alert_policies_enable_disable(self, params, ome_connection_mock_for_alert_policies,
                                               ome_response_mock, ome_default_args, module_mock, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['json_data']
        ome_connection_mock_for_alert_policies.get_all_items_with_pagination.return_value = params[
            'json_data']
        ome_default_args.update(params['mparams'])
        result = self._run_module(
            ome_default_args, check_mode=params.get('check_mode', False))
        assert result['msg'] == params['message']

    @pytest.mark.parametrize("params", [
        {"message": SUCCESS_MSG.format("delete"), "success": True,
         "json_data": {"report_list": [{'Name': "new alert policy", "Id": 12, "DefaultPolicy": False}],
                       "value": [{'Name': "new alert policy", "Id": 12, "DefaultPolicy": False}]},
         "mparams": {"name": "new alert policy", "state": "absent"}},
        {"message": CHANGES_MSG, "success": True, "check_mode": True,
         "json_data": {"report_list": [{'Name': "new alert policy", "Id": 12, "DefaultPolicy": False}],
                       "value": [{'Name': "new alert policy", "Id": 12, "DefaultPolicy": False}]},
         "mparams": {"name": "new alert policy", "state": "absent"}},
        {"message": "Default Policies new alert policy cannot be deleted.", "success": True,
         "json_data": {"report_list": [{'Name': "new alert policy", "Id": 12, "DefaultPolicy": False}],
                       "value": [{'Name': "new alert policy", "Id": 12, "DefaultPolicy": True}]},
         "mparams": {"name": "new alert policy", "state": "absent"}},
        {"message": "Policy does not exist.", "success": True, "check_mode": True,
         "json_data": {"report_list": [{'Name': "new alert policy", "Id": 12, "DefaultPolicy": False}],
                       "value": [{'Name': "new alert policy 1", "Id": 12, "DefaultPolicy": False}]},
         "mparams": {"name": "new alert policy", "state": "absent"}},
        {"message": "Policy does not exist.", "success": True,
         "json_data": {"report_list": [{'Name': "new alert policy", "Id": 12, "DefaultPolicy": False}],
                       "value": [{'Name': "new alert policy 1", "Id": 12, "DefaultPolicy": False}]},
         "mparams": {"name": "new alert policy", "state": "absent"}},
    ])
    def test_ome_alert_policies_delete(self, params, ome_connection_mock_for_alert_policies,
                                       ome_response_mock, ome_default_args, module_mock, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['json_data']
        ome_connection_mock_for_alert_policies.get_all_items_with_pagination.return_value = params[
            'json_data']
        ome_default_args.update(params['mparams'])
        result = self._run_module(
            ome_default_args, check_mode=params.get('check_mode', False))
        assert result['msg'] == params['message']

    @pytest.mark.parametrize("exc_type",
                             [SSLValidationError, ConnectionError, TypeError, ValueError, OSError, HTTPError, URLError])
    def test_ome_alert_policies_category_info_main_exception_failure_case(self, exc_type, mocker, ome_default_args,
                                                                          ome_connection_mock_for_alert_policies,
                                                                          ome_response_mock):
        json_str = to_text(json.dumps({"data": "out"}))
        ome_default_args.update({"name": "new alert policy", "enable": True})
        if exc_type == HTTPError:
            mocker.patch(MODULE_PATH + 'get_alert_policies', side_effect=exc_type(
                'http://testhost.com', 401, 'http error message', {
                    "accept-type": "application/json"},
                StringIO(json_str)))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
        elif exc_type == URLError:
            mocker.patch(MODULE_PATH + 'get_alert_policies',
                         side_effect=exc_type("exception message"))
            result = self._run_module(ome_default_args)
            assert result['unreachable'] is True
        else:
            mocker.patch(MODULE_PATH + 'get_alert_policies',
                         side_effect=exc_type("exception message"))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
