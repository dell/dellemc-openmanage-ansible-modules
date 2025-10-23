import sys
import json

fc_api_output = sys.argv[1]
fc_capability_api_output = sys.argv[2]
fc_portmetrics_api_output = sys.argv[3]
fc_statistics_api_output = sys.argv[4]
ethernet_ethernet_data_api_output = sys.argv[5]
NA = "Not Available"


def get_capability_fc_details(id):
    fc_capability_output = json.loads(fc_capability_api_output)
    dcb_protocol, fcoe_boot_support, fcoe_offload_support, flex_add_support, \
        fc_part_support, pxe_boot_support, tcp_chimney_support, wol_support, \
        iscsi_boot_support, iscsi_offload_support = "", "", "", "", \
        "", "", "", "", "", ""
    for member in fc_capability_output.get("Members", []):
        if member.get("Id", "") == id:
            iscsi_offload_support = member.get("iSCSIOffloadSupport", "")
            dcb_protocol = member.get("DCBExchangeProtocol", "")
            wol_support = member.get("PartitionWOLSupport", "")
            fcoe_boot_support = member.get("FCoEBootSupport", "")
            pxe_boot_support = member.get("PXEBootSupport", "")
            fcoe_offload_support = member.get("FCoEOffloadSupport", "")
            flex_add_support = member.get("FlexAddressingSupport", "")
            iscsi_boot_support = member.get("iSCSIBootSupport", "")
            fc_part_support = member.get("NicPartitioningSupport", "")
            tcp_chimney_support = member.get("TCPChimneySupport", "")
    return dcb_protocol, fcoe_boot_support, fcoe_offload_support, \
        flex_add_support, fc_part_support, pxe_boot_support, \
        tcp_chimney_support, wol_support, iscsi_boot_support, \
        iscsi_offload_support


def get_fc_portmetrics_details(fc_port_id):
    fc_portmetrics_output = json.loads(fc_portmetrics_api_output)
    link_status = ""
    for member in fc_portmetrics_output.get("Members", []):
        if member.get("Id", "") == fc_port_id:
            link_status = member.get("PartitionLinkStatus", "")
    return link_status


def get_fcstatistics_details(id):
    fc_statistics_output = json.loads(fc_statistics_api_output)
    rx_bytes, rx_multicast, rx_unicast, tx_bytes, tx_multicast, \
        tx_unicast = "", "", "", "", "", ""
    for member in fc_statistics_output.get("Members", []):
        if member.get("Id", "") == id:
            rx_bytes = member.get("RxBytes", "")
            tx_unicast = member.get("TxUnicastPackets", "")
            rx_unicast = member.get("RxUnicastPackets", "")
            tx_bytes = member.get("TxBytes", "")
            tx_multicast = member.get("TxMutlicastPackets", "")
            rx_multicast = member.get("RxMutlicastPackets", "")
    return rx_bytes, rx_multicast, rx_unicast, tx_bytes, \
        tx_multicast, tx_unicast


def get_fc_ethernet_details():
    ethernet_ethernet_data_output = json.loads(ethernet_ethernet_data_api_output)
    mac_address = ethernet_ethernet_data_output.get("MACAddress", "")
    link_speed = ethernet_ethernet_data_output.get("SpeedMbps", "")
    auto_neg = ethernet_ethernet_data_output.get("AutoNeg", "")
    perm_mac_addr = ethernet_ethernet_data_output.get("PermanentMACAddress", "")
    health = ethernet_ethernet_data_output.get("Status", {}).get("Health", NA)
    return mac_address, link_speed, auto_neg, perm_mac_addr, health


def mapped_fc_data(fc, fc_port_id):
    """Maps FC fields from the API response to a structured format."""
    def sanitize(value):
        return NA if value == "" else value

    dcb_protocol, fcoe_boot_support, fcoe_offload_support, flex_add_support, \
        fc_part_support, pxe_boot_support, tcp_chimney_support, wol_support, \
        iscsi_boot_support, iscsi_offload_support = get_capability_fc_details(fc_port_id)

    link_status = get_fc_portmetrics_details(fc_port_id)
    mac_address, link_speed, auto_neg, perm_mac_addr, health = get_fc_ethernet_details()
    rx_bytes, rx_multicast, rx_unicast, tx_bytes, tx_multicast, tx_unicast = get_fcstatistics_details(fc_port_id)

    output = {
        "iSCSIOffloadSupport": sanitize(iscsi_offload_support),
        "ControllerBIOSVersion": fc.get("ControllerBIOSVersion", NA),
        "DCBExchangeProtocol": sanitize(dcb_protocol),
        "WWN": fc.get("WWN", NA),
        "DataBusWidth": fc.get("DataBusWidth", NA),
        "EFIVersion": fc.get("EFIVersion", NA),
        "FCoEBootSupport": sanitize(fcoe_boot_support),
        "VirtWWPN": fc.get("VirtWWPN", NA),
        "FCoEOffloadMode": fc.get("FCoEOffloadMode", NA),
        "FCoEWWNN": fc.get("FCoEWWNN", NA),
        "FQDD": fc.get("Id", NA),
        "FamilyVersion": fc.get("FamilyVersion", NA),
        "FlexAddressingSupport": sanitize(flex_add_support),
        "IPv4Address": fc.get("IPv4Addresses", NA),
        "IPv6Address": fc.get("IPv6Addresses", NA),
        "Key": fc.get("Id", NA),
        "LinkDuplex": fc.get("LinkDuplex", NA),
        "TxBytes": sanitize(tx_bytes),
        "TxMutlicast": sanitize(tx_multicast),
        "TxUnicast": sanitize(tx_unicast),
        "LinkSpeed": sanitize(link_speed),
        "LinkStatus": sanitize(link_status),
        "MaxBandwidthPercent": fc.get("MaxBandwidthPercent", NA),
        "MediaType": fc.get("MediaType", NA),
        "FCCapabilities": fc.get("FCCapabilities", NA),
        "NicMode": fc.get("NicMode", NA),
        "NicPartitioningSupport": sanitize(fc_part_support),
        "PermanentFCOEMACAddress": fc.get("PermanentFCOEMACAddress", NA),
        "PXEBootSupport": sanitize(pxe_boot_support),
        "PrimaryStatus": "Healthy" if health == "OK" else health,
        "PermanentMACAddress": sanitize(perm_mac_addr),
        "PermanentiSCSIMACAddress": fc.get("PermanentiSCSIMACAddress", NA),
        "ProductName": fc.get("ProductName", NA),
        "Protocol": fc.get("Protocol", NA),
        "SupportedBootProtocol": fc.get("SupportedBootProtocol", NA),
        "SwitchConnectionID": fc.get("SwitchConnectionID", NA),
        "SwitchPortConnectionID": fc.get("SwitchPortConnectionID", NA),
        "TCPChimneySupport": sanitize(tcp_chimney_support),
        "VFSRIOVSupport": fc.get("VFSRIOVSupport", NA),
        "VendorName": fc.get("VendorName", NA),
        "VirtMacAddr": sanitize(mac_address),
        "FCoEOffloadSupport": sanitize(fcoe_offload_support),
        "VirtWWN": fc.get("VirtWWN", NA),
        "WOLSupport": sanitize(wol_support),
        "DeviceDescription": fc.get("Description", NA),
        "WWPN": fc.get("WWPN", NA),
        "CurrentMACAddress": sanitize(mac_address),
        "iSCSIBootSupport": sanitize(iscsi_boot_support),
        "iScsiOffloadMode": fc.get("iScsiOffloadMode", NA),
        "AutoNegotiation": sanitize(auto_neg),
        "RxBytes": sanitize(rx_bytes),
        "RxMutlicast": sanitize(rx_multicast),
        "RxUnicast": sanitize(rx_unicast)
    }
    return output


output = []
fc_output = json.loads(fc_api_output)
fc_members = fc_output.get("Members", [])
for fc in fc_members:
    output.append(mapped_fc_data(fc, fc.get("Id")))
print(output)
