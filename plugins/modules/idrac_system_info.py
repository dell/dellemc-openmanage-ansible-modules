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
module: idrac_system_info
short_description: Get the PowerEdge Server System Inventory
version_added: "3.0.0"
description:
    - Get the PowerEdge Server System Inventory.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options

requirements:
    - "omsdk >= 1.2.488"
    - "python >= 3.9.6"
author: "Rajeev Arakkal (@rajeevarakkal)"
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports both IPv4 and IPv6 address for I(idrac_ip).
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Get System Inventory
  dellemc.openmanage.idrac_system_info:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
"""

RETURN = r'''
---
msg:
  description: "Overall system inventory information status."
  returned: always
  type: str
  sample: "Successfully fetched the system inventory details."
system_info:
  type: dict
  description: Details of the PowerEdge Server System Inventory.
  returned: success
  sample: {
            "BIOS": [
                {
                    "BIOSReleaseDate": "11/26/2019",
                    "FQDD": "BIOS.Setup.1-1",
                    "InstanceID": "DCIM:INSTALLED#741__BIOS.Setup.1-1",
                    "Key": "DCIM:INSTALLED#741__BIOS.Setup.1-1",
                    "SMBIOSPresent": "True",
                    "VersionString": "2.4.8"
                }
            ]
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
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


# Main
def main():
    specs = {}
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        supports_check_mode=True)
    try:
        with iDRACConnection(module.params) as idrac:
            idrac.get_entityjson()
            msg = idrac.get_json_device()
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, SSLValidationError, IOError, ValueError, TypeError, ConnectionError) as e:
        module.fail_json(msg=str(e))

    module.exit_json(msg="Successfully fetched the system inventory details.",
                     system_info=msg)


if __name__ == '__main__':
    main()
