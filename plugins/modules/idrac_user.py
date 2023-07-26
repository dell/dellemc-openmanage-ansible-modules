#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.1.0
# Copyright (C) 2018-2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_user
short_description: Configure settings for user accounts
version_added: "2.1.0"
description:
  - This module allows to perform the following,
  - Add a new user account.
  - Edit a user account.
  - Enable or Disable a user account.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
  state:
    type: str
    description:
      - Select C(present) to create or modify a user account.
      - Select C(absent) to remove a user account.
    choices: [present, absent]
    default: present
  user_name:
    type: str
    required: true
    description: Provide the I(user_name) of the account to be created, deleted or modified.
  user_password:
    type: str
    description:
      - Provide the password for the user account. The password can be changed when the user account is modified.
      - To ensure security, the I(user_password) must be at least eight characters long and must contain
        lowercase and upper-case characters, numbers, and special characters.
  new_user_name:
    type: str
    description: Provide the I(user_name) for the account to be modified.
  privilege:
    type: str
    description:
      - Following are the role-based privileges.
      - A user with C(Administrator) privilege can log in to iDRAC, and then configure iDRAC, configure users,
        clear logs, control and configure system, access virtual console, access virtual media, test alerts,
        and execute debug commands.
      - A user with C(Operator) privilege can log in to iDRAC, and then configure iDRAC, control and configure system,
        access virtual console, access virtual media, and execute debug commands.
      - A user with C(ReadOnly) privilege can only log in to iDRAC.
      - A user with C(None), no privileges assigned.
      - Will be ignored, if custom_privilege parameter is provided.
    choices: [Administrator, ReadOnly, Operator, None]
  custom_privilege:
    type: int
    description:
      - The privilege level assigned to the user.
    version_added: "8.1.0"
  ipmi_lan_privilege:
    type: str
    description: The Intelligent Platform Management Interface LAN privilege level assigned to the user.
    choices: [Administrator, Operator, User, No Access]
  ipmi_serial_privilege:
    type: str
    description:
      - The Intelligent Platform Management Interface Serial Port privilege level assigned to the user.
      - This option is only applicable for rack and tower servers.
    choices: [Administrator, Operator, User, No Access]
  enable:
    type: bool
    description: Provide the option to enable or disable a user from logging in to iDRAC.
  sol_enable:
    type: bool
    description: Enables Serial Over Lan (SOL) for an iDRAC user.
  protocol_enable:
    type: bool
    description: Enables protocol for the iDRAC user.
  authentication_protocol:
    type: str
    description:
      - This option allows to configure one of the following authentication protocol
        types to authenticate the iDRAC user.
      - Secure Hash Algorithm C(SHA).
      - Message Digest 5 C(MD5).
      - An authentication protocol is not configured if C(None) is selected.
    choices: [None, SHA, MD5]
  privacy_protocol:
    type: str
    description:
      - This option allows to configure one of the following privacy encryption protocols for the iDRAC user.
      - Data Encryption Standard C(DES).
      - Advanced Encryption Standard C(AES).
      - A privacy protocol is not configured if C(None) is selected.
    choices: [None, DES, AES]
requirements:
  - "python >= 3.8.6"
author: "Felix Stephen (@felixs88)"
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Configure a new iDRAC user
  dellemc.openmanage.idrac_user:
    idrac_ip: 198.162.0.1
    idrac_user: idrac_user
    idrac_password: idrac_password
    ca_path: "/path/to/ca_cert.pem"
    state: present
    user_name: user_name
    user_password: user_password
    privilege: Administrator
    ipmi_lan_privilege: Administrator
    ipmi_serial_privilege: Administrator
    enable: true
    sol_enable: true
    protocol_enable: true
    authentication_protocol: SHA
    privacy_protocol: AES

- name: Modify existing iDRAC user username and password
  dellemc.openmanage.idrac_user:
    idrac_ip: 198.162.0.1
    idrac_user: idrac_user
    idrac_password: idrac_password
    ca_path: "/path/to/ca_cert.pem"
    state: present
    user_name: user_name
    new_user_name: new_user_name
    user_password: user_password

- name: Delete existing iDRAC user account
  dellemc.openmanage.idrac_user:
    idrac_ip: 198.162.0.1
    idrac_user: idrac_user
    idrac_password: idrac_password
    ca_path: "/path/to/ca_cert.pem"
    state: absent
    user_name: user_name
"""

RETURN = r'''
---
msg:
  description: Status of the iDRAC user configuration.
  returned: always
  type: str
  sample: "Successfully created user account details."
status:
  description: Configures the iDRAC users attributes.
  returned: success
  type: dict
  sample: {
    "@Message.ExtendedInfo": [{
      "Message": "Successfully Completed Request",
      "MessageArgs": [],
      "MessageArgs@odata.count": 0,
      "MessageId": "Base.1.5.Success",
      "RelatedProperties": [],
      "RelatedProperties@odata.count": 0,
      "Resolution": "None",
      "Severity": "OK"
      }, {
      "Message": "The operation successfully completed.",
      "MessageArgs": [],
      "MessageArgs@odata.count": 0,
      "MessageId": "IDRAC.2.1.SYS413",
      "RelatedProperties": [],
      "RelatedProperties@odata.count": 0,
      "Resolution": "No response action is required.",
      "Severity": "Informational"}
      ]}
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
import re
import time
from ssl import SSLError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, idrac_auth_params
from ansible.module_utils.basic import AnsibleModule


ACCOUNT_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Accounts/"
ATTRIBUTE_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Attributes/"
USER_ROLES = {"Administrator": 511, "Operator": 499, "ReadOnly": 1, "None": 0}
ACCESS = {0: "Disabled", 1: "Enabled"}
INVALID_PRIVILAGE_MSG = "custom_privilege value should be from 0 to 511."
INVALID_PRIVILAGE_MIN = 0
INVALID_PRIVILAGE_MAX = 511


def compare_payload(json_payload, idrac_attr):
    """
    :param json_payload: json payload created for update operation
    :param idrac_attr: idrac user attributes
    case1: always skip password for difference
    case2: as idrac_attr returns privilege in the format of string so
    convert payload to string only for comparision
    :return: bool
    """
    copy_json = json_payload.copy()
    for key, val in dict(copy_json).items():
        split_key = key.split("#")[1]
        if split_key == "Password":
            is_change_required = True
            break
        if split_key == "Privilege":
            copy_json[key] = str(val)
    else:
        is_change_required = bool(list(set(copy_json.items()) - set(idrac_attr.items())))
    return is_change_required


def get_user_account(module, idrac):
    """
    This function gets the slot id and slot uri for create and modify.
    :param module: ansible module arguments
    :param idrac: idrac objects
    :return: user_attr, slot_uri, slot_id, empty_slot, empty_slot_uri
    """
    slot_uri, slot_id, empty_slot, empty_slot_uri = None, None, None, None
    if not module.params["user_name"]:
        module.fail_json(msg="User name is not valid.")
    response = idrac.export_scp(export_format="JSON", export_use="Default", target="IDRAC", job_wait=True)
    user_attributes = idrac.get_idrac_local_account_attr(response.json_data, fqdd="iDRAC.Embedded.1")
    slot_num = tuple(range(2, 17))
    for num in slot_num:
        user_name = "Users.{0}#UserName".format(num)
        if user_attributes.get(user_name) == module.params["user_name"]:
            slot_id = num
            slot_uri = ACCOUNT_URI + str(num)
            break
        if not user_attributes.get(user_name) and (empty_slot_uri and empty_slot) is None:
            empty_slot = num
            empty_slot_uri = ACCOUNT_URI + str(num)
    return user_attributes, slot_uri, slot_id, empty_slot, empty_slot_uri


def get_payload(module, slot_id, action=None):
    """
    This function creates the payload with slot id.
    :param module: ansible module arguments
    :param action: new user name is only applicable in case of update user name.
    :param slot_id: slot id for user slot
    :return: json data with slot id
    """
    user_privilege = module.params["custom_privilege"] if "custom_privilege" in module.params and \
        module.params["custom_privilege"] is not None else USER_ROLES.get(module.params["privilege"])

    slot_payload = {"Users.{0}.UserName": module.params["user_name"],
                    "Users.{0}.Password": module.params["user_password"],
                    "Users.{0}.Enable": ACCESS.get(module.params["enable"]),
                    "Users.{0}.Privilege": user_privilege,
                    "Users.{0}.IpmiLanPrivilege": module.params["ipmi_lan_privilege"],
                    "Users.{0}.IpmiSerialPrivilege": module.params["ipmi_serial_privilege"],
                    "Users.{0}.SolEnable": ACCESS.get(module.params["sol_enable"]),
                    "Users.{0}.ProtocolEnable": ACCESS.get(module.params["protocol_enable"]),
                    "Users.{0}.AuthenticationProtocol": module.params["authentication_protocol"],
                    "Users.{0}.PrivacyProtocol": module.params["privacy_protocol"], }
    if module.params["new_user_name"] is not None and action == "update":
        user_name = "Users.{0}.UserName".format(slot_id)
        slot_payload[user_name] = module.params["new_user_name"]
    elif module.params["state"] == "absent":
        slot_payload = {"Users.{0}.UserName": "", "Users.{0}.Enable": "Disabled", "Users.{0}.Privilege": 0,
                        "Users.{0}.IpmiLanPrivilege": "No Access", "Users.{0}.IpmiSerialPrivilege": "No Access",
                        "Users.{0}.SolEnable": "Disabled", "Users.{0}.ProtocolEnable": "Disabled",
                        "Users.{0}.AuthenticationProtocol": "SHA", "Users.{0}.PrivacyProtocol": "AES"}
    payload = dict([(k.format(slot_id), v) for k, v in slot_payload.items() if v is not None])
    return payload


def convert_payload_xml(payload):
    """
    this function converts payload to xml and json data.
    :param payload: user input for payload
    :return: returns xml and json data
    """
    root = """<SystemConfiguration><Component FQDD="iDRAC.Embedded.1">{0}</Component></SystemConfiguration>"""
    attr = ""
    json_payload = {}
    for k, v in payload.items():
        key = re.sub(r"(?<=\d)\.", "#", k)
        attr += '<Attribute Name="{0}">{1}</Attribute>'.format(key, v)
        json_payload[key] = v
    root = root.format(attr)
    return root, json_payload


def create_or_modify_account(module, idrac, slot_uri, slot_id, empty_slot_id, empty_slot_uri, user_attr):
    """
    This function create user account in case not exists else update it.
    :param module: user account module arguments
    :param idrac: idrac object
    :param slot_uri: slot uri for update
    :param slot_id: slot id for update
    :param empty_slot_id: empty slot id for create
    :param empty_slot_uri: empty slot uri for create
    :return: json
    """
    generation, firmware_version = idrac.get_server_generation
    msg, response = "Unable to retrieve the user details.", {}
    if (slot_id and slot_uri) is None and (empty_slot_id and empty_slot_uri) is not None:
        msg = "Successfully created user account."
        payload = get_payload(module, empty_slot_id, action="create")
        if module.check_mode:
            module.exit_json(msg="Changes found to commit!", changed=True)
        if generation >= 14:
            response = idrac.invoke_request(ATTRIBUTE_URI, "PATCH", data={"Attributes": payload})
        elif generation < 14:
            xml_payload, json_payload = convert_payload_xml(payload)
            time.sleep(10)
            response = idrac.import_scp(import_buffer=xml_payload, target="ALL", job_wait=True)
    elif (slot_id and slot_uri) is not None:
        msg = "Successfully updated user account."
        payload = get_payload(module, slot_id, action="update")
        xml_payload, json_payload = convert_payload_xml(payload)
        value = compare_payload(json_payload, user_attr)
        if module.check_mode:
            if value:
                module.exit_json(msg="Changes found to commit!", changed=True)
            module.exit_json(msg="No changes found to commit!")
        if not value:
            module.exit_json(msg="Requested changes are already present in the user slot.")
        if generation >= 14:
            response = idrac.invoke_request(ATTRIBUTE_URI, "PATCH", data={"Attributes": payload})
        elif generation < 14:
            time.sleep(10)
            response = idrac.import_scp(import_buffer=xml_payload, target="ALL", job_wait=True)
    elif (slot_id and slot_uri and empty_slot_id and empty_slot_uri) is None:
        module.fail_json(msg="Maximum number of users reached. Delete a user account and retry the operation.")
    return response, msg


def remove_user_account(module, idrac, slot_uri, slot_id):
    """
    remove user user account by passing empty payload details.
    :param module: user account module arguments.
    :param idrac: idrac object.
    :param slot_uri: user slot uri.
    :param slot_id: user slot id.
    :return: json.
    """
    response, msg = {}, "Successfully deleted user account."
    payload = get_payload(module, slot_id, action="delete")
    xml_payload, json_payload = convert_payload_xml(payload)
    if module.check_mode and (slot_id and slot_uri) is not None:
        module.exit_json(msg="Changes found to commit!", changed=True)
    elif module.check_mode and (slot_uri and slot_id) is None:
        module.exit_json(msg="No changes found to commit!")
    elif not module.check_mode and (slot_uri and slot_id) is not None:
        time.sleep(10)
        response = idrac.import_scp(import_buffer=xml_payload, target="ALL", job_wait=True)
    else:
        module.exit_json(msg="The user account is absent.")
    return response, msg


def validate_input(module):
    if module.params["state"] == "present":
        user_privilege = module.params["custom_privilege"] if "custom_privilege" in module.params and \
            module.params["custom_privilege"] is not None else USER_ROLES.get(module.params["privilege"], 0)
        if INVALID_PRIVILAGE_MIN > user_privilege or user_privilege > INVALID_PRIVILAGE_MAX:
            module.fail_json(msg=INVALID_PRIVILAGE_MSG)


def main():
    specs = {
        "state": {"required": False, "choices": ['present', 'absent'], "default": "present"},
        "new_user_name": {"required": False},
        "user_name": {"required": True},
        "user_password": {"required": False, "no_log": True},
        "privilege": {"required": False, "choices": ['Administrator', 'ReadOnly', 'Operator', 'None']},
        "custom_privilege": {"required": False, "type": "int"},
        "ipmi_lan_privilege": {"required": False, "choices": ['Administrator', 'Operator', 'User', 'No Access']},
        "ipmi_serial_privilege": {"required": False, "choices": ['Administrator', 'Operator', 'User', 'No Access']},
        "enable": {"required": False, "type": "bool"},
        "sol_enable": {"required": False, "type": "bool"},
        "protocol_enable": {"required": False, "type": "bool"},
        "authentication_protocol": {"required": False, "choices": ['SHA', 'MD5', 'None']},
        "privacy_protocol": {"required": False, "choices": ['AES', 'DES', 'None']},
    }
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        supports_check_mode=True)
    try:
        validate_input(module)
        with iDRACRedfishAPI(module.params, req_session=True) as idrac:
            user_attr, slot_uri, slot_id, empty_slot_id, empty_slot_uri = get_user_account(module, idrac)
            if module.params["state"] == "present":
                response, message = create_or_modify_account(module, idrac, slot_uri, slot_id, empty_slot_id,
                                                             empty_slot_uri, user_attr)
            elif module.params["state"] == "absent":
                response, message = remove_user_account(module, idrac, slot_uri, slot_id)
            error = response.json_data.get("error")
            oem = response.json_data.get("Oem")
            if oem:
                oem_msg = oem.get("Dell").get("Message")
                error_msg = ["Unable to complete application of configuration profile values.",
                             "Import of Server Configuration Profile operation completed with errors."]
                if oem_msg in error_msg:
                    module.fail_json(msg=oem_msg, error_info=response.json_data)
            if error:
                module.fail_json(msg=error.get("message"), error_info=response.json_data)
            module.exit_json(msg=message, status=response.json_data, changed=True)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError, SSLError) as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
