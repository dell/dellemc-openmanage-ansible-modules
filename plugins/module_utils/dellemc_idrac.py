# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 9.1.0
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
import os
from ansible.module_utils.common.parameters import env_fallback
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import compress_ipv6
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI


idrac_auth_params = {
    "idrac_ip": {"required": True, "type": 'str'},
    "idrac_user": {"required": True, "type": 'str', "fallback": (env_fallback, ['IDRAC_USERNAME'])},
    "idrac_password": {"required": True, "type": 'str', "aliases": ['idrac_pwd'], "no_log": True, "fallback": (env_fallback, ['IDRAC_PASSWORD'])},
    "idrac_port": {"required": False, "default": 443, "type": 'int'},
    "validate_certs": {"type": "bool", "default": True},
    "ca_path": {"type": "path"},
    "timeout": {"type": "int", "default": 30},
}


class iDRACConnection:

    def __init__(self, module_params):
        self.idrac_ip = compress_ipv6(module_params['idrac_ip'])
        self.idrac_user = module_params['idrac_user']
        self.idrac_pwd = module_params['idrac_password']
        self.idrac_port = module_params.get('idrac_port', 443)
        self.validate_certs = module_params.get('validate_certs', True)
        self.ca_path = module_params.get('ca_path')
        self.timeout = module_params.get('timeout', 30)
        if not all((self.idrac_ip, self.idrac_user, self.idrac_pwd)):
            raise ValueError("hostname, username and password required")
        self.redfish_api = None

    def __enter__(self):
        self.redfish_api = iDRACRedfishAPI(
            idrac_ip=self.idrac_ip,
            idrac_user=self.idrac_user,
            idrac_password=self.idrac_pwd,
            idrac_port=self.idrac_port,
            validate_certs=self.validate_certs,
            ca_path=self.ca_path,
            timeout=self.timeout
        )
        return self.redfish_api

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.redfish_api:
            self.redfish_api.logout()
        return False
