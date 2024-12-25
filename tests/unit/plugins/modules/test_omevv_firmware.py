# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.8.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import datetime
from unittest.mock import MagicMock
from ansible_collections.dellemc.openmanage.plugins.modules.omevv_firmware import FirmwareUpdate, UpdateCluster
from ansible_collections.dellemc.openmanage.plugins.modules import omevv_firmware
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import AnsibleFailJSonException
from mock import MagicMock

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
SOURCE_NOT_FOUND_MSG = "The Requested resource cannot be found."
TRIGGER_UPDATE_CHECK_URI = "/Consoles/{vcenter_uuid}/CanTriggerUpdate"
UPDATE_CLUSTER_EXECUTE_JOB = "UpdateCluster.execute_update_job"
ANSIBLE_MODULE_EXIT_JSON = "ansible.module_utils.basic.AnsibleModule.exit_json"
OMEVV_INFO_FIRMWARE_DRIFT_INFO = "OMEVVInfo.get_firmware_drift_info_for_single_host"
UPDATE_CLUSTER_GET_TARGET = "UpdateCluster.get_target"
OMEVV_INFO_CLUSTER_GROUP_ID = "OMEVVInfo.get_group_id_of_cluster"


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

    # def test_get_payload_details(self, mocker, omevv_connection_firmware):
    #     # Scenario 1: payload details with description
    #     host_id = 123456
    #     obj = MagicMock()
    #     omevv_obj = self.module.FirmwareUpdate(
    #         omevv_connection_firmware, obj)
    #     mocker.patch(MODULE_PATH + 'FirmwareUpdate.set_firmware', return_value={})
    #     mocker.patch(MODULE_PATH + 'FirmwareUpdate.set_schedule', return_value={})
    #     mocker.patch(MODULE_PATH + 'FirmwareUpdate.set_job_details', return_value={})
    #     mocker.patch(MODULE_PATH + 'FirmwareUpdate.add_targets', return_value={})
    #     result = omevv_obj.get_payload_details(host_id)
    #     assert result is True

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
        omevv_default_args.update({"job_description": "Test Job Description"})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        omevv_obj = FirmwareUpdate(f_module, omevv_connection_firmware)
        result = omevv_obj.set_job_details({}, {"job_name": "Test job name",
                                                "job_description": "Test Job Description"})
        assert result == {'jobDescription': 'Test Job Description',
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
        mocker.patch(MODULE_PATH + 'FirmwareUpdate.host_servicetag_existence', return_value=None)
        mocker.patch(UTILS_PATH + 'validate_job_wait', return_value=True)
        try:
            omevv_obj.validate_params()
        except AnsibleFailJSonException as err:
            assert err.args[0] == TIMEOUT_NEGATIVE_OR_ZERO_MSG
            assert err.fail_kwargs.get('failed') is True

    def test_validate_params_date_time(self, mocker, omevv_connection_firmware,
                                       omevv_default_args):
        omevv_default_args.update({"date_time": "2020-11-01T00:00:00Z"})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        omevv_obj = FirmwareUpdate(f_module, omevv_connection_firmware)
        mocker.patch(MODULE_PATH + 'FirmwareUpdate.host_servicetag_existence', return_value=None)
        mocker.patch(UTILS_PATH + 'validate_job_wait', return_value=True)
        result = omevv_obj.validate_params()
        assert result is True

    def test_validate_params_job_wait_false(self, mocker, omevv_connection_firmware,
                                            omevv_default_args):
        omevv_default_args.update({"enter_maintenance_mode_timeout": 61})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        omevv_obj = FirmwareUpdate(f_module, omevv_connection_firmware)
        mocker.patch(MODULE_PATH + 'FirmwareUpdate.host_servicetag_existence', return_value=None)
        mocker.patch(UTILS_PATH + 'validate_job_wait', return_value=False)
        result = omevv_obj.validate_params()
        assert result is True


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

    def test_execute_check_mode_false(self, mocker, omevv_connection_firmware, omevv_default_args):
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
                     return_value=(1, 2, 3, 4, 5))
        mocker.patch(MODULE_PATH + 'UpdateCluster.is_update_job_allowed', return_value=True)
        mocker.patch(MODULE_PATH + 'UpdateCluster.is_job_name_existing', return_value=None)
        mocker.patch(MODULE_PATH + 'UpdateCluster.handle_check_mode', return_value=None)
        mocker.patch(MODULE_PATH + 'UpdateCluster.handle_firmware_update', return_value=True)
        result = omevv_obj.execute()
        assert result is None

    def test_execute_check_mode_true(self, mocker, omevv_connection_firmware, omevv_default_args):
        omevv_default_args.update({"targets": []})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=True)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)
        mocker.patch(MODULE_PATH + 'FirmwareUpdate.validate_params', return_value=None)
        target = {"cluster": ""}
        mocker.patch(MODULE_PATH + UPDATE_CLUSTER_GET_TARGET, return_value=target)
        value = (1034, {}, [1001])
        mocker.patch(MODULE_PATH + 'UpdateCluster.process_non_cluster_target', return_value=value)
        mocker.patch(MODULE_PATH + 'UpdateCluster.is_firmware_update_needed',
                     return_value=(1, 2, 3, 4, 5))
        mocker.patch(MODULE_PATH + 'UpdateCluster.is_update_job_allowed', return_value=False)
        mocker.patch(MODULE_PATH + 'UpdateCluster.is_job_name_existing', return_value=False)
        mocker.patch(MODULE_PATH + 'UpdateCluster.handle_check_mode', return_value=None)
        mocker.patch(MODULE_PATH + 'UpdateCluster.handle_firmware_update', return_value=None)
        result = omevv_obj.execute()
        assert result is None

    def test_process_cluster_target(self, mocker, omevv_connection_firmware, omevv_default_args):
        omevv_default_args.update({"targets": [{'host': 123456,
                                               'cluster': 'cluster_a'}]})
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=True)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)
        target = [123456, 123457]
        mocker.patch(MODULE_PATH + 'UpdateCluster.get_host_id', return_value=target)
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
        mocker.patch(MODULE_PATH + 'UpdateCluster.get_host_id', return_value=target)
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
        mocker.patch(MODULE_PATH + 'UpdateCluster.get_host_from_parameters', return_value=target)
        cluster_name_value = "cluster_a"
        mocker.patch(INFO_UTILS_PATH + 'OMEVVInfo.get_cluster_name', return_value=cluster_name_value)
        group_id_value = 1357
        mocker.patch(INFO_UTILS_PATH + OMEVV_INFO_CLUSTER_GROUP_ID, return_value=group_id_value)
        payload = {}
        mocker.patch(MODULE_PATH + 'FirmwareUpdate.get_payload_details', return_value=payload)
        parameters = {'targets': [{'host': 123456, 'cluster': 'cluster_a'}]}
        result = omevv_obj.process_non_cluster_target(parameters)
        assert result == (1357, {}, 123456)

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
        mocker.patch(MODULE_PATH + 'UpdateCluster.get_host_from_parameters', return_value=target)
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
        mocker.patch(MODULE_PATH + 'UpdateCluster.get_host_from_parameters', return_value=target)
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
        mocker.patch(MODULE_PATH + 'UpdateCluster.get_host_id', return_value=(3, 4))
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
        mocker.patch(MODULE_PATH + 'UpdateCluster.get_host_id', return_value=(3, 4))
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
        before_no_change_dict = {'component1': {'firmwareversion': '1.0.0'}}
        after_no_change_dict = {'component1': {'firmwareversion': '1.0.1'}}
        before_dict = {'component2': {'firmwareversion': '2.0.0'}}
        after_dict = {'component2': {'firmwareversion': '2.0.1'}}

        # Execute the method with change
        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.handle_check_mode(firmware_update_needed,
                                        before_no_change_dict,
                                        after_no_change_dict,
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
        before_no_change_dict = {}
        after_no_change_dict = {}
        before_dict = {}
        after_dict = {}

        # Execute the method without diff
        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.handle_check_mode(firmware_update_needed,
                                        before_no_change_dict,
                                        after_no_change_dict,
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
        before_no_change_dict = {'component1': {'firmwareversion': '1.0.0'}}
        after_no_change_dict = {'component1': {'firmwareversion': '1.0.0'}}
        before_dict = {}
        after_dict = {}

        # Execute the method with no change
        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.handle_check_mode(firmware_update_needed,
                                        before_no_change_dict,
                                        after_no_change_dict,
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
        before_no_change_dict = {}
        after_no_change_dict = {}
        before_dict = {}
        after_dict = {}

        # Execute the method without diff and no change
        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.handle_check_mode(firmware_update_needed,
                                        before_no_change_dict,
                                        after_no_change_dict,
                                        before_dict, after_dict)

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

    def test_get_target_empty_list(self, omevv_connection_firmware, omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        # Setup the parameters for the test
        target_list = []

        # Execute the method
        result = omevv_obj.get_target(target_list)

        # Verify the result
        assert result is None

    def test_get_host_id_with_service_tag(self, mocker, omevv_connection_firmware, omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        # Setup the parameters for the test
        vcenter_uuid = 'test_vcenter_uuid'
        target = {'cluster': None, 'host': None, 'servicetag': 'SVCTAG1'}
        host_id = 123456
        host_service_tag = 'SVCTAG1'

        # Mocking the omevv_info_obj.get_host_id method
        mocker.patch(INFO_UTILS_PATH + 'OMEVVInfo.get_host_id', return_value=(host_id, host_service_tag))

        # Execute the method
        result_host_id, result_host_service_tag = omevv_obj.get_host_id(vcenter_uuid, target)

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

        # Mocking the omevv_info_obj.get_host_id method
        mocker.patch(INFO_UTILS_PATH + 'OMEVVInfo.get_host_id', return_value=(host_id,
                                                                              host_service_tag))

        # Execute the method
        result_host_id, result_host_service_tag = omevv_obj.get_host_id(vcenter_uuid, target)

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
        result_host_ids, result_host_service_tags = omevv_obj.get_host_id(vcenter_uuid, target)

        # Verify the result
        assert result_host_ids == host_ids
        assert result_host_service_tags == host_service_tags


class TestUpdateClusterFirmware(FakeAnsibleModule):
    module = UpdateCluster

    @pytest.fixture
    def omevv_firmware_mock(self):
        return MagicMock()

    @pytest.fixture
    def omevv_connection_firmware(self, mocker, omevv_firmware_mock):
        mocker.patch(MODULE_PATH + 'RestOMEVV',
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
        mocker.patch(MODULE_PATH + 'UpdateCluster.check_firmware_update', return_value=(True, {}, {}, {}, {}, 'SVCTAG1'))

        # Execute the method
        firmware_update_needed, main_before_no_change_dict, main_after_no_change_dict, main_before_dict, main_after_dict = omevv_obj.is_firmware_update_needed(
            vcenter_uuid, cluster_group_id, host_ids, target, host_service_tags)

        # Verify the result
        assert firmware_update_needed
        assert main_before_dict == {'SVCTAG1': {}}
        assert main_after_dict == {'SVCTAG1': {}}

    def test_is_firmware_update_needed_multiple_hosts(self, mocker, omevv_connection_firmware, omevv_default_args):
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
            (True, {}, {}, {}, {}, 'SVCTAG1'),
            (False, {}, {}, {}, {}, 'SVCTAG2')
        ])

        # Execute the method
        firmware_update_needed, main_before_no_change_dict, main_after_no_change_dict, main_before_dict, main_after_dict = omevv_obj.is_firmware_update_needed(
            vcenter_uuid, cluster_group_id, host_ids, target, host_service_tags)

        # Verify the result
        assert firmware_update_needed
        assert main_before_dict == {'SVCTAG1': {}, 'SVCTAG2': {}}
        assert main_after_dict == {'SVCTAG1': {}, 'SVCTAG2': {}}

    def test_check_firmware_update_compliant(self, mocker, omevv_connection_firmware, omevv_default_args):
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

        firmware_update_needed, before_no_change_dict, after_no_change_dict, before_dict, after_dict, current_host_st = omevv_obj.check_firmware_update(
            vcenter_uuid, cluster_group_id, host_id, target)

        assert not firmware_update_needed
        assert before_no_change_dict == {'component1': {'firmwareversion': '1.0.0'}}
        assert after_no_change_dict == {'component1': {'firmwareversion': '1.0.0'}}
        assert before_dict == {}
        assert after_dict == {}

    def test_check_firmware_update_non_compliant(self, mocker, omevv_connection_firmware, omevv_default_args):
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

        firmware_update_needed, before_no_change_dict, after_no_change_dict, before_dict, after_dict, current_host_st = omevv_obj.check_firmware_update(
            vcenter_uuid, cluster_group_id, host_id, target)

        assert firmware_update_needed
        assert before_no_change_dict == {}
        assert after_no_change_dict == {}
        assert before_dict == {'component1': {'firmwareversion': '1.0.0'}}
        assert after_dict == {'component1': {'firmwareversion': '2.0.0'}}

    def test_check_firmware_update_mixed_status(self, mocker, omevv_connection_firmware, omevv_default_args):
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

        firmware_update_needed, before_no_change_dict, after_no_change_dict, before_dict, after_dict, current_host_st = omevv_obj.check_firmware_update(
            vcenter_uuid, cluster_group_id, host_id, target)

        assert firmware_update_needed
        assert before_no_change_dict == {'component2': {'firmwareversion': '3.0.0'}}
        assert after_no_change_dict == {'component2': {'firmwareversion': '3.0.0'}}
        assert before_dict == {'component1': {'firmwareversion': '1.0.0'}}
        assert after_dict == {'component1': {'firmwareversion': '2.0.0'}}

    def test_is_update_job_allowed_true(self, mocker, omevv_connection_firmware, omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        vcenter_uuid = 'test_vcenter_uuid'
        cluster_group_id = 'test_cluster_group_id'
        cluster_name = 'test_cluster_name'

        # Mock the check_existing_update_job method to return True
        mocker.patch(MODULE_PATH + 'OMEVVFirmwareUpdate.check_existing_update_job',
                     return_value=True)

        # Execute the method
        result = omevv_obj.is_update_job_allowed(vcenter_uuid, cluster_group_id, cluster_name)

        # Verify the result
        assert result is True

    def test_is_job_name_existing_false(self, mocker, omevv_connection_firmware, omevv_default_args):
        f_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)

        vcenter_uuid = 'test_vcenter_uuid'
        job_name = 'test_job_name'

        # Mock the check_existing_job_name method to return False
        mocker.patch(MODULE_PATH + 'OMEVVFirmwareUpdate.check_existing_job_name',
                     return_value=False)

        # Execute the method
        result = omevv_obj.is_job_name_existing(vcenter_uuid, job_name)

        # Verify the result
        assert result is False

    def test_handle_job_response_run_now_true_job_wait_false(self, mocker, omevv_connection_firmware, omevv_default_args):
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
            omevv_obj.handle_job_response(parameters, vcenter_uuid, resp, job_resp, err_msg, before_dict, after_dict)

        # Verify the exit message for submission
        assert excinfo.value.args[0] == SUCCESS_UPDATE_SUBMIT_MSG

    def test_handle_job_response_run_now_false(self, mocker, omevv_connection_firmware, omevv_default_args):
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

    def test_wait_for_job_completion_success(self, mocker, omevv_connection_firmware, omevv_default_args):
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

        mocker.patch(MODULE_PATH + 'OMEVVFirmwareUpdate.firmware_update_job_track',
                     side_effect=mock_firmware_update_job_track)

        # Mock time.sleep to avoid delays during testing
        mocker.patch('time.sleep', return_value=None)

        # Mock the exit_json method to capture the result
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON, side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.wait_for_job_completion(vcenter_uuid, resp, job_resp, err_msg, before_dict, after_dict)

        # Verify the exit message for job completion
        assert excinfo.value.args[0] == SUCCESS_UPDATE_MSG

    def test_wait_for_job_completion_failure(self, mocker, omevv_connection_firmware, omevv_default_args):
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

        mocker.patch(MODULE_PATH + 'OMEVVFirmwareUpdate.firmware_update_job_track',
                     side_effect=mock_firmware_update_job_track)

        # Mock time.sleep to avoid delays during testing
        mocker.patch('time.sleep', return_value=None)

        # Mock the exit_json method to capture the result
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON, side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_obj.wait_for_job_completion(vcenter_uuid, resp, job_resp, err_msg, before_dict, after_dict)

        # Verify the exit message for job failure
        assert excinfo.value.args[0] == FAILED_UPDATE_MSG

    def test_main_http_error(self, mocker, omevv_default_args):
        # Mock the OMEVVAnsibleModule initialization
        mock_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        mocker.patch(MODULE_PATH + 'OMEVVAnsibleModule', return_value=mock_module)

        # Mock the 'RestOMEVV' context manager to raise HTTPError
        mocker.patch(MODULE_PATH + 'RestOMEVV',
                     __enter__=MagicMock(), __exit__=MagicMock(),
                     side_effect=HTTPError('url', 500, 'Internal Server Error', {}, None))

        # Mock json load to return error message in case of exception
        mocker.patch('json.load', return_value={"message": "Internal Server Error"})

        # Mock the exit_json method to capture the exit
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON, side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_firmware.main()

        assert excinfo.value.args[0] == "Internal Server Error"

    def test_main_url_error(self, mocker, omevv_default_args):
        # Mock the OMEVVAnsibleModule initialization
        mock_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        mocker.patch(MODULE_PATH + 'OMEVVAnsibleModule', return_value=mock_module)

        # Mock the 'RestOMEVV' context manager to raise URLError
        mocker.patch(MODULE_PATH + 'RestOMEVV', __enter__=MagicMock(), __exit__=MagicMock(),
                     side_effect=URLError('url error'))

        # Mock the exit_json method to capture the exit
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON, side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_firmware.main()

        assert excinfo.value.args[0] == "The URL with IP XX.XX.XX.XX and port None cannot be reached."

    def test_main_general_exception(self, mocker, omevv_default_args):
        # Mock the OMEVVAnsibleModule initialization
        mock_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        mocker.patch(MODULE_PATH + 'OMEVVAnsibleModule', return_value=mock_module)

        # Mock the 'RestOMEVV' context manager to raise a general exception
        mocker.patch(MODULE_PATH + 'RestOMEVV', __enter__=MagicMock(), __exit__=MagicMock(),
                     side_effect=ValueError('general error'))

        # Mock the exit_json method to capture the exit
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON, side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_firmware.main()

        assert excinfo.value.args[0] == 'general error'

    def test_main_source_not_found_error(self, mocker, omevv_default_args):
        # Mock the OMEVVAnsibleModule initialization
        mock_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        mocker.patch(MODULE_PATH + 'OMEVVAnsibleModule', return_value=mock_module)

        # Mock the 'RestOMEVV' context manager to raise HTTPError with code 404
        mocker.patch(MODULE_PATH + 'RestOMEVV', __enter__=MagicMock(), __exit__=MagicMock(), side_effect=HTTPError('url', 404, 'Not Found', {}, None))

        # Mock the exit_json method to capture the exit
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON, side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_firmware.main()

        # Verify the exception message
        assert excinfo.value.args[0] == SOURCE_NOT_FOUND_MSG

    def test_main_http_error_with_error_info(self, mocker, omevv_default_args):
        # Mock the OMEVVAnsibleModule initialization
        mock_module = self.get_module_mock(params=omevv_default_args, check_mode=False)
        mocker.patch(MODULE_PATH + 'OMEVVAnsibleModule', return_value=mock_module)

        # Define the error details
        error_message = "Some HTTP error occurred"
        error_info = {"message": error_message, "type": "HTTPError"}

        # Mock the HTTPError with a sample error details
        http_error = HTTPError('url', 403, 'Forbidden', {}, None)
        mocker.patch(MODULE_PATH + 'RestOMEVV', __enter__=MagicMock(), __exit__=MagicMock(),
                     side_effect=http_error)

        # Mock json load to return a custom error message with details
        mocker.patch('json.load', return_value=error_info)

        # Mock the exit_json method to capture the exit
        mocker.patch(ANSIBLE_MODULE_EXIT_JSON, side_effect=AnsibleFailJSonException)

        with pytest.raises(AnsibleFailJSonException) as excinfo:
            omevv_firmware.main()

        # Verify the exception message and error info
        assert excinfo.value.args[0] == error_message
