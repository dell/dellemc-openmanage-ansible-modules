
import sys
import json

sensors_api_output = sys.argv[1]
NA = "Not Available"


def sensors_battery_mapped_data(resp):
    health_state_map = {
        "Degraded/Warning": "Warning",
        "CriticalFailure": "Critical",
        "NonRecoverableError": "Critical",
        "MajorFailure": "Critical",
        "OK": "Healthy",
        "Unknown": "Unknown",
        "MinorFailure": "Critical"
    }
    health_state = resp.get("HealthState", NA)
    primary_status = health_state_map.get(health_state, NA)
    output = {
        "CurrentReading": resp.get("CurrentReading", NA),
        "State": resp.get("EnabledState", NA),
        "DeviceID": resp.get("Id", NA),
        "Key": resp.get("ElementName", NA),
        "SensorType": resp.get("SensorType", NA),
        "Location": resp.get("ElementName", NA),
        "OtherSensorTypeDescription": NA,
        "PrimaryStatus": primary_status,
        "HealthState": resp.get("HealthState", NA),
        "CurrentState": resp.get("CurrentState", NA)
    }
    return output


output = []
sensors_output = json.loads(sensors_api_output)
for mem in sensors_output.get("Members", []):
    if mem.get("ElementName", "") == "System Board CMOS Battery":
        output.append(sensors_battery_mapped_data(mem))
print(output)
