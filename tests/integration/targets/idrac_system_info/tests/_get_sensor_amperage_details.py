import json
import sys

NA = "Not Available"
sensor_amperage_api_output = sys.argv[1]

def map_sensor_amperage_data(sensor):
    health_state_map = {
        "CriticalFailure": "Critical",
        "Degraded/Warning": "Warning",
        "MajorFailure": "Critical",
        "MinorFailure": "Critical",
        "NonRecoverableError": "Critical",
        "OK": "Healthy",
        "Unknown": "Unknown"
    }
    
    health_state = sensor.get("Status", {}).get("Health", NA)
    primary_status = health_state_map.get(health_state, NA)
    output = {
        "CurrentReading": sensor.get("Reading", NA),
        "CurrentState": sensor.get("Oem", {}).get("Dell", {}).get("CurrentState", NA),
        "DeviceID": sensor.get("Oem", {}).get("Dell", {}).get("DeviceID", NA),
        "HealthState": sensor.get("Oem", {}).get("Dell", {}).get("CurrentState", NA),
        "Key": sensor.get("Name", NA),
        "Location": sensor.get("Name", NA),
        "OtherSensorTypeDescription": NA,
        "PrimaryStatus": primary_status,
        "ProbeType": NA,
        "SensorType": "Amperage",
        "State": sensor.get("Status", {}).get("State", NA),
    }
    return output

sensor_amperage_output = json.loads(sensor_amperage_api_output)
output = [map_sensor_amperage_data(sensor_amperage) for sensor_amperage in sensor_amperage_output.get("Members", [])]
