# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.2.0
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_lifecycle_controller_logs
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from mock import MagicMock, patch, Mock
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestExportLcLogs(FakeAnsibleModule):
    module = idrac_lifecycle_controller_logs

    @pytest.fixture
    def idrac_export_lc_logs_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.file_share_manager = idrac_obj
        omsdk_mock.log_mgr = idrac_obj
        return idrac_obj

    @pytest.fixture
    def idrac_connection_export_lc_logs_mock(self, mocker, idrac_export_lc_logs_mock):
        idrac_conn_class_mock = mocker.patch(MODULE_PATH + 'idrac_lifecycle_controller_logs.iDRACConnection',
                                             return_value=idrac_export_lc_logs_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_export_lc_logs_mock
        return idrac_export_lc_logs_mock

    @pytest.fixture
    def idrac_file_manager_export_lc_logs_mock(self, mocker):
        try:
            lclog_file_name_format = "%ip_%Y%m%d_%H%M%S_LC_Log.log"
            file_manager_obj = mocker.patch(MODULE_PATH + 'idrac_lifecycle_controller_logs.file_share_manager')
        except AttributeError:
            file_manager_obj = MagicMock()
        obj = MagicMock()
        file_manager_obj.create_share_obj.return_value = obj
        file_manager_obj.myshare.new_file(lclog_file_name_format).return_value = obj
        return file_manager_obj

    def test_main_export_lc_logs_success_case(self, idrac_connection_export_lc_logs_mock, idrac_default_args, mocker,
                                              idrac_file_manager_export_lc_logs_mock):
        idrac_default_args.update({"share_name": "sharename", "share_user": "shareuser",
                                   "share_password": "sharepassword", "job_wait": True})
        message = {"Status": "Success", "JobStatus": "Success"}
        mocker.patch(MODULE_PATH + 'idrac_lifecycle_controller_logs.run_export_lc_logs', return_value=message)
        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Successfully exported the lifecycle controller logs."

    def test_run_export_lc_logs_success_case01(self, idrac_connection_export_lc_logs_mock, idrac_default_args,
                                               idrac_file_manager_export_lc_logs_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "job_wait": True})
        idrac_connection_export_lc_logs_mock.log_mgr.lclog_export.return_value = {"Status": "Success"}
        f_module = self.get_module_mock(params=idrac_default_args)
        msg = self.module.run_export_lc_logs(idrac_connection_export_lc_logs_mock, f_module)
        assert msg == {'Status': 'Success'}

    def test_run_export_lc_logs_status_fail_case01(self, idrac_connection_export_lc_logs_mock, idrac_default_args,
                                                   idrac_file_manager_export_lc_logs_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "job_wait": True})
        idrac_connection_export_lc_logs_mock.log_mgr.lclog_export.return_value = {"Status": "failed"}
        f_module = self.get_module_mock(params=idrac_default_args)
        msg = self.module.run_export_lc_logs(idrac_connection_export_lc_logs_mock, f_module)
        assert msg == {'Status': 'failed'}

    @pytest.mark.parametrize("exc_type", [RuntimeError, SSLValidationError, ConnectionError, KeyError,
                                          ImportError, ValueError, TypeError, HTTPError, URLError])
    def test_main_export_lc_logs_exception_handling_case(self, exc_type, mocker, idrac_connection_export_lc_logs_mock,
                                                         idrac_default_args, idrac_file_manager_export_lc_logs_mock):
        idrac_default_args.update({"share_name": "sharename", "share_user": "shareuser",
                                   "share_password": "sharepassword", "job_wait": True})
        idrac_connection_export_lc_logs_mock.log_mgr.lclog_export.return_value = {"Status": "Failed"}
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'idrac_lifecycle_controller_logs.run_export_lc_logs',
                         side_effect=exc_type('test'))
        else:
            mocker.patch(MODULE_PATH + 'idrac_lifecycle_controller_logs.run_export_lc_logs',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
        if not exc_type == URLError:
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result
