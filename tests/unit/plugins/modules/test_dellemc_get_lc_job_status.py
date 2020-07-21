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
from ansible_collections.dellemc.openmanage.plugins.modules import dellemc_get_lc_job_status
from ansible_collections.dellemc.openmanage.tests.unit.modules.common import FakeAnsibleModule, Constants
from ansible_collections.dellemc.openmanage.tests.unit.compat.mock import MagicMock
from ansible_collections.dellemc.openmanage.tests.unit.compat.mock import PropertyMock
from ansible_collections.dellemc.openmanage.tests.unit.utils import set_module_args, exit_json, fail_json, AnsibleFailJson, AnsibleExitJson
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")


class TestLcJobStatus(FakeAnsibleModule):
    module = dellemc_get_lc_job_status

    @pytest.fixture
    def idrac_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.job_mgr = idrac_obj
        type(idrac_obj).get_job_status = PropertyMock(return_value="job_id")
        return idrac_obj

    @pytest.fixture
    def idrac_get_lc_job_status_connection_mock(self, mocker, idrac_mock):
        idrac_conn_class_mock = mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                                             'dellemc_get_lc_job_status.iDRACConnection', return_value=idrac_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_mock
        return idrac_mock

    def test_main_idrac_get_lc_job_status_success_case01(self, idrac_get_lc_job_status_connection_mock,
                                                         idrac_default_args, mocker):
        idrac_default_args.update({"job_id": "job_id"})
        message = ({"msg": {}, "failed": False, "changed": False}, False)
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.dellemc_get_lc_job_status.run_get_lc_job_status',
                     return_value=message)
        idrac_get_lc_job_status_connection_mock.job_mgr.get_job_status.return_value = {"Status": "Success"}
        result = self._run_module(idrac_default_args)
        assert result["changed"] is False
        assert result["failed"] is False

    def test_run_get_lc_job_status_success_case01(self, idrac_get_lc_job_status_connection_mock, idrac_default_args):
        idrac_default_args.update({"job_id": "job_id"})
        obj2 = MagicMock()
        idrac_get_lc_job_status_connection_mock = obj2
        type(obj2).get_job_status = PropertyMock(return_value="job_id")
        f_module = self.get_module_mock(params=idrac_default_args)
        msg, err = self.module.run_get_lc_job_status(idrac_get_lc_job_status_connection_mock, f_module)
        assert msg == {'changed': False, 'failed': False,
                       'msg': idrac_get_lc_job_status_connection_mock.job_mgr.get_job_status()}
        assert msg['failed'] is False
        assert err is False

    def test_main_idrac_get_lc_job_status_failed_case01(self, idrac_get_lc_job_status_connection_mock,
                                                        idrac_default_args):
        f_module = self.get_module_mock(params=idrac_default_args)
        error_msg = "Error in Runtime"
        obj2 = MagicMock()
        idrac_get_lc_job_status_connection_mock.job_mgr = obj2
        type(obj2).get_job_status = PropertyMock(side_effect=Exception(error_msg))
        msg, err = self.module.run_get_lc_job_status(idrac_get_lc_job_status_connection_mock, f_module)
        assert msg['failed'] is True
        assert msg['msg'] == "Error: {0}".format(error_msg)
        assert err is True

    def test_main_get_lc_job_status_failed_case01(self, idrac_get_lc_job_status_connection_mock, idrac_default_args):
        idrac_default_args.update({"job_id": "job_id"})
        error_msg = "Error occurs"
        obj2 = MagicMock()
        idrac_get_lc_job_status_connection_mock.job_mgr = obj2
        type(obj2).get_job_status = PropertyMock(side_effect=Exception(error_msg))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result['changed'] is False
        assert result['failed'] is True
        assert result['msg'] == "Error: {0}".format(error_msg)

    @pytest.mark.parametrize("exc_type", [ImportError, ValueError, RuntimeError])
    def test_main_exception_handling_case(self, exc_type, mocker, idrac_get_lc_job_status_connection_mock,
                                          idrac_default_args):
        idrac_default_args.update({"job_id": "job_id"})
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.dellemc_get_lc_job_status.run_get_lc_job_status',
                      side_effect=exc_type('test'))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True
