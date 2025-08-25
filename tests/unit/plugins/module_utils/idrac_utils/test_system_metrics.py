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

from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.system_metrics import IDRACSystemMetricsInfo
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils

NA = "Not Available"


class TestIDRACSystemMetricsInfo(TestUtils):

    def test_get_system_metrics_info_success(self, idrac_mock):
        # Mock response for energy consumption
        energy_resp = {"LifetimeReading": 12345}
        # Mock response for temperature
        temp_resp = {
            "Oem": {
                "Dell": {
                    "DurationInCriticalThresholdPercent": 5,
                    "DurationInWarningThresholdPercent": 10
                }
            }
        }
        # Mock response for power consumption
        power_resp = {"LowestReading": 200}

        # Patch invoke_request sequential responses
        idrac_mock.invoke_request.side_effect = [
            type("Resp", (), {"status_code": 200, "json_data": energy_resp}),
            type("Resp", (), {"status_code": 200, "json_data": temp_resp}),
            type("Resp", (), {"status_code": 200, "json_data": power_resp}),
        ]

        metrics_info = IDRACSystemMetricsInfo(idrac_mock)
        result = metrics_info.get_system_metrics_info()

        expected = [{
            "EnergyConsumption": 12345,
            "InletTempCriticalPerc": 5,
            "InletTempWarnPerc": 10,
            "Key": "SystemMetrics",
            "PowerConsumption": 200,
            "SystemMetrics": "Not Available"
        }]

        assert result == expected

    def test_get_system_metrics_info_missing_fields(self, idrac_mock):
        # Missing LifetimeReading and Dell values
        energy_resp = {}
        temp_resp = {"Oem": {"Dell": {}}}
        power_resp = {}

        idrac_mock.invoke_request.side_effect = [
            type("Resp", (), {"status_code": 200, "json_data": energy_resp}),
            type("Resp", (), {"status_code": 200, "json_data": temp_resp}),
            type("Resp", (), {"status_code": 200, "json_data": power_resp}),
        ]

        metrics_info = IDRACSystemMetricsInfo(idrac_mock)
        result = metrics_info.get_system_metrics_info()

        expected = [{
            "EnergyConsumption": NA,
            "InletTempCriticalPerc": NA,
            "InletTempWarnPerc": NA,
            "Key": "SystemMetrics",
            "PowerConsumption": NA,
            "SystemMetrics": "Not Available"
        }]

        assert result == expected

    def test_get_system_metrics_info_non_200_responses(self, idrac_mock):
        # Force non-200 to check fallbacks
        idrac_mock.invoke_request.side_effect = [
            type("Resp", (), {"status_code": 500, "json_data": {}}),
            type("Resp", (), {"status_code": 404, "json_data": {}}),
            type("Resp", (), {"status_code": 503, "json_data": {}}),
        ]

        metrics_info = IDRACSystemMetricsInfo(idrac_mock)
        result = metrics_info.get_system_metrics_info()

        expected = [{
            "EnergyConsumption": {},
            "InletTempCriticalPerc": {},
            "InletTempWarnPerc": {},
            "Key": "SystemMetrics",
            "PowerConsumption": {},
            "SystemMetrics": "Not Available"
        }]

        assert result == expected
