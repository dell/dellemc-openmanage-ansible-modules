# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 9.8.0
# Copyright (C) 2024-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

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
from ansible.module_utils.urls import open_url
from ansible.module_utils.six.moves.urllib.parse import urlencode
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import config_ipv6


class OpenURLResponse(object):
    """Handles HTTPResponse"""

    def __init__(self, response):
        """
        Initializes a new instance of the class.

        Args:
            response (object): The response object to read the body from.

        Returns:
            None
        """
        self.body = None
        self.resp = response
        if self.resp:
            self.body = self.resp.read()

    @property
    def json_data(self):
        """
        Returns the JSON data parsed from the `body` attribute of the object.

        Returns:
            dict: The parsed JSON data.

        Raises:
            ValueError: If the `body` attribute cannot be parsed as JSON.
        """
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
    def token_header(self):
        return self.resp.headers.get('X-Auth-Token')


class RestAPI:
    def __init__(self, root_uri, module_params, req_session=False,
                 protocol="https", basic_headers=None):
        self.hostname = config_ipv6(str(module_params.get("hostname", "")).strip(']['))
        self.username = module_params.get("username")
        self.password = module_params.get("password")
        self.port = module_params.get("port")
        self.validate_certs = module_params.get("validate_certs")
        self.ca_path = module_params.get("ca_path")
        self.timeout = module_params.get("timeout")
        self.req_session = req_session
        self.session_id = None
        self.protocol = protocol
        self.root_uri = root_uri
        self._headers = basic_headers or {}

    def __build_url(self, path, query_param=None):
        url = '{0}://{1}:{2}'.format(self.protocol, self.hostname, self.port)
        if path:
            url = '{0}{1}'.format(url, path)
        if query_param:
            url += "?{0}".format(urlencode(query_param).replace('+', '%20'))
        return url

    def _get_omam_ca_env(self):
        """Check if the value is set in REQUESTS_CA_BUNDLE or CURL_CA_BUNDLE or OMAM_CA_BUNDLE or returns None"""
        return os.environ.get("REQUESTS_CA_BUNDLE") or os.environ.get("CURL_CA_BUNDLE") or os.environ.get("OMAM_CA_BUNDLE")

    def _url_common_args_spec(self, method, api_timeout=None, headers=None):
        """Creates an argument common spec"""
        base_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self._headers.update(base_headers)
        if isinstance(headers, dict):
            self._headers.update(headers)
        return {
            "method": method,
            "validate_certs": self.validate_certs,
            "ca_path": self.ca_path or self._get_omam_ca_env(),
            "use_proxy": True,
            "headers": self._headers,
            "timeout": api_timeout or self.timeout,
            "follow_redirects": 'all',
        }

    def _args_without_session(self, method, api_timeout, headers=None):
        """Creates an argument spec in case of basic authentication"""
        url_kwargs = self._url_common_args_spec(method, api_timeout, headers=headers)
        url_kwargs["url_username"] = self.username
        url_kwargs["url_password"] = self.password
        url_kwargs["force_basic_auth"] = True
        return url_kwargs

    def _args_with_session(self, method, api_timeout, headers=None):
        """Creates an argument spec, in case of authentication with session"""
        url_kwargs = self._url_common_args_spec(method, api_timeout, headers=headers)
        url_kwargs["force_basic_auth"] = False
        return url_kwargs

    def validate_input(self):
        if not (1 <= self.port <= 65535):
            raise ValueError("Invalid port number. Enter the valid port number.")
        if self.timeout is None or self.timeout <= 0:
            raise ValueError("Invalid timeout value. Enter the valid positive integer.")

    def _base_invoke_request(self, method, path, data=None, query_param=None, headers=None,
                             api_timeout=None, dump=True, auth_token_header='X-Auth-Token'):
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
        self.validate_input()
        if self.req_session and auth_token_header in self._headers:
            url_kwargs = self._args_with_session(method, api_timeout, headers=headers)
        else:
            url_kwargs = self._args_without_session(method, api_timeout, headers=headers)
        if data and dump:
            data = json.dumps(data)
        path = self.root_uri + path
        url = self.__build_url(path, query_param=query_param)
        resp = open_url(url, data=data, **url_kwargs)
        resp_data = OpenURLResponse(resp)
        return resp_data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False
