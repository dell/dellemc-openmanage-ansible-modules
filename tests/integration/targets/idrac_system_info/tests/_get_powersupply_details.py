import sys
import json

GET_IDRAC_POWERSUPPLY_LIST = sys.argv[1]
NA = "Not Available"

RED_TYPE_MAPPING = {
    "N+1": "2",
    "Sparing": "4",
    "Input Power Redundancy": "32768"
}


def get_red_type_set_api(dellpowersupplyview, output):
    red_type_list = dellpowersupplyview.get("RedTypeOfSet")
    if red_type_list:
        mapped_red_type_list = \
            [RED_TYPE_MAPPING.get(x) for x in red_type_list]
        output["RedTypeOfSet"] = ",".join(mapped_red_type_list)
    else:
        output["RedTypeOfSet"] = NA


def get_power_supply_details_api(member):
    output = {}
    dellpowersupplyview = member.get("Oem", {}).get("Dell", {}).\
        get("DellPowerSupplyView", {})
    output["DetailedState"] = dellpowersupplyview.get("DetailedState", NA)
    output["DeviceDescription"] = dellpowersupplyview.\
        get("DeviceDescription", NA)
    output["FQDD"] = member.get("Id", NA)
    output["Key"] = member.get("Id", NA)
    output["Name"] = member.get("Name", NA)
    output["FirmwareVersion"] = member.get("FirmwareVersion", NA)
    output["Model"] = member.get("Model", NA)
    output["InputVoltage"] = NA
    output["Manufacturer"] = member.get("Manufacturer", NA)
    output["PartNumber"] = member.get("PartNumber", NA)
    output["PowerSupplySensorState"] = NA
    if member.get("Status", {}).get("Health") == "OK":
        output["PrimaryStatus"] = "Healthy"
    else:
        output["PrimaryStatus"] = member.\
            get("Status", {}).get("Health", NA)
    output["RAIDState"] = NA
    maxinputwatt = dellpowersupplyview.get("Range1MaxInputPowerWatts")
    if maxinputwatt:
        output["Range1MaxInputPower"] = str(maxinputwatt) + " W"
    else:
        output["Range1MaxInputPower"] = NA
    output["RedMinNumberNeeded"] = dellpowersupplyview.get("RedMinNumberNeeded", NA)
    output["SerialNumber"] = member.get("SerialNumber", NA)
    if member.get("PowerCapacityWatts"):
        output["TotalOutputPower"] = str(member.get("PowerCapacityWatts")) + " W"
    else:
        output["TotalOutputPower"] = NA
    output["Type"] = member.get("PowerSupplyType", NA)
    output["powerSupplyStateCapabilitiesUnique"] = dellpowersupplyview.\
        get("powerSupplyStateCapabilitiesUnique", NA)
    output["Redundancy"] = dellpowersupplyview.\
        get("RedundancyStatus", NA)
    get_red_type_set_api(dellpowersupplyview, output)
    return output


def get_power_supply_info_api():
    power_supply_output = []
    for each_member in json.loads(GET_IDRAC_POWERSUPPLY_LIST).get('Members'):
        power_supply_output.append(get_power_supply_details_api(each_member))
    return power_supply_output


print(get_power_supply_info_api())
