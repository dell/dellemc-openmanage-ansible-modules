import sys
import json

GET_IDRAC_SYSTEM_JSON = sys.argv[1]
GET_IDRAC_FIRMWARE_JSON = sys.argv[2]
NA = ""


def get_bios_release_date_and_version_and_symbios(system_data):
    version = system_data.get("BiosVersion", NA)
    system = system_data.get("Oem", {}).get("Dell", {}).get("DellSystem", {})
    is_symbios_available = "True" if system.get("smbiosGUID", "") else "False"
    return system.get("BIOSReleaseDate", NA), version, is_symbios_available


def get_bios_fqdd_and_instance_id_and_key(firmware_data):
    members = firmware_data.get("Members", [])
    for each in members:
        if each.get('ElementName', '') == 'BIOS' and each.get('Status', '') == 'Installed':
            instance_id = each.get('Id', NA)
            fqdd = instance_id.split('__')[-1] if '__' in instance_id else NA
            key = fqdd
            return fqdd, instance_id, key
    return NA, NA, NA


system_data = json.loads(GET_IDRAC_SYSTEM_JSON)
firmware_data = json.loads(GET_IDRAC_FIRMWARE_JSON)

bios_release_date, version_string, symbios = get_bios_release_date_and_version_and_symbios(system_data)
fqdd, instance_id, key = get_bios_fqdd_and_instance_id_and_key(firmware_data)

output = {
    "BIOSReleaseDate": bios_release_date,
    "FQDD": fqdd,
    "InstanceID": instance_id,
    "Key": key,
    "SMBIOSPresent": symbios,
    "VersionString": version_string
}

print(json.dumps([output], indent=2, ensure_ascii=False))
