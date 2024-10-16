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

PROFILE_URI = "/RepositoryProfiles"
TEST_CONNECTION_URI = "/RepositoryProfiles/TestConnection"

    
class OMEVVFirmwareProfile:
    def __init__(self, omevv, module):
        self.omevv = omevv
        self.module = module

    def test_connection(self, payload):
        """
        Tests the connection to the vCenter server.

        """
        resp = self.omevv.invoke_request("POST", TEST_CONNECTION_URI, payload)
        return resp
    
    def get_firmware_repository_profile(self):
        """
        Retrieves all firmware repository profile Information.

        """
        resp = self.omevv.invoke_request("GET", PROFILE_URI)
        return resp
    
    def get_specific_firmware_repository_profile(self, profile_id):
        """
        Retrieves all firmware repository profile Information.

        """
        resp = self.omevv.invoke_request("GET", PROFILE_URI + "/" + str(profile_id))
        return resp
    
    def create_firmware_repository_profile(self, payload):
        """
        Creates a firmware repository profile.

        """
        resp = self.omevv.invoke_request("POST", PROFILE_URI, payload)
        return resp
    
    def modify_firmware_repository_profile(self, profile_id, payload):
        """
        Modifies a firmware repository profile.

        """
        resp = self.omevv.invoke_request("PUT", PROFILE_URI + "/" + str(profile_id), payload)
        return resp

    def delete_firmware_repository_profile(self, profile_id):
        """
        Deletes a firmware repository profile.

        """
        resp = self.omevv.invoke_request("DELETE", PROFILE_URI + "/" + str(profile_id))
        return resp
