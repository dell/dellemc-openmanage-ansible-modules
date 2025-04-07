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

GET_IDRAC_SENSOR_VOLTAGE_DETAILS_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/Power#/Voltages"


class IDRACSensorsVoltageInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def sensors_voltage_mapped_data(self, sensor):
        keys_to_search = {
            "CurrentReading": "ReadingVolts",
            "CurrentState": "Status.State",
            "DeviceID": "DeviceID",
            "HealthState": "Status.Health",
            "Key": "Name",
            "Location": "PhysicalContext",
            "OtherSensorTypeDescription": "Not Available",
            "PrimaryStatus": "Status.Health",
            "Reading(V)": "ReadingVolts",
            "SensorType": "Voltage",
            "State": "Status.State",
            "VoltageProbeIndex": "Not Available",
            "VoltageProbeType": "Not Available"
        }

        sensor_data = {}

        for key, response_key in keys_to_search.items():
            if key == "DeviceID":
                sensor_data[key] = f"iDRAC.Embedded.1#{sensor.get('Name', 'Unknown')}"
            elif key == "SensorType":
                sensor_data[key] = "Voltage"
            elif "." in response_key:
                keys = response_key.split(".")
                data = sensor
                for k in keys:
                    data = data.get(k, "Not Available")
                sensor_data[key] = data
            else:
                sensor_data[key] = sensor.get(response_key, "Not Available")

        return sensor_data

    def get_sensors_voltage_info(self):
        output = []
        resp = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_SENSOR_VOLTAGE_DETAILS_URI_10)
        if resp.status_code == 200:
            voltage_sensors = resp.json_data.get("Voltages", [])
            for sensor in voltage_sensors:
                output.append(self.sensors_voltage_mapped_data(sensor))
        return output
