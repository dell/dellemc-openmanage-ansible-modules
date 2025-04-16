import sys
import json
import ast

fan_api_output = sys.argv[1]
NA = "Not Available"


def map_fan_data(fan):
    health = fan.get("Status", {}).get("Health", NA)
    fan_pwm = fan.get("Oem", {}).get("Dell", {}).get("FanPWM", 0)
    current_reading = fan.get("SpeedPercent", {}).get("SpeedRPM", NA)
    output = {
        "ActiveCooling": fan.get("HotPluggable", NA),
        "CurrentReading": current_reading,
        "DeviceDescription": fan.get("Name", NA),
        "FQDD": fan.get("Id", NA),
        "Key": fan.get("Id", NA),
        "Location": fan.get("Location", NA),
        "PWM": fan_pwm,
        "PrimaryStatus": "Healthy" if health == "OK" else health,
        "State": fan.get("State", NA),
        "VariableSpeed": "true" if fan_pwm > 0 else "false"
    }
    return output


output = []
# fan_output = ast.literal_eval(fan_api_output)
fan_output = json.loads(fan_api_output)
fan_members = fan_output.get("Members", [])
for fan in fan_members:
    output.append(map_fan_data(fan))
print(json.dumps(output, indent=2, ensure_ascii=False))
