# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.2.0
# Copyright (C) 2022-2023 Dell Inc. or its subsidiaries. All Rights Reserved.

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
from ansible_collections.dellemc.openmanage.plugins.modules import ome_smart_fabric_uplink_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_smart_fabric_uplink_info.'


@pytest.fixture
def ome_connection_mock_for_smart_fabric_uplink_info(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeSmartFabricUplinkInfo(FakeAnsibleModule):
    module = ome_smart_fabric_uplink_info

    uplink_info = [{
        "Description": "",
        "Id": "1ad54420-b145-49a1-9779-21a579ef6f2d",
        "MediaType": "Ethernet",
        "Name": "u1",
        "NativeVLAN": 1,
        "Networks": [{
            "CreatedBy": "system",
            "CreationTime": "2018-09-25 14:46:12.374",
            "Description": "null",
            "Id": 10155,
            "InternalRefNWUUId": "f15a36b6-e3d3-46b2-9e7d-bf9cd66e180d",
            "Name": "testvlan",
            "Type": 1,
            "UpdatedBy": "root",
            "UpdatedTime": "2019-06-27 15:06:22.836",
            "VlanMaximum": 143,
            "VlanMinimum": 143
        }],
        "Ports": [{
            "AdminStatus": "Enabled",
            "BlinkStatus": "OFF",
            "ConfiguredSpeed": "0",
            "CurrentSpeed": "0",
            "Description": "",
            "Id": "SVCTAG1:ethernet1/1/35",
            "MaxSpeed": "0",
            "MediaType": "Ethernet",
            "Name": "",
            "NodeServiceTag": "SVCTAG1",
            "OpticsType": "NotPresent",
            "PortNumber": "ethernet1/1/35",
            "Role": "Uplink",
            "Status": "Down",
            "Type": "PhysicalEthernet"
        }, {
            "AdminStatus": "Enabled",
            "BlinkStatus": "OFF",
            "ConfiguredSpeed": "0",
            "CurrentSpeed": "0",
            "Description": "",
            "Id": "SVCTAG1:ethernet1/1/35",
            "MaxSpeed": "0",
            "MediaType": "Ethernet",
            "Name": "",
            "NodeServiceTag": "SVCTAG1",
            "OpticsType": "NotPresent",
            "PortNumber": "ethernet1/1/35",
            "Role": "Uplink",
            "Status": "Down",
            "Type": "PhysicalEthernet"
        }],
        "Summary": {
            "NetworkCount": 1,
            "PortCount": 2
        },
        "UfdEnable": "Disabled"
    }]

    @pytest.mark.parametrize("params", [{"success": True,
                                         "json_data": {"value": [{
                                             "Id": "1ad54420-b145-49a1-9779-21a579ef6f2d",
                                             "Name": "u1",
                                             "Description": "",
                                             "MediaType": "Ethernet",
                                             "NativeVLAN": 1,
                                             "Summary": {"PortCount": 2,
                                                         "NetworkCount": 1
                                                         },
                                             "UfdEnable": "Disabled",
                                             "Ports@odata.count": 2,
                                             "Ports": [{
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": "",
                                                 "Type": "PhysicalEthernet",
                                                 "MediaType": "Ethernet",
                                                 "NodeServiceTag": "SVCTAG1",
                                                 "PortNumber": "ethernet1/1/35",
                                                 "Status": "Down",
                                                 "AdminStatus": "Enabled",
                                                 "CurrentSpeed": "0",
                                                 "MaxSpeed": "0",
                                                 "ConfiguredSpeed": "0",
                                                 "OpticsType": "NotPresent",
                                                 "BlinkStatus": "OFF",
                                                 "Role": "Uplink"
                                             }, {
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": "",
                                                 "Type": "PhysicalEthernet",
                                                 "MediaType": "Ethernet",
                                                 "NodeServiceTag": "SVCTAG1",
                                                 "PortNumber": "ethernet1/1/35",
                                                 "Status": "Down",
                                                 "AdminStatus": "Enabled",
                                                 "CurrentSpeed": "0",
                                                 "MaxSpeed": "0",
                                                 "ConfiguredSpeed": "0",
                                                 "OpticsType": "NotPresent",
                                                 "BlinkStatus": "OFF",
                                                 "Role": "Uplink"
                                             }],
                                             "Networks@odata.count": 1,
                                             "Networks": [{
                                                 "Id": 10155,
                                                 "Name": "testvlan",
                                                 "Description": "null",
                                                 "VlanMaximum": 143,
                                                 "VlanMinimum": 143,
                                                 "Type": 1,
                                                 "CreatedBy": "system",
                                                 "CreationTime": "2018-09-25 14:46:12.374",
                                                 "UpdatedBy": "root",
                                                 "UpdatedTime": "2019-06-27 15:06:22.836",
                                                 "InternalRefNWUUId": "f15a36b6-e3d3-46b2-9e7d-bf9cd66e180d"
                                             }]
                                         }]
                                         },
                                         "fabric_id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2",
                                         "uplink_id": "1ad54420-b145-49a1-9779-21a579ef6f2d"}])
    def test_uplink_details_from_fabric_id(self, params, ome_connection_mock_for_smart_fabric_uplink_info, ome_response_mock):
        ome_response_mock.success = params["success"]
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params.get("fabric_id"))
        resp = self.module.get_uplink_details_from_fabric_id(f_module, ome_connection_mock_for_smart_fabric_uplink_info,
                                                             params.get("fabric_id"))
        assert resp[0]["Id"] == params["uplink_id"]

    @pytest.mark.parametrize("params", [{"success": True,
                                         "json_data": {"value": [{
                                             "Id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2",
                                             "Name": "f1",
                                             "Description": "Fabric f1",
                                             "OverrideLLDPConfiguration": "Disabled",
                                             "ScaleVLANProfile": "Enabled",
                                             "Summary": {
                                                 "NodeCount": 2,
                                                 "ServerCount": 1,
                                                 "UplinkCount": 1
                                             },
                                             "LifeCycleStatus": [{
                                                 "Activity": "Create",
                                                 "Status": "2060"
                                             }],
                                             "FabricDesignMapping": [{
                                                 "DesignNode": "Switch-A",
                                                 "PhysicalNode": "SVCTAG1"
                                             }, {
                                                 "DesignNode": "Switch-B",
                                                 "PhysicalNode": "SVCTAG1"
                                             }],
                                             "Actions": "null",
                                         }]},
                                         "fabric_name": "f1",
                                         "fabric_id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2"
                                         }]
                             )
    def test_get_fabric_name_details(self, params, ome_connection_mock_for_smart_fabric_uplink_info,
                                     ome_response_mock):
        ome_response_mock.success = params["success"]
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params.get("fabric_name"))
        fabric_id = self.module.get_fabric_id_from_name(f_module, ome_connection_mock_for_smart_fabric_uplink_info,
                                                        params.get("fabric_name"))
        assert fabric_id == params["fabric_id"]

    @pytest.mark.parametrize("params", [{"inp": {"fabric_id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2", "uplink_id": "1ad54420-b145-49a1-9779-21a579ef6f2d"},
                                         "success": True,
                                         "json_data": {
                                             "Id": "1ad54420-b145-49a1-9779-21a579ef6f2d",
                                             "Name": "u1",
                                             "Description": "",
                                             "MediaType": "Ethernet",
                                             "NativeVLAN": 1,
                                             "Summary": {
                                                 "PortCount": 2,
                                                 "NetworkCount": 1
                                             },
                                             "UfdEnable": "Disabled",
                                             "Ports@odata.count": 2,
                                             "Ports": [{
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": "",
                                                 "Type": "PhysicalEthernet",
                                                 "MediaType": "Ethernet",
                                                 "NodeServiceTag": "SVCTAG1",
                                                 "PortNumber": "ethernet1/1/35",
                                                 "Status": "Down",
                                                 "AdminStatus": "Enabled",
                                                 "CurrentSpeed": "0",
                                                 "MaxSpeed": "0",
                                                 "ConfiguredSpeed": "0",
                                                 "OpticsType": "NotPresent",
                                                 "BlinkStatus": "OFF",
                                                 "Role": "Uplink"
                                             }, {
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": "",
                                                 "Type": "PhysicalEthernet",
                                                 "MediaType": "Ethernet",
                                                 "NodeServiceTag": "SVCTAG1",
                                                 "PortNumber": "ethernet1/1/35",
                                                 "Status": "Down",
                                                 "AdminStatus": "Enabled",
                                                 "CurrentSpeed": "0",
                                                 "MaxSpeed": "0",
                                                 "ConfiguredSpeed": "0",
                                                 "OpticsType": "NotPresent",
                                                 "BlinkStatus": "OFF",
                                                 "Role": "Uplink"
                                             }],
                                             "Networks@odata.count": 1,
                                             "Networks": [{
                                                 "Id": 10155,
                                                 "Name": "testvlan",
                                                 "Description": "null",
                                                 "VlanMaximum": 143,
                                                 "VlanMinimum": 143,
                                                 "Type": 1,
                                                 "CreatedBy": "system",
                                                 "CreationTime": "2018-09-25 14:46:12.374",
                                                 "UpdatedBy": "root",
                                                 "UpdatedTime": "2019-06-27 15:06:22.836",
                                                 "InternalRefNWUUId": "f15a36b6-e3d3-46b2-9e7d-bf9cd66e180d"
                                             }]},
                                         "uplink_id": "1ad54420-b145-49a1-9779-21a579ef6f2d",
                                         "fabric_id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2"
                                         }]
                             )
    def test_get_uplink_details(self, params, ome_connection_mock_for_smart_fabric_uplink_info,
                                ome_response_mock):
        ome_response_mock.success = params["success"]
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params.get("inp", {}))
        resp = self.module.get_uplink_details(f_module, ome_connection_mock_for_smart_fabric_uplink_info,
                                              params.get("fabric_id"), params.get("uplink_id"))
        assert resp[0]["Id"] == params["uplink_id"]

    @pytest.mark.parametrize("params", [{"inp": {"fabric_id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2"},
                                         "success": True,
                                         "json_data": {
                                             "value": [{
                                                 "Id": "1ad54420-b145-49a1-9779-21a579ef6f2d",
                                                 "Name": "u1",
                                                 "Description": "",
                                                 "MediaType": "Ethernet",
                                                 "NativeVLAN": 1,
                                                 "Summary": {
                                                     "PortCount": 2,
                                                     "NetworkCount": 1
                                                 },
                                                 "UfdEnable": "Disabled",
                                                 "Ports@odata.count": 2,
                                                 "Ports": [{
                                                     "Id": "SVCTAG1:ethernet1/1/35",
                                                     "Name": "",
                                                     "Description": "",
                                                     "Type": "PhysicalEthernet",
                                                     "MediaType": "Ethernet",
                                                     "NodeServiceTag": "SVCTAG1",
                                                     "PortNumber": "ethernet1/1/35",
                                                     "Status": "Down",
                                                     "AdminStatus": "Enabled",
                                                     "CurrentSpeed": "0",
                                                     "MaxSpeed": "0",
                                                     "ConfiguredSpeed": "0",
                                                     "OpticsType": "NotPresent",
                                                     "BlinkStatus": "OFF",
                                                     "Role": "Uplink"
                                                 }, {
                                                     "Id": "SVCTAG1:ethernet1/1/35",
                                                     "Name": "",
                                                     "Description": "",
                                                     "Type": "PhysicalEthernet",
                                                     "MediaType": "Ethernet",
                                                     "NodeServiceTag": "SVCTAG1",
                                                     "PortNumber": "ethernet1/1/35",
                                                     "Status": "Down",
                                                     "AdminStatus": "Enabled",
                                                     "CurrentSpeed": "0",
                                                     "MaxSpeed": "0",
                                                     "ConfiguredSpeed": "0",
                                                     "OpticsType": "NotPresent",
                                                     "BlinkStatus": "OFF",
                                                     "Role": "Uplink"
                                                 }],
                                                 "Networks@odata.count": 1,
                                                 "Networks": [{
                                                     "Id": 10155,
                                                     "Name": "testvlan",
                                                     "Description": "null",
                                                     "VlanMaximum": 143,
                                                     "VlanMinimum": 143,
                                                     "Type": 1,
                                                     "CreatedBy": "system",
                                                     "CreationTime": "2018-09-25 14:46:12.374",
                                                     "UpdatedBy": "root",
                                                     "UpdatedTime": "2019-06-27 15:06:22.836",
                                                     "InternalRefNWUUId": "f15a36b6-e3d3-46b2-9e7d-bf9cd66e180d"
                                                 }]
                                             }]},
                                         "uplink_name": "u1",
                                         "fabric_id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2",
                                         "uplink_id": "1ad54420-b145-49a1-9779-21a579ef6f2d"
                                         }]
                             )
    def test_get_uplink_name_details(self, params, ome_connection_mock_for_smart_fabric_uplink_info,
                                     ome_response_mock):
        ome_response_mock.success = params["success"]
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params.get("inp", {}))
        uplink_id = self.module.get_uplink_id_from_name(f_module, ome_connection_mock_for_smart_fabric_uplink_info,
                                                        params.get("uplink_name"), params.get("fabric_id"))
        assert uplink_id == params["uplink_id"]

    @pytest.mark.parametrize("params", [{"success": True,
                                         "mparams": {"fabric_id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f"},
                                         "msg": "Successfully retrieved the fabric uplink information.",
                                         "get_uplink_details_from_fabric_id": {"value": [{
                                             "Id": "1ad54420-b145-49a1-9779-21a579ef6f2d",
                                             "Name": "u1",
                                             "Description": "",
                                             "MediaType": "Ethernet",
                                             "NativeVLAN": 1,
                                             "Summary": {
                                                 "PortCount": 2,
                                                 "NetworkCount": 1
                                             },
                                             "UfdEnable": "Disabled",
                                             "Ports@odata.count": 2,
                                             "Ports": [{
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": "",
                                                 "Type": "PhysicalEthernet",
                                                 "MediaType": "Ethernet",
                                                 "NodeServiceTag": "SVCTAG1",
                                                 "PortNumber": "ethernet1/1/35",
                                                 "Status": "Down",
                                                 "AdminStatus": "Enabled",
                                                 "CurrentSpeed": "0",
                                                 "MaxSpeed": "0",
                                                 "ConfiguredSpeed": "0",
                                                 "OpticsType": "NotPresent",
                                                 "BlinkStatus": "OFF",
                                                 "Role": "Uplink"
                                             }, {
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": "",
                                                 "Type": "PhysicalEthernet",
                                                 "MediaType": "Ethernet",
                                                 "NodeServiceTag": "SVCTAG1",
                                                 "PortNumber": "ethernet1/1/35",
                                                 "Status": "Down",
                                                 "AdminStatus": "Enabled",
                                                 "CurrentSpeed": "0",
                                                 "MaxSpeed": "0",
                                                 "ConfiguredSpeed": "0",
                                                 "OpticsType": "NotPresent",
                                                 "BlinkStatus": "OFF",
                                                 "Role": "Uplink"
                                             }],
                                             "Networks@odata.count": 1,
                                             "Networks": [{
                                                 "Id": 10155,
                                                 "Name": "testvlan",
                                                 "Description": "null",
                                                 "VlanMaximum": 143,
                                                 "VlanMinimum": 143,
                                                 "Type": 1,
                                                 "CreatedBy": "system",
                                                 "CreationTime": "2018-09-25 14:46:12.374",
                                                 "UpdatedBy": "root",
                                                 "UpdatedTime": "2019-06-27 15:06:22.836",
                                                 "InternalRefNWUUId": "f15a36b6-e3d3-46b2-9e7d-bf9cd66e180d"
                                             }]
                                         }]}
                                         }, {"success": False,
                                             "mparams": {"fabric_id": "f1"},
                                             "msg": "Unable to retrieve smart fabric uplink information.",
                                             "get_uplink_details_from_fabric_id": {}},
                                        ]
                             )
    def test_main_case_success_all(self, params, ome_connection_mock_for_smart_fabric_uplink_info, ome_default_args, ome_response_mock,
                                   mocker):
        mocker.patch(MODULE_PATH + 'get_uplink_details_from_fabric_id',
                     return_value=params.get("get_uplink_details_from_fabric_id"))
        mocker.patch(MODULE_PATH + 'strip_uplink_info',
                     return_value=params.get("get_uplink_details_from_fabric_id"))
        ome_response_mock.success = True
        ome_response_mock.json_data = params.get("strip_uplink_info")
        ome_default_args.update(params.get('mparams'))
        result = self._run_module(ome_default_args)
        assert result["msg"] == 'Successfully retrieved the fabric uplink information.'

    def test_ome_smart_fabric_main_success_case_fabric_id(self, mocker, ome_default_args, ome_connection_mock_for_smart_fabric_uplink_info,
                                                          ome_response_mock):
        ome_default_args.update({"fabric_id": "1"})
        ome_response_mock.success = True
        ome_response_mock.json_data = {"value": [{"fabric_id": "1"}]}
        ome_response_mock.status_code = 200
        mocker.patch(
            MODULE_PATH + 'strip_uplink_info',
            return_value=self.uplink_info)
        result = self._run_module(ome_default_args)
        assert 'uplink_info' in result
        assert result['msg'] == "Successfully retrieved the fabric uplink information."

    @pytest.mark.parametrize("params", [{"success": True,
                                         "json_data": {"value": [{
                                             "Id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2",
                                             "Name": "f1",
                                             "Description": "Fabric f1",
                                             "OverrideLLDPConfiguration": "Disabled",
                                             "ScaleVLANProfile": "Enabled",
                                             "Summary": {
                                                 "NodeCount": 2,
                                                 "ServerCount": 1,
                                                 "UplinkCount": 1
                                             },
                                             "LifeCycleStatus": [{
                                                 "Activity": "Create",
                                                 "Status": "2060"
                                             }],
                                             "FabricDesignMapping": [{
                                                 "DesignNode": "Switch-A",
                                                 "PhysicalNode": "SVCTAG1"
                                             }, {
                                                 "DesignNode": "Switch-B",
                                                 "PhysicalNode": "SVCTAG1"
                                             }],
                                             "Actions": "null",
                                         }]},
                                         "fabric_name": "f1",
                                         "fabric_id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2"
                                         }]
                             )
    def test_ome_smart_fabric_main_success_case_fabric_name(self, params, mocker, ome_default_args, ome_connection_mock_for_smart_fabric_uplink_info,
                                                            ome_response_mock):
        ome_default_args.update({"fabric_name": "f1"})
        ome_response_mock.success = True
        ome_response_mock.json_data = params["json_data"]
        ome_response_mock.status_code = 200
        mocker.patch(
            MODULE_PATH + 'strip_uplink_info',
            return_value=self.uplink_info)
        result = self._run_module(ome_default_args)
        assert 'uplink_info' in result
        assert result['msg'] == "Successfully retrieved the fabric uplink information."

    @pytest.mark.parametrize("params", [{"inp": {"fabric_id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2", "uplink_id": "1ad54420-b145-49a1-9779-21a579ef6f2d"},
                                         "success": True,
                                         "json_data": {
                                             "Id": "1ad54420-b145-49a1-9779-21a579ef6f2d",
                                             "Name": "u1",
                                             "Description": "",
                                             "MediaType": "Ethernet",
                                             "NativeVLAN": 1,
                                             "Summary": {
                                                 "PortCount": 2,
                                                 "NetworkCount": 1
                                             },
                                             "UfdEnable": "Disabled",
                                             "Ports@odata.count": 2,
                                             "Ports": [{
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": "",
                                                 "Type": "PhysicalEthernet",
                                                 "MediaType": "Ethernet",
                                                 "NodeServiceTag": "SVCTAG1",
                                                 "PortNumber": "ethernet1/1/35",
                                                 "Status": "Down",
                                                 "AdminStatus": "Enabled",
                                                 "CurrentSpeed": "0",
                                                 "MaxSpeed": "0",
                                                 "ConfiguredSpeed": "0",
                                                 "OpticsType": "NotPresent",
                                                 "BlinkStatus": "OFF",
                                                 "Role": "Uplink"
                                             }, {
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": "",
                                                 "Type": "PhysicalEthernet",
                                                 "MediaType": "Ethernet",
                                                 "NodeServiceTag": "SVCTAG1",
                                                 "PortNumber": "ethernet1/1/35",
                                                 "Status": "Down",
                                                 "AdminStatus": "Enabled",
                                                 "CurrentSpeed": "0",
                                                 "MaxSpeed": "0",
                                                 "ConfiguredSpeed": "0",
                                                 "OpticsType": "NotPresent",
                                                 "BlinkStatus": "OFF",
                                                 "Role": "Uplink"
                                             }],
                                             "Networks@odata.count": 1,
                                             "Networks": [{
                                                 "Id": 10155,
                                                 "Name": "testvlan",
                                                 "Description": "null",
                                                 "VlanMaximum": 143,
                                                 "VlanMinimum": 143,
                                                 "Type": 1,
                                                 "CreatedBy": "system",
                                                 "CreationTime": "2018-09-25 14:46:12.374",
                                                 "UpdatedBy": "root",
                                                 "UpdatedTime": "2019-06-27 15:06:22.836",
                                                 "InternalRefNWUUId": "f15a36b6-e3d3-46b2-9e7d-bf9cd66e180d"
                                             }]},
                                         "uplink_id": "1ad54420-b145-49a1-9779-21a579ef6f2d",
                                         "fabric_id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2"
                                         }]
                             )
    def test_ome_smart_fabric_main_failure_case_uplink_id(self, params, mocker, ome_default_args, ome_connection_mock_for_smart_fabric_uplink_info,
                                                          ome_response_mock):
        ome_default_args.update({"uplink_id": "u1"})
        ome_response_mock.success = True
        ome_response_mock.json_data = params["json_data"]
        ome_response_mock.status_code = 200
        mocker.patch(
            MODULE_PATH + 'strip_uplink_info',
            return_value=self.uplink_info)
        result = self._run_module(ome_default_args)
        assert result['msg'] == "fabric_id or fabric_name is required along with uplink_id."

    @pytest.mark.parametrize("params", [{"inp": {"fabric_id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2", "uplink_id": "1ad54420-b145-49a1-9779-21a579ef6f2d"},
                                         "success": True,
                                         "json_data": {
                                             "Id": "1ad54420-b145-49a1-9779-21a579ef6f2d",
                                             "Name": "u1",
                                             "Description": "",
                                             "MediaType": "Ethernet",
                                             "NativeVLAN": 1,
                                             "Summary": {
                                                 "PortCount": 2,
                                                 "NetworkCount": 1
                                             },
                                             "UfdEnable": "Disabled",
                                             "Ports@odata.count": 2,
                                             "Ports": [{
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": "",
                                                 "Type": "PhysicalEthernet",
                                                 "MediaType": "Ethernet",
                                                 "NodeServiceTag": "SVCTAG1",
                                                 "PortNumber": "ethernet1/1/35",
                                                 "Status": "Down",
                                                 "AdminStatus": "Enabled",
                                                 "CurrentSpeed": "0",
                                                 "MaxSpeed": "0",
                                                 "ConfiguredSpeed": "0",
                                                 "OpticsType": "NotPresent",
                                                 "BlinkStatus": "OFF",
                                                 "Role": "Uplink"
                                             }, {
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": "",
                                                 "Type": "PhysicalEthernet",
                                                 "MediaType": "Ethernet",
                                                 "NodeServiceTag": "SVCTAG1",
                                                 "PortNumber": "ethernet1/1/35",
                                                 "Status": "Down",
                                                 "AdminStatus": "Enabled",
                                                 "CurrentSpeed": "0",
                                                 "MaxSpeed": "0",
                                                 "ConfiguredSpeed": "0",
                                                 "OpticsType": "NotPresent",
                                                 "BlinkStatus": "OFF",
                                                 "Role": "Uplink"
                                             }],
                                             "Networks@odata.count": 1,
                                             "Networks": [{
                                                 "Id": 10155,
                                                 "Name": "testvlan",
                                                 "Description": "null",
                                                 "VlanMaximum": 143,
                                                 "VlanMinimum": 143,
                                                 "Type": 1,
                                                 "CreatedBy": "system",
                                                 "CreationTime": "2018-09-25 14:46:12.374",
                                                 "UpdatedBy": "root",
                                                 "UpdatedTime": "2019-06-27 15:06:22.836",
                                                 "InternalRefNWUUId": "f15a36b6-e3d3-46b2-9e7d-bf9cd66e180d"
                                             }]},
                                         "uplink_id": "1ad54420-b145-49a1-9779-21a579ef6f2d",
                                         "fabric_id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2"
                                         }]
                             )
    def test_ome_smart_fabric_main_success_case_uplink_id(self, params, mocker, ome_default_args, ome_connection_mock_for_smart_fabric_uplink_info,
                                                          ome_response_mock):
        ome_default_args.update({"fabric_id": "f1", "uplink_id": "u1"})
        ome_response_mock.success = True
        ome_response_mock.json_data = params["json_data"]
        ome_response_mock.status_code = 200
        mocker.patch(
            MODULE_PATH + 'strip_uplink_info',
            return_value=self.uplink_info)
        result = self._run_module(ome_default_args)
        assert 'uplink_info' in result
        assert result['msg'] == "Successfully retrieved the fabric uplink information."

    @pytest.mark.parametrize("params", [{"inp": {"fabric_id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2", "uplink_id": "1ad54420-b145-49a1-9779-21a579ef6f2d"},
                                         "success": True,
                                         "json_data": {
                                             "Id": "1ad54420-b145-49a1-9779-21a579ef6f2d",
                                             "Name": "u1",
                                             "Description": "",
                                             "MediaType": "Ethernet",
                                             "NativeVLAN": 1,
                                             "Summary": {
                                                 "PortCount": 2,
                                                 "NetworkCount": 1
                                             },
                                             "UfdEnable": "Disabled",
                                             "Ports@odata.count": 2,
                                             "Ports": [{
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": "",
                                                 "Type": "PhysicalEthernet",
                                                 "MediaType": "Ethernet",
                                                 "NodeServiceTag": "SVCTAG1",
                                                 "PortNumber": "ethernet1/1/35",
                                                 "Status": "Down",
                                                 "AdminStatus": "Enabled",
                                                 "CurrentSpeed": "0",
                                                 "MaxSpeed": "0",
                                                 "ConfiguredSpeed": "0",
                                                 "OpticsType": "NotPresent",
                                                 "BlinkStatus": "OFF",
                                                 "Role": "Uplink"
                                             }, {
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": "",
                                                 "Type": "PhysicalEthernet",
                                                 "MediaType": "Ethernet",
                                                 "NodeServiceTag": "SVCTAG1",
                                                 "PortNumber": "ethernet1/1/35",
                                                 "Status": "Down",
                                                 "AdminStatus": "Enabled",
                                                 "CurrentSpeed": "0",
                                                 "MaxSpeed": "0",
                                                 "ConfiguredSpeed": "0",
                                                 "OpticsType": "NotPresent",
                                                 "BlinkStatus": "OFF",
                                                 "Role": "Uplink"
                                             }],
                                             "Networks@odata.count": 1,
                                             "Networks": [{
                                                 "Id": 10155,
                                                 "Name": "testvlan",
                                                 "Description": "null",
                                                 "VlanMaximum": 143,
                                                 "VlanMinimum": 143,
                                                 "Type": 1,
                                                 "CreatedBy": "system",
                                                 "CreationTime": "2018-09-25 14:46:12.374",
                                                 "UpdatedBy": "root",
                                                 "UpdatedTime": "2019-06-27 15:06:22.836",
                                                 "InternalRefNWUUId": "f15a36b6-e3d3-46b2-9e7d-bf9cd66e180d"
                                             }]},
                                         "uplink_id": "1ad54420-b145-49a1-9779-21a579ef6f2d",
                                         "fabric_id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2"
                                         }]
                             )
    def test_ome_smart_fabric_main_failure_case_uplink_name(self, params, mocker, ome_default_args, ome_connection_mock_for_smart_fabric_uplink_info,
                                                            ome_response_mock):
        ome_default_args.update({"uplink_name": "u1"})
        ome_response_mock.success = True
        ome_response_mock.json_data = params["json_data"]
        ome_response_mock.status_code = 200
        mocker.patch(
            MODULE_PATH + 'strip_uplink_info',
            return_value=self.uplink_info)
        result = self._run_module(ome_default_args)
        assert result['msg'] == "fabric_id or fabric_name is required along with uplink_name."

    @pytest.mark.parametrize("params", [{"success": True,
                                         "json_data": {"value": [{
                                             "Id": "1ad54420-b145-49a1-9779-21a579ef6f2d",
                                             "Name": "u1",
                                             "Description": "",
                                             "MediaType": "Ethernet",
                                             "NativeVLAN": 1,
                                             "Summary": {"PortCount": 2,
                                                         "NetworkCount": 1
                                                         },
                                             "UfdEnable": "Disabled",
                                             "Ports@odata.count": 2,
                                             "Ports": [{
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": "",
                                                 "Type": "PhysicalEthernet",
                                                 "MediaType": "Ethernet",
                                                 "NodeServiceTag": "SVCTAG1",
                                                 "PortNumber": "ethernet1/1/35",
                                                 "Status": "Down",
                                                 "AdminStatus": "Enabled",
                                                 "CurrentSpeed": "0",
                                                 "MaxSpeed": "0",
                                                 "ConfiguredSpeed": "0",
                                                 "OpticsType": "NotPresent",
                                                 "BlinkStatus": "OFF",
                                                 "Role": "Uplink"
                                             }, {
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": "",
                                                 "Type": "PhysicalEthernet",
                                                 "MediaType": "Ethernet",
                                                 "NodeServiceTag": "SVCTAG1",
                                                 "PortNumber": "ethernet1/1/35",
                                                 "Status": "Down",
                                                 "AdminStatus": "Enabled",
                                                 "CurrentSpeed": "0",
                                                 "MaxSpeed": "0",
                                                 "ConfiguredSpeed": "0",
                                                 "OpticsType": "NotPresent",
                                                 "BlinkStatus": "OFF",
                                                 "Role": "Uplink"
                                             }],
                                             "Networks@odata.count": 1,
                                             "Networks": [{
                                                 "Id": 10155,
                                                 "Name": "testvlan",
                                                 "Description": "null",
                                                 "VlanMaximum": 143,
                                                 "VlanMinimum": 143,
                                                 "Type": 1,
                                                 "CreatedBy": "system",
                                                 "CreationTime": "2018-09-25 14:46:12.374",
                                                 "UpdatedBy": "root",
                                                 "UpdatedTime": "2019-06-27 15:06:22.836",
                                                 "InternalRefNWUUId": "f15a36b6-e3d3-46b2-9e7d-bf9cd66e180d"
                                             }]
                                         }]
                                         },
                                         "fabric_id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2",
                                         "uplink_id": "1ad54420-b145-49a1-9779-21a579ef6f2d"}])
    def test_ome_smart_fabric_main_success_case_uplink_name(self, params, mocker, ome_default_args, ome_connection_mock_for_smart_fabric_uplink_info,
                                                            ome_response_mock):
        ome_default_args.update({"fabric_id": "f1", "uplink_name": "u1"})
        ome_response_mock.success = True
        ome_response_mock.json_data = params.get("json_data")
        ome_response_mock.status_code = 200
        mocker.patch(
            MODULE_PATH + 'strip_uplink_info',
            return_value=self.uplink_info)
        result = self._run_module(ome_default_args)
        assert 'uplink_info' in result
        assert result['msg'] == "Successfully retrieved the fabric uplink information."

    @pytest.mark.parametrize("params", [{"success": True,
                                         "json_data": {"value": [{
                                             "Id": "1ad54420-b145-49a1-9779-21a579ef6f2d",
                                             "Name": "u1",
                                             "Description": "",
                                             "MediaType": "Ethernet",
                                             "NativeVLAN": 1,
                                             "Summary": {"PortCount": 2,
                                                         "NetworkCount": 1
                                                         },
                                             "UfdEnable": "Disabled",
                                             "Ports@odata.count": 2,
                                             "Ports": [{
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": "",
                                             }, {
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": ""
                                             }],
                                             "Networks@odata.count": 1,
                                             "Networks": [{
                                                 "Id": 10155,
                                                 "Name": "testvlan",
                                                 "Description": "null"
                                             }]
                                         }],
                                             "Networks": [{
                                                 "Id": 10155,
                                                 "Name": "testvlan",
                                                 "Description": "null"
                                             }],
                                             "Ports": [{
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": "",
                                             }, {
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": ""
                                             }]
                                         },
                                        'message': "Successfully retrieved the fabric uplink information.",
                                         'mparams': {"fabric_id": "f1",
                                                     "uplink_id": "u1"}
                                         }, {"success": True,
                                             "json_data": {"value": [{
                                                 "Uplinks@odata.navigationLink": "/odata/UpLink/1ad54420/b145/49a1/9779/21a579ef6f2d",
                                                 "Id": "1ad54420-b145-49a1-9779-21a579ef6f2d",
                                                 "Name": "u1",
                                                 "Description": "",
                                                 "MediaType": "Ethernet",
                                                 "NativeVLAN": 1,
                                                 "Summary": {"PortCount": 2,
                                                             "NetworkCount": 1
                                                             },
                                                 "UfdEnable": "Disabled",
                                                 "Ports@odata.count": 2,
                                                 "Ports": [{
                                                     "Id": "SVCTAG1:ethernet1/1/35",
                                                     "Name": "",
                                                     "Description": "",
                                                 }, {
                                                     "Id": "SVCTAG1:ethernet1/1/35",
                                                     "Name": "",
                                                     "Description": ""
                                                 }],
                                                 "Networks@odata.count": 1,
                                                 "Networks": [{
                                                     "Id": 10155,
                                                     "Name": "testvlan",
                                                     "Description": "null"
                                                 }]
                                             }],
                                                 "Networks": [{
                                                     "Id": 10155,
                                                     "Name": "testvlan",
                                                     "Description": "null"
                                                 }],
                                                 "Ports": [{
                                                     "Id": "SVCTAG1:ethernet1/1/35",
                                                     "Name": "",
                                                     "Description": "",
                                                 }, {
                                                     "Id": "SVCTAG1:ethernet1/1/35",
                                                     "Name": "",
                                                     "Description": ""
                                                 }]
                                             },
                                        'message': "Successfully retrieved the fabric uplink information.",
                                             'mparams': {}
                                             }])
    def test_ome_smart_fabric_exit_json(self, params, ome_default_args, ome_connection_mock_for_smart_fabric_uplink_info,
                                        ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['json_data']
        ome_default_args.update(params['mparams'])
        result = self._run_module(
            ome_default_args, check_mode=params.get('check_mode', False))
        assert 'uplink_info' in result
        assert result['msg'] == params['message']

    @pytest.mark.parametrize("params", [{"success": True,
                                         "json_data": {"value": [{
                                             "Id": "1ad54420-b145-49a1-9779-21a579ef6f2d",
                                             "Name": "u1",
                                             "Description": "",
                                             "MediaType": "Ethernet",
                                             "NativeVLAN": 1,
                                             "Summary": {"PortCount": 2,
                                                         "NetworkCount": 1
                                                         },
                                             "UfdEnable": "Disabled",
                                             "Ports@odata.count": 2,
                                             "Ports": [{
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": "",
                                                 "Type": "PhysicalEthernet",
                                                 "MediaType": "Ethernet",
                                                 "NodeServiceTag": "SVCTAG1",
                                                 "PortNumber": "ethernet1/1/35",
                                                 "Status": "Down",
                                                 "AdminStatus": "Enabled",
                                                 "CurrentSpeed": "0",
                                                 "MaxSpeed": "0",
                                                 "ConfiguredSpeed": "0",
                                                 "OpticsType": "NotPresent",
                                                 "BlinkStatus": "OFF",
                                                 "Role": "Uplink"
                                             }, {
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": "",
                                                 "Type": "PhysicalEthernet",
                                                 "MediaType": "Ethernet",
                                                 "NodeServiceTag": "SVCTAG1",
                                                 "PortNumber": "ethernet1/1/35",
                                                 "Status": "Down",
                                                 "AdminStatus": "Enabled",
                                                 "CurrentSpeed": "0",
                                                 "MaxSpeed": "0",
                                                 "ConfiguredSpeed": "0",
                                                 "OpticsType": "NotPresent",
                                                 "BlinkStatus": "OFF",
                                                 "Role": "Uplink"
                                             }],
                                             "Networks@odata.count": 1,
                                             "Networks": [{
                                                 "Id": 10155,
                                                 "Name": "testvlan",
                                                 "Description": "null",
                                                 "VlanMaximum": 143,
                                                 "VlanMinimum": 143,
                                                 "Type": 1,
                                                 "CreatedBy": "system",
                                                 "CreationTime": "2018-09-25 14:46:12.374",
                                                 "UpdatedBy": "root",
                                                 "UpdatedTime": "2019-06-27 15:06:22.836",
                                                 "InternalRefNWUUId": "f15a36b6-e3d3-46b2-9e7d-bf9cd66e180d"
                                             }]
                                         }]
                                         },
                                         "fabric_id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2",
                                         "uplink_id": "1ad54420-b145-49a1-9779-21a579ef6f2d"}])
    def test_get_all_uplink_details(self, params, ome_connection_mock_for_smart_fabric_uplink_info, ome_response_mock):
        ome_response_mock.success = params["success"]
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock()
        resp = self.module.get_all_uplink_details(
            f_module, ome_connection_mock_for_smart_fabric_uplink_info)
        assert resp == []

    @pytest.mark.parametrize("params", [{"success": True,
                                         "inp": {"fabric_id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2",
                                                 "uplink_name": "1ad54420-b145-49a1-9779-21a579ef6f2d"},
                                         "json_data": {"value": [{
                                             "Id": "1ad54420-b145-49a1-9779-21a579ef6f2d",
                                             "Name": "u1",
                                             "Description": "",
                                             "MediaType": "Ethernet",
                                             "NativeVLAN": 1,
                                             "Summary": {"PortCount": 2,
                                                         "NetworkCount": 1
                                                         },
                                             "UfdEnable": "Disabled",
                                             "Ports@odata.count": 2,
                                             "Ports": [{
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": "",
                                                 "Type": "PhysicalEthernet",
                                                 "MediaType": "Ethernet",
                                                 "NodeServiceTag": "SVCTAG1",
                                                 "PortNumber": "ethernet1/1/35",
                                                 "Status": "Down",
                                                 "AdminStatus": "Enabled",
                                                 "CurrentSpeed": "0",
                                                 "MaxSpeed": "0",
                                                 "ConfiguredSpeed": "0",
                                                 "OpticsType": "NotPresent",
                                                 "BlinkStatus": "OFF",
                                                 "Role": "Uplink"
                                             }, {
                                                 "Id": "SVCTAG1:ethernet1/1/35",
                                                 "Name": "",
                                                 "Description": "",
                                                 "Type": "PhysicalEthernet",
                                                 "MediaType": "Ethernet",
                                                 "NodeServiceTag": "SVCTAG1",
                                                 "PortNumber": "ethernet1/1/35",
                                                 "Status": "Down",
                                                 "AdminStatus": "Enabled",
                                                 "CurrentSpeed": "0",
                                                 "MaxSpeed": "0",
                                                 "ConfiguredSpeed": "0",
                                                 "OpticsType": "NotPresent",
                                                 "BlinkStatus": "OFF",
                                                 "Role": "Uplink"
                                             }],
                                             "Networks@odata.count": 1,
                                             "Networks": [{
                                                 "Id": 10155,
                                                 "Name": "testvlan",
                                                 "Description": "null",
                                                 "VlanMaximum": 143,
                                                 "VlanMinimum": 143,
                                                 "Type": 1,
                                                 "CreatedBy": "system",
                                                 "CreationTime": "2018-09-25 14:46:12.374",
                                                 "UpdatedBy": "root",
                                                 "UpdatedTime": "2019-06-27 15:06:22.836",
                                                 "InternalRefNWUUId": "f15a36b6-e3d3-46b2-9e7d-bf9cd66e180d"
                                             }]
                                         }]
                                         },
                                         "fabric_id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2",
                                         "uplink_name": "1ad54420-b145-49a1-9779-21a579ef6f2d"}])
    def test_get_uplink_name_failure_case(self, params, mocker, ome_connection_mock_for_smart_fabric_uplink_info, ome_response_mock, ome_default_args):
        ome_default_args.update(params.get("inp"))
        ome_response_mock.success = params["success"]
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params.get("inp"))
        # result = self.module.get_uplink_id_from_name(f_module, ome_connection_mock_for_smart_fabric_uplink_info,
        #                                                 params.get("uplink_name"), params.get("fabric_id"))
        mocker.patch(
            MODULE_PATH + 'get_uplink_id_from_name',
            return_value="")
        uplink_id = self.module.get_uplink_id_from_name(ome_default_args)
        assert uplink_id == ""

    @pytest.mark.parametrize("params", [{"uplink_name": "f1", "fabric_id": "u1"}])
    def test_get_uplink_id_from_name_HTTPError_error_case(self, params, ome_default_args, mocker,
                                                          ome_connection_mock):
        json_str = to_text(json.dumps({"info": "error_details"}))
        error_msg = "Unable to retrieve smart fabric uplink information."
        ome_connection_mock.invoke_request.side_effect = HTTPError('https://testdell.com', 404,
                                                                   error_msg,
                                                                   {"accept-type": "application/json"},
                                                                   StringIO(json_str))
        f_module = self.get_module_mock()
        with pytest.raises(Exception) as exc:
            self.module.get_uplink_id_from_name(f_module, ome_connection_mock, params.get("uplink_name"),
                                                params.get('fabric_id'))
        assert exc.value.args[0] == error_msg

    @pytest.mark.parametrize("params", [{"fabric_name": "f1"}])
    def test_get_all_uplink_details_HTTPError_error_case(self, params, ome_default_args, mocker,
                                                         ome_connection_mock):
        json_str = to_text(json.dumps({"info": "error_details"}))
        error_msg = "Unable to retrieve smart fabric uplink information."
        ome_connection_mock.invoke_request.side_effect = HTTPError('https://testdell.com', 404,
                                                                   error_msg,
                                                                   {"accept-type": "application/json"},
                                                                   StringIO(json_str))
        f_module = self.get_module_mock()
        with pytest.raises(Exception) as exc:
            self.module.get_all_uplink_details(f_module, ome_connection_mock)
        assert exc.value.args[0] == error_msg

    @pytest.mark.parametrize("params", [{"fabric_name": "f1"}])
    def test_get_fabric_id_from_name_HTTPError_error_case(self, params, ome_default_args, mocker,
                                                          ome_connection_mock):
        json_str = to_text(json.dumps({"info": "error_details"}))
        error_msg = "Unable to retrieve smart fabric uplink information."
        ome_connection_mock.invoke_request.side_effect = HTTPError('https://testdell.com', 404,
                                                                   error_msg,
                                                                   {"accept-type": "application/json"},
                                                                   StringIO(json_str))
        f_module = self.get_module_mock()
        with pytest.raises(Exception) as exc:
            self.module.get_fabric_id_from_name(
                f_module, ome_connection_mock, params.get('fabric_name'))
        assert exc.value.args[0] == error_msg

    @pytest.mark.parametrize("params", [{"fabric_id": "f1", "uplink_id": "u1"}])
    def test_get_uplink_details_HTTPError_error_case(self, params, ome_default_args, mocker,
                                                     ome_connection_mock):
        json_str = to_text(json.dumps({"info": "error_details"}))
        error_msg = "Unable to retrieve smart fabric uplink information with uplink ID {0}.".format(
            params.get('uplink_id'))
        ome_connection_mock.invoke_request.side_effect = HTTPError('https://testdell.com', 404,
                                                                   error_msg,
                                                                   {"accept-type": "application/json"},
                                                                   StringIO(json_str))
        f_module = self.get_module_mock()
        with pytest.raises(Exception) as exc:
            self.module.get_uplink_details(f_module, ome_connection_mock, params.get(
                'fabric_id'), params.get('uplink_id'))
        assert exc.value.args[0] == error_msg

    @pytest.mark.parametrize("params", [{"fabric_id": "f1"}])
    def test_get_uplink_details_from_fabric_id_HTTPError_error_case(self, params, ome_default_args, mocker,
                                                                    ome_connection_mock):
        json_str = to_text(json.dumps({"info": "error_details"}))
        error_msg = "Unable to retrieve smart fabric uplink information with fabric ID {0}.".format(
            params.get('fabric_id'))
        ome_connection_mock.invoke_request.side_effect = HTTPError('https://testdell.com', 404,
                                                                   error_msg,
                                                                   {"accept-type": "application/json"},
                                                                   StringIO(json_str))
        f_module = self.get_module_mock()
        with pytest.raises(Exception) as exc:
            self.module.get_uplink_details_from_fabric_id(
                f_module, ome_connection_mock, params.get('fabric_id'))
        assert exc.value.args[0] == error_msg

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_smart_fabric_uplink_info_main_exception_failure_case(self, exc_type, mocker, ome_default_args,
                                                                      ome_connection_mock_for_smart_fabric_uplink_info,
                                                                      ome_response_mock):
        ome_default_args.update({"fabric_id": "f1"})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'get_uplink_details_from_fabric_id',
                         side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'get_uplink_details_from_fabric_id',
                         side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'get_uplink_details_from_fabric_id',
                         side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
