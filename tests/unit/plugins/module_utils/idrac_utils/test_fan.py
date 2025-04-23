from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.fan import IDRACFanInfo
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils


class TestIDRACFanInfo(TestUtils):
    def test_get_fan_info(self, idrac_mock):
        response = {
            "Members": [
                {
                    "HotPluggable": "true",
                    "SpeedPercent": {
                        "SpeedRPM": 14120
                    },
                    "Name": "Fan2A",
                    "Id": "CoolingController.1.Fan2A",
                    "Location": {
                        "PartLocation": {
                            "LocationOrdinalValue": 1,
                            "LocationType": "Slot"
                        }
                    },
                    "Oem": {
                        "Dell": {
                            "FanPWM": 50
                        }
                    },
                    "Status": {
                        "Health": "OK"
                    },
                    "State": "Not Available",
                    # "VariableSpeed": "true"
                },
                {
                    "HotPluggable": "true",
                    "SpeedPercent": {
                        "SpeedRPM": 14100
                    },
                    "Name": "Fan2B",
                    "Id": "CoolingController.1.Fan2B",
                    "Location": {
                        "PartLocation": {
                            "LocationOrdinalValue": 2,
                            "LocationType": "Slot"
                        }
                    },
                    "Oem": {
                        "Dell": {
                            "FanPWM": 80
                        }
                    },
                    "Status": {
                        "Health": "OK"
                    },
                    "State": "Not Available",
                    # "VariableSpeed": "true"
                },
            ]
        }
        idrac_mock.invoke_request.return_value.json_data = response
        idrac_fan_info = IDRACFanInfo(idrac_mock)
        result = idrac_fan_info.get_fan_info()
        expected_result = [
            {
                "ActiveCooling": "true",
                "CurrentReading": 14120,
                "DeviceDescription": "Fan2A",
                "FQDD": "CoolingController.1.Fan2A",
                "Key": "CoolingController.1.Fan2A",
                "Location": {
                    "PartLocation": {
                        "LocationOrdinalValue": 1,
                        "LocationType": "Slot"
                    }
                },
                "PWM": 50,
                "PrimaryStatus": "Healthy",
                "State": "Not Available",
                "VariableSpeed": "true"
            },
            {
                "ActiveCooling": "true",
                "CurrentReading": 14100,
                "DeviceDescription": "Fan2B",
                "FQDD": "CoolingController.1.Fan2B",
                "Key": "CoolingController.1.Fan2B",
                "Location": {
                    "PartLocation": {
                        "LocationOrdinalValue": 2,
                        "LocationType": "Slot"
                    }
                },
                "PWM": 80,
                "PrimaryStatus": "Healthy",
                "State": "Not Available",
                "VariableSpeed": "true"
            }
        ]
        assert result == expected_result
