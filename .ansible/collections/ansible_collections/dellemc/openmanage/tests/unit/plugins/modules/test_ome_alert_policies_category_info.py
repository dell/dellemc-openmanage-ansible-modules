# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.2.0
# Copyright (C) 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
from io import StringIO

import pytest
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import ome_alert_policies_category_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_alert_policies_category_info.'
SUCCESS_MSG = "Successfully retrieved alert policies category information."


@pytest.fixture
def ome_connection_mock_for_alert_category(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeAlertCategoryInfo(FakeAnsibleModule):
    module = ome_alert_policies_category_info

    @pytest.mark.parametrize("params", [
        {"message": SUCCESS_MSG,
            "json_data": {
                "@odata.context": "/api/$metadata#Collection(AlertService.AlertCategories)",
                "@odata.count": 13,
                "value": [
                    {
                        "@odata.type": "#AlertService.AlertCategories",
                        "@odata.id": "/api/AlertService/AlertCategories('Application')",
                        "Name": "Application",
                        "IsBuiltIn": True,
                        "CategoriesDetails": [
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 4,
                                "Name": "Audit",
                                "CatalogName": "Application",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 90,
                                        "Name": "Devices",
                                        "Description": "Devices"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 10,
                                        "Name": "Generic",
                                        "Description": "Generic"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 151,
                                        "Name": "Power Configuration",
                                        "Description": "Power Configuration"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 35,
                                        "Name": "Users",
                                        "Description": "Users"
                                    }
                                ]
                            },
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 5,
                                "Name": "Configuration",
                                "CatalogName": "Application",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 85,
                                        "Name": "Application",
                                        "Description": "Application"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 116,
                                        "Name": "Device Warranty",
                                        "Description": "Device Warranty"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 90,
                                        "Name": "Devices",
                                        "Description": "Devices"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 36,
                                        "Name": "Discovery",
                                        "Description": "Discovery"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 10,
                                        "Name": "Generic",
                                        "Description": "Generic"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 84,
                                        "Name": "Groups",
                                        "Description": "Groups"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 47,
                                        "Name": "Job",
                                        "Description": "Job"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 118,
                                        "Name": "Metrics",
                                        "Description": "Metrics"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 20,
                                        "Name": "Miscellaneous",
                                        "Description": "Miscellaneous"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 93,
                                        "Name": "Monitoring",
                                        "Description": "Monitoring"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 151,
                                        "Name": "Power Configuration",
                                        "Description": "Power Configuration"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 31,
                                        "Name": "Reports",
                                        "Description": "Reports"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 9,
                                        "Name": "Security",
                                        "Description": "Security"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 88,
                                        "Name": "Templates",
                                        "Description": "Templates"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 35,
                                        "Name": "Users",
                                        "Description": "Users"
                                    }
                                ]
                            },
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 7,
                                "Name": "Miscellaneous",
                                "CatalogName": "Application",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 20,
                                        "Name": "Miscellaneous",
                                        "Description": "Miscellaneous"
                                    }
                                ]
                            },
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 2,
                                "Name": "Storage",
                                "CatalogName": "Application",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 90,
                                        "Name": "Devices",
                                        "Description": "Devices"
                                    }
                                ]
                            },
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 1,
                                "Name": "System Health",
                                "CatalogName": "Application",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 90,
                                        "Name": "Devices",
                                        "Description": "Devices"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 7400,
                                        "Name": "Health Status of Managed device",
                                        "Description": "Health Status of Managed device"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 47,
                                        "Name": "Job",
                                        "Description": "Job"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 118,
                                        "Name": "Metrics",
                                        "Description": "Metrics"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 151,
                                        "Name": "Power Configuration",
                                        "Description": "Power Configuration"
                                    }
                                ]
                            },
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 3,
                                "Name": "Updates",
                                "CatalogName": "Application",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 85,
                                        "Name": "Application",
                                        "Description": "Application"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 112,
                                        "Name": "Firmware",
                                        "Description": "Firmware"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "@odata.type": "#AlertService.AlertCategories",
                        "@odata.id": "/api/AlertService/AlertCategories('Dell%20Storage')",
                        "Name": "Dell Storage",
                        "IsBuiltIn": True,
                        "CategoriesDetails": [
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 2,
                                "Name": "Storage",
                                "CatalogName": "Dell Storage",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 7700,
                                        "Name": "Other",
                                        "Description": "Other"
                                    }
                                ]
                            },
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 1,
                                "Name": "System Health",
                                "CatalogName": "Dell Storage",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 7700,
                                        "Name": "Other",
                                        "Description": "Other"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 18,
                                        "Name": "Storage",
                                        "Description": "Storage"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "@odata.type": "#AlertService.AlertCategories",
                        "@odata.id": "/api/AlertService/AlertCategories('iDRAC')",
                        "Name": "iDRAC",
                        "IsBuiltIn": True,
                        "CategoriesDetails": [
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 4,
                                "Name": "Audit",
                                "CatalogName": "iDRAC",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 41,
                                        "Name": "Auto System Reset",
                                        "Description": "Auto System Reset"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 54,
                                        "Name": "BIOS Management",
                                        "Description": "BIOS Management"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 75,
                                        "Name": "BIOS POST",
                                        "Description": "BIOS POST"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 12,
                                        "Name": "Debug",
                                        "Description": "Debug"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 53,
                                        "Name": "Group Manager",
                                        "Description": "Group Manager"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 11,
                                        "Name": "Hardware Config",
                                        "Description": "Hardware Config"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 45,
                                        "Name": "iDRAC Service Module",
                                        "Description": "iDRAC Service Module"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 114,
                                        "Name": "IP Address",
                                        "Description": "IP Address"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 122,
                                        "Name": "iSM PEEK Component",
                                        "Description": "iSM PEEK Component"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 48,
                                        "Name": "Licensing",
                                        "Description": "Licensing"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 15,
                                        "Name": "Management Module",
                                        "Description": "Management Module"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 96,
                                        "Name": "OS Event",
                                        "Description": "OS Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 7700,
                                        "Name": "Other",
                                        "Description": "Other"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 81,
                                        "Name": "PCI Device",
                                        "Description": "PCI Device"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 78,
                                        "Name": "Power Supply",
                                        "Description": "Power Supply"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 23,
                                        "Name": "Power Usage",
                                        "Description": "Power Usage"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 28,
                                        "Name": "Power Usage POW",
                                        "Description": "Power Usage POW"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 109,
                                        "Name": "RAC Event",
                                        "Description": "RAC Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 120,
                                        "Name": "Secure Enterprise Key Management",
                                        "Description": "Secure Enterprise Key Management"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 25,
                                        "Name": "Security Event",
                                        "Description": "Security Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 52,
                                        "Name": "Software Change",
                                        "Description": "Software Change"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 39,
                                        "Name": "Software Config",
                                        "Description": "Software Config"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 92,
                                        "Name": "Support Assist",
                                        "Description": "Support Assist"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 71,
                                        "Name": "System Info",
                                        "Description": "System Info"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 55,
                                        "Name": "UEFI Event",
                                        "Description": "UEFI Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 56,
                                        "Name": "User Tracking",
                                        "Description": "User Tracking"
                                    }
                                ]
                            },
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 5,
                                "Name": "Configuration",
                                "CatalogName": "iDRAC",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 49,
                                        "Name": "Auto-Discovery",
                                        "Description": "Auto-Discovery"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 107,
                                        "Name": "Backup/Restore",
                                        "Description": "Backup/Restore"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 54,
                                        "Name": "BIOS Management",
                                        "Description": "BIOS Management"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 104,
                                        "Name": "BOOT Control",
                                        "Description": "BOOT Control"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 59,
                                        "Name": "Certificate Management",
                                        "Description": "Certificate Management"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 51,
                                        "Name": "Firmware Download",
                                        "Description": "Firmware Download"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 53,
                                        "Name": "Group Manager",
                                        "Description": "Group Manager"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 11,
                                        "Name": "Hardware Config",
                                        "Description": "Hardware Config"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 98,
                                        "Name": "IO Identity Optimization",
                                        "Description": "IO Identity Optimization"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 105,
                                        "Name": "IO Virtualization",
                                        "Description": "IO Virtualization"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 114,
                                        "Name": "IP Address",
                                        "Description": "IP Address"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 27,
                                        "Name": "Job Control",
                                        "Description": "Job Control"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 57,
                                        "Name": "Lifecycle Controller",
                                        "Description": "Lifecycle Controller"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 3,
                                        "Name": "Link Status",
                                        "Description": "Link Status"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 123,
                                        "Name": "Liquid Cooling System",
                                        "Description": "Liquid Cooling System"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 19,
                                        "Name": "Log Event",
                                        "Description": "Log Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 15,
                                        "Name": "Management Module",
                                        "Description": "Management Module"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 80,
                                        "Name": "Memory",
                                        "Description": "Memory"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 102,
                                        "Name": "NIC Configuration",
                                        "Description": "NIC Configuration"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 97,
                                        "Name": "OS Deployment",
                                        "Description": "OS Deployment"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 81,
                                        "Name": "PCI Device",
                                        "Description": "PCI Device"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 23,
                                        "Name": "Power Usage",
                                        "Description": "Power Usage"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 61,
                                        "Name": "Processor",
                                        "Description": "Processor"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 109,
                                        "Name": "RAC Event",
                                        "Description": "RAC Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 120,
                                        "Name": "Secure Enterprise Key Management",
                                        "Description": "Secure Enterprise Key Management"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 25,
                                        "Name": "Security Event",
                                        "Description": "Security Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 39,
                                        "Name": "Software Config",
                                        "Description": "Software Config"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 18,
                                        "Name": "Storage",
                                        "Description": "Storage"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 113,
                                        "Name": "Storage Controller",
                                        "Description": "Storage Controller"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 92,
                                        "Name": "Support Assist",
                                        "Description": "Support Assist"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 29,
                                        "Name": "System Event Log",
                                        "Description": "System Event Log"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 71,
                                        "Name": "System Info",
                                        "Description": "System Info"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 79,
                                        "Name": "Test Alert",
                                        "Description": "Test Alert"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 55,
                                        "Name": "UEFI Event",
                                        "Description": "UEFI Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 66,
                                        "Name": "vFlash Event",
                                        "Description": "vFlash Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 7,
                                        "Name": "Virtual Console",
                                        "Description": "Virtual Console"
                                    }
                                ]
                            },
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 2,
                                "Name": "Storage",
                                "CatalogName": "iDRAC",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 108,
                                        "Name": "Battery Event",
                                        "Description": "Battery Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 106,
                                        "Name": "Fan Event",
                                        "Description": "Fan Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 11,
                                        "Name": "Hardware Config",
                                        "Description": "Hardware Config"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 94,
                                        "Name": "Physical Disk",
                                        "Description": "Physical Disk"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 78,
                                        "Name": "Power Supply",
                                        "Description": "Power Supply"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 23,
                                        "Name": "Power Usage",
                                        "Description": "Power Usage"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 109,
                                        "Name": "RAC Event",
                                        "Description": "RAC Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 44,
                                        "Name": "Redundancy",
                                        "Description": "Redundancy"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 25,
                                        "Name": "Security Event",
                                        "Description": "Security Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 52,
                                        "Name": "Software Change",
                                        "Description": "Software Change"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 119,
                                        "Name": "Software Defined Storage",
                                        "Description": "Software Defined Storage"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 18,
                                        "Name": "Storage",
                                        "Description": "Storage"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 113,
                                        "Name": "Storage Controller",
                                        "Description": "Storage Controller"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 82,
                                        "Name": "Storage Enclosure",
                                        "Description": "Storage Enclosure"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 110,
                                        "Name": "Temperature",
                                        "Description": "Temperature"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 46,
                                        "Name": "Virtual Disk",
                                        "Description": "Virtual Disk"
                                    }
                                ]
                            },
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 1,
                                "Name": "System Health",
                                "CatalogName": "iDRAC",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 67,
                                        "Name": "Amperage",
                                        "Description": "Amperage"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 41,
                                        "Name": "Auto System Reset",
                                        "Description": "Auto System Reset"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 108,
                                        "Name": "Battery Event",
                                        "Description": "Battery Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 75,
                                        "Name": "BIOS POST",
                                        "Description": "BIOS POST"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 89,
                                        "Name": "Cable",
                                        "Description": "Cable"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 106,
                                        "Name": "Fan Event",
                                        "Description": "Fan Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 83,
                                        "Name": "Fibre Channel",
                                        "Description": "Fibre Channel"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 11,
                                        "Name": "Hardware Config",
                                        "Description": "Hardware Config"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 45,
                                        "Name": "iDRAC Service Module",
                                        "Description": "iDRAC Service Module"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 111,
                                        "Name": "IDSDM Redundancy",
                                        "Description": "IDSDM Redundancy"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 105,
                                        "Name": "IO Virtualization",
                                        "Description": "IO Virtualization"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 3,
                                        "Name": "Link Status",
                                        "Description": "Link Status"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 123,
                                        "Name": "Liquid Cooling System",
                                        "Description": "Liquid Cooling System"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 19,
                                        "Name": "Log Event",
                                        "Description": "Log Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 15,
                                        "Name": "Management Module",
                                        "Description": "Management Module"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 80,
                                        "Name": "Memory",
                                        "Description": "Memory"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 102,
                                        "Name": "NIC Configuration",
                                        "Description": "NIC Configuration"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 96,
                                        "Name": "OS Event",
                                        "Description": "OS Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 7700,
                                        "Name": "Other",
                                        "Description": "Other"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 81,
                                        "Name": "PCI Device",
                                        "Description": "PCI Device"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 94,
                                        "Name": "Physical Disk",
                                        "Description": "Physical Disk"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 78,
                                        "Name": "Power Supply",
                                        "Description": "Power Supply"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 23,
                                        "Name": "Power Usage",
                                        "Description": "Power Usage"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 61,
                                        "Name": "Processor",
                                        "Description": "Processor"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 68,
                                        "Name": "Processor Absent",
                                        "Description": "Processor Absent"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 103,
                                        "Name": "PSU Absent",
                                        "Description": "PSU Absent"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 109,
                                        "Name": "RAC Event",
                                        "Description": "RAC Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 44,
                                        "Name": "Redundancy",
                                        "Description": "Redundancy"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 120,
                                        "Name": "Secure Enterprise Key Management",
                                        "Description": "Secure Enterprise Key Management"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 25,
                                        "Name": "Security Event",
                                        "Description": "Security Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 39,
                                        "Name": "Software Config",
                                        "Description": "Software Config"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 18,
                                        "Name": "Storage",
                                        "Description": "Storage"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 92,
                                        "Name": "Support Assist",
                                        "Description": "Support Assist"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 29,
                                        "Name": "System Event Log",
                                        "Description": "System Event Log"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 71,
                                        "Name": "System Info",
                                        "Description": "System Info"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 13,
                                        "Name": "System Performance Event",
                                        "Description": "System Performance Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 110,
                                        "Name": "Temperature",
                                        "Description": "Temperature"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 16,
                                        "Name": "Temperature Statistics",
                                        "Description": "Temperature Statistics"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 55,
                                        "Name": "UEFI Event",
                                        "Description": "UEFI Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 5,
                                        "Name": "vFlash Absent",
                                        "Description": "vFlash Absent"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 66,
                                        "Name": "vFlash Event",
                                        "Description": "vFlash Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 7,
                                        "Name": "Virtual Console",
                                        "Description": "Virtual Console"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 46,
                                        "Name": "Virtual Disk",
                                        "Description": "Virtual Disk"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 40,
                                        "Name": "Voltage",
                                        "Description": "Voltage"
                                    }
                                ]
                            },
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 3,
                                "Name": "Updates",
                                "CatalogName": "iDRAC",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 51,
                                        "Name": "Firmware Download",
                                        "Description": "Firmware Download"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 24,
                                        "Name": "Firmware Update Job",
                                        "Description": "Firmware Update Job"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 53,
                                        "Name": "Group Manager",
                                        "Description": "Group Manager"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 27,
                                        "Name": "Job Control",
                                        "Description": "Job Control"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 109,
                                        "Name": "RAC Event",
                                        "Description": "RAC Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 52,
                                        "Name": "Software Change",
                                        "Description": "Software Change"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 71,
                                        "Name": "System Info",
                                        "Description": "System Info"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 55,
                                        "Name": "UEFI Event",
                                        "Description": "UEFI Event"
                                    }
                                ]
                            },
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 6,
                                "Name": "Work Notes",
                                "CatalogName": "iDRAC",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 54,
                                        "Name": "BIOS Management",
                                        "Description": "BIOS Management"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "@odata.type": "#AlertService.AlertCategories",
                        "@odata.id": "/api/AlertService/AlertCategories('IF-MIB')",
                        "Name": "IF-MIB",
                        "IsBuiltIn": True,
                        "CategoriesDetails": [
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 4,
                                "Name": "Audit",
                                "CatalogName": "IF-MIB",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 101,
                                        "Name": "Interface",
                                        "Description": "Interface"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "@odata.type": "#AlertService.AlertCategories",
                        "@odata.id": "/api/AlertService/AlertCategories('Internal%20Events%20Catalog')",
                        "Name": "Internal Events Catalog",
                        "IsBuiltIn": True,
                        "CategoriesDetails": [
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 4,
                                "Name": "Audit",
                                "CatalogName": "Internal Events Catalog",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 54,
                                        "Name": "BIOS Management",
                                        "Description": "BIOS Management"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 12,
                                        "Name": "Debug",
                                        "Description": "Debug"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 90,
                                        "Name": "Devices",
                                        "Description": "Devices"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 115,
                                        "Name": "Fabric",
                                        "Description": "Fabric"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 106,
                                        "Name": "Fan Event",
                                        "Description": "Fan Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 21,
                                        "Name": "Feature Card",
                                        "Description": "Feature Card"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 10,
                                        "Name": "Generic",
                                        "Description": "Generic"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 53,
                                        "Name": "Group Manager",
                                        "Description": "Group Manager"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 11,
                                        "Name": "Hardware Config",
                                        "Description": "Hardware Config"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 45,
                                        "Name": "iDRAC Service Module",
                                        "Description": "iDRAC Service Module"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 101,
                                        "Name": "Interface",
                                        "Description": "Interface"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 114,
                                        "Name": "IP Address",
                                        "Description": "IP Address"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 27,
                                        "Name": "Job Control",
                                        "Description": "Job Control"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 48,
                                        "Name": "Licensing",
                                        "Description": "Licensing"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 57,
                                        "Name": "Lifecycle Controller",
                                        "Description": "Lifecycle Controller"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 32,
                                        "Name": "Link",
                                        "Description": "Link"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 3,
                                        "Name": "Link Status",
                                        "Description": "Link Status"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 19,
                                        "Name": "Log Event",
                                        "Description": "Log Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 15,
                                        "Name": "Management Module",
                                        "Description": "Management Module"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 80,
                                        "Name": "Memory",
                                        "Description": "Memory"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 77,
                                        "Name": "Node",
                                        "Description": "Node"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 81,
                                        "Name": "PCI Device",
                                        "Description": "PCI Device"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 151,
                                        "Name": "Power Configuration",
                                        "Description": "Power Configuration"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 78,
                                        "Name": "Power Supply",
                                        "Description": "Power Supply"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 23,
                                        "Name": "Power Usage",
                                        "Description": "Power Usage"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 109,
                                        "Name": "RAC Event",
                                        "Description": "RAC Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 44,
                                        "Name": "Redundancy",
                                        "Description": "Redundancy"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 95,
                                        "Name": "REST",
                                        "Description": "REST"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 9,
                                        "Name": "Security",
                                        "Description": "Security"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 14,
                                        "Name": "Server",
                                        "Description": "Server"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 52,
                                        "Name": "Software Change",
                                        "Description": "Software Change"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 39,
                                        "Name": "Software Config",
                                        "Description": "Software Config"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 92,
                                        "Name": "Support Assist",
                                        "Description": "Support Assist"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 71,
                                        "Name": "System Info",
                                        "Description": "System Info"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 110,
                                        "Name": "Temperature",
                                        "Description": "Temperature"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 56,
                                        "Name": "User Tracking",
                                        "Description": "User Tracking"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 35,
                                        "Name": "Users",
                                        "Description": "Users"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 50,
                                        "Name": "Virtual Media",
                                        "Description": "Virtual Media"
                                    }
                                ]
                            },
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 5,
                                "Name": "Configuration",
                                "CatalogName": "Internal Events Catalog",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 49,
                                        "Name": "Auto-Discovery",
                                        "Description": "Auto-Discovery"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 107,
                                        "Name": "Backup/Restore",
                                        "Description": "Backup/Restore"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 54,
                                        "Name": "BIOS Management",
                                        "Description": "BIOS Management"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 104,
                                        "Name": "BOOT Control",
                                        "Description": "BOOT Control"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 59,
                                        "Name": "Certificate Management",
                                        "Description": "Certificate Management"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 4,
                                        "Name": "Chassis",
                                        "Description": "Chassis"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 8,
                                        "Name": "Common",
                                        "Description": "Common"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 116,
                                        "Name": "Device Warranty",
                                        "Description": "Device Warranty"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 90,
                                        "Name": "Devices",
                                        "Description": "Devices"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 34,
                                        "Name": "Diagnostics",
                                        "Description": "Diagnostics"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 115,
                                        "Name": "Fabric",
                                        "Description": "Fabric"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 70,
                                        "Name": "Fabric NVFA",
                                        "Description": "Fabric NVFA"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 106,
                                        "Name": "Fan Event",
                                        "Description": "Fan Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 83,
                                        "Name": "Fibre Channel",
                                        "Description": "Fibre Channel"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 51,
                                        "Name": "Firmware Download",
                                        "Description": "Firmware Download"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 53,
                                        "Name": "Group Manager",
                                        "Description": "Group Manager"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 84,
                                        "Name": "Groups",
                                        "Description": "Groups"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 11,
                                        "Name": "Hardware Config",
                                        "Description": "Hardware Config"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 86,
                                        "Name": "Interface NVIF",
                                        "Description": "Interface NVIF"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 98,
                                        "Name": "IO Identity Optimization",
                                        "Description": "IO Identity Optimization"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 114,
                                        "Name": "IP Address",
                                        "Description": "IP Address"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 27,
                                        "Name": "Job Control",
                                        "Description": "Job Control"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 48,
                                        "Name": "Licensing",
                                        "Description": "Licensing"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 57,
                                        "Name": "Lifecycle Controller",
                                        "Description": "Lifecycle Controller"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 19,
                                        "Name": "Log Event",
                                        "Description": "Log Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 15,
                                        "Name": "Management Module",
                                        "Description": "Management Module"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 37,
                                        "Name": "Network",
                                        "Description": "Network"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 102,
                                        "Name": "NIC Configuration",
                                        "Description": "NIC Configuration"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 77,
                                        "Name": "Node",
                                        "Description": "Node"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 73,
                                        "Name": "Node NVNO",
                                        "Description": "Node NVNO"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 97,
                                        "Name": "OS Deployment",
                                        "Description": "OS Deployment"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 1,
                                        "Name": "Part Replacement",
                                        "Description": "Part Replacement"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 81,
                                        "Name": "PCI Device",
                                        "Description": "PCI Device"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 151,
                                        "Name": "Power Configuration",
                                        "Description": "Power Configuration"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 78,
                                        "Name": "Power Supply",
                                        "Description": "Power Supply"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 23,
                                        "Name": "Power Usage",
                                        "Description": "Power Usage"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 109,
                                        "Name": "RAC Event",
                                        "Description": "RAC Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 22,
                                        "Name": "Remote Service",
                                        "Description": "Remote Service"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 95,
                                        "Name": "REST",
                                        "Description": "REST"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 63,
                                        "Name": "SAS IOM",
                                        "Description": "SAS IOM"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 9,
                                        "Name": "Security",
                                        "Description": "Security"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 25,
                                        "Name": "Security Event",
                                        "Description": "Security Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 30,
                                        "Name": "Server Interface",
                                        "Description": "Server Interface"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 39,
                                        "Name": "Software Config",
                                        "Description": "Software Config"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 18,
                                        "Name": "Storage",
                                        "Description": "Storage"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 6,
                                        "Name": "Subscription",
                                        "Description": "Subscription"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 92,
                                        "Name": "Support Assist",
                                        "Description": "Support Assist"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 71,
                                        "Name": "System Info",
                                        "Description": "System Info"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 88,
                                        "Name": "Templates",
                                        "Description": "Templates"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 79,
                                        "Name": "Test Alert",
                                        "Description": "Test Alert"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 43,
                                        "Name": "Topology",
                                        "Description": "Topology"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 17,
                                        "Name": "Topology Graph",
                                        "Description": "Topology Graph"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 55,
                                        "Name": "UEFI Event",
                                        "Description": "UEFI Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 33,
                                        "Name": "Uplink",
                                        "Description": "Uplink"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 56,
                                        "Name": "User Tracking",
                                        "Description": "User Tracking"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 35,
                                        "Name": "Users",
                                        "Description": "Users"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 66,
                                        "Name": "vFlash Event",
                                        "Description": "vFlash Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 74,
                                        "Name": "vFlash Media",
                                        "Description": "vFlash Media"
                                    }
                                ]
                            },
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 7,
                                "Name": "Miscellaneous",
                                "CatalogName": "Internal Events Catalog",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 85,
                                        "Name": "Application",
                                        "Description": "Application"
                                    }
                                ]
                            },
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 2,
                                "Name": "Storage",
                                "CatalogName": "Internal Events Catalog",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 108,
                                        "Name": "Battery Event",
                                        "Description": "Battery Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 89,
                                        "Name": "Cable",
                                        "Description": "Cable"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 34,
                                        "Name": "Diagnostics",
                                        "Description": "Diagnostics"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 106,
                                        "Name": "Fan Event",
                                        "Description": "Fan Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 100,
                                        "Name": "Fluid Cache",
                                        "Description": "Fluid Cache"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 11,
                                        "Name": "Hardware Config",
                                        "Description": "Hardware Config"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 94,
                                        "Name": "Physical Disk",
                                        "Description": "Physical Disk"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 78,
                                        "Name": "Power Supply",
                                        "Description": "Power Supply"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 109,
                                        "Name": "RAC Event",
                                        "Description": "RAC Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 63,
                                        "Name": "SAS IOM",
                                        "Description": "SAS IOM"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 25,
                                        "Name": "Security Event",
                                        "Description": "Security Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 52,
                                        "Name": "Software Change",
                                        "Description": "Software Change"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 99,
                                        "Name": "SSD Devices",
                                        "Description": "SSD Devices"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 18,
                                        "Name": "Storage",
                                        "Description": "Storage"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 113,
                                        "Name": "Storage Controller",
                                        "Description": "Storage Controller"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 82,
                                        "Name": "Storage Enclosure",
                                        "Description": "Storage Enclosure"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 110,
                                        "Name": "Temperature",
                                        "Description": "Temperature"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 46,
                                        "Name": "Virtual Disk",
                                        "Description": "Virtual Disk"
                                    }
                                ]
                            },
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 1,
                                "Name": "System Health",
                                "CatalogName": "Internal Events Catalog",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 67,
                                        "Name": "Amperage",
                                        "Description": "Amperage"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 41,
                                        "Name": "Auto System Reset",
                                        "Description": "Auto System Reset"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 108,
                                        "Name": "Battery Event",
                                        "Description": "Battery Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 75,
                                        "Name": "BIOS POST",
                                        "Description": "BIOS POST"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 89,
                                        "Name": "Cable",
                                        "Description": "Cable"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 69,
                                        "Name": "Dell Key Manager",
                                        "Description": "Dell Key Manager"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 90,
                                        "Name": "Devices",
                                        "Description": "Devices"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 34,
                                        "Name": "Diagnostics",
                                        "Description": "Diagnostics"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 115,
                                        "Name": "Fabric",
                                        "Description": "Fabric"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 70,
                                        "Name": "Fabric NVFA",
                                        "Description": "Fabric NVFA"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 106,
                                        "Name": "Fan Event",
                                        "Description": "Fan Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 83,
                                        "Name": "Fibre Channel",
                                        "Description": "Fibre Channel"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 64,
                                        "Name": "FlexAddress SD",
                                        "Description": "FlexAddress SD"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 11,
                                        "Name": "Hardware Config",
                                        "Description": "Hardware Config"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 62,
                                        "Name": "IDSDM Absent",
                                        "Description": "IDSDM Absent"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 65,
                                        "Name": "IDSDM Media",
                                        "Description": "IDSDM Media"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 111,
                                        "Name": "IDSDM Redundancy",
                                        "Description": "IDSDM Redundancy"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 3,
                                        "Name": "Link Status",
                                        "Description": "Link Status"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 19,
                                        "Name": "Log Event",
                                        "Description": "Log Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 15,
                                        "Name": "Management Module",
                                        "Description": "Management Module"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 80,
                                        "Name": "Memory",
                                        "Description": "Memory"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 118,
                                        "Name": "Metrics",
                                        "Description": "Metrics"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 102,
                                        "Name": "NIC Configuration",
                                        "Description": "NIC Configuration"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 77,
                                        "Name": "Node",
                                        "Description": "Node"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 96,
                                        "Name": "OS Event",
                                        "Description": "OS Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 81,
                                        "Name": "PCI Device",
                                        "Description": "PCI Device"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 94,
                                        "Name": "Physical Disk",
                                        "Description": "Physical Disk"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 151,
                                        "Name": "Power Configuration",
                                        "Description": "Power Configuration"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 78,
                                        "Name": "Power Supply",
                                        "Description": "Power Supply"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 23,
                                        "Name": "Power Usage",
                                        "Description": "Power Usage"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 61,
                                        "Name": "Processor",
                                        "Description": "Processor"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 68,
                                        "Name": "Processor Absent",
                                        "Description": "Processor Absent"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 103,
                                        "Name": "PSU Absent",
                                        "Description": "PSU Absent"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 109,
                                        "Name": "RAC Event",
                                        "Description": "RAC Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 44,
                                        "Name": "Redundancy",
                                        "Description": "Redundancy"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 63,
                                        "Name": "SAS IOM",
                                        "Description": "SAS IOM"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 25,
                                        "Name": "Security Event",
                                        "Description": "Security Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 39,
                                        "Name": "Software Config",
                                        "Description": "Software Config"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 92,
                                        "Name": "Support Assist",
                                        "Description": "Support Assist"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 29,
                                        "Name": "System Event Log",
                                        "Description": "System Event Log"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 71,
                                        "Name": "System Info",
                                        "Description": "System Info"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 13,
                                        "Name": "System Performance Event",
                                        "Description": "System Performance Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 110,
                                        "Name": "Temperature",
                                        "Description": "Temperature"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 16,
                                        "Name": "Temperature Statistics",
                                        "Description": "Temperature Statistics"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 55,
                                        "Name": "UEFI Event",
                                        "Description": "UEFI Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 56,
                                        "Name": "User Tracking",
                                        "Description": "User Tracking"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 5,
                                        "Name": "vFlash Absent",
                                        "Description": "vFlash Absent"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 66,
                                        "Name": "vFlash Event",
                                        "Description": "vFlash Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 74,
                                        "Name": "vFlash Media",
                                        "Description": "vFlash Media"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 40,
                                        "Name": "Voltage",
                                        "Description": "Voltage"
                                    }
                                ]
                            },
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 3,
                                "Name": "Updates",
                                "CatalogName": "Internal Events Catalog",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 106,
                                        "Name": "Fan Event",
                                        "Description": "Fan Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 51,
                                        "Name": "Firmware Download",
                                        "Description": "Firmware Download"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 24,
                                        "Name": "Firmware Update Job",
                                        "Description": "Firmware Update Job"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 27,
                                        "Name": "Job Control",
                                        "Description": "Job Control"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 57,
                                        "Name": "Lifecycle Controller",
                                        "Description": "Lifecycle Controller"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 109,
                                        "Name": "RAC Event",
                                        "Description": "RAC Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 52,
                                        "Name": "Software Change",
                                        "Description": "Software Change"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 39,
                                        "Name": "Software Config",
                                        "Description": "Software Config"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 71,
                                        "Name": "System Info",
                                        "Description": "System Info"
                                    }
                                ]
                            },
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 6,
                                "Name": "Work Notes",
                                "CatalogName": "Internal Events Catalog",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 56,
                                        "Name": "User Tracking",
                                        "Description": "User Tracking"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "@odata.type": "#AlertService.AlertCategories",
                        "@odata.id": "/api/AlertService/AlertCategories('Networking')",
                        "Name": "Networking",
                        "IsBuiltIn": True,
                        "CategoriesDetails": [
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 1,
                                "Name": "System Health",
                                "CatalogName": "Networking",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 7700,
                                        "Name": "Other",
                                        "Description": "Other"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "@odata.type": "#AlertService.AlertCategories",
                        "@odata.id": "/api/AlertService/AlertCategories('OMSA')",
                        "Name": "OMSA",
                        "IsBuiltIn": True,
                        "CategoriesDetails": [
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 4,
                                "Name": "Audit",
                                "CatalogName": "OMSA",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 19,
                                        "Name": "Log Event",
                                        "Description": "Log Event"
                                    }
                                ]
                            },
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 5,
                                "Name": "Configuration",
                                "CatalogName": "OMSA",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 41,
                                        "Name": "Auto System Reset",
                                        "Description": "Auto System Reset"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 61,
                                        "Name": "Processor",
                                        "Description": "Processor"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 25,
                                        "Name": "Security Event",
                                        "Description": "Security Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 71,
                                        "Name": "System Info",
                                        "Description": "System Info"
                                    }
                                ]
                            },
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 1,
                                "Name": "System Health",
                                "CatalogName": "OMSA",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 67,
                                        "Name": "Amperage",
                                        "Description": "Amperage"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 41,
                                        "Name": "Auto System Reset",
                                        "Description": "Auto System Reset"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 108,
                                        "Name": "Battery Event",
                                        "Description": "Battery Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 89,
                                        "Name": "Cable",
                                        "Description": "Cable"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 11,
                                        "Name": "Hardware Config",
                                        "Description": "Hardware Config"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 80,
                                        "Name": "Memory",
                                        "Description": "Memory"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 7700,
                                        "Name": "Other",
                                        "Description": "Other"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 78,
                                        "Name": "Power Supply",
                                        "Description": "Power Supply"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 23,
                                        "Name": "Power Usage",
                                        "Description": "Power Usage"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 61,
                                        "Name": "Processor",
                                        "Description": "Processor"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 44,
                                        "Name": "Redundancy",
                                        "Description": "Redundancy"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 25,
                                        "Name": "Security Event",
                                        "Description": "Security Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 29,
                                        "Name": "System Event Log",
                                        "Description": "System Event Log"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 71,
                                        "Name": "System Info",
                                        "Description": "System Info"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 110,
                                        "Name": "Temperature",
                                        "Description": "Temperature"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 66,
                                        "Name": "vFlash Event",
                                        "Description": "vFlash Event"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 40,
                                        "Name": "Voltage",
                                        "Description": "Voltage"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "@odata.type": "#AlertService.AlertCategories",
                        "@odata.id": "/api/AlertService/AlertCategories('OpenManage%20Enterprise')",
                        "Name": "OpenManage Enterprise",
                        "IsBuiltIn": True,
                        "CategoriesDetails": [
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 1,
                                "Name": "System Health",
                                "CatalogName": "OpenManage Enterprise",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 7400,
                                        "Name": "Health Status of Managed device",
                                        "Description": "Health Status of Managed device"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 118,
                                        "Name": "Metrics",
                                        "Description": "Metrics"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 71,
                                        "Name": "System Info",
                                        "Description": "System Info"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "@odata.type": "#AlertService.AlertCategories",
                        "@odata.id": "/api/AlertService/AlertCategories('OpenManage%20Essentials')",
                        "Name": "OpenManage Essentials",
                        "IsBuiltIn": True,
                        "CategoriesDetails": [
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 1,
                                "Name": "System Health",
                                "CatalogName": "OpenManage Essentials",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 7400,
                                        "Name": "Health Status of Managed device",
                                        "Description": "Health Status of Managed device"
                                    },
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 7700,
                                        "Name": "Other",
                                        "Description": "Other"
                                    }
                                ]
                            },
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 6,
                                "Name": "Work Notes",
                                "CatalogName": "OpenManage Essentials",
                                "SubCategoryDetails": []
                            }
                        ]
                    },
                    {
                        "@odata.type": "#AlertService.AlertCategories",
                        "@odata.id": "/api/AlertService/AlertCategories('Power%20Manager')",
                        "Name": "Power Manager",
                        "IsBuiltIn": True,
                        "CategoriesDetails": [
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 1,
                                "Name": "System Health",
                                "CatalogName": "Power Manager",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 151,
                                        "Name": "Power Configuration",
                                        "Description": "Power Configuration"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "@odata.type": "#AlertService.AlertCategories",
                        "@odata.id": "/api/AlertService/AlertCategories('RFC1215')",
                        "Name": "RFC1215",
                        "IsBuiltIn": True,
                        "CategoriesDetails": [
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 1,
                                "Name": "System Health",
                                "CatalogName": "RFC1215",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 7700,
                                        "Name": "Other",
                                        "Description": "Other"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "@odata.type": "#AlertService.AlertCategories",
                        "@odata.id": "/api/AlertService/AlertCategories('SNMPv2-MIB')",
                        "Name": "SNMPv2-MIB",
                        "IsBuiltIn": True,
                        "CategoriesDetails": [
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 1,
                                "Name": "System Health",
                                "CatalogName": "SNMPv2-MIB",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 7700,
                                        "Name": "Other",
                                        "Description": "Other"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "@odata.type": "#AlertService.AlertCategories",
                        "@odata.id": "/api/AlertService/AlertCategories('VMWare')",
                        "Name": "VMWare",
                        "IsBuiltIn": True,
                        "CategoriesDetails": [
                            {
                                "@odata.type": "#AlertService.AlertCategory",
                                "Id": 1,
                                "Name": "System Health",
                                "CatalogName": "VMWare",
                                "SubCategoryDetails": [
                                    {
                                        "@odata.type": "#AlertService.AlertSubCategory",
                                        "Id": 7700,
                                        "Name": "Other",
                                        "Description": "Other"
                                    }
                                ]
                            }
                        ]
                    }
                ]}}])
    def test_ome_alert_policies_category_info(self, params, ome_connection_mock_for_alert_category, ome_response_mock,
                                              ome_default_args, module_mock, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['json_data']
        result = self._run_module(
            ome_default_args, check_mode=params.get('check_mode', False))
        assert isinstance(result['categories'], list)
        assert result['msg'] == params['message']
        for ctr in result['categories']:
            assert 'CategoriesDetails' in ctr
            for k in ctr.keys():
                assert '@odata.' not in k

    @pytest.mark.parametrize("exc_type",
                             [SSLValidationError, ConnectionError, TypeError, ValueError, OSError, HTTPError, URLError])
    def test_ome_alert_policies_category_info_main_exception_failure_case(self, exc_type, mocker, ome_default_args,
                                                                          ome_connection_mock_for_alert_category,
                                                                          ome_response_mock):
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type == HTTPError:
            mocker.patch(MODULE_PATH + 'get_all_data_with_pagination', side_effect=exc_type(
                'https://testhost.com', 401, 'http error message', {
                    "accept-type": "application/json"},
                StringIO(json_str)))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
        elif exc_type == URLError:
            mocker.patch(MODULE_PATH + 'get_all_data_with_pagination',
                         side_effect=exc_type("exception message"))
            # ome_connection_mock_for_alert_category.get_all_data_with_pagination.side_effect = exc_type("exception message")
            result = self._run_module(ome_default_args)
            assert result['unreachable'] is True
        else:
            mocker.patch(MODULE_PATH + 'get_all_data_with_pagination',
                         side_effect=exc_type("exception message"))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
