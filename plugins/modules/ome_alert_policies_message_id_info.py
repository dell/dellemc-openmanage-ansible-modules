#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.2.0
# Copyright (C) 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_alert_policies_message_id_info
short_description: Get message ID information of alert policies for OpenManage Enterprise.
version_added: "8.2.0"
description:
   - "This module retrieves the message ID information of alert policies for OpenManage Enterprise."
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
requirements:
    - "python >= 3.9.6"
author: "Shivam Sharma (@ShivamSh3)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
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
  type: str
  description: Error description in case of error.
  returned: on error
  sample: "HTTP Error 501: 501"
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
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import remove_key
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError

ALERT_MESSAGE_URI = "AlertService/AlertMessageDefinitions"


def main():
    specs = ome_auth_params
    module = AnsibleModule(
        argument_spec=specs,
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            resp = rest_obj.invoke_request('GET', ALERT_MESSAGE_URI)
            message_ids = remove_key(resp.json_data)
            module.exit_json(message_ids=message_ids["value"])
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError, SSLError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
