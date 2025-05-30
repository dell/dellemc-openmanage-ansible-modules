#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2023-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_alert_policies_category_info
short_description: Retrieves information of all OME alert policy categories.
version_added: "8.2.0"
description: This module allows to retrieve all the alert policy categories for OpenManage Enterprise and OpenManage Enterprise Modular.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
requirements:
    - "python >= 3.9.6"
author:
    - "Jagadeesh N V(@jagadeeshnv)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise or OpenManage Enterprise Modular.
    - This module supports IPv4 and IPv6 addresses.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Retrieve information about all the OME alert policy categories
  dellemc.openmanage.ome_alert_policies_category_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
'''

RETURN = r'''
---
msg:
  type: str
  description: Status of the alert policies category fetch operation.
  returned: always
  sample: "Successfully retrieved alert policies category information."
categories:
  type: list
  description: Information about the alert categories.
  returned: always
  sample: [{
        "CategoriesDetails": [
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
                "MessageId": "CGEN1234",
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
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import remove_key
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import get_all_data_with_pagination

ALERT_CATEGORY_URI = "AlertService/AlertCategories"
SUCCESS_MSG = "Successfully retrieved alert policies category information."


def get_formatted_categories(rest_obj):
    report = get_all_data_with_pagination(rest_obj, ALERT_CATEGORY_URI)
    categories = remove_key(report.get("report_list", []))
    return categories


def main():
    specs = {}
    module = OmeAnsibleModule(
        argument_spec=specs,
        supports_check_mode=True)
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            categories = get_formatted_categories(rest_obj)
            module.exit_json(msg=SUCCESS_MSG, categories=categories)
    except HTTPError as err:
        module.exit_json(failed=True, msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(failed=True, msg=str(err))


if __name__ == "__main__":
    main()
