# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 10.0.2
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
GET_IDRAC_FC_STATISTICS_DETAILS_URI = "/redfish/v1/Chassis/System.Embedded.1/Oem/Dell/DellFCStatistics"
NA = "Not Available"


class IDRACFCInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def get_fc_capability_details(self, id):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_FC_CAPABILITY_DETAILS_URI)
        if response.status_code == 200:
            for member in response.json_data.get("Members", []):
                if member.get("Id", "") == id:
                    feature_licensing_support = member.get("FeatureLicensingSupport", "")
                    uefi_support = member.get("uEFISupport", "")
                    flex_addressing_support = member.get("FlexAddressingSupport", "")
                    on_chip_thermal_sensor = member.get("OnChipThermalSensor", "")
                    fc_max_num_exchanges = member.get("FCMaxNumberExchanges", "")
                    fc_max_num_outstanding_cmds = member.get("FCMaxNumberOutStandingCommands", "")
                    persistence_policy_support = member.get("PersistencePolicySupport", "")

                    return feature_licensing_support, uefi_support, flex_addressing_support, \
                        on_chip_thermal_sensor, fc_max_num_exchanges, fc_max_num_outstanding_cmds, \
                        persistence_policy_support

        return "", "", "", "", "", "", ""

    def get_fc_port_metrics_details(self, id):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_FC_PORT_METRICS_DETAILS_URI)
        if response.status_code == 200:
            for member in response.json_data.get("Members", []):
                if member.get("Id", "") == id:
                    os_driver_state = member.get("OSDriverState", "")
                    fc_tx_total_frames = member.get("FCTxTotalFrames", "")
                    fc_rx_total_frames = member.get("FCRxTotalFrames", "")
                    fc_tx_sequences = member.get("FCTxSequences", "")
                    fc_rx_sequences = member.get("FCRxSequences", "")
                    fc_tx_kb_count = member.get("FCTxKBCount", "")
                    fc_rx_kb_count = member.get("FCRxKBCount", "")
                    fc_invalid_crcs = member.get("FCInvalidCRCs", "")
                    fc_loss_of_signals = member.get("FCLossOfSignals", "")
                    fc_link_failures = member.get("FCLinkFailures", "")

                    oem_data = member.get("Oem", {})
                    if not isinstance(oem_data, dict):
                        oem_data = {}

                    return os_driver_state, fc_tx_total_frames, fc_rx_total_frames, \
                        fc_tx_sequences, fc_rx_sequences, fc_tx_kb_count, fc_rx_kb_count, \
                        fc_invalid_crcs, fc_loss_of_signals, fc_link_failures, oem_data

        return "", "", "", "", "", "", "", "", "", "", {}

    def get_fc_statistics_details(self, id):
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_FC_STATISTICS_DETAILS_URI)
        if response.status_code == 200:
            for member in response.json_data.get("Members", []):
                if member.get("Id", "") == id:
                    port_status = member.get("PortStatus", "")
                    return port_status
        return ""

    def map_fc_data(self, fc, id):
        """Maps FC fields from the API response to a structured format."""
        def sanitize(value):
            return NA if value == "" else value

        feature_licensing_support, uefi_support, flex_addressing_support, \
            on_chip_thermal_sensor, fc_max_num_exchanges, fc_max_num_outstanding_cmds, \
            persistence_policy_support = self.get_fc_capability_details(id)

        os_driver_state, fc_tx_total_frames, fc_rx_total_frames, \
            fc_tx_sequences, fc_rx_sequences, fc_tx_kb_count, fc_rx_kb_count, \
            fc_invalid_crcs, fc_loss_of_signals, fc_link_failures, oem_data = self.get_fc_port_metrics_details(id)

        port_status = self.get_fc_statistics_details(id)

        output = {
            "DeviceName": fc.get("DeviceName", NA),
            "Id": fc.get("Id", NA),
            "Bus": fc.get("Bus", NA),
            "PortDownRetryCount": fc.get("PortDownRetryCount", NA),
            "VendorName": fc.get("VendorName", NA),
            "HardZoneAddress": fc.get("HardZoneAddress", NA),
            "Description": fc.get("Description", NA),
            "PortLoginTimeout": fc.get("PortLoginTimeout", NA),
            "FramePayloadSize": fc.get("FramePayloadSize", NA),
            "LinkDownTimeout": fc.get("LinkDownTimeout", NA),
            "SerialNumber": fc.get("SerialNumber", NA),
            "LoopResetDelay": fc.get("LoopResetDelay", NA),
            "FCoEOSDriverVersion": fc.get("FCoEOSDriverVersion", NA),
            "FCTapeEnable": fc.get("FCTapeEnable", NA),
            "ProductName": fc.get("ProductName", NA),
            "SecondFCTargetLUN": fc.get("SecondFCTargetLUN", NA),
            "Name": fc.get("Name", NA),
            "FabricLoginTimeout": fc.get("FabricLoginTimeout", NA),
            "ChipType": fc.get("ChipType", NA),
            "RDMAOSDriverVersion": fc.get("RDMAOSDriverVersion", NA),
            "HardZoneEnable": fc.get("HardZoneEnable", NA),
            "EFIVersion": fc.get("EFIVersion", NA),
            "DeviceDescription": fc.get("DeviceDescription", NA),
            "FabricLoginRetryCount": fc.get("FabricLoginRetryCount", NA),
            "ISCSIOSDriverVersion": fc.get("ISCSIOSDriverVersion", NA),
            "SecondFCTargetWWPN": fc.get("SecondFCTargetWWPN", NA),
            "Device": fc.get("Device", NA),
            "LANDriverVersion": fc.get("LANDriverVersion", NA),
            "FCOSDriverVersion": fc.get("FCOSDriverVersion", NA),
            "Function": fc.get("Function", NA),
            "FamilyVersion": fc.get("FamilyVersion", NA),
            "PortLoginRetryCount": fc.get("PortLoginRetryCount", NA),
            "PartNumber": fc.get("PartNumber", NA),
            "PortDownTimeout": fc.get("PortDownTimeout", NA),
            "FeatureLicensingSupport": sanitize(feature_licensing_support),
            "UEFISupport": sanitize(uefi_support),
            "FlexAddressingSupport": sanitize(flex_addressing_support),
            "OnChipThermalSensor": sanitize(on_chip_thermal_sensor),
            "FCMaxNumberExchanges": sanitize(fc_max_num_exchanges),
            "FCMaxNumberOutStandingCommands": sanitize(fc_max_num_outstanding_cmds),
            "PersistencePolicySupport": sanitize(persistence_policy_support),
            "FCInvalidCRCs": sanitize(fc_invalid_crcs),
            "FCLinkFailures": sanitize(fc_link_failures),
            "FCLossOfSignals": sanitize(fc_loss_of_signals),
            "FCTxTotalFrames": sanitize(fc_tx_total_frames),
            "FCRxTotalFrames": sanitize(fc_rx_total_frames),
            "FCTxSequences": sanitize(fc_tx_sequences),
            "FCRxSequences": sanitize(fc_rx_sequences),
            "FCTxKBCount": sanitize(fc_tx_kb_count),
            "FCRxKBCount": sanitize(fc_rx_kb_count),
            "OSDriverState": sanitize(os_driver_state),
            "Oem": oem_data if isinstance(oem_data, dict) else {},
            "PortStatus": sanitize(port_status)
        }

        return output

    def get_fc_info(self):
        """Fetches FC data from iDRAC and maps it."""
        output = []
        resp = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_FC_DETAILS_URI)

        if resp.status_code == 200:
            fc_members = resp.json_data.get("Members", [])
            for fc in fc_members:
                output.append(self.map_fc_data(fc, fc.get("Id")))
            return output
