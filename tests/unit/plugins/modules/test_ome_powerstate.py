# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.3.0
# Copyright (C) 2020-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from io import StringIO
from ansible.module_utils._text import to_text
from ansible_collections.dellemc.openmanage.plugins.modules import ome_powerstate

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


@pytest.fixture
def ome_connection_powerstate_mock(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'ome_powerstate.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmePowerstate(FakeAnsibleModule):
    module = ome_powerstate

    payload = {
        "Builtin": False,
        "CreatedBy": "admin",
        "Editable": True,
        "EndTime": None,
        "Id": 29099,
        "JobDescription": "Firmware Update Task",
        "JobName": "Firmware Update Task",
        "JobStatus": {
            "Id": 2080,
            "Name": "New"
        },
        "JobType": {
            "Id": 5,
            "Internal": False,
            "Name": "Update_Task"
        },
        "LastRun": None,
        "LastRunStatus": {
            "Id": 2200,
            "Name": "NotRun"
        },
        "NextRun": None,
        "Params": [
            {
                "JobId": 29099,
                "Key": "operationName",
                "Value": "INSTALL_FIRMWARE"
            },
            {
                "JobId": 29099,
                "Key": "complianceUpdate",
                "Value": "false"
            },
            {
                "JobId": 29099,
                "Key": "stagingValue",
                "Value": "false"
            },
            {
                "JobId": 29099,
                "Key": "signVerify",
                "Value": "true"
            }
        ],
        "Schedule": "startnow",
        "StartTime": None,
        "State": "Enabled",
        "Targets": [
            {
                "Data": "DCIM:INSTALLED#741__BIOS.Setup.1-1=1577776981156",
                "Id": 28628,
                "JobId": 29099,
                "TargetType": {
                    "Id": 1000,
                    "Name": "DEVICE"
                }
            }
        ],
        "UpdatedBy": None,
        "Visible": True
    }

    @pytest.mark.parametrize("param", [payload])
    def test_spawn_update_job_case(self, param, ome_response_mock,
                                   ome_connection_powerstate_mock):
        ome_response_mock.status_code = 201
        ome_response_mock.success = True
        ome_response_mock.json_data = {
            "Builtin": False,
            "CreatedBy": "admin",
            "Editable": True,
            "EndTime": None,
            "Id": 29099,
            "JobDescription": "Firmware Update Task",
            "JobName": "Firmware Update Task",
            "JobStatus": {
                "Id": 2080,
                "Name": "New"
            },
            "JobType": {
                "Id": 5,
                "Internal": False,
                "Name": "Update_Task"
            },
            "LastRun": None,
            "LastRunStatus": {
                "Id": 2200,
                "Name": "NotRun"
            },
            "NextRun": None,
            "Params": [
                {
                    "JobId": 29099,
                    "Key": "operationName",
                    "Value": "INSTALL_FIRMWARE"
                },
                {
                    "JobId": 29099,
                    "Key": "complianceUpdate",
                    "Value": "false"
                },
                {
                    "JobId": 29099,
                    "Key": "stagingValue",
                    "Value": "false"
                },
                {
                    "JobId": 29099,
                    "Key": "signVerify",
                    "Value": "true"
                }
            ],

            "Schedule": "startnow",
            "StartTime": None,
            "State": "Enabled",
            "Targets": [{
                "Data": "DCIM:INSTALLED#741__BIOS.Setup.1-1=1577776981156",
                "Id": 28628,
                "JobId": 29099,
                "TargetType": {
                    "Id": 1000,
                    "Name": "DEVICE"
                }
            }],
            "UpdatedBy": None,
            "Visible": True
        }
        data = self.module.spawn_update_job(ome_connection_powerstate_mock, param)
        assert data == param

    def test_build_power_state_payload_success_case(self, ome_connection_powerstate_mock):

        payload = self.module.build_power_state_payload(Constants.device_id1, "off", 2000)
        assert payload == {
            'Id': 0,
            'JobDescription': 'DeviceAction_Task',
            'JobName': 'DeviceAction_Task_PowerState',
            'JobType': {
                'Id': 3,
                'Name': 'DeviceAction_Task'
            },
            'Params': [
                {
                    'Key': 'operationName',
                    'Value': 'POWER_CONTROL'
                },
                {
                    'Key': 'powerState',
                    'Value': '2000'
                }
            ],
            'Schedule': 'startnow',
            'State': 'Enabled',
            'Targets': [
                {
                    'Data': '',
                    'Id': 1234,
                    'TargetType': {
                        'Id': 'off',
                        'Name': 'DEVICE'
                    }
                }
            ]
        }

    def test_get_device_state_success_case01(self, ome_connection_powerstate_mock, ome_response_mock):
        json_data = {
            "report_list": [{"Id": Constants.device_id1, "PowerState": "on", "Type": 1000}]}
        ome_response_mock.status_code = 200
        ome_response_mock.success = True
        f_module = self.get_module_mock()
        data = self.module.get_device_state(f_module, json_data, Constants.device_id1)
        assert data == ("on", 1000)

    def test_get_device_state_fail_case01(self, ome_connection_powerstate_mock, ome_response_mock):
        json_data = {
            "report_list": [{"Id": Constants.device_id1, "PowerState": "on", "Type": 4000}]}
        ome_response_mock.status_code = 500
        ome_response_mock.success = False
        f_module = self.get_module_mock()
        with pytest.raises(Exception) as exc:
            self.module.get_device_state(f_module, json_data, Constants.device_id1)
        assert exc.value.args[0] == "Unable to complete the operation because power" \
                                    " state supports device type 1000 and 2000."

    def test_get_device_state_fail_case02(self, ome_connection_powerstate_mock, ome_response_mock):
        json_data = {
            "report_list": [{"Id": 1224, "power_state": "on", "Type": 1000}]}
        f_module = self.get_module_mock()
        with pytest.raises(Exception) as exc:
            self.module.get_device_state(f_module, json_data, Constants.device_id1)
        assert exc.value.args[0] == "Unable to complete the operation because the entered target" \
                                    " device id '{0}' is invalid.".format(1234)

    def test_main_powerstate_success_case01(self, ome_default_args, mocker, ome_connection_powerstate_mock,
                                            ome_response_mock):
        mocker.patch(
            MODULE_PATH + 'ome_powerstate.get_device_resource',
            return_value={"Repository": "payload"})
        ome_default_args.update({"device_id": "11111", "power_state": "off"})
        ome_response_mock.success = True
        ome_response_mock.json_data = {"value": [{"device_id": "11111", "power_state": "off"}]}
        ome_response_mock.status_code = 200
        data = self._run_module(ome_default_args)
        assert data['changed'] is True
        assert data['msg'] == "Power State operation job submitted successfully."

    def test_main_powerstate_success_case02(self, ome_default_args, mocker, ome_connection_powerstate_mock,
                                            ome_response_mock):
        mocker.patch(MODULE_PATH + 'ome_powerstate.get_device_resource',
                     return_value={"Repository": "payload"})
        ome_default_args.update({"device_service_tag": "KLBR111", "power_state": "on"})
        ome_response_mock.success = True
        ome_response_mock.json_data = {"value": [{"device_id": "11111", "power_state": "on"}]}
        ome_response_mock.status_code = 200
        data = self._run_module(ome_default_args)
        assert data['changed'] is True
        assert data['msg'] == "Power State operation job submitted successfully."

    def test_main_powerstate_failure_case(self, ome_default_args, mocker, ome_connection_powerstate_mock,
                                          ome_response_mock):
        mocker.patch(MODULE_PATH + 'ome_powerstate.get_device_resource',
                     return_value={"Repository": "payload"})
        mocker.patch(MODULE_PATH + 'ome_powerstate.spawn_update_job',
                     return_value="payload")
        ome_default_args.update({"device_service_tag": None, "power_state": "on"})
        ome_response_mock.json_data = {"value": [{"device_service_tag": None, "power_state": "on"}]}
        ome_response_mock.status_code = 500
        data = self._run_module_with_fail_json(ome_default_args)
        assert data['msg'] == "device_id and device_service_tag attributes should not be None."

    def test_get_device_resource_success_case01(self, mocker, ome_default_args, ome_connection_powerstate_mock,
                                                ome_response_mock):
        ome_default_args.update({"device_id": Constants.service_tag1, "power_state": "on", "Type": 1000,
                                 "device_service_tag": Constants.service_tag1})
        mocker.patch(MODULE_PATH + 'ome_powerstate.get_device_state',
                     return_value=('on', 1000))
        mocker.patch(MODULE_PATH + 'ome_powerstate.build_power_state_payload',
                     return_value={'Id': 0, 'JobDescription': 'DeviceAction_Task',
                                   'JobName': 'DeviceAction_Task_PowerState',
                                   'JobType': {'Id': 3, 'Name': 'DeviceAction_Task'},
                                   'Params': [{'Key': 'operationName', 'Value': 'POWER_CONTROL'},
                                              {'Key': 'powerState', 'Value': '2000'}],
                                   'Schedule': 'startnow',
                                   'State': 'Enabled',
                                   'Targets': [{'Data': '',
                                                'Id': 1234,
                                                'TargetType': {'Id': 'off',
                                                               'Name': 'DEVICE'}}]})
        ome_connection_powerstate_mock.get_all_report_details.return_value = {
            'report_list': [{"DeviceServiceTag": Constants.service_tag1, "Id": Constants.service_tag1,
                             "power_state": "on"}]}
        f_module = self.get_module_mock(params=ome_default_args)
        f_module.check_mode = False
        data = self.module.get_device_resource(f_module, ome_connection_powerstate_mock)
        assert data == {'Id': 0, 'JobDescription': 'DeviceAction_Task', 'JobName': 'DeviceAction_Task_PowerState',
                        'JobType': {'Id': 3, 'Name': 'DeviceAction_Task'},
                        'Params': [{'Key': 'operationName', 'Value': 'POWER_CONTROL'},
                                   {'Key': 'powerState', 'Value': '2000'}],
                        'Schedule': 'startnow',
                        'State': 'Enabled',
                        'Targets': [{'Data': '',
                                     'Id': 1234,
                                     'TargetType': {'Id': 'off',
                                                    'Name': 'DEVICE'}}]}

    def test_get_device_resource_success_case02(self, mocker, ome_default_args, ome_connection_powerstate_mock,
                                                ome_response_mock):
        ome_default_args.update({"device_id": Constants.service_tag1, "power_state": "on", "Type": 1000,
                                 "device_service_tag": Constants.service_tag1})
        mocker.patch(MODULE_PATH + 'ome_powerstate.get_device_state',
                     return_value=('on', 1000))
        mocker.patch(MODULE_PATH + 'ome_powerstate.build_power_state_payload',
                     return_value={'Id': 0, 'JobDescription': 'DeviceAction_Task',
                                   'JobName': 'DeviceAction_Task_PowerState',
                                   'JobType': {'Id': 3, 'Name': 'DeviceAction_Task'},
                                   'Params': [{'Key': 'operationName', 'Value': 'POWER_CONTROL'},
                                              {'Key': 'powerState', 'Value': '2000'}],
                                   'Schedule': 'startnow',
                                   'State': 'Enabled',
                                   'Targets': [{'Data': '',
                                                'Id': 1234,
                                                'TargetType': {'Id': 'off',
                                                               'Name': 'DEVICE'}}]})
        ome_connection_powerstate_mock.get_all_report_details.return_value = {
            'report_list': [{"DeviceServiceTag": None, "Id": Constants.service_tag1,
                             "power_state": "on"}]}
        f_module = self.get_module_mock(params=ome_default_args, check_mode=False)
        with pytest.raises(Exception) as exc:
            self.module.get_device_resource(f_module, ome_connection_powerstate_mock)
        assert exc.value.args[0] == "Unable to complete the operation because the entered target device " \
                                    "service tag 'MXL1234' is invalid."

    def test_get_device_resource_success_case03(self, mocker, ome_default_args, ome_connection_powerstate_mock,
                                                ome_response_mock):
        ome_default_args.update({"device_id": Constants.service_tag1, "power_state": "coldboot", "Type": 1000,
                                 "device_service_tag": Constants.service_tag1})
        mocker.patch(MODULE_PATH + 'ome_powerstate.get_device_state',
                     return_value=('off', 1000))
        mocker.patch(MODULE_PATH + 'ome_powerstate.build_power_state_payload',
                     return_value={'Id': 0, 'JobDescription': 'DeviceAction_Task',
                                   'JobName': 'DeviceAction_Task_PowerState',
                                   'JobType': {'Id': 3, 'Name': 'DeviceAction_Task'},
                                   'Params': [{'Key': 'operationName', 'Value': 'POWER_CONTROL'},
                                              {'Key': 'powerState', 'Value': '2000'}],
                                   'Schedule': 'startnow',
                                   'State': 'Enabled',
                                   'Targets': [{'Data': '',
                                                'Id': 1234,
                                                'TargetType': {'Id': 'off',
                                                               'Name': 'DEVICE'}}]})
        ome_connection_powerstate_mock.get_all_report_details.return_value = {
            'report_list': [{"DeviceServiceTag": Constants.service_tag1, "Id": Constants.service_tag1,
                             "power_state": "coldboot"}]}
        ome_response_mock.success = True
        f_module = self.get_module_mock(params=ome_default_args, check_mode=True)
        with pytest.raises(Exception) as exc:
            self.module.get_device_resource(f_module, ome_connection_powerstate_mock)
        assert exc.value.args[0] == "No changes found to commit."

    def test_get_device_resource_success_case04(self, mocker, ome_default_args, ome_connection_powerstate_mock,
                                                ome_response_mock):
        ome_default_args.update({"device_id": Constants.service_tag1, "power_state": "on", "Type": 1000,
                                 "device_service_tag": Constants.service_tag1})
        mocker.patch(MODULE_PATH + 'ome_powerstate.get_device_state',
                     return_value=(2, 1000))
        mocker.patch(MODULE_PATH + 'ome_powerstate.build_power_state_payload',
                     return_value={'Id': 0, 'JobDescription': 'DeviceAction_Task',
                                   'JobName': 'DeviceAction_Task_PowerState',
                                   'JobType': {'Id': 3, 'Name': 'DeviceAction_Task'},
                                   'Params': [{'Key': 'operationName', 'Value': 'POWER_CONTROL'},
                                              {'Key': 'powerState', 'Value': '2000'}],
                                   'Schedule': 'startnow',
                                   'State': 'Enabled',
                                   'Targets': [{'Data': '',
                                                'Id': 1234,
                                                'TargetType': {'Id': 'off',
                                                               'Name': 'DEVICE'}}]})
        ome_connection_powerstate_mock.get_all_report_details.return_value = {
            'report_list': [
                {"DeviceServiceTag": Constants.service_tag1,
                 "Id": Constants.service_tag1, "power_state": "on"
                 }
            ]
        }
        f_module = self.get_module_mock(params=ome_default_args, check_mode=True)
        with pytest.raises(Exception) as exc:
            self.module.get_device_resource(f_module, ome_connection_powerstate_mock)
        assert exc.value.args[0] == "No changes found to commit."

    def test_get_device_resource_failed_case01(self, mocker, ome_default_args, ome_connection_powerstate_mock,
                                               ome_response_mock):
        ome_default_args.update({"device_id": None, "power_state": "on", "Type": 1000,
                                 "device_service_tag": "@#4"})
        mocker.patch(MODULE_PATH + 'ome_powerstate.get_device_state',
                     return_value=('on', 1000))
        ome_connection_powerstate_mock.get_all_report_details.return_value = {
            'report_list': [{"DeviceServiceTag": "@#4", "Id": None,
                             "power_state": "on"}]}
        f_module = self.get_module_mock(params=ome_default_args, check_mode=True)
        with pytest.raises(Exception) as exc:
            self.module.get_device_resource(f_module, ome_connection_powerstate_mock)
        assert exc.value.args[0] == "Changes found to commit."

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_powerstate_main_exception_case(self, exc_type, mocker, ome_default_args,
                                            ome_connection_powerstate_mock,
                                            ome_response_mock):
        ome_default_args.update({"device_service_tag": Constants.service_tag1, "power_state": "on"})
        ome_response_mock.json_data = {"value": [{"device_service_tag": Constants.service_tag1, "power_state": "on",
                                                  "Id": Constants.device_id1}]}
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(
                MODULE_PATH + 'ome_powerstate.get_device_resource',
                side_effect=exc_type('test'))
            mocker.patch(
                MODULE_PATH + 'ome_powerstate.spawn_update_job',
                side_effect=exc_type('test'))
        else:
            mocker.patch(
                MODULE_PATH + 'ome_powerstate.spawn_update_job',
                side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                     {"accept-type": "application/json"}, StringIO(json_str)))
            mocker.patch(
                MODULE_PATH + 'ome_powerstate.get_device_resource',
                side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                     {"accept-type": "application/json"}, StringIO(json_str)))
        result = self._run_module_with_fail_json(ome_default_args)
        assert 'power_state' not in result
        assert 'msg' in result
        assert result['failed'] is True
        if exc_type == HTTPError:
            assert 'msg' in result
