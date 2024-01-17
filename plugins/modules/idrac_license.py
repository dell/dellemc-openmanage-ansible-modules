#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.7.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: idrac_license
short_description: Configure iDRAC licenses
version_added: "8.7.0"
description:
  - This module allows to import, export and delete licenses on iDRAC.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
  license_id:
    description:
      - Entitlement ID of the license that is to be imported, exported or deleted.
      - I(license_id) is required when I(delete) is C(true) or I(export) is C(true).
    type: str
    aliases: ['entitlement_id']
  delete:
    description:
      - Delete the license from the iDRAC.
      - When I(delete) is C(true), then I(license_id) is required.
      - I(delete) is mutually exclusive with I(export) and I(import).
    type: bool
    default: false
  export:
    description:
      - Export the license from the iDRAC.
      - When I(export) is C(true), I(license_id) and I(share_parameters) is required.
      - I(export) is mutually exclusive with I(delete) and I(import).
    type: bool
    default: false
  import:
    description:
      - Import the license from the iDRAC.
      - When I(import) is C(true), I(share_parameters) is required.
      - I(import) is mutually exclusive with I(delete) and I(export).
    type: bool
    default: false
  share_parameters:
    description:
      - Parameters that are required for the import and export operation of a license.
      - I(share_parameters) is required when I(export) or I(import) is C(true).
    type: dict
    suboptions:
      share_type:
        description:
          - Share type of the network share.
          - C(local) uses local path for I(import) and I(export) operation.
          - C(nfs) uses NFS share for I(import) and I(export) operation.
          - C(cifs) uses CIFS share for I(import) and I(export) operation.
          - C(http) uses HTTP share for I(import) and I(export) operation.
          - C(https) uses HTTPS share for I(import) and I(export) operation.
        type: str
        choices: [local, nfs, cifs, http, https]
        default: local
      file_name:
        description:
          - License file name for I(import) and I(export) operation.
          - I(file_name) is required when I(import) is C(true).
        type: str
      ip_address:
        description:
          - IP address of the network share.
          - I(ip_address) is required when I(share_type) is C(nfs), C(cifs), C(http) or C(https).
        type: str
      share_name:
        description:
          - Network share or local path of the license file.
        type: str
      workgroup:
        description:
          - Workgroup of the network share.
          - I(workgroup) is applicable only when I(share_type) is C(cifs).
        type: str
      username:
        description:
          - Username of the network share.
          - I(username) is required when I(share_type) is C(cifs).
        type: str
      password:
        description:
          - Password of the network share.
          - I(password) is required when I(share_type) is C(cifs).
        type: str
      ignore_certificate_warning:
        description:
          - Ignores the certificate warning while connecting to Share and is only applicable when I(share_type) is C(https).
          - C(off) ignores the certificate warning.
          - C(on) does not ignore the certificate warning.
        type: str
        choices: ["off", "on"]
        default: "off"
      proxy_support:
        description:
          - Specifies if proxy is to be used or not.
          - C(off) does not use proxy settings.
          - C(default_proxy) uses the default proxy settings.
          - C(parameters_proxy) uses the specified proxy settings. I(proxy_server) is required when I(proxy_support) is C(parameters_proxy).
          - I(proxy_support) is only applicable when I(share_type) is C(https) or C(https).
        type: str
        choices: ["off", "default_proxy", "parameters_proxy"]
        default: "off"
      proxy_type:
        description:
          - The proxy type of the proxy server.
          - C(http) to select HTTP proxy.
          - C(socks) to select SOCKS proxy.
          - I(proxy_type) is only applicable when I(share_type) is C(https) or C(https) and when I(proxy_support) is C(parameters_proxy).
        type: str
        choices: [http, socks]
        default: http
      proxy_server:
        description:
          - The IP address of the proxy server.
          - I(proxy_server) is required when I(proxy_support) is C(parameters_proxy).
          - I(proxy_server) is only applicable when I(share_type) is C(https) or C(https) and when I(proxy_support) is C(parameters_proxy).
        type: str
      proxy_port:
        description:
          - The port of the proxy server.
          - I(proxy_port) is only applicable when I(share_type) is C(https) or C(https) and when I(proxy_support) is C(parameters_proxy).
        type: str
        default: '80'
      proxy_username:
        description:
          - The username of the proxy server.
          - I(proxy_username) is only applicable when I(share_type) is C(https) or C(https) and when I(proxy_support) is C(parameters_proxy).
        type: str
      proxy_password:
        description:
          - The password of the proxy server.
          - I(proxy_password) is only applicable when I(share_type) is C(https) or C(https) and when I(proxy_support) is C(parameters_proxy).
        type: str
  resource_id:
    type: str
    description:
      - Id of the resource.
      - If the value for resource ID is not provided, the module picks the first resource ID available from the list of system resources returned by the iDRAC.
requirements:
  - "python >= 3.8.6"
author:
  - "Rajshekar P(@rajshekarp87)"
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports only iDRAC9 and above.
    - This module supports IPv4 and IPv6 addresses.
    - This module does not support C(check_mode).
"""

EXAMPLES = r"""
---
- name: Export a license from iDRAC to local
  dellemc.openmanage.idrac_license:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    license_id: "LICENSE_123"
    export: true
    share_parameters:
      share_type: "local"
      share_name: "/path/to/share"
      file_name: "license_file"

- name: Export a license from iDRAC to NFS share
  dellemc.openmanage.idrac_license:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    license_id: "LICENSE_123"
    export: true
    share_parameters:
      share_type: "nfs"
      share_name: "/path/to/share"
      file_name: "license_file"

- name: Export a license from iDRAC to CIFS share
  dellemc.openmanage.idrac_license:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    license_id: "LICENSE_123"
    export: true
    share_parameters:
      share_type: "cifs"
      share_name: "/path/to/share"
      file_name: "license_file"
      ip_address: "192.168.0.1"
      username: "username"
      password: "password"
      workgroup: "workgroup"

- name: Export a license from iDRAC to HTTP share via proxy
  dellemc.openmanage.idrac_license:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    license_id: "LICENSE_123"
    export: true
    share_parameters:
      share_type: "http"
      share_name: "/path/to/share"
      file_name: "license_file"
      ip_address: "192.168.0.1"
      username: "username"
      password: "password"
      proxy_support: "parameters_proxy"
      proxy_type: socks
      proxy_server: "192.168.0.2"
      proxy_port: "1080"
      proxy_username: "proxy_username"
      proxy_password: "proxy_password"

- name: Export a license from iDRAC to HTTPS share
  dellemc.openmanage.idrac_license:
    idrac_ip: "192.168.0.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    license_id: "LICENSE_123"
    export: true
    share_parameters:
      share_type: "https"
      share_name: "/path/to/share"
      file_name: "license_file"
      ip_address: "192.168.0.1"
      username: "username"
      password: "password"
      ignore_certificate_warning: "on"

- name: Import a license to iDRAC from local
  dellemc.openmanage.idrac_license:
    idrac_ip: 198.162.0.1
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    import: true
    share_parmaters:
      file_name: "license_file_name.xml"
      share_type: local
      share_name: "/path/to/share"

- name: Import a license to iDRAC from NFS share
  dellemc.openmanage.idrac_license:
    idrac_ip: 198.162.0.1
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    import: true
    share_parmaters:
      file_name: "license_file_name.xml"
      share_type: nfs
      ip_address: "192.168.0.1"
      share_name: "/path/to/share"

- name: Import a license to iDRAC from CIFS share
  dellemc.openmanage.idrac_license:
    idrac_ip: 198.162.0.1
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    import: true
    share_parmaters:
      file_name: "license_file_name.xml"
      share_type: cifs
      ip_address: "192.168.0.1"
      share_name: "/path/to/share"
      username: "username"
      password: "password"

- name: Import a license to iDRAC from HTTP share
  dellemc.openmanage.idrac_license:
    idrac_ip: 198.162.0.1
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    import: true
    share_parmaters:
      file_name: "license_file_name.xml"
      share_type: http
      ip_address: "192.168.0.1"
      share_name: "/path/to/share"
      username: "username"
      password: "password"

- name: Import a license to iDRAC from HTTPS share via proxy
  dellemc.openmanage.idrac_license:
    idrac_ip: 198.162.0.1
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    import: true
    share_parmaters:
      file_name: "license_file_name.xml"
      share_type: https
      ip_address: "192.168.0.1"
      share_name: "/path/to/share"
      username: "username"
      password: "password"
      proxy_support: "parameters_proxy"
      proxy_server: "192.168.0.2"
      proxy_port: "808"
      proxy_username: "proxy_username"
      proxy_password: "proxy_password"

- name: Delete a License from iDRAC
  dellemc.openmanage.idrac_license:
    idrac_ip: 198.162.0.1
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    license_id: "LICENCE_123"
    delete: true
"""

RETURN = r'''
---
msg:
  type: str
  description: Status of the license operation.
  returned: always
  sample: "Successfully exported the license."
job_details:
    description: Returns the output for status of the job.
    returned: For import and export operations
    type: dict
    sample: {
        "ActualRunningStartTime": "2024-01-09T05:16:19",
        "ActualRunningStopTime": "2024-01-09T05:16:19",
        "CompletionTime": "2024-01-09T05:16:19",
        "Description": "Job Instance",
        "EndTime": null,
        "Id": "JID_XXXXXXXXX",
        "JobState": "Completed",
        "JobType": "LicenseExport",
        "Message": "The command was successful.",
        "MessageArgs": [],
        "MessageId": "LIC900",
        "Name": "Export: License",
        "PercentComplete": 100,
        "StartTime": "2024-01-09T05:16:19",
        "TargetSettingsURI": null
    }
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
      "code": "Base.1.8.GeneralError",
      "message": "A general error has occurred. See ExtendedInfo for more information.",
      "@Message.ExtendedInfo": [
        {
          "MessageId": "Base.1.8.AccessDenied",
          "Message": "The authentication credentials included with this request are missing or invalid.",
          "MessageArgs": [],
          "RelatedProperties": [],
          "Severity": "Critical",
          "Resolution": "Attempt to ensure that the URI is correct and that the service has the appropriate credentials."
        }
      ]
    }
  }
'''

import json
import os
import base64
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.compat.version import LooseVersion
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, idrac_auth_params
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    get_idrac_firmware_version, get_dynamic_uri, get_manager_res_id,
    validate_and_get_first_resource_id_uri, remove_key, idrac_redfish_job_tracking)

REDFISH = "/redfish/v1"
MANAGERS_URI = "/redfish/v1/Managers"
IDRAC_JOB_URI = "{res_uri}/Jobs/{job_id}"

OEM = "Oem"
MANUFACTURER = "Dell"
LICENSE_MANAGEMENT_SERVICE = "DellLicenseManagementService"
ACTIONS = "Actions"
EXPORT_LOCAL = "#DellLicenseManagementService.ExportLicense"
EXPORT_NETWORK_SHARE = "#DellLicenseManagementService.ExportLicenseToNetworkShare"
IMPORT_LOCAL = "#DellLicenseManagementService.ImportLicense"
IMPORT_NETWORK_SHARE = "#DellLicenseManagementService.ImportLicenseFromNetworkShare"

INVALID_LICENSE_MSG = "License id '{license_id}' is invalid."
SUCCESS_EXPORT_MSG = "Successfully exported the license."
SUCCESS_DELETE_MSG = "Successfully deleted the license."
SUCCESS_IMPORT_MSG = "Successfully imported the license."
FAILURE_MSG = "Unable to '{operation}' the license with id '{license_id}'."
FAILURE_IMPORT_MSG = "Unable to import the license."
NO_FILE_MSG = "License file not found."
INVALID_FILE_MSG = "File extension is invalid. Supported extensions for local 'share_type' " \
                   "is: .txt and .xml, and for network 'share_type' is: .xml."
INVALID_DIRECTORY_MSG = "Provided directory path '{path}' is not valid."
INSUFFICIENT_DIRECTORY_PERMISSION_MSG = "Provided directory path '{path}' is not writable. " \
                                        "Please check if the directory has appropriate permissions"
MISSING_PARAMETER_MSG = "Missing required parameter 'file_name'."

IGNORE_CERTIFICATE_WARNING = {"off": "Off", "on": "On"}
PROXY_SUPPORT = {"off": "Off", "default_proxy": "DefaultProxy", "parameters_proxy": "ParametersProxy"}
PROXY_TYPE = {"http": "HTTP", "socks": "SOCKS"}


class DeleteLicense:
    def __init__(self, idrac, module):
        self.idrac = idrac
        self.module = module

    def execute(self, module):
        license_id = module.params.get('license_id')
        check_license_id(self, module, license_id, "delete")
        license_url = __get_license_url(self)
        delete_license_url = license_url + f"/{license_id}"
        delete_license_response = self.idrac.invoke_request(delete_license_url, 'DELETE')
        status = delete_license_response.status_code
        if status == 204:
            module.exit_json(msg=SUCCESS_DELETE_MSG, changed=True)
        else:
            module.exit_json(FAILURE_MSG.format(operation="delete", license_id=license_id), failed=True)
        return delete_license_response


class ExportLicense:
    def __init__(self, idrac, module):
        self.idrac = idrac
        self.module = module

    def execute(self, module):
        share_type = module.params.get('share_parameters').get('share_type')
        license_id = module.params.get('license_id')
        check_license_id(self, module, license_id, "export")
        export_url = self.__get_export_license_url(module)
        if share_type == "local":
            export_license_status = self.__export_license_local(module, export_url)
        elif share_type in ["http", "https"]:
            export_license_status = self.__export_license_http(module, export_url)
            job_status = get_job_status(self, module, export_license_status)
        elif share_type == "cifs":
            export_license_status = self.__export_license_cifs(module, export_url)
            job_status = get_job_status(self, module, export_license_status)
        elif share_type == "nfs":
            export_license_status = self.__export_license_nfs(module, export_url)
            job_status = get_job_status(self, module, export_license_status)
        status = export_license_status.status_code
        if share_type in ["http", "https", "cifs", "nfs"]:
            if status in [200, 202]:
                module.exit_json(msg=SUCCESS_EXPORT_MSG, changed=True, job_details=job_status)
            else:
                module.exit_json(msg=FAILURE_MSG.format(operation="export", license_id=license_id), failed=True, job_details=job_status)
        else:
            if status in [200, 202]:
                module.exit_json(msg=SUCCESS_EXPORT_MSG, changed=True, job_details={})
            else:
                module.exit_json(msg=FAILURE_MSG.format(operation="export", license_id=license_id), failed=True, job_details={})
        return export_license_status

    def __export_license_local(self, module, export_url):
        export_license_url = export_url
        payload = {}
        payload["EntitlementID"] = module.params.get('license_id')
        path = module.params.get('share_parameters').get('share_name')
        if not (os.path.exists(path) or os.path.isdir(path)):
            module.exit_json(msg=INVALID_DIRECTORY_MSG.format(path=path), failed=True)
        if not os.access(path, os.W_OK):
            module.exit_json(msg=INSUFFICIENT_DIRECTORY_PERMISSION_MSG.format(path=path), failed=True)
        license_name = module.params.get('share_parameters').get('file_name')
        if license_name:
            license_file_name = f"{license_name}_iDRAC_license.txt"
        else:
            license_file_name = f"{module.params['license_id']}_iDRAC_license.txt"
        license_status = self.idrac.invoke_request(export_license_url, "POST", data=payload)
        license_data = license_status.json_data
        license_file = license_data.get("LicenseFile")
        file_name = os.path.join(path, license_file_name)
        with open(file_name, "w") as fp:
            fp.writelines(license_file)
        return license_status

    def __export_license_http(self, module, export_url):
        export_license_url = export_url
        payload = {}
        payload["EntitlementID"] = module.params.get('license_id')
        proxy_details = get_proxy_details(module)
        payload.update(proxy_details)
        export_status = self.__export_license(module, payload, export_license_url)
        return export_status

    def __export_license_cifs(self, module, export_url):
        export_license_url = export_url
        payload = {}
        payload["EntitlementID"] = module.params.get('license_id')
        payload["ShareType"] = "CIFS"
        if module.params.get('share_parameters').get('workgroup'):
            payload["Workgroup"] = module.params.get('share_parameters').get('workgroup')
        share_details = get_share_details(module)
        payload.update(share_details)
        export_status = self.__export_license(module, payload, export_license_url)
        return export_status

    def __export_license_nfs(self, module, export_url):
        export_license_url = export_url
        payload = {}
        payload["EntitlementID"] = module.params.get('license_id')
        payload["ShareType"] = "NFS"
        payload["IPAddress"] = module.params.get('share_parameters').get('ip_address')
        payload["ShareName"] = module.params.get('share_parameters').get('share_name')
        export_status = self.__export_license(module, payload, export_license_url)
        return export_status

    def __get_export_license_url(self, module):
        uri, error_msg = validate_and_get_first_resource_id_uri(
            self.module, self.idrac, MANAGERS_URI)
        if error_msg:
            self.module.exit_json(msg=error_msg, failed=True)
        resp = get_dynamic_uri(self.idrac, uri)
        url = resp.get('Links', {}).get(OEM, {}).get(MANUFACTURER, {}).get(LICENSE_MANAGEMENT_SERVICE, {}).get('@odata.id', {})
        action_resp = get_dynamic_uri(self.idrac, url)
        if module.params.get('share_parameters').get('share_type') == "local":
            license_service = EXPORT_LOCAL
        else:
            license_service = EXPORT_NETWORK_SHARE
        export_url = action_resp.get(ACTIONS, {}).get(license_service, {}).get('target', {})
        return export_url

    def __export_license(self, module, payload, export_license_url):
        license_name = module.params.get('share_parameters').get('file_name')
        if license_name:
            license_file_name = f"{license_name}_iDRAC_license.xml"
        else:
            license_file_name = f"{module.params['license_id']}_iDRAC_license.xml"
        payload["FileName"] = license_file_name
        license_status = self.idrac.invoke_request(export_license_url, "POST", data=payload)
        return license_status


class ImportLicense:
    def __init__(self, idrac, module):
        self.idrac = idrac
        self.module = module

    def execute(self, module):
        if not module.params.get('share_parameters').get('file_name'):
            module.exit_json(msg=MISSING_PARAMETER_MSG, failed=True)
        share_type = module.params.get('share_parameters').get('share_type')
        self.__check_file_extension(module)
        import_license_url = self.__get_import_license_url(module)
        resource_id = get_manager_res_id(self.idrac)
        if share_type == "local":
            import_license_status = self.__import_license_local(module, import_license_url, resource_id)
        elif share_type in ["http", "https"]:
            import_license_status = self.__import_license_http(module, import_license_url, resource_id)
            job_status = get_job_status(self, module, import_license_status)
        elif share_type == "cifs":
            import_license_status = self.__import_license_cifs(module, import_license_url, resource_id)
            job_status = get_job_status(self, module, import_license_status)
        elif share_type == "nfs":
            import_license_status = self.__import_license_nfs(module, import_license_url, resource_id)
            job_status = get_job_status(self, module, import_license_status)
        status = import_license_status.status_code
        if share_type in ["http", "https", "cifs", "nfs"]:
            if status in [200, 202]:
                module.exit_json(msg=SUCCESS_IMPORT_MSG, changed=True, job_details=job_status)
            else:
                module.exit_json(msg=FAILURE_IMPORT_MSG, failed=True, job_details=job_status)
        else:
            if status in [200, 202]:
                module.exit_json(msg=SUCCESS_IMPORT_MSG, changed=True, job_details={})
            else:
                module.exit_json(msg=FAILURE_IMPORT_MSG, failed=True, job_details={})
        return import_license_status

    def __import_license_local(self, module, import_license_url, resource_id):
        payload = {}
        path = module.params.get('share_parameters').get('share_name')
        if not (os.path.exists(path) or os.path.isdir(path)):
            module.exit_json(msg=f"Provided directory path '{path}' is not valid.", failed=True)
        file_path = module.params.get('share_parameters').get('share_name') + "/" + module.params.get('share_parameters').get('file_name')
        file_exits = os.path.exists(file_path)
        if file_exits:
            with open(file_path, "rb") as cert:
                cert_content = cert.read()
                read_file = base64.encodebytes(cert_content).decode('ascii')
        else:
            module.exit_json(msg=NO_FILE_MSG, failed=True)
        payload["LicenseFile"] = read_file
        payload["FQDD"] = resource_id
        payload["ImportOptions"] = "Force"
        import_status = self.idrac.invoke_request(import_license_url, "POST", data=payload)
        return import_status

    def __import_license_http(self, module, import_license_url, resource_id):
        payload = {}
        payload["LicenseName"] = module.params.get('share_parameters').get('file_name')
        payload["FQDD"] = resource_id
        payload["ImportOptions"] = "Force"
        proxy_details = get_proxy_details(module)
        payload.update(proxy_details)
        import_status = self.idrac.invoke_request(import_license_url, "POST", data=payload)
        return import_status

    def __import_license_cifs(self, module, import_license_url, resource_id):
        payload = {}
        payload["ShareType"] = "CIFS"
        payload["LicenseName"] = module.params.get('share_parameters').get('file_name')
        payload["FQDD"] = resource_id
        payload["ImportOptions"] = "Force"
        if module.params.get('share_parameters').get('workgroup'):
            payload["Workgroup"] = module.params.get('share_parameters').get('workgroup')
        share_details = get_share_details(module)
        payload.update(share_details)
        import_status = self.idrac.invoke_request(import_license_url, "POST", data=payload)
        return import_status

    def __import_license_nfs(self, module, import_license_url, resource_id):
        payload = {}
        payload["ShareType"] = "NFS"
        payload["IPAddress"] = module.params.get('share_parameters').get('ip_address')
        payload["ShareName"] = module.params.get('share_parameters').get('share_name')
        payload["LicenseName"] = module.params.get('share_parameters').get('file_name')
        payload["FQDD"] = resource_id
        payload["ImportOptions"] = "Force"
        import_status = self.idrac.invoke_request(import_license_url, "POST", data=payload)
        return import_status

    def __check_file_extension(self, module):
        share_type = module.params.get('share_parameters').get('share_type')
        file_name = module.params.get('share_parameters').get('file_name')
        valid_extensions = {".txt", ".xml"} if share_type == "local" else {".xml"}
        file_extension = file_name.lower().endswith(tuple(valid_extensions))
        if not file_extension:
            module.exit_json(msg=INVALID_FILE_MSG, failed=True)

    def __get_import_license_url(self, module):
        uri, error_msg = validate_and_get_first_resource_id_uri(
            self.module, self.idrac, MANAGERS_URI)
        if error_msg:
            self.module.exit_json(msg=error_msg, failed=True)
        resp = get_dynamic_uri(self.idrac, uri)
        url = resp.get('Links', {}).get(OEM, {}).get(MANUFACTURER, {}).get(LICENSE_MANAGEMENT_SERVICE, {}).get('@odata.id', {})
        action_resp = get_dynamic_uri(self.idrac, url)
        if module.params.get('share_parameters').get('share_type') == "local":
            license_service = IMPORT_LOCAL
        else:
            license_service = IMPORT_NETWORK_SHARE
        import_url = action_resp.get(ACTIONS, {}).get(license_service, {}).get('target', {})
        return import_url


def check_license_id(self, module, license_id, operation):
    license_uri = __get_license_url(self)
    license_url = license_uri + f"/{license_id}"
    try:
        response = self.idrac.invoke_request(license_url, 'GET')
        return response
    except Exception:
        module.exit_json(msg=FAILURE_MSG.format(operation=operation, license_id=license_id), failed=True)


def __get_license_url(self):
    v1_resp = get_dynamic_uri(self.idrac, REDFISH)
    license_service_url = v1_resp.get('LicenseService', {}).get('@odata.id', {})
    license_service_resp = get_dynamic_uri(self.idrac, license_service_url)
    license_url = license_service_resp.get('Licenses', {}).get('@odata.id', {})
    return license_url


def get_job_status(self, module, export_license_status):
    res_uri = validate_and_get_first_resource_id_uri(self.module, self.idrac, MANAGERS_URI)
    job_tracking_uri = export_license_status.headers.get("Location")
    job_id = job_tracking_uri.split("/")[-1]
    job_uri = IDRAC_JOB_URI.format(job_id=job_id, res_uri=res_uri[0])
    job_failed, msg, job_dict, wait_time = idrac_redfish_job_tracking(self.idrac, job_uri)
    job_dict = remove_key(job_dict, regex_pattern='(.*?)@odata')
    if job_failed:
        module.exit_json(
            msg=job_dict.get('Message'),
            failed=True,
            job_details=job_dict)
    return job_dict


def get_share_details(module):
    share_details = {}
    share_details["IPAddress"] = module.params.get('share_parameters').get('ip_address')
    share_details["ShareName"] = module.params.get('share_parameters').get('share_name')
    share_details["UserName"] = module.params.get('share_parameters').get('username')
    share_details["Password"] = module.params.get('share_parameters').get('password')
    return share_details


def get_proxy_details(module):
    proxy_details = {}
    if module.params.get('share_parameters').get('share_type') == "http":
        proxy_details["ShareType"] = "HTTP"
    else:
        proxy_details["ShareType"] = "HTTPS"
    proxy_details["IPAddress"] = module.params.get('share_parameters').get('ip_address')
    proxy_details["ShareName"] = module.params.get('share_parameters').get('share_name')
    proxy_details["UserName"] = module.params.get('share_parameters').get('username')
    proxy_details["Password"] = module.params.get('share_parameters').get('password')
    proxy_details["IgnoreCertWarning"] = IGNORE_CERTIFICATE_WARNING[module.params.get('share_parameters').get('ignore_certificate_warning')]
    if module.params.get('share_parameters').get('proxy_support') == "parameters_proxy":
        proxy_details["ProxySupport"] = PROXY_SUPPORT[module.params.get('share_parameters').get('proxy_support')]
        proxy_details["ProxyType"] = PROXY_TYPE[module.params.get('share_parameters').get('proxy_type')]
        proxy_details["ProxyServer"] = module.params.get('share_parameters').get('proxy_server')
        proxy_details["ProxyPort"] = module.params.get('share_parameters').get('proxy_port')
        if module.params.get('share_parameters').get('proxy_username') and module.params.get('share_parameters').get('proxy_password'):
            proxy_details["ProxyUname"] = module.params.get('share_parameters').get('proxy_username')
            proxy_details["ProxyPasswd"] = module.params.get('share_parameters').get('proxy_password')
    return proxy_details


def main():
    specs = get_argument_spec()
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[("import", "export", "delete")],
        required_if=[
            ["import", True, ("share_parameters",)],
            ["export", True, ("license_id", "share_parameters",)],
            ["delete", True, ("license_id",)]
        ],
        supports_check_mode=False
    )

    try:
        with iDRACRedfishAPI(module.params) as idrac:
            idrac_firmware_version = get_idrac_firmware_version(idrac)
            if LooseVersion(idrac_firmware_version) <= '3.0':
                module.exit_json(msg="iDRAC firmware version is not supported.", failed=True)
            license_obj = None
            if module.params["import"]:
                license_obj = ImportLicense(idrac, module)
            elif module.params["export"]:
                license_obj = ExportLicense(idrac, module)
            elif module.params["delete"]:
                license_obj = DeleteLicense(idrac, module)
            if license_obj:
                license_status = license_obj.execute(module)
            else:
                module.exit_json(msg="Task is skipped as none of import, export or delete is specified.", skipped=True)
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (ImportError, ValueError, RuntimeError, SSLValidationError,
            ConnectionError, KeyError, TypeError, IndexError) as e:
        module.exit_json(msg=str(e), failed=True)


def get_argument_spec():
    return {
        "license_id": {"type": 'str', "aliases": ['entitlement_id']},
        "delete": {"type": 'bool', "default": False},
        "export": {"type": 'bool', "default": False},
        "import": {"type": 'bool', "default": False},
        "share_parameters": {
            "type": 'dict',
            "options": {
                "share_type": {
                    "type": 'str',
                    "default": 'local',
                    "choices": ['local', 'nfs', 'cifs', 'http', 'https']
                },
                "file_name": {"type": 'str'},
                "ip_address": {"type": 'str'},
                "share_name": {"type": 'str'},
                "workgroup": {"type": 'str'},
                "username": {"type": 'str'},
                "password": {"type": 'str', "no_log": True},
                "ignore_certificate_warning": {
                    "type": 'str',
                    "default": "off",
                    "choices": ["off", "on"]
                },
                "proxy_support": {
                    "type": 'str',
                    "default": "off",
                    "choices": ["off", "default_proxy", "parameters_proxy"]
                },
                "proxy_type": {
                    "type": 'str',
                    "default": 'http',
                    "choices": ['http', 'socks']
                },
                "proxy_server": {"type": 'str'},
                "proxy_port": {"type": 'str', "default": '80'},
                "proxy_username": {"type": 'str'},
                "proxy_password": {"type": 'str', "no_log": True}
            },
            "required_if": [
                ["share_type", "local", ["share_name"]],
                ["share_type", "nfs", ["ip_address", "share_name"]],
                ["share_type", "cifs", ["ip_address", "share_name", "username", "password"]],
                ["share_type", "http", ["ip_address", "share_name"]],
                ["share_type", "https", ["ip_address", "share_name"]],
                ["proxy_support", "parameters_proxy", ["proxy_server"]]
            ],
            "required_together": [
                ("username", "password"),
                ("proxy_username", "proxy_password")
            ]
        },
        "resource_id": {"type": 'str'}
    }


if __name__ == '__main__':
    main()
