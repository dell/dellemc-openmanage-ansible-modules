# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.0.0
# Copyright (C) 2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_user_info
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from mock import MagicMock
from ansible.module_utils._text import to_text
from io import StringIO

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestIDRACUserInfo(FakeAnsibleModule):
    module = idrac_user_info

    @pytest.fixture
    def idrac_user_info_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_user_info_mock(self, mocker, idrac_user_info_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'idrac_user_info.iDRACRedfishAPI',
                                       return_value=idrac_user_info_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_user_info_mock
        return idrac_user_info_mock

    def _test_user_info_main_success_case_all(self, idrac_default_args, idrac_connection_user_info_mock,
                                              idrac_user_info_mock):
        idrac_user_info_mock.status_code = 200
        idrac_user_info_mock.success = True
        result = self._run_module(idrac_default_args)
        assert 'user_info' in result

    def test_user_info_main_success_case_user_id(self, idrac_default_args, idrac_connection_user_info_mock,
                                                 idrac_user_info_mock):
        idrac_default_args.update({"user_id": 1})
        idrac_user_info_mock.success = True
        idrac_user_info_mock.json_data = {"value": [{"user_id": 1}]}
        idrac_user_info_mock.status_code = 200
        result = self._run_module(idrac_default_args)
        assert result['changed'] is False
        assert 'user_info' in result

    def _test_get_user_info_failure_case(self, idrac_default_args, idrac_connection_user_info_mock,
                                         idrac_user_info_mock):
        idrac_user_info_mock.status_code = 500
        idrac_user_info_mock.success = False
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result['msg'] == 'Unable to retrieve the user information.'

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_idrac_user_info_main_exception_handling_case(self, exc_type, mocker, idrac_default_args,
                                                          idrac_connection_user_info_mock, idrac_user_info_mock):
        idrac_user_info_mock.status_code = 400
        idrac_user_info_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            idrac_connection_user_info_mock.invoke_request.side_effect = exc_type('test')
        else:
            idrac_connection_user_info_mock.invoke_request.side_effect = exc_type('http://testhost.com', 400,
                                                                                  'http error message',
                                                                                  {"accept-type": "application/json"},
                                                                                  StringIO(json_str))
        if not exc_type == URLError:
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result
