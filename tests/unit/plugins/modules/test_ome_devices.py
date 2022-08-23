# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 6.1.0
# Copyright (C) 2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
from io import StringIO
from ssl import SSLError

import pytest
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import CHANGES_MSG, NO_CHANGES_MSG
from ansible_collections.dellemc.openmanage.plugins.modules import ome_devices
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

DELETE_SUCCESS = "The devices(s) are removed successfully."
INVALID_DEV_ST = "Unable to complete the operation because the entered target device(s) '{0}' are invalid."
JOB_DESC = "The {0} task initiated from OpenManage Ansible Modules for devices with the ids '{1}'."
APPLY_TRIGGERED = "Successfully initiated the device action job."
JOB_SCHEDULED = "The job is scheduled successfully."
SUCCESS_MSG = "The device operation is performed successfully."

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_devices.'


@pytest.fixture
def ome_connection_mock_for_devices(mocker, ome_response_mock):
    connection_class_mock = mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.ome_devices.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeDevices(FakeAnsibleModule):
    module = ome_devices

    @pytest.mark.parametrize("params", [
        {"json_data": {"value": [{'Id': 24, 'Identifier': "ABCTAG1", "Type": 1000}]},
         'message': DELETE_SUCCESS, "success": True, 'mparams': {
            "device_service_tags": ["ABCTAG1", "BCDTAG2"], 'state': 'absent'}},
        {"json_data": {"value": [{'Id': 24, 'Identifier': "ABCTAG1", "Type": 1000}]},
         'message': CHANGES_MSG, "success": True,
         'check_mode': True,
         'mparams': {"device_service_tags": ["ABCTAG1", "BCDTAG2"], 'state': 'absent'}},
        {"json_data": {"value": [{'Id': 24, 'Identifier': "ABCTAG1", "Type": 1000}]},
         'message': NO_CHANGES_MSG, "success": True,
         'mparams': {"device_service_tags": ["ABCTAG2", "BCDTAG2"], 'state': 'absent'}},
        {"json_data": {"value": [{'Id': 24, 'Identifier': "ABCTAG2", "Type": 1001}]},
         'message': INVALID_DEV_ST.format(",".join(map(str, ["ABCTAG2"]))), "success": True,
         'mparams': {"device_service_tags": ["ABCTAG2"], 'state': 'present'}},
        {"json_data": {"value": [{'Id': 24, 'Identifier': "ABCTAG2", "Type": 1001}]},
         'message': INVALID_DEV_ST.format(",".join(map(str, [24, 25]))), "success": True,
         'mparams': {"device_ids": [24, 25], 'state': 'present'}},
        {"json_data": {"value": []},
         'message': INVALID_DEV_ST.format(",".join(map(str, [24]))), "success": True,
         'mparams': {"device_ids": [24], 'state': 'present'}}
    ])
    def test_ome_devices_delete(self, params, ome_connection_mock_for_devices, ome_response_mock, ome_default_args,
                                module_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['json_data']
        ome_connection_mock_for_devices.get_all_items_with_pagination.return_value = params['json_data']
        ome_default_args.update(params['mparams'])
        result = self._run_module(ome_default_args, check_mode=params.get('check_mode', False))
        assert result['msg'] == params['message']

    @pytest.mark.parametrize("params", [
        {"json_data": {"value": [{'Id': 24, 'Identifier': "ABCTAG1", "Type": 1000},
                                 {'Id': 25, 'Identifier': "BCDTAG2", "Type": 1000}]},
         'message': APPLY_TRIGGERED, "success": True, 'mparams': {
            "device_service_tags": ["ABCTAG1", "BCDTAG2"], "job_wait": False,
            "job_name": "my test job", "job_description": "My job description"
        }, "check_similar_job": {}},
        {"json_data": {"value": [{'Id': 24, 'Identifier': "ABCTAG1", "Type": 1000},
                                 {'Id': 25, 'Identifier': "BCDTAG2", "Type": 1000}]},
         'message': APPLY_TRIGGERED, "success": True, 'mparams': {
            "device_service_tags": ["ABCTAG1", "BCDTAG2"], "job_wait": False
        }, "check_similar_job": {}},
        {"json_data": {"value": [{'Id': 24, 'Identifier': "ABCTAG1", "Type": 1000},
                                 {'Id': 25, 'Identifier': "BCDTAG2", "Type": 1000}]},
         'message': JOB_SCHEDULED, "success": True, 'mparams': {
            "device_service_tags": ["ABCTAG1", "BCDTAG2"], "job_wait": False,
            "job_schedule": "my cron task"
        }, "check_similar_job": {}},
        {"json_data": {"value": [{'Id': 24, 'Identifier': "ABCTAG1", "Type": 1000},
                                 {'Id': 25, 'Identifier': "BCDTAG2", "Type": 1000}]},
         'message': CHANGES_MSG, "success": True, 'mparams': {
            "device_service_tags": ["ABCTAG1", "BCDTAG2"], "job_wait": False},
         "check_similar_job": {}, "check_mode": True
         },
        {"json_data": {
            "value": [
                {
                    "Id": 14874,
                    "JobName": "Refresh inventory",
                    "JobDescription": JOB_DESC.format("Refresh inventory", "13216"),
                    "Schedule": "startnow",
                    "State": "Enabled",
                    "Targets": [
                        {
                            "JobId": 14874,
                            "Id": 13123,
                            "Data": "",
                            "TargetType": {
                                "Id": 1000,
                                "Name": "DEVICE"
                            }
                        }
                    ],
                    "Params": [
                        {
                            "JobId": 14874,
                            "Key": "action",
                            "Value": "CONFIG_INVENTORY"
                        },
                        {
                            "JobId": 14874,
                            "Key": "isCollectDriverInventory",
                            "Value": "true"
                        }
                    ],
                    "LastRunStatus": {
                        "@odata.type": "#JobService.JobStatus",
                        "Id": 2060,
                        "Name": "Completed"
                    },
                    "JobType": {
                        "@odata.type": "#JobService.JobType",
                        "Id": 8,
                        "Name": "Inventory_Task",
                    },
                },
                {
                    "Id": 14874,
                    "JobName": "Refresh inventory",
                    "JobDescription": JOB_DESC.format("Refresh inventory", "13216"),
                    "Schedule": "startnow",
                    "State": "Enabled",
                    "Targets": [
                        {
                            "JobId": 14874,
                            "Id": 13216,
                            "Data": "",
                            "TargetType": {
                                "Id": 1000,
                                "Name": "DEVICE"
                            }
                        }
                    ],
                    "Params": [
                        {
                            "JobId": 14874,
                            "Key": "action",
                            "Value": "CONFIG_INVENTORY"
                        },
                        {
                            "JobId": 14874,
                            "Key": "isCollectDriverInventory",
                            "Value": "false"
                        }
                    ],
                    "LastRunStatus": {
                        "@odata.type": "#JobService.JobStatus",
                        "Id": 2060,
                        "Name": "Completed"
                    },
                    "JobType": {
                        "@odata.type": "#JobService.JobType",
                        "Id": 8,
                        "Name": "Inventory_Task",
                    },
                },
                {
                    "Id": 14874,
                    "JobName": "Refresh inventory",
                    "JobDescription": JOB_DESC.format("Refresh inventory", "13216"),
                    "Schedule": "startnow",
                    "State": "Enabled",
                    "Targets": [
                        {
                            "JobId": 14874,
                            "Id": 13216,
                            "Data": "",
                            "TargetType": {
                                "Id": 1000,
                                "Name": "DEVICE"
                            }
                        }
                    ],
                    "Params": [
                        {
                            "JobId": 14874,
                            "Key": "action",
                            "Value": "CONFIG_INVENTORY"
                        },
                        {
                            "JobId": 14874,
                            "Key": "isCollectDriverInventory",
                            "Value": "true"
                        }
                    ],
                    "LastRunStatus": {
                        "@odata.type": "#JobService.JobStatus",
                        "Id": 2060,
                        "Name": "Completed"
                    },
                    "JobType": {
                        "@odata.type": "#JobService.JobType",
                        "Id": 8,
                        "Name": "Inventory_Task",
                    },
                }
            ]
        },
            'message': APPLY_TRIGGERED, "success": True, 'mparams': {
            "device_service_tags": ["ABCTAG1", "BCDTAG2"], "job_wait": False
        }, "get_dev_ids": ([13216], {})},

        {"json_data": {
            "value": [
                {
                    "Id": 14874,
                    "JobName": "Refresh inventory",
                    "JobDescription": JOB_DESC.format("Refresh inventory", "13216"),
                    "Schedule": "startnow",
                    "State": "Enabled",
                    "Targets": [
                        {
                            "JobId": 14874,
                            "Id": 13216,
                            "Data": "",
                            "TargetType": {
                                "Id": 1000,
                                "Name": "DEVICE"
                            }
                        }
                    ],
                    "Params": [
                        {
                            "JobId": 14874,
                            "Key": "action",
                            "Value": "CONFIG_INVENTORY"
                        },
                        {
                            "JobId": 14874,
                            "Key": "isCollectDriverInventory",
                            "Value": "true"
                        }
                    ],
                    "LastRunStatus": {
                        "@odata.type": "#JobService.JobStatus",
                        "Id": 2060,
                        "Name": "Completed"
                    },
                    "JobType": {
                        "@odata.type": "#JobService.JobType",
                        "Id": 8,
                        "Name": "Inventory_Task",
                    },
                }
            ]
        },
            'message': CHANGES_MSG, "success": True, 'mparams': {
            "device_service_tags": ["ABCTAG1", "BCDTAG2"], "job_wait": False
        }, "get_dev_ids": ([13216], {}), "check_mode": True},
        {"json_data": {
            "value": [
                {
                    "Id": 14874,
                    "JobName": "Refresh inventory",
                    "JobDescription": JOB_DESC.format("Refresh inventory", "13216"),
                    "Schedule": "startnow",
                    "State": "Enabled",
                    "Targets": [
                        {
                            "JobId": 14874,
                            "Id": 13216,
                            "Data": "",
                            "TargetType": {
                                "Id": 1000,
                                "Name": "DEVICE"
                            }
                        }
                    ],
                    "Params": [
                        {
                            "JobId": 14874,
                            "Key": "action",
                            "Value": "CONFIG_INVENTORY"
                        },
                        {
                            "JobId": 14874,
                            "Key": "isCollectDriverInventory",
                            "Value": "true"
                        }
                    ],
                    "LastRunStatus": {
                        "@odata.type": "#JobService.JobStatus",
                        "Id": 2050,
                        "Name": "Completed"
                    },
                    "JobType": {
                        "@odata.type": "#JobService.JobType",
                        "Id": 8,
                        "Name": "Inventory_Task",
                    },
                }
            ]},
            'message': NO_CHANGES_MSG, "success": True, 'mparams': {
            "device_service_tags": ["ABCTAG1", "BCDTAG2"], "job_wait": False
        }, "get_dev_ids": ([13216], {})},
        {"json_data": {
            "value": [
                {
                    "Id": 14874,
                    "JobName": "Reset iDRAC",
                    "JobDescription": JOB_DESC.format("Reset iDRAC", "13216"),
                    "Schedule": "startnow",
                    "State": "Enabled",
                    "Targets": [
                        {
                            "JobId": 14874,
                            "Id": 13216,
                            "Data": "",
                            "TargetType": {
                                "Id": 1000,
                                "Name": "DEVICE"
                            }
                        }
                    ],
                    "Params": [
                        {
                            "JobId": 14874,
                            "Key": "operationName",
                            "Value": "RESET_IDRAC"
                        }
                    ],
                    "LastRunStatus": {
                        "@odata.type": "#JobService.JobStatus",
                        "Id": 2050,
                        "Name": "Completed"
                    },
                    "JobType": {
                        "@odata.type": "#JobService.JobType",
                        "Id": 3,
                        "Name": "DeviceAction_Task",
                    },
                }
            ]},
            'message': NO_CHANGES_MSG, "success": True, 'mparams': {
            "device_service_tags": ["ABCTAG1", "BCDTAG2"],
            "job_wait": False, "device_action": 'reset_idrac',
        }, "get_dev_ids": ([13216], {})},
        {"json_data": {
            "value": [
                {
                    "Id": 14874,
                    "JobName": "Clear iDRAC job queue",
                    "JobDescription": JOB_DESC.format("Clear iDRAC job queue", "13216"),
                    "Schedule": "startnow",
                    "State": "Enabled",
                    "Targets": [
                        {
                            "JobId": 14874,
                            "Id": 13216,
                            "Data": "",
                            "TargetType": {
                                "Id": 1000,
                                "Name": "DEVICE"
                            }
                        }
                    ],
                    "Params": [
                        {
                            "JobId": 14874,
                            "Key": "deviceTypes",
                            "Value": "1000"
                        },
                        {
                            "JobId": 14874,
                            "Key": "operationName",
                            "Value": "REMOTE_RACADM_EXEC"
                        },
                        {
                            "JobId": 14874,
                            "Key": "Command",
                            "Value": "jobqueue delete -i JID_CLEARALL_FORCE"
                        },
                        {
                            "JobId": 14874,
                            "Key": "CommandTimeout",
                            "Value": "60"
                        }
                    ],
                    "LastRunStatus": {
                        "@odata.type": "#JobService.JobStatus",
                        "Id": 2050,
                        "Name": "Completed"
                    },
                    "JobType": {
                        "@odata.type": "#JobService.JobType",
                        "Id": 3,
                        "Name": "DeviceAction_Task",
                    },
                }
            ]},
            'message': NO_CHANGES_MSG, "success": True, 'mparams': {
            "device_service_tags": ["ABCTAG1", "BCDTAG2"],
            "job_wait": False, "device_action": 'clear_idrac_job_queue',
        }, "get_dev_ids": ([13216], {})},
        {"json_data": {"Id": 14874, "LastRunStatus": {"Id": 2060, "Name": "Completed"}},
         'message': SUCCESS_MSG, "success": True, 'mparams': {
            "device_service_tags": ["ABCTAG1", "BCDTAG2"], "job_wait": True
        }, "check_similar_job": {}, "get_dev_ids": ([13216], {})},
        {"json_data": {"Id": 14874, "LastRunStatus": {"Id": 2070, "Name": "Completed"},
                       "Value": "Job Tracking has failed"},
         'message': "Job Tracking has failed", "success": True, 'mparams': {
            "device_service_tags": ["ABCTAG1", "BCDTAG2"], "job_wait": True
        }, "check_similar_job": {}, "get_dev_ids": ([13216], {})}
    ])
    def test_ome_devices_main_state_present(self, params, ome_connection_mock_for_devices, ome_response_mock,
                                            ome_default_args, module_mock, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['json_data']
        mocks = ["check_similar_job", "get_dev_ids"]
        for m in mocks:
            if m in params:
                mocker.patch(MODULE_PATH + m, return_value=params.get(m, {}))
        mocker.patch("ansible_collections.dellemc.openmanage.plugins.module_utils.utils." + 'time.sleep', return_value=None)
        ome_default_args.update(params['mparams'])
        result = self._run_module(ome_default_args, check_mode=params.get('check_mode', False))
        assert result['msg'] == params['message']

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_devices_main_exception_failure_case(self, exc_type, mocker, ome_default_args,
                                                     ome_connection_mock_for_devices, ome_response_mock):
        ome_default_args.update({"state": "absent", "device_service_tags": "t1"})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'get_dev_ids', side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'get_dev_ids', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'get_dev_ids',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result
