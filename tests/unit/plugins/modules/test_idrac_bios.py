# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 6.2.0
# Copyright (C) 2018-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_bios
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_bios.'

BIOS_JOB_RUNNING = "BIOS Config job is running. Wait for the job to complete."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_MSG = "Changes found to be applied."
SUCCESS_CLEAR = "Successfully cleared the pending BIOS attributes."
SUCCESS_COMPLETE = "Successfully applied the BIOS attributes update."
SCHEDULED_SUCCESS = "Successfully scheduled the job for the BIOS attributes update."
COMMITTED_SUCCESS = "Successfully committed changes. The job is in pending state. The changes will be applied {0}"
RESET_TRIGGERRED = "Reset BIOS action triggered successfully."
HOST_RESTART_FAILED = "Unable to restart the host. Check the host status and restart the host manually."
BIOS_RESET_TRIGGERED = "The BIOS reset action has been triggered successfully. The host reboot is complete."
BIOS_RESET_COMPLETE = "BIOS reset to defaults has been completed successfully."
BIOS_RESET_PENDING = "Pending attributes to be applied. " \
                     "Clear or apply the pending changes before resetting the BIOS."
FORCE_BIOS_DELETE = "The BIOS configuration job is scheduled. Use 'force' to delete the job."
INVALID_ATTRIBUTES_MSG = "The values specified for the attributes are invalid."
UNSUPPORTED_APPLY_TIME = "Apply time {0} is not supported."
MAINTENANCE_OFFSET = "The maintenance time must be post-fixed with local offset to {0}."
MAINTENANCE_TIME = "The specified maintenance time window occurs in the past, " \
                   "provide a future time to schedule the maintenance window."


@pytest.fixture
def idrac_redfish_mock_for_bios(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestConfigBios(FakeAnsibleModule):
    module = idrac_bios

    @pytest.mark.parametrize("params", [
        {"json_data": {"Attributes": {}}, 'message': NO_CHANGES_MSG,
         "success": True, 'mparams': {'clear_pending': True}},
        {"json_data": {"Attributes": {}}, 'message': NO_CHANGES_MSG,
         "success": True, 'mparams': {'clear_pending': True}, "check_mode": True},
        {"json_data": {"Attributes": {"test": "value"}}, 'message': BIOS_JOB_RUNNING,
         "success": True, 'mparams': {'clear_pending': True},
         "check_scheduled_bios_job": ("job1", "Running")},
        {"json_data": {"Attributes": {"test": "value"}}, 'message': BIOS_JOB_RUNNING,
         "success": True, 'mparams': {'clear_pending': True},
         "check_scheduled_bios_job": ("job1", "Starting")},
        {"json_data": {"Attributes": {"test": "value"}}, 'message': SUCCESS_CLEAR,
         "success": True, 'mparams': {'clear_pending': True},
         "check_scheduled_bios_job": ("job1", "Scheduled")},
        {"json_data": {"Attributes": {"test": "value"}}, 'message': CHANGES_MSG,
         "success": True, 'mparams': {'clear_pending': True},
         "check_scheduled_bios_job": ("job1", "Scheduled"), "check_mode": True},
        {"json_data": {"Attributes": {"test": "value"}}, 'message': CHANGES_MSG,
         "success": True, 'mparams': {'clear_pending': True},
         "check_scheduled_bios_job": ("job1", "Scheduler"), "check_mode": True},
        {"json_data": {"Attributes": {"test": "value"}}, 'message': SUCCESS_CLEAR,
         "success": True, 'mparams': {'clear_pending': True},
         "check_scheduled_bios_job": (None, "Scheduled")},
        {"json_data": {"Attributes": {"test": "value"}}, 'message': CHANGES_MSG,
         "success": True, 'mparams': {'clear_pending': True},
         "check_scheduled_bios_job": (None, "Scheduled"), "check_mode": True},
        {"json_data": {"Attributes": {"test": "value"},
                       "Members": [
                           {"Id": "job_1", "JobType": "RAIDConfiguration", "JobState": "Scheduled"},
                           {"Id": "job_1", "JobType": "BIOSConfiguration", "JobState": "Scheduled"}]},
         'message': SUCCESS_CLEAR,
         "success": True, 'mparams': {'clear_pending': True}},
        {"json_data": {"Attributes": {"test": "value"},
                       "Members": [{"Id": "job_1", "JobType": "BIOSConfiguration", "JobState": "Running"}]},
         'message': BIOS_JOB_RUNNING,
         "success": True, 'mparams': {'clear_pending': True}},
        {"json_data": {"Attributes": {"test": "value"},
                       "Members": [{"Id": "job_1", "JobType": "BIOSConfiguration", "JobState": "Starting"}]},
         'message': BIOS_JOB_RUNNING,
         "success": True, 'mparams': {'clear_pending': True}},
    ])
    def test_idrac_bios_clear_pending(self, params, idrac_redfish_mock_for_bios, ome_response_mock, idrac_default_args,
                                      mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params.get('json_data')
        mocks = ["get_pending_attributes", "check_scheduled_bios_job", "delete_scheduled_bios_job"]
        for m in mocks:
            if m in params:
                mocker.patch(MODULE_PATH + m, return_value=params.get(m, {}))
        idrac_default_args.update(params['mparams'])
        result = self._run_module(idrac_default_args, check_mode=params.get('check_mode', False))
        assert result['status_msg'] == params['message']

    @pytest.mark.parametrize("params", [
        {"json_data": {"Attributes": {}}, 'message': BIOS_RESET_TRIGGERED,
         "reset_host": True,
         "success": True, 'mparams': {'reset_bios': True}},
        {"json_data": {"Attributes": {"BootMode": "Uefi"}}, 'message': BIOS_RESET_PENDING,
         "reset_host": True,
         "success": True, 'mparams': {'reset_bios': True}},
        {"json_data": {"DateTime": "2022-09-14T05:59:35-05:00",
                       "DateTimeLocalOffset": "-05:00",
                       "Members": [{"Created": "2022-09-14T05:59:20-05:00", "MessageId": "SYS1003"},
                                   {"Created": "2022-09-14T05:59:10-05:00", "MessageId": "UEFI0157"},
                                   {"Created": "2022-09-14T05:59:30-05:00", "MessageId": "SYS1002"}],
                       "Entries": {
                           "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Lclog/Entries"
                       },
                       "Attributes": {}},
         'message': BIOS_RESET_TRIGGERED, "reset_host": True,
         "success": True, 'mparams': {'reset_bios': True}},
        {"json_data": {"DateTime": "2022-09-14T05:59:35-05:00",
                       "DateTimeLocalOffset": "-05:00",
                       "Members": [{"Created": "2022-09-14T05:59:20-05:00", "MessageId": "SYS1003"},
                                   {"Created": "2022-09-14T05:59:10-05:00", "MessageId": "UEFI0157"},
                                   {"Created": "2022-09-14T05:59:40-05:00", "MessageId": "SYS1002"}],
                       "Entries": {
                           "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Lclog/Entries"
                       },
                       "Attributes": {}},
         'message': BIOS_RESET_COMPLETE, "reset_host": True,
         "success": True, 'mparams': {'reset_bios': True}},
        {"json_data": {"Attributes": {}}, 'message': CHANGES_MSG,
         "reset_host": True, "check_mode": True,
         "success": True, 'mparams': {'reset_bios': True}},
        {"json_data": {"PowerState": "On"}, 'message': BIOS_RESET_TRIGGERED,
         "success": True, 'mparams': {'reset_bios': True, "reset_type": "force_restart"}},
        {"json_data": {"PowerState": "Off"}, 'message': "{0} {1}".format(RESET_TRIGGERRED, HOST_RESTART_FAILED),
         "success": True, 'mparams': {'reset_bios': True}},
        {"json_data": {"PowerState": "On"}, 'message': HOST_RESTART_FAILED,
         "get_power_state": "On", "power_act_host": False,
         "success": True, 'mparams': {'reset_bios': True}},
        {"json_data": {"PowerState": "On"}, 'message': HOST_RESTART_FAILED,
         "get_power_state": "Off", "power_act_host": False,
         "success": True, 'mparams': {'reset_bios': True}},
    ])
    def test_idrac_bios_reset_bios(self, params, idrac_redfish_mock_for_bios, ome_response_mock, idrac_default_args,
                                   mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params.get('json_data')
        mocks = ["reset_host", "get_power_state", "track_power_state", "power_act_host"]
        for m in mocks:
            if m in params:
                mocker.patch(MODULE_PATH + m, return_value=params.get(m, {}))
        mocker.patch("ansible_collections.dellemc.openmanage.plugins.module_utils.utils." + 'time.sleep',
                     return_value=None)
        idrac_default_args.update(params['mparams'])
        result = self._run_module(idrac_default_args, check_mode=params.get('check_mode', False))
        assert result['status_msg'] == params['message']

    @pytest.mark.parametrize("params", [
        {"json_data": {"Attributes": {"NumLock": "On"}}, 'message': NO_CHANGES_MSG,
         "reset_host": True, "get_pending_attributes": {}, "validate_vs_registry": {},
         "success": True, 'mparams': {"attributes": {"NumLock": "On"}}},
        {"json_data": {"Attributes": {},
                       "RegistryEntries": {
                           "Attributes": [
                               {
                                   "AttributeName": "SystemModelName",
                                   "ReadOnly": True,
                                   "Type": "String"
                               }, {
                                   "AttributeName": "MemoryMode",
                                   "ReadOnly": False,
                                   "Type": "Enumeration",
                                   "Value": [
                                       {
                                           "ValueDisplayName": "Off",
                                           "ValueName": "PersistentMemoryOff"
                                       },
                                       {
                                           "ValueDisplayName": "Non-Volatile DIMM",
                                           "ValueName": "NVDIMM"
                                       }
                                   ],
                               }, {
                                   "AttributeName": "ValidEnum",
                                   "ReadOnly": False,
                                   "Type": "Enumeration",
                                   "Value": [
                                       {
                                           "ValueDisplayName": "Enabled",
                                           "ValueName": "On"
                                       },
                                       {
                                           "ValueDisplayName": "Disabled",
                                           "ValueName": "Off"
                                       }
                                   ],
                                   "WriteOnly": False
                               }, {
                                   "AttributeName": "IntSetting",
                                   "LowerBound": 0,
                                   "ReadOnly": False,
                                   "Type": "Integer",
                                   "UpperBound": 32,
                               }, {
                                   "AttributeName": "IntSetting3",
                                   "LowerBound": 0,
                                   "ReadOnly": False,
                                   "Type": "Integer",
                                   "UpperBound": 32,
                               }, {
                                   "AttributeName": "IntSetting2",
                                   "LowerBound": 0,
                                   "ReadOnly": False,
                                   "Type": "Integer",
                                   "UpperBound": 32,
                               }, ]}},
         'message': 'Job is in progress.',
         "reset_host": True,
         "get_pending_attributes": {},
         "idrac_redfish_job_tracking": (True, 'Job is in progress.', {}, 10),
         "success": True,
         'mparams': {"attributes": {"NumLock": "On", "SystemModelName": "new name", "MemoryMode": "DRAM",
                                    "IntSetting": 33, "IntSetting2": 'zero', "IntSetting3": 25,
                                    "ValidEnum": "On"}}},
        {"json_data": {"Attributes": {"NumLock": "On"}}, 'message': CHANGES_MSG,
         "reset_host": True, "get_pending_attributes": {}, "validate_vs_registry": {},
         "check_mode": True,
         "success": True, 'mparams': {"attributes": {"NumLock": "Off"}}},
        {"json_data": {
            "Attributes": {"NumLock": "On"},
            "@Redfish.Settings": {
                "SupportedApplyTimes": ["OnReset", "InMaintenanceWindowOnReset"]}},
            'message': UNSUPPORTED_APPLY_TIME.format('AtMaintenanceWindowStart'),
            "reset_host": True, "get_pending_attributes": {}, "validate_vs_registry": {},
            "success": True, 'mparams': {"attributes": {"NumLock": "Off"},
                                         "apply_time": 'AtMaintenanceWindowStart',
                                         "maintenance_window": {"start_time": '"2022-09-30T05:15:40-05:00"',
                                                                "duration": 600}}},
        {"json_data": {"DateTime": "2022-09-14T05:59:35-05:00",
                       "DateTimeLocalOffset": "-05:00",
                       "Attributes": {"NumLock": "On"},
                       "@Redfish.Settings": {
                           "SupportedApplyTimes": ["OnReset", 'AtMaintenanceWindowStart',
                                                   "InMaintenanceWindowOnReset"]}},
         'message': MAINTENANCE_OFFSET.format('-05:00'),
         "reset_host": True, "get_pending_attributes": {}, "validate_vs_registry": {},
         "success": True, 'mparams': {"attributes": {"NumLock": "Off"},
                                      "apply_time": 'AtMaintenanceWindowStart',
                                      "maintenance_window": {"start_time": '"2022-09-30T05:15:40-00:00"',
                                                             "duration": 600}}},
        {"json_data": {"DateTime": '2022-09-30T05:15:41-05:00',
                       "DateTimeLocalOffset": "-05:00",
                       "Attributes": {"NumLock": "On"},
                       "@Redfish.Settings": {
                           "SupportedApplyTimes": ["OnReset", 'AtMaintenanceWindowStart',
                                                   "InMaintenanceWindowOnReset"]}},
         'message': MAINTENANCE_TIME,
         "reset_host": True, "get_pending_attributes": {}, "validate_vs_registry": {},
         "success": True, 'mparams': {"attributes": {"NumLock": "Off"},
                                      "apply_time": 'AtMaintenanceWindowStart',
                                      "maintenance_window": {"start_time": '2022-09-30T05:15:40-05:00',
                                                             "duration": 600}}},
        {"json_data": {"DateTime": '2022-09-30T05:15:39-05:00',
                       "DateTimeLocalOffset": "-05:00",
                       "Attributes": {"NumLock": "On"},
                       "@Redfish.Settings": {
                           "SupportedApplyTimes": ["OnReset", 'AtMaintenanceWindowStart',
                                                   "InMaintenanceWindowOnReset"]}},
         'message': COMMITTED_SUCCESS.format('AtMaintenanceWindowStart'),
         "reset_host": True, "get_pending_attributes": {}, "validate_vs_registry": {},
         "success": True, 'mparams': {"attributes": {"NumLock": "Off"},
                                      "apply_time": 'AtMaintenanceWindowStart',
                                      "maintenance_window": {"start_time": '2022-09-30T05:15:40-05:00',
                                                             "duration": 600}}},
        {"json_data": {"DateTime": '2022-09-30T05:15:39-05:00',
                       "DateTimeLocalOffset": "-05:00",
                       "Attributes": {"NumLock": "On"},
                       "@Redfish.Settings": {
                           "SupportedApplyTimes": []}},
         'message': SCHEDULED_SUCCESS,
         "reset_host": True, "get_pending_attributes": {}, "validate_vs_registry": {},
         "success": True, 'mparams': {"attributes": {"NumLock": "Off"}, 'job_wait': False}},
        {"json_data": {"DateTime": '2022-09-30T05:15:39-05:00',
                       "DateTimeLocalOffset": "-05:00",
                       "Attributes": {"NumLock": "On"},
                       "@Redfish.Settings": {
                           "SupportedApplyTimes": ["OnReset", 'AtMaintenanceWindowStart',
                                                   "InMaintenanceWindowOnReset"]}},
         'message': SCHEDULED_SUCCESS,
         "reset_host": True, "get_pending_attributes": {}, "validate_vs_registry": {},
         "success": True, 'mparams': {"attributes": {"NumLock": "Off"}, 'job_wait': False}},
        {"json_data": {"DateTime": '2022-09-30T05:15:39-05:00',
                       "DateTimeLocalOffset": "-05:00",
                       "Attributes": {"NumLock": "On"},
                       "@Redfish.Settings": {
                           "SupportedApplyTimes": ["OnReset", 'AtMaintenanceWindowStart',
                                                   "InMaintenanceWindowOnReset"]}},
         'message': COMMITTED_SUCCESS.format('OnReset'),
         "reset_host": True, "get_pending_attributes": {}, "validate_vs_registry": {},
         "success": True, 'mparams': {"attributes": {"NumLock": "Off"}, 'apply_time': 'OnReset'}},
        {"json_data": {
            "Attributes": {"NumLock": "On"},
            "@Redfish.Settings": {
                "SupportedApplyTimes": ["OnReset", "AtMaintenanceWindowStart", "InMaintenanceWindowOnReset"]}},
            'message': BIOS_JOB_RUNNING,
            "reset_host": True, "get_pending_attributes": {"AssetTag": 'test'}, "validate_vs_registry": {},
            "check_scheduled_bios_job": ("job1", "Running"),
            "success": True, 'mparams': {"attributes": {"NumLock": "Off"}}},
        {"json_data": {
            "Attributes": {"NumLock": "On"},
            "@Redfish.Settings": {
                "SupportedApplyTimes": ["OnReset", "AtMaintenanceWindowStart", "InMaintenanceWindowOnReset"]}},
            'message': "Attributes committed but reboot has failed {0}".format(HOST_RESTART_FAILED),
            "reset_host": False, "get_pending_attributes": {"AssetTag": 'test'}, "validate_vs_registry": {},
            "check_scheduled_bios_job": ("job1", "Scheduled"), "apply_attributes": ("job1", True),
            "success": True, 'mparams': {"attributes": {"NumLock": "Off"}}},
        {"json_data": {
            "Attributes": {"NumLock": "On"},
            "@Redfish.Settings":
                {"SupportedApplyTimes": ["OnReset", "AtMaintenanceWindowStart", "InMaintenanceWindowOnReset"]}},
            'message': "Job Tracking Failed",
            "reset_host": True, "get_pending_attributes": {"AssetTag": 'test'}, "validate_vs_registry": {},
            "check_scheduled_bios_job": ("job1", "Scheduled"), "apply_attributes": ("job1", True),
            "idrac_redfish_job_tracking": (True, "Job Tracking Failed", {}, 10),
            "success": True, 'mparams': {"attributes": {"NumLock": "Off"}}},
        {"json_data": {
            "Attributes": {"NumLock": "On"},
            "@Redfish.Settings": {
                "SupportedApplyTimes": ["OnReset", "AtMaintenanceWindowStart", "InMaintenanceWindowOnReset"]}},
            'message': SUCCESS_COMPLETE,
            "reset_host": True, "get_pending_attributes": {"AssetTag": 'test'}, "validate_vs_registry": {},
            "check_scheduled_bios_job": ("job1", "Scheduled"), "apply_attributes": ("job1", True),
            "idrac_redfish_job_tracking": (False, "Job Tracking Failed", {}, 10),
            "success": True, 'mparams': {"attributes": {"NumLock": "Off"}}},
        {"json_data": {
            "Attributes": {"NumLock": "On"},
            "@Redfish.Settings": {
                "SupportedApplyTimes": ["OnReset", "AtMaintenanceWindowStart", "InMaintenanceWindowOnReset"]}},
            'message': SCHEDULED_SUCCESS,
            "reset_host": True, "get_pending_attributes": {"AssetTag": 'test'}, "validate_vs_registry": {},
            "check_scheduled_bios_job": ("job1", "Scheduled"), "apply_attributes": ("job1", True),
            "idrac_redfish_job_tracking": (False, "Job Tracking Failed", {}, 10),
            "success": True, 'mparams': {"attributes": {"NumLock": "Off"}, "job_wait": False}},
        {"json_data": {
            "Attributes": {"NumLock": "On"},
            "@Redfish.Settings": {
                "SupportedApplyTimes": ["OnReset", "AtMaintenanceWindowStart", "InMaintenanceWindowOnReset"]}},
            'message': COMMITTED_SUCCESS.format("Immediate"),
            "reset_host": False, "get_pending_attributes": {"AssetTag": 'test'}, "validate_vs_registry": {},
            "check_scheduled_bios_job": ("job1", "Scheduled"), "apply_attributes": (None, True),
            "success": True, 'mparams': {"attributes": {"NumLock": "Off"}}},
    ])
    def test_idrac_bios_attributes(self, params, idrac_redfish_mock_for_bios, ome_response_mock, idrac_default_args,
                                   mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params.get('json_data')
        ome_response_mock.headers = {'Location': 'job1'}
        mocks = ["get_current_attributes", "get_attributes_registry", "get_pending_attributes",
                 "check_scheduled_bios_job", "apply_attributes", "idrac_redfish_job_tracking",
                 "reset_host", "get_power_state", "track_power_state", "power_act_host"]
        for m in mocks:
            if m in params:
                mocker.patch(MODULE_PATH + m, return_value=params.get(m, {}))
        mocker.patch("ansible_collections.dellemc.openmanage.plugins.module_utils.utils." + 'time.sleep',
                     return_value=None)
        idrac_default_args.update(params['mparams'])
        result = self._run_module(idrac_default_args, check_mode=params.get('check_mode', False))
        assert result['status_msg'] == params['message']

    def test_validate_negative_job_time_out(self, idrac_default_args):
        idrac_default_args.update({"job_wait": True, "job_wait_timeout": -5})
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as ex:
            self.module.validate_negative_job_time_out(f_module)
        assert ex.value.args[0] == "The parameter job_wait_timeout value cannot be negative or zero."
