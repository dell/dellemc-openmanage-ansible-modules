import sys
import json

GET_IDRAC_MEMORY_LIST = sys.argv[1]
NA = "Not Available"

MAPPING_DICT_FOR_RANK_API = {
    0: "Unknown",
    1: "Single Rank",
    2: "Double Rank",
    4: "Quad Rank"
}
MAPPING_MEMORY_TYPE_DICT_API = {
    "Other": "1",
    "Unknown": "2",
    "DRAM": "3",
    "EDRAM": "4",
    "VRAM": "5",
    "SRAM": "6",
    "RAM": "7",
    "ROM": "8",
    "Flash": "9",
    "EEPROM": "10",
    "FEPROM": "11",
    "EPROM": "12",
    "CDRAM": "13",
    "3DRAM": "14",
    "SDRAM": "15",
    "SGRAM": "16",
    "RDRAM": "17",
    "DDR": "18",
    "DDR-2": "19",
    "DDR-2-FB-DIMM": "20",
    "DDR-3": "24",
    "FBD2": "25"
}


def get_parameters_with_units_api(response, output):
    if output["CurrentOperatingSpeed"] is not None:
        output["CurrentOperatingSpeed"] = \
            str(float(response.get("OperatingSpeedMhz"))) \
            + " MHz"
    else:
        output["CurrentOperatingSpeed"] = NA
    if output["Speed"]:
        output["Speed"] = \
            str(response.get("AllowedSpeedsMHz")[0] / 1000)\
            + " GHz"
    else:
        output["Speed"] = NA
    if output["Size"] is not None:
        output["Size"] = \
            str(response.get("CapacityMiB") / 1024) + " GB"
    else:
        output["Size"] = NA
    return output


def get_memory_details_api(response):
    output = {}
    output["BankLabel"] = response.get("Oem", {})\
        .get("Dell", {}).get("DellMemory", {}).get("BankLabel", NA)
    output["CurrentOperatingSpeed"] = \
        response.get("OperatingSpeedMhz")
    output["DeviceDescription"] = \
        response.get("Description", NA)
    output["FQDD"] = response.get("Id", NA)
    output["Key"] = response.get("Id", NA)
    output["ManufactureDate"] = response.get("Oem", {})\
        .get("Dell", {}).get("DellMemory", {}).\
        get("ManufactureDate", NA)
    output["Manufacturer"] = response.\
        get("Manufacturer", NA)
    output["MemoryType"] = MAPPING_MEMORY_TYPE_DICT_API.get(
        response.get("MemoryDeviceType"), NA)
    output["MemoryType_API"] = response.get("MemoryDeviceType", NA)
    output["Model"] = response.get("Oem", {})\
        .get("Dell", {}).get("DellMemory", {}).\
        get("Model", NA)
    output["PartNumber"] = response.get("PartNumber", NA)
    output["PrimaryStatus"] = \
        response.get("Status", {}).get("Health", NA)
    output["Rank"] = \
        MAPPING_DICT_FOR_RANK_API.get(response.get("RankCount"), NA)
    output["SerialNumber"] = response.\
        get("SerialNumber", NA)
    output["Size"] = response.get("CapacityMiB")
    output["Speed"] = response.get("AllowedSpeedsMHz")
    output["memoryDeviceStateSettings"] = \
        response.get("Status", {}).get("State", NA)
    if response.get("Status", {}).get("Health") == "OK":
        output["PrimaryStatus"] = "Healthy"
    else:
        output["PrimaryStatus"] = response.\
            get("Status", {}).get("Health", NA)
    get_parameters_with_units_api(response, output)
    return output


def get_memory_info_api():
    memory_output = []
    for each_memory in json.loads(GET_IDRAC_MEMORY_LIST).get('Members'):
        memory_output.append(get_memory_details_api(each_memory))
    return memory_output


print(get_memory_info_api())
