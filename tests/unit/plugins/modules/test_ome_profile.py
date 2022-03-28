# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.2.0
# Copyright (C) 2021 Dell Inc. or its subsidiaries. All Rights Reserved.

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
from ansible_collections.dellemc.openmanage.plugins.modules import ome_profile
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_profile.'
CHANGES_MSG = "Changes found to be applied."
NO_CHANGES_MSG = "No changes found to be applied."


@pytest.fixture
def ome_connection_mock_for_profile(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeProfile(FakeAnsibleModule):
    module = ome_profile

    @pytest.mark.parametrize("params",
                             [{"mparams": {"template_id": 123}, "success": True,
                               "json_data": {"value": [{"Name": "vlan_name", "Id": 123, "IdentityPoolId": 23}]},
                               "res": {"Name": "vlan_name", "Id": 123, "IdentityPoolId": 23}},
                              {"mparams": {"template_name": "temp1"}, "success": True,
                               "json_data": {"value": [{"Name": "temp1", "Id": 123, "IdentityPoolId": 23}]},
                               "res": {"Name": "temp1", "Id": 123, "IdentityPoolId": 23}}])
    def test_get_template_details(self, params, ome_connection_mock_for_profile, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params["mparams"])
        result = self.module.get_template_details(f_module, ome_connection_mock_for_profile)
        assert result == params["res"]

    @pytest.mark.parametrize("params",
                             [{"mparams": {"device_id": 123}, "success": True,
                               "json_data": {"value": [{"Name": "vlan_name", "Id": 123, "IdentityPoolId": 23}]},
                               "res": {"Name": "vlan_name", "Id": 123, "IdentityPoolId": 23}},
                              {"mparams": {"device_service_tag": "ABC1234"}, "success": True,
                               "json_data": {"value": [{"Identifier": "ABC1234", "Id": 123, "IdentityPoolId": 23}]},
                               "res": {"Identifier": "ABC1234", "Id": 123, "IdentityPoolId": 23}}])
    def test_get_target_details(self, params, ome_connection_mock_for_profile, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params["mparams"])
        result = self.module.get_target_details(f_module, ome_connection_mock_for_profile)
        assert result == params["res"]

    @pytest.mark.parametrize("params",
                             [{"mparams": {
                                 "attributes": {
                                     "Attributes": [
                                         {
                                             "Id": 93812,
                                             "IsIgnored": False,
                                             "Value": "Aisle Five"
                                         },
                                         {
                                             "DisplayName": 'System, Server Topology, ServerTopology 1 Aisle Name',
                                             "IsIgnored": False,
                                             "Value": "Aisle 5"
                                         }
                                     ]
                                 }}, "success": True,
                                 "json_data": {
                                     "Id": 11,
                                     "Name": "ProfileViewEditAttributes",
                                     "AttributeGroupNames": [],
                                     "AttributeGroups": [
                                         {
                                             "GroupNameId": 5,
                                             "DisplayName": "System",
                                             "SubAttributeGroups": [
                                                 {
                                                     "GroupNameId": 33016,
                                                     "DisplayName": "Server Operating System",
                                                     "SubAttributeGroups": [],
                                                     "Attributes": [
                                                         {
                                                             "AttributeId": 93820,
                                                             "DisplayName": "ServerOS 1 Server Host Name",
                                                             "Description": None,
                                                             "Value": None,
                                                             "IsReadOnly": False,
                                                             "IsIgnored": True,
                                                         }
                                                     ]
                                                 },
                                                 {
                                                     "GroupNameId": 33019,
                                                     "DisplayName": "Server Topology",
                                                     "SubAttributeGroups": [],
                                                     "Attributes": [
                                                         {
                                                             "AttributeId": 93812,
                                                             "CustomId": 0,
                                                             "AttributeEditInfoId": 2248,
                                                             "DisplayName": "ServerTopology 1 Aisle Name",
                                                             "Description": None,
                                                             "Value": "Aisle 5",
                                                             "IsReadOnly": False,
                                                             "IsIgnored": True,
                                                         },
                                                         {
                                                             "AttributeId": 93811,
                                                             "DisplayName": "ServerTopology 1 Data Center Name",
                                                             "Value": "BLG 2nd Floor DS 1",
                                                             "IsReadOnly": False,
                                                             "IsIgnored": True,
                                                         },
                                                         {
                                                             "AttributeId": 93813,
                                                             "DisplayName": "ServerTopology 1 Rack Name",
                                                             "Description": None,
                                                             "Value": None,
                                                             "IsReadOnly": False,
                                                             "IsIgnored": True,
                                                         },
                                                         {
                                                             "AttributeId": 93814,
                                                             "DisplayName": "ServerTopology 1 Rack Slot",
                                                             "Description": None,
                                                             "Value": None,
                                                             "IsReadOnly": False,
                                                             "IsIgnored": True,
                                                         }
                                                     ]
                                                 }
                                             ],
                                             "Attributes": []
                                         },
                                         {
                                             "GroupNameId": 9,
                                             "DisplayName": "iDRAC",
                                             "SubAttributeGroups": [
                                                 {
                                                     "GroupNameId": 32688,
                                                     "DisplayName": "Active Directory",
                                                     "SubAttributeGroups": [],
                                                     "Attributes": [
                                                         {
                                                             "AttributeId": 93523,
                                                             "DisplayName": "ActiveDirectory 1 Active Directory RAC Name",
                                                             "Description": None,
                                                             "Value": None,
                                                             "IsReadOnly": False,
                                                             "IsIgnored": True,
                                                         }
                                                     ]
                                                 },
                                                 {
                                                     "GroupNameId": 32930,
                                                     "DisplayName": "NIC Information",
                                                     "SubAttributeGroups": [],
                                                     "Attributes": [
                                                         {
                                                             "AttributeId": 93035,
                                                             "DisplayName": "NIC 1 DNS RAC Name",
                                                             "Description": None,
                                                             "Value": None,
                                                             "IsReadOnly": False,
                                                             "IsIgnored": True,
                                                         },
                                                         {
                                                             "AttributeId": 92510,
                                                             "DisplayName": "NIC 1 Enable VLAN",
                                                             "Description": None,
                                                             "Value": "Disabled",
                                                             "IsReadOnly": False,
                                                             "IsIgnored": False,
                                                         }
                                                     ]
                                                 }
                                             ],
                                             "Attributes": []}]},
                                 "diff": 2}])
    def test_attributes_check(self, params, ome_connection_mock_for_profile, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params["mparams"])
        result = self.module.attributes_check(f_module, ome_connection_mock_for_profile,
                                              params['mparams']['attributes'], 123)
        assert result == params["diff"]

    @pytest.mark.parametrize("params", [{"mparams": {"command": 'create'}, "func": "create_profile"},
                                        {"mparams": {"command": 'modify'}, "func": "modify_profile"},
                                        {"mparams": {"command": 'delete'}, "func": "delete_profile"},
                                        {"mparams": {"command": 'assign'}, "func": "assign_profile"},
                                        {"mparams": {"command": 'unassign'}, "func": "unassign_profile"},
                                        {"mparams": {"command": 'migrate'}, "func": "migrate_profile"}])
    def test_profile_operation(self, mocker, params, ome_connection_mock_for_profile, ome_response_mock):
        mocker.patch(MODULE_PATH + params.get('func'), return_value={"Id": 12})
        f_module = self.get_module_mock(params=params["mparams"])
        self.module.profile_operation(f_module, ome_connection_mock_for_profile)

    @pytest.mark.parametrize("params", [{"mparams": {"name": "p1"}, "success": True, "json_data": {
        "value": [{"Id": 123, "ProfileName": "p1"}]}, "res": {"Id": 123, "ProfileName": "p1"}}])
    def test_get_profile(self, params, ome_connection_mock_for_profile, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params["mparams"])
        result = self.module.get_profile(ome_connection_mock_for_profile, f_module)
        assert result == params["res"]

    @pytest.mark.parametrize("params", [{"mparams": {
        "command": "create", "template_name": "t1", "name_prefix": "profile",
        "number_of_profiles": 2, "description": "Created 1",
        "boot_to_network_iso": {
            "boot_to_network": True,
            "share_type": "CIFS",
            "share_ip": "100.200.300",
            "share_user": "shareuser",
            "share_pwd": "sharepwd",
            "workgroup": "workgroup",
            "iso_path": "pathofiso.iso",
            "iso_timeout": 8
        }
    },
        "success": True,
        "json_data": [1, 2],
        "res": "Successfully created 2 profile(s)."},
        {
            "mparams":
                {
                    "command": "create",
                    "template_name": "t1",
                    "name_prefix": "profile",
                    "number_of_profiles": 1
                },
            "success": True,
            "json_data": [1],
            "res": "Successfully created 1 profile(s)."},
        {
            "mparams":
                {
                    "command": "create",
                    "template_name": "t1",
                    "name_prefix": "profile",
                    "number_of_profiles": 1
                },
            "success": True, "check_mode": True, "json_data": [1], "res": CHANGES_MSG}
    ])
    def test_create_profile(self, mocker, params, ome_connection_mock_for_profile, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        mocker.patch(MODULE_PATH + 'get_template_details', return_value={"Id": 12})
        f_module = self.get_module_mock(params=params["mparams"], check_mode=params.get('check_mode', False))
        error_message = params["res"]
        with pytest.raises(Exception) as err:
            self.module.create_profile(f_module, ome_connection_mock_for_profile)
        assert err.value.args[0] == error_message

    @pytest.mark.parametrize("params", [
        {"mparams": {"command": "modify", "name": "profile"},
         "success": True,
         "prof": {}, "json_data": 0,
         "res": "Profile with the name 'profile' not found."},
        {"mparams": {"command": "modify", "name": "profile", "new_name": "modified profile",
                     "description": "new description",
                     "boot_to_network_iso": {"boot_to_network": True, "share_type": "NFS", "share_ip": "192.168.0.1",
                                             "iso_path": "path/to/my_iso.iso",
                                             "iso_timeout": 8},
                     "attributes": {"Attributes": [{"Id": 4506, "Value": "server attr 1",
                                                    "IsIgnored": True}]}}, "success": True,
         "prof": {"Id": 1234,
                  "ProfileName": "jrofile 00002",
                  "ProfileDescription": "from source template t1",
                  "NetworkBootToIso": {"BootToNetwork": True, "ShareType": "NFS", "IsoPath": "abcd.iso",
                                       "ShareDetail": {"IpAddress": "XX.XX.XX.XX", "ShareName": "XX.XX.XX.XX", },
                                       "IsoTimeout": 4},
                  "ProfileState": 0, },
         "json_data": 0,
         "res": "Successfully modified the profile."},
        {"mparams": {"command": "modify", "name": "myprofile", "new_name": "myprofile"},
         "success": True,
         "prof": {"Id": 1234, "ProfileName": "myprofile", "ProfileDescription": "my description"},
         "json_data": 0, "res": "No changes found to be applied."},
        {"mparams": {"command": "modify", "name": "profile", "new_name": "modified profile",
                     "description": "new description",
                     "boot_to_network_iso": {"boot_to_network": True, "share_type": "NFS", "share_ip": "192.168.0.1",
                                             "iso_path": "path/to/my_iso.iso", "iso_timeout": 8},
                     "attributes": {"Attributes": [{"Id": 4506, "Value": "server attr 1",
                                                    "IsIgnored": True}]}}, "success": True,
         "prof": {"Id": 1234, "ProfileName": "jrofile 00002",
                  "ProfileDescription": "from source template t1",
                  "NetworkBootToIso": {
                      "BootToNetwork": True, "ShareType": "NFS", "IsoPath": "abcd.iso",
                      "ShareDetail": {"IpAddress": "XX.XX.XX.XX", "ShareName": "XX.XX.XX.XX"}, "IsoTimeout": 4},
                  "ProfileState": 0, },
         "json_data": 0, "attributes_check": 2, "check_mode": True, "res": CHANGES_MSG}
    ])
    def test_modify_profile(self, mocker, params, ome_connection_mock_for_profile, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        mocker.patch(MODULE_PATH + 'get_profile', return_value=params.get('prof'))
        mocker.patch(MODULE_PATH + 'attributes_check', return_value=params.get('attributes_check', 0))
        f_module = self.get_module_mock(params=params["mparams"], check_mode=params.get('check_mode', False))
        error_message = params["res"]
        with pytest.raises(Exception) as err:
            self.module.modify_profile(f_module, ome_connection_mock_for_profile)
        assert err.value.args[0] == error_message

    @pytest.mark.parametrize("params", [
        {"mparams": {"command": "delete", "name": "profile"}, "success": True,
         "prof": {"Id": 12, "ProfileState": 4}, "json_data": 0,
         "res": "Profile has to be in an unassigned state for it to be deleted."},
        {"mparams": {"command": "delete", "name": "profile"}, "success": True,
         "prof": {"Id": 12, "ProfileState": 0}, "json_data": 0,
         "res": "Successfully deleted the profile."},
        {"mparams": {"command": "delete", "name": "profile"}, "success": True,
         "prof": {"Id": 12, "ProfileState": 0}, "json_data": 0, "check_mode": True,
         "res": CHANGES_MSG},
        {"mparams": {"command": "delete", "name": "profile"}, "success": True,
         "prof": {}, "json_data": 0,
         "res": "Profile with the name 'profile' not found."},
        {"mparams": {"command": "delete", "filters": "profile"}, "success": True,
         "prof": {"Id": 12, "ProfileState": 0}, "json_data": 0,
         "res": "Successfully completed the delete operation."},
        {"mparams": {"command": "delete", "filters": "profile"}, "success": True,
         "prof": {"Id": 12, "ProfileState": 0}, "json_data": 0, "check_mode": True,
         "res": CHANGES_MSG},
    ])
    def test_delete_profile(self, mocker, params, ome_connection_mock_for_profile, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        mocker.patch(MODULE_PATH + 'get_profile', return_value=params.get('prof'))
        f_module = self.get_module_mock(params=params["mparams"], check_mode=params.get('check_mode', False))
        error_message = params["res"]
        with pytest.raises(Exception) as err:
            self.module.delete_profile(f_module, ome_connection_mock_for_profile)
        assert err.value.args[0] == error_message

    @pytest.mark.parametrize("params", [
        {"mparams": {"command": "assign", "name": "profile"}, "success": True,
         "prof": {"Id": 123, "ProfileState": 1, "TargetName": "ABC1234"}, "json_data": 0,
         "res": "The profile is assigned to a different target. Unassign the profile and then proceed with assigning the"
                " profile to the target."},
        {"mparams": {"command": "assign", "name": "profile"}, "success": True, "prof": {},
         "json_data": 0, "res": "Profile with the name 'profile' not found."},
        {"mparams": {"command": "assign", "name": "profile", "device_id": 234}, "success": True,
         "prof": {"Id": 123, "ProfileState": 0}, "target": {"Id": 234, "Name": "mytarget"},
         "json_data": [234, 123],
         "res": "The target device is invalid for the given profile."},
        {"mparams": {"command": "assign", "name": "profile", "device_id": 234,
                     "boot_to_network_iso": {"boot_to_network": True, "share_type": "NFS", "share_ip": "192.168.0.1",
                                             "iso_path": "path/to/my_iso.iso",
                                             "iso_timeout": 8},
                     "attributes": {"Attributes": [{"Id": 4506, "Value": "server attr 1", "IsIgnored": True}]}},
         "success": True,
         "prof": {"Id": 123, "ProfileState": 0}, "target": {"Id": 234, "Name": "mytarget"}, "json_data": [23, 123],
         "res": "Successfully applied the assign operation."},
        {"mparams": {"command": "assign", "name": "profile", "device_service_tag": "ABCDEFG",
                     "boot_to_network_iso": {"boot_to_network": True, "share_type": "NFS", "share_ip": "192.168.0.1",
                                             "iso_path": "path/to/my_iso.iso",
                                             "iso_timeout": 8},
                     "attributes": {"Attributes": [{"Id": 4506, "Value": "server attr 1", "IsIgnored": True}]}},
         "success": True, "prof": {"Id": 123, "ProfileState": 0}, "target": {"Id": 234, "Name": "mytarget"},
         "json_data": [23, 123], "res": "Successfully applied the assign operation."},
        {"mparams": {"command": "assign", "name": "profile", "device_id": 234,
                     "boot_to_network_iso": {"boot_to_network": True, "share_type": "NFS", "share_ip": "192.168.0.1",
                                             "iso_path": "path/to/my_iso.iso",
                                             "iso_timeout": 8},
                     "attributes": {"Attributes": [{"Id": 4506, "Value": "server attr 1", "IsIgnored": True}]}},
         "success": True,
         "prof": {"Id": 123, "ProfileState": 4, "TargetId": 234}, "target": {"Id": 234, "Name": "mytarget"},
         "json_data": [23, 123],
         "res": "The profile is assigned to the target 234."},
        {"mparams": {"command": "assign", "name": "profile", "device_id": 234,
                     "boot_to_network_iso": {"boot_to_network": True, "share_type": "NFS", "share_ip": "192.168.0.1",
                                             "iso_path": "path/to/my_iso.iso",
                                             "iso_timeout": 8},
                     "attributes": {"Attributes": [{"Id": 4506, "Value": "server attr 1", "IsIgnored": True}]}},
         "success": True,
         "prof": {"Id": 123, "ProfileState": 4, "TargetId": 235}, "target": {"Id": 234, "Name": "mytarget"},
         "json_data": [23, 123],
         "res": "The profile is assigned to a different target. Use the migrate command or unassign the profile and "
                "then proceed with assigning the profile to the target."},
        {"mparams": {"command": "assign", "name": "profile", "device_service_tag": "STG1234",
                     "boot_to_network_iso": {"boot_to_network": True, "share_type": "NFS", "share_ip": "192.168.0.1",
                                             "iso_path": "path/to/my_iso.iso",
                                             "iso_timeout": 8},
                     "attributes": {"Attributes": [{"Id": 4506, "Value": "server attr 1", "IsIgnored": True}]}},
         "success": True,
         "prof": {"Id": 123, "ProfileState": 1, "TargetId": 235, "TargetName": "STG1234"}, "target": "Target invalid.",
         "json_data": [23, 123],
         "res": "The profile is assigned to the target STG1234."},
        {"mparams": {"command": "assign", "name": "profile", "device_id": 123,
                     "boot_to_network_iso": {"boot_to_network": True, "share_type": "NFS", "share_ip": "192.168.0.1",
                                             "iso_path": "path/to/my_iso.iso",
                                             "iso_timeout": 8},
                     "attributes": {"Attributes": [{"Id": 4506, "Value": "server attr 1", "IsIgnored": True}]}},
         "success": True,
         "prof": {"Id": 123, "ProfileState": 1, "TargetId": 235, "TargetName": "STG1234"}, "target": "Target invalid.",
         "json_data": [23, 123],
         "res": "Target invalid."},
        {"mparams": {"command": "assign", "name": "profile", "device_id": 234,
                     "boot_to_network_iso": {"boot_to_network": True, "share_type": "NFS", "share_ip": "192.168.0.1",
                                             "iso_path": "path/to/my_iso.iso",
                                             "iso_timeout": 8},
                     "attributes": {"Attributes": [{"Id": 4506, "Value": "server attr 1", "IsIgnored": True}]}},
         "success": True, "check_mode": True,
         "prof": {"Id": 123, "ProfileState": 0}, "target": {"Id": 234, "Name": "mytarget"}, "json_data": [23, 123],
         "res": CHANGES_MSG},
        {"mparams": {"command": "assign", "name": "profile", "device_id": 234,
                     "boot_to_network_iso": {"boot_to_network": True, "share_type": "NFS", "share_ip": "192.168.0.1",
                                             "iso_path": "path/to/my_iso.iso",
                                             "iso_timeout": 8},
                     "attributes": {"Attributes": [{"Id": 4506, "Value": "server attr 1", "IsIgnored": True}]}},
         "success": True,
         "prof": {"Id": 123, "ProfileState": 0, "DeploymentTaskId": 12}, "target": {"Id": 234, "Name": "mytarget"},
         "json_data": [23, 123],
         "res": "Successfully triggered the job for the assign operation."},
    ])
    def test_assign_profile(self, mocker, params, ome_connection_mock_for_profile, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        mocker.patch(MODULE_PATH + 'get_profile', return_value=params.get('prof'))
        mocker.patch(MODULE_PATH + 'get_target_details', return_value=params.get('target'))
        f_module = self.get_module_mock(params=params["mparams"], check_mode=params.get('check_mode', False))
        error_message = params["res"]
        mocker.patch(MODULE_PATH + 'time.sleep', return_value=None)
        with pytest.raises(Exception) as err:
            self.module.assign_profile(f_module, ome_connection_mock_for_profile)
        assert err.value.args[0] == error_message

    @pytest.mark.parametrize("params", [
        {"mparams": {"command": "unassign", "name": "profile"}, "success": True,
         "prof": {"Id": 12, "ProfileState": 0},
         "json_data": 0, "res": "Profile is in an unassigned state."},
        {"mparams": {"command": "unassign", "name": "profile"}, "success": True,
         "prof": {}, "json_data": 0,
         "res": "Profile with the name 'profile' not found."},
        {"mparams": {"command": "unassign", "filters": "profile"}, "success": True,
         "prof": {"Id": 12, "ProfileState": 4},
         "json_data": 0, "res": "Successfully applied the unassign operation. No job was triggered."},
        {"mparams": {"command": "unassign", "filters": "profile"}, "success": True,
         "json_data": 0, "prof": {"Id": 12, "ProfileState": 1},
         "res": "Successfully applied the unassign operation. No job was triggered."},
        {"mparams": {"command": "unassign", "name": "profile"}, "success": True,
         "prof": {"Id": 12, "ProfileState": 4, "DeploymentTaskId": 123},
         "json_data": {"LastRunStatus": {"Name": "Running"}},
         "res": "Profile deployment task is in progress. Wait for the job to finish."},
        {"mparams": {"command": "unassign", "name": "profile"}, "success": True,
         "prof": {"Id": 12, "ProfileState": 4, "DeploymentTaskId": 123},
         "json_data": {"LastRunStatus": {"Name": "Starting"}},
         "res": "Successfully triggered a job for the unassign operation."},
        {"mparams": {"command": "unassign", "name": "profile"}, "success": True,
         "prof": {"Id": 12, "ProfileState": 4, "DeploymentTaskId": 123},
         "json_data": {"LastRunStatus": {"Name": "Starting"}}, "check_mode": True,
         "res": CHANGES_MSG}
    ])
    def test_unassign_profile(self, mocker, params, ome_connection_mock_for_profile, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        mocker.patch(MODULE_PATH + 'get_profile', return_value=params.get('prof'))
        f_module = self.get_module_mock(params=params["mparams"], check_mode=params.get('check_mode', False))
        error_message = params["res"]
        mocker.patch(MODULE_PATH + 'time.sleep', return_value=None)
        with pytest.raises(Exception) as err:
            self.module.unassign_profile(f_module, ome_connection_mock_for_profile)
        assert err.value.args[0] == error_message

    @pytest.mark.parametrize("params", [
        {"mparams": {"command": "migrate", "name": "profile"}, "success": True,
         "prof": {"Id": 12, "ProfileState": 4, "TargetId": 14, "DeploymentTaskId": 123},
         "target": {"Id": 12},
         "json_data": [1, 2, 3], "res": "Successfully triggered the job for the migrate operation."},
        {"mparams": {"command": "migrate", "name": "profile"}, "success": True,
         "prof": {},
         "target": {"Id": 12, "TargetId": 14}, "json_data": 0,
         "res": "Profile with the name 'profile' not found."},
        {"mparams": {"command": "migrate", "name": "profile"}, "success": True,
         "prof": {"Id": 12, "ProfileState": 0, "TargetId": 14},
         "target": {"Id": 13, "TargetId": 14}, "json_data": [1, 2, 3],
         "res": "Profile needs to be in a deployed state for a migrate operation."},
        {"mparams": {"command": "migrate", "name": "profile"}, "success": True,
         "prof": {"Id": 12, "ProfileState": 4, "TargetId": 12}, "target": {"Id": 12}, "json_data": 0,
         "res": "No changes found to be applied."},
        {"mparams": {"command": "migrate", "name": "profile"}, "success": True,
         "prof": {"Id": 12, "ProfileState": 4, "TargetId": 14, "DeploymentTaskId": 123},
         "target": "Target invalid.",
         "json_data": [1, 2, 3], "res": "Target invalid."},
        {"mparams": {"command": "migrate", "name": "profile"}, "success": True,
         "prof": {"Id": 12, "ProfileState": 4, "TargetId": 14, "DeploymentTaskId": 123},
         "target": {"Id": 12},
         "json_data": [12, 21, 13], "res": "The target device is invalid for the given profile."},
        {"mparams": {"command": "migrate", "name": "profile"}, "success": True,
         "prof": {"Id": 12, "ProfileState": 4, "TargetId": 14, "DeploymentTaskId": 123},
         "target": {"Id": 12}, "check_mode": True,
         "json_data": [1, 2, 3], "res": CHANGES_MSG},
    ])
    def test_migrate_profile(self, mocker, params, ome_connection_mock_for_profile, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        mocker.patch(MODULE_PATH + 'get_profile', return_value=params.get('prof'))
        mocker.patch(MODULE_PATH + 'get_target_details', return_value=params.get('target'))
        f_module = self.get_module_mock(params=params["mparams"], check_mode=params.get('check_mode', False))
        error_message = params["res"]
        mocker.patch(MODULE_PATH + 'time.sleep', return_value=None)
        with pytest.raises(Exception) as err:
            self.module.migrate_profile(f_module, ome_connection_mock_for_profile)
        assert err.value.args[0] == error_message

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_profile_main_exception_failure_case(self, exc_type, mocker, ome_default_args,
                                                     ome_connection_mock_for_profile, ome_response_mock):
        ome_default_args.update({"template_name": "t1"})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'profile_operation', side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'profile_operation', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'profile_operation',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result
