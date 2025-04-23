
from ansible_collections.dellemc.openmanage.plugins.\
    module_utils.idrac_utils.info.pcidevice import IDRACPCIDeviceInfo
from ansible_collections.dellemc.openmanage.tests.unit.\
    plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils
from unittest.mock import MagicMock
pcidevice_link =\
    ["/redfish/v1/Chassis/System.Embedded.1/PCIeDevices/1"]
NA = "Not Available"


class TestIDRACPCIDeviceInfo(TestUtils):
    def test_get_pcidevice_info(self, idrac_mock):
        pci_device_info = IDRACPCIDeviceInfo(idrac_mock)
        pci_device_info.get_device_links = MagicMock(
            return_value=pcidevice_link)
        pci_device_info.get_device_details = MagicMock(
            return_value={})
        result = pci_device_info.get_pcidevice_info()
        assert result == []

    def test_get_device_function_details(self, idrac_mock):
        mock_response = {
            "Oem": {
                "Dell": {
                    "DellPCIeFunction": {
                        "SlotLength": "Other",
                        "SlotType": "OCPNIC3.0SmallFormFactor",
                        "DataBusWidth": "16XOrX16",
                        "Id": "NIC.Slot.10-3-1"
                    }
                }
            }
        }
        idrac_mock.invoke_request.return_value.json_data = mock_response
        pci_device_info = IDRACPCIDeviceInfo(idrac_mock)
        buswidth, buswidth_api, deviceid, slot_type, \
            slot_type_api, slot_length, slot_length_api = \
            pci_device_info.get_device_function_details(pcidevice_link)
        assert buswidth == "000D"
        assert buswidth_api == "16XOrX16"
        assert deviceid == "NIC.Slot.10-3-1"
        assert slot_type == NA
        assert slot_type_api == "OCPNIC3.0SmallFormFactor"
        assert slot_length == '0001'
        assert slot_length_api == "Other"

    def test_get_device_function_details_empty(self, idrac_mock):
        mock_response = {}
        idrac_mock.invoke_request.return_value.status_code = 400
        idrac_mock.invoke_request.return_value.json_data = mock_response
        pci_device_info = IDRACPCIDeviceInfo(idrac_mock)
        buswidth, buswidth_api, deviceid, slot_type, \
            slot_type_api, slot_length, slot_length_api = \
            pci_device_info.get_device_function_details(pcidevice_link)
        assert buswidth == NA
        assert buswidth_api == NA
        assert deviceid == NA
        assert slot_type == NA
        assert slot_type_api == NA
        assert slot_length == NA
        assert slot_length_api == NA

    def test_get_device_details(self, idrac_mock):
        mock_response = {
            "Links": {
                "PCIeFunctions": [
                    {
                        "@odata.id": "/some/link"
                    }
                ]
            }
        }
        idrac_mock.invoke_request.return_value.json_data = mock_response
        pci_device_info = IDRACPCIDeviceInfo(idrac_mock)

        buswidth = "buswidth"
        buswidth_api = "buswidth_api"
        deviceid = "deviceid"
        slot_type = "slot_type"
        slot_type_api = "slot_type_api"
        slot_length = "slot_length"
        slot_length_api = "slot_length_api"
        pci_device_info.get_device_function_details = MagicMock(
            return_value=(buswidth, buswidth_api, deviceid, slot_type,
                          slot_type_api, slot_length, slot_length_api))
        result = pci_device_info.get_device_details(pcidevice_link)
        assert result[0]["DataBusWidth"] == buswidth
        assert result[0]["DataBusWidth_API"] == buswidth_api
        assert result[0]["FQDD"] == deviceid
        assert result[0]["Key"] == deviceid
        assert result[0]["SlotType"] == slot_type
        assert result[0]["SlotType_API"] == slot_type_api
        assert result[0]["SlotLength"] == slot_length
        assert result[0]["SlotLength_API"] == slot_length_api

    def test_get_device_details_empty(self, idrac_mock):
        mock_response = {}
        idrac_mock.invoke_request.return_value.status_code = 400
        idrac_mock.invoke_request.return_value.json_data = mock_response
        pci_device_info = IDRACPCIDeviceInfo(idrac_mock)
        result = pci_device_info.get_device_details(pcidevice_link)
        assert result == []

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
        result = idrac_memory_info.get_device_links()
        expected_result = [
            pcidevice_link[0]
        ]
        assert result == expected_result

    def test_get_pcidevice_links_empty(self, idrac_mock):
        links_response = {}
        idrac_mock.invoke_request.return_value.status_code = 400
        idrac_mock.invoke_request.return_value.json_data = links_response
        idrac_memory_info = IDRACPCIDeviceInfo(idrac_mock)
        result = idrac_memory_info.get_device_links()
        assert result == []

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
        expected_result = [{
            'Description': None,
            'DeviceDescription': None,
            'FQDD': 'Not Available',
            'Key': 'Not Available',
            'Manufacturer': None,
            'SlotLength': 'Not Available',
            'SlotLength_API': 'Not Available',
            'SlotType': 'Not Available',
            'SlotType_API': 'Not Available',
            'DataBusWidth': 'Not Available',
            'DataBusWidth_API': 'Not Available'
        }]
        assert result == expected_result
