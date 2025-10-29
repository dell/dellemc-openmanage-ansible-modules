import pytest
from unittest.mock import MagicMock
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.fc import IDRACFCInfo

NA = "Not Available"


class TestIDRACFCInfo:

    @pytest.fixture
    def idrac_mock(self):
        return MagicMock()

    @pytest.fixture
    def fc_info(self, idrac_mock):
        return IDRACFCInfo(idrac_mock)

    def test_get_fc_capability_details_non_200(self, fc_info, idrac_mock):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json_data = {}  # Optional: for safety
        idrac_mock.invoke_request.return_value = mock_response

        result = fc_info.get_fc_capability_details("FC1")
        assert result == ("", "", "", "", "", "", "")

    def test_get_fc_port_metrics_details_non_200(self, fc_info, idrac_mock):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json_data = {}
        idrac_mock.invoke_request.return_value = mock_response

        result = fc_info.get_fc_port_metrics_details("FC1")
        assert result == ("", "", "", "", "", "", "", "", "", "", {})

    def test_get_fc_statistics_details_non_200(self, fc_info, idrac_mock):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json_data = {}
        idrac_mock.invoke_request.return_value = mock_response

        result = fc_info.get_fc_statistics_details("FC1")
        assert result == ""

    def test_get_fc_info_success(self, fc_info, idrac_mock):
        idrac_mock.invoke_request.side_effect = [
            MagicMock(status_code=200, json_data={
                "Members": [
                    {
                        "Id": "FC1",
                        "DeviceName": "FC Adapter",
                        "VendorName": "Dell",
                        "ProductName": "Dell FC Card",
                        "PortStatus": "Up",
                        "FCTxTotalFrames": 1000,
                        "FCRxTotalFrames": 900,
                        "OSDriverState": "Running"
                    }
                ]
            }),

            MagicMock(status_code=200, json_data={
                "Members": [
                    {
                        "Id": "FC1",
                        "FeatureLicensingSupport": "Supported",
                        "uEFISupport": "Supported",
                        "FlexAddressingSupport": "Supported",
                        "OnChipThermalSensor": "Yes",
                        "FCMaxNumberExchanges": 128,
                        "FCMaxNumberOutStandingCommands": 64,
                        "PersistencePolicySupport": "Supported"
                    }
                ]
            }),

            MagicMock(status_code=200, json_data={
                "Members": [
                    {
                        "Id": "FC1",
                        "OSDriverState": "Running",
                        "FCTxTotalFrames": 1000,
                        "FCRxTotalFrames": 900,
                        "FCTxSequences": 50,
                        "FCRxSequences": 45,
                        "FCTxKBCount": 2048,
                        "FCRxKBCount": 1024,
                        "FCInvalidCRCs": 0,
                        "FCLossOfSignals": 0,
                        "FCLinkFailures": 0,
                        "Oem": {}
                    }
                ]
            }),

            MagicMock(status_code=200, json_data={
                "Members": [
                    {
                        "Id": "FC1",
                        "PortStatus": "Up"
                    }
                ]
            })
        ]

        result = fc_info.get_fc_info()

        assert result[0]["Id"] == "FC1"
        assert result[0]["PortStatus"] == "Up"
        assert result[0]["FCTxTotalFrames"] == 1000
        assert result[0]["FCRxTotalFrames"] == 900
        assert result[0]["OSDriverState"] == "Running"

    def test_get_fc_info_non_200(self):
        mock_idrac = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_idrac.invoke_request.return_value = mock_response

        fc_info = IDRACFCInfo(mock_idrac)
        result = fc_info.get_fc_info()
        assert result is None

    def test_get_fc_capability_details_match(self, fc_info, idrac_mock):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json_data = {
            "Members": [
                {
                    "Id": "FC1",
                    "FeatureLicensingSupport": "Supported",
                    "uEFISupport": "Enabled",
                    "FlexAddressingSupport": "Yes",
                    "OnChipThermalSensor": "Present",
                    "FCMaxNumberExchanges": 128,
                    "FCMaxNumberOutStandingCommands": 64,
                    "PersistencePolicySupport": "True"
                }
            ]
        }
        idrac_mock.invoke_request.return_value = mock_response

        result = fc_info.get_fc_capability_details("FC1")

        assert result == (
            "Supported", "Enabled", "Yes", "Present", 128, 64, "True"
        )

    def test_get_fc_port_metrics_details_oem_not_dict(self, fc_info, idrac_mock):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json_data = {
            "Members": [
                {
                    "Id": "FC1",
                    "OSDriverState": "Running",
                    "FCTxTotalFrames": 100,
                    "FCRxTotalFrames": 90,
                    "FCTxSequences": 10,
                    "FCRxSequences": 9,
                    "FCTxKBCount": 2048,
                    "FCRxKBCount": 1024,
                    "FCInvalidCRCs": 0,
                    "FCLossOfSignals": 0,
                    "FCLinkFailures": 0,
                    "Oem": "InvalidString"
                }
            ]
        }
        idrac_mock.invoke_request.return_value = mock_response

        result = fc_info.get_fc_port_metrics_details("FC1")
        # last element should be {}, not string
        assert result[-1] == {}

    def test_get_fc_statistics_details_match(self, fc_info, idrac_mock):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json_data = {
            "Members": [
                {"Id": "FC1", "PortStatus": "Up"}
            ]
        }
        idrac_mock.invoke_request.return_value = mock_response

        result = fc_info.get_fc_statistics_details("FC1")
        assert result == "Up"

    def test_get_fc_statistics_details_no_match(self, fc_info, idrac_mock):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json_data = {
            "Members": [
                {"Id": "FC2", "PortStatus": "Down"}
            ]
        }
        idrac_mock.invoke_request.return_value = mock_response

        result = fc_info.get_fc_statistics_details("FC1")
        assert result == ""
