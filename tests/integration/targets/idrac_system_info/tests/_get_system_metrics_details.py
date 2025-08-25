import sys
import json

# Multiple API responses are passed as arguments
systemboard_powerconsumption_api_output = sys.argv[1]
systemboard_inlettemp_api_output = sys.argv[2]
powerheadroom_api_output = sys.argv[3]

NA = "Not Available"


def get_system_metrics_info_api(power_data, temp_data, headroom_data):
    # Parse JSON
    power_data = json.loads(power_data)
    temp_data = json.loads(temp_data)
    headroom_data = json.loads(headroom_data)

    # Extract values
    energy_consump = power_data.get("LifetimeReading", NA)

    oem_dell = temp_data.get("Oem", {}).get("Dell", {})
    inlettemp_critical = oem_dell.get("DurationInCriticalThresholdPercent", NA)
    inlettemp_warn = oem_dell.get("DurationInWarningThresholdPercent", NA)

    power_consumption = headroom_data.get("LowestReading", NA)

    return [{
        "EnergyConsumption": energy_consump,
        "InletTempCriticalPerc": inlettemp_critical,
        "InletTempWarnPerc": inlettemp_warn,
        "Key": "SystemMetrics",
        "PowerConsumption": power_consumption,
        "SystemMetrics": NA
    }]


def main():
    try:
        result = get_system_metrics_info_api(
            systemboard_powerconsumption_api_output,
            systemboard_inlettemp_api_output,
            powerheadroom_api_output
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps([{"Error": str(e)}]))


if __name__ == "__main__":
    main()
