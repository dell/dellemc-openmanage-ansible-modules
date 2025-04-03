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


class IDRACNICInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def map_nic_data(self, nic):
        """Maps NIC fields from the API response to a structured format."""
        keys_to_search = {
            "AutoNegotiation": "AutoNeg",
            "ControllerBIOSVersion": "N/A",
            "CurrentMACAddress": "MACAddress",
            "DCBExchangeProtocol": "Not Supported",
            "DataBusWidth": "N/A",
            "DeviceDescription": "Description",
            "EFIVersion": "N/A",
            "FCoEBootSupport": "Not Supported",
            "FCoEOffloadMode": "Unknown",
            "FCoEOffloadSupport": "Not Supported",
            "FCoEWWNN": "Not Available",
            "FQDD": "Id",
            "FamilyVersion": "N/A",
            "FlexAddressingSupport": "Supported",
            "IPv4Address": "IPv4Addresses",
            "IPv6Address": "IPv6Addresses",
            "Key": "Id",
            "LinkDuplex": "FullDuplex",
            "LinkSpeed": "SpeedMbps",
            "LinkStatus": "LinkStatus",
            "MaxBandwidth": "N/A",
            "MediaType": "N/A",
            "NICCapabilities": "Not Available",
            "NicMode": "Unknown",
            "NicPartitioningSupport": "Not Supported",
            "PXEBootSupport": "Supported",
            "PermanentFCOEMACAddress": "Not Available",
            "PermanentMACAddress": "PermanentMACAddress",
            "PermanentiSCSIMACAddress": "Not Available",
            "PrimaryStatus": "Status.Health",
            "ProductName": "N/A",
            "Protocol": "NIC",
            "RxBytes": "N/A",
            "RxMutlicast": "N/A",
            "RxUnicast": "N/A",
            "SupportedBootProtocol": "Not Available",
            "SwitchConnectionID": "N/A",
            "SwitchPortConnectionID": "N/A",
            "TCPChimneySupport": "Not Supported",
            "TxBytes": "N/A",
            "TxMutlicast": "N/A",
            "TxUnicast": "N/A",
            "VFSRIOVSupport": "Not Supported",
            "VendorName": "N/A",
            "VirtMacAddr": "MACAddress",
            "VirtWWN": "Not Available",
            "VirtWWPN": "Not Available",
            "WOLSupport": "Supported",
            "WWN": "Not Available",
            "WWPN": "Not Available",
            "iSCSIBootSupport": "Not Supported",
            "iSCSIOffloadSupport": "Not Supported",
            "iScsiOffloadMode": "Unknown"
        }

        nic_data = {}

        for key, response_key in keys_to_search.items():
            if key in ["IPv4Address", "IPv6Address"]:
                # Extract first available IP address, if present
                addresses = nic.get(response_key, [])
                nic_data[key] = addresses[0] if addresses else "Not Available"
            elif "." in response_key:
                # Handle nested fields like Status.Health
                keys = response_key.split(".")
                data = nic
                for k in keys:
                    data = data.get(k, "Not Available")
                nic_data[key] = data
            else:
                nic_data[key] = nic.get(response_key, "Not Available")

        return nic_data

    def get_nic_info(self):
        """Fetches NIC data from iDRAC and maps it."""
        output = []
        resp = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_NIC_DETAILS_URI_10)

        if resp.status_code == 200:
            nic_members = resp.json_data.get("Members", [])
            for nic in nic_members:
                output.append(self.map_nic_data(nic))
            return output
