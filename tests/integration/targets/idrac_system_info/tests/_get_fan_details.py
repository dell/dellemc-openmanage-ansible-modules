import json
import sys

NA = "Not Available"
fan_api_output = sys.argv[1]


def map_fan_data(fan):
    current_reading = fan.get("SpeedPercent", {}).get("SpeedRPM", NA)
    fan_pwm = fan.get("Oem", {}).get("Dell", {}).get("FanPWM", 0)
    health = fan.get("Status", {}).get("Health", NA)
    output = {
        "VariableSpeed": "true" if fan_pwm > 0 else "false",
        "CurrentReading": current_reading,
        "DeviceDescription": fan.get("Name", NA),
        "Key": fan.get("Id", NA),
        "PWM": fan_pwm,
        "PrimaryStatus": "Healthy" if health == "OK" else health,
        "State": fan.get("State", NA),
        "ActiveCooling": fan.get("HotPluggable", NA),
        "FQDD": fan.get("Id", NA),
        "Location": fan.get("Location", NA)
    }
    return output


fan_output = json.loads(fan_api_output)
output = [map_fan_data(fan) for fan in fan_output.get("Members", [])]
print(output)
