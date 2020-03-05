# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0.8
# Copyright (C) 2020 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

from __future__ import absolute_import

import pytest
from ansible.modules.remote_management.dellemc import ome_template_network_vlan
from units.modules.remote_management.dellemc.common import FakeAnsibleModule, Constants
from units.compat.mock import MagicMock
from units.modules.remote_management.dellemc.common import AnsibleFailJSonException
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from units.modules.utils import AnsibleExitJson
from ssl import SSLError
from io import StringIO
from ansible.module_utils._text import to_text
import json
from ansible.module_utils import basic
from units.modules.utils import set_module_args, exit_json, fail_json, AnsibleExitJson
import ast

@pytest.fixture
def ome_connection_mock_for_template_network_vlan(mocker, ome_response_mock):
    connection_class_mock = mocker.patch('ansible.modules.remote_management.dellemc.ome_template_network_vlan.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeTemplateNetworkVlan(FakeAnsibleModule):
    module = ome_template_network_vlan

    def main_ome_template_network_vlan_success_case1(self, mocker, ome_default_args,
                                                  ome_connection_mock_for_template_network_vlan, ome_response_mock):
        sub_param = {"tagged_networks": [
                {"port": 2,"tagged_network_ids": [22763],
                    "tagged_network_names": ["gold","silver"]},
                {"port": 4,"tagged_network_names": ["bronze"]}],
            "template_id": 12,
            "untagged_networks": [
                {"port": 2,"untagged_network_name": "plat"},
                {"port": 3,"untagged_network_id": 0}
            ]}
        untag_dict = {1: 5, 2: 0, 3: 4}
        tagged_dict = {1: [1, 2], 2: [], 3: [6]}
        payload = {"TemplateId": 12, "VlanAttributes" : [{"ComponentId": 2302, "Tagged": [12765, 12767, 12768], "Untagged": 12766},
                                             {"ComponentId": 2301, "Tagged": [12765, 12766], "Untagged": 12767}]}
        mocker.patch('ansible.modules.remote_management.dellemc.ome_template_network_vlan.get_vlan_payload',
                     return_value=())
        mocker.patch('ansible.modules.remote_management.dellemc.ome_template_network_vlan.get_vlan_payload',
                     return_value=payload)
        ome_default_args.update(sub_param)
        result = self.execute_module(ome_default_args)
        assert result['changed'] is True
        assert "msg" in result
        assert result["msg"] == "Successfully applied the network settings to template"


    def test_get_item_id(self, ome_connection_mock_for_template_network_vlan, ome_response_mock):
        ome_response_mock.success = True
        ome_response_mock.json_data = { "value": [{"Name": "template_name", "Id": 123}]}
        id = self.module.get_item_id(ome_connection_mock_for_template_network_vlan, "template_name", "uri")
        assert id == 123

    def test_get_key(self):
        val = "1"
        d = {"one": "1", "two": "2"}
        k = self.module.get_key(val, d)
        assert k == "one"

    def test_get_vlan_name_id_map(self, ome_connection_mock_for_template_network_vlan, ome_response_mock):
        ome_response_mock.success = True
        ome_response_mock.json_data = {"value": [{"Name": "vlan1", "Id": 1},
                                                 {"Name": "vlan2", "Id": 2}]}
        d = self.module.get_vlan_name_id_map(ome_connection_mock_for_template_network_vlan)
        assert d == {"vlan1":1, "vlan2":2}

    def test_get_template_vlan_info(self, ome_connection_mock_for_template_network_vlan, ome_response_mock):
        f_module = self.get_module_mock(params={"nic_identifier": "NIC Slot 4"})
        temp_net_details = {
                                "AttributeGroups": [{
                                    "GroupNameId": 1001,"DisplayName": "NICModel",
                                    "SubAttributeGroups": [{
                                        "GroupNameId": 1,"DisplayName": "NIC Slot 4",
                                        "SubAttributeGroups": [{
                                            "GroupNameId": 1,"SubAttributeGroups": [{"GroupNameId": 1,"DisplayName": "Partition",
                                                "SubAttributeGroups": [],
                                                "Attributes": [{"CustomId": 2302,"DisplayName": "Vlan Tagged","Value": "12765, 12767, 12768"},
                                                {"CustomId": 2302,"DisplayName": "Vlan UnTagged","Value": "12766"}]}],
                                            "Attributes": []},
                                        {"GroupNameId": 2,"DisplayName": "Port ",
                                            "SubAttributeGroups": [{
                                                "GroupNameId": 1,"DisplayName": "Partition ",
                                                "SubAttributeGroups": [],
                                                "Attributes": [{
                                                    "CustomId": 2301,"DisplayName": "Vlan Tagged","Value": "12766"},
                                                {"CustomId": 2301,"DisplayName": "Vlan UnTagged","Value": "12767"}]
                                            }],
                                            "Attributes": []}],"Attributes": []}],"Attributes": []}]}
        ome_response_mock.success = True
        ome_response_mock.json_data = temp_net_details
        port_id_map, port_untagged_map, port_tagged_map = self.module.get_template_vlan_info(
            f_module, ome_connection_mock_for_template_network_vlan, 12)
        assert port_id_map == {1: 2302, 2:2301}
        assert port_untagged_map == {1: 12766, 2: 12767}
        assert port_tagged_map == {1: [12765, 12767, 12768], 2: [12766]}

    def test_get_vlan_payload(self, mocker, ome_connection_mock_for_template_network_vlan):
        f_module = self.get_module_mock(params={"template_id": 12})
        untag_dict = {1: 12766}
        tagged_dict = {2: [12765, 12766]}
        port_id_map = {1: 2302, 2: 2301}
        port_untagged_map = {1: 12766, 2: 12767}
        port_tagged_map = {1: [12765, 12767, 12768], 2: [12766]}
        mocker.patch('ansible.modules.remote_management.dellemc.ome_template_network_vlan.get_template_vlan_info',
                     return_value=(port_id_map, port_untagged_map, port_tagged_map))
        payload = self.module.get_vlan_payload(f_module, ome_connection_mock_for_template_network_vlan, untag_dict, tagged_dict)
        assert payload["TemplateId"] == 12
        assert payload["VlanAttributes"] == [{"ComponentId":2302,"Tagged":[12765, 12767, 12768], "Untagged":12766},
                                             {"ComponentId":2301,"Tagged":[12765, 12766], "Untagged":12767}]

    def test_validate_vlans(self, mocker, ome_connection_mock_for_template_network_vlan):
        f_module = self.get_module_mock(params={ "tagged_networks": [
                {"port": 1,"tagged_network_ids": [1,2]},
                {"port": 2,"tagged_network_names": []},
                {"port": 3,"tagged_network_names": ["bronze"]}],
            "untagged_networks": [
                {"port": 1,"untagged_network_name": "plat"},
                {"port": 2,"untagged_network_id": 0},
                {"port": 3,"untagged_network_id": 4}]})
        mocker.patch('ansible.modules.remote_management.dellemc.ome_template_network_vlan.get_vlan_name_id_map',
                     return_value={"vlan1":1, "vlan2":2, "gold":3, "silver":4, "plat":5, "bronze": 6})
        untag_dict, tagged_dict = self.module.validate_vlans(f_module, ome_connection_mock_for_template_network_vlan)
        assert untag_dict == {1: 5, 2: 0, 3:4}
        assert tagged_dict == {1:[1,2], 2: [], 3:[6]}

    @pytest.mark.parametrize("modify_setting_payload", [{"Description": "Identity pool with ethernet and fcoe settings2"}, {"Name": "pool2"}, {"EthernetSettings":{"Mac":{"IdentityCount":61,"StartingMacAddress":"UFBQUFAA"}}},
                                                        {"Description": "Identity pool with ethernet and fcoe settings2", "EthernetSettings": {"Mac": {"IdentityCount": 60, "StartingMacAddress": "UFBQUFAA"}},
                                                         "FcoeSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "cHBwcHAA"}}}])
    def test_compare_payload_attributes_case_false(self, modify_setting_payload):
        modify_setting_payload = modify_setting_payload
        existing_setting_payload = {"@odata.context":"/api/$metadata#IdentityPoolService.IdentityPool","@odata.type":"#IdentityPoolService.IdentityPool","@odata.id":"/api/IdentityPoolService/IdentityPools(23)","Id":23,"Name":"pool1","Description":"Identity pool with ethernet and fcoe settings1","CreatedBy":"admin","CreationTime":"2020-01-31 09:28:16.491424","LastUpdatedBy":"admin","LastUpdateTime":"2020-01-31 09:49:59.012549","EthernetSettings":{"Mac":{"IdentityCount":60,"StartingMacAddress":"UFBQUFAA"}},"IscsiSettings":None,"FcoeSettings":{"Mac":{"IdentityCount":70,"StartingMacAddress":"cHBwcHAA"}},"FcSettings":None,"UsageCounts":{"@odata.id":"/api/IdentityPoolService/IdentityPools(23)/UsageCounts"},"UsageIdentitySets@odata.navigationLink":"/api/IdentityPoolService/IdentityPools(23)/UsageIdentitySets"}
        val = self.module.compare_nested_dict(modify_setting_payload, existing_setting_payload)
        assert val is False

    @pytest.mark.parametrize("modify_setting_payload", [
                                                        {"Name": "pool1", "EthernetSettings": {"Mac": {"StartingMacAddress": "qrvM3e6q"}}},
                                                        {"Name": "pool1", "EthernetSettings": {"Mac": {"IdentityCount": 70}}},
                                                        {"Description": "Identity pool with ethernet setting", "EthernetSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "qrvM3e6q"}},
                                                         "FcoeSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "cHBwcHAA"}}}])
    def test_compare_payload_attributes_case_true(self, modify_setting_payload):
        """setting values are same as existing payload and no need to apply the changes again"""
        modify_setting_payload = modify_setting_payload
        existing_setting_payload = {"@odata.context":"/api/$metadata#IdentityPoolService.IdentityPool","@odata.type":"#IdentityPoolService.IdentityPool","@odata.id":"/api/IdentityPoolService/IdentityPools(30)","Id":30,"Name":"pool1","Description":"Identity pool with ethernet setting","CreatedBy":"admin","CreationTime":"2020-01-31 11:31:13.621182","LastUpdatedBy":"admin","LastUpdateTime":"2020-01-31 11:34:28.00876","EthernetSettings": {"Mac": {"IdentityCount": 70,"StartingMacAddress": "qrvM3e6q"}},"IscsiSettings": None,"FcoeSettings":{"Mac":{"IdentityCount":70,"StartingMacAddress":"cHBwcHAA"}},"FcSettings":None,"UsageCounts":{"@odata.id":"/api/IdentityPoolService/IdentityPools(30)/UsageCounts"},"UsageIdentitySets@odata.navigationLink":"/api/IdentityPoolService/IdentityPools(30)/UsageIdentitySets"}
        val = self.module.compare_nested_dict(modify_setting_payload, existing_setting_payload)
        assert val is True










