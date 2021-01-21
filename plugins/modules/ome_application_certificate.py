#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.0.0
# Copyright (C) 2020-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_application_certificate
short_description: This module allows to generate a CSR and upload the certificate
version_added: "2.1.0"
description:
  - This module allows the generation a new certificate signing request (CSR) and to upload the certificate
    on OpenManage Enterprise.
notes:
  - If a certificate is uploaded, which is identical to an already existing certificate, it is accepted by the module.
  - This module does not support C(check_mode).
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
  command:
    description: C(generate_csr) allows the generation of a CSR and C(upload) uploads the certificate.
    type: str
    default: generate_csr
    choices: [generate_csr, upload]
  distinguished_name:
    description: Name of the certificate issuer. This option is applicable for C(generate_csr).
    type: str
  department_name:
    description: Name of the department that issued the certificate. This option is applicable for C(generate_csr).
    type: str
  business_name:
    description: Name of the business that issued the certificate. This option is applicable for C(generate_csr).
    type: str
  locality:
    description: Local address of the issuer of the certificate. This option is applicable for C(generate_csr).
    type: str
  country_state:
    description: State in which the issuer resides. This option is applicable for C(generate_csr).
    type: str
  country:
    description: Country in which the issuer resides. This option is applicable for C(generate_csr).
    type: str
  email:
    description: Email associated with the issuer. This option is applicable for C(generate_csr).
    type: str
  upload_file:
    type: str
    description: Local path of the certificate file to be uploaded. This option is applicable for C(upload).
        Once the certificate is uploaded, OpenManage Enterprise cannot be accessed for a few seconds.
requirements:
    - "python >= 2.7.5"
author: "Felix Stephen (@felixs88)"
'''

EXAMPLES = r'''
---
- name: Generate a certificate signing request
  dellemc.openmanage.ome_application_certificate:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    command: "generate_csr"
    distinguished_name: "hostname.com"
    department_name: "Remote Access Group"
    business_name: "Dell Inc."
    locality: "Round Rock"
    country_state: "Texas"
    country: "US"
    email: "support@dell.com"

- name: Upload the certificate
  dellemc.openmanage.ome_application_certificate:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    command: "upload"
    upload_file: "/path/certificate.cer"
'''

RETURN = r'''
---
msg:
  type: str
  description: Overall status of the certificate signing request.
  returned: always
  sample: "Successfully generated certificate signing request."
csr_status:
  type: dict
  description: Details of the generated certificate.
  returned: on success
  sample:
    {"CertificateData": "-----BEGIN CERTIFICATE REQUEST-----GHFSUEKLELE
      af3u4h2rkdkfjasczjfefhkrr/frjrfrjfrxnvzklf/nbcvxmzvndlskmcvbmzkdk
      kafhaksksvklhfdjtrhhffgeth/tashdrfstkm@kdjFGD/sdlefrujjfvvsfeikdf
      yeufghdkatbavfdomehtdnske/tahndfavdtdfgeikjlagmdfbandfvfcrfgdtwxc
      qwgfrteyupojmnsbajdkdbfs/ujdfgthedsygtamnsuhakmanfuarweyuiwruefjr
      etwuwurefefgfgurkjkdmbvfmvfvfk==-----END CERTIFICATE REQUEST-----"
    }
error_info:
  description: Details of the HTTP error.
  returned: on HTTP error
  type: dict
  sample:
    {
        "error": {
            "code": "Base.1.0.GeneralError",
            "message": "A general error has occurred. See ExtendedInfo for more information.",
            "@Message.ExtendedInfo": [
                {
                    "MessageId": "CSEC9002",
                    "RelatedProperties": [],
                    "Message": "Unable to upload the certificate because the certificate file provided is invalid.",
                    "MessageArgs": [],
                    "Severity": "Critical",
                    "Resolution": "Make sure the CA certificate and private key are correct and retry the operation."
                }
            ]
        }
    }
'''

import json
import os
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


def get_resource_parameters(module):
    command = module.params["command"]
    csr_uri = "ApplicationService/Actions/ApplicationService.{0}"
    method = "POST"
    if command == "generate_csr":
        uri = csr_uri.format("GenerateCSR")
        payload = {"DistinguishedName": module.params["distinguished_name"],
                   "DepartmentName": module.params["department_name"],
                   "BusinessName": module.params["business_name"],
                   "Locality": module.params["locality"], "State": module.params["country_state"],
                   "Country": module.params["country"], "Email": module.params["email"]}
    else:
        file_path = module.params["upload_file"]
        uri = csr_uri.format("UploadCertificate")
        if os.path.exists(file_path):
            with open(file_path, 'rb') as payload:
                payload = payload.read()
        else:
            module.fail_json(msg="No such file or directory.")
    return method, uri, payload


def main():
    module = AnsibleModule(
        argument_spec={
            "hostname": {"required": True, "type": "str"},
            "username": {"required": True, "type": "str"},
            "password": {"required": True, "type": "str", "no_log": True},
            "port": {"required": False, "type": "int", "default": 443},
            "command": {"type": "str", "required": False,
                        "choices": ["generate_csr", "upload"], "default": "generate_csr"},
            "distinguished_name": {"required": False, "type": "str"},
            "department_name": {"required": False, "type": "str"},
            "business_name": {"required": False, "type": "str"},
            "locality": {"required": False, "type": "str"},
            "country_state": {"required": False, "type": "str"},
            "country": {"required": False, "type": "str"},
            "email": {"required": False, "type": "str"},
            "upload_file": {"required": False, "type": "str"},
        },
        required_if=[["command", "generate_csr", ["distinguished_name", "department_name",
                                                  "business_name", "locality", "country_state",
                                                  "country", "email"]],
                     ["command", "upload", ["upload_file"]]],
        supports_check_mode=False
    )
    header = {"Content-Type": "application/octet-stream", "Accept": "application/octet-stream"}
    try:
        with RestOME(module.params, req_session=False) as rest_obj:
            method, uri, payload = get_resource_parameters(module)
            command = module.params.get("command")
            dump = False if command == "upload" else True
            headers = header if command == "upload" else None
            resp = rest_obj.invoke_request(method, uri, headers=headers, data=payload, dump=dump)
            if resp.success:
                if command == "generate_csr":
                    module.exit_json(msg="Successfully generated certificate signing request.",
                                     csr_status=resp.json_data)
                module.exit_json(msg="Successfully uploaded application certificate.", changed=True)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, SSLError, TypeError, ConnectionError, SSLValidationError) as err:
        module.fail_json(msg=str(err))
    except Exception as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
