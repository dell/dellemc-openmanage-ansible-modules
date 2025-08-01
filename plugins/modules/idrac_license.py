#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.2
# Copyright (C) 2024-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

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
  - dellemc.openmanage.idrac_x_auth_options
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
          - For the I(import) operation, when I(share_type) is C(local), the supported extensions for I(file_name) are '.txt' and '.xml'.
            For other share types, the supported extension is '.xml'
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
          - C(on) ignores the certificate warning.
          - C(off) does not ignore the certificate warning.
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
        type: int
        default: 80
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
  - "python >= 3.9.6"
author:
  - "Rajshekar P(@rajshekarp87)"
  - "Akash Shendge(@shenda1)"
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports only iDRAC9 and above.
    - This module supports IPv4 and IPv6 addresses.
    - This module does not support C(check_mode).
    - When I(share_type) is C(local) for I(import) and I(export) operations, job_details are not displayed.
    - Due to API limitation, proxy parameters are ignored during the I(import) operation.
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
      ip_address: "192.168.0.1"

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
      proxy_port: 1080
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
    share_parameters:
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
    share_parameters:
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
    share_parameters:
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
    share_parameters:
      file_name: "license_file_name.xml"
      share_type: http
      ip_address: "192.168.0.1"
      share_name: "/path/to/share"
      username: "username"
      password: "password"

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
from urllib.error import HTTPError, URLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, IdracAnsibleModule
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    get_dynamic_uri, get_manager_res_id,
    validate_and_get_first_resource_id_uri, remove_key, idrac_redfish_job_tracking)

REDFISH = "/redfish/v1"
MANAGERS_URI = "/redfish/v1/Managers"
IDRAC_JOB_URI = "{res_uri}/Oem/Dell/Jobs/{job_id}"

OEM = "Oem"
MANUFACTURER = "Dell"
LICENSE_MANAGEMENT_SERVICE = "DellLicenseManagementService"
ACTIONS = "Actions"
EXPORT_NETWORK_SHARE = "#DellLicenseManagementService.ExportLicenseToNetworkShare"
IMPORT_LOCAL = "#DellLicenseManagementService.ImportLicense"
IMPORT_NETWORK_SHARE = "#LicenseService.Install"
ODATA = "@odata.id"
ODATA_REGEX = "(.*?)@odata"

AUTH_ERROR_MSG = "Unable to communicate with iDRAC {ip} with error: {error}. This may be due to one of the following: " \
                 "Incorrect username or password, unreachable iDRAC IP or a failure in TLS/SSL handshake."
INVALID_LICENSE_MSG = "License with ID '{license_id}' does not exist on the iDRAC."
SUCCESS_EXPORT_MSG = "Successfully exported the license."
SUCCESS_DELETE_MSG = "Successfully deleted the license."
SUCCESS_IMPORT_MSG = "Successfully imported the license."
FAILURE_MSG = "Unable to '{operation}' the license with id '{license_id}' as it does not exist."
FAILURE_IMPORT_MSG = "Unable to import the license."
NO_FILE_MSG = "License file not found."
UNSUPPORTED_IDRAC_MSG = "iDRAC version is not supported."
NO_OPERATION_SKIP_MSG = "Task is skipped as none of import, export or delete is specified."
INVALID_FILE_MSG = "File extension is invalid. Supported extensions for local 'share_type' " \
                   "are: .txt and .xml, and for network 'share_type' is: .xml."
INVALID_DIRECTORY_MSG = "Provided directory path '{path}' is not valid."
INSUFFICIENT_DIRECTORY_PERMISSION_MSG = "Provided directory path '{path}' is not writable. " \
                                        "Please check if the directory has appropriate permissions"
MISSING_FILE_NAME_PARAMETER_MSG = "Missing required parameter 'file_name'."

PROXY_SUPPORT = {"off": "Off", "default_proxy": "DefaultProxy", "parameters_proxy": "ParametersProxy"}


class License():
    def __init__(self, idrac, module):
        """
        Initializes the class instance with the provided idrac and module parameters.

        :param idrac: The idrac parameter.
        :type idrac: Any
        :param module: The module parameter.
        :type module: Any
        """
        self.idrac = idrac
        self.module = module

    def execute(self):
        """
        Executes the function with the given module.

        :param module: The module to execute.
        :type module: Any
        :return: None
        """

    def check_license_id(self, license_id):
        """
        Check the license ID for a given operation.

        :param self: The object instance.
        :param module: The Ansible module.
        :param license_id: The ID of the license to check.
        :param operation: The operation to perform.
        :return: The response from the license URL.
        """
        license_uri = self.get_license_url()
        license_url = license_uri + f"/{license_id}"
        try:
            response = self.idrac.invoke_request(license_url, 'GET')
            return response
        except Exception:
            self.module.exit_json(msg=INVALID_LICENSE_MSG.format(license_id=license_id), skipped=True)

    def get_license_url(self):
        """
        Retrieves the license URL for the current user.

        :return: The license URL as a string.
        """
        v1_resp = get_dynamic_uri(self.idrac, REDFISH)
        license_service_url = v1_resp.get('LicenseService', {}).get(ODATA, {})
        license_service_resp = get_dynamic_uri(self.idrac, license_service_url)
        license_url = license_service_resp.get('Licenses', {}).get(ODATA, {})
        return license_url

    def get_job_status(self, license_job_response):
        """
        Get the status of a job.

        Args:
            module (object): The module object.
            license_job_response (object): The response object for the license job.

        Returns:
            dict: The job details.
        """
        res_uri = validate_and_get_first_resource_id_uri(self.module, self.idrac, MANAGERS_URI)
        job_tracking_uri = license_job_response.headers.get("Location")
        job_id = job_tracking_uri.split("/")[-1]
        job_uri = IDRAC_JOB_URI.format(job_id=job_id, res_uri=res_uri[0])
        job_failed, msg, job_dict, wait_time = idrac_redfish_job_tracking(self.idrac, job_uri)
        job_dict = remove_key(job_dict, regex_pattern=ODATA_REGEX)
        if job_failed:
            self.module.exit_json(
                msg=job_dict.get('Message'),
                failed=True,
                job_details=job_dict)
        return job_dict

    def get_share_details(self):
        """
        Retrieves the share details from the given module.

        Args:
            module (object): The module object containing the share parameters.

        Returns:
            dict: A dictionary containing the share details with the following keys:
                - IPAddress (str): The IP address of the share.
                - ShareName (str): The name of the share.
                - UserName (str): The username for accessing the share.
                - Password (str): The password for accessing the share.
        """
        share_details = {}
        share_details["IPAddress"] = self.module.params.get('share_parameters').get('ip_address')
        share_details["ShareName"] = self.module.params.get('share_parameters').get('share_name')
        if self.module.params.get('share_parameters').get('username'):
            share_details["UserName"] = self.module.params.get('share_parameters').get('username')
        if self.module.params.get('share_parameters').get('password'):
            share_details["Password"] = self.module.params.get('share_parameters').get('password')
        return share_details

    def get_proxy_details(self):
        """
        Retrieves the proxy details based on the provided module parameters.

        Args:
            self: The instance of the class.
            module: The module object containing the parameters.

        Returns:
            dict: A dictionary containing the proxy details.
        """
        proxy_details = {}
        proxy_details["ShareType"] = self.module.params.get('share_parameters').get('share_type').upper()
        proxy_details["IgnoreCertWarning"] = self.module.params.get('share_parameters').get('ignore_certificate_warning').capitalize()
        if self.module.params.get('share_parameters').get('proxy_support') == "parameters_proxy":
            proxy_details["ProxySupport"] = PROXY_SUPPORT[self.module.params.get('share_parameters').get('proxy_support')]
            proxy_details["ProxyType"] = self.module.params.get('share_parameters').get('proxy_type').upper()
            proxy_details["ProxyServer"] = self.module.params.get('share_parameters').get('proxy_server')
            proxy_details["ProxyPort"] = str(self.module.params.get('share_parameters').get('proxy_port'))
            if self.module.params.get('share_parameters').get('proxy_username') and self.module.params.get('share_parameters').get('proxy_password'):
                proxy_details["ProxyUname"] = self.module.params.get('share_parameters').get('proxy_username')
                proxy_details["ProxyPasswd"] = self.module.params.get('share_parameters').get('proxy_password')
        return proxy_details


class DeleteLicense(License):
    def execute(self):
        """
        Executes the delete operation for a given license ID.

        Args:
            module (object): The Ansible module object.

        Returns:
            object: The response object from the delete operation.
        """
        license_id = self.module.params.get('license_id')
        self.check_license_id(license_id)
        license_url = self.get_license_url()
        delete_license_url = license_url + f"/{license_id}"
        delete_license_response = self.idrac.invoke_request(delete_license_url, 'DELETE')
        status = delete_license_response.status_code
        if status == 204:
            self.module.exit_json(msg=SUCCESS_DELETE_MSG, changed=True)
        else:
            self.module.exit_json(msg=FAILURE_MSG.format(operation="delete", license_id=license_id), failed=True)


class ExportLicense(License):
    STATUS_SUCCESS = [200, 202]

    def execute(self):
        """
        Executes the export operation for a given license ID.

        :param module: The Ansible module object.
        :type module: AnsibleModule

        :return: The response from the export operation.
        :rtype: Response
        """
        share_type = self.module.params.get('share_parameters').get('share_type')
        license_id = self.module.params.get('license_id')
        self.check_license_id(license_id)
        export_license_url = self.__get_export_license_url()
        job_status = {}
        if share_type == "local":
            export_license_response = self.__export_license_local(export_license_url)
        elif share_type in ["http", "https"]:
            export_license_response = self.__export_license_http(export_license_url)
            job_status = self.get_job_status(export_license_response)
        elif share_type == "cifs":
            export_license_response = self.__export_license_cifs(export_license_url)
            job_status = self.get_job_status(export_license_response)
        elif share_type == "nfs":
            export_license_response = self.__export_license_nfs(export_license_url)
            job_status = self.get_job_status(export_license_response)
        status = export_license_response.status_code
        if status in self.STATUS_SUCCESS:
            self.module.exit_json(msg=SUCCESS_EXPORT_MSG, changed=True, job_details=job_status)
        else:
            self.module.exit_json(msg=FAILURE_MSG.format(operation="export", license_id=license_id), failed=True, job_details=job_status)

    def __export_license_local(self, export_license_url):
        """
        Export the license to a local directory.

        Args:
            module (object): The Ansible module object.
            export_license_url (str): The URL for exporting the license.

        Returns:
            object: The license status after exporting.
        """
        payload = {}
        payload["EntitlementID"] = self.module.params.get('license_id')
        path = self.module.params.get('share_parameters').get('share_name')
        if not (os.path.exists(path) or os.path.isdir(path)):
            self.module.exit_json(msg=INVALID_DIRECTORY_MSG.format(path=path), failed=True)
        if not os.access(path, os.W_OK):
            self.module.exit_json(msg=INSUFFICIENT_DIRECTORY_PERMISSION_MSG.format(path=path), failed=True)
        license_name = self.module.params.get('share_parameters').get('file_name')
        if license_name:
            license_file_name = f"{license_name}"
        else:
            license_file_name = f"{self.module.params['license_id']}_iDRAC_license.xml"
        license_status = self.idrac.invoke_request(export_license_url, "GET")
        license_data = license_status.body
        license_file = license_data.decode("utf-8")
        file_name = os.path.join(path, license_file_name)
        with open(file_name, "w") as fp:
            fp.write(license_file)
        return license_status

    def __export_license_http(self, export_license_url):
        """
        Export the license using the HTTP protocol.

        Args:
            module (object): The module object.
            export_license_url (str): The URL for exporting the license.

        Returns:
            str: The export status.
        """
        payload = {}
        payload["EntitlementID"] = self.module.params.get('license_id')
        payload["ShareType"] = self.module.params.get('share_parameters').get('share_type')
        proxy_details = self.get_proxy_details()
        share_details = self.get_share_details()
        payload.update(proxy_details)
        payload.update(share_details)
        export_status = self.__export_license(payload, export_license_url)
        return export_status

    def __export_license_cifs(self, export_license_url):
        """
        Export the license using CIFS share type.

        Args:
            module (object): The Ansible module object.
            export_license_url (str): The URL for exporting the license.

        Returns:
            str: The export status.
        """
        payload = {}
        payload["EntitlementID"] = self.module.params.get('license_id')
        payload["ShareType"] = "CIFS"
        share_details = self.get_share_details()
        payload.update(share_details)
        if self.module.params.get('share_parameters').get('workgroup'):
            payload["Workgroup"] = self.module.params.get('share_parameters').get('workgroup')
        export_status = self.__export_license(payload, export_license_url)
        return export_status

    def __export_license_nfs(self, export_license_url):
        """
        Export the license using NFS share type.

        Args:
            module (object): The Ansible module object.
            export_license_url (str): The URL for exporting the license.

        Returns:
            dict: The export status of the license.
        """
        payload = {}
        payload["EntitlementID"] = self.module.params.get('license_id')
        payload["ShareType"] = "NFS"
        payload["IPAddress"] = self.module.params.get('share_parameters').get('ip_address')
        payload["ShareName"] = self.module.params.get('share_parameters').get('share_name')
        export_status = self.__export_license(payload, export_license_url)
        return export_status

    def __get_export_license_url(self):
        """
        Get the export license URL.

        :param module: The module object.
        :type module: object
        :return: The export license URL.
        :rtype: str
        """
        if self.module.params.get('share_parameters').get('share_type') != "local":
            uri, error_msg = validate_and_get_first_resource_id_uri(self.module, self.idrac, MANAGERS_URI)
            if error_msg:
                self.module.exit_json(msg=error_msg, failed=True)
            resp = get_dynamic_uri(self.idrac, uri)
            url = resp.get('Links', {}).get(OEM, {}).get(MANUFACTURER, {}).get(LICENSE_MANAGEMENT_SERVICE, {}).get(ODATA, {})
            action_resp = get_dynamic_uri(self.idrac, url)
            export_url = action_resp.get(ACTIONS, {}).get(EXPORT_NETWORK_SHARE, {}).get('target', {})
        else:
            response = self.check_license_id(self.module.params.get('license_id'))
            export_url = response.json_data.get("DownloadURI", {})
        return export_url

    def __export_license(self, payload, export_license_url):
        """
        Export the license to a file.

        Args:
            module (object): The Ansible module object.
            payload (dict): The payload containing the license information.
            export_license_url (str): The URL for exporting the license.

        Returns:
            dict: The license status after exporting.
        """
        license_name = self.module.params.get('share_parameters').get('file_name')
        if license_name:
            license_file_name = f"{license_name}"
        else:
            license_file_name = f"{self.module.params['license_id']}_iDRAC_license.xml"
        payload["FileName"] = license_file_name
        license_status = self.idrac.invoke_request(export_license_url, "POST", data=payload)
        return license_status


class ImportLicense(License):
    STATUS_SUCCESS = [200, 202]

    def execute(self):
        """
        Executes the import license process based on the given module parameters.

        Args:
            module (object): The Ansible module object.

        Returns:
            object: The response object from the import license API call.
        """
        if not self.module.params.get('share_parameters').get('file_name'):
            self.module.exit_json(msg=MISSING_FILE_NAME_PARAMETER_MSG, failed=True)
        share_type = self.module.params.get('share_parameters').get('share_type')
        self.__check_file_extension()
        import_license_url = self.__get_import_license_url()
        resource_id = get_manager_res_id(self.idrac)
        job_status = {}
        if share_type == "local":
            import_license_response = self.__import_license_local(import_license_url, resource_id)
        elif share_type in ["http", "https"]:
            import_license_response = self.__import_license_http(import_license_url)
            job_status = self.get_job_status(import_license_response)
        elif share_type == "cifs":
            import_license_response = self.__import_license_cifs(import_license_url)
            job_status = self.get_job_status(import_license_response)
        elif share_type == "nfs":
            import_license_response = self.__import_license_nfs(import_license_url)
            job_status = self.get_job_status(import_license_response)
        status = import_license_response.status_code
        if status in self.STATUS_SUCCESS:
            self.module.exit_json(msg=SUCCESS_IMPORT_MSG, changed=True, job_details=job_status)
        else:
            self.module.exit_json(msg=FAILURE_IMPORT_MSG, failed=True, job_details=job_status)

    def __import_license_local(self, import_license_url, resource_id):
        """
        Import a license locally.

        Args:
            module (object): The Ansible module object.
            import_license_url (str): The URL for importing the license.
            resource_id (str): The ID of the resource.

        Returns:
            dict: The import status of the license.
        """
        payload = {}
        path = self.module.params.get('share_parameters').get('share_name')
        if not (os.path.exists(path) or os.path.isdir(path)):
            self.module.exit_json(msg=INVALID_DIRECTORY_MSG.format(path=path), failed=True)
        file_path = self.module.params.get('share_parameters').get('share_name') + "/" + self.module.params.get('share_parameters').get('file_name')
        file_exits = os.path.exists(file_path)
        if file_exits:
            with open(file_path, "rb") as cert:
                cert_content = cert.read()
                read_file = base64.encodebytes(cert_content).decode('ascii')
        else:
            self.module.exit_json(msg=NO_FILE_MSG, failed=True)
        payload["LicenseFile"] = read_file
        payload["FQDD"] = resource_id
        payload["ImportOptions"] = "Force"
        try:
            import_status = self.idrac.invoke_request(import_license_url, "POST", data=payload)
        except HTTPError as err:
            filter_err = remove_key(json.load(err), regex_pattern=ODATA_REGEX)
            message_details = filter_err.get('error').get('@Message.ExtendedInfo')[0]
            message_id = message_details.get('MessageId')
            if 'LIC018' in message_id:
                self.module.exit_json(msg=message_details.get('Message'), skipped=True)
            else:
                self.module.exit_json(msg=message_details.get('Message'), error_info=filter_err, failed=True)
        return import_status

    def __import_license_http(self, import_license_url):
        """
        Imports a license using HTTP.

        Args:
            module (object): The Ansible module object.
            import_license_url (str): The URL for importing the license.

        Returns:
            object: The import status.
        """
        payload = {}
        if self.module.params.get('share_parameters').get('username'):
            payload["Username"] = self.module.params.get('share_parameters').get('username')
        if self.module.params.get('share_parameters').get('password'):
            payload["Password"] = self.module.params.get('share_parameters').get('password')

        payload["TransferProtocol"] = "HTTP" if self.module.params.get('share_parameters').get('share_type') == "http" else "HTTPS"
        payload["LicenseFileURI"] = (
            self.module.params.get('share_parameters').get('share_type') +
            "://" + self.module.params.get('share_parameters').get('ip_address') +
            self.module.params.get('share_parameters').get('share_name') + "/" +
            self.module.params.get('share_parameters').get('file_name')
        )
        import_status = self.idrac.invoke_request(import_license_url, "POST", data=payload)
        return import_status

    def __import_license_cifs(self, import_license_url):
        """
        Imports a license using CIFS share type.

        Args:
            self (object): The instance of the class.
            module (object): The Ansible module object.
            import_license_url (str): The URL for importing the license.

        Returns:
            object: The import status of the license.
        """
        payload = {}
        if self.module.params.get('share_parameters').get('workgroup'):
            payload["Workgroup"] = self.module.params.get('share_parameters').get('workgroup')
        if self.module.params.get('share_parameters').get('username'):
            payload["Username"] = self.module.params.get('share_parameters').get('username')
        if self.module.params.get('share_parameters').get('password'):
            payload["Password"] = self.module.params.get('share_parameters').get('password')
        payload["LicenseFileURI"] = (
            "//" + self.module.params.get('share_parameters').get('ip_address') +
            self.module.params.get('share_parameters').get('share_name') +
            "/" + self.module.params.get('share_parameters').get('file_name')
        )
        payload["TransferProtocol"] = "CIFS"
        import_status = self.idrac.invoke_request(import_license_url, "POST", data=payload)
        return import_status

    def __import_license_nfs(self, import_license_url):
        """
        Import a license from an NFS share.

        Args:
            module (object): The Ansible module object.
            import_license_url (str): The URL for importing the license.

        Returns:
            dict: The import status of the license.
        """
        payload = {}
        payload["TransferProtocol"] = "NFS"
        payload["LicenseFileURI"] = (
            self.module.params.get('share_parameters').get('ip_address') +
            self.module.params.get('share_parameters').get('share_name') +
            "/" + self.module.params.get('share_parameters').get('file_name')
        )
        import_status = self.idrac.invoke_request(import_license_url, "POST", data=payload)
        return import_status

    def __check_file_extension(self):
        """
        Check if the file extension of the given file name is valid.

        :param module: The Ansible module object.
        :type module: AnsibleModule

        :return: None
        """
        share_type = self.module.params.get('share_parameters').get('share_type')
        file_name = self.module.params.get('share_parameters').get('file_name')
        valid_extensions = {".txt", ".xml"} if share_type == "local" else {".xml"}
        file_extension = any(file_name.lower().endswith(ext) for ext in valid_extensions)
        if not file_extension:
            self.module.exit_json(msg=INVALID_FILE_MSG, failed=True)

    def __get_import_license_url(self):
        """
        Get the import license URL.

        :param module: The module object.
        :type module: object
        :return: The import license URL.
        :rtype: str
        """
        if self.module.params.get('share_parameters').get('share_type') == "local":
            uri, error_msg = validate_and_get_first_resource_id_uri(self.module, self.idrac, MANAGERS_URI)
            if error_msg:
                self.module.exit_json(msg=error_msg, failed=True)
            resp = get_dynamic_uri(self.idrac, uri)
            url = resp.get('Links', {}).get(OEM, {}).get(MANUFACTURER, {}).get(LICENSE_MANAGEMENT_SERVICE, {}).get(ODATA, {})
            action_resp = get_dynamic_uri(self.idrac, url)
            import_url = action_resp.get(ACTIONS, {}).get(IMPORT_LOCAL, {}).get('target', {})
        else:
            v1_resp = get_dynamic_uri(self.idrac, REDFISH)
            license_service_url = v1_resp.get('LicenseService', {}).get(ODATA, {})
            license_service_resp = get_dynamic_uri(self.idrac, license_service_url)
            import_url = license_service_resp.get(ACTIONS, {}).get(IMPORT_NETWORK_SHARE, {}).get('target', {})
        return import_url

    def get_job_status(self, license_job_response):
        res_uri = validate_and_get_first_resource_id_uri(self.module, self.idrac, MANAGERS_URI)
        job_tracking_uri = license_job_response.headers.get("Location")
        job_id = job_tracking_uri.split("/")[-1]
        job_uri = IDRAC_JOB_URI.format(job_id=job_id, res_uri=res_uri[0])
        job_failed, msg, job_dict, wait_time = idrac_redfish_job_tracking(self.idrac, job_uri)
        job_dict = remove_key(job_dict, regex_pattern=ODATA_REGEX)
        if job_failed:
            if job_dict.get('MessageId') == 'LIC018':
                self.module.exit_json(msg=job_dict.get('Message'), skipped=True, job_details=job_dict)
            else:
                self.module.exit_json(
                    msg=job_dict.get('Message'),
                    failed=True,
                    job_details=job_dict)
        return job_dict


class LicenseType:
    _license_classes = {
        "import": ImportLicense,
        "export": ExportLicense,
        "delete": DeleteLicense,
    }

    @staticmethod
    def license_operation(idrac, module):
        """
        Perform a license operation based on the given parameters.

        :param idrac: The IDRAC object.
        :type idrac: IDRAC
        :param module: The Ansible module object.
        :type module: AnsibleModule
        :return: The license class object based on the license type.
        :rtype: LicenseType
        """
        license_type = next((param for param in ["import", "export", "delete"] if module.params[param]), None)
        if not license_type:
            module.exit_json(msg=NO_OPERATION_SKIP_MSG, skipped=True)
        license_class = LicenseType._license_classes.get(license_type)
        return license_class(idrac, module)


def main():
    """
    Main function that serves as the entry point for the program.

    This function retrieves the argument specification using the `get_argument_spec` function and updates it with the `idrac_auth_params`.
    It then creates an `AnsibleModule` object with the updated argument specification, specifying the mutually exclusive arguments,
    required arguments if conditions are met, and setting `supports_check_mode` to `False`.

    The function then attempts to establish a connection with the iDRAC Redfish API using the `iDRACRedfishAPI` class.
    If the iDRAC version is supported, the function creates a `LicenseType` object using the `license_operation` method of the
    `LicenseType` class and calls the `execute` method on the `license_obj` object, passing in the `module` object.

    If an `HTTPError` occurs, the function loads the error response as JSON, removes a specific key using a regular expression pattern,
    and exits with the error message, the filtered error information, and sets `failed` to `True`.

    If a `URLError` occurs, the function exits with the error message and sets `unreachable` to `True`.

    If any of the following errors occur: `SSLValidationError`, `ConnectionError`, `TypeError`, `ValueError`, or `OSError`, the function
    exits with the error message and sets `failed` to `True`.

    Parameters:
        None

    Returns:
        None
    """
    specs = get_argument_spec()

    module = IdracAnsibleModule(
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
            license_obj = LicenseType.license_operation(idrac, module)
            if license_obj:
                license_obj.execute()
    except HTTPError as err:
        filter_err = remove_key(json.load(err), regex_pattern=ODATA_REGEX)
        module.exit_json(msg=str(err), error_info=filter_err, failed=True)
    except URLError as err:
        module.exit_json(msg=AUTH_ERROR_MSG.format(ip=module.params.get("idrac_ip"), error=str(err)), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


def get_argument_spec():
    """
    Returns a dictionary containing the argument spec for the get_argument_spec function.
    The argument spec is a dictionary that defines the parameters and their types and options for the function.
    The dictionary has the following keys:
        - "license_id": A string representing the license ID.
        - "delete": A boolean representing whether to delete the license.
        - "export": A boolean representing whether to export the license.
        - "import": A boolean representing whether to import the license.
        - "share_parameters": A dictionary representing the share parameters.
            - "type": A string representing the share type.
            - "options": A dictionary representing the options for the share parameters.
                - "share_type": A string representing the share type.
                - "file_name": A string representing the file name.
                - "ip_address": A string representing the IP address.
                - "share_name": A string representing the share name.
                - "workgroup": A string representing the workgroup.
                - "username": A string representing the username.
                - "password": A string representing the password.
                - "ignore_certificate_warning": A string representing whether to ignore certificate warnings.
                - "proxy_support": A string representing the proxy support.
                - "proxy_type": A string representing the proxy type.
                - "proxy_server": A string representing the proxy server.
                - "proxy_port": A integer representing the proxy port.
                - "proxy_username": A string representing the proxy username.
                - "proxy_password": A string representing the proxy password.
            - "required_if": A list of lists representing the required conditions for the share parameters.
            - "required_together": A list of lists representing the required conditions for the share parameters.
        - "resource_id": A string representing the resource ID.
    """
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
                "proxy_port": {"type": 'int', "default": 80},
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
