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
from ansible_collections.dellemc.openmanage.plugins.modules import omevv_firmware_repository_profile
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from io import StringIO
from unittest.mock import MagicMock
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.omevv_firmware_repository_profile.'
MODULE_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.omevv_utils.omevv_firmware_utils.'
OME_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.ome.'
SUCCESS_MSG = "Successfully retrieved the firmware repository profile information."
NO_PROFILE_MSG = "Unable to complete the operation because the '{profile_name}' is not a valid 'profile_name'."
FAILED_CONN_MSG = "Unable to complete the operation. Please check the connection details."
FAILED_MSG = "Unable to fetch the firmware repository profile information."
INVOKE_REQ_KEY = "RestOMEVV.invoke_request"
TIME_SLEEP = "time.sleep"
OME_INVOKE_REQ = "ansible_collections.dellemc.openmanage.plugins.module_utils.ome.RestOME.invoke_request"
GET_PAYLOAD_DETAILS = "FirmwareRepositoryProfile.get_payload_details"
GET_PROFILE_INFO_KEY = "OMEVVFirmwareProfile.get_firmware_repository_profile"
PERFORM_OPERATION_KEY = "FirmwareRepositoryProfile.execute"
PERFORM_TEST_CONNECTION = "FirmwareRepositoryProfile.test_connection"
PERFORM_CREATE_PROFILE = "OMEVVFirmwareProfile.create_firmware_repository_profile"
PERFORM_MODIFY_PROFILE = "OMEVVFirmwareProfile.modify_firmware_repository_profile"
PERFORM_DELETE_PROFILE = "OMEVVFirmwareProfile.delete_firmware_repository_profile"
PERFORM_TRIM = "ModifyFirmwareRepositoryProfile.trim_api_response"
GET_PROFILE_BY_ID = "OMEVVFirmwareProfile.get_firmware_repository_profile_by_id"
SEARCH_PROFILE_NAME = "OMEVVFirmwareProfile.search_profile_name"
CREATE_DIFF_MODE_CHECK = "CreateFirmwareRepositoryProfile.diff_mode_check"
DELETE_DIFF_MODE_CHECK = "DeleteFirmwareRepositoryProfile.diff_mode_check"
HTTP_ERROR = "http error message"
HTTP_ERROR_URL = 'https://testhost.com'
RETURN_TYPE = "application/json"
SHARE_PATH = "https://downloads.dell.com//catalog/catalog.xml.gz"
PROFILE_NAME = "Dell Default Catalog"
DESCRIPTION = "Latest Firmware From Dell"
VSAN = "vSAN Catalog"


class TestFirmwareRepositoryProfile(FakeAnsibleModule):
    module = omevv_firmware_repository_profile

    @pytest.fixture
    def omevv_firmware_repository_profile_mock(self):
        omevv_obj = MagicMock()
        return omevv_obj

    @pytest.fixture
    def omevv_connection_firmware_repository_profile(self, mocker, omevv_firmware_repository_profile_mock):
        omevv_conn_mock = mocker.patch(MODULE_PATH + 'RestOMEVV',
                                       return_value=omevv_firmware_repository_profile_mock)
        omevv_conn_mock.return_value.__enter__.return_value = omevv_firmware_repository_profile_mock
        return omevv_conn_mock

    def test_execute(self, omevv_default_args, omevv_connection_firmware_repository_profile):
        obj = MagicMock()
        omevv_obj = self.module.FirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, obj)
        omevv_obj.execute()

    def test_get_payload_details(self, mocker, omevv_connection_firmware_repository_profile, omevv_default_args):
        # Scenario 1: payload details with description
        obj = MagicMock()
        omevv_obj = self.module.FirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, obj)
        obj.params.get.return_value = {
            "state": "present",
            "name": "test",
            "description": "Test6",
            "protocol_type": "HTTPS",
            "catalog_path": SHARE_PATH
        }
        result = omevv_obj.get_payload_details()
        assert result

        # Scenario 2: payload details with description as None
        obj = MagicMock()
        omevv_obj = self.module.FirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, obj)
        obj.params.get.return_value = {
            "state": "present",
            "name": "test",
            "protocol_type": "HTTPS",
            "catalog_path": SHARE_PATH,
            "description": None
        }
        result = omevv_obj.get_payload_details()
        assert result

    def test_connection(self, omevv_connection_firmware_repository_profile, omevv_default_args, mocker):
        obj = MagicMock()
        # Scenario 1: When test connection is successful
        obj.success = True
        mocker.patch(MODULE_UTILS_PATH +
                     'OMEVVFirmwareProfile.test_connection', return_value=obj)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.FirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.test_connection(None, None)
        assert result is True

        # Scenario 2: When test connection is not successful
        obj.success = False
        mocker.patch(MODULE_UTILS_PATH +
                     'OMEVVFirmwareProfile.test_connection', return_value=obj)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.FirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.test_connection(None, None)
        assert result is True

    def test_trim_api_response(self, omevv_connection_firmware_repository_profile, omevv_default_args):
        # Scenario 1: Complete api_response
        api_response = {
            "id": 1000,
            "profileName": PROFILE_NAME,
            "description": DESCRIPTION,
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH
        }
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.FirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.trim_api_response(api_response)
        assert result

        # Scenario 2: api_response without description
        api_response = {
            "id": 1000,
            "profileName": PROFILE_NAME,
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": None
        }
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.FirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.trim_api_response(api_response)
        assert result

        # Scenario 3: api_response without sharePath
        api_response = {
            "id": 1000,
            "profileName": PROFILE_NAME,
            "protocolType": "CIFS",
            "sharePath": "/catalog/",
            "fileName": "catalog",
            "description": None
        }
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.FirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.trim_api_response(api_response)
        assert result


class TestCreateFirmwareRepositoryProfile(FakeAnsibleModule):
    module = omevv_firmware_repository_profile

    @pytest.fixture
    def omevv_firmware_repository_profile_mock(self):
        omevv_obj = MagicMock()
        return omevv_obj

    @pytest.fixture
    def omevv_connection_firmware_repository_profile(self, mocker, omevv_firmware_repository_profile_mock):
        omevv_conn_mock = mocker.patch(MODULE_PATH + 'RestOMEVV',
                                       return_value=omevv_firmware_repository_profile_mock)
        omevv_conn_mock.return_value.__enter__.return_value = omevv_firmware_repository_profile_mock
        return omevv_conn_mock

    def test_diff_mode_check(self, omevv_connection_firmware_repository_profile, omevv_default_args):
        # Scenario 1: payload with shareCredential
        payload = {
            "profileName": "test",
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": "Test6",
            "profileType": "Firmware",
            "shareCredential": {
                "username": "",
                "password": "",
                "domain": ""
            }
        }
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.CreateFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.diff_mode_check(payload)
        assert result is None

        # Scenario 2: payload without shareCredential
        payload = {
            "profileName": "test",
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": "Test6",
            "profileType": "Firmware"
        }
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.CreateFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.diff_mode_check(payload)
        assert result is None

    def test_create_firmware_repository_profile(self, omevv_connection_firmware_repository_profile, omevv_default_args, mocker):
        obj = MagicMock()
        obj2 = MagicMock()
        obj3 = MagicMock()
        # Scenario 1: When creation is success
        obj.success = True
        payload = {
            "profileName": "test",
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": "Test6",
            "profileType": "Firmware",
            "shareCredential": {
                "username": "",
                "password": "",
                "domain": ""
            }
        }
        obj2.json_data = {
            "id": 1000,
            "profileName": PROFILE_NAME,
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": DESCRIPTION,
            "status": "Success"
        }
        obj3.json_data = {
            "id": 1000,
            "profileName": PROFILE_NAME,
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": DESCRIPTION,
            "status": "Parsing"
        }
        mocker.patch(
            MODULE_PATH + GET_PAYLOAD_DETAILS, return_value=payload)
        mocker.patch(
            MODULE_PATH + PERFORM_TEST_CONNECTION, return_value=True)
        mocker.patch(
            MODULE_PATH + CREATE_DIFF_MODE_CHECK, return_value={})
        mocker.patch(MODULE_UTILS_PATH +
                     PERFORM_CREATE_PROFILE, return_value=(obj, ""))
        mocker.patch(MODULE_UTILS_PATH +
                     GET_PROFILE_BY_ID, side_effect=[obj3, obj2])
        mocker.patch(MODULE_PATH +
                     TIME_SLEEP, return_value=None)
        f_module = self.get_module_mock(params=omevv_default_args)
        obj = self.module.CreateFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.create_firmware_repository_profile()
        assert result is None

        # Scenario 2: When creation is failed
        obj.success = False
        payload = {
            "profileName": "test",
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": "Test6",
            "profileType": "Firmware",
            "shareCredential": {
                "username": "",
                "password": "",
                "domain": ""
            }
        }
        mocker.patch(
            MODULE_PATH + GET_PAYLOAD_DETAILS, return_value=payload)
        mocker.patch(
            MODULE_PATH + PERFORM_TEST_CONNECTION, return_value=True)
        mocker.patch(
            MODULE_PATH + CREATE_DIFF_MODE_CHECK, return_value={})
        mocker.patch(MODULE_UTILS_PATH +
                     PERFORM_CREATE_PROFILE, return_value=(obj, ""))
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.CreateFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.create_firmware_repository_profile()
        assert result is None

        # Senario 3: When creation is failed because api_response's status is failed
        obj = MagicMock()
        obj.json_data = {
            "id": 1000,
            "profileName": PROFILE_NAME,
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": DESCRIPTION,
            "status": "Failed"
        }
        mocker.patch(
            MODULE_PATH + GET_PAYLOAD_DETAILS, return_value=payload)
        mocker.patch(
            MODULE_PATH + PERFORM_TEST_CONNECTION, return_value=True)
        mocker.patch(
            MODULE_PATH + CREATE_DIFF_MODE_CHECK, return_value={})
        mocker.patch(MODULE_UTILS_PATH +
                     PERFORM_CREATE_PROFILE, return_value=(obj, ""))
        mocker.patch(MODULE_UTILS_PATH +
                     GET_PROFILE_BY_ID, return_value=obj)
        f_module = self.get_module_mock(params=omevv_default_args)
        obj = self.module.CreateFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.create_firmware_repository_profile()
        assert result is None

        # Scenario 4: When test connection is not successful
        mocker.patch(
            MODULE_PATH + PERFORM_TEST_CONNECTION, return_value=False)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.CreateFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.create_firmware_repository_profile()
        assert result is None

    def test_execute(self, omevv_connection_firmware_repository_profile, omevv_default_args, mocker):
        # Scenario 1: When profile exists
        obj = MagicMock()
        payload = {
            "profileName": "test",
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": "Test6",
            "profileType": "Firmware",
            "shareCredential": {
                "username": "",
                "password": "",
                "domain": ""
            }
        }
        obj.json_data = {
            "id": 1000,
            "profileName": PROFILE_NAME,
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": DESCRIPTION,
            "status": "Success"
        }
        mocker.patch(
            MODULE_PATH + GET_PAYLOAD_DETAILS, return_value=payload)
        mocker.patch(MODULE_UTILS_PATH +
                     GET_PROFILE_INFO_KEY, return_value=obj)
        mocker.patch(MODULE_UTILS_PATH +
                     SEARCH_PROFILE_NAME, return_value=obj)
        mocker.patch(
            MODULE_PATH + 'FirmwareRepositoryProfile.trim_api_response', return_value=(obj, ""))
        mocker.patch(
            MODULE_PATH + 'FirmwareRepositoryProfile.test_connection', return_value=True)
        mocker.patch(
            MODULE_PATH + CREATE_DIFF_MODE_CHECK, return_value={})
        mocker.patch(MODULE_PATH + 'recursive_diff', return_value=(obj, ""))
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.CreateFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.execute()
        assert result is None

        # Scenario 2: When profile does not exists and check_mode is true
        obj = MagicMock()
        payload = {
            "profileName": "test",
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": "Test6",
            "profileType": "Firmware",
            "shareCredential": {
                "username": "",
                "password": "",
                "domain": ""
            }
        }
        mocker.patch(
            MODULE_PATH + GET_PAYLOAD_DETAILS, return_value=payload)
        mocker.patch(MODULE_UTILS_PATH +
                     GET_PROFILE_INFO_KEY, return_value={})
        mocker.patch(MODULE_UTILS_PATH +
                     SEARCH_PROFILE_NAME, return_value={})
        mocker.patch(
            MODULE_PATH + 'FirmwareRepositoryProfile.trim_api_response', return_value=(obj, ""))
        mocker.patch(
            MODULE_PATH + 'FirmwareRepositoryProfile.test_connection', return_value=True)
        mocker.patch(
            MODULE_PATH + CREATE_DIFF_MODE_CHECK, return_value={})
        mocker.patch(MODULE_PATH + 'recursive_diff', return_value=(obj, ""))
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=True)
        obj = self.module.CreateFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.execute()
        assert result is None


class TestModifyFirmwareRepositoryProfile(FakeAnsibleModule):
    module = omevv_firmware_repository_profile

    @pytest.fixture
    def omevv_firmware_repository_profile_mock(self):
        omevv_obj = MagicMock()
        return omevv_obj

    @pytest.fixture
    def omevv_connection_firmware_repository_profile(self, mocker, omevv_firmware_repository_profile_mock):
        omevv_conn_mock = mocker.patch(MODULE_PATH + 'RestOMEVV',
                                       return_value=omevv_firmware_repository_profile_mock)
        omevv_conn_mock.return_value.__enter__.return_value = omevv_firmware_repository_profile_mock
        return omevv_conn_mock

    def test_diff_check(self, mocker, omevv_default_args, omevv_connection_firmware_repository_profile):
        # Scenario 1: Default scenario
        module_response = {
            "profileName": "test",
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": "Test6",
            "profileType": "Firmware",
            "shareCredential": {
                "username": "",
                "password": "",
                "domain": ""
            }
        }
        api_response = {
            "id": 1000,
            "profileName": PROFILE_NAME,
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": DESCRIPTION,
            "status": "Success"
        }
        diff = {'description': 'Latest Firmware From Dell', 'id': 1000,
                'profileName': 'Dell Default Catalog', 'status': 'Success'}
        mocker.patch(
            MODULE_PATH + 'ModifyFirmwareRepositoryProfile.diff_check', return_value=diff)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.ModifyFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.diff_check(api_response, module_response)
        assert result == diff

        # Scenario 2: api_response with CIFS
        api_response = {
            "id": 1000,
            "profileName": PROFILE_NAME,
            "protocolType": "CIFS",
            "sharePath": "/catalog/",
            "description": DESCRIPTION,
            "status": "Success",
            "fileName": "Catalog.xml"
        }
        mocker.patch(
            MODULE_PATH + 'ModifyFirmwareRepositoryProfile.diff_check', return_value={})
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.ModifyFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.diff_check(api_response, module_response)
        assert result == {}

        # Scenario 3: module_response without share_path
        module_response = {
            "profileName": "test",
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": "Test6",
            "profileType": "Firmware"
        }
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.ModifyFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.diff_check(api_response, module_response)
        assert result == {}

    def test_trim_api_response(self, mocker, omevv_default_args, omevv_connection_firmware_repository_profile):
        # Scenario 1: Complete api_response
        api_response = {
            "id": 1000,
            "profileName": PROFILE_NAME,
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": DESCRIPTION,
            "status": "Success"
        }
        trimmed_resp = {
            "profileName": PROFILE_NAME,
            "sharePath": SHARE_PATH,
            "description": DESCRIPTION
        }
        mocker.patch(
            MODULE_PATH + PERFORM_TRIM, return_value=trimmed_resp)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.ModifyFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.trim_api_response(api_response)
        assert result == trimmed_resp

        # Scenario 2: payload without description
        api_response = {
            "id": 1000,
            "profileName": PROFILE_NAME,
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "status": "Success"
        }
        payload = {
            "profileName": "test",
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "profileType": "Firmware",
            "shareCredential": {
                "username": "",
                "password": "",
                "domain": ""
            }
        }
        trimmed_resp = {
            "profileName": PROFILE_NAME,
            "sharePath": SHARE_PATH
        }
        mocker.patch(
            MODULE_PATH + PERFORM_TRIM, return_value=trimmed_resp)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.ModifyFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.trim_api_response(api_response, payload)
        assert result == trimmed_resp

    def test_rec_diff(self, mocker, omevv_default_args, omevv_connection_firmware_repository_profile):
        api_response = {
            "id": 1000,
            "profileName": PROFILE_NAME,
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": DESCRIPTION,
            "status": "Success"
        }
        payload = {
            "profileName": "test",
            "sharePath": SHARE_PATH,
            "shareCredential": {
                "username": "",
                "password": "",
                "domain": ""
            }
        }
        mocker.patch(
            MODULE_PATH + PERFORM_TRIM, return_value={})
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.ModifyFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.rec_diff(api_response, payload)
        assert result is None

    def test_modify_firmware_repository_profile(self, mocker, omevv_default_args, omevv_connection_firmware_repository_profile):
        obj = MagicMock()
        # Scenario 1: When modification is required
        obj.success = True
        payload = {
            "profileName": "test",
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": "Test6",
            "profileType": "Firmware",
            "shareCredential": {
                "username": "",
                "password": "",
                "domain": ""
            }
        }
        api_response = {
            "id": 1996,
            "profileName": PROFILE_NAME,
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": DESCRIPTION,
            "status": "Success"
        }
        mocker.patch(
            MODULE_PATH + GET_PAYLOAD_DETAILS, return_value=payload)
        mocker.patch(
            MODULE_PATH + PERFORM_TEST_CONNECTION, return_value=True)
        mocker.patch(MODULE_PATH + 'ModifyFirmwareRepositoryProfile.rec_diff',
                     return_value={"profileName": "test"})
        mocker.patch(MODULE_UTILS_PATH +
                     PERFORM_MODIFY_PROFILE, return_value=(obj, ""))
        mocker.patch(
            MODULE_PATH + 'ModifyFirmwareRepositoryProfile.output_modify_response', return_value=None)
        f_module = self.get_module_mock(params=omevv_default_args)
        obj = self.module.ModifyFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.modify_firmware_repository_profile(api_response, payload)
        assert result is None

        # Scenario 2: When modification is not successful
        obj.success = False
        mocker.patch(MODULE_UTILS_PATH +
                     PERFORM_MODIFY_PROFILE, return_value=(obj, ""))
        mocker.patch(
            MODULE_PATH + 'ModifyFirmwareRepositoryProfile.output_modify_response', return_value=None)
        f_module = self.get_module_mock(params=omevv_default_args)
        obj = self.module.ModifyFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.modify_firmware_repository_profile(api_response, payload)
        assert result is None

        # Scenario 3: When test connection is not successful
        obj.success = False
        mocker.patch(
            MODULE_PATH + PERFORM_TEST_CONNECTION, return_value=False)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.ModifyFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.modify_firmware_repository_profile(payload, api_response)
        assert result is None

    def test_output_modify_response(self, mocker, omevv_default_args, omevv_connection_firmware_repository_profile):
        # Scenario 1: When modification is successful
        obj = MagicMock()
        obj2 = MagicMock()
        obj.success = True
        obj.json_data = {
            "id": 1000,
            "profileName": PROFILE_NAME,
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": DESCRIPTION,
            "status": "Parsing"
        }
        obj2.json_data = {
            "id": 1000,
            "profileName": PROFILE_NAME,
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": DESCRIPTION,
            "status": "Success"
        }
        api_response = {
            "id": 1996,
            "profileName": PROFILE_NAME,
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": DESCRIPTION,
            "status": "Success"
        }
        mocker.patch(MODULE_UTILS_PATH +
                     GET_PROFILE_BY_ID, side_effect=[obj, obj2])
        mocker.patch(MODULE_PATH +
                     TIME_SLEEP, return_value={})
        mocker.patch(MODULE_UTILS_PATH +
                     PERFORM_MODIFY_PROFILE, return_value=(obj, ""))
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.ModifyFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.output_modify_response(api_response)
        assert result is None

        # Scenario 2: When modification is not successful
        obj.json_data = {
            "id": 1000,
            "profileName": PROFILE_NAME,
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": DESCRIPTION,
            "status": "Failed"
        }
        mocker.patch(MODULE_UTILS_PATH +
                     GET_PROFILE_BY_ID, return_value=obj)
        mocker.patch(MODULE_UTILS_PATH +
                     PERFORM_MODIFY_PROFILE, return_value=(obj, ""))
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.ModifyFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.output_modify_response(api_response)
        assert result is None


class TestResyncFirmwareRepositoryProfile(FakeAnsibleModule):
    module = omevv_firmware_repository_profile

    @pytest.fixture
    def omevv_firmware_repository_profile_mock(self):
        omevv_obj = MagicMock()
        return omevv_obj

    @pytest.fixture
    def ome_mock(self):
        ome_obj = MagicMock()
        return ome_obj

    @pytest.fixture
    def omevv_connection_firmware_repository_profile(self, mocker, omevv_firmware_repository_profile_mock):
        omevv_conn_mock = mocker.patch(MODULE_PATH + 'RestOMEVV',
                                       return_value=omevv_firmware_repository_profile_mock)
        omevv_conn_mock.return_value.__enter__.return_value = omevv_firmware_repository_profile_mock
        return omevv_conn_mock

    @pytest.fixture
    def ome_connection(self, mocker, ome_mock):
        ome_conn_mock = mocker.patch(MODULE_PATH + 'RestOME',
                                     return_value=ome_mock)
        ome_conn_mock.return_value.__enter__.return_value = ome_mock
        return ome_conn_mock

    def test_check_plugin_availability(self, mocker, omevv_default_args, omevv_connection_firmware_repository_profile, ome_connection):
        # Scenario 1: When plugin is available
        obj = MagicMock()
        obj.json_data = {
            "value": [
                {
                    "Name": "Update Manager",
                    "Publisher": "DELL",
                    "CurrentVersion": "1.5.1.436",
                    "Description": "Dell OpenManage Update Manager facilitates the creation and management of custom Repositories and Catalogs."
                }]}
        mocker.patch(OME_INVOKE_REQ, return_value=obj)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.ResyncFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, ome_connection, f_module)
        result = obj.check_plugin_availability()
        assert result is None

        # Scenario 2: When plugin is not available
        obj = MagicMock()
        obj.json_data = {"value": []}
        mocker.patch(OME_INVOKE_REQ, return_value=obj)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.ResyncFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, ome_connection, f_module)
        result = obj.check_plugin_availability()
        assert result is None

    def test_check_mode_support(self, mocker, omevv_default_args, omevv_connection_firmware_repository_profile, ome_connection):
        # Scenario 1: When changes are found to be applied
        obj = MagicMock()
        obj.json_data = {
            "value": [
                {
                    "Id": 10022,
                    "Name": VSAN,
                    "Description": "null",
                    "DateModified": "2024-12-10 15:14:45.061",
                    "Owner": "admin",
                    "LastModifiedBy": "admin",
                    "CatalogType": "vSAN Catalog for Enterprise Servers",
                }
            ]}
        presync_result = [
            {
                "id": 1000,
                "owner": "OMEVV",
                "profileName": PROFILE_NAME,
                "profileType": "Firmware",
                "protocolType": "HTTPS",
                "sharePath": SHARE_PATH,
                "status": "Success"
            }]

        postsync_result = [
            {
                "id": 1086,
                "owner": "UMP",
                "profileName": VSAN,
                "profileType": "Firmware",
                "protocolType": "Not Applicable",
                "sharePath": "//shared/dell/omc/cifs/idrac/RepositoryStore",
                "status": "Success"
            }
        ]
        mocker.patch(MODULE_UTILS_PATH +
                     GET_PROFILE_INFO_KEY, return_value=presync_result)
        mocker.patch(OME_INVOKE_REQ, return_value=obj)
        mocker.patch(MODULE_PATH +
                     'ResyncFirmwareRepositoryProfile.remove_keys', return_value=None)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.ResyncFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, ome_connection, f_module)
        result = obj.check_mode_support()
        assert result is None

        # Scenario 2: When no changes are found to be applied
        mocker.patch(MODULE_UTILS_PATH +
                     GET_PROFILE_INFO_KEY, return_value=postsync_result)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.ResyncFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, ome_connection, f_module)
        result = obj.check_mode_support()
        assert result is None

    def test_remove_keys(self, mocker, omevv_default_args, omevv_connection_firmware_repository_profile, ome_connection):
        ump_profiles = [
            {
                "@odata.type": "#UpdateManagementService.Repository",
                "@odata.id": "/api/UpdateManagementService/Repositories(10024)",
                "UrgentComponentsCount": 0,
                "RecommendedComponentsCount": 5,
                "OptionalComponentsCount": 3,
                "BaselineId": "133",
                "BaselineName": "Check",
                "BaselineDescription": "null",
                "BaselineVersion": "null",
                "RefreshedVersion": "null",
                "Name": VSAN,
                "Version": 1.00
            }
        ]
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.ResyncFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, ome_connection, f_module)
        result = obj.remove_keys(ump_profiles, ump_profiles)
        assert result is None

    def test_sort_profiles(self, mocker, omevv_default_args, omevv_connection_firmware_repository_profile, ome_connection):
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.ResyncFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, ome_connection, f_module)
        result = obj.sort_profiles([])
        assert result == []

    def test_execute(self, mocker, omevv_default_args, omevv_connection_firmware_repository_profile, ome_connection):
        # Scenario 1: When plugin is available
        obj = MagicMock()
        obj.resp = 200
        mocker.patch(
            MODULE_PATH + 'ResyncFirmwareRepositoryProfile.check_plugin_availability', return_value=None)
        mocker.patch(MODULE_UTILS_PATH +
                     GET_PROFILE_INFO_KEY, return_value={})
        mocker.patch(MODULE_UTILS_PATH +
                     'OMEVVFirmwareProfile.resync_repository_profiles_from_ump', return_value=obj)
        mocker.patch(MODULE_PATH +
                     TIME_SLEEP, return_value=None)
        mocker.patch(MODULE_UTILS_PATH +
                     GET_PROFILE_INFO_KEY, return_value={})
        # mocker.patch(
        #     MODULE_PATH + 'ResyncFirmwareRepositoryProfile.diff_check', return_value=(0, {}))
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.ResyncFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, ome_connection, f_module)
        result = obj.execute()
        assert result is None

        # Scenario 2: When plugin is not available
        obj = MagicMock()
        obj.success = False
        mocker.patch(MODULE_UTILS_PATH +
                     'OMEVVFirmwareProfile.resync_repository_profiles_from_ump', return_value=obj)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.ResyncFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, ome_connection, f_module)
        result = obj.execute()
        assert result is None


class TestDeleteFirmwareRepositoryProfile(FakeAnsibleModule):
    module = omevv_firmware_repository_profile

    @pytest.fixture
    def omevv_firmware_repository_profile_mock(self):
        omevv_obj = MagicMock()
        return omevv_obj

    @pytest.fixture
    def omevv_connection_firmware_repository_profile(self, mocker, omevv_firmware_repository_profile_mock):
        omevv_conn_mock = mocker.patch(MODULE_PATH + 'RestOMEVV',
                                       return_value=omevv_firmware_repository_profile_mock)
        omevv_conn_mock.return_value.__enter__.return_value = omevv_firmware_repository_profile_mock
        return omevv_conn_mock

    def test_diff_mode_check(self, omevv_connection_firmware_repository_profile, omevv_default_args):
        # Scenario 1: payload with shareCredential
        payload = {
            "profileName": "test",
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": "Test6",
            "profileType": "Firmware",
        }
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.DeleteFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.diff_mode_check(payload)
        assert result is None

    def test_delete_firmware_repository_profile(self, mocker, omevv_default_args, omevv_connection_firmware_repository_profile):
        obj = MagicMock()
        # Scenario 1: when delete is successful
        obj.success = True
        api_response = {
            "id": 1996,
            "profileName": PROFILE_NAME,
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": DESCRIPTION,
            "status": "Success"
        }
        mocker.patch(
            MODULE_PATH + DELETE_DIFF_MODE_CHECK, return_value={})
        mocker.patch(MODULE_UTILS_PATH +
                     PERFORM_DELETE_PROFILE, return_value=obj)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.DeleteFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.delete_firmware_repository_profile(api_response)
        assert result is None

        # Scenario 2: When delete is not successful
        obj.success = False
        mocker.patch(MODULE_UTILS_PATH +
                     PERFORM_DELETE_PROFILE, return_value=obj)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.DeleteFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.delete_firmware_repository_profile(api_response)
        assert result is None

    def test_execute(self, mocker, omevv_default_args, omevv_connection_firmware_repository_profile):
        # Scenario 1: When profile does not exist
        obj = MagicMock()
        mocker.patch(MODULE_UTILS_PATH +
                     GET_PROFILE_INFO_KEY, return_value={})
        mocker.patch(MODULE_UTILS_PATH +
                     SEARCH_PROFILE_NAME, return_value={})
        mocker.patch(
            MODULE_PATH + DELETE_DIFF_MODE_CHECK, return_value={})
        mocker.patch(MODULE_UTILS_PATH +
                     PERFORM_DELETE_PROFILE, return_value=obj)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.DeleteFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.execute()
        assert result is None

        # Scenario 2: When profile does not exists and check_mode is true
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=True)
        obj = self.module.DeleteFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.execute()
        assert result is None

        # Scenario 3: When profile exists and check_mode is true
        obj = MagicMock()
        obj.success = True
        res = {
            "id": 1996,
            "profileName": PROFILE_NAME,
            "protocolType": "HTTPS",
            "sharePath": SHARE_PATH,
            "description": DESCRIPTION,
            "status": "Success"
        }
        mocker.patch(MODULE_UTILS_PATH +
                     GET_PROFILE_INFO_KEY, return_value=res)
        mocker.patch(MODULE_UTILS_PATH +
                     SEARCH_PROFILE_NAME, return_value=res)
        mocker.patch(
            MODULE_PATH + DELETE_DIFF_MODE_CHECK, return_value={})
        mocker.patch(MODULE_UTILS_PATH +
                     PERFORM_DELETE_PROFILE, return_value=obj)
        f_module = self.get_module_mock(
            params=omevv_default_args, check_mode=True)
        obj = self.module.DeleteFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.execute()
        assert result is None

        # Scenario 4: When profile exists and check_mode is false
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.DeleteFirmwareRepositoryProfile(
            omevv_connection_firmware_repository_profile, f_module)
        result = obj.execute()
        assert result is None

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_omevv_firmware_repository_profile_main_exception_handling_case(self, exc_type, mocker, omevv_default_args,
                                                                            omevv_firmware_repository_profile_mock):
        omevv_firmware_repository_profile_mock.status_code = 400
        omevv_firmware_repository_profile_mock.success = False
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
