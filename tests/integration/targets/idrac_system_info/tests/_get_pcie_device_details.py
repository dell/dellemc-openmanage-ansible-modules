import sys
import json
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI

idrac_ip = sys.argv[1]
idrac_user = sys.argv[2]
idrac_password = sys.argv[3]
idrac_port = sys.argv[4]

GET_IDRAC_PCI_DETAILS_API = "/redfish/v1/Chassis/System.Embedded.1/PCIeDevices/"
NA = "Not Available"
SLOT_TYPE_MAPPING = {
    "Other": "0001",
    "Unknown": "0002",
    "ISA": "0003",
    "MCA": "0004",
    "EISA": "0005",
    "PCI": "0006",
    "VL-VESA": "0008",
    "Proprietary": "0009",
    "Processor Card Slot": "000A",
    "Proprietary Memory Card Slot": "000B",
    "I/O Riser Card Slot": "000C",
    "NuBus": "000D",
    "PC Card (PCMCIA)": "0007",
    "PCI - 66MHz Capable": "000E",
    "AGP": "000F",
    "AGP 2X": "0010",
    "AGP 4X": "0011",
    "PCI-X": "0012",
    "AGP 8X": "0013",
    "PC-98/C20": "00A0",
    "PC-98/C24": "00A1",
    "PC-98/E": "00A2",
    "PC-98/Local Bus": "00A3",
    "PC-98/Card": "00A4",
    "PCI Express x1": "00A6",
    "PCI Express x2": "00A7",
    "PCI Express x4": "00A8",
    "PCI Express x8": "00A9",
    "PCI Express x16": "00AA",
    "PCI Express": "00A5",
    "PCI Express Gen 2": "00AB",
    "PCI Express Gen 2 x1": "00AC",
    "PCI Express Gen 2 x2": "00AD",
    "PCI Express Gen 2 x4": "00AE",
    "PCI Express Gen 2 x8": "00AF",
    "PCI Express Gen 2 x16": "00B0",
    "PCI Express Gen 3 x1": "00B2",
    "PCI Express Gen 3 x2": "00B3",
    "PCI Express Gen 3 x4": "00B4",
    "PCI Express Gen 3 x8": "00B5",
    "PCI Express Gen 3 x16": "00B6",
    "PCI Express Gen 3": "00B1",
}
SLOT_LENGTH_MAPPING = {
    "Other": "0001",
    "Unknown": "0002",
    "Short Length": "0003",
    "Long Length": "0004"
}
BUS_WIDTH_MAPPING = {
    "Unknown": "0002",
    "8Bit": "0003",
    "16Bit": "0004",
    "Other": "0001",
    "32Bit": "0005",
    "64Bit": "0006",
    "1XOrX1": "0008",
    "2XOrX2": "0009",
    "4XOrX4": "000A",
    "128Bit": "0007",
    "8XOrX8": "000B",
    "12XOrX12": "000C",
    "16XOrX16": "000D",
    "32XOrX32": "000E"
}

params = {
    "idrac_ip": idrac_ip,
    "idrac_user": idrac_user,
    "idrac_password": idrac_password,
    "idrac_port": idrac_port
}
idrac_obj = iDRACRedfishAPI(params)


def get_device_links_api():
    resp = idrac_obj.invoke_request(method='GET', uri=GET_IDRAC_PCI_DETAILS_API)
    device_links_list = []
    if resp.status_code == 200:
        members = resp.json_data.get("Members")
        for each in members:
            device_links_list.append(each.get("@odata.id"))
    return device_links_list


def get_device_function_details_api(function_link_uri):
    function_link_details = idrac_obj.invoke_request(method='GET', uri=function_link_uri)
    pcie_function = function_link_details.json_data.get("Oem", {}).\
        get("Dell", {}).get("DellPCIeFunction", {})
    buswidth = BUS_WIDTH_MAPPING.get(pcie_function.get("DataBusWidth"), NA)
    buswidth_api = pcie_function.get("DataBusWidth", NA)
    deviceid = pcie_function.get("Id", NA)
    slot_type = SLOT_TYPE_MAPPING.get(pcie_function.get("SlotType"), NA)
    slot_type_api = pcie_function.get("SlotType", NA)
    slot_length = SLOT_LENGTH_MAPPING.get(pcie_function.get("SlotLength"), NA)
    slot_length_api = pcie_function.get("SlotLength", NA)
    return buswidth, buswidth_api, deviceid, slot_type, slot_type_api, slot_length, slot_length_api


def get_device_details_api(device_link):
    response = idrac_obj.invoke_request(method='GET', uri=device_link)
    output = []
    if response.status_code == 200:
        pci_functions = response.json_data.get("Links", {}).\
            get("PCIeFunctions", [{}])
        for link in pci_functions:
            tmp = {}
            device_link = link.get("@odata.id")
            if device_link is not None:
                buswidth, buswidth_api, deviceid, slot_type, \
                    slot_type_api, slot_length, slot_length_api = \
                    get_device_function_details_api(device_link)
                tmp["Description"] = response.json_data.get("Description")
                tmp["DataBusWidth"] = buswidth
                tmp["DataBusWidth_API"] = buswidth_api
                tmp["DeviceDescription"] = response.json_data.get("Description")
                tmp["FQDD"] = deviceid
                tmp["Key"] = deviceid
                tmp["SlotLength"] = slot_length
                tmp["SlotLength_API"] = slot_length_api
                tmp["Manufacturer"] = response.json_data.get("Manufacturer")
                tmp["SlotType"] = slot_type
                tmp["SlotType_API"] = slot_type_api
            output.append(tmp)
    return output


def get_pcidevice_info_api():
    pcidevice_output = []
    device_links_list = get_device_links_api()
    for each_link in device_links_list:
        pcidevice_output += get_device_details_api(each_link)
    return pcidevice_output


print(json.dumps(get_pcidevice_info_api()))
