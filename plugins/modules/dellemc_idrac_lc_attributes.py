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
module: dellemc_idrac_lc_attributes
short_description: Enable or disable Collect System Inventory on Restart (CSIOR) property for all iDRAC/LC jobs
version_added: "1.0.0"
description:
    -  This module is responsible for enabling or disabling of Collect System Inventory on Restart (CSIOR)
        property for all iDRAC/LC jobs.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
    share_name:
        required: True
        type: str
        description: Network share or a local path.
    share_user:
        type: str
        description: Network share user in the format 'user@domain' or 'domain\\user' if user is
            part of a domain else 'user'. This option is mandatory for CIFS Network Share.
    share_password:
        type: str
        description: Network share user password. This option is mandatory for CIFS Network Share.
        aliases: ['share_pwd']
    share_mnt:
        type: str
        description: Local mount path of the network share with read-write permission for ansible user.
            This option is mandatory for Network Share.
    csior:
        type: str
        description: Whether to Enable or Disable Collect System Inventory on Restart (CSIOR)
            property for all iDRAC/LC jobs.
        choices: [Enabled, Disabled]
        default: Enabled
requirements:
    - "omsdk"
    - "python >= 2.7.5"
author: "Felix Stephen (@felixs88)"
notes:
    - Run this module from a system that has direct access to DellEMC iDRAC.
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Set up iDRAC LC Attributes
  dellemc.openmanage.dellemc_idrac_lc_attributes:
       idrac_ip:   "192.168.0.1"
       idrac_user: "user_name"
       idrac_password:  "user_password"
       share_name: "192.168.0.1:/share"
       share_mnt: "/mnt/share"
       csior: "Enabled"
"""

RETURN = r'''
---
msg:
  description: Overall status of iDRAC LC attributes configuration.
  returned: always
  type: str
  sample: Successfully configured the iDRAC LC attributes.
lc_attribute_status:
    description: Collect System Inventory on Restart (CSIOR) property for all iDRAC/LC jobs is configured.
    returned: success
    type: dict
    sample: {
        "CompletionTime": "2020-03-30T00:06:53",
        "Description": "Job Instance",
        "EndTime": null,
        "Id": "JID_1234512345",
        "JobState": "Completed",
        "JobType": "ImportConfiguration",
        "Message": "Successfully imported and applied Server Configuration Profile.",
        "MessageArgs": [],
        "MessageArgs@odata.count": 0,
        "MessageId": "SYS053",
        "Name": "Import Configuration",
        "PercentComplete": 100,
        "StartTime": "TIME_NOW",
        "Status": "Success",
        "TargetSettingsURI": null,
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

import json
from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError

try:
    from omsdk.sdkfile import file_share_manager
    from omsdk.sdkcreds import UserCredentials
except ImportError:
    pass


# Get Lifecycle Controller status
def run_setup_idrac_csior(idrac, module):
    """
    Get Lifecycle Controller status

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    idrac.use_redfish = True
    upd_share = file_share_manager.create_share_obj(share_path=module.params['share_name'],
                                                    mount_point=module.params['share_mnt'],
                                                    isFolder=True,
                                                    creds=UserCredentials(
                                                        module.params['share_user'],
                                                        module.params['share_password'])
                                                    )

    set_liason = idrac.config_mgr.set_liason_share(upd_share)
    if set_liason['Status'] == "Failed":
        try:
            message = set_liason['Data']['Message']
        except (IndexError, KeyError):
            message = set_liason['Message']
        module.fail_json(msg=message)
    if module.params['csior'] == 'Enabled':
        # Enable csior
        idrac.config_mgr.enable_csior()
    elif module.params['csior'] == 'Disabled':
        # Disable csior
        idrac.config_mgr.disable_csior()

    if module.check_mode:
        status = idrac.config_mgr.is_change_applicable()
        if status.get("changes_applicable"):
            module.exit_json(msg="Changes found to commit!", changed=True)
        else:
            module.exit_json(msg="No changes found to commit!")
    else:
        return idrac.config_mgr.apply_changes(reboot=False)


# Main
def main():
    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_password=dict(required=True, type='str', aliases=['idrac_pwd'], no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Export Destination
            share_name=dict(required=True, type='str'),
            share_password=dict(required=False, type='str', aliases=['share_pwd'], no_log=True),
            share_user=dict(required=False, type='str'),
            share_mnt=dict(required=False, type='str'),
            csior=dict(required=False, choices=['Enabled', 'Disabled'], default='Enabled')
        ),

        supports_check_mode=True)

    try:
        with iDRACConnection(module.params) as idrac:
            status = run_setup_idrac_csior(idrac, module)
            if status.get('Status') == "Success":
                changed = True
                msg = "Successfully configured the iDRAC LC attributes."
                if status.get('Message') and (status.get('Message') == "No changes found to commit!" or
                                              "No changes were applied" in status.get('Message')):
                    msg = status.get('Message')
                    changed = False
                elif status.get('Status') == "Failed":
                    module.fail_json(msg="Failed to configure the iDRAC LC attributes.")
                module.exit_json(msg=msg, lc_attribute_status=status, changed=changed)
            else:
                module.fail_json(msg="Failed to configure the iDRAC LC attributes.")
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, ImportError, SSLValidationError, IOError, ValueError, TypeError, ConnectionError) as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
