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
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_lifecycle_controller_jobs
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from mock import MagicMock, PropertyMock
from io import StringIO
from ansible.module_utils._text import to_text
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")


MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestDeleteLcJob(FakeAnsibleModule):
    module = idrac_lifecycle_controller_jobs

    @pytest.fixture
    def idrac_lc_job_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.job_mgr = idrac_obj
        type(idrac_obj).delete_job = PropertyMock(return_value="msg")
        type(idrac_obj).delete_all_jobs = PropertyMock(return_value="msg")
        return idrac_obj

    @pytest.fixture
    def idrac_connection_delete_lc_job_queue_mock(self, mocker, idrac_lc_job_mock):
        idrac_conn_class_mock = mocker.patch(MODULE_PATH +
                                             'idrac_lifecycle_controller_jobs.iDRACConnection', return_value=idrac_lc_job_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_lc_job_mock
        return idrac_lc_job_mock

    def test_main_idrac_lc_job_success_case01(self, idrac_connection_delete_lc_job_queue_mock, idrac_default_args):
        idrac_default_args.update({"job_id": "job_id"})
        idrac_connection_delete_lc_job_queue_mock.job_mgr.delete_job.return_value = {"Status": "Success"}
        result = self._run_module(idrac_default_args)
        assert result == {'changed': True, 'msg': 'Successfully deleted the job.', 'status': {'Status': 'Success'}}

    def test_main_idrac_lc_job_success_case02(self, idrac_connection_delete_lc_job_queue_mock, idrac_default_args):
        idrac_connection_delete_lc_job_queue_mock.job_mgr.delete_all_jobs.return_value = {"Status": "Success"}
        result = self._run_module(idrac_default_args)
        assert result == {'changed': True, 'msg': 'Successfully deleted the job queue.', 'status': {'Status': 'Success'}}

    def test_main_idrac_delete_lc_job_failure_case(self, idrac_connection_delete_lc_job_queue_mock, idrac_default_args):
        idrac_default_args.update({"job_id": "job_id"})
        idrac_connection_delete_lc_job_queue_mock.job_mgr.delete_job.return_value = {"Status": "Error"}
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result == {'failed': True, 'msg': "Failed to delete the Job: {0}.".format("job_id"),
                          'status': {'Status': 'Error'}}

    @pytest.mark.parametrize("exc_type", [URLError, HTTPError, ImportError, ValueError, RuntimeError, TypeError])
    def test_main_exception_handling_idrac_lc_job_case(self, exc_type, idrac_connection_delete_lc_job_queue_mock,
                                                       idrac_default_args):
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            idrac_connection_delete_lc_job_queue_mock.job_mgr.delete_all_jobs.side_effect = exc_type('test')
            idrac_connection_delete_lc_job_queue_mock.job_mgr.delete_job.side_effect = exc_type('test')
        else:
            idrac_connection_delete_lc_job_queue_mock.job_mgr.delete_all_jobs.side_effect = \
                exc_type('http://testhost.com', 400, 'http error message', {"accept-type": "application/json"},
                         StringIO(json_str))
            idrac_connection_delete_lc_job_queue_mock.job_mgr.delete_job.side_effect = \
                exc_type('http://testhost.com', 400, 'http error message', {"accept-type": "application/json"},
                         StringIO(json_str))
        if not exc_type == URLError:
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        else:
            idrac_connection_delete_lc_job_queue_mock.job_mgr.delete_all_jobs
            idrac_connection_delete_lc_job_queue_mock.job_mgr.delete_job
            result = self._run_module(idrac_default_args)
        assert 'msg' in result
