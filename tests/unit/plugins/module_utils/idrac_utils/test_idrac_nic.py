
from ansible_collections.dellemc.openmanage.plugins.\
    module_utils.idrac_utils.info.idrac import IDRACInfo
from ansible_collections.dellemc.openmanage.tests.unit.\
    plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils
from unittest.mock import MagicMock


class TestIDRACInfo(TestUtils):
    def test_get_idrac_nic_info(self, idrac_mock):
        mock_response = {
            "PowerState": "On",
            "ManagerType": "BMC",
            "Id": "iDRAC.Embedded.1",
            "Status": {
                "State": "Enabled",
                "Health": "OK"
            }
        }
        attributes_mock_response = {
            "FQDD": "iDRAC.Embedded.1",
            "GroupName": "Not Available",
            "GroupStatus": "Not Available",
            "IPv4Address": "x.x.x.x",
            "IPv6Address": "::",
            "Key": "iDRAC.Embedded.1",
            "NICDuplex": "Full",
            "NICEnabled": "Enabled",
            "NICSpeed": "1000",
            "PermanentMACAddress": "6c:3c:8c:8c:6c:7e",
            "PrimaryStatus": "Healthy",
            "ProductInfo": "Integrated Dell Remote Access Controller",
            "SwitchConnection": "0c:29:ef:ba:2f:a0",
            "SwitchPortConnection": "ethernet1/1/17"
        }
        idrac_mock.invoke_request.return_value.json_data = mock_response
        idrac_nic_info = IDRACInfo(idrac_mock)
        idrac_nic_info.get_idrac_nic_attributes = MagicMock(
            return_value=attributes_mock_response)
        result = idrac_nic_info.get_idrac_nic_info()
        expected_result = [{
            "FQDD": "iDRAC.Embedded.1",
            "GroupName": "Not Available",
            "GroupStatus": "Not Available",
            "IPv4Address": "x.x.x.x",
            "IPv6Address": "::",
            "Key": "iDRAC.Embedded.1",
            "NICDuplex": "Full",
            "NICEnabled": "Enabled",
            "NICSpeed": "1000",
            "PermanentMACAddress": "6c:3c:8c:8c:6c:7e",
            "PrimaryStatus": "Healthy",
            "ProductInfo": "Integrated Dell Remote Access Controller",
            "SwitchConnection": "0c:29:ef:ba:2f:a0",
            "SwitchPortConnection": "ethernet1/1/17"
        }]
        assert result == expected_result

    def test_extract_idrac_nic_attributes_info(self, idrac_mock):
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
                "NIC.1.MACAddress": "6c:3c:8c:8c:6c:7e",
                "IPv4.1.Address": "x.x.x.x",
                "IPv6.1.Address1": "::",
                "Users.1.SolEnable": "Disabled",
                "IPMILan.1.Enable": "Disabled",
                "Info.1.IPMIVersion": "2.0",
                "NIC.1.Enable": "Enabled",
                "NIC.1.SwitchConnection": "0c:29:ef:ba:2f:a0",
                "NIC.1.SwitchPortConnection": "ethernet1/1/17",
                "status_code": 200
            }
        }
        response = {
            "FQDD": "iDRAC.Embedded.1",
            "Key": "iDRAC.Embedded.1",
            "PrimaryStatus": "Healthy"
        }
        idrac_mock.invoke_request.return_value.json_data = mock_response
        idrac_nic_info = IDRACInfo(idrac_mock)
        result = idrac_nic_info.get_idrac_nic_attributes(output=response)
        expected_result = {
            "FQDD": "iDRAC.Embedded.1",
            "GroupName": "Not Available",
            "GroupStatus": "Not Available",
            "IPv4Address": "x.x.x.x",
            "IPv6Address": "::",
            "Key": "iDRAC.Embedded.1",
            "NICDuplex": "Full",
            "NICEnabled": "Enabled",
            "NICSpeed": "1000",
            "PermanentMACAddress": "6c:3c:8c:8c:6c:7e",
            "PrimaryStatus": "Healthy",
            "ProductInfo": "Integrated Dell Remote Access Controller",
            "SwitchConnection": "0c:29:ef:ba:2f:a0",
            "SwitchPortConnection": "ethernet1/1/17"
        }
        assert result == expected_result
