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
module: idrac_lifecycle_controller_jobs
short_description: Delete the Lifecycle Controller Jobs
version_added: "2.1.0"
description:
    - Delete a Lifecycle Controller job using its job ID or delete all jobs.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
    job_id:
        type: str
        description:
           - Job ID of the specific job to be deleted.
           - All the jobs in the job queue are deleted if this option is not specified.

requirements:
    - "omsdk >= 1.2.488"
    - "python >= 3.8.6"
author:
    - "Felix Stephen (@felixs88)"
    - "Anooja Vardhineni (@anooja-vardhineni)"
notes:
    - Run this module from a system that has direct access to DellEMC iDRAC.
    - This module does not support C(check_mode).
"""
EXAMPLES = """
---
- name: Delete Lifecycle Controller job queue
  dellemc.openmanage.idrac_lifecycle_controller_jobs:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       ca_path: "/path/to/ca_cert.pem"

- name: Delete Lifecycle Controller job using a job ID
  dellemc.openmanage.idrac_lifecycle_controller_jobs:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       ca_path: "/path/to/ca_cert.pem"
       job_id: "JID_801841929470"
"""
RETURN = """
---
msg:
  type: str
  description: Status of the delete operation.
  returned: always
  sample: 'Successfully deleted the job.'
status:
  type: dict
  description: Details of the delete operation.
  returned: success
  sample: {
        'Message': 'The specified job was deleted',
        'MessageID': 'SUP020',
        'ReturnValue': '0'
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


import json
from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection, idrac_auth_params
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError


def main():
    specs = {
        "job_id": {"required": False, "type": 'str'}
    }
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        supports_check_mode=False)
    try:
        with iDRACConnection(module.params) as idrac:
            job_id, resp = module.params.get('job_id'), {}
            if job_id is not None:
                resp = idrac.job_mgr.delete_job(job_id)
                jobstr = "job"
            else:
                resp = idrac.job_mgr.delete_all_jobs()
                jobstr = "job queue"
            if resp["Status"] == "Error":
                msg = "Failed to delete the Job: {0}.".format(job_id)
                module.fail_json(msg=msg, status=resp)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (ImportError, ValueError, RuntimeError, TypeError) as e:
        module.fail_json(msg=str(e))
    module.exit_json(msg="Successfully deleted the {0}.".format(jobstr), status=resp, changed=True)


if __name__ == '__main__':
    main()
