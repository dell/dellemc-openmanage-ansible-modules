import sys
import json
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI

NA = "Not Available"

enclosure_uri = sys.argv[1]
idrac_host = sys.argv[2]
idrac_user = sys.argv[3]
idrac_password = sys.argv[4]
idrac_port = sys.argv[5]


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


full_url = f"{enclosure_uri}"

params = {
    "idrac_ip": idrac_host,
    "idrac_user": idrac_user,
    "idrac_password": idrac_password,
    "idrac_port": idrac_port,
    "validate_certs": False
}

red_api = iDRACRedfishAPI(params)
response = red_api.invoke_request(method='GET', uri=full_url)

enclosure_json = response.json_data

structured = get_enclosure_data(enclosure_json)

enclosure_sensor_info = get_controller_enclosure_sensor_info(enclosure_json)

output = {
    "Enclosure": [structured],
    "EnclosureSensor": enclosure_sensor_info
}

print(json.dumps(output, ensure_ascii=False))
