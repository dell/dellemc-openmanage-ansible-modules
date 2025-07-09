#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.10.0
# Copyright (C) 2022-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: idrac_certificates
short_description: Configure certificates for iDRAC
version_added: "5.5.0"
description:
  - This module allows to generate certificate signing request, import, and export certificates on iDRAC.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_x_auth_options
options:
  command:
    description:
      - "C(generate_csr), generate CSR. This requires I(cert_params) and I(certificate_path).
      This is applicable only for C(HTTPS)"
      - C(import), import the certificate file. This requires I(certificate_path).
      - C(export), export the certificate. This requires I(certificate_path).
      - C(reset), reset the certificate to default settings. This is applicable only for C(HTTPS).
    type: str
    choices: [import, export, generate_csr, reset]
    default: 'generate_csr'
  certificate_type:
    description:
      - Type of the iDRAC certificate.
      - C(HTTPS) The Dell self-signed SSL certificate.
      - C(CA) Certificate Authority(CA) signed SSL certificate.
      - C(CUSTOMCERTIFICATE) The custom PKCS12 certificate and private key. Export of custom certificate is supported only on iDRAC firmware version 7.00.00.00
        and above.
      - C(CSC) The custom signing SSL certificate.
      - C(CLIENT_TRUST_CERTIFICATE) Client trust certificate.
    type: str
    choices: [HTTPS, CA, CUSTOMCERTIFICATE, CSC, CLIENT_TRUST_CERTIFICATE]
    default: 'HTTPS'
  certificate_path:
    description:
      - Absolute path of the certificate file if I(command) is C(import).
      - Directory path with write permissions if I(command) is C(generate_csr) or C(export).
    type: path
  passphrase:
    description: The passphrase string if the certificate to be imported is passphrase protected.
    type: str
  ssl_key:
    description:
    - Absolute path of the private or SSL key file.
    - This is applicable only when I(command) is C(import) and I(certificate_type) is C(HTTPS).
    - Uploading the SSL key to iDRAC is supported on firmware version 6.00.02.00 and above.
    type: path
    version_added: 8.6.0
  cert_params:
    description: Certificate parameters to generate signing request.
    type: dict
    suboptions:
      common_name:
        description: The common name of the certificate.
        type: str
        required: true
      organization_unit:
        description: The name associated with an organizational unit. For example department name.
        type: str
        required: true
      locality_name:
        description: The city or other location where the entity applying for certification is located.
        type: str
        required: true
      state_name:
        description: The state where the entity applying for certification is located.
        type: str
        required: true
      country_code:
        description: The country code of the country where the entity applying for certification is located.
        type: str
        required: true
      email_address:
        description: The email associated with the CSR.
        type: str
      organization_name:
        description: The name associated with an organization.
        type: str
        required: true
      subject_alt_name:
        description: The alternative domain names associated with the request.
        type: list
        elements: str
        default: []
  resource_id:
    description: Redfish ID of the resource.
    type: str
  reset:
    description:
      - To reset the iDRAC after the certificate operation.
      - This is applicable when I(command) is C(import) or C(reset).
    type: bool
    default: true
  wait:
    description:
      - Maximum wait time for iDRAC to start after the reset, in seconds.
      - This is applicable when I(command) is C(import) or C(reset) and I(reset) is C(true).
    type: int
    default: 600
requirements:
  - "python >= 3.9.6"
author:
  - "Jagadeesh N V(@jagadeeshnv)"
  - "Rajshekar P(@rajshekarp87)"
  - "Kristian Lamb V(@kristian_lamb)"
notes:
    - The certificate operations are supported on iDRAC firmware version 6.10.80.00 and above.
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports C(check_mode).
    - This module supports IPv4 and IPv6 addresses.
"""

EXAMPLES = r"""
---
- name: Generate HTTPS certificate signing request
  dellemc.openmanage.idrac_certificates:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "generate_csr"
    certificate_type: "HTTPS"
    certificate_path: "/home/omam/mycerts"
    cert_params:
      common_name: "sample.domain.com"
      organization_unit: "OrgUnit"
      locality_name: "Bangalore"
      state_name: "Karnataka"
      country_code: "IN"
      email_address: "admin@domain.com"
      organization_name: "OrgName"
      subject_alt_name:
        - 192.198.2.1

- name: Import a HTTPS certificate.
  dellemc.openmanage.idrac_certificates:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "import"
    certificate_type: "HTTPS"
    certificate_path: "/path/to/cert.pem"

- name: Import an HTTPS certificate along with its private key.
  dellemc.openmanage.idrac_certificates:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "import"
    certificate_type: "HTTPS"
    certificate_path: "/path/to/cert.pem"
    ssl_key: "/path/to/private_key.pem"

- name: Export a HTTPS certificate.
  dellemc.openmanage.idrac_certificates:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "export"
    certificate_type: "HTTPS"
    certificate_path: "/home/omam/mycert_dir"

- name: Import a CSC certificate.
  dellemc.openmanage.idrac_certificates:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "import"
    certificate_type: "CSC"
    certificate_path: "/path/to/cert.pem"

- name: Import a custom certificate with a passphrase.
  dellemc.openmanage.idrac_certificates:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    command: "import"
    certificate_type: "CUSTOMCERTIFICATE"
    certificate_path: "/path/to/idrac_cert.p12"
    passphrase: "cert_passphrase"
    reset: false

- name: Export a Client trust certificate.
  dellemc.openmanage.idrac_certificates:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "export"
    certificate_type: "CLIENT_TRUST_CERTIFICATE"
    certificate_path: "/home/omam/mycert_dir"
"""

RETURN = r'''
---
msg:
  type: str
  description: Status of the certificate configuration operation.
  returned: always
  sample: "Successfully performed the 'generate_csr' certificate operation."
certificate_path:
  type: str
  description: The csr or exported certificate file path
  returned: when I(command) is C(export) or C(generate_csr)
  sample: "/home/ansible/myfiles/cert.pem"
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
import time
import base64
import os
from datetime import datetime
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, IdracAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import reset_idrac

IMPORT_SSL_CERTIFICATE = "#DelliDRACCardService.ImportSSLCertificate"
EXPORT_SSL_CERTIFICATE = "#DelliDRACCardService.ExportSSLCertificate"
IDRAC_CARD_SERVICE_ACTION_URI = "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions"

NOT_SUPPORTED_ACTION = "Certificate '{operation}' not supported for the specified certificate type '{cert_type}'."
SUCCESS_MSG = "Successfully performed the '{command}' certificate operation."
SUCCESS_MSG_SSL = "Successfully performed the SSL key upload and '{command}' certificate operation."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_MSG = "Changes found to be applied."
WAIT_NEGATIVE_OR_ZERO_MSG = "The value for the `wait` parameter cannot be negative or zero."
SYSTEM_ID = "System.Embedded.1"
MANAGER_ID = "iDRAC.Embedded.1"
ACTIONS_PFIX = f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService."
SYSTEMS_URI = "/redfish/v1/Systems"
MANAGERS_URI = "/redfish/v1/Managers"
IDRAC_SERVICE = "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService"
CSR_SSL = "/redfish/v1/CertificateService/Actions/CertificateService.GenerateCSR"
IMPORT_SSL = f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.ImportSSLCertificate"
UPLOAD_SSL = f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.UploadSSLKey"
EXPORT_SSL = f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.ExportSSLCertificate"
RESET_SSL = f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.SSLResetCfg"
IDRAC_RESET = "/redfish/v1/Managers/{res_id}/Actions/Manager.Reset"
GET_LAST_GENERATED_CSR = "/redfish/v1/CertificateService/Actions/Oem/DellCertificateService.GetLastGeneratedCSR"
CERT_STATUS = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/iDRAC.Embedded.1?$select=Security.1.ConfigCertStatus"

idrac_service_actions = {
    "#DelliDRACCardService.DeleteCertificate": f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.DeleteCertificate",
    "#DelliDRACCardService.ExportCertificate": f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.ExportCertificate",
    EXPORT_SSL_CERTIFICATE: EXPORT_SSL,
    "#DelliDRACCardService.FactoryIdentityCertificateGenerateCSR":
        f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.FactoryIdentityCertificateGenerateCSR",
    "#DelliDRACCardService.FactoryIdentityExportCertificate":
        f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.FactoryIdentityExportCertificate",
    "#DelliDRACCardService.FactoryIdentityImportCertificate":
        f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.FactoryIdentityImportCertificate",
    "#DelliDRACCardService.GenerateSEKMCSR": f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.GenerateSEKMCSR",
    "#DelliDRACCardService.ImportCertificate": f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.ImportCertificate",
    IMPORT_SSL_CERTIFICATE: IMPORT_SSL,
    "#DelliDRACCardService.UploadSSLKey": UPLOAD_SSL,
    "#DelliDRACCardService.SSLResetCfg": f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.SSLResetCfg",
    "#DelliDRACCardService.iDRACReset": f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.iDRACReset"
}

rfish_cert_coll = {'Server': {
    "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/NetworkProtocol/HTTPS/Certificates"
}}
out_file_path = {"CSRString": 'certificate_path',
                 "CertificateFile": 'certificate_path'}
changed_map = {"generate_csr": False, "import": True, "export": False, "reset": True}
# reset_map = {"generate_csr": False, "import": True, "export": False, "reset": True}
csr_transform = {"common_name": "CommonName",
                 "organization_unit": "OrganizationalUnit",
                 "locality_name": 'City',
                 "state_name": 'State',
                 "country_code": "Country",
                 "email_address": 'Email',
                 "organization_name": "Organization",
                 "subject_alt_name": 'AlternativeNames'}
action_url_map = {"generate_csr": {},
                  "import": {'Server': IMPORT_SSL_CERTIFICATE,
                             'CA': IMPORT_SSL_CERTIFICATE,
                             'CustomCertificate': IMPORT_SSL_CERTIFICATE,
                             'CSC': IMPORT_SSL_CERTIFICATE,
                             'ClientTrustCertificate': IMPORT_SSL_CERTIFICATE},
                  "export": {'Server': EXPORT_SSL_CERTIFICATE,
                             'CA': EXPORT_SSL_CERTIFICATE,
                             'CustomCertificate': EXPORT_SSL_CERTIFICATE,
                             'CSC': EXPORT_SSL_CERTIFICATE,
                             'ClientTrustCertificate': EXPORT_SSL_CERTIFICATE},
                  "reset": {'Server': "#DelliDRACCardService.SSLResetCfg"}}

dflt_url_map = {"generate_csr": {'Server': CSR_SSL},
                "import": {'Server': IMPORT_SSL,
                           'CA': IMPORT_SSL,
                           'CUSTOMCERTIFICATE': IMPORT_SSL,
                           'CSC': IMPORT_SSL,
                           'ClientTrustCertificate': IMPORT_SSL},
                "export": {'Server': EXPORT_SSL,
                           'CA': EXPORT_SSL,
                           'CUSTOMCERTIFICATE': EXPORT_SSL,
                           'CSC': EXPORT_SSL,
                           'ClientTrustCertificate': EXPORT_SSL},
                "reset": {'Server': RESET_SSL}}
certype_map = {'HTTPS': "Server", 'CA': "CA", 'CUSTOMCERTIFICATE': "CustomCertificate", 'CSC': "CSC",
               'CLIENT_TRUST_CERTIFICATE': "ClientTrustCertificate"}


def get_ssl_payload(module, operation, cert_type):
    payload = {}
    method = 'POST'

    if operation == 'import':
        payload = _build_import_payload(module, cert_type)
    elif operation == 'export':
        payload = {"SSLCertType": cert_type}
    elif operation == 'generate_csr':
        payload = _build_generate_csr_payload(module, cert_type)
    elif operation == 'reset':
        payload = '{}'

    return payload, method


def _build_import_payload(module, cert_type):
    payload = {"CertificateType": cert_type}

    if module.params.get('passphrase'):
        payload['Passphrase'] = module.params.get('passphrase')

    cert_path = module.params.get('certificate_path')
    try:
        if str(cert_path).lower().endswith('.p12') or str(cert_path).lower().endswith('.pfx'):
            with open(cert_path, 'rb') as cert_file:
                cert_content = cert_file.read()
                cert_file_content = base64.encodebytes(cert_content).decode('ascii')
        else:
            with open(cert_path, "r") as cert_file:
                cert_file_content = cert_file.read()
    except OSError as file_error:
        module.exit_json(msg=str(file_error), failed=True)

    payload['SSLCertificateFile'] = cert_file_content
    return payload


def _build_generate_csr_payload(module, cert_type):
    payload = {}
    cert_params = module.params.get("cert_params")

    for key, value in csr_transform.items():
        if cert_params.get(key) is not None:
            if value == 'AlternativeNames':
                forming_string = ",".join(cert_params.get(key))
                payload[value] = [forming_string]
            else:
                payload[value] = cert_params.get(key)

    if rfish_cert_coll.get(cert_type):
        payload["CertificateCollection"] = rfish_cert_coll.get(cert_type)

    return payload


payload_map = {"Server": get_ssl_payload,
               "CA": get_ssl_payload,
               "CustomCertificate": get_ssl_payload,
               "CSC": get_ssl_payload,
               "ClientTrustCertificate": get_ssl_payload}


def get_res_id(idrac, cert_type):
    resp = None
    cert_map = {"Server": MANAGER_ID}
    try:
        resp = idrac.invoke_request(cert_map.get(cert_type, MANAGERS_URI), "GET")
        membs = resp.json_data.get("Members")
        res_uri = membs[0].get('@odata.id')  # Getting the first item
        res_id = res_uri.split("/")[-1]
    except Exception:
        res_id = cert_map.get(cert_type, MANAGER_ID)
    return res_id


def get_idrac_service(idrac, res_id):
    resp = None
    resp = idrac.invoke_request(f"{MANAGERS_URI}/{res_id}", 'GET')
    srvc_data = resp.json_data
    dell_srvc = srvc_data['Links']['Oem']['Dell']['DelliDRACCardService']
    srvc = dell_srvc.get("@odata.id", IDRAC_SERVICE.format(res_id=res_id))
    return srvc


def get_actions_map(idrac, idrac_service_uri):
    resp = None
    actions = idrac_service_actions
    try:
        resp = idrac.invoke_request(idrac_service_uri, 'GET')
        srvc_data = resp.json_data
        actions = dict((k, v.get('target')) for k, v in srvc_data.get('Actions').items())
    except Exception:
        actions = idrac_service_actions
    return actions


def get_cert_url(actions, operation, cert_type, res_id):
    idrac_key = action_url_map.get(operation).get(cert_type)
    dynurl = actions.get(idrac_key)
    if not dynurl:
        dynurl = dflt_url_map.get(operation).get(cert_type)
    if dynurl:
        dynurl = dynurl.format(res_id=res_id)
    return dynurl


def upload_ssl_key(module, idrac, actions, ssl_key, res_id):
    if not os.path.exists(ssl_key) or os.path.isdir(ssl_key):
        module.exit_json(msg=f"Unable to locate the SSL key file at {ssl_key}.", failed=True)

    try:
        with open(ssl_key, "r") as file:
            scert_file = file.read()
    except OSError as err:
        module.exit_json(msg=str(err), failed=True)

    if not module.check_mode:
        upload_url = actions.get("#DelliDRACCardService.UploadSSLKey")
        if not upload_url:
            module.exit_json("Upload of SSL key not supported", failed=True)

        payload = {}
        payload = {'SSLKeyString': scert_file}
        idrac.invoke_request(upload_url.format(res_id=res_id), "POST", data=payload)


def certificate_action(module, idrac, actions, operation, cert_type, res_id):
    cert_url = get_cert_url(actions, operation, cert_type, res_id)
    if not cert_url:
        module.exit_json(msg=NOT_SUPPORTED_ACTION.format(operation=operation, cert_type=module.params.get('certificate_type')))
    cert_payload, method = payload_map.get(cert_type)(module, operation, cert_type)
    exit_certificates(module, idrac, cert_url, cert_payload, method, cert_type, res_id)


def write_to_file(module, cert_data, dkey):
    f_ext = {'HTTPS': ".pem", 'CA': ".pem", "CUSTOMCERTIFICATE": ".crt", 'CSC': ".crt", 'CLIENT_TRUST_CERTIFICATE': ".crt"}
    path = module.params.get('certificate_path')
    if not (os.path.exists(path) or os.path.isdir(path)):
        module.exit_json(msg=f"Provided directory path '{path}' is not valid.", failed=True)
    if not os.access(path, os.W_OK):
        module.exit_json(msg=f"Provided directory path '{path}' is not writable. Please check if you "
                             "have appropriate permissions.", failed=True)
    d = datetime.now()
    if module.params.get('command') == 'generate_csr':
        ext = '.txt'
    else:
        ext = f_ext.get(module.params.get('certificate_type'))
    cert_file_name = f"{module.params['idrac_ip']}_{d.strftime('%Y%m%d_%H%M%S')}_{module.params.get('certificate_type')}{ext}"
    file_name = os.path.join(path, cert_file_name)
    write_data = cert_data.pop(dkey, None)
    with open(file_name, "w") as fp:
        fp.writelines(write_data)
    cert_data[out_file_path.get(dkey)] = file_name


def format_output(module, cert_data):
    cp = cert_data.copy()
    klist = cp.keys()
    for k in klist:
        if "message" in k.lower():
            cert_data.pop(k, None)
        if k in out_file_path:
            write_to_file(module, cert_data, k)
    cert_data.pop("CertificateCollection", None)
    return cert_data


def get_export_data(idrac, cert_type, res_id):
    try:
        resp = idrac.invoke_request(EXPORT_SSL.format(res_id=res_id), "POST", data={"SSLCertType": cert_type})
        cert_data = resp.json_data
    except Exception:
        cert_data = {"CertificateFile": ""}
    return cert_data.get("CertificateFile")


def check_csr_generated(idrac):
    resp = None
    generated = False
    #  Wating max 120(24*5) seconds for CSR to be generated
    count = 24
    while not generated and count > 0:
        resp = idrac.invoke_request(CERT_STATUS, "GET")
        generated = True if resp.json_data.get("Attributes").get("Security.1.ConfigCertStatus") == 2 else False
        time.sleep(5)
        count -= 1
    return generated


def perform_operation_and_download_csr(idrac, cert_url, method, cert_payload, module):
    resp = None
    try:
        resp = idrac.invoke_request(cert_url, method, data=cert_payload, api_timeout=60)
    except HTTPError as err:
        json_err = json.load(err)
        msg_id = json_err.get("error").get("@Message.ExtendedInfo")[0].get("MessageId")
        if err.code == 503 and msg_id in ['IDRAC.2.9.SYS537', 'IDRAC.2.8.SYS537']:
            body = {'CertificateCollection': rfish_cert_coll['Server']}
            if check_csr_generated(idrac):
                resp = idrac.invoke_request(GET_LAST_GENERATED_CSR, "POST", data=body)
        else:
            module.exit_json(failed=True, error_info=json_err, msg=str(err))
    return resp


def exit_certificates(module, idrac, cert_url, cert_payload, method, cert_type, res_id):
    resp = None
    cmd = module.params.get('command')
    changed = changed_map.get(cmd)
    reset = changed_map.get(cmd) and module.params.get('reset')
    result = {"changed": changed}
    reset_msg = ""
    if changed:
        reset_msg = "Reset iDRAC to apply the new certificate." \
                    " Until the iDRAC is reset, the old certificate will remain active."
    if module.params.get('command') == 'import':
        export_cert = get_export_data(idrac, cert_type, res_id)
        if cert_payload.get('SSLCertificateFile') in export_cert:
            module.exit_json(msg=NO_CHANGES_MSG)
    if module.check_mode and changed:
        module.exit_json(msg=CHANGES_MSG, changed=changed)
    if module.params.get('command') == 'reset' and cert_type == "Server":
        resp = idrac.invoke_request(cert_url, method, data=cert_payload, dump=False)
    else:
        resp = perform_operation_and_download_csr(idrac, cert_url, method, cert_payload, module)
    cert_data = resp.json_data
    cert_output = format_output(module, cert_data)
    result.update(cert_output)
    if reset:
        reset, track_failed, reset_msg = reset_idrac(idrac, module.params.get('wait'), res_id)
    if cmd == "import" and cert_type == "Server" and module.params.get('ssl_key'):
        result['msg'] = "{0} {1}".format(SUCCESS_MSG_SSL.format(command=cmd), reset_msg)
    else:
        result['msg'] = "{0}{1}".format(SUCCESS_MSG.format(command=cmd), reset_msg)
    module.exit_json(**result)


def main():
    specs = {
        "command": {"type": 'str', "default": 'generate_csr',
                    "choices": ['generate_csr', 'export', 'import', 'reset']},
        "certificate_type": {"type": 'str', "default": 'HTTPS',
                             "choices": ['HTTPS', 'CA', 'CUSTOMCERTIFICATE', 'CSC', 'CLIENT_TRUST_CERTIFICATE']},
        "certificate_path": {"type": 'path'},
        "ssl_key": {"type": 'path'},
        "passphrase": {"type": 'str', "no_log": True},
        "cert_params": {"type": 'dict', "options": {
            "common_name": {"type": 'str', "required": True},
            "organization_unit": {"type": 'str', "required": True},
            "locality_name": {"type": 'str', "required": True},
            "state_name": {"type": 'str', "required": True},
            "country_code": {"type": 'str', "required": True},
            "email_address": {"type": 'str'},
            "organization_name": {"type": 'str', "required": True},
            "subject_alt_name": {"type": 'list', "elements": 'str', "default": []}
        }},
        "resource_id": {"type": 'str'},
        "reset": {"type": 'bool', "default": True},
        "wait": {"type": 'int', "default": 600}
    }

    module = IdracAnsibleModule(
        argument_spec=specs,
        required_if=[
            ['command', 'generate_csr', ('cert_params', 'certificate_path',)],
            ['command', 'import', ('certificate_path',)],
            ['command', 'export', ('certificate_path',)]
        ],
        supports_check_mode=True)

    try:
        with iDRACRedfishAPI(module.params) as idrac:
            cert_type = certype_map.get(module.params.get('certificate_type'))
            operation = module.params.get('command')
            res_id = module.params.get('resource_id')
            if not res_id:
                res_id = get_res_id(idrac, cert_type)
            idrac_service_uri = get_idrac_service(idrac, res_id)
            actions_map = get_actions_map(idrac, idrac_service_uri)
            if operation in ["import", "reset"] and module.params.get('reset') and module.params.get('wait') <= 0:
                module.exit_json(msg=WAIT_NEGATIVE_OR_ZERO_MSG, failed=True)
            ssl_key = module.params.get('ssl_key')
            if operation == "import" and ssl_key is not None and cert_type == "Server":
                upload_ssl_key(module, idrac, actions_map, ssl_key, res_id)
            certificate_action(module, idrac, actions_map, operation, cert_type, res_id)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (ImportError, ValueError, RuntimeError, SSLValidationError,
            ConnectionError, KeyError, TypeError, IndexError) as e:
        module.exit_json(msg=str(e), failed=True)


if __name__ == '__main__':
    main()
