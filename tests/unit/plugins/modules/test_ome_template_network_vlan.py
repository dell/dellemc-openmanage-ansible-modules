# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.5
# Copyright (C) 2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible_collections.dellemc.openmanage.plugins.modules import ome_template_network_vlan
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ssl import SSLError
from io import StringIO
from ansible.module_utils._text import to_text
import json

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_template_network_vlan.'


@pytest.fixture
def ome_connection_mock_for_template_network_vlan(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeTemplateNetworkVlan(FakeAnsibleModule):
    module = ome_template_network_vlan

    def test_main_ome_template_network_vlan_success_case1(self, mocker, ome_default_args,
                                                          ome_connection_mock_for_template_network_vlan,
                                                          ome_response_mock):
        sub_param = {
            "nic_identifier": "NIC1",
            "tagged_networks": [
                {
                    "port": 2,
                    "tagged_network_ids": [22763],
                    "tagged_network_names": ["gold", "silver"]
                },
                {
                    "port": 4,
                    "tagged_network_names": ["bronze"]
                }
            ],
            "template_id": 12,
            "untagged_networks": [
                {
                    "port": 2,
                    "untagged_network_name": "plat"
                },
                {
                    "port": 3,
                    "untagged_network_id": 0
                }
            ]
        }
        ome_default_args.update(sub_param)
        untag_dict = {1: 5, 2: 0, 3: 4}
        tagged_dict = {1: [1, 2], 2: [], 3: [6]}
        payload = {"TemplateId": 12,
                   "VlanAttributes": [{"ComponentId": 2302, "Tagged": [12765, 12767, 12768], "Untagged": 12766},
                                      {"ComponentId": 2301, "Tagged": [12765, 12766], "Untagged": 12767}]}
        mocker.patch(MODULE_PATH + 'validate_vlans',
                     return_value=(untag_dict, tagged_dict))
        mocker.patch(MODULE_PATH + 'get_vlan_payload',
                     return_value=payload)
        ome_response_mock.json_data = {}
        ome_response_mock.success = True
        result = self.execute_module(ome_default_args)
        assert result['changed'] is True
        assert "msg" in result
        assert result["msg"] == "Successfully applied the network settings to the template"

    @pytest.mark.parametrize("params",
                             [{"mparams": {"template_id": 123}, "success": True,
                               "json_data": {"value": [{"Name": "vlan_name", "Id": 123, "IdentityPoolId": 23}]},
                               "res": {"Name": "vlan_name", "Id": 123, "IdentityPoolId": 23}}])
    def test_get_template_details(self, params, ome_connection_mock_for_template_network_vlan, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params["mparams"])
        result = self.module.get_template_details(f_module, ome_connection_mock_for_template_network_vlan)
        assert result == params["res"]

    @pytest.mark.parametrize("kv",
                             [{"key": "1", "dct": {"one": "1", "two": "2"}, "res": "one"},
                              {"key": "3", "dct": {"one": "1", "two": "2"}, "res": None}])
    def test_get_key(self, kv):
        val = kv["key"]
        d = kv["dct"]
        k = self.module.get_key(val, d)
        assert k == kv["res"]

    def test_get_vlan_name_id_map(self, ome_connection_mock_for_template_network_vlan, ome_response_mock):
        ome_response_mock.success = True
        ome_response_mock.json_data = {"value": [{"Name": "vlan1", "Id": 1},
                                                 {"Name": "vlan2", "Id": 2}]}
        d = self.module.get_vlan_name_id_map(ome_connection_mock_for_template_network_vlan)
        assert d == {"vlan1": 1, "vlan2": 2}

    def test_get_template_vlan_info(self, ome_connection_mock_for_template_network_vlan, ome_response_mock):
        f_module = self.get_module_mock(params={"nic_identifier": "NIC Slot 4"})
        temp_net_details = {
            "AttributeGroups": [{
                "GroupNameId": 1001,
                "DisplayName": "NICModel",
                "SubAttributeGroups": [{
                    "GroupNameId": 1,
                    "DisplayName": "NIC Slot 4",
                    "SubAttributeGroups": [
                        {
                            "GroupNameId": 1,
                            "SubAttributeGroups": [{
                                "GroupNameId": 1,
                                "DisplayName": "Partition",
                                "SubAttributeGroups": [],
                                "Attributes": [
                                    {
                                        "CustomId": 2302,
                                        "DisplayName": "Vlan Tagged",
                                        "Value": "12765, 12767, 12768"
                                    },
                                    {
                                        "CustomId": 2302,
                                        "DisplayName": "Vlan UnTagged",
                                        "Value": "12766"
                                    }
                                ]
                            }],
                            "Attributes": []
                        },
                        {
                            "GroupNameId": 2,
                            "DisplayName": "Port ",
                            "SubAttributeGroups": [{
                                "GroupNameId": 1,
                                "DisplayName": "Partition ",
                                "SubAttributeGroups": [],
                                "Attributes": [
                                    {
                                        "CustomId": 2301,
                                        "DisplayName": "Vlan Tagged",
                                        "Value": "12766"
                                    },
                                    {
                                        "CustomId": 2301,
                                        "DisplayName": "Vlan UnTagged",
                                        "Value": "12767"
                                    }
                                ]
                            }],
                            "Attributes": []
                        }
                    ],
                    "Attributes": []
                }],
                "Attributes": []
            }]
        }
        ome_response_mock.success = True
        ome_response_mock.json_data = temp_net_details
        port_id_map, port_untagged_map, port_tagged_map, port_nic_bond_map, nic_bonding_tech\
            = self.module.get_template_vlan_info(f_module, ome_connection_mock_for_template_network_vlan, 12)
        assert port_id_map == {1: 2302, 2: 2301}
        assert port_untagged_map == {1: 12766, 2: 12767}
        assert port_tagged_map == {1: [12765, 12767, 12768], 2: [12766]}

    def test_get_vlan_payload(self, mocker, ome_connection_mock_for_template_network_vlan):
        f_module = self.get_module_mock(params={"template_id": 12})
        untag_dict = {1: 12766}
        tagged_dict = {2: [12765, 12766]}
        port_id_map = {1: 2302, 2: 2301}
        port_untagged_map = {1: 12766, 2: 12767}
        port_tagged_map = {1: [12765, 12767, 12768], 2: [12766]}
        port_nic_bond_map = {1: True, 2: False}
        nic_bonding_tech = "LACP"
        mocker.patch(MODULE_PATH + 'get_template_details',
                     return_value={"Name": "vlan_name", "Id": 12, "IdentityPoolId": 23})
        mocker.patch(MODULE_PATH + 'get_template_vlan_info',
                     return_value=(port_id_map, port_untagged_map, port_tagged_map, port_nic_bond_map, nic_bonding_tech))
        payload = self.module.get_vlan_payload(f_module, ome_connection_mock_for_template_network_vlan, untag_dict,
                                               tagged_dict)
        assert payload["TemplateId"] == 12
        assert payload["VlanAttributes"] == [{"ComponentId": 2302, "Tagged": [12765, 12767, 12768], "Untagged": 12766,
                                              'IsNicBonded': True},
                                             {"ComponentId": 2301, "Tagged": [12765, 12766], "Untagged": 12767,
                                              'IsNicBonded': False}]

    def test_validate_vlans(self, mocker, ome_connection_mock_for_template_network_vlan):
        f_module = self.get_module_mock(params={"tagged_networks": [
            {"port": 1, "tagged_network_ids": [1, 2]},
            {"port": 2, "tagged_network_names": []},
            {"port": 3, "tagged_network_names": ["bronze"]}],
            "untagged_networks": [
                {"port": 1, "untagged_network_name": "plat"},
                {"port": 2, "untagged_network_id": 0},
                {"port": 3, "untagged_network_id": 4}]})
        mocker.patch(MODULE_PATH + 'get_vlan_name_id_map',
                     return_value={"vlan1": 1, "vlan2": 2, "gold": 3, "silver": 4, "plat": 5, "bronze": 6})
        untag_dict, tagged_dict = self.module.validate_vlans(f_module, ome_connection_mock_for_template_network_vlan)
        assert untag_dict == {1: 5, 2: 0, 3: 4}
        assert tagged_dict == {1: [1, 2], 2: [], 3: [6]}

    @pytest.mark.parametrize("params",
                             [{"inp": {"nic_identifier": "NIC1",
                                       "template_id": 12},
                               "msg": "Either tagged_networks | untagged_networks data needs to be provided"},
                              {"inp": {"untagged_networks": [
                                  {"port": 2, "untagged_network_name": "plat"},
                                  {"port": 2, "untagged_network_id": 0}
                              ]},
                                  "msg": "port 2 is repeated for untagged_network_id"},
                              {"inp": {"tagged_networks": [
                                  {"port": 1, "tagged_network_ids": [1, 7]},
                                  {"port": 2, "tagged_network_names": []},
                                  {"port": 3, "tagged_network_names": ["bronze"]}]},
                                  "msg": "7 is not a valid vlan id port 1"},
                              {"inp": {"tagged_networks": [
                                  {"port": 1, "tagged_network_ids": []},
                                  {"port": 3, "tagged_network_names": ["bronzy"]}]},
                                  "msg": "bronzy is not a valid vlan name port 3"},
                              {"inp": {"untagged_networks": [
                                  {"port": 2, "untagged_network_name": "platy"},
                                  {"port": 3, "untagged_network_id": 0}
                              ]},
                                  "msg": "platy is not a valid vlan name for port 2"},
                              {"inp": {"untagged_networks": [
                                  {"port": 2, "untagged_network_name": "plat"},
                                  {"port": 1, "untagged_network_id": 7}
                              ]},
                                  "msg": "untagged_network_id: 7 is not a valid vlan id for port 1"},
                              {"inp": {"tagged_networks": [
                                  {"port": 1, "tagged_network_ids": [1]}],
                                  "untagged_networks": [
                                      {"port": 1, "untagged_network_id": 1}]},
                                  "msg": "vlan 1('vlan1') cannot be in both tagged and untagged list for port 1"}
                              ])
    def test_validate_vlans_failure(self, params, mocker, ome_connection_mock_for_template_network_vlan):
        f_module = self.get_module_mock(params["inp"])
        mocker.patch(MODULE_PATH + 'get_vlan_name_id_map',
                     return_value={"vlan1": 1, "vlan2": 2, "gold": 3, "silver": 4, "plat": 5, "bronze": 6})
        with pytest.raises(Exception) as exc:
            self.module.validate_vlans(f_module, ome_connection_mock_for_template_network_vlan)
        assert exc.value.args[0] == params["msg"]

    @pytest.mark.parametrize("modify_setting_payload",
                             [{"Description": "Identity pool with ethernet and fcoe settings2"}, {"Name": "pool2"},
                              {"EthernetSettings": {"Mac": {"IdentityCount": 61, "StartingMacAddress": "UFBQUFAA"}}},
                              {"Description": "Identity pool with ethernet and fcoe settings2",
                               "EthernetSettings": {"Mac": {"IdentityCount": 60, "StartingMacAddress": "UFBQUFAA"}},
                               "FcoeSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "cHBwcHAA"}}}])
    def test_compare_payload_attributes_case_false(self, modify_setting_payload):
        existing_setting_payload = {
            "@odata.context": "/api/$metadata#IdentityPoolService.IdentityPool",
            "@odata.type": "#IdentityPoolService.IdentityPool",
            "@odata.id": "/api/IdentityPoolService/IdentityPools(23)",
            "Id": 23,
            "Name": "pool1",
            "Description": "Identity pool with ethernet and fcoe settings1",
            "CreatedBy": "admin",
            "CreationTime": "2020-01-31 09:28:16.491424",
            "LastUpdatedBy": "admin",
            "LastUpdateTime": "2020-01-31 09:49:59.012549",
            "EthernetSettings": {
                "Mac": {
                    "IdentityCount": 60,
                    "StartingMacAddress": "UFBQUFAA"
                }
            },
            "IscsiSettings": None,
            "FcoeSettings": {
                "Mac": {
                    "IdentityCount": 70,
                    "StartingMacAddress": "cHBwcHAA"
                }
            },
            "FcSettings": None,
            "UsageCounts": {
                "@odata.id": "/api/IdentityPoolService/IdentityPools(23)/UsageCounts"
            },
            "UsageIdentitySets@odata.navigationLink": "/api/IdentityPoolService/IdentityPools(23)/UsageIdentitySets"
        }
        val = self.module.compare_nested_dict(modify_setting_payload, existing_setting_payload)
        assert val is False

    @pytest.mark.parametrize("vlan_payload", [
        {"Name": "pool1", "EthernetSettings": {"Mac": {"StartingMacAddress": "qrvM3e6q"}}},
        {"Name": "pool1", "EthernetSettings": {"Mac": {"IdentityCount": 70}}},
        {"Description": "Identity pool with ethernet setting",
         "EthernetSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "qrvM3e6q"}},
         "FcoeSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "cHBwcHAA"}}}])
    def test_compare_payload_attributes_case_true(self, vlan_payload):
        """setting values are same as existing payload and no need to apply the changes again"""
        existing_setting_payload = {
            "@odata.context": "/api/$metadata#IdentityPoolService.IdentityPool",
            "@odata.type": "#IdentityPoolService.IdentityPool",
            "@odata.id": "/api/IdentityPoolService/IdentityPools(30)",
            "Id": 30,
            "Name": "pool1",
            "Description": "Identity pool with ethernet setting",
            "CreatedBy": "admin",
            "CreationTime": "2020-01-31 11:31:13.621182",
            "LastUpdatedBy": "admin",
            "LastUpdateTime": "2020-01-31 11:34:28.00876",
            "EthernetSettings": {
                "Mac": {
                    "IdentityCount": 70,
                    "StartingMacAddress": "qrvM3e6q"
                }
            },
            "IscsiSettings": None,
            "FcoeSettings": {
                "Mac": {
                    "IdentityCount": 70,
                    "StartingMacAddress": "cHBwcHAA"
                }
            },
            "FcSettings": None,
            "UsageCounts": {
                "@odata.id": "/api/IdentityPoolService/IdentityPools(30)/UsageCounts"
            },
            "UsageIdentitySets@odata.navigationLink": "/api/IdentityPoolService/IdentityPools(30)/UsageIdentitySets"
        }
        val = self.module.compare_nested_dict(vlan_payload, existing_setting_payload)
        assert val is True

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_application_network_vlan_main_success_failure_case(self, exc_type, mocker, ome_default_args,
                                                                    ome_connection_mock_for_template_network_vlan,
                                                                    ome_response_mock):
        ome_default_args.update({"nic_identifier": "NIC1", "template_id": 123, "tagged_networks": [
            {"port": 2, "tagged_network_ids": [22763], "tagged_network_names": ["gold", "silver"]}]})
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'validate_vlans',
                         side_effect=exc_type("TEST"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'validate_vlans',
                         side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'validate_vlans',
                         side_effect=exc_type('http://testhost.com', 400,
                                              'http error message',
                                              {"accept-type": "application/json"},
                                              StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'proxy_configuration' not in result
        assert 'msg' in result
