from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.sensors_battery import IDRACSensorsBatteryInfo
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils

NA = "Not Available"


class TestIDRACSensorsBatteryInfo(TestUtils):
    def test_get_sensors_battery_info(self, idrac_mock):
        response = {
            "Members": [
                {
                    "ElementName": "System Board CMOS Battery",
                    "Id": "iDRAC.Embedded.1_0x23_SystemBoardCMOSBattery",
                    "HealthState": "OK",
                    "EnabledState": "Enabled",
                    "Name": "DellSensor",
                    "SensorType": "Other",
                    "Description": "An instance of DellSensor",
                    "CurrentState": "Good"
                }
            ]
        }
        idrac_mock.invoke_request.return_value.json_data = response
        idrac_sensors_battery_info = IDRACSensorsBatteryInfo(idrac_mock)
        result = idrac_sensors_battery_info.get_sensors_battery_info()
        expected_result = [
            {
                "CurrentReading": NA,
                "CurrentState": "Good",
                "DeviceID": "iDRAC.Embedded.1_0x23_SystemBoardCMOSBattery",
                "HealthState": "OK",
                "Key": "System Board CMOS Battery",
                "Location": "System Board CMOS Battery",
                "OtherSensorTypeDescription": NA,
                "PrimaryStatus": "Healthy",
                "SensorType": "Other",
                "State": "Enabled"
            }
        ]
        assert result == expected_result
