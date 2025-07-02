#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.4
# Copyright (C) 2021-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
---
module: ome_active_directory
short_description: Configure Active Directory groups to be used with Directory Services
description: "This module allows to add, modify, and delete OpenManage Enterprise connection with Active Directory
Service."
version_added: "4.0.0"
author:
  - Jagadeesh N V(@jagadeeshnv)
  - Bhavneet Sharma (@Bhavneet-Sharma)
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  domain_server:
    type: list
    elements: str
    description:
      - Enter the domain name or FQDN or IP address of the domain controller.
      - If I(domain_controller_lookup) is C(DNS), enter the domain name to query DNS for the domain controllers.
      - "If I(domain_controller_lookup) is C(MANUAL), enter the FQDN or the IP address of the domain controller.
      The maximum number of Active Directory servers that can be added is three."
  domain_controller_lookup:
    type: str
    description:
      - Select the Domain Controller Lookup method.
    choices:
      - DNS
      - MANUAL
    default: DNS
  domain_controller_port:
    type: int
    description:
      - Domain controller port.
      - By default, Global Catalog Address port number 3269 is populated.
      - For the Domain Controller Access, enter 636 as the port number.
      - C(NOTE), Only LDAPS ports are supported.
    default: 3269
  group_domain:
    type: str
    description:
      - Provide the group domain in the format C(example.com) or C(ou=org, dc=example, dc=com).
  id:
    type: int
    description:
      - Provide the ID of the existing Active Directory service connection.
      - This is applicable for modification and deletion.
      - This is mutually exclusive with I(name).
  name:
    type: str
    description:
      - Provide a name for the Active Directory connection.
      - This is applicable for creation and deletion.
      - This is mutually exclusive with I(name).
  network_timeout:
    type: int
    description:
      - Enter the network timeout duration in seconds.
      - The supported timeout duration range is 15 to 300 seconds.
    default: 120
  search_timeout:
    type: int
    description:
      - Enter the search timeout duration in seconds.
      - The supported timeout duration range is 15 to 300 seconds.
    default: 120
  state:
    type: str
    description:
      - C(present) allows to create or modify an Active Directory service.
      - C(absent) allows to delete a Active Directory service.
    choices:
      - present
      - absent
    default: present
  test_connection:
    type: bool
    description:
      - Enables testing the connection to the domain controller.
      - The connection to the domain controller is tested with the provided Active Directory service details.
      - If test fails, module will error out.
      - If C(true), I(domain_username) and I(domain_password) has to be provided.
    default: false
  domain_password:
    type: str
    description:
      - Provide the domain password.
      - This is applicable when I(test_connection) is C(true).
  domain_username:
    type: str
    description:
      - Provide the domain username either in the UPN (username@domain) or NetBIOS (domain\\\\username) format.
      - This is applicable when I(test_connection) is C(true).
  validate_certificate:
    type: bool
    description:
      - Enables validation of SSL certificate of the domain controller.
      - The module will always report change when this is C(true).
    default: false
  certificate_file:
    type: path
    description:
      - Provide the full path of the SSL certificate.
      - The certificate should be a Root CA Certificate encoded in Base64 format.
      - This is applicable when I(validate_certificate) is C(true).
requirements:
  - "python >= 3.9.6"
notes:
  - The module will always report change when I(validate_certificate) is C(true).
  - Run this module from a system that has direct access to OpenManage Enterprise.
  - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Add Active Directory service using DNS lookup along with the test connection
  dellemc.openmanage.ome_active_directory:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    name: my_ad1
    domain_server:
      - domainname.com
    group_domain: domainname.com
    test_connection: true
    domain_username: user@domainname
    domain_password: domain_password

- name: Add Active Directory service using IP address of the domain controller with certificate validation
  dellemc.openmanage.ome_active_directory:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    name: my_ad2
    domain_controller_lookup: MANUAL
    domain_server:
      - 192.68.20.181
    group_domain: domainname.com
    validate_certificate: true
    certificate_file: "/path/to/certificate/file.cer"

- name: Modify domain controller IP address, network_timeout and group_domain
  dellemc.openmanage.ome_active_directory:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    name: my_ad2
    domain_controller_lookup: MANUAL
    domain_server:
      - 192.68.20.189
    group_domain: newdomain.in
    network_timeout: 150

- name: Delete Active Directory service
  dellemc.openmanage.ome_active_directory:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    name: my_ad2
    state: absent

- name: Test connection to existing Active Directory service with certificate validation
  dellemc.openmanage.ome_active_directory:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    name: my_ad2
    test_connection: true
    domain_username: user@domainname
    domain_password: domain_password
    validate_certificate: true
    certificate_file: "/path/to/certificate/file.cer"
"""

RETURN = """
---
msg:
  type: str
  description: Overall status of the Active Directory operation.
  returned: always
  sample: "Successfully renamed the slot(s)."
active_directory:
  type: dict
  description: The Active Directory that was added, modified or deleted by this module.
  returned: on change
  sample: {
    "Name": "ad_test",
    "Id": 21789,
    "ServerType": "MANUAL",
    "ServerName": ["192.168.20.181"],
    "DnsServer": [],
    "GroupDomain": "dellemcdomain.com",
    "NetworkTimeOut": 120,
    "Password": null,
    "SearchTimeOut": 120,
    "ServerPort": 3269,
    "CertificateValidation": false
  }
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
     "error_info": {
        "error": {
            "@Message.ExtendedInfo": [
                {
                    "Message": "Unable to connect to the LDAP or AD server because the entered credentials are invalid.",
                    "MessageArgs": [],
                    "MessageId": "CSEC5002",
                    "RelatedProperties": [],
                    "Resolution": "Make sure the server input configuration are valid and retry the operation.",
                    "Severity": "Critical"
                }
            ],
            "code": "Base.1.0.GeneralError",
            "message": "A general error has occurred. See ExtendedInfo for more information."
        }
     }
  }
"""

import json
import os
from ssl import SSLError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible.module_utils.common.dict_transformations import recursive_diff

AD_URI = "AccountService/ExternalAccountProvider/ADAccountProvider"
TEST_CONNECTION = "AccountService/ExternalAccountProvider/Actions/ExternalAccountProvider.TestADConnection"
DELETE_AD = "AccountService/ExternalAccountProvider/Actions/ExternalAccountProvider.DeleteExternalAccountProvider"
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
MAX_AD_MSG = "Unable to add the account provider because the maximum number of configurations allowed for an" \
             " Active Directory service is {0}."
CREATE_SUCCESS = "Successfully added the Active Directory service."
MODIFY_SUCCESS = "Successfully modified the Active Directory service."
DELETE_SUCCESS = "Successfully deleted the Active Directory service."
DOM_SERVER_MSG = "Specify the domain server. Domain server is required to create an Active Directory service."
GRP_DOM_MSG = "Specify the group domain. Group domain is required to create an Active Directory service."
CERT_INVALID = "The provided certificate file path is invalid or not readable."
DOMAIN_ALLOWED_COUNT = "Maximum entries allowed for {0} lookup type is {1}."
TEST_CONNECTION_SUCCESS = "Test Connection is successful. "
TEST_CONNECTION_FAIL = "Test Connection has failed. "
ERR_READ_FAIL = "Unable to retrieve the error details."
INVALID_ID = "The provided Active Directory ID is invalid."
TIMEOUT_RANGE = "The {0} value is not in the range of {1} to {2}."
MAX_AD = 2
MIN_TIMEOUT = 15
MAX_TIMEOUT = 300


def get_ad(module, rest_obj):
    ad = {}
    prm = module.params
    resp = rest_obj.invoke_request('GET', AD_URI)
    ad_list = resp.json_data.get('value')
    ad_cnt = len(ad_list)
    ky = 'Name'
    vl = 'name'
    if prm.get('id'):
        ky = 'Id'
        vl = 'id'
    for adx in ad_list:
        if str(adx.get(ky)).lower() == str(prm.get(vl)).lower():
            ad = adx
            break
    return ad, ad_cnt


def test_http_error_fail(module, err):
    try:
        error_info = json.load(err)
        err_list = error_info.get('error', {}).get('@Message.ExtendedInfo',
                                                   [ERR_READ_FAIL])
        if err_list:
            err_rsn = err_list[0].get("Message")
    except Exception:
        err_rsn = ERR_READ_FAIL
    module.exit_json(msg="{0}{1}".format(TEST_CONNECTION_FAIL, err_rsn),
                     error_info=error_info, failed=True)


def test_connection(module, rest_obj, create_payload):
    try:
        create_payload['UserName'] = module.params.get('domain_username')
        create_payload['Password'] = module.params.get('domain_password')
        rest_obj.invoke_request('POST', TEST_CONNECTION, data=create_payload,
                                api_timeout=create_payload['NetworkTimeOut'])
        create_payload.pop('UserName', None)
        create_payload.pop('Password', None)
    except HTTPError as err:
        test_http_error_fail(module, err)
    except SSLError as err:
        module.exit_json(msg="{0}{1}".format(TEST_CONNECTION_FAIL, str(err)),
                         failed=True)
    except Exception as err:
        module.exit_json(msg="{0}{1}".format(TEST_CONNECTION_FAIL, str(err)),
                         failed=True)


def make_payload(prm):
    dc_type = {'DNS': 'DnsServer', 'MANUAL': 'ServerName'}
    tmplt_ad = {'name': 'Name', 'domain_controller_port': 'ServerPort', 'domain_controller_lookup': 'ServerType',
                'domain_server': dc_type[prm.get('domain_controller_lookup')], 'group_domain': 'GroupDomain',
                'network_timeout': 'NetworkTimeOut', 'search_timeout': 'SearchTimeOut',
                'validate_certificate': 'CertificateValidation'}
    payload = dict([(v, prm.get(k)) for k, v in tmplt_ad.items() if prm.get(k) is not None])
    return payload


def validate_n_testconnection(module, rest_obj, payload):
    dc_cnt = {'DNS': 1, 'MANUAL': 3}
    dc_type = {'DNS': 'DnsServer', 'MANUAL': 'ServerName'}
    dc_lookup = payload.get('ServerType')
    if len(payload.get(dc_type[dc_lookup])) > dc_cnt[dc_lookup]:
        module.exit_json(msg=DOMAIN_ALLOWED_COUNT.format(
            dc_lookup, dc_cnt[dc_lookup]), failed=True)
    t_list = ['NetworkTimeOut', 'SearchTimeOut']
    for tx in t_list:
        if payload.get(tx) not in range(MIN_TIMEOUT, MAX_TIMEOUT + 1):
            module.exit_json(msg=TIMEOUT_RANGE.format(
                tx, MIN_TIMEOUT, MAX_TIMEOUT), failed=True)
    payload['CertificateFile'] = ""
    if payload.get('CertificateValidation'):
        cert_path = module.params.get('certificate_file')
        if os.path.exists(cert_path):
            with open(cert_path, 'r') as certfile:
                cert_data = certfile.read()
                payload['CertificateFile'] = cert_data
        else:
            module.exit_json(msg=CERT_INVALID, failed=True)
    msg = ""
    if module.params.get('test_connection'):
        test_connection(module, rest_obj, payload)
        msg = TEST_CONNECTION_SUCCESS
    return msg


def create_ad(module, rest_obj):
    prm = module.params
    if not prm.get('domain_server'):
        module.exit_json(msg=DOM_SERVER_MSG, failed=True)
    if not prm.get('group_domain'):
        module.exit_json(msg=GRP_DOM_MSG, failed=True)
    create_payload = make_payload(prm)
    msg = validate_n_testconnection(module, rest_obj, create_payload)
    if module.check_mode:
        module.exit_json(msg="{0}{1}".format(msg, CHANGES_FOUND), changed=True)
    resp = rest_obj.invoke_request('POST', AD_URI, data=create_payload)
    ad = resp.json_data
    ad.pop('CertificateFile', "")
    module.exit_json(msg="{0}{1}".format(msg, CREATE_SUCCESS), active_directory=ad, changed=True)


def modify_ad(module, rest_obj, ad):
    prm = module.params
    modify_payload = make_payload(prm)
    ad = rest_obj.strip_substr_dict(ad)
    if ad.get('ServerName'):
        (ad.get('ServerName')).sort()
    if modify_payload.get('ServerName'):
        (modify_payload.get('ServerName')).sort()
    diff = recursive_diff(modify_payload, ad)
    is_change = False
    if diff and diff[0]:
        is_change = True
        ad.update(modify_payload)
    msg = validate_n_testconnection(module, rest_obj, ad)
    if not is_change and not ad.get('CertificateValidation'):
        module.exit_json(msg="{0}{1}".format(msg, NO_CHANGES_MSG), active_directory=ad)
    if module.check_mode:
        module.exit_json(msg="{0}{1}".format(msg, CHANGES_FOUND), changed=True)
    resp = rest_obj.invoke_request('PUT', "{0}({1})".format(AD_URI, ad['Id']), data=ad)
    ad = resp.json_data
    ad.pop('CertificateFile', "")
    module.exit_json(msg="{0}{1}".format(msg, MODIFY_SUCCESS), active_directory=ad, changed=True)


def delete_ad(module, rest_obj, ad):
    ad = rest_obj.strip_substr_dict(ad)
    if module.check_mode:
        module.exit_json(msg=CHANGES_FOUND, active_directory=ad, changed=True)
    rest_obj.invoke_request('POST', DELETE_AD, data={"AccountProviderIds": [int(ad['Id'])]})
    module.exit_json(msg=DELETE_SUCCESS, active_directory=ad, changed=True)


def _go_for_create_modify(module, rest_obj, ad, ad_cnt):
    if ad:
        modify_ad(module, rest_obj, ad)
    else:
        if module.params.get('id'):
            module.exit_json(msg=INVALID_ID, failed=True)
        if ad_cnt < MAX_AD:
            create_ad(module, rest_obj)
        module.exit_json(msg=MAX_AD_MSG.format(MAX_AD), failed=True)


def main():
    specs = {
        "state": {"type": 'str', "choices": ["present", "absent"], "default": 'present'},
        "name": {"type": 'str'},
        "id": {"type": 'int'},
        "domain_controller_lookup": {"type": 'str', "choices": ['MANUAL', 'DNS'], "default": 'DNS'},
        "domain_server": {"type": 'list', "elements": 'str'},
        "group_domain": {"type": 'str'},
        "domain_controller_port": {"type": 'int', "default": 3269},
        "network_timeout": {"type": 'int', "default": 120},
        "search_timeout": {"type": 'int', "default": 120},
        "validate_certificate": {"type": 'bool', "default": False},
        "certificate_file": {"type": 'path'},
        "test_connection": {"type": 'bool', "default": False},
        "domain_username": {"type": 'str'},
        "domain_password": {"type": 'str', "no_log": True}
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        required_one_of=[('name', 'id')],
        required_if=[
            ('test_connection', True, ('domain_username', 'domain_password',)),
            ('validate_certificate', True, ('certificate_file',))],
        mutually_exclusive=[('name', 'id')],
        supports_check_mode=True)
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            ad, ad_cnt = get_ad(module, rest_obj)
            if module.params.get('state') == 'present':
                _go_for_create_modify(module, rest_obj, ad, ad_cnt)
            else:
                if ad:
                    delete_ad(module, rest_obj, ad)
                module.exit_json(msg=NO_CHANGES_MSG)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True, failed=True)
    except (
            IOError, ValueError, TypeError, ConnectionError, AttributeError, IndexError, KeyError,
            OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
