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
from ansible_collections.dellemc.openmanage.plugins.modules import ome_alert_policies_message_id_info
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from io import StringIO
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


@pytest.fixture
def ome_alert_policies_message_id_info_mock(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'ome_alert_policies_message_id_info.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeAlertPoliciesMessageIDInfo(FakeAnsibleModule):
    module = ome_alert_policies_message_id_info

    def test_alert_policies_message_id_info_success_case(self, ome_default_args, ome_alert_policies_message_id_info_mock, ome_response_mock):
        ome_response_mock.json_data = {"value": [
            {
                "Category": "System Health",
                "Message": "The ${0} sensor has failed, and the last recorded value by the sensor was ${1} A.",
                "MessageId": "AMP400",
                "Prefix": "AMP",
                "SequenceNo": 400,
                "Severity": "Critical",
                "SubCategory": "Amperage"
            }
        ]}
        ome_response_mock.status_code = 200
        result = self._run_module(ome_default_args)
        assert 'message_ids' in result
        assert result['msg'] == "Successfully retrieved alert policies message ids information."

    def test_ome_alert_policies_message_id_info_empty_case(self, ome_default_args,
                                                           ome_alert_policies_message_id_info_mock,
                                                           ome_response_mock):
        ome_response_mock.json_data = {"value": []}
        ome_response_mock.status_code = 200
        ome_response_mock.success = True
        result = self._run_module(ome_default_args)
        assert result['message_ids'] == []

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError,
                              TypeError, ValueError])
    def test_ome_alert_policies_message_id_info_main_exception_handling_case(self, exc_type, ome_default_args,
                                                                             ome_alert_policies_message_id_info_mock,
                                                                             ome_response_mock):
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            ome_alert_policies_message_id_info_mock.invoke_request.side_effect = exc_type('test')
        else:
            ome_alert_policies_message_id_info_mock.invoke_request.side_effect = exc_type('https://testhost.com',
                                                                                          400,
                                                                                          'http error message',
                                                                                          {"accept-type": "application/json"},
                                                                                          StringIO(json_str))
        result = self._run_module(ome_default_args)
        if exc_type != URLError:
            assert result['failed'] is True
        assert 'msg' in result
