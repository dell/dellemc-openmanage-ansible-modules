import sys
import json
import yaml

NA = "Not Available"


def map_fan_sensor_data(resp):
    """Maps the fan sensor response into the expected output format."""
    health = resp.get("Status", {}).get("Health", NA)
    state = resp.get("Status", {}).get("State", NA)
    device_id = resp.get("Oem", {}).get("Dell", {}).get("DeviceID", NA)
    current_state = resp.get("Oem", {}).get("Dell", {}).get("CurrentState", NA)

    return {
        "CurrentReading": resp.get("Reading", NA),
        "CurrentState": current_state,
        "DeviceID": device_id,
        "Location": resp.get("Name", NA),
        "HealthState": health,
        "FQDD": resp.get("FQDD", NA),
        "Name": resp.get("FanName", NA),
        "OtherSensorTypeDescription": resp.get("OtherSensorTypeDescription", NA),
        "PrimaryStatus": "Healthy" if health == "OK" else health,
        "Key": resp.get("Name", NA),
        "SensorType": "Fan",
        "Type": resp.get("Type", NA),
        "State": state,
        "SubType": resp.get("SubType", NA),
        "coolingUnitIndexReference": resp.get("coolingUnitIndexReference", NA),
    }


def main():

    thermal_json = json.loads(sys.argv[1])
    sensors_map_json = json.loads(sys.argv[2])

    fan_info_list = []

    # Extract fan names from thermal endpoint
    fan_names = [
        member.get("FanName")
        for member in thermal_json.get("Fans", [])
        if member.get("FanName")
    ]

    # For each fan, get its details from the provided map
    for fan_name in fan_names:
        fan_resp = sensors_map_json.get(fan_name)
        if fan_resp:
            fan_info_list.append(map_fan_sensor_data(fan_resp))

    print(yaml.safe_dump(fan_info_list, default_flow_style=False))


if __name__ == "__main__":
    main()
