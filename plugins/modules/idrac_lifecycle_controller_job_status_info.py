#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.1
# Copyright (C) 2018-2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: idrac_lifecycle_controller_job_status_info
short_description: Get the status of a Lifecycle Controller job.
version_added: "2.10.0"
description: This module shows the status of a specific Lifecycle Controller job using its job ID.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
    job_id:
        required: True
        type: str
        description: JOB ID in the format "JID_123456789012".
requirements:
    - "omsdk"
    - "python >= 2.7.5"
author:
    - "Rajeev Arakkal (@rajeevarakkal)"
    - "Anooja Vardhineni (@anooja-vardhineni)"
"""

EXAMPLES = """
---
- name: Show status of a Lifecycle Control job.
  dellemc.openmanage.idrac_lifecycle_controller_job_status_info:
       idrac_ip:  "192.168.0.1"
       idrac_user:  "user_name"
       idrac_password:  "user_password"
       job_id:  "JID_1234567890"
"""

RETURNS = """
msg:
  description: Displays the status of a Lifecycle Controller job.
  returned: success
  type: dict
  sample: {
    "ElapsedTimeSinceCompletion": "8742",
    "InstanceID": "JID_844222910040",
    "JobStartTime": "NA",
    "JobStatus": "Completed",
    "JobUntilTime": "NA",
    "Message": "Job completed successfully.",
    "MessageArguments": "NA",
    "MessageID": "RED001",
    "Name": "update:DCIM:INSTALLED#iDRAC.Embedded.1-1#IDRACinfo",
    "PercentComplete": "100",
    "Status": "Success"
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
            "job_id": {"required": True, "type": 'str'}
        },
        supports_check_mode=False)

    try:
        with iDRACConnection(module.params) as idrac:
            job_id, msg, failed = module.params.get('job_id'), {}, False
            msg = idrac.job_mgr.get_job_status(job_id)
            if msg.get('Status') == "Found Fault":
                failed = True
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError) as e:
        module.fail_json(msg=str(e))
    module.exit_json(msg=msg, failed=failed)


if __name__ == '__main__':
    main()
