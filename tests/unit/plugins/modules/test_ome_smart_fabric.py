# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.0.0
# Copyright (C) 2020-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import ome_smart_fabric
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text

CHECK_MODE_CHANGE_FOUND_MSG = "Changes found to be applied."
CHECK_MODE_CHANGE_NOT_FOUND_MSG = "No Changes found to be applied."
FABRIC_NOT_FOUND_ERROR_MSG = "The smart fabric '{0}' is not present in the system."
DOMAIN_SERVICE_TAG_ERROR_MSG = "Unable to retrieve the domain information because the" \
                               " domain of the provided service tag {0} is not available."
LEAD_CHASSIS_ERROR_MSG = "System should be a lead chassis if the assigned fabric topology type is {0}."
SYSTEM_NOT_SUPPORTED_ERROR_MSG = "Fabric management is not supported on the specified system."
DESIGN_MODEL_ERROR_MSG = "The network type of the {0} must be {1}."
DEVICE_SERVICE_TAG_TYPE_ERROR_MSG = "The {0} type must be {1}."
DEVICE_SERVICE_TAG_NOT_FOUND_ERROR_MSG = "Unable to retrieve the device information because the device" \
                                         " with the provided service tag {0} is not available."
IDEMPOTENCY_MSG = "Specified fabric details are the same as the existing settings."
REQUIRED_FIELD = "Options 'fabric_design', 'primary_switch_service_tag' and 'secondary_switch_service_tag'" \
                 " are required for fabric creation."
DUPLICATE_TAGS = "The switch details of the primary switch overlaps with the secondary switch details."
PRIMARY_SWITCH_OVERLAP_MSG = "The primary switch service tag is overlapping with existing secondary switch details."
SECONDARY_SWITCH_OVERLAP_MSG = "The switch details of the secondary switch overlaps with the existing primary" \
                               " switch details."
MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
device_details = {
    "Id": Constants.device_id1,
    "Type": 4000,
    "Identifier": "GTCT8T2",
    "DeviceServiceTag": "GTCT8T2",
    "ChassisServiceTag": "FPTN6Z2",
    "Model": "MX9116n Fabric Engine",
    "PowerState": 17,
    "ManagedState": 3000,
    "Status": 1000,
    "SystemId": 2031,
    "DeviceName": "IOM-A2",
    "SlotConfiguration": {
        "ChassisName": "MX-FPTN6Z2",
        "SlotId": "13313",
        "DeviceType": "4000",
        "ChassisId": "13294",
        "SlotNumber": "2",
        "SledBlockPowerOn": "null",
        "SlotName": "IOM-A2",
        "ChassisServiceTag": "FPTN6Z2",
        "SlotType": "4000"
    },
    "DeviceManagement": [
        {
            "ManagementId": 76383,
            "NetworkAddress": Constants.hostname1,
            "MacAddress": "00:00:00:00:00",
            "ManagementType": 2,
            "InstrumentationName": "MX9116n Fabric Engine",
            "DnsName": "",
            "ManagementProfile": [
                {
                    "ManagementProfileId": 76383,
                    "ProfileId": "FX7_BASE",
                    "ManagementId": 76383,
                    "AgentName": "",
                    "Version": "",
                    "ManagementURL": "",
                    "HasCreds": 0,
                    "Status": 1000,
                    "StatusDateTime": "2020-05-07 15:00:14.718"
                }
            ]
        }
    ]
}
all_fabric_details = [
    {
        "Id": "1312cceb-c3dd-4348-95c1-d8541a17d776",
        "Name": "Fabric_1",
        "Description": "create new fabric1",
        "OverrideLLDPConfiguration": "NA",
        "ScaleVLANProfile": "NA",
        "FabricDesignMapping": [
            {
                "DesignNode": "Switch-A",
                "PhysicalNode": "2HB7NX2"
            },
            {
                "DesignNode": "Switch-B",
                "PhysicalNode": "2HBFNX2"
            }
        ],
        "FabricDesign": {
            "@odata.id": "/api/NetworkService/Fabrics('1312cceb-c3dd-4348-95c1-d8541a17d776')/FabricDesign"
        }
    },
    {
        "Id": "1312cceb-c3dd-4348-95c1-123456",
        "Name": "Fabric_1_2",
        "Description": "create new fabric2",
        "OverrideLLDPConfiguration": "Enabled",
        "ScaleVLANProfile": "NA",
        "FabricDesignMapping": [
            {
                "DesignNode": "Switch-A",
                "PhysicalNode": Constants.service_tag1
            },
            {
                "DesignNode": "Switch-B",
                "PhysicalNode": Constants.service_tag2
            }
        ],
        "FabricDesign": {
            "@odata.id": "/api/NetworkService/Fabrics('1312cceb-c3dd-4348-95c1-123456')/FabricDesign"
        }
    }
]


@pytest.fixture
def ome_connection_mock_for_smart_fabric(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'ome_smart_fabric.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeSmartFabric(FakeAnsibleModule):
    module = ome_smart_fabric

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_main_ome_smart_fabric_exception_handling_case(self, exc_type, ome_default_args,
                                                           ome_connection_mock_for_smart_fabric,
                                                           ome_response_mock, mocker):
        ome_default_args.update({"name": "name", "new_name": "new_name"})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'ome_smart_fabric.fabric_actions',
                         side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'ome_smart_fabric.fabric_actions',
                         side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            for status_code, msg in {501: SYSTEM_NOT_SUPPORTED_ERROR_MSG, 400: 'http error message'}.items():
                mocker.patch(MODULE_PATH + 'ome_smart_fabric.fabric_actions',
                             side_effect=exc_type('http://testhost.com', status_code, msg,
                                                  {"accept-type": "application/json"}, StringIO(json_str)))
                result = self._run_module_with_fail_json(ome_default_args)
                assert result['failed'] is True
                assert msg in result['msg']
        assert 'msg' in result

    def test_get_msm_device_details_success_case(self, ome_connection_mock_for_smart_fabric, ome_default_args, mocker):
        """
        success case: when provided design type and role type natches return the service tag and msm details
        """
        ome_default_args.update({"fabric_design": "2xMX9116n_Fabric_Switching_Engines_in_different_chassis"})
        f_module = self.get_module_mock(params=ome_default_args)
        resp_data = {
            "Id": Constants.device_id1,
            "value": [
                {
                    "Id": 10086,
                    "DeviceId": 10061,
                    "PublicAddress": [
                        ome_default_args["hostname"],
                        "1000:mock_val"
                    ],
                    "Identifier": Constants.service_tag1,
                    "DomainRoleTypeValue": "LEAD",
                    "Version": "1.20.00",
                },
                {
                    "Id": 13341,
                    "DeviceId": 13294,
                    "PublicAddress": [
                        Constants.hostname2,
                        "1000:mocked_val"
                    ],
                    "Identifier": Constants.service_tag2,
                    "DomainTypeValue": "MSM",
                    "DomainRoleTypeValue": "MEMBER",
                    "Version": "1.20.00",
                }
            ]
        }
        ome_connection_mock_for_smart_fabric.get_all_items_with_pagination.return_value = resp_data
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.get_service_tag_with_fqdn',
                     return_value=None)
        service_tag, msm_version = self.module.get_msm_device_details(ome_connection_mock_for_smart_fabric, f_module)
        assert service_tag == Constants.service_tag1
        assert msm_version == "1.20.00"

    def test_get_msm_device_details_fqdn_success_case1(self, ome_connection_mock_for_smart_fabric, ome_default_args,
                                                       mocker):
        """
        when hostname provided is fqdn and
        success case: when provided design type and role type matches return the service tag and msm details
        """
        ome_default_args.update(
            {"hostname": "XX-XXXX.yyy.lab", "fabric_design": "2xMX9116n_Fabric_Switching_Engines_in_different_chassis"})
        f_module = self.get_module_mock(params=ome_default_args)
        resp_data = {
            "Id": Constants.device_id1,
            "value": [
                {
                    "Id": 10086,
                    "DeviceId": 10061,
                    "PublicAddress": [
                        ome_default_args["hostname"],
                        "1000:mock_val"
                    ],
                    "Identifier": Constants.service_tag1,
                    "DomainRoleTypeValue": "LEAD",
                    "Version": "1.20.00",
                },
                {
                    "Id": 13341,
                    "DeviceId": 13294,
                    "PublicAddress": [
                        Constants.hostname2,
                        "1000:mocked_val"
                    ],
                    "Identifier": Constants.service_tag2,
                    "DomainTypeValue": "MSM",
                    "DomainRoleTypeValue": "MEMBER",
                    "Version": "1.20.00",
                }
            ]
        }
        ome_connection_mock_for_smart_fabric.get_all_items_with_pagination.return_value = resp_data
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.get_service_tag_with_fqdn',
                     return_value="FKMLRZ2")
        service_tag, msm_version = self.module.get_msm_device_details(ome_connection_mock_for_smart_fabric, f_module)
        assert service_tag == Constants.service_tag1
        assert msm_version == "1.20.00"

    def test_get_msm_device_details_fqdn_success_case2(self, ome_connection_mock_for_smart_fabric, ome_default_args,
                                                       mocker):
        """
        when hostname provided is fqdn and
        success case: when provided design type is same and fqdn is not of lead type
        """
        ome_default_args.update(
            {"hostname": "XX-XXXX.yyy.lab", "fabric_design": "2xMX5108n_Ethernet_Switches_in_same_chassis"})
        f_module = self.get_module_mock(params=ome_default_args)
        resp_data = {
            "Id": Constants.device_id1,
            "value": [
                {
                    "Id": 10086,
                    "DeviceId": 10061,
                    "PublicAddress": [
                        Constants.hostname1,
                        "1000:mock_ipv6"
                    ],
                    "Identifier": Constants.service_tag1,
                    "DomainRoleTypeValue": "LEAD",
                    "Version": "1.20.00",
                },
                {
                    "Id": 13341,
                    "DeviceId": 13294,
                    "PublicAddress": [
                        Constants.hostname2,
                        "1001:mocked_ippv6"
                    ],
                    "Identifier": Constants.service_tag2,
                    "DomainTypeValue": "MSM",
                    "DomainRoleTypeValue": "MEMBER",
                    "Version": "1.20.10",
                }
            ]
        }
        ome_connection_mock_for_smart_fabric.get_all_items_with_pagination.return_value = resp_data
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.get_service_tag_with_fqdn',
                     return_value=Constants.service_tag2)
        service_tag, msm_version = self.module.get_msm_device_details(ome_connection_mock_for_smart_fabric, f_module)
        assert service_tag == Constants.service_tag2
        assert msm_version == "1.20.10"

    def test_get_msm_device_details_fqdn_failure_case1(self, ome_connection_mock_for_smart_fabric, ome_default_args,
                                                       mocker):
        """
        when hostname provided is fqdn and
        failure case: when provided design type is 2xMX9116n_Fabric_Switching_Engines_in_different_chassis
         but fqdn is not of lead type
        """
        ome_default_args.update(
            {"hostname": "XX-XXXX.yyy.lab", "fabric_design": "2xMX9116n_Fabric_Switching_Engines_in_different_chassis"})
        f_module = self.get_module_mock(params=ome_default_args)
        resp_data = {
            "Id": Constants.device_id1,
            "value": [
                {
                    "Id": 10086,
                    "DeviceId": 10061,
                    "PublicAddress": [
                        Constants.hostname1,
                        "1000:mock_val"
                    ],
                    "Identifier": Constants.service_tag1,
                    "DomainRoleTypeValue": "LEAD",
                    "Version": "1.20.00",
                },
                {
                    "Id": 13341,
                    "DeviceId": 13294,
                    "PublicAddress": [
                        Constants.hostname2,
                        "1000:mocked_val"
                    ],
                    "Identifier": Constants.service_tag2,
                    "DomainTypeValue": "MSM",
                    "DomainRoleTypeValue": "MEMBER",
                    "Version": "1.20.00",
                }
            ]
        }
        ome_connection_mock_for_smart_fabric.get_all_items_with_pagination.return_value = resp_data
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.get_service_tag_with_fqdn',
                     return_value=Constants.service_tag2)
        with pytest.raises(Exception, match=LEAD_CHASSIS_ERROR_MSG.format(ome_default_args["fabric_design"])) as ex:
            self.module.get_msm_device_details(ome_connection_mock_for_smart_fabric, f_module)

    def test_get_msm_device_details_fqdn_failure_case2(self, ome_connection_mock_for_smart_fabric, ome_default_args,
                                                       mocker):
        """
        when hostname provided is fqdn and
        failure case: when provided fqdn not available in domain list should throw an error
        """
        ome_default_args.update(
            {"hostname": "XX-XXXX.yyy.lab", "fabric_design": "2xMX9116n_Fabric_Switching_Engines_in_different_chassis"})
        f_module = self.get_module_mock(params=ome_default_args)
        resp_data = {
            "value": [
            ]
        }
        ome_connection_mock_for_smart_fabric.get_all_items_with_pagination.return_value = resp_data
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.get_service_tag_with_fqdn',
                     return_value="FPTN6Z2")
        with pytest.raises(Exception, match=SYSTEM_NOT_SUPPORTED_ERROR_MSG):
            self.module.get_msm_device_details(ome_connection_mock_for_smart_fabric, f_module)

    def test_get_msm_device_details_failure_case_01(self, ome_connection_mock_for_smart_fabric, ome_default_args,
                                                    mocker):
        """
        raise exception if design type is 2xMX9116n_Fabric_Switching_Engines_in_different_chassis but domain type is not lead
        """
        ome_default_args.update({"fabric_design": "2xMX9116n_Fabric_Switching_Engines_in_different_chassis"})
        f_module = self.get_module_mock(params=ome_default_args)
        resp_data = {"Id": Constants.device_id1, "value": [
            {
                "@odata.id": "/api/ManagementDomainService/Domains(25038)",
                "Id": 25038,
                "DeviceId": Constants.device_id1,
                "PublicAddress": [
                    ome_default_args["hostname"]
                ],
                "Name": "MX-2H5DNX2",
                "Description": "PowerEdge MX7000",
                "Identifier": Constants.service_tag1,
                "DomainTypeId": 4000,
                "DomainTypeValue": "MSM",
                "DomainRoleTypeId": 3002,
                "DomainRoleTypeValue": "STANDALONE",
                "Version": "1.20.00",
                "Local": True,
                "GroupId": "d78ba475-f5d5-4dbb-97da-b4b1f190caa2",
                "GroupName": None,
                "BackupLead": False,
                "Capabilities": [],
                "BackupLeadHealth": 2000
            }
        ]}
        ome_connection_mock_for_smart_fabric.get_all_items_with_pagination.return_value = resp_data
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.get_service_tag_with_fqdn',
                     return_value=None)
        with pytest.raises(Exception, match=LEAD_CHASSIS_ERROR_MSG.format(ome_default_args["fabric_design"])) as ex:
            self.module.get_msm_device_details(ome_connection_mock_for_smart_fabric, f_module)

    def test_get_msm_device_details_failure_case_02(self, ome_connection_mock_for_smart_fabric, ome_default_args,
                                                    mocker):
        """
        raise exception if there is no domain values in system
        """
        ome_default_args.update({"fabric_design": "2xMX9116n_Fabric_Switching_Engines_in_different_chassis"})
        f_module = self.get_module_mock(params=ome_default_args)
        resp_data = {"Id": None, "value": [
        ]}
        ome_connection_mock_for_smart_fabric.get_all_items_with_pagination.return_value = resp_data
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.get_service_tag_with_fqdn',
                     return_value=None)
        with pytest.raises(Exception, match=SYSTEM_NOT_SUPPORTED_ERROR_MSG):
            self.module.get_msm_device_details(ome_connection_mock_for_smart_fabric, f_module)

    @pytest.mark.parametrize("modify_payload", [
        {"Name": "Fabric-2"},
        {"Name": "Fabric-1", "Description": "This is a fabric1."},
        {"FabricDesignMapping": [
            {
                "DesignNode": "Switch-A",
                "PhysicalNode": Constants.service_tag1
            },
            {
                "DesignNode": "Switch-B",
                "PhysicalNode": Constants.service_tag2
            }
        ], },
        {
            "FabricDesign": {
                "Name": "2xMX9116n_Fabric_Switching_Engines_in_different_chassis"
            }
        }
    ])
    def test_compare_payloads_diff_case_01(self, modify_payload):
        current_payload = {
            "Id": "8f25f714-9ea8-48e9-8eac-162d5d842e9f",
            "Name": "Fabric-1",
            "Description": "This is a fabric.",
            "FabricDesignMapping": [
                {
                    "DesignNode": "Switch-A",
                    "PhysicalNode": "2HB7NX2"
                },
                {
                    "DesignNode": "Switch-B",
                    "PhysicalNode": "2HBFNX2"
                }
            ],
            "FabricDesign": {
                "Name": "2xMX5108n_Ethernet_Switches_in_same_chassis"
            }
        }
        diff = self.module.compare_payloads(modify_payload, current_payload)
        assert diff is True

    @pytest.mark.parametrize("current_payload", [
        {"Name": "Fabric-1", "Description": "This is a fabric1."},
        {"Name": "Fabric-1", "Description": "This is a fabric.", "FabricDesignMapping": [
            {
                "DesignNode": "Switch-A",
                "PhysicalNode": Constants.service_tag1
            },
            {
                "DesignNode": "Switch-B",
                "PhysicalNode": Constants.service_tag2
            }
        ], "FabricDesign": {
            "Name": "2xMX5108n_Ethernet_Switches_in_same_chassis"
        }}])
    def test_compare_payloads_diff_case_02(self, current_payload):
        modify_payload = {
            "Id": "8f25f714-9ea8-48e9-8eac-162d5d842e9f",
            "Name": "Fabric-1",
            "Description": "This is a fabric.",
            "FabricDesignMapping": [
                {
                    "DesignNode": "Switch-A",
                    "PhysicalNode": "2HB7NX2"
                },
                {
                    "DesignNode": "Switch-B",
                    "PhysicalNode": "2HBFNX2"
                }
            ],
            "FabricDesign": {
                "Name": "2xMX5108n_Ethernet_Switches_in_same_chassis"
            }
        }
        diff = self.module.compare_payloads(modify_payload, current_payload)
        assert diff is True

    @pytest.mark.parametrize("modify_payload", [
        {"Name": "Fabric-1", "Id": "8f25f714-9ea8-48e9-8eac-162d5d842e9f"},
        {"Name": "Fabric-1", "Description": "This is a fabric.", "Id": "8f25f714-9ea8-48e9-8eac-162d5d842e9f", },
        {"Id": "8f25f714-9ea8-48e9-8eac-162d5d842e9f", "Name": "Fabric-1", "FabricDesignMapping": [
            {
                "DesignNode": "Switch-A",
                "PhysicalNode": Constants.service_tag1
            },
            {
                "DesignNode": "Switch-B",
                "PhysicalNode": Constants.service_tag2
            }
        ], },
        {
            "Id": "8f25f714-9ea8-48e9-8eac-162d5d842e9f",
            "Name": "Fabric-1",
            "FabricDesign": {
                "Name": "2xMX5108n_Ethernet_Switches_in_same_chassis"
            }
        },
        {
            "Id": "8f25f714-9ea8-48e9-8eac-162d5d842e9f",
            "Name": "Fabric-1",
            "Description": "This is a fabric.",
            "FabricDesignMapping": [
                {
                    "DesignNode": "Switch-A",
                    "PhysicalNode": Constants.service_tag1
                },
                {
                    "DesignNode": "Switch-B",
                    "PhysicalNode": Constants.service_tag2
                }
            ],
            "FabricDesign": {
                "Name": "2xMX5108n_Ethernet_Switches_in_same_chassis"
            }
        }
    ])
    def test_compare_payloads_no_diff_case_01(self, modify_payload):
        current_payload = {
            "Id": "8f25f714-9ea8-48e9-8eac-162d5d842e9f",
            "Name": "Fabric-1",
            "Description": "This is a fabric.",
            "FabricDesignMapping": [
                {
                    "DesignNode": "Switch-A",
                    "PhysicalNode": Constants.service_tag1
                },
                {
                    "DesignNode": "Switch-B",
                    "PhysicalNode": Constants.service_tag2
                }
            ],
            "FabricDesign": {
                "Name": "2xMX5108n_Ethernet_Switches_in_same_chassis"
            }
        }
        val = self.module.compare_payloads(modify_payload, current_payload)
        print(val)
        assert val is False

    @pytest.mark.parametrize('val', [(True, CHECK_MODE_CHANGE_FOUND_MSG), (False, CHECK_MODE_CHANGE_NOT_FOUND_MSG)])
    def test_idempotency_check_for_state_present_modify_check_mode_case01(self, mocker, val):
        f_module = self.get_module_mock(params={}, check_mode=True)
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.compare_payloads',
                     return_value=val[0])
        with pytest.raises(Exception, match=val[1]):
            self.module.idempotency_check_for_state_present("8f25f714-9ea8-48e9-8eac-162d5d842e9f",
                                                            {}, {},
                                                            f_module)

    def test_idempotency_check_for_state_present_modify_non_check_mode_case01(self, mocker):
        f_module = self.get_module_mock(params={}, check_mode=False)
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.compare_payloads',
                     return_value=False)
        with pytest.raises(Exception, match=IDEMPOTENCY_MSG):
            self.module.idempotency_check_for_state_present("8f25f714-9ea8-48e9-8eac-162d5d842e9f",
                                                            {}, {},
                                                            f_module)

    def test_idempotency_check_for_state_present_create_non_check_mode_case01(self, mocker):
        f_module = self.get_module_mock(params={}, check_mode=True)
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.compare_payloads',
                     return_value=False)
        with pytest.raises(Exception, match=CHECK_MODE_CHANGE_FOUND_MSG):
            self.module.idempotency_check_for_state_present(None,
                                                            {}, {},
                                                            f_module)

    def test_design_node_dict_update_case_01(self):
        design_node_map = [
            {
                "DesignNode": "Switch-A",
                "PhysicalNode": Constants.service_tag1
            },
            {
                "DesignNode": "Switch-B",
                "PhysicalNode": Constants.service_tag2
            }
        ]
        val = self.module.design_node_dict_update(design_node_map)
        assert val == {
            'PhysicalNode1': Constants.service_tag1,
            'PhysicalNode2': Constants.service_tag2
        }

    def test_design_node_dict_update_case_02(self):
        design_node_map = [
            {
                "DesignNode": "Switch-B",
                "PhysicalNode": Constants.service_tag2
            }
        ]
        val = self.module.design_node_dict_update(design_node_map)
        assert val == {
            'PhysicalNode2': Constants.service_tag2
        }

    def test_design_node_dict_update_case_03(self):
        design_node_map = [
            {
                "DesignNode": "Switch-B",
                "PhysicalNode": Constants.service_tag2
            }
        ]
        val = self.module.design_node_dict_update(design_node_map)
        assert val == {
            'PhysicalNode2': Constants.service_tag2
        }

    @pytest.mark.parametrize("modify_payload", [
        {
            'PhysicalNode1': Constants.service_tag2,
            'PhysicalNode2': "XYZ"
        },
        {
            'PhysicalNode1': Constants.service_tag2,
        }
    ])
    def test_validate_switches_overlap_case_01(self, modify_payload):
        current_dict = {
            'PhysicalNode1': Constants.service_tag1,
            'PhysicalNode2': Constants.service_tag2
        }
        modify_dict = modify_payload
        f_module = self.get_module_mock(params={"primary_switch_service_tag": Constants.service_tag2,
                                                "secondary_switch_service_tag": "XYZ"
                                                })
        with pytest.raises(Exception, match=PRIMARY_SWITCH_OVERLAP_MSG):
            self.module.validate_switches_overlap(current_dict, modify_dict, f_module)

    @pytest.mark.parametrize("modify_payload", [
        {
            'PhysicalNode1': "XYZ",
            'PhysicalNode2': Constants.service_tag1
        },
        {
            'PhysicalNode2': Constants.service_tag1
        }
    ])
    def test_validate_switches_overlap_case_02(self, modify_payload):
        current_dict = {
            'PhysicalNode1': Constants.service_tag1,
            'PhysicalNode2': Constants.service_tag2
        }
        modify_dict = modify_payload
        f_module = self.get_module_mock(params={"primary_switch_service_tag": "XYZ",
                                                "secondary_switch_service_tag": Constants.service_tag1
                                                })
        with pytest.raises(Exception, match=SECONDARY_SWITCH_OVERLAP_MSG):
            self.module.validate_switches_overlap(current_dict, modify_dict, f_module)

    def test_validate_switches_overlap_case_03(self):
        """
        interchanging switches should be allowed
        """
        current_dict = {
            'PhysicalNode1': Constants.service_tag1,
            'PhysicalNode2': Constants.service_tag2
        }
        modify_dict = {
            'PhysicalNode1': Constants.service_tag2,
            'PhysicalNode2': Constants.service_tag1
        }
        f_module = self.get_module_mock(params={"primary_switch_service_tag": Constants.service_tag2,
                                                "secondary_switch_service_tag": Constants.service_tag1
                                                })
        self.module.validate_switches_overlap(current_dict, modify_dict, f_module)

    def test_fabric_design_map_payload_creation_case01(self, mocker):
        modify_payload = [
            {
                "DesignNode": "Switch-A",
                "PhysicalNode": Constants.service_tag1
            },
            {
                "DesignNode": "Switch-B",
                "PhysicalNode": Constants.service_tag2
            }
        ]
        current_payload = [
            {
                "DesignNode": "Switch-A",
                "PhysicalNode": "xyz123"
            },
            {
                "DesignNode": "Switch-B",
                "PhysicalNode": "abc456"
            }
        ]
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.validate_switches_overlap', return_value=None)
        f_module = self.get_module_mock(params={})
        design_map = self.module.fabric_design_map_payload_creation(modify_payload, current_payload, f_module)
        assert design_map == modify_payload

    def test_fabric_design_map_payload_creation_case02(self, mocker):
        modify_payload = [
            {
                "DesignNode": "Switch-A",
                "PhysicalNode": Constants.service_tag1
            }
        ]
        current_payload = [
            {
                "DesignNode": "Switch-A",
                "PhysicalNode": "xyz123"
            },
            {
                "DesignNode": "Switch-B",
                "PhysicalNode": "abc456"
            }
        ]
        f_module = self.get_module_mock(params={})
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.validate_switches_overlap', return_value=None)
        design_map = self.module.fabric_design_map_payload_creation(modify_payload, current_payload, f_module)
        assert design_map == [
            {
                "DesignNode": "Switch-A",
                "PhysicalNode": Constants.service_tag1
            },
            {
                "DesignNode": "Switch-B",
                "PhysicalNode": "abc456"
            }
        ]

    def test_fabric_design_map_payload_creation_case03(self, mocker):
        modify_payload = [
        ]
        current_payload = [
        ]
        f_module = self.get_module_mock(params={})
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.validate_switches_overlap', return_value=None)
        design_map = self.module.fabric_design_map_payload_creation(modify_payload, current_payload, f_module)
        assert design_map == []

    def test_merge_payload_case_01(self):
        modify_payload = {
            "Name": "new_name",
            "Id": "8f25f714-9ea8-48e9-8eac-162d5d842e9f",
        }
        current_payload = {
            "Id": "8f25f714-9ea8-48e9-8eac-162d5d842e9f",
            "Name": "Fabric-1",
            "Description": "This is a fabric.",
            "FabricDesignMapping": [
                {
                    "DesignNode": "Switch-A",
                    "PhysicalNode": Constants.service_tag1
                },
                {
                    "DesignNode": "Switch-B",
                    "PhysicalNode": Constants.service_tag2
                }
            ],
            "FabricDesign": {
                "Name": "2xMX5108n_Ethernet_Switches_in_same_chassis"
            }
        }
        f_module = self.get_module_mock(params={})
        payload = self.module.merge_payload(modify_payload, current_payload, f_module)
        assert payload["Name"] == modify_payload["Name"]
        assert payload["Id"] == modify_payload["Id"]
        assert payload["Description"] == current_payload["Description"]
        assert payload["FabricDesignMapping"] == current_payload["FabricDesignMapping"]
        assert payload["FabricDesign"] == current_payload["FabricDesign"]

    def test_merge_payload_case_02(self):
        modify_payload = {
            "Name": "new_name",
            "Id": "8f25f714-9ea8-48e9-8eac-162d5d842e9f",
            "FabricDesignMapping": [
                {
                    "DesignNode": "Switch-A",
                    "PhysicalNode": "XYZ123"
                }],
            "FabricDesign": {
                "Name": "2xMX9116n_Fabric_Switching_Engines_in_same_chassis"
            }
        }
        current_payload = {
            "Id": "8f25f714-9ea8-48e9-8eac-162d5d842e9f",
            "Name": "Fabric-1",
            "Description": "This is a fabric.",
            "FabricDesignMapping": [
                {
                    "DesignNode": "Switch-A",
                    "PhysicalNode": Constants.service_tag1
                },
                {
                    "DesignNode": "Switch-B",
                    "PhysicalNode": Constants.service_tag2
                }
            ],
            "FabricDesign": {
                "Name": "2xMX5108n_Ethernet_Switches_in_same_chassis"
            }
        }
        f_module = self.get_module_mock(params={})
        payload = self.module.merge_payload(modify_payload, current_payload, f_module)
        assert payload["Name"] == modify_payload["Name"]
        assert payload["Id"] == modify_payload["Id"]
        assert payload["Description"] == current_payload["Description"]
        assert payload["FabricDesign"] == modify_payload["FabricDesign"]
        assert payload["FabricDesignMapping"] == [
            {
                "DesignNode": "Switch-A",
                "PhysicalNode": "XYZ123"
            },
            {
                "DesignNode": "Switch-B",
                "PhysicalNode": Constants.service_tag2
            }
        ]

    def test_merge_payload_case_03(self):
        modify_payload = {
            "Name": "new_name",
            "Id": "8f25f714-9ea8-48e9-8eac-162d5d842e9f",
            "FabricDesignMapping": [
                {
                    "DesignNode": "Switch-A",
                    "PhysicalNode": Constants.service_tag1
                },
                {
                    "DesignNode": "Switch-B",
                    "PhysicalNode": Constants.service_tag2
                }
            ],
            "FabricDesign": {
                "Name": "2xMX5108n_Ethernet_Switches_in_same_chassis"
            }
        }
        current_payload = {
            "Id": "8f25f714-9ea8-48e9-8eac-162d5d842e9f",
            "Name": "Fabric-1",
            "Description": "This is a fabric."
        }
        f_module = self.get_module_mock(params={})
        payload = self.module.merge_payload(modify_payload, current_payload, f_module)
        assert payload["Name"] == modify_payload["Name"]
        assert payload["Id"] == modify_payload["Id"]
        assert payload["Description"] == current_payload["Description"]
        assert payload["FabricDesign"] == modify_payload["FabricDesign"]
        assert payload["FabricDesignMapping"] == modify_payload["FabricDesignMapping"]

    def test_get_fabric_design(self, ome_connection_mock_for_smart_fabric, ome_response_mock):
        resp_data = {
            "Name": "2xMX5108n_Ethernet_Switches_in_same_chassis"
        }
        ome_response_mock.json_data = resp_data
        fabric_design_uri = "/api/NetworkService/Fabrics('0bebadec-b61b-4b16-b354-5196396a4a18')/FabricDesign"
        fabric_design = self.module.get_fabric_design(fabric_design_uri, ome_connection_mock_for_smart_fabric)
        assert fabric_design == {"Name": "2xMX5108n_Ethernet_Switches_in_same_chassis"}

    def test_get_current_payload(self, mocker, ome_connection_mock_for_smart_fabric):
        fabric_details = {
            "Id": "1312cceb-c3dd-4348-95c1-d8541a17d776",
            "Name": "Fabric_",
            "Description": "create new fabric1",
            "OverrideLLDPConfiguration": "NA",
            "ScaleVLANProfile": "NA",
            "FabricDesignMapping": [
                {
                    "DesignNode": "Switch-A",
                    "PhysicalNode": "2HB7NX2"
                },
                {
                    "DesignNode": "Switch-B",
                    "PhysicalNode": "2HBFNX2"
                }
            ],
            "FabricDesign": {
                "@odata.id": "/api/NetworkService/Fabrics('1312cceb-c3dd-4348-95c1-d8541a17d776')/FabricDesign"
            }
        }
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.get_fabric_design',
                     return_value={"Name": "2xMX5108n_Ethernet_Switches_in_same_chassis"})
        payload = self.module.get_current_payload(fabric_details, ome_connection_mock_for_smart_fabric)
        assert payload == {
            "Id": "1312cceb-c3dd-4348-95c1-d8541a17d776",
            "Name": "Fabric_",
            "Description": "create new fabric1",
            "FabricDesignMapping": [
                {
                    "DesignNode": "Switch-A",
                    "PhysicalNode": "2HB7NX2"
                },
                {
                    "DesignNode": "Switch-B",
                    "PhysicalNode": "2HBFNX2"
                }
            ],
            "FabricDesign": {"Name": "2xMX5108n_Ethernet_Switches_in_same_chassis"}
        }

    def test_get_current_payload_case02(self, mocker, ome_connection_mock_for_smart_fabric):
        fabric_details = {
            "Id": "1312cceb-c3dd-4348-95c1-d8541a17d776",
            "Name": "Fabric_",
            "Description": "create new fabric1",
            "OverrideLLDPConfiguration": "Disabled",
            "ScaleVLANProfile": "NA",
            "FabricDesignMapping": [
                {
                    "DesignNode": "Switch-A",
                    "PhysicalNode": "2HB7NX2"
                },
                {
                    "DesignNode": "Switch-B",
                    "PhysicalNode": "2HBFNX2"
                }
            ],
            "FabricDesign": {
                "@odata.id": "/api/NetworkService/Fabrics('1312cceb-c3dd-4348-95c1-d8541a17d776')/FabricDesign"
            }
        }
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.get_fabric_design',
                     return_value={"Name": "2xMX5108n_Ethernet_Switches_in_same_chassis"})
        payload = self.module.get_current_payload(fabric_details, ome_connection_mock_for_smart_fabric)
        assert payload == {
            "Id": "1312cceb-c3dd-4348-95c1-d8541a17d776",
            "OverrideLLDPConfiguration": "Disabled",
            "Name": "Fabric_",
            "Description": "create new fabric1",
            "FabricDesignMapping": [
                {
                    "DesignNode": "Switch-A",
                    "PhysicalNode": "2HB7NX2"
                },
                {
                    "DesignNode": "Switch-B",
                    "PhysicalNode": "2HBFNX2"
                }
            ],
            "FabricDesign": {"Name": "2xMX5108n_Ethernet_Switches_in_same_chassis"}
        }

    @pytest.mark.parametrize("params, expected", [({"name": "fabric1"}, {"Name": "fabric1"}),
                                                  ({"name": "fabric1", "description": "fabric desc"},
                                                   {"Name": "fabric1", "Description": "fabric desc"}),
                                                  ({"name": "fabric1", "description": "fabric desc",
                                                    "override_LLDP_configuration": "Enabled"},
                                                   {"Name": "fabric1", "Description": "fabric desc",
                                                    "OverrideLLDPConfiguration": "Enabled"}
                                                   )])
    def test_create_modify_payload_case_01(self, params, expected, ome_default_args):
        ome_default_args.update(params)
        payload = self.module.create_modify_payload(ome_default_args, None, "1.1")
        assert payload == expected

    def test_create_modify_payload_case_02(self, ome_default_args):
        params = {"name": "fabric1", "new_name": "fabric2", "primary_switch_service_tag": Constants.service_tag1,
                  "secondary_switch_service_tag": Constants.service_tag2,
                  "fabric_design": "2xMX5108n_Ethernet_Switches_in_same_chassis",
                  "override_LLDP_configuration": "Disabled"}
        ome_default_args.update(params)
        payload = self.module.create_modify_payload(ome_default_args, "1312cceb-c3dd-4348-95c1-d8541a17d776", "1.0")
        assert payload["FabricDesignMapping"] == [{"DesignNode": "Switch-A",
                                                   "PhysicalNode": Constants.service_tag1},
                                                  {"DesignNode": "Switch-B",
                                                   "PhysicalNode": Constants.service_tag2}
                                                  ]
        assert payload["Name"] == "fabric2"
        assert "OverrideLLDPConfiguration" not in payload
        assert payload["FabricDesign"] == {"Name": "2xMX5108n_Ethernet_Switches_in_same_chassis"}
        assert payload["Id"] == "1312cceb-c3dd-4348-95c1-d8541a17d776"

    def test_get_fabric_id_cse_01(self):
        fabric_id, fabric_id_details = self.module.get_fabric_id_details("Fabric_1", all_fabric_details)
        assert fabric_id == "1312cceb-c3dd-4348-95c1-d8541a17d776"
        assert fabric_id_details == all_fabric_details[0]

    def test_get_fabric_id_cse_02(self):
        fabric_id, fabric_id_details = self.module.get_fabric_id_details("Fabric_New", all_fabric_details)
        assert fabric_id is None
        assert fabric_id_details is None

    def test_get_fabric_id_cse_03(self):
        fabric_id, fabric_id_details = self.module.get_fabric_id_details("Fabric_1", [])
        assert fabric_id is None
        assert fabric_id_details is None

    @pytest.mark.parametrize("identifier, expected_type", [("primary_switch_service_tag", "NETWORK_IOM"),
                                                           ("secondary_switch_service_tag", "NETWORK_IOM"),
                                                           ("hostname", "CHASSIS")])
    def test_validate_device_type_case_01(self, ome_default_args, identifier, expected_type):
        ome_default_args.update({"primary_switch_service_tag": Constants.service_tag1,
                                 "secondary_switch_service_tag": Constants.service_tag2})
        f_module = self.get_module_mock(params={identifier: "val"})
        with pytest.raises(Exception, match=DEVICE_SERVICE_TAG_TYPE_ERROR_MSG.format(identifier, expected_type)):
            self.module.validate_device_type("SERVER", identifier, {}, f_module)

    @pytest.mark.parametrize("identifier", ["primary_switch_service_tag", "secondary_switch_service_tag"])
    def test_validate_device_type_case_02(self, ome_default_args, identifier):
        ome_default_args.update({"primary_switch_service_tag": Constants.service_tag1,
                                 "secondary_switch_service_tag": Constants.service_tag2,
                                 "fabric_design": "2xMX5108n_Ethernet_Switches_in_same_chassis"
                                 })

        f_module = self.get_module_mock(params=ome_default_args)
        with pytest.raises(Exception, match=DESIGN_MODEL_ERROR_MSG.format(identifier, 'MX5108n')):
            self.module.validate_device_type("NETWORK_IOM", identifier, device_details, f_module)

    @pytest.mark.parametrize("identifier", ["primary_switch_service_tag", "secondary_switch_service_tag"])
    def test_validate_device_type_case_03(self, ome_default_args, identifier):
        ome_default_args.update({"primary_switch_service_tag": Constants.service_tag1,
                                 "secondary_switch_service_tag": Constants.service_tag2,
                                 "fabric_design": "2xMX9116n_Fabric_Switching_Engines_in_same_chassis"
                                 })

        f_module = self.get_module_mock(params=ome_default_args)
        self.module.validate_device_type("NETWORK_IOM", identifier, device_details, f_module)

    def test_validate_service_tag_case_01(self, mocker, ome_connection_mock_for_smart_fabric, ome_default_args):
        ome_default_args.update({"primary_switch_service_tag": Constants.service_tag1,
                                 "secondary_switch_service_tag": Constants.service_tag2,
                                 "fabric_design": "2xMX9116n_Fabric_Switching_Engines_in_same_chassis"
                                 })

        f_module = self.get_module_mock(params=ome_default_args)
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.validate_device_type', return_value=None)
        ome_connection_mock_for_smart_fabric.get_device_id_from_service_tag.return_value = {"value": device_details,
                                                                                            "Id": Constants.device_id1}
        self.module.validate_service_tag(Constants.service_tag1, "primary_switch_service_tag",
                                         {2000: "CHASSIS", 4000: "NETWORK_IOM",
                                          1000: "SERVER",
                                          3000: "STORAGE"}, ome_connection_mock_for_smart_fabric, f_module)

    def test_validate_service_tag_exception_case_01(self, mocker, ome_connection_mock_for_smart_fabric,
                                                    ome_default_args):
        ome_default_args.update({"primary_switch_service_tag": Constants.service_tag1,
                                 "secondary_switch_service_tag": Constants.service_tag2,
                                 "fabric_design": "2xMX9116n_Fabric_Switching_Engines_in_same_chassis"
                                 })

        f_module = self.get_module_mock(params=ome_default_args)
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.validate_device_type', return_value=None)
        ome_connection_mock_for_smart_fabric.get_device_id_from_service_tag.return_value = {"value": {}, "Id": None}
        with pytest.raises(Exception, match=DEVICE_SERVICE_TAG_NOT_FOUND_ERROR_MSG.format(Constants.service_tag1)):
            self.module.validate_service_tag(Constants.service_tag1, "primary_switch_service_tag",
                                             {2000: "CHASSIS", 4000: "NETWORK_IOM",
                                              1000: "SERVER",
                                              3000: "STORAGE"}, ome_connection_mock_for_smart_fabric, f_module)

    @pytest.mark.parametrize("params", [{"primary_switch_service_tag": Constants.service_tag1,
                                         "secondary_switch_service_tag": Constants.service_tag2,
                                         "fabric_design": "2xMX9116n_Fabric_Switching_Engines_in_same_chassis"
                                         },
                                        {"primary_switch_service_tag": None,
                                         "secondary_switch_service_tag": None,
                                         }
                                        ])
    def test_validate_devices_case_01(self, params, mocker, ome_connection_mock_for_smart_fabric, ome_default_args):
        ome_default_args.update(params)

        f_module = self.get_module_mock(params=ome_default_args)
        ome_connection_mock_for_smart_fabric.get_device_type.return_value = {2000: "CHASSIS", 4000: "NETWORK_IOM",
                                                                             1000: "SERVER",
                                                                             3000: "STORAGE"}
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.validate_service_tag', return_value=None)
        self.module.validate_devices(Constants.service_tag1, ome_connection_mock_for_smart_fabric, f_module)

    def test_validate_devices_case_02(self, mocker, ome_connection_mock_for_smart_fabric, ome_default_args):
        ome_default_args.update({"primary_switch_service_tag": Constants.service_tag2,
                                 "secondary_switch_service_tag": Constants.service_tag2,
                                 "fabric_design": "2xMX9116n_Fabric_Switching_Engines_in_same_chassis"
                                 })

        f_module = self.get_module_mock(params=ome_default_args)
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.validate_service_tag', return_value=None)
        ome_connection_mock_for_smart_fabric.get_device_type.return_value = {2000: "CHASSIS",
                                                                             4000: "NETWORK_IOM",
                                                                             1000: "SERVER",
                                                                             3000: "STORAGE"}
        with pytest.raises(Exception, match=DUPLICATE_TAGS):
            self.module.validate_devices(Constants.service_tag1, ome_connection_mock_for_smart_fabric, f_module)

    def test_required_field_check_for_create_case_01(self, ome_default_args):
        ome_default_args.update({"primary_switch_service_tag": Constants.service_tag1,
                                 "secondary_switch_service_tag": Constants.service_tag2,
                                 "fabric_design": "2xMX9116n_Fabric_Switching_Engines_in_same_chassis",
                                 "state": "present"
                                 })

        f_module = self.get_module_mock(params=ome_default_args)
        self.module.required_field_check_for_create("fabric_id", f_module)

    def test_required_field_check_for_create_case_02(self, ome_default_args):
        ome_default_args.update({"primary_switch_service_tag": Constants.service_tag1,
                                 "secondary_switch_service_tag": Constants.service_tag2,
                                 "fabric_design": "2xMX9116n_Fabric_Switching_Engines_in_same_chassis",
                                 "state": "present"
                                 })

        f_module = self.get_module_mock(params=ome_default_args)
        self.module.required_field_check_for_create(None, f_module)

    @pytest.mark.parametrize("params", [{"primary_switch_service_tag": Constants.service_tag1},
                                        {"secondary_switch_service_tag": Constants.service_tag1},
                                        {"fabric_design": Constants.service_tag1},
                                        {"fabric_design": Constants.service_tag1,
                                         "primary_switch_service_tag": Constants.service_tag1},
                                        {"fabric_design": Constants.service_tag1,
                                         "secondary_switch_service_tag": Constants.service_tag1},
                                        {"primary_switch_service_tag": Constants.service_tag1,
                                         "secondary_switch_service_tag": Constants.service_tag2},
                                        {"primary_switch_service_tag": None,
                                         "secondary_switch_service_tag": None},
                                        {"primary_switch_service_tag": None,
                                         "secondary_switch_service_tag": None}
                                        ])
    def test_required_field_check_for_create_case_03(self, params, ome_default_args):
        ome_default_args.update(params)
        f_module = self.get_module_mock(params=ome_default_args)
        with pytest.raises(Exception, match=REQUIRED_FIELD):
            self.module.required_field_check_for_create(None, f_module)

    def test_process_output_case01(self, ome_connection_mock_for_smart_fabric, ome_default_args):
        ome_default_args.update({"primary_switch_service_tag": Constants.service_tag1,
                                 "secondary_switch_service_tag": Constants.service_tag2,
                                 "fabric_design": "2xMX9116n_Fabric_Switching_Engines_in_same_chassis",
                                 "state": "present"
                                 })
        f_module = self.get_module_mock(params=ome_default_args)
        with pytest.raises(Exception, match="Fabric modification operation is initiated.") as err:
            self.module.process_output("Fabric1", True, "Fabric modification operation is initiated.", "1234",
                                       ome_connection_mock_for_smart_fabric, f_module)
        err.value.fail_kwargs['fabric_id'] == "1234"

    def test_process_output_case02(self, mocker, ome_connection_mock_for_smart_fabric, ome_default_args):
        ome_default_args.update({"primary_switch_service_tag": Constants.service_tag1,
                                 "secondary_switch_service_tag": Constants.service_tag2,
                                 "fabric_design": "2xMX9116n_Fabric_Switching_Engines_in_same_chassis",
                                 "state": "present"
                                 })
        f_module = self.get_module_mock(params=ome_default_args)
        resp = {
            "error": {
                "code": "Base.1.0.GeneralError",
                "message": "A general error has occurred. See ExtendedInfo for more information.",
                "@Message.ExtendedInfo":
                    [
                        {
                            "MessageId": "CDEV7154",
                            "RelatedProperties": [],
                            "Message": "Fabric update is successful. The OverrideLLDPConfiguration attribute is not"
                                       " provided "
                                       " in the payload, so it preserves the previous value.",
                            "MessageArgs": [],
                            "Severity": "Informational",
                            "Resolution": "Please update the Fabric with the OverrideLLDPConfiguration as Disabled or"
                                          " Enabled "
                                          " if necessary. "
                        }
                    ]
            }
        }
        ome_connection_mock_for_smart_fabric.get_all_items_with_pagination.return_value = {"value": all_fabric_details,
                                                                                           "total_count": 2}
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.get_fabric_id_details',
                     return_value=(all_fabric_details[0]["Id"], all_fabric_details[0]))
        with pytest.raises(Exception, match="Fabric creation operation is initiated.") as err:
            self.module.process_output("Fabric1", resp, "Fabric creation operation is initiated.", None,
                                       ome_connection_mock_for_smart_fabric, f_module)
        err.value.fail_kwargs['fabric_id'] == all_fabric_details[0]["Id"]
        err.value.fail_kwargs['additional_info'] == resp

    def test_process_output_case03(self, ome_connection_mock_for_smart_fabric, ome_default_args):
        ome_default_args.update({"primary_switch_service_tag": Constants.service_tag1,
                                 "secondary_switch_service_tag": Constants.service_tag2,
                                 "fabric_design": "2xMX9116n_Fabric_Switching_Engines_in_same_chassis",
                                 "state": "present"
                                 })
        f_module = self.get_module_mock(params=ome_default_args)
        with pytest.raises(Exception, match="Fabric creation operation is initiated.") as err:
            self.module.process_output("Fabric1", "1234", "Fabric creation operation is initiated.", None,
                                       ome_connection_mock_for_smart_fabric, f_module)
        err.value.fail_kwargs['fabric_id'] == "1234"

    def test_create_modify_fabric_modify_case_01(self, ome_connection_mock_for_smart_fabric, ome_default_args, mocker,
                                                 ome_response_mock):
        ome_default_args.update({"primary_switch_service_tag": Constants.service_tag1,
                                 "secondary_switch_service_tag": Constants.service_tag2,
                                 "fabric_design": "2xMX9116n_Fabric_Switching_Engines_in_same_chassis",
                                 "state": "present"
                                 })

        mocker.patch(MODULE_PATH + 'ome_smart_fabric.required_field_check_for_create',
                     return_value=None)
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.get_msm_device_details',
                     return_value=(Constants.service_tag1, "1.1"))
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.validate_devices', return_value=None)
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.get_fabric_id_details',
                     return_value=(all_fabric_details[0]["Id"], all_fabric_details[0]))
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.create_modify_payload',
                     return_value={"Name": "fabric2", "Description": "fabric desc2",
                                   "OverrideLLDPConfiguration": "Enabled"})
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.get_current_payload',
                     return_value={
                         "Name": "fabric1",
                         "Description": "fabric desc1",
                         "OverrideLLDPConfiguration": "Enabled",
                         "FabricDesignMapping": [
                             {
                                 "DesignNode": "Switch-A",
                                 "PhysicalNode": "3QM4WV2"
                             },
                             {
                                 "DesignNode": "Switch-B",
                                 "PhysicalNode": "GTCT8T2"
                             }
                         ],
                         "FabricDesign": {
                             "Name": "2xMX9116n_Fabric_Switching_Engines_in_different_chassis"
                         }
                     })
        mocker_merge_payload = mocker.patch(MODULE_PATH + 'ome_smart_fabric.merge_payload',
                                            return_value={
                                                "Name": "fabric2",
                                                "Description": "fabric desc2",
                                                "OverrideLLDPConfiguration": "Enabled",
                                                "FabricDesignMapping": [
                                                    {
                                                        "DesignNode": "Switch-A",
                                                        "PhysicalNode": "3QM4WV2"
                                                    },
                                                    {
                                                        "DesignNode": "Switch-B",
                                                        "PhysicalNode": "GTCT8T2"
                                                    }
                                                ],
                                                "FabricDesign": {
                                                    "Name": "2xMX9116n_Fabric_Switching_Engines_in_different_chassis"
                                                }
                                            })
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.idempotency_check_for_state_present', return_value=None)
        mocker_process_output = mocker.patch(MODULE_PATH + 'ome_smart_fabric.process_output', return_value=None)
        ome_response_mock.json_data = "true"
        f_module = self.get_module_mock(params=ome_default_args)
        self.module.create_modify_fabric("Fabric1", all_fabric_details, ome_connection_mock_for_smart_fabric,
                                         f_module)
        assert mocker_process_output.called
        assert mocker_merge_payload.called

    def test_create_modify_fabric_create_case_02(self, ome_connection_mock_for_smart_fabric, ome_default_args, mocker,
                                                 ome_response_mock):
        ome_default_args.update({"primary_switch_service_tag": Constants.service_tag1,
                                 "secondary_switch_service_tag": Constants.service_tag2,
                                 "fabric_design": "2xMX9116n_Fabric_Switching_Engines_in_same_chassis",
                                 "state": "present"
                                 })

        f_module = self.get_module_mock(params=ome_default_args)
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.required_field_check_for_create',
                     return_value=None)
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.get_msm_device_details',
                     return_value=(Constants.service_tag1, "1.1"))
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.validate_devices', return_value=None)
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.get_fabric_id_details',
                     return_value=(None, {}))
        mocker_create_modify_payload = mocker.patch(MODULE_PATH + 'ome_smart_fabric.create_modify_payload',
                                                    return_value={"Name": "fabric2", "Description": "fabric desc2",
                                                                  "OverrideLLDPConfiguration": "Enabled"})
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.idempotency_check_for_state_present', return_value=None)
        ome_response_mock.json_data = "123456789abcd"
        mocker_process_output = mocker.patch(MODULE_PATH + 'ome_smart_fabric.process_output', return_value=None)
        self.module.create_modify_fabric("Fabric1", all_fabric_details, ome_connection_mock_for_smart_fabric,
                                         f_module)
        assert mocker_process_output.called
        assert mocker_create_modify_payload.called

    def test_check_fabric_exits_for_state_absent_non_check_mode_case01(self, mocker,
                                                                       ome_connection_mock_for_smart_fabric,
                                                                       ome_default_args):
        ome_default_args.update({
            "state": "absent",
            "name": "Fabric1"
        })

        f_module = self.get_module_mock(params=ome_default_args, check_mode=False)
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.get_fabric_id_details',
                     return_value=(None, {}))
        with pytest.raises(Exception, match=FABRIC_NOT_FOUND_ERROR_MSG.format("Fabric1")):
            self.module.check_fabric_exits_for_state_absent(all_fabric_details[0], f_module, "Fabric1")

    def test_check_fabric_exits_for_state_absent_non_check_mode_case02(self, mocker,
                                                                       ome_connection_mock_for_smart_fabric,
                                                                       ome_default_args):
        ome_default_args.update({
            "state": "absent",
            "name": "Fabric1"
        })

        f_module = self.get_module_mock(params=ome_default_args, check_mode=False)
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.get_fabric_id_details',
                     return_value=(all_fabric_details[0]["Id"], all_fabric_details[0]))
        fabric_id = self.module.check_fabric_exits_for_state_absent(all_fabric_details[0], f_module, "Fabric1")
        assert fabric_id == all_fabric_details[0]["Id"]

    def test_check_fabric_exits_for_state_absent_check_mode_case01(self, mocker,
                                                                   ome_connection_mock_for_smart_fabric,
                                                                   ome_default_args):
        ome_default_args.update({
            "state": "absent",
            "name": "Fabric1"
        })

        f_module = self.get_module_mock(params=ome_default_args, check_mode=True)
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.get_fabric_id_details',
                     return_value=(None, {}))
        with pytest.raises(Exception, match=CHECK_MODE_CHANGE_NOT_FOUND_MSG):
            self.module.check_fabric_exits_for_state_absent(all_fabric_details[0], f_module, "Fabric1")

    def test_check_fabric_exits_for_state_absent_check_mode_case02(self, mocker,
                                                                   ome_connection_mock_for_smart_fabric,
                                                                   ome_default_args):
        ome_default_args.update({
            "state": "absent",
            "name": "Fabric1"
        })

        f_module = self.get_module_mock(params=ome_default_args, check_mode=True)
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.get_fabric_id_details',
                     return_value=(all_fabric_details[0]["Id"], all_fabric_details[0]))
        with pytest.raises(Exception, match=CHECK_MODE_CHANGE_FOUND_MSG):
            self.module.check_fabric_exits_for_state_absent(all_fabric_details[0], f_module, "Fabric1")

    def test_delete_fabric(self, ome_connection_mock_for_smart_fabric, ome_default_args, mocker):
        ome_default_args.update({
            "state": "absent",
            "name": "Fabric1"
        })

        f_module = self.get_module_mock(params=ome_default_args, check_mode=True)
        mocker.patch(MODULE_PATH + 'ome_smart_fabric.check_fabric_exits_for_state_absent',
                     return_value=all_fabric_details[0]["Id"])
        with pytest.raises(Exception, match="Fabric deletion operation is initiated.") as err:
            self.module.delete_fabric(all_fabric_details, ome_connection_mock_for_smart_fabric, f_module, "Fabric1")
        err.value.fail_kwargs['fabric_id'] == all_fabric_details[0]["Id"]

    def test_fabric_actions_case_01(self, mocker, ome_connection_mock_for_smart_fabric, ome_default_args):
        ome_default_args.update({
            "state": "absent",
            "name": "Fabric1"
        })
        ome_connection_mock_for_smart_fabric.get_all_items_with_pagination.return_value = {"value": all_fabric_details,
                                                                                           "total_count": 2}
        delete_fabric = mocker.patch(MODULE_PATH + 'ome_smart_fabric.delete_fabric',
                                     return_value=None)
        f_module = self.get_module_mock(params=ome_default_args, check_mode=True)
        self.module.fabric_actions(ome_connection_mock_for_smart_fabric, f_module)
        assert delete_fabric.called

    def test_fabric_actions_case_02(self, mocker, ome_connection_mock_for_smart_fabric, ome_default_args):
        ome_default_args.update({
            "state": "present",
            "name": "Fabric1"
        })
        ome_connection_mock_for_smart_fabric.get_all_items_with_pagination.return_value = {"value": all_fabric_details,
                                                                                           "total_count": 2}
        create_modify_fabric = mocker.patch(MODULE_PATH + 'ome_smart_fabric.create_modify_fabric',
                                            return_value=None)
        f_module = self.get_module_mock(params=ome_default_args, check_mode=True)
        self.module.fabric_actions(ome_connection_mock_for_smart_fabric, f_module)
        assert create_modify_fabric.called

    def test_get_service_tag_with_fqdn_success_case(self, ome_default_args, ome_connection_mock_for_smart_fabric):
        ome_default_args.update({"hostname": "M-YYYY.abcd.lab"})
        resp_data = {
            "@odata.context": "/api/$metadata#Collection(DeviceService.Device)",
            "@odata.count": 2,
            "value": [
                {
                    "@odata.type": "#DeviceService.Device",
                    "@odata.id": "/api/DeviceService/Devices(Constants.device_id1)",
                    "Id": Constants.device_id1,
                    "Type": 2000,
                    "Identifier": Constants.service_tag1,
                    "DeviceServiceTag": Constants.service_tag1,
                    "ChassisServiceTag": None,
                    "Model": "PowerEdge MX7000",
                    "PowerState": 17,
                    "ManagedState": 3000,
                    "Status": 4000,
                    "ConnectionState": True,
                    "AssetTag": None,
                    "SystemId": 2031,
                    "DeviceName": "MX-Constants.service_tag1",
                    "LastInventoryTime": "2020-07-11 17:00:18.925",
                    "LastStatusTime": "2020-07-11 09:00:07.444",
                    "DeviceSubscription": None,
                    "DeviceCapabilities": [
                        18,
                        8,
                        201,
                        202
                    ],
                    "SlotConfiguration": {
                        "ChassisName": None
                    },
                    "DeviceManagement": [
                        {
                            "ManagementId": 111111,
                            "NetworkAddress": ome_default_args["hostname"],
                            "MacAddress": "xx:yy:zz:x1x1",
                            "ManagementType": 2,
                            "InstrumentationName": "MX-Constants.service_tag1",
                            "DnsName": "M-YYYY.abcd.lab",
                            "ManagementProfile": [
                                {
                                    "ManagementProfileId": 111111,
                                    "ProfileId": "MSM_BASE",
                                    "ManagementId": 111111,
                                    "ManagementURL": "https://" + ome_default_args["hostname"] + ":443",
                                    "HasCreds": 0,
                                    "Status": 1000,
                                    "StatusDateTime": "2020-07-11 17:00:18.925"
                                }
                            ]
                        },
                        {
                            "ManagementId": 33333,
                            "NetworkAddress": "[1234.abcd:5678:345]",
                            "MacAddress": "22:xx:yy:11",
                            "ManagementType": 2,
                            "InstrumentationName": "MX-Constants.service_tag1",
                            "DnsName": "M-YYYY.abcd.lab",
                            "ManagementProfile": [
                                {
                                    "ManagementProfileId": 33333,
                                    "ProfileId": "MSM_BASE",
                                    "ManagementId": 33333,
                                    "ManagementURL": "https://[1234:abcd:567:xyzs]:443",
                                    "HasCreds": 0,
                                    "Status": 1000,
                                    "StatusDateTime": "2020-07-11 17:00:18.925"
                                }
                            ]
                        }
                    ],
                    "Actions": None
                },
                {
                    "@odata.type": "#DeviceService.Device",
                    "@odata.id": "/api/DeviceService/Devices(Constants.device_id1)",
                    "Id": Constants.device_id1,
                    "Type": 2000,
                    "Identifier": Constants.service_tag2,
                    "DeviceServiceTag": Constants.service_tag2,
                    "ChassisServiceTag": None,
                    "Model": "PowerEdge MX7000",
                    "PowerState": 17,
                    "ManagedState": 3000,
                    "Status": 4000,
                    "ConnectionState": True,
                    "AssetTag": None,
                    "SystemId": 2031,
                    "DeviceName": "MX-Constants.service_tag2",
                    "LastInventoryTime": "2020-07-11 17:00:18.925",
                    "LastStatusTime": "2020-07-11 09:00:07.444",
                    "DeviceSubscription": None,
                    "DeviceCapabilities": [
                        18,
                        8,
                        201,
                        202
                    ],
                    "SlotConfiguration": {
                        "ChassisName": None
                    },
                    "DeviceManagement": [
                        {
                            "ManagementId": 111111,
                            "NetworkAddress": ome_default_args["hostname"],
                            "MacAddress": "xx:yy:zz:x1x1",
                            "ManagementType": 2,
                            "InstrumentationName": "MX-Constants.service_tag2",
                            "DnsName": "M-XXXX.abcd.lab",
                            "ManagementProfile": [
                                {
                                    "ManagementProfileId": 111111,
                                    "ProfileId": "MSM_BASE",
                                    "ManagementId": 111111,
                                    "ManagementURL": "https://" + ome_default_args["hostname"] + ":443",
                                    "HasCreds": 0,
                                    "Status": 1000,
                                    "StatusDateTime": "2020-07-11 17:00:18.925"
                                }
                            ]
                        },
                        {
                            "ManagementId": 22222,
                            "NetworkAddress": "[1234.abcd:5678:345]",
                            "MacAddress": "22:xx:yy:11",
                            "ManagementType": 2,
                            "InstrumentationName": "MX-Constants.service_tag2",
                            "DnsName": "M-XXXX.abcd.lab",
                            "ManagementProfile": [{
                                "ManagementProfileId": 22222,
                                "ProfileId": "MSM_BASE",
                                "ManagementId": 22222,
                                "ManagementURL": "https://[1234:abcd:567:xyzs]:443",
                                "HasCreds": 0,
                                "Status": 1000,
                                "StatusDateTime": "2020-07-11 17:00:18.925"
                            }]
                        }
                    ],
                    "Actions": None
                }
            ]
        }
        f_module = self.get_module_mock(params=ome_default_args, check_mode=True)
        ome_connection_mock_for_smart_fabric.get_all_items_with_pagination.return_value = resp_data
        service_tag = self.module.get_service_tag_with_fqdn(ome_connection_mock_for_smart_fabric, f_module)
        assert service_tag == Constants.service_tag1

    def test_get_service_tag_with_fqdn_success_case2(self, ome_default_args, ome_connection_mock_for_smart_fabric):
        ome_default_args.update({"hostname": Constants.hostname1})
        resp_data = {
            "@odata.context": "/api/$metadata#Collection(DeviceService.Device)",
            "@odata.count": 2,
            "value": [
                {
                    "@odata.type": "#DeviceService.Device",
                    "@odata.id": "/api/DeviceService/Devices(Constants.device_id1)",
                    "Id": Constants.device_id1,
                    "Type": 2000,
                    "Identifier": Constants.service_tag1,
                    "DeviceServiceTag": Constants.service_tag1,
                    "ChassisServiceTag": None,
                    "Model": "PowerEdge MX7000",
                    "PowerState": 17,
                    "ManagedState": 3000,
                    "Status": 4000,
                    "ConnectionState": True,
                    "AssetTag": None,
                    "SystemId": 2031,
                    "DeviceName": "MX-Constants.service_tag1",
                    "LastInventoryTime": "2020-07-11 17:00:18.925",
                    "LastStatusTime": "2020-07-11 09:00:07.444",
                    "DeviceSubscription": None,
                    "DeviceCapabilities": [
                        18,
                        8,
                        201,
                        202
                    ],
                    "SlotConfiguration": {
                        "ChassisName": None
                    },
                    "DeviceManagement": [
                        {
                            "ManagementId": 111111,
                            "NetworkAddress": ome_default_args["hostname"],
                            "MacAddress": "xx:yy:zz:x1x1",
                            "ManagementType": 2,
                            "InstrumentationName": "MX-Constants.service_tag1",
                            "DnsName": "M-YYYY.abcd.lab",
                            "ManagementProfile": [
                                {
                                    "ManagementProfileId": 111111,
                                    "ProfileId": "MSM_BASE",
                                    "ManagementId": 111111,
                                    "ManagementURL": "https://" + ome_default_args["hostname"] + ":443",
                                    "HasCreds": 0,
                                    "Status": 1000,
                                    "StatusDateTime": "2020-07-11 17:00:18.925"
                                }
                            ]
                        },
                        {
                            "ManagementId": 33333,
                            "NetworkAddress": "[1234.abcd:5678:345]",
                            "MacAddress": "22:xx:yy:11",
                            "ManagementType": 2,
                            "InstrumentationName": "MX-Constants.service_tag1",
                            "DnsName": "M-YYYY.abcd.lab",
                            "ManagementProfile": [
                                {
                                    "ManagementProfileId": 33333,
                                    "ProfileId": "MSM_BASE",
                                    "ManagementId": 33333,
                                    "ManagementURL": "https://[1234:abcd:567:xyzs]:443",
                                    "HasCreds": 0,
                                    "Status": 1000,
                                    "StatusDateTime": "2020-07-11 17:00:18.925"
                                }
                            ]
                        }
                    ],
                    "Actions": None
                },
                {
                    "@odata.type": "#DeviceService.Device",
                    "@odata.id": "/api/DeviceService/Devices(Constants.device_id1)",
                    "Id": Constants.device_id1,
                    "Type": 2000,
                    "Identifier": Constants.service_tag2,
                    "DeviceServiceTag": Constants.service_tag2,
                    "ChassisServiceTag": None,
                    "Model": "PowerEdge MX7000",
                    "PowerState": 17,
                    "ManagedState": 3000,
                    "Status": 4000,
                    "ConnectionState": True,
                    "AssetTag": None,
                    "SystemId": 2031,
                    "DeviceName": "MX-Constants.service_tag2",
                    "LastInventoryTime": "2020-07-11 17:00:18.925",
                    "LastStatusTime": "2020-07-11 09:00:07.444",
                    "DeviceSubscription": None,
                    "DeviceCapabilities": [
                        18,
                        8,
                        201,
                        202
                    ],
                    "SlotConfiguration": {
                        "ChassisName": None
                    },
                    "DeviceManagement": [
                        {
                            "ManagementId": 111111,
                            "NetworkAddress": ome_default_args["hostname"],
                            "MacAddress": "xx:yy:zz:x1x1",
                            "ManagementType": 2,
                            "InstrumentationName": "MX-Constants.service_tag2",
                            "DnsName": "M-XXXX.abcd.lab",
                            "ManagementProfile": [
                                {
                                    "ManagementProfileId": 111111,
                                    "ProfileId": "MSM_BASE",
                                    "ManagementId": 111111,
                                    "ManagementURL": "https://" + ome_default_args["hostname"] + ":443",
                                    "HasCreds": 0,
                                    "Status": 1000,
                                    "StatusDateTime": "2020-07-11 17:00:18.925"
                                }
                            ]
                        },
                        {
                            "ManagementId": 22222,
                            "NetworkAddress": "[1234.abcd:5678:345]",
                            "MacAddress": "22:xx:yy:11",
                            "ManagementType": 2,
                            "InstrumentationName": "MX-Constants.service_tag2",
                            "DnsName": "M-XXXX.abcd.lab",
                            "ManagementProfile": [
                                {
                                    "ManagementProfileId": 22222,
                                    "ProfileId": "MSM_BASE",
                                    "ManagementId": 22222,
                                    "ManagementURL": "https://[1234:abcd:567:xyzs]:443",
                                    "HasCreds": 0,
                                    "Status": 1000,
                                    "StatusDateTime": "2020-07-11 17:00:18.925"
                                }
                            ]
                        }
                    ],
                    "Actions": None
                }
            ]
        }
        f_module = self.get_module_mock(params=ome_default_args, check_mode=True)
        ome_connection_mock_for_smart_fabric.get_all_items_with_pagination.return_value = resp_data
        service_tag = self.module.get_service_tag_with_fqdn(ome_connection_mock_for_smart_fabric, f_module)
        assert service_tag is None

    def test_get_service_tag_with_fqdn_success_case3(self, ome_default_args, ome_connection_mock_for_smart_fabric):
        ome_default_args.update({"hostname": Constants.hostname1})
        resp_data = {"value": []}
        f_module = self.get_module_mock(params=ome_default_args, check_mode=True)
        ome_connection_mock_for_smart_fabric.get_all_items_with_pagination.return_value = resp_data
        service_tag = self.module.get_service_tag_with_fqdn(ome_connection_mock_for_smart_fabric, f_module)
        assert service_tag is None
