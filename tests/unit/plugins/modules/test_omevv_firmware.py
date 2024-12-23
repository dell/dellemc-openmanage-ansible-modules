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
from ansible_collections.dellemc.openmanage.plugins.modules import omevv_firmware
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from mock import MagicMock

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.omevv_firmware.'
MODULE_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.omevv_utils.omevv_firmware_utils.'
SUCCESS_MSG = "Successfully retrieved the firmware repository profile information."
NO_PROFILE_MSG = "Unable to complete the operation because the '{profile_name}' is not a valid 'profile_name'."
FAILED_CONN_MSG = "Unable to complete the operation. Please check the connection details."
FAILED_MSG = "Unable to fetch the firmware repository profile information."
INVOKE_REQ_KEY = "RestOMEVV.invoke_request"
# GET_PAYLOAD_DETAILS = "FirmwareRepositoryProfile.get_payload_details"
# GET_PROFILE_INFO_KEY = "OMEVVFirmwareProfile.get_firmware_repository_profile"
# PERFORM_OPERATION_KEY = "FirmwareRepositoryProfile.execute"
# PERFORM_TEST_CONNECTION = "FirmwareRepositoryProfile.test_connection"
# PERFORM_CREATE_PROFILE = "OMEVVFirmwareProfile.create_firmware_repository_profile"
# PERFORM_MODIFY_PROFILE = "OMEVVFirmwareProfile.modify_firmware_repository_profile"
# PERFORM_DELETE_PROFILE = "OMEVVFirmwareProfile.delete_firmware_repository_profile"
# PERFORM_TRIM = "ModifyFirmwareRepositoryProfile.trim_api_response"
# GET_PROFILE_BY_ID = "OMEVVFirmwareProfile.get_firmware_repository_profile_by_id"
# SEARCH_PROFILE_NAME = "OMEVVFirmwareProfile.search_profile_name"
# CREATE_DIFF_MODE_CHECK = "CreateFirmwareRepositoryProfile.diff_mode_check"
# DELETE_DIFF_MODE_CHECK = "DeleteFirmwareRepositoryProfile.diff_mode_check"
# HTTP_ERROR = "http error message"
# HTTP_ERROR_URL = 'https://testhost.com'
# RETURN_TYPE = "application/json"
# SHARE_PATH = "https://downloads.dell.com//catalog/catalog.xml.gz"
# PROFILE_NAME = "Dell Default Catalog"
# DESCRIPTION = "Latest Firmware From Dell"


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
        assert result

    def test_add_optional_fields(self, mocker, omevv_connection_firmware, omevv_default_args):
        firmware = {'targets': []}
        parameters = {}
        obj = MagicMock()
        param_key = 'check_vSAN_health'
        firmware_key = 'check_vSAN_health'
        omevv_obj = self.module.FirmwareUpdate(
            omevv_connection_firmware, obj)
        omevv_obj.add_optional_fields(firmware, parameters)
        result = None
        assert result is None

    def test_add_optional_fields_1(self, mocker, omevv_connection_firmware, omevv_default_args):
        firmware = {'targets': []}
        parameters = {}
        obj = MagicMock()
        param_key = None
        firmware_key = 'check_vSAN_health'
        omevv_obj = self.module.FirmwareUpdate(
            omevv_connection_firmware, obj)
        omevv_obj.add_optional_fields(firmware, parameters)
        result = None
        assert result is None
