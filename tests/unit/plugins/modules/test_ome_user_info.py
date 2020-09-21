# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.1
# Copyright (C) 2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import ome_user_info
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from io import StringIO
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


@pytest.fixture
def ome_connection_user_info_mock(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'ome_user_info.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeUserInfo(FakeAnsibleModule):
    module = ome_user_info

    @pytest.mark.parametrize("module_params,data", [({"system_query_options": {"filter": "abc"}}, "$filter")])
    def test_user_get_query_parameters(self, module_params, data, ome_connection_user_info_mock):
        res = self.module._get_query_parameters(module_params)
        if data is not None:
            assert data in res
        else:
            assert res is None

    def test_user_info_main_success_case_all(self, ome_default_args, ome_connection_user_info_mock, ome_response_mock):
        ome_response_mock.json_data = {"value": [{"account_id": 1,
                                                  "system_query_options": "the user based on UserName"}]}
        ome_response_mock.status_code = 200
        result = self._run_module(ome_default_args)
        assert 'user_info' in result

    def test_user_info_main_success_case_account_id(self, ome_default_args, ome_connection_user_info_mock,
                                                    ome_response_mock):
        ome_default_args.update({"account_id": 1})
        ome_response_mock.success = True
        ome_response_mock.json_data = {"value": [{"account_id": 1}]}
        ome_response_mock.status_code = 200
        result = self._run_module(ome_default_args)
        assert result['changed'] is False
        assert 'user_info' in result

    def test_user_info_success_case03(self, ome_default_args, ome_connection_user_info_mock, ome_response_mock, mocker):
        mocker.patch(MODULE_PATH + 'ome_user_info._get_query_parameters',
                     return_value={"filter": "abc"})
        ome_default_args.update({"system_query_options": {"filter": "abc"}})
        ome_response_mock.success = True
        ome_response_mock.json_data = {"value": [{"filter": "abc"}]}
        ome_response_mock.status_code = 200
        result = self._run_module(ome_default_args)
        assert result['changed'] is False
        assert 'user_info' in result

    def test_get_user_info_failure_case(self, ome_default_args, ome_connection_user_info_mock, ome_response_mock):
        ome_response_mock.status_code = 500
        ome_response_mock.success = False
        result = self._run_module_with_fail_json(ome_default_args)
        assert result['msg'] == 'Unable to retrieve the account details.'

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_ome_user_info_main_exception_handling_case(self, exc_type, mocker, ome_default_args,
                                                        ome_connection_user_info_mock, ome_response_mock):
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            ome_connection_user_info_mock.invoke_request.side_effect = exc_type('test')
        else:
            ome_connection_user_info_mock.invoke_request.side_effect = exc_type('http://testhost.com', 400,
                                                                                'http error message',
                                                                                {"accept-type": "application/json"},
                                                                                StringIO(json_str))
        if not exc_type == URLError:
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(ome_default_args)
        assert 'msg' in result
