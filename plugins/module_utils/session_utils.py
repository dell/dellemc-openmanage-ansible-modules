# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 9.2.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

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
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import config_ipv6


class OpenURLResponse():
    """
    HTTP response handler class.
    """
    def __init__(self, resp):
        """
        Initializes a new instance of the class.

        Args:
            resp (Response): The response object to read the body from.

        Initializes the following instance variables:
            - body (bytes): The body of the response, or None if the response is None.
            - resp (Response): The response object.

        If the response is not None, the body is set to the content of the response.
        """
        self.body = None
        self.resp = resp
        if self.resp:
            self.body = self.resp.read()

    @property
    def json_data(self):
        """
        Returns the JSON data parsed from the `body` attribute of the object.

        :return: The parsed JSON data.
        :raises ValueError: If the `body` attribute cannot be parsed as JSON.
        """
        try:
            return json.loads(self.body)
        except ValueError as exc:
            raise ValueError("Unable to parse json") from exc

    @property
    def status_code(self):
        """
        Get the status code of the response.

        Returns:
            int: The status code of the response.
        """
        return self.resp.getcode()

    @property
    def success(self):
        """
        Returns a boolean indicating whether the status code of the response is within the range
          of 200-299.

        :return: True if the status code is within the range of 200-299, False otherwise.
        :rtype: bool
        """
        status = self.status_code
        return status >= 200 & status <= 299

    @property
    def headers(self):
        """
        Returns the headers of the response object.

        :return: A dictionary containing the headers of the response object.
        :rtype: dict
        """
        return self.resp.headers

    @property
    def reason(self):
        """
        Get the reason for the response.

        Returns:
            str: The reason for the response.
        """
        return self.resp.reason


class SessionAPI():
    """
    Main class for session operations.
    """
    def __init__(self, module_params, req_session=False):
        """
        Initializes the object with the given module parameters and optional request session.

        Args:
            module_params (dict): A dictionary containing the module parameters.
            req_session (bool, optional): Indicates if a request session is required. Defaults
              to False.

        Initializes the following instance variables:
            - ipaddress (str): The value of the "hostname" key from module_params.
            - username (str): The value of the "username" key from module_params, if the "state" key
              is "present".
            - password (str): The value of the "password" key from module_params, if the "state" key
              is "present".
            - _headers (dict): A dictionary containing the headers for the HTTP requests.
            - port (str): The value of the "port" key from module_params.
            - validate_certs (bool): The value of the "validate_certs" key from module_params, or
              False if not provided.
            - ca_path (str): The value of the "ca_path" key from module_params.
            - timeout (int): The value of the "timeout" key from module_params.
            - use_proxy (bool): The value of the "use_proxy" key from module_params, or True if
              not provided.
            - req_session (bool): The value of the req_session parameter.
            - session_id (None): Initialized as None.
            - protocol (str): Set to 'https'.
            - ipaddress (str): The result of calling the config_ipv6 function with the ipaddress
              value.
        """
        self.ipaddress = module_params.get("hostname")
        self.username = module_params.get("username")
        self.password = module_params.get("password")
        self.port = module_params.get("port")
        self.validate_certs = module_params.get("validate_certs", False)
        self.ca_path = module_params.get("ca_path")
        self.timeout = module_params.get("timeout")
        self.use_proxy = module_params.get("use_proxy", True)
        self.req_session = req_session
        self.session_id = None
        self.protocol = 'https'
        self.ipaddress = config_ipv6(self.ipaddress)
        self.set_headers(module_params)

    def set_headers(self, module_params):
        """
        Set the headers for the HTTP request based on the module parameters.

        Parameters:
            module_params (dict): The module parameters containing the state and auth_token.

        Returns:
            None

        This function sets the headers for the HTTP request based on the state parameter in the
        module_params.
        If the state is "present", the headers will include 'Content-Type' and 'Accept' with values
        'application/json'.
        If the state is not "present", the headers will include 'Content-Type', 'Accept', and
        'X-Auth-Token' with the value from the auth_token parameter in module_params.
        """
        if module_params.get("state") == "present":
            self._headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        else:
            self._headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Auth-Token': module_params.get("auth_token")
            }

    def _get_url(self, uri):
        """
        Generate the full URL by combining the protocol, IP address, port, and URI.

        Parameters:
            uri (str): The URI to be appended to the URL.

        Returns:
            str: The full URL generated by combining the protocol, IP address, port, and URI.
        """
        return f"{self.protocol}://{self.ipaddress}:{self.port}{uri}"

    def _build_url(self, path, query_param=None):
        """
        Builds a URL by concatenating the base URI with the given path and query parameters.

        Args:
            path (str): The path component of the URL.
            query_param (dict, optional): A dictionary of query parameters to be appended to the
            URL. Defaults to None.

        Returns:
            str: The fully constructed URL.

        Raises:
            None

        Examples:
            >>> session = SessionUtils()
            >>> session._build_url("/api/endpoint", {"param1": "value1", "param2": "value2"})
            "/api/endpoint?param1=value1&param2=value2"
        """
        url = path
        base_uri = self._get_url(url)
        if path:
            url = base_uri
        if query_param:
            url += f"?{urlencode(query_param)}"
        return url

    def _url_common_args_spec(self, method, api_timeout, headers=None):
        """
        Generates the common arguments for a URL request.

        Args:
            method (str): The HTTP method for the request.
            api_timeout (int, optional): The timeout for the API request. If None, the default
            timeout is used.
            headers (dict, optional): Additional headers to include in the request.

        Returns:
            dict: A dictionary containing the common arguments for the URL request. The dictionary
            has the following keys:
                - method (str): The HTTP method for the request.
                - validate_certs (bool): Whether to validate the SSL certificates.
                - ca_path (str): The path to the CA certificate bundle.
                - use_proxy (bool): Whether to use a proxy for the request.
                - headers (dict): The headers to include in the request.
                - timeout (int): The timeout for the request.
                - follow_redirects (str): The policy for following redirects.

        """
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

    def _args_session(self, path, method, api_timeout, headers=None):
        """
        Returns a dictionary containing the arguments needed to establish a session.

        :param path: A string representing the path of the API endpoint.
        :param method: A string representing the HTTP method to be used.
        :param api_timeout: An integer representing the timeout for the API request.
        :param headers: An optional dictionary containing additional headers to be included in the
        request.
        :return: A dictionary containing the arguments needed to establish a session, including the
        URL arguments, headers, and API timeout.
        """
        req_header = self._headers
        if headers:
            req_header.update(headers)
        url_kwargs = self._url_common_args_spec(method, api_timeout, headers=headers)
        return url_kwargs

    def invoke_request(self, uri, method, data=None, query_param=None, headers=None, api_timeout=None, dump=True):
        """
        Sends an HTTP request to the specified URI using the specified method.

        Args:
            uri (str): The URI to send the request to.
            method (str): The HTTP method to use for the request.
            data (Optional[dict]): The data to send with the request. Defaults to None.
            query_param (Optional[dict]): The query parameters to include in the request URL.
            Defaults to None.
            headers (Optional[dict]): The headers to include in the request. Defaults to None.
            api_timeout (Optional[int]): The timeout value for the request in seconds.
              Defaults to None.
            dump (bool): Whether to JSON dump the data before sending the request. Defaults to True.

        Returns:
            OpenURLResponse: The response object containing the response data.

        Raises:
            HTTPError: If an HTTP error occurs during the request.
            URLError: If a URL error occurs during the request.
            SSLValidationError: If an SSL validation error occurs during the request.
            ConnectionError: If a connection error occurs during the request.
        """
        try:
            url_kwargs = self._args_session(uri, method, api_timeout, headers=headers)
            if data and dump:
                data = json.dumps(data)
            url = self._build_url(uri, query_param=query_param)
            resp = open_url(url, data=data, **url_kwargs)
            resp_data = OpenURLResponse(resp)
        except (HTTPError, URLError, SSLValidationError, ConnectionError) as err:
            raise err
        return resp_data

    def __enter__(self):
        """
        Returns the current instance of the class, allowing it to be used in a context manager.

        :return: The current instance of the class.
        :rtype: self
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager and return False.

        This method is called when the context manager is exited. It takes in three parameters:
        - exc_type: the type of the exception that occurred, or None if no exception occurred.
        - exc_value: the value of the exception that occurred, or None if no exception occurred.
        - traceback: the traceback of the exception that occurred, or None if no exception occurred.

        This method always returns False.

        Returns:
            bool: False
        """
        return False

    def _get_omam_ca_env(self):
        """
        Returns the value of the environment variable REQUESTS_CA_BUNDLE, or if it is not set,
        the value of the environment variable CURL_CA_BUNDLE, or if that is not set,
        the value of the environment variable OMAM_CA_BUNDLE.

        :return: The value of the environment variable, or None if none of the variables are set.
        :rtype: str or None
        """
        return (os.environ.get("REQUESTS_CA_BUNDLE") or
                os.environ.get("CURL_CA_BUNDLE") or
                os.environ.get("OMAM_CA_BUNDLE"))
