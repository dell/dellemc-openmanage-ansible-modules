import pytest
from unittest.mock import MagicMock
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.nic import IDRACNICInfo

NA = "Not Available"


class TestIDRACNICInfo:

    @pytest.fixture
    def idrac_mock(self):
        return MagicMock()

    @pytest.fixture
    def nic_info(self, idrac_mock):
        return IDRACNICInfo(idrac_mock)

    def test_get_nic_capability_details_non_200(self, nic_info, idrac_mock):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json_data = {}  # Optional: for safety
        idrac_mock.invoke_request.return_value = mock_response

        result = nic_info.get_nic_capability_details("NIC1")
        assert result == ("", "", "", "", "", "", "", "", "", "")

    def test_get_nic_port_metrics_details_non_200(self, nic_info, idrac_mock):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json_data = {}
        idrac_mock.invoke_request.return_value = mock_response

        result = nic_info.get_nic_port_metrics_details("NIC1")
        assert result == ""

    def test_get_nic_statistics_details_non_200(self, nic_info, idrac_mock):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json_data = {}
        idrac_mock.invoke_request.return_value = mock_response

        result = nic_info.get_nic_statistics_details("NIC1")
        assert result == ("", "", "", "", "", "")

    def test_get_ethernet_details_initial_non_200(self, nic_info, idrac_mock):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json_data = {}
        idrac_mock.invoke_request.return_value = mock_response

        result = nic_info.get_ethernet_details()
        assert result == ("", "", "", "", "")

    def test_get_nic_info_success(self, nic_info, idrac_mock):

        idrac_mock.invoke_request.side_effect = [
            MagicMock(status_code=200, json_data={
                "Members": [
                    {
                        "Id": "NIC1",
                        "ControllerBIOSVersion": "1.0.0",
                        "DataBusWidth": "64",
                        "Description": "NIC",
                        "EFIVersion": "2.0",
                        "FCoEOffloadMode": "Enabled",
                        "FCoEWWNN": "5001f1a",
                        "FamilyVersion": "X550",
                        "IPv4Addresses": [{"Address": "x.x.x.x"}],
                        "IPv6Addresses": [{"Address": "fexx::abxx"}],
                        "LinkDuplex": "Full",
                        "MaxBandwidthPercent": 100,
                        "MediaType": "Ethernet",
                        "NICCapabilities": ["PXE", "iSCSI"],
                        "NicMode": "Shared",
                        "PermanentFCOEMACAddress": "00:11:22:33:44:55",
                        "PermanentiSCSIMACAddress": "00:11:22:33:44:66",
                        "ProductName": "Broadcom NetXtreme",
                        "Protocol": "Ethernet",
                        "SupportedBootProtocol": ["PXE"],
                        "SwitchConnectionID": "1",
                        "SwitchPortConnectionID": "A1",
                        "VFSRIOVSupport": True,
                        "VendorName": "Broadcom",
                        "VirtWWN": "5001f1b",
                        "VirtWWPN": "5001f1c",
                        "WWN": "5001f1d",
                        "WWPN": "5001f1e",
                        "iScsiOffloadMode": "Enabled"
                    }
                ]
            }),

            MagicMock(status_code=200, json_data={
                "Members": [
                    {
                        "Id": "NIC1",
                        "DCBExchangeProtocol": "Enabled",
                        "FCoEBootSupport": "Enabled",
                        "FCoEOffloadSupport": "Enabled",
                        "FlexAddressingSupport": "Supported",
                        "NicPartitioningSupport": "Supported",
                        "PXEBootSupport": "Enabled",
                        "TCPChimneySupport": "Disabled",
                        "PartitionWOLSupport": "Supported",
                        "iSCSIBootSupport": "Enabled",
                        "iSCSIOffloadSupport": "Enabled"
                    }
                ]
            }),

            MagicMock(status_code=200, json_data={
                "Members": [
                    {"Id": "NIC1", "PartitionLinkStatus": "Up"}
                ]
            }),

            MagicMock(status_code=200, json_data={
                "Members": [{"@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/EthernetInterfaces/NIC1"}]
            }),

            MagicMock(status_code=200, json_data={
                "MACAddress": "xx:xx:xx",
                "SpeedMbps": 1000,
                "AutoNeg": True,
                "PermanentMACAddress": "aa:bb:cc:dd",
                "Status": {"Health": "OK"}
            }),

            MagicMock(status_code=200, json_data={
                "Members": [
                    {
                        "Id": "NIC1",
                        "RxBytes": 123456,
                        "RxMutlicastPackets": 10,
                        "RxUnicastPackets": 200,
                        "TxBytes": 654321,
                        "TxMutlicastPackets": 15,
                        "TxUnicastPackets": 300
                    }
                ]
            })
        ]

        result = nic_info.get_nic_info()

        assert result[0]["FQDD"] == "NIC1"
        assert result[0]["CurrentMACAddress"] == "xx:xx:xx"
        assert result[0]["RxBytes"] == 123456
        assert result[0]["TxBytes"] == 654321
        assert result[0]["PXEBootSupport"] == "Enabled"
        assert result[0]["PrimaryStatus"] == "Healthy"

    def test_get_nic_info_non_200(self):
        mock_idrac = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_idrac.invoke_request.return_value = mock_response

        nic_info = IDRACNICInfo(mock_idrac)
        result = nic_info.get_nic_info()
        assert result is None
