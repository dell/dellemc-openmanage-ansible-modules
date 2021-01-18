# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.0.0
# Copyright (C) 2019-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.six.moves.urllib.parse import urlencode

SESSION_RESOURCE_COLLECTION = {
    "SESSION": "SessionService/Sessions",
    "SESSION_ID": "SessionService/Sessions('{Id}')",
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
        return self.status_code in (200, 201, 202, 204)

    @property
    def token_header(self):
        return self.resp.headers.get('X-Auth-Token')


class RestOME(object):
    """Handles OME API requests"""

    def __init__(self, module_params=None, req_session=False):
        self.module_params = module_params
        self.hostname = self.module_params["hostname"]
        self.username = self.module_params["username"]
        self.password = self.module_params["password"]
        self.port = self.module_params["port"]
        self.req_session = req_session
        self.session_id = None
        self.protocol = 'https'
        self._headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def _get_base_url(self):
        """builds base url"""
        return '{0}://{1}:{2}/api'.format(self.protocol, self.hostname, self.port)

    def _build_url(self, path, query_param=None):
        """builds complete url"""
        url = path
        base_uri = self._get_base_url()
        if path:
            url = '{0}/{1}'.format(base_uri, path)
        if query_param:
            """Ome filtering does not work as expected when '+' is passed,
            urlencode will encode spaces as '+' so replace it to '%20'"""
            url += "?{0}".format(urlencode(query_param).replace('+', '%20'))
        return url

    def _url_common_args_spec(self, method, api_timeout, headers=None):
        """Creates an argument common spec"""
        req_header = self._headers
        if headers:
            req_header.update(headers)
        url_kwargs = {
            "method": method,
            "validate_certs": False,
            "use_proxy": True,
            "headers": req_header,
            "timeout": api_timeout,
            "follow_redirects": 'all',
        }
        return url_kwargs

    def _args_without_session(self, method, api_timeout=30, headers=None):
        """Creates an argument spec in case of basic authentication"""
        req_header = self._headers
        if headers:
            req_header.update(headers)
        url_kwargs = self._url_common_args_spec(method, api_timeout, headers=headers)
        url_kwargs["url_username"] = self.username
        url_kwargs["url_password"] = self.password
        url_kwargs["force_basic_auth"] = True
        return url_kwargs

    def _args_with_session(self, method, api_timeout=30, headers=None):
        """Creates an argument spec, in case of authentication with session"""
        url_kwargs = self._url_common_args_spec(method, api_timeout, headers=headers)
        url_kwargs["force_basic_auth"] = False
        return url_kwargs

    def invoke_request(self, method, path, data=None, query_param=None, headers=None,
                       api_timeout=30, dump=True):
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
                url_kwargs = self._args_without_session(method, api_timeout, headers=headers)
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
                       'Password': self.password,
                       'SessionType': 'API', }
            path = SESSION_RESOURCE_COLLECTION["SESSION"]
            resp = self.invoke_request('POST', path, data=payload)
            if resp and resp.success:
                self.session_id = resp.json_data.get("Id")
                self._headers["X-Auth-Token"] = resp.token_header
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

    def get_all_report_details(self, uri):
        """
        This implementation mainly dependent on '@odata.count' value.
        Currently first request without query string, always returns total number of available
        reports in '@odata.count'.
        """
        try:
            resp = self.invoke_request('GET', uri)
            data = resp.json_data
            report_list = data["value"]
            total_count = data['@odata.count']
            remaining_count = total_count - len(report_list)
            first_page_count = len(report_list)
            while remaining_count > 0:
                resp = self.invoke_request('GET', uri, query_param={"$top": first_page_count, "$skip": len(report_list)})
                data = resp.json_data
                value = data["value"]
                report_list.extend(value)
                remaining_count = remaining_count - len(value)
            return {"resp_obj": resp, "report_list": report_list}
        except (URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError) as err:
            raise err

    def get_job_type_id(self, jobtype_name):
        """This provides an ID of the job type."""
        job_type_id = None
        resp = self.invoke_request('GET', "JobService/JobTypes")
        data = resp.json_data["value"]
        for each in data:
            if each["Name"] == jobtype_name:
                job_type_id = each["Id"]
                break
        return job_type_id

    def get_device_id_from_service_tag(self, service_tag):
        """
        :param service_tag: service tag of the device
        :return: dict
        Id: int: device id
        value: dict: device id details
        not_found_msg: str: message if service tag not found
        """
        device_id = None
        query = "DeviceServiceTag eq '{0}'".format(service_tag)
        response = self.invoke_request("GET", "DeviceService/Devices", query_param={"$filter": query})
        value = response.json_data.get("value", [])
        device_info = {}
        if value:
            device_info = value[0]
            device_id = device_info["Id"]
        return {"Id": device_id, "value": device_info}

    def get_all_items_with_pagination(self, uri):
        """
         This implementation mainly to get all available items from ome for pagination
         supported GET uri
        :param uri: uri which supports pagination
        :return: dict.
        """
        try:
            resp = self.invoke_request('GET', uri)
            data = resp.json_data
            total_items = data.get("value", [])
            total_count = data.get('@odata.count', 0)
            next_link = data.get('@odata.nextLink', "")
            while next_link:
                resp = self.invoke_request('GET', uri)
                data = resp.json_data
                value = data["value"]
                total_items.extend(value)
            return {"total_count": total_count, "value": total_items}
        except (URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError) as err:
            raise err

    def get_device_type(self):
        """
        Returns device type map where as key is type and value is type name
        eg: {1000: "SERVER", 2000: "CHASSIS", 4000: "NETWORK_IOM", "8000": "STORAGE_IOM", 3000: "STORAGE"}
        :return: dict, first item dict gives device type map
        """
        device_map = {}
        response = self.invoke_request("GET", "DeviceService/DeviceType")
        if response.json_data.get("value"):
            device_map = dict([(item["DeviceType"], item["Name"]) for item in response.json_data["value"]])
        return device_map
