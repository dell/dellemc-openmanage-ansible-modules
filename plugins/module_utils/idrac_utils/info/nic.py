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

GET_IDRAC_NIC_DETAILS_URI_10 = "/redfish/v1/Systems/System.Embedded.1/EthernetInterfaces?$expand=*($levels=1)"
GET_IDRAC_MANAGER_ATTRIBUTES = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/iDRAC.Embedded.1"
NA = "Not Available"


class IDRACNICInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    # "LinkDuplex" :{
    #     "0" : "Unknown",
    #     "1" : "Full Duplex",
    #     "2" : "Half Duplex"
    # }

    def map_nic_data(self, nic):
        """Maps NIC fields from the API response to a structured format."""
        health = nic.get("Status", {}).get("Health", NA)
        output = {
            "AutoNegotiation": nic.get("AutoNeg", NA),
            # "ControllerBIOSVersion": nic.get("ControllerBIOSVersion", NA),
            "CurrentMACAddress": nic.get("MACAddress", NA),
            # "DCBExchangeProtocol": nic.get("DCBExchangeProtocol", NA),
            # "DataBusWidth": nic.get("DataBusWidth", NA),
            "DeviceDescription": nic.get("Description", NA),
            # "EFIVersion": nic.get("EFIVersion", NA),
            # "FCoEBootSupport": nic.get("FCoEBootSupport", NA),
            # "FCoEOffloadMode": nic.get("FCoEOffloadMode", NA),
            # "FCoEOffloadSupport": nic.get("FCoEOffloadSupport", NA),
            # "FCoEWWNN": nic.get("FCoEWWNN", NA),
            "FQDD": nic.get("Id", NA),
            # "FamilyVersion": nic.get("FamilyVersion", NA),
            # "FlexAddressingSupport": nic.get("FlexAddressingSupport", NA),
            "IPv4Address": nic.get("IPv4Addresses", NA),
            "IPv6Address": nic.get("IPv6Addresses", NA),
            "Key": nic.get("Id", NA),
            # "LinkDuplex": nic.get("LinkDuplex", NA),
            # "LinkSpeed": nic.get("LinkSpeed", NA),
            "LinkStatus": nic.get("LinkStatus", NA),
            "MaxBandwidth": nic.get("SpeedMbps", NA),
            # "MediaType": nic.get("MediaType", NA),
            # "NICCapabilities": nic.get("NICCapabilities", NA),
            # "NicMode": nic.get("NicMode", NA),
            # "NicPartitioningSupport": nic.get("NicPartitioningSupport", NA),
            # "PXEBootSupport": nic.get("PXEBootSupport", NA),
            # "PermanentFCOEMACAddress": nic.get("PermanentFCOEMACAddress", NA),
            "PermanentMACAddress": nic.get("PermanentMACAddress", NA),
            # "PermanentiSCSIMACAddress": nic.get("PermanentiSCSIMACAddress", NA),
            "PrimaryStatus": "Healthy" if health == "OK" else health,
            # "ProductName": nic.get("ProductName", NA),
            # "Protocol": nic.get("Protocol", NA),
            # "RxBytes": nic.get("RxBytes", NA),
            # "RxMutlicast": nic.get("RxMutlicast", NA),
            # "RxUnicast": nic.get("RxUnicast", NA),
            # "SupportedBootProtocol": nic.get("SupportedBootProtocol", NA),
            # "SwitchConnectionID": nic.get("SwitchConnectionID", NA),
            # "SwitchPortConnectionID": nic.get("SwitchPortConnectionID", NA),
            # "TCPChimneySupport": nic.get("TCPChimneySupport", NA),
            # "TxBytes": nic.get("TxBytes", NA),
            # "TxMutlicast": nic.get("TxMutlicast", NA),
            # "TxUnicast": nic.get("TxUnicast", NA),
            # "VFSRIOVSupport": nic.get("VFSRIOVSupport", NA),
            # "VendorName": nic.get("VendorName", NA),
            # "VirtMacAddr": nic.get("VirtMacAddr", NA),
            # "VirtWWN": nic.get("VirtWWN", NA),
            # "VirtWWPN": nic.get("VirtWWPN", NA),
            # "WOLSupport": nic.get("WOLSupport", NA),
            # "WWN": nic.get("WWN", NA),
            # "WWPN": nic.get("WWPN", NA),
            # "iSCSIBootSupport": nic.get("iSCSIBootSupport", NA),
            # "iSCSIOffloadSupport": nic.get("iSCSIOffloadSupport", NA),
            # "iScsiOffloadMode": nic.get("iScsiOffloadMode", NA)
        }

        return output

    def get_nic_info(self):
        """Fetches NIC data from iDRAC and maps it."""
        output = []
        resp = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_NIC_DETAILS_URI_10)

        if resp.status_code == 200:
            nic_members = resp.json_data.get("Members", [])
            for nic in nic_members:
                output.append(self.map_nic_data(nic))
            return output
