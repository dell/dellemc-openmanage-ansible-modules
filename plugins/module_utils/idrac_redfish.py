# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 9.12.3
# Copyright (C) 2019-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:

#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.

#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import re
import time
import os
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.six.moves.urllib.parse import urlencode
from ansible.module_utils.common.parameters import env_fallback
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import config_ipv6
from ansible.module_utils.basic import AnsibleModule

idrac_auth_params = {
    "idrac_ip": {"required": True, "type": 'str'},
    "idrac_user": {"required": True, "type": 'str', "fallback": (env_fallback, ['IDRAC_USERNAME'])},
    "idrac_password": {"required": True, "type": 'str', "aliases": ['idrac_pwd'], "no_log": True, "fallback": (env_fallback, ['IDRAC_PASSWORD'])},
    "idrac_port": {"required": False, "default": 443, "type": 'int'},
    "validate_certs": {"type": "bool", "default": True},
    "ca_path": {"type": "path"},
    "timeout": {"type": "int", "default": 30},

}

SESSION_RESOURCE_COLLECTION = {
    "SESSION": "/redfish/v1/SessionService/Sessions",
    "SESSION_ID": "/redfish/v1/SessionService/Sessions/{Id}",
}
MANAGER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"
EXPORT_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager.ExportSystemConfiguration"
IMPORT_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager.ImportSystemConfiguration"
IMPORT_PREVIEW = "/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager.ImportSystemConfigurationPreview"
GET_IDRAC_MANAGER_ATTRIBUTES_9_10 = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/iDRAC.Embedded.1"


class OpenURLResponse(object):
    """Handles HTTPResponse"""

    def __init__(self, resp):
        self.body = None
        self.resp = resp
        if self.resp:
            self.body = self.resp.read()

    @property
    def json_data(self):
        try:
            return json.loads(self.body)
        except ValueError:
            raise ValueError("Unable to parse json")

    @property
    def status_code(self):
        return self.resp.getcode()

    @property
    def success(self):
        status = self.status_code
        return status >= 200 & status <= 299

    @property
    def headers(self):
        return self.resp.headers

    @property
    def reason(self):
        return self.resp.reason


class iDRACRedfishAPI(object):
    """REST api for iDRAC modules."""

    def __init__(self, module_params, req_session=False):
        self.ipaddress = module_params['idrac_ip']
        self.username = module_params['idrac_user']
        self.password = module_params['idrac_password']
        self.x_auth_token = module_params.get('x_auth_token')
        self.port = module_params['idrac_port']
        self.validate_certs = module_params.get("validate_certs", False)
        self.ca_path = module_params.get("ca_path")
        self.timeout = module_params.get("timeout", 30)
        self.use_proxy = module_params.get("use_proxy", True)
        self.req_session = req_session
        self.session_id = None
        self.protocol = 'https'
        self._headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self.ipaddress = config_ipv6(self.ipaddress)

    def _get_url(self, uri):
        return "{0}://{1}:{2}{3}".format(self.protocol, self.ipaddress, self.port, uri)

    def _build_url(self, path, query_param=None):
        """builds complete url"""
        url = path
        base_uri = self._get_url(url)
        if path:
            url = base_uri
        if query_param:
            url += "?{0}".format(urlencode(query_param))
        return url

    def _url_common_args_spec(self, method, api_timeout, headers=None):
        """Creates an argument common spec"""
        req_header = self._headers
        if headers:
            req_header.update(headers)
        if api_timeout is None:
            api_timeout = self.timeout
        if self.ca_path is None:
            self.ca_path = self._get_omam_ca_env()
        url_kwargs = {
            "method": method,
            "validate_certs": self.validate_certs,
            "ca_path": self.ca_path,
            "use_proxy": self.use_proxy,
            "headers": req_header,
            "timeout": api_timeout,
            "follow_redirects": 'all',
        }
        return url_kwargs

    def _args_without_session(self, path, method, api_timeout, headers=None):
        """Creates an argument spec in case of basic authentication"""
        req_header = self._headers
        if headers:
            req_header.update(headers)
        url_kwargs = self._url_common_args_spec(method, api_timeout, headers=headers)
        if not (path == SESSION_RESOURCE_COLLECTION["SESSION"] and method == 'POST'):
            url_kwargs["url_username"] = self.username
            url_kwargs["url_password"] = self.password
            url_kwargs["force_basic_auth"] = True
        return url_kwargs

    def _args_with_session(self, method, api_timeout, headers=None):
        """Creates an argument spec, in case of authentication with session"""
        url_kwargs = self._url_common_args_spec(method, api_timeout, headers=headers)
        url_kwargs["force_basic_auth"] = False
        return url_kwargs

    def invoke_request(self, uri, method, data=None, query_param=None, headers=None, api_timeout=None, dump=True):
        try:
            if 'X-Auth-Token' in self._headers:
                url_kwargs = self._args_with_session(method, api_timeout, headers=headers)
            else:
                url_kwargs = self._args_without_session(uri, method, api_timeout, headers=headers)
            if data and dump:
                data = json.dumps(data)
            url = self._build_url(uri, query_param=query_param)
            resp = open_url(url, data=data, **url_kwargs)
            resp_data = OpenURLResponse(resp)
        except (HTTPError, URLError, SSLValidationError, ConnectionError) as err:
            raise err
        return resp_data

    def __enter__(self):
        """Creates sessions by passing it to header"""
        if self.req_session and not self.x_auth_token:
            payload = {'UserName': self.username,
                       'Password': self.password}
            path = SESSION_RESOURCE_COLLECTION["SESSION"]
            resp = self.invoke_request(path, 'POST', data=payload)
            if resp and resp.success:
                self.session_id = resp.json_data.get("Id")
                self._headers["X-Auth-Token"] = resp.headers.get('X-Auth-Token')
            else:
                msg = "Could not create the session"
                raise ConnectionError(msg)
        elif self.x_auth_token is not None:
            self._headers["X-Auth-Token"] = self.x_auth_token
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Deletes a session id, which is in use for request"""
        if self.session_id:
            path = SESSION_RESOURCE_COLLECTION["SESSION_ID"].format(Id=self.session_id)
            self.invoke_request(path, 'DELETE')
        return False

    @property
    def get_server_generation(self):
        """
        This method fetches the connected server generation.
        :return: 14, 4.11.11.11
        """
        firmware_version = None
        response = self.invoke_request(MANAGER_URI, 'GET')
        generation = 0
        if response.status_code == 200:
            generation = int(re.search(r"\d+(?=G)", response.json_data["Model"]).group())
            firmware_version = response.json_data["FirmwareVersion"]
        hw_model = ""
        try:
            hw_model_out = self.invoke_request(GET_IDRAC_MANAGER_ATTRIBUTES_9_10, 'GET')
            if hw_model_out.status_code == 200:
                hw_model = hw_model_out.json_data.get('Attributes', {}).get('Info.1.HWModel', "iDRAC 9")
        except HTTPError:
            hw_model = "iDRAC 8"

        return generation, firmware_version, hw_model

    def wait_for_job_complete(self, task_uri, job_wait=False):
        """
        This function wait till the job completion.
        :param task_uri: uri to track job.
        :param job_wait: True or False decide whether to wait till the job completion.
        :return: object
        """
        response = None
        while job_wait:
            try:
                response = self.invoke_request(task_uri, "GET")
                if response.json_data.get("TaskState") == "Running" or \
                        response.json_data.get("TaskState") == "New":
                    time.sleep(10)
                else:
                    break
            except ValueError:
                response = response.body
                break
        return response

    def wait_for_job_completion(self, job_uri, job_wait=False, reboot=False, apply_update=False):
        """
        This function wait till the job completion.
        :param job_uri: uri to track job.
        :param job_wait: True or False decide whether to wait till the job completion.
        :return: object
        """
        time.sleep(5)
        response = self.invoke_request(job_uri, "GET")
        while job_wait:
            response = self.invoke_request(job_uri, "GET")
            if response.json_data.get("PercentComplete") == 100 and \
                    response.json_data.get("JobState") == "Completed":
                break
            if response.json_data.get("JobState") == "Starting" and not reboot and apply_update:
                break
            time.sleep(30)
        return response

    def export_scp(self, export_format=None, export_use=None, target=None,
                   job_wait=False, share=None, include_in_export="Default"):
        """
        This method exports system configuration details from the system.
        :param export_format: XML or JSON.
        :param export_use: Default or Clone or Replace.
        :param target: IDRAC or NIC or ALL or BIOS or RAID.
        :param job_wait: True or False decide whether to wait till the job completion.
        :return: exported data in requested format.
        """
        payload = {"ExportFormat": export_format, "ExportUse": export_use,
                   "ShareParameters": {"Target": target}}
        if share is None:
            share = {}
        if share.get("share_ip") is not None:
            payload["ShareParameters"]["IPAddress"] = share["share_ip"]
        if share.get("share_name") is not None and share.get("share_name"):
            payload["ShareParameters"]["ShareName"] = share["share_name"]
        if share.get("share_type") is not None:
            payload["ShareParameters"]["ShareType"] = share["share_type"]
        if share.get("file_name") is not None:
            payload["ShareParameters"]["FileName"] = share["file_name"]
        if share.get("username") is not None:
            payload["ShareParameters"]["Username"] = share["username"]
        if share.get("password") is not None:
            payload["ShareParameters"]["Password"] = share["password"]
        if share.get("ignore_certificate_warning") is not None:
            payload["ShareParameters"]["IgnoreCertificateWarning"] = share["ignore_certificate_warning"]
        if share.get("proxy_support") is not None:
            payload["ShareParameters"]["ProxySupport"] = share["proxy_support"]
        if share.get("proxy_type") is not None:
            payload["ShareParameters"]["ProxyType"] = share["proxy_type"]
        if share.get("proxy_port") is not None:
            payload["ShareParameters"]["ProxyPort"] = share["proxy_port"]
        if share.get("proxy_server") is not None:
            payload["ShareParameters"]["ProxyServer"] = share["proxy_server"]
        if share.get("proxy_username") is not None:
            payload["ShareParameters"]["ProxyUserName"] = share["proxy_username"]
        if share.get("proxy_password") is not None:
            payload["ShareParameters"]["ProxyPassword"] = share["proxy_password"]
        payload["IncludeInExport"] = [include_in_export]
        response = self.invoke_request(EXPORT_URI, "POST", data=payload)
        if response.status_code == 202 and job_wait:
            task_uri = response.headers["Location"]
            response = self.wait_for_job_complete(task_uri, job_wait=job_wait)
        return response

    def import_scp_share(self, shutdown_type=None, host_powerstate=None, job_wait=True,
                         target=None, import_buffer=None, share=None, time_to_wait=300):
        """
        This method imports system configuration using share.
        :param shutdown_type: graceful
        :param host_powerstate: on
        :param file_name: import.xml
        :param job_wait: True
        :param target: iDRAC
        :param share: dictionary which has all the share details.
        :return: json response
        """
        payload = {"ShutdownType": shutdown_type, "EndHostPowerState": host_powerstate,
                   "ShareParameters": {"Target": target}, "TimeToWait": time_to_wait}
        if import_buffer is not None:
            payload["ImportBuffer"] = import_buffer
        if share is None:
            share = {}
        if share.get("share_ip") is not None:
            payload["ShareParameters"]["IPAddress"] = share["share_ip"]
        if share.get("share_name") is not None and share.get("share_name"):
            payload["ShareParameters"]["ShareName"] = share["share_name"]
        if share.get("share_type") is not None:
            payload["ShareParameters"]["ShareType"] = share["share_type"]
        if share.get("file_name") is not None:
            payload["ShareParameters"]["FileName"] = share["file_name"]
        if share.get("username") is not None:
            payload["ShareParameters"]["Username"] = share["username"]
        if share.get("password") is not None:
            payload["ShareParameters"]["Password"] = share["password"]
        if share.get("ignore_certificate_warning") is not None:
            payload["ShareParameters"]["IgnoreCertificateWarning"] = share["ignore_certificate_warning"]
        if share.get("proxy_support") is not None:
            payload["ShareParameters"]["ProxySupport"] = share["proxy_support"]
        if share.get("proxy_type") is not None:
            payload["ShareParameters"]["ProxyType"] = share["proxy_type"]
        if share.get("proxy_port") is not None:
            payload["ShareParameters"]["ProxyPort"] = share["proxy_port"]
        if share.get("proxy_server") is not None:
            payload["ShareParameters"]["ProxyServer"] = share["proxy_server"]
        if share.get("proxy_username") is not None:
            payload["ShareParameters"]["ProxyUserName"] = share["proxy_username"]
        if share.get("proxy_password") is not None:
            payload["ShareParameters"]["ProxyPassword"] = share["proxy_password"]
        response = self.invoke_request(IMPORT_URI, "POST", data=payload)
        return response

    def import_preview(self, import_buffer=None, target=None, share=None, job_wait=False):
        payload = {"ShareParameters": {"Target": target}}
        if import_buffer is not None:
            payload["ImportBuffer"] = import_buffer
        if share is None:
            share = {}
        if share.get("share_ip") is not None:
            payload["ShareParameters"]["IPAddress"] = share["share_ip"]
        if share.get("share_name") is not None and share.get("share_name"):
            payload["ShareParameters"]["ShareName"] = share["share_name"]
        if share.get("share_type") is not None:
            payload["ShareParameters"]["ShareType"] = share["share_type"]
        if share.get("file_name") is not None:
            payload["ShareParameters"]["FileName"] = share["file_name"]
        if share.get("username") is not None:
            payload["ShareParameters"]["Username"] = share["username"]
        if share.get("password") is not None:
            payload["ShareParameters"]["Password"] = share["password"]
        if share.get("ignore_certificate_warning") is not None:
            payload["ShareParameters"]["IgnoreCertificateWarning"] = share["ignore_certificate_warning"]
        if share.get("proxy_support") is not None:
            payload["ShareParameters"]["ProxySupport"] = share["proxy_support"]
        if share.get("proxy_type") is not None:
            payload["ShareParameters"]["ProxyType"] = share["proxy_type"]
        if share.get("proxy_port") is not None:
            payload["ShareParameters"]["ProxyPort"] = share["proxy_port"]
        if share.get("proxy_server") is not None:
            payload["ShareParameters"]["ProxyServer"] = share["proxy_server"]
        if share.get("proxy_username") is not None:
            payload["ShareParameters"]["ProxyUserName"] = share["proxy_username"]
        if share.get("proxy_password") is not None:
            payload["ShareParameters"]["ProxyPassword"] = share["proxy_password"]
        response = self.invoke_request(IMPORT_PREVIEW, "POST", data=payload)
        if response.status_code == 202 and job_wait:
            task_uri = response.headers["Location"]
            response = self.wait_for_job_complete(task_uri, job_wait=job_wait)
        return response

    def import_scp(self, import_buffer=None, target=None, job_wait=False, time_to_wait=300):
        """
        This method imports system configuration details to the system.
        :param import_buffer: import buffer payload content xml or json format
        :param target: IDRAC or NIC or ALL or BIOS or RAID.
        :param job_wait: True or False decide whether to wait till the job completion.
        :return: json response
        """
        payload = {"ImportBuffer": import_buffer, "ShareParameters": {"Target": target}, "TimeToWait": time_to_wait}
        response = self.invoke_request(IMPORT_URI, "POST", data=payload)
        if response.status_code == 202 and job_wait:
            task_uri = response.headers["Location"]
            response = self.wait_for_job_complete(task_uri, job_wait=job_wait)
        return response

    def import_preview_scp(self, import_buffer=None, target=None, job_wait=False):
        """
        This method imports preview system configuration details to the system.
        :param import_buffer: import buffer payload content xml or json format
        :param target: IDRAC or NIC or ALL or BIOS or RAID.
        :param job_wait: True or False decide whether to wait till the job completion.
        :return: json response
        """
        payload = {"ImportBuffer": import_buffer, "ShareParameters": {"Target": target}}
        response = self.invoke_request(IMPORT_PREVIEW, "POST", data=payload)
        if response.status_code == 202 and job_wait:
            task_uri = response.headers["Location"]
            response = self.wait_for_job_complete(task_uri, job_wait=job_wait)
        return response

    def get_idrac_local_account_attr(self, idrac_attribues, fqdd=None):
        """
        This method filtered from all the user attributes from the given idrac attributes.
        :param idrac_attribues: all the idrac attribues in json data format.
        :return: user attributes in dictionary format
        """
        user_attr = None
        if "SystemConfiguration" in idrac_attribues:
            sys_config = idrac_attribues.get("SystemConfiguration")
            for comp in sys_config.get("Components"):
                if comp.get("FQDD") == fqdd:
                    attributes = comp.get("Attributes")
                    break
            user_attr = dict([(attr["Name"], attr["Value"]) for attr in attributes if attr["Name"].startswith("Users.")])
        return user_attr

    def _get_omam_ca_env(self):
        """Check if the value is set in REQUESTS_CA_BUNDLE or CURL_CA_BUNDLE or OMAM_CA_BUNDLE or returns None"""
        return os.environ.get("REQUESTS_CA_BUNDLE") or os.environ.get("CURL_CA_BUNDLE") or os.environ.get("OMAM_CA_BUNDLE")

    def validate_idrac10_and_above(self):
        gen_details = self.get_server_generation
        hw_model = gen_details[2]
        return hw_model == 'iDRAC 10'

    def get_job_uri(self):
        idrac10_or_above = self.validate_idrac10_and_above()
        if idrac10_or_above:
            return "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/{job_id}"
        return "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/{job_id}"

    def find_ip_address(self, sharename):
        pattern_ipv4 = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        ipv4_addresses = re.findall(pattern_ipv4, sharename)
        pattern_ipv6 = r'\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\b'
        ipv6_addresses = re.findall(pattern_ipv6, sharename)
        address = None
        if ipv4_addresses:
            address = ipv4_addresses[0]
        elif ipv6_addresses:
            address = ipv6_addresses[0]
        return address


class IdracAnsibleModule(AnsibleModule):
    def __init__(self, argument_spec, bypass_checks=False, no_log=False,
                 mutually_exclusive=None, required_together=None,
                 required_one_of=None, add_file_common_args=False,
                 supports_check_mode=False, required_if=None, required_by=None):
        idrac_argument_spec = {
            "idrac_ip": {"required": True, "type": 'str'},
            "idrac_user": {"required": False, "type": 'str', "fallback": (env_fallback, ['IDRAC_USERNAME'])},
            "idrac_password": {"required": False, "type": 'str', "aliases": ['idrac_pwd'], "no_log": True, "fallback": (env_fallback, ['IDRAC_PASSWORD'])},
            "x_auth_token": {"required": False, "type": 'str', "no_log": True, "fallback": (env_fallback, ['IDRAC_X_AUTH_TOKEN'])},
            "idrac_port": {"required": False, "default": 443, "type": 'int'},
            "validate_certs": {"type": "bool", "default": True},
            "ca_path": {"type": "path"},
            "timeout": {"type": "int", "default": 30},
        }
        argument_spec.update(idrac_argument_spec)

        auth_mutually_exclusive = [("idrac_user", "x_auth_token"), ("idrac_password", "x_auth_token")]
        auth_required_one_of = [("idrac_user", "x_auth_token")]
        auth_required_together = [("idrac_user", "idrac_password")]

        if mutually_exclusive is None:
            mutually_exclusive = []
        mutually_exclusive.extend(auth_mutually_exclusive)
        if required_together is None:
            required_together = []
        required_together.extend(auth_required_together)
        if required_one_of is None:
            required_one_of = []
        required_one_of.extend(auth_required_one_of)
        if required_by is None:
            required_by = {}

        super().__init__(argument_spec, bypass_checks, no_log,
                         mutually_exclusive, required_together,
                         required_one_of, add_file_common_args,
                         supports_check_mode, required_if, required_by)
