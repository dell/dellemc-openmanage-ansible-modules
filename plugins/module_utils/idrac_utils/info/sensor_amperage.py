# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 10.0.0
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

from .chassis_sensor_util import IDRACChassisSensors

GET_IDRAC_SENSOR_PS1CURRENT1_URI = "/redfish/v1/Chassis/System.Embedded.1/Sensors/PS1Current1"
GET_IDRAC_SENSOR_PWR_CONSUMPTION_URI = "/redfish/v1/Chassis/System.Embedded.1/Sensors/SystemBoardPwrConsumption"

NA = "Not Available"


class IDRACSensorAmperageInfo(object):
    def __init__(self, idrac, chassis_sensors: IDRACChassisSensors):
        self.idrac = idrac
        self.chassis_sensors = chassis_sensors

    def map_sensor_amperage_data(self, sensor):
        health_state_map = {
            "CriticalFailure": "Critical",
            "Degraded/Warning": "Warning",
            "MajorFailure": "Critical",
            "MinorFailure": "Critical",
            "NonRecoverableError": "Critical",
            "OK": "Healthy",
            "Unknown": "Unknown"
        }

        health_state = sensor.get("Status", {}).get("Health", NA)
        primary_status = health_state_map.get(health_state, NA)
        output = {
            "CurrentReading": sensor.get("Reading", NA),
            "CurrentState": sensor.get("Oem", {}).get("Dell", {}).get("CurrentState", NA),
            "DeviceID": sensor.get("Oem", {}).get("Dell", {}).get("DeviceID", NA),
            "HealthState": sensor.get("Oem", {}).get("Dell", {}).get("CurrentState", NA),
            "Key": sensor.get("Name", NA),
            "Location": sensor.get("Name", NA),
            "OtherSensorTypeDescription": NA,
            "PrimaryStatus": primary_status,
            "ProbeType": NA,
            "SensorType": "Amperage",
            "State": sensor.get("Status", {}).get("State", NA),
        }
        return output

    def get_sensor_amperage_info(self):
        """Fetches sensor amperage data from iDRAC and maps it."""
        output = []
        current_resp = self.chassis_sensors.get_sensor(GET_IDRAC_SENSOR_PS1CURRENT1_URI)
        power_resp = self.chassis_sensors.get_sensor(GET_IDRAC_SENSOR_PWR_CONSUMPTION_URI)

        if current_resp.status_code == 200 and power_resp.status_code == 200:
            for sensor in [current_resp.json_data, power_resp.json_data]:
                output.append(self.map_sensor_amperage_data(sensor))
        return output
