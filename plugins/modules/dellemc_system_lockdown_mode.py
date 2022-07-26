#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 6.0.0
# Copyright (C) 2018-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
---
module: dellemc_system_lockdown_mode
short_description: Configures system lockdown mode for iDRAC
version_added: "1.0.0"
deprecated:
  removed_at_date: "2024-07-31"
  why: Replaced with M(dellemc.openmanage.idrac_attributes).
  alternative: Use M(dellemc.openmanage.idrac_attributes) instead.
  removed_from_collection: dellemc.openmanage
description:
    - This module is allows to Enable or Disable System lockdown Mode.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
    share_name:
        type: str
        description:
          - (deprecated)Network share or a local path.
          - This option is deprecated and will be removed in the later version.
    share_user:
        type: str
        description:
          - (deprecated)Network share user in the format 'user@domain' or 'domain\\user' if user is
            part of a domain else 'user'. This option is mandatory for CIFS Network Share.
          - This option is deprecated and will be removed in the later version.
    share_password:
        type: str
        description:
          - (deprecated)Network share user password. This option is mandatory for CIFS Network Share.
          - This option is deprecated and will be removed in the later version.
        aliases: ['share_pwd']
    share_mnt:
        type: str
        description:
          - (deprecated)Local mount path of the network share with read-write permission for ansible user.
            This option is mandatory for Network Share.
          - This option is deprecated and will be removed in the later version.
    lockdown_mode:
        required:  True
        type: str
        description: Whether to Enable or Disable system lockdown mode.
        choices: [Enabled, Disabled]
requirements:
    - "omsdk >= 1.2.488"
    - "python >= 3.8.6"
author: "Felix Stephen (@felixs88)"
notes:
    - This module requires 'Administrator' privilege for I(idrac_user).
    - Run this module from a system that has direct access to Dell EMC iDRAC.
    - This module does not support C(check_mode).
"""

EXAMPLES = """
---
- name: Check System  Lockdown Mode
  dellemc.openmanage.dellemc_system_lockdown_mode:
       idrac_ip:   "192.168.0.1"
       idrac_user: "user_name"
       idrac_password:  "user_password"
       ca_path: "/path/to/ca_cert.pem"
       lockdown_mode: "Disabled"
"""

RETURN = r'''
---
msg:
    description: "Lockdown mode of the system is configured."
    returned: always
    type: str
    sample: "Successfully completed the lockdown mode operations."
system_lockdown_status:
  type: dict
  description: Storage configuration job and progress details from the iDRAC.
  returned: success
  sample:
    {
      "Data": {
        "StatusCode": 200,
        "body": {
          "@Message.ExtendedInfo": [
           {
            "Message": "Successfully Completed Request",
            "MessageArgs": [],
            "MessageArgs@odata.count": 0,
            "MessageId": "Base.1.0.Success",
            "RelatedProperties": [],
            "RelatedProperties@odata.count": 0,
            "Resolution": "None",
            "Severity": "OK"
           }
          ]
         }
        },
        "Message": "none",
        "Status": "Success",
        "StatusCode": 200,
        "retval": true
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

import os
import tempfile
import json
from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection, idrac_auth_params
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
try:
    from omsdk.sdkfile import file_share_manager
    from omsdk.sdkcreds import UserCredentials
except ImportError:
    pass


# Get Lifecycle Controller status
def run_system_lockdown_mode(idrac, module):
    """
    Get Lifecycle Controller status

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    msg = {'changed': False, 'failed': False, 'msg': "Successfully completed the lockdown mode operations."}
    idrac.use_redfish = True
    share_path = tempfile.gettempdir() + os.sep
    upd_share = file_share_manager.create_share_obj(share_path=share_path, isFolder=True)
    if not upd_share.IsValid:
        module.fail_json(msg="Unable to access the share. Ensure that the share name, "
                             "share mount, and share credentials provided are correct.")
    set_liason = idrac.config_mgr.set_liason_share(upd_share)
    if set_liason['Status'] == "Failed":
        try:
            message = set_liason['Data']['Message']
        except (IndexError, KeyError):
            message = set_liason['Message']
        module.fail_json(msg=message)
    if module.params['lockdown_mode'] == 'Enabled':
        msg["system_lockdown_status"] = idrac.config_mgr.enable_system_lockdown()
    elif module.params['lockdown_mode'] == 'Disabled':
        msg["system_lockdown_status"] = idrac.config_mgr.disable_system_lockdown()

    if msg.get("system_lockdown_status") and "Status" in msg['system_lockdown_status']:
        if msg['system_lockdown_status']['Status'] == "Success":
            msg['changed'] = True
        else:
            module.fail_json(msg="Failed to complete the lockdown mode operations.")
    return msg


# Main
def main():
    specs = dict(
        share_name=dict(required=False, type='str'),
        share_password=dict(required=False, type='str',
                            aliases=['share_pwd'], no_log=True),
        share_user=dict(required=False, type='str'),
        share_mnt=dict(required=False, type='str'),
        lockdown_mode=dict(required=True, choices=['Enabled', 'Disabled'])
    )
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        supports_check_mode=False)

    try:
        with iDRACConnection(module.params) as idrac:
            msg = run_system_lockdown_mode(idrac, module)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, ImportError, SSLValidationError, IOError, ValueError, TypeError, ConnectionError) as e:
        module.fail_json(msg=str(e))
    module.exit_json(msg=msg["msg"], system_lockdown_status=msg["system_lockdown_status"], changed=msg["changed"])


if __name__ == '__main__':
    main()
