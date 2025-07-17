# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.3
# Copyright (C) 2019-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
from io import StringIO
from ssl import SSLError

import pytest
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import ome_firmware_baseline
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

BASELINE_JOB_RUNNING = "Firmware baseline '{name}' with ID {id} is running. Please retry after job completion."
MULTI_BASLEINES = "Multiple baselines present. Run the module again using a specific ID."
BASELINE_DEL_SUCCESS = "Successfully deleted the firmware baseline."
NO_CHANGES_MSG = "No changes found to be applied."
INVALID_BASELINE_ID = "Invalid baseline ID provided."
BASELINE_TRIGGERED = "Successfully triggered the firmware baseline task."
NO_CATALOG_MESSAGE = "Catalog name not provided for baseline creation."
NO_TARGETS_MESSAGE = "Targets not specified for baseline creation."
CATALOG_STATUS_MESSAGE = "Unable to create the firmware baseline as the catalog is in {status} status."
BASELINE_UPDATED = "Successfully {op} the firmware baseline."
DISCOVER_JOB_COMPLETE = "Successfully completed the Discovery job."
JOB_TRACK_SUCCESS = "Discovery job has {0}."
JOB_TRACK_FAIL = "No devices discovered, job is in {0} state."
SETTLING_TIME = 3
MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline.'

payload_out1 = {
    "Name": "baseline1",
    "Description": "baseline_description",
    "CatalogId": 12,
    "RepositoryId": 23,
    "DowngradeEnabled": True,
    'FilterNoRebootRequired': True,
    "Is64Bit": True,
    "Targets": [
        {"Id": 123,
         "Type": {
             "Id": 1000,
             "Name": "DEVICE"
         }}]
}
payload_out2 = {
    "Name": "baseline1",
    "CatalogId": 12,
    'FilterNoRebootRequired': False,
    "RepositoryId": 23, 'Description': None, 'DowngradeEnabled': True, 'Is64Bit': True,
    "Targets": [
        {"Id": 123,
         "Type": {
             "Id": 1000,
             "Name": "DEVICE"
         }}]
}

baseline_status1 = {
    "CatalogId": 123,
    "Description": "BASELINE DESCRIPTION",
    "DeviceComplianceReports": [],
    "DowngradeEnabled": True,
    "Id": 0,
    "Is64Bit": True,
    "Name": "my_baseline",
    "RepositoryId": 123,
    "RepositoryName": "catalog123",
    "RepositoryType": "HTTP",
    "Targets": [
        {
            "Id": 10083,
            "Type": {
                "Id": 1000,
                "Name": "DEVICE"
            }
        },
        {
            "Id": 10076,
            "Type": {
                "Id": 1000,
                "Name": "DEVICE"
            }
        }
    ],
    "TaskId": 11235,
    "TaskStatusId": 0
}


@pytest.fixture
def ome_connection_mock_for_firmware_baseline(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(
        'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeFirmwareBaseline(FakeAnsibleModule):
    module = ome_firmware_baseline

    @pytest.fixture
    def mock__get_catalog_payload(self, mocker):
        mock_payload = mocker.patch(
            MODULE_PATH + '_get_baseline_payload',
            return_value={
                "Name": "baseline_name",
                "CatalogId": "cat_id",
                "RepositoryId": "repo_id",
                "Targets": {}
            }
        )
        return mock_payload

    catrepo_param1 = "catalog1"
    catrepo_out1 = (22, 12)
    catrepo_param2 = None
    catrepo_out2 = (None, None)
    catrepo_param3 = "catalog3"
    catrepo_out3 = (None, None)

    @pytest.mark.parametrize("params", [{"inp": catrepo_param1, "out": catrepo_out1},
                                        {"inp": catrepo_param2, "out": catrepo_out2},
                                        {"inp": catrepo_param3, "out": catrepo_out3}])
    def test_get_catrepo_ids(self, ome_connection_mock_for_firmware_baseline,
                             ome_response_mock, params):
        ome_connection_mock_for_firmware_baseline.get_all_items_with_pagination.return_value = {
            "value": [
                {
                    "Id": 22,
                    "Repository": {
                        "Id": 12,
                        "Name": "catalog1",
                    },
                    "Status": "Completed"
                },
                {
                    "Id": 23,
                    "Repository": {
                        "Id": 12,
                        "Name": "catalog2",
                    },
                    "Status": "Completed"
                }
            ]
        }
        f_module = self.get_module_mock(params=params["inp"])
        catrepo = self.module.get_catrepo_ids(f_module, params["inp"], ome_connection_mock_for_firmware_baseline)
        assert catrepo == params["out"]

    @pytest.mark.parametrize("params", [{"inp": catrepo_param1, "out": catrepo_out1}])
    def test_get_catrepo_ids_fail(self, ome_connection_mock_for_firmware_baseline,
                                  ome_response_mock, params):
        ome_connection_mock_for_firmware_baseline.get_all_items_with_pagination.return_value = {
            "value": [
                {
                    "Id": 22,
                    "Repository": {
                        "Id": 12,
                        "Name": "catalog1",
                    },
                    "Status": "Running"
                }
            ]
        }
        f_module = self.get_module_mock(params=params["inp"])
        with pytest.raises(Exception) as exc:
            self.module.get_catrepo_ids(f_module, params["inp"], ome_connection_mock_for_firmware_baseline)
        assert exc.value.args[0] == "Unable to create the firmware baseline as the catalog is in Running status."

    @pytest.mark.parametrize("params", [{"mparams": {"state": "absent", "baseline_name": "my_baseline1"}, "res": [
        {"Id": 12, "Name": "my_baseline1"}], "json_data": {
        "value": [{"Id": 12, "Name": "my_baseline1"}]}, "success": True}, {
        "mparams": {"state": "absent", "baseline_id": 12},
        "res": [{"Id": 12, "Name": "my_baseline1"}],
        "json_data": {"value": [{"Id": 11, "Name": "my_baseline2"},
                                {"Id": 12, "Name": "my_baseline1"}]}, "success": True}])
    def test_check_existing_baseline(self, mocker, params, ome_connection_mock_for_firmware_baseline, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        ome_connection_mock_for_firmware_baseline.get_all_items_with_pagination.return_value = params['json_data']
        f_module = self.get_module_mock(params=params["mparams"])
        res = self.module.check_existing_baseline(f_module, ome_connection_mock_for_firmware_baseline)
        assert res == params["res"]

    @pytest.mark.parametrize("params", [
        {"json_data": {"Name": 'd1'}, 'job_failed': False, 'job_message': BASELINE_UPDATED.format(op='created'),
         'mparams': {'catalog_name': 'c1', 'device_ids': 123, 'job_wait': True, 'job_wait_timeout': 1000}},
        {"json_data": {"Name": 'd1'}, 'job_failed': True, 'job_message': JOB_TRACK_FAIL,
         'mparams': {'catalog_name': 'c1', 'device_ids': 123, 'job_wait': True, 'job_wait_timeout': 1000}},
        {"json_data": {"Name": 'd1'}, 'job_failed': True, 'job_message': BASELINE_TRIGGERED,
         'mparams': {'catalog_name': 'c1', 'device_ids': 123, 'job_wait': False, 'schedule': 'RunLater',
                     'job_wait_timeout': 1000}}])
    def test_create_baseline(self, params, mocker, ome_connection_mock_for_firmware_baseline, ome_response_mock):
        mocker.patch(MODULE_PATH + '_get_baseline_payload', return_value={})
        mocker.patch(MODULE_PATH + 'check_existing_baseline', return_value=[{"Id": 123}])
        mocker.patch(MODULE_PATH + 'time.sleep', return_value=None)
        ome_connection_mock_for_firmware_baseline.job_tracking.return_value = \
            (params['job_failed'], params['job_message'])
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params['mparams'])
        error_message = params["job_message"]
        with pytest.raises(Exception) as err:
            self.module.create_baseline(f_module, ome_connection_mock_for_firmware_baseline)
        assert err.value.args[0] == error_message

    @pytest.mark.parametrize("params", [
        {"json_data": {"Name": 'd1', },
         'job_failed': False, 'job_message': BASELINE_UPDATED.format(op='modified'),
         'mparams': {"baseline_description": "new description", "baseline_name": "c4", "catalog_name": "baseline",
                     "device_service_tags": ["2H7HNX2", "2HB9NX2"], "downgrade_enabled": False, "is_64_bit": False,
                     "job_wait": True, "job_wait_timeout": 600, "new_baseline_name": "new name"},
         "baseline_list": [{"CatalogId": 25, "Description": "", "DowngradeEnabled": True, "Id": 40, "Is64Bit": True,
                            "Name": "c4", "RepositoryId": 15,
                            "Targets": [{"Id": 13456, "Type": {"Id": 1000, "Name": "DEVICE"}},
                                        {"Id": 13457, "Type": {"Id": 1000, "Name": "DEVICE"}}], "TaskId": 14465,
                            "TaskStatusId": 2010}],
         "get_catrepo_ids": (12, 13), "get_target_list": [{"Id": 13456, "Type": {"Id": 1000, "Name": "DEVICE"}},
                                                          {"Id": 13457, "Type": {"Id": 1000, "Name": "DEVICE"}}]
         },
        {"json_data": {"Name": 'd1'}, 'job_failed': True, 'job_message': JOB_TRACK_FAIL,
         'mparams': {'catalog_name': 'c1', 'device_ids': 123, 'job_wait': True, 'job_wait_timeout': 1000},
         "baseline_list": [{"Id": 12, "Name": "c1", "TaskStatusId": 2010, "TaskId": 12}], },
        {"json_data": {"Name": 'd1'}, 'job_failed': True, 'job_message': BASELINE_TRIGGERED,
         "baseline_list": [{"Id": 12, "Name": "c1", "TaskStatusId": 2010, "TaskId": 12}],
         'mparams': {'catalog_name': 'c1', 'device_ids': 123, 'job_wait': False, 'schedule': 'RunLater',
                     'job_wait_timeout': 1000}}])
    def test_modify_baseline(self, params, mocker, ome_connection_mock_for_firmware_baseline, ome_response_mock):
        mocker.patch(MODULE_PATH + 'time.sleep', return_value=None)
        mocker.patch(MODULE_PATH + 'get_catrepo_ids', return_value=params.get('get_catrepo_ids', (12, 13)))
        mocker.patch(MODULE_PATH + 'get_target_list', return_value=params.get('get_target_list', []))
        ome_connection_mock_for_firmware_baseline.job_tracking.return_value = \
            (params['job_failed'], params['job_message'])
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params['mparams'])
        error_message = params["job_message"]
        with pytest.raises(Exception) as err:
            self.module.modify_baseline(f_module, ome_connection_mock_for_firmware_baseline, params['baseline_list'])
        assert err.value.args[0] == error_message

    @pytest.mark.parametrize("params",
                             [{"mparams": {"state": "absent", "baseline_job_name": "my_baseline1"},
                               "baseline_list": [{"Id": 12, "Name": "my_baseline1", "TaskStatusId": 2010}],
                               "job_state_dict": {12: 2010}, "res": BASELINE_DEL_SUCCESS.format(n=1),
                               "json_data": 1, "success": True},
                              {"mparams": {"state": "absent", "baseline_job_name": "my_baseline1"},
                               "baseline_list": [{"Id": 12, "Name": "my_baseline1", "TaskStatusId": 2050, "TaskId": 12}],
                               "job_state_dict": {12: 2050},
                               "res": BASELINE_JOB_RUNNING.format(name='my_baseline1', id=12), "json_data": 1,
                               "success": True}])
    def test_delete_baseline(self, mocker, params, ome_connection_mock_for_firmware_baseline, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params["mparams"])
        error_message = params["res"]
        with pytest.raises(Exception) as err:
            self.module.delete_baseline(f_module, ome_connection_mock_for_firmware_baseline, params['baseline_list'])
        assert err.value.args[0] == error_message

    def test_get_catrepo_ids_success(self, ome_connection_mock_for_firmware_baseline,
                                     ome_response_mock):
        ome_response_mock.success = False
        f_module = self.get_module_mock()
        catrepo = self.module.get_catrepo_ids(f_module, "catalog1", ome_connection_mock_for_firmware_baseline)
        assert catrepo == (None, None)

    inp_param1 = {"device_service_tags": ["R840PT3", "R940PT3"]}
    out1 = [
        {
            "Id": 12,
            "Type": {
                "Id": 1000,
                "Name": "DEVICE"
            }
        },
        {
            "Id": 23,
            "Type": {
                "Id": 1000,
                "Name": "DEVICE"
            }
        }
    ]
    inp_param2 = {"device_service_tags": ["R840PT3"]}
    out2 = [{
        "Id": 12,
        "Type": {
            "Id": 1000,
            "Name": "DEVICE"
        }
    }]

    @pytest.mark.parametrize("params", [{"inp": inp_param1, "out": out1},
                                        {"inp": inp_param2, "out": out2}])
    def test_get_dev_ids(self, ome_connection_mock_for_firmware_baseline,
                         ome_response_mock, params):
        f_module = self.get_module_mock(params=params["inp"])
        ome_connection_mock_for_firmware_baseline.get_all_items_with_pagination.return_value = {
            "value":
                [
                    {
                        "Id": 12,
                        "Type": 1000,
                        "DeviceServiceTag": "R840PT3"
                    },
                    {
                        "Id": 23,
                        "Type": 1000,
                        "DeviceServiceTag": "R940PT3"
                    }
                ]
        }
        targets = self.module.get_dev_ids(f_module, ome_connection_mock_for_firmware_baseline,
                                          "device_service_tags", "DeviceServiceTag")
        assert targets == params["out"]

    @pytest.mark.parametrize("params", [{"inp": inp_param2, "out": out2}])
    def test_get_dev_ids_fail(self, ome_connection_mock_for_firmware_baseline,
                              ome_response_mock, params):
        f_module = self.get_module_mock(params=params["inp"])
        ome_connection_mock_for_firmware_baseline.get_all_items_with_pagination.return_value = {
            "value":
                [
                    {
                        "Id": 13,
                        "Type": 1000,
                        "DeviceServiceTag": "R940PT3"
                    }
                ]
        }
        with pytest.raises(Exception) as err:
            self.module.get_dev_ids(f_module, ome_connection_mock_for_firmware_baseline,
                                    "device_service_tags", "DeviceServiceTag")
        assert err.value.args[0] == "Unable to complete the operation because the entered target DeviceServiceTag 'R840PT3' is invalid."
    grp_param1 = {"device_group_names": ["group1", "group2"]}
    grp_out1 = [
        {
            "Id": 12,
            "Type": {
                "Id": 6000,
                "Name": "GROUP"
            }
        },
        {
            "Id": 23,
            "Type": {
                "Id": 6000,
                "Name": "GROUP"
            }
        }
    ]
    grp_param2 = {"device_group_names": ["group1"]}
    grp_out2 = [
        {
            "Id": 12,
            "Type": {
                "Id": 6000,
                "Name": "GROUP"
            }
        }
    ]

    @pytest.mark.parametrize("params", [{"inp": grp_param1, "out": grp_out1},
                                        {"inp": grp_param2, "out": grp_out2}])
    def test_get_group_ids(self, ome_connection_mock_for_firmware_baseline,
                           ome_response_mock, params):
        f_module = self.get_module_mock(params=params["inp"])
        ome_response_mock.success = True
        ome_connection_mock_for_firmware_baseline.get_all_items_with_pagination.return_value = {
            "value": [
                {
                    "Id": 12,
                    "TypeId": 6000,
                    "Name": "group1"
                },
                {
                    "Id": 23,
                    "TypeId": 6000,
                    "Name": "group2"
                }
            ]
        }
        targets = self.module.get_group_ids(f_module, ome_connection_mock_for_firmware_baseline)
        assert targets == params["out"]

    @pytest.mark.parametrize("params", [{"inp": grp_param2, "out": grp_out2}])
    def test_get_group_ids_fail(self, ome_connection_mock_for_firmware_baseline,
                                ome_response_mock, params):
        f_module = self.get_module_mock(params=params["inp"])
        ome_connection_mock_for_firmware_baseline.get_all_items_with_pagination.return_value = {
            "value": [
                {
                    "Id": 23,
                    "TypeId": 6000,
                    "Name": "group2"
                }
            ]
        }
        with pytest.raises(Exception) as err:
            self.module.get_group_ids(f_module, ome_connection_mock_for_firmware_baseline)
        assert err.value.args[0] == "Unable to complete the operation because the entered target Group Name 'group1' is invalid."

    payload_param1 = {"catalog_name": "cat1",
                      "baseline_name": "baseline1",
                      "baseline_description": "baseline_description",
                      "downgrade_enabled": True,
                      "is_64_bit": True,
                      "filter_no_reboot_required": True}
    payload_param2 = {"catalog_name": "cat1",
                      "baseline_name": "baseline1",
                      "baseline_description": None,
                      "downgrade_enabled": None,
                      "is_64_bit": None,
                      "filter_no_reboot_required": False}

    @pytest.mark.parametrize("params", [{"inp": payload_param1, "out": payload_out1},
                                        {"inp": payload_param2, "out": payload_out2}])
    def test__get_baseline_payload(self, ome_connection_mock_for_firmware_baseline, params, mocker):
        f_module = self.get_module_mock(params=params["inp"])
        mocker.patch(
            MODULE_PATH + 'get_catrepo_ids',
            return_value=(12, 23))
        mocker.patch(
            MODULE_PATH + 'get_target_list',
            return_value=[{"Id": 123, "Type": {"Id": 1000, "Name": "DEVICE"}}])
        payload = self.module._get_baseline_payload(f_module, ome_connection_mock_for_firmware_baseline)
        assert payload == params["out"]

    def test__get_baseline_payload_failure01(self, ome_default_args, ome_connection_mock_for_firmware_baseline, mocker):
        f_module = self.get_module_mock(params={"catalog_name": "cat1",
                                                "baseline_name": "baseline1"})
        mocker.patch(
            MODULE_PATH + 'get_catrepo_ids',
            return_value=(None, None))
        mocker.patch(
            MODULE_PATH + 'get_target_list',
            return_value=[{"Id": 123, "Type": {
                "Id": 1000, "Name": "DEVICE"}}])
        with pytest.raises(Exception) as exc:
            self.module._get_baseline_payload(f_module, ome_connection_mock_for_firmware_baseline)
        assert exc.value.args[0] == "No Catalog with name cat1 found"

    def test__get_baseline_payload_failure02(self, ome_default_args, ome_connection_mock_for_firmware_baseline, mocker):
        f_module = self.get_module_mock(params={"catalog_name": "cat1",
                                                "baseline_name": "baseline1"})
        mocker.patch(
            MODULE_PATH + 'get_catrepo_ids',
            return_value=(12, 23))
        mocker.patch(
            MODULE_PATH + 'get_target_list',
            return_value=None)
        with pytest.raises(Exception) as exc:
            self.module._get_baseline_payload(f_module, ome_connection_mock_for_firmware_baseline)
        assert exc.value.args[0] == NO_TARGETS_MESSAGE

    target_param1 = {"device_ids": [12, 23]}
    target_out1 = [
        {
            "Id": 12,
            "Type": {
                "Id": 1000,
                "Name": "DEVICE"
            }
        },
        {
            "Id": 23,
            "Type": {
                "Id": 1000,
                "Name": "DEVICE"
            }
        }
    ]
    target_param2 = {"x": 3}
    target_out2 = None

    @pytest.mark.parametrize("params", [{"inp": inp_param1, "out": out1},
                                        {"inp": inp_param2, "out": out2},
                                        {"inp": grp_param1, "out": grp_out1},
                                        {"inp": grp_param2, "out": grp_out2},
                                        {"inp": target_param1, "out": target_out1},
                                        {"inp": target_param2, "out": target_out2}])
    def test_get_target_list(self, ome_connection_mock_for_firmware_baseline, params, mocker):
        f_module = self.get_module_mock(params=params["inp"])
        mocker.patch(
            MODULE_PATH + 'get_dev_ids',
            return_value=params["out"])
        mocker.patch(
            MODULE_PATH + 'get_group_ids',
            return_value=params["out"])
        targets = self.module.get_target_list(f_module, ome_connection_mock_for_firmware_baseline)
        assert targets == params["out"]

    @pytest.mark.parametrize("params", [
        {"json_data": {"JobId": 1234},
         "check_existing_baseline": [],
         "mparams": {"state": "absent", "baseline_name": "b1", "device_ids": [12, 23], 'catalog_name': 'c1',
                     'job_wait': False},
         'message': NO_CHANGES_MSG, "success": True
         },
        {"json_data": {"JobId": 1234},
         "check_existing_baseline": [{"name": "b1", "Id": 123, "TaskStatusId": 2060}], "check_mode": True,
         "mparams": {"state": "absent", "baseline_id": 123, "device_ids": [12, 23], 'catalog_name': 'c1',
                     'job_wait': False},
         'message': "Changes found to be applied.", "success": True
         },
        {"json_data": {"JobId": 1234},
         "check_existing_baseline": [], "check_mode": True,
         "mparams": {"state": "present", "baseline_name": "b1", "device_ids": [12, 23], 'catalog_name': 'c1',
                     'job_wait': False},
         'message': "Changes found to be applied.", "success": True
         }
    ])
    def test_main_success(self, params, ome_connection_mock_for_firmware_baseline, ome_default_args, ome_response_mock, mocker):
        mocker.patch(MODULE_PATH + 'check_existing_baseline', return_value=params.get("check_existing_baseline"))
        mocker.patch(MODULE_PATH + '_get_baseline_payload', return_value=params.get("_get_baseline_payload"))
        ome_response_mock.success = True
        ome_response_mock.json_data = params.get("json_data")
        ome_default_args.update(params.get('mparams'))
        result = self._run_module(ome_default_args, check_mode=params.get("check_mode", False))
        assert result["msg"] == params['message']

    @pytest.mark.parametrize("params", [
        {"json_data": {"JobId": 1234},
         "check_existing_baseline": [], "check_mode": True,
         "mparams": {"state": "present", "baseline_id": 123, "device_ids": [12, 23], 'catalog_name': 'c1',
                     'job_wait': False},
         'message': INVALID_BASELINE_ID, "success": True
         },
        {"json_data": {"JobId": 1234},
         "check_existing_baseline": [{"Name": "b1", "Id": 123, "TaskStatusId": 2050, "TaskId": 2050}], "check_mode": True,
         "mparams": {"state": "present", "baseline_id": 123, "device_ids": [12, 23], 'catalog_name': 'c1',
                     'job_wait': False},
         'message': "Firmware baseline 'b1' with ID 123 is running. Please retry after job completion.", "success": True
         },
        {"json_data": {"JobId": 1234},
         "check_existing_baseline": [{"Name": "b1", "Id": 123, "TaskStatusId": 2060, "TaskId": 2050}],
         "check_mode": True, "get_catrepo_ids": (None, None),
         "mparams": {"state": "present", "baseline_id": 123, "device_ids": [12, 23], 'catalog_name': 'c1',
                     'job_wait': False},
         'message': "No Catalog with name c1 found", "success": True
         },
    ])
    def test_main_failure(self, params, ome_connection_mock_for_firmware_baseline, ome_default_args, ome_response_mock, mocker):
        mocker.patch(MODULE_PATH + 'check_existing_baseline', return_value=params.get("check_existing_baseline"))
        mocker.patch(MODULE_PATH + '_get_baseline_payload', return_value=params.get("_get_baseline_payload"))
        mocker.patch(MODULE_PATH + 'get_catrepo_ids', return_value=params.get("get_catrepo_ids"))
        ome_response_mock.success = True
        ome_response_mock.json_data = params.get("json_data")
        ome_default_args.update(params.get('mparams'))
        result = self._run_module(ome_default_args)
        assert result["msg"] == params['message']

    def test_main_failure01(self, ome_connection_mock_for_firmware_baseline, ome_default_args, ome_response_mock,
                            mocker):
        mocker.patch(
            MODULE_PATH + '_get_baseline_payload',
            return_value=payload_out1)
        ome_response_mock.success = False
        ome_response_mock.json_data = baseline_status1
        ome_default_args.update({"baseline_name": "b1", "device_ids": [12, 23]})
        result = self._run_module(ome_default_args)
        assert result["failed"] is True
        assert 'msg' in result

    def test_main_failure02(self, ome_connection_mock_for_firmware_baseline, ome_default_args, ome_response_mock,
                            mocker):
        mocker.patch(
            MODULE_PATH + '_get_baseline_payload',
            return_value=payload_out1)
        ome_response_mock.success = False
        ome_response_mock.json_data = baseline_status1
        ome_default_args.update({"baseline_name": "b1"})
        result = self._run_module(ome_default_args)
        assert result["failed"] is True
        assert 'msg' in result

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_baseline_main_exception_failure_case(self, exc_type, mocker, ome_default_args,
                                                      ome_connection_mock_for_firmware_baseline, ome_response_mock):
        ome_default_args.update({"state": "absent", "baseline_name": "t1"})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'check_existing_baseline', side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'check_existing_baseline', side_effect=exc_type("exception message"))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'check_existing_baseline',
                         side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result
