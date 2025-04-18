import sys
import json

sensors_api_output = sys.argv[1]
# intrusion_api_ouput = sys.argv[2]
NA = "Not Available"


def sensors_intrusion_mapped_data(resp):
    health_state = resp.get("HealthState", NA)
    output = {
        "CurrentReading": resp.get("CurrentReading", NA),
        "CurrentState": resp.get("CurrentState", NA),
        "DeviceID": resp.get("Id", NA),
        "HealthState": resp.get("HealthState", NA),
        "Key": resp.get("ElementName", NA),
        "Location": resp.get("ElementName", NA),
        "OtherSensorTypeDescription": NA,
        "PrimaryStatus": "Healthy" if health_state == "OK" else health_state,
        "SensorType": resp.get("SensorType", NA),
        "State": resp.get("EnabledState", NA),
        "Type": NA
    }
    return output


output = []
sensors_output = json.loads(sensors_api_output)
for mem in sensors_output.get("Members", []):
    if mem.get("ElementName", "") == "System Board Intrusion":
        output.append(sensors_intrusion_mapped_data(mem))
