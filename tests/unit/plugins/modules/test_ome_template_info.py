# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.3
# Copyright (C) 2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import ome_template_info
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from io import StringIO
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


@pytest.fixture
def ome_connection_template_info_mock(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'ome_template_info.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeTemplateInfo(FakeAnsibleModule):
    module = ome_template_info

    @pytest.mark.parametrize("module_params,data", [({"system_query_options": {"filter": "abc"}}, "$filter")])
    def test_get_query_parameters(self, module_params, data):
        res = self.module._get_query_parameters(module_params)
        if data is not None:
            assert data in res
        else:
            assert res is None

    def test_get_template_info_success_case01(self, ome_default_args, ome_connection_template_info_mock,
                                              ome_response_mock):
        ome_response_mock.json_data = {"value": [""]}
        ome_response_mock.status_code = 200
        result = self._run_module(ome_default_args)
        assert 'template_info' in result

    def test_get_template_info_success_case02(self, mocker, ome_default_args, ome_connection_template_info_mock,
                                              ome_response_mock):
        ome_default_args.update({"template_id": "24"})
        ome_response_mock.success = True
        ome_response_mock.json_data = {"value": [{"template_id": "24"}]}
        ome_response_mock.status_code = 200
        result = self._run_module(ome_default_args)
        assert result['changed'] is False
        assert 'template_info' in result

    def test_get_template_info_success_case03(self, mocker, ome_default_args, ome_connection_template_info_mock,
                                              ome_response_mock):
        mocker.patch(MODULE_PATH + 'ome_template_info._get_query_parameters',
                     return_value={"filter": "abc"})
        ome_default_args.update({"system_query_options": {"filter": "abc"}})
        ome_response_mock.success = True
        ome_response_mock.json_data = {"value": [{"filter": "abc"}]}
        ome_response_mock.status_code = 200
        result = self._run_module(ome_default_args)
        assert result['changed'] is False
        assert 'template_info' in result

    def test_get_template_info_failure_case(self, ome_default_args, ome_connection_template_info_mock,
                                            ome_response_mock):
        ome_response_mock.status_code = 500
        result = self._run_module_with_fail_json(ome_default_args)
        assert result['msg'] == 'Failed to fetch the template facts'

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_ome_template_info_main_exception_handling_case(self, exc_type, mocker, ome_default_args,
                                                            ome_connection_template_info_mock, ome_response_mock):
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            ome_connection_template_info_mock.invoke_request.side_effect = exc_type('test')
        else:
            ome_connection_template_info_mock.invoke_request.side_effect = exc_type('http://testhost.com', 400,
                                                                                    'http error message',
                                                                                    {"accept-type": "application/json"},
                                                                                    StringIO(json_str))
        result = self._run_module_with_fail_json(ome_default_args)
        assert 'template_info' not in result
        assert 'msg' in result
        assert result['failed'] is True
