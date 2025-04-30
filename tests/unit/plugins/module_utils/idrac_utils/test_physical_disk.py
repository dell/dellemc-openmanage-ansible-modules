from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.physical_disk import IDRACPhysicalDiskInfo
from unittest.mock import MagicMock
NA = "Not Available"
PHYSICAL_DISK_RESPONSE = [
    {
        "BlockSize": "512",
        "BusProtocol": "Not Available",
        "DeviceDescription": "Disk 0 in Backplane 1 of RAID Controller in SL 3",
        "DriveFormFactor": "2.5Inch",
        "FreeSize": "479559942144",
        "HotSpareStatus": "Not Available",
        "Key": "Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.3-1",
        "Manufacturer": "SAMSUNG",
        "ManufacturingDay": "0",
        "ManufacturingWeek": "0",
        "ManufacturingYear": "0",
        "Size": "Not Available",
        "MaxCapableSpeed": "6 Gbps",
        "MediaType": "SSD",
        "Model": "MZ7L3480HCHQAD3",
        "PPID": "KR-0C2C58-SSW00-3BU-01TE-A00",
        "PredictiveFailureState": "SmartAlertAbsent",
        "PrimaryStatus": "Not Available",
        "RAIDNegotiatedSpeed": "None",
        "FQDD": "Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.3-1",
        "RaidStatus": "Ready",
        "RemainingRatedWriteEndurance": "Not Available",
        "Revision": "HJ53",
        "SASAddress": "3F4EE0806EB75A1F",
        "SecurityState": "Not Available",
        "SerialNumber": "S6NANG0WB09554",
        "Slot": "0",
        "SupportedEncryptionTypes": "Not Available",
        "T10PICapability": "NotSupported",
        "UsedSize": "0"
    }
]

expected_result = {
    "BlockSize": "512",
    "BusProtocol": "Not Available",
    "DeviceDescription": "Disk 0 in Backplane 1 of RAID Controller in SL 3",
    "DriveFormFactor": "2.5Inch",
    "FQDD": "Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.3-1",
    "FreeSize": "479559942144",
    "HotSpareStatus": "Not Available",
    "Key": "Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.3-1",
    "Manufacturer": "SAMSUNG",
    "ManufacturingWeek": "0",
    "RaidStatus": "Ready",
    "ManufacturingYear": "0",
    "MaxCapableSpeed": "6 Gbps",
    "MediaType": "SSD",
    "Model": "MZ7L3480HCHQAD3",
    "PPID": "KR-0C2C58-SSW00-3BU-01TE-A00",
    "PredictiveFailureState": "SmartAlertAbsent",
    "PrimaryStatus": "Not Available",
    "RAIDNegotiatedSpeed": "None",
    "RemainingRatedWriteEndurance": "Not Available",
    "Revision": "HJ53",
    "SASAddress": "3F4EE0806EB75A1F",
    "SecurityState": "Not Available",
    "SerialNumber": "S6NANG0WB09554",
    "ManufacturingDay": "0",
    "Size": "Not Available",
    "Slot": "0",
    "SupportedEncryptionTypes": "Not Available",
    "T10PICapability": "NotSupported",
    "UsedSize": "0"
}

drive_response = {
    "BlockSizeBytes": 512,
    "CapableSpeedGbs": 6,
    "CapacityBytes": 479559942144,
    "ConfigurationLock": "Disabled",
    "Description": "Disk 0 in Backplane 1 of RAID Controller in SL 3",
    "EncryptionAbility": "None",
    "EncryptionStatus": "Unencrypted",
    "FailurePredicted": False,
    "HotspareType": "None",
    "Id": "Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.3-1",
    "PCIeFunctions": [],
    "PCIeFunctions@odata.count": 0,
    "Location": [],
    "LocationIndicatorActive": None,
    "Manufacturer": "SAMSUNG",
    "MediaType": "SSD",
    "Model": "MZ7L3480HCHQAD3",
    "Name": "Solid State Disk 0:1:0",
    "NegotiatedSpeedGbs": 6,
    "Oem": {
        "Dell": {
            "DellPhysicalDisk": {
                "@odata.context": "/redfish/v1/$metadata#DellPhysicalDisk.DellPhysicalDisk",
                "@odata.id": "/redfish/v1/Systems/System.Embedded.1/Oem/Dell/DellDrives/Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.3-1",
                "@odata.type": "#DellPhysicalDisk.v1_7_0.DellPhysicalDisk",
                "AvailableSparePercent": None,
                "Certified": "Yes",
                "Connector": 0,
                "CryptographicEraseCapable": "Capable",
                "Description": "An instance of DellPhysicalDisk will have Physical Disk specific data.",
                "DeviceProtocol": None,
                "DeviceSidebandProtocol": None,
                "DriveFormFactor": "2.5Inch",
                "EncryptionProtocol": "None",
                "ErrorDescription": None,
                "ErrorRecoverable": "NotApplicable",
                "ForeignKeyIdentifier": None,
                "FreeSizeInBytes": 479559942144,
                "Id": "Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.3-1",
                "LastSystemInventoryTime": "2025-04-01T11:13:14+00:00",
                "LastUpdateTime": "2025-04-01T11:13:28+00:00",
                "ManufacturingDay": 0,
                "ManufacturingYear": 0,
                "Name": "DellPhysicalDisk",
                "NonRAIDDiskCachePolicy": "Unknown",
                "OperationName": "None",
                "OperationPercentCompletePercent": 0,
                "PCIeCapableLinkWidth": "None",
                "PCIeNegotiatedLinkWidth": "None",
                "PPID": "KR-0C2C58-SSW00-3BU-01TE-A00",
                "ManufacturingWeek": 0,
                "PowerStatus": "On",
                "PredictiveFailureState": "SmartAlertAbsent",
                "ProductID": "MZ7L3480HCHQAD3",
                "RAIDType": "Unknown",
                "RaidStatus": "Ready",
                "SASAddress": "3F4EE0806EB75A1F",
                "Slot": 0,
                "SystemEraseCapability": "CryptographicErasePD",
                "T10PICapability": "NotSupported",
                "UsedSizeInBytes": 0,
                "WWN": "3F4EE0806EB75A1F"
            }
        }
    },
    "Operations": [],
    "Operations@odata.count": 0,
    "PartNumber": "KR-0C2C58-SSW00-3BU-01TE-A00",
    "PhysicalLocation": {
        "PartLocation": {
            "LocationOrdinalValue": 0,
            "LocationType": "Slot"
        }
    },
    "PredictedMediaLifeLeftPercent": 99,
    "Protocol": "SATA",
    "Revision": "HJ53",
    "RotationSpeedRPM": None,
    "SerialNumber": "S6NANG0WB09554",
    "Status": {
        "Health": "OK",
        "HealthRollup": "OK",
        "State": "Enabled"
    },
    "WriteCacheEnabled": True
}


class TestIDRACPhysicalDiskInfo(TestUtils):
    def mock_response(self, json_data, status_code=200):
        mock = MagicMock()
        mock.status_code = status_code
        mock.json_data = json_data
        return mock

    def test_get_idrac_physical_disk_info(self, idrac_mock):
        storage_response = {
            "Members": [
                {
                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1/Storage/RAID.SL.3-1"
                }
            ]
        }
        controller_response = {
            "Drives": [
                {
                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1/Storage/RAID.SL.3-1/Drives/Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.3-1"
                }
            ]
        }
        idrac_mock.invoke_request.side_effect = [
            self.mock_response(storage_response),
            self.mock_response(controller_response),
            self.mock_response(drive_response)
        ]

        physical_disk_info = IDRACPhysicalDiskInfo(idrac_mock)
        result = physical_disk_info.get_physical_disk_info()

        assert result == [expected_result]

    def test_get_idrac_physical_disk_info_empty_storage(self, idrac_mock):
        storage_response = {
            "Members": [
                {
                    "@odata.id": None
                }
            ]
        }
        idrac_mock.invoke_request.side_effect = [
            self.mock_response(storage_response)
        ]

        physical_disk_info = IDRACPhysicalDiskInfo(idrac_mock)
        result = physical_disk_info.get_physical_disk_info()

        expected_result = [
        ]

        assert result == expected_result

    def test_get_idrac_physical_disk_info_empty_drive(self, idrac_mock):
        storage_response = {
            "Members": [
                {
                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1/Storage/RAID.SL.3-1"
                }
            ]
        }
        controller_response = {
            "Drives": [
                {
                    "@odata.id": None
                }
            ]
        }
        idrac_mock.invoke_request.side_effect = [
            self.mock_response(storage_response),
            self.mock_response(controller_response)
        ]

        physical_disk_info = IDRACPhysicalDiskInfo(idrac_mock)
        result = physical_disk_info.get_physical_disk_info()

        assert result == []

    def test_get_physical_disk_mapped_info(self, idrac_mock):
        idrac_physical_disk_info = IDRACPhysicalDiskInfo(idrac_mock)
        result = idrac_physical_disk_info.physical_disk_mapped_data(disk=drive_response)

        assert result == expected_result
