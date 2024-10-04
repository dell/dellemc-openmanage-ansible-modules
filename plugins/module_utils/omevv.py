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

from ansible_collections.dellemc.openmanage.plugins.module_utils.rest_api import RestAPI, RestAnsibleModule
from ansible.module_utils.common.parameters import env_fallback

root_omevv_uri = "/omevv/GatewayService/v1"
session_resource = {}


class RestOMEVV(RestAPI):
    def __init__(self, module_params, protocol="https"):
        self.uuid = module_params.get("vcenter_uuid", "")
        self.omevv_header_dict = {
            "x_omivv-api-vcenter-identifier": self.uuid if self.uuid is not None else ""
        }
        super().__init__(
            root_uri=root_omevv_uri,
            module_params=module_params,
            session_resource_collection=session_resource,
            req_session=False,
            protocol=protocol
        )

    def invoke_request(self, method, path, data=None, query_param=None, headers=None,
                       api_timeout=None, dump=True):
        if isinstance(headers, dict):
            self.omevv_header_dict.update(headers)
        return self._base_invoke_request(method, path, data, query_param, self.omevv_header_dict,
                                         api_timeout, dump)


class OMEVVAnsibleModule(RestAnsibleModule):
    def __init__(self, argument_spec, bypass_checks=False, no_log=False,
                 mutually_exclusive=None, required_together=None,
                 required_one_of=None, add_file_common_args=False,
                 supports_check_mode=False, required_if=None, required_by=None,
                 env_fallback_username='OMEVV_VCENTER_USERNAME',
                 env_fallback_password='OMEVV_VCENTER_PASSWORD',
                 env_fallback_uuid='OMEVV_VCENTER_UUID'):
        if "vcenter_uuid" in argument_spec:
            argument_spec.update({"vcenter_uuid": {"required": False, "type": "str",
                                           "fallback": (env_fallback, [env_fallback_uuid])}})
        super().__init__(argument_spec, bypass_checks, no_log,
                         mutually_exclusive, required_together,
                         required_one_of, add_file_common_args,
                         supports_check_mode, required_if, required_by,
                         env_fallback_username, env_fallback_password)
