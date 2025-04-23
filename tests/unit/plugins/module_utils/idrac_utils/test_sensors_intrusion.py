from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.sensors_intrusion import IDRACSensorsIntrusionInfo
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils

NA = "Not Available"


class TestIDRACSensorsIntrusionInfo(TestUtils):
    def test_get_sensors_intrusion_info(self, idrac_mock):
        response = {
            "Members": [
                {
                    "ElementName": "System Board Intrusion",
                    "Id": "iDRAC.Embedded.1_0x23_SystemBoardIntrusion",
                    "HealthState": "OK",
                    "EnabledState": "Enabled",
                    "Name": "DellSensor",
                    "SensorType": "Intrusion",
                    "Description": "An instance of DellSensor",
                    "CurrentState": "No Breach"
                }
            ]
        }
        idrac_mock.invoke_request.return_value.json_data = response
        idrac_sensors_intrusion_info = IDRACSensorsIntrusionInfo(idrac_mock)
        result = idrac_sensors_intrusion_info.get_sensors_intrusion_info()
        expected_result = [
            {
                "CurrentReading": NA,
                "CurrentState": "No Breach",
                "DeviceID": "iDRAC.Embedded.1_0x23_SystemBoardIntrusion",
                "HealthState": "OK",
                "Key": "System Board Intrusion",
                "Location": "System Board Intrusion",
                "OtherSensorTypeDescription": NA,
                "PrimaryStatus": "Healthy",
                "SensorType": "Intrusion",
                "State": "Enabled",
                "Type": NA
            }
        ]
        assert result == expected_result
