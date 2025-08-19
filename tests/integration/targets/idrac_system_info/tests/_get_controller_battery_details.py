import json
import sys

NA = "Not Available"
controller_battery_api_output = sys.argv[1]


def map_controller_battery_data(battery):
    health_state_map = {
        "Unknown": "Unknown",
        "OK": "Healthy",
        "NonRecoverableError": "Critical",
        "MinorFailure": "Critical",
        "MajorFailure": "Critical",
        "Degraded/Warning": "Warning",
        "CriticalFailure": "Critical",
    }
    
    health_state = battery.get("PrimaryStatus", NA)
    primary_status = health_state_map.get(health_state, NA)
    output = {
        "RAIDState": battery.get("RAIDState", NA),
        "PrimaryStatus": primary_status,
        "Key": battery.get("Id", NA),
        "InstanceID": battery.get("Id", NA),
        "FQDD": battery.get("FQDD", NA),
        "DeviceDescription": battery.get("Name", NA),
    }
    return output

controller_battery_output = json.loads(controller_battery_api_output)
output = [map_controller_battery_data(controller_battery) for controller_battery in controller_battery_output.get("Members", [])]
