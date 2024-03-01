# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 9.1.0
# Copyright (C) 2019-2024 Dell Inc. or its subsidiaries. All Rights Reserved.

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
from enum import Enum
import sys
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.six.moves.urllib.parse import urlencode
from ansible.module_utils.common.parameters import env_fallback
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import get_dynamic_uri, validate_and_get_first_resource_id_uri

SYSTEMS_URI = "/redfish/v1/Systems"
CONTROLLER_ID_NOT_FOUND = 'Controller ID is required.'

class EnumWrapper:
    enum_entries = {}
    enum_name = None

    def __init__(self, name, entries):
        EnumWrapper.enum_entries[name] = entries
        self.enum_type = Enum(name, EnumWrapper.enum_entries[name])

    @staticmethod
    def mapvalue(self, i, value):
        pass

    @staticmethod
    def resolve(enval):
        return (enval.value)

RAIDactionTypes = EnumWrapper("RAIDactionTypes", {
    "Create": "Create",
    "CreateAuto": "CreateAuto",
    "Delete": "Delete",
    "Update": "Update",
}).enum_type

RAIDdefaultReadPolicyTypes = EnumWrapper("RAIDdefaultReadPolicyTypes", {
    "Adaptive": "Adaptive",
    "AdaptiveReadAhead": "AdaptiveReadAhead",
    "NoReadAhead": "NoReadAhead",
    "ReadAhead": "ReadAhead",
}).enum_type

RAIDinitOperationTypes = EnumWrapper("RAIDinitOperationTypes", {
    "Fast": "Fast",
    "T_None": "None",
}).enum_type

DiskCachePolicyTypes = EnumWrapper("DiskCachePolicyTypes", {
    "Default": "Default",
    "Disabled": "Disabled",
    "Enabled": "Enabled",
}).enum_type

RAIDresetConfigTypes = EnumWrapper("RAIDresetConfigTypes", {
    "T_False": "False",
    "T_True": "True",
}).enum_type

class Controller:
    def __init__(self, module, idrac) -> None:
        self.idrac_obj = idrac
        self.module_inp = module
        self.controller_details = {}

    def validate_and_fetch(self) -> tuple[str, dict]:
        # Validation when state is create and controller_id is not provided
        state = self.module_inp.params.get('state')
        if state in ['create'] and not self.controller_id:
            return CONTROLLER_ID_NOT_FOUND, self.controller_details
        base_resource_uri = validate_and_get_first_resource_id_uri(self.module_inp, self.idrac_obj, SYSTEMS_URI)
        self.controller_details = get_dynamic_uri(self.module_inp, self.idrac_obj, self.controller_id)
        


    

class Volume:
    def __init__(self, module) -> None:
        self.module = None
        self.volume_details = {}
    
    def validate(self) -> tuple[str, dict]:
        params = self.module.params
        # Validation for create
        state = params.get('state')
        volume_id = params.get('volume_id')
        if state in ['create'] and not volume_id:
            return 'Volume ID is required.', self.volume_details
        
        
