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
from ansible_collections.dellemc.openmanage.plugins.modules.omevv_firmware import FirmwareUpdate, UpdateCluster
from ansible_collections.dellemc.openmanage.plugins.modules import omevv_firmware
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

    # def test_execute(self, omevv_default_args, omevv_connection_firmware_repository_profile):
    #     pass
    #     # obj = MagicMock()
    #     # omevv_obj = self.module.FirmwareRepositoryProfile(
    #     #     omevv_connection_firmware_repository_profile, obj)
    #     # omevv_obj.execute()

    def test_get_payload_details(self, mocker, omevv_connection_firmware, omevv_default_args):
        # Scenario 1: payload details with description
        host_id = 123456
        obj = MagicMock()
        omevv_obj = self.module.FirmwareUpdate(
            omevv_connection_firmware, obj)
        mocker.patch(MODULE_PATH + 'FirmwareUpdate.add_optional_fields', return_value=None)
        mocker.patch(MODULE_PATH + 'FirmwareUpdate.set_schedule', return_value=None)
        mocker.patch(MODULE_PATH + 'FirmwareUpdate.set_job_details', return_value=None)
        mocker.patch(MODULE_PATH + 'FirmwareUpdate.add_targets', return_value=None)
        result = omevv_obj.get_payload_details(host_id)
        assert "firmware" in result

    def test_add_optional_fields(self, mocker, omevv_connection_firmware, omevv_default_args):
        firmware = {'targets': []}
        parameters = {}
        obj = MagicMock()
        omevv_obj = self.module.FirmwareUpdate(
            omevv_connection_firmware, obj)
        result = omevv_obj.add_optional_fields(firmware, parameters)
        assert result is None

    def test_set_schedule(self, mocker, omevv_connection_firmware, omevv_default_args):
        obj = MagicMock()
        omevv_obj = self.module.FirmwareUpdate(
            omevv_connection_firmware, obj)
        result = omevv_obj.set_schedule({}, {})
        assert result is None

    def test_set_job_details(self, mocker, omevv_connection_firmware, omevv_default_args):
        obj = MagicMock()
        omevv_obj = self.module.FirmwareUpdate(
            omevv_connection_firmware, obj)
        result = omevv_obj.set_job_details({}, {})
        assert result is None

    def test_add_targets_device_id_list(self, mocker, omevv_connection_firmware, omevv_default_args):
        obj = MagicMock()
        omevv_obj = self.module.FirmwareUpdate(
            omevv_connection_firmware, obj)
        target_list = [
            {'firmware_components': 1}
        ]
        result = omevv_obj.add_targets({'targets': []}, target_list, [100, 101])
        assert result is None

    def test_add_targets_device_id_string(self, mocker, omevv_connection_firmware, omevv_default_args):
        obj = MagicMock()
        omevv_obj = self.module.FirmwareUpdate(
            omevv_connection_firmware, obj)
        target_list = [
            {'firmware_components': 1}
        ]
        result = omevv_obj.add_targets({'targets': []}, target_list, 100)
        assert result is None

    def test_host_servicetag_existence(self, mocker, omevv_connection_firmware, omevv_default_args):
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

    def test_host_servicetag_existence_not_exits(self, mocker, omevv_connection_firmware, omevv_default_args):
        omevv_default_args.update({"targets": []})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        omevv_obj = FirmwareUpdate(f_module, omevv_connection_firmware)
        try:
            omevv_obj.host_servicetag_existence()
        except AnsibleFailJSonException as err:
            assert err.args[0] == CLUSTER_HOST_SERVICETSAG_REQUIRED_MSG

    def test_validate_date_time_invalid(self, mocker, omevv_connection_firmware, omevv_default_args):
        omevv_default_args.update({"date_time": "2020-13-01T00:00:00Z"})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        omevv_obj = FirmwareUpdate(f_module, omevv_connection_firmware)
        try:
            omevv_obj.validate_date_time()
        except AnsibleFailJSonException as err:
            assert err.args[0] == INVALID_DATE_TIME_MSG

    def test_validate_date_time_valid(self, mocker, omevv_connection_firmware, omevv_default_args):
        omevv_default_args.update({"date_time": "2020-11-01T00:00:00Z"})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        omevv_obj = FirmwareUpdate(f_module, omevv_connection_firmware)
        result = omevv_obj.validate_date_time()
        assert result == datetime.datetime(2020, 11, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)

    def test_enter_maintenance_mode_timeout(self, mocker, omevv_connection_firmware, omevv_default_args):
        omevv_default_args.update({"enter_maintenance_mode_timeout": 59})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        omevv_obj = FirmwareUpdate(f_module, omevv_connection_firmware)
        try:
            omevv_obj.enter_maintenance_mode_timeout()
        except AnsibleFailJSonException as err:
            assert err.args[0] == MAINTENANCE_MODE_TIMEOUT_INVALID_MSG

    def test_validate_params(self, mocker, omevv_connection_firmware, omevv_default_args):
        omevv_default_args.update({"enter_maintenance_mode_timeout": 61})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        omevv_obj = FirmwareUpdate(f_module, omevv_connection_firmware)
        mocker.patch(MODULE_PATH + 'FirmwareUpdate.host_servicetag_existence', return_value=None)
        mocker.patch(UTILS_PATH + 'validate_job_wait', return_value=True)
        try:
            omevv_obj.validate_params()
        except AnsibleFailJSonException as err:
            assert err.args[0] == TIMEOUT_NEGATIVE_OR_ZERO_MSG

    def test_validate_params_job_wait_false(self, mocker, omevv_connection_firmware, omevv_default_args):
        omevv_default_args.update({"enter_maintenance_mode_timeout": 61})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        omevv_obj = FirmwareUpdate(f_module, omevv_connection_firmware)
        mocker.patch(MODULE_PATH + 'FirmwareUpdate.host_servicetag_existence', return_value=None)
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

    def test_execute_check_mode_false(self, mocker, omevv_connection_firmware, omevv_default_args):
        omevv_default_args.update({"targets": []})
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=False)
        omevv_obj = UpdateCluster(f_module, omevv_connection_firmware)
        mocker.patch(MODULE_PATH + 'FirmwareUpdate.validate_params', return_value=None)
        target = {"cluster": "cluster1"}
        mocker.patch(MODULE_PATH + 'UpdateCluster.get_target', return_value=target)
        value = (1034, {}, 1001)
        mocker.patch(MODULE_PATH + 'UpdateCluster.process_cluster_target', return_value=value)
        mocker.patch(MODULE_PATH + 'UpdateCluster.is_firmware_update_needed', return_value=(1, 2, 3, 4, 5))
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
        mocker.patch(MODULE_PATH + 'UpdateCluster.get_target', return_value=target)
        value = (1034, {}, [1001])
        mocker.patch(MODULE_PATH + 'UpdateCluster.process_non_cluster_target', return_value=value)
        mocker.patch(MODULE_PATH + 'UpdateCluster.is_firmware_update_needed', return_value=(1, 2, 3, 4, 5))
        mocker.patch(MODULE_PATH + 'UpdateCluster.is_update_job_allowed', return_value=False)
        mocker.patch(MODULE_PATH + 'UpdateCluster.is_job_name_existing', return_value=False)
        mocker.patch(MODULE_PATH + 'UpdateCluster.handle_check_mode', return_value=None)
        mocker.patch(MODULE_PATH + 'UpdateCluster.handle_firmware_update', return_value=None)
        result = omevv_obj.execute()
        assert result is None
