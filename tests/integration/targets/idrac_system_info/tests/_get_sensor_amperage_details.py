import json
import sys

NA = "Not Available"
sensor_amperage_api_output = sys.argv[1]


def map_sensor_amperage_data(sensor):
    health_state_map = {
        "Unknown": "Unknown",
        "MinorFailure": "Critical",
        "MajorFailure": "Critical",
        "Degraded/Warning": "Warning",
        "OK": "Healthy",
        "NonRecoverableError": "Critical",
        "CriticalFailure": "Critical",
    }

    health_state = sensor.get("Status", {}).get("Health", NA)
    primary_status = health_state_map.get(health_state, NA)
    output = {
        "SensorType": "Amperage",
        "State": sensor.get("Status", {}).get("State", NA),
        "ProbeType": NA,
        "PrimaryStatus": primary_status,
        "OtherSensorTypeDescription": NA,
        "Location": sensor.get("Name", NA),
        "Key": sensor.get("Name", NA),
        "HealthState": sensor.get("Oem", {}).get("Dell", {}).get("CurrentState", NA),
        "DeviceID": sensor.get("Oem", {}).get("Dell", {}).get("DeviceID", NA),
        "CurrentState": sensor.get("Oem", {}).get("Dell", {}).get("CurrentState", NA),
        "CurrentReading": sensor.get("Reading", NA),
    }
    return output


sensor_amperage_output = json.loads(sensor_amperage_api_output)
output = [map_sensor_amperage_data(sensor_amperage) for sensor_amperage in sensor_amperage_output.get("Members", [])]
