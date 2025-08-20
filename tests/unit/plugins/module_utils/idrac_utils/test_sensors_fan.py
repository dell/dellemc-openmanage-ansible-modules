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

from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.sensors_fan import IDRACSensorsFanInfo
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils
from unittest.mock import MagicMock

NA = "Not Available"


class TestIDRACSensorsFanInfo(TestUtils):
    def test_get_sensors_fan_info(self, idrac_mock):
        # First call: Thermal endpoint (fan names)
        thermal_response = MagicMock()
        thermal_response.status_code = 200
        thermal_response.json_data = {
            "Fans": [
                {"FanName": "Fan1"},
                {"FanName": "Fan2"}
            ]
        }

        # Second call: Fan1 details
        fan1_response = MagicMock()
        fan1_response.status_code = 200
        fan1_response.json_data = {
            "Reading": 4440,
            "Oem": {"Dell": {"DeviceID": "iDRAC.Embedded.1#Fan1"}},
            "Status": {"State": "Enabled", "Health": "OK"},
            "Name": "Fan1",
            "FanName": "Fan1"
        }

        # Third call: Fan2 details
        fan2_response = MagicMock()
        fan2_response.status_code = 200
        fan2_response.json_data = {
            "Reading": 4530,
            "Oem": {"Dell": {"DeviceID": "iDRAC.Embedded.1#Fan2"}},
            "Status": {"State": "Enabled", "Health": "OK"},
            "Name": "Fan2",
            "FanName": "Fan2"
        }

        # Make invoke_request return these responses in order
        idrac_mock.invoke_request.side_effect = [
            thermal_response,
            fan1_response,
            fan2_response
        ]

        idrac_sensors_fan_info = IDRACSensorsFanInfo(idrac_mock)
        result = idrac_sensors_fan_info.get_sensors_fan_info()

        expected_result = [
            {
                "CurrentReading": 4440,
                "CurrentState": "Not Available",
                "DeviceID": "iDRAC.Embedded.1#Fan1",
                "FQDD": "Not Available",
                "HealthState": "OK",
                "Key": "Fan1",
                "Location": "Fan1",
                "Name": "Fan1",
                "OtherSensorTypeDescription": "Not Available",
                "PrimaryStatus": "Healthy",
                "SensorType": "Fan",
                "State": "Enabled",
                "SubType": "Not Available",
                "Type": "Not Available",
                "coolingUnitIndexReference": "Not Available"
            },
            {
                "CurrentReading": 4530,
                "CurrentState": "Not Available",
                "DeviceID": "iDRAC.Embedded.1#Fan2",
                "FQDD": "Not Available",
                "HealthState": "OK",
                "Key": "Fan2",
                "Location": "Fan2",
                "Name": "Fan2",
                "OtherSensorTypeDescription": "Not Available",
                "PrimaryStatus": "Healthy",
                "SensorType": "Fan",
                "State": "Enabled",
                "SubType": "Not Available",
                "Type": "Not Available",
                "coolingUnitIndexReference": "Not Available"
            }
        ]

        assert result == expected_result
