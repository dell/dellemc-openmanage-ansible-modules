#
# Dell OpenManage Ansible Modules
# Version 9.13.0
# Copyright (C) 2025 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.sensors_temperature import IDRACSensorsTemperatureInfo
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils
from unittest.mock import MagicMock

NA = "Not Available"


class TestIDRACSensorsTemperatureInfo(TestUtils):
    def test_get_sensors_temperature_info(self, idrac_mock):
        thermal_response = MagicMock()
        thermal_response.status_code = 200
        thermal_response.json_data = {
            "Temperatures": [
                {"Name": "Temp Sensor 1"},
                {"Name": "Temp Sensor 2"}
            ]
        }

        temp1_response = MagicMock()
        temp1_response.status_code = 200
        temp1_response.json_data = {
            "Reading": 45,
            "Oem": {"Dell": {"DeviceID": "iDRAC.Embedded.1#Temp1"}},
            "Status": {"State": "Enabled", "Health": "OK"},
            "Name": "TempSensor1",
            "Type": "Temperature"
        }

        temp2_response = MagicMock()
        temp2_response.status_code = 200
        temp2_response.json_data = {
            "Reading": 50,
            "Oem": {"Dell": {"DeviceID": "iDRAC.Embedded.1#Temp2"}},
            "Status": {"State": "Enabled", "Health": "OK"},
            "Name": "TempSensor2",
            "Type": "Temperature"
        }

        idrac_mock.invoke_request.side_effect = [
            thermal_response,
            temp1_response,
            temp2_response
        ]

        idrac_sensors_temp_info = IDRACSensorsTemperatureInfo(idrac_mock)
        result = idrac_sensors_temp_info.get_sensors_temperature_info()

        expected_result = [
            {
                "CurrentReading": 45,
                "CurrentState": "Not Available",
                "DeviceID": "iDRAC.Embedded.1#Temp1",
                "HealthState": "OK",
                "Key": "TempSensor1",
                "Location": "TempSensor1",
                "OtherSensorTypeDescription": "Not Available",
                "PrimaryStatus": "Healthy",
                "SensorType": "Temperature",
                "State": "Enabled",
                "Type": "Temperature"
            },
            {
                "CurrentReading": 50,
                "CurrentState": "Not Available",
                "DeviceID": "iDRAC.Embedded.1#Temp2",
                "HealthState": "OK",
                "Key": "TempSensor2",
                "Location": "TempSensor2",
                "OtherSensorTypeDescription": "Not Available",
                "PrimaryStatus": "Healthy",
                "SensorType": "Temperature",
                "State": "Enabled",
                "Type": "Temperature"
            }
        ]

        assert result == expected_result
