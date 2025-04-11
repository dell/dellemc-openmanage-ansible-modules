import sys
import json
import ast

enclosure_api_output = sys.argv[1]
NA = "Not Available"


def map_enclosure_data(resp):
    dellchassis = resp.get("Oem", {}).get("Dell", {}).get("DellChassisEnclosure", {})
    return {
        "AssetTag": NA if (asset := resp.get("AssetTag")) == "" else asset,
        "Connector": str(dellchassis.get("Connector", NA)),
        "DeviceDescription": resp.get("Description", NA),
        "EMMCount": str(dellchassis.get("Links", {}).get("DellEnclosureEMMCollection@odata.count", NA)),
        "FQDD": resp.get("Id", NA),
        "FanCount": NA,
        "Key": resp.get("Id", NA),
        "PSUCount": NA,
        "PrimaryStatus": resp.get("Status", {}).get("Health", NA),
        "ProductName": resp.get("Name", NA),
        "ServiceTag": NA if (svctag := dellchassis.get("ServiceTag")) is None else svctag,
        "SlotCount": str(dellchassis.get("SlotCount", NA)),
        "State": NA,
        "Version": dellchassis.get("Version", NA),
        "WiredOrder": str(dellchassis.get("WiredOrder", NA))
    }


def map_enclosure_sensor(enclosure):
    return {
        "FQDD": enclosure.get("FQDD", NA),
        "Key": enclosure.get("Key", NA)
    }


enclosure_data = ast.literal_eval(enclosure_api_output)
enclosure_data = json.loads(enclosure_data)

enclosure = map_enclosure_data(enclosure_data)
sensor = map_enclosure_sensor(enclosure)

print(json.dumps({
    "Enclosure": [enclosure],
    "EnclosureSensor": [sensor]
}, ensure_ascii=False))
