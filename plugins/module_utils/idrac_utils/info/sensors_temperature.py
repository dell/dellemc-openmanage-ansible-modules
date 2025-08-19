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
#


GET_IDRAC_THERMAL_DETAILS_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/Thermal"
GET_IDRAC_SENSOR_TEMPERATURE_DETAILS_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/Sensors/{temp_sensor_name}"
NA = "Not Available"


class IDRACSensorsTemperatureInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def fetch_temp_sensor_names(self):
        """Fetches a list of all temperature sensor names from the IDRAC endpoint."""
        resp = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_THERMAL_DETAILS_URI_10)
        if resp.status_code != 200:
            return []

        return [
            member.get("Name", "").replace(" ", "")
            for member in resp.json_data.get("Temperatures", [])
            if member.get("Name")
        ]

    def fetch_temp_sensor_details(self, temp_sensor_name):
        """Fetches raw temperature sensor details for a given sensor name."""
        sensor_uri = GET_IDRAC_SENSOR_TEMPERATURE_DETAILS_URI_10.format(temp_sensor_name=temp_sensor_name)
        resp = self.idrac.invoke_request(method='GET', uri=sensor_uri)
        return resp.json_data if resp.status_code == 200 else None

    def sensors_temperature_mapped_data(self, resp):
        health = resp.get("Status", {}).get("Health", {})
        state = resp.get("Status", {}).get("State", {}) or NA
        device_id = resp.get("Oem", {}).get("Dell", {}).get("DeviceID", {}) or NA
        current_state = resp.get("Oem", {}).get("Dell", {}).get("CurrentState", {}) or NA
        output = {
            "CurrentReading": resp.get("Reading", NA),
            "CurrentState": current_state,
            "DeviceID": device_id,
            "HealthState": health,
            "Key": resp.get("Name", NA),
            "Location": resp.get("Name", NA),
            "OtherSensorTypeDescription": resp.get("OtherSensorTypeDescription", NA),
            "PrimaryStatus": "Healthy" if health == "OK" else health,
            "SensorType": "Temperature",
            "State": state,
            "Type": resp.get("Type", NA),
        }
        return output

    def get_sensors_temperature_info(self):
        output = []

        for temp_sensor_name in self.fetch_temp_sensor_names():
            temp_resp = self.fetch_temp_sensor_details(temp_sensor_name)
            if temp_resp:
                output.append(self.sensors_temperature_mapped_data(temp_resp))

        return output
