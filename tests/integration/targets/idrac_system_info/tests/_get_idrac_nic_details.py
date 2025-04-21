import sys
import json

manager_details = sys.argv[1]
nic_details = sys.argv[2]
NOT_AVAILABLE = "Not Available"


def get_idrac_nic_info_api(manager_details, nic_details):
    output = {}
    resp = json.loads(manager_details)
    output["Key"] = resp.get("Id", NOT_AVAILABLE)
    output["FQDD"] = resp.get("Id", NOT_AVAILABLE)
    if resp.get("Status", {}).get("Health") == "OK":
        output["PrimaryStatus"] = "Healthy"
    else:
        output["PrimaryStatus"] = resp.\
            get("Status", {}).get("Health", NOT_AVAILABLE)
    idrac_attributes_response = json.loads(nic_details)
    output["IPv6Address"] = idrac_attributes_response.\
        get("Attributes", {}).get("IPv6.1.Address1", NOT_AVAILABLE)
    output["NICSpeed"] = idrac_attributes_response.\
        get("Attributes", {}).get("NIC.1.Speed", NOT_AVAILABLE)
    output["IPv4Address"] = idrac_attributes_response.\
        get("Attributes", {}).get("IPv4.1.Address", NOT_AVAILABLE)
    output["PermanentMACAddress"] = idrac_attributes_response.\
        get("Attributes", {}).get("NIC.1.MACAddress", NOT_AVAILABLE)
    output["GroupName"] = NOT_AVAILABLE
    output["GroupStatus"] = NOT_AVAILABLE
    output["NICDuplex"] = idrac_attributes_response.\
        get("Attributes", {}).get("NIC.1.Duplex", NOT_AVAILABLE)
    output["NICEnabled"] = idrac_attributes_response.\
        get("Attributes", {}).get("NIC.1.Enable", NOT_AVAILABLE)
    output["SwitchConnection"] = idrac_attributes_response.\
        get("Attributes", {}).get("NIC.1.SwitchConnection", NOT_AVAILABLE)
    output["ProductInfo"] = idrac_attributes_response.\
        get("Attributes", {}).get("Info.1.Product")
    output["SwitchPortConnection"] = \
        idrac_attributes_response.\
        get("Attributes", {}).\
        get("NIC.1.SwitchPortConnection", NOT_AVAILABLE)
    return [output]


print(get_idrac_nic_info_api(manager_details, nic_details))
