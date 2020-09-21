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
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_lifecycle_controller_job_status_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible_collections.dellemc.openmanage.tests.unit.compat.mock import MagicMock, PropertyMock
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestLcJobStatus(FakeAnsibleModule):
    module = idrac_lifecycle_controller_job_status_info

    @pytest.fixture
    def idrac_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.job_mgr = idrac_obj
        type(idrac_obj).get_job_status = PropertyMock(return_value="job_id")
        return idrac_obj

    @pytest.fixture
    def idrac_get_lc_job_status_connection_mock(self, mocker, idrac_mock):
        idrac_conn_class_mock = mocker.patch(MODULE_PATH +
                                             'idrac_lifecycle_controller_job_status_info.iDRACConnection',
                                             return_value=idrac_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_mock
        return idrac_mock

    def test_main_idrac_get_lc_job_status_success_case01(self, idrac_get_lc_job_status_connection_mock,
                                                         idrac_default_args, mocker):
        idrac_default_args.update({"job_id": "job_id"})
        idrac_get_lc_job_status_connection_mock.job_mgr.get_job_status.return_value = {"Status": "Success"}
        result = self._run_module(idrac_default_args)
        assert result["changed"] is False

    @pytest.mark.parametrize("exc_type", [SSLValidationError, URLError, ValueError, TypeError,
                                          ConnectionError, HTTPError])
    def test_main_exception_handling_case(self, exc_type, mocker, idrac_get_lc_job_status_connection_mock,
                                          idrac_default_args):
        idrac_default_args.update({"job_id": "job_id"})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type == URLError:
            idrac_get_lc_job_status_connection_mock.job_mgr.get_job_status.side_effect = exc_type("url open error")
            result = self._run_module(idrac_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            idrac_get_lc_job_status_connection_mock.job_mgr.get_job_status.side_effect = exc_type("exception message")
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        else:
            idrac_get_lc_job_status_connection_mock.job_mgr.get_job_status.side_effect = exc_type('http://testhost.com', 400,
                                                                                                  'http error message',
                                                                                                  {"accept-type": "application/json"},
                                                                                                  StringIO(json_str))
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        assert 'msg' in result
