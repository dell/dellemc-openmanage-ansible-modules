import json
import sys

NA = "Not Available"
sensors_api_output = sys.argv[1]


def mapped_sensors_intrusion_data(resp):
    health_state = resp.get("HealthState", NA)
    output = {
        "Type": NA,
        "CurrentReading": resp.get("CurrentReading", NA),
        "DeviceID": resp.get("Id", NA),
        "HealthState": resp.get("HealthState", NA),
        "SensorType": resp.get("SensorType", NA),
        "Key": resp.get("ElementName", NA),
        "OtherSensorTypeDescription": NA,
        "State": resp.get("EnabledState", NA),
        "CurrentState": resp.get("CurrentState", NA),
        "Location": resp.get("ElementName", NA),
        "PrimaryStatus": "Healthy" if health_state == "OK" else health_state
    }
    return output


sensors_output = json.loads(sensors_api_output)
output = []
for mem in sensors_output.get("Members", []):
    if mem.get("ElementName", "") == "System Board Intrusion":
        output.append(mapped_sensors_intrusion_data(mem))
print(output)
