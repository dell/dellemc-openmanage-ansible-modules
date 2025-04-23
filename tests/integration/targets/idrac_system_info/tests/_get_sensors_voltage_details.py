import sys
import json

GET_IDRAC_SENSORS_VOLTAGE_LIST = sys.argv[1]
NA = "Not Available"


def sensors_voltage_mapped_data_api(resp):
    health = resp.get("HealthState", NA)

    output = {
        "CurrentReading": resp.get("CurrentReading", NA),
        "CurrentState": resp.get("CurrentState", NA),
        "DeviceID": resp.get("Id", NA),
        "VoltageProbeType": resp.get("VoltageProbeType", NA),
        "HealthState": resp.get("HealthState", NA),
        "Key": resp.get("ElementName", NA),
        "Location": resp.get("ElementName", NA),
        "PrimaryStatus": "Healthy" if health == "OK" else health,
        "SensorType": resp.get("SensorType", NA),
        "State": resp.get("EnabledState", NA),
        "OtherSensorTypeDescription": NA,
        "VoltageProbeIndex": resp.get("VoltageProbeIndex", NA)
    }

    return output


def get_sensors_voltage_info_api():
    output = []
    for mem in json.loads(GET_IDRAC_SENSORS_VOLTAGE_LIST).get("Members", []):
        if mem.get("SensorType", "") == "Voltage":
            output.append(sensors_voltage_mapped_data_api(mem))
    return output


print(json.dumps(get_sensors_voltage_info_api()))
