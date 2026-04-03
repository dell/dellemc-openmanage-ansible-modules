#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.1.0
# Copyright (C) 2018-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
---
module: dellemc_idrac_lc_attributes
short_description: Enable or disable Collect System Inventory on Restart (CSIOR) property for all iDRAC/LC jobs
version_added: "1.0.0"
deprecated:
  removed_at_date: "2024-12-31"
  why: Replaced with M(dellemc.openmanage.idrac_attributes).
  alternative: Use M(dellemc.openmanage.idrac_attributes) instead.
  removed_from_collection: dellemc.openmanage
description:
    -  This module is responsible for enabling or disabling of Collect System Inventory on Restart (CSIOR)
        property for all iDRAC/LC jobs.
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
    csior:
        type: str
        description: Whether to Enable or Disable Collect System Inventory on Restart (CSIOR)
            property for all iDRAC/LC jobs.
        choices: [Enabled, Disabled]
        default: Enabled
requirements:
    - "python >= 3.9.6"
author: "Felix Stephen (@felixs88)"
notes:
    - This module requires 'Administrator' privilege for I(idrac_user).
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports both IPv4 and IPv6 address for I(idrac_ip).
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Set up iDRAC LC Attributes
  dellemc.openmanage.dellemc_idrac_lc_attributes:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
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
from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection, idrac_auth_params
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError


# Get Lifecycle Controller status
def run_setup_idrac_csior(idrac, module):
    """
    Get Lifecycle Controller status

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    raise NotImplementedError("Legacy omsdk support has been removed.")


# Main
def main():
    specs = dict(
        share_name=dict(required=False, type='str'),
        share_password=dict(required=False, type='str', aliases=['share_pwd'], no_log=True),
        share_user=dict(required=False, type='str'),
        share_mnt=dict(required=False, type='str'),
        csior=dict(required=False, choices=['Enabled', 'Disabled'], default='Enabled')
    )
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
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
                module.exit_json(msg=msg, lc_attribute_status=status, changed=changed)
            else:
                module.fail_json(msg="Failed to configure the iDRAC LC attributes.")
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, ImportError, SSLValidationError, IOError, ValueError, TypeError, ConnectionError) as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':  # pragma: no cover
    main()
