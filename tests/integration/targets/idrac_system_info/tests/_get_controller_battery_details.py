import json
import sys

NA = "Not Available"
controller_battery_api_output = sys.argv[1]


def map_controller_battery_data(battery):
    health_state_map = {
        "CriticalFailure": "Critical",
        "Degraded/Warning": "Warning",
        "MajorFailure": "Critical",
        "MinorFailure": "Critical",
        "NonRecoverableError": "Critical",
        "OK": "Healthy",
        "Unknown": "Unknown"
    }
    
    health_state = battery.get("PrimaryStatus", NA)
    primary_status = health_state_map.get(health_state, NA)
    output = {
        "DeviceDescription": battery.get("Name", NA),
        "FQDD": battery.get("FQDD", NA),
        "InstanceID": battery.get("Id", NA),
        "Key": battery.get("Id", NA),
        "PrimaryStatus": primary_status,
        "RAIDState": battery.get("RAIDState", NA),
    }
    return output

controller_battery_output = json.loads(controller_battery_api_output)
output = [map_controller_battery_data(controller_battery) for controller_battery in controller_battery_output.get("Members", [])]
