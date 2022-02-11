# -*- coding: utf-8 -*-

# Dell EMC OpenManage Ansible Modules
# Version 5.0.1
# Copyright (C) 2019-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

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
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.six.moves.urllib.parse import urlencode

redfish_auth_params = {
    "baseuri": {"required": True, "type": "str"},
    "username": {"required": True, "type": "str"},
    "password": {"required": True, "type": "str", "no_log": True},
    "validate_certs": {"type": "bool", "default": True},
    "ca_path": {"type": "path"},
    "timeout": {"type": "int", "default": 30},
}

SESSION_RESOURCE_COLLECTION = {
    "SESSION": "/redfish/v1/Sessions",
    "SESSION_ID": "/redfish/v1/Sessions/{Id}",
}


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


class Redfish(object):
    """Handles iDRAC Redfish API requests"""

    def __init__(self, module_params=None, req_session=False):
        self.module_params = module_params
        self.hostname = self.module_params["baseuri"]
        self.username = self.module_params["username"]
        self.password = self.module_params["password"]
        self.validate_certs = self.module_params.get("validate_certs", True)
        self.ca_path = self.module_params.get("ca_path")
        self.timeout = self.module_params.get("timeout", 30)
        self.use_proxy = self.module_params.get("use_proxy", True)
        self.req_session = req_session
        self.session_id = None
        self.protocol = 'https'
        self.root_uri = '/redfish/v1/'
        self._headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def _get_base_url(self):
        """builds base url"""
        return '{0}://{1}'.format(self.protocol, self.hostname)

    def _build_url(self, path, query_param=None):
        """builds complete url"""
        url = path
        base_uri = self._get_base_url()
        if path:
            url = base_uri + path
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
        if self.req_session:
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
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Deletes a session id, which is in use for request"""
        if self.session_id:
            path = SESSION_RESOURCE_COLLECTION["SESSION_ID"].format(Id=self.session_id)
            self.invoke_request('DELETE', path)
        return False

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
