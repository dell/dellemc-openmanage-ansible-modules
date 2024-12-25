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
from ansible_collections.dellemc.openmanage.plugins.modules import omevv_baseline_profile_info
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from io import StringIO
from unittest.mock import MagicMock
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
SUCCESS_MSG = "Successfully retrieved the baseline profile information."
NO_PROFILE_MSG = "'{profile_name}' baseline profile name does not exist in OMEVV."
INVOKE_REQ_KEY = "omevv_baseline_profile_info.RestOMEVV.invoke_request"
GET_PROFILE_INFO_KEY = "omevv_baseline_profile_info.OMEVVBaselineProfile.get_baseline_profiles"
GET_SPECIFIC_PROFILE_INFO_KEY = "omevv_baseline_profile_info.OMEVVBaselineProfile.get_baseline_profile_by_name"
PERFORM_OPERATION_KEY = "omevv_baseline_profile_info.OMEVVBaselineProfileInfo.perform_module_operation"
VCENTER_ERROR = "vCenter with UUID xx is not registered."
HTTP_ERROR = "http error message"
HTTP_ERROR_URL = 'https://testhost.com'
RETURN_TYPE = "application/json"


class TestOMEVVBaselineProfileInfo(FakeAnsibleModule):
    module = omevv_baseline_profile_info

    @pytest.fixture
    def omevv_baseline_profile_info_mock(self):
        omevv_obj = MagicMock()
        return omevv_obj

    @pytest.fixture
    def omevv_connection_vcenter_info(self, mocker, omevv_baseline_profile_info_mock):
        omevv_conn_mock = mocker.patch(MODULE_PATH + 'omevv_baseline_profile_info.RestOMEVV',
                                       return_value=omevv_baseline_profile_info_mock)
        omevv_conn_mock.return_value.__enter__.return_value = omevv_baseline_profile_info_mock
        return omevv_conn_mock

    def test_perform_operation(self, omevv_default_args, omevv_connection_vcenter_info,
                               omevv_baseline_profile_info_mock, mocker):
        sample_resp = [
            {
                "id": 1000,
                "name": "Baseline-1",
                "description": "Baseline-1 desc",
                "consoleId": "0b566c5f-49d6-4bcb-a480-7f380ab88aa3",
                "consoleAddress": "xx.xx.xx.xx",
                "firmwareRepoId": 1000,
                "firmwareRepoName": "Dell Default Catalog",
                "configurationRepoId": None,
                "configurationRepoName": None,
                "driverRepoId": None,
                "driverRepoName": None,
                "driftJobId": 1743,
                "driftJobName": "BP-Baseline-1-Host-Firmware-Drift-Detection",
                "dateCreated": "2024-10-16T10:25:29.786Z",
                "dateModified": None,
                "lastmodifiedBy": "Administrator@VSPHERE.LOCAL",
                "version": "1.0.0-0",
                "lastSuccessfulUpdatedTime": "2024-10-16T10:27:35.212Z",
                "clusterGroups": [],
                "datacenter_standAloneHostsGroups": [],
                "baselineType": None,
                "status": "SUCCESSFUL"
            },
            {
                "id": 1001,
                "name": "Baseline-2",
                "description": "Baseline - 2 description",
                "consoleId": "0b566c5f-49d6-4bcb-a480-7f380ab88aa3",
                "consoleAddress": "xx.xx.xx.xx",
                "firmwareRepoId": 1000,
                "firmwareRepoName": "Dell Default Catalog",
                "configurationRepoId": None,
                "configurationRepoName": None,
                "driverRepoId": None,
                "driverRepoName": None,
                "driftJobId": 1812,
                "driftJobName": "BP-Baseline - 2-Host-Firmware-Drift-Detection",
                "dateCreated": "2024-10-16T12:38:56.581Z",
                "dateModified": None,
                "lastmodifiedBy": "Administrator@VSPHERE.LOCAL",
                "version": "1.0.0-0",
                "lastSuccessfulUpdatedTime": "2024-10-16T12:41:02.641Z",
                "clusterGroups": [],
                "datacenter_standAloneHostsGroups": [
                    {
                        "associated_datacenterID": "datacenter-1001",
                        "associated_datacenterName": "Standalone Hosts-Test-DC",
                        "omevv_groupID": 1002
                    }
                ],
                "baselineType": "DATACENTER_NONCLUSTER",
                "status": "SUCCESSFUL"
            }
        ]
        # Scenario 1: Retrieve all baseline profile information
        mocker.patch(MODULE_PATH + GET_PROFILE_INFO_KEY, return_value=sample_resp)
        resp = self._run_module(omevv_default_args)
        assert resp['msg'] == SUCCESS_MSG
        assert resp['changed'] is False

        # Scenario 2: Retrieve single profile information
        omevv_default_args.update({'name': 'Baseline-1'})
        mocker.patch(MODULE_PATH + GET_SPECIFIC_PROFILE_INFO_KEY, return_value=sample_resp[0])
        resp = self._run_module(omevv_default_args)
        assert resp['msg'] == SUCCESS_MSG
        assert resp['changed'] is False

        # Scenario 3: Retrieve not successfull profile information
        profile_name = "Invalid_profile"
        omevv_default_args.update({'name': profile_name})
        mocker.patch(MODULE_PATH + GET_SPECIFIC_PROFILE_INFO_KEY, return_value={})
        resp = self._run_module(omevv_default_args)
        assert resp['msg'] == NO_PROFILE_MSG.format(profile_name=profile_name)
        assert resp['changed'] is False

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_omevv_baseline_profile_info_main_exception_handling_case(self, exc_type, mocker, omevv_default_args,
                                                                      omevv_connection_vcenter_info,
                                                                      omevv_baseline_profile_info_mock):
        omevv_baseline_profile_info_mock.status_code = 400
        omevv_baseline_profile_info_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + PERFORM_OPERATION_KEY,
                         side_effect=exc_type('test'))
        else:
            mocker.patch(MODULE_PATH + PERFORM_OPERATION_KEY,
                         side_effect=exc_type(HTTP_ERROR_URL, 400,
                                              HTTP_ERROR,
                                              {"accept-type": RETURN_TYPE},
                                              StringIO(json_str)))
        result = self._run_module(omevv_default_args)
        if exc_type != URLError:
            assert result['failed'] is True
        else:
            assert result['unreachable'] is True
        assert 'msg' in result

        # Scenario: When HTTPError gives SYS011
        error_msg = to_text(json.dumps(
            {"error": {'errorCode': {'MessageId': "12027", "Message": VCENTER_ERROR}}})
        )
        if exc_type in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + PERFORM_OPERATION_KEY,
                         side_effect=exc_type(HTTP_ERROR_URL, 400,
                                              HTTP_ERROR,
                                              {"accept-type": RETURN_TYPE},
                                              StringIO(error_msg)))
        result_out = self._run_module(omevv_default_args)
        assert 'msg' in result_out
