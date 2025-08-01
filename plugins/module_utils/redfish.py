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
import os
import re
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.six.moves.urllib.parse import urlencode
from ansible.module_utils.common.parameters import env_fallback
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import config_ipv6
from ansible.module_utils.basic import AnsibleModule

redfish_auth_params = {
    "baseuri": {"required": True, "type": "str"},
    "username": {"required": True, "type": "str", "fallback": (env_fallback, ['IDRAC_USERNAME'])},
    "password": {"required": True, "type": "str", "no_log": True, "fallback": (env_fallback, ['IDRAC_PASSWORD'])},
    "validate_certs": {"type": "bool", "default": True},
    "ca_path": {"type": "path"},
    "timeout": {"type": "int", "default": 30},
}

SESSION_RESOURCE_COLLECTION = {
    "SESSION": "/redfish/v1/SessionService/Sessions",
    "SESSION_ID": "/redfish/v1/SessionService/Sessions/{Id}",
}

HOST_UNRESOLVED_MSG = "Unable to resolve hostname or IP {0}."
MANAGER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"
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
    def success(self):
        status = self.status_code
        return status >= 200 & status <= 299

    @property
    def headers(self):
        return self.resp.headers

    @property
    def status_code(self):
        return self.resp.getcode()

    @property
    def reason(self):
        return self.resp.reason


class Redfish(object):
    """Handles iDRAC Redfish API requests"""

    def __init__(self, module_params=None, req_session=False):
        self.module_params = module_params
        self.hostname = self.module_params["baseuri"]
        self.username = self.module_params["username"]
        self.password = self.module_params["password"]
        self.x_auth_token = self.module_params.get("x_auth_token")
        self.validate_certs = self.module_params.get("validate_certs", True)
        self.ca_path = self.module_params.get("ca_path")
        self.timeout = self.module_params.get("timeout", 30)
        self.use_proxy = self.module_params.get("use_proxy", True)
        self.req_session = req_session
        self.session_id = None
        self.protocol = 'https'
        self.root_uri = '/redfish/v1/'
        self._headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self.hostname = config_ipv6(self.hostname)

    def _get_base_url(self):
        """builds base url"""
        return '{0}://{1}'.format(self.protocol, self.hostname)

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

    def _build_url(self, path, query_param=None):
        """builds complete url"""
        url = path
        base_uri = self._get_base_url()
        if path:
            url = base_uri + path
        if query_param:
            url += "?{0}".format(urlencode(query_param))
        return url

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

    def invoke_request(self, method, path, data=None, query_param=None, headers=None,
                       api_timeout=None, dump=True):
        """
        Sends a request through open_url
        Returns :class:`OpenURLResponse` object.
        :arg method: HTTP verb to use for the request
        :arg path: path to request without query parameter
        :arg data: (optional) Payload to send with the request
        :arg query_param: (optional) Dictionary of query parameter to send with request
        :arg headers: (optional) Dictionary of HTTP Headers to send with the
            request
        :arg api_timeout: (optional) How long to wait for the server to send
            data before giving up
        :arg dump: (Optional) boolean value for dumping payload data.
        :returns: OpenURLResponse
        """
        try:
            if 'X-Auth-Token' in self._headers:
                url_kwargs = self._args_with_session(method, api_timeout, headers=headers)
            else:
                url_kwargs = self._args_without_session(path, method, api_timeout, headers=headers)
            if data and dump:
                data = json.dumps(data)
            url = self._build_url(path, query_param=query_param)
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
            resp = self.invoke_request('POST', path, data=payload)
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
        """Deletes a session id, which is in use for request for redfish session"""
        if self.session_id:
            path = SESSION_RESOURCE_COLLECTION["SESSION_ID"].format(Id=self.session_id)
            self.invoke_request('DELETE', path)
        return False

    @property
    def get_server_generation(self):
        """
        This method fetches the connected server generation.
        :return: 14, 4.11.11.11, iDRAC 9
        """
        firmware_version = None
        response = self.invoke_request(method='GET', path=MANAGER_URI)
        if response.status_code == 200:
            generation = int(re.search(r"\d+(?=G)", response.json_data["Model"]).group())
            firmware_version = response.json_data["FirmwareVersion"]
        hw_model = ""
        try:
            hw_model_out = self.invoke_request(method='GET', path=GET_IDRAC_MANAGER_ATTRIBUTES_9_10)
            if hw_model_out.status_code == 200:
                hw_model = hw_model_out.json_data.get('Attributes', {}).get('Info.1.HWModel', "iDRAC 9")
        except HTTPError:
            hw_model = "iDRAC 8"
        return generation, firmware_version, hw_model

    def strip_substr_dict(self, odata_dict, chkstr='@odata.'):
        cp = odata_dict.copy()
        klist = cp.keys()
        for k in klist:
            if chkstr in str(k).lower():
                odata_dict.pop(k)
        return odata_dict

    def _get_omam_ca_env(self):
        """Check if the value is set in REQUESTS_CA_BUNDLE or CURL_CA_BUNDLE or OMAM_CA_BUNDLE or returns None"""
        return os.environ.get("REQUESTS_CA_BUNDLE") or os.environ.get("CURL_CA_BUNDLE") or os.environ.get("OMAM_CA_BUNDLE")


class RedfishAnsibleModule(AnsibleModule):
    def __init__(self, argument_spec, bypass_checks=False, no_log=False,
                 mutually_exclusive=None, required_together=None,
                 required_one_of=None, add_file_common_args=False,
                 supports_check_mode=False, required_if=None, required_by=None):
        redfish_argument_spec = {
            "baseuri": {"required": True, "type": "str"},
            "username": {"required": False, "type": "str", "fallback": (env_fallback, ['IDRAC_USERNAME'])},
            "password": {"required": False, "type": "str", "no_log": True, "fallback": (env_fallback, ['IDRAC_PASSWORD'])},
            "x_auth_token": {"required": False, "type": "str", "no_log": True, "fallback": (env_fallback, ['IDRAC_X_AUTH_TOKEN'])},
            "validate_certs": {"type": "bool", "default": True},
            "ca_path": {"type": "path"},
            "timeout": {"type": "int", "default": 30},
        }
        argument_spec.update(redfish_argument_spec)

        auth_mutually_exclusive = [("username", "x_auth_token"), ("password", "x_auth_token")]
        auth_required_one_of = [("username", "x_auth_token")]
        auth_required_together = [("username", "password")]

        if mutually_exclusive is None:
            mutually_exclusive = []
        mutually_exclusive.extend(auth_mutually_exclusive)
        if required_one_of is None:
            required_one_of = []
        required_one_of.extend(auth_required_one_of)
        if required_together is None:
            required_together = []
        required_together.extend(auth_required_together)
        if required_by is None:
            required_by = {}

        super().__init__(argument_spec, bypass_checks, no_log,
                         mutually_exclusive, required_together,
                         required_one_of, add_file_common_args,
                         supports_check_mode, required_if, required_by)
