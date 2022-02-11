#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.0.1
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_application_network_webserver
short_description: Updates the Web server configuration on OpenManage Enterprise
version_added: "2.1.0"
description: This module allows to configure a network web server on OpenManage Enterprise.
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  webserver_port:
    description:
      - Port number used by OpenManage Enterprise to establish a secure server connection.
      - "I(WARNING) A change in port number results in a loss of connectivity in the current session
      for more than a minute."
    type: int
  webserver_timeout:
    description:
      - The duration in minutes after which a web user interface session is automatically disconnected.
      - If a change is made to the session timeout, it will only take effect after the next log in.
    type: int
requirements:
    - "python >= 3.8.6"
author:
    - "Jagadeesh N V(@jagadeeshnv)"
notes:
    - Run this module from a system that has direct access to DellEMC OpenManage Enterprise.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Update web server port and session time out
  dellemc.openmanage.ome_application_network_webserver:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    webserver_port: 9443
    webserver_timeout: 20

- name: Update session time out
  dellemc.openmanage.ome_application_network_webserver:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    webserver_timeout: 30

- name: Update web server port
  dellemc.openmanage.ome_application_network_webserver:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    webserver_port: 8443
'''

RETURN = r'''
---
msg:
  type: str
  description: Overall status of the network web server configuration change.
  returned: always
  sample: "Successfully updated network web server configuration."
webserver_configuration:
  type: dict
  description: Updated application network web server configuration.
  returned: success
  sample: {
        "TimeOut": 20,
        "PortNumber": 443,
        "EnableWebServer": true
        }
error_info:
  description: Details of the HTTP error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
        "@Message.ExtendedInfo": [
            {
               "Message": "Unable to complete the request because the input value
                for  PortNumber  is missing or an invalid value is entered.",
                "MessageArgs": [
                    "PortNumber"
                ],
                "MessageId": "CGEN6002",
                "RelatedProperties": [],
                "Resolution": "Enter a valid value and retry the operation.",
                "Severity": "Critical"
            }
        ],
        "code": "Base.1.0.GeneralError",
        "message": "A general error has occurred. See ExtendedInfo for more information."
    }
    }
'''

import json
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError

WEBSERVER_CONFIG = "ApplicationService/Network/WebServerConfiguration"


def get_updated_payload(rest_obj, module):
    params = module.params
    resp = rest_obj.invoke_request("GET", WEBSERVER_CONFIG)
    current_setting = resp.json_data
    port_changed = 0
    # Remove odata keys ["@odata.context", "@odata.type", "@odata.id"]
    cp = current_setting.copy()
    klist = cp.keys()
    for k in klist:
        if str(k).lower().startswith('@odata'):
            current_setting.pop(k)
    diff = 0
    webserver_payload_map = {
        "webserver_port": "PortNumber",
        "webserver_timeout": "TimeOut",
    }
    for config, pload in webserver_payload_map.items():
        pval = params.get(config)
        if pval is not None:
            if current_setting.get(pload) != pval:
                current_setting[pload] = pval
                if pload == "PortNumber":
                    port_changed = pval
                diff += 1
    if diff == 0:  # Idempotency
        if module.check_mode:
            module.exit_json(msg="No changes found to be applied to the web server.")
        module.exit_json(
            msg="No changes made to the web server configuration as the entered"
                " values are the same as the current configuration.", webserver_configuration=current_setting)
    if module.check_mode:
        module.exit_json(changed=True, msg="Changes found to be applied to the web server.")
    return current_setting, port_changed


def main():
    specs = {
        "webserver_port": {"required": False, "type": "int"},
        "webserver_timeout": {"required": False, "type": "int"},
    }
    specs.update(ome_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        required_one_of=[["webserver_port", "webserver_timeout"]],
        supports_check_mode=True
    )
    try:
        with RestOME(module.params, req_session=False) as rest_obj:
            updated_payload, port_change = get_updated_payload(rest_obj, module)
            msg = "Successfully updated network web server configuration."
            resp = rest_obj.invoke_request("PUT", WEBSERVER_CONFIG, data=updated_payload)
            module.exit_json(msg=msg, webserver_configuration=resp.json_data, changed=True)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except SSLError as err:
        if port_change:
            module.exit_json(msg="{0} Port has changed to {1}.".format(msg, port_change),
                             webserver_configuration=updated_payload, changed=True)
        else:
            module.fail_json(msg=str(err))
    except (IOError, ValueError, TypeError, ConnectionError, SSLValidationError, OSError) as err:
        module.fail_json(msg=str(err))
    except Exception as err:
        module.fail_json(msg=str(err))


if __name__ == "__main__":
    main()
