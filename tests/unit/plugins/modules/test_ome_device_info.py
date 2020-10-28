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
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible_collections.dellemc.openmanage.plugins.modules import ome_device_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants

resource_basic_inventory = {"basic_inventory": "DeviceService/Devices"}
resource_detailed_inventory = {"detailed_inventory:": {"device_id": {Constants.device_id1: None},
                                                       "device_service_tag": {
                                                           Constants.device_id2: Constants.service_tag1}}}

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestOmeDeviceInfo(FakeAnsibleModule):
    module = ome_device_info

    @pytest.fixture
    def validate_device_inputs_mock(self, mocker):
        validate_device_inputs_mock = mocker.patch(MODULE_PATH + 'ome_device_info._validate_inputs')
        validate_device_inputs_mock.return_value = None

    @pytest.fixture
    def get_device_resource_parameters_mock(self, mocker):
        response_class_mock = mocker.patch(MODULE_PATH + 'ome_device_info._get_resource_parameters',
                                           return_value=resource_basic_inventory)
        return response_class_mock

    def test_main_basic_inventory_success_case(self, ome_default_args, module_mock, validate_device_inputs_mock,
                                               ome_connection_mock,
                                               get_device_resource_parameters_mock, ome_response_mock):
        ome_response_mock.json_data = {"@odata.context": "/api/$metadata#Collection(DeviceService.Device)",
                                       "@odata.count": 1}
        increment_device_details = {"resp_obj": ome_response_mock,
                                    "report_list": [{"DeviceServiceTag": Constants.service_tag1,
                                                     "Id": Constants.device_id1}]}
        ome_connection_mock.get_all_report_details.return_value = increment_device_details
        ome_response_mock.status_code = 200
        result = self._run_module(ome_default_args)
        assert result['changed'] is False
        assert 'device_info' in result
        assert result["device_info"] == {"@odata.context": "/api/$metadata#Collection(DeviceService.Device)",
                                         "@odata.count": 1,
                                         "value": [{"DeviceServiceTag": Constants.service_tag1,
                                                    "Id": Constants.device_id1}]}

    def test_main_basic_inventory_query_param_success_case(self, mocker, ome_default_args, module_mock,
                                                           validate_device_inputs_mock, ome_connection_mock,
                                                           get_device_resource_parameters_mock, ome_response_mock):
        quer_param_mock = mocker.patch(MODULE_PATH + 'ome_device_info._get_query_parameters')
        quer_param_mock.return_value = {"filter": "Type eq '1000'"}
        ome_response_mock.json_data = {"value": [{"device_id1": "details", "device_id2": "details"}]}
        ome_response_mock.status_code = 200
        result = self._run_module(ome_default_args)
        assert result['changed'] is False
        assert 'device_info' in result
        assert result["device_info"] == {"value": [{"device_id1": "details", "device_id2": "details"}]}

    def test_main_basic_inventory_failure_case(self, ome_default_args, module_mock, validate_device_inputs_mock,
                                               ome_connection_mock,
                                               get_device_resource_parameters_mock, ome_response_mock):
        ome_response_mock.status_code = 500
        ome_response_mock.json_data = {"@odata.context": "/api/$metadata#Collection(DeviceService.Device)",
                                       "@odata.count": 0}
        ome_connection_mock.get_all_report_details.return_value = {"resp_obj": ome_response_mock, "report_list": []}
        result = self._run_module_with_fail_json(ome_default_args)
        assert result['msg'] == 'Failed to fetch the device information'

    def test_main_detailed_inventory_success_case(self, ome_default_args, module_mock, validate_device_inputs_mock,
                                                  ome_connection_mock,
                                                  get_device_resource_parameters_mock, ome_response_mock):
        ome_default_args.update(
            {"fact_subset": "detailed_inventory", "system_query_options": {"device_id": [Constants.device_id1],
                                                                           "device_service_tag": [
                                                                               Constants.service_tag1]}})
        detailed_inventory = {"detailed_inventory:": {
            "device_id": {Constants.device_id1: "DeviceService/Devices(Constants.device_id1)/InventoryDetails"},
            "device_service_tag": {Constants.service_tag1: "DeviceService/Devices(4321)/InventoryDetails"}}}
        get_device_resource_parameters_mock.return_value = detailed_inventory
        ome_response_mock.json_data = {
            "value": [{"device_id": {"1234": "details"}}, {"device_service_tag": {Constants.service_tag1: "details"}}]}
        ome_response_mock.status_code = 200
        result = self._run_module(ome_default_args)
        assert result['changed'] is False
        assert 'device_info' in result

    def test_main_detailed_inventory_http_error_case(self, ome_default_args, module_mock, validate_device_inputs_mock,
                                                     ome_connection_mock,
                                                     get_device_resource_parameters_mock, ome_response_mock):
        ome_default_args.update(
            {"fact_subset": "detailed_inventory", "system_query_options": {"device_id": [Constants.device_id1],
                                                                           "device_service_tag": [
                                                                               Constants.service_tag1]}})
        detailed_inventory = {"detailed_inventory:": {
            "device_id": {Constants.device_id1: "DeviceService/Devices(Constants.device_id1)/InventoryDetails"},
            "device_service_tag": {Constants.service_tag1: "DeviceService/Devices(4321)/InventoryDetails"}}}
        get_device_resource_parameters_mock.return_value = detailed_inventory
        ome_connection_mock.invoke_request.side_effect = HTTPError('http://testhost.com', 400, '', {}, None)
        result = self._run_module_with_fail_json(ome_default_args)
        assert 'device_info' not in result

    def test_main_HTTPError_error_case(self, ome_default_args, module_mock, validate_device_inputs_mock,
                                       ome_connection_mock,
                                       get_device_resource_parameters_mock, ome_response_mock):
        ome_connection_mock.invoke_request.side_effect = HTTPError('http://testhost.com', 400, '', {}, None)
        ome_response_mock.json_data = {"value": [{"device_id1": "details", "device_id2": "details"}]}
        ome_response_mock.status_code = 400
        result = self._run_module_with_fail_json(ome_default_args)
        assert 'device_info' not in result
        assert result['failed'] is True

    @pytest.mark.parametrize("fact_subset, mutually_exclusive_call",
                             [("basic_inventory", False), ("detailed_inventory", True)])
    def test_validate_inputs(self, fact_subset, mutually_exclusive_call, mocker):
        module_params = {"fact_subset": fact_subset}
        check_mutually_inclusive_arguments_mock = mocker.patch(MODULE_PATH +
                                                               'ome_device_info._check_mutually_inclusive_arguments')
        check_mutually_inclusive_arguments_mock.return_value = None
        self.module._validate_inputs(module_params)
        if mutually_exclusive_call:
            check_mutually_inclusive_arguments_mock.assert_called()
        else:
            check_mutually_inclusive_arguments_mock.assert_not_called()
        check_mutually_inclusive_arguments_mock.reset_mock()

    system_query_options_params = [{"system_query_options": None}, {"system_query_options": {"device_id": None}},
                                   {"system_query_options": {"device_service_tag": None}}]

    @pytest.mark.parametrize("system_query_options_params", system_query_options_params)
    def test_check_mutually_inclusive_arguments(self, system_query_options_params):
        module_params = {"fact_subset": "subsystem_health"}
        required_args = ["device_id", "device_service_tag"]
        module_params.update(system_query_options_params)
        with pytest.raises(ValueError) as ex:
            self.module._check_mutually_inclusive_arguments(module_params["fact_subset"], module_params,
                                                            ["device_id", "device_service_tag"])
        assert "One of the following {0} is required for {1}".format(required_args,
                                                                     module_params["fact_subset"]) == str(ex.value)

    params = [{"fact_subset": "basic_inventory", "system_query_options": {"device_id": [Constants.device_id1]}},
              {"fact_subset": "subsystem_health",
               "system_query_options": {"device_service_tag": [Constants.service_tag1]}},
              {"fact_subset": "detailed_inventory",
               "system_query_options": {"device_id": [Constants.device_id1], "inventory_type": "serverDeviceCards"}}]

    @pytest.mark.parametrize("module_params", params)
    def test_get_resource_parameters(self, module_params, ome_connection_mock):
        self.module._get_resource_parameters(module_params, ome_connection_mock)

    @pytest.mark.parametrize("module_params,data", [({"system_query_options": None}, None),
                                                    ({"system_query_options": {"fileter": None}}, None),
                                                    ({"system_query_options": {"filter": "abc"}}, "$filter")])
    def test_get_query_parameters(self, module_params, data):
        res = self.module._get_query_parameters(module_params)
        if data is not None:
            assert data in res
        else:
            assert res is None

    @pytest.mark.parametrize("module_params", params)
    def test_get_device_identifier_map(self, module_params, ome_connection_mock, mocker):
        get_device_id_from_service_tags_mock = mocker.patch(MODULE_PATH +
                                                            'ome_device_info._get_device_id_from_service_tags')
        get_device_id_from_service_tags_mock.return_value = None
        res = self.module._get_device_identifier_map(module_params, ome_connection_mock)
        assert isinstance(res, dict)

    def test_check_duplicate_device_id(self):
        self.module._check_duplicate_device_id([Constants.device_id1],
                                               {Constants.device_id1: Constants.service_tag1})
        assert self.module.device_fact_error_report[Constants.service_tag1] == "Duplicate report of device_id: 1234"

    @pytest.mark.parametrize("val,expected_res", [(123, True), ("abc", False)])
    def test_is_int(self, val, expected_res):
        actual_res = self.module.is_int(val)
        assert actual_res == expected_res

    def test_get_device_id_from_service_tags(self, ome_connection_mock, ome_response_mock, mocker):
        mocker.patch(MODULE_PATH + 'ome_device_info.update_device_details_with_filtering')
        ome_response_mock.json_data.update({"@odata.context": "/api/$metadata#Collection(DeviceService.Device)"})
        ome_response_mock.json_data.update({"@odata.count": 1})
        ome_connection_mock.get_all_report_details.return_value = {"resp_obj": ome_response_mock, "report_list": [
            {"DeviceServiceTag": Constants.service_tag1,
             "Id": Constants.device_id1}]}
        self.module._get_device_id_from_service_tags([Constants.service_tag1, "INVALID"], ome_connection_mock)

    def test_get_device_id_from_service_tags_error_case(self, ome_connection_mock, ome_response_mock):
        ome_connection_mock.get_all_report_details.side_effect = HTTPError('http://testhost.com', 400, '', {}, None)
        with pytest.raises(HTTPError) as ex:
            self.module._get_device_id_from_service_tags(["INVALID"], ome_connection_mock)

    def test_update_device_details_with_filtering_success_case_01(self, ome_connection_mock, ome_response_mock):
        non_available_tags = [Constants.service_tag2]
        service_tag_dict = {Constants.device_id1: Constants.service_tag1}
        ome_response_mock.json_data = {
            "value": [{"DeviceServiceTag": Constants.service_tag2, "Id": Constants.device_id2}]}
        self.module.update_device_details_with_filtering(non_available_tags, service_tag_dict, ome_connection_mock)
        assert service_tag_dict[Constants.device_id1] == Constants.service_tag1
        assert service_tag_dict[Constants.device_id2] == Constants.service_tag2
        assert len(non_available_tags) == 0

    def test_update_device_details_with_filtering_success_case_02(self, ome_connection_mock, ome_response_mock):
        non_available_tags = ["MX700"]
        service_tag_dict = {Constants.device_id1: Constants.service_tag1}
        ome_response_mock.json_data = {"value": [{"DeviceServiceTag": "MX7000", "Id": Constants.device_id2}]}
        self.module.update_device_details_with_filtering(non_available_tags, service_tag_dict, ome_connection_mock)
        assert service_tag_dict[Constants.device_id1] == Constants.service_tag1
        assert Constants.device_id2 not in service_tag_dict
        assert len(non_available_tags) == 1

    def test_update_device_details_with_filtering_failure_case_01(self, ome_connection_mock, ome_response_mock):
        error_msg = '400: Bad Request'
        service_tag_dict = {}
        non_available_tags = [Constants.service_tag2]
        ome_connection_mock.invoke_request.side_effect = HTTPError('http://testhost.com', 400, error_msg, {}, None)
        with pytest.raises(HTTPError, match=error_msg) as ex:
            self.module.update_device_details_with_filtering(non_available_tags, service_tag_dict, ome_connection_mock)

    def test_main_detailed_inventory_device_fact_error_report_case_01(self, ome_default_args, module_mock,
                                                                      validate_device_inputs_mock, ome_connection_mock,
                                                                      get_device_resource_parameters_mock,
                                                                      ome_response_mock):
        ome_default_args.update(
            {"fact_subset": "detailed_inventory", "system_query_options": {"device_id": [Constants.device_id1],
                                                                           "device_service_tag": [
                                                                               Constants.service_tag1]}})
        detailed_inventory = {
            "detailed_inventory:": {
                "device_id": {
                    Constants.device_id1: "DeviceService/Devices(Constants.device_id1)/InventoryDetails"
                },
                "device_service_tag": {
                    Constants.service_tag1: "DeviceService/Devices(4321)/InventoryDetails"
                }
            }
        }
        get_device_resource_parameters_mock.return_value = detailed_inventory
        ome_response_mock.json_data = {"value": [{"device_id": {Constants.device_id1: "details"}},
                                                 {"device_service_tag": {Constants.service_tag1: "details"}}]}
        ome_response_mock.status_code = 200
        self.module.device_fact_error_report = {
            Constants.service_tag1: "Duplicate report of device_id: {0}".format(Constants.device_id1)}
        result = self._run_module(ome_default_args)
        assert result['changed'] is False
        assert 'device_info' in result

    def test_main_detailed_inventory_device_fact_error_report_case_02(self, ome_default_args, module_mock,
                                                                      validate_device_inputs_mock,
                                                                      ome_connection_mock,
                                                                      get_device_resource_parameters_mock,
                                                                      ome_response_mock):
        ome_default_args.update(
            {"fact_subset": "detailed_inventory", "system_query_options": {"device_id": [Constants.device_id1],
                                                                           "device_service_tag": [
                                                                               Constants.service_tag1]}})
        detailed_inventory = {
            "device_service_tag": {
                Constants.service_tag1: "DeviceService/Devices(4321)/InventoryDetails"
            }
        }
        get_device_resource_parameters_mock.return_value = detailed_inventory
        ome_response_mock.json_data = {"value": [{"device_id": {Constants.device_id1: "details"}},
                                                 {"device_service_tag": {Constants.service_tag1: "details"}}]}
        ome_response_mock.status_code = 200
        self.module.device_fact_error_report = {
            Constants.service_tag1: "Duplicate report of device_id: {0}".format(Constants.device_id1)}
        result = self._run_module(ome_default_args)
        assert result['changed'] is False
        assert 'device_info' in result
