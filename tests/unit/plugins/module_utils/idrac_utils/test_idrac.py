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

    def test_get_idrac_nic_info(self, idrac_mock):
        manager_response = {
            "Id": "iDRAC.Embedded.1",
            "Status": {
                "Health": "OK"
            }
        }
        attributes_response = {
            "Attributes": {
                "IPv4.1.Address": "xx.xx.xx.xx",
                "IPv6.1.Address1": "xx:xx",
                "NIC.1.Speed": "1 Gbps",
                "NIC.1.Duplex": "Full",
                "NIC.1.MACAddress": "xx:xx:xx:xx",
                "Info.1.Product": "iDRAC9",
                "NIC.1.Enable": "true",
                "NIC.1.SwitchConnection": "Connected",
                "NIC.1.SwitchPortConnection": "Port 1"
            }
        }

        idrac_mock.invoke_request.side_effect = [
            self.mock_response(manager_response),
            self.mock_response(attributes_response)
        ]

        idrac_info = IDRACInfo(idrac_mock)
        result = idrac_info.get_idrac_nic_info()

        expected_result = [{
            "Key": "iDRAC.Embedded.1",
            "FQDD": "iDRAC.Embedded.1",
            "PrimaryStatus": "Healthy",
            "IPv4Address": "xx.xx.xx.xx",
            "IPv6Address": "xx:xx",
            "NICSpeed": "1 Gbps",
            "NICDuplex": "Full",
            "PermanentMACAddress": "xx:xx:xx:xx",
            "ProductInfo": "iDRAC9",
            "GroupName": NOT_AVAILABLE,
            "GroupStatus": NOT_AVAILABLE,
            "NICEnabled": "true",
            "SwitchConnection": "Connected",
            "SwitchPortConnection": "Port 1"
        }]

        assert result == expected_result
