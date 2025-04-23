import sys
import json
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI

NA = "Not Available"

storage_api_output = sys.argv[1]
idrac_host = sys.argv[2]
idrac_user = sys.argv[3]
idrac_password = sys.argv[4]
idrac_port = sys.argv[5]

NA = "Not Available"


def physical_disk_mapped_data(disk):
    physical_disk_data =\
        disk.get("Oem", {}).get("Dell", {}).get("DellPhysicalDisk", {})
    output = {
        "BusProtocol": NA,
        "T10PICapability": str(
            physical_disk_data.get("T10PICapability", NA)
        ),
        "DeviceDescription": str(disk.get("Description", NA)),
        "FQDD": str(disk.get("Id", NA)),
        "FreeSize": str(physical_disk_data.get("FreeSizeInBytes", NA)),
        "HotSpareStatus": NA,
        "Slot": str(physical_disk_data.get("Slot", NA)),
        "MaxCapableSpeed": str(disk.get("CapableSpeedGbs", NA)) + " Gbps",
        "RaidStatus": str(physical_disk_data.get("RaidStatus", NA)),
        "Manufacturer": str(disk.get("Manufacturer", NA)),
        "SASAddress": str(physical_disk_data.get("SASAddress", NA)),
        "ManufacturingYear": str(
            physical_disk_data.get("ManufacturingYear", NA)
        ),
        "MediaType": str(disk.get("MediaType", NA)),
        "PPID": str(physical_disk_data.get("PPID", NA)),
        "PredictiveFailureState": str(
            physical_disk_data.get("PredictiveFailureState", NA)
        ),
        "PrimaryStatus": NA,
        "Model": str(disk.get("Model", NA)),
        "RAIDNegotiatedSpeed": str(disk.get("RotationSpeedRPM", NA)),
        "RemainingRatedWriteEndurance": NA,
        "ManufacturingDay": str(
            physical_disk_data.get("ManufacturingDay", NA)
        ),
        "Revision": str(disk.get("Revision", NA)),
        "SecurityState": NA,
        "Key": str(disk.get("Id", NA)),
        "SerialNumber": str(disk.get("SerialNumber", NA)),
        "ManufacturingWeek": str(
            physical_disk_data.get("ManufacturingWeek", NA)
        ),
        "Size": NA,
        "SupportedEncryptionTypes": NA,
        "DriveFormFactor": str(
            physical_disk_data.get("DriveFormFactor", NA)
        ),
        "UsedSize": str(physical_disk_data.get("UsedSizeInBytes", NA)),
        "BlockSize": str(disk.get("BlockSizeBytes", NA))
    }
    return output


def get_physical_disk_info():
    output = []
    # Get storage collection
    storage_output = json.loads(storage_api_output)
    members = storage_output.get("Members", [])

    params = {
        "idrac_ip": idrac_host,
        "idrac_port": idrac_port,
        "idrac_password": idrac_password,
        "idrac_user": idrac_user,
        "validate_certs": False
    }

    red_api = iDRACRedfishAPI(params)

    for member in members:
        storage_uri = member.get("@odata.id")
        if not storage_uri:
            continue

        # Get storage entity details (RAID controller)
        storage_resp = red_api.invoke_request(method='GET', uri=storage_uri)
        if storage_resp.status_code != 200:
            continue

        drives = storage_resp.json_data.get("Drives", [])
        for drive in drives:
            drive_uri = drive.get("@odata.id")
            if not drive_uri:
                continue

            drive_resp = red_api.invoke_request(method='GET', uri=drive_uri)
            if drive_resp.status_code == 200:
                output.append(physical_disk_mapped_data(drive_resp.json_data))

    return output


print(get_physical_disk_info())
