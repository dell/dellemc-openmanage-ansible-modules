# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 9.12.0
# Copyright (C) 2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:

#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.

#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


GET_IDRAC_POWER_SUPPLY_DETAILS_URI = "/redfish/v1/Chassis/System.Embedded.1/PowerSubsystem/PowerSupplies"
NA = "Not Available"
RED_TYPE_MAPPING = {
    "N+1": "2",
    "Sparing": "4",
    "Input Power Redundancy": "32768"
}


class IDRACPowerSupplyInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def get_power_supply_links(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_POWER_SUPPLY_DETAILS_URI)
        power_supply_links_list = []
        if response.status_code == 200:
            members = response.json_data.get("Members")
            for each in members:
                power_supply_links_list.append(each.get("@odata.id"))
        return power_supply_links_list

    def get_red_type_set(self, response, output):
        red_type_list = response.get("Oem", {}).\
            get("Dell", {}).get("DellPowerSupplyView", {}).\
            get("RedTypeOfSet")
        if red_type_list:
            mapped_red_type_list = \
                [RED_TYPE_MAPPING.get(x) for x in red_type_list]
            output["RedTypeOfSet"] = ",".join(mapped_red_type_list)
        else:
            output["RedTypeOfSet"] = NA

    def get_power_supply_details(self, memory_link):
        response = self.idrac.invoke_request(method='GET', uri=memory_link)
        output = {}
        if response.status_code == 200:
            output["DetailedState"] = \
                response.json_data.get("Oem", {}).get("Dell", {}).\
                get("DellPowerSupplyView", {}).get("DetailedState", NA)
            output["DeviceDescription"] = response.json_data.get("Oem", {}).\
                get("Dell", {}).get("DellPowerSupplyView", {}).\
                get("DeviceDescription", NA)
            output["FQDD"] = response.json_data.get("Id", NA)
            output["Key"] = response.json_data.get("Id", NA)
            output["Name"] = response.json_data.get("Name", NA)
            output["FirmwareVersion"] = \
                response.json_data.get("FirmwareVersion", NA)
            output["Model"] = response.json_data.get("Model", NA)
            output["InputVoltage"] = NA
            output["Manufacturer"] = \
                response.json_data.get("Manufacturer", NA)
            output["PartNumber"] = response.json_data.get("PartNumber", NA)
            output["PowerSupplySensorState"] = NA
            if response.json_data.get("Status", {}).get("Health") == "OK":
                output["PrimaryStatus"] = "Healthy"
            else:
                output["PrimaryStatus"] = response.json_data.\
                    get("Status", {}).get("Health", NA)
            output["RAIDState"] = NA
            maxinputwatt = \
                response.json_data.get("Oem", {}).get("Dell", {}).\
                get("DellPowerSupplyView", {}).\
                get("Range1MaxInputPowerWatts")
            if maxinputwatt:
                output["Range1MaxInputPower"] = str(maxinputwatt) + " W"
            else:
                output["Range1MaxInputPower"] = NA
            output["RedMinNumberNeeded"] = \
                response.json_data.get("Oem", {}).get("Dell", {}).\
                get("DellPowerSupplyView", {}).get("RedMinNumberNeeded", NA)
            output["SerialNumber"] = \
                response.json_data.get("SerialNumber", NA)
            if response.json_data.get("PowerCapacityWatts"):
                output["TotalOutputPower"] = \
                    str(response.json_data.get("PowerCapacityWatts")) + " W"
            else:
                output["TotalOutputPower"] = NA
            output["Type"] = response.json_data.get("PowerSupplyType", NA)
            output["powerSupplyStateCapabilitiesUnique"] = \
                response.json_data.get("Oem", {}).get("Dell", {}).\
                get("DellPowerSupplyView", {}).\
                get("powerSupplyStateCapabilitiesUnique", NA)
            output["Redundancy"] = response.json_data.get("Oem", {}).\
                get("Dell", {}).get("DellPowerSupplyView", {}).\
                get("RedundancyStatus", NA)
            self.get_red_type_set(response.json_data, output)
        return output

    def get_power_supply_info(self):
        power_supply_output = []
        power_supply_links_list = self.get_power_supply_links()
        for each_link in power_supply_links_list:
            power_supply_output.append(self.get_power_supply_details(each_link))
        return power_supply_output
