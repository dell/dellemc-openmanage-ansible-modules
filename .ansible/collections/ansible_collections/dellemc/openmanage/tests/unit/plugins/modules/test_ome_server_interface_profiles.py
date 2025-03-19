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
from ansible_collections.dellemc.openmanage.plugins.modules import ome_server_interface_profiles
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

APPLY_TRIGGERED = "Successfully initiated the apply server profiles job."
NO_STAG = "No profile found for service tag {service_tag}."
CHANGES_MSG = "Changes found to be applied."
NO_CHANGES_MSG = "No changes found to be applied."
VLAN_NOT_FOUND = "The VLAN with a name {vlan_name} not found."
DUPLICATE_NIC_IDENTIFIED = "Duplicate NIC identfiers provided."
INVALID_UNTAGGED = "The untagged VLAN {id} provided for the NIC ID {nic_id} is not valid."
NW_OVERLAP = "Network profiles of {service_tag} provided for tagged or untagged VLANs of {nic_id} overlaps."
INVALID_DEV_ST = "Unable to complete the operation because the entered target device service tag(s) '{0}' are invalid."
INVALID_DEV_ID = "Unable to complete the operation because the entered target device ids '{0}' are invalid."

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_server_interface_profiles.'


@pytest.fixture
def ome_connection_mock_for_sips(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeSIPs(FakeAnsibleModule):
    module = ome_server_interface_profiles

    @pytest.mark.parametrize("params", [
        {"json_data": {"JobId": 1234},
         'message': APPLY_TRIGGERED, "success": True,
         'Devices': {"value": [{"Id": 123, "Identifier": "ABC1234"}]},
         "_get_profile": {
             "Id": "ABC1234",
             "ServerServiceTag": "ABC1234",
             "BondingTechnology": "NoTeaming"},
         "_get_interface": {
             "NIC.Mezzanine.1A-1-1": {
                 "NativeVLAN": 3,
                 "Networks": [
                     11569,
                     10155
                 ],
                 "NicBonded": False
             },
             "NIC.Mezzanine.1A-2-1": {
                 "NativeVLAN": 2,
                 "Networks": [
                     11569,
                     10155,
                     12350
                 ],
                 "NicBonded": False
             }},
         "vlan_map": {"testvlan": 10155, "VLAN 1": 11569, "range120-125": 12350, "range130-135": 12352, "two": 14679,
                      "three": 14681},
         "natives": {143: 10155, 1: 11569, 2: 14679, 3: 14681, 0: 0},
         'mparams': {"job_wait": False, "device_service_tag": ["ABC1234"],
                     "nic_configuration": [{
                         "nic_identifier": "NIC.Mezzanine.1A-1-1",
                         "tagged_networks": {
                             "names": ["testvlan"],
                             "state": "present"},
                         "team": False,
                         "untagged_network": 3},
                         {
                             "nic_identifier": "NIC.Mezzanine.1A-2-1",
                             "tagged_networks": {"names": ["range120-125"],
                                                 "state": "present"},
                             "team": True,
                             "untagged_network": 3}],
                     "nic_teaming": "NoTeaming",
                     }},
        {"json_data": {"JobId": 1234},
         'message': INVALID_DEV_ST.format('ABC123'), "success": True,
         'Devices': {"value": [{"Id": 123, "Identifier": "ABC1234"}]},
         'mparams': {"job_wait": False, "device_service_tag": ["ABC123"],
                     "nic_configuration": [],
                     "nic_teaming": "NoTeaming",
                     }},
        {"json_data": {"JobId": 1234},
         'message': INVALID_DEV_ID.format('1111'), "success": True,
         'Devices': {"value": [{"Id": 123, "Identifier": "ABC1234"}]},
         'mparams': {"job_wait": False, "device_id": [1111],
                     "nic_configuration": [],
                     "nic_teaming": "NoTeaming",
                     }},
        {"json_data": {"JobId": 1234},
         'message': INVALID_UNTAGGED.format(id=10, nic_id="NIC.Mezzanine.1A-1-1"), "success": True,
         'Devices': {"value": [{"Id": 123, "Identifier": "ABC1234"}]},
         "_get_profile": {
             "Id": "ABC1234",
             "ServerServiceTag": "ABC1234",
             "BondingTechnology": "NoTeaming"},
         "_get_interface": {
             "NIC.Mezzanine.1A-1-1": {
                 "NativeVLAN": 3,
                 "Networks": [
                     11569,
                     10155
                 ],
                 "NicBonded": False
             },
             "NIC.Mezzanine.1A-2-1": {
                 "NativeVLAN": 3,
                 "Networks": [
                     11569,
                     10155,
                     12350
                 ],
                 "NicBonded": False
             }},
         "vlan_map": {"testvlan": 10155, "VLAN 1": 11569, "range120-125": 12350, "range130-135": 12352, "two": 14679,
                      "three": 14681},
         "natives": {143: 10155, 1: 11569, 2: 14679, 3: 14681, 0: 0},
         'mparams': {"job_wait": False, "device_service_tag": ["ABC1234"],
                     "nic_configuration": [{
                         "nic_identifier": "NIC.Mezzanine.1A-1-1",
                         "tagged_networks": {
                             "names": ["testvlan"],
                             "state": "present"},
                         "team": False,
                         "untagged_network": 10},
                         {
                             "nic_identifier": "NIC.Mezzanine.1A-2-1",
                             "tagged_networks": {"names": ["range120-125"],
                                                 "state": "present"},
                             "team": True,
                             "untagged_network": 3}],
                     "nic_teaming": "NoTeaming",
                     }},
        {"json_data": {"JobId": 1234},
         'message': VLAN_NOT_FOUND.format(vlan_name='vlan_x'), "success": True,
         'Devices': {"value": [{"Id": 123, "Identifier": "ABC1234"}]},
         "_get_profile": {
             "Id": "ABC1234",
             "ServerServiceTag": "ABC1234",
             "BondingTechnology": "NoTeaming"},
         "_get_interface": {
             "NIC.Mezzanine.1A-1-1": {
                 "NativeVLAN": 3,
                 "Networks": [
                     11569,
                     10155
                 ],
                 "NicBonded": False
             },
             "NIC.Mezzanine.1A-2-1": {
                 "NativeVLAN": 3,
                 "Networks": [
                     11569,
                     10155,
                     12350
                 ],
                 "NicBonded": False
             }},
         "vlan_map": {"vlan": 10155, "VLAN 1": 11569, "range120-125": 12350, "range130-135": 12352, "two": 14679,
                      "three": 14681},
         "natives": {143: 10155, 1: 11569, 2: 14679, 3: 14681, 0: 0},
         'mparams': {"job_wait": False, "device_service_tag": ["ABC1234"],
                     "nic_configuration": [{
                         "nic_identifier": "NIC.Mezzanine.1A-1-1",
                         "tagged_networks": {
                             "names": ["vlan_x"],
                             "state": "present"},
                         "team": False,
                         "untagged_network": 3},
                         {
                             "nic_identifier": "NIC.Mezzanine.1A-2-1",
                             "tagged_networks": {"names": ["range120-125"],
                                                 "state": "present"},
                             "team": True,
                             "untagged_network": 3}],
                     "nic_teaming": "NoTeaming",
                     }},
        {"json_data": {"JobId": 1234},
         'message': NO_CHANGES_MSG, "success": True,
         'Devices': {"value": [{"Id": 123, "Identifier": "ABC1234"}]},
         "_get_profile": {
             "Id": "ABC1234",
             "ServerServiceTag": "ABC1234",
             "BondingTechnology": "NoTeaming"},
         "_get_interface": {
             "NIC.Mezzanine.1A-1-1": {
                 "NativeVLAN": 3,
                 "Networks": [
                     11569,
                     10155
                 ],
                 "NicBonded": False
             },
             "NIC.Mezzanine.1A-2-1": {
                 "NativeVLAN": 3,
                 "Networks": [
                     12350
                 ],
                 "NicBonded": False
             }},
         "vlan_map": {"testvlan": 10155, "VLAN 1": 11569, "range120-125": 12350, "range130-135": 12352, "two": 14679,
                      "three": 14681},
         "natives": {143: 10155, 1: 11569, 2: 14679, 3: 14681, 0: 0},
         'mparams': {"job_wait": False, "device_service_tag": ["ABC1234"],
                     "nic_configuration": [{
                         "nic_identifier": "NIC.Mezzanine.1A-1-1",
                         "tagged_networks": {
                             "names": ["testvlan", "VLAN 1"],
                             "state": "present"},
                         "team": False,
                         "untagged_network": 3},
                         {
                             "nic_identifier": "NIC.Mezzanine.1A-2-1",
                             "tagged_networks": {"names": ["range120-125"],
                                                 "state": "present"},
                             "team": False,
                             "untagged_network": 3}],
                     "nic_teaming": "NoTeaming",
                     }},
        {"json_data": {"JobId": 1234}, "check_mode": True,
         'message': CHANGES_MSG, "success": True,
         'Devices': {"value": [{"Id": 123, "Identifier": "ABC1234"}]},
         "_get_profile": {
             "Id": "ABC1234",
             "ServerServiceTag": "ABC1234",
             "BondingTechnology": "NoTeaming"},
         "_get_interface": {
             "NIC.Mezzanine.1A-1-1": {
                 "NativeVLAN": 3,
                 "Networks": [
                     11569
                 ],
                 "NicBonded": False
             },
             "NIC.Mezzanine.1A-2-1": {
                 "NativeVLAN": 3,
                 "Networks": [
                     11569
                 ],
                 "NicBonded": False
             }},
         "vlan_map": {"testvlan": 10155, "VLAN 1": 11569, "range120-125": 12350, "range130-135": 12352, "two": 14679,
                      "three": 14681},
         "natives": {143: 10155, 1: 11569, 2: 14679, 3: 14681, 0: 0},
         'mparams': {"job_wait": False, "device_service_tag": ["ABC1234"],
                     "nic_configuration": [{
                         "nic_identifier": "NIC.Mezzanine.1A-1-1",
                         "tagged_networks": {
                             "names": ["testvlan"],
                             "state": "present"},
                         "team": False,
                         "untagged_network": 3},
                         {
                             "nic_identifier": "NIC.Mezzanine.1A-2-1",
                             "tagged_networks": {"names": ["range120-125"],
                                                 "state": "present"},
                             "team": True,
                             "untagged_network": 3}],
                     "nic_teaming": "NoTeaming",
                     }},
        {"json_data": {"JobId": 1234},
         'message': DUPLICATE_NIC_IDENTIFIED, "success": True,
         'Devices': {"value": [{"Id": 123, "Identifier": "ABC1234"}]},
         "_get_profile": {
             "Id": "ABC1234",
             "ServerServiceTag": "ABC1234",
             "BondingTechnology": "NoTeaming"},
         "_get_interface": {
             "NIC.Mezzanine.1A-1-1": {
                 "NativeVLAN": 3,
                 "Networks": [
                     11569,
                     10155
                 ],
                 "NicBonded": False
             },
             "NIC.Mezzanine.1A-2-1": {
                 "NativeVLAN": 2,
                 "Networks": [
                     11569,
                     10155,
                     12350
                 ],
                 "NicBonded": False
             }},
         "vlan_map": {"testvlan": 10155, "VLAN 1": 11569, "range120-125": 12350, "range130-135": 12352, "two": 14679,
                      "three": 14681},
         "natives": {143: 10155, 1: 11569, 2: 14679, 3: 14681, 0: 0},
         'mparams': {"job_wait": False, "device_service_tag": ["ABC1234"],
                     "nic_configuration": [{
                         "nic_identifier": "NIC.Mezzanine.1A-1-1",
                         "tagged_networks": {
                             "names": ["testvlan"],
                             "state": "present"},
                         "team": False,
                         "untagged_network": 3},
                         {
                             "nic_identifier": "NIC.Mezzanine.1A-1-1",
                             "tagged_networks": {"names": ["range120-125"],
                                                 "state": "present"},
                             "team": True,
                             "untagged_network": 3}],
                     "nic_teaming": "NoTeaming",
                     }},
        {"json_data":
         {"Id": 14808,
          "JobId": 1234,
          "JobName": "Server profile(s) configuration task",
          "JobDescription": "Applies bonding technology to profile and networks to NICs.",
          "Value": "Successfully Applied bonding technology to profile and networks to NICs.",
          "LastRunStatus": {
              "@odata.type": "#JobService.JobStatus",
              "Id": 2060,
              "Name": "Completed"
          },
          },
         'message': "Successfully Applied bonding technology to profile and networks to NICs.", "success": True,
         'Devices': {"value": [{"Id": 123, "Identifier": "ABC1234"}]},
         "_get_profile": {
             "Id": "ABC1234",
             "ServerServiceTag": "ABC1234",
             "BondingTechnology": "NoTeaming"},
         "_get_interface": {
             "NIC.Mezzanine.1A-1-1": {
                 "NativeVLAN": 3,
                 "Networks": [
                     11569,
                     10155
                 ],
                 "NicBonded": False
             },
             "NIC.Mezzanine.1A-2-1": {
                 "NativeVLAN": 2,
                 "Networks": [
                     11569,
                     10155,
                     12350
                 ],
                 "NicBonded": False
             }},
         "vlan_map": {"testvlan": 10155, "VLAN 1": 11569, "range120-125": 12350, "range130-135": 12352, "two": 14679,
                      "three": 14681},
         "natives": {143: 10155, 1: 11569, 2: 14679, 3: 14681, 0: 0},
         'mparams': {"device_service_tag": ["ABC1234"],
                     "nic_configuration": [{
                         "nic_identifier": "NIC.Mezzanine.1A-1-1",
                         "tagged_networks": {
                             "names": ["testvlan"],
                             "state": "present"},
                         "team": False,
                         "untagged_network": 3},
                         {
                             "nic_identifier": "NIC.Mezzanine.1A-2-1",
                             "tagged_networks": {"names": ["range120-125"],
                                                 "state": "present"},
                             "team": True,
                             "untagged_network": 3}],
                     "nic_teaming": "NoTeaming",
                     }},
        {"json_data": {
            "Id": 14808,
            "JobId": 1234,
            "JobName": "Server profile(s) configuration task",
            "JobDescription": "Applies bonding technology to profile and networks to NICs.",
            "Value": 1234,  # to cause exception
            "LastRunStatus": {
                "@odata.type": "#JobService.JobStatus",
                "Id": 2060,
                "Name": "Completed"
            },
        },
            'message': "Applies bonding technology to profile and networks to NICs.", "success": True,
            'Devices': {"value": [{"Id": 123, "Identifier": "ABC1234"}]},
            "_get_profile": {
                "Id": "ABC1234",
                "ServerServiceTag": "ABC1234",
                "BondingTechnology": "NoTeaming"},
            "_get_interface": {
                "NIC.Mezzanine.1A-1-1": {
                    "NativeVLAN": 3,
                    "Networks": [
                        11569,
                        10155
                    ],
                    "NicBonded": False
                },
                "NIC.Mezzanine.1A-2-1": {
                    "NativeVLAN": 2,
                    "Networks": [
                        11569,
                        10155,
                        12350
                    ],
                    "NicBonded": False
                }},
            "vlan_map": {"testvlan": 10155, "VLAN 1": 11569, "range120-125": 12350, "range130-135": 12352, "two": 14679,
                         "three": 14681},
            "natives": {143: 10155, 1: 11569, 2: 14679, 3: 14681, 0: 0},
            'mparams': {"device_service_tag": ["ABC1234"],
                        "nic_configuration": [{
                            "nic_identifier": "NIC.Mezzanine.1A-1-1",
                            "tagged_networks": {
                                "names": ["testvlan"],
                                "state": "present"},
                            "team": False,
                            "untagged_network": 3},
                            {
                                "nic_identifier": "NIC.Mezzanine.1A-2-1",
                                "tagged_networks": {"names": ["range120-125"],
                                                    "state": "present"},
                                "team": True,
                                "untagged_network": 3}],
                        "nic_teaming": "NoTeaming",
                        }}
    ])
    def test_ome_sips_success_case(
            self,
            params,
            ome_connection_mock_for_sips,
            ome_response_mock,
            ome_default_args,
            mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['json_data']
        ome_connection_mock_for_sips.get_all_items_with_pagination.return_value = params[
            'Devices']
        mocker.patch(
            MODULE_PATH +
            '_get_profile',
            return_value=params.get(
                '_get_profile',
                {}))
        mocker.patch(
            MODULE_PATH +
            '_get_interface',
            return_value=params.get(
                '_get_interface',
                {}))
        mocker.patch(
            MODULE_PATH + 'get_vlan_ids',
            return_value=(
                params.get('vlan_map'),
                params.get('natives')))
        ome_default_args.update(params['mparams'])
        result = self._run_module(
            ome_default_args, check_mode=params.get(
                'check_mode', False))
        assert result['msg'] == params['message']

    @pytest.mark.parametrize("params",
                             [{"json_data": {"Id": "ABC1234",
                                             "ServerServiceTag": "ABC1234",
                                             "BondingTechnology": "NoTeaming"},
                               "service_tag": "ABC1234"}])
    def test_ome_get_profile(
            self,
            params,
            ome_connection_mock_for_sips,
            ome_response_mock,
            ome_default_args,
            mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['json_data']
        f_module = self.get_module_mock(ome_default_args)
        result = self.module._get_profile(
            f_module,
            ome_connection_mock_for_sips,
            params.get("service_tag"))
        assert result["Id"] == params.get("service_tag")

    @pytest.mark.parametrize("params", [
        {"json_data": {
            "@odata.context": "/api/$metadata#Collection(NetworkService.ServerInterfaceProfile)",
            "@odata.count": 2,
            "value": [
                {
                    "Id": "NIC.Mezzanine.1A-1-1",
                    "OnboardedPort": "59HW8X2:ethernet1/1/1",
                    "NativeVLAN": 3,
                    "NicBonded": False,
                    "FabricId": "f918826e-2515-4967-98f4-5488e810ca2e",
                    "Networks@odata.count": 2,
                    "Networks": [
                        {
                            "Id": 10155,
                            "Name": "testvlan",
                            "Description": None,
                            "VlanMaximum": 143,
                            "VlanMinimum": 143,
                            "Type": 1,
                        },
                        {
                            "Id": 11569,
                            "Name": "VLAN 1",
                            "Description": "VLAN 1",
                            "VlanMaximum": 1,
                            "VlanMinimum": 1,
                            "Type": 2,
                        }
                    ]
                },
                {
                    "Id": "NIC.Mezzanine.1A-2-1",
                    "OnboardedPort": "6H7J6Z2:ethernet1/1/1",
                    "NativeVLAN": 3,
                    "NicBonded": False,
                    "FabricId": "f918826e-2515-4967-98f4-5488e810ca2e",
                    "Networks@odata.count": 3,
                    "Networks": [
                        {
                            "Id": 10155,
                            "Name": "testvlan",
                            "Description": None,
                            "VlanMaximum": 143,
                            "VlanMinimum": 143,
                            "Type": 1,
                        },
                        {
                            "Id": 11569,
                            "Name": "VLAN 1",
                            "Description": "VLAN 1",
                            "VlanMaximum": 1,
                            "VlanMinimum": 1,
                            "Type": 2,
                        },
                        {
                            "Id": 12350,
                            "Name": "range120-125",
                            "Description": None,
                            "VlanMaximum": 125,
                            "VlanMinimum": 120,
                            "Type": 3,
                        }
                    ]
                }
            ]
        },
            "service_tag": "ABC1234", "intrfc": {
            "NIC.Mezzanine.1A-1-1": {
                "NativeVLAN": 3,
                "Networks": {
                    11569,
                    10155
                },
                "NicBonded": False
            },
            "NIC.Mezzanine.1A-2-1": {
                "NativeVLAN": 3,
                "Networks": {
                    11569,
                    10155,
                    12350
                },
                "NicBonded": False
            }
        }}])
    def test_ome_get_interface(
            self,
            params,
            ome_connection_mock_for_sips,
            ome_response_mock,
            ome_default_args,
            mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['json_data']
        f_module = self.get_module_mock(ome_default_args)
        result = self.module._get_interface(
            f_module,
            ome_connection_mock_for_sips,
            params.get("service_tag"))
        assert result == params.get("intrfc")

    @pytest.mark.parametrize("params",
                             [{"json_data": {"@odata.context": "/api/$metadata#Collection(NetworkConfigurationService.Network)",
                                             "@odata.count": 6,
                                             "value": [{"Id": 10155,
                                                        "Name": "testvlan",
                                                        "VlanMaximum": 143,
                                                        "VlanMinimum": 143,
                                                        "Type": 1,
                                                        },
                                                       {"Id": 11569,
                                                        "Name": "VLAN 1",
                                                        "Description": "VLAN 1",
                                                        "VlanMaximum": 1,
                                                        "VlanMinimum": 1,
                                                        "Type": 2,
                                                        },
                                                       {"Id": 12350,
                                                        "Name": "range120-125",
                                                        "VlanMaximum": 125,
                                                        "VlanMinimum": 120,
                                                        "Type": 3,
                                                        },
                                                       {"Id": 12352,
                                                        "Name": "range130-135",
                                                        "VlanMaximum": 135,
                                                        "VlanMinimum": 130,
                                                        "Type": 4,
                                                        },
                                                       {"Id": 14679,
                                                        "Name": "two",
                                                        "VlanMaximum": 2,
                                                        "VlanMinimum": 2,
                                                        "Type": 1,
                                                        },
                                                       {"Id": 14681,
                                                        "Name": "three",
                                                        "VlanMaximum": 3,
                                                        "VlanMinimum": 3,
                                                        "Type": 3,
                                                        }]},
                                 "vlan_map": {"testvlan": 10155,
                                              "VLAN 1": 11569,
                                              "range120-125": 12350,
                                              "range130-135": 12352,
                                              "two": 14679,
                                              "three": 14681},
                                 "natives": {143: 10155,
                                             1: 11569,
                                             2: 14679,
                                             3: 14681,
                                             0: 0}}])
    def test_ome_get_vlan_ids(
            self,
            params,
            ome_connection_mock_for_sips,
            ome_response_mock,
            ome_default_args,
            mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['json_data']
        vlan_map, natives = self.module.get_vlan_ids(
            ome_connection_mock_for_sips)
        assert vlan_map == params.get("vlan_map")
        assert natives == params.get("natives")

    @pytest.mark.parametrize("exc_type",
                             [IOError,
                              ValueError,
                              SSLError,
                              TypeError,
                              ConnectionError,
                              HTTPError,
                              URLError])
    def test_ome_sips_main_exception_failure_case(
            self,
            exc_type,
            mocker,
            ome_default_args,
            ome_connection_mock_for_sips,
            ome_response_mock):
        ome_default_args.update({"device_service_tag": ["SRV1234"],
                                 "nic_configuration": [{'nic_identifier': "NIC1"}]})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(
                MODULE_PATH + 'get_valid_service_tags',
                side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(
                MODULE_PATH + 'get_valid_service_tags',
                side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'get_valid_service_tags',
                         side_effect=exc_type('https://testhost.com',
                                              400,
                                              'http error message',
                                              {"accept-type": "application/json"},
                                              StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result
