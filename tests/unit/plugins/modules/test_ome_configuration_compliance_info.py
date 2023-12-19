# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.2.0
# Copyright (C) 2021-2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
from io import StringIO

import pytest
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import ome_configuration_compliance_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_configuration_compliance_info.'


@pytest.fixture
def ome_connection_mock_for_compliance_info(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    ome_connection_mock_obj.get_all_report_details.return_value = {
        "report_list": []}
    ome_connection_mock_obj.get_all_items_with_pagination.return_value = {
        "value": []}
    return ome_connection_mock_obj


class TestBaselineComplianceInfo(FakeAnsibleModule):
    module = ome_configuration_compliance_info

    @pytest.mark.parametrize("params", [
        {"json_data": {"report_list": [
            {'Name': 'b1', 'Id': 123,
             'TemplateId': 23},
            {'Name': 'b2', 'Id': 124,
             'TemplateId': 24}],
            'ComplianceAttributeGroups': [{"Device": "Compliant"}]},
            'report': [{'Device': 'Compliant'}],
            'mparams': {"baseline": "b1", "device_id": 1234}},
        {"json_data": {"report_list": [
            {'Name': 'b1', 'Id': 123, 'TemplateId': 23},
            {'Name': 'b2', 'Id': 124, 'TemplateId': 24}],
            'value': [{'Id': 123, 'ServiceTag': 'ABCD123'},
                      {'Id': 124, 'ServiceTag': 'ABCD124'}],
            'ComplianceAttributeGroups': [{"Device": "Compliant"}]},
            'report': [{'ComplianceAttributeGroups': [{'Device': 'Compliant'}], 'Id': 123, 'ServiceTag': 'ABCD123'}],
            'mparams': {"baseline": "b1", "device_service_tag": 'ABCD123'}}
    ])
    def test_ome_configuration_compliance_info_success(self, params, ome_connection_mock_for_compliance_info, ome_response_mock,
                                                       ome_default_args, module_mock, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['json_data']
        ome_connection_mock_for_compliance_info.get_all_report_details.return_value = params[
            'json_data']
        ome_connection_mock_for_compliance_info.get_all_items_with_pagination.return_value = params[
            'json_data']
        ome_default_args.update(params['mparams'])
        result = self._run_module(
            ome_default_args, check_mode=params.get('check_mode', False))
        assert result['compliance_info'] == params['report']

    def test_validate_device(self, ome_connection_mock_for_compliance_info):
        value_list = [{"Id": 25011, "ServiceTag": "FGHREF"}]
        report = ome_connection_mock_for_compliance_info.get_all_items_with_pagination.return_value = {
            "value": value_list}
        f_module = self.get_module_mock(
            params={'baseline': "baseline_one", "device_id": 25011})
        device = self.module.validate_device(f_module, report,
                                             device_id=25011, service_tag=None, base_id=None)
        service_tag = self.module.validate_device(f_module, report,
                                                  device_id=None, service_tag="FGHREF", base_id=None)
        with pytest.raises(Exception) as exc:
            self.module.validate_device(f_module, report,
                                        device_id=25012, service_tag=None, base_id=None)
        assert device == 25011
        assert service_tag == 25011
        assert exc.value.args[0] == "Unable to complete the operation because the entered " \
                                    "target device id or service tag '25012' is invalid."

    def test_get_baseline_id(self, ome_connection_mock_for_compliance_info):
        report_list = [{"Id": 1, "Name": "baseline_one", "TemplateId": 1}]
        ome_connection_mock_for_compliance_info.get_all_report_details.return_value = {
            "report_list": report_list}
        f_module = self.get_module_mock(params={'baseline': "baseline_one"})
        base_id, template_id = self.module.get_baseline_id(
            f_module, "baseline_one", ome_connection_mock_for_compliance_info)
        with pytest.raises(Exception) as exc:
            self.module.get_baseline_id(
                f_module, "baseline_two", ome_connection_mock_for_compliance_info)
        assert exc.value.args[0] == "Unable to complete the operation because the entered " \
                                    "target baseline name 'baseline_two' is invalid."
        assert base_id == 1

    def test_compliance_report(self, ome_connection_mock_for_compliance_info, mocker, ome_response_mock):
        value_list = [{"Id": 25011, "TemplateId": 1}]
        ome_connection_mock_for_compliance_info.get_all_items_with_pagination.return_value = {
            "value": value_list}
        mocker.patch(MODULE_PATH + "get_baseline_id", return_value=25011)
        f_module = self.get_module_mock(params={'baseline': "baseline_one"})
        ome_response_mock.json_data = {
            "value": [{"Id": 25011, "TemplateId": 1}]}
        mocker.patch(MODULE_PATH + 'get_baseline_id', return_value=(1, 1))
        report = self.module.compliance_report(
            f_module, ome_connection_mock_for_compliance_info)
        assert report == [
            {'Id': 25011, 'ComplianceAttributeGroups': None, 'TemplateId': 1}]

    @pytest.mark.parametrize("exc_type",
                             [SSLValidationError, ConnectionError, TypeError, ValueError, OSError, HTTPError, URLError])
    def test_main_exception(self, exc_type, ome_connection_mock_for_compliance_info, mocker,
                            ome_response_mock, ome_default_args):
        ome_default_args.update(
            {"baseline": "baseline_one", "device_id": 25011})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type == HTTPError:
            mocker.patch(MODULE_PATH + 'compliance_report', side_effect=exc_type(
                'https://testhost.com', 401, 'http error message', {
                    "accept-type": "application/json"},
                StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        elif exc_type == URLError:
            mocker.patch(MODULE_PATH + 'compliance_report',
                         side_effect=exc_type("exception message"))
            result = self._run_module(ome_default_args)
            assert result['unreachable'] is True
        else:
            mocker.patch(MODULE_PATH + 'compliance_report',
                         side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
