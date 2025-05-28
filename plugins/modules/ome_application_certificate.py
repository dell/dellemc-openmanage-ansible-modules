#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.6.0
# Copyright (C) 2020-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

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
    description:
      - C(generate_csr) allows the generation of a CSR.
      - C(upload) uploads the certificate on OpenManage Enterprise.
      - C(upload_cert_chain) uploads the certificate chain on OpenManage Enterprise.
    type: str
    default: generate_csr
    choices: [generate_csr, upload, upload_cert_chain]
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
  subject_alternative_names:
    description:
      - Subject alternative name required for the certificate signing request generation.
      - Supports up to 4 comma separated values starting from primary, secondary, Tertiary and Quaternary values.
    type: str
    version_added: 8.1.0
  upload_file:
    type: str
    description: Local path of the certificate file to be uploaded. This option is applicable for C(upload) and C(upload_cert_chain).
      Once the certificate is uploaded, OpenManage Enterprise cannot be accessed for a few seconds. The formats of the certificate
      file are .crt, .cer, .ca-bundle, .p7b, .der, and .pem.
requirements:
    - "python >= 3.9.6"
author:
  - "Felix Stephen (@felixs88)"
  - "Kritika Bhateja (@Kritika-Bhateja-03)"
  - "Jennifer John (@Jennifer-John)"
  - "Abhishek Sinha (@ABHISHEK-SINHA10)"
  - "Saksham Nautiyal (@Saksham-Nautiyal)"
'''

EXAMPLES = r'''
---
- name: Generate a certificate signing request
  dellemc.openmanage.ome_application_certificate:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: "generate_csr"
    distinguished_name: "hostname.com"
    department_name: "Remote Access Group"
    business_name: "Dell Inc."
    locality: "Round Rock"
    country_state: "Texas"
    country: "US"
    email: "support@dell.com"

- name: Generate a certificate signing request with subject alternative names
  dellemc.openmanage.ome_application_certificate:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: "generate_csr"
    distinguished_name: "hostname.com"
    subject_alternative_names: "hostname1.chassis.com,hostname2.chassis.com"
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
    ca_path: "/path/to/ca_cert.pem"
    command: "upload"
    upload_file: "/path/certificate.cer"

- name: Upload the certificate chain
  dellemc.openmanage.ome_application_certificate:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    command: "upload_cert_chain"
    upload_file: "/path/certificate_chain.p7b"
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
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import get_ome_version
from urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.compat.version import LooseVersion

UNSUPPORTED_OME = "This operation is not supported on OpenManage Enterprise version {ome_version}"
CERT_SIGN = "Successfully generated certificate signing request."
CERT_UPLOAD = "Successfully uploaded application certificate."


def generate_csr_payload(module):
    return {
        "DistinguishedName": module.params["distinguished_name"],
        "DepartmentName": module.params["department_name"],
        "BusinessName": module.params["business_name"],
        "Locality": module.params["locality"],
        "State": module.params["country_state"],
        "Country": module.params["country"],
        "Email": module.params["email"],
        "San": get_san(module.params["subject_alternative_names"])
    }


def read_file_payload(module):
    file_path = module.params["upload_file"]
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            return file.read()
    else:
        module.fail_json(msg="No such file or directory.")


def get_resource_parameters(module):
    command = module.params["command"]
    csr_uri = "ApplicationService/Actions/ApplicationService.{0}"
    method = "POST"
    payload = None

    # Mapping of command to their respective actions
    command_map = {
        "generate_csr": {
            "uri": csr_uri.format("GenerateCSR"),
            "payload_func": generate_csr_payload
        },
        "upload": {
            "uri": csr_uri.format("UploadCertificate"),
            "payload_func": read_file_payload
        },
        "upload_cert_chain": {
            "uri": csr_uri.format("UploadCertChain"),
            "payload_func": read_file_payload
        }
    }

    command_details = command_map.get(command)
    if not command_details:
        module.fail_json(msg=f"Unknown command: {command}")

    uri = command_details["uri"]
    payload = command_details["payload_func"](module)

    return method, uri, payload


def read_file(module):
    """Reads the file content for 'upload' and 'upload_cert_chain' commands."""
    file_path = module.params["upload_file"]
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            return file.read()
    else:
        module.fail_json(msg="No such file or directory.")


def get_san(subject_alternative_names):
    if not subject_alternative_names:
        return subject_alternative_names
    return subject_alternative_names.replace(" ", "")


def format_csr_string(csr_string):
    # Remove the header and footer
    csr_string = csr_string.replace("-----BEGIN CERTIFICATE REQUEST-----", "")
    csr_string = csr_string.replace("-----END CERTIFICATE REQUEST-----", "")
    csr_string = csr_string.replace("\n", "")

    # Format the remaining string with proper line breaks
    formatted_csr = '\n'.join([csr_string[i:i + 64] for i in range(0, len(csr_string), 64)])

    # Add the header and footer back
    formatted_csr = "-----BEGIN CERTIFICATE REQUEST-----\n" + formatted_csr + "\n-----END CERTIFICATE REQUEST-----"

    return formatted_csr


def main():
    specs = {
        "command": {"type": "str", "required": False,
                    "choices": ["generate_csr", "upload", "upload_cert_chain"], "default": "generate_csr"},
        "distinguished_name": {"required": False, "type": "str"},
        "department_name": {"required": False, "type": "str"},
        "business_name": {"required": False, "type": "str"},
        "locality": {"required": False, "type": "str"},
        "country_state": {"required": False, "type": "str"},
        "country": {"required": False, "type": "str"},
        "email": {"required": False, "type": "str"},
        "subject_alternative_names": {"required": False, "type": "str"},
        "upload_file": {"required": False, "type": "str"}
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        required_if=[["command", "generate_csr", ["distinguished_name", "department_name",
                                                  "business_name", "locality", "country_state",
                                                  "country", "email"]],
                     ["command", "upload", ["upload_file"]],
                     ["command", "upload_cert_chain", ["upload_file"]]],
        supports_check_mode=False
    )

    header = {"Content-Type": "application/octet-stream", "Accept": "application/octet-stream"}
    try:
        with RestOME(module.params, req_session=False) as rest_obj:
            command = module.params.get("command")
            if command == "upload_cert_chain":
                ome_version = get_ome_version(rest_obj)
                if LooseVersion(ome_version) < "3.10":
                    module.exit_json(msg=UNSUPPORTED_OME.format(ome_version=ome_version), skipped=True)

            method, uri, payload = get_resource_parameters(module)
            dump = False if command in ["upload", "upload_cert_chain"] else True
            headers = header if command in ["upload", "upload_cert_chain"] else None
            resp = rest_obj.invoke_request(method, uri, headers=headers, data=payload, dump=dump)
            if resp.success:
                if command == "generate_csr":
                    resp_copy = resp.json_data
                    formatted_csr = format_csr_string(resp_copy["CertificateData"])
                    resp_copy["CertificateData"] = formatted_csr
                    module.exit_json(msg=CERT_SIGN,
                                     csr_status=resp_copy)
                else:
                    module.exit_json(msg=CERT_UPLOAD, changed=True)
            else:
                module.fail_json(msg="Request failed", error_info=resp.json_data)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, TypeError, ConnectionError, SSLValidationError, OSError) as err:
        module.fail_json(msg=str(err))
    except Exception as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
