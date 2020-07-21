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
from ansible_collections.dellemc.openmanage.plugins.modules import dellemc_delete_lc_job
from ansible_collections.dellemc.openmanage.tests.unit.modules.common import FakeAnsibleModule, Constants
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.compat.mock import MagicMock
from ansible_collections.dellemc.openmanage.tests.unit.compat.mock import PropertyMock
from ansible_collections.dellemc.openmanage.tests.unit.compat.mock import MagicMock, patch, Mock
import pytest, json
from io import StringIO
from ansible.module_utils._text import to_text
from ansible_collections.dellemc.openmanage.tests.unit.utils import set_module_args, exit_json, fail_json, AnsibleFailJson, AnsibleExitJson
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")


class TestDeleteLcJob(FakeAnsibleModule):
    module = dellemc_delete_lc_job

    @pytest.fixture
    def idrac_lc_job_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.job_mgr = idrac_obj
        type(idrac_obj).delete_job = PropertyMock(return_value="msg")
        return idrac_obj

    @pytest.fixture
    def idrac_connection_delete_lc_job_mock(self, mocker, idrac_lc_job_mock):
        idrac_conn_class_mock = mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                                             'dellemc_delete_lc_job.iDRACConnection', return_value=idrac_lc_job_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_lc_job_mock
        return idrac_lc_job_mock

    def test_main_delete_lc_job_success_case(self, idrac_connection_delete_lc_job_mock, idrac_default_args,
                                              mocker):
        idrac_default_args.update({"job_id": "job_id"})
        message = {"Status": "Success"}
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.dellemc_delete_lc_job.run_delete_lc_job',
                     return_value=(message, False))
        idrac_connection_delete_lc_job_mock.job_mgr.delete_job.return_value = {"Status": "Success"}
        result = self._run_module(idrac_default_args)
        assert result == {'Status': 'Success', 'changed': False}

    def test_run_delete_lc_job_success_case01(self, idrac_connection_delete_lc_job_mock, idrac_default_args):
        idrac_default_args.update({"job_id": "job_id"})
        idrac_connection_delete_lc_job_mock.job_mgr.delete_job.return_value = {"Status": "Success"}
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        msg, err = self.module.run_delete_lc_job(idrac_connection_delete_lc_job_mock, f_module)
        assert msg == {'changed': False,
           'failed': False,
           'msg': {'Message': 'Job not found to delete!',
                   'Status': 'Success',
                   'changes_applicable': False}}

    def test_run_delete_lc_job_success_case02(self, idrac_connection_delete_lc_job_mock, idrac_default_args):
        idrac_default_args.update({"job_id": "job_id"})
        idrac_connection_delete_lc_job_mock.job_mgr.get_job_status.return_value = {"Status": "Fault"}
        idrac_connection_delete_lc_job_mock.job_mgr.delete_job.return_value = {'Status': 'Success'}
        f_module = self.get_module_mock(params=idrac_default_args)
        msg, err = self.module.run_delete_lc_job(idrac_connection_delete_lc_job_mock, f_module)
        assert msg == {'changed': True, 'failed': False, 'msg': {'Status': 'Success'}}

    def test_run_delete_lc_job_success_case03(self, idrac_connection_delete_lc_job_mock, idrac_default_args):
        idrac_default_args.update({"job_id": "job_id"})
        idrac_connection_delete_lc_job_mock.job_mgr.delete_job.return_value = {"Status": "Success"}
        idrac_connection_delete_lc_job_mock.job_mgr.get_job_status.return_value = {"Status": "Fault"}
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        msg, err = self.module.run_delete_lc_job(idrac_connection_delete_lc_job_mock, f_module)
        assert msg == {'changed': True,
           'failed': False,
           'msg': {'Message': 'Job found to delete!',
                   'Status': 'Success',
                   'changes_applicable': True}}

    def test_run_delete_lc_job_success_case04(self, idrac_connection_delete_lc_job_mock, idrac_default_args):
        idrac_default_args.update({"job_id": "job_id"})
        idrac_connection_delete_lc_job_mock.job_mgr.get_job_status.return_value = {"Status": "Fault"}
        idrac_connection_delete_lc_job_mock.job_mgr.delete_job.return_value = {'Status': 'success'}
        f_module = self.get_module_mock(params=idrac_default_args)
        msg, err = self.module.run_delete_lc_job(idrac_connection_delete_lc_job_mock, f_module)
        assert msg == {'changed': False, 'failed': True, 'msg': {'Status': 'success'}}

    def test_run_delete_lc_job_status_fail_case01(self, idrac_connection_delete_lc_job_mock, idrac_default_args):
        idrac_default_args.update({"job_id": "job_id"})
        idrac_connection_delete_lc_job_mock.job_mgr.delete_job.return_value = {"Status": "failed"}
        f_module = self.get_module_mock(params=idrac_default_args)
        msg, err = self.module.run_delete_lc_job(idrac_connection_delete_lc_job_mock, f_module)
        assert msg == {'changed': False, 'failed': True, 'msg': 'Invalid Job ID: job_id'}

    def test_run_delete_lc_job_failed_case01(self, idrac_connection_delete_lc_job_mock, idrac_default_args):
        idrac_default_args.update({"job_id": "job_id"})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        idrac_connection_delete_lc_job_mock.job_mgr.get_job_status.return_value = {"status": "Fault"}
        obj2 = MagicMock()
        idrac_connection_delete_lc_job_mock.job_mgr = obj2
        type(obj2).get_job_status = PropertyMock(side_effect=Exception())
        msg, err = self.module.run_delete_lc_job(idrac_connection_delete_lc_job_mock, f_module)
        assert msg['failed'] is True
        assert err is True

    def test_main_run_delete_lc_job_fail_case(self, idrac_connection_delete_lc_job_mock, idrac_default_args,
                                               mocker):
        idrac_default_args.update({"job_id": "job_id"})
        message = {"Status": "Failed"}
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.dellemc_delete_lc_job.run_delete_lc_job',
                     return_value=(message, True))
        idrac_connection_delete_lc_job_mock.job_mgr.delete_job.return_value = {"Status": "Failed"}
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result == {'Status': 'Failed', 'failed': True}

    @pytest.mark.parametrize("exc_type", [ImportError, ValueError, RuntimeError])
    def test_main_delete_lc_job_exception_handling_case(self, exc_type, idrac_connection_delete_lc_job_mock,
                                                        mocker, idrac_default_args):
        idrac_default_args.update({"job_id": "job_id"})
        idrac_connection_delete_lc_job_mock.job_mgr.delete_job.return_value = {"Status": "Failed"}
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.dellemc_delete_lc_job.run_delete_lc_job',
                     side_effect=exc_type('test'))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True
