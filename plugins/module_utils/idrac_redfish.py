# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.5.0
# Copyright (C) 2019-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import re
import time
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.six.moves.urllib.parse import urlencode

SESSION_RESOURCE_COLLECTION = {
    "SESSION": "/redfish/v1/Sessions",
    "SESSION_ID": "/redfish/v1/Sessions/{Id}",
}
MANAGER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"
EXPORT_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager.ExportSystemConfiguration"
IMPORT_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager.ImportSystemConfiguration"


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
        self.port = module_params['idrac_port']
        self.validate_certs = module_params.get("validate_certs", False)
        self.use_proxy = module_params.get("use_proxy", True)
        self.req_session = req_session
        self.session_id = None
        self.protocol = 'https'
        self._headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

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
        url_kwargs = {
            "method": method,
            "validate_certs": self.validate_certs,
            "use_proxy": self.use_proxy,
            "headers": req_header,
            "timeout": api_timeout,
            "follow_redirects": 'all',
        }
        return url_kwargs

    def _args_without_session(self, path, method, api_timeout=30, headers=None):
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

    def _args_with_session(self, method, api_timeout=30, headers=None):
        """Creates an argument spec, in case of authentication with session"""
        url_kwargs = self._url_common_args_spec(method, api_timeout, headers=headers)
        url_kwargs["force_basic_auth"] = False
        return url_kwargs

    def invoke_request(self, uri, method, data=None, query_param=None, headers=None, api_timeout=30, dump=True):
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
        if self.req_session:
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
        model, firmware_version = None, None
        response = self.invoke_request(MANAGER_URI, 'GET')
        if response.status_code == 200:
            generation = int(re.search(r"\d+(?=G)", response.json_data["Model"]).group())
            firmware_version = response.json_data["FirmwareVersion"]
        return generation, firmware_version

    def wait_for_job_complete(self, task_uri, job_wait=False):
        """
        This function wait till the job completion.
        :param task_uri: uri to track job.
        :param job_wait: True or False decide whether to wait till the job completion.
        :return: object
        """
        response = None
        while job_wait:
            response = self.invoke_request(task_uri, "GET")
            if response.json_data.get("TaskState") == "Running":
                time.sleep(10)
            else:
                break
        return response

    def wait_for_job_completion(self, job_uri, job_wait=False, reboot=False, apply_update=False):
        """
        This function wait till the job completion.
        :param job_uri: uri to track job.
        :param job_wait: True or False decide whether to wait till the job completion.
        :return: object
        """
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
                   job_wait=False, share=None):
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
        response = self.invoke_request(EXPORT_URI, "POST", data=payload)
        if response.status_code == 202 and job_wait:
            task_uri = response.headers["Location"]
            response = self.wait_for_job_complete(task_uri, job_wait=job_wait)
        return response

    def import_scp_share(self, shutdown_type=None, host_powerstate=None, job_wait=True,
                         target=None, share=None):
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
        response = self.invoke_request(IMPORT_URI, "POST", data=payload)
        if response.status_code == 202 and job_wait:
            task_uri = response.headers["Location"]
            response = self.wait_for_job_complete(task_uri, job_wait=job_wait)
        return response

    def import_scp(self, import_buffer=None, target=None, job_wait=False):
        """
        This method imports system configuration details to the system.
        :param import_buffer: import buffer payload content xml or json format
        :param target: IDRAC or NIC or ALL or BIOS or RAID.
        :param job_wait: True or False decide whether to wait till the job completion.
        :return: json response
        """
        payload = {"ImportBuffer": import_buffer, "ShareParameters": {"Target": target}}
        response = self.invoke_request(IMPORT_URI, "POST", data=payload)
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
