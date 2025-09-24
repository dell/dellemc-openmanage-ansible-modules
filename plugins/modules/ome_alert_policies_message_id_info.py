#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.1
# Copyright (C) 2023-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

DOCUMENTATION = r'''
---
module: ome_alert_policies_message_id_info
short_description: Get message ID information of alert policies.
version_added: "8.2.0"
description:
   - "This module retrieves the message ID information of alert policies for OpenManage Enterprise
      and OpenManage Enterprise Modular."
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
requirements:
    - "python >= 3.9.6"
author: "Shivam Sharma (@ShivamSh3)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise
      or OpenManage Enterprise Modular.
    - This module supports C(check_mode).
    - This module supports IPv4 and IPv6 addresses.
'''

EXAMPLES = r'''
---
- name: Get message ID details of all alert policies
  dellemc.openmanage.ome_alert_policies_message_id_info:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
'''

RETURN = r'''
---
msg:
  description: "Status of the alert policies message ids fetch operation."
  returned: always
  type: str
  sample: "Successfully retrieved alert policies message ids information."
message_ids:
  type: dict
  description: Details of the message ids.
  returned: success
  sample: [
  {
    "Category": "System Health",
    "DetailedDescription": "The current sensor identified in the message has failed. This condition
     can cause system performance issues and degradation in the monitoring capability of the system.",
    "Message": "The ${0} sensor has failed, and the last recorded value by the sensor was ${1} A.",
    "MessageId": "AMP400",
    "Prefix": "AMP",
    "RecommendedAction": "Check the Embedded System Management (ESM) Log for any sensor related faults.
      If there is a failed sensor, replace the system board. For more information, contact your service provider.",
    "SequenceNo": 400,
    "Severity": "Critical",
    "SubCategory": "Amperage"
  },
  {
    "Category": "System Health",
    "DetailedDescription": "The current sensor identified in the message has failed. This condition can cause
     system performance issues and degradation in the monitoring capability of the system.",
    "Message": "Unable to read the ${0} sensor value.",
    "MessageId": "AMP401",
    "Prefix": "AMP",
    "RecommendedAction": "Check the Embedded System Management (ESM) Log for any sensor related faults. If
     there is a failed sensor, replace the system board. For more information, contact your service provider.",
    "SequenceNo": 401,
    "Severity": "Warning",
    "SubCategory": "Amperage"
  }
]
error_info:
  type: dict
  description: Details of the HTTP Error.
  returned: on HTTP error
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
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import remove_key, get_all_data_with_pagination
from urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError

ALERT_MESSAGE_URI = "AlertService/AlertMessageDefinitions"
SUCCESSFUL_MSG = "Successfully retrieved alert policies message ids information."
EMPTY_MSG = "No alert policies message id information were found."


def main():
    specs = {}
    module = OmeAnsibleModule(
        argument_spec=specs,
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            message_id_info = get_all_data_with_pagination(rest_obj, ALERT_MESSAGE_URI)
            if not message_id_info.get("report_list", []):
                module.exit_json(msg=EMPTY_MSG, message_ids=[])
            message_ids = remove_key(message_id_info['report_list'])
            module.exit_json(msg=SUCCESSFUL_MSG, message_ids=message_ids)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError, SSLError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
