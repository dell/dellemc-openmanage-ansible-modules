#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.0.1
# Copyright (C) 2018-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_lifecycle_controller_logs
short_description: Export Lifecycle Controller logs to a network share or local path.
version_added: "2.1.0"
description:
  - Export Lifecycle Controller logs to a given network share or local path.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
  share_name:
    description:
      - Network share or local path.
      - CIFS, NFS network share types are supported.
    type: str
    required: True
  share_user:
    type: str
    description: Network share user in the format 'user@domain' or 'domain\\user' if user is
      part of a domain else 'user'. This option is mandatory for CIFS Network Share.
  share_password:
    type: str
    description: Network share user password. This option is mandatory for CIFS Network Share.
    aliases: ['share_pwd']
  job_wait:
    description: Whether to wait for the running job completion or not.
    type: bool
    default: True

requirements:
  - "omsdk >= 1.2.488"
  - "python >= 3.8.6"
author:
  - "Rajeev Arakkal (@rajeevarakkal)"
  - "Anooja Vardhineni (@anooja-vardhineni)"
notes:
  - This module requires 'Administrator' privilege for I(idrac_user).
  - Exporting data to a local share is supported only on iDRAC9-based PowerEdge Servers and later.
  - Run this module from a system that has direct access to Dell EMC iDRAC.
  - This module does not support C(check_mode).
"""

EXAMPLES = r'''
---
- name: Export lifecycle controller logs to NFS share.
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "192.168.0.0:/nfsfileshare"

- name: Export lifecycle controller logs to CIFS share.
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "\\\\192.168.0.2\\share"
    share_user: "share_user_name"
    share_password: "share_user_pwd"

- name: Export lifecycle controller logs to LOCAL path.
  dellemc.openmanage.idrac_lifecycle_controller_logs:
    idrac_ip: "190.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    share_name: "/example/export_lc"
'''

RETURN = """
---
msg:
  type: str
  description: Status of the export lifecycle controller logs job.
  returned: always
  sample: "Successfully exported the lifecycle controller logs."
lc_logs_status:
  description: Status of the export operation along with job details and file path.
  returned: success
  type: dict
  sample: {
    "ElapsedTimeSinceCompletion": "0",
    "InstanceID": "JID_274774785395",
    "JobStartTime": "NA",
    "JobStatus": "Completed",
    "JobUntilTime": "NA",
    "Message": "LCL Export was successful",
    "MessageArguments": "NA",
    "MessageID": "LC022",
    "Name": "LC Export",
    "PercentComplete": "100",
    "Status": "Success",
    "file": "192.168.0.0:/nfsfileshare/190.168.0.1_20210728_133437_LC_Log.log",
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
"""


from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection, idrac_auth_params
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
import json
try:
    from omsdk.sdkfile import file_share_manager
    from omsdk.sdkcreds import UserCredentials
except ImportError:
    pass


def get_user_credentials(module):
    share_username = module.params['share_user']
    share_password = module.params['share_password']
    work_group = None
    if share_username is not None and "@" in share_username:
        username_domain = share_username.split("@")
        share_username = username_domain[0]
        work_group = username_domain[1]
    elif share_username is not None and "\\" in share_username:
        username_domain = share_username.split("\\")
        work_group = username_domain[0]
        share_username = username_domain[1]
    share = file_share_manager.create_share_obj(share_path=module.params['share_name'],
                                                creds=UserCredentials(share_username, share_password,
                                                                      work_group=work_group), isFolder=True)
    return share


def run_export_lc_logs(idrac, module):
    """
    Export Lifecycle Controller Log to the given file share

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    lclog_file_name_format = "%ip_%Y%m%d_%H%M%S_LC_Log.log"
    share_username = module.params.get('share_user')
    if (share_username is not None) and ("@" in share_username or "\\" in share_username):
        myshare = get_user_credentials(module)
    else:
        myshare = file_share_manager.create_share_obj(share_path=module.params['share_name'],
                                                      creds=UserCredentials(module.params['share_user'],
                                                                            module.params['share_password']),
                                                      isFolder=True)
    lc_log_file = myshare.new_file(lclog_file_name_format)
    job_wait = module.params['job_wait']
    msg = idrac.log_mgr.lclog_export(lc_log_file, job_wait)
    return msg


# Main()
def main():
    specs = {
        "share_name": {"required": True, "type": 'str'},
        "share_user": {"required": False, "type": 'str'},
        "share_password": {"required": False, "type": 'str', "aliases": ['share_pwd'], "no_log": True},
        "job_wait": {"required": False, "type": 'bool', "default": True},
    }
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        supports_check_mode=False)

    try:
        with iDRACConnection(module.params) as idrac:
            msg = run_export_lc_logs(idrac, module)
            if msg.get("Status") in ["Failed", "Failure"] or msg.get("JobStatus") in ["Failed", "Failure"]:
                msg.pop("file", None)
                module.fail_json(msg="Unable to export the lifecycle controller logs.", lc_logs_status=msg)
            message = "Successfully exported the lifecycle controller logs."
            if module.params['job_wait'] is False:
                message = "The export lifecycle controller log job is submitted successfully."
            module.exit_json(msg=message, lc_logs_status=msg)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError) as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
