import sys
import json

nic_api_output = sys.argv[1]
nic_capability_api_output = sys.argv[2]
nic_portmetrics_api_output = sys.argv[3]
nic_statistics_api_output = sys.argv[4]
ethernet_ethernet_data_api_output = sys.argv[5]
NA = "Not Available"


def get_capability_nic_details(id):
    nic_capability_output = json.loads(nic_capability_api_output)
    dcb_protocol, fcoe_boot_support, fcoe_offload_support, flex_add_support, \
        nic_part_support, pxe_boot_support, tcp_chimney_support, wol_support, \
        iscsi_boot_support, iscsi_offload_support = "", "", "", "", \
        "", "", "", "", "", ""
    for member in nic_capability_output.get("Members", []):
        if member.get("Id", "") == id:
            iscsi_offload_support = member.get("iSCSIOffloadSupport", "")
            dcb_protocol = member.get("DCBExchangeProtocol", "")
            wol_support = member.get("PartitionWOLSupport", "")
            fcoe_boot_support = member.get("FCoEBootSupport", "")
            pxe_boot_support = member.get("PXEBootSupport", "")
            fcoe_offload_support = member.get("FCoEOffloadSupport", "")
            flex_add_support = member.get("FlexAddressingSupport", "")
            iscsi_boot_support = member.get("iSCSIBootSupport", "")
            nic_part_support = member.get("NicPartitioningSupport", "")
            tcp_chimney_support = member.get("TCPChimneySupport", "")
    return dcb_protocol, fcoe_boot_support, fcoe_offload_support, \
        flex_add_support, nic_part_support, pxe_boot_support, \
        tcp_chimney_support, wol_support, iscsi_boot_support, \
        iscsi_offload_support


def get_nic_portmetrics_details(nic_port_id):
    nic_portmetrics_output = json.loads(nic_portmetrics_api_output)
    link_status = ""
    for member in nic_portmetrics_output.get("Members", []):
        if member.get("Id", "") == nic_port_id:
            link_status = member.get("PartitionLinkStatus", "")
    return link_status


def get_nicstatistics_details(id):
    nic_statistics_output = json.loads(nic_statistics_api_output)
    rx_bytes, rx_multicast, rx_unicast, tx_bytes, tx_multicast, \
        tx_unicast = "", "", "", "", "", ""
    for member in nic_statistics_output.get("Members", []):
        if member.get("Id", "") == id:
            rx_bytes = member.get("RxBytes", "")
            tx_unicast = member.get("TxUnicastPackets", "")
            rx_unicast = member.get("RxUnicastPackets", "")
            tx_bytes = member.get("TxBytes", "")
            tx_multicast = member.get("TxMutlicastPackets", "")
            rx_multicast = member.get("RxMutlicastPackets", "")
    return rx_bytes, rx_multicast, rx_unicast, tx_bytes, \
        tx_multicast, tx_unicast


def get_nic_ethernet_details():
    ethernet_ethernet_data_output = json.loads(ethernet_ethernet_data_api_output)
    mac_address = ethernet_ethernet_data_output.get("MACAddress", "")
    link_speed = ethernet_ethernet_data_output.get("SpeedMbps", "")
    auto_neg = ethernet_ethernet_data_output.get("AutoNeg", "")
    perm_mac_addr = ethernet_ethernet_data_output.get("PermanentMACAddress", "")
    health = ethernet_ethernet_data_output.get("Status", {}).get("Health", NA)
    return mac_address, link_speed, auto_neg, perm_mac_addr, health


def mapped_nic_data(nic, nic_port_id):
    """Maps NIC fields from the API response to a structured format."""
    def sanitize(value):
        return NA if value == "" else value

    dcb_protocol, fcoe_boot_support, fcoe_offload_support, flex_add_support, \
        nic_part_support, pxe_boot_support, tcp_chimney_support, wol_support, \
        iscsi_boot_support, iscsi_offload_support = get_capability_nic_details(nic_port_id)

    link_status = get_nic_portmetrics_details(nic_port_id)
    mac_address, link_speed, auto_neg, perm_mac_addr, health = get_nic_ethernet_details()
    rx_bytes, rx_multicast, rx_unicast, tx_bytes, tx_multicast, tx_unicast = get_nicstatistics_details(nic_port_id)

    output = {
        "iSCSIOffloadSupport": sanitize(iscsi_offload_support),
        "ControllerBIOSVersion": nic.get("ControllerBIOSVersion", NA),
        "DCBExchangeProtocol": sanitize(dcb_protocol),
        "WWN": nic.get("WWN", NA),
        "DataBusWidth": nic.get("DataBusWidth", NA),
        "EFIVersion": nic.get("EFIVersion", NA),
        "FCoEBootSupport": sanitize(fcoe_boot_support),
        "VirtWWPN": nic.get("VirtWWPN", NA),
        "FCoEOffloadMode": nic.get("FCoEOffloadMode", NA),
        "FCoEWWNN": nic.get("FCoEWWNN", NA),
        "FQDD": nic.get("Id", NA),
        "FamilyVersion": nic.get("FamilyVersion", NA),
        "FlexAddressingSupport": sanitize(flex_add_support),
        "IPv4Address": nic.get("IPv4Addresses", NA),
        "IPv6Address": nic.get("IPv6Addresses", NA),
        "Key": nic.get("Id", NA),
        "LinkDuplex": nic.get("LinkDuplex", NA),
        "TxBytes": sanitize(tx_bytes),
        "TxMutlicast": sanitize(tx_multicast),
        "TxUnicast": sanitize(tx_unicast),
        "LinkSpeed": sanitize(link_speed),
        "LinkStatus": sanitize(link_status),
        "MaxBandwidthPercent": nic.get("MaxBandwidthPercent", NA),
        "MediaType": nic.get("MediaType", NA),
        "NICCapabilities": nic.get("NICCapabilities", NA),
        "NicMode": nic.get("NicMode", NA),
        "NicPartitioningSupport": sanitize(nic_part_support),
        "PermanentFCOEMACAddress": nic.get("PermanentFCOEMACAddress", NA),
        "PXEBootSupport": sanitize(pxe_boot_support),
        "PrimaryStatus": "Healthy" if health == "OK" else health,
        "PermanentMACAddress": sanitize(perm_mac_addr),
        "PermanentiSCSIMACAddress": nic.get("PermanentiSCSIMACAddress", NA),
        "ProductName": nic.get("ProductName", NA),
        "Protocol": nic.get("Protocol", NA),
        "SupportedBootProtocol": nic.get("SupportedBootProtocol", NA),
        "SwitchConnectionID": nic.get("SwitchConnectionID", NA),
        "SwitchPortConnectionID": nic.get("SwitchPortConnectionID", NA),
        "TCPChimneySupport": sanitize(tcp_chimney_support),
        "VFSRIOVSupport": nic.get("VFSRIOVSupport", NA),
        "VendorName": nic.get("VendorName", NA),
        "VirtMacAddr": sanitize(mac_address),
        "FCoEOffloadSupport": sanitize(fcoe_offload_support),
        "VirtWWN": nic.get("VirtWWN", NA),
        "WOLSupport": sanitize(wol_support),
        "DeviceDescription": nic.get("Description", NA),
        "WWPN": nic.get("WWPN", NA),
        "CurrentMACAddress": sanitize(mac_address),
        "iSCSIBootSupport": sanitize(iscsi_boot_support),
        "iScsiOffloadMode": nic.get("iScsiOffloadMode", NA),
        "AutoNegotiation": sanitize(auto_neg),
        "RxBytes": sanitize(rx_bytes),
        "RxMutlicast": sanitize(rx_multicast),
        "RxUnicast": sanitize(rx_unicast)
    }
    return output


output = []
nic_output = json.loads(nic_api_output)
nic_members = nic_output.get("Members", [])
for nic in nic_members:
    output.append(mapped_nic_data(nic, nic.get("Id")))
print(output)
