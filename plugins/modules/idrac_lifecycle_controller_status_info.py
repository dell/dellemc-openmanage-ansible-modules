#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.0.0
# Copyright (C) 2018-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_lifecycle_controller_status_info
short_description: Get the status of the Lifecycle Controller
version_added: "2.1.0"
description:
    - This module shows the status of the Lifecycle Controller on a Dell EMC PowerEdge server.
extends_documentation_fragment:
    - dellemc.openmanage.idrac_auth_options

requirements:
    - "omsdk"
    - "python >= 2.7.5"
author:
    - "Rajeev Arakkal (@rajeevarakkal)"
    - "Anooja Vardhineni (@anooja-vardhineni)"
notes:
    - Run this module from a system that has direct access to DellEMC iDRAC.
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Show status of the Lifecycle Controller
  dellemc.openmanage.idrac_lifecycle_controller_status_info:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
"""

RETURN = r'''
---
msg:
  description: Overall status of fetching lifecycle controller status.
  returned: always
  type: str
  sample: "Successfully fetched the lifecycle controller status."
lc_status_info:
  description: Displays the status of the Lifecycle Controller on a Dell EMC PowerEdge server.
  returned: success
  type: dict
  sample: {
      "msg": {
        "LCReady": true,
        "LCStatus": "Ready"
      }
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


from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.module_utils.basic import AnsibleModule
import json


def main():
    module = AnsibleModule(
        argument_spec={
            "idrac_ip": {"required": True, "type": 'str'},
            "idrac_user": {"required": True, "type": 'str'},
            "idrac_password": {"required": True, "type": 'str', "aliases": ['idrac_pwd'], "no_log": True},
            "idrac_port": {"required": False, "default": 443, "type": 'int'},
        },
        supports_check_mode=True)

    try:
        with iDRACConnection(module.params) as idrac:
            lcready = idrac.config_mgr.LCReady
            lcstatus = idrac.config_mgr.LCStatus
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError) as e:
        module.fail_json(msg=str(e))
    module.exit_json(msg="Successfully fetched the lifecycle controller status.",
                     lc_status_info={'LCReady': lcready, 'LCStatus': lcstatus})


if __name__ == '__main__':
    main()
