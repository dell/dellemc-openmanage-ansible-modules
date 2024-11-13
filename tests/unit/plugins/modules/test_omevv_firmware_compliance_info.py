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
from ansible_collections.dellemc.openmanage.plugins.modules import omevv_firmware_compliance_info
from urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from io import StringIO
from unittest.mock import MagicMock
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.omevv_firmware_compliance_info.'
MODULE_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.omevv_utils.omevv_info_utils.OMEVVInfo.'

PARTIAL_HOST_WARN_MSG = "Unable to fetch the firmware compliance report of few of the hosts - {0}"
CLUSTER_NOT_VALID_MSG = "Unable to complete the operation because the {cluster_name} is not valid."
ALL_HOST_CLUSTER_NOT_VALID_MSG = "Unable to complete the operation because none of clusters and hosts are valid."
SUCCESS_FETCHED_MSG = "Successfully fetched the firmware compliance report."

FIRMWARE_COMPLIANCE = 'FirmwareComplianceInfo'
HTTP_ERROR = "http error message"
HTTP_ERROR_URL = 'https://testhost.com'
RETURN_TYPE = "application/json"
GET_HOST_GROUP_ID_AND_CLUSTER_NAME = ".get_hostid_groupid_and_cluster_name"


class TestFirmwareComplianceInfo(FakeAnsibleModule):
    module = omevv_firmware_compliance_info

    @pytest.fixture
    def omevv_firmware_compliance_info_mock(self):
        omevv_obj = MagicMock()
        return omevv_obj

    @pytest.fixture
    def omevv_connection_compliance_info(self, mocker, omevv_firmware_compliance_info_mock):
        omevv_conn_mock = mocker.patch(MODULE_PATH + 'RestOMEVV',
                                       return_value=omevv_firmware_compliance_info_mock)
        omevv_conn_mock.return_value.__enter__.return_value = omevv_firmware_compliance_info_mock
        return omevv_conn_mock

    def test_extract_host_id(self, mocker, omevv_default_args, omevv_connection_compliance_info):
        managed_hosts = [{"clusterName": "New Cluster", "id": 10},
                         {"clusterName": "Ansible Cluster", "id": 15}]
        invalid_result = {"hostnames": ["X.Y.Z"], "servicetags": ["ABC"]}
        mocker.patch(MODULE_UTILS_PATH + 'get_managed_host_details', return_value=(managed_hosts, invalid_result))
        f_module = self.get_module_mock(params=omevv_default_args)
        firm_compliance_obj = self.module.FirmwareComplianceInfo(omevv_connection_compliance_info, f_module)
        host_id = firm_compliance_obj.extract_host_id('ABCDEF', 'xx.xx.xx.xx', 'Ansible Cluster')
        assert host_id == [15]

    def test_get_hostid_groupid_and_cluster_name_without_cluster_input(self, omevv_default_args, omevv_connection_compliance_info):
        f_module = self.get_module_mock(params=omevv_default_args)
        firm_compliance_obj = self.module.FirmwareComplianceInfo(f_module, omevv_connection_compliance_info)
        flat_data = firm_compliance_obj.get_hostid_groupid_and_cluster_name()
        assert flat_data == ({}, [])

    def test_get_hostid_groupid_and_cluster_name_with_only_cluster_input(self, omevv_default_args,
                                                                         omevv_connection_compliance_info,
                                                                         mocker):
        omevv_default_args.update({"clusters": [{"cluster_name": "JHI Cluster"}]})
        mocker.patch(MODULE_UTILS_PATH + 'get_group_id_of_cluster', return_value=1005)
        mocker.patch(MODULE_PATH + FIRMWARE_COMPLIANCE + '.extract_host_id', return_value=[10, 12])
        f_module = self.get_module_mock(params=omevv_default_args)
        firm_compliance_obj = self.module.FirmwareComplianceInfo(f_module, omevv_connection_compliance_info)
        flat_data = firm_compliance_obj.get_hostid_groupid_and_cluster_name()
        assert flat_data == ({'JHI Cluster': {'groupId': 1005, 'hostId': [10, 12]}}, [])

    def test_get_hostid_groupid_and_cluster_name_with_invalid_cluster_input(self, omevv_default_args,
                                                                            omevv_connection_compliance_info,
                                                                            mocker):
        omevv_default_args.update({"clusters": [{"cluster_name": "Invalid Cluster"}]})
        mocker.patch(MODULE_UTILS_PATH + 'get_group_id_of_cluster', return_value=-1)
        mocker.patch(MODULE_PATH + FIRMWARE_COMPLIANCE + '.extract_host_id', return_value=[10, 9])
        f_module = self.get_module_mock(params=omevv_default_args)
        firm_compliance_obj = self.module.FirmwareComplianceInfo(f_module, omevv_connection_compliance_info)
        flat_data = firm_compliance_obj.get_hostid_groupid_and_cluster_name()
        assert flat_data == ({}, ['Invalid Cluster'])

    def test_execute_when_no_cluster(self, omevv_default_args,
                                     omevv_connection_compliance_info,
                                     mocker):
        cluster_detail = [{'cluster': 'PQR Cluster'}]
        mocker.patch(MODULE_PATH + FIRMWARE_COMPLIANCE + GET_HOST_GROUP_ID_AND_CLUSTER_NAME, return_value=({}, []))
        mocker.patch(MODULE_PATH + FIRMWARE_COMPLIANCE + '.get_all_cluster_drift_info', return_value=cluster_detail)
        resp = self._run_module(omevv_default_args)
        assert resp["msg"] == SUCCESS_FETCHED_MSG
        assert resp["firmware_compliance_info"] == cluster_detail

    def test_execute_when_specific_host(self, omevv_default_args,
                                        omevv_connection_compliance_info,
                                        mocker):
        host_detail = [{'cluster': 'PQR Cluster', 'host': 'xx.xx.xx.xx'}]
        mocker.patch(MODULE_PATH + FIRMWARE_COMPLIANCE + GET_HOST_GROUP_ID_AND_CLUSTER_NAME, return_value=(True, []))
        mocker.patch(MODULE_PATH + FIRMWARE_COMPLIANCE + '.get_host_drift_info', return_value=host_detail)
        resp = self._run_module(omevv_default_args)
        assert resp["msg"] == SUCCESS_FETCHED_MSG
        assert resp["firmware_compliance_info"] == host_detail

    def test_execute_when_no_host_cluster_matches(self, omevv_default_args,
                                                  omevv_connection_compliance_info,
                                                  mocker):
        host_detail = []
        mocker.patch(MODULE_PATH + FIRMWARE_COMPLIANCE + GET_HOST_GROUP_ID_AND_CLUSTER_NAME, return_value=({}, []))
        mocker.patch(MODULE_PATH + FIRMWARE_COMPLIANCE + '.get_host_drift_info', return_value=host_detail)
        resp = self._run_module(omevv_default_args)
        assert resp["msg"] == ALL_HOST_CLUSTER_NOT_VALID_MSG
        assert resp["skipped"] is True

    def test_get_host_drift_info(self, omevv_default_args,
                                 omevv_connection_compliance_info,
                                 mocker):
        flat_data = {"QWERTY Cluster": {'groupId': 1005, 'hostId': [10, 12]}}
        mocker.patch(MODULE_UTILS_PATH + 'get_firmware_drift_info_for_multiple_host', return_value=[{}])
        f_module = self.get_module_mock(params=omevv_default_args)
        firm_compliance_obj = self.module.FirmwareComplianceInfo(f_module, omevv_connection_compliance_info)
        out = firm_compliance_obj.get_host_drift_info('123', flat_data)
        assert out == [{"cluster": "QWERTY Cluster"}]

    def test_get_host_drift_info_with_HTTP_Error(self, omevv_default_args,
                                                 omevv_connection_compliance_info,
                                                 mocker):
        flat_data = {"AAA Cluster": {'groupId': 1005, 'hostId': [10, 12]}}
        f_module = self.get_module_mock(params=omevv_default_args)
        firm_compliance_obj = self.module.FirmwareComplianceInfo(f_module, omevv_connection_compliance_info)
        error_string = to_text(json.dumps({'errorCode': '18001', 'message': "Error"}))
        mocker.patch(MODULE_UTILS_PATH + 'get_firmware_drift_info_for_multiple_host',
                     side_effect=HTTPError(HTTP_ERROR_URL, 400,
                                           HTTP_ERROR,
                                           {"accept-type": RETURN_TYPE},
                                           StringIO(error_string)))
        out = firm_compliance_obj.get_host_drift_info('123', flat_data)
        assert out == []

    def test_get_all_cluster_drift_info(self, omevv_default_args,
                                        omevv_connection_compliance_info,
                                        mocker):
        all_cluster = [{'name': 'BB Cluster'}, {'name': 'CC Cluster'}]
        mocker.patch(MODULE_UTILS_PATH + 'get_cluster_info', return_value=all_cluster)
        mocker.patch(MODULE_UTILS_PATH + 'get_group_id_of_cluster', return_value=1000)
        mocker.patch(MODULE_UTILS_PATH + 'get_firmware_drift_info_for_single_cluster', return_value={})
        f_module = self.get_module_mock(params=omevv_default_args)
        firm_compliance_obj = self.module.FirmwareComplianceInfo(f_module, omevv_connection_compliance_info)
        out = firm_compliance_obj.get_all_cluster_drift_info('456')
        assert out == [{'cluster': 'BB Cluster'}, {'cluster': 'CC Cluster'}]

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_omevv_firmware_repository_profile_main_exception_handling_case(self, exc_type, mocker, omevv_default_args,
                                                                            omevv_firmware_compliance_info_mock):
        omevv_firmware_compliance_info_mock.status_code = 400
        omevv_firmware_compliance_info_mock.success = False
        json_str = to_text(json.dumps(
            {"errorCode": "501", "message": "Error"}))
        if exc_type in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + FIRMWARE_COMPLIANCE +
                         '.execute',
                         side_effect=exc_type(HTTP_ERROR_URL, 400,
                                              HTTP_ERROR,
                                              {"accept-type": RETURN_TYPE},
                                              StringIO(json_str)))
        else:
            mocker.patch(MODULE_PATH + FIRMWARE_COMPLIANCE +
                         '.execute', side_effect=exc_type('test'))
        result = self._run_module(omevv_default_args)
        if exc_type == URLError:
            assert result['changed'] is False
        else:
            assert result['failed'] is True
        assert 'msg' in result
