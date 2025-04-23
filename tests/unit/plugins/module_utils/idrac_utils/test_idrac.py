from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.idrac import IDRACInfo
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils
from unittest.mock import MagicMock

NOT_AVAILABLE = "Not Available"


class TestIDRACInfo(TestUtils):
    def mock_response(self, json_data, status_code=200):
        mock = MagicMock()
        mock.status_code = status_code
        mock.json_data = json_data
        return mock

    def test_get_idrac_system_details(self, idrac_mock):
        mock_response = {
            "Model": "PowerEdge R770"
        }
        idrac_mock.invoke_request.return_value.json_data = mock_response
        idrac_info = IDRACInfo(idrac_mock)
        idrac_info.get_idrac_system_details()
        assert idrac_info.idrac_data["Model"] == "PowerEdge R770"

    def test_get_idrac_details(self, idrac_mock):
        mock_response = {
            "smbiosGUID": "44454c4c-3400-1030-8035-d7c04f313035"
        }
        idrac_mock.invoke_request.return_value.json_data = mock_response
        idrac_info = IDRACInfo(idrac_mock)
        idrac_info.get_idrac_details()
        assert idrac_info.idrac_data["GUID"] == "44454c4c-3400-1030-8035-d7c04f313035"

    def test_get_idrac_manager_details(self, idrac_mock):
        mock_response = {
            "FirmwareVersion": "x.x.x.x",
            "Oem": {
                "Dell": {
                    "DelliDRACCard": {
                        "URLString": "https://x.x.x.x:443",
                    }
                }
            },
            "Id": "iDRAC.Embedded.1"
        }
        idrac_mock.invoke_request.return_value.json_data = mock_response
        idrac_info = IDRACInfo(idrac_mock)
        idrac_info.get_idrac_manager_details()
        assert idrac_info.idrac_data["FirmwareVersion"] == "x.x.x.x"
        assert idrac_info.idrac_data["URLString"] == "https://x.x.x.x:443"
        assert idrac_info.idrac_data["Key"] == "iDRAC.Embedded.1"
        assert idrac_info.idrac_data["FQDD"] == "iDRAC.Embedded.1"

    def test_get_idrac_attributes_details(self, idrac_mock):
        mock_response = {
            "Description": "This schema provides the oem attributes",
            "AttributeRegistry": "ManagerAttributeRegistry.v1_0_0",
            "Id": "iDRAC.Embedded.1",
            "Name": "OEMAttributeRegistry",
            "Attributes": {
                "Lockdown.1.SystemLockdown": "Disabled",
                "Info.1.Product": "Integrated Dell Remote Access Controller",
                "Info.1.Description": "This system component provides a complete set of remote management functions for Dell PowerEdge Servers",
                "NIC.1.Speed": "1000",
                "NIC.1.Duplex": "Full",
                "NIC.1.DNSDomainName": "laas.adc.delllabs.net",
                "Network.1.DNSRacName": "idrac-W405105",
                "IPv4.1.Address": "x.x.x.x",
                "IPv6.1.Address1": "::",
                "Users.1.SolEnable": 0,
                "IPMILan.1.Enable": 0,
                "Info.1.IPMIVersion": "2.0",
                "NIC.1.MACAddress": "6c:3c:8c:8c:6c:7e"
            }
        }
        idrac_mock.invoke_request.return_value.json_data = mock_response
        idrac_info = IDRACInfo(idrac_mock)
        idrac_info.get_idrac_attributes_details()
        assert idrac_info.idrac_data["DNSDomainName"] == "laas.adc.delllabs.net"
        assert idrac_info.idrac_data["DNSRacName"] == "idrac-W405105"
        assert idrac_info.idrac_data["DeviceDescription"] == "iDRAC"
        assert idrac_info.idrac_data["GroupName"] == "Not Available"
        assert idrac_info.idrac_data["GroupStatus"] == "Not Available"
        assert idrac_info.idrac_data["IPMIVersion"] == "2.0"
        assert idrac_info.idrac_data["IPv4Address"] == "x.x.x.x"
        assert idrac_info.idrac_data["IPv6Address"] == "::"
        assert idrac_info.idrac_data["LANEnabledState"] == 0
        assert idrac_info.idrac_data["MACAddress"] == "6c:3c:8c:8c:6c:7e"
        assert idrac_info.idrac_data["NICDuplex"] == "Full"
        assert idrac_info.idrac_data["NICSpeed"] == "1000"
        assert idrac_info.idrac_data["PermanentMACAddress"] == "6c:3c:8c:8c:6c:7e"
        assert idrac_info.idrac_data["ProductDescription"] == \
            "This system component provides a complete set of remote management functions for Dell PowerEdge Servers"
        assert idrac_info.idrac_data["ProductInfo"] == "Integrated Dell Remote Access Controller"
        assert idrac_info.idrac_data["SOLEnabledState"] == 0
        assert idrac_info.idrac_data["SystemLockDown"] == "Disabled"

    def test_get_subsystem_info(self, idrac_mock):
        idrac_system_details = {
            "Model": "PowerEdge R770"
        }
        idrac_details = {
            "GUID": "44454c4c-3400-1030-8035-d7c04f313035",
            "Model": "PowerEdge R770"
        }
        idrac_manager_details = {
            "FirmwareVersion": "x.x.x.x",
            "URLString": "https://x.x.x.x:443",
            "Key": "iDRAC.Embedded.1",
            "FQDD": "iDRAC.Embedded.1",
            "GUID": "44454c4c-3400-1030-8035-d7c04f313035",
            "Model": "PowerEdge R770"
        }
        idrac_attributes_details = {
            "DNSDomainName": "laas.adc.delllabs.net",
            "DNSRacName": "idrac-W405105",
            "DeviceDescription": "iDRAC",
            "FQDD": "iDRAC.Embedded.1",
            "FirmwareVersion": "x.x.x.x",
            "GUID": "44454c4c-3400-1030-8035-d7c04f313035",
            "GroupName": "Not Available",
            "GroupStatus": "Not Available",
            "IPMIVersion": "2.0",
            "IPv4Address": "x.x.x.x",
            "IPv6Address": "::",
            "Key": "iDRAC.Embedded.1",
            "LANEnabledState": 0,
            "MACAddress": "6c:3c:8c:8c:6c:7e",
            "Model": "PowerEdge R770",
            "NICDuplex": "Full",
            "NICSpeed": "1000",
            "PermanentMACAddress": "6c:3c:8c:8c:6c:7e",
            "ProductDescription": "This system component provides a complete set of remote management functions for Dell PowerEdge Servers",
            "ProductInfo": "Integrated Dell Remote Access Controller",
            "SOLEnabledState": 0,
            "SystemLockDown": "Disabled",
            "URLString": "https://x.x.x.x:443"
        }
        idrac_info = IDRACInfo(idrac_mock)
        idrac_info.get_idrac_details = MagicMock(
            return_value=idrac_details)
        idrac_info.get_idrac_system_details = MagicMock(
            return_value=idrac_system_details)
        idrac_info.get_idrac_manager_details = MagicMock(
            return_value=idrac_manager_details)
        idrac_info.get_idrac_attributes_details = MagicMock(
            return_value=idrac_attributes_details
        )
        result = idrac_info.get_idrac_info_details()
        expected_result = [
            {
                "DNSDomainName": "laas.adc.delllabs.net",
                "DNSRacName": "idrac-W405105",
                "DeviceDescription": "iDRAC",
                "FQDD": "iDRAC.Embedded.1",
                "FirmwareVersion": "x.x.x.x",
                "GUID": "44454c4c-3400-1030-8035-d7c04f313035",
                "GroupName": "Not Available",
                "GroupStatus": "Not Available",
                "IPMIVersion": "2.0",
                "IPv4Address": "x.x.x.x",
                "IPv6Address": "::",
                "Key": "iDRAC.Embedded.1",
                "LANEnabledState": 0,
                "MACAddress": "6c:3c:8c:8c:6c:7e",
                "Model": "PowerEdge R770",
                "NICDuplex": "Full",
                "NICSpeed": "1000",
                "PermanentMACAddress": "6c:3c:8c:8c:6c:7e",
                "ProductDescription": "This system component provides a complete set of remote management functions for Dell PowerEdge Servers",
                "ProductInfo": "Integrated Dell Remote Access Controller",
                "SOLEnabledState": 0,
                "SystemLockDown": "Disabled",
                "URLString": "https://x.x.x.x:443"
            }
        ]
        assert result == expected_result
