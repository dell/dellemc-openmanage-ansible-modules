# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.0.0
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_lifecycle_controller_jobs
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from urllib.error import URLError, HTTPError
from ansible.module_utils.urls import SSLValidationError
from unittest.mock import MagicMock
from io import StringIO
from ansible.module_utils._text import to_text


MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestDeleteLcJob(FakeAnsibleModule):
    module = idrac_lifecycle_controller_jobs

    @pytest.fixture
    def idrac_redfish_lc_jobs_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_redfish_lc_jobs_connection_mock(self, mocker, idrac_redfish_lc_jobs_mock):
        idrac_redfish_conn_class_mock = mocker.patch(
            MODULE_PATH + 'idrac_lifecycle_controller_jobs.iDRACRedfishAPI',
            return_value=idrac_redfish_lc_jobs_mock
        )
        idrac_redfish_conn_class_mock.return_value.__enter__.return_value = idrac_redfish_lc_jobs_mock
        return idrac_redfish_lc_jobs_mock

    def test_main_get_lc_job_success_case00(self,
                                            idrac_default_args,
                                            mocker):
        mock_idrac = MagicMock()

        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_jobs.iDRACRedfishAPI",
            return_value=mock_idrac
        )
        mock_idrac.__enter__.return_value = mock_idrac
        idrac_default_args.update({"job_id": "job_id"})
        mocker.patch(MODULE_PATH +
                     "idrac_lifecycle_controller_jobs."
                     "IDRACLifecycleControllerJobs.lifecycle_controller_jobs_operation",
                     return_value=({"Status": "Success"}, "job"))
        result = self._run_module(idrac_default_args)
        assert result == {'changed': True, 'msg': 'Successfully deleted the job.', 'status': {'Status': 'Success'}}

    def test_main_get_lc_job_success_case01(self,
                                            idrac_default_args,
                                            mocker):
        mock_idrac = MagicMock()

        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_jobs.iDRACRedfishAPI",
            return_value=mock_idrac
        )
        mock_idrac.__enter__.return_value = mock_idrac
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_jobs.IDRACLifecycleControllerJobs.lifecycle_controller_jobs_operation",
                     return_value=({"Status": "Success"}, "job queue"))
        result = self._run_module(idrac_default_args)
        assert result == {'changed': True, 'msg': 'Successfully deleted the job queue.', 'status': {'Status': 'Success'}}

    def test_main_get_lc_job_failure_case(self,
                                          idrac_default_args,
                                          mocker):
        mock_idrac = MagicMock()

        mocker.patch(
            MODULE_PATH + "idrac_lifecycle_controller_jobs.iDRACRedfishAPI",
            return_value=mock_idrac
        )
        mock_idrac.__enter__.return_value = mock_idrac

        error_response = {
            "error": {
                "@Message.ExtendedInfo": [
                    {
                        "MessageId": "JobFailed",
                        "Message": "Invalid Job Id.",
                        "Resolution": "Provide valid Job Id."
                    }
                ],
                "code": "Base.1.0.GeneralError",
                "message": "A general error occurred"
            }
        }

        json_str = json.dumps(error_response)

        http_error = HTTPError(
            url='https://testhost.com',
            code=400,
            msg='Bad Request',
            hdrs={"Content-Type": "application/json"},
            fp=StringIO(json_str)
        )

        mocker.patch(MODULE_PATH +
                     "idrac_lifecycle_controller_jobs."
                     "IDRACLifecycleControllerJobs."
                     "lifecycle_controller_jobs_operation",
                     side_effect=http_error)

        idrac_default_args.update({"job_id": "job_id"})

        result = self._run_module(idrac_default_args)
        expected = {
            'changed': False,
            'failed': True,
            'msg': 'Failed to delete the Job: job_id.',
            'status': {
                'Status': 'Error',
                'Message': 'Invalid Job Id.',
                'MessageID': 'JobFailed',
                'Return': 'Error',
                'retval': True,
                'Data': {
                    'DeleteJobQueue_OUTPUT': {
                        'Message': 'Invalid Job Id.',
                        'MessageID': 'JobFailed'
                    }
                }
            }
        }

        assert result == expected

    @pytest.mark.parametrize("exc_type", [URLError, HTTPError, ImportError, ValueError, RuntimeError, TypeError])
    def test_main_exception_handling_idrac_lc_job_case(self, exc_type,
                                                       idrac_redfish_lc_jobs_connection_mock,
                                                       idrac_default_args, mocker):
        error_body = {"error": {"@Message.ExtendedInfo": [{"Message": "http error message", "MessageId": "ERR001"}]}}
        json_str = to_text(json.dumps(error_body))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(
                MODULE_PATH + "idrac_lifecycle_controller_jobs.IDRACLifecycleControllerJobs.lifecycle_controller_jobs_operation",
                side_effect=exc_type('test'))
        else:
            mocker.patch(
                MODULE_PATH + "idrac_lifecycle_controller_jobs.IDRACLifecycleControllerJobs.lifecycle_controller_jobs_operation",
                side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                     {"accept-type": "application/json"}, StringIO(json_str)))
        if exc_type != URLError:
            result = self._run_module(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result
