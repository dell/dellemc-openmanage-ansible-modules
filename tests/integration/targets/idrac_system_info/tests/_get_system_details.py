import json
import sys

NA = "Not Available"
system_api_output = sys.argv[1]
manager_api_output = sys.argv[2]
bios_api_data = sys.argv[3]
manager_system_attributes_api_output = sys.argv[4]
idrac_attributes_api_output = sys.argv[5]


def get_firmwarever_idrac_url(manager_output):
    power_state = manager_output.get("PowerState", "")
    idrac_url = manager_output.get("Oem", {}).\
        get("Dell", {}).get("DelliDRACCard", {}).get("URLString", "")
    version = manager_output.get("FirmwareVersion", "")
    return version , idrac_url , power_state


def get_system_memsize_and_cpldversion_and_manufacturer():
    bios_data = json.loads(bios_api_data)
    manufacturer = bios_data.get("Attributes", {}).get("SystemManufacturer", "")
    memsize = bios_data.get("Attributes", {}).get("SysMemSize", "")
    cpld_version = bios_data.get("Attributes", {}).get("SystemCpldVersion", "")
    return cpld_version, memsize, manufacturer


def get_system_os_version_and_os_name():
    system_attributes_output = json.loads(manager_system_attributes_api_output)
    os_version = system_attributes_output.get("Attributes", {}).get("ServerOS.1.OSVersion", "")
    os_name = system_attributes_output.get("Attributes", {}).get("ServerOS.1.OSName", "")
    return os_name, os_version


def get_sys_lockdownmode():
    idrac_attributes = json.loads(idrac_attributes_api_output)
    system_lockdown_mode = idrac_attributes.get("Attributes", {}).get("Lockdown.1.SystemLockdown", "")
    return system_lockdown_mode


def mapped_data_system(resp, manager_output):
    firmware_ver, idrac_url, power_state = get_firmwarever_idrac_url(manager_output)
    system_data = resp.get("Oem", {}).get("Dell", {}).get("DellSystem", {})
    os_name, os_version = get_system_os_version_and_os_name()
    cpld_version, memsize, manufacturer = get_system_memsize_and_cpldversion_and_manufacturer()
    health_rollup = resp.get("Status", {}).get("HealthRollup")
    system_lockdown_mode = get_sys_lockdownmode()
    output = {
        "smbiosGUID": system_data.get("smbiosGUID", NA),
        "BIOSReleaseDate": system_data.get("BIOSReleaseDate", NA),
        "AssetTag": NA if (asset := resp.get("AssetTag")) == "" else asset,
        "_Type": "Server",
        "BaseBoardChassisSlot": system_data.get("BaseBoardChassisSlot", NA),
        "BladeGeometry": system_data.get("BladeGeometry", NA),
        "BoardSerialNumber": system_data.get("BoardSerialNumber", NA),
        "CMCIP": system_data.get("CMCIP", NA),
        "ChassisModel": system_data.get("ChassisModel", NA),
        "ChassisName": system_data.get("ChassisName", NA),
        "ChassisSystemHeight": system_data.get("ChassisSystemHeightUnit", NA),
        "CurrentRollupStatus": system_data.get("CurrentRollupStatus", NA),
        "DeviceType": resp.get("DeviceType", NA),
        "ExpressServiceCode": system_data.get("ExpressServiceCode", NA),
        "HostName": resp.get("HostName", NA),
        "Key": resp.get("SKU"),
        "LifecycleControllerVersion": NA if (firmware_ver == "") else firmware_ver,
        "Manufacturer": NA if (manufacturer == "") else manufacturer,
        "MaxCPUSockets": system_data.get("MaxCPUSockets", NA),
        "MaxDIMMSlots": system_data.get("MaxDIMMSlots", NA),
        "MaxPCIeSlots": system_data.get("MaxPCIeSlots", NA),
        "MemoryOperationMode": system_data.get("MemoryOperationMode", NA),
        "Model": system_data.get("SystemGeneration", NA),
        "OSVersion": NA if (os_version == "") else os_version,
        "PlatformGUID": system_data.get("PlatformGUID", NA),
        "PowerCapEnabledState": system_data.get("PowerCapEnabledState", NA),
        "PowerState": NA if (power_state == "") else power_state,
        "RACType": system_data.get("RACType", NA),
        "SysMemTotalSize": NA if (memsize == "") else memsize,
        "SysName": system_data.get("Name", NA),
        "SystemGeneration": system_data.get("SystemGeneration", NA),
        "SystemID": system_data.get("SystemID", NA),
        "SystemLockDown": NA if (system_lockdown_mode == "") else system_lockdown_mode,
        "SystemRevision": system_data.get("SystemRevision", NA),
        "UUID": system_data.get("UUID", NA),
        "iDRACURL": NA if (idrac_url == "") else idrac_url,
        "BIOSVersionString": resp.get("BiosVersion", NA),
        "BoardPartNumber": system_data.get("BoardPartNumber", NA),
        "CPLDVersion": NA if (cpld_version == "") else cpld_version,
        "ChassisServiceTag": system_data.get("ChassisServiceTag", NA),
        "ServiceTag": system_data.get("NodeID", NA),
        "PowerCap": system_data.get("PowerCap", NA),
        "NodeID": system_data.get("NodeID", NA),
        "DeviceDescription": resp.get("Name"),
        "PrimaryStatus": "Healthy" if health_rollup == "OK" \
            else (health_rollup or "Not Available"),
        "MachineName": system_data.get("MachineName", NA),
        "OSName": NA if (os_name == "") else os_name,
        "ServerAllocation": system_data.get("ServerAllocation", NA),
    }
    return output


system_output = json.loads(system_api_output)
manager_output = json.loads(manager_api_output)
output = []
output.append(mapped_data_system(system_output, manager_output))
print(json.dumps(output, indent=2, ensure_ascii=False))
