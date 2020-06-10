#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0.14
# Copyright (C) 2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import

import pytest
from ansible.modules.remote_management.dellemc import dellemc_export_lc_logs
from units.modules.remote_management.dellemc.common import FakeAnsibleModule, Constants
from units.compat.mock import MagicMock, patch, Mock
from units.modules.utils import set_module_args, exit_json, fail_json, AnsibleFailJson, AnsibleExitJson
from units.compat.mock import PropertyMock
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")


class TestExportLcLogs(FakeAnsibleModule):
    module = dellemc_export_lc_logs

    @pytest.fixture
    def idrac_export_lc_logs_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.file_share_manager = idrac_obj
        omsdk_mock.log_mgr = idrac_obj
        return idrac_obj

    @pytest.fixture
    def idrac_connection_export_lc_logs_mock(self, mocker, idrac_export_lc_logs_mock):
        idrac_conn_class_mock = mocker.patch('ansible.modules.remote_management.dellemc.'
                                             'dellemc_export_lc_logs.iDRACConnection',
                                             return_value=idrac_export_lc_logs_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_export_lc_logs_mock
        return idrac_export_lc_logs_mock

    @pytest.fixture
    def idrac_file_manager_export_lc_logs_mock(self, mocker):
        try:
            lclog_file_name_format = "%ip_%Y%m%d_%H%M%S_LC_Log.log"
            file_manager_obj = mocker.patch(
                'ansible.modules.remote_management.dellemc.dellemc_export_lc_logs.file_share_manager')
        except AttributeError:
            file_manager_obj = MagicMock()
        obj = MagicMock()
        file_manager_obj.create_share_obj.return_value = obj
        file_manager_obj.myshare.new_file(lclog_file_name_format).return_value = obj
        return file_manager_obj

    def test_main_export_lc_logs_success_case(self,idrac_connection_export_lc_logs_mock, idrac_default_args, mocker,
                                             idrac_file_manager_export_lc_logs_mock):
        idrac_default_args.update({"share_name": "sharename", "share_user": "shareuser",
                                   "share_password": "sharepassword", "job_wait": True})
        message = {"Status": "Success"}
        mocker.patch('ansible.modules.remote_management.dellemc.dellemc_export_lc_logs.run_export_lc_logs',
                     return_value=(message, False))
        idrac_connection_export_lc_logs_mock.log_mgr.lclog_export.return_value = {"Status": "Success"}
        result = self._run_module(idrac_default_args)
        assert result == {'Status': 'Success', 'changed': False}

    def test_run_export_lc_logs_success_case01(self, idrac_connection_export_lc_logs_mock, idrac_default_args,
                                               idrac_file_manager_export_lc_logs_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "job_wait": True})
        idrac_connection_export_lc_logs_mock.log_mgr.lclog_export.return_value = {"status": "Success"}
        f_module = self.get_module_mock(params=idrac_default_args)
        msg, err = self.module.run_export_lc_logs(idrac_connection_export_lc_logs_mock, f_module)
        assert msg == {'changed': False, 'failed': False, 'msg': {'status': 'Success'}}
        assert msg['failed'] is False

    def test_run_export_lc_logs_status_fail_case01(self, idrac_connection_export_lc_logs_mock, idrac_default_args,
                                               idrac_file_manager_export_lc_logs_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "job_wait": True})
        idrac_connection_export_lc_logs_mock.log_mgr.lclog_export.return_value = {"Status": "failed"}
        f_module = self.get_module_mock(params=idrac_default_args)
        msg, err = self.module.run_export_lc_logs(idrac_connection_export_lc_logs_mock, f_module)
        assert msg == {'msg': {'Status': 'failed'}, 'failed': True, 'changed': False}
        assert msg['failed'] is True

    def test_run_export_lc_logs_failed_case01(self, idrac_connection_export_lc_logs_mock, idrac_default_args,
                                           idrac_file_manager_export_lc_logs_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "job_wait": True})
        error_msg = "Error in Runtime"
        obj2 = MagicMock()
        idrac_connection_export_lc_logs_mock.log_mgr = obj2
        type(obj2).lclog_export = Mock(side_effect=Exception(error_msg))
        f_module = self.get_module_mock(params=idrac_default_args)
        result, err = self.module.run_export_lc_logs(idrac_connection_export_lc_logs_mock, f_module)
        assert result['failed'] is True
        assert result['msg'] == "Error: {0}".format(error_msg)

    def test_main_run_export_lc_logs_fail_case(self,idrac_connection_export_lc_logs_mock, idrac_default_args, mocker,
                                             idrac_file_manager_export_lc_logs_mock):
        idrac_default_args.update({"share_name": "sharename", "share_user": "shareuser",
                                   "share_password": "sharepassword", "job_wait": True})
        message = {"Status": "Failed"}
        mocker.patch('ansible.modules.remote_management.dellemc.dellemc_export_lc_logs.run_export_lc_logs',
                     return_value=(message, True))
        idrac_connection_export_lc_logs_mock.log_mgr.lclog_export.return_value = {"Status": "Failed"}
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result == {'Status': 'Failed', 'failed': True}

    @pytest.mark.parametrize("exc_type", [ImportError, ValueError, RuntimeError])
    def test_main_export_lc_logs_exception_handling_case(self, exc_type, mocker, idrac_connection_export_lc_logs_mock,
                                                       idrac_default_args, idrac_file_manager_export_lc_logs_mock):
        idrac_default_args.update({"share_name": "sharename", "share_user": "shareuser",
                                   "share_password": "sharepassword", "job_wait": True})
        idrac_connection_export_lc_logs_mock.log_mgr.lclog_export.return_value = {"Status": "Failed"}
        mocker.patch('ansible.modules.remote_management.dellemc.dellemc_export_lc_logs.run_export_lc_logs',
                     side_effect=exc_type('test'))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True
