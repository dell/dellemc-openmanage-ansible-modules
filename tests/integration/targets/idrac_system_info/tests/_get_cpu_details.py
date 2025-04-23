import sys
import json
import ast

cpu_api_output = sys.argv[1]
NA = "Not Available"


def map_cpu_data(cpu):
    processor = cpu.get("Oem", {}).get("Dell", {}).get("DellProcessor", {})
    ccs = str(int(processor.get("CurrentClockSpeedMhz", 0)) / 1000) + " GHz"
    mcs = str(int(cpu.get("MaxSpeedMHz", 0)) / 1000) + " GHz"
    chars = "64-bit Capable" if cpu.get("InstructionSet", "").lower() == "x86-64" else "Unknown"

    return {
        "CPUFamily": processor.get("CPUFamily", NA),
        "Characteristics": chars,
        "CurrentClockSpeed": ccs,
        "DeviceDescription": cpu.get("Name", NA),
        "ExecuteDisabledCapable": processor.get("ExecuteDisabledCapable", NA),
        "ExecuteDisabledEnabled": processor.get("ExecuteDisabledEnabled", NA),
        "FQDD": cpu.get("Id", NA),
        "HyperThreadingCapable": processor.get("HyperThreadingCapable", NA),
        "HyperThreadingEnabled": processor.get("HyperThreadingEnabled", NA),
        "Key": cpu.get("Socket", NA),
        "Manufacturer": cpu.get("Manufacturer", NA),
        "MaxClockSpeed": mcs,
        "Model": cpu.get("Model", NA),
        "NumberOfEnabledCores": str(cpu.get("TotalEnabledCores", NA)),
        "NumberOfEnabledThreads": str(cpu.get("TotalThreads", NA)),
        "NumberOfProcessorCores": str(cpu.get("TotalCores", NA)),
        "PrimaryStatus": cpu.get("Status", {}).get("Health", NA),
        "TurboModeCapable": processor.get("TurboModeCapable", NA),
        "TurboModeEnabled": processor.get("TurboModeEnabled", NA),
        "VirtualizationTechnologyCapable": processor.get("VirtualizationTechnologyCapable", NA),
        "VirtualizationTechnologyEnabled": processor.get("VirtualizationTechnologyEnabled", NA),
        "Voltage": processor.get("Volts", NA),
        "processorDeviceStateSettings": NA
    }


cpu_data = ast.literal_eval(cpu_api_output)
cpu_data = json.loads(cpu_data)

output = [map_cpu_data(cpu) for cpu in cpu_data.get("Members", [])]

print(json.dumps(output, ensure_ascii=False))
