
import sys
import json

sensors_api_output = sys.argv[1]
NA = "Not Available"


def sensors_battery_mapped_data(resp):
    health_state_map = {
        "CriticalFailure": "Critical",
        "Degraded/Warning": "Warning",
        "MajorFailure": "Critical",
        "MinorFailure": "Critical",
        "NonRecoverableError": "Critical",
        "OK": "Healthy",
        "Unknown": "Unknown"
    }
    health_state = resp.get("HealthState", NA)
    primary_status = health_state_map.get(health_state, NA)
    output = {
        "CurrentReading": resp.get("CurrentReading", NA),
        "CurrentState": resp.get("CurrentState", NA),
        "DeviceID": resp.get("Id", NA),
        "HealthState": resp.get("HealthState", NA),
        "Key": resp.get("ElementName", NA),
        "Location": resp.get("ElementName", NA),
        "OtherSensorTypeDescription": NA,
        "PrimaryStatus": primary_status,
        "SensorType": resp.get("SensorType", NA),
        "State": resp.get("EnabledState", NA)
    }
    return output


output = []
sensors_output = json.loads(sensors_api_output)
for mem in sensors_output.get("Members", []):
    if mem.get("ElementName", "") == "System Board CMOS Battery":
        output.append(sensors_battery_mapped_data(mem))
# print(json.dumps(output, indent=2, ensure_ascii=False))
print(output)