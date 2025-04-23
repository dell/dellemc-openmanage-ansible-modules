
from ansible_collections.dellemc.openmanage.plugins.\
    module_utils.idrac_utils.info.controller import IDRACControllerInfo
from ansible_collections.dellemc.openmanage.tests.unit.\
    plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils
from unittest.mock import MagicMock


class TestIDRACControllerInfo(TestUtils):
    def test_get_controller_info(self, idrac_mock):
        mock_response = {
            "Members": [{
                "Bus": "1",
                "CacheSize": "0.0 MB",
                "CachecadeCapability": "Cachecade Virtual Disk not supported",
                "ControllerFirmwareVersion": "x.x.x.x",
                "DeviceCardDataBusWidth": "4x or x4",
                "DeviceCardSlotLength": "4",
                "DeviceCardSlotType": "PCI Express Gen 4 x8",
                "DeviceDescription": "Storage Controller in Slot 1",
                "DriverVersion": "Not Available",
                "DeviceCardManufacturer": "DELL",
                "EncryptionCapability": "None",
                "EncryptionMode": "None",
                "FQDD": "NonRAID.Slot.1-1",
                "Key": "NonRAID.Slot.1-1",
                "MaxAvailablePCILinkSpeed": "Not Available",
                "MaxPossiblePCILinkSpeed": "Not Available",
                "PCISlot": "1",
                "PCIVendorID": "1000",
                "PrimaryStatus": "Healthy",
                "RollupStatus": "Healthy",
                "SASAddress": "52CEA7F09B369000",
                "SecurityStatus": "Encryption Not Capable",
                "SlicedVDCapability": "Sliced Virtual Disk creation not supported",
                "SupportControllerBootMode": "0",
                "ProductName": "Dell HBA355i Adp",
                "SupportEnhancedAutoForeignImport": "0",
                "SupportRAID10UnevenSpans": "0",
                "T10PICapability": "0"
            }]
        }
        idrac_mock.invoke_request.return_value.json_data = mock_response
        video_info = IDRACControllerInfo(idrac_mock)
        video_info.get_controller_data = MagicMock(
            return_value=mock_response["Members"][0])
        result = video_info.get_controller_system_info()
        expected_result = [{
            "Bus": "1",
            "CacheSize": "0.0 MB",
            "CachecadeCapability": "Cachecade Virtual Disk not supported",
            "ControllerFirmwareVersion": "x.x.x.x",
            "DeviceCardDataBusWidth": "4x or x4",
            "DeviceCardManufacturer": "DELL",
            "DeviceCardSlotLength": "4",
            "DeviceCardSlotType": "PCI Express Gen 4 x8",
            "DeviceDescription": "Storage Controller in Slot 1",
            "DriverVersion": "Not Available",
            "EncryptionCapability": "None",
            "EncryptionMode": "None",
            "FQDD": "NonRAID.Slot.1-1",
            "Key": "NonRAID.Slot.1-1",
            "MaxAvailablePCILinkSpeed": "Not Available",
            "MaxPossiblePCILinkSpeed": "Not Available",
            "PCISlot": "1",
            "PCIVendorID": "1000",
            "PrimaryStatus": "Healthy",
            "ProductName": "Dell HBA355i Adp",
            "RollupStatus": "Healthy",
            "SASAddress": "52CEA7F09B369000",
            "SecurityStatus": "Encryption Not Capable",
            "SlicedVDCapability": "Sliced Virtual Disk creation not supported",
            "SupportControllerBootMode": "0",
            "SupportEnhancedAutoForeignImport": "0",
            "SupportRAID10UnevenSpans": "0",
            "T10PICapability": "0"
        }]
        assert result == expected_result

    def test_extract_controller_info(self, idrac_mock):
        mock_response = {
            "Members": [{
                "Bus": "1",
                "CacheSizeInMB": "8124",
                "CachecadeCapability": "Cachecade Virtual Disk not supported",
                "ControllerFirmwareVersion": "x.x.x.x",
                "DeviceCardDataBusWidth": "4x or x4",
                "DeviceCardManufacturer": "DELL",
                "DeviceCardSlotLength": "4",
                "DeviceCardSlotType": "PCI Express Gen 4 x8",
                "DriverVersion": "Not Available",
                "EncryptionCapability": "None",
                "EncryptionMode": "None",
                "Id": "NonRAID.Slot.1-1",
                "Key": "NonRAID.Slot.1-1",
                "DeviceDescription": "Storage Controller in Slot 1",
                "MaxAvailablePCILinkSpeed": "Not Available",
                "MaxPossiblePCILinkSpeed": "Not Available",
                "PCISlot": "1",
                "PCIVendorID": "1000",
                "PrimaryStatus": "Healthy",
                "ProductName": "Dell HBA355i Adp",
                "RollupStatus": "Healthy",
                "SASAddress": "52CEA7F09B369000",
                "SlicedVDCapability": "Sliced Virtual Disk creation not supported",
                "SupportControllerBootMode": "0",
                "SupportEnhancedAutoForeignImport": "0",
                "SupportRAID10UnevenSpans": "0",
                "SecurityStatus": "Encryption Not Capable",
                "T10PICapability": "0"
            }]
        }
        video_info = IDRACControllerInfo(idrac_mock)
        result = video_info.get_controller_data(resp=mock_response["Members"][0])
        expected_result = {
            "Bus": "Not Available",
            "CacheSize": "8124 MB",
            "CachecadeCapability": "Cachecade Virtual Disk not supported",
            "ControllerFirmwareVersion": "x.x.x.x",
            "DeviceCardDataBusWidth": "4x or x4",
            "DeviceCardManufacturer": "Not Available",
            "DeviceCardSlotLength": "4",
            "DeviceCardSlotType": "PCI Express Gen 4 x8",
            "DeviceDescription": "Not Available",
            "DriverVersion": "Not Available",
            "EncryptionCapability": "None",
            "EncryptionMode": "Not Available",
            "FQDD": "NonRAID.Slot.1-1",
            "Key": "NonRAID.Slot.1-1",
            "MaxAvailablePCILinkSpeed": "Not Available",
            "MaxPossiblePCILinkSpeed": "Not Available",
            "PCISlot": "1",
            "PCIVendorID": "Not Available",
            "PrimaryStatus": "Not Available",
            "ProductName": "Not Available",
            "RollupStatus": "Healthy",
            "SASAddress": "52CEA7F09B369000",
            "SecurityStatus": "Encryption Not Capable",
            "SlicedVDCapability": "Sliced Virtual Disk creation not supported",
            "SupportControllerBootMode": "0",
            "SupportEnhancedAutoForeignImport": "0",
            "SupportRAID10UnevenSpans": "0",
            "T10PICapability": "0"
        }
        assert result == expected_result
