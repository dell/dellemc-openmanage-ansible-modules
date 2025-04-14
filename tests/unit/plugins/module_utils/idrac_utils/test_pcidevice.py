
from ansible_collections.dellemc.openmanage.plugins.\
    module_utils.idrac_utils.info.pcidevice import IDRACPCIDeviceInfo
from ansible_collections.dellemc.openmanage.tests.unit.\
    plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils

pcidevice_link =\
    ["/redfish/v1/Chassis/System.Embedded.1/PCIeDevices/1"]
NA = "Not Available"


class TestIDRACPCIDeviceInfo(TestUtils):
    # def test_get_pcidevice_info(self, idrac_mock):
    #     response = {
    #         "Oem": {
    #             "Dell": {
    #                 "DellPCIeFunction": {
    #                     "SlotLength": "Other",
    #                     "SlotType": "OCPNIC3.0SmallFormFactor",
    #                     "DataBusWidth": "16XOrX16",
    #                     "Id": "NIC.Slot.10-3-1",
    #                     "LastSystemInventoryTime": "2025-04-10T08:19:07+00:00",
    #                     "LastUpdateTime": "2024-11-14T19:13:41+00:00"
    #                     }
    #                 }
    #         }
    #     }
    #     idrac_mock.invoke_request.return_value.json_data = response
    #     idrac_memory_info = IDRACPCIDeviceInfo(idrac_mock)
    #     result = idrac_memory_info.get_device_details(pcidevice_link[0])
    #     expected_result = {
    #             "DataBusWidth": "0002",
    #             "DataBusWidth_API": "Unknown",
    #             "Description": "Integrated Matrox G200eW3 Graphics Controller",
    #             "DeviceDescription": "Integrated Matrox G200eW3 Graphics Controller",
    #             "FQDD": "Video.Embedded.1-1",
    #             "Key": "Video.Embedded.1-1",
    #             "Manufacturer": "Matrox Electronics Systems Ltd.",
    #             "SlotLength": "0002",
    #             "SlotLength_API": "Unknown",
    #             "SlotType": "0002",
    #             "SlotType_API": "Unknown"
    #         }
    #     assert result == expected_result

    def test_get_pcidevice_links(self, idrac_mock):
        links_response = {
            "Members": [
                {
                    "@odata.id": pcidevice_link[0]
                }
            ]
        }
        idrac_mock.invoke_request.return_value.json_data = links_response
        idrac_memory_info = IDRACPCIDeviceInfo(idrac_mock)
        result = idrac_memory_info.get_power_supply_links()
        expected_result = [
            pcidevice_link[0]
        ]
        assert result == expected_result

    def test_get_pcidevice_info_empty(self, idrac_mock):
        links_response = {
            "Members": [
                {
                    "@odata.id": pcidevice_link[0]
                }
            ]
        }
        idrac_mock.invoke_request.return_value.json_data = links_response
        idrac_memory_info = IDRACPCIDeviceInfo(idrac_mock)
        result = idrac_memory_info.get_device_details(links_response)
        expected_result = expected_result = {
            'Description': None,
            'DeviceDescription': None,
            'FQDD': 'Not Available',
            'Key': 'Not Available',
            'Manufacturer': None,
            'SlotLength': 'Not Available',
            'SlotLength_API': 'Not Available',
            'SlotType': 'Not Available',
            'SlotType_API': 'Not Available',
        }
        assert result == expected_result
