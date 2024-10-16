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
import json
from ansible_collections.dellemc.openmanage.plugins.modules import omevv_firmware_repository_profile
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from io import StringIO
from mock import MagicMock
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.omevv_firmware_repository_profile.'
SUCCESS_MSG = "Successfully retrieved the firmware repository profile information."
NO_PROFILE_MSG = "Unable to complete the operation because the '{profile_name}' is not a valid 'profile_name'."
FAILED_MSG = "Unable to fetch the firmware repository profile information."
INVOKE_REQ_KEY = "RestOMEVV.invoke_request"
GET_PROFILE_INFO_KEY = "OMEVVFirmwareProfile.get_firmware_repository_profile"
PERFORM_OPERATION_KEY = "FirmwareRepositoryProfile.execute"
HTTP_ERROR = "http error message"
HTTP_ERROR_URL = 'https://testhost.com'
RETURN_TYPE = "application/json"


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

    def test_connection(self, omevv_connection_firmware_repository_profile, omevv_default_args, mocker):
        payload = {
            "profileName": "test",
            "description": "Test6",
            "protocolType": "HTTPS",
            "profileType": "Firmware",
            "sharePath": "https://downloads.dell.com////catalog/catalog.xml.gz",
            "catalogPath": "https://downloads.dell.com////catalog/catalog.xml.gz",
            "checkCertificate": False}
        mocker.patch(MODULE_PATH + 'FirmwareRepositoryProfile.get_payload_details', return_value=payload)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.FirmwareRepositoryProfile(omevv_connection_firmware_repository_profile, f_module)
        result = obj.test_connection()
        assert result == True

    def test_get_firmware_repository_profile(self, omevv_connection_firmware_repository_profile, omevv_default_args, mocker):
        obj = MagicMock()
        sample_resp = [
            {
                "id": 1000,
                "profileName": "Dell Default Catalog",
                "description": "Latest Firmware From Dell",
                "profileType": "Firmware",
                "sharePath": "https://downloads.dell.com//catalog/catalog.xml.gz",
                "fileName": "catalog.xml",
                "status": "Success",
                "factoryCreated": True,
                "factoryType": "Default",
                "catalogCreatedDate": "2024-08-27T01:58:10Z",
                "catalogLastChecked": "2024-09-09T19:30:16Z",
                "checkCertificate": "",
                "protocolType": "HTTPS",
                "createdBy": "OMEVV Default",
                "modifiedBy": "",
                "owner": "OMEVV"
            }
        ]
        obj.json_data = sample_resp
        mocker.patch(MODULE_PATH + 'FirmwareRepositoryProfile.execute', return_value=True)
        mocker.patch(MODULE_PATH + GET_PROFILE_INFO_KEY, return_value=obj)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.FirmwareRepositoryProfile(omevv_connection_firmware_repository_profile, f_module)
        result = obj.get_firmware_repository_profile()
        assert result == sample_resp

    def test_search_profile_name(self, omevv_connection_firmware_repository_profile, omevv_default_args):
        data = [
            {
                "id": 1000,
                "profileName": "Dell Default Catalog",
                "description": "Latest Firmware From Dell",
                "profileType": "Firmware",
                "sharePath": "https://downloads.dell.com//catalog/catalog.xml.gz",
                "fileName": "catalog.xml",
                "status": "Success",
                "factoryCreated": True,
                "factoryType": "Default",
                "catalogCreatedDate": "2024-08-27T01:58:10Z",
                "catalogLastChecked": "2024-09-09T19:30:16Z",
                "checkCertificate": "",
                "protocolType": "HTTPS",
                "createdBy": "OMEVV Default",
                "modifiedBy": "",
                "owner": "OMEVV"
            }
        ]
        # Scenario 1: When profile name is present in the list
        profile_name = "Dell Default Catalog"
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.FirmwareRepositoryProfile(omevv_connection_firmware_repository_profile, f_module)
        result = obj.search_profile_name(data, profile_name)
        assert result == data[0]

        # Scenario 2: When profile name is not present in the list
        profile_name = "Dell"
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.FirmwareRepositoryProfile(omevv_connection_firmware_repository_profile, f_module)
        result = obj.search_profile_name(data, profile_name)
        assert result == {}

    def test_validate_catalog_path(self, omevv_connection_firmware_repository_profile, omevv_default_args):
        protocol_type = "HTTPS"        
        # Scenario 1: When catalog path is valid
        catalog_path = "https://downloads.dell.com//catalog/catalog.xml.gz"
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.FirmwareRepositoryProfile(omevv_connection_firmware_repository_profile, f_module)
        obj.validate_catalog_path(protocol_type, catalog_path)

        # Scenario 2: When catalog path is not valid
        protocol_type = "HTTPS"
        catalog_path = "https://downloads.dell.com//catalog/catalog"
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.FirmwareRepositoryProfile(omevv_connection_firmware_repository_profile, f_module)
        assert obj.validate_catalog_path(protocol_type, catalog_path) is None


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
    
    def test_create_firmware_repository_profile(self, omevv_connection_firmware_repository_profile, omevv_default_args, mocker):
        obj = MagicMock()
        # Scenario 1: When creation is success
        obj.success = True
        payload = {
            "profileName": "test",
            "description": "Test6",
            "protocolType": "HTTPS",
            "profileType": "Firmware",
            "sharePath": "https://downloads.dell.com////catalog/catalog.xml.gz"}
        mocker.patch(MODULE_PATH + 'FirmwareRepositoryProfile.get_payload_details', return_value=payload)
        mocker.patch(MODULE_PATH + 'FirmwareRepositoryProfile.execute', return_value=True)
        mocker.patch(MODULE_PATH + GET_PROFILE_INFO_KEY, return_value=obj)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj = self.module.CreateFirmwareRepositoryProfile(omevv_connection_firmware_repository_profile, f_module)
        obj.create_firmware_repository_profile()

        # Scenario 2: When creation is failed
        obj2 = MagicMock()
        obj2.status_code = 400
        mocker.patch(MODULE_PATH + 'FirmwareRepositoryProfile.get_payload_details', return_value=payload)
        mocker.patch(MODULE_PATH + 'FirmwareRepositoryProfile.execute', return_value=True)
        mocker.patch(MODULE_PATH + GET_PROFILE_INFO_KEY, return_value=obj2)
        f_module = self.get_module_mock(
            params=omevv_default_args)
        obj2 = self.module.CreateFirmwareRepositoryProfile(omevv_connection_firmware_repository_profile, f_module)
        obj2.create_firmware_repository_profile()

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_omevv_firmware_repository_profile_main_exception_handling_case(self, exc_type, mocker, omevv_default_args,
                                                                                 omevv_connection_firmware_repository_profile, omevv_firmware_repository_profile_mock):
        omevv_firmware_repository_profile_mock.status_code = 400
        omevv_firmware_repository_profile_mock.success = False
        json_str = to_text(json.dumps({"errorCode": "501", "message": "Error"}))
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
            assert result['unreachable'] is True
        else:
            assert result['failed'] is True
        assert 'msg' in result

        # Scenario 1: When errorCode is 18001
        error_string = to_text(json.dumps({'errorCode': '18001', 'message': "Error"}))
        if exc_type in [HTTPError]:
            mocker.patch(MODULE_PATH + PERFORM_OPERATION_KEY,
                         side_effect=exc_type(HTTP_ERROR_URL, 400,
                                              HTTP_ERROR,
                                              {"accept-type": RETURN_TYPE},
                                              StringIO(error_string)))
        res_out = self._run_module(omevv_default_args)
        assert 'msg' in res_out

        # Scenario 2: When errorCode is 500
        error_string = to_text(json.dumps({'errorCode': '500', 'message': "Error"}))
        if exc_type in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + PERFORM_OPERATION_KEY,
                         side_effect=exc_type(HTTP_ERROR_URL, 400,
                                              HTTP_ERROR,
                                              {"accept-type": RETURN_TYPE},
                                              StringIO(error_string)))
        res_out = self._run_module(omevv_default_args)
        assert 'msg' in res_out
