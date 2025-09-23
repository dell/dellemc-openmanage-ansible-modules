# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 10.0.1
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

GET_IDRAC_SENSORS_URI = "/redfish/v1/Chassis/System.Embedded.1/Sensors"


class _chassis_response(object):
    def __init__(self, status_code: int):
        self.status_code = status_code


class IDRACChassisSensors(object):
    def __init__(self, idrac):
        self.idrac = idrac
        sensor_resp = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_SENSORS_URI)
        self.sensors = {member["@odata.id"] for member in sensor_resp.json_data.get("Members", [])}

    def get_sensor(self, sensor: str):
        if sensor not in self.sensors:
            return _chassis_response(404)
        return self.idrac.invoke_request(method='GET', uri=sensor)
