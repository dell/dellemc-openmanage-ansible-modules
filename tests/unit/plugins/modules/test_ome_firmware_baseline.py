# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.3
# Copyright (C) 2019-2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible_collections.dellemc.openmanage.plugins.modules import ome_firmware_baseline
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'

payload_out1 = {
    "Name": "baseline1",
    "Description": "baseline_description",
    "CatalogId": 12,
    "RepositoryId": 23,
    "DowngradeEnabled": True,
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
    "RepositoryId": 23,
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


class TestOmeFirmwareCatalog(FakeAnsibleModule):
    module = ome_firmware_baseline

    @pytest.fixture
    def mock__get_catalog_payload(self, mocker):
        mock_payload = mocker.patch(
            MODULE_PATH + 'ome_firmware_baseline._get_baseline_payload',
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
        ome_response_mock.success = True
        ome_response_mock.json_data = {
            "value": [
                {
                    "Id": 22,
                    "Repository": {
                        "Id": 12,
                        "Name": "catalog1",
                    }
                },
                {
                    "Id": 23,
                    "Repository": {
                        "Id": 12,
                        "Name": "catalog2",
                    }
                }
            ]
        }
        catrepo = self.module.get_catrepo_ids(params["inp"], ome_connection_mock_for_firmware_baseline)
        assert catrepo == params["out"]

    def test_get_catrepo_ids_success(self, ome_connection_mock_for_firmware_baseline,
                                     ome_response_mock):
        ome_response_mock.success = False
        catrepo = self.module.get_catrepo_ids("catalog1", ome_connection_mock_for_firmware_baseline)
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
        ome_response_mock.success = True
        ome_response_mock.json_data = {
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

    grp_param1 = {"device_group_names": ["group1", "group2"]}
    grp_out1 = [
        {
            "Id": 12,
            "Type": {
                "Id": 2000,
                "Name": "GROUP"
            }
        },
        {
            "Id": 23,
            "Type": {
                "Id": 2000,
                "Name": "GROUP"
            }
        }
    ]
    grp_param2 = {"device_group_names": ["group1"]}
    grp_out2 = [
        {
            "Id": 12,
            "Type": {
                "Id": 2000,
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
        ome_response_mock.json_data = {
            "value": [
                {
                    "Id": 12,
                    "TypeId": 2000,
                    "Name": "group1"
                },
                {
                    "Id": 23,
                    "TypeId": 2000,
                    "Name": "group2"
                }
            ]
        }
        targets = self.module.get_group_ids(f_module, ome_connection_mock_for_firmware_baseline)
        assert targets == params["out"]

    payload_param1 = {"catalog_name": "cat1",
                      "baseline_name": "baseline1",
                      "baseline_description": "baseline_description",
                      "downgrade_enabled": True,
                      "is_64_bit": True}
    payload_param2 = {"catalog_name": "cat1",
                      "baseline_name": "baseline1",
                      "baseline_description": None,
                      "downgrade_enabled": None,
                      "is_64_bit": None}

    @pytest.mark.parametrize("params", [{"inp": payload_param1, "out": payload_out1},
                                        {"inp": payload_param2, "out": payload_out2}])
    def test__get_baseline_payload(self, ome_connection_mock_for_firmware_baseline, params, mocker):
        f_module = self.get_module_mock(params=params["inp"])
        mocker.patch(
            MODULE_PATH + 'ome_firmware_baseline.get_catrepo_ids',
            return_value=(12, 23))
        mocker.patch(
            MODULE_PATH + 'ome_firmware_baseline.get_target_list',
            return_value=[{"Id": 123, "Type": {
                "Id": 1000, "Name": "DEVICE"}}])
        payload = self.module._get_baseline_payload(f_module, ome_connection_mock_for_firmware_baseline)
        assert payload == params["out"]

    def test__get_baseline_payload_failure01(self, ome_default_args, ome_connection_mock_for_firmware_baseline, mocker):
        f_module = self.get_module_mock(params={"catalog_name": "cat1",
                                                "baseline_name": "baseline1"})
        mocker.patch(
            MODULE_PATH + 'ome_firmware_baseline.get_catrepo_ids',
            return_value=(None, None))
        mocker.patch(
            MODULE_PATH + 'ome_firmware_baseline.get_target_list',
            return_value=[{"Id": 123, "Type": {
                "Id": 1000, "Name": "DEVICE"}}])
        with pytest.raises(Exception) as exc:
            self.module._get_baseline_payload(f_module, ome_connection_mock_for_firmware_baseline)
        assert exc.value.args[0] == "No Catalog with name cat1 found"

    def test__get_baseline_payload_failure02(self, ome_default_args, ome_connection_mock_for_firmware_baseline, mocker):
        f_module = self.get_module_mock(params={"catalog_name": "cat1",
                                                "baseline_name": "baseline1"})
        mocker.patch(
            MODULE_PATH + 'ome_firmware_baseline.get_catrepo_ids',
            return_value=(12, 23))
        mocker.patch(
            MODULE_PATH + 'ome_firmware_baseline.get_target_list',
            return_value=None)
        with pytest.raises(Exception) as exc:
            self.module._get_baseline_payload(f_module, ome_connection_mock_for_firmware_baseline)
        assert exc.value.args[0] == "No Targets specified"

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
            MODULE_PATH + 'ome_firmware_baseline.get_dev_ids',
            return_value=params["out"])
        mocker.patch(
            MODULE_PATH + 'ome_firmware_baseline.get_group_ids',
            return_value=params["out"])
        targets = self.module.get_target_list(f_module, ome_connection_mock_for_firmware_baseline)
        assert targets == params["out"]

    def test_main_success(self, ome_connection_mock_for_firmware_baseline, ome_default_args, ome_response_mock, mocker):
        mocker.patch(
            MODULE_PATH + 'ome_firmware_baseline._get_baseline_payload',
            return_value=payload_out1)
        ome_response_mock.success = True
        ome_response_mock.json_data = baseline_status1
        ome_default_args.update({"baseline_name": "b1", "device_ids": [12, 23]})
        result = self._run_module(ome_default_args)
        assert result["changed"] is True
        assert 'baseline_status' in result

    def test_main_failure01(self, ome_connection_mock_for_firmware_baseline, ome_default_args, ome_response_mock,
                            mocker):
        mocker.patch(
            MODULE_PATH + 'ome_firmware_baseline._get_baseline_payload',
            return_value=payload_out1)
        ome_response_mock.success = False
        ome_response_mock.json_data = baseline_status1
        ome_default_args.update({"baseline_name": "b1", "device_ids": [12, 23]})
        result = self._run_module_with_fail_json(ome_default_args)
        assert result["failed"] is True
        assert 'msg' in result

    def test_main_failure02(self, ome_connection_mock_for_firmware_baseline, ome_default_args, ome_response_mock,
                            mocker):
        mocker.patch(
            MODULE_PATH + 'ome_firmware_baseline._get_baseline_payload',
            return_value=payload_out1)
        ome_response_mock.success = False
        ome_response_mock.json_data = baseline_status1
        ome_default_args.update({"baseline_name": "b1"})
        result = self._run_module_with_fail_json(ome_default_args)
        assert result["failed"] is True
        assert 'msg' in result
