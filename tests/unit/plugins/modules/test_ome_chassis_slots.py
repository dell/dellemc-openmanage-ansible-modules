# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.1
# Copyright (C) 2021-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
import pytest
from ssl import SSLError
from io import StringIO
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils._text import to_text
from ansible_collections.dellemc.openmanage.plugins.modules import ome_chassis_slots
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, AnsibleFailJSonException

DEVICE_REPEATED = "Duplicate device entry found for devices with identifiers {0}."
CHASSIS_REPEATED = "Duplicate chassis entry found for chassis with service tags {0}."
CHASSIS_TAG_INVALID = "Provided chassis {0} is invalid."
INVALID_SLOT_DEVICE = "Unable to rename one or more slots because either the specified device is invalid or slots " \
                      "cannot be configured. The devices for which the slots cannot be renamed are: {0}."
JOBS_TRIG_FAIL = "Unable to initiate the slot name rename jobs."
SUCCESS_MSG = "Successfully renamed the slot(s)."
SUCCESS_REFRESH_MSG = "The rename slot job(s) completed successfully. " \
                      "For changes to reflect, refresh the inventory task manually."
FAILED_MSG = "Failed to rename {0} of {1} slot names."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
INVALID_SLOT_NUMBERS = "Unable to rename one or more slots because the slot number(s) are invalid: {0}."
SLOT_NUM_DUP = "Slot numbers are repeated for chassis {0}."

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_chassis_slots.'
MODULE_UTIL_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.ome.'


@pytest.fixture
def ome_connection_mock_for_chassis_slots(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeChassisSlots(FakeAnsibleModule):
    module = ome_chassis_slots

    def _run_config_error_test(self, params, ome_response_mock, ome_connection_mock, ome_default_args):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        ome_connection_mock.get_all_items_with_pagination.return_value = params["json_data"]
        ome_default_args.update(params["mparams"])
        return self._run_module(ome_default_args)

    @pytest.mark.parametrize("params", [{'mparams': {"device_options": [
        {"slot_name": "t1",
         "device_service_tag": "ABCD1234"}]},
        "invalid_list": set(["ABCD1234"]), "json_data": {
        "value": [{"Id": 10053, "Identifier": "2H5DNX2", "SlotConfiguration": {"ChassisName": None}},
                  {"Id": 10054, "Type": 1000, "Identifier": "2H7HNX2",
                   "SlotConfiguration": {"DeviceType": "1000", "ChassisId": "10053", "SlotNumber": "1",
                                         "SlotName": "my_840c", "SlotType": "2000"}}]},
        'message': INVALID_SLOT_DEVICE, "success": True},
        {'mparams': {"device_options": [{"slot_name": "s1", "device_id": 10054},
                                        {"slot_name": "s2",
                                            "device_service_tag": "ABCD1234"},
                                        {"slot_name": "s1", "device_id": 10052},
                                        ]},
         "invalid_list": set(["ABCD1234"]),
         "json_data":
         {"value": [{"Id": 10053, "Identifier": "2H5DNX2",
                     "SlotConfiguration": {"ChassisName": None}},
                    {"Id": 10054, "Type": 1000, "Identifier": "ABCD1234",
                     "SlotConfiguration": {"DeviceType": "1000", "ChassisId": "10053", "SlotNumber": "1",
                                           "SlotName": "my_840c", "SlotType": "2000"}}]}, 'message': DEVICE_REPEATED,
         "success": True}, {
        'mparams': {"device_options": [{"slot_name": "s1", "device_id": 10054},
                                       {"slot_name": "s2",
                                        "device_service_tag": "ABCD1234"},
                                       {"slot_name": "s2",
                                        "device_service_tag": "ABCD1234"},
                                       {"slot_name": "s2",
                                        "device_service_tag": "PQRS1234"}, ]},
        "invalid_list": set(["ABCD1234"]), "json_data": {
            "value": [{"Id": 10053, "Identifier": "2H5DNX2", "SlotConfiguration": {"ChassisName": None}},
                      {"Id": 10052, "Type": 1000, "Identifier": "PQRS1234",
                       "SlotConfiguration": {"DeviceType": "1000", "ChassisId": "10053", "SlotNumber": "1",
                                             "SlotName": "my_840c", "SlotType": "2000"}},
                      {"Id": 10054, "Type": 1000, "Identifier": "ABCD1234",
                       "SlotConfiguration": {"DeviceType": "1000", "ChassisId": "10053", "SlotNumber": "1",
                                             "SlotName": "my_840c", "SlotType": "2000"}}]}, 'message': DEVICE_REPEATED,
        "success": True},
        {
        'mparams': {"device_options": []},
        "invalid_list": set(["ABCD1234"]), "json_data": {
            "value": [{"Id": 10053, "Identifier": "2H5DNX2", "SlotConfiguration": {"ChassisName": None}},
                      {"Id": 10052, "Type": 1000, "Identifier": "PQRS1234",
                       "SlotConfiguration": {"DeviceType": "1000", "ChassisId": "10053", "SlotNumber": "1",
                                             "SlotName": "my_840c", "SlotType": "2000"}},
                      {"Id": 10054, "Type": 1000, "Identifier": "ABCD1234",
                       "SlotConfiguration": {"DeviceType": "1000", "ChassisId": "10053", "SlotNumber": "1",
                                             "SlotName": "my_840c", "SlotType": "2000"}}]}, 'message': NO_CHANGES_MSG,
        "success": True},
        {
        "mparams": {"slot_options": [{"chassis_service_tag": "ABC1234",
                                      "slots": [{"slot_name": "t1", "slot_number": 1}, {"slot_name": "s1", "slot_number": 5}]},
                                     {"chassis_service_tag": "ABC1234",
                                      "slots": [{"slot_name": "t2", "slot_number": 2}, {"slot_name": "s2", "slot_number": 6}]}]},
        "invalid_list": {"ABC1234"},
        "json_data": {
            "value": [{"Id": 10053, "Identifier": "2H5DNX2", "SlotConfiguration": {"ChassisName": None}},
                      {"Id": 10054, "Type": 1000, "Identifier": "ABCD1234",
                       "SlotConfiguration": {"DeviceType": "1000", "ChassisId": "10053", "SlotNumber": "1", "SlotName": "my_840c", "SlotType": "2000"}}]},
        "message": CHASSIS_REPEATED,
        "success": True},
        {
        "mparams": {
            "slot_options": [
                {
                    "chassis_service_tag": "ABC1234",
                    "slots": [
                        {"slot_name": "t1", "slot_number": 1},
                        {"slot_name": "s1", "slot_number": 5},
                    ],
                },
                {
                    "chassis_service_tag": "ABC1235",
                    "slots": [
                        {"slot_name": "t2", "slot_number": 2},
                        {"slot_name": "s2", "slot_number": 6},
                    ],
                },
            ]},
        "invalid_list": {"ABC1234"},
        "json_data": {
            "value": [
                {
                    "Id": 10053,
                    "Identifier": "2H5DNX2",
                    "SlotConfiguration": {"ChassisName": None},
                },
                {
                    "Id": 10054,
                    "Type": 1000,
                    "Identifier": "ABCD1234",
                    "SlotConfiguration": {
                        "DeviceType": "1000",
                        "ChassisId": "10053",
                        "SlotNumber": "1",
                        "SlotName": "my_840c",
                        "SlotType": "2000",
                    },
                },
            ]
        },
        "message": CHASSIS_TAG_INVALID,
        "success": True},
        {
        'mparams': {"device_options": [{"slot_name": "s2", "device_service_tag": "PQRS1234"}]},
        "invalid_list": set(["PQRS1234"]),
        "json_data": {
            "value": [{"Id": 10053, "Identifier": "2H5DNX2"},
                      {"Id": 10052, "Type": 1000, "Identifier": "PQRS1234"},
                      {"Id": 10054, "Type": 1000, "Identifier": "ABCD1234"}]},
        'message': INVALID_SLOT_DEVICE,
        "success": True},
        {
        'mparams': {"device_options": [{"slot_name": "s2", "device_id": 10054}]},
        "invalid_list": set(["10054"]),
        "json_data": {
            "value": [{"Id": 10053, "Identifier": "2H5DNX2"},
                      {"Id": 10052, "Type": 1000, "Identifier": "PQRS1234"},
                      {"Id": 10054, "Type": 1000, "Identifier": "ABCD1234"}]},
        'message': INVALID_SLOT_DEVICE,
        "success": True},
    ])
    def test_get_device_slot_config_errors(self, params, ome_connection_mock_for_chassis_slots, ome_response_mock, ome_default_args, module_mock):
        # Test device slot config error
        result = self._run_config_error_test(params, ome_response_mock, ome_connection_mock_for_chassis_slots, ome_default_args)
        expected_msg = params["message"].format(';'.join(set(params.get("invalid_list"))))
        assert result["msg"] == expected_msg

    @pytest.mark.parametrize("params", [{"json_data": {'Name': 'j1', 'Id': 24}, "slot_data": {
        "ABC1234": {"ChassisId": "123", "SlotNumber": "1", "SlotType": "2000"}}, "failed_jobs": {}}])
    def test_start_slot_name_jobs(
            self, params, ome_connection_mock_for_chassis_slots, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        # ome_connection_mock_for_chassis_slots.job_submission.return_value = params['json_data']
        ome_response_mock.json_data = params["json_data"]
        failed_jobs = self.module.start_slot_name_jobs(
            ome_connection_mock_for_chassis_slots, params.get('slot_data'))
        assert failed_jobs == params['failed_jobs']

    @pytest.mark.parametrize("params", [
        {"json_data": {"value": [{'Name': 'j1', 'Id': 12, "LastRunStatus": {"Id": 2060, "Name": "Completed"}}]},
         "slot_data": {"ABC1234": {"new_name": "s1", "SlotNumber": "1", "SlotType": "2000", "JobId": 12}},
         "failed_jobs": {}}])
    def test_get_job_states(
            self, params, ome_connection_mock_for_chassis_slots, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        f_module = self.get_module_mock()
        ome_response_mock.json_data = params["json_data"]
        failed_jobs = self.module.get_job_states(f_module, ome_connection_mock_for_chassis_slots,
                                                 params.get('slot_data'))
        assert failed_jobs == params['failed_jobs']

    @pytest.mark.parametrize("params", [{'mparams': {"device_options": [{"slot_name": "my_840c", "device_id": 10054},
                                                                        {"slot_name": "my_740c",
                                                                         "device_service_tag": "ABCD1234"}]},
                                         "json_data": {"value": [{"Id": 10053, "Identifier": "ABCD1234",
                                                                  "SlotConfiguration": {"DeviceType": "1000",
                                                                                        "ChassisId": "10053",
                                                                                        "SlotNumber": "1",
                                                                                        "SlotName": "my_740c",
                                                                                        "SlotType": "2000"}},
                                                                 {"Id": 10054, "Type": 1000, "Identifier": "PQRS1234",
                                                                  "SlotConfiguration": {"DeviceType": "1000",
                                                                                        "ChassisId": "10053",
                                                                                        "SlotNumber": "1",
                                                                                        "SlotName": "my_840c",
                                                                                        "SlotType": "2000"}}]},
                                         'message': NO_CHANGES_MSG, "check_mode": True}, {'mparams': {
                                             "device_options": [{"slot_name": "my_840", "device_id": 10054},
                                                                {"slot_name": "my_740",
                                                                 "device_service_tag": "ABCD1234"}]},
        "json_data": {"value": [{"Id": 10053, "Identifier": "ABCD1234",
                                 "SlotConfiguration": {"DeviceType": "1000",
                                                       "ChassisId": "10053", "SlotNumber": "1", "SlotName": "my_740c",
                                                       "SlotType": "2000"}},
                                {"Id": 10054, "Type": 1000, "Identifier": "PQRS1234",
                                 "SlotConfiguration": {"DeviceType": "1000", "ChassisId": "10053", "SlotNumber": "1",
                                                       "SlotName": "my_840c", "SlotType": "2000"}}]},
        'message': CHANGES_FOUND, "check_mode": True}, ])
    def test_check_mode_idempotency(
            self, params, ome_connection_mock_for_chassis_slots, ome_default_args):
        ome_connection_mock_for_chassis_slots.get_all_items_with_pagination.return_value = params[
            'json_data']
        ome_default_args.update(params['mparams'])
        result = self._run_module(
            ome_default_args, check_mode=params.get(
                'check_mode', False))
        assert result['msg'] == params['message']

    @pytest.mark.parametrize("params", [{'mparams': {"device_options": [{"slot_name": "t1", "device_id": 10053},
                                                                        {"slot_name": "t1",
                                                                         "device_service_tag": "ABCD1234"}]},
                                         "json_data": {"value": [{"Id": 10053, "Identifier": "2H5DNX2",
                                                                  "SlotConfiguration": {"DeviceType": "1000",
                                                                                        "ChassisId": "10053",
                                                                                        "SlotNumber": "1",
                                                                                        "SlotName": "my_840c",
                                                                                        "SlotType": "2000"}},
                                                                 {"Id": 10054, "Identifier": "ABCD1234",
                                                                  "SlotConfiguration": {"DeviceType": "1000",
                                                                                        "ChassisId": "10053",
                                                                                        "SlotNumber": "1",
                                                                                        "SlotName": "my_840c",
                                                                                        "SlotType": "2000"}}], },
                                         'message': SUCCESS_MSG, "success": True}])
    def test_ome_chassis_slots_success_case(self, params, ome_connection_mock_for_chassis_slots, ome_response_mock,
                                            ome_default_args, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_connection_mock_for_chassis_slots.get_all_items_with_pagination.return_value = params[
            'json_data']
        ome_connection_mock_for_chassis_slots.job_tracking.return_value = (
            False, "job_track_msg")
        mocker.patch(
            MODULE_PATH +
            'trigger_refresh_inventory',
            return_value=[1])
        mocker.patch(
            MODULE_PATH +
            'start_slot_name_jobs',
            return_value=params.get(
                'start_slot_name_jobs',
                {}))
        mocker.patch(
            MODULE_PATH +
            'get_job_states',
            return_value=params.get(
                'get_job_states',
                {}))
        ome_default_args.update(params['mparams'])
        result = self._run_module(
            ome_default_args, check_mode=params.get(
                'check_mode', False))
        assert result['msg'] == params['message']

    @pytest.mark.parametrize("params", [{'mparams': {"slot_options": [{"chassis_service_tag": "ABC1234",
                                                                       "slots": [{"slot_name": "t1", "slot_number": 1},
                                                                                 {"slot_name": "s1",
                                                                                  "slot_number": 5}]}]},
                                         "chassi": {'value': [{"Identifier": "ABC1234", "Id": 1234}]},
                                         "bladeslots": {'ABC1234_1': {"SlotNumber": "1", "SlotName": "myslotty"}},
                                         "storageslots": {'value': [{"SlotNumber": "5", "SlotName": "stor-slot1"}]},
                                         "slot_data": {"ABC1234_1": {"SlotNumber": "1", "SlotName": "myslotty"}}}])
    def test_slot_number_config(self, params, ome_connection_mock_for_chassis_slots, ome_response_mock,
                                ome_default_args, mocker):
        mocker.patch(
            MODULE_PATH + 'get_device_type',
            return_value=params.get('chassi'))
        mocker.patch(
            MODULE_PATH + 'get_slot_data',
            return_value=params.get('bladeslots'))
        f_module = self.get_module_mock(params=params["mparams"])
        slot_data = self.module.slot_number_config(
            f_module, ome_connection_mock_for_chassis_slots)
        assert slot_data == params['slot_data']

    @pytest.mark.parametrize("params", [{"slot_options": {"chassis_service_tag": "ABC1234",
                                                          "slots": [{"slot_name": "t1", "slot_number": 1},
                                                                    {"slot_name": "s1", "slot_number": 5}]},
                                         "chass_id": 1234, "chassi": {'value': [{"Identifier": "ABC1234", "Id": 1234}]},
                                         "bladeslots": {'value': [{"SlotNumber": "1", "SlotName": "blade-slot1",
                                                                   "Id": 234}]},
                                         "storageslots": {'value': [{"ChassisServiceTag": "ABC1234",
                                                                     "SlotConfiguration": {
                                                                         "SlotId": "123", "SlotNumber": "5",
                                                                         "SlotName": "stor-slot1"}}]},
                                         "slot_dict_diff": {'ABC1234_5': {'SlotNumber': '5', 'SlotName': 'stor-slot1',
                                                                          'ChassisId': 1234, 'SlotId': "123",
                                                                          'ChassisServiceTag': 'ABC1234',
                                                                          'new_name': 's1'},
                                                            'ABC1234_1': {'SlotNumber': '1', 'SlotName': 'blade-slot1',
                                                                          'ChassisId': 1234, 'SlotId': "234",
                                                                          "Id": 234,
                                                                          'ChassisServiceTag': 'ABC1234',
                                                                          'new_name': 't1'}}}])
    def test_get_slot_data(self, params, ome_connection_mock_for_chassis_slots, ome_response_mock, ome_default_args,
                           mocker):
        mocker.patch(
            MODULE_PATH + 'get_device_type',
            return_value=params.get('storageslots'))
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["bladeslots"]
        ch_slots = params['slot_options']
        f_module = self.get_module_mock()
        slot_dict_diff = self.module.get_slot_data(f_module, ome_connection_mock_for_chassis_slots, ch_slots,
                                                   params['chass_id'])
        assert slot_dict_diff == params['slot_dict_diff']

    @pytest.mark.parametrize("params", [{"json_data": {'Name': 'j1', 'Id': 24}, "slot_data": {
        "ABC1234": {"ChassisId": "123", "SlotNumber": "1", "ChassisServiceTag": "ABC1234"}}, "jobs": [1]}])
    def test_trigger_refresh_inventory(
            self, params, ome_connection_mock_for_chassis_slots, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        jobs = self.module.trigger_refresh_inventory(
            ome_connection_mock_for_chassis_slots, params.get('slot_data'))
        assert jobs == params['jobs']

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_groups_main_exception_failure_case(self, exc_type, mocker, ome_default_args,
                                                    ome_connection_mock_for_chassis_slots, ome_response_mock):
        ome_default_args.update(
            {"device_options": [{"slot_name": "t1", "device_id": 1234}]})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(
                MODULE_PATH + 'get_device_slot_config',
                side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(
                MODULE_PATH + 'get_device_slot_config',
                side_effect=exc_type("exception message"))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'get_device_slot_config',
                         side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result

    @pytest.mark.parametrize(
        "params",
        [
            {
                "slot_options": {
                    "chassis_service_tag": "ABC1234",
                    "slots": [
                        {"slot_name": "t1", "slot_number": 1},
                        {"slot_name": "s1", "slot_number": 5},
                        {"slot_name": "s2", "slot_number": 6},
                    ],
                },
                "chass_id": 1234,
                "chassi": {
                    "value": [{"Identifier": "ABC1234", "Id": 1234}]
                },
                "bladeslots": {
                    "value": [{"SlotNumber": "1", "SlotName": "blade-slot1", "Id": 234}]
                },
                "invalid_list": {"6"},
                "message": INVALID_SLOT_NUMBERS,
                "storageslots": {
                    "value": [
                        {
                            "ChassisServiceTag": "ABC1234",
                            "SlotConfiguration": {
                                "SlotId": "123",
                                "SlotNumber": "5",
                                "SlotName": "stor-slot1",
                            },
                        }
                    ]
                },
            },
            {
                "slot_options": {
                    "chassis_service_tag": "ABC1234",
                    "slots": [
                        {"slot_name": "t1", "slot_number": 1},
                        {"slot_name": "s1", "slot_number": 5},
                        {"slot_name": "s1", "slot_number": 5},
                    ],
                },
                "chass_id": 1234,
                "chassi": {
                    "value": [{"Identifier": "ABC1234", "Id": 1234}]
                },
                "bladeslots": {
                    "value": [{"SlotNumber": "1", "SlotName": "blade-slot1", "Id": 234}]
                },
                "invalid_list": {"ABC1234"},
                "message": SLOT_NUM_DUP,
                "storageslots": {
                    "value": [
                        {
                            "ChassisServiceTag": "ABC1234",
                            "SlotConfiguration": {
                                "SlotId": "123",
                                "SlotNumber": "5",
                                "SlotName": "stor-slot1",
                            },
                        }
                    ]
                },
            },
        ]
    )
    def test_invalid_slot_numbers(self, params, ome_connection_mock_for_chassis_slots, ome_response_mock, mocker):
        mocker.patch(
            MODULE_PATH + 'get_device_type',
            return_value=params.get('storageslots'))
        ome_response_mock.json_data = params["bladeslots"]
        ch_slots = params['slot_options']
        f_module = self.get_module_mock()
        with pytest.raises(AnsibleFailJSonException) as exc_info:
            self.module.get_slot_data(f_module, ome_connection_mock_for_chassis_slots, ch_slots, params['chass_id'])

        # Validate the error message
        expected_msg = params['message'].format(';'.join(params['invalid_list']))
        assert str(exc_info.value) == expected_msg
