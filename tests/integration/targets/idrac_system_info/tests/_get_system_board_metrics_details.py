import sys
import json

# Multiple API responses are passed as arguments
cpu_usage_uri_details = sys.argv[1]
io_usage_uri_details = sys.argv[2]
mem_usage_uri_details = sys.argv[3]
sys_usage_uri_details = sys.argv[4]
power_consumption_uri_details = sys.argv[5]
current_consumption_uri_details = sys.argv[6]
power_headroom_uri_details = sys.argv[7]

NA = "Not Available"


def get_system_board_metrics_info_api(
        cpu_usage_uri_details, io_usage_uri_details, mem_usage_uri_details,
        sys_usage_uri_details, power_consumption_uri_details,
        current_consumption_uri_details, power_headroom_uri_details):
    # Parse JSON
    cpu_usage_data = json.loads(cpu_usage_uri_details)
    io_usage_data = json.loads(io_usage_uri_details)
    mem_usage_data = json.loads(mem_usage_uri_details)
    sys_usage_data = json.loads(sys_usage_uri_details)
    power_consumption_data = json.loads(power_consumption_uri_details)
    current_consumption_data = json.loads(current_consumption_uri_details)
    power_headroom_data = json.loads(power_headroom_uri_details)

    # Extract values
    cpu_usage_avg_hour = cpu_usage_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastHour", {}).get("Reading", NA)
    cpu_usage_avg_day = cpu_usage_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastDay", {}).get("Reading", NA)
    cpu_usage_avg_week = cpu_usage_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastWeek", {}).get("Reading", NA)
    cpu_usage_max_hour = cpu_usage_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastHour", {}).get("Reading", NA)
    cpu_usage_max_day = cpu_usage_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastDay", {}).get("Reading", NA)
    cpu_usage_max_week = cpu_usage_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastWeek", {}).get("Reading", NA)
    cpu_usage_min_hour = cpu_usage_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastHour", {}).get("Reading", NA)
    cpu_usage_min_day = cpu_usage_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastDay", {}).get("Reading", NA)
    cpu_usage_min_week = cpu_usage_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastWeek", {}).get("Reading", NA)
    cpu_usage_peak = cpu_usage_data.get("PeakReading", NA)

    io_usage_avg_hour = io_usage_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastHour", {}).get("Reading", NA)
    io_usage_avg_day = io_usage_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastDay", {}).get("Reading", NA)
    io_usage_avg_week = io_usage_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastWeek", {}).get("Reading", NA)
    io_usage_max_hour = io_usage_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastHour", {}).get("Reading", NA)
    io_usage_max_day = io_usage_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastDay", {}).get("Reading", NA)
    io_usage_max_week = io_usage_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastWeek", {}).get("Reading", NA)
    io_usage_min_hour = io_usage_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastHour", {}).get("Reading", NA)
    io_usage_min_day = io_usage_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastDay", {}).get("Reading", NA)
    io_usage_min_week = io_usage_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastWeek", {}).get("Reading", NA)
    io_usage_peak = io_usage_data.get("PeakReading", NA)

    mem_usage_avg_hour = mem_usage_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastHour", {}).get("Reading", NA)
    mem_usage_avg_day = mem_usage_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastDay", {}).get("Reading", NA)
    mem_usage_avg_week = mem_usage_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastWeek", {}).get("Reading", NA)
    mem_usage_max_hour = mem_usage_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastHour", {}).get("Reading", NA)
    mem_usage_max_day = mem_usage_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastDay", {}).get("Reading", NA)
    mem_usage_max_week = mem_usage_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastWeek", {}).get("Reading", NA)
    mem_usage_min_hour = mem_usage_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastHour", {}).get("Reading", NA)
    mem_usage_min_day = mem_usage_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastDay", {}).get("Reading", NA)
    mem_usage_min_week = mem_usage_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastWeek", {}).get("Reading", NA)
    mem_usage_peak = mem_usage_data.get("PeakReading", NA)

    sys_usage_avg_hour = sys_usage_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastHour", {}).get("Reading", NA)
    sys_usage_avg_day = sys_usage_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastDay", {}).get("Reading", NA)
    sys_usage_avg_week = sys_usage_data.get("Oem", {}).get("Dell", {}).get("AverageReadings", {}).get("LastWeek", {}).get("Reading", NA)
    sys_usage_max_hour = sys_usage_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastHour", {}).get("Reading", NA)
    sys_usage_max_day = sys_usage_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastDay", {}).get("Reading", NA)
    sys_usage_max_week = sys_usage_data.get("Oem", {}).get("Dell", {}).get("PeakReadings", {}).get("LastWeek", {}).get("Reading", NA)
    sys_usage_min_hour = sys_usage_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastHour", {}).get("Reading", NA)
    sys_usage_min_day = sys_usage_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastDay", {}).get("Reading", NA)
    sys_usage_min_week = sys_usage_data.get("Oem", {}).get("Dell", {}).get("LowestReadings", {}).get("LastWeek", {}).get("Reading", NA)
    sys_usage_peak = sys_usage_data.get("PeakReading", NA)

    peak_power = power_consumption_data.get("PeakReading", NA)
    peak_amperage = current_consumption_data.get("PeakReading", NA)
    peak_headroom = power_headroom_data.get("LowestReading", NA)

    return [{
        "Key": "SystemBoardMetrics",

        "PeakPower": peak_power,
        "PeakAmperage": peak_amperage,
        "PeakHeadroom": peak_headroom,

        "SYSUsageAvg1H": sys_usage_avg_hour,
        "SYSUsageAvg1D": sys_usage_avg_day,
        "SYSUsageAvg1W": sys_usage_avg_week,
        "SYSUsageMax1H": sys_usage_max_hour,
        "SYSUsageMax1D": sys_usage_max_day,
        "SYSUsageMax1W": sys_usage_max_week,
        "SYSUsageMin1H": sys_usage_min_hour,
        "SYSUsageMin1D": sys_usage_min_day,
        "SYSUsageMin1W": sys_usage_min_week,
        "SYSPeakSYSUsage": sys_usage_peak,

        "CPUUsageAvg1H": cpu_usage_avg_hour,
        "CPUUsageAvg1D": cpu_usage_avg_day,
        "CPUUsageAvg1W": cpu_usage_avg_week,
        "CPUUsageMax1H": cpu_usage_max_hour,
        "CPUUsageMax1D": cpu_usage_max_day,
        "CPUUsageMax1W": cpu_usage_max_week,
        "CPUUsageMin1H": cpu_usage_min_hour,
        "CPUUsageMin1D": cpu_usage_min_day,
        "CPUUsageMin1W": cpu_usage_min_week,
        "SYSPeakCPUUsage": cpu_usage_peak,

        "MemoryUsageAvg1H": mem_usage_avg_hour,
        "MemoryUsageAvg1D": mem_usage_avg_day,
        "MemoryUsageAvg1W": mem_usage_avg_week,
        "MemoryUsageMax1H": mem_usage_max_hour,
        "MemoryUsageMax1D": mem_usage_max_day,
        "MemoryUsageMax1W": mem_usage_max_week,
        "MemoryUsageMin1H": mem_usage_min_hour,
        "MemoryUsageMin1D": mem_usage_min_day,
        "MemoryUsageMin1W": mem_usage_min_week,
        "SYSPeakMemoryUsage": mem_usage_peak,

        "IOUsageAvg1H": io_usage_avg_hour,
        "IOUsageAvg1D": io_usage_avg_day,
        "IOUsageAvg1W": io_usage_avg_week,
        "IOUsageMax1H": io_usage_max_hour,
        "IOUsageMax1D": io_usage_max_day,
        "IOUsageMax1W": io_usage_max_week,
        "IOUsageMin1H": io_usage_min_hour,
        "IOUsageMin1D": io_usage_min_day,
        "IOUsageMin1W": io_usage_min_week,
        "SYSPeakIOUsage": io_usage_peak,
        "SystemBoardMetrics": NA
    }]


def main():
    try:
        result = get_system_board_metrics_info_api(
            cpu_usage_uri_details,
            io_usage_uri_details,
            mem_usage_uri_details,
            sys_usage_uri_details,
            power_consumption_uri_details,
            current_consumption_uri_details,
            power_headroom_uri_details
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps([{"Error": str(e)}]))


if __name__ == "__main__":
    main()
