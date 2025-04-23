import json
import json
import sys
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI

idrac_ip = sys.argv[1]
idrac_user = sys.argv[2]
idrac_password = sys.argv[3]
idrac_port = sys.argv[4]
NA = "Not Available"

GET_IDRAC_MANAGER_IDRAC_ATTRIBUTES = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/iDRAC.Embedded.1"
GET_IDRAC_SYSTEM_DETAILS_URI_10 = "/redfish/v1/Systems/System.Embedded.1"
GET_IDRAC_BIOS_URI = "/redfish/v1/Systems/System.Embedded.1/Bios"
GET_IDRAC_MANAGER_SYSTEM_ATTRIBUTES = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/System.Embedded.1"
GET_IDRAC_MANAGER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/"

params = {
    "idrac_ip": idrac_ip,
    "idrac_user": idrac_user,
    "idrac_password": idrac_password,
    "idrac_port": idrac_port
}
idrac_obj = iDRACRedfishAPI(params)


def get_firmwarever_idrac_url():
    response = idrac_obj.invoke_request(method='GET', uri=GET_IDRAC_MANAGER_URI)
    if response.status_code == 200:
        idrac_url = response.json_data.get("Oem", {}).\
            get("Dell", {}).get("DelliDRACCard", {}).get("URLString")
        version = response.json_data.get("FirmwareVersion", "")
        power_state = response.json_data.get("PowerState", "")
        return version , idrac_url , power_state
    return "", "", ""


def get_system_memsize_and_cpldversion_and_manufacturer():
    response = idrac_obj.invoke_request(method='GET', uri=GET_IDRAC_BIOS_URI)
    if response.status_code == 200:
        memsize = response.json_data.get("Attributes", {}).get("SysMemSize", "")
        cpld_version = response.json_data.get("Attributes", {}).\
            get("SystemCpldVersion", "")
        manufacturer = response.json_data.get("Attributes", {}).get("SystemManufacturer", "")
        return cpld_version, memsize, manufacturer
    return "", "", ""


def get_system_os_version_and_os_name():
    response = idrac_obj.invoke_request(method='GET', uri=GET_IDRAC_MANAGER_SYSTEM_ATTRIBUTES)
    if response.status_code == 200:
        os_version = response.json_data.get("Attributes", {}).\
            get("ServerOS.1.OSVersion", "")
        os_name = response.json_data.get("Attributes", {}).get("ServerOS.1.OSName", "")
        return os_name, os_version
    return "", ""


def get_sys_lockdownmode():
    response = idrac_obj.invoke_request(method='GET', uri=GET_IDRAC_MANAGER_IDRAC_ATTRIBUTES)
    if response.status_code == 200:
        system_lockdown_mode = response.json_data.\
            get("Attributes", {}).get("Lockdown.1.SystemLockdown", "")
        return system_lockdown_mode
    return "", ""


def mapped_data_system(resp):
    firmware_ver, idrac_url, power_state = get_firmwarever_idrac_url()
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
        "PrimaryStatus": "Healthy" if health_rollup == "OK" else (
            health_rollup or "Not Available"
        ),
        "MachineName": system_data.get("MachineName", NA),
        "OSName": NA if (os_name == "") else os_name,
        "ServerAllocation": system_data.get("ServerAllocation", NA),
    }
    return output


def get_system_info():
    output = []
    resp = idrac_obj.invoke_request(method='GET', uri=GET_IDRAC_SYSTEM_DETAILS_URI_10)
    if resp.status_code == 200:
        output.append(mapped_data_system(resp.json_data))
    return output


print(json.dumps(get_system_info()))
