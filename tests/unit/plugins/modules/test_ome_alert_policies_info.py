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
from ansible_collections.dellemc.openmanage.plugins.modules import ome_alert_policies_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text


MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
MODULE_SUCCESS_MESSAGE_ALL = "Successfully retrieved all the OME alert policies information."
MODULE_SUCCESS_MESSAGE_SPECIFIC = "Successfully retrieved {0} OME alert policy information."
POLICY_NAME_NOT_FOUND_OR_EMPTY = "The OME alert policy name {0} provided does not exist or empty."


class TestOmeAlertPolicyInfo(FakeAnsibleModule):
    """Pyest class for ome_alert_policies_info module."""
    module = ome_alert_policies_info
    resp_mock_value = {"@odata.context": "/api/$metadata#Collection(JobService.Job)",
                       "@odata.count": 1,
                       "value": [
                           {
                               "Id": 10006,
                               "Name": "TestAlert1",
                               "Description": "This policy is applicable to critical alerts.",
                               "State": True,
                               "Visible": True,
                               "Owner": None,
                           },
                           {
                               "Id": 10010,
                               "Name": "TestAlert2",
                               "Description": "This policy is applicable to critical alerts.",
                               "State": True,
                               "Visible": True,
                               "Owner": None,
                           }
                       ]}

    @pytest.fixture
    def ome_connection_alert_policy_info_mock(self, mocker, ome_response_mock):
        connection_class_mock = mocker.patch(MODULE_PATH + 'ome_alert_policies_info.RestOME')
        ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
        ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
        return ome_connection_mock_obj

    def test_all_ome_alert_policy_info_success_case(self, ome_default_args, ome_connection_alert_policy_info_mock,
                                                    ome_response_mock):
        ome_response_mock.json_data = self.resp_mock_value
        ome_response_mock.success = True
        result = self._run_module(ome_default_args)
        assert result['policies'][0]["Id"] == 10006
        assert "@odata.count" not in result['policies'][0]
        assert result['msg'] == MODULE_SUCCESS_MESSAGE_ALL

    def test_policy_name_ome_alert_policy_info_success_case(self, ome_default_args, ome_connection_alert_policy_info_mock,
                                                            ome_response_mock):
        policy_name = 'TestAlert2'
        ome_default_args.update({"policy_name": policy_name})
        ome_response_mock.json_data = self.resp_mock_value
        ome_response_mock.success = True
        result = self._run_module(ome_default_args)
        assert result['policies'][0]["Id"] == 10010
        assert "@odata.count" not in result['policies'][0]
        assert result['msg'] == MODULE_SUCCESS_MESSAGE_SPECIFIC.format(policy_name)

    def test_random_policy_name_ome_alert_policy_info(self, ome_default_args, ome_connection_alert_policy_info_mock,
                                                      ome_response_mock):
        random_name = 'Random'
        ome_default_args.update({"policy_name": random_name})
        ome_response_mock.json_data = self.resp_mock_value
        ome_response_mock.success = True
        result = self._run_module(ome_default_args)
        assert result['policies'] == []
        assert result['msg'] == POLICY_NAME_NOT_FOUND_OR_EMPTY.format(random_name)

    def test_empty_policy_name_ome_alert_policy_info(self, ome_default_args, ome_connection_alert_policy_info_mock,
                                                     ome_response_mock):
        empty_name = ""
        ome_default_args.update({"policy_name": empty_name})
        ome_response_mock.json_data = self.resp_mock_value
        ome_response_mock.success = True
        result = self._run_module(ome_default_args)
        assert result['policies'] == []
        assert result['msg'] == POLICY_NAME_NOT_FOUND_OR_EMPTY.format(empty_name)

    @pytest.mark.parametrize("exc_type", [URLError, HTTPError, SSLValidationError, ConnectionError,
                                          TypeError, ValueError])
    def test_ome_alert_policy_info_main_exception_case(self, exc_type, mocker, ome_default_args, ome_connection_alert_policy_info_mock,
                                                       ome_response_mock):
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(
                MODULE_PATH + 'ome_alert_policies_info.OMEAlertPolicyInfo.get_alert_policy_info',
                side_effect=exc_type('test'))
        else:
            mocker.patch(
                MODULE_PATH + 'ome_alert_policies_info.OMEAlertPolicyInfo.get_alert_policy_info',
                side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                     {"accept-type": "application/json"}, StringIO(json_str)))
        result = self._run_module(ome_default_args)
        if exc_type != URLError:
            assert result['failed'] is True
        assert 'msg' in result
