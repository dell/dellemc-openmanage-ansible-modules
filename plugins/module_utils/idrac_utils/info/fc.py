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

GET_IDRAC_FC_DETAILS_URI = "/redfish/v1/Chassis/System.Embedded.1/Oem/Dell/DellFC"
GET_IDRAC_FC_CAPABILITY_DETAILS_URI = "/redfish/v1/Chassis/System.Embedded.1/Oem/Dell/DellFCCapabilities"
GET_IDRAC_FC_PORT_METRICS_DETAILS_URI = "/redfish/v1/Chassis/System.Embedded.1//Oem/Dell/DellFCPortMetrics"
GET_IDRAC_ETHERNET_DETAILS_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/EthernetInterfaces/"
GET_IDRAC_STATISTICS_DETAILS_URI = "/redfish/v1/Chassis/System.Embedded.1/Oem/Dell/DellFCStatistics"
GET_IDRAC_MANAGER_ATTRIBUTES = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/iDRAC.Embedded.1"
NA = "Not Available"


class IDRACFCInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def get_fc_capability_details(self, id):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_FC_CAPABILITY_DETAILS_URI)
        if response.status_code == 200:
            for member in response.json_data.get("Members", []):
                if member.get("Id", "") == id:
                    dcb_protocol = member.get("DCBExchangeProtocol", "")
                    fcoe_boot_support = member.get("FCoEBootSupport", "")
                    fcoe_offload_support = member.get("FCoEOffloadSupport", "")
                    flex_add_support = member.get("FlexAddressingSupport", "")
                    FC_part_support = member.get("FCPartitioningSupport", "")
                    pxe_boot_support = member.get("PXEBootSupport", "")
                    tcp_chimney_support = member.get("TCPChimneySupport", "")
                    wol_support = member.get("PartitionWOLSupport", "")
                    iscsi_boot_support = member.get("iSCSIBootSupport", "")
                    iscsi_offload_support = member.get("iSCSIOffloadSupport", "")
                    return dcb_protocol, fcoe_boot_support, fcoe_offload_support, flex_add_support, \
                        FC_part_support, pxe_boot_support, tcp_chimney_support, wol_support, \
                        iscsi_boot_support, iscsi_offload_support

        return "", "", "", "", "", "", "", "", "", ""

    def get_fc_port_metrics_details(self, id):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_FC_PORT_METRICS_DETAILS_URI)
        if response.status_code == 200:
            for member in response.json_data.get("Members", []):
                if member.get("Id", "") == id:
                    link_status = member.get("PartitionLinkStatus", "")
                    return link_status
        return ""

    def get_fc_statistics_details(self, id):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_STATISTICS_DETAILS_URI)
        if response.status_code == 200:
            for member in response.json_data.get("Members", []):
                if member.get("Id", "") == id:
                    rx_bytes = member.get("RxBytes", "")
                    rx_multicast = member.get("RxMutlicastPackets", "")
                    rx_unicast = member.get("RxunicastPackets", "")
                    tx_bytes = member.get("TxBytes", "")
                    tx_multicast = member.get("TxMutlicastPackets", "")
                    tx_unicast = member.get("TxunicastPackets", "")
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

    def map_FC_data(self, FC, id):
        """Maps FC fields from the API response to a structured format."""
        def sanitize(value):
            return NA if value == "" else value

        dcb_protocol, fcoe_boot_support, fcoe_offload_support, flex_add_support, FC_part_support, \
            pxe_boot_support, tcp_chimney_support, wol_support, iscsi_boot_support, iscsi_offload_support = self.get_fc_capability_details(id)

        link_status = self.get_fc_port_metrics_details(id)
        mac_address, link_speed, auto_neg, perm_mac_addr, health = self.get_ethernet_details()
        rx_bytes, rx_multicast, rx_unicast, tx_bytes, tx_multicast, tx_unicast = self.get_fc_statistics_details(id)

        output = {
            "AutoNegotiation": sanitize(auto_neg),
            "ControllerBIOSVersion": FC.get("ControllerBIOSVersion", NA),
            "CurrentMACAddress": sanitize(mac_address),
            "DCBExchangeProtocol": sanitize(dcb_protocol),
            "DataBusWidth": FC.get("DataBusWidth", NA),
            "DeviceDescription": FC.get("Description", NA),
            "EFIVersion": FC.get("EFIVersion", NA),
            "FCoEBootSupport": sanitize(fcoe_boot_support),
            "FCoEOffloadMode": FC.get("FCoEOffloadMode", NA),
            "FCoEOffloadSupport": sanitize(fcoe_offload_support),
            "FCoEWWNN": FC.get("FCoEWWNN", NA),
            "FQDD": FC.get("Id", NA),
            "FamilyVersion": FC.get("FamilyVersion", NA),
            "FlexAddressingSupport": sanitize(flex_add_support),
            "IPv4Address": FC.get("IPv4Addresses", NA),
            "IPv6Address": FC.get("IPv6Addresses", NA),
            "Key": FC.get("Id", NA),
            "LinkDuplex": FC.get("LinkDuplex", NA),
            "LinkSpeed": sanitize(link_speed),
            "LinkStatus": sanitize(link_status),
            "MaxBandwidthPercent": FC.get("MaxBandwidthPercent", NA),
            "MediaType": FC.get("MediaType", NA),
            "FCCapabilities": FC.get("FCCapabilities", NA),
            "FCMode": FC.get("FCMode", NA),
            "FCPartitioningSupport": sanitize(FC_part_support),
            "PXEBootSupport": sanitize(pxe_boot_support),
            "PermanentFCOEMACAddress": FC.get("PermanentFCOEMACAddress", NA),
            "PermanentMACAddress": sanitize(perm_mac_addr),
            "PermanentiSCSIMACAddress": FC.get("PermanentiSCSIMACAddress", NA),
            "PrimaryStatus": "Healthy" if health == "OK" else health,
            "ProductName": FC.get("ProductName", NA),
            "Protocol": FC.get("Protocol", NA),
            "RxBytes": sanitize(rx_bytes),
            "RxMutlicast": sanitize(rx_multicast),
            "Rxunicast": sanitize(rx_unicast),
            "SupportedBootProtocol": FC.get("SupportedBootProtocol", NA),
            "SwitchConnectionID": FC.get("SwitchConnectionID", NA),
            "SwitchPortConnectionID": FC.get("SwitchPortConnectionID", NA),
            "TCPChimneySupport": sanitize(tcp_chimney_support),
            "TxBytes": sanitize(tx_bytes),
            "TxMutlicast": sanitize(tx_multicast),
            "Txunicast": sanitize(tx_unicast),
            "VFSRIOVSupport": FC.get("VFSRIOVSupport", NA),
            "VendorName": FC.get("VendorName", NA),
            "VirtMacAddr": sanitize(mac_address),
            "VirtWWN": FC.get("VirtWWN", NA),
            "VirtWWPN": FC.get("VirtWWPN", NA),
            "WOLSupport": sanitize(wol_support),
            "WWN": FC.get("WWN", NA),
            "WWPN": FC.get("WWPN", NA),
            "iSCSIBootSupport": sanitize(iscsi_boot_support),
            "iSCSIOffloadSupport": sanitize(iscsi_offload_support),
            "iScsiOffloadMode": FC.get("iScsiOffloadMode", NA)
        }
        return output

    def get_fc_info(self):
        """Fetches FC data from iDRAC and maps it."""
        output = []
        resp = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_FC_DETAILS_URI)

        if resp.status_code == 200:
            FC_members = resp.json_data.get("Members", [])
            for FC in FC_members:
                output.append(self.map_FC_data(FC, FC.get("Id")))
            return output
