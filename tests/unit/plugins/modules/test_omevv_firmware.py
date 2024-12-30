# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.10.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
import datetime
from unittest.mock import MagicMock
from io import StringIO
from ansible_collections.dellemc.openmanage.plugins.modules.omevv_firmware import FirmwareUpdate, UpdateCluster
from ansible_collections.dellemc.openmanage.plugins.modules import omevv_firmware
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import AnsibleFailJSonException
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.omevv_firmware.'
UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.'
INFO_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.omevv_utils.omevv_info_utils.'
MODULE_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.omevv_utils.omevv_firmware_utils.'
SUCCESS_MSG = "Successfully retrieved the firmware repository profile information."
NO_PROFILE_MSG = "Unable to complete the operation because the '{profile_name}' is not a valid 'profile_name'."
FAILED_CONN_MSG = "Unable to complete the operation. Please check the connection details."
FAILED_MSG = "Unable to fetch the firmware repository profile information."
INVOKE_REQ_KEY = "RestOMEVV.invoke_request"
SUCCESS_UPDATE_SUBMIT_MSG = "Successfully submitted the firmware updated job."
SUCCESS_UPDATE_MSG = "Successfully completed the firmware update."
SUCCESS_UPDATE_SCHEDULED_MSG = "Successfully scheduled the firmware update job."
FAILED_UPDATE_MSG = "Failed to complete the firmware update."
INVALID_DATE_TIME_MSG = "Invalid date time. Enter a valid date time in the format of " \
                        "YYYY-MM-DDTHH:MM:SSZ."
MAINTENANCE_MODE_TIMEOUT_INVALID_MSG = "The value for the 'enter_maintenance_mode_timeout' " \
                                       "parameter must be between 60 and 1440."
CLUSTER_HOST_SERVICETAG_MUTUAL_EXCLUSIVE_MSG = "parameters are mutually " \
                                               "exclusive: cluster|host|servicetag."
CLUSTER_HOST_SERVICETSAG_REQUIRED_MSG = "Either 'cluster' or 'host' or 'servicetag' must " \
                                        "be specified."
UPDATE_JOB_PRESENT_MSG = "Update job is either running or in a scheduled state for cluster " \
                         "'{cluster_name}'. Wait for its completion and trigger."
JOB_NAME_ALREADY_EXISTS_MSG = "Job with name '{job_name}' already exists. Provide different name."
CLUSTER_HOST_NOT_FOUND_MSG = "No managed hosts found in the cluster."
HOST_NOT_FOUND_MSG = "Host '{managed_host}' not found under managed hosts."
CLUSTER_NOT_FOUND_MSG = "Provided cluster name '{cluster_name}' is not valid."
CHANGES_FOUND_MSG = "Changes found to be applied."
CHANGES_NOT_FOUND_MSG = "No changes found to be applied."
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The value for the 'job_wait_timeout' parameter cannot be " \
                               "negative or zero."
UNREACHABLE_MSG = "The URL with the {ip}:{port} cannot be reached."
FAILED_UPDATE_TIMEOUT_MSG = "Firmware update job timed out after {0} seconds."
SOURCE_NOT_FOUND_MSG = "The Requested resource cannot be found."
TRIGGER_UPDATE_CHECK_URI = "/Consoles/{vcenter_uuid}/CanTriggerUpdate"
UPDATE_CLUSTER_EXECUTE_JOB = "UpdateCluster.execute_update_job"
ANSIBLE_MODULE_EXIT_JSON = "ansible.module_utils.basic.AnsibleModule.exit_json"
OMEVV_INFO_FIRMWARE_DRIFT_INFO = "OMEVVInfo.get_firmware_drift_info_for_single_host"
UPDATE_CLUSTER_GET_TARGET = "UpdateCluster.get_target"
OMEVV_INFO_CLUSTER_GROUP_ID = "OMEVVInfo.get_group_id_of_cluster"
FIRM_UPDATE_HOST_SERVICETAG_EXISTENCE = "FirmwareUpdate.host_servicetag_existence"
UPDATE_CLUSTER_GET_HOST_ID = "UpdateCluster.get_host_id_either_host_or_service_tag"
UPDATE_CLUSTER_GET_HOST = "UpdateCluster.get_host_from_parameters"
OMEVV_FIRM_UPDATE_JOB_TRACK = "OMEVVFirmwareUpdate.firmware_update_job_track"
JOB_DESCRIPTION = "Test job description"
SLEEP_TIME = "time.sleep"


class TestFirmwareUpdate(FakeAnsibleModule):
    module = omevv_firmware

    @pytest.fixture
    def omevv_firmware_mock(self):
        omevv_obj = MagicMock()
        return omevv_obj

    @pytest.fixture
    def omevv_connection_firmware(self, mocker, omevv_firmware_mock):
        omevv_conn_mock = mocker.patch(MODULE_PATH + 'RestOMEVV',
                                       return_value=omevv_firmware_mock)
        omevv_conn_mock.return_value.__enter__.return_value = omevv_firmware_mock
        return omevv_conn_mock

    def test_get_payload_details(self, mocker, omevv_connection_firmware, omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        host_id = 123456
        parameters = {
            'targets': [{'firmware_components': ['component1']}],
            'check_vSAN_health': True,
            'run_now': True,
            'job_name': 'test_job',
            'job_description': JOB_DESCRIPTION,
        }

        # Mock module params
        mocker.patch.object(f_module, 'params', parameters)

        # Mock implementations
        mocker.patch.object(omevv_obj, 'set_firmware', wraps=omevv_obj.set_firmware)
        mocker.patch.object(omevv_obj, 'set_schedule', wraps=omevv_obj.set_schedule)
        mocker.patch.object(omevv_obj, 'set_job_details', wraps=omevv_obj.set_job_details)
        mocker.patch.object(omevv_obj, 'add_targets', wraps=omevv_obj.add_targets)

        # Execute the method
        result = omevv_obj.get_payload_details(host_id)

        # Verify result
        expected_result = {
            'firmware': {
                'targets': [
                    {
                        'firmwarecomponents': ['component1'],
                        'id': 123456,
                    }
                ],
                'checkvSANHealth': True,
                'deleteJobsQueue': None,
                'drsCheck': None,
                'enterMaintenanceModeOption': None,
                'enterMaintenanceModetimeout': None,
                'evacuateVMs': None,
                'exitMaintenanceMode': None,
                'maintenanceModeCountCheck': None,
                'rebootOptions': None,
                'resetIDrac': None,
            },
            'schedule': {
                'runNow': True,
            },
            'jobDescription': JOB_DESCRIPTION,
            'jobName': 'test_job',
        }

        assert result == expected_result

    def test_get_payload_details_scheduled(self, mocker, omevv_connection_firmware,
                                           omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        host_id = 123456
        parameters = {
            'targets': [{'firmware_components': ['component1']}],
            'check_vSAN_health': True,
            'run_now': False,
            'date_time': '2023-01-01T00:00:00Z',
            'job_name': 'test_job',
            'job_description': JOB_DESCRIPTION,
        }

        # Mock module params
        mocker.patch.object(f_module, 'params', parameters)

        # Mock implementations
        mocker.patch.object(omevv_obj, 'set_firmware', wraps=omevv_obj.set_firmware)
        mocker.patch.object(omevv_obj, 'set_schedule', wraps=omevv_obj.set_schedule)
        mocker.patch.object(omevv_obj, 'set_job_details', wraps=omevv_obj.set_job_details)
        mocker.patch.object(omevv_obj, 'add_targets', wraps=omevv_obj.add_targets)

        # Execute the method
        result = omevv_obj.get_payload_details(host_id)

        # Verify result
        expected_result = {
            'firmware': {
                'targets': [
                    {
                        'firmwarecomponents': ['component1'],
                        'id': 123456,
                    },
                ],
                'checkvSANHealth': True,
                'deleteJobsQueue': None,
                'drsCheck': None,
                'enterMaintenanceModeOption': None,
                'enterMaintenanceModetimeout': None,
                'evacuateVMs': None,
                'exitMaintenanceMode': None,
                'maintenanceModeCountCheck': None,
                'rebootOptions': None,
                'resetIDrac': None,
            },
            'schedule': {
                'runNow': False,
                'dateTime': '2023-01-01T00:00:00Z',
            },
            'jobDescription': JOB_DESCRIPTION,
            'jobName': 'test_job',
        }

        assert result == expected_result

    def test_set_firmware(self, omevv_connection_firmware):
        value = {'check_vSAN_health': True}
        obj = MagicMock()
        omevv_obj = self.module.FirmwareUpdate(
            omevv_connection_firmware, obj)
        result = omevv_obj.set_firmware({}, value)
        assert result['checkvSANHealth'] == value['check_vSAN_health']

    def test_set_schedule(self, omevv_connection_firmware):
        obj = MagicMock()
        omevv_obj = self.module.FirmwareUpdate(
            omevv_connection_firmware, obj)
        result = omevv_obj.set_schedule({}, {})
        assert result == {'schedule': {'dateTime': None, 'runNow': None}}

    def test_set_job_details(self, omevv_connection_firmware):
        obj = MagicMock()
        omevv_obj = self.module.FirmwareUpdate(
            omevv_connection_firmware, obj)
        result = omevv_obj.set_job_details({}, {"job_name": "Test job name"})
        assert result == {'jobDescription': None,
                          'jobName': 'Test job name'}

    def test_set_job_details_job_description(self, omevv_connection_firmware,
                                             omevv_default_args):
        omevv_default_args.update({"job_description": JOB_DESCRIPTION})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        omevv_obj = FirmwareUpdate(f_module, omevv_connection_firmware)
        result = omevv_obj.set_job_details({}, {"job_name": "Test job name",
                                                "job_description": JOB_DESCRIPTION})
        assert result == {'jobDescription': JOB_DESCRIPTION,
                          'jobName': 'Test job name'}

    def test_add_targets_device_id_list(self, omevv_connection_firmware):
        obj = MagicMock()
        omevv_obj = self.module.FirmwareUpdate(
            omevv_connection_firmware, obj)
        target_list = [
            {'firmware_components': 1}
        ]
        result = omevv_obj.add_targets({'targets': []}, target_list, [100, 101])
        assert result == {'targets': [{'firmwarecomponents': 1, 'id': 100},
                                      {'firmwarecomponents': 1, 'id': 101}]}

    def test_add_targets_device_id_string(self, omevv_connection_firmware):
        obj = MagicMock()
        omevv_obj = self.module.FirmwareUpdate(
            omevv_connection_firmware, obj)
        target_list = [
            {'firmware_components': 1}
        ]
        result = omevv_obj.add_targets({'targets': []}, target_list, 100)
        assert result == {'targets': [{'firmwarecomponents': 1, 'id': 100}]}

    def test_host_servicetag_existence(self, omevv_connection_firmware, omevv_default_args):
        omevv_default_args.update({"targets": [{'cluster': 'cluster_a',
                                                'host': 123456,
                                                'servicetag': 'SVCTAG1'}]})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        omevv_obj = FirmwareUpdate(f_module, omevv_connection_firmware)
        try:
            omevv_obj.host_servicetag_existence()
        except AnsibleFailJSonException as err:
            assert err.args[0] == CLUSTER_HOST_SERVICETAG_MUTUAL_EXCLUSIVE_MSG
            assert err.fail_kwargs.get('failed') is True

    def test_host_servicetag_existence_not_exits(self, omevv_connection_firmware,
                                                 omevv_default_args):
        omevv_default_args.update({"targets": [{}]})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        omevv_obj = FirmwareUpdate(f_module, omevv_connection_firmware)
        try:
            omevv_obj.host_servicetag_existence()
        except AnsibleFailJSonException as err:
            assert err.args[0] == CLUSTER_HOST_SERVICETSAG_REQUIRED_MSG
            assert err.fail_kwargs.get('failed') is True

    def test_validate_date_time_invalid(self, omevv_connection_firmware,
                                        omevv_default_args):
        omevv_default_args.update({"date_time": "2020-13-01T00:00:00Z"})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        omevv_obj = FirmwareUpdate(f_module, omevv_connection_firmware)
        try:
            omevv_obj.validate_date_time()
        except AnsibleFailJSonException as err:
            assert err.args[0] == INVALID_DATE_TIME_MSG
            assert err.fail_kwargs.get('failed') is True

    def test_validate_date_time_valid(self, omevv_connection_firmware, omevv_default_args):
        omevv_default_args.update({"date_time": "2020-11-01T00:00:00Z"})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        omevv_obj = FirmwareUpdate(f_module, omevv_connection_firmware)
        result = omevv_obj.validate_date_time()
        assert result == datetime.datetime(2020, 11, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)

    def test_enter_maintenance_mode_timeout(self, omevv_connection_firmware,
                                            omevv_default_args):
        omevv_default_args.update({"enter_maintenance_mode_timeout": 59})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        omevv_obj = FirmwareUpdate(f_module, omevv_connection_firmware)
        try:
            omevv_obj.enter_maintenance_mode_timeout()
        except AnsibleFailJSonException as err:
            assert err.args[0] == MAINTENANCE_MODE_TIMEOUT_INVALID_MSG

    def test_validate_params(self, mocker, omevv_connection_firmware, omevv_default_args):
        omevv_default_args.update({"job_wait_timeout": 0})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        omevv_obj = FirmwareUpdate(f_module, omevv_connection_firmware)
        mocker.patch(MODULE_PATH + FIRM_UPDATE_HOST_SERVICETAG_EXISTENCE, return_value=None)
        try:
            omevv_obj.validate_params()
        except AnsibleFailJSonException as err:
            assert err.args[0] == TIMEOUT_NEGATIVE_OR_ZERO_MSG
            assert err.fail_kwargs.get('failed') is True

    def test_validate_params_job_wait_false(self, mocker, omevv_connection_firmware,
                                            omevv_default_args):
        omevv_default_args.update({"enter_maintenance_mode_timeout": 61})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        omevv_obj = FirmwareUpdate(f_module, omevv_connection_firmware)
        mocker.patch(MODULE_PATH + FIRM_UPDATE_HOST_SERVICETAG_EXISTENCE, return_value=None)
        mocker.patch(UTILS_PATH + 'validate_job_wait', return_value=False)
        result = omevv_obj.validate_params()
        assert result is None


class TestUpdateCluster(FakeAnsibleModule):
    module = omevv_firmware

    @pytest.fixture
    def omevv_firmware_mock(self):
        omevv_obj = MagicMock()
        return omevv_obj

    @pytest.fixture
    def omevv_connection_firmware(self, mocker, omevv_firmware_mock):
        omevv_conn_mock = mocker.patch(MODULE_PATH + 'RestOMEVV',
                                       return_value=omevv_firmware_mock)
        omevv_conn_mock.return_value.__enter__.return_value = omevv_firmware_mock
        return omevv_conn_mock

    def test_execute_check_mode_false(self, mocker, omevv_connection_firmware,
                                      omevv_default_args):
        omevv_default_args.update({"targets": []})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)
        mocker.patch(MODULE_PATH + 'FirmwareUpdate.validate_params', return_value=None)
        target = {"cluster": "cluster1"}
        mocker.patch(MODULE_PATH + UPDATE_CLUSTER_GET_TARGET, return_value=target)
        value = (1034, {}, 1001)
        mocker.patch(MODULE_PATH + 'UpdateCluster.process_cluster_target', return_value=value)
        mocker.patch(MODULE_PATH + 'UpdateCluster.is_firmware_update_needed',
                     return_value=(False, 2, 3))
        mocker.patch(MODULE_PATH + 'UpdateCluster.is_update_job_allowed', return_value=True)
        mocker.patch(MODULE_PATH + 'UpdateCluster.is_job_name_existing', return_value=None)
        mocker.patch(MODULE_PATH + 'UpdateCluster.handle_check_mode', return_value=None)
        mocker.patch(MODULE_PATH + 'UpdateCluster.handle_firmware_update', return_value=True)
        try:
            omevv_obj.execute()
        except AnsibleFailJSonException as err:
            assert err.args[0] == CHANGES_NOT_FOUND_MSG

    def test_process_cluster_target(self, mocker, omevv_connection_firmware,
                                    omevv_default_args):
        omevv_default_args.update({"targets": [{'host': 123456,
                                               'cluster': 'cluster_a'}]})
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=True)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)
        target = [123456, 123457]
        mocker.patch(MODULE_PATH + UPDATE_CLUSTER_GET_HOST_ID, return_value=target)
        cluster_name_value = "cluster_a"
        mocker.patch(INFO_UTILS_PATH + OMEVV_INFO_CLUSTER_GROUP_ID,
                     return_value=cluster_name_value)
        payload = {}
        mocker.patch(MODULE_PATH + 'FirmwareUpdate.get_payload_details', return_value=payload)
        target = {'cluster': 'cluster_a'}
        result = omevv_obj.process_cluster_target(target)
        assert result == ('cluster_a', {}, 123456)

    def test_process_cluster_target_no_hosts(self, mocker, omevv_connection_firmware,
                                             omevv_default_args):
        omevv_default_args.update({"targets": [{'host': 123456}]})
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=True)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)
        target = [None, 123457]
        mocker.patch(MODULE_PATH + UPDATE_CLUSTER_GET_HOST_ID, return_value=target)
        targets = {'cluster': 'cluster_a'}
        try:
            omevv_obj.process_cluster_target(targets)
        except AnsibleFailJSonException as err:
            assert err.args[0] == CLUSTER_HOST_NOT_FOUND_MSG

    def test_process_non_cluster_target(self, mocker,
                                        omevv_connection_firmware,
                                        omevv_default_args):
        omevv_default_args.update({"parameters": [{'host': 123456,
                                                   'cluster': 'cluster_a'}]})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=True)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)
        target = {"cluster": "cluster1"}
        mocker.patch(MODULE_PATH + UPDATE_CLUSTER_GET_TARGET, return_value=target)
        target = [123456, 123457]
        mocker.patch(MODULE_PATH + UPDATE_CLUSTER_GET_HOST, return_value=target)
        cluster_name_value = "cluster_a"
        mocker.patch(INFO_UTILS_PATH + 'OMEVVInfo.get_cluster_name',
                     return_value=cluster_name_value)
        group_id_value = 1357
        mocker.patch(INFO_UTILS_PATH + OMEVV_INFO_CLUSTER_GROUP_ID,
                     return_value=group_id_value)
        payload = {}
        mocker.patch(MODULE_PATH + 'FirmwareUpdate.get_payload_details', return_value=payload)
        parameters = {'targets': [{'host': 123456, 'cluster': 'cluster_a'}]}
        result = omevv_obj.process_non_cluster_target(parameters)
        assert result == ('cluster_a', 1357, {}, 123456)

    def test_process_non_cluster_target_not_valid_host(self, mocker,
                                                       omevv_connection_firmware,
                                                       omevv_default_args):
        omevv_default_args.update({"parameters": [{'host': 123456,
                                                   'cluster': 'cluster_a'}]})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=True)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)
        target = {"cluster": "cluster1", "host": 123456}
        mocker.patch(MODULE_PATH + UPDATE_CLUSTER_GET_TARGET, return_value=target)
        target = [None, 123457]
        mocker.patch(MODULE_PATH + UPDATE_CLUSTER_GET_HOST, return_value=target)
        parameters = {'targets': [{'host': None, 'cluster': 'cluster_a'}]}
        try:
            omevv_obj.process_non_cluster_target(parameters)
        except AnsibleFailJSonException as err:
            assert err.args[0] == "Host '123456' not found under managed hosts."

    def test_process_non_cluster_target_not_valid_servicetag(self, mocker,
                                                             omevv_connection_firmware,
                                                             omevv_default_args):
        omevv_default_args.update({"parameters": [{'host': 123456,
                                                   'cluster': 'cluster_a'}]})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=True)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)
        target = {"cluster": "cluster1", "host": None, "servicetag": "invalid_servicetag"}
        mocker.patch(MODULE_PATH + UPDATE_CLUSTER_GET_TARGET, return_value=target)
        target = [None, 123457]
        mocker.patch(MODULE_PATH + UPDATE_CLUSTER_GET_HOST, return_value=target)
        parameters = {'targets': [{'host': None, 'cluster': 'cluster_a'}]}
        try:
            omevv_obj.process_non_cluster_target(parameters)
        except AnsibleFailJSonException as err:
            assert err.args[0] == "Host 'invalid_servicetag' not found under managed hosts."

    def test_get_host_from_parameters(self, mocker,
                                      omevv_connection_firmware,
                                      omevv_default_args):
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=True)
        target = {"cluster": "cluster1", "host": 123456}
        mocker.patch(MODULE_PATH + UPDATE_CLUSTER_GET_TARGET, return_value=target)
        mocker.patch(MODULE_PATH + UPDATE_CLUSTER_GET_HOST_ID, return_value=(3, 4))
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)
        result = omevv_obj.get_host_from_parameters(1, {'targets': target})
        assert result == (None, None)

    def test_get_host_from_parameters_no_cluster(self, mocker,
                                                 omevv_connection_firmware,
                                                 omevv_default_args):
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=True)
        target = {"cluster": "", "host": 123456}
        mocker.patch(MODULE_PATH + UPDATE_CLUSTER_GET_TARGET, return_value=target)
        mocker.patch(MODULE_PATH + UPDATE_CLUSTER_GET_HOST_ID, return_value=(3, 4))
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)
        result = omevv_obj.get_host_from_parameters(1, {'targets': target})
        assert result == (3, 4)

    def test_handle_check_mode_firmware_update_needed_change(self,
                                                             omevv_connection_firmware,
                                                             omevv_default_args):
        omevv_default_args.update({"_ansible_diff": True})
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=True)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        # Setup the parameters for the test
        firmware_update_needed = True
        before_dict = {'component2': {'firmwareversion': '2.0.0'}}
        after_dict = {'component2': {'firmwareversion': '2.0.1'}}

        # Execute the method with change
        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.handle_check_mode(firmware_update_needed,
                                        before_dict, after_dict)

        assert excinfo.value.args[0] == CHANGES_FOUND_MSG

    def test_handle_check_mode_firmware_update_needed_no_diff(self,
                                                              omevv_connection_firmware,
                                                              omevv_default_args):
        omevv_default_args.update({"_ansible_diff": False})
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=True)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        # Setup the parameters for the test
        firmware_update_needed = True
        before_dict = {}
        after_dict = {}

        # Execute the method without diff
        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.handle_check_mode(firmware_update_needed,
                                        before_dict, after_dict)

        assert excinfo.value.args[0] == CHANGES_FOUND_MSG

    def test_handle_check_mode_no_firmware_update_needed_with_diff(self,
                                                                   omevv_connection_firmware,
                                                                   omevv_default_args):
        omevv_default_args.update({"_ansible_diff": True})
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=True)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        # Setup the parameters for the test
        firmware_update_needed = False
        before_dict = {}
        after_dict = {}

        # Execute the method with no change
        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.handle_check_mode(firmware_update_needed,
                                        before_dict, after_dict)

        assert excinfo.value.args[0] == CHANGES_NOT_FOUND_MSG

    def test_handle_check_mode_no_firmware_update_needed_no_diff(self,
                                                                 omevv_connection_firmware,
                                                                 omevv_default_args):
        omevv_default_args.update({"_ansible_diff": False})
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=True)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        # Setup the parameters for the test
        firmware_update_needed = False
        before_dict = {}
        after_dict = {}

        # Execute the method without diff and no change
        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.handle_check_mode(firmware_update_needed,
                                        before_dict, after_dict)

        assert excinfo.value.args[0] == CHANGES_NOT_FOUND_MSG

    def test_handle_check_mode_changes_needed_with_diff(self, mocker, omevv_connection_firmware,
                                                        omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=True)
        f_module._diff = True  # Enable diff support
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        firmware_update_needed = True
        before_dict = {'component2': {'firmwareversion': '2.0.0'}}
        after_dict = {'component2': {'firmwareversion': '3.0.0'}}

        # Mock the exit_json method to capture the result
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON,
                     side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.handle_check_mode(firmware_update_needed,
                                        before_dict, after_dict)

        # Verify the exit message for changes found with diff
        assert excinfo.value.args[0] == CHANGES_FOUND_MSG

    def test_handle_check_mode_changes_needed_without_diff(self, mocker, omevv_connection_firmware,
                                                           omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=True)
        f_module._diff = False  # Disable diff support
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        firmware_update_needed = True
        before_dict = {'component2': {'firmwareversion': '2.0.0'}}
        after_dict = {'component2': {'firmwareversion': '3.0.0'}}

        # Mock the exit_json method to capture the result
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON,
                     side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.handle_check_mode(firmware_update_needed, before_dict, after_dict)

        # Verify the exit message for changes found without diff
        assert excinfo.value.args[0] == CHANGES_FOUND_MSG

    def test_handle_check_mode_no_changes_needed_with_diff(self, mocker, omevv_connection_firmware,
                                                           omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=True)
        f_module._diff = True  # Enable diff support
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        firmware_update_needed = False
        before_dict = {'component2': {'firmwareversion': '2.0.0'}}
        after_dict = {'component2': {'firmwareversion': '3.0.0'}}

        # Mock the exit_json method to capture the result
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON,
                     side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.handle_check_mode(firmware_update_needed, before_dict, after_dict)

        # Verify the exit message for no changes found with diff
        assert excinfo.value.args[0] == CHANGES_NOT_FOUND_MSG

    def test_handle_check_mode_no_changes_needed_without_diff(self, mocker,
                                                              omevv_connection_firmware,
                                                              omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=True)
        f_module._diff = False  # Disable diff support
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        firmware_update_needed = False
        before_dict = {'component2': {'firmwareversion': '2.0.0'}}
        after_dict = {'component2': {'firmwareversion': '3.0.0'}}

        # Mock the exit_json method to capture the result
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON,
                     side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.handle_check_mode(firmware_update_needed, before_dict, after_dict)

        # Verify the exit message for no changes found without diff
        assert excinfo.value.args[0] == CHANGES_NOT_FOUND_MSG

    def test_handle_firmware_update_run_now(self, mocker,
                                            omevv_connection_firmware,
                                            omevv_default_args):
        omevv_default_args.update({"run_now": True})
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        # Setup the parameters for the test
        vcenter_uuid = 'test_vcenter_uuid'
        cluster_group_id = 'test_cluster_group_id'
        payload = {'test_key': 'test_value'}
        parameters = omevv_default_args
        before_dict = {'component1': {'firmwareversion': '1.0.0'}}
        after_dict = {'component1': {'firmwareversion': '1.0.1'}}
        job_details = {'job_id': '12345'}

        mocker.patch(MODULE_PATH + UPDATE_CLUSTER_EXECUTE_JOB, return_value=job_details)

        # Mocking the exit method to capture the output
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON,
                     side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.handle_firmware_update(vcenter_uuid,
                                             cluster_group_id,
                                             payload, parameters,
                                             before_dict, after_dict)

        assert excinfo.value.args[0] == SUCCESS_UPDATE_MSG

    def test_handle_firmware_update_scheduled(self, mocker,
                                              omevv_connection_firmware,
                                              omevv_default_args):
        omevv_default_args.update({"run_now": False})
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        # Setup the parameters for the test
        vcenter_uuid = 'test_vcenter_uuid'
        cluster_group_id = 'test_cluster_group_id'
        payload = {'test_key': 'test_value'}
        parameters = omevv_default_args
        before_dict = {'component1': {'firmwareversion': '1.0.0'}}
        after_dict = {'component1': {'firmwareversion': '1.0.1'}}
        job_details = {'job_id': '12345'}

        mocker.patch(MODULE_PATH + UPDATE_CLUSTER_EXECUTE_JOB, return_value=job_details)

        # Mocking the exit method to capture the output
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON,
                     side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.handle_firmware_update(vcenter_uuid,
                                             cluster_group_id,
                                             payload, parameters,
                                             before_dict, after_dict)

        assert excinfo.value.args[0] == SUCCESS_UPDATE_SCHEDULED_MSG

    def test_handle_firmware_update_failed(self, mocker,
                                           omevv_connection_firmware,
                                           omevv_default_args):
        omevv_default_args.update({"run_now": True})
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        # Setup the parameters for the test
        vcenter_uuid = 'test_vcenter_uuid'
        cluster_group_id = 'test_cluster_group_id'
        payload = {'test_key': 'test_value'}
        parameters = omevv_default_args
        before_dict = {'component1': {'firmwareversion': '1.0.0'}}
        after_dict = {'component1': {'firmwareversion': '1.0.1'}}
        job_resp = None

        mocker.patch(MODULE_PATH + UPDATE_CLUSTER_EXECUTE_JOB, return_value=job_resp)
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON,
                     side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.handle_firmware_update(vcenter_uuid,
                                             cluster_group_id,
                                             payload, parameters,
                                             before_dict, after_dict)

        assert excinfo.value.args[0] == SUCCESS_UPDATE_MSG

    def test_get_target_single_target(self, omevv_connection_firmware, omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        # Setup the parameters for the test
        target_list = [
            {'cluster': 'cluster_a', 'host': 123456, 'servicetag': 'SVCTAG1'}
        ]

        # Execute the method
        result = omevv_obj.get_target(target_list)

        # Verify the result
        assert result == {'cluster': 'cluster_a', 'host': 123456, 'servicetag': 'SVCTAG1'}

    def test_get_target_multiple_targets(self,
                                         omevv_connection_firmware,
                                         omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        # Setup the parameters for the test
        target_list = [
            {'cluster': 'cluster_a', 'host': 123456, 'servicetag': 'SVCTAG1'},
            {'cluster': 'cluster_b', 'host': 123457, 'servicetag': 'SVCTAG2'}
        ]

        # Execute the method
        result = omevv_obj.get_target(target_list)

        # Verify the result
        assert result == {'cluster': 'cluster_a', 'host': 123456, 'servicetag': 'SVCTAG1'}

    def test_get_host_id_with_service_tag(self, mocker, omevv_connection_firmware, omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        # Setup the parameters for the test
        vcenter_uuid = 'test_vcenter_uuid'
        target = {'cluster': None, 'host': None, 'servicetag': 'SVCTAG1'}
        host_id = 123456
        host_service_tag = 'SVCTAG1'

        # Mocking the omevv_info_obj.get_host_id_either_host_or_service_tag method
        mocker.patch(INFO_UTILS_PATH + 'OMEVVInfo.get_host_id_either_host_or_service_tag', return_value=(host_id, host_service_tag))

        # Execute the method
        result_host_id, result_host_service_tag = omevv_obj.get_host_id_either_host_or_service_tag(vcenter_uuid, target)

        # Verify the result
        assert result_host_id == host_id
        assert result_host_service_tag == host_service_tag

    def test_get_host_id_with_host(self, mocker, omevv_connection_firmware, omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        # Setup the parameters for the test
        vcenter_uuid = 'test_vcenter_uuid'
        target = {'cluster': None, 'host': 'host1', 'servicetag': None}
        host_id = 123456
        host_service_tag = 'SVCTAG1'

        # Mocking the omevv_info_obj.get_host_id_either_host_or_service_tag method
        mocker.patch(INFO_UTILS_PATH + 'OMEVVInfo.get_host_id_either_host_or_service_tag',
                     return_value=(host_id, host_service_tag))

        # Execute the method
        result_host_id, result_host_service_tag = omevv_obj.get_host_id_either_host_or_service_tag(
            vcenter_uuid, target)

        # Verify the result
        assert result_host_id == host_id
        assert result_host_service_tag == host_service_tag

    def test_get_host_id_with_cluster(self, mocker, omevv_connection_firmware, omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        # Setup the parameters for the test
        vcenter_uuid = 'test_vcenter_uuid'
        target = {'cluster': 'cluster1', 'host': None, 'servicetag': None}
        host_ids = [123456, 123457]
        host_service_tags = ['SVCTAG1', 'SVCTAG2']
        cluster_group_id = 789

        # Mocking the necessary methods
        mocker.patch(INFO_UTILS_PATH + OMEVV_INFO_CLUSTER_GROUP_ID,
                     return_value=cluster_group_id)
        mocker.patch(INFO_UTILS_PATH + 'OMEVVInfo.get_cluster_managed_host_details',
                     return_value=(host_ids, host_service_tags))

        # Execute the method
        result_host_ids, result_host_service_tags = omevv_obj.get_host_id_either_host_or_service_tag(
            vcenter_uuid, target)

        # Verify the result
        assert result_host_ids == host_ids
        assert result_host_service_tags == host_service_tags

    def test_execute_update_job_failure(self, mocker, omevv_connection_firmware,
                                        omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        vcenter_uuid = 'test_vcenter_uuid'
        cluster_group_id = 'test_cluster_group_id'
        payload = {
            'schedule': {'runNow': True},
            'firmware': {
                'enterMaintenanceModetimeout': 60,
                'drsCheck': True,
                'evacuateVMs': True,
                'exitMaintenanceMode': True,
                'rebootOptions': 'SAFEREBOOT',
                'enterMaintenanceModeOption': 'FULL_DATA_MIGRATION',
                'maintenanceModeCountCheck': True,
                'checkvSANHealth': True,
                'resetIDrac': True,
                'deleteJobsQueue': True,
                'targets': [{'targetId': '1'}]
            },
            'jobName': 'TestJob',
            'jobDescription': JOB_DESCRIPTION
        }
        parameters = {'run_now': True}
        before_dict = {'component1': {'firmwareversion': '1.0.0'}}
        after_dict = {'component1': {'firmwareversion': '2.0.0'}}

        # Mock the update_cluster method to return a failed response
        failed_resp = MagicMock()
        failed_resp.success = False
        failed_resp.error_msg = "An error occurred"
        mocker.patch(MODULE_PATH + 'OMEVVFirmwareUpdate.update_cluster',
                     return_value=(failed_resp, failed_resp.error_msg))

        # Mock the exit_json method to capture the result
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON,
                     side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.execute_update_job(vcenter_uuid, cluster_group_id,
                                         payload, parameters, before_dict, after_dict)

        # Verify the exception message
        assert excinfo.value.args[0] == FAILED_UPDATE_MSG

    def test_wait_for_job_completion_while_loop(self, mocker, omevv_connection_firmware,
                                                omevv_default_args):
        omevv_default_args.update({'job_wait_timeout': 60})
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        vcenter_uuid = 'test_vcenter_uuid'
        resp = MagicMock()
        job_resp_initial = {'state': 'IN_PROGRESS'}  # Initial state that triggers the while loop
        job_resp_final = {'state': 'COMPLETED',
                          'lastExecutionHistory': {'statusSummary': 'SUCCESSFUL'}}
        err_msg = None
        before_dict = {'component1': {'firmwareversion': '1.0.0'}}
        after_dict = {'component1': {'firmwareversion': '2.0.0'}}

        # Mock the firmware_update_job_track method to return IN_PROGRESS, then COMPLETED
        firmware_update_job_track = mocker.patch(
            MODULE_PATH + OMEVV_FIRM_UPDATE_JOB_TRACK,
            side_effect=[
                (job_resp_initial, None),
                (job_resp_final, None),
            ],
        )

        # Mock time.sleep to avoid actual delay
        mocker.patch(SLEEP_TIME, return_value=None)

        # Mock the exit_json method to capture the result
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON,
                     side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.wait_for_job_completion(vcenter_uuid, resp, job_resp_initial,
                                              err_msg, before_dict, after_dict)

        # Verify the exit message for success
        assert excinfo.value.args[0] == SUCCESS_UPDATE_MSG

        # Verify that the firmware_update_job_track was called twice (initial + final)
        assert firmware_update_job_track.call_count == 2

    def test_wait_for_job_completion_while_loop_failure(self, mocker, omevv_connection_firmware,
                                                        omevv_default_args):
        omevv_default_args.update({'job_wait_timeout': 60})
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        vcenter_uuid = 'test_vcenter_uuid'
        resp = MagicMock()
        job_resp_initial = {'state': 'IN_PROGRESS'}  # Initial state that triggers the while loop
        job_resp_final = {'state': 'FAILED', 'lastExecutionHistory': {'statusSummary': 'FAILED'}}
        err_msg = "Job failed"
        before_dict = {'component1': {'firmwareversion': '1.0.0'}}
        after_dict = {'component1': {'firmwareversion': '2.0.0'}}

        # Mock the firmware_update_job_track method to return IN_PROGRESS, then FAILED
        firmware_update_job_track = mocker.patch(
            MODULE_PATH + OMEVV_FIRM_UPDATE_JOB_TRACK,
            side_effect=[
                (job_resp_initial, None),
                (job_resp_final, err_msg),
            ],
        )

        # Mock time.sleep to avoid actual delay
        mocker.patch(SLEEP_TIME, return_value=None)

        # Mock the exit_json method to capture the result
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON,
                     side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.wait_for_job_completion(vcenter_uuid, resp, job_resp_initial,
                                              err_msg, before_dict, after_dict)

        # Verify the exit message for failure
        assert excinfo.value.args[0] == FAILED_UPDATE_MSG

        # Verify that the firmware_update_job_track was called twice (initial + final)
        assert firmware_update_job_track.call_count == 2


class TestUpdateClusterFirmware(FakeAnsibleModule):
    module = omevv_firmware

    @pytest.fixture
    def omevv_firmware_mock(self):
        return MagicMock()

    @pytest.fixture
    def omevv_connection_firmware(self, mocker, omevv_firmware_mock):
        mocker.patch(
            MODULE_PATH + 'RestOMEVV',
            return_value=omevv_firmware_mock).return_value.__enter__.return_value = omevv_firmware_mock
        return omevv_firmware_mock

    def test_is_firmware_update_needed_update_needed(self, mocker,
                                                     omevv_connection_firmware,
                                                     omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        # Setup the parameters for the test
        vcenter_uuid = 'test_vcenter_uuid'
        cluster_group_id = 'test_cluster_group_id'
        host_ids = [123456]
        target = [{'firmware_components': ['component1']}]
        host_service_tags = ['SVCTAG1']

        # Mock the `check_firmware_update` method to return that an update is needed
        mocker.patch(MODULE_PATH + 'UpdateCluster.check_firmware_update', return_value=(True, {}, {}, 'SVCTAG1'))

        # Execute the method
        firmware_update_needed, main_before_dict, main_after_dict = omevv_obj.is_firmware_update_needed(
            vcenter_uuid, cluster_group_id, host_ids, target, host_service_tags)

        # Verify the result
        assert firmware_update_needed
        assert main_before_dict == {'SVCTAG1': {}}
        assert main_after_dict == {'SVCTAG1': {}}

    def test_is_firmware_update_needed_multiple_hosts(self, mocker, omevv_connection_firmware,
                                                      omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        # Setup the parameters for the test
        vcenter_uuid = 'test_vcenter_uuid'
        cluster_group_id = 'test_group_id'
        host_ids = [123456, 789012]
        target = [{'firmware_components': ['component1']}]
        host_service_tags = ['SVCTAG1', 'SVCTAG2']

        # Mock the `check_firmware_update` method to return different results for multiple hosts
        mocker.patch(MODULE_PATH + 'UpdateCluster.check_firmware_update', side_effect=[
            (True, {}, {}, 'SVCTAG1'),
            (False, {}, {}, 'SVCTAG2')
        ])

        # Execute the method
        firmware_update_needed, main_before_dict, main_after_dict = omevv_obj.is_firmware_update_needed(
            vcenter_uuid, cluster_group_id, host_ids, target, host_service_tags)

        # Verify the result
        assert firmware_update_needed
        assert main_before_dict == {'SVCTAG1': {}, 'SVCTAG2': {}}
        assert main_after_dict == {'SVCTAG1': {}, 'SVCTAG2': {}}

    def test_check_firmware_update_compliant(self, mocker, omevv_connection_firmware,
                                             omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        vcenter_uuid = 'test_vcenter_uuid'
        cluster_group_id = 'test_cluster_group_id'
        host_id = 123456
        target = [{'firmware_components': ['component1']}]

        firmware_drift_info = {
            "hostComplianceReports": [{
                "serviceTag": "SVCTAG1",
                "componentCompliances": [
                    {
                        "sourceName": "component1",
                        "driftStatus": "Compliant",
                        "currentValue": "1.0.0",
                        "baselineValue": "1.0.0"
                    }
                ]
            }]
        }

        mocker.patch(MODULE_PATH + OMEVV_INFO_FIRMWARE_DRIFT_INFO,
                     return_value=firmware_drift_info)

        firmware_update_needed, before_dict, after_dict, st_1 = omevv_obj.check_firmware_update(
            vcenter_uuid, cluster_group_id, host_id, target)

        assert not firmware_update_needed
        assert before_dict == {'component1': {'firmwareversion': '1.0.0'}}
        assert after_dict == {'component1': {'firmwareversion': '1.0.0'}}

    def test_check_firmware_update_non_compliant(self, mocker, omevv_connection_firmware,
                                                 omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        vcenter_uuid = 'test_vcenter_uuid'
        cluster_group_id = 'test_cluster_group_id'
        host_id = 123456
        target = [{'firmware_components': ['component1']}]

        firmware_drift_info = {
            "hostComplianceReports": [{
                "serviceTag": "SVCTAG1",
                "componentCompliances": [
                    {
                        "sourceName": "component1",
                        "driftStatus": "NonCompliant",
                        "currentValue": "1.0.0",
                        "baselineValue": "2.0.0"
                    }
                ]
            }]
        }

        mocker.patch(MODULE_PATH + OMEVV_INFO_FIRMWARE_DRIFT_INFO,
                     return_value=firmware_drift_info)

        firmware_update_needed, before_dict, after_dict, st_1 = omevv_obj.check_firmware_update(
            vcenter_uuid, cluster_group_id, host_id, target)

        assert firmware_update_needed
        assert before_dict == {'component1': {'firmwareversion': '1.0.0'}}
        assert after_dict == {'component1': {'firmwareversion': '2.0.0'}}

    def test_check_firmware_update_mixed_status(self, mocker, omevv_connection_firmware,
                                                omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        vcenter_uuid = 'test_vcenter_uuid'
        cluster_group_id = 'test_cluster_group_id'
        host_id = 123456
        target = [{'firmware_components': ['component1', 'component2']}]

        firmware_drift_info = {
            "hostComplianceReports": [{
                "serviceTag": "SVCTAG1",
                "componentCompliances": [
                    {
                        "sourceName": "component1",
                        "driftStatus": "NonCompliant",
                        "currentValue": "1.0.0",
                        "baselineValue": "2.0.0"
                    },
                    {
                        "sourceName": "component2",
                        "driftStatus": "Compliant",
                        "currentValue": "3.0.0",
                        "baselineValue": "3.0.0"
                    }
                ]
            }]
        }

        mocker.patch(MODULE_PATH + OMEVV_INFO_FIRMWARE_DRIFT_INFO,
                     return_value=firmware_drift_info)

        firmware_update_needed, before_dict, after_dict, st_1 = omevv_obj.check_firmware_update(
            vcenter_uuid, cluster_group_id, host_id, target)

        assert firmware_update_needed
        assert before_dict == {'component1': {'firmwareversion': '1.0.0'}, 'component2': {'firmwareversion': '3.0.0'}}
        assert after_dict == {'component1': {'firmwareversion': '2.0.0'}, 'component2': {'firmwareversion': '3.0.0'}}

    def test_is_update_job_allowed_false(self, mocker,
                                         omevv_connection_firmware, omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        vcenter_uuid = 'test_vcenter_uuid'
        cluster_group_id = 'test_cluster_group_id'
        cluster_name = 'test_cluster_name'

        # Mock the check_existing_update_job method to return True
        mocker.patch(MODULE_PATH + 'OMEVVFirmwareUpdate.check_existing_update_job',
                     return_value=False)

        try:
            omevv_obj.is_update_job_allowed(vcenter_uuid, cluster_group_id, cluster_name)
        except AnsibleFailJSonException as err:
            assert err.args[0] == UPDATE_JOB_PRESENT_MSG.format(cluster_name=cluster_name)

    def test_is_job_name_existing_false(self, mocker, omevv_connection_firmware, omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        vcenter_uuid = 'test_vcenter_uuid'
        job_name = 'test_job_name'

        # Mock the check_existing_job_name method to return False
        mocker.patch(MODULE_PATH + 'OMEVVFirmwareUpdate.check_existing_job_name',
                     return_value=True)

        # Execute the method
        try:
            omevv_obj.is_job_name_existing(vcenter_uuid, job_name=job_name)
        except AnsibleFailJSonException as err:
            assert err.args[0] == JOB_NAME_ALREADY_EXISTS_MSG.format(job_name=job_name)

    def test_handle_job_response_run_now_true_job_wait_false(self, mocker,
                                                             omevv_connection_firmware,
                                                             omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        parameters = {'run_now': True, 'job_wait': False}
        vcenter_uuid = 'test_vcenter_uuid'
        resp = MagicMock()
        job_resp = {'state': 'SUBMITTED'}
        err_msg = None
        before_dict = {'component1': {'firmwareversion': '1.0.0'}}
        after_dict = {'component1': {'firmwareversion': '2.0.0'}}

        # Mock the exit_json method to capture the result
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON, side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.handle_job_response(parameters, vcenter_uuid, resp, job_resp,
                                          err_msg, before_dict, after_dict)

        # Verify the exit message for submission
        assert excinfo.value.args[0] == SUCCESS_UPDATE_SUBMIT_MSG

    def test_handle_job_response_run_now_false(self, mocker, omevv_connection_firmware,
                                               omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        parameters = {'run_now': False}
        vcenter_uuid = 'test_vcenter_uuid'
        resp = MagicMock()
        job_resp = {'state': 'SCHEDULED'}
        err_msg = None
        before_dict = {'component1': {'firmwareversion': '1.0.0'}}
        after_dict = {'component1': {'firmwareversion': '2.0.0'}}

        # Mock the exit_json method to capture the result
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON, side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.handle_job_response(parameters, vcenter_uuid, resp,
                                          job_resp, err_msg,
                                          before_dict, after_dict)

        # Verify the exit message for scheduled job
        assert excinfo.value.args[0] == SUCCESS_UPDATE_SCHEDULED_MSG

    def test_wait_for_job_completion_success(self, mocker, omevv_connection_firmware,
                                             omevv_default_args):
        omevv_default_args.update({'job_wait_timeout': 60})
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        vcenter_uuid = 'test_vcenter_uuid'
        resp = MagicMock()
        job_resp = {'state': 'COMPLETED', 'lastExecutionHistory': {'statusSummary': 'SUCCESSFUL'}}
        err_msg = None
        before_dict = {'component1': {'firmwareversion': '1.0.0'}}
        after_dict = {'component1': {'firmwareversion': '2.0.0'}}

        # Mock the firmware_update_job_track method to simulate job completion
        def mock_firmware_update_job_track(vcenter_uuid, json_data):
            return (job_resp, None) if job_resp['state'] == 'COMPLETED' else (job_resp, "Error")

        mocker.patch(MODULE_PATH + OMEVV_FIRM_UPDATE_JOB_TRACK,
                     side_effect=mock_firmware_update_job_track)

        # Mock time.sleep to avoid delays during testing
        mocker.patch(SLEEP_TIME, return_value=None)

        # Mock the exit_json method to capture the result
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON, side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.wait_for_job_completion(vcenter_uuid, resp, job_resp, err_msg, before_dict, after_dict)

        # Verify the exit message for job completion
        assert excinfo.value.args[0] == SUCCESS_UPDATE_MSG

    def test_wait_for_job_completion_failure(self, mocker, omevv_connection_firmware, omevv_default_args):
        omevv_default_args.update({'job_wait_timeout': 60})
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        vcenter_uuid = 'test_vcenter_uuid'
        resp = MagicMock()
        job_resp = {'state': 'FAILED', 'lastExecutionHistory': {'statusSummary': 'FAILED'}}
        err_msg = "Job Failed"
        before_dict = {'component1': {'firmwareversion': '1.0.0'}}
        after_dict = {'component1': {'firmwareversion': '2.0.0'}}

        # Mock the firmware_update_job_track method to simulate job failure
        def mock_firmware_update_job_track(vcenter_uuid, json_data):
            return (job_resp, err_msg) if job_resp['state'] == 'FAILED' else (job_resp, None)

        mocker.patch(MODULE_PATH + OMEVV_FIRM_UPDATE_JOB_TRACK,
                     side_effect=mock_firmware_update_job_track)

        # Mock time.sleep to avoid delays during testing
        mocker.patch(SLEEP_TIME, return_value=None)

        # Mock the exit_json method to capture the result
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON, side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.wait_for_job_completion(vcenter_uuid, resp, job_resp, err_msg, before_dict, after_dict)

        # Verify the exit message for job failure
        assert excinfo.value.args[0] == FAILED_UPDATE_MSG

    def test_wait_for_job_completion_failure_long_time(self, mocker, omevv_connection_firmware, omevv_default_args):
        omevv_default_args.update({'job_wait_timeout': -10})
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        vcenter_uuid = 'test_vcenter_uuid'
        resp = MagicMock()
        job_resp = {'state': 'FAILED', 'lastExecutionHistory': {'statusSummary': 'FAILED'}}
        err_msg = "Job Failed"
        before_dict = {'component1': {'firmwareversion': '1.0.0'}}
        after_dict = {'component1': {'firmwareversion': '2.0.0'}}

        # Mock the firmware_update_job_track method to simulate job failure
        def mock_firmware_update_job_track(vcenter_uuid, json_data):
            return (job_resp, err_msg) if job_resp['state'] == 'FAILED' else (job_resp, None)

        mocker.patch(MODULE_PATH + OMEVV_FIRM_UPDATE_JOB_TRACK,
                     side_effect=mock_firmware_update_job_track)

        # Mock time.sleep to avoid delays during testing
        mocker.patch(SLEEP_TIME, return_value=None)

        # Mock the exit_json method to capture the result
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON, side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.wait_for_job_completion(vcenter_uuid, resp, job_resp, err_msg, before_dict, after_dict)

        # Verify the exit message for job failure
        assert excinfo.value.args[0] == FAILED_UPDATE_TIMEOUT_MSG.format('-10')

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_omevv_firmware_repository_profile_main_exception_handling_case(self, exc_type, mocker, omevv_default_args,
                                                                            omevv_firmware_mock):
        HTTP_ERROR = "http error message"
        HTTP_ERROR_URL = 'https://testhost.com'
        RETURN_TYPE = "application/json"
        omevv_firmware_mock.status_code = 400
        omevv_firmware_mock.success = False
        json_str = to_text(json.dumps(
            {"errorCode": "501", "message": "Error"}))
        if exc_type in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'UpdateCluster' +
                         '.execute',
                         side_effect=exc_type(HTTP_ERROR_URL, 400,
                                              HTTP_ERROR,
                                              {"accept-type": RETURN_TYPE},
                                              StringIO(json_str)))
        else:
            mocker.patch(MODULE_PATH + 'UpdateCluster' +
                         '.execute', side_effect=exc_type('test'))
        omevv_default_args.update({"run_now": True,
                                   "targets": [{"firmware_components": "testhost.com"}]})
        result = self._run_module(omevv_default_args)
        if exc_type == URLError:
            assert result['changed'] is False
        else:
            assert result['failed'] is True
        assert 'msg' in result
