import sys
import json
import ast

system_details_output = sys.argv[1]
idrac_system_output = sys.argv[2]
manager_output = sys.argv[3]
manager_idrac_output = sys.argv[4]


NA = "Not Available"


def map_idrac_details(system_details_output, idrac_system_output, idrac_data):
    system_data = ast.literal_eval(system_details_output)
    system_data = json.loads(system_data)
    idrac_data["GUID"] = system_data["smbiosGUID"]
    idrac_system_data = ast.literal_eval(idrac_system_output)
    idrac_system_data = json.loads(idrac_system_data)
    idrac_data["Model"] = idrac_system_data["Model"]


def map_idrac_manager_details(manager_output, idrac_data):
    manager_data = ast.literal_eval(manager_output)
    manager_data = json.loads(manager_data)
    idrac_data["FirmwareVersion"] = manager_data["FirmwareVersion"]
    idrac_data["URLString"] = manager_data["Oem"]["Dell"]["DelliDRACCard"].get("URLString")
    idrac_data["Key"] = manager_data["Id"]
    idrac_data["FQDD"] = manager_data["Id"]


def map_idrac_attributes_data(manager_idrac_output, idrac_data):
    manager_idrac_data = ast.literal_eval(manager_idrac_output)
    manager_idrac_data = json.loads(manager_idrac_data)
    idrac_data["SystemLockDown"] = manager_idrac_data["Attributes"].get("Lockdown.1.SystemLockdown")
    idrac_data["ProductInfo"] = manager_idrac_data["Attributes"].get("Info.1.Product")
    idrac_data["ProductDescription"] = manager_idrac_data["Attributes"].get("Info.1.Description")
    idrac_data["NICSpeed"] = manager_idrac_data["Attributes"].get("NIC.1.Speed")
    idrac_data["NICDuplex"] = manager_idrac_data["Attributes"].get("NIC.1.Duplex")
    domain_name = manager_idrac_data["Attributes"].get("NIC.1.DNSDomainName")
    idrac_data["DNSDomainName"] = "Not Available" if domain_name == "" else domain_name
    idrac_data["DNSRacName"] = manager_idrac_data["Attributes"].get("Network.1.DNSRacName")
    idrac_data["MACAddress"] = manager_idrac_data["Attributes"].get("NIC.1.MACAddress")
    idrac_data["PermanentMACAddress"] = manager_idrac_data["Attributes"].get("NIC.1.MACAddress")
    idrac_data["IPv4Address"] = manager_idrac_data["Attributes"].get("IPv4.1.Address")
    idrac_data["IPv6Address"] = manager_idrac_data["Attributes"].get("IPv6.1.Address1")
    sol_enabled = manager_idrac_data["Attributes"].get("Users.1.SolEnable")
    idrac_data["SOLEnabledState"] = 1 if sol_enabled == "Enabled" else 0
    lan_enabled = manager_idrac_data["Attributes"].get("IPMILan.1.Enable")
    idrac_data["LANEnabledState"] = 1 if lan_enabled == "Enabled" else 0
    idrac_data["IPMIVersion"] = manager_idrac_data["Attributes"].get("Info.1.IPMIVersion")


def get_idrac_info(idrac_data):
    map_idrac_attributes_data(manager_idrac_output, idrac_data)
    map_idrac_manager_details(manager_output, idrac_data)
    map_idrac_details(system_details_output, idrac_system_output, idrac_data)
    return idrac_data


idrac_data = {
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
idrac_data = get_idrac_info(idrac_data)
print(json.dumps([idrac_data], ensure_ascii=False))
