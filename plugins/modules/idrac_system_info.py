#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.8.0
# Copyright (C) 2021-2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_system_info
short_description: Get the PowerEdge Server System Inventory
version_added: "3.0.0"
description:
    - Get the PowerEdge Server System Inventory.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options

requirements:
    - "omsdk >= 1.2.488"
    - "python >= 3.9.6"
author:
  - "Rajeev Arakkal (@rajeevarakkal)"
  - "Saksham Nautiyal (@Saksham-Nautiyal)"
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports both IPv4 and IPv6 address for I(idrac_ip).
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Get System Inventory
  dellemc.openmanage.idrac_system_info:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
"""

RETURN = r'''
---
msg:
  description: "Overall system inventory information status."
  returned: always
  type: str
  sample: "Successfully fetched the system inventory details."
system_info:
  type: dict
  description: Details of the PowerEdge Server System Inventory.
  returned: success
  sample: {
            "BIOS": [
                {
                    "BIOSReleaseDate": "11/26/2019",
                    "FQDD": "BIOS.Setup.1-1",
                    "InstanceID": "DCIM:INSTALLED#741__BIOS.Setup.1-1",
                    "Key": "DCIM:INSTALLED#741__BIOS.Setup.1-1",
                    "SMBIOSPresent": "True",
                    "VersionString": "2.4.8"
                }
            ]
  }
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
      "code": "Base.1.0.GeneralError",
      "message": "A general error has occurred. See ExtendedInfo for more information.",
      "@Message.ExtendedInfo": [
        {
          "MessageId": "GEN1234",
          "RelatedProperties": [],
          "Message": "Unable to process the request because an error occurred.",
          "MessageArgs": [],
          "Severity": "Critical",
          "Resolution": "Retry the operation. If the issue persists, contact your system administrator."
        }
      ]
    }
  }
'''

import json
from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection, idrac_auth_params
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    GET_IDRAC_FIRMWARE_URI_10, GET_IDRAC_BIOS_DETAILS_URI_10, GET_IDRAC_CPU_DETAILS_URI_10, GET_IDRAC_CONTROLLER_DETAILS_URI_10,
    GET_IDRAC_CONTROLLER_BATTERY_DETAILS_URI_10, GET_IDRAC_CHASSIS_URI_10, GET_IDRAC_ENCLOSURE_FAN_SENSOR_DETAILS_URI_10,
    GET_IDRAC_ENCLOSURE_TEMP_SENSOR_DETAILS_URI_10, GET_IDRAC_FAN_DETAILS_URI_10, GET_IDRAC_LICENSE_DETAILS_URI_10, GET_IDRAC_MEMORY_DETAILS_URI_10,
    GET_IDRAC_NIC_DETAILS_URI_10, GET_IDRAC_PCI_DETAILS_URI_10, GET_IDRAC_STORAGE_DETAILS_URI_10, GET_IDRAC_POWER_SUPPLY_DETAILS_URI_10,
    GET_IDRAC_SENSOR_VOLTAGE_DETAILS_URI_10, GET_IDRAC_SENSOR_BATTERY_DETAILS_URI_10, GET_IDRAC_SENSOR_FAN_DETAILS_URI_10,
    GET_IDRAC_SENSOR_INTRUSION_DETAILS_URI_10, GET_IDRAC_SENSOR_TEMPERATURE_DETAILS_URI_10, GET_IDRAC_SYSTEM_DETAILS_URI_10, GET_IDRAC_VIDEO_DETAILS_URI_10,
    remove_key)
from ansible.module_utils.basic import AnsibleModule
from urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


def extract_bios_data(response):
    keys_to_search = {
        "BIOSReleaseDate": "BIOSReleaseDate",
        "FQDD": "FQDD",
        "InstanceID": "InstanceID",
        "Key": "InstanceID",
        "SMBIOSPresent": "SMBIOSPresent",
        "VersionString": "SystemBiosVersion"
    }

    bios_list = []
    bios_attributes = response.get("Attributes", {})
    bios_data = {}
    for key, response_key in keys_to_search.items():
        if response_key == "Not Available":
            bios_data[key] = "Not Available"
        else:
            bios_data[key] = bios_attributes.get(response_key, "Not Available")

    software_images = response.get("Links", {}).get("SoftwareImages", [])
    if software_images:
        odata_id = software_images[0].get("@odata.id", "")
        fqdd_parts = odata_id.split("__")
        bios_data["FQDD"] = fqdd_parts[-1] if len(fqdd_parts) > 1 else "Not Available"
    else:
        bios_data["FQDD"] = "Not Available"

    version_string = bios_attributes.get("SystemBiosVersion")
    bios_data["SMBIOSPresent"] = "True" if version_string else "False"

    bios_list.append(bios_data)

    return {"BIOS": bios_list}


def extract_cpu_data(response, Subsystem):
    keys_to_search = {
        "CPUFamily": "CPUFamily",
        "Characteristics": "Not Available",
        "CurrentClockSpeed": "CurrentClockSpeedMhz",
        "DeviceDescription": "Not Available",
        "ExecuteDisabledCapable": "ExecuteDisabledCapable",
        "ExecuteDisabledEnabled": "ExecuteDisabledEnabled",
        "FQDD": "not available",
        "HyperThreadingCapable": "HyperThreadingCapable",
        "HyperThreadingEnabled": "HyperThreadingEnabled",
        "Key": "Id",
        "Manufacturer": "Manufacturer",
        "MaxClockSpeed": "MaxSpeedMHz",
        "Model": "Model",
        "NumberOfEnabledCores": "TotalEnabledCores",
        "NumberOfEnabledThreads": "TotalThreads",
        "NumberOfProcessorCores": "TotalCores",
        "PrimaryStatus": "Health",
        "TurboModeCapable": "TurboModeCapable",
        "TurboModeEnabled": "TurboModeEnabled",
        "VirtualizationTechnologyCapable": "VirtualizationTechnologyCapable",
        "VirtualizationTechnologyEnabled": "VirtualizationTechnologyEnabled",
        "Voltage": "Volts",
        "processorDeviceStateSettings": "Not Available"
    }

    cpu_list = []
    if "Members" in response:
        for member in response["Members"]:
            processor = member.get("Oem", {}).get("Dell", {}).get("DellProcessor", {})
            cpu_data = {}

            for key, response_key in keys_to_search.items():
                if response_key == "Not Available":
                    cpu_data[key] = "Not Available"
                else:
                    if response_key in member:
                        cpu_data[key] = member.get(response_key, "Not Available")
                    else:
                        cpu_data[key] = processor.get(response_key, "Not Available")

            max_clock_speed = cpu_data.get("MaxClockSpeed")
            if max_clock_speed and isinstance(max_clock_speed, (int, float)):
                cpu_data["MaxClockSpeed"] = max_clock_speed / 1000

            Subsystem.append({
                "Key": "CPU",
                "PrimaryStatus": member.get("Status", {}).get("Health", "Unknown")
            })
            cpu_list.append(cpu_data)

    return {"CPU": cpu_list}


def extract_controller_data(response):
    keys_to_search = {
        "Bus": "Bus",
        "CacheSize": "CacheSize",
        "CachecadeCapability": "CachecadeCapability",
        "ControllerFirmwareVersion": "ControllerFirmwareVersion",
        "DeviceCardDataBusWidth": "DeviceCardDataBusWidth",
        "DeviceCardManufacturer": "DeviceCardManufacturer",
        "DeviceCardSlotLength": "DeviceCardSlotLength",
        "DeviceCardSlotType": "DeviceCardSlotType",
        "DeviceDescription": "DeviceDescription",
        "DriverVersion": "DriverVersion",
        "EncryptionCapability": "EncryptionCapability",
        "EncryptionMode": "EncryptionMode",
        "FQDD": "FQDD",
        "Key": "Key",
        "MaxAvailablePCILinkSpeed": "MaxAvailablePCILinkSpeed",
        "MaxPossiblePCILinkSpeed": "MaxPossiblePCILinkSpeed",
        "PCISlot": "PCISlot",
        "PCIVendorID": "PCIVendorID",
        "PrimaryStatus": "Health",
        "ProductName": "ProductName",
        "RollupStatus": "RollupStatus",
        "SASAddress": "SASAddress",
        "SecurityStatus": "SecurityStatus",
        "SlicedVDCapability": "SlicedVDCapability",
        "SupportControllerBootMode": "SupportControllerBootMode",
        "SupportEnhancedAutoForeignImport": "SupportEnhancedAutoForeignImport",
        "SupportRAID10UnevenSpans": "SupportRAID10UnevenSpans",
        "T10PICapability": "T10PICapability"
    }

    controller_list = []
    if "Members" in response:
        for member in response["Members"]:
            controller = member.get("Oem", {}).get("Dell", {}).get("DellController", {})
            controller_data = {}

            for key, response_key in keys_to_search.items():
                if response_key in member:
                    controller_data[key] = member.get(response_key, "Not Available")
                else:
                    controller_data[key] = controller.get(response_key, "Not Available")

            controller_list.append(controller_data)

    return {"Controller": controller_list}


def extract_controller_battery_data(response):
    keys_to_search = {
        "BatteryStatus": "Status",
        "BatteryHealth": "Health",
        "BatteryCapacity": "Capacity",
        "BatteryType": "BatteryType",
        "BatteryVoltage": "Voltage",
        "BatteryFirmwareVersion": "FirmwareVersion"
    }

    battery_list = []

    if "Members" in response and response["Members"]:
        for member in response["Members"]:
            battery_data = {}

            for key, response_key in keys_to_search.items():
                battery_data[key] = member.get(response_key, "Not Available")

            battery_list.append(battery_data)

    return {"ControllerBattery": battery_list}


def extract_controller_sensor_data(response):
    keys_to_search = {
        "FQDD": "FQDD",
        "Key": "Key"
    }
    sensor_list = []
    if "Members" in response and response["Members"]:
        for member in response["Members"]:
            sensor_data = {}

            for key, response_key in keys_to_search.items():
                sensor_data[key] = member.get(response_key, "Not Available")

            sensor_list.append(sensor_data)

    return {"ControllerSensor": sensor_list}


def extract_enclosure_data(response):
    keys_to_search = {
        "AssetTag": "ServiceTag",
        "Connector": "Connector",
        "DeviceDescription": "DeviceDescription",
        "EMMCount": "DellEnclosureEMMCollection@odata.count",
        "FQDD": "Id",
        "FanCount": "TempProbeCount",
        "Key": "Id",
        "PSUCount": "PSUCount",
        "PrimaryStatus": "PrimaryStatus",
        "ProductName": "Name",
        "ServiceTag": "ServiceTag",
        "SlotCount": "SlotCount",
        "State": "State",
        "Version": "Version",
        "WiredOrder": "WiredOrder"
    }

    enclosure_list = []
    for each_data in response:
        if "Members" in each_data and each_data["Members"]:
            for member in each_data["Members"]:
                enclosure_data = {}

                for key, response_key in keys_to_search.items():
                    enclosure_data[key] = member.get(response_key, "Not Available")

        enclosure_list.append(enclosure_data)

        return {"Enclosure": enclosure_list}


def extract_enclosure_fan_data(response):
    keys_to_search = {
        "FQDD": "FQDD",
        "Key": "Id"
    }

    enclosure_fan_list = []

    if "Members" in response and response["Members"]:
        for member in response["Members"]:
            fan_data = {}
            for key, response_key in keys_to_search.items():
                fan_data[key] = member.get(response_key, "Not Available")
            enclosure_fan_list.append(fan_data)

    return {"EnclosureFanSensors": enclosure_fan_list}


def extract_enclosure_temp_data(response):
    keys_to_search = {
        "FQDD": "FQDD",
        "Key": "Id"
    }

    temp_sensors_list = []

    if "Members" in response and response["Members"]:
        for member in response["Members"]:
            temp_data = {}
            for key, response_key in keys_to_search.items():
                temp_data[key] = member.get(response_key, "Not Available")
            temp_sensors_list.append(temp_data)

    return {"EnclosureTemperatureSensors": temp_sensors_list}


def extract_fan_data(response):
    keys_to_search = {
        "ActiveCooling": "HotPluggable",
        "BaseUnits": "SpeedPercent",
        "CurrentReading": "SpeedPercent",
        "DeviceDescription": "Name",
        "FQDD": "Id",
        "Key": "Id",
        "Location": "Location",
        "PWM": "Oem.Dell.FanPWM",
        "PrimaryStatus": "Status.Health",
        "RateUnits": "SpeedPercent.SpeedRPM",
        "RedundancyStatus": "Status.State",
        "State": "Status.State",
        "VariableSpeed": "Oem.Dell.FanType"
    }

    fan_list = []

    if "Members" in response and response["Members"]:
        for member in response["Members"]:
            fan_data = {}

            for key, response_key in keys_to_search.items():
                keys = response_key.split(".")
                value = member
                for k in keys:
                    value = value.get(k, "Not Available") if isinstance(value, dict) else "Not Available"

                fan_data[key] = value

            fan_list.append(fan_data)

    return {"Fan": fan_list}


def extract_license_data(response, Subsystem):
    keys_to_search = {
        "InstanceID": "Id",
        "Key": "Id",
        "LicenseDescription": "Description",
        "LicenseInstallDate": "InstallDate",
        "LicenseSoldDate": "ExpirationDate",
        "LicenseType": "LicenseType",
        "PrimaryStatus": "Health"
    }

    license_list = []

    if "Members" in response and response["Members"]:
        for member in response["Members"]:
            license_data = {}

            for key, response_key in keys_to_search.items():
                if response_key == "Health":
                    license_data["PrimaryStatus"] = member.get("Status", {}).get("Health", "Not Available")
                else:
                    license_data[key] = member.get(response_key, "Not Available")

            Subsystem.append({
                "Key": "License",
                "PrimaryStatus": member.get("Status", {}).get("Health", "Unknown")
            })

            license_list.append(license_data)

    return {"License": license_list}


def extract_memory_data(response, subsystem):
    keys_to_search = {
        "BankLabel": "BankLabel",
        "CurrentOperatingSpeed": "OperatingSpeedMhz",
        "DeviceDescription": "Description",
        "FQDD": "Id",
        "Key": "Id",
        "ManufactureDate": "ManufactureDate",
        "Manufacturer": "Manufacturer",
        "MemoryType": "MemoryDeviceType",
        "Model": "Model",
        "PartNumber": "PartNumber",
        "PrimaryStatus": "Health",
        "Rank": "RankCount",
        "SerialNumber": "SerialNumber",
        "Size": "CapacityMiB",
        "Speed": "OperatingSpeedMhz",
        "memoryDeviceStateSettings": "Enabled"
    }

    memory_list = []
    primary_status = "Unknown"

    if "Members" in response and response["Members"]:
        for member in response["Members"]:
            memory_data = {}

            for key, response_key in keys_to_search.items():
                if key in ["BankLabel", "ManufactureDate", "Model"]:
                    dell_memory = member.get("Oem", {}).get("Dell", {}).get("DellMemory", {})
                    if key == "BankLabel":
                        memory_data[key] = dell_memory.get("BankLabel", "Not Available")
                    elif key == "ManufactureDate":
                        memory_data[key] = dell_memory.get("ManufactureDate", "Not Available")
                    elif key == "Model":
                        memory_data[key] = dell_memory.get("Model", "Not Available")
                elif key == "PrimaryStatus":
                    health_status = member.get("Status", {}).get("Health", "Unknown")
                    memory_data[key] = health_status
                    primary_status = health_status if health_status != "Unknown" else primary_status
                elif key == "Speed":
                    speed_mhz = member.get("OperatingSpeedMhz", 0)
                    memory_data[key] = f"{speed_mhz / 1000:.1f} GHz" if speed_mhz else "Not Available"
                elif key == "Size":
                    capacity_mib = member.get("CapacityMiB", 0)
                    memory_data[key] = f"{capacity_mib / 1024:.1f} GB" if capacity_mib else "Not Available"
                else:
                    memory_data[key] = member.get(response_key, "Not Available")

            memory_list.append(memory_data)

    subsystem.append({
        "Key": "Memory",
        "PrimaryStatus": primary_status
    })

    return {"Memory": memory_list}


def extract_nic_data(response):
    keys_to_search = {
        "AutoNegotiation": "AutoNeg",
        "ControllerBIOSVersion": "N/A",
        "CurrentMACAddress": "MACAddress",
        "DCBExchangeProtocol": "Not Supported",
        "DataBusWidth": "N/A",
        "DeviceDescription": "Description",
        "EFIVersion": "N/A",
        "FCoEBootSupport": "Not Supported",
        "FCoEOffloadMode": "Unknown",
        "FCoEOffloadSupport": "Not Supported",
        "FCoEWWNN": "Not Available",
        "FQDD": "Id",
        "FamilyVersion": "N/A",
        "FlexAddressingSupport": "Supported",
        "IPv4Address": "IPv4Addresses",
        "IPv6Address": "IPv6Addresses",
        "Key": "Id",
        "LinkDuplex": "FullDuplex",
        "LinkSpeed": "SpeedMbps",
        "LinkStatus": "LinkStatus",
        "MaxBandwidth": "N/A",
        "MediaType": "N/A",
        "NICCapabilities": "Not Available",
        "NicMode": "Unknown",
        "NicPartitioningSupport": "Not Supported",
        "PXEBootSupport": "Supported",
        "PermanentFCOEMACAddress": "Not Available",
        "PermanentMACAddress": "PermanentMACAddress",
        "PermanentiSCSIMACAddress": "Not Available",
        "PrimaryStatus": "Status",
        "ProductName": "N/A",
        "Protocol": "NIC",
        "RxBytes": "N/A",
        "RxMutlicast": "N/A",
        "RxUnicast": "N/A",
        "SupportedBootProtocol": "Not Available",
        "SwitchConnectionID": "N/A",
        "SwitchPortConnectionID": "N/A",
        "TCPChimneySupport": "Not Supported",
        "TxBytes": "N/A",
        "TxMutlicast": "N/A",
        "TxUnicast": "N/A",
        "VFSRIOVSupport": "Not Supported",
        "VendorName": "N/A",
        "VirtMacAddr": "MACAddress",
        "VirtWWN": "Not Available",
        "VirtWWPN": "Not Available",
        "WOLSupport": "Supported",
        "WWN": "Not Available",
        "WWPN": "Not Available",
        "iSCSIBootSupport": "Not Supported",
        "iSCSIOffloadSupport": "Not Supported",
        "iScsiOffloadMode": "Unknown"
    }

    nic_list = []

    if "Members" in response and response["Members"]:
        for member in response["Members"]:
            nic_data = {}

            for key, response_key in keys_to_search.items():
                if key in ["IPv4Address", "IPv6Address"]:
                    # Handle IP Addresses (if available)
                    addresses = member.get(response_key, [])
                    nic_data[key] = addresses[0] if addresses else "Not Available"
                elif key == "PrimaryStatus":
                    # Health status from Status
                    nic_data[key] = member.get("Status", {}).get("Health", "Unknown")
                else:
                    nic_data[key] = member.get(response_key, "Not Available")

            nic_list.append(nic_data)

    return {"NIC": nic_list}


def extract_pci_data(response):
    keys_to_search = {
        "BusWidth": "DataBusWidth",
        "DeviceDescription": "DeviceDescription",
        "DeviceID": "Key",
        "Manufacturer": "Manufacturer",
        "SlotLength": "SlotLength",
        "SlotType": "SlotType",
        "Description": "Description"
    }

    pci_list = []

    if "Members" in response and response["Members"]:
        for member in response["Members"]:
            pci_data = {}

            for key, response_key in keys_to_search.items():
                pci_data[key] = member.get(response_key, "Not Available")

            pci_list.append(pci_data)

    return {"PCIDevice": pci_list}


def extract_physical_disk_data(response):
    physical_disk_info = []
    physical_disk_info = response.get('Members', {})
    return {"PhysicalDisk": physical_disk_info}


def extract_power_supply_data(response, subsystem):
    keys_to_search = {
        "DetailedState": "Oem.Dell.DellPowerSupplyView.DetailedState",
        "DeviceDescription": "Oem.Dell.DellPowerSupplyView.DeviceDescription",
        "FQDD": "Id",
        "FirmwareVersion": "FirmwareVersion",
        "InputVoltage": "InputNominalVoltageType",
        "Key": "Id",
        "Manufacturer": "Manufacturer",
        "Model": "Model",
        "Name": "Name",
        "PartNumber": "PartNumber",
        "PowerSupplySensorState": "Oem.Dell.DellPowerSupplyView.PowerSupplySensorState",
        "PrimaryStatus": "Status.Health",
        "RAIDState": "Not Available",
        "Range1MaxInputPower": "Oem.Dell.DellPowerSupplyView.Range1MaxInputPowerWatts",
        "RedMinNumberNeeded": "Oem.Dell.DellPowerSupply.RedMinNumberNeeded",
        "RedTypeOfSet": "Oem.Dell.DellPowerSupplyView.RedTypeOfSet",
        "Redundancy": "Oem.Dell.DellPowerSupplyView.RedundancyStatus",
        "SerialNumber": "SerialNumber",
        "TotalOutputPower": "TotalOutputPower",
        "Type": "PowerSupplyType",
        "powerSupplyStateCapabilitiesUnique": "Oem.Dell.DellPowerSupplyView.powerSupplyStateCapabilitiesUnique"
    }

    power_supply_list = []

    if "Members" in response and response["Members"]:
        for member in response["Members"]:
            power_supply_data = {}

            for key, response_key in keys_to_search.items():

                if '.' in response_key:
                    keys = response_key.split('.')
                    data = member
                    for k in keys:
                        data = data.get(k, "Not Available")
                    power_supply_data[key] = data
                else:
                    power_supply_data[key] = member.get(response_key, "Not Available")

            power_supply_list.append(power_supply_data)

    subsystem.append({
        "Key": "Power Supply",
        "PrimaryStatus": power_supply_list[0].get("PrimaryStatus", "Unknown") if power_supply_list else "Unknown"
    })

    return {"PowerSupply": power_supply_list}


def extract_sensors_voltage_data(response, Subsystem):
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

    voltage_sensor_list = []

    if "Voltages" in response and isinstance(response["Voltages"], list):
        for sensor in response["Voltages"]:
            sensor_data = {}

            for key, response_key in keys_to_search.items():
                if key == "DeviceID":
                    sensor_data[key] = f"iDRAC.Embedded.1#{sensor.get('Name', 'Unknown')}"
                elif '.' in response_key:
                    keys = response_key.split('.')
                    data = sensor
                    for k in keys:
                        data = data.get(k, "Not Available")
                    sensor_data[key] = data
                else:
                    sensor_data[key] = sensor.get(response_key, "Not Available")

            voltage_sensor_list.append(sensor_data)

    Subsystem.append({
        "Key": "Sensors_Voltage",
        "PrimaryStatus": voltage_sensor_list[0].get("PrimaryStatus", "Unknown") if voltage_sensor_list else "Unknown"
    })

    return {"Sensors_Voltage": voltage_sensor_list}


def extract_sensors_battery_data(response, subsystem):
    keys_to_search = {
        "CurrentReading": "Not Available",
        "CurrentState": response.get("CurrentState", "Not Available"),
        "DeviceID": "iDRAC.Embedded.1#SystemBoardCMOSBattery",
        "HealthState": response.get("HealthState", "Not Available"),
        "Key": "System Board CMOS Battery",
        "Location": "System Board CMOS Battery",
        "OtherSensorTypeDescription": "Battery",
        "PrimaryStatus": "Healthy",
        "SensorType": "Battery",
        "State": response.get("EnabledState", "Not Available")
    }

    battery_sensor_data = {}

    for key, value in keys_to_search.items():
        battery_sensor_data[key] = value if isinstance(value, str) else value

    primary_status = battery_sensor_data.get("PrimaryStatus", "Unknown")

    subsystem.append({
        "Key": "Sensors_Battery",
        "PrimaryStatus": primary_status
    })

    return {"Sensors_Battery": battery_sensor_data}


def extract_sensors_fan_data(response, subsystem):
    keys_to_search = {
        "CurrentReading": "CurrentReading",
        "CurrentState": "CurrentState",
        "DeviceID": "DeviceID",
        "FQDD": "FQDD",
        "HealthState": "HealthState",
        "Key": "Key",
        "Location": "Location",
        "Name": "Name",
        "OtherSensorTypeDescription": "OtherSensorTypeDescription",
        "PrimaryStatus": "PrimaryStatus",
        "SensorType": "SensorType",
        "State": "State",
        "SubType": "SubType",
        "Type": "Type",
        "coolingUnitIndexReference": "coolingUnitIndexReference"
    }

    sensor_fan_list = []

    if "Members" in response and response["Members"]:
        for member in response["Members"]:
            sensor_fan_data = {}

            for key, response_key in keys_to_search.items():
                sensor_fan_data[key] = member.get(response_key, "Not Available")

            sensor_fan_list.append(sensor_fan_data)

            primary_status = sensor_fan_data.get("PrimaryStatus", "Unknown")
            subsystem.append({
                "Key": "Sensors_fan",
                "PrimaryStatus": primary_status
            })

    return {"FanSensors": sensor_fan_list}


def extract_sensors_intrusion_data(response, subsystem):
    keys_to_search = {
        "CurrentReading": "Not Available",
        "CurrentState": "No Breach",
        "DeviceID": "iDRAC.Embedded.1#SystemBoardIntrusion",
        "HealthState": "Normal",
        "Key": "System Board Intrusion",
        "Location": "System Board Intrusion",
        "OtherSensorTypeDescription": "Not Available",
        "PrimaryStatus": "Healthy",
        "SensorType": "Intrusion",
        "State": "Enabled",
        "Type": "Not Available"
    }

    intrusion_sensor_data = {}

    for key, value in keys_to_search.items():
        intrusion_sensor_data[key] = value

    intrusion_sensor_data["CurrentState"] = response.get("PhysicalSecurity", {}).get("IntrusionSensor", "Not Available")

    subsystem.append({
        "Key": "Sensors_Intrusion",
        "PrimaryStatus": intrusion_sensor_data.get("PrimaryStatus", "Unknown")
    })

    return {"Sensors_Intrusion": intrusion_sensor_data}


def extract_sensors_temperature_data(response, Subsystem):
    keys_to_search = {
        "CurrentReading": "CurrentReading",
        "CurrentState": "CurrentState",
        "DeviceID": "DeviceID",
        "HealthState": "HealthState",
        "Key": "Key",
        "Location": "Location",
        "OtherSensorTypeDescription": "OtherSensorTypeDescription",
        "PrimaryStatus": "PrimaryStatus",
        "SensorType": "SensorType",
        "State": "State",
        "Type": "Type"
    }

    temperature_sensor_list = []

    if "Members" in response and response["Members"]:
        for member in response["Members"]:
            temperature_sensor_data = {}
            for key, response_key in keys_to_search.items():
                temperature_sensor_data[key] = member.get(response_key, "Not Available")

            Subsystem.append({
                "Key": "Sensors_Temperature",
                "PrimaryStatus": temperature_sensor_data.get("PrimaryStatus", "Unknown")
            })

            temperature_sensor_list.append(temperature_sensor_data)

    return {"Sensors_Temperature": temperature_sensor_list}


def extract_system_data(response, Subsystem):
    system_info = []
    systems = response.get("Oem", {}).get("Dell", {}).get("DellSystem", None)
    system_info.append(systems)

    Subsystem.append({
        "Key": "System",
        "Status": response.get("Status", {}).get("Health", "Unknown")
    })
    return {"System": system_info}


def extract_video_data(response):
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

    return {"Video": video_list}


def extract_virtual_disk_data(response):
    keys_to_search = {
        "BlockSizeBytes": "BlockSizeBytes",
        "CapacityBytes": "CapacityBytes",
        "Description": "Description",
        "Id": "Id",
        "Name": "Name",
        "MediaSpanCount": "MediaSpanCount",
        "VolumeType": "VolumeType",
        "Health": "Status.Health",
        "HealthRollup": "Status.HealthRollup",
        "State": "Status.State",
        "RAIDType": "RAIDType",
        "ReadCachePolicy": "ReadCachePolicy",
        "WriteCachePolicy": "WriteCachePolicy"
    }

    virtual_disk_list = []

    if "Members" in response and response["Members"]:
        for member in response["Members"]:
            virtual_disk_data = {}

            for key, response_key in keys_to_search.items():
                keys = response_key.split('.')
                value = member

                for k in keys:
                    value = value.get(k, "Not Available")
                    if value == "Not Available":
                        break

                virtual_disk_data[key] = value

            virtual_disk_list.append(virtual_disk_data)

    return {"VirtualDisk": virtual_disk_list}


def get_storage_controllers(idrac, module):

    storage_uri = '/redfish/v1/Systems/System.Embedded.1/Storage'
    response = idrac.invoke_request(method='GET', uri=storage_uri)

    if response.status_code == 200:
        storage_data = response.json_data
        controllers = storage_data.get("Members", [])
        controller_uris = []

        for controller in controllers:
            controller_uri = controller.get("@odata.id")
            if controller_uri:
                controller_uris.append(controller_uri)

        return controller_uris


def get_enclosure_uris(idrac, module):
    chassis_uri = '/redfish/v1/Chassis'
    response = idrac.invoke_request(method='GET', uri=chassis_uri)

    if response.status_code == 200:
        chassis_data = response.json_data
        members = chassis_data.get("Members", [])
        enclosure_uris = []

        for member in members:
            member_uri = member.get("@odata.id")
            if member_uri and "Enclosure" in member_uri:
                enclosure_uris.append(member_uri)

        return enclosure_uris

    return []


def extract_physical_disk_data(response):
    keys_to_search = {
        "BlockSizeBytes": "BlockSizeBytes",
        "CapableSpeedGbs": "CapableSpeedGbs",
        "CapacityBytes": "CapacityBytes",
        "ConfigurationLock": "ConfigurationLock",
        "Description": "Description",
        "EncryptionAbility": "EncryptionAbility",
        "EncryptionStatus": "EncryptionStatus",
        "FailurePredicted": "FailurePredicted",
        "HotspareType": "HotspareType",
        "Id": "Id",
        "Manufacturer": "Manufacturer",
        "MediaType": "MediaType",
        "Model": "Model",
        "PartNumber": "PartNumber",
        "PredictedMediaLifeLeftPercent": "PredictedMediaLifeLeftPercent",
        "Protocol": "Protocol",
        "Revision": "Revision",
        "RotationSpeedRPM": "RotationSpeedRPM",
        "SerialNumber": "SerialNumber",
        "Status": "Status",
    }

    physical_disk_list = []

    if "Members" in response and response["Members"]:
        for member in response["Members"]:
            physical_disk_data = {}

            for key, response_key in keys_to_search.items():
                physical_disk_data[key] = member.get(response_key, "Not Available")

            physical_disk_list.append(physical_disk_data)

    return {"PhysicalDisk": physical_disk_list}


def extract_idrac_data(response):
    keys_to_search = {
        "DNSDomainName": "DNSDomainName",
        "DNSRacName": "DNSRacName",
        "DeviceDescription": "DeviceDescription",
        "FQDD": "FQDD",
        "FirmwareVersion": "FirmwareVersion",
        "GUID": "GUID",
        "GroupName": "GroupName",
        "GroupStatus": "GroupStatus",
        "IPMIVersion": "IPMIVersion",
        "IPv4Address": "IPv4Address",
        "IPv6Address": "IPv6Address",
        "Key": "Id",
        "LANEnabledState": "InterfaceEnabled",
        "MACAddress": "MACAddress",
        "Model": "EthernetInterfaceType",
        "NICDuplex": "FullDuplex",
        "NICSpeed": "SpeedMbps",
        "PermanentMACAddress": "PermanentMACAddress",
        "ProductDescription": "Description",
        "ProductInfo": "Name",
        "SOLEnabledState": "Not Applicable",
        "SystemLockDown": "LinkStatus",
        "URLString": "UefiDevicePath"
    }

    idrac_list = []

    if "Members" in response and response["Members"]:
        for member in response["Members"]:
            idrac_data = {}

            for key, response_key in keys_to_search.items():
                if response_key == "IPv4Addresses":
                    ipv4_list = member.get("IPv4Addresses", [])
                    idrac_data[key] = ipv4_list[0]["Address"] if ipv4_list else "Not Available"
                elif response_key == "IPv6Addresses":
                    ipv6_list = member.get("IPv6Addresses", [])
                    idrac_data[key] = ipv6_list[0]["Address"] if ipv6_list else "Not Available"
                elif response_key == "Status":
                    status = member.get("Status", {})
                    idrac_data["PrimaryStatus"] = status.get("Health", "Not Available")
                else:
                    idrac_data[key] = member.get(response_key, "Not Available")

            idrac_list.append(idrac_data)

    return {"iDRAC": idrac_list}


def extract_idrac_nic_data(response):
    keys_to_search = {
        "FQDD": "Id",
        "GroupName": "Not Available",
        "GroupStatus": "Not Available",
        "IPv4Address": "IPv4Addresses",
        "IPv6Address": "IPv6Addresses",
        "Key": "Id",
        "NICDuplex": "FullDuplex",
        "NICEnabled": "InterfaceEnabled",
        "NICSpeed": "SpeedMbps",
        "PermanentMACAddress": "PermanentMACAddress",
        "PrimaryStatus": "Status",
        "ProductInfo": "Integrated Dell Remote Access Controller",
        "SwitchConnection": "Not Available",
        "SwitchPortConnection": "Not Available"
    }

    idrac_nic_list = []

    if "Members" in response and response["Members"]:
        for member in response["Members"]:
            nic_data = {}

            for key, response_key in keys_to_search.items():
                if response_key == "IPv4Addresses":
                    ipv4_list = member.get("IPv4Addresses", [])
                    nic_data[key] = ipv4_list[0]["Address"] if ipv4_list else "Not Available"
                elif response_key == "IPv6Addresses":
                    ipv6_list = member.get("IPv6Addresses", [])
                    nic_data[key] = ipv6_list[0]["Address"] if ipv6_list else "Not Available"
                elif response_key == "Status":
                    status = member.get("Status", {})
                    nic_data["PrimaryStatus"] = status.get("Health", "Not Available")
                else:
                    nic_data[key] = member.get(response_key, response_key) if response_key != "Not Available" else "Not Available"

            idrac_nic_list.append(nic_data)

    return {"iDRACNIC": idrac_nic_list}


def get_idrac_system_info(idrac, module):
    try:
        response = idrac.invoke_request(method='GET', uri=GET_IDRAC_FIRMWARE_URI_10)
        if response.status_code == 200:
            combined_data = {}
            Subsystem = []
            uris = {
                "bios": GET_IDRAC_BIOS_DETAILS_URI_10,
                "cpu": GET_IDRAC_CPU_DETAILS_URI_10,
                "controller": GET_IDRAC_CONTROLLER_DETAILS_URI_10,
                "controller_battery": GET_IDRAC_CONTROLLER_BATTERY_DETAILS_URI_10,
                "enclosure": GET_IDRAC_CHASSIS_URI_10,
                "enclosure_fan": GET_IDRAC_ENCLOSURE_FAN_SENSOR_DETAILS_URI_10,
                "enclosure_temp": GET_IDRAC_ENCLOSURE_TEMP_SENSOR_DETAILS_URI_10,
                "fan": GET_IDRAC_FAN_DETAILS_URI_10,
                "license": GET_IDRAC_LICENSE_DETAILS_URI_10,
                "memory": GET_IDRAC_MEMORY_DETAILS_URI_10,
                "nic": GET_IDRAC_NIC_DETAILS_URI_10,
                "pci": GET_IDRAC_PCI_DETAILS_URI_10,
                "physical_disk": GET_IDRAC_STORAGE_DETAILS_URI_10,
                "power_supply": GET_IDRAC_POWER_SUPPLY_DETAILS_URI_10,
                "sensors_voltage": GET_IDRAC_SENSOR_VOLTAGE_DETAILS_URI_10,
                "sensors_battery": GET_IDRAC_SENSOR_BATTERY_DETAILS_URI_10,
                "sensor_fan": GET_IDRAC_SENSOR_FAN_DETAILS_URI_10,
                "sensors_intrusion": GET_IDRAC_SENSOR_INTRUSION_DETAILS_URI_10,
                "sensors_temp": GET_IDRAC_SENSOR_TEMPERATURE_DETAILS_URI_10,
                "system": GET_IDRAC_SYSTEM_DETAILS_URI_10,
                "video": GET_IDRAC_VIDEO_DETAILS_URI_10,
                "virtual_disk": GET_IDRAC_STORAGE_DETAILS_URI_10,
                "iDRAC": GET_IDRAC_NIC_DETAILS_URI_10,
                "iDRACNIC": GET_IDRAC_NIC_DETAILS_URI_10
            }

            for key, uri in uris.items():
                system_response = idrac.invoke_request(method='GET', uri=uri)

                if system_response.status_code == 200:
                    data = system_response.json_data

                    if key == "bios":
                        bios_data = extract_bios_data(data)
                        filter_data = remove_key(bios_data)
                        combined_data.update(filter_data)
                    elif key == "cpu":
                        cpu_data = extract_cpu_data(data, Subsystem)
                        combined_data.update(cpu_data)
                    elif key == "controller":
                        controller_data = extract_controller_data(data)
                        combined_data.update(controller_data)
                    elif key == "controller_battery":
                        controller_battery_data = extract_controller_battery_data(data)
                        combined_data.update(controller_battery_data)
                    elif key == "controller_sensor":
                        controller_sensor_data = extract_controller_sensor_data(data)
                        combined_data.update(controller_sensor_data)
                    elif key == "enclosure":
                        enclosure_uris = get_enclosure_uris(idrac, module)
                        all_enclosure_data = []
                        if enclosure_uris:
                            for enclosure_uri in enclosure_uris:
                                oem_uri = f"{enclosure_uri}/Oem/Dell/DellEnclosures"
                                oem_response = []
                                oem_response = idrac.invoke_request(method='GET', uri=oem_uri)
                                if oem_response.status_code == 200:
                                    all_enclosure_data.append(oem_response.json_data)

                            extracted_enclosure_data = extract_enclosure_data(all_enclosure_data)
                            combined_data.update(extracted_enclosure_data)
                        else:
                            combined_data["Enclosures"] = []

                    elif key == "enclosure_sensor":
                        enclosure_fan_data = extract_enclosure_fan_data(data)
                        combined_data.update(enclosure_fan_data)
                        enclosure_temp_data = extract_enclosure_temp_data(data)
                        combined_data.update(enclosure_temp_data)
                        combined_data["EnclosureSensors"].append({
                            "EnclosureFan": enclosure_fan_data
                        })
                        combined_data["EnclosureSensors"].append({
                            "EnclosureTemperature": enclosure_temp_data
                        })
                    elif key == "fan":
                        fan_data = extract_fan_data(data)
                        combined_data.update(fan_data)
                    elif key == "license":
                        license_data = extract_license_data(data, Subsystem)
                        combined_data.update(license_data)
                    elif key == "memory":
                        memory_data = extract_memory_data(data, Subsystem)
                        combined_data.update(memory_data)
                    elif key == "nic":
                        nic_data = extract_nic_data(data)
                        combined_data.update(nic_data)
                    elif key == "pci":
                        pci_data = extract_pci_data(data)
                        combined_data.update(pci_data)
                    elif key == "physical_disk":
                        controller_uris = get_storage_controllers(idrac, module)
                        all_physical_disk_data = {}

                        for controller_uri in controller_uris:
                            drives_uri = f"{controller_uri}/?$select=Drives"
                            drives_response = idrac.invoke_request(method='GET', uri=drives_uri)

                            if drives_response.status_code == 200:
                                drives_data = drives_response.json_data

                                drive_uris = []
                                if "Drives" in drives_data:
                                    for drive in drives_data["Drives"]:
                                        drive_uri = drive.get("@odata.id")
                                        if drive_uri:
                                            drive_uris.append(drive_uri)

                                drive_data_list = []
                                for drive_uri in drive_uris:
                                    drive_response = idrac.invoke_request(method='GET', uri=drive_uri)
                                    if drive_response.status_code == 200:
                                        drive_data_list.append(drive_response.json_data)

                                extracted_physical_disk_data = extract_physical_disk_data({"Members": drive_data_list})
                                all_physical_disk_data.update(extracted_physical_disk_data)

                        combined_data.update(all_physical_disk_data)

                    elif key == "power_supply":
                        power_supply_data = extract_power_supply_data(data, Subsystem)
                        combined_data.update(power_supply_data)
                    elif key == "sensors_voltage":
                        sensors_voltage_data = extract_sensors_voltage_data(data, Subsystem)
                        combined_data.update(sensors_voltage_data)
                    elif key == "sensors_battery":
                        sensors_battery_data = extract_sensors_battery_data(data, Subsystem)
                        combined_data.update(sensors_battery_data)
                    elif key == "sensors_fan":
                        sensors_fan_data = extract_sensors_fan_data(data, Subsystem)
                        combined_data.update(sensors_fan_data)
                    elif key == "sensors_intrusion":
                        sensors_intrusion_data = extract_sensors_intrusion_data(data, Subsystem)
                        combined_data.update(sensors_intrusion_data)
                    elif key == "sensors_temp":
                        sensors_temp_data = extract_sensors_temperature_data(data, Subsystem)
                        combined_data.update(sensors_temp_data)
                    elif key == "system":
                        system_data = extract_system_data(data, Subsystem)
                        filter_data = remove_key(system_data)
                        combined_data.update(filter_data)
                    elif key == "video":
                        video_data = extract_video_data(data)
                        combined_data.update(video_data)
                    elif key == "virtual_disk":
                        controller_uris = get_storage_controllers(idrac, module)

                        for controller_uri in controller_uris:
                            virtual_disk_uri = f"{controller_uri}/Volumes?$expand=*($levels=1)"
                            virtual_disk_response = idrac.invoke_request(method='GET', uri=virtual_disk_uri)

                            if virtual_disk_response.status_code == 200:
                                extracted_virtual_disk_data = extract_virtual_disk_data(virtual_disk_response.json_data)
                                combined_data.update(extracted_virtual_disk_data)
                    elif key == "iDRAC":
                        idrac_data = extract_idrac_data(data)
                        combined_data.update(idrac_data)
                    elif key == "iDRACNIC":
                        idrac_nic_data = extract_idrac_nic_data(data)
                        combined_data.update(idrac_nic_data)

            combined_data["EnclosureSensors"] = {
                "EnclosureFan": combined_data.get("EnclosureFans", []),
                "EnclosureTemperature": combined_data.get("EnclosureTemperatures", [])
            }

            combined_data["Subsystem"] = Subsystem
            return combined_data

    except HTTPError as err:
        return get_from_wsman(module)


def get_from_wsman(module):
    with iDRACConnection(module.params) as idrac:
        idrac.get_entityjson()
        msg = idrac.get_json_device()
        return msg


def main():
    specs = {}
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        supports_check_mode=True)
    try:
        with iDRACRedfishAPI(module.params) as idrac:
            system_info = get_idrac_system_info(idrac, module)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, SSLValidationError, IOError, ValueError, TypeError, ConnectionError) as e:
        module.fail_json(msg=str(e))

    module.exit_json(msg="Successfully fetched the system inventory details.",
                     system_info=system_info)


if __name__ == '__main__':
    main()
