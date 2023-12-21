# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.0.0
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import ome_template_identity_pool
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ssl import SSLError
from io import StringIO
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_template_identity_pool.'
template1 = \
    {
        "@odata.context": "/api/$metadata#TemplateService.Template",
        "@odata.type": "#TemplateService.Template",
        "@odata.id": "/api/TemplateService/Templates(9)",
        "Id": 9,
        "Name": "template",
        "Description": None,
        "Content": None,
        "SourceDeviceId": 10116,
        "TypeId": 2,
        "ViewTypeId": 2,
        "TaskId": 10125,
        "HasIdentityAttributes": True,
        "Status": 2060,
        "IdentityPoolId": 1,
        "IsPersistencePolicyValid": True,
        "IsStatelessAvailable": True,
        "IsBuiltIn": False,
        "CreatedBy": "admin",
        "CreationTime": "2022-02-02 09:33:25.887057",
        "LastUpdatedBy": "admin",
        "LastUpdatedTime": "2022-02-02 13:53:37.443315",
        "Views@odata.navigationLink": "/api/TemplateService/Templates(9)/Views",
        "AttributeDetails": {
            "@odata.id": "/api/TemplateService/Templates(9)/AttributeDetails"
        }
    }


@pytest.fixture
def ome_connection_mock_template_identity_pool(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOMETemplateIdentityPool(FakeAnsibleModule):
    module = ome_template_identity_pool

    @pytest.mark.parametrize("exc_type", [HTTPError, URLError, ValueError, TypeError, ConnectionError, SSLError])
    def test_main_template_identity_failure(self, exc_type, mocker, ome_default_args,
                                            ome_connection_mock_template_identity_pool):
        ome_default_args.update({"template_name": "template"})
        ome_connection_mock_template_identity_pool.json_data = {"template_name": "ansible_template"}
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type == URLError:
            mocker.patch(
                MODULE_PATH + 'get_template_id',
                side_effect=exc_type('url error'))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(
                MODULE_PATH + 'get_template_id',
                side_effect=exc_type('error'))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(
                MODULE_PATH + 'get_identity_id',
                side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                     {"accept-type": "application/json"}, StringIO(json_str))
            )
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result

    def test_main_success(self, mocker, ome_default_args, ome_connection_mock_template_identity_pool,
                          ome_response_mock):
        mocker.patch(MODULE_PATH + "get_template_id", return_value=template1)
        mocker.patch(MODULE_PATH + "get_identity_id", return_value=10)
        ome_default_args.update({"template_name": "template", "identity_pool_name": "pool_name"})
        ome_response_mock.json_data = {"msg": "Successfully assigned identity pool to template.", "changed": True}
        ome_response_mock.success = True
        ome_response_mock.status_code = 200
        result = self.execute_module(ome_default_args)
        assert "msg" in result
        assert result["msg"] == "Successfully attached identity pool to " \
                                "template."

    def test_get_template_vlan_info(self, ome_connection_mock_template_identity_pool, ome_response_mock):
        f_module = self.get_module_mock(params={"nic_identifier": "NIC Slot 4"})
        temp_net_details = {
            "AttributeGroups": [
                {
                    "GroupNameId": 1001,
                    "DisplayName": "NICModel",
                    "SubAttributeGroups": [{
                        "GroupNameId": 1,
                        "DisplayName": "NIC Slot 4",
                        "SubAttributeGroups": [],
                        "Attributes": []
                    }],
                    "Attributes": []
                },
                {
                    "GroupNameId": 1005,
                    "DisplayName": "NicBondingTechnology",
                    "SubAttributeGroups": [],
                    "Attributes": [{"AttributeId": 0,
                                    "DisplayName": "Nic Bonding Technology",
                                    "Description": None, "Value": "LACP",
                                    "IsIgnored": False}]
                }
            ]
        }
        ome_response_mock.success = True
        ome_response_mock.json_data = temp_net_details
        nic_bonding_tech = self.module.get_template_vlan_info(ome_connection_mock_template_identity_pool, 12)
        assert nic_bonding_tech == "LACP"

    def test_get_template_id(self, ome_connection_mock_template_identity_pool, ome_response_mock):
        ome_response_mock.json_data = {"value": [{"Name": "template", "Id": 9, "IdentityPoolId": 1}]}
        ome_response_mock.success = True
        f_module = self.get_module_mock(params={"template_name": "template"})
        res_temp = self.module.get_template_id(ome_connection_mock_template_identity_pool, f_module)
        assert res_temp == {"Name": "template", "Id": 9, "IdentityPoolId": 1}

    def test_get_identity_id(self, ome_connection_mock_template_identity_pool):
        data = {"report_list": [{"Name": "pool_name", "Id": 10}]}
        ome_connection_mock_template_identity_pool.get_all_report_details.return_value = data
        f_module = self.get_module_mock(params={"identity_pool_name": "pool_name"})
        result = self.module.get_identity_id(ome_connection_mock_template_identity_pool, f_module)
        assert result == 10

    def test_get_identity_id_fail(self, ome_connection_mock_template_identity_pool, ome_response_mock):
        data = {"report_list": [{"Name": "pool_name", "Id": 10}]}
        ome_connection_mock_template_identity_pool.get_all_report_details.return_value = data
        f_module = self.get_module_mock(params={"identity_pool_name": "invalid_pool_name"})
        with pytest.raises(Exception) as exc:
            self.module.get_identity_id(ome_connection_mock_template_identity_pool, f_module)
        assert exc.value.args[0] == "Unable to complete the operation because the requested identity pool with " \
                                    "name 'invalid_pool_name' is not present."
