# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 9.8.0
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

from ansible_collections.dellemc.openmanage.plugins.module_utils.rest_api import RestAPI
from ansible.module_utils.common.parameters import env_fallback
from ansible.module_utils.basic import AnsibleModule

root_omevv_uri = "/omevv/GatewayService/v1"


class RestOMEVV(RestAPI):
    def __init__(self, module_params, protocol="https",
                 root_uri=root_omevv_uri):
        self.uuid = module_params.get("vcenter_uuid", "")
        super().__init__(
            root_uri=root_uri,
            module_params=module_params,
            req_session=False,
            protocol=protocol
        )

    def invoke_request(self, method, path, data=None, query_param=None, headers=None,
                       api_timeout=None, dump=True):
        """
        Sends a request through the base invoke request method.

        Args:
            method (str): The HTTP method to use for the request.
            path (str): The path to request without query parameter.
            data (dict, optional): The payload to send with the request. Defaults to None.
            query_param (dict, optional): The dictionary of query parameters to send with the request. Defaults to None.
            headers (dict, optional): The dictionary of HTTP headers to send with the request. Defaults to None.
            api_timeout (int, optional): The timeout value for the request. Defaults to None.
            dump (bool, optional): Whether to dump the payload data. Defaults to True.

        Returns:
            Response: The response object from the request.
        """
        if self.uuid:
            headers = headers or {}
            headers["x_omivv-api-vcenter-identifier"] = self.uuid
        return self._base_invoke_request(method, path, data, query_param, headers,
                                         api_timeout, dump)


class OMEVVAnsibleModule(AnsibleModule):
    def __init__(self, argument_spec, bypass_checks=False, no_log=False,
                 mutually_exclusive=None, required_together=None,
                 required_one_of=None, add_file_common_args=False,
                 supports_check_mode=False, required_if=None, required_by=None,
                 uuid_required=True):
        temp_argument_spec = {
            "hostname": {"required": True, "type": "str"},
            "vcenter_username": {"required": False, "type": "str", "fallback": (env_fallback, ['OMEVV_VCENTER_USERNAME'])},
            "vcenter_password": {"required": False, "type": "str", "no_log": True, "fallback": (env_fallback, ['OMEVV_VCENTER_PASSWORD'])},
            "port": {"type": "int", "default": 443},
            "validate_certs": {"type": "bool", "default": True},
            "ca_path": {"type": "path"},
            "timeout": {"type": "int", "default": 30},
        }
        argument_spec.update(temp_argument_spec)
        if uuid_required:
            argument_spec.update({"vcenter_uuid": {"required": True, "type": "str",
                                                   "fallback": (env_fallback, ['OMEVV_VCENTER_UUID'])}})
        auth_required_together = [("username", "password")]

        if mutually_exclusive is None:
            mutually_exclusive = []
        if required_together is None:
            required_together = []
        required_together.extend(auth_required_together)
        if required_one_of is None:
            required_one_of = []
        if required_by is None:
            required_by = {}
        if required_if is None:
            required_if = {}

        super().__init__(argument_spec, bypass_checks, no_log,
                         mutually_exclusive, required_together,
                         required_one_of, add_file_common_args,
                         supports_check_mode, required_if, required_by)
