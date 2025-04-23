
from ansible_collections.dellemc.openmanage.plugins.\
    module_utils.idrac_utils.info.video import IDRACVideoInfo
from ansible_collections.dellemc.openmanage.tests.unit.\
    plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils
from unittest.mock import MagicMock


class TestIDRACVideoInfo(TestUtils):
    def test_get_video_info(self, idrac_mock):
        mock_response = {
            "Members": [{
                "Description": "Integrated Matrox G200eW3 Graphics Controller",
                "DeviceDescription": "Embedded Video Controller 1",
                "FQDD": "Video.Embedded.1-1",
                "Key": "Video.Embedded.1-1",
                "Manufacturer": "Matrox Electronics Systems Ltd."
            }]
        }
        idrac_mock.invoke_request.return_value.json_data = mock_response
        video_info = IDRACVideoInfo(idrac_mock)
        video_info.extract_video_data = MagicMock(
            return_value=mock_response["Members"])
        result = video_info.get_idrac_video_details()
        expected_result = [
            {
                "Description": "Integrated Matrox G200eW3 Graphics Controller",
                "DeviceDescription": "Embedded Video Controller 1",
                "FQDD": "Video.Embedded.1-1",
                "Key": "Video.Embedded.1-1",
                "Manufacturer": "Matrox Electronics Systems Ltd."
            }
        ]
        assert result == expected_result

    def test_extract_video_info(self, idrac_mock):
        mock_response = {
            "Members": [
                {
                    "Description": "Integrated Matrox G200eW3 Graphics Controller",
                    "DeviceDescription": "Embedded Video Controller 1",
                    "FQDD": "Video.Embedded.1-1",
                    "Key": "Video.Embedded.1-1",
                    "Manufacturer": "Matrox Electronics Systems Ltd."
                }
            ]
        }
        video_info = IDRACVideoInfo(idrac_mock)
        result = video_info.extract_video_data(response=mock_response)
        expected_result = [
            {
                "Description": "Integrated Matrox G200eW3 Graphics Controller",
                "DeviceDescription": "Embedded Video Controller 1",
                "FQDD": "Video.Embedded.1-1",
                "Key": "Video.Embedded.1-1",
                "Manufacturer": "Matrox Electronics Systems Ltd."
            }
        ]
        assert result == expected_result
