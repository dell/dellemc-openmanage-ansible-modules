# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.2.0
# Copyright (C) 2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import ome_configuration_compliance_baseline
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ssl import SSLError
from io import StringIO
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_configuration_compliance_baseline.'
INVALID_DEVICES = "{identifier} details are not available."
TEMPLATE_ID_ERROR_MSG = "Template with ID '{0}' not found."
TEMPLATE_NAME_ERROR_MSG = "Template '{0}' not found."
NAMES_ERROR = "Only delete operations accept multiple baseline names. All the other operations accept only a single " \
              "baseline name."
BASELINE_CHECK_MODE_CHANGE_MSG = "Baseline '{name}' already exists."
CHECK_MODE_CHANGES_MSG = "Changes found to be applied."
CHECK_MODE_NO_CHANGES_MSG = "No changes found to be applied."
BASELINE_CHECK_MODE_NOCHANGE_MSG = "Baseline '{name}' does not exist."
CREATE_MSG = "Successfully created the configuration compliance baseline."
DELETE_MSG = "Successfully deleted the configuration compliance baseline(s)."
TASK_PROGRESS_MSG = "The initiated task for the configuration compliance baseline is in progress."
CREATE_FAILURE_PROGRESS_MSG = "The initiated task for the configuration compliance baseline has failed"
INVALID_IDENTIFIER = "Target with {identifier} {invalid_val} not found."
IDEMPOTENCY_MSG = "The specified configuration compliance baseline details are the same as the existing settings."
INVALID_COMPLIANCE_IDENTIFIER = "Unable to complete the operation because the entered target {0} {1}" \
                                " is not associated with the baseline '{2}'."
INVALID_TIME = "job_wait_timeout {0} is not valid."
REMEDIATE_MSG = "Successfully completed the remediate operation."
MODIFY_MSG = "Successfully modified the configuration compliance baseline."
JOB_FAILURE_PROGRESS_MSG = "The initiated task for the configuration compliance baseline has failed."

device_info = {
    "value": [
        {
            "Id": Constants.device_id1,
            "Type": 2000,
            "Identifier": Constants.service_tag1,
            "DeviceServiceTag": Constants.service_tag1,
            "ChassisServiceTag": None,
            "Model": "PowerEdge MX7000",
            "PowerState": 17,
            "DeviceCapabilities": [33, 11],
            "ManagedState": 3000,
            "Status": 1000,
            "ConnectionState": True,
            "SystemId": 2031,
            "DeviceName": "MX-MOCK"
        },
        {
            "Id": Constants.device_id2,
            "Type": 2000,
            "Identifier": Constants.service_tag2,
            "DeviceServiceTag": Constants.service_tag2,
            "ChassisServiceTag": None,
            "Model": "PowerEdge MX7000",
            "PowerState": 17,
            "ManagedState": 3000,
            "Status": 1000,
            "ConnectionState": True,
            "SystemId": 2031,
            "DeviceName": "MX-MOCK"
        }
    ]
}

group_info = {
    "@odata.count": 2,
    "value": [
        {
            "Id": Constants.device_id1,
            "Name": "Network Mock",
        },
        {
            "Id": Constants.device_id2,
            "Name": "OEM Mock",
        }
    ]
}

baseline_info = {
    "@odata.count": 1,
    "value": [
        {
            "@odata.type": "#TemplateService.Baseline",
            "@odata.id": "/api/TemplateService/Baselines(30)",
            "Id": 30,
            "Name": "baseline5",
            "Description": None,
            "TemplateId": 102,
            "TemplateName": "one",
            "TemplateType": 2,
            "TaskId": 26606,
            "PercentageComplete": "100",
            "TaskStatus": 2070,
            "LastRun": "2021-03-02 19:29:31.503",
            "BaselineTargets": [
                {
                    "Id": 10074,
                    "Type": {
                        "Id": 1000,
                        "Name": "DEVICE"
                    }
                }
            ],
            "ConfigComplianceSummary": {
                "ComplianceStatus": "OK",
                "NumberOfCritical": 0,
                "NumberOfWarning": 0,
                "NumberOfNormal": 0,
                "NumberOfIncomplete": 0
            },
            "DeviceConfigComplianceReports@odata.navigationLink": "/api/TemplateService/Baselines(30)/DeviceConfigComplianceReports"
        }
    ]
}

baseline_output = {
    "Id": 30,
    "Name": "baseline5",
    "Description": None,
    "TemplateId": 102,
    "TemplateName": "one",
    "TemplateType": 2,
    "TaskId": 26606,
    "PercentageComplete": "100",
    "TaskStatus": 2070,
    "LastRun": "2021-03-02 19:29:31.503",
    "BaselineTargets": [
        {
            "Id": 10074,
            "Type": {
                "Id": 1000,
                "Name": "DEVICE"
            }
        }
    ],
    "ConfigComplianceSummary": {
        "ComplianceStatus": "OK",
        "NumberOfCritical": 0,
        "NumberOfWarning": 0,
        "NumberOfNormal": 0,
        "NumberOfIncomplete": 0
    },
}

compliance_report = {
    "@odata.count": 2,
    "value": [
        {
            "@odata.id": "/api/TemplateService/Baselines(30)/DeviceConfigComplianceReports({0})".format(
                Constants.device_id1),
            "Id": Constants.device_id1,
            "DeviceName": "mock_devicename",
            "Model": "mock_model",
            "ServiceTag": Constants.service_tag1,
            "ComplianceStatus": "COMPLIANT",
            "DeviceType": 1000,
            "InventoryTime": "2021-03-10 21:39:16.958627",
        },
        {
            "@odata.id": "/api/TemplateService/Baselines(30)/DeviceConfigComplianceReports({0})".format(
                Constants.device_id2),
            "Id": Constants.device_id2,
            "DeviceName": "mock_devicename",
            "Model": "mock_model",
            "ServiceTag": Constants.service_tag2,
            "ComplianceStatus": "NONCOMPLIANT",
            "DeviceType": 1000,
            "InventoryTime": "2021-03-10 21:39:16.958627",
        }
    ]
}


@pytest.fixture
def ome_connection_mock_for_compliance(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeConfigCompBaseline(FakeAnsibleModule):
    module = ome_configuration_compliance_baseline

    @pytest.mark.parametrize("params", [{"name": "baseline", "template_name": "iDRAC 13G Enable Low Latency Profile"},
                                        {"name": "baseline", "template_id": 1}])
    def test_ome_configuration_get_template_details_case1(self, params, ome_response_mock,
                                                          ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(params=params)
        template_info = {
            "@odata.count": 1,
            "value": [{
                "Id": 1,
                "Name": "iDRAC 13G Enable Low Latency Profile",
                "Description": "Tune workload for High Performance Computing Environment",
                "SourceDeviceId": 0,
                "TypeId": 2,
                "ViewTypeId": 4,
            }]
        }
        ome_response_mock.json_data = template_info
        template_data = self.module.get_template_details(f_module, ome_connection_mock_for_compliance)
        assert template_data == template_info["value"][0]

    @pytest.mark.parametrize("params", [{"names": "baseline", "template_name": "iDRAC 13G Enable Low Latency Profile"},
                                        {"names": "baseline", "template_id": 1}])
    def test_ome_configuration_get_template_details_case2(self, params, ome_response_mock,
                                                          ome_connection_mock_for_compliance):
        """
        when invalid template name and ids are provided
        """
        f_module = self.get_module_mock(params=params)
        template_info = {
            "@odata.count": 1,
            "value": []
        }
        ome_response_mock.json_data = template_info
        with pytest.raises(Exception) as err:
            self.module.get_template_details(f_module, ome_connection_mock_for_compliance)
        if "template_id" in params:
            assert err.value.args[0] == TEMPLATE_ID_ERROR_MSG.format(params['template_id'])
        else:
            assert err.value.args[0] == TEMPLATE_NAME_ERROR_MSG.format(params['template_name'])

    def test_validate_identifiers_case01(self):
        """
        No exception thrown when valid device ids are passed
        """
        requested_values = [Constants.device_id1, Constants.device_id2]
        f_module = self.get_module_mock(params={"device_ids": requested_values})
        available_values = dict([(item["Id"], item["Identifier"]) for item in device_info["value"]])
        self.module.validate_identifiers(available_values.keys(), requested_values, "device_ids", f_module)

    def test_validate_identifiers_case02(self):
        """
        No exception thrown when valid device se tagsrvice are passed
        """
        requested_values = [Constants.service_tag2, Constants.service_tag1]
        available_values = dict([(item["Id"], item["Identifier"]) for item in device_info["value"]])
        f_module = self.get_module_mock(params={"device_service_tags": requested_values})
        self.module.validate_identifiers(available_values.values(), requested_values, "device_service_tags", f_module)

    @pytest.mark.parametrize("val", [[Constants.service_tag1, "abc", "xyz"], ["abc", "xyz"]])
    def test_validate_identifiers_case03(self, val):
        """
        Exception should be thrown when invalid service tags are passed
        """
        requested_values = val
        f_module = self.get_module_mock(params={"device_service_tags": requested_values})
        available_values = dict([(item["Id"], item["Identifier"]) for item in device_info["value"]])
        with pytest.raises(Exception) as err:
            self.module.validate_identifiers(available_values.values(), requested_values, "device_service_tags",
                                             f_module)
        assert err.value.args[0].find("Target with device_service_tags") != -1

    def test_get_identifiers_case01(self):
        """
        get the device id from serivice tags
        """
        available_identifiers_map = dict([(item["Id"], item["Identifier"]) for item in device_info["value"]])
        requested_values = [Constants.service_tag1]
        val = self.module.get_identifiers(available_identifiers_map, requested_values)
        assert val == [Constants.device_id1]

    def test_get_identifiers_case02(self):
        """
          get the group id from group Names
          """
        available_identifiers_map = dict([(item["Id"], item["Name"]) for item in group_info["value"]])
        requested_values = ["OEM Mock"]
        val = self.module.get_identifiers(available_identifiers_map, requested_values)
        assert val == [Constants.device_id2]

    def test_get_group_ids(self, ome_connection_mock_for_compliance):
        """
        success case
        """
        f_module = self.get_module_mock(params={"device_group_names": ["OEM Mock"], "command": "create",
                                                "template_id": 2})
        ome_connection_mock_for_compliance.get_all_items_with_pagination.return_value = {
            "total_count": group_info["@odata.count"], "value": group_info["value"]}
        value = self.module.get_group_ids(f_module, ome_connection_mock_for_compliance)
        assert value == [Constants.device_id2]

    def test_get_group_ids_failure_case1(self, ome_connection_mock_for_compliance):
        """
        success case
        """
        f_module = self.get_module_mock(params={"device_group_names": ["OEM Mock Invalid"], "command": "create",
                                                "template_id": 2})
        ome_connection_mock_for_compliance.get_all_items_with_pagination.return_value = {
            "total_count": group_info["@odata.count"],
            "value": group_info["value"]
        }
        with pytest.raises(Exception) as err:
            self.module.get_group_ids(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == "Target with device_group_names OEM Mock Invalid not found."

    def test_get_group_ids_failure_case2(self, ome_connection_mock_for_compliance):
        """
        success case
        """
        f_module = self.get_module_mock(params={"device_group_names": ["OEM Mock Invalid"], "command": "create",
                                                "template_id": 2})
        ome_connection_mock_for_compliance.get_all_items_with_pagination.return_value = {
            "total_count": group_info["@odata.count"],
            "value": []
        }
        with pytest.raises(Exception) as err:
            self.module.get_group_ids(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == INVALID_DEVICES.format(identifier="Group")

    def test_get_device_ids_case01(self, ome_response_mock, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(
            params={"device_ids": [Constants.device_id2, Constants.device_id1], "command": "create",
                    "template_id": 2})
        ome_connection_mock_for_compliance.get_all_report_details.return_value = {
            "resp_obj": ome_response_mock, "report_list": device_info["value"]}
        value, compatible_map = self.module.get_device_ids(f_module, ome_connection_mock_for_compliance)
        assert value == [Constants.device_id2, Constants.device_id1]
        assert compatible_map == {"capable": [Constants.device_id1], "non_capable": [Constants.device_id2]}

    def test_get_device_ids_case2(self, ome_response_mock, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(params={"device_service_tags": [Constants.service_tag1], "command": "create",
                                                "template_id": 2})
        ome_connection_mock_for_compliance.get_all_report_details.return_value = {
            "resp_obj": ome_response_mock, "report_list": device_info["value"]}
        value, compatible_map = self.module.get_device_ids(f_module, ome_connection_mock_for_compliance)
        assert value == [Constants.device_id1]
        assert compatible_map == {"capable": [Constants.service_tag1], "non_capable": [Constants.service_tag2]}

    def test_get_device_ids_case01_failurecase(self, ome_response_mock, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(params={"device_ids": [100], "command": "create",
                                                "template_id": 2})
        ome_connection_mock_for_compliance.get_all_report_details.return_value = {
            "resp_obj": ome_response_mock, "report_list": device_info["value"]}
        with pytest.raises(Exception) as err:
            self.module.get_device_ids(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == "Target with device_ids 100 not found."

    def test_get_device_ids_case2_failure_case(self, ome_response_mock, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(params={"device_service_tags": ["xyz"], "command": "create",
                                                "template_id": 2})
        ome_connection_mock_for_compliance.get_all_report_details.return_value = {
            "resp_obj": ome_response_mock, "report_list": device_info["value"]}
        with pytest.raises(Exception) as err:
            self.module.get_device_ids(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == "Target with device_service_tags xyz not found."

    def test_get_device_ids_failure_case(self, ome_response_mock, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(params={"device_ids": [Constants.device_id2], "command": "create",
                                                "template_id": 2})
        ome_connection_mock_for_compliance.get_all_report_details.return_value = {
            "resp_obj": ome_response_mock, "report_list": []}
        with pytest.raises(Exception) as err:
            self.module.get_device_ids(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == INVALID_DEVICES.format(identifier="Device")

    def test_create_payload_case1(self, mocker, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(
            params={"device_ids": [Constants.device_id1, Constants.device_id2], "command": "create",
                    "template_id": 2, "names": ["baseline1"]})
        mocker.patch(MODULE_PATH + 'get_device_ids',
                     return_value=([Constants.device_id1, Constants.device_id2], {}))
        mocker.patch(MODULE_PATH + 'validate_capability',
                     return_value=None)
        mocker.patch(MODULE_PATH + 'get_template_details',
                     return_value={"Id": 2, "Name": "template1"})
        payload = self.module.create_payload(f_module, ome_connection_mock_for_compliance)
        assert payload == {
            "Name": "baseline1",
            "TemplateId": 2,
            "BaselineTargets": [{"Id": Constants.device_id1},
                                {"Id": Constants.device_id2}]
        }

    def test_create_payload_case2(self, mocker, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(
            params={"device_service_tags": [Constants.service_tag1, Constants.service_tag2], "command": "create",
                    "template_id": 2, "names": ["baseline1"]})
        mocker.patch(MODULE_PATH + 'get_device_ids',
                     return_value=([Constants.device_id1, Constants.device_id2], "map"))
        mocker.patch(MODULE_PATH + 'validate_capability',
                     return_value=None)
        mocker.patch(MODULE_PATH + 'get_template_details',
                     return_value={"Id": 2, "Name": "template1"})
        payload = self.module.create_payload(f_module, ome_connection_mock_for_compliance)
        assert payload == {
            "Name": "baseline1",
            "TemplateId": 2,
            "BaselineTargets": [{"Id": Constants.device_id1},
                                {"Id": Constants.device_id2}]
        }

    def test_create_payload_case3(self, mocker, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(params={"device_group_names": ["xyz"], "command": "create",
                                                "template_id": 2, "names": ["baseline1"]})
        mocker.patch(MODULE_PATH + 'get_group_ids',
                     return_value=[Constants.device_id1, Constants.device_id2])
        mocker.patch(MODULE_PATH + 'get_template_details',
                     return_value={"Id": 2, "Name": "template1"})
        payload = self.module.create_payload(f_module, ome_connection_mock_for_compliance)
        assert payload == {
            "Name": "baseline1",
            "TemplateId": 2,
            "BaselineTargets": [{"Id": Constants.device_id1},
                                {"Id": Constants.device_id2}]
        }

    def test_get_baseline_compliance_info(self, ome_connection_mock_for_compliance):
        ome_connection_mock_for_compliance.get_all_items_with_pagination.return_value = baseline_info
        val = self.module.get_baseline_compliance_info(ome_connection_mock_for_compliance, "baseline5", "Name")
        assert val == baseline_output

    def test_get_baseline_compliance_info_case2(self, ome_connection_mock_for_compliance):
        ome_connection_mock_for_compliance.get_all_items_with_pagination.return_value = baseline_info
        val = self.module.get_baseline_compliance_info(ome_connection_mock_for_compliance, 30, "Id")
        assert val == baseline_output

    def test_track_compliance_task_completion_case01(self, mocker, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(params={"device_group_names": ["xyz"], "command": "create",
                                                "template_id": 2, "names": ["baseline1"], "job_wait": True,
                                                "job_wait_timeout": 600})
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value=baseline_output)
        mocker.patch(MODULE_PATH + 'time.sleep', return_value=None)
        msg, info = self.module.track_compliance_task_completion(ome_connection_mock_for_compliance, 30, f_module)
        assert msg == CREATE_MSG
        assert info == baseline_output

    def test_track_compliance_task_completion_case02(self, mocker, ome_connection_mock_for_compliance):
        baseline_output["PercentageComplete"] = 25
        mocker.patch(MODULE_PATH + 'time.sleep', return_value=None)
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info', return_value=baseline_output)
        f_module = self.get_module_mock(params={"device_group_names": ["xyz"], "command": "create",
                                                "template_id": 2, "names": ["baseline1"], "job_wait": True,
                                                "job_wait_timeout": 600})
        msg, info = self.module.track_compliance_task_completion(ome_connection_mock_for_compliance, 30, f_module)
        assert msg == TASK_PROGRESS_MSG
        assert info == baseline_output
        assert info["PercentageComplete"] == 25

    def test_track_compliance_task_completion_case03(self, mocker, ome_connection_mock_for_compliance):
        baseline_output["PercentageComplete"] = 25
        mocker.patch(MODULE_PATH + 'time.sleep', return_value=None)
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info', return_value=baseline_output)
        f_module = self.get_module_mock(params={"device_group_names": ["xyz"], "command": "create",
                                                "template_id": 2, "names": ["baseline1"], "job_wait": False,
                                                "job_wait_timeout": 600})
        msg, info = self.module.track_compliance_task_completion(ome_connection_mock_for_compliance, 30, f_module)
        assert msg == TASK_PROGRESS_MSG
        assert info == baseline_output
        assert info["PercentageComplete"] == 25

    @pytest.mark.parametrize('val', [True, False])
    def test_validate_create_baseline_idempotency(self, mocker, val, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(params={"names": ["baseline5"]}, check_mode=val)
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value=baseline_output)
        with pytest.raises(Exception) as err:
            self.module.validate_create_baseline_idempotency(f_module,
                                                             ome_connection_mock_for_compliance)
        assert err.value.args[0] == BASELINE_CHECK_MODE_CHANGE_MSG.format(name=baseline_output["Name"])

    def test_validate_create_baseline_idempotency_case2(self, mocker, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(params={"names": ["baseline5"]}, check_mode=True)
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value=baseline_output)
        with pytest.raises(Exception) as err:
            self.module.validate_create_baseline_idempotency(f_module,
                                                             ome_connection_mock_for_compliance)
        assert err.value.args[0] == BASELINE_CHECK_MODE_CHANGE_MSG.format(name="baseline5")

    def test_create_baseline_case01(self, mocker, ome_response_mock, ome_connection_mock_for_compliance):
        mocker.patch(MODULE_PATH + 'validate_create_baseline_idempotency',
                     return_value=None)
        mocker.patch(MODULE_PATH + 'create_payload',
                     return_value={})
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value=baseline_output)
        f_module = self.get_module_mock(params={"names": ["baseline5"], "job_wait": False, "job_wait_timeout": 600},
                                        check_mode=False)
        ome_response_mock.json_data = {"Id": 1}
        ome_connection_mock_for_compliance.job_tracking.return_value = False, "message"
        with pytest.raises(Exception) as err:
            self.module.create_baseline(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == TASK_PROGRESS_MSG

    @pytest.mark.parametrize("val",
                             [(False, "Job completed successfully."), (False, "other message."), (True, "message2")])
    def test_create_baseline_case02(self, val, mocker, ome_response_mock, ome_connection_mock_for_compliance):
        mocker.patch(MODULE_PATH + 'validate_create_baseline_idempotency',
                     return_value=None)
        mocker.patch(MODULE_PATH + 'create_payload',
                     return_value={})
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value=baseline_output)
        f_module = self.get_module_mock(params={"job_wait": True, "job_wait_timeout": 600}, check_mode=False)
        ome_connection_mock_for_compliance.job_tracking.return_value = val[0], val[1]
        ome_response_mock.json_data = {"Id": 1}
        with pytest.raises(Exception) as err:
            self.module.create_baseline(f_module, ome_connection_mock_for_compliance)
        if val[0] is False and "successfully" in val[1]:
            assert err.value.args[0] == CREATE_MSG
        elif val[0] is False and "successfully" not in val[1]:
            assert err.value.args[0] == val[1]
        else:
            assert err.value.args[0] == val[1]

    def test_validate_names(self):
        f_module = self.get_module_mock(params={"names": ["abc"]}, check_mode=False)
        self.module.validate_names("create", f_module)

    def test_validate_names_case02(self):
        f_module = self.get_module_mock(params={"names": ["abc", "xyz"]}, check_mode=False)
        with pytest.raises(Exception) as err:
            self.module.validate_names("create", f_module)
        assert err.value.args[0] == NAMES_ERROR

    @pytest.mark.parametrize("command", ["create"])
    def test_compliance_operation(self, mocker, command, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(params={"names": ["abc"], "command": "create"}, check_mode=False)
        mocker.patch(MODULE_PATH + 'validate_job_time',
                     return_value=None)
        mock_create = mocker.patch(MODULE_PATH + 'create_baseline',
                                   return_value=None)
        self.module.compliance_operation(f_module, ome_connection_mock_for_compliance)
        assert mock_create.called

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_compliance_main_exception_failure_case(self, exc_type, mocker, ome_default_args,
                                                        ome_connection_mock_for_compliance, ome_response_mock):
        ome_default_args.update({"template_name": "t1", "names": "baseline1"})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'compliance_operation', side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'compliance_operation', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'compliance_operation',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result

    def test_compliance_create_argument_exception_case1(self, ome_default_args):
        ome_default_args.update({"template_name": "t1"})
        result = self._run_module_with_fail_json(ome_default_args)
        assert result["msg"] == "missing required arguments: names"

    def test_compliance_create_argument_exception_case2(self, ome_default_args):
        ome_default_args.update({"template_id": 1})
        result = self._run_module_with_fail_json(ome_default_args)
        assert result["msg"] == "missing required arguments: names"

    def test_compliance_create_argument_exception_case3(self, ome_default_args):
        ome_default_args.update({"names": "baseline1"})
        result = self._run_module_with_fail_json(ome_default_args)
        assert result["msg"] == "command is create but any of the following are missing: template_name, template_id"

    def test_compliance_create_argument_exception_case4(self, ome_default_args):
        ome_default_args.update({"names": "baseline1", "template_name": "t1", "template_id": 1})
        result = self._run_module_with_fail_json(ome_default_args)
        assert result["msg"] == "parameters are mutually exclusive: template_id|template_name"

    def test_compliance_create_argument_exception_case5(self, ome_default_args):
        ome_default_args.update({"names": "baseline1", "device_ids": 1, "template_name": "t1",
                                 "device_service_tags": "xyz"})
        result = self._run_module_with_fail_json(ome_default_args)
        assert result["msg"] == "parameters are mutually exclusive: device_ids|device_service_tags"

    def test_compliance_create_argument_exception_case6(self, ome_default_args):
        ome_default_args.update({"names": "baseline1", "template_name": "t1", "device_ids": 1,
                                 "device_group_names": "xyz"})
        result = self._run_module_with_fail_json(ome_default_args)
        assert result["msg"] == "parameters are mutually exclusive: device_ids|device_group_names"

    def test_compliance_create_argument_exception_case7(self, ome_default_args):
        ome_default_args.update({"names": "baseline1", "template_name": "t1", "device_service_tags": "abc",
                                 "device_group_names": "xyz"})
        result = self._run_module_with_fail_json(ome_default_args)
        assert result["msg"] == "parameters are mutually exclusive: device_service_tags|device_group_names"

    def test_compliance_create_argument_exception_case8(self, ome_default_args):
        ome_default_args.update(
            {"names": "baseline1", "template_name": "t1", "device_ids": 1, "device_service_tags": "xyz",
             "device_group_names": "abc"})
        result = self._run_module_with_fail_json(ome_default_args)
        assert result["msg"] == "parameters are mutually exclusive: device_ids|device_service_tags, " \
                                "device_ids|device_group_names, device_service_tags|device_group_names"

    @pytest.mark.parametrize("command", ["delete"])
    def test_compliance_operation_delete(self, mocker, command, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(params={"names": ["abc"], "command": "delete"}, check_mode=False)
        mock_delete_compliance = mocker.patch(MODULE_PATH + 'delete_compliance',
                                              return_value=None)
        mocker.patch(MODULE_PATH + 'validate_job_time',
                     return_value=None)
        self.module.compliance_operation(f_module, ome_connection_mock_for_compliance)
        assert mock_delete_compliance.called

    def test_delete_idempotency_check_case01(self, mocker, ome_connection_mock_for_compliance):
        mocker.patch(MODULE_PATH + 'get_identifiers',
                     return_value=[30])
        f_module = self.get_module_mock(params={"names": ["baseline5"]}, check_mode=False)
        ome_connection_mock_for_compliance.get_all_items_with_pagination.return_value = baseline_info
        val = self.module.delete_idempotency_check(f_module, ome_connection_mock_for_compliance)
        assert val == [30]

    def test_delete_idempotency_check_case02(self, mocker, ome_connection_mock_for_compliance):
        mocker.patch(MODULE_PATH + 'get_identifiers',
                     return_value=[30])
        f_module = self.get_module_mock(params={"names": ["baseline5"]}, check_mode=True)
        ome_connection_mock_for_compliance.get_all_items_with_pagination.return_value = baseline_info
        with pytest.raises(Exception) as err:
            self.module.delete_idempotency_check(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == CHECK_MODE_CHANGES_MSG

    def test_delete_idempotency_check_case03(self, mocker, ome_connection_mock_for_compliance):
        mocker.patch(MODULE_PATH + 'get_identifiers',
                     return_value=[])
        f_module = self.get_module_mock(params={"names": ["baseline5"]}, check_mode=True)
        ome_connection_mock_for_compliance.get_all_items_with_pagination.return_value = baseline_info
        with pytest.raises(Exception) as err:
            self.module.delete_idempotency_check(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == CHECK_MODE_NO_CHANGES_MSG

    def test_delete_compliance_case01(self, mocker, ome_connection_mock_for_compliance, ome_response_mock):
        mocker.patch(MODULE_PATH + 'delete_idempotency_check',
                     return_value=[30])
        f_module = self.get_module_mock(params={"names": ["baseline5"]}, check_mode=False)
        ome_response_mock.json_data = None
        ome_response_mock.status_code = 204
        with pytest.raises(Exception) as err:
            self.module.delete_compliance(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == DELETE_MSG

    def test_compliance_operation_modify(self, mocker, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(params={"names": ["abc"], "command": "modify"}, check_mode=False)
        mock_modify = mocker.patch(MODULE_PATH + 'modify_baseline',
                                   return_value=None)
        mocker.patch(MODULE_PATH + 'validate_job_time',
                     return_value=None)
        self.module.compliance_operation(f_module, ome_connection_mock_for_compliance)
        assert mock_modify.called

    @pytest.mark.parametrize("val", [(False, "Job completed successfully."), (False, "message1"), (True, "message2")])
    def test_modify_baseline_case01(self, val, mocker, ome_response_mock, ome_connection_mock_for_compliance):
        payload = {
            "Name": "baseline1",
            "TemplateId": 2,
            "BaselineTargets": [{"Id": Constants.device_id1},
                                {"Id": Constants.device_id2}]
        }
        f_module = self.get_module_mock(params={"names": ["abc"], "command": "modify", "job_wait": True,
                                                "job_wait_timeout": 600}, check_mode=False)
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value=baseline_output)
        mocker.patch(MODULE_PATH + 'create_payload',
                     return_value=payload)
        mocker.patch(MODULE_PATH + 'idempotency_check_for_command_modify',
                     return_value=None)
        ome_connection_mock_for_compliance.job_tracking.return_value = val[0], val[1]
        ome_response_mock.json_data = {"Id": 1}
        with pytest.raises(Exception) as err:
            self.module.modify_baseline(f_module, ome_connection_mock_for_compliance)
        if val[0] is False and "successfully" in val[1]:
            assert err.value.args[0] == MODIFY_MSG
        elif val[0] is False and "successfully" not in val[1]:
            assert err.value.args[0] == val[1]
        else:
            assert err.value.args[0] == val[1]

    def test_modify_baseline_case02(self, mocker, ome_response_mock, ome_connection_mock_for_compliance):
        payload = {
            "Name": "baseline1",
            "TemplateId": 2,
            "BaselineTargets": [{"Id": Constants.device_id1},
                                {"Id": Constants.device_id2}]
        }
        f_module = self.get_module_mock(
            params={"names": ["abc"], "command": "modify", "job_wait": False,
                    "job_wait_timeout": 600}, check_mode=False)
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value=baseline_output)
        mocker.patch(MODULE_PATH + 'create_payload',
                     return_value=payload)
        mocker.patch(MODULE_PATH + 'idempotency_check_for_command_modify',
                     return_value=None)
        ome_response_mock.json_data = {"Id": 1}
        with pytest.raises(Exception) as err:
            self.module.modify_baseline(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == TASK_PROGRESS_MSG

    def test_modify_baseline_case03(self, mocker, ome_response_mock, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(params={"names": ["abc"], "command": "modify"}, check_mode=False)
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value={})
        with pytest.raises(Exception) as err:
            self.module.modify_baseline(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == BASELINE_CHECK_MODE_NOCHANGE_MSG.format(name="abc")

    def test_modify_baseline_case04(self, mocker, ome_response_mock, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(params={"names": ["abc"], "command": "modify"}, check_mode=False)
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value={})
        with pytest.raises(Exception) as err:
            self.module.modify_baseline(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == BASELINE_CHECK_MODE_NOCHANGE_MSG.format(name="abc")

    def test_idempotency_check_for_command_modify_case1(self, mocker):
        f_module = self.get_module_mock(params={"names": ["abc"], "command": "modify"}, check_mode=True)
        mocker.patch(MODULE_PATH + 'compare_payloads',
                     return_value="diff")
        with pytest.raises(Exception) as err:
            self.module.idempotency_check_for_command_modify("current_payload", "expected_payload", f_module)
        assert err.value.args[0] == CHECK_MODE_CHANGES_MSG

    def test_idempotency_check_for_command_modify_case2(self, mocker):
        f_module = self.get_module_mock(params={"names": ["abc"], "command": "modify"}, check_mode=True)
        mocker.patch(MODULE_PATH + 'compare_payloads',
                     return_value=None)
        with pytest.raises(Exception) as err:
            self.module.idempotency_check_for_command_modify("current_payload", "expected_payload", f_module)
        assert err.value.args[0] == CHECK_MODE_NO_CHANGES_MSG

    def test_idempotency_check_for_command_modify_case3(self, mocker):
        f_module = self.get_module_mock(params={"names": ["abc"], "command": "modify"}, check_mode=False)
        mocker.patch(MODULE_PATH + 'compare_payloads',
                     return_value={})
        with pytest.raises(Exception) as err:
            self.module.idempotency_check_for_command_modify("current_payload", "expected_payload", f_module)
        assert err.value.args[0] == IDEMPOTENCY_MSG

    @pytest.mark.parametrize("modify_payload", [{"Id": 29, "Name": "baselin9", "TemplateId": 102},
                                                {"Id": 29, "Name": "baselin8", "TemplateId": 103},
                                                {"Id": 29, "Name": "baselin8", "TemplateId": 102,
                                                 "BaselineTargets": [{"Id": 10074}]},
                                                {"Id": 29, "Name": "baselin8", "TemplateId": 102,
                                                 "BaselineTargets": [{"Id": 10079}]},
                                                {"Id": 29, "Name": "baselin8", "TemplateId": 102,
                                                 "BaselineTargets": [{"Id": 10075},
                                                                     {"Id": 10074}]}
                                                ])
    def test_compliance_compare_payloads_diff_case_01(self, modify_payload):
        current_payload = {
            "Id": 29,
            "Name": "baselin8",
            "Description": "desc",
            "TemplateId": 102,
            "BaselineTargets": [
                {
                    "Id": 10075
                }
            ]
        }
        val = self.module.compare_payloads(modify_payload, current_payload)
        assert val is True

    @pytest.mark.parametrize("current_payload", [{"Id": 29, "Name": "baselin8", "Description": "desc1"},
                                                 {"Id": 29, "Name": "baselin9", "TemplateId": 102},
                                                 {"Id": 29, "Name": "baselin8", "TemplateId": 103},
                                                 {"Id": 29, "Name": "baselin8", "TemplateId": 102,
                                                  "BaselineTargets": [{"Id": 10074}]},
                                                 {"Id": 29, "Name": "baselin8", "TemplateId": 102,
                                                  "BaselineTargets": [{"Id": 10079}]}])
    def test_compliance_compare_payloads_diff_case_02(self, current_payload):
        modify_payload = {
            "Id": 29,
            "Name": "baselin8",
            "Description": "desc",
            "TemplateId": 102,
            "BaselineTargets": [
                {
                    "Id": 10075
                }
            ]
        }
        val = self.module.compare_payloads(modify_payload, current_payload)
        assert val is True

    @pytest.mark.parametrize("modify_payload", [{"Id": 29, "Name": "baselin8", "TemplateId": 102},
                                                {"Id": 29, "Name": "baselin8", "Description": "desc"},
                                                {"Id": 29, "Name": "baselin8",
                                                 "BaselineTargets": [{"Id": 10075}]}])
    def test_compliance_compare_payloads_no_diff_case_03(self, modify_payload):
        current_payload = {
            "Id": 29,
            "Name": "baselin8",
            "Description": "desc",
            "TemplateId": 102,
            "BaselineTargets": [
                {
                    "Id": 10075
                }
            ]
        }
        val = self.module.compare_payloads(modify_payload, current_payload)
        assert val is False

    def test_get_ome_version(self, ome_response_mock, ome_connection_mock_for_compliance):
        ome_response_mock.json_data = {
            "Name": "OM Enterprise",
            "Description": "OpenManage Enterprise",
            "Vendor": "Dell, Inc.",
            "ProductType": 1,
            "Version": "3.4.1",
            "BuildNumber": "24",
            "OperationJobId": 0
        }
        version = self.module.get_ome_version(ome_connection_mock_for_compliance)
        assert version == "3.4.1"

    def validate_validate_remediate_idempotency_with_device_ids(self, mocker, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(
            params={"device_ids": [Constants.device_id2, Constants.device_id1], "command": "remediate",
                    "names": ["baseline1"]})
        mocker.patch(MODULE_PATH + 'get_device_ids',
                     return_value=([Constants.device_id2, Constants.device_id1], "map"))
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value=baseline_output)
        ome_connection_mock_for_compliance.get_all_items_with_pagination.return_value = {
            "total_count": compliance_report["@odata.count"], "value": compliance_report["value"]}
        noncomplaint_devices, baseline_info = self.module.validate_remediate_idempotency(f_module,
                                                                                         ome_connection_mock_for_compliance)
        assert noncomplaint_devices == [Constants.device_id2]
        assert baseline_info == baseline_output

    def validate_validate_remediate_idempotency_with_service_tags(self, mocker, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(
            params={"device_ids": [Constants.service_tag1, Constants.service_tag2], "command": "remediate",
                    "names": ["baseline1"]})
        mocker.patch(MODULE_PATH + 'get_device_ids',
                     return_value=([Constants.device_id2, Constants.device_id1], "map"))
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value=baseline_output)
        ome_connection_mock_for_compliance.get_all_items_with_pagination.return_value = {
            "total_count": compliance_report["@odata.count"], "value": compliance_report["value"]}
        noncomplaint_devices, baseline_info = self.module.validate_remediate_idempotency(f_module,
                                                                                         ome_connection_mock_for_compliance)
        assert noncomplaint_devices == [Constants.device_id2]
        assert baseline_info == baseline_output

    def validate_validate_remediate_idempotency_without_devices(self, mocker, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(
            params={"command": "remediate", "names": ["baseline1"]})
        mocker.patch(MODULE_PATH + 'get_device_ids',
                     return_value=([Constants.device_id2, Constants.device_id1], "map"))
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value=baseline_output)
        ome_connection_mock_for_compliance.get_all_items_with_pagination.return_value = {
            "total_count": compliance_report["@odata.count"], "value": compliance_report["value"]}
        noncomplaint_devices, baseline_info = self.module.validate_remediate_idempotency(f_module,
                                                                                         ome_connection_mock_for_compliance)
        assert noncomplaint_devices == [Constants.device_id2]
        assert baseline_info == baseline_output

    def validate_validate_remediate_idempotency_wen_all_complaint(self, mocker, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(
            params={"command": "remediate", "names": ["baseline1"]})
        mocker.patch(MODULE_PATH + 'get_device_ids',
                     return_value=([Constants.device_id2, Constants.device_id1], "map"))
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value=baseline_output)
        report = {
            "@odata.count": 2,
            "value": [
                {
                    "Id": Constants.device_id1,
                    "ServiceTag": Constants.service_tag1,
                    "ComplianceStatus": "COMPLIANT"
                },
                {
                    "Id": Constants.device_id2,
                    "ServiceTag": Constants.service_tag2,
                    "ComplianceStatus": "COMPLIANT"
                }
            ]
        }
        ome_connection_mock_for_compliance.get_all_items_with_pagination.return_value = {
            "total_count": report["@odata.count"], "value": report["value"]}
        with pytest.raises(Exception) as err:
            self.module.validate_remediate_idempotency(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == CHECK_MODE_NO_CHANGES_MSG

    def validate_validate_remediate_idempotency_without_devices_check_mode(self, mocker,
                                                                           ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(
            params={"command": "remediate", "names": ["baseline1"]}, check_mode=True)
        mocker.patch(MODULE_PATH + 'get_device_ids',
                     return_value=([Constants.device_id2, Constants.device_id1], "map"))
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value=baseline_output)
        ome_connection_mock_for_compliance.get_all_items_with_pagination.return_value = {
            "total_count": compliance_report["@odata.count"], "value": compliance_report["value"]}
        with pytest.raises(Exception) as err:
            self.module.validate_remediate_idempotency(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == CHECK_MODE_CHANGES_MSG

    @pytest.mark.parametrize("val", ["3.4.1", "3.4.5", "3.4.0", "3.4", "3.3", "3.3.0", "3.0.0", "2.1"])
    def test_create_remediate_payload_case01_for_old_releases(self, val, mocker, ome_connection_mock_for_compliance):
        mocker.patch(MODULE_PATH + 'get_ome_version',
                     return_value=val)
        payload = self.module.create_remediate_payload([Constants.device_id1], baseline_output,
                                                       ome_connection_mock_for_compliance)
        assert "TargetIds" in payload

    @pytest.mark.parametrize("val", ["3.5.1", "3.5.5", "3.5.0", "3.5"])
    def test_create_remediate_payload_case01_for_new_releases(self, val, mocker, ome_connection_mock_for_compliance):
        mocker.patch(MODULE_PATH + 'get_ome_version',
                     return_value=val)
        payload = self.module.create_remediate_payload([Constants.device_id1], baseline_output,
                                                       ome_connection_mock_for_compliance)
        assert "DeviceIds" in payload

    def test_remediate_baseline_case1(self, mocker, ome_connection_mock_for_compliance, ome_response_mock):
        f_module = self.get_module_mock(
            params={"command": "remediate", "names": ["baseline1"], "job_wait": True, "job_wait_timeout": 600},
            check_mode=True)
        mocker.patch(MODULE_PATH + 'validate_remediate_idempotency',
                     return_value=([Constants.device_id1], baseline_output))
        mocker.patch(MODULE_PATH + 'create_remediate_payload',
                     return_value="payload")
        ome_response_mock.json_data = 1234
        ome_connection_mock_for_compliance.job_tracking.return_value = True, "job fail message"
        with pytest.raises(Exception) as err:
            self.module.remediate_baseline(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == "job fail message"

    def test_remediate_baseline_case2(self, mocker, ome_connection_mock_for_compliance, ome_response_mock):
        f_module = self.get_module_mock(
            params={"command": "remediate", "names": ["baseline1"], "job_wait": True, "job_wait_timeout": 600},
            check_mode=True)
        mocker.patch(MODULE_PATH + 'validate_remediate_idempotency',
                     return_value=([Constants.device_id1], baseline_output))
        mocker.patch(MODULE_PATH + 'create_remediate_payload',
                     return_value="payload")
        ome_response_mock.json_data = 1234
        ome_connection_mock_for_compliance.job_tracking.return_value = False, "Job completed successfully."
        with pytest.raises(Exception) as err:
            self.module.remediate_baseline(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == REMEDIATE_MSG

    def test_remediate_baseline_case3(self, mocker, ome_connection_mock_for_compliance, ome_response_mock):
        f_module = self.get_module_mock(
            params={"command": "remediate", "names": ["baseline1"], "job_wait": False, "job_wait_timeout": 600},
            check_mode=True)
        mocker.patch(MODULE_PATH + 'validate_remediate_idempotency',
                     return_value=([Constants.device_id1], baseline_output))
        mocker.patch(MODULE_PATH + 'create_remediate_payload',
                     return_value="payload")
        ome_response_mock.json_data = 1234
        with pytest.raises(Exception) as err:
            self.module.remediate_baseline(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == TASK_PROGRESS_MSG

    @pytest.mark.parametrize("inparams", [{"command": "create", "names": ["baseline1"],
                                           "job_wait": True, "job_wait_timeout": 0},
                                          {"command": "modify", "names": ["baseline1"], "job_wait": True,
                                           "job_wait_timeout": 0}])
    def test_validate_job_time(self, inparams):
        command = inparams['command']
        f_module = self.get_module_mock(
            params=inparams)
        with pytest.raises(Exception) as err:
            self.module.validate_job_time(command, f_module)
        assert err.value.args[0] == INVALID_TIME.format(inparams["job_wait_timeout"])

    @pytest.mark.parametrize("command", ["remediate"])
    def test_compliance_remediate_operation(self, mocker, command, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(params={"names": ["abc"], "command": "remediate"}, check_mode=False)
        mocker.patch(MODULE_PATH + 'validate_job_time',
                     return_value=None)
        mock_remediate = mocker.patch(MODULE_PATH + 'remediate_baseline',
                                      return_value=None)
        self.module.compliance_operation(f_module, ome_connection_mock_for_compliance)
        assert mock_remediate.called

    @pytest.mark.parametrize("inparams", [{"command": "modify", "names": ["baseline1"], "job_wait": True,
                                           "job_wait_timeout": 1},
                                          {"command": "modify", "names": ["baseline1"], "job_wait": False,
                                           "job_wait_timeout": 1},
                                          {"command": "delete", "names": ["baseline1"], "job_wait": True,
                                           "job_wait_timeout": 1},
                                          ])
    def test_validate_job_time_no_err_case(self, inparams):
        command = inparams['command']
        f_module = self.get_module_mock(
            params=inparams)
        self.module.validate_job_time(command, f_module)

    def test_remediate_baseline_case4(self, mocker, ome_connection_mock_for_compliance, ome_response_mock):
        f_module = self.get_module_mock(
            params={"command": "remediate", "names": ["baseline1"], "job_wait": True, "job_wait_timeout": 600},
            check_mode=True)
        mocker.patch(MODULE_PATH + 'validate_remediate_idempotency',
                     return_value=([Constants.device_id1], baseline_output))
        mocker.patch(MODULE_PATH + 'create_remediate_payload',
                     return_value="payload")
        ome_response_mock.json_data = 1234
        ome_connection_mock_for_compliance.job_tracking.return_value = False, "Job is running."
        with pytest.raises(Exception) as err:
            self.module.remediate_baseline(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == "Job is running."

    def test_modify_baseline_case05(self, mocker, ome_response_mock, ome_connection_mock_for_compliance):
        payload = {
            "Name": "baseline1",
            "TemplateId": 2
        }
        f_module = self.get_module_mock(params={"names": ["abc"], "command": "modify", "job_wait": False,
                                                "job_wait_timeout": 600}, check_mode=False)
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value=baseline_output)
        mocker.patch(MODULE_PATH + 'create_payload',
                     return_value=payload)
        mocker.patch(MODULE_PATH + 'idempotency_check_for_command_modify',
                     return_value=None)
        ome_response_mock.json_data = {"Id": 1}
        with pytest.raises(Exception) as err:
            self.module.modify_baseline(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == TASK_PROGRESS_MSG

    def test_validate_create_baseline_idempotency_case3(self, mocker, ome_connection_mock_for_compliance):
        f_module = self.get_module_mock(params={"names": ["baseline5"]}, check_mode=True)
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value={})
        with pytest.raises(Exception) as err:
            self.module.validate_create_baseline_idempotency(f_module,
                                                             ome_connection_mock_for_compliance)
        assert err.value.args[0] == CHECK_MODE_CHANGES_MSG

    def test_validate_capability_no_err_case01(self):
        capability_map = {"capable": [Constants.device_id1], "non_capable": [Constants.device_id2], }
        f_module = self.get_module_mock(params={"device_ids": [Constants.device_id1]}, check_mode=True)
        self.module.validate_capability(f_module, capability_map)

    def test_validate_capability_no_err_case02(self):
        capability_map = {"capable": [Constants.service_tag1], "non_capable": [Constants.service_tag2]}
        f_module = self.get_module_mock(params={"device_service_tags": [Constants.service_tag1]}, check_mode=True)
        self.module.validate_capability(f_module, capability_map)

    def test_validate_capability_err_case01(self):
        NO_CAPABLE_DEVICES = "Target device_service_tags contains devices which cannot be used for a baseline " \
                             "compliance operation."
        capability_map = {"capable": [Constants.service_tag2], "non_capable": [Constants.service_tag1]}
        f_module = self.get_module_mock(params={"device_service_tags": [Constants.service_tag1]}, check_mode=True)
        with pytest.raises(Exception) as err:
            self.module.validate_capability(f_module, capability_map)
        assert err.value.args[0] == NO_CAPABLE_DEVICES

    def test_validate_remediate_idempotency_case01(self, mocker, ome_connection_mock_for_compliance):
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value={})
        f_module = self.get_module_mock(params={"names": ["name1"]}, check_mode=True)
        with pytest.raises(Exception) as err:
            self.module.validate_remediate_idempotency(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == BASELINE_CHECK_MODE_NOCHANGE_MSG.format(name="name1")

    def test_validate_remediate_idempotency_case02(self, mocker, ome_connection_mock_for_compliance):
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value=baseline_output)
        compliance_status = [
            {
                "Id": Constants.device_id1,
                "DeviceName": "XX.XXX.X.XXX",
                "IpAddresses": [
                    "XX.XXX.X.XXX"
                ],
                "Model": "PowerEdge MX840c",
                "ServiceTag": Constants.service_tag1,
                "ComplianceStatus": 1,
                "DeviceType": 1000,
                "InventoryTime": "2020-10-05 18:28:09.842072"
            }
        ]
        f_module = self.get_module_mock(params={"names": ["name1"], "device_ids": [Constants.device_id1]},
                                        check_mode=True)
        capability_map = {"capable": [Constants.service_tag1], "non_capable": [Constants.service_tag2]}
        mocker.patch(MODULE_PATH + 'get_device_ids',
                     return_value=([Constants.device_id2, Constants.device_id1], capability_map))
        ome_connection_mock_for_compliance.get_all_items_with_pagination.return_value = {
            "total_count": 1, "value": compliance_status}
        with pytest.raises(Exception) as err:
            self.module.validate_remediate_idempotency(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == CHECK_MODE_NO_CHANGES_MSG

    def test_validate_remediate_idempotency_case03(self, mocker, ome_connection_mock_for_compliance):
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value=baseline_output)
        compliance_status = [
            {
                "Id": Constants.device_id1,
                "DeviceName": "XX.XXX.X.XXX",
                "IpAddresses": [
                    "XX.XXX.X.XXX"
                ],
                "Model": "PowerEdge MX840c",
                "ServiceTag": Constants.service_tag1,
                "ComplianceStatus": 2,
                "DeviceType": 1000,
                "InventoryTime": "2020-10-05 18:28:09.842072"
            }
        ]
        f_module = self.get_module_mock(params={"names": ["name1"], "device_ids": [Constants.device_id1]},
                                        check_mode=True)
        capability_map = {"capable": [Constants.service_tag1], "non_capable": [Constants.service_tag2]}
        mocker.patch(MODULE_PATH + 'get_device_ids',
                     return_value=([Constants.device_id2, Constants.device_id1], capability_map))
        ome_connection_mock_for_compliance.get_all_items_with_pagination.return_value = {
            "total_count": 1, "value": compliance_status}
        with pytest.raises(Exception) as err:
            self.module.validate_remediate_idempotency(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == CHECK_MODE_CHANGES_MSG

    def test_validate_remediate_idempotency_case04(self, mocker, ome_connection_mock_for_compliance):
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value=baseline_output)
        compliance_status = [
            {
                "Id": Constants.device_id1,
                "DeviceName": "XX.XXX.X.XXX",
                "IpAddresses": [
                    "XX.XXX.X.XXX"
                ],
                "Model": "PowerEdge MX840c",
                "ServiceTag": Constants.service_tag1,
                "ComplianceStatus": 2,
                "DeviceType": 1000,
                "InventoryTime": "2020-10-05 18:28:09.842072"
            }
        ]
        f_module = self.get_module_mock(params={"names": ["name1"], "device_service_tags": [Constants.service_tag1]},
                                        check_mode=True)
        capability_map = {"capable": [Constants.service_tag1], "non_capable": [Constants.service_tag2]}
        mocker.patch(MODULE_PATH + 'get_device_ids',
                     return_value=([Constants.device_id2, Constants.device_id1], capability_map))
        ome_connection_mock_for_compliance.get_all_items_with_pagination.return_value = {
            "total_count": 1, "value": compliance_status}
        with pytest.raises(Exception) as err:
            self.module.validate_remediate_idempotency(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == CHECK_MODE_CHANGES_MSG

    def test_validate_remediate_idempotency_case05(self, mocker, ome_connection_mock_for_compliance):
        mocker.patch(MODULE_PATH + 'get_baseline_compliance_info',
                     return_value=baseline_output)
        compliance_status = [
            {
                "Id": Constants.device_id1,
                "DeviceName": "XX.XXX.X.XXX",
                "IpAddresses": [
                    "XX.XXX.X.XXX"
                ],
                "Model": "PowerEdge MX840c",
                "ServiceTag": Constants.service_tag1,
                "ComplianceStatus": 2,
                "DeviceType": 1000,
                "InventoryTime": "2020-10-05 18:28:09.842072"
            }
        ]
        f_module = self.get_module_mock(params={"names": ["name1"]},
                                        check_mode=True)
        capability_map = {"capable": [Constants.service_tag1], "non_capable": [Constants.service_tag2]}
        mocker.patch(MODULE_PATH + 'get_device_ids',
                     return_value=([Constants.device_id2, Constants.device_id1], capability_map))
        ome_connection_mock_for_compliance.get_all_items_with_pagination.return_value = {
            "total_count": 1, "value": compliance_status}
        with pytest.raises(Exception) as err:
            self.module.validate_remediate_idempotency(f_module, ome_connection_mock_for_compliance)
        assert err.value.args[0] == CHECK_MODE_CHANGES_MSG
