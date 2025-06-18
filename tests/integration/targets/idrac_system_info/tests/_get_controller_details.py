import sys
import json

controller_api_output = sys.argv[1]
NA = "Not Available"


def get_controller_data(resp):
    output = {
        "Bus": NA,
        "T10PICapability": str(resp.get("T10PICapability", NA)),
        "ControllerFirmwareVersion": (
            str(resp.get("ControllerFirmwareVersion", NA))
        ),
        "DeviceCardDataBusWidth": str(resp.get("DeviceCardDataBusWidth", NA)),
        "SupportControllerBootMode": (
            str(resp.get("SupportControllerBootMode", NA))
        ),
        "DeviceCardManufacturer": NA,
        "DeviceCardSlotLength": str(resp.get("DeviceCardSlotLength", NA)),
        "DeviceCardSlotType": str(resp.get("DeviceCardSlotType", NA)),
        "EncryptionCapability": str(resp.get("EncryptionCapability", NA)),
        "EncryptionMode": str(resp.get("WiredOrder", NA)),
        "FQDD": str(resp.get("Id", NA)),
        "RollupStatus": str(resp.get("RollupStatus", NA)),
        "Key": str(resp.get("Id", NA)),
        "MaxAvailablePCILinkSpeed": (
            str(resp.get("MaxAvailablePCILinkSpeed", NA))
        ),
        "PCISlot": str(resp.get("PCISlot", NA)),
        "PCIVendorID": NA,
        "PrimaryStatus": NA,
        "DriverVersion": str(resp.get("DriverVersion", NA)),
        "SASAddress": str(resp.get("SASAddress", NA)),
        "SecurityStatus": str(resp.get("SecurityStatus", NA)),
        "MaxPossiblePCILinkSpeed": (
            str(resp.get("MaxPossiblePCILinkSpeed", NA))
        ),
        "SlicedVDCapability": (
            str(resp.get("SlicedVDCapability", NA))
        ),
        "SupportEnhancedAutoForeignImport": (
            str(resp.get("SupportEnhancedAutoForeignImport", NA))
        ),
        "CachecadeCapability": str(resp.get("CachecadeCapability", NA)),
        "SupportRAID10UnevenSpans": (
            str(resp.get("SupportRAID10UnevenSpans", NA))
        ),
        "CacheSize": str(resp.get("CacheSizeInMB")) + " MB",
        "DeviceDescription": NA,
        "ProductName": NA,
    }
    return output


output = []
controller_output = json.loads(controller_api_output)
for each_member in controller_output.get("Members", []):
    output.append(get_controller_data(each_member))
print(output)
