# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.3
# Copyright (C) 2019-2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible_collections.dellemc.openmanage.tests.unit.compat.mock import patch, mock_open

import pytest
import json
import sys
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text
from ansible_collections.dellemc.openmanage.plugins.modules import ome_firmware
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'

device_resource = {"device_path": "DeviceService/Devices"}


@pytest.fixture
def ome_connection_firmware_mock(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'ome_firmware.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeFirmware(FakeAnsibleModule):
    module = ome_firmware

    @pytest.fixture
    def get_dup_file_mock(self):
        m = mock_open()
        m.return_value.readlines.return_value = ['this is line 1\n']

    payload = {
        "Builtin": False,
        "CreatedBy": "admin",
        "Editable": True,
        "EndTime": None,
        "Id": 29099,
        "JobDescription": "Firmware Update Task",
        "JobName": "Firmware Update Task",
        "JobStatus": {
            "Id": 2080,
            "Name": "New"
        },
        "JobType": {
            "Id": 5,
            "Internal": False,
            "Name": "Update_Task"
        },
        "LastRun": None,
        "LastRunStatus": {
            "Id": 2200,
            "Name": "NotRun"
        },
        "NextRun": None,
        "Params": [
            {
                "JobId": 29099,
                "Key": "operationName",
                "Value": "INSTALL_FIRMWARE"
            },
            {
                "JobId": 29099,
                "Key": "complianceUpdate",
                "Value": "false"
            },
            {
                "JobId": 29099,
                "Key": "stagingValue",
                "Value": "false"
            },
            {
                "JobId": 29099,
                "Key": "signVerify",
                "Value": "true"
            }
        ],
        "Schedule": "startnow",
        "StartTime": None,
        "State": "Enabled",
        "Targets": [
            {
                "Data": "DCIM:INSTALLED#741__BIOS.Setup.1-1=1577776981156",
                "Id": 28628,
                "JobId": 29099,
                "TargetType": {
                    "Id": 1000,
                    "Name": "DEVICE"
                }
            }
        ],
        "UpdatedBy": None,
        "Visible": True
    }

    @pytest.mark.parametrize("param", [payload])
    def test_spawn_update_job_case(self, param, ome_response_mock,
                                   ome_connection_firmware_mock):
        ome_response_mock.status_code = 201
        ome_response_mock.success = True
        ome_response_mock.json_data = {"Builtin": False,
                                       "CreatedBy": "admin",
                                       "Editable": True,
                                       "EndTime": None,
                                       "Id": 29099,
                                       "JobDescription": "Firmware Update Task",
                                       "JobName": "Firmware Update Task",
                                       "JobStatus": {"Id": 2080,
                                                     "Name": "New"},
                                       "JobType": {"Id": 5,
                                                   "Internal": False,
                                                   "Name": "Update_Task"},
                                       "LastRun": None,
                                       "LastRunStatus": {"Id": 2200,
                                                         "Name": "NotRun"},
                                       "NextRun": None,
                                       "Params": [{"JobId": 29099,
                                                   "Key": "operationName",
                                                   "Value": "INSTALL_FIRMWARE"},
                                                  {"JobId": 29099,
                                                   "Key": "complianceUpdate",
                                                   "Value": "false"},
                                                  {"JobId": 29099,
                                                   "Key": "stagingValue",
                                                   "Value": "false"},
                                                  {"JobId": 29099,
                                                   "Key": "signVerify",
                                                   "Value": "true"}],

                                       "Schedule": "startnow",
                                       "StartTime": None,
                                       "State": "Enabled",
                                       "Targets": [{"Data": "DCIM:INSTALLED#741__BIOS.Setup.1-1=1577776981156",
                                                    "Id": 28628,
                                                    "JobId": 29099,
                                                    "TargetType": {"Id": 1000,
                                                                   "Name": "DEVICE"}}],
                                       "UpdatedBy": None,
                                       "Visible": True}
        result = self.module.spawn_update_job(ome_connection_firmware_mock, param)
        assert result == param

    payload1 = {
        "Id": 0, "JobName": "Firmware Update Task",
        "JobDescription": "Firmware Update Task", "Schedule": "startnow",
        "State": "Enabled", "CreatedBy": "admin",
        "JobType": {"Id": 5, "Name": "Update_Task"},
        "Targets": [{
            "Data": "DCIM:INSTALLED#741__BIOS.Setup.1-1=1577786112600",
            "Id": 28628,
            "TargetType": {
                "Id": 1000,
                "Name": "SERVER"
            }
        }],
        "Params": [{"JobId": 0, "Key": "operationName", "Value": "INSTALL_FIRMWARE"},
                   {"JobId": 0, "Key": "complianceUpdate", "Value": "false"},
                   {"JobId": 0, "Key": "stagingValue", "Value": "false"},
                   {"JobId": 0, "Key": "signVerify", "Value": "true"}]
    }
    target_data = [
        {
            "Data": "DCIM:INSTALLED#741__BIOS.Setup.1-1=1577786112600",
            "Id": 28628,
            "TargetType": {
                "Id": 1000,
                "Name": "SERVER"
            }
        }
    ]

    @pytest.mark.parametrize("param", [{"inp": target_data, "out": payload1}])
    def _test_job_payload_for_update_success_case(self,
                                                  ome_connection_firmware_mock, param):
        f_module = self.get_module_mock()
        payload = self.module.job_payload_for_update(f_module,
                                                     ome_connection_firmware_mock, param["inp"])
        assert payload == param["out"]

    dupdata = [{"DeviceId": 1674, "DeviceReport": {"DeviceTypeId": "1000", "DeviceTypeName": "SERVER"}},
               {"DeviceId": 1662, "DeviceReport": {"DeviceTypeId": "1000", "DeviceTypeName": "SERVER"}}]

    filepayload1 = {'SingleUpdateReportBaseline': [],
                    'SingleUpdateReportGroup': [],
                    'SingleUpdateReportFileToken': 1577786112600,
                    'SingleUpdateReportTargets': [1674, 2222, 3333]}

    @pytest.mark.parametrize("param", [{"inp": filepayload1, "outp": target_data}])
    def test_get_applicable_components_success_case(self, param, ome_default_args, ome_response_mock,
                                                    ome_connection_firmware_mock):
        ome_response_mock.json_data = [
            {
                "DeviceId": 28628,
                "DeviceReport": {
                    "Components": [
                        {
                            "ComponentCriticality": "Recommended",
                            "ComponentCurrentVersion": "2.4.7",
                            "ComponentName": "PowerEdge BIOS",
                            "ComponentRebootRequired": "true",
                            "ComponentSourceName": "DCIM:INSTALLED#741__BIOS.Setup.1-1",
                            "ComponentTargetIdentifier": "159",
                            "ComponentUniqueIdentifier": "72400448-3a22-4da9-bd19-27a0e2082962",
                            "ComponentUpdateAction": "EQUAL",
                            "ComponentUriInformation": None,
                            "ComponentVersion": "2.4.7",
                            "ImpactAssessment": "",
                            "IsCompliant": "OK",
                            "PrerequisiteInfo": ""
                        }
                    ],
                    "DeviceIPAddress": "192.168.0.3",
                    "DeviceId": "28628",
                    "DeviceModel": "PowerEdge R940",
                    "DeviceName": "192.168.0.3",
                    "DeviceServiceTag": "HC2XFL2",
                    "DeviceTypeId": "1000",
                    "DeviceTypeName": "SERVER"
                }
            }
        ]
        ome_response_mock.success = True
        ome_response_mock.status_code = 200
        f_module = self.get_module_mock()
        result = self.module.get_applicable_components(ome_connection_firmware_mock, param["inp"], f_module)
        assert result == param["outp"]

    @pytest.mark.parametrize("param", [payload])
    def test_get_applicable_components_failed_case(self, param, ome_default_args, ome_response_mock):
        ome_response_mock.json_data = {
            "value": [{"DeviceReport": {"DeviceTypeId": "1000", "DeviceTypeName": "SERVER"}, "DeviceId": "Id"}]}
        ome_response_mock.status_code = 500
        ome_response_mock.success = False
        f_module = self.get_module_mock()
        with pytest.raises(Exception) as exc:
            self.module.get_applicable_components(ome_response_mock, param, f_module)
        assert exc.value.args[0] == "Unable to get components DUP applies."

    filepayload = {'SingleUpdateReportBaseline': [],
                   'SingleUpdateReportGroup': [],
                   'SingleUpdateReportTargets': [],
                   'SingleUpdateReportFileToken': '1577786112600'}

    outpayload = {'SingleUpdateReportBaseline': [],
                  'SingleUpdateReportGroup': [],
                  'SingleUpdateReportTargets': [],
                  'SingleUpdateReportFileToken': '1577786112600'}

    @pytest.mark.parametrize("duppayload", [{"inp": filepayload, "out": outpayload}])
    def test_get_dup_applicability_payload_success_case(self, duppayload):
        data = self.module.get_dup_applicability_payload("1577786112600", None, None)
        assert data == duppayload["out"]

    def test_upload_dup_file_success_case01(self, ome_connection_firmware_mock, ome_response_mock):
        ome_response_mock.json_data = "1577786112600"
        ome_response_mock.success = True
        ome_response_mock.status_code = 200
        f_module = self.get_module_mock(params={'dup_file': "/root1/Ansible_EXE/BIOS_87V69_WN64_2.4.7.EXE"})
        if sys.version_info.major == 3:
            builtin_module_name = 'builtins'
        else:
            builtin_module_name = '__builtin__'
        with patch("{0}.open".format(builtin_module_name), mock_open(read_data="data")) as mock_file:
            result = self.module.upload_dup_file(ome_connection_firmware_mock, f_module)
        assert result == (True, "1577786112600")

    def test_upload_dup_file_failure_case01(self, ome_response_mock, ome_connection_firmware_mock):
        ome_response_mock.json_data = {'value': [{"device_id": 28628,
                                                  "dup_file": "/root1/Ansible_EXE/BIOS_87V69_WN64_2.4.7.EXE"}]}
        ome_response_mock.success = False
        f_module = self.get_module_mock({'dup_file': False})
        with pytest.raises(Exception) as exc:
            self.module.upload_dup_file(ome_connection_firmware_mock, f_module)
        assert exc.value.args[0] == "argument {0} is type of {1} and we were unable to convert to string: {1} " \
                                    "cannot be converted to a string".format("dup_file", type(True))

    def test_upload_dup_file_failure_case02(self, ome_default_args,
                                            ome_connection_firmware_mock, ome_response_mock):
        ome_response_mock.json_data = {"value": [{"Id": [1111, 2222, 3333], "DeviceServiceTag": "KLBR222",
                                                  "dup_file": "/root/Ansible_EXE/BIOS_87V69_WN64_2.4.7.EXE"}]}
        ome_response_mock.status_code = 500

        if sys.version_info.major == 3:
            builtin_module_name = 'builtins'
        else:
            builtin_module_name = '__builtin__'
        f_module = self.get_module_mock(
            params={'dup_file': "/root1/Ansible_EXE/BIOS_87V69_WN64_2.4.7.EXE", 'hostname': '192.168.0.1'})
        with patch("{0}.open".format(builtin_module_name), mock_open(read_data="data")) as mock_file:
            with pytest.raises(Exception) as exc:
                self.module.upload_dup_file(ome_connection_firmware_mock, f_module)
        assert exc.value.args[0] == "Unable to upload {0} to {1}".format('/root1/Ansible_EXE/BIOS_87V69_WN64_2.4.7.EXE',
                                                                         '192.168.0.1')

    def test_get_device_ids_success_case(self, ome_connection_firmware_mock, ome_response_mock, ome_default_args):
        ome_default_args.update()
        ome_response_mock.status_code = 200
        ome_response_mock.json_data = {'value': [{'Id': 'DeviceServiceTag'}]}
        ome_response_mock.success = True
        f_module = self.get_module_mock()
        data = self.module.get_device_ids(ome_connection_firmware_mock, f_module, [1111, 2222, 3333])
        assert data == ['1111', '2222', '3333']

    def test_get_device_ids_failure_case01(self, ome_connection_firmware_mock, ome_response_mock):
        ome_response_mock.json_data = {'value': [{'Id': 'DeviceServiceTag'}]}
        ome_response_mock.success = False
        f_module = self.get_module_mock()
        with pytest.raises(Exception) as exc:
            self.module.get_device_ids(ome_connection_firmware_mock, f_module, ["@#!1", 2222, 3333])
        assert exc.value.args[0] == "Unable to complete the operation because the entered target device service" \
                                    " tag(s) or device id(s) '{0}' are invalid.".format("@#!1")

    def test__validate_device_attributes_success_case(self, ome_connection_firmware_mock, ome_response_mock,
                                                      ome_default_args):
        ome_default_args.update({'device_service_tag': ['R9515PT'], 'device_id': [2222]})
        ome_response_mock.status_code = 200
        ome_response_mock.json_data = {'value': [{'device_service_tag': ['R9515PT'], 'device_id': [2222]}]}
        ome_response_mock.success = True
        f_module = self.get_module_mock(params={'device_service_tag': ['R9515PT'], 'device_id': [2222]})
        data = self.module._validate_device_attributes(f_module)
        assert "R9515PT" in data

    def test__validate_device_attributes_failed_case(self, ome_connection_firmware_mock, ome_response_mock):
        ome_response_mock.json_data = {'value': [{'device_service_tag': None, 'device_id': None}]}
        ome_response_mock.success = False
        f_module = self.get_module_mock()
        # with pytest.raises(Exception) as exc:
        devlist = self.module._validate_device_attributes(f_module)
        assert devlist == []
        # assert exc.value.args[0] == "Either device_id or device_service_tag or device_group_names" \
        #                             " or baseline_names should be specified."

    def test_get_group_ids_fail_case(self, ome_default_args, ome_response_mock, ome_connection_firmware_mock):
        ome_default_args.update({'device_group_names': ["Servers"], "dup_file": ""})
        ome_response_mock.json_data = [{"Id": 1024,
                                        "Name": "Servers"}]
        ome_response_mock.success = False
        data = self._run_module_with_fail_json(ome_default_args)
        assert data["msg"] == "Unable to complete the operation because the entered target device group name(s)" \
                              " '{0}' are invalid.".format(",".join(set(["Servers"])))

    # def test_get_baseline_ids_fail_case(self, ome_default_args, ome_response_mock, ome_connection_firmware_mock):
    #     ome_default_args.update({'baseline_name': "baseline_servers",
    #     "dup_file": ""})
    #     ome_response_mock.json_data = [{"Id": 12,
    #                                     "Name": "baseline_servers"}]
    #     ome_response_mock.success = False
    #     data = self._run_module_with_fail_json(ome_default_args)
    #     assert data["msg"] == "Unable to complete the operation because the entered target baseline name" \
    #                           " '{0}' is invalid.".format(",".join(set([
    #         "baseline_servers"])))

    def test_main_firmware_success_case01(self, ome_default_args, mocker, ome_connection_firmware_mock):
        ome_default_args.update({"device_id": Constants.device_id1, "device_service_tag": Constants.service_tag1,
                                 "dup_file": ""})
        mocker.patch(MODULE_PATH + 'ome_firmware._validate_device_attributes',
                     return_value=[Constants.device_id1, Constants.service_tag1])
        mocker.patch(MODULE_PATH + 'ome_firmware.get_device_ids',
                     return_value=[Constants.device_id1, Constants.device_id2])
        mocker.patch(MODULE_PATH + 'ome_firmware.upload_dup_file',
                     return_value=["SUCCESS", "token_id"])
        mocker.patch(MODULE_PATH + 'ome_firmware.get_dup_applicability_payload',
                     return_value={"report_payload": "values"})
        mocker.patch(MODULE_PATH + 'ome_firmware.get_applicable_components',
                     return_value="target_data")
        mocker.patch(MODULE_PATH + 'ome_firmware.job_payload_for_update',
                     return_value={"job_payload": "values"})
        mocker.patch(MODULE_PATH + 'ome_firmware.spawn_update_job',
                     return_value="Success")
        data = self._run_module(ome_default_args)
        assert data['changed'] is True
        assert data['msg'] == "Successfully submitted the firmware update job."
        assert data['update_status'] == "Success"

    def test_main_firmware_success_case02(self, ome_default_args, mocker, ome_connection_firmware_mock):
        ome_default_args.update({"baseline_name": "baseline_name"})
        mocker.patch(MODULE_PATH + 'ome_firmware.validate_inputs')
        mocker.patch(MODULE_PATH + 'ome_firmware.get_baseline_ids',
                     return_value=[1, 2])
        mocker.patch(MODULE_PATH + 'ome_firmware.job_payload_for_update',
                     return_value={"job_payload": "values"})
        mocker.patch(MODULE_PATH + 'ome_firmware.spawn_update_job',
                     return_value="Success")
        mocker.patch(MODULE_PATH + 'ome_firmware.baseline_based_update',
                     return_value="target_data")
        data = self._run_module(ome_default_args)
        assert data['changed'] is True
        assert data['msg'] == "Successfully submitted the firmware update job."
        assert data['update_status'] == "Success"

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_firmware_main_exception_case(self, exc_type, mocker, ome_default_args,
                                          ome_response_mock, ome_connection_firmware_mock):
        ome_default_args.update({"device_id": Constants.device_id1, "device_service_tag": Constants.service_tag1,
                                 "dup_file": ""})
        mocker.patch(MODULE_PATH + 'ome_firmware._validate_device_attributes')
        ome_response_mock.json_data = {"value": [{"Id": "DeviceServiceTag",
                                                  "dup_file": ""}]}
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))

        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(
                MODULE_PATH + 'ome_firmware.get_device_ids')
            mocker.patch(
                MODULE_PATH + 'ome_firmware.upload_dup_file',
                side_effect=exc_type('test'))
        else:
            mocker.patch(
                MODULE_PATH + 'ome_firmware.get_dup_applicability_payload')
            mocker.patch(
                MODULE_PATH + 'ome_firmware.get_applicable_components')
            mocker.patch(
                MODULE_PATH + 'ome_firmware.job_payload_for_update')
            mocker.patch(
                MODULE_PATH + 'ome_firmware.spawn_update_job',
                side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                     {"accept-type": "application/json"}, StringIO(json_str)))
        if not exc_type == URLError:
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(ome_default_args)
        assert 'msg' in result

    def test_job_payload_for_update_case_01(self, ome_connection_firmware_mock):
        """response None case"""
        f_module = self.get_module_mock()
        target_data = {}
        ome_connection_firmware_mock.get_job_type_id.return_value = None
        msg = "Unable to fetch the job type Id."
        with pytest.raises(Exception, match=msg) as exc:
            self.module.job_payload_for_update(ome_connection_firmware_mock, f_module, target_data)

    def test_job_payload_for_update_case_02(self, ome_connection_firmware_mock, ome_response_mock):
        """baseline case"""
        f_module = self.get_module_mock()
        target_data = {}
        baseline = {"baseline_id": 1, "repo_id": 2, "catalog_id": 3}
        ome_connection_firmware_mock.get_job_type_id.return_value = ome_response_mock
        payload = self.module.job_payload_for_update(ome_connection_firmware_mock, f_module, target_data, baseline)
        for item in payload["Params"]:
            if item["Key"] == "complianceReportId":
                assert item["Value"] == str(baseline["baseline_id"])
            if item["Key"] == "repositoryId":
                assert item["Value"] == str(baseline["repo_id"])
            if item["Key"] == "catalogId":
                assert item["Value"] == str(baseline["catalog_id"])

    def test_job_payload_for_update_case_03(self, ome_connection_firmware_mock, ome_response_mock):
        """response None case"""
        f_module = self.get_module_mock()
        target_data = {}
        ome_connection_firmware_mock.get_job_type_id.return_value = ome_response_mock
        payload = self.module.job_payload_for_update(ome_connection_firmware_mock, f_module, target_data)
        for item in payload["Params"]:
            if "JobId" in item:
                assert item["JobId"] == 0
                assert item["Key"] == "complianceUpdate"
                assert item["Value"] == "false"

    def test_get_baseline_ids_case01(self, ome_connection_firmware_mock, ome_response_mock):
        response = {"report_list": [{"Name": "baseline_name", "Id": 1, "RepositoryId": 2, "CatalogId": 3}]}
        ome_response_mock.json_data = response
        ome_connection_firmware_mock.get_all_report_details.return_value = response
        f_module = self.get_module_mock(params={'baseline_name': "baseline_name"})
        baseline_detail = self.module.get_baseline_ids(ome_connection_firmware_mock, f_module)
        assert baseline_detail["baseline_id"] == response["report_list"][0]["Id"]
        assert baseline_detail["repo_id"] == response["report_list"][0]["RepositoryId"]
        assert baseline_detail["catalog_id"] == response["report_list"][0]["CatalogId"]

    def test_get_baseline_ids_case02(self, ome_connection_firmware_mock, ome_response_mock):
        response = {"report_list": [{"Name": "baseline_name", "Id": 1, "RepositoryId": 2, "CatalogId": 3}]}
        ome_response_mock.json_data = response
        ome_connection_firmware_mock.get_all_report_details.return_value = response
        f_module = self.get_module_mock(params={'baseline_name': "baseline_name2"})
        with pytest.raises(Exception) as exc:
            self.module.get_baseline_ids(ome_connection_firmware_mock, f_module)
        assert exc.value.args[0] == "Unable to complete the operation because the entered target" \
                                    " baseline name 'baseline_name2' is invalid."

    def test_get_baseline_ids_case03(self, ome_connection_firmware_mock, ome_response_mock):
        """Note: there is error in message format but UT message is updated as per module message"""
        response = {"report_list": {}}
        ome_response_mock.json_data = response
        ome_connection_firmware_mock.get_all_report_details.return_value = response
        f_module = self.get_module_mock(params={'baseline_name': "baseline_name2"})
        with pytest.raises(Exception) as exc:
            self.module.get_baseline_ids(ome_connection_firmware_mock, f_module)
        assert exc.value.args[0] == "Unable to complete the operation because" \
                                    " the enteredtarget baseline name does not exist."

    def test_get_dup_baseline_case_01(self, ome_connection_firmware_mock):
        baseline = "baseline_name1,baseline_name2,baseline_name3"
        report_list = [{'Name': 'baseline_name1', 'Id': 1}, {'Name': 'baseline_name2', 'Id': 2},
                       {'Name': 'baseline_name3', 'Id': 3}]
        ome_connection_firmware_mock.get_all_report_details.return_value = {"report_list": report_list}
        f_module = self.get_module_mock(params={'baseline_name': baseline})
        baseline_ids = self.module.get_dup_baseline(ome_connection_firmware_mock, f_module)
        assert baseline_ids == [1, 2, 3]

    def test_get_dup_baseline_exception_case_01(self, ome_connection_firmware_mock):
        baseline = "baseline_name5"
        report_list = [{'Name': 'baseline_name1', 'Id': 1}, {'Name': 'baseline_name2', 'Id': 2},
                       {'Name': 'baseline_name3', 'Id': 3}]
        ome_connection_firmware_mock.get_all_report_details.return_value = {"report_list": report_list}
        f_module = self.get_module_mock(params={'baseline_name': baseline})
        with pytest.raises(Exception) as exc:
            self.module.get_dup_baseline(ome_connection_firmware_mock, f_module)
        assert exc.value.args[0] == "Unable to complete the operation because the entered" \
                                    " target baseline name(s) 'baseline_name5' are invalid."

    def test_get_dup_baseline_exception_case_02(self, ome_connection_firmware_mock):
        baseline = "baseline_name1,baseline_name2,baseline_name3"
        ome_connection_firmware_mock.get_all_report_details.return_value = {"report_list": []}
        f_module = self.get_module_mock(params={'baseline_name': baseline})
        with pytest.raises(Exception) as exc:
            self.module.get_dup_baseline(ome_connection_firmware_mock, f_module)
        assert exc.value.args[0] == "Unable to complete the operation because the" \
                                    " enteredtarget baseline name(s) does not exists."

    def test_baseline_based_update_exception_case_01(self, ome_connection_firmware_mock):
        ome_connection_firmware_mock.get_all_report_details.return_value = {"report_list": []}
        f_module = self.get_module_mock()
        with pytest.raises(Exception) as exc:
            self.module.baseline_based_update(ome_connection_firmware_mock, f_module, {"baseline_id": 1})
        assert exc.value.args[0] == "No components available for update."

    def test_baseline_based_update_case_02(self, ome_connection_firmware_mock):
        f_module = self.get_module_mock(params={'baseline_id': 1})
        response = {"report_list": [
            {"DeviceId": 1111, "DeviceTypeId": 2000, "DeviceName": "MX-111", "DeviceTypeName": "CHASSIS",
             "ComponentComplianceReports": [{"UpdateAction": "UPGRADE", "SourceName": "SAS.xx.x2"}]}]}
        ome_connection_firmware_mock.get_all_report_details.return_value = response
        compliance_report_list = self.module.baseline_based_update(ome_connection_firmware_mock, f_module,
                                                                   {"baseline_id": 1})
        assert compliance_report_list == [
            {'Id': 1111, 'Data': 'SAS.xx.x2', 'TargetType': {'Id': 2000, 'Name': 'CHASSIS'}}]

    def test_baseline_based_update_case_03(self, ome_connection_firmware_mock):
        f_module = self.get_module_mock(params={'baseline_id': 1})
        response = {"report_list": [
            {"DeviceId": 1111, "DeviceTypeId": 2000, "DeviceName": "MX-111", "DeviceTypeName": "CHASSIS",
             "ComponentComplianceReports": []}]}
        ome_connection_firmware_mock.get_all_report_details.return_value = response
        with pytest.raises(Exception, match="No components available for update.") as exc:
            self.module.baseline_based_update(ome_connection_firmware_mock, f_module, {"baseline_id": 1})

    def test_validate_inputs(self):
        f_module = self.get_module_mock(params={"device_id": 111})
        msg = "Parameter 'dup_file' to be provided along with 'device_id'|'device_service_tag'|'device_group_names'"
        with pytest.raises(Exception) as exc:
            self.module.validate_inputs(f_module)
        assert exc.value.args[0] == msg
