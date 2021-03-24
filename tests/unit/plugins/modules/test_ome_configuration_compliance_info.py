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
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.modules import ome_configuration_compliance_info
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants, \
    AnsibleFailJSonException
from io import StringIO
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_configuration_compliance_info.'


@pytest.fixture
def ome_connection_mock_for_compliance_info(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    ome_connection_mock_obj.get_all_report_details.return_value = {"report_list": []}
    return ome_connection_mock_obj


class TestBaselineComplianceInfo(FakeAnsibleModule):
    module = ome_configuration_compliance_info

    def test_validate_device(self, ome_connection_mock_for_compliance_info):
        report_list = [{"Id": 25011, "ServiceTag": "FGHREF"}]
        ome_connection_mock_for_compliance_info.get_all_report_details.return_value = {"report_list": report_list}
        f_module = self.get_module_mock(params={'baseline': "baseline_one", "device_id": 25011})
        device = self.module.validate_device(f_module, ome_connection_mock_for_compliance_info,
                                             device_id=25011, service_tag=None, base_id=None)
        service_tag = self.module.validate_device(f_module, ome_connection_mock_for_compliance_info,
                                                  device_id=None, service_tag="FGHREF", base_id=None)
        with pytest.raises(Exception) as exc:
            self.module.validate_device(f_module, ome_connection_mock_for_compliance_info,
                                        device_id=25012, service_tag=None, base_id=None)
        assert device == 25011
        assert service_tag == 25011
        assert exc.value.args[0] == "Unable to complete the operation because the entered " \
                                    "target device id or service tag '25012' is invalid."

    def test_get_baseline_id(self, ome_connection_mock_for_compliance_info):
        report_list = [{"Id": 1, "Name": "baseline_one", "TemplateId": 1}]
        ome_connection_mock_for_compliance_info.get_all_report_details.return_value = {"report_list": report_list}
        f_module = self.get_module_mock(params={'baseline': "baseline_one"})
        base_id, template_id = self.module.get_baseline_id(f_module, "baseline_one", ome_connection_mock_for_compliance_info)
        with pytest.raises(Exception) as exc:
            self.module.get_baseline_id(f_module, "baseline_two", ome_connection_mock_for_compliance_info)
        assert exc.value.args[0] == "Unable to complete the operation because the entered " \
                                    "target baseline name 'baseline_two' is invalid."
        assert base_id == 1

    def test_compliance_report(self, ome_connection_mock_for_compliance_info, mocker, ome_response_mock):
        mocker.patch(MODULE_PATH + "get_baseline_id", return_value=25011)
        f_module = self.get_module_mock(params={'baseline': "baseline_one"})
        ome_response_mock.json_data = {"value": [{"Id": 25011, "TemplateId": 1}]}
        mocker.patch(MODULE_PATH + 'get_baseline_id', return_value=(1, 1))
        report = self.module.compliance_report(f_module, ome_connection_mock_for_compliance_info)
        assert report == [{'Id': 25011, 'ComplianceAttributeGroups': None, 'TemplateId': 1}]

    def test_main_exception(self, ome_connection_mock_for_compliance_info, mocker,
                            ome_response_mock, ome_default_args):
        ome_default_args.update({"baseline": "baseline_one", "device_id": 25011})
        response = mocker.patch(MODULE_PATH + 'compliance_report')
        ome_response_mock.status_code = 200
        ome_response_mock.success = True
        ome_response_mock.json_data = {"report": "compliance_report"}
        report = self._run_module(ome_default_args)
        assert report["changed"] is False
