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


GET_IDRAC_CPU_DETAILS_URI_10 = "/redfish/v1/Systems/System.Embedded.1/Processors?$expand=*($levels=1)"
GET_IDRAC_LICENSE_DETAILS_URI_10 = "/redfish/v1/LicenseService/Licenses?$expand=*($levels=1)"
GET_IDRAC_MEMORY_DETAILS_URI_10 = "/redfish/v1/Systems/System.Embedded.1/Memory?%24expand=*(%24levels%3D1)"
GET_IDRAC_POWER_SUPPLY_DETAILS_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/PowerSubsystem/PowerSupplies?$expand=*($levels=1)"
GET_IDRAC_SENSOR_VOLTAGE_DETAILS_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/Power#/Voltages"
GET_IDRAC_DELL_SENSORS_DETAILS_URI_10 = "/redfish/v1/Systems/System.Embedded.1/Oem/Dell/DellSensors"
GET_IDRAC_SENSOR_FAN_DETAILS_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/Oem/Dell/DellEnclosureFanSensors"
GET_IDRAC_SENSOR_INTRUSION_DETAILS_URI_10 = "/redfish/v1/Chassis/System.Embedded.1?$select=PhysicalSecurity/IntrusionSensor"
GET_IDRAC_SENSOR_TEMPERATURE_DETAILS_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/Oem/Dell/DellEnclosureTemperatureSensors"
GET_IDRAC_STORAGE_DETAILS_URI_10 = "/redfish/v1/Systems/System.Embedded.1/Storage?$expand=*($levels=1)"
GET_IDRAC_SENSOR_AMPERAGE_DETAILS_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/Sensors/SystemBoardPwrConsumption"
GET_IDRAC_SYSTEM_DETAILS_URI_10 = "/redfish/v1/Systems/System.Embedded.1"


class IDRACSubsystemInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac
        self.sub_system = []

    def get_idrac_cpu_health_status(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_CPU_DETAILS_URI_10)
        output = response.json_data
        members = output.get("Members", [])
        if members:
            health_status = members[0].get("Status", {}).get("Health", "Unknown")
        else:
            health_status = "Unknown"
        return {
            "Key": "CPU",
            "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
        }

    def get_idrac_license_health_status(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_LICENSE_DETAILS_URI_10)
        output = response.json_data
        members = output.get("Members", [])
        if members:
            health_status = members[0].get("Status", {}).get("Health", "Unknown")
        else:
            health_status = "Unknown"
        return {
            "Key": "License",
            "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
        }

    def get_idrac_memory_health_status(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_MEMORY_DETAILS_URI_10)
        output = response.json_data
        members = output.get("Members", [])
        if members:
            health_status = members[0].get("Status", {}).get("Health", "Unknown")
        else:
            health_status = "Unknown"
        return {
            "Key": "Memory",
            "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
        }

    def get_idrac_power_supply_health_status(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_POWER_SUPPLY_DETAILS_URI_10)
        output = response.json_data
        members = output.get("Members", [])
        if members:
            health_status = members[0].get("Status", {}).get("Health", "Unknown")
        else:
            health_status = "Unknown"
        return {
            "Key": "PowerSupply",
            "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
        }

    def get_idrac_sensor_voltage_health_status(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_SENSOR_VOLTAGE_DETAILS_URI_10)
        output = response.json_data
        members = output.get("Redundancy", [])
        if members:
            health_status = members[0].get("Status", {}).get("Health", "Unknown")
        else:
            health_status = "Unknown"
        return {
            "Key": "Sensors_Voltage",
            "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
        }

    def get_idrac_sensor_battery_health_status(self):
        found = False
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_DELL_SENSORS_DETAILS_URI_10)
        for mem in response.json_data.get("Members", []):
            if mem.get("ElementName", "") == "System Board CMOS Battery":
                health_status = mem.get("HealthState")
                return {
                    "Key": "Sensors_Battery",
                    "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
                }

        if not found:
            return {
                "Key": "Sensors_Battery",
                "PrimaryStatus": "Unknown"
            }

    def get_idrac_sensor_fan_health_status(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_SENSOR_FAN_DETAILS_URI_10)
        output = response.json_data
        members = output.get("Members", [])
        if members:
            health_status = members[0].get("Status", {}).get("Health", "Unknown")
        else:
            health_status = "Unknown"
        return {
            "Key": "Sensors_Fan",
            "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
        }

    def get_idrac_sensor_intrusion_health_status(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_SENSOR_INTRUSION_DETAILS_URI_10)
        output = response.json_data
        health_status = output["PhysicalSecurity"].get("IntrusionSensor", "Unknown")
        return {
            "Key": "Sensors_Intrusion",
            "PrimaryStatus": "Healthy" if health_status == "Normal" else health_status
        }

    def get_idrac_sensor_temperature_health_status(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_SENSOR_TEMPERATURE_DETAILS_URI_10)
        output = response.json_data
        members = output.get("Members", [])
        if members:
            health_status = members[0].get("Status", {}).get("Health", "Unknown")
        else:
            health_status = "Unknown"
        return {
            "Key": "Sensors_Temperature",
            "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
        }

    def get_idrac_system_health_status(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_SYSTEM_DETAILS_URI_10)
        output = response.json_data
        health_status = output["Status"].get("Health", "Unknown")
        return {
            "Key": "System",
            "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
        }

    def get_idrac_vflash_health_status(self):
        # Hardcoding value, since no api is available
        return {
            "Key": "VFlash",
            "PrimaryStatus": "Unknown"
        }

    def get_idrac_sensor_amperage_health_status(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_SENSOR_AMPERAGE_DETAILS_URI_10)
        output = response.json_data
        health_status = output["Status"].get("Health", "Unknown")
        return {
            "Key": "Sensors_Amperage",
            "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
        }

    def get_storage_health_status_data(self, uri):
        response = self.idrac.invoke_request(method='GET', uri=uri)
        output = response.json_data
        health_status = output["Status"].get("Health", "Unknown") or "Unknown"
        return health_status

    def get_idrac_storage_health_status(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_STORAGE_DETAILS_URI_10)
        output = response.json_data
        members = output.get("Members", [])
        health_status = "Unknown"
        if members:
            URI = members[0].get("@odata.id", "")
            health_status = self.get_storage_health_status_data(uri=URI)
        return {
            "Key": "Storage",
            "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
        }

    def get_subsystem_info(self):
        self.sub_system.append(self.get_idrac_system_health_status())
        self.sub_system.append(self.get_idrac_memory_health_status())
        self.sub_system.append(self.get_idrac_cpu_health_status())
        self.sub_system.append(self.get_idrac_sensor_fan_health_status())
        self.sub_system.append(self.get_idrac_power_supply_health_status())
        self.sub_system.append(self.get_idrac_storage_health_status())
        self.sub_system.append(self.get_idrac_license_health_status())
        self.sub_system.append(self.get_idrac_sensor_voltage_health_status())
        self.sub_system.append(self.get_idrac_sensor_temperature_health_status())
        self.sub_system.append(self.get_idrac_sensor_battery_health_status())
        self.sub_system.append(self.get_idrac_vflash_health_status())
        self.sub_system.append(self.get_idrac_sensor_intrusion_health_status())
        self.sub_system.append(self.get_idrac_sensor_amperage_health_status())
        return self.sub_system
