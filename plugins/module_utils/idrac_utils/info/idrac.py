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
#

GET_IDRAC_DELL_SYSTEM_DETAILS_URI_10 = "/redfish/v1/Systems/System.Embedded.1/Oem/Dell/DellSystem/System.Embedded.1"
GET_IDRAC_SYSTEM_DETAILS_URI_10 = "/redfish/v1/Systems/System.Embedded.1/"
GET_IDRAC_MANAGER_DETAILS_URI_10 = "/redfish/v1/Managers/iDRAC.Embedded.1"
GET_IDRAC_MANAGER_ATTRIBUTES = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/iDRAC.Embedded.1"
NOT_AVAILABLE = "Not Available"
MACADDRESS_KEY = "NIC.1.MACAddress"
iDRAC = {
    "DNSDomainName": "",
    "DNSRacName": "",
    "DeviceDescription": "iDRAC",
    "FQDD": "",
    "FirmwareVersion": "",
    "GUID": "",
    "GroupName": NOT_AVAILABLE,
    "GroupStatus": NOT_AVAILABLE,
    "IPMIVersion": "",
    "IPv4Address": "",
    "IPv6Address": "",
    "Key": "",
    "LANEnabledState": "",
    "MACAddress": "",
    "Model": "",
    "NICDuplex": "",
    "NICSpeed": "",
    "PermanentMACAddress": "",
    "ProductDescription": "",
    "ProductInfo": "",
    "SOLEnabledState": "",
    "SystemLockDown": "",
    "URLString": ""
}


class IDRACInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def get_idrac_details(self):
        idrac_dell_system_response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_DELL_SYSTEM_DETAILS_URI_10)
        if idrac_dell_system_response.status_code == 200:
            idrac_system_data = idrac_dell_system_response.json_data
            iDRAC["GUID"] = idrac_system_data["smbiosGUID"]
        idrac_system_response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_SYSTEM_DETAILS_URI_10)
        if idrac_system_response.status_code == 200:
            idrac_system_data = idrac_system_response.json_data
            iDRAC["Model"] = idrac_system_data["Model"]

    def get_idrac_manager_details(self):
        idrac_manager_response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_MANAGER_DETAILS_URI_10)
        if idrac_manager_response.status_code == 200:
            idrac_manager_data = idrac_manager_response.json_data
            iDRAC["FirmwareVersion"] = idrac_manager_data["FirmwareVersion"]
            iDRAC["URLString"] = idrac_manager_data["Oem"]["Dell"]["DelliDRACCard"].get("URLString")
            iDRAC["Key"] = idrac_manager_data["Id"]
            iDRAC["FQDD"] = idrac_manager_data["Id"]

    def get_idrac_attributes_details(self):
        idrac_attributes_response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_MANAGER_ATTRIBUTES)
        if idrac_attributes_response.status_code == 200:
            idrac_attributes_data = idrac_attributes_response.json_data
            iDRAC["SystemLockDown"] = idrac_attributes_data["Attributes"].get("Lockdown.1.SystemLockdown")
            iDRAC["ProductInfo"] = idrac_attributes_data["Attributes"].get("Info.1.Product")
            iDRAC["ProductDescription"] = idrac_attributes_data["Attributes"].get("Info.1.Description")
            iDRAC["NICSpeed"] = idrac_attributes_data["Attributes"].get("NIC.1.Speed")
            iDRAC["NICDuplex"] = idrac_attributes_data["Attributes"].get("NIC.1.Duplex")
            domain_name = idrac_attributes_data["Attributes"].get("NIC.1.DNSDomainName")
            iDRAC["DNSDomainName"] = "Not Available" if domain_name == "" else domain_name
            iDRAC["DNSRacName"] = idrac_attributes_data["Attributes"].get("Network.1.DNSRacName")
            iDRAC["MACAddress"] = idrac_attributes_data["Attributes"].get(MACADDRESS_KEY)
            iDRAC["PermanentMACAddress"] = idrac_attributes_data["Attributes"].get(MACADDRESS_KEY)
            iDRAC["IPv4Address"] = idrac_attributes_data["Attributes"].get("IPv4.1.Address")
            iDRAC["IPv6Address"] = idrac_attributes_data["Attributes"].get("IPv6.1.Address1")
            sol_enabled = idrac_attributes_data["Attributes"].get("Users.1.SolEnable")
            iDRAC["SOLEnabledState"] = 1 if sol_enabled == "Enabled" else 0
            lan_enabled = idrac_attributes_data["Attributes"].get("IPMILan.1.Enable")
            iDRAC["LANEnabledState"] = 1 if lan_enabled == "Enabled" else 0
            iDRAC["IPMIVersion"] = idrac_attributes_data["Attributes"].get("Info.1.IPMIVersion")

    def get_idrac_info_details(self):
        self.get_idrac_details()
        self.get_idrac_manager_details()
        self.get_idrac_attributes_details()
        return iDRAC

    def get_idrac_nic_info(self):
        output = {}
        managerresponse = \
            self.idrac.invoke_request(
                method='GET',
                uri=GET_IDRAC_MANAGER_DETAILS_URI_10
            )
        if managerresponse.status_code == 200:
            resp = managerresponse.json_data
            output["Key"] = resp.get("Id", NOT_AVAILABLE)
            output["FQDD"] = resp.get("Id", NOT_AVAILABLE)
            if resp.get("Status", {}).get("Health") == "OK":
                output["PrimaryStatus"] = "Healthy"
            else:
                output["PrimaryStatus"] = resp.\
                    get("Status", {}).get("Health", NOT_AVAILABLE)
        idrac_attributes_response = \
            self.idrac.invoke_request(
                method='GET',
                uri=GET_IDRAC_MANAGER_ATTRIBUTES)
        if idrac_attributes_response.status_code == 200:
            output["IPv4Address"] = idrac_attributes_response.json_data.\
                get("Attributes", {}).get("IPv4.1.Address", NOT_AVAILABLE)
            output["IPv6Address"] = idrac_attributes_response.json_data.\
                get("Attributes", {}).get("IPv6.1.Address1", NOT_AVAILABLE)
            output["NICSpeed"] = idrac_attributes_response.json_data.\
                get("Attributes", {}).get("NIC.1.Speed", NOT_AVAILABLE)
            output["NICDuplex"] = idrac_attributes_response.json_data.\
                get("Attributes", {}).get("NIC.1.Duplex", NOT_AVAILABLE)
            output["PermanentMACAddress"] = idrac_attributes_response.json_data.\
                get("Attributes", {}).get(MACADDRESS_KEY)
            output["ProductInfo"] = idrac_attributes_response.json_data.\
                get("Attributes", {}).get("Info.1.Product")
            output["GroupName"] = NOT_AVAILABLE
            output["GroupStatus"] = NOT_AVAILABLE
            output["NICEnabled"] = idrac_attributes_response.json_data.\
                get("Attributes", {}).get("NIC.1.Enable", NOT_AVAILABLE)
            output["SwitchConnection"] = idrac_attributes_response.json_data.\
                get("Attributes", {}).get("NIC.1.SwitchConnection", NOT_AVAILABLE)
            output["SwitchPortConnection"] = \
                idrac_attributes_response.json_data.\
                get("Attributes", {}).\
                get("NIC.1.SwitchPortConnection", NOT_AVAILABLE)
        return output
