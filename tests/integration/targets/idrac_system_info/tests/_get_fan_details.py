import sys
import json
import ast

fan_api_output = sys.argv[1]
NA = "Not Available"

def map_fan_data(fan):
    health = fan.get("Status", {}).get("Health", NA)
    fan_pwm = fan.get("Oem", {}).get("Dell", {}).get("FanPWM", 0)
    keys_to_search = {
        "ActiveCooling": "HotPluggable",
        "CurrentReading": "SpeedPercent.SpeedRPM",
        "DeviceDescription": "Name",
        "FQDD": "Id",
        "Key": "Id",
        "Location": "Location",
        "PWM": "Oem.Dell.FanPWM",
        "PrimaryStatus": "Status.Health",
        "State": "State",
        "VariableSpeed": "true" if fan_pwm > 0 else "false"
    }

    fan_data = {}

    for key, response_key in keys_to_search.items():
        if key == "PrimaryStatus":
            fan_data[key] = "Healthy" if health == "OK" else (health or NA)
        elif key == "VariableSpeed":
            fan_pwm = fan.get("Oem", {}).get("Dell", {}).get("FanPWM", 0)
            fan_data[key] = "true" if fan_pwm > 0 else "false"
        else:
            keys = response_key.split(".")
            value = fan
            for k in keys:
                value = value.get(k, NA) if isinstance(value, dict) else NA
            fan_data[key] = value

    return fan_data

output = []
fan_output = ast.literal_eval(fan_api_output)
fan_output = json.loads(fan_output)
fan_members = fan_output.get("Members", [])
for fan in fan_members:
    output.append(map_fan_data(fan))
print(output)