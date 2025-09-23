#
# Dell OpenManage Ansible Modules
# Version 10.0.0
# Copyright (C) 2025 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.system_board_metrics import IDRACSystemBoardMetricsInfo
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.chassis_sensor_util import IDRACChassisSensors
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils

NA = "Not Available"


class TestIDRACSystemBoardMetricsInfo(TestUtils):
    all_na = [
        {
            "Key": "SystemBoardMetrics",

            "CPUUsageAvg1H": NA,
            "CPUUsageAvg1D": NA,
            "CPUUsageAvg1W": NA,
            "CPUUsageMax1H": NA,
            "CPUUsageMax1D": NA,
            "CPUUsageMax1W": NA,
            "CPUUsageMin1H": NA,
            "CPUUsageMin1D": NA,
            "CPUUsageMin1W": NA,
            "SYSPeakCPUUsage": NA,

            "IOUsageAvg1H": NA,
            "IOUsageAvg1D": NA,
            "IOUsageAvg1W": NA,
            "IOUsageMax1H": NA,
            "IOUsageMax1D": NA,
            "IOUsageMax1W": NA,
            "IOUsageMin1H": NA,
            "IOUsageMin1D": NA,
            "IOUsageMin1W": NA,
            "SYSPeakIOUsage": NA,

            "MemoryUsageAvg1H": NA,
            "MemoryUsageAvg1D": NA,
            "MemoryUsageAvg1W": NA,
            "MemoryUsageMax1H": NA,
            "MemoryUsageMax1D": NA,
            "MemoryUsageMax1W": NA,
            "MemoryUsageMin1H": NA,
            "MemoryUsageMin1D": NA,
            "MemoryUsageMin1W": NA,
            "SYSPeakMemoryUsage": NA,

            "SYSUsageAvg1H": NA,
            "SYSUsageAvg1D": NA,
            "SYSUsageAvg1W": NA,
            "SYSUsageMax1H": NA,
            "SYSUsageMax1D": NA,
            "SYSUsageMax1W": NA,
            "SYSUsageMin1H": NA,
            "SYSUsageMin1D": NA,
            "SYSUsageMin1W": NA,
            "SYSPeakSYSUsage": NA,

            "PeakPower": NA,
            "PeakAmperage": NA,
            "PeakHeadroom": NA,

            "SystemBoardMetrics": NA
        }
    ]

    def test_get_system_metrics_info_success(self, idrac_mock):
        sensors = self._get_chassis_resp(idrac_mock)
        # Mock responses
        cpu_usage_resp = {
            "Oem": {
                "Dell": {
                    "AverageReadings": {
                        "LastHour": {"Reading": 2},
                        "LastDay": {"Reading": 2},
                        "LastWeek": {"Reading": 2}
                    },
                    "PeakReadings": {
                        "LastHour": {"Reading": 3},
                        "LastDay": {"Reading": 3},
                        "LastWeek": {"Reading": 3}
                    },
                    "LowestReadings": {
                        "LastHour": {"Reading": 1},
                        "LastDay": {"Reading": 1},
                        "LastWeek": {"Reading": 1}
                    },
                }
            },
            "PeakReading": 3
        }
        io_usage_resp = {
            "Oem": {
                "Dell": {
                    "AverageReadings": {
                        "LastHour": {"Reading": 5},
                        "LastDay": {"Reading": 5},
                        "LastWeek": {"Reading": 5}
                    },
                    "PeakReadings": {
                        "LastHour": {"Reading": 6},
                        "LastDay": {"Reading": 6},
                        "LastWeek": {"Reading": 6}
                    },
                    "LowestReadings": {
                        "LastHour": {"Reading": 4},
                        "LastDay": {"Reading": 4},
                        "LastWeek": {"Reading": 4}
                    },
                }
            },
            "PeakReading": 6
        }
        mem_usage_resp = {
            "Oem": {
                "Dell": {
                    "AverageReadings": {
                        "LastHour": {"Reading": 8},
                        "LastDay": {"Reading": 8},
                        "LastWeek": {"Reading": 8}
                    },
                    "PeakReadings": {
                        "LastHour": {"Reading": 9},
                        "LastDay": {"Reading": 9},
                        "LastWeek": {"Reading": 9}
                    },
                    "LowestReadings": {
                        "LastHour": {"Reading": 7},
                        "LastDay": {"Reading": 7},
                        "LastWeek": {"Reading": 7}
                    },
                }
            },
            "PeakReading": 9
        }
        sys_usage_resp = {
            "Oem": {
                "Dell": {
                    "AverageReadings": {
                        "LastHour": {"Reading": 11},
                        "LastDay": {"Reading": 11},
                        "LastWeek": {"Reading": 11}
                    },
                    "PeakReadings": {
                        "LastHour": {"Reading": 12},
                        "LastDay": {"Reading": 12},
                        "LastWeek": {"Reading": 12}
                    },
                    "LowestReadings": {
                        "LastHour": {"Reading": 10},
                        "LastDay": {"Reading": 10},
                        "LastWeek": {"Reading": 10}
                    },
                }
            },
            "PeakReading": 12
        }
        power_resp = {"PeakReading": 531}
        amperage_resp = {"PeakReading": 4.265625}
        headroom_resp = {"LowestReading": 969}

        # Patch invoke_request sequential responses
        idrac_mock.invoke_request.side_effect = self._get_sequential_responses(
            cpu_usage_resp,
            io_usage_resp,
            mem_usage_resp,
            sys_usage_resp,
            power_resp,
            amperage_resp,
            headroom_resp
        )

        system_board_metrics_info = IDRACSystemBoardMetricsInfo(idrac_mock, sensors)
        result = system_board_metrics_info.get_system_board_metrics_info()

        expected = [{
            "Key": "SystemBoardMetrics",

            "CPUUsageAvg1H": 2,
            "CPUUsageAvg1D": 2,
            "CPUUsageAvg1W": 2,
            "CPUUsageMax1H": 3,
            "CPUUsageMax1D": 3,
            "CPUUsageMax1W": 3,
            "CPUUsageMin1H": 1,
            "CPUUsageMin1D": 1,
            "CPUUsageMin1W": 1,
            "SYSPeakCPUUsage": 3,

            "IOUsageAvg1H": 5,
            "IOUsageAvg1D": 5,
            "IOUsageAvg1W": 5,
            "IOUsageMax1H": 6,
            "IOUsageMax1D": 6,
            "IOUsageMax1W": 6,
            "IOUsageMin1H": 4,
            "IOUsageMin1D": 4,
            "IOUsageMin1W": 4,
            "SYSPeakIOUsage": 6,

            "MemoryUsageAvg1H": 8,
            "MemoryUsageAvg1D": 8,
            "MemoryUsageAvg1W": 8,
            "MemoryUsageMax1H": 9,
            "MemoryUsageMax1D": 9,
            "MemoryUsageMax1W": 9,
            "MemoryUsageMin1H": 7,
            "MemoryUsageMin1D": 7,
            "MemoryUsageMin1W": 7,
            "SYSPeakMemoryUsage": 9,

            "SYSUsageAvg1H": 11,
            "SYSUsageAvg1D": 11,
            "SYSUsageAvg1W": 11,
            "SYSUsageMax1H": 12,
            "SYSUsageMax1D": 12,
            "SYSUsageMax1W": 12,
            "SYSUsageMin1H": 10,
            "SYSUsageMin1D": 10,
            "SYSUsageMin1W": 10,
            "SYSPeakSYSUsage": 12,

            "PeakPower": 531,
            "PeakAmperage": 4.265625,
            "PeakHeadroom": 969,

            "SystemBoardMetrics": NA
        }]

        assert result == expected

    def test_get_system_metrics_info_missing_fields(self, idrac_mock):
        sensors = self._get_chassis_resp(idrac_mock)
        # Mock responses with missing fields
        cpu_usage_resp = {
            "Oem": {
                "Dell": {
                    "AverageReadings": {
                        "LastHour": {},
                        "LastDay": {},
                        "LastWeek": {}
                    },
                    "PeakReadings": {
                        "LastHour": {},
                        "LastDay": {},
                        "LastWeek": {}
                    },
                    "LowestReadings": {
                        "LastHour": {},
                        "LastDay": {},
                        "LastWeek": {}
                    },
                }
            }
        }
        io_usage_resp = {
            "Oem": {
                "Dell": {
                    "AverageReadings": {
                        "LastHour": {},
                        "LastDay": {},
                        "LastWeek": {}
                    },
                    "PeakReadings": {
                        "LastHour": {},
                        "LastDay": {},
                        "LastWeek": {}
                    },
                    "LowestReadings": {
                        "LastHour": {},
                        "LastDay": {},
                        "LastWeek": {}
                    },
                }
            }
        }
        mem_usage_resp = {
            "Oem": {
                "Dell": {
                    "AverageReadings": {
                        "LastHour": {},
                        "LastDay": {},
                        "LastWeek": {}
                    },
                    "PeakReadings": {
                        "LastHour": {},
                        "LastDay": {},
                        "LastWeek": {}
                    },
                    "LowestReadings": {
                        "LastHour": {},
                        "LastDay": {},
                        "LastWeek": {}
                    },
                }
            }
        }
        sys_usage_resp = {
            "Oem": {
                "Dell": {
                    "AverageReadings": {
                        "LastHour": {},
                        "LastDay": {},
                        "LastWeek": {}
                    },
                    "PeakReadings": {
                        "LastHour": {},
                        "LastDay": {},
                        "LastWeek": {}
                    },
                    "LowestReadings": {
                        "LastHour": {},
                        "LastDay": {},
                        "LastWeek": {}
                    },
                }
            }
        }
        power_resp = {}
        amperage_resp = {}
        headroom_resp = {}

        # Patch invoke_request sequential responses
        idrac_mock.invoke_request.side_effect = self._get_sequential_responses(
            cpu_usage_resp,
            io_usage_resp,
            mem_usage_resp,
            sys_usage_resp,
            power_resp,
            amperage_resp,
            headroom_resp
        )

        system_board_metrics_info = IDRACSystemBoardMetricsInfo(idrac_mock, sensors)
        result = system_board_metrics_info.get_system_board_metrics_info()

        assert result == self.all_na

    def test_get_system_metrics_info_non_200_responses(self, idrac_mock):
        sensors = self._get_chassis_resp(idrac_mock, False)
        # Force non-200 to check fallbacks
        idrac_mock.invoke_request.side_effect = [
            type("Resp", (), {"status_code": 503, "json_data": {}}),
            type("Resp", (), {"status_code": 500, "json_data": {}}),
            type("Resp", (), {"status_code": 404, "json_data": {}}),
            type("Resp", (), {"status_code": 503, "json_data": {}}),
            type("Resp", (), {"status_code": 500, "json_data": {}}),
            type("Resp", (), {"status_code": 404, "json_data": {}}),
            type("Resp", (), {"status_code": 503, "json_data": {}}),
        ]

        system_board_metrics_info = IDRACSystemBoardMetricsInfo(idrac_mock, sensors)
        result = system_board_metrics_info.get_system_board_metrics_info()

        assert result == self.all_na

    def _get_sequential_responses(self, cpu_usage_resp, io_usage_resp, mem_usage_resp, sys_usage_resp, power_resp, amperage_resp, headroom_resp):
        return [
            type("Resp", (), {"status_code": 200, "json_data": cpu_usage_resp}),
            type("Resp", (), {"status_code": 200, "json_data": io_usage_resp}),
            type("Resp", (), {"status_code": 200, "json_data": mem_usage_resp}),
            type("Resp", (), {"status_code": 200, "json_data": sys_usage_resp}),
            type("Resp", (), {"status_code": 200, "json_data": power_resp}),
            type("Resp", (), {"status_code": 200, "json_data": amperage_resp}),
            type("Resp", (), {"status_code": 200, "json_data": headroom_resp}),
        ]

    def _get_chassis_resp(self, idrac_mock, all_members=True):
        chassis_resp = {
            "Members": [
                {"@odata.id": "/redfish/v1/Chassis/System.Embedded.1/Sensors/SystemBoardIOUsage"},
                {"@odata.id": "/redfish/v1/Chassis/System.Embedded.1/Sensors/SystemBoardMEMUsage"},
                {"@odata.id": "/redfish/v1/Chassis/System.Embedded.1/Sensors/SystemBoardSYSUsage"},
                {"@odata.id": "/redfish/v1/Chassis/System.Embedded.1/Sensors/SystemBoardPwrConsumption"},
                {"@odata.id": "/redfish/v1/Chassis/System.Embedded.1/Sensors/SystemBoardCurrentConsumption"},
                {"@odata.id": "/redfish/v1/Chassis/System.Embedded.1/Sensors/PowerHeadroom"},
            ]
        }
        if all_members:
            chassis_resp["Members"].append({"@odata.id": "/redfish/v1/Chassis/System.Embedded.1/Sensors/SystemBoardCPUUsage"})
        idrac_mock.invoke_request.return_value.json_data = chassis_resp
        return IDRACChassisSensors(idrac_mock)
