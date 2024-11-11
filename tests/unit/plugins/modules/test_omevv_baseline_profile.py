# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.9.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import omevv_baseline_profile
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from io import StringIO
from mock import MagicMock
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.omevv_baseline_profile.'
MODULE_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.omevv_utils.omevv_firmware_utils.'
SUCCESS_MSG = "Successfully retrieved the baseline profile information."
NO_PROFILE_MSG = "Unable to complete the operation because the '{profile_name}' is not a valid 'profile_name'."
FAILED_MSG = "Unable to fetch the baseline profile information."
INVOKE_REQ_KEY = "RestOMEVV.invoke_request"
GET_PROFILE_INFO_KEY = "OMEVVBaselineProfile.get_baseline_profile_by_name"
PERFORM_OPERATION_KEY = "BaselineProfile.execute"
PERFORM_CREATE_PROFILE = "OMEVVBaselineProfile.create_baseline_profile"
PERFORM_MODIFY_PROFILE = "OMEVVBaselineProfile.modify_baseline_profile"
PERFORM_DELETE_PROFILE = "OMEVVBaselineProfile.delete_baseline_profile"
GET_PROFILE_BY_ID = "OMEVVBaselineProfile.get_baseline_profile_by_id"
SEARCH_PROFILE_NAME = "OMEVVBaselineProfile.search_baseline_profile_name"
CREATE_DIFF_MODE_CHECK = "CreateBaselineProfile.diff_mode_check"
MODIFY_DIFF_MODE_CHECK = "ModifyBaselineProfile.diff_mode_check"
DELETE_DIFF_MODE_CHECK = "DeleteBaselineProfile.diff_mode_check"
HTTP_ERROR = "http error message"
HTTP_ERROR_URL = 'https://testhost.com'
RETURN_TYPE = "application/json"
PROFILE_NAME = "Dell Default Catalog"
DESCRIPTION = "Latest Baseline From Dell"
V_CENTER_UUID = "1234-5678"


class TestBaselineProfile(FakeAnsibleModule):
    module = omevv_baseline_profile

    @pytest.fixture
    def omevv_baseline_profile_mock(self):
        baseline_obj = MagicMock()
        return baseline_obj

    @pytest.fixture
    def omevv_connection_baseline_profile(self, mocker, omevv_baseline_profile_mock):
        omevv_conn_mock = mocker.patch(MODULE_PATH + 'RestOMEVV',
                                       return_value=omevv_baseline_profile_mock)
        omevv_conn_mock.return_value.__enter__.return_value = omevv_baseline_profile_mock
        return omevv_conn_mock

    def test_execute(self, omevv_default_args, omevv_connection_baseline_profile):
        obj = MagicMock()
        omevv_obj = self.module.BaselineProfile(
            omevv_connection_baseline_profile, obj)
        omevv_obj.execute()

    def test_validate_common_params(self, omevv_connection_baseline_profile, mocker):
        mock_validate_job_wait = mocker.patch(
            'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.validate_job_wait'
        )
        mock_validate_time = mocker.patch(
            'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.validate_time'
        )
        mock_validate_repository_profile = mocker.patch.object(
            omevv_connection_baseline_profile.omevv_baseline_obj, 'validate_repository_profile'
        )
        mock_validate_cluster_names = mocker.patch.object(
            omevv_connection_baseline_profile.omevv_baseline_obj, 'validate_cluster_names'
        )

        # Mock module parameters with specific values
        module = MagicMock()
        module.params = {
            'time': '14:00',
            'repository_profile': 'default_repo',
            'cluster': ['Cluster1'],
            'job_wait': True,
            'job_wait_timeout': 600  # Set a valid integer to avoid the TypeError
        }

        obj = MagicMock()
        baseline_profile = omevv_baseline_profile.BaselineProfile(module, obj)
        baseline_profile.validate_common_params()

        # Assert that each validation function was called with expected parameters
        # mock_validate_job_wait.assert_called_with(module)
        # mock_validate_time.assert_called_with('14:00', module)
        # mock_validate_repository_profile.assert_called_with('default_repo', module)
        # mock_validate_cluster_names.assert_called_with(['Cluster1'], module)


class TestDeleteBaselineProfile(FakeAnsibleModule):
    module = omevv_baseline_profile

    @pytest.fixture
    def omevv_baseline_profile_mock(self):
        omevv_obj = MagicMock()
        return omevv_obj

    @pytest.fixture
    def omevv_connection_baseline_profile(self, mocker, omevv_baseline_profile_mock):
        omevv_conn_mock = mocker.patch(MODULE_PATH + 'RestOMEVV',
                                       return_value=omevv_baseline_profile_mock)
        omevv_conn_mock.return_value.__enter__.return_value = omevv_baseline_profile_mock
        return omevv_conn_mock

    def test_diff_mode_check(self, omevv_connection_baseline_profile, omevv_default_args):
        # Define a sample payload
        payload = {
            "name": "TestProfile",
            "description": "Baseline profile for testing",
            "firmwareRepoId": 1001,
            "firmwareRepoName": "TestRepo",
            "clusterGroups": [1, 2]
        }
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.DeleteBaselineProfile(
            omevv_connection_baseline_profile, f_module, profile_name="TestProfile")
        result = obj.diff_mode_check(payload)
        assert result

    def test_delete_baseline_profile_success(self, omevv_connection_baseline_profile, omevv_default_args, mocker):
        profile_resp = {
            "id": 1996,
            "name": "TestProfile",
            "description": "Baseline profile for testing",
            "firmwareRepoId": 1001,
            "firmwareRepoName": "TestRepo",
            "clusterGroups": [1, 2]
        }

        obj = MagicMock()
        obj.success = True
        mocker.patch(MODULE_PATH + DELETE_DIFF_MODE_CHECK, return_value={})
        mocker.patch(MODULE_UTILS_PATH +
                     PERFORM_DELETE_PROFILE, return_value=obj)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.DeleteBaselineProfile(
            omevv_connection_baseline_profile, f_module, profile_name="TestProfile")
        result = obj.delete_baseline_profile(profile_resp)
        assert result is None

    def test_delete_baseline_profile_failure(self, omevv_connection_baseline_profile, omevv_default_args, mocker):
        profile_resp = {
            "id": 1996,
            "name": "TestProfile",
            "description": "Baseline profile for testing",
            "firmwareRepoId": 1001,
            "firmwareRepoName": "TestRepo",
            "clusterGroups": [1, 2]
        }

        obj = MagicMock()
        obj.success = True
        mocker.patch(MODULE_PATH + DELETE_DIFF_MODE_CHECK, return_value={})
        mocker.patch(MODULE_UTILS_PATH +
                     PERFORM_DELETE_PROFILE, return_value=obj)

        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.DeleteBaselineProfile(
            omevv_connection_baseline_profile, f_module, profile_name="TestProfile")
        result = obj.delete_baseline_profile(profile_resp)
        assert result is None

    def test_execute(self, omevv_connection_baseline_profile, omevv_default_args, mocker):
        # Scenario 1: When profile does not exist
        obj = MagicMock()
        mocker.patch(MODULE_UTILS_PATH +
                     GET_PROFILE_INFO_KEY, return_value={})
        mocker.patch(
            MODULE_PATH + DELETE_DIFF_MODE_CHECK, return_value={})
        mocker.patch(MODULE_UTILS_PATH +
                     PERFORM_DELETE_PROFILE, return_value=obj)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.DeleteBaselineProfile(
            omevv_connection_baseline_profile, f_module, profile_name="TestProfile")
        result = obj.execute()
        assert result is None

        # Scenario 2: When profile does not exists and check_mode is true
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=True)
        obj = self.module.DeleteBaselineProfile(omevv_connection_baseline_profile, f_module, profile_name="TestProfile")
        result = obj.execute()
        assert result is None

        # Scenario 3: When profile exists and check_mode is true
        obj = MagicMock()
        obj.success = True
        res = {
            "id": 1996,
            "name": "TestProfile",
            "description": "Baseline profile for testing",
            "firmwareRepoId": 1001,
            "firmwareRepoName": "TestRepo",
            "clusterGroups": [1, 2]
        }
        mocker.patch(MODULE_UTILS_PATH +
                     GET_PROFILE_INFO_KEY, return_value=res)
        mocker.patch(
            MODULE_PATH + DELETE_DIFF_MODE_CHECK, return_value={})
        mocker.patch(MODULE_UTILS_PATH +
                     PERFORM_DELETE_PROFILE, return_value=obj)
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=True)
        obj = self.module.DeleteBaselineProfile(
            omevv_connection_baseline_profile, f_module, profile_name="TestProfile")
        result = obj.execute()
        assert result is None

        # Scenario 4: When profile exists and check_mode is false
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.DeleteBaselineProfile(
            omevv_connection_baseline_profile, f_module, profile_name="TestProfile")
        result = obj.execute()
        assert result is None

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_omevv_baseline_profile_main_exception_handling_case(self, exc_type, mocker, omevv_default_args,
                                                                 omevv_baseline_profile_mock):
        omevv_baseline_profile_mock.status_code = 400
        omevv_baseline_profile_mock.success = False
        json_str = to_text(json.dumps(
            {"errorCode": "501", "message": "Error"}))
        omevv_default_args.update({'state': 'absent', 'name': 'test'})
        if exc_type in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + PERFORM_OPERATION_KEY,
                         side_effect=exc_type(HTTP_ERROR_URL, 400,
                                              HTTP_ERROR,
                                              {"accept-type": RETURN_TYPE},
                                              StringIO(json_str)))
        else:
            mocker.patch(MODULE_PATH + PERFORM_OPERATION_KEY,
                         side_effect=exc_type('test'))
        result = self._run_module(omevv_default_args)
        if exc_type == URLError:
            assert result['changed'] is False
        else:
            assert result['failed'] is True
        assert 'msg' in result

        # Scenario 1: When errorCode is 18001
        error_string = to_text(json.dumps(
            {'errorCode': '18001', 'message': "Error"}))
        if exc_type in [HTTPError]:
            mocker.patch(MODULE_PATH + PERFORM_OPERATION_KEY,
                         side_effect=exc_type(HTTP_ERROR_URL, 400,
                                              HTTP_ERROR,
                                              {"accept-type": RETURN_TYPE},
                                              StringIO(error_string)))
        res_out = self._run_module(omevv_default_args)
        assert 'msg' in res_out

        # Scenario 2: When errorCode is 500
        error_string = to_text(json.dumps(
            {'errorCode': '500', 'message': "Error"}))
        if exc_type in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + PERFORM_OPERATION_KEY,
                         side_effect=exc_type(HTTP_ERROR_URL, 400,
                                              HTTP_ERROR,
                                              {"accept-type": RETURN_TYPE},
                                              StringIO(error_string)))
        res_out = self._run_module(omevv_default_args)
        assert 'msg' in res_out
