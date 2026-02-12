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
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.chassis_sensor_util import IDRACChassisSensors
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils
import pytest

NA = "Not Available"


class Resp:
    def __init__(self, status_code, data):
        self.status_code = status_code
        self.json_data = data


class TestIDRACSystemMetricsInfo(TestUtils):

    @pytest.fixture
    def sensors(self, idrac_mock, mocker):
        sensors = IDRACChassisSensors(idrac_mock)
        return sensors

    def test_get_system_metrics_info_success(self, sensors, mocker, idrac_mock):

        mocker.patch.object(
            sensors,
            "get_sensor",
            side_effect=[
                Resp(200, {"LifetimeReading": 12345}),
                Resp(200, {"Oem": {"Dell": {
                    "DurationInCriticalThresholdPercent": 5,
                    "DurationInWarningThresholdPercent": 10
                }}}),
                Resp(200, {"LowestReading": 200}),
            ]
        )

        metrics_info = IDRACSystemMetricsInfo(idrac_mock, sensors)
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

    def test_get_system_metrics_info_missing_fields(self, sensors, mocker, idrac_mock):

        mocker.patch.object(
            sensors,
            "get_sensor",
            side_effect=[
                Resp(200, {}),
                Resp(200, {"Oem": {"Dell": {}}}),
                Resp(200, {}),
            ]
        )

        metrics_info = IDRACSystemMetricsInfo(idrac_mock, sensors)
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

    def test_get_system_metrics_info_non_200_responses(self, sensors, mocker, idrac_mock):

        mocker.patch.object(
            sensors,
            "get_sensor",
            side_effect=[
                Resp(500, {}),
                Resp(404, {}),
                Resp(404, {}),
                Resp(503, {}),
            ]
        )

        metrics_info = IDRACSystemMetricsInfo(idrac_mock, sensors)
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
