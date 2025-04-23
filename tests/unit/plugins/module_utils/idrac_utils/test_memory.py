from ansible_collections.dellemc.openmanage.tests.unit.plugins.\
    module_utils.idrac_utils.test_idrac_utils import TestUtils
from ansible_collections.dellemc.openmanage.plugins.\
    module_utils.idrac_utils.info.memory import IDRACMemoryInfo

NA = "Not Available"
MEMORY_LINK = [
    "/redfish/v1/Systems/System.Embedded.1/Memory/DIMM.Socket.A1"
]
LINKS_RESPONSE = {
    "Members": [
        {
            "@odata.id": MEMORY_LINK[0]
        }
    ]
}
NOT_AVAILABLE_OUTPUT = {
    "BankLabel": NA,
    "CurrentOperatingSpeed": NA,
    "DeviceDescription": NA,
    "FQDD": NA,
    "Key": NA,
    "ManufactureDate": NA,
    "Manufacturer": NA,
    "MemoryType": NA,
    "MemoryType_API": NA,
    "Model": NA,
    "PartNumber": NA,
    "PrimaryStatus": NA,
    "Rank": NA,
    "SerialNumber": NA,
    "Size": NA,
    "Speed": NA,
    "memoryDeviceStateSettings": NA
}


class TestIDRACMemoryInfo(TestUtils):
    def test_get_memory_info(self, idrac_mock):
        response = {
            "Id": "DIMM.Socket.A1",
            "AllowedSpeedsMHz": [6400],
            "Description": "DeviceDescription",
            "Manufacturer": "Manufacturer",
            "MemoryDeviceType": "DDR5",
            "PartNumber": "PartNumber",
            "Status": {
                "State": "Enabled",
                "Health": "OK"
            },
            "RankCount": 2,
            "SerialNumber": "ABMC",
            "CapacityMiB": 32768,
            "OperatingSpeedMhz": 6400,
            "Oem": {
                "Dell": {
                    "DellMemory": {
                        "ManufactureDate": "Mon Nov 13 06:00:00 2023 UTC",
                        "BankLabel": "A",
                        "Model": "DDR5 DIMM"
                    }
                }
            }
        }
        idrac_mock.invoke_request.return_value.json_data = response
        idrac_memory_info = IDRACMemoryInfo(idrac_mock)
        result = idrac_memory_info.get_memory_details(MEMORY_LINK)
        expected_result = {
            "BankLabel": "A",
            "CurrentOperatingSpeed": "6400.0 MHz",
            "DeviceDescription": "DeviceDescription",
            "FQDD": "DIMM.Socket.A1",
            "Key": "DIMM.Socket.A1",
            "ManufactureDate": "Mon Nov 13 06:00:00 2023 UTC",
            "Manufacturer": "Manufacturer",
            "MemoryType": NA,
            "MemoryType_API": "DDR5",
            "Model": "DDR5 DIMM",
            "PartNumber": "PartNumber",
            "PrimaryStatus": "Healthy",
            "Rank": "Double Rank",
            "SerialNumber": "ABMC",
            "Size": "32.0 GB",
            "Speed": "6.4 GHz",
            "memoryDeviceStateSettings": "Enabled"
        }
        assert result == expected_result

    def test_get_memory_links(self, idrac_mock):
        idrac_mock.invoke_request.return_value.json_data = LINKS_RESPONSE
        idrac_memory_info = IDRACMemoryInfo(idrac_mock)
        result = idrac_memory_info.get_memory_links()
        assert result == MEMORY_LINK

    def test_get_memory_links_empty(self, idrac_mock):
        idrac_mock.invoke_request.return_value.status_code = 400
        idrac_mock.invoke_request.return_value.json_data = LINKS_RESPONSE
        idrac_memory_info = IDRACMemoryInfo(idrac_mock)
        result = idrac_memory_info.get_memory_links()
        assert result == []

    def test_get_memory_details_empty(self, idrac_mock):
        idrac_mock.invoke_request.return_value.status_code = 400
        idrac_mock.invoke_request.return_value.json_data = LINKS_RESPONSE
        idrac_memory_info = IDRACMemoryInfo(idrac_mock)
        result = idrac_memory_info.get_memory_details(LINKS_RESPONSE)
        assert result == {}

    def test_get_memory_info_empty(self, idrac_mock):
        idrac_mock.invoke_request.return_value.json_data = LINKS_RESPONSE
        idrac_memory_info = IDRACMemoryInfo(idrac_mock)
        result = idrac_memory_info.get_memory_info()
        assert result == [NOT_AVAILABLE_OUTPUT]
