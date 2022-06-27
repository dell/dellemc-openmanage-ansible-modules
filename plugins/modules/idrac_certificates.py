#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.5.0
# Copyright (C) 2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: idrac_certificates
short_description: Configure certificates for iDRAC
version_added: "5.5.0"
description:
  - This module allows to generate certificate signing request, import, and export certificates on iDRAC.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
  command:
    description:
      - "C(generate_csr), generate CSR. This requires I(cert_params) and I(certificate_path).
      This is applicable only for C(HTTPS)"
      - C(import), import the certificate file. This requires I(certificate_path).
      - C(export), export the certificate. This requires I(certificate_path).
      - C(reset), reset the certificate to default settings. This is applicable only for C(HTTPS).
    type: str
    choices: ['import', 'export', 'generate_csr', 'reset']
    default: 'generate_csr'
  certificate_type:
    description:
      - Type of the iDRAC certificate.
      - C(HTTPS) The Dell self-signed SSL certificate.
      - C(CA) Certificate Authority(CA) signed SSL certificate.
      - C(CSC) The custom signed SSL certificate.
      - C(CLIENT_TRUST_CERTIFICATE) Client trust certificate.
    type: str
    choices: ['HTTPS', 'CA', 'CSC', 'CLIENT_TRUST_CERTIFICATE']
    default: 'HTTPS'
  certificate_path:
    description:
      - Absolute path of the certificate file if I(command) is C(import).
      - Directory path with write permissions if I(command) is C(generate_csr) or C(export).
    type: path
  passphrase:
    description: The passphrase string if the certificate to be imported is passphrase protected.
    type: str
  cert_params:
    description: Certificate parameters to generate signing request.
    type: dict
    suboptions:
      common_name:
        description: The common name of the certificate.
        type: str
        required: True
      organization_unit:
        description: The name associated with an organizational unit. For example department name.
        type: str
        required: True
      locality_name:
        description: The city or other location where the entity applying for certification is located.
        type: str
        required: True
      state_name:
        description: The state where the entity applying for certification is located.
        type: str
        required: True
      country_code:
        description: The country code of the country where the entity applying for certification is located.
        type: str
        required: True
      email_address:
        description: The email associated with the CSR.
        type: str
        required: True
      organization_name:
        description: The name associated with an organization.
        type: str
        required: True
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
    default: True
  wait:
    description:
      - Maximum wait time for iDRAC to start after the reset, in seconds.
      - This is applicable when I(command) is C(import) or C(reset) and I(reset) is C(True).
    type: int
    default: 300
requirements:
  - "python >= 3.8.6"
author:
  - "Jagadeesh N V(@jagadeeshnv)"
notes:
    - The certificate operations are supported on iDRAC firmware 5.10.10.00 and above.
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
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

- name: Export a Client trust certificate.
  dellemc.openmanage.idrac_certificates:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "export"
    certificate_type: "CLIENT_TRUST_CERTIFICATE"
    certificate_path: "/home/omam/mycert_dir"
'''

RETURN = r'''
---
msg:
  type: str
  description: Status of the certificate configuration operation.
  returned: always
  sample: "Successfully performed the operation generate_csr."
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
import base64
import os
from datetime import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, idrac_auth_params
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import reset_idrac

NOT_SUPPORTED_ACTION = "Certificate {op} not supported for the specified certificate type {certype}."
SUCCESS_MSG = "Successfully performed the '{command}' operation."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_MSG = "Changes found to be applied."
SYSTEM_ID = "System.Embedded.1"
MANAGER_ID = "iDRAC.Embedded.1"
ACTIONS_PFIX = "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService."
SYSTEMS_URI = "/redfish/v1/Systems"
MANAGERS_URI = "/redfish/v1/Managers"
IDRAC_SERVICE = "/redfish/v1/Dell/Managers/{res_id}/DelliDRACCardService"
CSR_SSL = "/redfish/v1/CertificateService/Actions/CertificateService.GenerateCSR"
IMPORT_SSL = "/redfish/v1/Dell/Managers/{res_id}/DelliDRACCardService/Actions/DelliDRACCardService.ImportSSLCertificate"
EXPORT_SSL = "/redfish/v1/Dell/Managers/{res_id}/DelliDRACCardService/Actions/DelliDRACCardService.ExportSSLCertificate"
RESET_SSL = "/redfish/v1/Dell/Managers/{res_id}/DelliDRACCardService/Actions/DelliDRACCardService.SSLResetCfg"
IDRAC_RESET = "/redfish/v1/Managers/{res_id}/Actions/Manager.Reset"

idrac_service_actions = {
    "#DelliDRACCardService.DeleteCertificate": "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.DeleteCertificate",
    "#DelliDRACCardService.ExportCertificate": "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.ExportCertificate",
    "#DelliDRACCardService.ExportSSLCertificate": EXPORT_SSL,
    "#DelliDRACCardService.FactoryIdentityCertificateGenerateCSR":
        "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.FactoryIdentityCertificateGenerateCSR",
    "#DelliDRACCardService.FactoryIdentityExportCertificate":
        "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.FactoryIdentityExportCertificate",
    "#DelliDRACCardService.FactoryIdentityImportCertificate":
        "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.FactoryIdentityImportCertificate",
    "#DelliDRACCardService.GenerateSEKMCSR": "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.GenerateSEKMCSR",
    "#DelliDRACCardService.ImportCertificate": "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.ImportCertificate",
    "#DelliDRACCardService.ImportSSLCertificate": IMPORT_SSL,
    "#DelliDRACCardService.SSLResetCfg": "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.SSLResetCfg",
    "#DelliDRACCardService.iDRACReset": "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.iDRACReset"
}

rfish_cert_coll = {'Server': {
    "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/NetworkProtocol/HTTPS/Certificates"
}}
out_mapper = {}
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
                  "import": {'Server': "#DelliDRACCardService.ImportSSLCertificate",
                             'CA': "#DelliDRACCardService.ImportSSLCertificate",
                             'CSC': "#DelliDRACCardService.ImportSSLCertificate",
                             'ClientTrustCertificate': "#DelliDRACCardService.ImportSSLCertificate"},
                  "export": {'Server': "#DelliDRACCardService.ExportSSLCertificate",
                             'CA': "#DelliDRACCardService.ExportSSLCertificate",
                             'CSC': "#DelliDRACCardService.ExportSSLCertificate",
                             'ClientTrustCertificate': "#DelliDRACCardService.ExportSSLCertificate"},
                  "reset": {'Server': "#DelliDRACCardService.SSLResetCfg"}}

dflt_url_map = {"generate_csr": {'Server': CSR_SSL},
                "import": {'Server': IMPORT_SSL,
                           'CA': IMPORT_SSL,
                           'CSC': IMPORT_SSL,
                           'ClientTrustCertificate': IMPORT_SSL},
                "export": {'Server': EXPORT_SSL,
                           'CA': EXPORT_SSL,
                           'CSC': EXPORT_SSL,
                           'ClientTrustCertificate': EXPORT_SSL},
                "reset": {'Server': RESET_SSL}}
certype_map = {'HTTPS': "Server", 'CA': "CA", 'CSC': "CSC",
               'CLIENT_TRUST_CERTIFICATE': "ClientTrustCertificate"}


def get_ssl_payload(module, op, certype):
    payload = {}
    method = 'POST'
    if op == 'import':
        payload["CertificateType"] = certype
        if module.params.get('passphrase'):
            payload['Passphrase'] = module.params.get('passphrase')
        fpath = module.params.get('certificate_path')
        try:
            if str(fpath).lower().endswith('.p12') or str(fpath).lower().endswith(
                    '.pfx'):  # Linux generates .p12 Windows .pfx
                with open(fpath, 'rb') as cert:
                    cert_content = cert.read()
                    cert_file = base64.encodebytes(cert_content).decode('ascii')
            else:
                with open(fpath, "r") as cert:
                    cert_file = cert.read()
        except OSError as file_err:
            module.exit_json(msg=str(file_err), failed=True)
        payload['SSLCertificateFile'] = cert_file
    elif op == 'export':
        payload['SSLCertType'] = certype
    elif op == 'generate_csr':
        payload = {}
        cert_params = module.params.get("cert_params")
        for k, v in csr_transform.items():
            payload[v] = cert_params.get(k)
        if rfish_cert_coll.get(certype):
            payload["CertificateCollection"] = rfish_cert_coll.get(certype)
    elif op == 'reset':
        payload = "{}"
    return payload, method


payload_map = {"Server": get_ssl_payload,
               "CA": get_ssl_payload,
               "CSC": get_ssl_payload,
               "ClientTrustCertificate": get_ssl_payload}


def get_res_id(idrac, certype):
    cert_map = {"Server": MANAGER_ID}
    try:
        resp = idrac.invoke_request("GET", cert_map.get(certype, MANAGERS_URI))
        membs = resp.json_data.get("Members")
        res_uri = membs[0].get('@odata.id')  # Getting the first item
        res_id = res_uri.split("/")[-1]
    except Exception:
        res_id = cert_map.get(certype, MANAGER_ID)
    return res_id


def get_idrac_service(idrac, res_id):
    srvc = IDRAC_SERVICE.format(res_id=res_id)
    try:
        resp = idrac.invoke_request('GET', "{0}/{1}".format(MANAGERS_URI, res_id))
        srvc_data = resp.json_data
        dell_srvc = srvc_data['Links']['Oem']['Dell']['DelliDRACCardService']
        srvc = dell_srvc.get("@odata.id", IDRAC_SERVICE.format(res_id=res_id))
    except Exception:
        srvc = IDRAC_SERVICE.format(res_id=res_id)
    return srvc


def get_actions_map(idrac, idrac_service_uri):
    actions = idrac_service_actions
    try:
        resp = idrac.invoke_request(idrac_service_uri, 'GET')
        srvc_data = resp.json_data
        actions = dict((k, v.get('target')) for k, v in srvc_data.get('Actions').items())
    except Exception as exc:
        actions = idrac_service_actions
    return actions


def get_cert_url(actions, op, certype, res_id):
    idrac_key = action_url_map.get(op).get(certype)
    dynurl = actions.get(idrac_key)
    if not dynurl:
        dynurl = dflt_url_map.get(op).get(certype)
    if dynurl:
        dynurl = dynurl.format(res_id=res_id)
    return dynurl


def certificate_action(module, idrac, actions, op, certype, res_id):
    cert_url = get_cert_url(actions, op, certype, res_id)
    if not cert_url:
        module.exit_json(msg=NOT_SUPPORTED_ACTION.format(op=op, certype=module.params.get('certificate_type')))
    cert_payload, method = payload_map.get(certype)(module, op, certype)
    exit_certificates(module, idrac, cert_url, cert_payload, method, certype, res_id)


def write_to_file(module, cert_data, dkey):
    f_ext = {'HTTPS': ".pem", 'CA': ".pem", 'CSC': ".crt", 'CLIENT_TRUST_CERTIFICATE': ".crt"}
    path = module.params.get('certificate_path')
    if not (os.path.exists(path) or os.path.isdir(path)):
        module.exit_json(msg="Provided directory path '{0}' is not valid.".format(path), failed=True)
    if not os.access(path, os.W_OK):
        module.exit_json(msg="Provided directory path '{0}' is not writable. Please check if you "
                             "have appropriate permissions.".format(path), failed=True)
    d = datetime.now()
    if module.params.get('command') == 'generate_csr':
        ext = '.txt'
    else:
        ext = f_ext.get(module.params.get('certificate_type'))
    cert_file_name = "{0}_{1}{2}{3}_{4}{5}{6}_{7}{8}".format(
        module.params["idrac_ip"], d.date().year, d.date().month, d.date().day,
        d.time().hour, d.time().minute, d.time().second, module.params.get('certificate_type'), ext)
    file_name = os.path.join(path, cert_file_name)
    write_data = cert_data.pop(dkey, None)
    with open(file_name, "w") as fp:
        fp.writelines(write_data)
    cert_data[out_file_path.get(dkey)] = file_name


def format_output(module, cert_data):
    # cert_data = strip_substr_dict(cert_data, chkstr='@odata')
    result = {}
    cp = cert_data.copy()
    klist = cp.keys()
    for k in klist:
        if "message" in k.lower():
            cert_data.pop(k, None)
        if k in out_mapper:
            cert_data[out_mapper.get(k)] = cert_data.pop(k, None)
        if k in out_file_path:
            write_to_file(module, cert_data, k)
    if result:
        cert_data.update({'result': result})
    cert_data.pop("CertificateCollection", None)
    return cert_data


def get_export_data(idrac, certype, res_id):
    try:
        resp = idrac.invoke_request(EXPORT_SSL.format(res_id=res_id), "POST", data={"SSLCertType": certype})
        cert_data = resp.json_data
    except Exception:
        cert_data = {"CertificateFile": ""}
    return cert_data.get("CertificateFile")


def exit_certificates(module, idrac, cert_url, cert_payload, method, certype, res_id):
    cmd = module.params.get('command')
    changed = changed_map.get(cmd)
    reset = changed_map.get(cmd) and module.params.get('reset')
    result = {"changed": changed}
    reset_msg = ""
    if changed:
        reset_msg = " Reset iDRAC to apply new certificate." \
                    " Until iDRAC is reset, the old certificate will be active."
    if module.params.get('command') == 'import':
        export_cert = get_export_data(idrac, certype, res_id)
        if cert_payload.get('SSLCertificateFile') in export_cert:
            module.exit_json(msg=NO_CHANGES_MSG)
    if module.check_mode and changed:
        module.exit_json(msg=CHANGES_MSG, changed=changed)
    if module.params.get('command') == 'reset' and certype == "Server":
        resp = idrac.invoke_request(cert_url, method, data=cert_payload, dump=False)
    else:
        resp = idrac.invoke_request(cert_url, method, data=cert_payload)
    cert_data = resp.json_data
    cert_output = format_output(module, cert_data)
    result.update(cert_output)
    if reset:
        reset, track_failed, reset_msg = reset_idrac(idrac, module.params.get('wait'), res_id)
    result['msg'] = "{0}{1}".format(SUCCESS_MSG.format(command=cmd), reset_msg)
    module.exit_json(**result)


def main():
    specs = {
        "command": {"type": 'str', "default": 'generate_csr',
                    "choices": ['generate_csr', 'export', 'import', 'reset']},
        "certificate_type": {"type": 'str', "default": 'HTTPS',
                             "choices": ['HTTPS', 'CA', 'CSC', 'CLIENT_TRUST_CERTIFICATE']},
        "certificate_path": {"type": 'path'},
        "passphrase": {"type": 'str', "no_log": True},
        "cert_params": {"type": 'dict', "options": {
            "common_name": {"type": 'str', "required": True},
            "organization_unit": {"type": 'str', "required": True},
            "locality_name": {"type": 'str', "required": True},
            "state_name": {"type": 'str', "required": True},
            "country_code": {"type": 'str', "required": True},
            "email_address": {"type": 'str', "required": True},
            "organization_name": {"type": 'str', "required": True},
            "subject_alt_name": {"type": 'list', "elements": 'str', "default": []}
        }},
        "resource_id": {"type": 'str'},
        "reset": {"type": 'bool', "default": True},
        "wait": {"type": 'int', "default": 300}
    }
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        required_if=[
            ['command', 'generate_csr', ('cert_params', 'certificate_path',)],
            ['command', 'import', ('certificate_path',)],
            ['command', 'export', ('certificate_path',)]
        ],
        supports_check_mode=True)

    try:
        with iDRACRedfishAPI(module.params) as idrac:
            certype = certype_map.get(module.params.get('certificate_type'))
            op = module.params.get('command')
            res_id = module.params.get('resource_id')
            if not res_id:
                res_id = get_res_id(idrac, certype)
            idrac_service_uri = get_idrac_service(idrac, res_id)
            actions_map = get_actions_map(idrac, idrac_service_uri)
            certificate_action(module, idrac, actions_map, op, certype, res_id)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (ImportError, ValueError, RuntimeError, SSLValidationError,
            ConnectionError, KeyError, TypeError, IndexError) as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
