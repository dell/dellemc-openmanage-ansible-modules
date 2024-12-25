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
from ansible_collections.dellemc.openmanage.plugins.modules.omevv_baseline_profile import ModifyBaselineProfile
from urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from io import StringIO
from unittest.mock import MagicMock
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.omevv_baseline_profile.'
MODULE_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.omevv_utils.omevv_firmware_utils.'
INFO_UTILS = "ansible_collections.dellemc.openmanage.plugins.module_utils.omevv_utils.omevv_info_utils."
UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.'
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
CREATE_DIFF_MODE_CHECK = "CreateBaselineProfile.diff_mode_check"
MODIFY_DIFF_MODE_CHECK = "ModifyBaselineProfile.diff_mode_check"
DELETE_DIFF_MODE_CHECK = "DeleteBaselineProfile.diff_mode_check"
DELETE_EXECUTE = "DeleteBaselineProfile.execute"
COMMON = "BaselineProfile.validate_common_params"
CHANGES_FOUND_MSG = "Changes found to be applied."
GET_REPO_ID = "OMEVVBaselineProfile.get_repo_id_by_name"
GET_CLUSTER_ID = "OMEVVBaselineProfile.get_cluster_id"
GET_GROUP_ID = "OMEVVBaselineProfile.get_group_ids_for_clusters"
GET_JOB_SCHEDULE = "OMEVVBaselineProfile.create_job_schedule"
GET_CURRENT_JOB_SCHEDULE = "OMEVVBaselineProfile.get_current_job_schedule"
ADD_REMOVE_GROUP_ID = "OMEVVBaselineProfile.get_add_remove_group_ids"
CLUSTER_INFO = "OMEVVInfo.get_cluster_info"
GET_GROUP_ID_CLUSTER = "OMEVVInfo.get_group_id_of_cluster"
HTTP_ERROR = "http error message"
HTTP_ERROR_URL = 'https://testhost.com'
RETURN_TYPE = "application/json"
PROFILE_NAME = "Dell Default Catalog"
PROFILE_TEST = "profile-test"
CLUSTER_NAME = "My Cluster"
BASELINE_PROFILE = "Baseline profile for testing"
DESCRIPTION = "Latest Baseline From Dell"
JOB_SCHEDULE = {"monday": False, "tuesday": False, "wednesday": False,
                "thursday": True, "friday": True, "saturday": True, "time": "05:30", "sunday": True}


class TestBaselineProfile(FakeAnsibleModule):
    module = omevv_baseline_profile

    @pytest.fixture
    def omevv_baseline_profile_mock(self):
        omevv_obj = MagicMock()
        return omevv_obj

    @pytest.fixture
    def omevv_connection_baseline_profile(self, mocker, omevv_baseline_profile_mock):
        omevv_conn_mock = mocker.patch(
            MODULE_PATH + 'RestOMEVV', return_value=omevv_baseline_profile_mock)
        omevv_conn_mock.return_value.__enter__.return_value = omevv_baseline_profile_mock
        return omevv_conn_mock

    def test_execute(self, omevv_default_args, omevv_connection_baseline_profile):
        obj = MagicMock()
        omevv_obj = self.module.BaselineProfile(
            omevv_connection_baseline_profile, obj)
        omevv_obj.execute()

    def test_validate_common_params(self, omevv_connection_baseline_profile, omevv_default_args, mocker):
        obj = MagicMock()
        obj.success = True
        mocker.patch(
            MODULE_PATH + 'validate_job_wait', return_value=True)
        mocker.patch(
            MODULE_PATH + 'validate_time', return_value=None)
        mocker.patch(MODULE_UTILS_PATH +
                     'OMEVVBaselineProfile.validate_repository_profile', return_value=(True, ""))
        mocker.patch(MODULE_UTILS_PATH +
                     'OMEVVBaselineProfile.validate_cluster_names', return_value=(True, ""))
        f_module = self.get_module_mock(params=omevv_default_args)
        obj = self.module.BaselineProfile(
            omevv_connection_baseline_profile, f_module)
        result = obj.validate_common_params()
        assert result is None

        # Scenario 2: When validate_repository_profile fails
        mocker.patch(MODULE_UTILS_PATH +
                     'OMEVVBaselineProfile.validate_repository_profile', return_value=(False, ""))
        f_module = self.get_module_mock(params=omevv_default_args)
        obj = self.module.BaselineProfile(
            omevv_connection_baseline_profile, f_module)
        result = obj.validate_common_params()
        assert result is None

        # Scenario 3: When validate_cluster_names fails
        mocker.patch(MODULE_UTILS_PATH +
                     'OMEVVBaselineProfile.validate_cluster_names', return_value=(False, ""))
        f_module = self.get_module_mock(params=omevv_default_args)
        obj = self.module.BaselineProfile(
            omevv_connection_baseline_profile, f_module)
        result = obj.validate_common_params()
        assert result is None

        # Scenario 4: When validate_job_wait fails
        mocker.patch(
            MODULE_PATH + 'validate_job_wait', return_value=False)
        f_module = self.get_module_mock(params=omevv_default_args)
        obj = self.module.BaselineProfile(
            omevv_connection_baseline_profile, f_module)
        result = obj.validate_common_params()
        assert result is None


class TestCreateBaselineProfile(FakeAnsibleModule):
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

        payload = {
            "name": "baseline_profile_test",
            "firmwareRepoId": "repo1234",
            "groupIds": ["group1", "group2"],
            "jobSchedule": {
                "days": "Monday",
                "time": "12:00"
            }
        }
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.CreateBaselineProfile(
            omevv_connection_baseline_profile, f_module)
        result = obj.diff_mode_check(payload)
        assert result

        # with description
        payload = {
            "name": "baseline_profile_test",
            "firmwareRepoId": "repo1234",
            "description": "API",
            "groupIds": ["group1", "group2"],
            "jobSchedule": {
                "days": "Monday",
                "time": "12:00"
            }
        }
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.CreateBaselineProfile(
            omevv_connection_baseline_profile, f_module)
        result = obj.diff_mode_check(payload)
        assert result

    def test_perform_create_baseline_profile_success(self, omevv_connection_baseline_profile, omevv_default_args, mocker):
        obj = MagicMock()
        # Scenario 1: When creation is success
        obj.success = True
        payload = {
            "name": BASELINE_PROFILE,
            "description": "API",
            "firmwareRepoId": 1000,
            "groupIds": [
                1012
            ],
            "jobSchedule": JOB_SCHEDULE
        }

        obj2 = {
            'id': 1124,
            'name': PROFILE_TEST,
            'description': 'TEST',
            'consoleId': '1234-5678',
            'firmwareRepoId': 1000,
            'firmwareRepoName': PROFILE_NAME,
            "lastmodifiedBy": "OMEVV",
            "version": "1.0.0-0",
            "clusterGroups": [{"clusterID": "domain-c1048", "clusterName": CLUSTER_NAME, "omevv_groupID": 1038}],
            "baselineType": "CLUSTER",
            "status": "SUCCESSFUL"}

        obj3 = {
            'id': 1124,
            'name': PROFILE_TEST,
            'description': 'TEST',
            'consoleId': '1234-5678',
            'firmwareRepoId': 1000,
            'firmwareRepoName': PROFILE_NAME,
            "lastmodifiedBy": "OMEVV",
            "clusterGroups": [{"clusterID": "domain-c1048", "clusterName": CLUSTER_NAME, "omevv_groupID": 1038}],
            "baselineType": "CLUSTER",
            "status": "CREATING"}

        mocker.patch(
            MODULE_PATH + CREATE_DIFF_MODE_CHECK, return_value={})
        mocker.patch(MODULE_UTILS_PATH +
                     PERFORM_CREATE_PROFILE, return_value=(obj, ""))
        mocker.patch(MODULE_UTILS_PATH +
                     GET_PROFILE_BY_ID, side_effect=[obj3, obj2])
        mocker.patch(MODULE_PATH +
                     'time.sleep', return_value=None)
        mocker.patch(MODULE_UTILS_PATH +
                     GET_PROFILE_INFO_KEY, return_value=obj2)
        f_module = self.get_module_mock(params=omevv_default_args)
        obj = self.module.CreateBaselineProfile(
            omevv_connection_baseline_profile, f_module)
        result = obj.perform_create_baseline_profile(payload)
        assert result is None

    def test_perform_create_baseline_profile_failure(self, omevv_connection_baseline_profile, omevv_default_args, mocker):
        obj = MagicMock()
        obj.success = False
        payload = {
            "name": BASELINE_PROFILE,
            "description": "API",
            "firmwareRepoId": 1000,
            "groupIds": [
                1012
            ],
            "jobSchedule": JOB_SCHEDULE
        }
        mocker.patch(
            MODULE_PATH + CREATE_DIFF_MODE_CHECK, return_value={})
        mocker.patch(MODULE_UTILS_PATH +
                     PERFORM_CREATE_PROFILE, return_value=(obj, ""))
        f_module = self.get_module_mock(params=omevv_default_args)
        obj = self.module.CreateBaselineProfile(
            omevv_connection_baseline_profile, f_module)
        result = obj.perform_create_baseline_profile(payload)
        assert result is None

    def test_perform_create_baseline_profile_api_response_failure(self, omevv_connection_baseline_profile, omevv_default_args, mocker):
        # Senario 3: When creation is failed because api_response's status is failed
        payload = {
            "name": BASELINE_PROFILE,
            "description": "API",
            "firmwareRepoId": 1000,
            "groupIds": [
                1012
            ],
            "jobSchedule": JOB_SCHEDULE
        }
        failed_resp = {
            'id': 1124,
            'name': PROFILE_TEST,
            'description': 'TEST',
            'consoleId': '1234-5678',
            'firmwareRepoId': 1000,
            "status": "FAILED"}

        mocker.patch(
            MODULE_PATH + CREATE_DIFF_MODE_CHECK, return_value={})
        mocker.patch(MODULE_UTILS_PATH +
                     GET_PROFILE_BY_ID, return_value=failed_resp)
        f_module = self.get_module_mock(params=omevv_default_args)
        obj = self.module.CreateBaselineProfile(
            omevv_connection_baseline_profile, f_module)
        result = obj.perform_create_baseline_profile(payload)
        assert result is None

    def test_execute(self, omevv_connection_baseline_profile, omevv_default_args, mocker):
        ob = {'id': 1124, 'status': 'SUCCESSFUL'}
        job_schedule = JOB_SCHEDULE
        mocker.patch(
            MODULE_PATH + 'BaselineProfile.validate_common_params', return_value=None)
        mocker.patch(MODULE_UTILS_PATH +
                     GET_REPO_ID, return_value=1234)
        mocker.patch(MODULE_UTILS_PATH +
                     GET_CLUSTER_ID, return_value=[1234, 5678])
        mocker.patch(MODULE_UTILS_PATH +
                     GET_JOB_SCHEDULE, return_value=job_schedule)
        mocker.patch(
            MODULE_PATH + CREATE_DIFF_MODE_CHECK, return_value={})
        mocker.patch(
            MODULE_PATH + 'CreateBaselineProfile.perform_create_baseline_profile', return_value=ob)
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=True)
        obj = self.module.CreateBaselineProfile(
            omevv_connection_baseline_profile, f_module)
        result = obj.execute()
        assert result is None

        # Scenario 2: If job_schedule is None
        mocker.patch(MODULE_UTILS_PATH +
                     GET_JOB_SCHEDULE, return_value=None)
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        obj = self.module.CreateBaselineProfile(
            omevv_connection_baseline_profile, f_module)
        result = obj.execute()
        assert result is None


class TestModifyBaselineProfile(FakeAnsibleModule):
    module = omevv_baseline_profile

    @pytest.fixture
    def omevv_baseline_profile_mock(self):
        omevv_obj = MagicMock()
        return omevv_obj

    @pytest.fixture
    def omevv_connection_baseline_profile(self, mocker, omevv_baseline_profile_mock):
        omevv_conn_mock = mocker.patch(
            MODULE_PATH + 'RestOMEVV', return_value=omevv_baseline_profile_mock)
        omevv_conn_mock.return_value.__enter__.return_value = omevv_baseline_profile_mock
        return omevv_conn_mock

    def test_diff_mode_check(self, omevv_connection_baseline_profile, omevv_default_args, mocker):

        payload = {
            "name": "baseline_profile_test",
            "firmwareRepoId": "repo1234",
            "groupIds": ["group1"],
            "jobSchedule": {
                "days": "Monday",
                "time": "12:00"
            },
            "cluster_groups": [
                {
                    "clusterID": 1234,
                    "clusterName": "cluster1",
                    "omevv_groupID": 1234
                }
            ],
            "description": "Original description"
        }
        existing_profile = {
            "name": "baseline_profile_test",
            "firmwareRepoId": "repo1234",
            "groupIds": ["group1"],
            "jobSchedule": {
                "days": "Monday",
                "time": "12:00"
            },
            "clusterGroups": [
                {
                    "clusterID": 1234,
                    "clusterName": "cluster1",
                    "omevv_groupID": 1234
                }
            ],
            "description": "Original description"
        }
        schedule = JOB_SCHEDULE
        ob = MagicMock()
        ob.json_data = schedule

        cluster_info = {"entityId": 1234}
        omevv_default_args['cluster'] = ["Cluster1"]

        mocker.patch(INFO_UTILS + CLUSTER_INFO, return_value=cluster_info)
        mocker.patch(INFO_UTILS + GET_GROUP_ID_CLUSTER, return_value=[1234])
        mocker.patch(MODULE_UTILS_PATH +
                     GET_CURRENT_JOB_SCHEDULE, return_value=ob)

        f_module = self.get_module_mock(params=omevv_default_args)

        obj = self.module.ModifyBaselineProfile(
            f_module,
            omevv_connection_baseline_profile,
            existing_profile
        )

        result = obj.diff_mode_check(payload)
        assert result

    def test_perform_modify_baseline_profile_success(self, omevv_connection_baseline_profile, omevv_default_args, mocker):
        obj = MagicMock()
        # Scenario 1: When modification is required
        obj.success = True
        payload = {
            "addgroupIds": [1038],
            "removeGroupIds": [1032],
            "jobSchedule": JOB_SCHEDULE,
            "description": "SUCCESS TEST",
            "configurationRepoId": 0,
            "firmwareRepoId": 1000,
            "driverRepoId": 0,
            "modifiedBy": "Administrator@VSPHERE.LOCAL"
        }

        existing_profile = {
            'id': 1124,
            'name': PROFILE_TEST,
            'description': 'TEST',
            'consoleId': '1234-5678',
            'firmwareRepoId': 1000,
            'firmwareRepoName': PROFILE_NAME,
            "lastmodifiedBy": "OMEVV",
            "clusterGroups": [{"clusterID": "domain-c1020", "clusterName": CLUSTER_NAME, "omevv_groupID": 1032}],
            "baselineType": "CLUSTER",
            "status": "SUCCESSFUL"}

        api_response = {
            'id': 1124,
            'name': PROFILE_TEST,
            'description': 'SUCCESS TEST',
            'consoleId': '1234-5678',
            'firmwareRepoId': 1000,
            'firmwareRepoName': PROFILE_NAME,
            "lastmodifiedBy": "OMEVV",
            "lastSuccessfulUpdatedTime": "2024-11-12T15:26:25.541Z",
            "clusterGroups": [{"clusterID": "domain-c1048", "clusterName": CLUSTER_NAME, "omevv_groupID": 1038}],
            "baselineType": "CLUSTER",
            "status": "MODIFYING"}

        mocker.patch(
            MODULE_PATH + MODIFY_DIFF_MODE_CHECK, return_value={})
        mocker.patch(MODULE_UTILS_PATH +
                     PERFORM_MODIFY_PROFILE, return_value=(obj, ""))
        mocker.patch(MODULE_UTILS_PATH +
                     GET_PROFILE_BY_ID, side_effect=[api_response, existing_profile])
        mocker.patch(MODULE_PATH +
                     'time.sleep', return_value=None)
        f_module = self.get_module_mock(params=omevv_default_args)
        obj = self.module.ModifyBaselineProfile(
            omevv_connection_baseline_profile, f_module, existing_profile)
        result = obj.perform_modify_baseline_profile(payload, existing_profile)
        assert result is None

    def test_perform_modify_baseline_profile_failure(self, omevv_connection_baseline_profile, omevv_default_args, mocker):
        # Scenario 2: When modification is not successful
        payload = {
            "addgroupIds": [1038],
            "removeGroupIds": [1032],
            "jobSchedule": JOB_SCHEDULE,
            "description": "SUCCESS TEST",
            "configurationRepoId": 0,
            "firmwareRepoId": 1000,
            "driverRepoId": 0,
            "modifiedBy": "Administrator@VSPHERE.LOCAL"
        }

        existing_profile = {
            'id': 1124,
            'name': PROFILE_TEST,
            'description': 'TEST',
            'consoleId': '1234-5678',
            'firmwareRepoId': 1000,
            'firmwareRepoName': PROFILE_NAME,
            "lastmodifiedBy": "OMEVV",
            "clusterGroups": [{"clusterID": "domain-c1020", "clusterName": CLUSTER_NAME, "omevv_groupID": 1032}],
            "baselineType": "CLUSTER",
            "status": "FAILED"}

        obj = MagicMock()
        obj.success = False
        mocker.patch(
            MODULE_PATH + MODIFY_DIFF_MODE_CHECK, return_value={})
        mocker.patch(MODULE_UTILS_PATH +
                     PERFORM_MODIFY_PROFILE, return_value=(obj, ""))
        f_module = self.get_module_mock(params=omevv_default_args)
        obj = self.module.ModifyBaselineProfile(
            omevv_connection_baseline_profile, f_module, existing_profile)
        result = obj.perform_modify_baseline_profile(payload, existing_profile)
        assert result is None

    def test_execute(self, omevv_connection_baseline_profile, omevv_default_args, mocker):
        # Scenario 1: When modificaton is required
        ob = {'id': 1124, 'status': 'SUCCESSFUL'}
        job_schedule = JOB_SCHEDULE

        existing_profile = {
            'id': 1124,
            'name': PROFILE_TEST,
            'description': 'TEST',
            'consoleId': '1234-5678',
            'firmwareRepoId': 1000,
            'firmwareRepoName': 'Dell Default Catalog',
            "lastmodifiedBy": "OMEVV",
            "version": "1.0.0-0",
            "lastSuccessfulUpdatedTime": "2024-11-12T15:26:25.541Z",
            "clusterGroups": [{"clusterID": "domain-c1020", "clusterName": CLUSTER_NAME, "omevv_groupID": 1032}],
            "datacenter_standAloneHostsGroups": [],
            "baselineType": "CLUSTER",
            "status": "SUCCESSFUL"}

        mocker.patch(
            MODULE_PATH + 'ModifyBaselineProfile.perform_modify_baseline_profile', return_value=ob)
        omevv_default_args.update(
            {"vcenter_uuid": "1234-5678", "cluster": "abcd"})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        obj = ModifyBaselineProfile(
            omevv_connection_baseline_profile, f_module, existing_profile)
        obj.validate_common_params = MagicMock(return_value=None)
        obj.omevv_baseline_obj.get_add_remove_group_ids = MagicMock(
            return_value=(None, None))
        omevv_default_args.update(
            {"vcenter_uuid": "1234-5678", "cluster": "abcd"})
        mocker.patch(MODULE_UTILS_PATH +
                     GET_JOB_SCHEDULE, return_value=job_schedule)
        obj.omevv_baseline_obj.get_repo_id_by_name = MagicMock(
            return_value=1234)
        obj.omevv_baseline_obj.create_job_schedule = MagicMock(
            return_value=job_schedule)
        obj.diff_mode_check = MagicMock(return_value={
            "before": {"description": "old_description", "jobSchedule": "old_schedule"},
            "after": {"description": "new_description", "jobSchedule": "new_schedule"}
        })
        result = obj.execute()
        assert result is None

        # Scenario 2: When diff is False
        obj.diff_mode_check = MagicMock(return_value={
            "before": {},
            "after": {}
        })
        result = obj.execute()
        assert result is None


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
            "description": BASELINE_PROFILE,
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

    def test_perform_delete_baseline_profile(self, omevv_connection_baseline_profile, omevv_default_args, mocker):
        profile_resp = {
            "id": 1996,
            "name": "TestProfile",
            "description": BASELINE_PROFILE,
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
        result = obj.perform_delete_baseline_profile(profile_resp)
        assert result is None

        # Scenario 2: When perform_delete_baseline_profile fails
        obj.success = False
        mocker.patch(MODULE_UTILS_PATH +
                     PERFORM_DELETE_PROFILE, return_value=obj)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.DeleteBaselineProfile(
            omevv_connection_baseline_profile, f_module, profile_name="TestProfile")
        result = obj.perform_delete_baseline_profile(profile_resp)
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
        obj = self.module.DeleteBaselineProfile(
            omevv_connection_baseline_profile, f_module, profile_name="TestProfile")
        result = obj.execute()
        assert result is None

        # Scenario 3: When profile exists and check_mode is true
        obj = MagicMock()
        obj.success = True
        res = {
            "id": 1996,
            "name": "TestProfile",
            "description": BASELINE_PROFILE,
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

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_omevv_baseline_profile_main_exception_handling_case(self, exc_type, mocker, omevv_default_args,
                                                                 omevv_baseline_profile_mock):
        omevv_baseline_profile_mock.status_code = 400
        omevv_baseline_profile_mock.success = False
        json_str = to_text(json.dumps(
            {"errorCode": "501", "message": "Error"}))
        omevv_default_args.update({'state': 'absent', 'name': 'test', 'validate_certs': False})
        if exc_type in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + DELETE_EXECUTE,
                         side_effect=exc_type(HTTP_ERROR_URL, 400,
                                              HTTP_ERROR,
                                              {"accept-type": RETURN_TYPE},
                                              StringIO(json_str)))
        else:
            mocker.patch(MODULE_PATH + DELETE_EXECUTE,
                         side_effect=exc_type('test'))
        result = self._run_module(omevv_default_args)
        if exc_type == URLError:
            assert result['changed'] is False
        else:
            assert result['failed'] is True
        assert 'msg' in result

        # Scenario 1: When errorCode is 404
        omevv_baseline_profile_mock.status_code = 404
        omevv_default_args.update({'state': 'absent', 'name': 'test', 'validate_certs': False})
        error_string = to_text(json.dumps(
            {'errorCode': '404', 'message': "The Requested resource cannot be found."}))
        if exc_type in [HTTPError]:
            mocker.patch(MODULE_PATH + DELETE_EXECUTE,
                         side_effect=exc_type(HTTP_ERROR_URL, 404,
                                              HTTP_ERROR,
                                              {"accept-type": RETURN_TYPE},
                                              StringIO(error_string)))
        res_out = self._run_module(omevv_default_args)
        assert 'msg' in res_out

        # Scenario 2: When errorCode is 500
        error_string = to_text(json.dumps(
            {'errorCode': '500', 'message': "Error"}))
        if exc_type in [HTTPError]:
            mocker.patch(MODULE_PATH + DELETE_EXECUTE,
                         side_effect=exc_type(HTTP_ERROR_URL, 500,
                                              HTTP_ERROR,
                                              {"accept-type": RETURN_TYPE},
                                              StringIO(error_string)))
        res_out = self._run_module(omevv_default_args)
        assert 'msg' in res_out

        # Scenario 3: When state is present
        params = {
            'state': 'present',
            'name': PROFILE_TEST,
            "repository_profile": "repository-profile",
            "cluster": ["cluster-1", "cluster-2"],
            "days": ["sunday", "wednesday"],
            "time": "22:10"}
        omevv_default_args.update(params)
        mocker.patch(MODULE_UTILS_PATH + GET_PROFILE_INFO_KEY, return_value={})
        res_out = self._run_module(omevv_default_args)
        assert 'msg' in res_out
