import sys
import json
import ast

system_details_output = sys.argv[1]
idrac_system_output = sys.argv[2]
manager_output = sys.argv[3]
manager_idrac_output = sys.argv[4]


NA = "Not Available"


def map_idrac_details(system_details_output, idrac_system_output, iDRAC):
    system_data = ast.literal_eval(system_details_output)
    system_data = json.loads(system_data)
    iDRAC["GUID"] = system_data["smbiosGUID"]
    idrac_system_data = ast.literal_eval(idrac_system_output)
    idrac_system_data = json.loads(idrac_system_data)
    iDRAC["Model"] = idrac_system_data["Model"]


def map_idrac_manager_details(manager_output, iDRAC):
    manager_data = ast.literal_eval(manager_output)
    manager_data = json.loads(manager_data)
    iDRAC["FirmwareVersion"] = manager_data["FirmwareVersion"]
    iDRAC["URLString"] = manager_data["Oem"]["Dell"]["DelliDRACCard"].get("URLString")
    iDRAC["Key"] = manager_data["Id"]
    iDRAC["FQDD"] = manager_data["Id"]


def map_idrac_attributes_data(manager_idrac_output, iDRAC):
    manager_idrac_data = ast.literal_eval(manager_idrac_output)
    manager_idrac_data = json.loads(manager_idrac_data)
    iDRAC["SystemLockDown"] = manager_idrac_data["Attributes"].get("Lockdown.1.SystemLockdown")
    iDRAC["ProductInfo"] = manager_idrac_data["Attributes"].get("Info.1.Product")
    iDRAC["ProductDescription"] = manager_idrac_data["Attributes"].get("Info.1.Description")
    iDRAC["NICSpeed"] = manager_idrac_data["Attributes"].get("NIC.1.Speed")
    iDRAC["NICDuplex"] = manager_idrac_data["Attributes"].get("NIC.1.Duplex")
    domain_name = manager_idrac_data["Attributes"].get("NIC.1.DNSDomainName")
    iDRAC["DNSDomainName"] = "Not Available" if domain_name == "" else domain_name
    iDRAC["DNSRacName"] = manager_idrac_data["Attributes"].get("Network.1.DNSRacName")
    iDRAC["MACAddress"] = manager_idrac_data["Attributes"].get("NIC.1.MACAddress")
    iDRAC["PermanentMACAddress"] = manager_idrac_data["Attributes"].get("NIC.1.MACAddress")
    iDRAC["IPv4Address"] = manager_idrac_data["Attributes"].get("IPv4.1.Address")
    iDRAC["IPv6Address"] = manager_idrac_data["Attributes"].get("IPv6.1.Address1")
    sol_enabled = manager_idrac_data["Attributes"].get("Users.1.SolEnable")
    iDRAC["SOLEnabledState"] = 1 if sol_enabled == "Enabled" else 0
    lan_enabled = manager_idrac_data["Attributes"].get("IPMILan.1.Enable")
    iDRAC["LANEnabledState"] = 1 if lan_enabled == "Enabled" else 0
    iDRAC["IPMIVersion"] = manager_idrac_data["Attributes"].get("Info.1.IPMIVersion")


def get_idrac_info(iDRAC):
    map_idrac_attributes_data(manager_idrac_output, iDRAC)
    map_idrac_manager_details(manager_output, iDRAC)
    map_idrac_details(system_details_output, idrac_system_output, iDRAC)
    return iDRAC


iDRAC = {
    "DNSDomainName": "",
    "DNSRacName": "",
    "DeviceDescription": "iDRAC",
    "FQDD": "",
    "FirmwareVersion": "",
    "GUID": "",
    "GroupName": NA,
    "GroupStatus": NA,
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
iDRAC = get_idrac_info(iDRAC)
print(json.dumps([iDRAC], ensure_ascii=False))
