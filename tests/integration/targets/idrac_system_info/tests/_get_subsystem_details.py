import sys
import json

cpu_api_output = sys.argv[1]
license_api_output = sys.argv[2]
memory_api_output = sys.argv[3]
power_supply_api_output = sys.argv[4]
voltage_api_output = sys.argv[5]
sensor_api_output = sys.argv[6]
fan_sensor_api_output = sys.argv[7]
intrusion_api_output = sys.argv[8]
temperature_api_output = sys.argv[9]
storage_api_output = sys.argv[10]
sensor_amperage_api_output = sys.argv[11]
system_api_output = sys.argv[12]


def map_cpu_health_status(cpu_api_output, output):
    subsystem_data = json.loads(cpu_api_output)

    members = subsystem_data.get("Members", [])
    if members:
        health_status = members[0].get("Status", {}).get("Health", "Unknown")
    else:
        health_status = "Unknown"
    output.append({
        "Key": "CPU",
        "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
    })


def map_license_health_status(license_api_output, output):
    subsystem_data = json.loads(license_api_output)
    members = subsystem_data.get("Members", [])
    if members:
        health_status = members[0].get("Status", {}).get("Health", "Unknown")
    else:
        health_status = "Unknown"
    output.append({
        "Key": "License",
        "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
    })


def map_memory_health_status(memory_api_output, output):
    subsystem_data = json.loads(memory_api_output)
    members = subsystem_data.get("Members", [])
    if members:
        health_status = members[0].get("Status", {}).get("Health", "Unknown")
    else:
        health_status = "Unknown"
    output.append({
        "Key": "Memory",
        "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
    })


def map_power_supply_health_status(power_supply_data_output, output):
    subsystem_data = json.loads(power_supply_data_output)
    members = subsystem_data.get("Members", [])
    if members:
        health_status = members[0].get("Status", {}).get("Health", "Unknown")
    else:
        health_status = "Unknown"
    output.append({
        "Key": "PowerSupply",
        "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
    })


def map_sensor_voltage_health_status(voltage_api_output, output):
    subsystem_data = json.loads(voltage_api_output)
    members = subsystem_data.get("Redundancy", [])
    if members:
        health_status = members[0].get("Status", {}).get("Health", "Unknown")
    else:
        health_status = "Unknown"
    output.append({
        "Key": "Sensors_Voltage",
        "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
    })


def map_sensor_battery_health_status(sensor_api_output, output):
    found = False
    subsystem_data = json.loads(sensor_api_output)
    for mem in subsystem_data.get("Members", []):
        if mem.get("ElementName", "") == "System Board CMOS Battery":
            health_status = mem.get("HealthState")
            output.append({
                "Key": "Sensors_Battery",
                "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
            })
            found = True
            break

    if not found:
        output.append({
            "Key": "Sensors_Battery",
            "PrimaryStatus": "Unknown"
        })


def map_sensor_fan_health_status(fan_sensor_api_output, output):
    subsystem_data = json.loads(fan_sensor_api_output)
    members = subsystem_data.get("Members", [])
    if members:
        health_status = members[0].get("Status", {}).get("Health", "Unknown")
    else:
        health_status = "Unknown"
    output.append({
        "Key": "Sensors_Fan",
        "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
    })


def map_sensor_intrusion_health_status(intrusion_api_output, output):
    subsystem_data = json.loads(intrusion_api_output)
    health_status = subsystem_data["PhysicalSecurity"].get("IntrusionSensor", "Unknown")
    output.append({
        "Key": "Sensors_Intrusion",
        "PrimaryStatus": "Healthy" if health_status == "Normal" else health_status
    })


def map_sensor_temperature_health_status(temperature_api_output, output):
    subsystem_data = json.loads(temperature_api_output)
    members = subsystem_data.get("Members", [])
    if members:
        health_status = members[0].get("Status", {}).get("Health", "Unknown")
    else:
        health_status = "Unknown"
    output.append({
        "Key": "Sensors_Temperature",
        "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
    })


def map_system_health_status(system_api_output, output):
    subsystem_data = json.loads(system_api_output)
    health_status = subsystem_data["Status"].get("Health", "Unknown")
    output.append({
        "Key": "System",
        "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
    })


def map_vflash_health_status(output):
    # Hardcoding value, since no api is available
    output.append({
        "Key": "VFlash",
        "PrimaryStatus": "Unknown"
    })


def map_sensor_amperage_health_status(sensor_amperage_api_output, output):
    subsystem_data = json.loads(sensor_amperage_api_output)
    health_status = subsystem_data["Status"].get("Health", "Unknown")
    output.append({
        "Key": "Sensors_Amperage",
        "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
    })


def map_storage_health_status(storage_api_output, output):
    subsystem_data = json.loads(storage_api_output)
    health_status = subsystem_data["Status"].get("Health", "Unknown") or "Unknown"
    output.append({
        "Key": "Storage",
        "PrimaryStatus": "Healthy" if health_status == "OK" else health_status
    })


def get_subsystem_info(output):
    map_system_health_status(system_api_output, output)
    map_memory_health_status(memory_api_output, output)
    map_cpu_health_status(cpu_api_output, output)
    map_sensor_fan_health_status(fan_sensor_api_output, output)
    map_power_supply_health_status(power_supply_api_output, output)
    map_storage_health_status(storage_api_output, output)
    map_license_health_status(license_api_output, output)
    map_sensor_voltage_health_status(voltage_api_output, output)
    map_sensor_temperature_health_status(temperature_api_output, output)
    map_sensor_battery_health_status(sensor_api_output, output)
    map_vflash_health_status(output)
    map_sensor_intrusion_health_status(intrusion_api_output, output)
    map_sensor_amperage_health_status(sensor_amperage_api_output, output)
    return output


output = []
output = get_subsystem_info(output)
print(json.dumps(output, ensure_ascii=False))
