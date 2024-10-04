#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.1.0
# Copyright (C) 2021-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_firmware_info
short_description: Get Firmware Inventory
version_added: "3.0.0"
description: Get Firmware Inventory.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options

requirements:
    - "omsdk >= 1.2.488"
    - "python >= 3.9.6"
author: 
  - "Rajeev Arakkal (@rajeevarakkal)"
  - "Saksham Nautiyal (@Saksham-Nautiyal)"
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports both IPv4 and IPv6 address for I(idrac_ip).
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Get Installed Firmware Inventory
  dellemc.openmanage.idrac_firmware_info:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
"""

RETURN = r'''
---
msg:
  description: "Fetching the firmware inventory details."
  returned: always
  type: str
  sample: "Successfully fetched the firmware inventory details."
firmware_info:
  type: dict
  description: Details of the firmware.
  returned: success
  sample: {
            "Firmware": [{
                "BuildNumber": "0",
                "Classifications": "10",
                "ComponentID": "102573",
                "ComponentType": "FRMW",
                "DeviceID": null,
                "ElementName": "Power Supply.Slot.1",
                "FQDD": "PSU.Slot.1",
                "HashValue": null,
                "IdentityInfoType": "OrgID:ComponentType:ComponentID",
                "IdentityInfoValue": "DCIM:firmware:102573",
                "InstallationDate": "2018-11-22T03:58:23Z",
                "InstanceID": "DCIM:INSTALLED#0x15__PSU.Slot.1",
                "IsEntity": "true",
                "Key": "DCIM:INSTALLED#0x15__PSU.Slot.1",
                "MajorVersion": "0",
                "MinorVersion": "3",
                "RevisionNumber": "67",
                "RevisionString": null,
                "Status": "Installed",
                "SubDeviceID": null,
                "SubVendorID": null,
                "Updateable": "true",
                "VendorID": null,
                "VersionString": "00.3D.67",
                "impactsTPMmeasurements": "false"
            }]
  }
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
          "MessageId": "GEN1234",
          "RelatedProperties": [],
          "Message": "Unable to process the request because an error occurred.",
          "MessageArgs": [],
          "Severity": "Critical",
          "Resolution": "Retry the operation. If the issue persists, contact your system administrator."
        }
      ]
    }
  }
'''


import json
from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection, idrac_auth_params
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import remove_key
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from urllib.error import URLError, HTTPError

GET_IDRAC_FIRMWARE_DETAILS_URI= "/redfish/v1/UpdateService/Oem/Dell/DellSoftwareInventory?$select=Members"
GET_IDRAC_FIRMWARE_URI= "/redfish/v1/UpdateService/Oem/Dell/DellSoftwareInventory"

def get_idrac_firmware_info(idrac, module):
    try:
        response = idrac.invoke_request(method='GET',uri=GET_IDRAC_FIRMWARE_URI)

        if response.status_code == 200:
            details_response = idrac.invoke_request(method='GET', uri=GET_IDRAC_FIRMWARE_DETAILS_URI)
            
            if details_response and details_response.status_code == 200 and details_response.json_data:
                filtered_data = remove_key(details_response.json_data)
                return filtered_data
    except:
        with iDRACConnection(module.params) as idrac:
            firmware_details = idrac.update_mgr.InstalledFirmware
            return firmware_details

def main():
    specs = {}
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        supports_check_mode=True
    )

    try:
        with iDRACRedfishAPI(module.params) as idrac:
            firmware_info = get_idrac_firmware_info(idrac, module)
    except HTTPError as err:
        module.fail_json(msg="HTTP error occurred", error_info=str(err))
    except URLError as err:
        module.fail_json(msg="Network error occurred", unreachable=True, error_info=str(err))
    except (RuntimeError, SSLValidationError, IOError, ValueError, TypeError, ConnectionError) as e:
        module.fail_json(msg="An error occurred", error_info=str(e))

    module.exit_json(
        msg="Successfully fetched the firmware inventory details.",
        firmware_info = firmware_info
    )


if __name__ == '__main__':
    main()