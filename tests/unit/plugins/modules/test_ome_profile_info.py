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
from ansible_collections.dellemc.openmanage.plugins.modules import ome_profile_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

SUCCESS_MSG = "Successfully retrieved the profile information."
NO_PROFILES_MSG = "No profiles were found."

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_profile_info.'


@pytest.fixture
def ome_connection_mock_for_profile_info(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeProfileInfo(FakeAnsibleModule):
    module = ome_profile_info

    @pytest.mark.parametrize("params", [
        {"json_data": {"value": [{'Id': 1234, 'Name': "ABCTAG1", "Type": 1000}],
                       "AttributeGroups": [
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
                                               "AttributeId": 7587,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2342,
                                               "DisplayName": "ActiveDirectory 1 Active Directory RAC Name",
                                               "Description": None,
                                               "Value": None,
                                               "IsReadOnly": False,
                                               "IsIgnored": True,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 3
                                           }
                                       ]
                                   },
                                   {
                                       "GroupNameId": 32851,
                                       "DisplayName": "IPv4 Information",
                                       "SubAttributeGroups": [],
                                       "Attributes": [
                                           {
                                               "AttributeId": 8133,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2199,
                                               "DisplayName": "IPv4 1 IPv4 DHCP Enable",
                                               "Description": None,
                                               "Value": "Enabled",
                                               "IsReadOnly": False,
                                               "IsIgnored": True,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 2
                                           },
                                           {
                                               "AttributeId": 7974,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2198,
                                               "DisplayName": "IPv4 1 IPv4 Enable",
                                               "Description": None,
                                               "Value": "Enabled",
                                               "IsReadOnly": False,
                                               "IsIgnored": True,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 2
                                           }
                                       ]
                                   },
                                   {
                                       "GroupNameId": 32852,
                                       "DisplayName": "IPv4 Static Information",
                                       "SubAttributeGroups": [],
                                       "Attributes": [
                                           {
                                               "AttributeId": 7916,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2400,
                                               "DisplayName": "IPv4Static 1 Gateway",
                                               "Description": None,
                                               "Value": "XX.XX.XX.XX",
                                               "IsReadOnly": False,
                                               "IsIgnored": True,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 2
                                           },
                                           {
                                               "AttributeId": 8245,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2399,
                                               "DisplayName": "IPv4Static 1 IPv4 Address",
                                               "Description": None,
                                               "Value": "XX.XX.XX.XX20",
                                               "IsReadOnly": False,
                                               "IsIgnored": True,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 3
                                           },
                                           {
                                               "AttributeId": 7724,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2403,
                                               "DisplayName": "IPv4Static 1 Net Mask",
                                               "Description": None,
                                               "Value": "XXX.XXX.XXX.XXX",
                                               "IsReadOnly": False,
                                               "IsIgnored": True,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 2
                                           }
                                       ]
                                   },
                                   {
                                       "GroupNameId": 32855,
                                       "DisplayName": "IPv6 Information",
                                       "SubAttributeGroups": [],
                                       "Attributes": [
                                           {
                                               "AttributeId": 8186,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2207,
                                               "DisplayName": "IPv6 1 IPV6 Auto Config",
                                               "Description": None,
                                               "Value": "Enabled",
                                               "IsReadOnly": False,
                                               "IsIgnored": True,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 2
                                           },
                                           {
                                               "AttributeId": 7973,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2205,
                                               "DisplayName": "IPv6 1 IPV6 Enable",
                                               "Description": None,
                                               "Value": "Disabled",
                                               "IsReadOnly": False,
                                               "IsIgnored": True,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 2
                                           }
                                       ]
                                   },
                                   {
                                       "GroupNameId": 32856,
                                       "DisplayName": "IPv6 Static Information",
                                       "SubAttributeGroups": [],
                                       "Attributes": [
                                           {
                                               "AttributeId": 8244,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2405,
                                               "DisplayName": "IPv6Static 1 IPv6 Address 1",
                                               "Description": None,
                                               "Value": "::",
                                               "IsReadOnly": False,
                                               "IsIgnored": True,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 3
                                           },
                                           {
                                               "AttributeId": 7917,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2404,
                                               "DisplayName": "IPv6Static 1 IPv6 Gateway",
                                               "Description": None,
                                               "Value": "::",
                                               "IsReadOnly": False,
                                               "IsIgnored": True,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 2
                                           },
                                           {
                                               "AttributeId": 7687,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2408,
                                               "DisplayName": "IPv6Static 1 IPV6 Link Local Prefix Length",
                                               "Description": None,
                                               "Value": None,
                                               "IsReadOnly": False,
                                               "IsIgnored": True,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 3
                                           }
                                       ]
                                   },
                                   {
                                       "GroupNameId": 32930,
                                       "DisplayName": "NIC Information",
                                       "SubAttributeGroups": [],
                                       "Attributes": [
                                           {
                                               "AttributeId": 8111,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2193,
                                               "DisplayName": "NIC 1 DNS RAC Name",
                                               "Description": None,
                                               "Value": None,
                                               "IsReadOnly": False,
                                               "IsIgnored": True,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 3
                                           },
                                           {
                                               "AttributeId": 7189,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2194,
                                               "DisplayName": "NIC 1 Enable VLAN",
                                               "Description": None,
                                               "Value": "Disabled",
                                               "IsReadOnly": False,
                                               "IsIgnored": False,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 2
                                           },
                                           {
                                               "AttributeId": 7166,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2197,
                                               "DisplayName": "NIC 1 VLAN ID",
                                               "Description": None,
                                               "Value": "1",
                                               "IsReadOnly": False,
                                               "IsIgnored": False,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 2
                                           }
                                       ]
                                   },
                                   {
                                       "GroupNameId": 32934,
                                       "DisplayName": "NIC Static Information",
                                       "SubAttributeGroups": [],
                                       "Attributes": [
                                           {
                                               "AttributeId": 8116,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2396,
                                               "DisplayName": "NICStatic 1 DNS Domain Name",
                                               "Description": None,
                                               "Value": None,
                                               "IsReadOnly": False,
                                               "IsIgnored": True,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 3
                                           }
                                       ]
                                   }
                               ],
                               "Attributes": []
                           },
                           {
                               "GroupNameId": 4,
                               "DisplayName": "NIC",
                               "SubAttributeGroups": [
                                   {
                                       "GroupNameId": 66,
                                       "DisplayName": "NIC.Integrated.1-1-1",
                                       "SubAttributeGroups": [
                                           {
                                               "GroupNameId": 32761,
                                               "DisplayName": "FCoE Target 01",
                                               "SubAttributeGroups": [],
                                               "Attributes": [
                                                   {
                                                       "AttributeId": 6723,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4769,
                                                       "DisplayName": "Boot LUN",
                                                       "Description": None,
                                                       "Value": "0",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6735,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 5083,
                                                       "DisplayName": "Boot Order",
                                                       "Description": None,
                                                       "Value": "0",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": False,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6722,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4734,
                                                       "DisplayName": "Virtual LAN ID",
                                                       "Description": None,
                                                       "Value": "1",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6721,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4641,
                                                       "DisplayName": "World Wide Port Name Target",
                                                       "Description": None,
                                                       "Value": "00:00:00:00:00:00:00:00",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   }
                                               ]
                                           },
                                           {
                                               "GroupNameId": 32762,
                                               "DisplayName": "FCoE Target 02",
                                               "SubAttributeGroups": [],
                                               "Attributes": [
                                                   {
                                                       "AttributeId": 6733,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 5113,
                                                       "DisplayName": "Boot Order",
                                                       "Description": None,
                                                       "Value": "0",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": False,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   }
                                               ]
                                           },
                                           {
                                               "GroupNameId": 32763,
                                               "DisplayName": "FCoE Target 03",
                                               "SubAttributeGroups": [],
                                               "Attributes": [
                                                   {
                                                       "AttributeId": 6732,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 5122,
                                                       "DisplayName": "Boot Order",
                                                       "Description": None,
                                                       "Value": "0",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": False,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   }
                                               ]
                                           },
                                           {
                                               "GroupNameId": 32764,
                                               "DisplayName": "FCoE Target 04",
                                               "SubAttributeGroups": [],
                                               "Attributes": [
                                                   {
                                                       "AttributeId": 6734,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 5082,
                                                       "DisplayName": "Boot Order",
                                                       "Description": None,
                                                       "Value": "0",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": False,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   }
                                               ]
                                           },
                                           {
                                               "GroupNameId": 32870,
                                               "DisplayName": "iSCSI General Parameters",
                                               "SubAttributeGroups": [],
                                               "Attributes": [
                                                   {
                                                       "AttributeId": 6730,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4768,
                                                       "DisplayName": "CHAP Authentication",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 3
                                                   },
                                                   {
                                                       "AttributeId": 6729,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4767,
                                                       "DisplayName": "CHAP Mutual Authentication",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 3
                                                   }
                                               ]
                                           },
                                           {
                                               "GroupNameId": 32871,
                                               "DisplayName": "iSCSI Initiator Parameters",
                                               "SubAttributeGroups": [],
                                               "Attributes": [
                                                   {
                                                       "AttributeId": 6713,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4601,
                                                       "DisplayName": "CHAP ID",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6712,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4681,
                                                       "DisplayName": "CHAP Secret",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   }
                                               ]
                                           },
                                           {
                                               "GroupNameId": 32867,
                                               "DisplayName": "iSCSI Target 01",
                                               "SubAttributeGroups": [],
                                               "Attributes": [
                                                   {
                                                       "AttributeId": 6720,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4802,
                                                       "DisplayName": "Boot LUN",
                                                       "Description": None,
                                                       "Value": "0",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6719,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4920,
                                                       "DisplayName": "CHAP Secret",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6718,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4609,
                                                       "DisplayName": "IP Address",
                                                       "Description": None,
                                                       "Value": "0.0.0.0",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6717,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4537,
                                                       "DisplayName": "iSCSI Name",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6716,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4698,
                                                       "DisplayName": "TCP Port",
                                                       "Description": None,
                                                       "Value": "3260",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   }
                                               ]
                                           }
                                       ],
                                       "Attributes": []
                                   },
                                   {
                                       "GroupNameId": 67,
                                       "DisplayName": "NIC.Integrated.1-2-1",
                                       "SubAttributeGroups": [
                                           {
                                               "GroupNameId": 32761,
                                               "DisplayName": "FCoE Target 01",
                                               "SubAttributeGroups": [],
                                               "Attributes": [
                                                   {
                                                       "AttributeId": 6788,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4769,
                                                       "DisplayName": "Boot LUN",
                                                       "Description": None,
                                                       "Value": "0",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6801,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 5083,
                                                       "DisplayName": "Boot Order",
                                                       "Description": None,
                                                       "Value": "0",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": False,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6787,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4734,
                                                       "DisplayName": "Virtual LAN ID",
                                                       "Description": None,
                                                       "Value": "1",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6786,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4641,
                                                       "DisplayName": "World Wide Port Name Target",
                                                       "Description": None,
                                                       "Value": "00:00:00:00:00:00:00:00",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   }
                                               ]
                                           },
                                           {
                                               "GroupNameId": 32762,
                                               "DisplayName": "FCoE Target 02",
                                               "SubAttributeGroups": [],
                                               "Attributes": [
                                                   {
                                                       "AttributeId": 6799,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 5113,
                                                       "DisplayName": "Boot Order",
                                                       "Description": None,
                                                       "Value": "0",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": False,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   }
                                               ]
                                           },
                                           {
                                               "GroupNameId": 32763,
                                               "DisplayName": "FCoE Target 03",
                                               "SubAttributeGroups": [],
                                               "Attributes": [
                                                   {
                                                       "AttributeId": 6798,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 5122,
                                                       "DisplayName": "Boot Order",
                                                       "Description": None,
                                                       "Value": "0",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": False,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   }
                                               ]
                                           },
                                           {
                                               "GroupNameId": 32764,
                                               "DisplayName": "FCoE Target 04",
                                               "SubAttributeGroups": [],
                                               "Attributes": [
                                                   {
                                                       "AttributeId": 6800,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 5082,
                                                       "DisplayName": "Boot Order",
                                                       "Description": None,
                                                       "Value": "0",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": False,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   }
                                               ]
                                           },
                                           {
                                               "GroupNameId": 32870,
                                               "DisplayName": "iSCSI General Parameters",
                                               "SubAttributeGroups": [],
                                               "Attributes": [
                                                   {
                                                       "AttributeId": 6796,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4768,
                                                       "DisplayName": "CHAP Authentication",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 3
                                                   },
                                                   {
                                                       "AttributeId": 6795,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4767,
                                                       "DisplayName": "CHAP Mutual Authentication",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 3
                                                   }
                                               ]
                                           },
                                           {
                                               "GroupNameId": 32871,
                                               "DisplayName": "iSCSI Initiator Parameters",
                                               "SubAttributeGroups": [],
                                               "Attributes": [
                                                   {
                                                       "AttributeId": 6778,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4601,
                                                       "DisplayName": "CHAP ID",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6777,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4681,
                                                       "DisplayName": "CHAP Secret",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   }
                                               ]
                                           },
                                           {
                                               "GroupNameId": 32867,
                                               "DisplayName": "iSCSI Target 01",
                                               "SubAttributeGroups": [],
                                               "Attributes": [
                                                   {
                                                       "AttributeId": 6785,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4802,
                                                       "DisplayName": "Boot LUN",
                                                       "Description": None,
                                                       "Value": "0",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6784,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4920,
                                                       "DisplayName": "CHAP Secret",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6783,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4609,
                                                       "DisplayName": "IP Address",
                                                       "Description": None,
                                                       "Value": "0.0.0.0",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6782,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4537,
                                                       "DisplayName": "iSCSI Name",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6781,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4698,
                                                       "DisplayName": "TCP Port",
                                                       "Description": None,
                                                       "Value": "3260",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   }
                                               ]
                                           }
                                       ],
                                       "Attributes": []
                                   },
                                   {
                                       "GroupNameId": 65,
                                       "DisplayName": "NIC.Integrated.1-3-1",
                                       "SubAttributeGroups": [
                                           {
                                               "GroupNameId": 32870,
                                               "DisplayName": "iSCSI General Parameters",
                                               "SubAttributeGroups": [],
                                               "Attributes": [
                                                   {
                                                       "AttributeId": 6677,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4768,
                                                       "DisplayName": "CHAP Authentication",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 3
                                                   },
                                                   {
                                                       "AttributeId": 6676,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4767,
                                                       "DisplayName": "CHAP Mutual Authentication",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 3
                                                   }
                                               ]
                                           },
                                           {
                                               "GroupNameId": 32871,
                                               "DisplayName": "iSCSI Initiator Parameters",
                                               "SubAttributeGroups": [],
                                               "Attributes": [
                                                   {
                                                       "AttributeId": 6664,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4601,
                                                       "DisplayName": "CHAP ID",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6663,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4681,
                                                       "DisplayName": "CHAP Secret",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   }
                                               ]
                                           },
                                           {
                                               "GroupNameId": 32867,
                                               "DisplayName": "iSCSI Target 01",
                                               "SubAttributeGroups": [],
                                               "Attributes": [
                                                   {
                                                       "AttributeId": 6671,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4802,
                                                       "DisplayName": "Boot LUN",
                                                       "Description": None,
                                                       "Value": "0",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6670,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4920,
                                                       "DisplayName": "CHAP Secret",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6669,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4609,
                                                       "DisplayName": "IP Address",
                                                       "Description": None,
                                                       "Value": "0.0.0.0",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6668,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4537,
                                                       "DisplayName": "iSCSI Name",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6667,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4698,
                                                       "DisplayName": "TCP Port",
                                                       "Description": None,
                                                       "Value": "3260",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   }
                                               ]
                                           }
                                       ],
                                       "Attributes": []
                                   },
                                   {
                                       "GroupNameId": 68,
                                       "DisplayName": "NIC.Integrated.1-4-1",
                                       "SubAttributeGroups": [
                                           {
                                               "GroupNameId": 32870,
                                               "DisplayName": "iSCSI General Parameters",
                                               "SubAttributeGroups": [],
                                               "Attributes": [
                                                   {
                                                       "AttributeId": 6852,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4768,
                                                       "DisplayName": "CHAP Authentication",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 3
                                                   },
                                                   {
                                                       "AttributeId": 6851,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4767,
                                                       "DisplayName": "CHAP Mutual Authentication",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 3
                                                   }
                                               ]
                                           },
                                           {
                                               "GroupNameId": 32871,
                                               "DisplayName": "iSCSI Initiator Parameters",
                                               "SubAttributeGroups": [],
                                               "Attributes": [
                                                   {
                                                       "AttributeId": 6838,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4601,
                                                       "DisplayName": "CHAP ID",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6837,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4681,
                                                       "DisplayName": "CHAP Secret",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   }
                                               ]
                                           },
                                           {
                                               "GroupNameId": 32867,
                                               "DisplayName": "iSCSI Target 01",
                                               "SubAttributeGroups": [],
                                               "Attributes": [
                                                   {
                                                       "AttributeId": 6846,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4802,
                                                       "DisplayName": "Boot LUN",
                                                       "Description": None,
                                                       "Value": "0",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6845,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4920,
                                                       "DisplayName": "CHAP Secret",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6844,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4609,
                                                       "DisplayName": "IP Address",
                                                       "Description": None,
                                                       "Value": "0.0.0.0",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6843,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4537,
                                                       "DisplayName": "iSCSI Name",
                                                       "Description": None,
                                                       "Value": None,
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
                                                   },
                                                   {
                                                       "AttributeId": 6842,
                                                       "CustomId": 0,
                                                       "AttributeEditInfoId": 4698,
                                                       "DisplayName": "TCP Port",
                                                       "Description": None,
                                                       "Value": "3260",
                                                       "IsReadOnly": False,
                                                       "IsIgnored": True,
                                                       "IsSecure": False,
                                                       "IsLinkedToSecure": False,
                                                       "TargetSpecificTypeId": 2
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
                               "GroupNameId": 5,
                               "DisplayName": "System",
                               "SubAttributeGroups": [
                                   {
                                       "GroupNameId": 33016,
                                       "DisplayName": "Server Operating System",
                                       "SubAttributeGroups": [],
                                       "Attributes": [
                                           {
                                               "AttributeId": 8513,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2497,
                                               "DisplayName": "ServerOS 1 Server Host Name",
                                               "Description": None,
                                               "Value": None,
                                               "IsReadOnly": False,
                                               "IsIgnored": True,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 3
                                           }
                                       ]
                                   },
                                   {
                                       "GroupNameId": 33019,
                                       "DisplayName": "Server Topology",
                                       "SubAttributeGroups": [],
                                       "Attributes": [
                                           {
                                               "AttributeId": 8593,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2248,
                                               "DisplayName": "ServerTopology 1 Aisle Name",
                                               "Description": None,
                                               "Value": None,
                                               "IsReadOnly": False,
                                               "IsIgnored": True,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 2
                                           },
                                           {
                                               "AttributeId": 8551,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2247,
                                               "DisplayName": "ServerTopology 1 Data Center Name",
                                               "Description": None,
                                               "Value": None,
                                               "IsReadOnly": False,
                                               "IsIgnored": True,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 2
                                           },
                                           {
                                               "AttributeId": 8371,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2249,
                                               "DisplayName": "ServerTopology 1 Rack Name",
                                               "Description": None,
                                               "Value": None,
                                               "IsReadOnly": False,
                                               "IsIgnored": True,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 3
                                           },
                                           {
                                               "AttributeId": 8370,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2250,
                                               "DisplayName": "ServerTopology 1 Rack Slot",
                                               "Description": None,
                                               "Value": None,
                                               "IsReadOnly": False,
                                               "IsIgnored": True,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 3
                                           },
                                           {
                                               "AttributeId": 8346,
                                               "CustomId": 0,
                                               "AttributeEditInfoId": 2500,
                                               "DisplayName": "ServerTopology 1 Room Name",
                                               "Description": None,
                                               "Value": None,
                                               "IsReadOnly": False,
                                               "IsIgnored": True,
                                               "IsSecure": False,
                                               "IsLinkedToSecure": False,
                                               "TargetSpecificTypeId": 2
                                           }
                                       ]
                                   }
                               ],
                               "Attributes": []
                           }]
                       },
         'message': SUCCESS_MSG, "success": True, 'case': "template with id",
         'mparams': {"template_id": 1234}},
        {"json_data": {"value": [{'Id': 1234, 'Name': "temp1", "Type": 1000}]},
         'message': SUCCESS_MSG, "success": True, 'case': "template with name",
         'mparams': {"template_name": "temp1"}},
        {"json_data": {"value": [{'Id': 1234, 'Name': "temp2", "Type": 1000}]},
         'message': "Template with name 'temp1' not found.", "success": True, 'case': "template with name",
         'mparams': {"template_name": "temp1"}},
        {"json_data": {'Id': 1234, 'Name': "temp1", "Type": 1000},
         'message': SUCCESS_MSG, "success": True, 'case': "profile with id",
         'mparams': {"profile_id": 1234}},
        {"json_data": {"value": [{'Id': 1235, 'ProfileName': "prof0", "Type": 1000},
                                 {'Id': 1234, 'ProfileName': "prof1", "Type": 1000}]},
         'message': SUCCESS_MSG, "success": True, 'case': "profile with name",
         'mparams': {"profile_name": "prof1"}},
        {"json_data": {"value": [{'Id': 1235, 'ProfileName': "prof0", "Type": 1000},
                                 {'Id': 1234, 'ProfileName': "prof1", "Type": 1000}]},
         'message': "Profiles with profile_name prof2 not found.", "success": True, 'case': "profile with name",
         'mparams': {"profile_name": "prof2"}},
        {"json_data": {"value": [{'Id': 1234, 'Name': "prof1", "Type": 1000}]},
         'message': SUCCESS_MSG, "success": True, 'case': "template with name",
         'mparams': {"system_query_options": {"filter": "ProfileName eq 'prof2'"}}},
        {"json_data": {"value": [{'Id': 1234, 'Name': "prof1", "Type": 1000}]},
         'message': SUCCESS_MSG, "success": True, 'case': "template with name",
         'mparams': {}},
    ])
    def test_ome_profile_info_success(self, params, ome_connection_mock_for_profile_info, ome_response_mock,
                                      ome_default_args, module_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['json_data']
        ome_connection_mock_for_profile_info.get_all_items_with_pagination.return_value = params['json_data']
        ome_default_args.update(params['mparams'])
        result = self._run_module(ome_default_args, check_mode=params.get('check_mode', False))
        assert result['msg'] == params['message']

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_profile_info_main_exception_failure_case(self, exc_type, mocker, ome_default_args,
                                                          ome_connection_mock_for_profile_info, ome_response_mock):
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
