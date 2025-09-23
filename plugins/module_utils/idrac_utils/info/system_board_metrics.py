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

from .chassis_sensor_util import IDRACChassisSensors

GET_SYSTEMBOARD_CPUUSAGE_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/Sensors/SystemBoardCPUUsage"
GET_SYSTEMBOARD_IOUSAGE_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/Sensors/SystemBoardIOUsage"
GET_SYSTEMBOARD_MEMUSAGE_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/Sensors/SystemBoardMEMUsage"
GET_SYSTEMBOARD_SYSUSAGE_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/Sensors/SystemBoardSYSUsage"

GET_SYSTEMBOARD_PWRCONSUMPTION_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/Sensors/SystemBoardPwrConsumption"
GET_SYSTEMBOARD_CURRENTCONSUMPTION_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/Sensors/SystemBoardCurrentConsumption"
GET_POWERHEADROOM_URI_10 = "/redfish/v1/Chassis/System.Embedded.1/Sensors/PowerHeadroom"

NA = "Not Available"


class IDRACSystemBoardMetricsInfo(object):
    def __init__(self, idrac, chassis_sensors: IDRACChassisSensors):
        self.idrac = idrac
        self.chassis_sensors = chassis_sensors

    def get_cpu_usage_details(self):
        response = self.chassis_sensors.get_sensor(GET_SYSTEMBOARD_CPUUSAGE_URI_10)
        if response.status_code == 200:
            cpu_usage_avg_hour = response.json_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastHour", {}).get("Reading", NA)
            cpu_usage_avg_day = response.json_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastDay", {}).get("Reading", NA)
            cpu_usage_avg_week = response.json_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastWeek", {}).get("Reading", NA)
            cpu_usage_max_hour = response.json_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastHour", {}).get("Reading", NA)
            cpu_usage_max_day = response.json_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastDay", {}).get("Reading", NA)
            cpu_usage_max_week = response.json_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastWeek", {}).get("Reading", NA)
            cpu_usage_min_hour = response.json_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastHour", {}).get("Reading", NA)
            cpu_usage_min_day = response.json_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastDay", {}).get("Reading", NA)
            cpu_usage_min_week = response.json_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastWeek", {}).get("Reading", NA)
            cpu_usage_peak = response.json_data.get("PeakReading", NA)
            return (
                cpu_usage_avg_hour, cpu_usage_avg_day, cpu_usage_avg_week,
                cpu_usage_max_hour, cpu_usage_max_day, cpu_usage_max_week,
                cpu_usage_min_hour, cpu_usage_min_day, cpu_usage_min_week,
                cpu_usage_peak
            )
        return NA, NA, NA, NA, NA, NA, NA, NA, NA, NA

    def get_io_usage_details(self):
        response = self.chassis_sensors.get_sensor(GET_SYSTEMBOARD_IOUSAGE_URI_10)
        if response.status_code == 200:
            io_usage_avg_hour = response.json_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastHour", {}).get("Reading", NA)
            io_usage_avg_day = response.json_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastDay", {}).get("Reading", NA)
            io_usage_avg_week = response.json_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastWeek", {}).get("Reading", NA)
            io_usage_max_hour = response.json_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastHour", {}).get("Reading", NA)
            io_usage_max_day = response.json_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastDay", {}).get("Reading", NA)
            io_usage_max_week = response.json_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastWeek", {}).get("Reading", NA)
            io_usage_min_hour = response.json_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastHour", {}).get("Reading", NA)
            io_usage_min_day = response.json_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastDay", {}).get("Reading", NA)
            io_usage_min_week = response.json_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastWeek", {}).get("Reading", NA)
            io_usage_peak = response.json_data.get("PeakReading", NA)
            return (
                io_usage_avg_hour, io_usage_avg_day, io_usage_avg_week,
                io_usage_max_hour, io_usage_max_day, io_usage_max_week,
                io_usage_min_hour, io_usage_min_day, io_usage_min_week,
                io_usage_peak
            )
        return NA, NA, NA, NA, NA, NA, NA, NA, NA, NA

    def get_mem_usage_details(self):
        response = self.chassis_sensors.get_sensor(GET_SYSTEMBOARD_MEMUSAGE_URI_10)
        if response.status_code == 200:
            mem_usage_avg_hour = response.json_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastHour", {}).get("Reading", NA)
            mem_usage_avg_day = response.json_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastDay", {}).get("Reading", NA)
            mem_usage_avg_week = response.json_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastWeek", {}).get("Reading", NA)
            mem_usage_max_hour = response.json_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastHour", {}).get("Reading", NA)
            mem_usage_max_day = response.json_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastDay", {}).get("Reading", NA)
            mem_usage_max_week = response.json_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastWeek", {}).get("Reading", NA)
            mem_usage_min_hour = response.json_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastHour", {}).get("Reading", NA)
            mem_usage_min_day = response.json_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastDay", {}).get("Reading", NA)
            mem_usage_min_week = response.json_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastWeek", {}).get("Reading", NA)
            mem_usage_peak = response.json_data.get("PeakReading", NA)
            return (
                mem_usage_avg_hour, mem_usage_avg_day, mem_usage_avg_week,
                mem_usage_max_hour, mem_usage_max_day, mem_usage_max_week,
                mem_usage_min_hour, mem_usage_min_day, mem_usage_min_week,
                mem_usage_peak
            )
        return NA, NA, NA, NA, NA, NA, NA, NA, NA, NA

    def get_sys_usage_details(self):
        response = self.chassis_sensors.get_sensor(GET_SYSTEMBOARD_SYSUSAGE_URI_10)
        if response.status_code == 200:
            sys_usage_avg_hour = response.json_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastHour", {}).get("Reading", NA)
            sys_usage_avg_day = response.json_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastDay", {}).get("Reading", NA)
            sys_usage_avg_week = response.json_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastWeek", {}).get("Reading", NA)
            sys_usage_max_hour = response.json_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastHour", {}).get("Reading", NA)
            sys_usage_max_day = response.json_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastDay", {}).get("Reading", NA)
            sys_usage_max_week = response.json_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastWeek", {}).get("Reading", NA)
            sys_usage_min_hour = response.json_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastHour", {}).get("Reading", NA)
            sys_usage_min_day = response.json_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastDay", {}).get("Reading", NA)
            sys_usage_min_week = response.json_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastWeek", {}).get("Reading", NA)
            sys_usage_peak = response.json_data.get("PeakReading", NA)
            return (
                sys_usage_avg_hour, sys_usage_avg_day, sys_usage_avg_week,
                sys_usage_max_hour, sys_usage_max_day, sys_usage_max_week,
                sys_usage_min_hour, sys_usage_min_day, sys_usage_min_week,
                sys_usage_peak
            )
        return NA, NA, NA, NA, NA, NA, NA, NA, NA, NA

    def get_peak_power_details(self):
        response = self.chassis_sensors.get_sensor(GET_SYSTEMBOARD_PWRCONSUMPTION_URI_10)
        if response.status_code == 200:
            return response.json_data.get("PeakReading", NA)
        return NA

    def get_peak_amperage_details(self):
        response = self.chassis_sensors.get_sensor(GET_SYSTEMBOARD_CURRENTCONSUMPTION_URI_10)
        if response.status_code == 200:
            return response.json_data.get("PeakReading", NA)
        return NA

    def get_peak_headroom_details(self):
        response = self.chassis_sensors.get_sensor(GET_POWERHEADROOM_URI_10)
        if response.status_code == 200:
            return response.json_data.get("LowestReading", NA)
        return NA

    def get_system_board_metrics_info(self):
        output = []

        (
            cpu_usage_avg_hour, cpu_usage_avg_day, cpu_usage_avg_week,
            cpu_usage_max_hour, cpu_usage_max_day, cpu_usage_max_week,
            cpu_usage_min_hour, cpu_usage_min_day, cpu_usage_min_week,
            cpu_usage_peak
        ) = self.get_cpu_usage_details()
        (
            io_usage_avg_hour, io_usage_avg_day, io_usage_avg_week,
            io_usage_max_hour, io_usage_max_day, io_usage_max_week,
            io_usage_min_hour, io_usage_min_day, io_usage_min_week,
            io_usage_peak
        ) = self.get_io_usage_details()
        (
            mem_usage_avg_hour, mem_usage_avg_day, mem_usage_avg_week,
            mem_usage_max_hour, mem_usage_max_day, mem_usage_max_week,
            mem_usage_min_hour, mem_usage_min_day, mem_usage_min_week,
            mem_usage_peak
        ) = self.get_mem_usage_details()
        (
            sys_usage_avg_hour, sys_usage_avg_day, sys_usage_avg_week,
            sys_usage_max_hour, sys_usage_max_day, sys_usage_max_week,
            sys_usage_min_hour, sys_usage_min_day, sys_usage_min_week,
            sys_usage_peak
        ) = self.get_sys_usage_details()

        peak_power = self.get_peak_power_details()
        peak_amperage = self.get_peak_amperage_details()
        peak_headroom = self.get_peak_headroom_details()

        output = [{
            "Key": "SystemBoardMetrics",

            "CPUUsageAvg1H": cpu_usage_avg_hour,
            "CPUUsageAvg1D": cpu_usage_avg_day,
            "CPUUsageAvg1W": cpu_usage_avg_week,
            "CPUUsageMax1H": cpu_usage_max_hour,
            "CPUUsageMax1D": cpu_usage_max_day,
            "CPUUsageMax1W": cpu_usage_max_week,
            "CPUUsageMin1H": cpu_usage_min_hour,
            "CPUUsageMin1D": cpu_usage_min_day,
            "CPUUsageMin1W": cpu_usage_min_week,
            "SYSPeakCPUUsage": cpu_usage_peak,

            "IOUsageAvg1H": io_usage_avg_hour,
            "IOUsageAvg1D": io_usage_avg_day,
            "IOUsageAvg1W": io_usage_avg_week,
            "IOUsageMax1H": io_usage_max_hour,
            "IOUsageMax1D": io_usage_max_day,
            "IOUsageMax1W": io_usage_max_week,
            "IOUsageMin1H": io_usage_min_hour,
            "IOUsageMin1D": io_usage_min_day,
            "IOUsageMin1W": io_usage_min_week,
            "SYSPeakIOUsage": io_usage_peak,

            "MemoryUsageAvg1H": mem_usage_avg_hour,
            "MemoryUsageAvg1D": mem_usage_avg_day,
            "MemoryUsageAvg1W": mem_usage_avg_week,
            "MemoryUsageMax1H": mem_usage_max_hour,
            "MemoryUsageMax1D": mem_usage_max_day,
            "MemoryUsageMax1W": mem_usage_max_week,
            "MemoryUsageMin1H": mem_usage_min_hour,
            "MemoryUsageMin1D": mem_usage_min_day,
            "MemoryUsageMin1W": mem_usage_min_week,
            "SYSPeakMemoryUsage": mem_usage_peak,

            "SYSUsageAvg1H": sys_usage_avg_hour,
            "SYSUsageAvg1D": sys_usage_avg_day,
            "SYSUsageAvg1W": sys_usage_avg_week,
            "SYSUsageMax1H": sys_usage_max_hour,
            "SYSUsageMax1D": sys_usage_max_day,
            "SYSUsageMax1W": sys_usage_max_week,
            "SYSUsageMin1H": sys_usage_min_hour,
            "SYSUsageMin1D": sys_usage_min_day,
            "SYSUsageMin1W": sys_usage_min_week,
            "SYSPeakSYSUsage": sys_usage_peak,

            "PeakPower": peak_power,
            "PeakAmperage": peak_amperage,
            "PeakHeadroom": peak_headroom,

            "SystemBoardMetrics": NA
        }]

        return output
