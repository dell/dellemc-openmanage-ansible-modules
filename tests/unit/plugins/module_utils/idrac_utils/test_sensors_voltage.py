from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.sensors_voltage import IDRACSensorsVoltageInfo
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils

NA = "Not Available"


class TestIDRACSensorsVoltageInfo(TestUtils):
    def test_get_sensors_voltage_info(self, idrac_mock):
        response = {
            "Members": [
                {
                    "ElementName": "System Board PS1 PG FAIL",
                    "Id": "iDRAC.Embedded.1_0x23_SystemBoardPS1PGFAIL",
                    "HealthState": "OK",
                    "EnabledState": "Enabled",
                    "Name": "DellSensor",
                    "SensorType": "Voltage",
                    "Description": "An instance of DellSensor",
                    "CurrentState": "No Breach"
                },
                {
                    "ElementName": "System Board PS2 PG FAIL",
                    "Id": "iDRAC.Embedded.1_0x23_SystemBoardPS2PGFAIL",
                    "HealthState": "OK",
                    "EnabledState": "Disabled",
                    "Name": "DellSensor",
                    "SensorType": "Voltage",
                    "Description": "An instance of DellSensor",
                    "CurrentState": "No Breach"
                }
            ]
        }
        idrac_mock.invoke_request.return_value.json_data = response
        idrac_sensors_voltage_info = IDRACSensorsVoltageInfo(idrac_mock)
        result = idrac_sensors_voltage_info.get_sensors_voltage_info()
        expected_result = [
            {
                "CurrentReading": NA,
                "CurrentState": "No Breach",
                "DeviceID": "iDRAC.Embedded.1_0x23_SystemBoardPS1PGFAIL",
                "HealthState": "OK",
                "Key": "System Board PS1 PG FAIL",
                "Location": "System Board PS1 PG FAIL",
                "OtherSensorTypeDescription": NA,
                "PrimaryStatus": "Healthy",
                "SensorType": "Voltage",
                "State": "Enabled",
                "VoltageProbeIndex": NA,
                "VoltageProbeType": NA
            },
            {
                "CurrentReading": NA,
                "CurrentState": "No Breach",
                "DeviceID": "iDRAC.Embedded.1_0x23_SystemBoardPS2PGFAIL",
                "HealthState": "OK",
                "Key": "System Board PS2 PG FAIL",
                "Location": "System Board PS2 PG FAIL",
                "OtherSensorTypeDescription": NA,
                "PrimaryStatus": "Healthy",
                "SensorType": "Voltage",
                "State": "Disabled",
                "VoltageProbeIndex": NA,
                "VoltageProbeType": NA
            }
        ]
        assert result == expected_result
