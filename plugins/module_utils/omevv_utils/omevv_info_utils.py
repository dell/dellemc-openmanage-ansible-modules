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

VCENTER_INFO_URI = "/Consoles"


class OMEVVInfo:
    def __init__(self, omevv_obj):
        self.omevv_obj = omevv_obj

    def search_vcenter_hostname(self, vcenter_data, vcenter_id):
        """
        Searches for a vCenter hostname in the given vcenter_data list.
        Parameters:
            vcenter_data (list): A list of vCenter data.
            vcenter_id (str): The hostname of the vCenter to search for.
        Returns:
            dict: The vCenter data that matches the given vcenter_id. If no match is found, an empty dictionary is returned.
        """
        for vcenter in vcenter_data:
            if vcenter.get('consoleAddress') == vcenter_id:
                return vcenter
        return {}

    def get_vcenter_info(self, vcenter_id=None):
        """
        Retrieves the vCenter information.
        Parameters:
            vcenter_id (str, optional): The hostname of the vCenter. If provided, retrieves the information for the specified vCenter.
        Returns:
            list: A list of vCenter information when `vcenter_id` is not provided
            dict: A dict containing the information for the specified vCenter when `vcenter_id` is provided. If no match is found, the empty dict is returned.
        """
        resp = self.omevv_obj.invoke_request('GET', VCENTER_INFO_URI)
        vcenter_info = []
        if resp.success:
            vcenter_info = resp.json_data
            if vcenter_id:
                vcenter_info = self.search_vcenter_hostname(vcenter_info, vcenter_id)
        return vcenter_info
