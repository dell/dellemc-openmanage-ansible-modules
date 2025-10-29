import sys
import json

fc_api_output = sys.argv[1]
fc_capability_api_output = sys.argv[2]
fc_portmetrics_api_output = sys.argv[3]
fc_statistics_api_output = sys.argv[4]
NA = "Not Available"


def get_capability_fc_details(id):
    fc_capability_output = json.loads(fc_capability_api_output)
    feature_licensing_support, uefi_support, flex_addressing_support, \
        on_chip_thermal_sensor, fc_max_num_exchanges, fc_max_num_outstanding_cmds, \
        persistence_policy_support = "", "", "", "", "", "", ""
    for member in fc_capability_output.get("Members", []):
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


def get_fc_portmetrics_details(id):
    fc_portmetrics_output = json.loads(fc_portmetrics_api_output)
    os_driver_state, fc_tx_total_frames, fc_rx_total_frames, \
        fc_tx_sequences, fc_rx_sequences, fc_tx_kb_count, fc_rx_kb_count, \
        fc_invalid_crcs, fc_loss_of_signals, fc_link_failures, oem_data = \
        "", "", "", "", "", "", "", "", "", "", {}
    for member in fc_portmetrics_output.get("Members", []):
        if member.get("Id", "") == id:
            fc_tx_total_frames = member.get("FCTxTotalFrames", "")
            fc_rx_total_frames = member.get("FCRxTotalFrames", "")
            fc_tx_sequences = member.get("FCTxSequences", "")
            fc_rx_sequences = member.get("FCRxSequences", "")
            fc_tx_kb_count = member.get("FCTxKBCount", "")
            fc_rx_kb_count = member.get("FCRxKBCount", "")
            fc_invalid_crcs = member.get("FCInvalidCRCs", "")
            fc_loss_of_signals = member.get("FCLossOfSignals", "")
            fc_link_failures = member.get("FCLinkFailures", "")
            os_driver_state = member.get("OSDriverState", "")

            oem_data = member.get("Oem", {})
            if not isinstance(oem_data, dict):
                oem_data = {}
    return os_driver_state, fc_tx_total_frames, fc_rx_total_frames, \
        fc_tx_sequences, fc_rx_sequences, fc_tx_kb_count, fc_rx_kb_count, \
        fc_invalid_crcs, fc_loss_of_signals, fc_link_failures, oem_data


def get_fc_statistics_details(id):
    fc_statistics_output = json.loads(fc_statistics_api_output)
    port_status = ""
    for member in fc_statistics_output.get("Members", []):
        if member.get("Id", "") == id:
            port_status = member.get("PortStatus", "")
    return port_status


def mapped_fc_data(fc, fc_port_id):
    """Maps FC fields from the API response to a structured format."""
    def sanitize(value):
        return NA if value == "" else value

    feature_licensing_support, uefi_support, flex_addressing_support, \
        on_chip_thermal_sensor, fc_max_num_exchanges, fc_max_num_outstanding_cmds, \
        persistence_policy_support = get_capability_fc_details(fc_port_id)

    os_driver_state, fc_tx_total_frames, fc_rx_total_frames, \
        fc_tx_sequences, fc_rx_sequences, fc_tx_kb_count, fc_rx_kb_count, \
        fc_invalid_crcs, fc_loss_of_signals, fc_link_failures, oem_data = get_fc_portmetrics_details(fc_port_id)

    port_status = get_fc_statistics_details(fc_port_id)

    output = {
        "PortStatus": sanitize(port_status),
        "Oem": oem_data if isinstance(oem_data, dict) else {},
        "OSDriverState": sanitize(os_driver_state),
        "FCRxKBCount": sanitize(fc_rx_kb_count),
        "FCTxKBCount": sanitize(fc_tx_kb_count),
        "FCRxSequences": sanitize(fc_rx_sequences),
        "FCTxSequences": sanitize(fc_tx_sequences),
        "FCRxTotalFrames": sanitize(fc_rx_total_frames),
        "FCTxTotalFrames": sanitize(fc_tx_total_frames),
        "FCLossOfSignals": sanitize(fc_loss_of_signals),
        "FCLinkFailures": sanitize(fc_link_failures),
        "FCInvalidCRCs": sanitize(fc_invalid_crcs),
        "PersistencePolicySupport": sanitize(persistence_policy_support),
        "FCMaxNumberOutStandingCommands": sanitize(fc_max_num_outstanding_cmds),
        "FCMaxNumberExchanges": sanitize(fc_max_num_exchanges),
        "OnChipThermalSensor": sanitize(on_chip_thermal_sensor),
        "FlexAddressingSupport": sanitize(flex_addressing_support),
        "UEFISupport": sanitize(uefi_support),
        "FeatureLicensingSupport": sanitize(feature_licensing_support),
        "PortDownTimeout": fc.get("PortDownTimeout", NA),
        "PartNumber": fc.get("PartNumber", NA),
        "PortLoginRetryCount": fc.get("PortLoginRetryCount", NA),
        "FamilyVersion": fc.get("FamilyVersion", NA),
        "Function": fc.get("Function", NA),
        "FCOSDriverVersion": fc.get("FCOSDriverVersion", NA),
        "LANDriverVersion": fc.get("LANDriverVersion", NA),
        "Device": fc.get("Device", NA),
        "SecondFCTargetWWPN": fc.get("SecondFCTargetWWPN", NA),
        "ISCSIOSDriverVersion": fc.get("ISCSIOSDriverVersion", NA),
        "FabricLoginRetryCount": fc.get("FabricLoginRetryCount", NA),
        "DeviceDescription": fc.get("DeviceDescription", NA),
        "EFIVersion": fc.get("EFIVersion", NA),
        "HardZoneEnable": fc.get("HardZoneEnable", NA),
        "RDMAOSDriverVersion": fc.get("RDMAOSDriverVersion", NA),
        "ChipType": fc.get("ChipType", NA),
        "FabricLoginTimeout": fc.get("FabricLoginTimeout", NA),
        "Name": fc.get("Name", NA),
        "SecondFCTargetLUN": fc.get("SecondFCTargetLUN", NA),
        "ProductName": fc.get("ProductName", NA),
        "FCTapeEnable": fc.get("FCTapeEnable", NA),
        "FCoEOSDriverVersion": fc.get("FCoEOSDriverVersion", NA),
        "LoopResetDelay": fc.get("LoopResetDelay", NA),
        "SerialNumber": fc.get("SerialNumber", NA),
        "LinkDownTimeout": fc.get("LinkDownTimeout", NA),
        "FramePayloadSize": fc.get("FramePayloadSize", NA),
        "PortLoginTimeout": fc.get("PortLoginTimeout", NA),
        "Description": fc.get("Description", NA),
        "HardZoneAddress": fc.get("HardZoneAddress", NA),
        "VendorName": fc.get("VendorName", NA),
        "PortDownRetryCount": fc.get("PortDownRetryCount", NA),
        "Bus": fc.get("Bus", NA),
        "Id": fc.get("Id", NA),
        "DeviceName": fc.get("DeviceName", NA)
    }
    return output


output = []
fc_output = json.loads(fc_api_output)
fc_members = fc_output.get("Members", [])
for fc in fc_members:
    output.append(mapped_fc_data(fc, fc.get("Id")))
