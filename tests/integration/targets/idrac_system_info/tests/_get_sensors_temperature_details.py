import sys
import json
import yaml

NA = "Not Available"


def map_temp_sensor_data(resp):
    """Maps the temperature sensor response into the expected output format."""
    health = resp.get("Status", {}).get("Health", NA)
    state = resp.get("Status", {}).get("State", NA)
    device_id = resp.get("Oem", {}).get("Dell", {}).get("DeviceID", NA)
    current_state = resp.get("Oem", {}).get("Dell", {}).get("CurrentState", NA)

    return {
        "CurrentReading": resp.get("Reading", NA),
        "CurrentState": current_state,
        "DeviceID": device_id,
        "HealthState": health,
        "Key": resp.get("Name", NA),
        "Location": resp.get("Name", NA),
        "OtherSensorTypeDescription": resp.get("OtherSensorTypeDescription", NA),
        "PrimaryStatus": "Healthy" if health == "OK" else health,
        "SensorType": "Temperature",
        "State": state,
        "Type": resp.get("Type", NA),
    }


def main():
    thermal_json = json.loads(sys.argv[1])
    sensors_map_json = json.loads(sys.argv[2])

    temp_info_list = []

    # Extract temperature sensor names from thermal endpoint
    temp_names = [
        member.get("Name", "").replace(" ", "")
        for member in thermal_json.get("Temperatures", [])
        if member.get("Name")
    ]

    # For each temperature sensor, get its details from the provided map
    for temp_name in temp_names:
        temp_resp = sensors_map_json.get(temp_name)
        if temp_resp:
            temp_info_list.append(map_temp_sensor_data(temp_resp))

    print(yaml.safe_dump(temp_info_list, default_flow_style=False))


if __name__ == "__main__":
    main()
