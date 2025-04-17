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

GET_IDRAC_NIC_DETAILS_URI = "/redfish/v1/Chassis/System.Embedded.1/Oem/Dell/DellNIC"
GET_IDRAC_NIC_CAPABILITY_DETAILS_URI = "/redfish/v1/Chassis/System.Embedded.1/Oem/Dell/DellNICCapabilities"
GET_IDRAC_NIC_PORT_METRICS_DETAILS_URI = "/redfish/v1/Chassis/System.Embedded.1//Oem/Dell/DellNICPortMetrics"
GET_IDRAC_ETHERNET_DETAILS_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/EthernetInterfaces/"
GET_IDRAC_STATISTICS_DETAILS_URI = "/redfish/v1/Chassis/System.Embedded.1/Oem/Dell/DellNICStatistics"
GET_IDRAC_MANAGER_ATTRIBUTES = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/iDRAC.Embedded.1"
NA = "Not Available"


class IDRACNICInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def get_nic_capability_details(self, id):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_NIC_CAPABILITY_DETAILS_URI)
        if response.status_code == 200:
            for member in response.json_data.get("Members", []):
                if member.get("Id", "") == id:
                    dcb_protocol = member.get("DCBExchangeProtocol", "")
                    fcoe_boot_support = member.get("FCoEBootSupport", "")
                    fcoe_offload_support = member.get("FCoEOffloadSupport", "")
                    flex_add_support = member.get("FlexAddressingSupport", "")
                    nic_part_support = member.get("NicPartitioningSupport", "")
                    pxe_boot_support = member.get("PXEBootSupport", "")
                    tcp_chimney_support = member.get("TCPChimneySupport", "")
                    wol_support = member.get("PartitionWOLSupport", "")
                    iscsi_boot_support = member.get("iSCSIBootSupport", "")
                    iscsi_offload_support = member.get("iSCSIOffloadSupport", "")
                    return dcb_protocol, fcoe_boot_support, fcoe_offload_support, flex_add_support, \
                        nic_part_support, pxe_boot_support, tcp_chimney_support, wol_support, \
                        iscsi_boot_support, iscsi_offload_support

        return "", "", "", "", "", "", "", "", "", ""

    def get_nic_port_metrics_details(self, id):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_NIC_PORT_METRICS_DETAILS_URI)
        if response.status_code == 200:
            for member in response.json_data.get("Members", []):
                if member.get("Id", "") == id:
                    link_status = member.get("PartitionLinkStatus", "")
                    return link_status
        return ""

    def get_nic_statistics_details(self, id):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_STATISTICS_DETAILS_URI)
        if response.status_code == 200:
            for member in response.json_data.get("Members", []):
                if member.get("Id", "") == id:
                    rx_bytes = member.get("RxBytes", "")
                    rx_multicast = member.get("RxMutlicastPackets", "")
                    rx_unicast = member.get("RxUnicastPackets", "")
                    tx_bytes = member.get("TxBytes", "")
                    tx_multicast = member.get("TxMutlicastPackets", "")
                    tx_unicast = member.get("TxUnicastPackets", "")
                    return rx_bytes, rx_multicast, rx_unicast, tx_bytes, tx_multicast, tx_unicast
        return "", "", "", "", "", ""

    def get_ethernet_details(self):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_ETHERNET_DETAILS_URI)
        if response.status_code == 200:
            members = response.json_data.get("Members", [])
            if members:
                first_member_uri = members[0].get("@odata.id")
                if first_member_uri:
                    eth_resp = self.idrac.invoke_request(method='GET', uri=first_member_uri)
                    if eth_resp.status_code == 200:
                        mac_address = eth_resp.json_data.get("MACAddress", "")
                        link_speed = eth_resp.json_data.get("SpeedMbps", "")
                        auto_neg = eth_resp.json_data.get("AutoNeg", "")
                        perm_mac_addr = eth_resp.json_data.get("PermanentMACAddress", "")
                        health = eth_resp.json_data.get("Status", {}).get("Health", NA)
                        return mac_address, link_speed, auto_neg, perm_mac_addr, health
        return "", "", "", "", ""

    def map_nic_data(self, nic, id):
        """Maps NIC fields from the API response to a structured format."""
        def sanitize(value):
            return NA if value == "" else value

        dcb_protocol, fcoe_boot_support, fcoe_offload_support, flex_add_support, nic_part_support, \
            pxe_boot_support, tcp_chimney_support, wol_support, iscsi_boot_support, iscsi_offload_support = self.get_nic_capability_details(id)

        link_status = self.get_nic_port_metrics_details(id)
        mac_address, link_speed, auto_neg, perm_mac_addr, health = self.get_ethernet_details()
        rx_bytes, rx_multicast, rx_unicast, tx_bytes, tx_multicast, tx_unicast = self.get_nic_statistics_details(id)

        output = {
            "AutoNegotiation": sanitize(auto_neg),
            "ControllerBIOSVersion": nic.get("ControllerBIOSVersion", NA),
            "CurrentMACAddress": sanitize(mac_address),
            "DCBExchangeProtocol": sanitize(dcb_protocol),
            "DataBusWidth": nic.get("DataBusWidth", NA),
            "DeviceDescription": nic.get("Description", NA),
            "EFIVersion": nic.get("EFIVersion", NA),
            "FCoEBootSupport": sanitize(fcoe_boot_support),
            "FCoEOffloadMode": nic.get("FCoEOffloadMode", NA),
            "FCoEOffloadSupport": sanitize(fcoe_offload_support),
            "FCoEWWNN": nic.get("FCoEWWNN", NA),
            "FQDD": nic.get("Id", NA),
            "FamilyVersion": nic.get("FamilyVersion", NA),
            "FlexAddressingSupport": sanitize(flex_add_support),
            "IPv4Address": nic.get("IPv4Addresses", NA),
            "IPv6Address": nic.get("IPv6Addresses", NA),
            "Key": nic.get("Id", NA),
            "LinkDuplex": nic.get("LinkDuplex", NA),
            "LinkSpeed": sanitize(link_speed),
            "LinkStatus": sanitize(link_status),
            "MaxBandwidthPercent": nic.get("MaxBandwidthPercent", NA),
            "MediaType": nic.get("MediaType", NA),
            "NICCapabilities": nic.get("NICCapabilities", NA),
            "NicMode": nic.get("NicMode", NA),
            "NicPartitioningSupport": sanitize(nic_part_support),
            "PXEBootSupport": sanitize(pxe_boot_support),
            "PermanentFCOEMACAddress": nic.get("PermanentFCOEMACAddress", NA),
            "PermanentMACAddress": sanitize(perm_mac_addr),
            "PermanentiSCSIMACAddress": nic.get("PermanentiSCSIMACAddress", NA),
            "PrimaryStatus": "Healthy" if health == "OK" else health,
            "ProductName": nic.get("ProductName", NA),
            "Protocol": nic.get("Protocol", NA),
            "RxBytes": sanitize(rx_bytes),
            "RxMutlicast": sanitize(rx_multicast),
            "RxUnicast": sanitize(rx_unicast),
            "SupportedBootProtocol": nic.get("SupportedBootProtocol", NA),
            "SwitchConnectionID": nic.get("SwitchConnectionID", NA),
            "SwitchPortConnectionID": nic.get("SwitchPortConnectionID", NA),
            "TCPChimneySupport": sanitize(tcp_chimney_support),
            "TxBytes": sanitize(tx_bytes),
            "TxMutlicast": sanitize(tx_multicast),
            "TxUnicast": sanitize(tx_unicast),
            "VFSRIOVSupport": nic.get("VFSRIOVSupport", NA),
            "VendorName": nic.get("VendorName", NA),
            "VirtMacAddr": sanitize(mac_address),
            "VirtWWN": nic.get("VirtWWN", NA),
            "VirtWWPN": nic.get("VirtWWPN", NA),
            "WOLSupport": sanitize(wol_support),
            "WWN": nic.get("WWN", NA),
            "WWPN": nic.get("WWPN", NA),
            "iSCSIBootSupport": sanitize(iscsi_boot_support),
            "iSCSIOffloadSupport": sanitize(iscsi_offload_support),
            "iScsiOffloadMode": nic.get("iScsiOffloadMode", NA)
        }
        return output

    def get_nic_info(self):
        """Fetches NIC data from iDRAC and maps it."""
        output = []
        resp = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_NIC_DETAILS_URI)

        if resp.status_code == 200:
            nic_members = resp.json_data.get("Members", [])
            for nic in nic_members:
                output.append(self.map_nic_data(nic, nic.get("Id")))
            return output
