#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.2.0
# Copyright (C) 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_alert_policies_category_info
short_description: Retrieves information of all OME alert policy categories.
version_added: "8.2.0"
description: This module allows to retrieve all the OME alert policy categories.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
requirements:
    - "python >= 3.9.6"
author:
    - "Jagadeesh N V(@jagadeeshnv)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
    - This module supports both IPv4 and IPv6 address.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Retrieve information about all the OME alert policies
  dellemc.openmanage.ome_alert_policies_category_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
'''

RETURN = r'''
---
categories:
  type: list
  description: Information about the alert categories.
  returned: always
  sample: [{
        "CategoriesDetails": [
            {
                "CatalogName": "Application",
                "Id": 4,
                "Name": "Audit",
                "SubCategoryDetails": [
                    {
                        "Description": "Devices",
                        "Id": 90,
                        "Name": "Devices"
                    },
                    {
                        "Description": "Generic",
                        "Id": 10,
                        "Name": "Generic"
                    },
                    {
                        "Description": "Power Configuration",
                        "Id": 151,
                        "Name": "Power Configuration"
                    },
                    {
                        "Description": "Users",
                        "Id": 35,
                        "Name": "Users"
                    }
                ]
            },
            {
                "CatalogName": "Application",
                "Id": 5,
                "Name": "Configuration",
                "SubCategoryDetails": [
                    {
                        "Description": "Application",
                        "Id": 85,
                        "Name": "Application"
                    },
                    {
                        "Description": "Users",
                        "Id": 35,
                        "Name": "Users"
                    }
                ]
            },
            {
                "CatalogName": "Application",
                "Id": 7,
                "Name": "Miscellaneous",
                "SubCategoryDetails": [
                    {
                        "Description": "Miscellaneous",
                        "Id": 20,
                        "Name": "Miscellaneous"
                    }
                ]
            },
            {
                "CatalogName": "Application",
                "Id": 2,
                "Name": "Storage",
                "SubCategoryDetails": [
                    {
                        "Description": "Devices",
                        "Id": 90,
                        "Name": "Devices"
                    }
                ]
            },
            {
                "CatalogName": "Application",
                "Id": 1,
                "Name": "System Health",
                "SubCategoryDetails": [
                    {
                        "Description": "Devices",
                        "Id": 90,
                        "Name": "Devices"
                    },
                    {
                        "Description": "Health Status of Managed device",
                        "Id": 7400,
                        "Name": "Health Status of Managed device"
                    },
                    {
                        "Description": "Job",
                        "Id": 47,
                        "Name": "Job"
                    },
                    {
                        "Description": "Metrics",
                        "Id": 118,
                        "Name": "Metrics"
                    },
                    {
                        "Description": "Power Configuration",
                        "Id": 151,
                        "Name": "Power Configuration"
                    }
                ]
            },
            {
                "CatalogName": "Application",
                "Id": 3,
                "Name": "Updates",
                "SubCategoryDetails": [
                    {
                        "Description": "Application",
                        "Id": 85,
                        "Name": "Application"
                    },
                    {
                        "Description": "Firmware",
                        "Id": 112,
                        "Name": "Firmware"
                    }
                ]
            }
        ],
        "IsBuiltIn": true,
        "Name": "Application"
    },
    {
        "CategoriesDetails": [
            {
                "CatalogName": "Dell Storage",
                "Id": 2,
                "Name": "Storage",
                "SubCategoryDetails": [
                    {
                        "Description": "Other",
                        "Id": 7700,
                        "Name": "Other"
                    }
                ]
            },
            {
                "CatalogName": "Dell Storage",
                "Id": 1,
                "Name": "System Health",
                "SubCategoryDetails": [
                    {
                        "Description": "Other",
                        "Id": 7700,
                        "Name": "Other"
                    },
                    {
                        "Description": "Storage",
                        "Id": 18,
                        "Name": "Storage"
                    }
                ]
            }
        ],
        "IsBuiltIn": true,
        "Name": "Dell Storage"
    },
    {
        "CategoriesDetails": [
            {
                "CatalogName": "iDRAC",
                "Id": 4,
                "Name": "Audit",
                "SubCategoryDetails": [
                    {
                        "Description": "Auto System Reset",
                        "Id": 41,
                        "Name": "Auto System Reset"
                    },
                    {
                        "Description": "BIOS Management",
                        "Id": 54,
                        "Name": "BIOS Management"
                    },
                    {
                        "Description": "BIOS POST",
                        "Id": 75,
                        "Name": "BIOS POST"
                    },
                    {
                        "Description": "System Info",
                        "Id": 71,
                        "Name": "System Info"
                    },
                    {
                        "Description": "UEFI Event",
                        "Id": 55,
                        "Name": "UEFI Event"
                    },
                    {
                        "Description": "User Tracking",
                        "Id": 56,
                        "Name": "User Tracking"
                    }
                ]
            },
            {
                "CatalogName": "iDRAC",
                "Id": 5,
                "Name": "Configuration",
                "SubCategoryDetails": [
                    {
                        "Description": "Auto-Discovery",
                        "Id": 49,
                        "Name": "Auto-Discovery"
                    },
                    {
                        "Description": "vFlash Event",
                        "Id": 66,
                        "Name": "vFlash Event"
                    },
                    {
                        "Description": "Virtual Console",
                        "Id": 7,
                        "Name": "Virtual Console"
                    }
                ]
            },
            {
                "CatalogName": "iDRAC",
                "Id": 2,
                "Name": "Storage",
                "SubCategoryDetails": [
                    {
                        "Description": "Battery Event",
                        "Id": 108,
                        "Name": "Battery Event"
                    },
                    {
                        "Description": "Virtual Disk",
                        "Id": 46,
                        "Name": "Virtual Disk"
                    }
                ]
            },
            {
                "CatalogName": "iDRAC",
                "Id": 1,
                "Name": "System Health",
                "SubCategoryDetails": [
                    {
                        "Description": "Amperage",
                        "Id": 67,
                        "Name": "Amperage"
                    },
                    {
                        "Description": "Auto System Reset",
                        "Id": 41,
                        "Name": "Auto System Reset"
                    },
                    {
                        "Description": "Voltage",
                        "Id": 40,
                        "Name": "Voltage"
                    }
                ]
            },
            {
                "CatalogName": "iDRAC",
                "Id": 3,
                "Name": "Updates",
                "SubCategoryDetails": [
                    {
                        "Description": "Firmware Download",
                        "Id": 51,
                        "Name": "Firmware Download"
                    },
                    {
                        "Description": "Firmware Update Job",
                        "Id": 24,
                        "Name": "Firmware Update Job"
                    },
                    {
                        "Description": "Group Manager",
                        "Id": 53,
                        "Name": "Group Manager"
                    },
                    {
                        "Description": "Job Control",
                        "Id": 27,
                        "Name": "Job Control"
                    },
                    {
                        "Description": "RAC Event",
                        "Id": 109,
                        "Name": "RAC Event"
                    },
                    {
                        "Description": "Software Change",
                        "Id": 52,
                        "Name": "Software Change"
                    },
                    {
                        "Description": "System Info",
                        "Id": 71,
                        "Name": "System Info"
                    },
                    {
                        "Description": "UEFI Event",
                        "Id": 55,
                        "Name": "UEFI Event"
                    }
                ]
            },
            {
                "CatalogName": "iDRAC",
                "Id": 6,
                "Name": "Work Notes",
                "SubCategoryDetails": [
                    {
                        "Description": "BIOS Management",
                        "Id": 54,
                        "Name": "BIOS Management"
                    }
                ]
            }
        ],
        "IsBuiltIn": true,
        "Name": "iDRAC"
    },
    {
        "CategoriesDetails": [
            {
                "CatalogName": "IF-MIB",
                "Id": 4,
                "Name": "Audit",
                "SubCategoryDetails": [
                    {
                        "Description": "Interface",
                        "Id": 101,
                        "Name": "Interface"
                    }
                ]
            }
        ],
        "IsBuiltIn": true,
        "Name": "IF-MIB"
    },
    {
        "CategoriesDetails": [
            {
                "CatalogName": "Internal Events Catalog",
                "Id": 4,
                "Name": "Audit",
                "SubCategoryDetails": [
                    {
                        "Description": "BIOS Management",
                        "Id": 54,
                        "Name": "BIOS Management"
                    },
                    {
                        "Description": "Debug",
                        "Id": 12,
                        "Name": "Debug"
                    },
                    {
                        "Description": "Support Assist",
                        "Id": 92,
                        "Name": "Support Assist"
                    },
                    {
                        "Description": "System Info",
                        "Id": 71,
                        "Name": "System Info"
                    },
                    {
                        "Description": "Temperature",
                        "Id": 110,
                        "Name": "Temperature"
                    },
                    {
                        "Description": "User Tracking",
                        "Id": 56,
                        "Name": "User Tracking"
                    },
                    {
                        "Description": "Users",
                        "Id": 35,
                        "Name": "Users"
                    },
                    {
                        "Description": "Virtual Media",
                        "Id": 50,
                        "Name": "Virtual Media"
                    }
                ]
            },
            {
                "CatalogName": "Internal Events Catalog",
                "Id": 5,
                "Name": "Configuration",
                "SubCategoryDetails": [
                    {
                        "Description": "Auto-Discovery",
                        "Id": 49,
                        "Name": "Auto-Discovery"
                    },
                    {
                        "Description": "Backup/Restore",
                        "Id": 107,
                        "Name": "Backup/Restore"
                    },
                    {
                        "Description": "UEFI Event",
                        "Id": 55,
                        "Name": "UEFI Event"
                    },
                    {
                        "Description": "Uplink",
                        "Id": 33,
                        "Name": "Uplink"
                    },
                    {
                        "Description": "User Tracking",
                        "Id": 56,
                        "Name": "User Tracking"
                    },
                    {
                        "Description": "Users",
                        "Id": 35,
                        "Name": "Users"
                    },
                    {
                        "Description": "vFlash Event",
                        "Id": 66,
                        "Name": "vFlash Event"
                    },
                    {
                        "Description": "vFlash Media",
                        "Id": 74,
                        "Name": "vFlash Media"
                    }
                ]
            },
            {
                "CatalogName": "Internal Events Catalog",
                "Id": 7,
                "Name": "Miscellaneous",
                "SubCategoryDetails": [
                    {
                        "Description": "Application",
                        "Id": 85,
                        "Name": "Application"
                    }
                ]
            },
            {
                "CatalogName": "Internal Events Catalog",
                "Id": 2,
                "Name": "Storage",
                "SubCategoryDetails": [
                    {
                        "Description": "Battery Event",
                        "Id": 108,
                        "Name": "Battery Event"
                    },
                    {
                        "Description": "Virtual Disk",
                        "Id": 46,
                        "Name": "Virtual Disk"
                    }
                ]
            },
            {
                "CatalogName": "Internal Events Catalog",
                "Id": 1,
                "Name": "System Health",
                "SubCategoryDetails": [
                    {
                        "Description": "Amperage",
                        "Id": 67,
                        "Name": "Amperage"
                    },
                    {
                        "Description": "Auto System Reset",
                        "Id": 41,
                        "Name": "Auto System Reset"
                    },
                    {
                        "Description": "System Info",
                        "Id": 71,
                        "Name": "System Info"
                    }
                ]
            },
            {
                "CatalogName": "Internal Events Catalog",
                "Id": 6,
                "Name": "Work Notes",
                "SubCategoryDetails": [
                    {
                        "Description": "User Tracking",
                        "Id": 56,
                        "Name": "User Tracking"
                    }
                ]
            }
        ],
        "IsBuiltIn": true,
        "Name": "Internal Events Catalog"
    },
    {
        "CategoriesDetails": [
            {
                "CatalogName": "Networking",
                "Id": 1,
                "Name": "System Health",
                "SubCategoryDetails": [
                    {
                        "Description": "Other",
                        "Id": 7700,
                        "Name": "Other"
                    }
                ]
            }
        ],
        "IsBuiltIn": true,
        "Name": "Networking"
    },
    {
        "CategoriesDetails": [
            {
                "CatalogName": "OMSA",
                "Id": 4,
                "Name": "Audit",
                "SubCategoryDetails": [
                    {
                        "Description": "Log Event",
                        "Id": 19,
                        "Name": "Log Event"
                    }
                ]
            },
            {
                "CatalogName": "OMSA",
                "Id": 5,
                "Name": "Configuration",
                "SubCategoryDetails": [
                    {
                        "Description": "Auto System Reset",
                        "Id": 41,
                        "Name": "Auto System Reset"
                    },
                    {
                        "Description": "Processor",
                        "Id": 61,
                        "Name": "Processor"
                    },
                    {
                        "Description": "Security Event",
                        "Id": 25,
                        "Name": "Security Event"
                    },
                    {
                        "Description": "System Info",
                        "Id": 71,
                        "Name": "System Info"
                    }
                ]
            },
            {
                "CatalogName": "OMSA",
                "Id": 1,
                "Name": "System Health",
                "SubCategoryDetails": [
                    {
                        "Description": "Amperage",
                        "Id": 67,
                        "Name": "Amperage"
                    },
                    {
                        "Description": "Voltage",
                        "Id": 40,
                        "Name": "Voltage"
                    }
                ]
            }
        ],
        "IsBuiltIn": true,
        "Name": "OMSA"
    },
    {
        "CategoriesDetails": [
            {
                "CatalogName": "OpenManage Enterprise",
                "Id": 1,
                "Name": "System Health",
                "SubCategoryDetails": [
                    {
                        "Description": "Health Status of Managed device",
                        "Id": 7400,
                        "Name": "Health Status of Managed device"
                    },
                    {
                        "Description": "Metrics",
                        "Id": 118,
                        "Name": "Metrics"
                    },
                    {
                        "Description": "System Info",
                        "Id": 71,
                        "Name": "System Info"
                    }
                ]
            }
        ],
        "IsBuiltIn": true,
        "Name": "OpenManage Enterprise"
    },
    {
        "CategoriesDetails": [
            {
                "CatalogName": "OpenManage Essentials",
                "Id": 1,
                "Name": "System Health",
                "SubCategoryDetails": [
                    {
                        "Description": "Health Status of Managed device",
                        "Id": 7400,
                        "Name": "Health Status of Managed device"
                    },
                    {
                        "Description": "Other",
                        "Id": 7700,
                        "Name": "Other"
                    }
                ]
            },
            {
                "CatalogName": "OpenManage Essentials",
                "Id": 6,
                "Name": "Work Notes",
                "SubCategoryDetails": []
            }
        ],
        "IsBuiltIn": true,
        "Name": "OpenManage Essentials"
    },
    {
        "CategoriesDetails": [
            {
                "CatalogName": "Power Manager",
                "Id": 1,
                "Name": "System Health",
                "SubCategoryDetails": [
                    {
                        "Description": "Power Configuration",
                        "Id": 151,
                        "Name": "Power Configuration"
                    }
                ]
            }
        ],
        "IsBuiltIn": true,
        "Name": "Power Manager"
    },
    {
        "CategoriesDetails": [
            {
                "CatalogName": "RFC1215",
                "Id": 1,
                "Name": "System Health",
                "SubCategoryDetails": [
                    {
                        "Description": "Other",
                        "Id": 7700,
                        "Name": "Other"
                    }
                ]
            }
        ],
        "IsBuiltIn": true,
        "Name": "RFC1215"
    },
    {
        "CategoriesDetails": [
            {
                "CatalogName": "SNMPv2-MIB",
                "Id": 1,
                "Name": "System Health",
                "SubCategoryDetails": [
                    {
                        "Description": "Other",
                        "Id": 7700,
                        "Name": "Other"
                    }
                ]
            }
        ],
        "IsBuiltIn": true,
        "Name": "SNMPv2-MIB"
    },
    {
        "CategoriesDetails": [
            {
                "CatalogName": "VMWare",
                "Id": 1,
                "Name": "System Health",
                "SubCategoryDetails": [
                    {
                        "Description": "Other",
                        "Id": 7700,
                        "Name": "Other"
                    }
                ]
            }
        ],
        "IsBuiltIn": true,
        "Name": "VMWare"
    }
]
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
        "code": "Base.1.0.GeneralError",
        "message": "A general error has occurred. See ExtendedInfo for more information.",
        "@Message.ExtendedInfo": [
            {
                "MessageId": "CGEN1006",
                "RelatedProperties": [],
                "Message": "Unable to complete the request because the resource URI does not exist or is not implemented.",
                "MessageArgs": [],
                "Severity": "Critical",
                "Resolution": "Check the request resource URI. Refer to the OpenManage Enterprise-Modular User's Guide
                for more information about resource URI and its properties."
            }
        ]
    }
  }
'''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import remove_key

ALERT_CATEGORY_URI = "AlertService/AlertCategories"


def get_formatted_categories(rest_obj): 
    resp = rest_obj.invoke_request("GET", ALERT_CATEGORY_URI)
    categories = remove_key(resp.json_data.get("value", []))
    return categories


def main():
    specs = {}
    specs.update(ome_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        supports_check_mode=True)
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            categories = get_formatted_categories(rest_obj)
            module.exit_json(categories=categories)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == "__main__":
    main()
