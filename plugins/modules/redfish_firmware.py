#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.0.0
# Copyright (C) 2019-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
---
module: redfish_firmware
short_description: To perform a component firmware update using the image file available on the local or remote system
version_added: "2.1.0"
description:
    - This module allows the firmware update of only one component at a time.
      If the module is run for more than one component, an error message is returned.
    - Depending on the component, the firmware update is applied after an automatic or manual reboot.
extends_documentation_fragment:
  - dellemc.openmanage.redfish_auth_options
options:
    image_uri:
        description:
            - Firmware Image location URI or local path.
            - For example- U(http://<web_address>/components.exe) or /home/firmware_repo/component.exe.
        type: str
        required: True
    transfer_protocol:
        description: Protocol used to transfer the firmware image file. Applicable for URI based update.
        type: str
        default: HTTP
        choices: ["CIFS", "FTP", "HTTP", "HTTPS", "NSF", "OEM", "SCP", "SFTP", "TFTP"]
requirements:
    - "python >= 2.7.5"
    - "urllib3"
author:
    - "Felix Stephen (@felixs88)"
notes:
    - Run this module from a system that has direct access to Redfish APIs.
    - This module does not support C(check_mode).
"""

EXAMPLES = """
---
- name: Update the firmware from a single executable file available in a HTTP protocol
  dellemc.openmanage.redfish_firmware:
    baseuri: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    image_uri: "http://192.168.0.2/firmware_repo/component.exe"
    transfer_protocol: "HTTP"

- name: Update the firmware from a single executable file available in a local path
  dellemc.openmanage.redfish_firmware:
    baseuri: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    image_uri: "/home/firmware_repo/component.exe"
"""

RETURN = """
---
msg:
  description: Overall status of the firmware update task.
  returned: always
  type: str
  sample: Successfully submitted the firmware update task.
task:
  description: Returns ID and URI of the created task.
  returned: success
  type: dict
  sample: {
        "id": "JID_XXXXXXXXXXXX",
        "uri": "/redfish/v1/TaskService/Tasks/JID_XXXXXXXXXXXX"
    }
error_info:
  type: dict
  description: Details of http error.
  returned: on http error
  sample:  {
        "error": {
            "@Message.ExtendedInfo": [
                {
                    "Message": "Unable to complete the operation because the JSON data format entered is invalid.",
                    "Resolution": "Do the following and the retry the operation:
                        1) Enter the correct JSON data format and retry the operation.
                        2) Make sure that no syntax error is present in JSON data format.
                        3) Make sure that a duplicate key is not present in JSON data format.",
                    "Severity": "Critical"
                },
                {
                    "Message": "The request body submitted was malformed JSON and
                        could not be parsed by the receiving service.",
                    "Resolution": "Ensure that the request body is valid JSON and resubmit the request.",
                    "Severity": "Critical"
                }
            ],
            "code": "Base.1.2.GeneralError",
            "message": "A general error has occurred. See ExtendedInfo for more information."
        }
    }
"""


import json
import os
from ansible_collections.dellemc.openmanage.plugins.module_utils.redfish import Redfish
from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError

try:
    from urllib3.fields import RequestField
    from urllib3.filepost import encode_multipart_formdata
    HAS_LIB = True
except ImportError:
    HAS_LIB = False

UPDATE_SERVICE = "UpdateService"


def _encode_form_data(payload_file):
    """Encode multipart/form-data for file upload."""
    fields = []
    f_name, f_data, f_type = payload_file.get("file")
    f_binary = f_data.read()
    req_field = RequestField(name="file", data=f_binary, filename=f_name)
    req_field.make_multipart(content_type=f_type)
    fields.append(req_field)
    data, content_type = encode_multipart_formdata(fields)
    return data, content_type


def _get_update_service_target(obj, module):
    """Returns all the URI which is required for firmware update dynamically."""
    action_resp = obj.invoke_request("GET", "{0}{1}".format(obj.root_uri, UPDATE_SERVICE))
    action_attr = action_resp.json_data["Actions"]
    protocol = module.params["transfer_protocol"]
    update_uri = None
    push_uri = action_resp.json_data.get('HttpPushUri')
    inventory_uri = action_resp.json_data.get('FirmwareInventory').get('@odata.id')
    if "#UpdateService.SimpleUpdate" in action_attr:
        update_service = action_attr.get("#UpdateService.SimpleUpdate")
        proto = update_service.get("TransferProtocol@Redfish.AllowableValues")
        if isinstance(proto, list) and protocol in proto and 'target' in update_service:
            update_uri = update_service.get('target')
        else:
            module.fail_json(msg="Target firmware version does not support {0} protocol.".format(protocol))
    if update_uri is None or push_uri is None or inventory_uri is None:
        module.fail_json(msg="Target firmware version does not support redfish firmware update.")
    return str(inventory_uri), str(push_uri), str(update_uri)


def firmware_update(obj, module):
    """Firmware update using single binary file from Local path or HTTP location."""
    image_path = module.params.get("image_uri")
    trans_proto = module.params["transfer_protocol"]
    inventory_uri, push_uri, update_uri = _get_update_service_target(obj, module)
    if image_path.startswith("http"):
        payload = {"ImageURI": image_path, "TransferProtocol": trans_proto}
        update_status = obj.invoke_request("POST", update_uri, data=payload)
    else:
        resp_inv = obj.invoke_request("GET", inventory_uri)
        binary_payload = {"file": (image_path.split(os.sep)[-1], open(os.path.join(image_path), "rb"), "multipart/form-data")}
        data, ctype = _encode_form_data(binary_payload)
        headers = {"If-Match": resp_inv.headers.get("etag")}
        headers.update({"Content-Type": ctype})
        upload_status = obj.invoke_request("POST", push_uri, data=data, headers=headers, dump=False, api_timeout=100)
        if upload_status.status_code == 201:
            payload = {"ImageURI": upload_status.headers.get("location")}
            update_status = obj.invoke_request("POST", update_uri, data=payload)
        else:
            update_status = upload_status
    return update_status


def main():
    module = AnsibleModule(
        argument_spec={
            "baseuri": {"required": True, "type": "str"},
            "username": {"required": True, "type": "str"},
            "password": {"required": True, "type": "str", "no_log": True},
            "image_uri": {"required": True, "type": "str"},
            "transfer_protocol": {"type": "str", "default": "HTTP",
                                  "choices": ["CIFS", "FTP", "HTTP", "HTTPS", "NSF", "OEM", "SCP", "SFTP", "TFTP"]},
        },
        supports_check_mode=False)
    if not HAS_LIB:
        module.fail_json(msg=missing_required_lib("urllib3"))
    try:
        message = "Failed to submit the firmware update task."
        with Redfish(module.params, req_session=True) as obj:
            status = firmware_update(obj, module)
            if status.success:
                message = "Successfully submitted the firmware update task."
                task_uri = status.headers.get("Location")
                task_id = task_uri.split("/")[-1]
                module.exit_json(msg=message, task={"id": task_id, "uri": task_uri}, changed=True)
            module.fail_json(msg=message, error_info=json.loads(status))
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except (RuntimeError, URLError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError, IOError, AssertionError) as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
