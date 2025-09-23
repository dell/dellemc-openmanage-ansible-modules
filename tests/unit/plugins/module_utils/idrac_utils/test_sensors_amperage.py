from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.sensor_amperage import IDRACSensorAmperageInfo
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.chassis_sensor_util import IDRACChassisSensors
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils


class TestIDRACSensorAmperageInfo(TestUtils):
    def test_get_sensor_amperage_info(self, idrac_mock):
        response = {
            "Members": [
                {"@odata.id": "/redfish/v1/Chassis/System.Embedded.1/Sensors/PS1Current1"},
                {"@odata.id": "/redfish/v1/Chassis/System.Embedded.1/Sensors/SystemBoardPwrConsumption"}
            ]
        }
        idrac_mock.invoke_request.return_value.json_data = response
        sensors = IDRACChassisSensors(idrac_mock)
        response = {
            "LifetimeReading": 704.729,
            "Status": {
                "State": "Enabled",
                "Health": "OK"
            },
            "@odata.context": "/redfish/v1/$metadata#Sensor.Sensor",
            "ReadingRangeMax": 1794,
            "ReadingType": "Power",
            "Id": "SystemBoardPwrConsumption",
            "SensorResetTime": "2024-11-27T10:51:40-06:00",
            "@odata.type": "#Sensor.v1_10_1.Sensor",
            "ReadingRangeMin": 0,
            "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/Sensors/SystemBoardPwrConsumption",
            "Oem": {
                "Dell": {
                    "RequestedState": "NotApplicable",
                    "@odata.context": "/redfish/v1/$metadata#DellOemSensor.DellOemSensor",
                    "LowestReadings": {
                        "LastHour": {
                            "Reading": 178,
                            "ReadingTime": "2025-08-13T04:37:13-05:00"
                        },
                        "LastWeek": {
                            "Reading": 172,
                            "ReadingTime": "2025-08-13T01:41:19-05:00"
                        },
                        "LastDay": {
                            "ReadingTime": "2025-08-13T01:41:19-05:00",
                            "Reading": 172
                        }
                    },
                    "DeviceID": "iDRAC.Embedded.1#PS1Current1",
                    "PossibleStates@odata.count": 9,
                    "@odata.type": "#DellOemSensor.v1_2_0.DellOemSensor",
                    "AverageReadings": {
                        "LastHour": {
                            "Reading": 182,
                            "AveragingIntervalAchieved": True
                        },
                        "LastWeek": {
                            "AveragingIntervalAchieved": True,
                            "Reading": 183
                        },
                        "LastDay": {
                            "AveragingIntervalAchieved": True,
                            "Reading": 183
                        }
                    },
                    "PossibleStates": [
                        "Unknown",
                        "Fatal",
                        "Normal",
                        "Upper Fatal",
                        "Upper Critical",
                        "Upper Non-Critical",
                        "Lower Non-Critical",
                        "Lower Critical",
                        "Lower Fatal"
                    ],
                    "CurrentState": "Normal",
                    "PeakReadings": {
                        "LastWeek": {
                            "ReadingTime": "2025-08-13T01:05:59-05:00",
                            "Reading": 431
                        },
                        "LastDay": {
                            "Reading": 431,
                            "ReadingTime": "2025-08-13T01:05:59-05:00"
                        },
                        "LastHour": {
                            "ReadingTime": "2025-08-13T04:31:17-05:00",
                            "Reading": 215
                        }
                    }
                }
            },
            "Reading": 181,
            "Name": "PS1 Current 1",
            "Description": "Instance of Sensor Id",
            "ReadingBasis": "Zero",
            "PeakReading": 531,
            "Thresholds": {
                "UpperCaution": {
                    "Reading": 1630
                },
                "UpperCautionUser": {
                    "Reading": 1630
                },
                "UpperCritical": {
                    "Reading": 1794
                },
                "LowerCaution": {
                    "Reading": 0
                },
                "LowerCritical": {
                    "Reading": 0
                }
            },
            "PeakReadingTime": "2025-06-04T09:35:44-05:00",
            "PhysicalContext": "SystemBoard",
            "ReadingUnits": "W",
            "LifetimeStartDateTime": "2024-11-27T10:51:39-06:00",
            "@odata.etag": "W/\"gen-2656\"",
            "Actions": {
                "Oem": {
                    "#DellOemSensor.GetHistoricalSensorReadings": {
                        "ReadingHistoryPeriod@Redfish.AllowableValues": [
                            "LastHour",
                            "LastDay",
                            "LastWeek"
                        ],
                    }
                }
            }
        }
        idrac_mock.invoke_request.return_value.json_data = response
        idrac_sensor_amperage_info = IDRACSensorAmperageInfo(idrac_mock, sensors)
        result = idrac_sensor_amperage_info.get_sensor_amperage_info()
        expected_result = [
            {
                "CurrentReading": 181,
                "CurrentState": "Normal",
                "DeviceID": "iDRAC.Embedded.1#PS1Current1",
                "HealthState": "Normal",
                "Key": "PS1 Current 1",
                "Location": "PS1 Current 1",
                "OtherSensorTypeDescription": "Not Available",
                "PrimaryStatus": "Healthy",
                "ProbeType": "Not Available",
                "SensorType": "Amperage",
                "State": "Enabled"
            },
            {
                "CurrentReading": 181,
                "CurrentState": "Normal",
                "DeviceID": "iDRAC.Embedded.1#PS1Current1",
                "HealthState": "Normal",
                "Key": "PS1 Current 1",
                "Location": "PS1 Current 1",
                "OtherSensorTypeDescription": "Not Available",
                "PrimaryStatus": "Healthy",
                "ProbeType": "Not Available",
                "SensorType": "Amperage",
                "State": "Enabled"
            }

        ]
        assert result == expected_result
