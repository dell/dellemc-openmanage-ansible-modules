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
from ansible_collections.dellemc.openmanage.plugins.modules import omevv_firmware_repository_profile_info
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from io import StringIO
from unittest.mock import MagicMock
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
SUCCESS_MSG = "Successfully retrieved the firmware repository profile information."
NO_PROFILE_MSG = "Unable to complete the operation because the '{profile_name}' is not a valid 'profile_name'."
FAILED_MSG = "Unable to fetch the firmware repository profile information."
INVOKE_REQ_KEY = "omevv_firmware_repository_profile_info.RestOMEVV.invoke_request"
GET_PROFILE_INFO_KEY = "omevv_firmware_repository_profile_info.OMEVVFirmwareProfile.get_firmware_repository_profile"
PERFORM_OPERATION_KEY = "omevv_firmware_repository_profile_info.OmevvFirmwareProfileInfo.perform_module_operation"
VCENTER_ERROR = "vCenter with UUID xx is not registered."
HTTP_ERROR = "http error message"
HTTP_ERROR_URL = 'https://testhost.com'
RETURN_TYPE = "application/json"


class TestOMEVVFirmwareRepositoryProfileInfo(FakeAnsibleModule):
    module = omevv_firmware_repository_profile_info

    @pytest.fixture
    def omevv_firmware_repository_profile_info_mock(self):
        omevv_obj = MagicMock()
        return omevv_obj

    @pytest.fixture
    def omevv_connection_vcenter_info(self, mocker, omevv_firmware_repository_profile_info_mock):
        omevv_conn_mock = mocker.patch(MODULE_PATH + 'omevv_firmware_repository_profile_info.RestOMEVV',
                                       return_value=omevv_firmware_repository_profile_info_mock)
        omevv_conn_mock.return_value.__enter__.return_value = omevv_firmware_repository_profile_info_mock
        return omevv_conn_mock

    def test_perform_operation(self, omevv_default_args, omevv_connection_vcenter_info,
                               omevv_firmware_repository_profile_info_mock, mocker):
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
            },

            {
                "id": 1001,
                "profileName": "Dell Default",
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
        # Scenario 1: Retrieve all profile information
        mocker.patch(MODULE_PATH + GET_PROFILE_INFO_KEY, return_value=sample_resp)
        resp = self._run_module(omevv_default_args)
        assert resp['msg'] == SUCCESS_MSG
        assert resp['changed'] is False

        # Scenario 2: Retrieve single profile information
        omevv_default_args.update({'name': 'Dell Default Catalog'})
        mocker.patch(MODULE_PATH + GET_PROFILE_INFO_KEY, return_value=sample_resp[0])
        resp = self._run_module(omevv_default_args)
        assert resp['msg'] == SUCCESS_MSG
        assert resp['changed'] is False

        # Scenario 3: Retrieve not successfull profile information
        omevv_default_args.update({'name': 'Invalid_profile'})
        mocker.patch(MODULE_PATH + GET_PROFILE_INFO_KEY, return_value={})
        resp = self._run_module(omevv_default_args)
        assert resp['msg'] == "'Invalid_profile' firmware repository profile name does not exist in OMEVV."
        assert resp['changed'] is False

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_omevv_firmware_repository_profile_info_main_exception_handling_case(self, exc_type, mocker, omevv_default_args,
                                                                                 omevv_connection_vcenter_info, omevv_firmware_repository_profile_info_mock):
        omevv_firmware_repository_profile_info_mock.status_code = 400
        omevv_firmware_repository_profile_info_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))
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

        # Scenario: When HTTPError gives SYS011
        error_string = to_text(json.dumps({"error": {'errorCode':
                                                     {
                                                         'MessageId': "12027",
                                                         "Message": VCENTER_ERROR
                                                     }}}))
        if exc_type in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + PERFORM_OPERATION_KEY,
                         side_effect=exc_type(HTTP_ERROR_URL, 400,
                                              HTTP_ERROR,
                                              {"accept-type": RETURN_TYPE},
                                              StringIO(error_string)))
        res_out = self._run_module(omevv_default_args)
        assert 'msg' in res_out
