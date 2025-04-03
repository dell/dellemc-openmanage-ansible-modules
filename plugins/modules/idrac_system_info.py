#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.1.0
# Copyright (C) 2021-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

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
author: "Rajeev Arakkal (@rajeevarakkal)"
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
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.firmware.info import IDRACFirmwareInfo
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.bios.info import IDRACBiosInfo
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.cpu.info import IDRACCpuInfo
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.controller.enclosure_info import IDRACEnclosureInfo
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.fan.info import IDRACFanInfo
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.nic.info import IDRACNICInfo
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.sensors_battery.info import IDRACSensorsBatteryInfo
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.sensors_fan.info import IDRACSensorsFanInfo
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.sensors_intrusion.info import IDRACSensorsIntrusionInfo
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.sensors_voltage.info import IDRACSensorsVoltageInfo
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.system.info import IDRACSystemInfo
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.video.info import IDRACVideoInfo
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.subsystem.info import IDRACSubsystemInfo
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.license.info import IDRACLicenseInfo
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.memory.info import IDRACMemoryInfo
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, IdracAnsibleModule
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


# Main
def main():
    specs = {}
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        supports_check_mode=True)
    idrac_redfish_module = IdracAnsibleModule(
        argument_spec=specs,
        supports_check_mode=True
    )
    try:
        with iDRACRedfishAPI(idrac_redfish_module.params) as idrac:
            firmware_obj = IDRACFirmwareInfo(idrac)
            system_info_dict = {
                "BIOS": "",
                "CPU": "",
                "Enclosure": "",
                "EnclosureSensor": "",
                "License": "",
                "Memory": "",
                "iDRACNIC": "",
                "PCIDevice": "",
                "PowerSupply": "",
                "Sensors_Temperature": "",
                "Sensors_Battery": "",
                "Sensors_Fan": "",
                "Sensors_Intrusion": "",
                "Sensors_Voltage": "",
                "NIC": "",
                "Fan": "",
                "System": "",
                "Subsystem": "",
                "Controller": "",
                "PhysicalDisk": "",
                "Video": "",
                "iDRAC": ""
            }
            if not firmware_obj.is_omsdk_required():
                system_info_dict["BIOS"] = IDRACBiosInfo(idrac).get_bios_system_info()
                system_info_dict["CPU"] = IDRACCpuInfo(idrac).get_cpu_system_info()
                system_info_dict["Enclosure"] = IDRACEnclosureInfo(idrac).get_enclosure_system_info()
                system_info_dict["EnclosureSensor"] = IDRACEnclosureInfo(idrac).get_controller_enclosure_sensor_info(system_info_dict["Enclosure"])
                system_info_dict["Sensors_Battery"] = IDRACSensorsBatteryInfo(idrac).get_sensors_battery_info()
                system_info_dict["Sensors_Intrusion"] = IDRACSensorsIntrusionInfo(idrac).get_sensors_intrusion_info()
                system_info_dict["Sensors_Voltage"] = IDRACSensorsVoltageInfo(idrac).get_sensors_voltage_info()
                system_info_dict["Sensors_Fan"] = IDRACSensorsFanInfo(idrac).get_sensors_fan_info()
                system_info_dict["Fan"] = IDRACFanInfo(idrac).get_fan_info()
                system_info_dict["NIC"] = IDRACNICInfo(idrac).get_nic_info()
                system_info_dict["System"] = IDRACSystemInfo(idrac).get_system_info()
                system_info_dict["Video"] = IDRACVideoInfo(idrac).get_idrac_video_details()
                system_info_dict["Subsystem"] = IDRACSubsystemInfo(idrac).get_subsystem_info()
                system_info_dict["License"] = IDRACLicenseInfo(idrac).get_license_info()
                system_info_dict["Memory"] = IDRACMemoryInfo(idrac).get_memory_info()
            else:
                with iDRACConnection(module.params) as idrac:
                    idrac.get_entityjson()
                    system_info_dict = idrac.get_json_device()
    except HTTPError as err:
        module.exit_json(msg=str(err), error_info=json.load(err), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, SSLValidationError, IOError, ValueError, TypeError, ConnectionError) as e:
        module.exit_json(msg=str(e), failed=True)

    module.exit_json(msg="Successfully fetched the system inventory details.",
                     system_info=system_info_dict)


if __name__ == '__main__':
    main()
