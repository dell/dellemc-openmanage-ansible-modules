# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.2.0
# Copyright (C) 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

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
from ansible_collections.dellemc.openmanage.plugins.modules import ome_template_network_vlan_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

SUCCESS_MSG = "Successfully retrieved the template network VLAN information."
NO_TEMPLATES_MSG = "No templates with network info were found."

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_template_network_vlan_info.'


@pytest.fixture
def ome_connection_mock_for_vlaninfo(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeTemplateVlanInfo(FakeAnsibleModule):
    module = ome_template_network_vlan_info

    @pytest.mark.parametrize("params", [
        {"json_data": {"value": [{'Id': 1234, 'Name': "ABCTAG1", "Type": 1000}],
                       "AttributeGroups": [
                           {
                               "GroupNameId": 1001,
                               "DisplayName": "NICModel",
                               "SubAttributeGroups": [
                                   {
                                       "GroupNameId": 3,
                                       "DisplayName": "NIC in Mezzanine 1B",
                                       "SubAttributeGroups": [
                                           {
                                               "GroupNameId": 1,
                                               "DisplayName": "Port ",
                                               "SubAttributeGroups": [
                                                   {
                                                       "GroupNameId": 1,
                                                       "DisplayName": "Partition ",
                                                       "SubAttributeGroups": [],
                                                       "Attributes": [
                                                           {
                                                               "AttributeId": 0,
                                                               "CustomId": 32,
                                                               "AttributeEditInfoId": 0,
                                                               "DisplayName": "Vlan Tagged",
                                                               "Description": None,
                                                               "Value": "25367, 32656, 32658, 26898",
                                                               "IsReadOnly": False,
                                                               "IsIgnored": False,
                                                               "IsSecure": False,
                                                               "IsLinkedToSecure": False,
                                                               "TargetSpecificTypeId": 0
                                                           },
                                                           {
                                                               "AttributeId": 0,
                                                               "CustomId": 32,
                                                               "AttributeEditInfoId": 0,
                                                               "DisplayName": "Vlan UnTagged",
                                                               "Description": None,
                                                               "Value": "21474",
                                                               "IsReadOnly": False,
                                                               "IsIgnored": False,
                                                               "IsSecure": False,
                                                               "IsLinkedToSecure": False,
                                                               "TargetSpecificTypeId": 0
                                                           },
                                                           {
                                                               "AttributeId": 0,
                                                               "CustomId": 32,
                                                               "AttributeEditInfoId": 0,
                                                               "DisplayName": "NIC Bonding Enabled",
                                                               "Description": None,
                                                               "Value": "False",
                                                               "IsReadOnly": False,
                                                               "IsIgnored": False,
                                                               "IsSecure": False,
                                                               "IsLinkedToSecure": False,
                                                               "TargetSpecificTypeId": 0
                                                           }
                                                       ]
                                                   }
                                               ],
                                               "Attributes": []
                                           },
                                           {
                                               "GroupNameId": 2,
                                               "DisplayName": "Port ",
                                               "SubAttributeGroups": [
                                                   {
                                                       "GroupNameId": 1,
                                                       "DisplayName": "Partition ",
                                                       "SubAttributeGroups": [],
                                                       "Attributes": [
                                                           {
                                                               "AttributeId": 0,
                                                               "CustomId": 31,
                                                               "AttributeEditInfoId": 0,
                                                               "DisplayName": "Vlan Tagged",
                                                               "Description": None,
                                                               "Value": None,
                                                               "IsReadOnly": False,
                                                               "IsIgnored": False,
                                                               "IsSecure": False,
                                                               "IsLinkedToSecure": False,
                                                               "TargetSpecificTypeId": 0
                                                           },
                                                           {
                                                               "AttributeId": 0,
                                                               "CustomId": 31,
                                                               "AttributeEditInfoId": 0,
                                                               "DisplayName": "Vlan UnTagged",
                                                               "Description": None,
                                                               "Value": "32658",
                                                               "IsReadOnly": False,
                                                               "IsIgnored": False,
                                                               "IsSecure": False,
                                                               "IsLinkedToSecure": False,
                                                               "TargetSpecificTypeId": 0
                                                           },
                                                           {
                                                               "AttributeId": 0,
                                                               "CustomId": 31,
                                                               "AttributeEditInfoId": 0,
                                                               "DisplayName": "NIC Bonding Enabled",
                                                               "Description": None,
                                                               "Value": "true",
                                                               "IsReadOnly": False,
                                                               "IsIgnored": False,
                                                               "IsSecure": False,
                                                               "IsLinkedToSecure": False,
                                                               "TargetSpecificTypeId": 0
                                                           }
                                                       ]
                                                   }
                                               ],
                                               "Attributes": []
                                           }
                                       ],
                                       "Attributes": []
                                   },
                                   {
                                       "GroupNameId": 1,
                                       "DisplayName": "NIC in Mezzanine 1A",
                                       "SubAttributeGroups": [
                                           {
                                               "GroupNameId": 1,
                                               "DisplayName": "Port ",
                                               "SubAttributeGroups": [
                                                   {
                                                       "GroupNameId": 1,
                                                       "DisplayName": "Partition ",
                                                       "SubAttributeGroups": [],
                                                       "Attributes": [
                                                           {
                                                               "AttributeId": 0,
                                                               "CustomId": 30,
                                                               "AttributeEditInfoId": 0,
                                                               "DisplayName": "Vlan Tagged",
                                                               "Description": None,
                                                               "Value": "32656, 32658",
                                                               "IsReadOnly": False,
                                                               "IsIgnored": False,
                                                               "IsSecure": False,
                                                               "IsLinkedToSecure": False,
                                                               "TargetSpecificTypeId": 0
                                                           },
                                                           {
                                                               "AttributeId": 0,
                                                               "CustomId": 30,
                                                               "AttributeEditInfoId": 0,
                                                               "DisplayName": "Vlan UnTagged",
                                                               "Description": None,
                                                               "Value": "25367",
                                                               "IsReadOnly": False,
                                                               "IsIgnored": False,
                                                               "IsSecure": False,
                                                               "IsLinkedToSecure": False,
                                                               "TargetSpecificTypeId": 0
                                                           },
                                                           {
                                                               "AttributeId": 0,
                                                               "CustomId": 30,
                                                               "AttributeEditInfoId": 0,
                                                               "DisplayName": "NIC Bonding Enabled",
                                                               "Description": None,
                                                               "Value": "true",
                                                               "IsReadOnly": False,
                                                               "IsIgnored": False,
                                                               "IsSecure": False,
                                                               "IsLinkedToSecure": False,
                                                               "TargetSpecificTypeId": 0
                                                           }
                                                       ]
                                                   }
                                               ],
                                               "Attributes": []
                                           },
                                           {
                                               "GroupNameId": 2,
                                               "DisplayName": "Port ",
                                               "SubAttributeGroups": [
                                                   {
                                                       "GroupNameId": 1,
                                                       "DisplayName": "Partition ",
                                                       "SubAttributeGroups": [],
                                                       "Attributes": [
                                                           {
                                                               "AttributeId": 0,
                                                               "CustomId": 29,
                                                               "AttributeEditInfoId": 0,
                                                               "DisplayName": "Vlan Tagged",
                                                               "Description": None,
                                                               "Value": "21474",
                                                               "IsReadOnly": False,
                                                               "IsIgnored": False,
                                                               "IsSecure": False,
                                                               "IsLinkedToSecure": False,
                                                               "TargetSpecificTypeId": 0
                                                           },
                                                           {
                                                               "AttributeId": 0,
                                                               "CustomId": 29,
                                                               "AttributeEditInfoId": 0,
                                                               "DisplayName": "Vlan UnTagged",
                                                               "Description": None,
                                                               "Value": "32656",
                                                               "IsReadOnly": False,
                                                               "IsIgnored": False,
                                                               "IsSecure": False,
                                                               "IsLinkedToSecure": False,
                                                               "TargetSpecificTypeId": 0
                                                           },
                                                           {
                                                               "AttributeId": 0,
                                                               "CustomId": 29,
                                                               "AttributeEditInfoId": 0,
                                                               "DisplayName": "NIC Bonding Enabled",
                                                               "Description": None,
                                                               "Value": "False",
                                                               "IsReadOnly": False,
                                                               "IsIgnored": False,
                                                               "IsSecure": False,
                                                               "IsLinkedToSecure": False,
                                                               "TargetSpecificTypeId": 0
                                                           }
                                                       ]
                                                   }
                                               ],
                                               "Attributes": []
                                           }
                                       ],
                                       "Attributes": []
                                   }
                               ],
                               "Attributes": []
                           },
                           {
                               "GroupNameId": 1005,
                               "DisplayName": "NicBondingTechnology",
                               "SubAttributeGroups": [],
                               "Attributes": [
                                   {
                                       "AttributeId": 0,
                                       "CustomId": 0,
                                       "AttributeEditInfoId": 0,
                                       "DisplayName": "Nic Bonding Technology",
                                       "Description": None,
                                       "Value": "LACP",
                                       "IsReadOnly": False,
                                       "IsIgnored": False,
                                       "IsSecure": False,
                                       "IsLinkedToSecure": False,
                                       "TargetSpecificTypeId": 0
                                   }
                               ]
                           }]},
         'message': SUCCESS_MSG, "success": True, 'case': "template with id",
         'mparams': {"template_id": 1234}},
        {"json_data": {"value": [{'Id': 1234, 'Name': "temp1", "ViewTypeId": 1}]},
         'message': SUCCESS_MSG, "success": True, 'case': "template with name",
         'mparams': {"template_name": "temp1"}},
        {"json_data": {"value": [{'Id': 1234, 'Name': "temp2", "ViewTypeId": 2}]},
         'message': "Template with name 'temp1' not found.", "success": True, 'case': "template not found",
         'mparams': {"template_name": "temp1"}},
        {"json_data": {"value": [{'Id': 1234, 'Name': "temp2", "ViewTypeId": 3}]},
         'message': SUCCESS_MSG, "success": True, 'case': "all templates case",
         'mparams': {}},
        {"json_data": {"value": [{'Id': 1234, 'Name': "temp2", "ViewTypeId": 4}]},
         'message': SUCCESS_MSG, "success": True, 'case': "invalid templates case",
         'mparams': {}}
    ])
    def test_ome_template_network_vlan_info_success(self, params, ome_connection_mock_for_vlaninfo, ome_response_mock,
                                                    ome_default_args, module_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['json_data']
        ome_connection_mock_for_vlaninfo.get_all_items_with_pagination.return_value = params['json_data']
        ome_default_args.update(params['mparams'])
        result = self._run_module(ome_default_args, check_mode=params.get('check_mode', False))
        assert result['msg'] == params['message']

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_template_network_vlan_info_main_exception_failure_case(self, exc_type, mocker, ome_default_args,
                                                                        ome_connection_mock_for_vlaninfo,
                                                                        ome_response_mock):
        ome_default_args.update({"template_id": 1234})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'get_template_details', side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'get_template_details', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'get_template_details',
                         side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result
