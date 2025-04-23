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
module: idrac_lifecycle_controller_job_status_info
short_description: Get the status of a Lifecycle Controller job
version_added: "2.1.0"
description: This module shows the status of a specific Lifecycle Controller job using its job ID.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
    job_id:
        required: true
        type: str
        description: JOB ID in the format "JID_123456789012".
requirements:
    - "omsdk >= 1.2.488"
    - "python >= 3.9.6"
author:
    - "Rajeev Arakkal (@rajeevarakkal)"
    - "Anooja Vardhineni (@anooja-vardhineni)"
    - "Trisha Datta (@trisha-dell)"
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports both IPv4 and IPv6 address for I(idrac_ip).
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Show status of a Lifecycle Control job
  dellemc.openmanage.idrac_lifecycle_controller_job_status_info:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    job_id: "JID_1234567890"
"""

RETURN = r'''
---
msg:
  description: Overall status of the job facts operation.
  returned: always
  type: str
  sample: "Successfully fetched the job info."
job_info:
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
'''


import json
from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac \
    import iDRACConnection, idrac_auth_params
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish \
    import iDRACRedfishAPI
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.\
    idrac_utils.info.lifecycle_controller_job_status \
    import IDRACLifecycleControllerJobStatusInfo
from ansible_collections.dellemc.openmanage.plugins.module_utils.\
    idrac_utils.info.firmware import IDRACFirmwareInfo

ERR_STATUS = 404
FETCH_MESSAGE = "Successfully fetched the job info."


def main():
    specs = {
        "job_id": {"required": True, "type": 'str'}
    }
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        supports_check_mode=True)

    try:
        with iDRACRedfishAPI(module.params) as idrac:
            firmware_obj = IDRACFirmwareInfo(idrac)
            if not firmware_obj.is_omsdk_required():
                response = \
                    IDRACLifecycleControllerJobStatusInfo(idrac). \
                    get_lifecycle_controller_job_status_info(job_id=module.params["job_id"])
                if response != "Job ID is invalid":
                    lifecycle_controller_job_status_info = \
                        IDRACLifecycleControllerJobStatusInfo(idrac). \
                        transform_job_status_data(info_data=response.json_data)
                else:
                    module.exit_json(msg=FETCH_MESSAGE,
                                     job_info={})
            else:
                with iDRACConnection(module.params) as idrac:
                    job_id = module.params.get('job_id')
                    lifecycle_controller_job_status_info = \
                        idrac.job_mgr.get_job_status(job_id)
                    if lifecycle_controller_job_status_info.get('Status') == "Found Fault":
                        module.exit_json(msg=FETCH_MESSAGE,
                                         job_info={})
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err),
                         failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError,
            SSLValidationError,
            IOError, ValueError,
            TypeError,
            ConnectionError) as e:
        module.exit_json(msg=str(e), failed=True)

    module.exit_json(msg="Successfully fetched the job info.",
                     job_info=lifecycle_controller_job_status_info)


if __name__ == '__main__':
    main()
