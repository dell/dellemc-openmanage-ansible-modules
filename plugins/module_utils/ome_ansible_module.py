#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.parameters import env_fallback

class OmeAnsibleModule(AnsibleModule):
    def __init__(self, argument_spec, bypass_checks=False, no_log=False,
                 mutually_exclusive=None, required_together=None,
                 required_one_of=None, add_file_common_args=False,
                 supports_check_mode=False, required_if=None, required_by=None):
        ome_argument_spec = {
            "hostname": {"required": True, "type": "str"},
            "username": {"required": False, "type": "str", "fallback": (env_fallback, ['OME_USERNAME'])},
            "password": {"required": False, "type": "str", "no_log": True, "fallback": (env_fallback, ['OME_PASSWORD'])},
            "x_auth_token": {"required": False, "type": "str", "no_log": True, "fallback": (env_fallback, ['OME_X_AUTH_TOKEN'])},
            "port": {"type": "int", "default": 443},
            "validate_certs": {"type": "bool", "default": True},
            "ca_path": {"type": "path"},
            "timeout": {"type": "int", "default": 30},
        }
        auth_mutually_exclusive = [("username", "x_auth_token"), ("password", "x_auth_token")]
        auth_required_one_of = [("username", "x_auth_token")]
        auth_required_together = [("username", "password")]

        argument_spec.update(ome_argument_spec)
        mutually_exclusive.extend(auth_mutually_exclusive)
        required_together.extend(auth_required_together)
        required_one_of.extend(auth_required_one_of)

        super(OmeAnsibleModule, self).__init__(argument_spec, bypass_checks, no_log,
                 mutually_exclusive, required_together,
                 required_one_of, add_file_common_args,
                 supports_check_mode, required_if, required_by)
