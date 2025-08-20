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

from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.controller_sensor import IDRACControllerSensorInfo
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils


class TestIDRACControllerSensorInfo(TestUtils):
    def test_get_controller_sensor_info(self, idrac_mock):
        response = {
            "Members": [
                {
                    "@odata.id": "/redfish/v1/RAID.SL.3-1"
                },
                {
                    "@odata.id": "/redfish/v1/BOSS.Slot.6-1"
                }
            ]
        }
        idrac_mock.invoke_request.return_value.status_code = 200
        idrac_mock.invoke_request.return_value.json_data = response
        idrac_controller_sensor_info = IDRACControllerSensorInfo(idrac_mock)
        result = idrac_controller_sensor_info.get_controller_sensor_info()
        expected_result = [
            {
                "FQDD": "RAID.SL.3-1",
                "Key": "RAID.SL.3-1"
            },
            {
                "FQDD": "BOSS.Slot.6-1",
                "Key": "BOSS.Slot.6-1"
            }
        ]
        assert result == expected_result
