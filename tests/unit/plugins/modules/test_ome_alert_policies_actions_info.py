# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.2.0
# Copyright (C) 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import ome_alert_policies_actions_info
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from io import StringIO
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


@pytest.fixture
def ome_alert_policies_actions_info_mock(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'ome_alert_policies_actions_info.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeAlertPoliciesActionsInfo(FakeAnsibleModule):
    module = ome_alert_policies_actions_info

    def test_ome_alert_policies_action_info_main_success_case_all(self,
                                                                  ome_alert_policies_actions_info_mock,
                                                                  ome_default_args, ome_response_mock):
        ome_response_mock.json_data = {"value": [
            {
                "Description": "Email",
                "Disabled": False,
                "Id": 50,
                "Name": "Email",
                "ParameterDetails": [
                    {
                        "Id": 1,
                        "Name": "subject",
                        "TemplateParameterTypeDetails": [
                            {
                                "Name": "maxLength",
                                "Value": "255"
                            }
                        ],
                        "Type": "string",
                        "Value": "Device Name: $name,  Device IP Address: $ip,  Severity: $severity"
                    }]}]}
        ome_response_mock.status_code = 200
        result = self._run_module(ome_default_args)
        assert 'actions' in result

    def test_ome_alert_policies_action_info_empty_case(self, ome_default_args,
                                                       ome_alert_policies_actions_info_mock,
                                                       ome_response_mock):
        ome_response_mock.json_data = {"value": []}
        ome_response_mock.status_code = 200
        ome_response_mock.success = True
        result = self._run_module(ome_default_args)
        assert result['actions'] == []

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError,
                              TypeError, ValueError])
    def test_ome_alert_policies_action_info_main_exception_handling_case(self, exc_type, ome_default_args,
                                                                         ome_alert_policies_actions_info_mock,
                                                                         ome_response_mock):
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            ome_alert_policies_actions_info_mock.invoke_request.side_effect = exc_type('test')
        else:
            ome_alert_policies_actions_info_mock.invoke_request.side_effect = exc_type('https://testhost.com',
                                                                                       400,
                                                                                       'http error message',
                                                                                       {"accept-type": "application/json"},
                                                                                       StringIO(json_str))
        result = self._run_module(ome_default_args)
        if exc_type != URLError:
            assert result['failed'] is True
        assert 'msg' in result
