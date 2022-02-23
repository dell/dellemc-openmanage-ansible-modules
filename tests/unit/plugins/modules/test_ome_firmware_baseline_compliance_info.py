# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.1.0
# Copyright (C) 2019-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text
from ansible_collections.dellemc.openmanage.plugins.modules import ome_firmware_baseline_compliance_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, \
    AnsibleFailJSonException, Constants


@pytest.fixture
def ome_connection_mock_for_firmware_baseline_compliance_info(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(
        'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeFirmwareCatalog(FakeAnsibleModule):
    module = ome_firmware_baseline_compliance_info

    def test__get_device_id_from_service_tags_for_baseline_success_case(self, ome_response_mock,
                                                                        ome_connection_mock_for_firmware_baseline_compliance_info):
        ome_connection_mock_for_firmware_baseline_compliance_info.get_all_report_details.return_value = {
            "report_list": [{"DeviceServiceTag": Constants.service_tag1, "Id": Constants.device_id1}]}
        f_module = self.get_module_mock()
        data = self.module._get_device_id_from_service_tags([Constants.service_tag1],
                                                            ome_connection_mock_for_firmware_baseline_compliance_info,
                                                            f_module)
        assert data == {Constants.device_id1: Constants.service_tag1}

    def test__get_device_id_from_service_tags_empty_case(self, ome_response_mock,
                                                         ome_connection_mock_for_firmware_baseline_compliance_info):
        ome_connection_mock_for_firmware_baseline_compliance_info.get_all_report_details.return_value = {
            "report_list": []}
        f_module = self.get_module_mock()
        with pytest.raises(Exception) as exc:
            data = self.module._get_device_id_from_service_tags([Constants.service_tag1],
                                                                ome_connection_mock_for_firmware_baseline_compliance_info,
                                                                f_module)
        assert exc.value.args[0] == "Unable to fetch the device information."

    def test_get_device_id_from_service_tags_for_baseline_error_case(self,
                                                                     ome_connection_mock_for_firmware_baseline_compliance_info,
                                                                     ome_response_mock):
        ome_connection_mock_for_firmware_baseline_compliance_info.get_all_report_details.side_effect = HTTPError(
            'http://testhost.com', 400, '', {}, None)
        f_module = self.get_module_mock()
        with pytest.raises(HTTPError) as ex:
            self.module._get_device_id_from_service_tags(["INVALID"],
                                                         ome_connection_mock_for_firmware_baseline_compliance_info,
                                                         f_module)

    def test_get_device_id_from_service_tags_for_baseline_value_error_case(self,
                                                                           ome_connection_mock_for_firmware_baseline_compliance_info,
                                                                           ome_response_mock):
        ome_connection_mock_for_firmware_baseline_compliance_info.get_all_report_details.return_value = {
            "report_list": []}
        f_module = self.get_module_mock()
        with pytest.raises(Exception) as exc:
            self.module._get_device_id_from_service_tags(["#$%^&"],
                                                         ome_connection_mock_for_firmware_baseline_compliance_info,
                                                         f_module)
        assert exc.value.args[0] == "Unable to fetch the device information."

    def test_get_device_ids_from_group_ids_success_case(self, ome_response_mock,
                                                        ome_connection_mock_for_firmware_baseline_compliance_info):
        ome_connection_mock_for_firmware_baseline_compliance_info.get_all_items_with_pagination.return_value = {
            "value": [{"DeviceServiceTag": Constants.service_tag1, "Id": Constants.device_id1}]}
        f_module = self.get_module_mock()
        device_ids = self.module.get_device_ids_from_group_ids(f_module, ["123", "345"],
                                                               ome_connection_mock_for_firmware_baseline_compliance_info)
        assert device_ids == [Constants.device_id1, Constants.device_id1]

    def test_get_device_ids_from_group_ids_empty_case(self, ome_response_mock,
                                                      ome_connection_mock_for_firmware_baseline_compliance_info):
        ome_connection_mock_for_firmware_baseline_compliance_info.get_all_report_details.return_value = {"report_list": []}
        f_module = self.get_module_mock()
        with pytest.raises(Exception) as exc:
            device_ids = self.module.get_device_ids_from_group_ids(f_module, ["123", "345"],
                                                                   ome_connection_mock_for_firmware_baseline_compliance_info)
        assert exc.value.args[0] == "Unable to fetch the device ids from specified device_group_names."

    def test_get_device_ids_from_group_ids_error_case(self, ome_connection_mock_for_firmware_baseline_compliance_info,
                                                      ome_response_mock):
        ome_connection_mock_for_firmware_baseline_compliance_info.get_all_items_with_pagination.side_effect = HTTPError(
            'http://testhost.com', 400, '', {}, None)
        f_module = self.get_module_mock()
        with pytest.raises(HTTPError) as ex:
            device_ids = self.module.get_device_ids_from_group_ids(f_module, ["123456"],
                                                                   ome_connection_mock_for_firmware_baseline_compliance_info)

    def test_get_device_ids_from_group_ids_value_error_case(self,
                                                            ome_connection_mock_for_firmware_baseline_compliance_info,
                                                            ome_response_mock):
        ome_connection_mock_for_firmware_baseline_compliance_info.get_all_items_with_pagination.return_value = {
            "value": []}
        f_module = self.get_module_mock()
        with pytest.raises(Exception) as exc:
            self.module.get_device_ids_from_group_ids(f_module, ["123456"],
                                                      ome_connection_mock_for_firmware_baseline_compliance_info)
        assert exc.value.args[0] == "Unable to fetch the device ids from specified device_group_names."

    def test_get_device_ids_from_group_names_success_case(self, mocker, ome_response_mock,
                                                          ome_connection_mock_for_firmware_baseline_compliance_info):
        ome_connection_mock_for_firmware_baseline_compliance_info.get_all_report_details.return_value = {
            "report_list": [{"Name": "group1", "Id": 123}]}
        mocker.patch(
            'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info.get_device_ids_from_group_ids',
            return_value=[Constants.device_id1, Constants.device_id2])
        f_module = self.get_module_mock(params={"device_group_names": ["group1", "group2"]})
        device_ids = self.module.get_device_ids_from_group_names(f_module,
                                                                 ome_connection_mock_for_firmware_baseline_compliance_info)
        assert device_ids == [Constants.device_id1, Constants.device_id2]

    def test_get_device_ids_from_group_names_empty_case(self, mocker, ome_response_mock,
                                                        ome_connection_mock_for_firmware_baseline_compliance_info):
        ome_connection_mock_for_firmware_baseline_compliance_info.get_all_report_details.return_value = {
            "report_list": []}
        mocker.patch(
            'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info.get_device_ids_from_group_ids',
            return_value=[])
        f_module = self.get_module_mock(params={"device_group_names": ["abc", "xyz"]})
        with pytest.raises(Exception) as ex:
            device_ids = self.module.get_device_ids_from_group_names(f_module,
                                                                     ome_connection_mock_for_firmware_baseline_compliance_info)
        assert ex.value.args[0] == "Unable to fetch the specified device_group_names."

    def test_get_device_ids_from_group_names_error_case(self, ome_connection_mock_for_firmware_baseline_compliance_info,
                                                        ome_response_mock):
        ome_connection_mock_for_firmware_baseline_compliance_info.get_all_report_details.side_effect = HTTPError(
            'http://testhost.com', 400, '', {}, None)
        f_module = self.get_module_mock(params={"device_group_names": ["abc", "xyz"]})
        with pytest.raises(HTTPError) as ex:
            self.module.get_device_ids_from_group_names(f_module,
                                                        ome_connection_mock_for_firmware_baseline_compliance_info)

    def test_get_device_ids_from_group_names_value_error_case(self,
                                                              ome_connection_mock_for_firmware_baseline_compliance_info,
                                                              ome_response_mock):
        ome_connection_mock_for_firmware_baseline_compliance_info.get_all_report_details.return_value = {
            "report_list": []}
        f_module = self.get_module_mock(params={"device_group_names": ["abc", "xyz"]})
        with pytest.raises(Exception) as exc:
            self.module.get_device_ids_from_group_names(f_module,
                                                        ome_connection_mock_for_firmware_baseline_compliance_info)
        assert exc.value.args[0] == "Unable to fetch the specified device_group_names."

    def test_get_identifiers_with_device_ids(self, ome_connection_mock_for_firmware_baseline_compliance_info,
                                             module_mock, default_ome_args):
        """when device_ids given """
        f_module = self.get_module_mock(params={"device_ids": [Constants.device_id1, Constants.device_id2]})
        identifiers, identifiers_type = self.module.get_identifiers(
            ome_connection_mock_for_firmware_baseline_compliance_info, f_module)
        assert identifiers == [Constants.device_id1, Constants.device_id2]
        assert identifiers_type == "device_ids"

    def test_get_identifiers_with_service_tags(self, mocker, ome_connection_mock_for_firmware_baseline_compliance_info,
                                               module_mock, default_ome_args):
        """when service tags given """
        f_module = self.get_module_mock(params={"device_service_tags": [Constants.service_tag1]})
        mocker.patch(
            'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info._get_device_id_from_service_tags',
            return_value={Constants.device_id1: Constants.service_tag1})
        identifiers, identifiers_type = self.module.get_identifiers(
            ome_connection_mock_for_firmware_baseline_compliance_info, f_module)
        assert identifiers == [Constants.device_id1]
        assert identifiers_type == "device_service_tags"

    def test_get_identifiers_with_group_names(self, mocker, ome_connection_mock_for_firmware_baseline_compliance_info,
                                              module_mock, default_ome_args):
        """when service tags given """
        f_module = self.get_module_mock(params={"device_group_names": [Constants.service_tag1]})
        mocker.patch(
            'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info.get_device_ids_from_group_names',
            return_value=[123, 456])
        identifiers, identifiers_type = self.module.get_identifiers(
            ome_connection_mock_for_firmware_baseline_compliance_info, f_module)
        assert identifiers == [123, 456]
        identifiers_type == "device_group_names"

    def test_get_identifiers_with_service_tags_empty_case(self, mocker,
                                                          ome_connection_mock_for_firmware_baseline_compliance_info,
                                                          module_mock, default_ome_args):
        """when service tags given """
        f_module = self.get_module_mock(params={"device_service_tags": [Constants.service_tag1]})
        mocker.patch(
            'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info._get_device_id_from_service_tags',
            return_value={})
        identifiers, identifiers_type = self.module.get_identifiers(
            ome_connection_mock_for_firmware_baseline_compliance_info, f_module)
        assert identifiers == []
        assert identifiers_type == "device_service_tags"

    def test_get_baseline_id_from_name_success_case(self, default_ome_args,
                                                    ome_connection_mock_for_firmware_baseline_compliance_info,
                                                    module_mock, ome_response_mock):
        ome_connection_mock_for_firmware_baseline_compliance_info.get_all_items_with_pagination.return_value = {
            "value": [{"Name": "baseline_name1", "Id": 111}, {"Name": "baseline_name2",
                                                              "Id": 222}]}
        f_module = self.get_module_mock(params={"baseline_name": "baseline_name1"})
        baseline_id = self.module.get_baseline_id_from_name(ome_connection_mock_for_firmware_baseline_compliance_info,
                                                            f_module)
        assert baseline_id == 111

    def test_get_baseline_id_from_name_when_name_not_exists(self, default_ome_args,
                                                            ome_connection_mock_for_firmware_baseline_compliance_info,
                                                            ome_response_mock):
        ome_connection_mock_for_firmware_baseline_compliance_info.get_all_items_with_pagination.return_value = {
            "value": [{"Name": "baseline_name1", "Id": 111}]}
        f_module = self.get_module_mock(params={"baseline_name": "not_exits"})
        with pytest.raises(AnsibleFailJSonException) as exc:
            self.module.get_baseline_id_from_name(ome_connection_mock_for_firmware_baseline_compliance_info, f_module)
        assert exc.value.args[0] == "Specified baseline_name does not exist in the system."

    def test_get_baseline_id_from_name_when_baseline_is_empty(self, default_ome_args,
                                                              ome_connection_mock_for_firmware_baseline_compliance_info,
                                                              ome_response_mock):
        ome_connection_mock_for_firmware_baseline_compliance_info.get_all_items_with_pagination.return_value = {
            "value": []}
        f_module = self.get_module_mock(params={"baseline_name": "baseline_name1"})
        with pytest.raises(AnsibleFailJSonException) as exc:
            self.module.get_baseline_id_from_name(ome_connection_mock_for_firmware_baseline_compliance_info, f_module)
        assert exc.value.args[0] == "No baseline exists in the system."

    def test_get_baseline_id_from_name_when_baselinename_is_none(self, default_ome_args,
                                                                 ome_connection_mock_for_firmware_baseline_compliance_info,
                                                                 ome_response_mock):
        ome_connection_mock_for_firmware_baseline_compliance_info.get_all_items_with_pagination.return_value = {
            "value": []}
        f_module = self.get_module_mock(params={"baseline_notexist": "data"})
        with pytest.raises(AnsibleFailJSonException) as exc:
            self.module.get_baseline_id_from_name(ome_connection_mock_for_firmware_baseline_compliance_info, f_module)
        assert exc.value.args[0] == "baseline_name is a mandatory option."

    def test_get_baseline_id_from_name_with_http_error_handlin_case(self,
                                                                    ome_connection_mock_for_firmware_baseline_compliance_info,
                                                                    ome_response_mock):
        ome_connection_mock_for_firmware_baseline_compliance_info.get_all_items_with_pagination.side_effect = HTTPError(
            'http://testhost.com', 400, '', {}, None)
        f_module = self.get_module_mock(params={"baseline_name": "baseline_name1"})
        with pytest.raises(HTTPError) as ex:
            self.module.get_baseline_id_from_name(ome_connection_mock_for_firmware_baseline_compliance_info, f_module)

    @pytest.mark.parametrize("exc_type",
                             [URLError, SSLValidationError, ConnectionError, TypeError, ValueError, HTTPError])
    def test_get_baseline_id_from_name_failure_case_01(self, exc_type,
                                                       ome_connection_mock_for_firmware_baseline_compliance_info,
                                                       ome_response_mock):
        if exc_type not in [HTTPError, SSLValidationError]:
            ome_connection_mock_for_firmware_baseline_compliance_info.get_all_items_with_pagination.side_effect = exc_type(
                'test')
        else:
            ome_connection_mock_for_firmware_baseline_compliance_info.get_all_items_with_pagination.side_effect = exc_type(
                'http://testhost.com', 400, '', {}, None)
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        f_module = self.get_module_mock(params={"baseline_name": "baseline_name1"})
        with pytest.raises(exc_type) as ex:
            self.module.get_baseline_id_from_name(ome_connection_mock_for_firmware_baseline_compliance_info, f_module)

    def test_get_baselines_report_by_device_ids_success_case(self, mocker,
                                                             ome_connection_mock_for_firmware_baseline_compliance_info,
                                                             ome_response_mock):
        mocker.patch(
            'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info.get_identifiers',
            return_value=([Constants.device_id1], "device_ids"))
        ome_response_mock.json_data = {"value": []}
        ome_response_mock.success = True
        f_module = self.get_module_mock()
        self.module.get_baselines_report_by_device_ids(ome_connection_mock_for_firmware_baseline_compliance_info,
                                                       f_module)

    def test_get_baselines_report_by_device_service_tag_not_exits_case(self, mocker,
                                                                       ome_connection_mock_for_firmware_baseline_compliance_info,
                                                                       ome_response_mock):
        mocker.patch(
            'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info.get_identifiers',
            return_value=([], "device_service_tags"))
        ome_response_mock.json_data = {"value": []}
        ome_response_mock.success = True
        f_module = self.get_module_mock()
        with pytest.raises(AnsibleFailJSonException) as exc:
            self.module.get_baselines_report_by_device_ids(ome_connection_mock_for_firmware_baseline_compliance_info,
                                                           f_module)
        assert exc.value.args[0] == "Device details not available as the service tag(s) provided are invalid."

    def test_get_baselines_report_by_group_names_not_exits_case(self, mocker,
                                                                ome_connection_mock_for_firmware_baseline_compliance_info,
                                                                ome_response_mock):
        mocker.patch(
            'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info.get_identifiers',
            return_value=([], "device_group_names"))
        ome_response_mock.json_data = {"value": []}
        ome_response_mock.success = True
        f_module = self.get_module_mock()
        with pytest.raises(AnsibleFailJSonException) as exc:
            self.module.get_baselines_report_by_device_ids(ome_connection_mock_for_firmware_baseline_compliance_info,
                                                           f_module)
        assert exc.value.args[0] == "Device details not available as the group name(s) provided are invalid."

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def _test_get_baselines_report_by_device_ids_exception_handling(self, mocker, exc_type,
                                                                    ome_connection_mock_for_firmware_baseline_compliance_info,
                                                                    ome_response_mock):
        """when invalid value for expose_durationis given """
        err_dict = {"file": {
            "error": {
                "code": "Base.1.0.GeneralError",
                "message": "A general error has occurred. See ExtendedInfo for more information.",
                "@Message.ExtendedInfo": [
                    {
                        "MessageId": "CUPD3090",
                        "RelatedProperties": [],
                        "Message": "Unable to retrieve baseline list either because the device "
                                   "ID(s) entered are invalid, the ID(s) provided are not "
                                   "associated with a baseline or a group is used as a target for "
                                   "a baseline.",
                        "MessageArgs": [],
                        "Severity": "Critical",
                        "Resolution": "Make sure the entered device ID(s) are valid and retry the operation."
                    }
                ]
            }
        }
        }
        mocker.patch(
            'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info.get_identifiers',
            return_value=([], "device_ids"))
        if exc_type not in [HTTPError, SSLValidationError]:
            ome_connection_mock_for_firmware_baseline_compliance_info.invoke_request.side_effect = exc_type('test')
        else:
            ome_connection_mock_for_firmware_baseline_compliance_info.invoke_request.side_effect = exc_type(
                'http://testhost.com', 400, '', err_dict, None)
        f_module = self.get_module_mock()
        with pytest.raises(exc_type):
            self.module.get_baselines_report_by_device_ids(
                ome_connection_mock_for_firmware_baseline_compliance_info,
                f_module)

    def test_get_baseline_compliance_reports_success_case_for_baseline_device(self, mocker, ome_response_mock,
                                                                              ome_connection_mock_for_firmware_baseline_compliance_info):
        mocker.patch(
            'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info.get_baseline_id_from_name',
            return_value=123)
        f_module = self.get_module_mock(params={"baseline_name": "baseline1"})
        ome_connection_mock_for_firmware_baseline_compliance_info.get_all_items_with_pagination.return_value = {
            "value": [{"baseline_device_report1": "data"}]}
        data = self.module.get_baseline_compliance_reports(ome_connection_mock_for_firmware_baseline_compliance_info,
                                                           f_module)
        assert data == [{"baseline_device_report1": "data"}]

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_get_baseline_compliance_reports_exception_handling_case(self, exc_type, mocker, ome_response_mock,
                                                                     ome_connection_mock_for_firmware_baseline_compliance_info):
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(
                'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info.get_baseline_id_from_name',
                side_effect=exc_type('exception message'))
        else:
            mocker.patch(
                'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info.get_baseline_id_from_name',
                side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                     {"accept-type": "application/json"}, StringIO(json_str)))
        f_module = self.get_module_mock(params={"baseline_name": "baseline1"})
        with pytest.raises(exc_type):
            self.module.get_baseline_compliance_reports(ome_connection_mock_for_firmware_baseline_compliance_info,
                                                        f_module)

    param_list1 = [{"baseline_name": ""},
                   {"baseline_name": None},
                   {"device_ids": []},
                   {"device_ids": None},
                   {"device_ids": [], "baseline_name": ""},
                   {"device_service_tags": []},
                   {"device_service_tags": [], "baseline_name": ""},
                   {"device_service_tags": None},
                   {"device_group_names": [], "baseline_name": ""},
                   {"device_group_names": []},
                   {"device_group_names": None},
                   {"device_ids": [], "device_service_tags": []},
                   {"device_ids": None, "device_service_tags": None},
                   {"device_ids": [], "device_service_tags": [], "device_group_names": []},
                   {"device_ids": None, "device_service_tags": None, "device_group_names": None},
                   {"device_ids": None, "device_service_tags": [], "device_group_names": None},
                   {"device_ids": [], "device_service_tags": [], "device_group_names": [], "baseline_name": ""},

                   ]

    @pytest.mark.parametrize("param", param_list1)
    def test_validate_input_error_handling_case(self, param):
        f_module = self.get_module_mock(params=param)
        with pytest.raises(Exception) as exc:
            self.module.validate_inputs(f_module)
        assert exc.value.args[0] == "one of the following is required: device_ids, " \
                                    "device_service_tags, device_group_names, baseline_name " \
                                    "to generate device based compliance report."

    params_list2 = [{
        "device_ids": [Constants.device_id1],
        "device_service_tags": [Constants.service_tag1]},
        {"device_ids": [Constants.device_id1]},
        {"device_group_names": ["group1"]},
        {"device_service_tags": [Constants.service_tag1]},
        {"baseline_name": "baseline1", "device_ids": [Constants.device_id1]},
        {"baseline_name": "baseline1", "device_group_names": ["group1"]}
    ]

    @pytest.mark.parametrize("param", params_list2)
    def test_validate_input_params_without_error_handling_case(self, param):
        f_module = self.get_module_mock(params=param)
        self.module.validate_inputs(f_module)

    def test_baseline_complaince_main_success_case_01(self, mocker, ome_default_args, module_mock,
                                                      ome_connection_mock_for_firmware_baseline_compliance_info):
        mocker.patch(
            'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info.validate_inputs')
        mocker.patch(
            'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info.get_baselines_report_by_device_ids',
            return_value=[{"device": "device_report"}])
        ome_default_args.update({"device_ids": [Constants.device_id1]})
        result = self._run_module(ome_default_args)
        assert result["changed"] is False
        assert 'baseline_compliance_info' in result
        assert 'msg' not in result

    def test_baseline_complaince_main_success_case_02(self, mocker, ome_default_args, module_mock,
                                                      ome_connection_mock_for_firmware_baseline_compliance_info):
        mocker.patch(
            'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info.validate_inputs')
        mocker.patch(
            'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info.get_baseline_compliance_reports',
            return_value=[{"baseline_device": "baseline_device_report"}])
        ome_default_args.update({"baseline_name": "baseline_name"})
        result = self._run_module(ome_default_args)
        assert result["changed"] is False
        assert 'baseline_compliance_info' in result
        assert 'msg' not in result

    def test_baseline_complaince_main_failure_case_01(self, ome_default_args, module_mock):
        """required parameter is not passed along with specified report_type"""
        # ome_default_args.update({})
        result = self._run_module_with_fail_json(ome_default_args)
        assert 'baseline_compliance_info' not in result
        assert 'msg' in result
        assert result['msg'] == "one of the following is required: device_ids, " \
                                "device_service_tags, device_group_names, baseline_name"
        assert result['failed'] is True

    param_list4 = [
        {"device_ids": [Constants.device_id1], "device_service_tags": [Constants.service_tag1]},
        {"device_service_tags": [Constants.device_id1], "device_group_names": ["group_name1"]},
        {"device_ids": [Constants.device_id1], "device_group_names": ["group_name1"]},
        {"device_ids": [Constants.device_id1], "device_service_tags": ["group_name1"]},
        {"device_ids": [Constants.device_id1], "device_service_tags": [Constants.service_tag1],
         "device_group_names": ["group_name1"]},
        {"device_ids": [Constants.device_id1], "device_service_tags": [Constants.service_tag1],
         "device_group_names": ["group_name1"], "baseline_name": "baseline1"
         },
        {"device_ids": [Constants.device_id1], "baseline_name": "baseline1"},
        {"device_service_tags": [Constants.service_tag1], "baseline_name": "baseline1"},
        {"device_group_names": ["group_name1"], "baseline_name": "baseline1"},
        {"device_ids": [], "device_service_tags": [],
         "device_group_names": [], "baseline_name": ""
         },
    ]

    @pytest.mark.parametrize("param", param_list4)
    def test_baseline_complaince_main_failure_case_02(self, param, ome_default_args, module_mock):
        """required parameter is not passed along with specified report_type"""
        ome_default_args.update(param)
        result = self._run_module_with_fail_json(ome_default_args)
        assert 'baseline_compliance_info' not in result
        assert 'msg' in result
        assert result["msg"] == "parameters are mutually exclusive: " \
                                "baseline_name|device_service_tags|device_ids|device_group_names"
        assert result['failed'] is True

    def test_baseline_complaince_main_failure_case_03(self, mocker, ome_default_args, module_mock, ome_response_mock,
                                                      ome_connection_mock_for_firmware_baseline_compliance_info):
        """when ome response return value is None"""
        mocker.patch(
            'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info.validate_inputs')
        mocker.patch(
            'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info.get_baselines_report_by_device_ids',
            return_value=None)
        ome_default_args.update({"device_ids": [Constants.device_id1]})
        result = self._run_module(ome_default_args)
        assert 'baseline_compliance_info' not in result
        assert result['msg'] == "Unable to fetch the compliance baseline information."

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_baseline_complaince_main_exception_handling_case(self, exc_type, mocker, ome_default_args,
                                                              ome_connection_mock_for_firmware_baseline_compliance_info,
                                                              ome_response_mock):
        ome_default_args.update({"device_service_tags": [Constants.service_tag1]})
        mocker.patch(
            'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info.validate_inputs')
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))

        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(
                'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info.get_baselines_report_by_device_ids',
                side_effect=exc_type('test'))
        else:
            mocker.patch(
                'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_baseline_compliance_info.get_baselines_report_by_device_ids',
                side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                     {"accept-type": "application/json"}, StringIO(json_str)))
        result = self._run_module_with_fail_json(ome_default_args)
        assert 'baseline_compliance_info' not in result
        assert 'msg' in result
        assert result['failed'] is True
        if exc_type == HTTPError:
            assert 'error_info' in result
