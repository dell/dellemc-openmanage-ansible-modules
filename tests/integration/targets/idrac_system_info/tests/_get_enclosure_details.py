import sys
import json
import requests
from requests.auth import HTTPBasicAuth

NA = "Not Available"

enclosure_uri = sys.argv[1]
idrac_host = sys.argv[2]
idrac_user = sys.argv[3]
idrac_password = sys.argv[4]


def get_enclosure_data(resp):
    dellchasis = resp.get("Oem", {}).get("Dell", {}).get("DellChassisEnclosure", {})
    asset = resp.get("AssetTag")
    svctag = dellchasis.get("ServiceTag")
    return {
        "AssetTag": NA if asset == "" else asset,
        "Connector": str(dellchasis.get("Connector")),
        "DeviceDescription": resp.get("Description"),
        "EMMCount": str(dellchasis.get("Links", {}).get("DellEnclosureEMMCollection@odata.count")),
        "FQDD": resp.get("Id", NA),
        "FanCount": NA,
        "Key": resp.get("Id", NA),
        "PSUCount": NA,
        "PrimaryStatus": resp.get("Status", {}).get("Health", NA),
        "ProductName": resp.get("Name", NA),
        "ServiceTag": NA if svctag is None else svctag,
        "SlotCount": str(dellchasis.get("SlotCount", NA)),
        "State": NA,
        "Version": dellchasis.get("Version", NA),
        "WiredOrder": str(dellchasis.get("WiredOrder", NA))
    }


def get_controller_enclosure_sensor_info(resp):
    enclosure_sensor_info = []
    enclosure_sensor_info.append({
        "FQDD": resp.get("Id", NA),
        "Key": resp.get("Id", NA)
    })
    return enclosure_sensor_info


full_url = f"{idrac_host}{enclosure_uri}"

response = requests.get(full_url, auth=HTTPBasicAuth(idrac_user, idrac_password), verify=False)
response.raise_for_status()

enclosure_json = response.json()

structured = get_enclosure_data(enclosure_json)

enclosure_sensor_info = get_controller_enclosure_sensor_info(enclosure_json)

output = {
    "Enclosure": [structured],
    "EnclosureSensor": enclosure_sensor_info
}

print(json.dumps(output, ensure_ascii=False))
