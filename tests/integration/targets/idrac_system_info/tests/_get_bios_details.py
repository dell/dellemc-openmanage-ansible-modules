import json
import sys
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI

idrac_ip = sys.argv[1]
idrac_user = sys.argv[2]
idrac_password = sys.argv[3]
idrac_port = sys.argv[4]

GET_IDRAC_SYSTEM_URI = "/redfish/v1/Systems/System.Embedded.1"
GET_IDRAC_FIRMWARE_URI = "/redfish/v1/UpdateService/Oem/Dell/DellSoftwareInventory"

params = {
    "idrac_ip": idrac_ip,
    "idrac_user": idrac_user,
    "idrac_password": idrac_password,
    "idrac_port": idrac_port
}
idrac_obj = iDRACRedfishAPI(params)


def get_bios_release_date_and_version_and_symbios():
    response = idrac_obj.invoke_request(method='GET', uri=GET_IDRAC_SYSTEM_URI)
    if response.status_code == 200:
        version = response.json_data.get("BiosVersion", "")
        system = response.json_data.get("Oem", {}).get("Dell", {}).get("DellSystem", {})
        is_symbios_available = "True" if system.get("smbiosGUID", "") else "False"
        return system.get("BIOSReleaseDate", ""), version, is_symbios_available
    return "", "", ""


def get_bios_fqdd_and_instance_id_and_key():
    response = idrac_obj.invoke_request(method='GET', uri=GET_IDRAC_FIRMWARE_URI)
    if response.status_code == 200:
        members = response.json_data.get("Members")
        for each in members:
            if each.get('ElementName', '') == 'BIOS' and each.get('Status', '') == 'Installed':
                instance_id = each.get('Id')
                fqdd = instance_id.split('__')[-1]
                key = fqdd
                return fqdd, instance_id, key
    return "", "", ""


def get_bios_system_info():
    output = {
        "BIOSReleaseDate": "",
        "FQDD": "",
        "InstanceID": "",
        "Key": "",
        "SMBIOSPresent": "",
        "VersionString": ""
    }
    release, version, symbios = get_bios_release_date_and_version_and_symbios()
    fqdd, instance_id, key = get_bios_fqdd_and_instance_id_and_key()
    output["BIOSReleaseDate"] = release
    output["VersionString"] = version
    output["SMBIOSPresent"] = symbios
    output["FQDD"] = fqdd
    output["InstanceID"] = instance_id
    output["Key"] = key
    return [output]


print(json.dumps(get_bios_system_info()))
