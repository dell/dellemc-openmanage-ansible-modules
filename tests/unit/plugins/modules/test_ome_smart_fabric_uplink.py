# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.3.0
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

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
from ansible_collections.dellemc.openmanage.plugins.modules import ome_smart_fabric_uplink
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_smart_fabric_uplink.'


@pytest.fixture
def ome_connection_mock_for_smart_fabric_uplink(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeSmartFabricUplink(FakeAnsibleModule):
    module = ome_smart_fabric_uplink

    @pytest.mark.parametrize("params",
                             [{"success": True, "json_data": {"value": [{"Name": "vlan_name", "Id": 123}]}, "id": 123},
                              {"success": True, "json_data": {"value": []}, "id": 0},
                              {"success": False, "json_data": {"value": [{"Name": "vlan_name", "Id": 123}]}, "id": 0},
                              {"success": True, "json_data": {"value": [{"Name": "vlan_name1", "Id": 123}]}, "id": 0}])
    def test_get_item_id(self, params, ome_connection_mock_for_smart_fabric_uplink, ome_response_mock):
        ome_response_mock.success = params["success"]
        ome_response_mock.json_data = params["json_data"]
        id, vlans = self.module.get_item_id(ome_connection_mock_for_smart_fabric_uplink, "vlan_name", "uri")
        assert id == params["id"]

    @pytest.mark.parametrize(
        "params", [{"uplinks": [{"Ports": [1, 2]}, {"Ports": []}], "portlist": [1, 2]},
                   {"uplinks": [{"Ports": [1, 2]}, {"Ports": [3, 4]}, {"Ports": [5, 4]}],
                    "portlist": [1, 2, 3, 4, 5, 4]},
                   {"uplinks": [{"Ports": [1, 2]}, {"Ports": [3, 4]}], "portlist": [1, 2, 3, 4]}, ])
    def test_get_all_uplink_ports(self, params):
        portlist = self.module.get_all_uplink_ports(params.get("uplinks"))
        assert portlist == params.get("portlist")

    @pytest.mark.parametrize("params", [{"inp": {"tagged_networks": ["vlan_name"]}, "success": True,
                                         "json_data": {"ApplicableUplinkNetworks": [{"Name": "vlan_name", "Id": 123}]},
                                         "payload": [123]}, ])
    def test_validate_networks(self, params, ome_connection_mock_for_smart_fabric_uplink, ome_response_mock):
        ome_response_mock.success = params["success"]
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params.get("inp", {}))
        vlan_payload = self.module.validate_networks(f_module, ome_connection_mock_for_smart_fabric_uplink, 1, 2)
        assert vlan_payload == params["payload"]

    @pytest.mark.parametrize("params", [{"inp": {"tagged_networks": ["vlan_name1"]}, "success": True,
                                         "json_data": {"ApplicableUplinkNetworks": [{"Name": "vlan_name", "Id": 123}]},
                                         "payload": [123],
                                         "error_msg": "Networks with names vlan_name1 are not applicable or valid."},
                                        {"inp": {"tagged_networks": ["vlan_name1", "vlan_name2"]}, "success": True,
                                         "json_data": {"ApplicableUplinkNetworks": [{"Name": "vlan_name", "Id": 123}]},
                                         "payload": [123],
                                         "error_msg": "Networks with names {0} are not applicable "
                                                      "or valid.".format(
                                             ",".join(set(["vlan_name1", "vlan_name2"])))}, ])
    def test_validate_networks_failure(self, params, ome_connection_mock_for_smart_fabric_uplink, ome_response_mock):
        ome_response_mock.success = params["success"]
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params.get("inp", {}))
        error_message = params["error_msg"]
        with pytest.raises(Exception) as err:
            self.module.validate_networks(f_module, ome_connection_mock_for_smart_fabric_uplink, 1, 2)
        assert err.value.args[0] == error_message

    @pytest.mark.parametrize("params", [
        {"inp": {"primary_switch_service_tag": "ABC123", "primary_switch_ports": ["ethernet1/1/7", "ethernet1/1/4"]},
         "success": True, "json_data": {
            "InventoryInfo": [{"PortNumber": "ethernet1/1/6"}, {"PortNumber": "ethernet1/1/7"},
                              {"PortNumber": "ethernet1/1/4"}]}, "get_item_id": (0, []), "payload": [123],
         "uplinks": [{"Ports": [{"Id": "ethernet1/1/6"}]}, {"Ports": [{"Id": "ethernet1/1/4"}]}],
         "error_msg": "Device with service tag ABC123 does not exist."}])
    def test_validate_ioms_failure(self, mocker, params, ome_connection_mock_for_smart_fabric_uplink,
                                   ome_response_mock):
        ome_response_mock.success = params["success"]
        ome_response_mock.json_data = params["json_data"]
        mocker.patch(MODULE_PATH + "get_item_id", return_value=(params.get("get_item_id")))
        f_module = self.get_module_mock(params=params.get("inp", {}))
        error_message = params["error_msg"]
        with pytest.raises(Exception) as err:
            self.module.validate_ioms(f_module, ome_connection_mock_for_smart_fabric_uplink, params.get("uplinks"))
        assert err.value.args[0] == error_message

    @pytest.mark.parametrize("params", [
        {"inp": {"primary_switch_service_tag": "ABC123", "primary_switch_ports": ["ethernet1/1/7", "ethernet1/1/4"]},
         "success": True, "json_data": {
            "InventoryInfo": [{"PortNumber": "ethernet1/1/6"}, {"PortNumber": "ethernet1/1/7"},
                              {"PortNumber": "ethernet1/1/4"}]}, "get_item_id": (2, []), "payload": [123],
         "uplinks": [{"Ports": [{"Id": "ethernet1/1/6"}]}, {"Ports": [{"Id": "ethernet1/1/4"}]}],
         "ioms": ['ABC123:ethernet1/1/7', 'ABC123:ethernet1/1/4']}])
    def test_validate_ioms(self, mocker, params, ome_connection_mock_for_smart_fabric_uplink, ome_response_mock):
        ome_response_mock.success = params["success"]
        ome_response_mock.json_data = params["json_data"]
        mocker.patch(MODULE_PATH + "get_item_id", return_value=(params.get("get_item_id")))
        f_module = self.get_module_mock(params=params.get("inp", {}))
        ioms = self.module.validate_ioms(f_module, ome_connection_mock_for_smart_fabric_uplink, params.get("uplinks"))
        assert ioms == params.get("ioms")

    @pytest.mark.parametrize("params", [{"inp": {"untagged_network": "vlan_name1"}, "success": True,
                                         "json_data": {
                                             "ApplicableUplinkNetworks": [{"Name": "vlan_name", "VlanMaximum": 123}]},
                                         "vlan_id": 123,
                                         "error_msg": "Native VLAN name vlan_name1 is not applicable or valid."}, ])
    def test_validate_native_vlan_failure(self, params, ome_connection_mock_for_smart_fabric_uplink, ome_response_mock):
        ome_response_mock.success = params["success"]
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params.get("inp", {}))
        error_message = params["error_msg"]
        with pytest.raises(Exception) as err:
            self.module.validate_native_vlan(f_module, ome_connection_mock_for_smart_fabric_uplink, 1, 2)
        assert err.value.args[0] == error_message

    @pytest.mark.parametrize("params", [{"inp": {"untagged_network": "vlan_name"}, "success": True, "json_data": {
        "ApplicableUplinkNetworks": [{"Name": "vlan_name", "VlanMaximum": 123}]}, "vlan_id": 123}, ])
    def test_validate_native_vlan_failure(self, params, ome_connection_mock_for_smart_fabric_uplink, ome_response_mock):
        ome_response_mock.success = params["success"]
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params.get("inp", {}))
        vlan_payload = self.module.validate_native_vlan(f_module, ome_connection_mock_for_smart_fabric_uplink, 1, 2)
        assert vlan_payload == params["vlan_id"]

    def test_delete_uplink(self, ome_connection_mock_for_smart_fabric_uplink, ome_response_mock):
        ome_response_mock.success = True
        ome_response_mock.json_data = {}
        f_module = self.get_module_mock(params={"fabric_name": "f1", "name": "uplink1"})
        with pytest.raises(Exception, match="Successfully deleted the uplink.") as err:
            self.module.delete_uplink(f_module, ome_connection_mock_for_smart_fabric_uplink, 12, 123)

    @pytest.mark.parametrize("params", [{"inp": {"fabric_name": "f1", "name": "uplink1"},
                                         "error_msg": "Mandatory parameter uplink_type not provided for uplink creation."},
                                        {"inp": {"fabric_name": "f1", "name": "uplink1", "uplink_type": "Ethernet"},
                                         "error_msg": "Mandatory parameter tagged_networks not provided for uplink creation."},
                                        {"inp": {"fabric_name": "f1", "name": "uplink1", "uplink_type": "FEthernet",
                                                 "tagged_networks": ["vlan1"]}, "get_item_id": (0, []),
                                         "error_msg": "Uplink Type FEthernet does not exist."}, {
                                            "inp": {"fabric_name": "f1", "name": "uplink1", "uplink_type": "Ethernet",
                                                    "tagged_networks": ["vlan1"]}, "get_item_id": (2, []),
                                            "error_msg": "Provide port details."}, {
                                            "inp": {"fabric_name": "f1", "name": "uplink1", "uplink_type": "Ethernet",
                                                    "tagged_networks": ["vlan1"],
                                                    "primary_switch_service_tag": "ABC123",
                                                    "secondary_switch_service_tag": "ABC123"}, "get_item_id": (2, []),
                                            "error_msg": "Primary and Secondary service tags must not be the same."}, {
                                            "inp": {"fabric_name": "f1", "name": "uplink1", "uplink_type": "Ethernet",
                                                    "tagged_networks": ["vlan1"],
                                                    "primary_switch_service_tag": "ABC123",
                                                    "secondary_switch_service_tag": "XYZ123"}, "get_item_id": (2, []),
                                            "validate_ioms": ["ST1:123", "ST2:345"], "validate_networks": [1, 2],
                                            "check_mode": True, "error_msg": "Changes found to be applied."}, {
                                            "inp": {"fabric_name": "f1", "name": "uplink1", "uplink_type": "Ethernet",
                                                    "tagged_networks": ["vlan1"],
                                                    "primary_switch_service_tag": "ABC123",
                                                    "secondary_switch_service_tag": "XYZ123"}, "get_item_id": (2, []),
                                            "validate_ioms": ["ST1:123", "ST2:345"], "validate_networks": [1, 2],
                                            "error_msg": "Successfully created the uplink."}, {
                                            "inp": {"fabric_name": "f1", "name": "uplink1", "uplink_type": "Ethernet",
                                                    "tagged_networks": ["vlan1"],
                                                    "primary_switch_service_tag": "ABC123",
                                                    "secondary_switch_service_tag": "XYZ123", "ufd_enable": "Enabled",
                                                    "description": "uplink description", "untagged_network": "vlan2"},
                                            "get_item_id": (2, []), "validate_ioms": ["ST1:123", "ST2:345"],
                                            "validate_networks": [1, 2], "validate_native_vlan": 1,
                                            "error_msg": "Successfully created the uplink."}, ])
    def test_create_uplink(self, mocker, params, ome_connection_mock_for_smart_fabric_uplink, ome_response_mock):
        f_module = self.get_module_mock(params=params.get("inp", {}), check_mode=params.get("check_mode", False))
        mocker.patch(MODULE_PATH + "get_item_id", return_value=(params.get("get_item_id")))
        mocker.patch(MODULE_PATH + "validate_ioms", return_value=(params.get("validate_ioms")))
        mocker.patch(MODULE_PATH + "validate_networks", return_value=(params.get("validate_networks")))
        mocker.patch(MODULE_PATH + "validate_native_vlan", return_value=(params.get("validate_native_vlan")))
        error_message = params["error_msg"]
        with pytest.raises(Exception) as err:
            self.module.create_uplink(f_module, ome_connection_mock_for_smart_fabric_uplink, params.get("fabric_id", 0),
                                      [])
        assert err.value.args[0] == error_message

    @pytest.mark.parametrize(
        "params", [{"inp": {"fabric_name": "f1", "name": "uplink1", "new_name": "uplink2",
                            "description": "modified from OMAM", "uplink_type": "Ethernet",
                            "ufd_enable": "Enabled", "untagged_network": "vlan2"},
                    "uplink_id": {"Id": "9cf5a5ee-aecc-45d1-a113-5c4055ab3b4c", "Name": "create1",
                                  "Description": "CREATED from OMAM",
                                  "MediaType": "Ethernet", "NativeVLAN": 0, "UfdEnable": "NA",
                                  "Ports": [{"Id": "2HBFNX2:ethernet1/1/14"}, {"Id": "2HB7NX2:ethernet1/1/13"}],
                                  "Networks": [{"Id": 36011}]},
                    "uplinks": [],
                    "get_item_id": (2, []), "validate_ioms": ["ST1:123", "ST2:345"],
                    "validate_networks": [1, 2], "validate_native_vlan": 1,
                    "error_msg": "Successfully modified the uplink."},
                   {"inp": {"fabric_name": "f1", "name": "uplink1", "new_name": "uplink2",
                            "description": "modified from OMAM", "uplink_type": "Ethernet",
                            "ufd_enable": "Enabled", "untagged_network": "vlan2"},
                    "uplink_id": {"Id": "9cf5a5ee-aecc-45d1-a113-5c4055ab3b4c", "Name": "create1",
                                  "Description": "CREATED from OMAM", "MediaType": "Ethernet", "NativeVLAN": 0,
                                  "UfdEnable": "NA",
                                  "Ports": [{"Id": "2HBFNX2:ethernet1/1/14"}, {"Id": "2HB7NX2:ethernet1/1/13"}],
                                  "Networks": [{"Id": 36011}]},
                    "uplinks": [], "get_item_id": (2, []),
                    "validate_ioms": ["ST1:123", "ST2:345"], "validate_networks": [1, 2], "validate_native_vlan": 1,
                    "check_mode": True, "error_msg": "Changes found to be applied."},
                   {"inp": {"fabric_name": "f1", "name": "uplink1", "new_name": "uplink2",
                            "uplink_type": "FEthernet"},
                    "uplink_id": {"Id": "9cf5a5ee-aecc-45d1-a113-5c4055ab3b4c", "Name": "create1",
                                  "Description": "CREATED from OMAM",
                                  "MediaType": "Ethernet", "NativeVLAN": 0, "UfdEnable": "NA",
                                  "Ports": [{"Id": "2HBFNX2:ethernet1/1/14"}, {"Id": "2HB7NX2:ethernet1/1/13"}],
                                  "Networks": [{"Id": 36011}]},
                    "uplinks": [], "get_item_id": (2, []),
                    "validate_ioms": ["ST1:123", "ST2:345"], "validate_networks": [1, 2],
                    "validate_native_vlan": 1, "error_msg": "Uplink Type cannot be modified."}, ])
    def test_modify_uplink(self, mocker, params, ome_connection_mock_for_smart_fabric_uplink, ome_response_mock):
        f_module = self.get_module_mock(params=params.get("inp", {}), check_mode=params.get("check_mode", False))
        mocker.patch(MODULE_PATH + "get_item_id", return_value=(params.get("get_item_id")))
        mocker.patch(MODULE_PATH + "validate_ioms", return_value=(params.get("validate_ioms")))
        mocker.patch(MODULE_PATH + "validate_networks", return_value=(params.get("validate_networks")))
        mocker.patch(MODULE_PATH + "validate_native_vlan", return_value=(params.get("validate_native_vlan")))
        error_message = params["error_msg"]
        with pytest.raises(Exception) as err:
            self.module.modify_uplink(f_module, ome_connection_mock_for_smart_fabric_uplink, params.get("fabric_id", 0),
                                      params.get("uplink_id", {}), params.get("uplinks", []))
        assert err.value.args[0] == error_message

    @pytest.mark.parametrize(
        "params", [{"inp": {"name": "uplink1", "fabric_name": "fabric1"},
                    "error_msg": "state is present but any of the following are missing: new_name, description,"
                                 " uplink_type, ufd_enable, primary_switch_service_tag, primary_switch_ports, "
                                 "secondary_switch_service_tag, secondary_switch_ports, tagged_networks, untagged_network"},
                   {"inp": {"name": "uplink1"},
                    "error_msg": "missing required arguments: fabric_name"},
                   {"inp": {"fabric_name": "fabric1"},
                    "error_msg": "missing required arguments: name"}, ])
    def test_main_case_failures(self, mocker, params, ome_default_args, ome_connection_mock_for_smart_fabric_uplink,
                                ome_response_mock):
        ome_default_args.update(params.get("inp"))
        ome_response_mock.json_data = params.get("json_data")
        mocker.patch(MODULE_PATH + "get_item_id", return_value=(params.get("get_item_id")))
        result = self._run_module_with_fail_json(ome_default_args)
        assert result['msg'] == params.get("error_msg")

    @pytest.mark.parametrize(
        "params", [{"inp": {"state": "absent", "name": "uplink1", "fabric_name": "fabric1", "ufd_enable": "Enabled"},
                    "get_item_id": (0, []), "error_msg": "Fabric with name fabric1 does not exist."},
                   {"inp": {"state": "absent", "name": "uplink1", "fabric_name": "fabric1", "ufd_enable": "Enabled"},
                    "get_item_id": (1, []),
                    "get_item_and_list": ({'Id': 1}, []), "error_msg": "Successfully deleted the uplink."},
                   {"inp": {"state": "absent", "name": "uplink1", "fabric_name": "fabric1", "ufd_enable": "Enabled"},
                    "get_item_id": (1, []),
                    "get_item_and_list": ({'Id': 1}, []), "check_mode": True,
                    "error_msg": "Changes found to be applied."}, ])
    def _test_main_case_failures2(self, mocker, params, ome_default_args, ome_connection_mock_for_smart_fabric_uplink,
                                  ome_response_mock):
        ome_default_args.update(params.get("inp"))
        ome_response_mock.json_data = params.get("json_data")
        mocker.patch(MODULE_PATH + "get_item_id", return_value=(params.get("get_item_id", (0, []))))
        mocker.patch(MODULE_PATH + "get_item_and_list", return_value=(params.get("get_item_and_list")))
        result = self.execute_module(ome_default_args, check_mode=params.get("check_mode", False))
        assert result['msg'] == params.get("error_msg")

    @pytest.mark.parametrize("params", [
        {"fail_json": True, "json_data": {"JobId": 1234},
         "get_item_id": (0, []),
         "mparams": {"state": "absent", "name": "uplink1", "fabric_name": "fabric1", "ufd_enable": "Enabled"},
         'message': "Fabric with name fabric1 does not exist.", "success": True
         },
        {"fail_json": False, "json_data": {"JobId": 1234},
         "get_item_id": (1, []), "get_item_and_list": ({}, []), "check_mode": True,
         "mparams": {"state": "absent", "name": "uplink1", "fabric_name": "fabric1", "ufd_enable": "Enabled"},
         'message': "No changes found to be applied to the uplink configuration.", "success": True
         },
        {"fail_json": False, "json_data": {"JobId": 1234},
         "get_item_id": (1, []), "get_item_and_list": ({}, []), "check_mode": False,
         "mparams": {"state": "absent", "name": "uplink1", "fabric_name": "fabric1", "ufd_enable": "Enabled"},
         'message': "Uplink uplink1 does not exist.", "success": True
         },
        {"fail_json": False, "json_data": {"JobId": 1234},
         "get_item_id": (1, []), "get_item_and_list": ({"Name": 'u1', 'Id': 12}, []), "check_mode": True,
         "mparams": {"state": "absent", "name": "uplink1", "fabric_name": "fabric1", "ufd_enable": "Enabled"},
         'message': "Changes found to be applied.", "success": True
         },
        {"fail_json": True, "json_data": {"JobId": 1234},
         "get_item_id": (1, []), "get_item_and_list":
             ({"Id": "12", "Name": "u1", "Description": "Ethernet_Uplink", "NativeVLAN": 1, "UfdEnable": "NA",
               "Ports": [{"Id": "2HB7NX2:ethernet1/1/13", "Name": ""},
                         {"Id": "2HB7NX2:ethernet1/1/12", "Name": ""}],
               "Networks": [{"Id": 31554, "Name": "VLAN2", }]},
              [{"Id": "12", "Name": "u1", "Description": "Ethernet_Uplink", "NativeVLAN": 1, "UfdEnable": "NA",
                "Ports": [{"Id": "2HB7NX2:ethernet1/1/13", "Name": "", },
                          {"Id": "2HB7NX2:ethernet1/1/12", "Name": "", }],
                "Networks": [{"Id": 31554, "Name": "VLAN2", }]},
               {"Name": 'u2', 'Id': 13}]),
         "mparams": {"state": "present", "name": "u1", "fabric_name": "fabric1",
                     "primary_switch_service_tag": "SVTAG1", "primary_switch_ports": [1, 2],
                     "secondary_switch_service_tag": 'SVTAG1', "secondary_switch_ports": [1, 2]},
         'message': "Primary and Secondary service tags must not be the same.", "success": True
         },
        {"fail_json": False, "json_data": {"JobId": 1234},
         "get_item_id": (1, []), "get_item_and_list":
             ({}, [{"Id": "12", "Name": "u1", "Description": "Ethernet_Uplink", "NativeVLAN": 1,
                    "UfdEnable": "NA", "Ports": [{"Id": "2HB7NX2:ethernet1/1/13", "Name": "", },
                                                 {"Id": "2HB7NX2:ethernet1/1/12", "Name": "", }],
                    "Networks": [{"Id": 31554, "Name": "VLAN2", }]}, {"Name": 'u2', 'Id': 13}]),
         "validate_networks": ['a', 'b'], "validate_ioms": ['a', 'b'],
         "mparams": {"state": "present", "name": "u1", "fabric_name": "fabric1", "uplink_type": 'Ethernet',
                     "tagged_networks": ['a', 'b'],
                     "primary_switch_service_tag": "SVTAG1", "primary_switch_ports": [1, 2],
                     "secondary_switch_service_tag": 'SVTAG2', "secondary_switch_ports": [1, 2]},
         'message': "Successfully created the uplink.", "success": True
         },
        {"fail_json": False, "json_data": {"JobId": 1234},
         "get_item_id": (1, []), "get_item_and_list":
             ({"Id": "12", "Name": "u1", "Description": "Ethernet_Uplink", "NativeVLAN": 1, "UfdEnable": "NA",
               "Ports": [{"Id": "2HB7NX2:ethernet1/1/13", "Name": "", },
                         {"Id": "2HB7NX2:ethernet1/1/12", "Name": "", }],
               "Networks": [{"Id": 31554, "Name": "VLAN2", }]},
              [{"Id": "12", "Name": "u1", "Description": "Ethernet_Uplink", "NativeVLAN": 1,
                "UfdEnable": "NA", "Ports": [{"Id": "2HB7NX2:ethernet1/1/13", "Name": "", },
                                             {"Id": "2HB7NX2:ethernet1/1/12", "Name": "", }],
                "Networks": [{"Id": 31554, "Name": "VLAN2", }]}, {"Name": 'u2', 'Id': 13}]),
         "validate_networks": ['a', 'b'], "validate_ioms": ['a', 'b'],
         "mparams": {"state": "present", "name": "u1", "fabric_name": "fabric1",
                     "tagged_networks": ['a', 'b'],
                     "primary_switch_service_tag": "SVTAG1", "primary_switch_ports": [1, 2],
                     "secondary_switch_service_tag": 'SVTAG2', "secondary_switch_ports": [1, 2]},
         'message': "Successfully modified the uplink.", "success": True
         },
    ])
    def test_main(self, params, ome_connection_mock_for_smart_fabric_uplink, ome_default_args, ome_response_mock,
                  mocker):
        mocker.patch(MODULE_PATH + 'get_item_id', return_value=params.get("get_item_id"))
        mocker.patch(MODULE_PATH + 'get_item_and_list', return_value=params.get("get_item_and_list"))
        mocker.patch(MODULE_PATH + 'validate_networks', return_value=params.get("validate_networks"))
        mocker.patch(MODULE_PATH + 'validate_ioms', return_value=params.get("validate_ioms"))
        ome_response_mock.success = True
        ome_response_mock.json_data = params.get("json_data")
        ome_default_args.update(params.get('mparams'))
        if params.get("fail_json", False):
            result = self._run_module_with_fail_json(ome_default_args)
        else:
            result = self._run_module(ome_default_args, check_mode=params.get("check_mode", False))
        assert result["msg"] == params['message']

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_smart_fabric_uplink_main_exception_failure_case(self, exc_type, mocker, ome_default_args,
                                                                 ome_connection_mock_for_smart_fabric_uplink,
                                                                 ome_response_mock):
        ome_default_args.update({"name": "uplink1", "state": "present", "fabric_name": "f1", "new_name": "uplink2"})
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'get_item_id', side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'get_item_id', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'get_item_id',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'uplink_id' not in result
        assert 'msg' in result
