#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.1
# Copyright (C) 2022-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_virtual_media
short_description: Configure the Remote File Share settings.
version_added: "6.3.0"
description:
  - This module allows to configure Remote File Share settings.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_x_auth_options
options:
  virtual_media:
    required: true
    type: list
    elements: dict
    description: Details of the Remote File Share.
    suboptions:
      insert:
        required: true
        type: bool
        description:
          - C(true) connects the remote image file.
          - C(false) ejects the remote image file if connected.
      image:
        type: path
        description:
          - The path of the image file. The supported file types are .img and .iso.
          - The file name with .img extension is redirected as a virtual floppy and a file name with .iso extension is
            redirected as a virtual CDROM.
          - This option is required when I(insert) is C(true).
          - "The following are the examples of the share location:
            CIFS share: //192.168.0.1/file_path/image_name.iso,
            NFS share: 192.168.0.2:/file_path/image_name.img,
            HTTP share: http://192.168.0.3/file_path/image_name.iso,
            HTTPS share: https://192.168.0.4/file_path/image_name.img"
          - CIFS share is not supported by iDRAC8.
          - HTTPS share with credentials is not supported by iDRAC8.
      index:
        type: int
        description:
          - Index of the Remote File Share. For example, to specify the Remote File Share 1, the value of I(index)
            should be 1. If I(index) is not specified, the order of I(virtual_media) list will be considered.
      domain:
        type: str
        description: Domain name of network share. This option is applicable for CIFS and HTTPS share.
      username:
        type: str
        description: Network share username. This option is applicable for CIFS and HTTPS share.
      password:
        type: str
        description:
          - Network share password. This option is applicable for CIFS and HTTPS share.
          - This module always reports as the changes found when I(password) is provided.
      media_type:
        type: str
        description: Type of the image file. This is applicable when I(insert) is C(true).
        choices: [CD, DVD, USBStick]
  force:
    type: bool
    description: C(true) ejects the image file if already connected and inserts the file provided in I(image).
      This is applicable when I(insert) is C(true).
    default: false
  resource_id:
    type: str
    description: Resource id of the iDRAC, if not specified manager collection id will be used.
requirements:
    - "python >= 3.9.6"
author:
    - "Felix Stephen (@felixs88)"
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports C(check_mode).
"""


EXAMPLES = """
---
- name: Insert image file to Remote File Share 1 using CIFS share.
  dellemc.openmanage.idrac_virtual_media:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    virtual_media:
      - insert: true
        image: "//192.168.0.2/file_path/file.iso"
        username: "username"
        password: "password"

- name: Insert image file to Remote File Share 2 using NFS share.
  dellemc.openmanage.idrac_virtual_media:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    virtual_media:
      - index: 2
        insert: true
        image: "192.168.0.4:/file_path/file.iso"

- name: Insert image file to Remote File Share 1 and 2 using HTTP.
  dellemc.openmanage.idrac_virtual_media:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    force: true
    virtual_media:
      - index: 1
        insert: true
        image: "http://192.168.0.4/file_path/file.img"
      - index: 2
        insert: true
        image: "http://192.168.0.4/file_path/file.img"

- name: Insert image file using HTTPS.
  dellemc.openmanage.idrac_virtual_media:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    force: true
    virtual_media:
      - index: 1
        insert: true
        image: "https://192.168.0.5/file_path/file.img"
        username: username
        password: password

- name: Eject multiple virtual media.
  dellemc.openmanage.idrac_virtual_media:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    force: true
    virtual_media:
      - index: 1
        insert: false
      - index: 2
        insert: false

- name: Ejection of image file from Remote File Share 1.
  dellemc.openmanage.idrac_virtual_media:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    force: true
    virtual_media:
      insert: false

- name: Insertion and ejection of image file in single task.
  dellemc.openmanage.idrac_virtual_media:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    force: true
    virtual_media:
      - index: 1
        insert: true
        image: https://192.168.0.5/file/file.iso
        username: username
        password: password
      - index: 2
        insert: false
"""


RETURN = r'''
---
msg:
  description: Successfully performed the virtual media operation.
  returned: success
  type: str
  sample: Successfully performed the virtual media operation.
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
import copy
import time
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, IdracAnsibleModule


MANAGER_BASE = "/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia"
SYSTEM_BASE = "/redfish/v1/Systems/System.Embedded.1/VirtualMedia"

EXCEEDED_ERROR = "Unable to complete the operation because the virtual media settings " \
                 "provided exceeded the maximum limit."
NO_CHANGES_FOUND = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
INVALID_INDEX = "Unable to compete the virtual media operation because the index provided is incorrect or invalid."
FAIL_MSG = "Unable to complete the virtual media operation."
SUCCESS_MSG = "Successfully performed the virtual media operation."
UNSUPPORTED_IMAGE = "Unable to complete the virtual media operation because unsupported image " \
                    "provided. The supported file types are .img and .iso."
UNSUPPORTED_MEDIA = "Unable to complete the virtual media operation because unsupported media type " \
                    "provided for index {0}"
UNSUPPORTED_MSG = "The system does not support the CIFS network share feature."
UNSUPPORTED_MSG_HTTPS = "The system does not support the HTTPS network share feature with credentials."


def get_virtual_media_info(idrac):
    resp = idrac.invoke_request("/redfish/v1/", "GET")
    redfish_version = resp.json_data["RedfishVersion"]
    rd_version = redfish_version.replace(".", "")
    if 1131 <= int(rd_version):
        vr_id = "system"
        member_resp = idrac.invoke_request("{0}?$expand=*($levels=1)".format(SYSTEM_BASE), "GET")
    else:
        vr_id = "manager"
        member_resp = idrac.invoke_request("{0}?$expand=*($levels=1)".format(MANAGER_BASE), "GET")
    response = member_resp.json_data["Members"]
    return response, vr_id, rd_version


def get_payload_data(each, vr_members, vr_id):
    is_change, unsup_media, input_vr_mem = False, None, {}
    vr_mem = vr_members[each["index"] - 1]

    if each["insert"]:
        exist_vr_mem = dict((k, vr_mem[k]) for k in ["Inserted", "Image", "UserName", "Password"] if vr_mem.get(k) is not None)
        input_vr_mem = {"Inserted": each["insert"], "Image": each["image"]}
        if each["image"].startswith("//") or each["image"].lower().startswith("https://"):
            username, password, domain = each.get("username"), each.get("password"), each.get("domain")
            if username is not None:
                if domain is not None:
                    username = "{0}\\{1}".format(domain, username)
                input_vr_mem["UserName"] = username
            if password is not None:
                input_vr_mem["Password"] = password
        else:
            exist_vr_mem.pop("UserName", None)
            exist_vr_mem.pop("Password", None)

        inp_mt = each.get("media_type")
        if inp_mt is not None and inp_mt == "CD" and input_vr_mem["Image"][-4:].lower() != ".iso":
            unsup_media = each["index"]
        if inp_mt is not None and inp_mt == "DVD" and input_vr_mem["Image"][-4:].lower() != ".iso":
            unsup_media = each["index"]
        if inp_mt is not None and inp_mt == "USBStick" and input_vr_mem["Image"][-4:].lower() != ".img":
            unsup_media = each["index"]

        is_change = bool(set(exist_vr_mem.items()) ^ set(input_vr_mem.items()))
    else:
        if vr_id == "manager":
            for vr_v in vr_members:
                exist_vr_mem = dict((k, vr_v[k]) for k in ["Inserted"])
                input_vr_mem = {"Inserted": each.get("insert")}
                is_change = bool(set(exist_vr_mem.items()) ^ set(input_vr_mem.items()))
                if is_change:
                    vr_mem = vr_v
                    break
        else:
            exist_vr_mem = dict((k, vr_mem[k]) for k in ["Inserted"])
            input_vr_mem = {"Inserted": each.get("insert")}
            is_change = bool(set(exist_vr_mem.items()) ^ set(input_vr_mem.items()))

    return is_change, input_vr_mem, vr_mem, unsup_media


def _validate_params(module, vr_members, rd_version):
    image = vr_members.get("image")
    if image is not None and (image.startswith("//") or image.startswith("\\\\")):
        if vr_members.get("username") is None or vr_members.get("password") is None:
            module.fail_json(msg="CIFS share required username and password.")
    if image is not None and image.startswith("\\\\"):
        vr_members["image"] = image.replace("\\", "/")
    if 140 >= int(rd_version) and image is not None:
        if (vr_members.get("username") is not None or vr_members.get("password") is not None) and \
                image.startswith("https://"):
            module.fail_json(msg=UNSUPPORTED_MSG_HTTPS)
        elif image.startswith("\\\\") or image.startswith("//"):
            module.fail_json(msg=UNSUPPORTED_MSG)


def virtual_media_operation(idrac, module, payload, vr_id):
    err_payload = []
    force = module.params["force"]

    for i in payload:
        try:
            if force and i["vr_mem"]["Inserted"] and i["payload"]["Inserted"]:
                idrac.invoke_request(i["vr_mem"]["Actions"]["#VirtualMedia.EjectMedia"]["target"],
                                     "POST", data="{}", dump=False)
                time.sleep(5)
                idrac.invoke_request(i["vr_mem"]["Actions"]["#VirtualMedia.InsertMedia"]["target"],
                                     "POST", data=i["payload"])
            elif not force and i["vr_mem"]["Inserted"] and i["payload"]["Inserted"]:
                idrac.invoke_request(i["vr_mem"]["Actions"]["#VirtualMedia.EjectMedia"]["target"],
                                     "POST", data="{}", dump=False)
                time.sleep(5)
                idrac.invoke_request(i["vr_mem"]["Actions"]["#VirtualMedia.InsertMedia"]["target"],
                                     "POST", data=i["payload"])
            elif not i["vr_mem"]["Inserted"] and i["payload"]["Inserted"]:
                idrac.invoke_request(i["vr_mem"]["Actions"]["#VirtualMedia.InsertMedia"]["target"],
                                     "POST", data=i["payload"])
            elif i["vr_mem"]["Inserted"] and not i["payload"]["Inserted"]:
                idrac.invoke_request(i["vr_mem"]["Actions"]["#VirtualMedia.EjectMedia"]["target"],
                                     "POST", data="{}", dump=False)
            time.sleep(5)
        except Exception as err:
            error = json.load(err).get("error")
            if vr_id == "manager":
                msg_id = error["@Message.ExtendedInfo"][0]["MessageId"]
                if "VRM0021" in msg_id or "VRM0012" in msg_id:
                    uri = i["vr_mem"]["Actions"]["#VirtualMedia.EjectMedia"]["target"]
                    if "RemovableDisk" in uri:
                        uri = uri.replace("RemovableDisk", "CD")
                    elif "CD" in uri:
                        uri = uri.replace("CD", "RemovableDisk")
                    idrac.invoke_request(uri, "POST", data="{}", dump=False)
                    time.sleep(5)
                    idrac.invoke_request(i["vr_mem"]["Actions"]["#VirtualMedia.InsertMedia"]["target"],
                                         "POST", data=i["payload"])
                else:
                    err_payload.append(error)
            else:
                err_payload.append(error)
    return err_payload


def virtual_media(idrac, module, vr_members, vr_id, rd_version):
    vr_input = module.params["virtual_media"]
    vr_input_copy = copy.deepcopy(vr_input)
    vr_index, invalid_idx, manager_idx = [], [], 0

    for idx, value in enumerate(vr_input_copy, start=1):
        if vr_id == "manager":
            if value.get("index") is not None:
                manager_idx = value["index"]
            if value.get("image") is not None and value.get("image")[-4:] == ".img":
                value["index"] = 1
            elif value.get("image") is not None and value.get("image")[-4:] == ".iso":
                value["index"] = 2
            elif not value["insert"] and value["index"] is None:
                value["index"] = idx
        else:
            if value.get("index") is None:
                value["index"] = idx
        if value["index"] == 0:
            invalid_idx.append(value["index"])
        vr_index.append(value["index"])

        _validate_params(module, value, rd_version)

    if ((len(set(vr_index)) != len(vr_index)) or (len(vr_members) < max(vr_index)) or invalid_idx) and vr_id == "system":
        module.fail_json(msg=INVALID_INDEX)
    if (vr_id == "manager") and (1 < manager_idx):
        module.fail_json(msg=INVALID_INDEX)
    payload, unsupported_media = [], []
    for each in vr_input_copy:

        is_change, ret_payload, action, unsup_media = get_payload_data(each, vr_members, vr_id)
        if unsup_media is not None:
            unsupported_media.append(unsup_media)
        if module.params["force"] and not is_change and each["insert"]:
            is_change = True
        if is_change:
            payload.append({"payload": ret_payload, "vr_mem": action, "input": each})

    if unsupported_media:
        if vr_id == "manager":
            module.fail_json(msg=UNSUPPORTED_MEDIA.format("1"))
        module.fail_json(msg=UNSUPPORTED_MEDIA.format(", ".join(list(map(str, unsupported_media)))))

    if module.check_mode and payload:
        module.exit_json(msg=CHANGES_FOUND, changed=True)
    elif module.check_mode and not payload:
        module.exit_json(msg=NO_CHANGES_FOUND)
    elif not module.check_mode and not payload:
        module.exit_json(msg=NO_CHANGES_FOUND)

    status = virtual_media_operation(idrac, module, payload, vr_id)

    return status


def _validate_image_format(module):
    unsup_image = False
    for each in module.params["virtual_media"]:
        if each["insert"] and each.get("image") is not None and each.get("image")[-4:].lower() not in [".iso", ".img"]:
            unsup_image = True
    if unsup_image:
        module.fail_json(msg=UNSUPPORTED_IMAGE)


def main():
    specs = {
        "virtual_media": {
            "required": True, "type": "list", "elements": "dict",
            "options": {
                "insert": {"required": True, "type": "bool"},
                "image": {"required": False, "type": "path"},
                "index": {"required": False, "type": "int"},
                "domain": {"required": False, "type": "str"},
                "username": {"required": False, "type": "str"},
                "password": {"required": False, "type": "str", "no_log": True},
                "media_type": {"required": False, "type": "str", "choices": ["CD", "DVD", "USBStick"]},
            },
            "required_if": [["insert", True, ("image", )]],
        },
        "force": {"required": False, "type": "bool", "default": False},
        "resource_id": {"required": False, "type": 'str'},
    }

    module = IdracAnsibleModule(argument_spec=specs, supports_check_mode=True)
    try:
        with iDRACRedfishAPI(module.params, req_session=True) as idrac:
            vr_media = module.params["virtual_media"]
            vr_members, vr_id, rd_version = get_virtual_media_info(idrac)
            if (len(vr_media) > len(vr_members) and vr_id == "system") or \
                    (len(vr_media) > 1 and vr_id == "manager"):
                module.fail_json(msg=EXCEEDED_ERROR)
            _validate_image_format(module)
            resp = virtual_media(idrac, module, vr_members, vr_id, rd_version)
            if resp:
                module.fail_json(msg=FAIL_MSG, error_info=resp)
            module.exit_json(msg=SUCCESS_MSG, changed=True)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
