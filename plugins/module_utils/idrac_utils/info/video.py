# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 9.12.0
# Copyright (C) 2025 Dell Inc. or its subsidiaries. All Rights Reserved.

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

GET_IDRAC_VIDEO_DETAILS_URI_10 = "/redfish/v1/Systems/System.Embedded.1/Oem/Dell/DellVideo"


class IDRACVideoInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def get_idrac_video_details(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_VIDEO_DETAILS_URI_10)
        final_output = self.extract_video_data(response.json_data)
        return final_output

    def extract_video_data(self, response):
        keys_to_search = {
            "Description": "Description",
            "DeviceDescription": "DeviceDescription",
            "FQDD": "FQDD",
            "Key": "Key",
            "Manufacturer": "Manufacturer"
        }
        video_list = []
        if "Members" in response and response["Members"]:
            for member in response["Members"]:
                video_data = {}
                for key, response_key in keys_to_search.items():
                    video_data[key] = member.get(response_key, "Not Available")
                video_list.append(video_data)
        return video_list
