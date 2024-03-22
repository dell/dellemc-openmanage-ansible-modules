# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.1.0
# Copyright (C) 2022-2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
from io import StringIO

import pytest
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import ome_application_console_preferences
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

SUCCESS_MSG = "Successfully updated the Console Preferences settings."
SETTINGS_URL = "ApplicationService/Settings"
NO_CHANGES = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
HEALTH_CHECK_UNIT_REQUIRED = "The health check unit is required when health check interval is specified."
HEALTH_CHECK_INTERVAL_REQUIRED = "The health check interval is required when health check unit is specified."
HEALTH_CHECK_INTERVAL_INVALID = "The health check interval specified is invalid for the {0}"
JOB_URL = "JobService/Jobs"
CIFS_URL = "ApplicationService/Actions/ApplicationService.UpdateShareTypeSettings"
CONSOLE_SETTINGS_VALUES = ["DATA_PURGE_INTERVAL", "EMAIL_SENDER", "TRAP_FORWARDING_SETTING",
                           "MX7000_ONBOARDING_PREF", "REPORTS_MAX_RESULTS_LIMIT",
                           "DISCOVERY_APPROVAL_POLICY", "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION",
                           "DEVICE_PREFERRED_NAME", "INVALID_DEVICE_HOSTNAME", "COMMON_MAC_ADDRESSES",
                           "CONSOLE_CONNECTION_SETTING", "MIN_PROTOCOL_VERSION", "SHARE_TYPE"]
MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_application_console_preferences.'
MODULE_UTIL_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.ome.'


@pytest.fixture
def ome_connection_mock_for_application_console_preferences(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeAppConsolePreferences(FakeAnsibleModule):
    module = ome_application_console_preferences

    @pytest.mark.parametrize("params", [{"module_args": {"report_row_limit": 123,
                                                         "mx7000_onboarding_preferences": "all",
                                                         "email_sender_settings": "admin@dell.com",
                                                         "trap_forwarding_format": "Normalized",
                                                         "metrics_collection_settings": 361},
                                         "json_data": {"value": [
                                             {"@odata.type": "#ApplicationService.ConsoleSetting",
                                              "Name": "DATA_PURGE_INTERVAL",
                                              "DefaultValue": "365",
                                              "Value": "361",
                                              "DataType": "java.lang.Integer",
                                              "GroupName": ""
                                              },
                                             {"@odata.type": "#ApplicationService.ConsoleSetting",
                                              "Name": "TRAP_FORWARDING_SETTING",
                                              "DefaultValue": "AsIs",
                                              "Value": "Normalized",
                                              "DataType": "java.lang.String",
                                              "GroupName": ""
                                              },
                                             {"@odata.type": "#ApplicationService.ConsoleSetting",
                                              "Name": "MX7000_ONBOARDING_PREF",
                                              "DefaultValue": "all",
                                              "Value": "all",
                                              "DataType": "java.lang.String",
                                              "GroupName": ""
                                              },
                                             {"@odata.type": "#ApplicationService.ConsoleSetting",
                                              "Name": "REPORTS_MAX_RESULTS_LIMIT",
                                              "DefaultValue": "0",
                                              "Value": "123",
                                              "DataType": "java.lang.Integer",
                                              "GroupName": ""
                                              },
                                             {"@odata.type": "#ApplicationService.ConsoleSetting",
                                              "Name": "EMAIL_SENDER",
                                              "DefaultValue": "omcadmin@dell.com",
                                              "Value": "admin@dell.com",
                                              "DataType": "java.lang.String",
                                              "GroupName": ""
                                              },
                                         ]},
                                         }])
    def test_fetch_cp_settings(self, params, ome_connection_mock_for_application_console_preferences,
                               ome_response_mock):
        ome_response_mock.success = True
        f_module = self.get_module_mock(params=params['module_args'])
        ome_response_mock.json_data = params["json_data"]
        ret_data = self.module.fetch_cp_settings(ome_connection_mock_for_application_console_preferences)
        assert ret_data == params["json_data"]["value"]

    @pytest.mark.parametrize("params", [{"module_args": {"device_health": {"health_check_interval": 55,
                                                                           "health_check_interval_unit": "Minutes"}},
                                         "json_data": {"@odata.type": "#JobService.Job",
                                                       "@odata.id": "/api/JobService/Jobs(10093)",
                                                       "Id": 10093,
                                                       "JobName": "Global Health Task",
                                                       "JobDescription": "Global Health Task",
                                                       "NextRun": "2022-03-15 05:25:00.0",
                                                       "LastRun": "2022-03-15 05:24:00.043",
                                                       "StartTime": None,
                                                       "EndTime": None,
                                                       "Schedule": "0 0/1 * 1/1 * ? *",
                                                       "State": "Enabled",
                                                       "CreatedBy": "admin",
                                                       "UpdatedBy": None,
                                                       "Visible": None,
                                                       "Editable": None,
                                                       "Builtin": False,
                                                       "UserGenerated": True,
                                                       "Targets": [{"JobId": 10093, "Id": 500, "Data": "", "TargetType": {"Id": 6000, "Name": "GROUP"}}],
                                                       "Params": [{"JobId": 10093, "Key": "metricType", "Value": "40, 50"}],
                                                       "LastRunStatus": {"@odata.type": "#JobService.JobStatus", "Id": 2060, "Name": "Completed"},
                                                       "JobType": {"@odata.type": "#JobService.JobType", "Id": 6, "Name": "Health_Task", "Internal": False},
                                                       "JobStatus": {"@odata.type": "#JobService.JobStatus", "Id": 2020, "Name": "Scheduled"},
                                                       "ExecutionHistories@odata.navigationLink": "/api/JobService/Jobs(10093)/ExecutionHistories",
                                                       "LastExecutionDetail": {"@odata.id": "/api/JobService/Jobs(10093)/LastExecutionDetail"}},
                                         }])
    def test_job_details(self, params, ome_connection_mock_for_application_console_preferences,
                         ome_response_mock):
        ome_response_mock.success = True
        f_module = self.get_module_mock(params=params['module_args'])
        ome_response_mock.json_data = {"value": [params["json_data"]]}
        ret_data = self.module.job_details(ome_connection_mock_for_application_console_preferences)
        assert ret_data == params["json_data"]

    @pytest.mark.parametrize("params",
                             [
                                 {"module_args":
                                     {
                                         "report_row_limit": 123,
                                         "mx7000_onboarding_preferences": "all",
                                         "email_sender_settings": "admin@dell.com",
                                         "trap_forwarding_format": "Normalized",
                                         "metrics_collection_settings": 361
                                     },
                                     "payload":
                                         {"ConsoleSetting":
                                             [
                                                 {
                                                     "Name": "DATA_PURGE_INTERVAL",
                                                     "DefaultValue": "365",
                                                     "Value": "361",
                                                     "DataType": "java.lang.Integer",
                                                     "GroupName": ""
                                                 },
                                                 {
                                                     "Name": "TRAP_FORWARDING_SETTING",
                                                     "DefaultValue": "AsIs",
                                                     "Value": "AsIs",
                                                     "DataType": "java.lang.String",
                                                     "GroupName": ""
                                                 },
                                                 {
                                                     "Name": "DEVICE_PREFERRED_NAME",
                                                     "DefaultValue": "SLOT_NAME",
                                                     "Value": "PREFER_DNS,PREFER_IDRAC_SYSTEM_HOSTNAME",
                                                     "DataType": "java.lang.String",
                                                     "GroupName": "DISCOVERY_SETTING"
                                                 }
                                             ]},
                                     "curr_payload": {"DATA_PURGE_INTERVAL": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                              "Name": "DATA_PURGE_INTERVAL",
                                                                              "DefaultValue": "365",
                                                                              "Value": "361",
                                                                              "DataType": "java.lang.Integer",
                                                                              "GroupName": ""},
                                                      "TRAP_FORWARDING_SETTING":
                                                          {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                           "Name": "TRAP_FORWARDING_SETTING",
                                                           "DefaultValue": "AsIs",
                                                           "Value": "Normalized",
                                                           "DataType": "java.lang.String",
                                                           "GroupName": ""},
                                                      "MX7000_ONBOARDING_PREF":
                                                          {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                           "Name": "MX7000_ONBOARDING_PREF",
                                                           "DefaultValue": "all",
                                                           "Value": "all",
                                                           "DataType": "java.lang.String",
                                                           "GroupName": ""},
                                                      "REPORTS_MAX_RESULTS_LIMIT":
                                                          {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                           "Name": "REPORTS_MAX_RESULTS_LIMIT",
                                                           "DefaultValue": "0",
                                                           "Value": "123",
                                                           "DataType": "java.lang.Integer",
                                                           "GroupName": ""},
                                                      "EMAIL_SENDER":
                                                          {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                           "Name": "EMAIL_SENDER",
                                                           "DefaultValue": "omcadmin@dell.com",
                                                           "Value": "admin@dell.com",
                                                           "DataType": "java.lang.String",
                                                           "GroupName": ""},
                                                      "DISCOVERY_APPROVAL_POLICY":
                                                          {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                           "Name": "DISCOVERY_APPROVAL_POLICY",
                                                           "DefaultValue": "Automatic",
                                                           "Value": "Automatic",
                                                           "DataType": "java.lang.String",
                                                           "GroupName": ""},
                                                      "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION":
                                                          {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                           "Name": "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION",
                                                           "DefaultValue": "false",
                                                           "Value": "true",
                                                           "DataType": "java.lang.Boolean",
                                                           "GroupName": ""},
                                                      "DEVICE_PREFERRED_NAME":
                                                          {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                           "Name": "DEVICE_PREFERRED_NAME",
                                                           "DefaultValue": "HOST_NAME",
                                                           "Value": "PREFER_DNS,PREFER_IDRAC_HOSTNAME",
                                                           "DataType": "java.lang.String",
                                                           "GroupName": "DISCOVERY_SETTING"},
                                                      "INVALID_DEVICE_HOSTNAME":
                                                          {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                           "Name": "INVALID_DEVICE_HOSTNAME",
                                                           "DefaultValue": "",
                                                           "Value": "localhost",
                                                           "DataType": "java.lang.String",
                                                           "GroupName": "DISCOVERY_SETTING"},
                                                      "COMMON_MAC_ADDRESSES":
                                                          {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                           "Name": "COMMON_MAC_ADDRESSES",
                                                           "DefaultValue": "",
                                                           "Value": "::",
                                                           "DataType": "java.lang.String",
                                                           "GroupName": "DISCOVERY_SETTING"},
                                                      "MIN_PROTOCOL_VERSION":
                                                          {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                           "Name": "MIN_PROTOCOL_VERSION",
                                                           "DefaultValue": "V2",
                                                           "Value": "V2",
                                                           "DataType": "java.lang.String",
                                                           "GroupName": "CIFS_PROTOCOL_SETTINGS"},
                                                      "CONSOLE_CONNECTION_SETTING":
                                                          {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                           "Name": "CONSOLE_CONNECTION_SETTING",
                                                           "DefaultValue": "last_known",
                                                           "Value": "last_known",
                                                           "DataType": "java.lang.String",
                                                           "GroupName": "CONSOLE_CONNECTION_SETTING"},
                                                      "SHARE_TYPE":
                                                          {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                           "Name": "SHARE_TYPE",
                                                           "DefaultValue": "CIFS",
                                                           "Value": "CIFS",
                                                           "DataType": "java.lang.String",
                                                           "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"}},
                                     "json_data": {"value": [
                                         {"@odata.type": "#ApplicationService.ConsoleSetting",
                                          "Name": "DATA_PURGE_INTERVAL",
                                          "DefaultValue": "365",
                                          "Value": "361",
                                          "DataType": "java.lang.Integer",
                                          "GroupName": ""},
                                         {"@odata.type": "#ApplicationService.ConsoleSetting",
                                          "Name": "TRAP_FORWARDING_SETTING",
                                          "DefaultValue": "AsIs",
                                          "Value": "Normalized",
                                          "DataType": "java.lang.String",
                                          "GroupName": ""},
                                         {"@odata.type": "#ApplicationService.ConsoleSetting",
                                          "Name": "MX7000_ONBOARDING_PREF",
                                          "DefaultValue": "all",
                                          "Value": "all",
                                          "DataType": "java.lang.String",
                                          "GroupName": ""},
                                         {"@odata.type": "#ApplicationService.ConsoleSetting",
                                          "Name": "REPORTS_MAX_RESULTS_LIMIT",
                                          "DefaultValue": "0",
                                          "Value": "123",
                                          "DataType": "java.lang.Integer",
                                          "GroupName": ""},
                                         {"@odata.type": "#ApplicationService.ConsoleSetting",
                                          "Name": "EMAIL_SENDER",
                                          "DefaultValue": "omcadmin@dell.com",
                                          "Value": "admin@dell.com",
                                          "DataType": "java.lang.String",
                                          "GroupName": ""},
                                         {"@odata.type": "#ApplicationService.ConsoleSetting",
                                          "Name": "DISCOVERY_APPROVAL_POLICY",
                                          "DefaultValue": "Automatic",
                                          "Value": "Automatic",
                                          "DataType": "java.lang.String",
                                          "GroupName": ""},
                                         {"@odata.type": "#ApplicationService.ConsoleSetting",
                                          "Name": "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION",
                                          "DefaultValue": "false",
                                          "Value": "true",
                                          "DataType": "java.lang.Boolean",
                                          "GroupName": ""},
                                         {"@odata.type": "#ApplicationService.ConsoleSetting",
                                          "Name": "DEVICE_PREFERRED_NAME",
                                          "DefaultValue": "HOST_NAME",
                                          "Value": "PREFER_DNS,PREFER_IDRAC_HOSTNAME",
                                          "DataType": "java.lang.String",
                                          "GroupName": "DISCOVERY_SETTING"},
                                         {"@odata.type": "#ApplicationService.ConsoleSetting",
                                          "Name": "INVALID_DEVICE_HOSTNAME",
                                          "DefaultValue": "",
                                          "Value": "localhost",
                                          "DataType": "java.lang.String",
                                          "GroupName": "DISCOVERY_SETTING"},
                                         {"@odata.type": "#ApplicationService.ConsoleSetting",
                                          "Name": "COMMON_MAC_ADDRESSES",
                                          "DefaultValue": "",
                                          "Value": "::",
                                          "DataType": "java.lang.String",
                                          "GroupName": "DISCOVERY_SETTING"},
                                         {"@odata.type": "#ApplicationService.ConsoleSetting",
                                          "Name": "MIN_PROTOCOL_VERSION",
                                          "DefaultValue": "V2",
                                          "Value": "V2",
                                          "DataType": "java.lang.String",
                                          "GroupName": "CIFS_PROTOCOL_SETTINGS"},
                                         {"@odata.type": "#ApplicationService.ConsoleSetting",
                                          "Name": "CONSOLE_CONNECTION_SETTING",
                                          "DefaultValue": "last_known",
                                          "Value": "last_known",
                                          "DataType": "java.lang.String",
                                          "GroupName": "CONSOLE_CONNECTION_SETTING"},
                                         {"@odata.type": "#ApplicationService.ConsoleSetting",
                                          "Name": "SHARE_TYPE",
                                          "DefaultValue": "CIFS",
                                          "Value": "CIFS",
                                          "DataType": "java.lang.String",
                                          "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"}]}, }
                             ])
    def test_create_payload_success(self, params, ome_connection_mock_for_application_console_preferences,
                                    ome_response_mock, ome_default_args, mocker):
        ome_response_mock.success = True
        ome_response_mock.json_data = {"value": [params["payload"]]}
        f_module = self.get_module_mock(params=params['module_args'])
        curr_payload = params["json_data"]["value"]
        ret_payload, payload_dict = self.module.create_payload(ome_connection_mock_for_application_console_preferences,
                                                               curr_payload)
        assert payload_dict == params["curr_payload"]

    @pytest.mark.parametrize("params",
                             [
                                 {"module_args":
                                     {
                                         "metrics_collection_settings": "361"
                                     },
                                     "payload":
                                         {"ConsoleSetting":
                                             [
                                                 {
                                                     "@odata.type": "#ApplicationService.ConsoleSetting",
                                                     "Name": "DATA_PURGE_INTERVAL",
                                                     "DefaultValue": "365",
                                                     "Value": "361",
                                                     "DataType": "java.lang.Integer",
                                                     "GroupName": ""
                                                 }
                                             ]},
                                     "curr_payload":
                                         {"DATA_PURGE_INTERVAL": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "DATA_PURGE_INTERVAL",
                                                                  "DefaultValue": "365",
                                                                  "Value": "361",
                                                                  "DataType": "java.lang.Integer",
                                                                  "GroupName": ""},
                                          "TRAP_FORWARDING_SETTING": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                      "Name": "TRAP_FORWARDING_SETTING",
                                                                      "DefaultValue": "AsIs",
                                                                      "Value": "Normalized",
                                                                      "DataType": "java.lang.String",
                                                                      "GroupName": ""},
                                          "MX7000_ONBOARDING_PREF": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                     "Name": "MX7000_ONBOARDING_PREF",
                                                                     "DefaultValue": "all",
                                                                     "Value": "all",
                                                                     "DataType": "java.lang.String",
                                                                     "GroupName": ""},
                                          "REPORTS_MAX_RESULTS_LIMIT": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                        "Name": "REPORTS_MAX_RESULTS_LIMIT",
                                                                        "DefaultValue": "0",
                                                                        "Value": "123",
                                                                        "DataType": "java.lang.Integer",
                                                                        "GroupName": ""},
                                          "EMAIL_SENDER": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                           "Name": "EMAIL_SENDER",
                                                           "DefaultValue": "omcadmin@dell.com",
                                                           "Value": "admin@dell.com",
                                                           "DataType": "java.lang.String",
                                                           "GroupName": ""},
                                          "DISCOVERY_APPROVAL_POLICY": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                        "Name": "DISCOVERY_APPROVAL_POLICY",
                                                                        "DefaultValue": "Automatic",
                                                                        "Value": "Automatic",
                                                                        "DataType": "java.lang.String",
                                                                        "GroupName": ""},
                                          "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                            "Name": "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION",
                                                                                            "DefaultValue": "false",
                                                                                            "Value": "true",
                                                                                            "DataType": "java.lang.Boolean",
                                                                                            "GroupName": ""},
                                          "DEVICE_PREFERRED_NAME": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                    "Name": "DEVICE_PREFERRED_NAME",
                                                                    "DefaultValue": "HOST_NAME",
                                                                    "Value": "PREFER_DNS,PREFER_IDRAC_HOSTNAME",
                                                                    "DataType": "java.lang.String",
                                                                    "GroupName": "DISCOVERY_SETTING"},
                                          "INVALID_DEVICE_HOSTNAME": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                      "Name": "INVALID_DEVICE_HOSTNAME",
                                                                      "DefaultValue": "",
                                                                      "Value": "localhost",
                                                                      "DataType": "java.lang.String",
                                                                      "GroupName": "DISCOVERY_SETTING"},
                                          "COMMON_MAC_ADDRESSES": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                   "Name": "COMMON_MAC_ADDRESSES",
                                                                   "DefaultValue": "",
                                                                   "Value": "::",
                                                                   "DataType": "java.lang.String",
                                                                   "GroupName": "DISCOVERY_SETTING"},
                                          "MIN_PROTOCOL_VERSION": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                   "Name": "MIN_PROTOCOL_VERSION",
                                                                   "DefaultValue": "V2",
                                                                   "Value": "V2",
                                                                   "DataType": "java.lang.String",
                                                                   "GroupName": "CIFS_PROTOCOL_SETTINGS"},
                                          "CONSOLE_CONNECTION_SETTING": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                         "Name": "CONSOLE_CONNECTION_SETTING",
                                                                         "DefaultValue": "last_known",
                                                                         "Value": "last_known",
                                                                         "DataType": "java.lang.String",
                                                                         "GroupName": "CONSOLE_CONNECTION_SETTING"},
                                          "SHARE_TYPE": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                         "Name": "SHARE_TYPE",
                                                         "DefaultValue": "CIFS",
                                                         "Value": "CIFS",
                                                         "DataType": "java.lang.String",
                                                         "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"}},
                                     "json_data": {"value": [
                                         {"@odata.type": "#ApplicationService.ConsoleSetting",
                                          "Name": "DATA_PURGE_INTERVAL",
                                          "DefaultValue": "365",
                                          "Value": "361",
                                          "DataType": "java.lang.Integer",
                                          "GroupName": ""
                                          },
                                         {"@odata.type": "#ApplicationService.ConsoleSetting",
                                          "Name": "TRAP_FORWARDING_SETTING",
                                          "DefaultValue": "AsIs",
                                          "Value": "Normalized",
                                          "DataType": "java.lang.String",
                                          "GroupName": ""
                                          },
                                         {"@odata.type": "#ApplicationService.ConsoleSetting",
                                          "Name": "MX7000_ONBOARDING_PREF",
                                          "DefaultValue": "all",
                                          "Value": "all",
                                          "DataType": "java.lang.String",
                                          "GroupName": ""
                                          },
                                         {"@odata.type": "#ApplicationService.ConsoleSetting",
                                          "Name": "REPORTS_MAX_RESULTS_LIMIT",
                                          "DefaultValue": "0",
                                          "Value": "123",
                                          "DataType": "java.lang.Integer",
                                          "GroupName": ""
                                          },
                                         {"@odata.type": "#ApplicationService.ConsoleSetting",
                                          "Name": "EMAIL_SENDER",
                                          "DefaultValue": "omcadmin@dell.com",
                                          "Value": "admin@dell.com",
                                          "DataType": "java.lang.String",
                                          "GroupName": ""
                                          },
                                         {
                                             "@odata.type": "#ApplicationService.ConsoleSetting",
                                             "Name": "DISCOVERY_APPROVAL_POLICY",
                                             "DefaultValue": "Automatic",
                                             "Value": "Automatic",
                                             "DataType": "java.lang.String",
                                             "GroupName": ""
                                         },
                                         {
                                             "@odata.type": "#ApplicationService.ConsoleSetting",
                                             "Name": "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION",
                                             "DefaultValue": "false",
                                             "Value": "true",
                                             "DataType": "java.lang.Boolean",
                                             "GroupName": ""
                                         },
                                         {
                                             "@odata.type": "#ApplicationService.ConsoleSetting",
                                             "Name": "DEVICE_PREFERRED_NAME",
                                             "DefaultValue": "HOST_NAME",
                                             "Value": "PREFER_DNS,PREFER_IDRAC_HOSTNAME",
                                             "DataType": "java.lang.String",
                                             "GroupName": "DISCOVERY_SETTING"
                                         },
                                         {
                                             "@odata.type": "#ApplicationService.ConsoleSetting",
                                             "Name": "INVALID_DEVICE_HOSTNAME",
                                             "DefaultValue": "",
                                             "Value": "localhost",
                                             "DataType": "java.lang.String",
                                             "GroupName": "DISCOVERY_SETTING"
                                         },
                                         {
                                             "@odata.type": "#ApplicationService.ConsoleSetting",
                                             "Name": "COMMON_MAC_ADDRESSES",
                                             "DefaultValue": "",
                                             "Value": "::",
                                             "DataType": "java.lang.String",
                                             "GroupName": "DISCOVERY_SETTING"
                                         },
                                         {
                                             "@odata.type": "#ApplicationService.ConsoleSetting",
                                             "Name": "MIN_PROTOCOL_VERSION",
                                             "DefaultValue": "V2",
                                             "Value": "V2",
                                             "DataType": "java.lang.String",
                                             "GroupName": "CIFS_PROTOCOL_SETTINGS"
                                         },
                                         {
                                             "@odata.type": "#ApplicationService.ConsoleSetting",
                                             "Name": "CONSOLE_CONNECTION_SETTING",
                                             "DefaultValue": "last_known",
                                             "Value": "last_known",
                                             "DataType": "java.lang.String",
                                             "GroupName": "CONSOLE_CONNECTION_SETTING"
                                         },
                                         {
                                             "@odata.type": "#ApplicationService.ConsoleSetting",
                                             "Name": "SHARE_TYPE",
                                             "DefaultValue": "CIFS",
                                             "Value": "CIFS",
                                             "DataType": "java.lang.String",
                                             "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"}]}, }])
    def test_create_payload_success_case02(self, params, ome_connection_mock_for_application_console_preferences,
                                           ome_response_mock, ome_default_args, mocker):
        ome_response_mock.success = True
        # ome_response_mock.json_data = {"value": [params["payload"]]}
        f_module = self.get_module_mock(params=params['module_args'])
        curr_payload = params["json_data"]["value"]
        ret_payload, payload_dict = self.module.create_payload(f_module, curr_payload)
        assert ret_payload == params["payload"]

    @pytest.mark.parametrize("params", [{"module_args": {"builtin_appliance_share": {"share_options": "CIFS",
                                                                                     "cifs_options": "V1"}},
                                         "payload": {"ConsoleSetting": [{"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                         "Name": "MIN_PROTOCOL_VERSION",
                                                                         "DefaultValue": "V2",
                                                                         "Value": "V1",
                                                                         "DataType": "java.lang.String",
                                                                         "GroupName": "CIFS_PROTOCOL_SETTINGS"}]},
                                         "curr_payload": {"DATA_PURGE_INTERVAL": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                  "Name": "DATA_PURGE_INTERVAL",
                                                                                  "DefaultValue": "365",
                                                                                  "Value": "361",
                                                                                  "DataType": "java.lang.Integer",
                                                                                  "GroupName": ""},
                                                          "TRAP_FORWARDING_SETTING": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                      "Name": "TRAP_FORWARDING_SETTING",
                                                                                      "DefaultValue": "AsIs",
                                                                                      "Value": "Normalized",
                                                                                      "DataType": "java.lang.String",
                                                                                      "GroupName": ""},
                                                          "MX7000_ONBOARDING_PREF": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                     "Name": "MX7000_ONBOARDING_PREF",
                                                                                     "DefaultValue": "all",
                                                                                     "Value": "all",
                                                                                     "DataType": "java.lang.String",
                                                                                     "GroupName": ""},
                                                          "REPORTS_MAX_RESULTS_LIMIT": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                        "Name": "REPORTS_MAX_RESULTS_LIMIT",
                                                                                        "DefaultValue": "0",
                                                                                        "Value": "123",
                                                                                        "DataType": "java.lang.Integer",
                                                                                        "GroupName": ""},
                                                          "EMAIL_SENDER": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                           "Name": "EMAIL_SENDER",
                                                                           "DefaultValue": "omcadmin@dell.com",
                                                                           "Value": "admin@dell.com",
                                                                           "DataType": "java.lang.String",
                                                                           "GroupName": ""},
                                                          "DISCOVERY_APPROVAL_POLICY": {
                                                              "@odata.type": "#ApplicationService.ConsoleSetting",
                                                              "Name": "DISCOVERY_APPROVAL_POLICY",
                                                              "DefaultValue": "Automatic",
                                                              "Value": "Automatic",
                                                              "DataType": "java.lang.String",
                                                              "GroupName": ""},
                                                          "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION": {
                                                              "@odata.type": "#ApplicationService.ConsoleSetting",
                                                              "Name": "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION",
                                                              "DefaultValue": "false",
                                                              "Value": "true",
                                                              "DataType": "java.lang.Boolean",
                                                              "GroupName": ""},
                                                          "DEVICE_PREFERRED_NAME": {
                                                              "@odata.type": "#ApplicationService.ConsoleSetting",
                                                              "Name": "DEVICE_PREFERRED_NAME",
                                                              "DefaultValue": "HOST_NAME",
                                                              "Value": "PREFER_DNS,PREFER_IDRAC_HOSTNAME",
                                                              "DataType": "java.lang.String",
                                                              "GroupName": "DISCOVERY_SETTING"},
                                                          "INVALID_DEVICE_HOSTNAME": {
                                                              "@odata.type": "#ApplicationService.ConsoleSetting",
                                                              "Name": "INVALID_DEVICE_HOSTNAME",
                                                              "DefaultValue": "",
                                                              "Value": "localhost",
                                                              "DataType": "java.lang.String",
                                                              "GroupName": "DISCOVERY_SETTING"},
                                                          "COMMON_MAC_ADDRESSES": {
                                                              "@odata.type": "#ApplicationService.ConsoleSetting",
                                                              "Name": "COMMON_MAC_ADDRESSES",
                                                              "DefaultValue": "",
                                                              "Value": "::",
                                                              "DataType": "java.lang.String",
                                                              "GroupName": "DISCOVERY_SETTING"},
                                                          "MIN_PROTOCOL_VERSION": {
                                                              "@odata.type": "#ApplicationService.ConsoleSetting",
                                                              "Name": "MIN_PROTOCOL_VERSION",
                                                              "DefaultValue": "V2",
                                                              "Value": "V2",
                                                              "DataType": "java.lang.String",
                                                              "GroupName": "CIFS_PROTOCOL_SETTINGS"},
                                                          "CONSOLE_CONNECTION_SETTING": {
                                                              "@odata.type": "#ApplicationService.ConsoleSetting",
                                                              "Name": "CONSOLE_CONNECTION_SETTING",
                                                              "DefaultValue": "last_known",
                                                              "Value": "last_known",
                                                              "DataType": "java.lang.String",
                                                              "GroupName": "CONSOLE_CONNECTION_SETTING"},
                                                          "SHARE_TYPE": {
                                                              "@odata.type": "#ApplicationService.ConsoleSetting",
                                                              "Name": "SHARE_TYPE",
                                                              "DefaultValue": "CIFS",
                                                              "Value": "CIFS",
                                                              "DataType": "java.lang.String",
                                                              "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"}},
                                         "json_data": {"value": [{"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "DATA_PURGE_INTERVAL",
                                                                  "DefaultValue": "365",
                                                                  "Value": "361",
                                                                  "DataType": "java.lang.Integer",
                                                                  "GroupName": ""},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "TRAP_FORWARDING_SETTING",
                                                                  "DefaultValue": "AsIs",
                                                                  "Value": "Normalized",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": ""},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "MX7000_ONBOARDING_PREF",
                                                                  "DefaultValue": "all",
                                                                  "Value": "all",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": ""},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "REPORTS_MAX_RESULTS_LIMIT",
                                                                  "DefaultValue": "0",
                                                                  "Value": "123",
                                                                  "DataType": "java.lang.Integer",
                                                                  "GroupName": ""},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "EMAIL_SENDER",
                                                                  "DefaultValue": "omcadmin@dell.com",
                                                                  "Value": "admin@dell.com",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": ""},
                                                                 {
                                                                     "@odata.type": "#ApplicationService.ConsoleSetting",
                                                                     "Name": "DISCOVERY_APPROVAL_POLICY",
                                                                     "DefaultValue": "Automatic",
                                                                     "Value": "Automatic",
                                                                     "DataType": "java.lang.String",
                                                                     "GroupName": ""},
                                                                 {
                                                                     "@odata.type": "#ApplicationService.ConsoleSetting",
                                                                     "Name": "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION",
                                                                     "DefaultValue": "false",
                                                                     "Value": "true",
                                                                     "DataType": "java.lang.Boolean",
                                                                     "GroupName": ""},
                                                                 {
                                                                     "@odata.type": "#ApplicationService.ConsoleSetting",
                                                                     "Name": "DEVICE_PREFERRED_NAME",
                                                                     "DefaultValue": "HOST_NAME",
                                                                     "Value": "PREFER_DNS,PREFER_IDRAC_HOSTNAME",
                                                                     "DataType": "java.lang.String",
                                                                     "GroupName": "DISCOVERY_SETTING"},
                                                                 {
                                                                     "@odata.type": "#ApplicationService.ConsoleSetting",
                                                                     "Name": "INVALID_DEVICE_HOSTNAME",
                                                                     "DefaultValue": "",
                                                                     "Value": "localhost",
                                                                     "DataType": "java.lang.String",
                                                                     "GroupName": "DISCOVERY_SETTING"},
                                                                 {
                                                                     "@odata.type": "#ApplicationService.ConsoleSetting",
                                                                     "Name": "COMMON_MAC_ADDRESSES",
                                                                     "DefaultValue": "",
                                                                     "Value": "::",
                                                                     "DataType": "java.lang.String",
                                                                     "GroupName": "DISCOVERY_SETTING"},
                                                                 {
                                                                     "@odata.type": "#ApplicationService.ConsoleSetting",
                                                                     "Name": "MIN_PROTOCOL_VERSION",
                                                                     "DefaultValue": "V2",
                                                                     "Value": "V2",
                                                                     "DataType": "java.lang.String",
                                                                     "GroupName": "CIFS_PROTOCOL_SETTINGS"},
                                                                 {
                                                                     "@odata.type": "#ApplicationService.ConsoleSetting",
                                                                     "Name": "CONSOLE_CONNECTION_SETTING",
                                                                     "DefaultValue": "last_known",
                                                                     "Value": "last_known",
                                                                     "DataType": "java.lang.String",
                                                                     "GroupName": "CONSOLE_CONNECTION_SETTING"},
                                                                 {
                                                                     "@odata.type": "#ApplicationService.ConsoleSetting",
                                                                     "Name": "SHARE_TYPE",
                                                                     "DefaultValue": "CIFS",
                                                                     "Value": "CIFS",
                                                                     "DataType": "java.lang.String",
                                                                     "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"}]}, }])
    def test_create_payload_success_case03(self, params, ome_connection_mock_for_application_console_preferences,
                                           ome_response_mock, ome_default_args, mocker):
        ome_response_mock.success = True
        # ome_response_mock.json_data = {"value": [params["payload"]]}
        f_module = self.get_module_mock(params=params['module_args'])
        curr_payload = params["json_data"]["value"]
        ret_payload, payload_dict = self.module.create_payload(f_module, curr_payload)
        assert ret_payload == params["payload"]

    @pytest.mark.parametrize("params", [
        {
            "payload": {
                "ConsoleSetting": [
                    {
                        "@odata.type": "#ApplicationService.ConsoleSetting",
                        "Name": "DATA_PURGE_INTERVAL",
                        "DefaultValue": "365",
                        "Value": "361",
                        "DataType": "java.lang.Integer",
                        "GroupName": ""
                    },
                    {
                        "@odata.type": "#ApplicationService.ConsoleSetting",
                        "Name": "TRAP_FORWARDING_SETTING",
                        "DefaultValue": "AsIs",
                        "Value": "AsIs",
                        "DataType": "java.lang.String",
                        "GroupName": ""
                    },
                    {
                        "@odata.type": "#ApplicationService.ConsoleSetting",
                        "Name": "DEVICE_PREFERRED_NAME",
                        "DefaultValue": "SLOT_NAME",
                        "Value": "PREFER_DNS,PREFER_IDRAC_SYSTEM_HOSTNAME",
                        "DataType": "java.lang.String",
                        "GroupName": "DISCOVERY_SETTING"
                    }
                ]
            },
            "cifs_payload": {
                "ConsoleSetting": [
                    {
                        "@odata.type": "#ApplicationService.ConsoleSetting",
                        "Name": "SHARE_TYPE",
                        "DefaultValue": "CIFS",
                        "Value": "CIFS",
                        "DataType": "java.lang.String",
                        "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"
                    }
                ]
            },
            "job_payload": {"Id": 0,
                            "JobName": "Global Health Task",
                            "JobDescription": "Global Health Task",
                            "Schedule": None,
                            "State": "Enabled",
                            "JobType": {"Id": 6, "Name": "Health_Task"},
                            "Params": [{"Key": "metricType", "Value": "40, 50"}],
                            "Targets": [{"Id": 500, "Data": "", "TargetType": {"Id": 6000, "Name": "GROUP"}}]},
            "job_data":
                {
                    "@odata.type": "#JobService.Job",
                    "@odata.id": "/api/JobService/Jobs(10093)",
                    "Id": 10093,
                    "JobName": "Global Health Task",
                    "JobDescription": "Global Health Task",
                    "NextRun": "2022-03-15 05:25:00.0",
                    "LastRun": "2022-03-15 05:24:00.043",
                    "StartTime": None,
                    "EndTime": None,
                    "Schedule": "0 0/1 * 1/1 * ? *",
                    "State": "Enabled",
                    "CreatedBy": "admin",
                    "UpdatedBy": None,
                    "Visible": None,
                    "Editable": None,
                    "Builtin": False,
                    "UserGenerated": True,
                    "Targets": [{"JobId": 10093, "Id": 500, "Data": "", "TargetType": {"Id": 6000, "Name": "GROUP"}}],
                    "Params": [{"JobId": 10093, "Key": "metricType", "Value": "40, 50"}],
                    "LastRunStatus": {"@odata.type": "#JobService.JobStatus", "Id": 2060, "Name": "Completed"},
                    "JobType": {"@odata.type": "#JobService.JobType", "Id": 6, "Name": "Health_Task",
                                "Internal": False},
                    "JobStatus": {"@odata.type": "#JobService.JobStatus", "Id": 2020, "Name": "Scheduled"},
                    "ExecutionHistories@odata.navigationLink": "/api/JobService/Jobs(10093)/ExecutionHistories",
                    "LastExecutionDetail": {"@odata.id": "/api/JobService/Jobs(10093)/LastExecutionDetail"}},
            "payload_dict": {"DATA_PURGE_INTERVAL": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                     "Name": "DATA_PURGE_INTERVAL",
                                                     "DefaultValue": "365",
                                                     "Value": "361",
                                                     "DataType": "java.lang.Integer",
                                                     "GroupName": ""
                                                     },
                             "TRAP_FORWARDING_SETTING": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                         "Name": "TRAP_FORWARDING_SETTING",
                                                         "DefaultValue": "AsIs",
                                                         "Value": "Normalized",
                                                         "DataType": "java.lang.String",
                                                         "GroupName": ""
                                                         },
                             "MX7000_ONBOARDING_PREF": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                        "Name": "MX7000_ONBOARDING_PREF",
                                                        "DefaultValue": "all",
                                                        "Value": "all",
                                                        "DataType": "java.lang.String",
                                                        "GroupName": ""
                                                        },
                             "REPORTS_MAX_RESULTS_LIMIT": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                           "Name": "REPORTS_MAX_RESULTS_LIMIT",
                                                           "DefaultValue": "0",
                                                           "Value": "123",
                                                           "DataType": "java.lang.Integer",
                                                           "GroupName": ""
                                                           },
                             "EMAIL_SENDER": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                              "Name": "EMAIL_SENDER",
                                              "DefaultValue": "omcadmin@dell.com",
                                              "Value": "admin@dell.com",
                                              "DataType": "java.lang.String",
                                              "GroupName": ""
                                              },
                             "DISCOVERY_APPROVAL_POLICY": {
                                 "@odata.type": "#ApplicationService.ConsoleSetting",
                                 "Name": "DISCOVERY_APPROVAL_POLICY",
                                 "DefaultValue": "Automatic",
                                 "Value": "Automatic",
                                 "DataType": "java.lang.String",
                                 "GroupName": ""},
                             "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION": {
                                 "@odata.type": "#ApplicationService.ConsoleSetting",
                                 "Name": "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION",
                                 "DefaultValue": "false",
                                 "Value": "true",
                                 "DataType": "java.lang.Boolean",
                                 "GroupName": ""},
                             "DEVICE_PREFERRED_NAME": {
                                 "@odata.type": "#ApplicationService.ConsoleSetting",
                                 "Name": "DEVICE_PREFERRED_NAME",
                                 "DefaultValue": "HOST_NAME",
                                 "Value": "PREFER_DNS,PREFER_IDRAC_HOSTNAME",
                                 "DataType": "java.lang.String",
                                 "GroupName": "DISCOVERY_SETTING"},
                             "INVALID_DEVICE_HOSTNAME": {
                                 "@odata.type": "#ApplicationService.ConsoleSetting",
                                 "Name": "INVALID_DEVICE_HOSTNAME",
                                 "DefaultValue": "",
                                 "Value": "localhost",
                                 "DataType": "java.lang.String",
                                 "GroupName": "DISCOVERY_SETTING"},
                             "COMMON_MAC_ADDRESSES": {
                                 "@odata.type": "#ApplicationService.ConsoleSetting",
                                 "Name": "COMMON_MAC_ADDRESSES",
                                 "DefaultValue": "",
                                 "Value": "::",
                                 "DataType": "java.lang.String",
                                 "GroupName": "DISCOVERY_SETTING"},
                             "MIN_PROTOCOL_VERSION": {
                                 "@odata.type": "#ApplicationService.ConsoleSetting",
                                 "Name": "MIN_PROTOCOL_VERSION",
                                 "DefaultValue": "V2",
                                 "Value": "V2",
                                 "DataType": "java.lang.String",
                                 "GroupName": "CIFS_PROTOCOL_SETTINGS"},
                             "CONSOLE_CONNECTION_SETTING": {
                                 "@odata.type": "#ApplicationService.ConsoleSetting",
                                 "Name": "CONSOLE_CONNECTION_SETTING",
                                 "DefaultValue": "last_known",
                                 "Value": "last_known",
                                 "DataType": "java.lang.String",
                                 "GroupName": "CONSOLE_CONNECTION_SETTING"},
                             "SHARE_TYPE": {
                                 "@odata.type": "#ApplicationService.ConsoleSetting",
                                 "Name": "SHARE_TYPE",
                                 "DefaultValue": "CIFS",
                                 "Value": "CIFS",
                                 "DataType": "java.lang.String",
                                 "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"}

                             },
            "schedule": None,
            "module_args": {
                "report_row_limit": 123,
            }
        }
    ])
    def test_update_console_preferences(self, params, ome_connection_mock_for_application_console_preferences,
                                        ome_response_mock, ome_default_args):
        ome_response_mock.success = True
        ome_default_args.update(params["module_args"])
        # ome_response_mock.json_data = {"value": [params["payload"]]}
        f_module = self.get_module_mock(params=params['module_args'])
        final_resp, cifs_resp, job_resp = self.module.update_console_preferences(f_module, ome_connection_mock_for_application_console_preferences,
                                                                                 params["payload"], params["cifs_payload"],
                                                                                 params["job_payload"], params["job_data"],
                                                                                 params["payload_dict"], params["schedule"])
        assert final_resp.status_code == 200

    @pytest.mark.parametrize("params", [
        {
            "payload": {
                "ConsoleSetting": [
                    {
                        "@odata.type": "#ApplicationService.ConsoleSetting",
                        "Name": "DATA_PURGE_INTERVAL",
                        "DefaultValue": "365",
                        "Value": "361",
                        "DataType": "java.lang.Integer",
                        "GroupName": ""
                    },
                    {
                        "@odata.type": "#ApplicationService.ConsoleSetting",
                        "Name": "TRAP_FORWARDING_SETTING",
                        "DefaultValue": "AsIs",
                        "Value": "AsIs",
                        "DataType": "java.lang.String",
                        "GroupName": ""
                    },
                    {
                        "@odata.type": "#ApplicationService.ConsoleSetting",
                        "Name": "DEVICE_PREFERRED_NAME",
                        "DefaultValue": "SLOT_NAME",
                        "Value": "PREFER_DNS,PREFER_IDRAC_SYSTEM_HOSTNAME",
                        "DataType": "java.lang.String",
                        "GroupName": "DISCOVERY_SETTING"
                    }
                ]
            },
            "cifs_payload": {
                "ConsoleSetting": [
                    {
                        "@odata.type": "#ApplicationService.ConsoleSetting",
                        "Name": "SHARE_TYPE",
                        "DefaultValue": "CIFS",
                        "Value": "CIFS",
                        "DataType": "java.lang.String",
                        "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"
                    }
                ]
            },
            "job_payload": {"Id": 0,
                            "JobName": "Global Health Task",
                            "JobDescription": "Global Health Task",
                            "Schedule": None,
                            "State": "Enabled",
                            "JobType": {"Id": 6, "Name": "Health_Task"},
                            "Params": [{"Key": "metricType", "Value": "40, 50"}],
                            "Targets": [{"Id": 500, "Data": "", "TargetType": {"Id": 6000, "Name": "GROUP"}}]},
            "job_data":
                {
                    "@odata.type": "#JobService.Job",
                    "@odata.id": "/api/JobService/Jobs(10093)",
                    "Id": 10093,
                    "JobName": "Global Health Task",
                    "JobDescription": "Global Health Task",
                    "NextRun": "2022-03-15 05:25:00.0",
                    "LastRun": "2022-03-15 05:24:00.043",
                    "StartTime": None,
                    "EndTime": None,
                    "Schedule": "0 0/1 * 1/1 * ? *",
                    "State": "Enabled",
                    "CreatedBy": "admin",
                    "UpdatedBy": None,
                    "Visible": None,
                    "Editable": None,
                    "Builtin": False,
                    "UserGenerated": True,
                    "Targets": [{"JobId": 10093, "Id": 500, "Data": "", "TargetType": {"Id": 6000, "Name": "GROUP"}}],
                    "Params": [{"JobId": 10093, "Key": "metricType", "Value": "40, 50"}],
                    "LastRunStatus": {"@odata.type": "#JobService.JobStatus", "Id": 2060, "Name": "Completed"},
                    "JobType": {"@odata.type": "#JobService.JobType", "Id": 6, "Name": "Health_Task",
                                "Internal": False},
                    "JobStatus": {"@odata.type": "#JobService.JobStatus", "Id": 2020, "Name": "Scheduled"},
                    "ExecutionHistories@odata.navigationLink": "/api/JobService/Jobs(10093)/ExecutionHistories",
                    "LastExecutionDetail": {"@odata.id": "/api/JobService/Jobs(10093)/LastExecutionDetail"}},
            "payload_dict": {"DATA_PURGE_INTERVAL": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                     "Name": "DATA_PURGE_INTERVAL",
                                                     "DefaultValue": "365",
                                                     "Value": "361",
                                                     "DataType": "java.lang.Integer",
                                                     "GroupName": ""},
                             "TRAP_FORWARDING_SETTING": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                         "Name": "TRAP_FORWARDING_SETTING",
                                                         "DefaultValue": "AsIs",
                                                         "Value": "Normalized",
                                                         "DataType": "java.lang.String",
                                                         "GroupName": ""},
                             "MX7000_ONBOARDING_PREF": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                        "Name": "MX7000_ONBOARDING_PREF",
                                                        "DefaultValue": "all",
                                                        "Value": "all",
                                                        "DataType": "java.lang.String",
                                                        "GroupName": ""},
                             "REPORTS_MAX_RESULTS_LIMIT": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                           "Name": "REPORTS_MAX_RESULTS_LIMIT",
                                                           "DefaultValue": "0",
                                                           "Value": "123",
                                                           "DataType": "java.lang.Integer",
                                                           "GroupName": ""},
                             "EMAIL_SENDER": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                              "Name": "EMAIL_SENDER",
                                              "DefaultValue": "omcadmin@dell.com",
                                              "Value": "admin@dell.com",
                                              "DataType": "java.lang.String",
                                              "GroupName": ""},
                             "DISCOVERY_APPROVAL_POLICY": {
                                 "@odata.type": "#ApplicationService.ConsoleSetting",
                                 "Name": "DISCOVERY_APPROVAL_POLICY",
                                 "DefaultValue": "Automatic",
                                 "Value": "Automatic",
                                 "DataType": "java.lang.String",
                                 "GroupName": ""},
                             "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION": {
                                 "@odata.type": "#ApplicationService.ConsoleSetting",
                                 "Name": "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION",
                                 "DefaultValue": "false",
                                 "Value": "true",
                                 "DataType": "java.lang.Boolean",
                                 "GroupName": ""},
                             "DEVICE_PREFERRED_NAME": {
                                 "@odata.type": "#ApplicationService.ConsoleSetting",
                                 "Name": "DEVICE_PREFERRED_NAME",
                                 "DefaultValue": "HOST_NAME",
                                 "Value": "PREFER_DNS,PREFER_IDRAC_HOSTNAME",
                                 "DataType": "java.lang.String",
                                 "GroupName": "DISCOVERY_SETTING"},
                             "INVALID_DEVICE_HOSTNAME": {
                                 "@odata.type": "#ApplicationService.ConsoleSetting",
                                 "Name": "INVALID_DEVICE_HOSTNAME",
                                 "DefaultValue": "",
                                 "Value": "localhost",
                                 "DataType": "java.lang.String",
                                 "GroupName": "DISCOVERY_SETTING"},
                             "COMMON_MAC_ADDRESSES": {
                                 "@odata.type": "#ApplicationService.ConsoleSetting",
                                 "Name": "COMMON_MAC_ADDRESSES",
                                 "DefaultValue": "",
                                 "Value": "::",
                                 "DataType": "java.lang.String",
                                 "GroupName": "DISCOVERY_SETTING"},
                             "MIN_PROTOCOL_VERSION": {
                                 "@odata.type": "#ApplicationService.ConsoleSetting",
                                 "Name": "MIN_PROTOCOL_VERSION",
                                 "DefaultValue": "V2",
                                 "Value": "V2",
                                 "DataType": "java.lang.String",
                                 "GroupName": "CIFS_PROTOCOL_SETTINGS"},
                             "CONSOLE_CONNECTION_SETTING": {
                                 "@odata.type": "#ApplicationService.ConsoleSetting",
                                 "Name": "CONSOLE_CONNECTION_SETTING",
                                 "DefaultValue": "last_known",
                                 "Value": "last_known",
                                 "DataType": "java.lang.String",
                                 "GroupName": "CONSOLE_CONNECTION_SETTING"},
                             "SHARE_TYPE": {
                                 "@odata.type": "#ApplicationService.ConsoleSetting",
                                 "Name": "SHARE_TYPE",
                                 "DefaultValue": "CIFS",
                                 "Value": "CIFS",
                                 "DataType": "java.lang.String",
                                 "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"}

                             },
            "schedule": "0 0 0/5 1/1 * ? *",
            "module_args": {
                "builtin_appliance_share": {"share_options": "HTTPS", "cifs_options": "V2"}
            }
        }
    ])
    def test_update_console_preferences_case02(self, params, ome_connection_mock_for_application_console_preferences,
                                               ome_response_mock, ome_default_args):
        ome_response_mock.success = True
        ome_default_args.update(params["module_args"])
        # ome_response_mock.json_data = {"value": [params["payload"]]}
        f_module = self.get_module_mock(params=params['module_args'])
        final_resp, cifs_resp, job_resp = self.module.update_console_preferences(f_module,
                                                                                 ome_connection_mock_for_application_console_preferences,
                                                                                 params["payload"],
                                                                                 params["cifs_payload"],
                                                                                 params["job_payload"],
                                                                                 params["job_data"],
                                                                                 params["payload_dict"],
                                                                                 params["schedule"])
        assert cifs_resp.success is True

    @pytest.mark.parametrize("params", [{"payload": {"ConsoleSetting": [{"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                         "Name": "DATA_PURGE_INTERVAL",
                                                                         "DefaultValue": "365",
                                                                         "Value": "361",
                                                                         "DataType": "java.lang.Integer",
                                                                         "GroupName": ""},
                                                                        {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                         "Name": "TRAP_FORWARDING_SETTING",
                                                                         "DefaultValue": "AsIs",
                                                                         "Value": "AsIs",
                                                                         "DataType": "java.lang.String",
                                                                         "GroupName": ""},
                                                                        {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                         "Name": "DEVICE_PREFERRED_NAME",
                                                                         "DefaultValue": "SLOT_NAME",
                                                                         "Value": "PREFER_DNS,PREFER_IDRAC_SYSTEM_HOSTNAME",
                                                                         "DataType": "java.lang.String",
                                                                         "GroupName": "DISCOVERY_SETTING"}]},
                                         "cifs_payload": {"ConsoleSetting": [{"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                              "Name": "SHARE_TYPE",
                                                                              "DefaultValue": "CIFS",
                                                                              "Value": "CIFS",
                                                                              "DataType": "java.lang.String",
                                                                              "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"}]},
                                         "job_payload": {"Id": 0,
                                                         "JobName": "Global Health Task",
                                                         "JobDescription": "Global Health Task",
                                                         "Schedule": "0 0 0/5 1/1 * ? *",
                                                         "State": "Enabled",
                                                         "JobType": {"Id": 6, "Name": "Health_Task"},
                                                         "Params": [{"Key": "metricType", "Value": "40, 50"}],
                                                         "Targets": [{"Id": 500, "Data": "", "TargetType": {"Id": 6000, "Name": "GROUP"}}]},
                                         "job_data": {"@odata.type": "#JobService.Job",
                                                      "@odata.id": "/api/JobService/Jobs(10093)",
                                                      "Id": 10093,
                                                      "JobName": "Global Health Task",
                                                      "JobDescription": "Global Health Task",
                                                      "NextRun": "2022-03-15 05:25:00.0",
                                                      "LastRun": "2022-03-15 05:24:00.043",
                                                      "StartTime": None,
                                                      "EndTime": None,
                                                      "Schedule": "0 0/1 * 1/1 * ? *",
                                                      "State": "Enabled",
                                                      "CreatedBy": "admin",
                                                      "UpdatedBy": None,
                                                      "Visible": None,
                                                      "Editable": None,
                                                      "Builtin": False,
                                                      "UserGenerated": True,
                                                      "Targets": [{"JobId": 10093, "Id": 500, "Data": "", "TargetType": {"Id": 6000, "Name": "GROUP"}}],
                                                      "Params": [{"JobId": 10093, "Key": "metricType", "Value": "40, 50"}],
                                                      "LastRunStatus": {"@odata.type": "#JobService.JobStatus", "Id": 2060, "Name": "Completed"},
                                                      "JobType": {"@odata.type": "#JobService.JobType", "Id": 6, "Name": "Health_Task", "Internal": False},
                                                      "JobStatus": {"@odata.type": "#JobService.JobStatus", "Id": 2020, "Name": "Scheduled"},
                                                      "ExecutionHistories@odata.navigationLink": "/api/JobService/Jobs(10093)/ExecutionHistories",
                                                      "LastExecutionDetail": {"@odata.id": "/api/JobService/Jobs(10093)/LastExecutionDetail"}},
                                         "payload_dict": {"DATA_PURGE_INTERVAL": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                  "Name": "DATA_PURGE_INTERVAL",
                                                                                  "DefaultValue": "365",
                                                                                  "Value": "361",
                                                                                  "DataType": "java.lang.Integer",
                                                                                  "GroupName": ""},
                                                          "TRAP_FORWARDING_SETTING": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                      "Name": "TRAP_FORWARDING_SETTING",
                                                                                      "DefaultValue": "AsIs",
                                                                                      "Value": "Normalized",
                                                                                      "DataType": "java.lang.String",
                                                                                      "GroupName": ""},
                                                          "MX7000_ONBOARDING_PREF": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                     "Name": "MX7000_ONBOARDING_PREF",
                                                                                     "DefaultValue": "all",
                                                                                     "Value": "all",
                                                                                     "DataType": "java.lang.String",
                                                                                     "GroupName": ""},
                                                          "REPORTS_MAX_RESULTS_LIMIT": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                        "Name": "REPORTS_MAX_RESULTS_LIMIT",
                                                                                        "DefaultValue": "0",
                                                                                        "Value": "123",
                                                                                        "DataType": "java.lang.Integer",
                                                                                        "GroupName": ""},
                                                          "EMAIL_SENDER": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                           "Name": "EMAIL_SENDER",
                                                                           "DefaultValue": "omcadmin@dell.com",
                                                                           "Value": "admin@dell.com",
                                                                           "DataType": "java.lang.String",
                                                                           "GroupName": ""},
                                                          "DISCOVERY_APPROVAL_POLICY": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                        "Name": "DISCOVERY_APPROVAL_POLICY",
                                                                                        "DefaultValue": "Automatic",
                                                                                        "Value": "Automatic",
                                                                                        "DataType": "java.lang.String",
                                                                                        "GroupName": ""},
                                                          "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                                            "Name": "NODE_INITIATED_DISCOVERY_SET_TRAP_"
                                                                                                                    "DESTINATION",
                                                                                                            "DefaultValue": "false",
                                                                                                            "Value": "true",
                                                                                                            "DataType": "java.lang.Boolean",
                                                                                                            "GroupName": ""},
                                                          "DEVICE_PREFERRED_NAME": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                    "Name": "DEVICE_PREFERRED_NAME",
                                                                                    "DefaultValue": "HOST_NAME",
                                                                                    "Value": "PREFER_DNS,PREFER_IDRAC_HOSTNAME",
                                                                                    "DataType": "java.lang.String",
                                                                                    "GroupName": "DISCOVERY_SETTING"},
                                                          "INVALID_DEVICE_HOSTNAME": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                      "Name": "INVALID_DEVICE_HOSTNAME",
                                                                                      "DefaultValue": "",
                                                                                      "Value": "localhost",
                                                                                      "DataType": "java.lang.String",
                                                                                      "GroupName": "DISCOVERY_SETTING"},
                                                          "COMMON_MAC_ADDRESSES": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                   "Name": "COMMON_MAC_ADDRESSES",
                                                                                   "DefaultValue": "",
                                                                                   "Value": "::",
                                                                                   "DataType": "java.lang.String",
                                                                                   "GroupName": "DISCOVERY_SETTING"},
                                                          "MIN_PROTOCOL_VERSION": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                   "Name": "MIN_PROTOCOL_VERSION",
                                                                                   "DefaultValue": "V2",
                                                                                   "Value": "V2",
                                                                                   "DataType": "java.lang.String",
                                                                                   "GroupName": "CIFS_PROTOCOL_SETTINGS"},
                                                          "CONSOLE_CONNECTION_SETTING": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                         "Name": "CONSOLE_CONNECTION_SETTING",
                                                                                         "DefaultValue": "last_known",
                                                                                         "Value": "last_known",
                                                                                         "DataType": "java.lang.String",
                                                                                         "GroupName": "CONSOLE_CONNECTION_SETTING"},
                                                          "SHARE_TYPE": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                         "Name": "SHARE_TYPE",
                                                                         "DefaultValue": "CIFS",
                                                                         "Value": "CIFS",
                                                                         "DataType": "java.lang.String",
                                                                         "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"}},
                                         "schedule": "0 0 0/5 1/1 * ? *",
                                         "module_args": {"device_health": {"health_check_interval": 50,
                                                                           "health_check_interval_unit": "Minutes"}}}])
    def test_update_console_preferences_case03(self, params, ome_connection_mock_for_application_console_preferences,
                                               ome_response_mock, ome_default_args):
        ome_response_mock.success = True
        ome_default_args.update(params["module_args"])
        # ome_response_mock.json_data = {"value": [params["payload"]]}
        f_module = self.get_module_mock(params=params['module_args'])
        final_resp, cifs_resp, job_resp = self.module.update_console_preferences(f_module,
                                                                                 ome_connection_mock_for_application_console_preferences,
                                                                                 params["payload"],
                                                                                 params["cifs_payload"],
                                                                                 params["job_payload"],
                                                                                 params["job_data"],
                                                                                 params["payload_dict"],
                                                                                 params["schedule"])
        assert job_resp.success is True

    @pytest.mark.parametrize("params", [{"module_args": {"report_row_limit": 123},
                                         "payload": {"ConsoleSetting": [{"Name": "DATA_PURGE_INTERVAL",
                                                                         "DefaultValue": "365",
                                                                         "Value": "361",
                                                                         "DataType": "java.lang.Integer",
                                                                         "GroupName": ""},
                                                                        {"Name": "TRAP_FORWARDING_SETTING",
                                                                         "DefaultValue": "AsIs",
                                                                         "Value": "AsIs",
                                                                         "DataType": "java.lang.String",
                                                                         "GroupName": ""},
                                                                        {"Name": "DEVICE_PREFERRED_NAME",
                                                                         "DefaultValue": "SLOT_NAME",
                                                                         "Value": "PREFER_DNS,PREFER_IDRAC_SYSTEM_HOSTNAME",
                                                                         "DataType": "java.lang.String",
                                                                         "GroupName": "DISCOVERY_SETTING"}]},
                                         "curr_payload": {"DATA_PURGE_INTERVAL": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                  "Name": "DATA_PURGE_INTERVAL",
                                                                                  "DefaultValue": "365",
                                                                                  "Value": "361",
                                                                                  "DataType": "java.lang.Integer",
                                                                                  "GroupName": ""},
                                                          "TRAP_FORWARDING_SETTING": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                      "Name": "TRAP_FORWARDING_SETTING",
                                                                                      "DefaultValue": "AsIs",
                                                                                      "Value": "Normalized",
                                                                                      "DataType": "java.lang.String",
                                                                                      "GroupName": ""},
                                                          "MX7000_ONBOARDING_PREF": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                     "Name": "MX7000_ONBOARDING_PREF",
                                                                                     "DefaultValue": "all",
                                                                                     "Value": "all",
                                                                                     "DataType": "java.lang.String",
                                                                                     "GroupName": ""},
                                                          "REPORTS_MAX_RESULTS_LIMIT": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                        "Name": "REPORTS_MAX_RESULTS_LIMIT",
                                                                                        "DefaultValue": "0",
                                                                                        "Value": "123",
                                                                                        "DataType": "java.lang.Integer",
                                                                                        "GroupName": ""},
                                                          "EMAIL_SENDER": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                           "Name": "EMAIL_SENDER",
                                                                           "DefaultValue": "omcadmin@dell.com",
                                                                           "Value": "admin@dell.com",
                                                                           "DataType": "java.lang.String",
                                                                           "GroupName": ""},
                                                          "DISCOVERY_APPROVAL_POLICY": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                        "Name": "DISCOVERY_APPROVAL_POLICY",
                                                                                        "DefaultValue": "Automatic",
                                                                                        "Value": "Automatic",
                                                                                        "DataType": "java.lang.String",
                                                                                        "GroupName": ""},
                                                          "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                                            "Name": "NODE_INITIATED_DISCOVERY_SET_TRAP_"
                                                                                                                    "DESTINATION",
                                                                                                            "DefaultValue": "false",
                                                                                                            "Value": "true",
                                                                                                            "DataType": "java.lang.Boolean",
                                                                                                            "GroupName": ""},
                                                          "DEVICE_PREFERRED_NAME": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                    "Name": "DEVICE_PREFERRED_NAME",
                                                                                    "DefaultValue": "HOST_NAME",
                                                                                    "Value": "PREFER_DNS,PREFER_IDRAC_HOSTNAME",
                                                                                    "DataType": "java.lang.String",
                                                                                    "GroupName": "DISCOVERY_SETTING"},
                                                          "INVALID_DEVICE_HOSTNAME": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                      "Name": "INVALID_DEVICE_HOSTNAME",
                                                                                      "DefaultValue": "",
                                                                                      "Value": "localhost",
                                                                                      "DataType": "java.lang.String",
                                                                                      "GroupName": "DISCOVERY_SETTING"},
                                                          "COMMON_MAC_ADDRESSES": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                   "Name": "COMMON_MAC_ADDRESSES",
                                                                                   "DefaultValue": "",
                                                                                   "Value": "::",
                                                                                   "DataType": "java.lang.String",
                                                                                   "GroupName": "DISCOVERY_SETTING"},
                                                          "MIN_PROTOCOL_VERSION": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                   "Name": "MIN_PROTOCOL_VERSION",
                                                                                   "DefaultValue": "V2",
                                                                                   "Value": "V2",
                                                                                   "DataType": "java.lang.String",
                                                                                   "GroupName": "CIFS_PROTOCOL_SETTINGS"},
                                                          "CONSOLE_CONNECTION_SETTING": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                         "Name": "CONSOLE_CONNECTION_SETTING",
                                                                                         "DefaultValue": "last_known",
                                                                                         "Value": "last_known",
                                                                                         "DataType": "java.lang.String",
                                                                                         "GroupName": "CONSOLE_CONNECTION_SETTING"},
                                                          "SHARE_TYPE": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                         "Name": "SHARE_TYPE",
                                                                         "DefaultValue": "CIFS",
                                                                         "Value": "CIFS",
                                                                         "DataType": "java.lang.String",
                                                                         "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"}},
                                         "json_data": {"value": [{"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "DATA_PURGE_INTERVAL",
                                                                  "DefaultValue": "365",
                                                                  "Value": "361",
                                                                  "DataType": "java.lang.Integer",
                                                                  "GroupName": ""},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "TRAP_FORWARDING_SETTING",
                                                                  "DefaultValue": "AsIs",
                                                                  "Value": "Normalized",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": ""},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "MX7000_ONBOARDING_PREF",
                                                                  "DefaultValue": "all",
                                                                  "Value": "all",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": ""},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "REPORTS_MAX_RESULTS_LIMIT",
                                                                  "DefaultValue": "0",
                                                                  "Value": "123",
                                                                  "DataType": "java.lang.Integer",
                                                                  "GroupName": ""},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "EMAIL_SENDER",
                                                                  "DefaultValue": "omcadmin@dell.com",
                                                                  "Value": "admin@dell.com",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": ""},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "DISCOVERY_APPROVAL_POLICY",
                                                                  "DefaultValue": "Automatic",
                                                                  "Value": "Automatic",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": ""},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION",
                                                                  "DefaultValue": "false",
                                                                  "Value": "true",
                                                                  "DataType": "java.lang.Boolean",
                                                                  "GroupName": ""},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "DEVICE_PREFERRED_NAME",
                                                                  "DefaultValue": "HOST_NAME",
                                                                  "Value": "PREFER_DNS,PREFER_IDRAC_HOSTNAME",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": "DISCOVERY_SETTING"},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "INVALID_DEVICE_HOSTNAME",
                                                                  "DefaultValue": "",
                                                                  "Value": "localhost",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": "DISCOVERY_SETTING"},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "COMMON_MAC_ADDRESSES",
                                                                  "DefaultValue": "",
                                                                  "Value": "::",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": "DISCOVERY_SETTING"},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "MIN_PROTOCOL_VERSION",
                                                                  "DefaultValue": "V2",
                                                                  "Value": "V2",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": "CIFS_PROTOCOL_SETTINGS"},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "CONSOLE_CONNECTION_SETTING",
                                                                  "DefaultValue": "last_known",
                                                                  "Value": "last_known",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": "CONSOLE_CONNECTION_SETTING"},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "SHARE_TYPE",
                                                                  "DefaultValue": "CIFS",
                                                                  "Value": "CIFS",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"}]}, }])
    def test_create_payload_dict(self, params, ome_connection_mock_for_application_console_preferences,
                                 ome_response_mock, ome_default_args, mocker):
        ome_response_mock.success = True
        ome_response_mock.json_data = {"value": [params["payload"]]}
        f_module = self.get_module_mock(params=params['module_args'])
        curr_payload = params["json_data"]["value"]
        ret_payload = self.module.create_payload_dict(curr_payload)
        assert ret_payload == params["curr_payload"]

    @pytest.mark.parametrize("params", [{"module_args": {"builtin_appliance_share": {"share_options": "CIFS",
                                                                                     "cifs_options": "V2"}},
                                         "payload": {"ConsoleSetting": [{"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                         "Name": "SHARE_TYPE",
                                                                         "DefaultValue": "CIFS",
                                                                         "Value": "CIFS",
                                                                         "DataType": "java.lang.String",
                                                                         "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"}]},
                                         "curr_payload": {"DATA_PURGE_INTERVAL": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                  "Name": "DATA_PURGE_INTERVAL",
                                                                                  "DefaultValue": "365",
                                                                                  "Value": "361",
                                                                                  "DataType": "java.lang.Integer",
                                                                                  "GroupName": ""},
                                                          "TRAP_FORWARDING_SETTING": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                      "Name": "TRAP_FORWARDING_SETTING",
                                                                                      "DefaultValue": "AsIs",
                                                                                      "Value": "Normalized",
                                                                                      "DataType": "java.lang.String",
                                                                                      "GroupName": ""},
                                                          "MX7000_ONBOARDING_PREF": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                     "Name": "MX7000_ONBOARDING_PREF",
                                                                                     "DefaultValue": "all",
                                                                                     "Value": "all",
                                                                                     "DataType": "java.lang.String",
                                                                                     "GroupName": ""},
                                                          "REPORTS_MAX_RESULTS_LIMIT": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                        "Name": "REPORTS_MAX_RESULTS_LIMIT",
                                                                                        "DefaultValue": "0",
                                                                                        "Value": "123",
                                                                                        "DataType": "java.lang.Integer",
                                                                                        "GroupName": ""},
                                                          "EMAIL_SENDER": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                           "Name": "EMAIL_SENDER",
                                                                           "DefaultValue": "omcadmin@dell.com",
                                                                           "Value": "admin@dell.com",
                                                                           "DataType": "java.lang.String",
                                                                           "GroupName": ""},
                                                          "DISCOVERY_APPROVAL_POLICY": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                        "Name": "DISCOVERY_APPROVAL_POLICY",
                                                                                        "DefaultValue": "Automatic",
                                                                                        "Value": "Automatic",
                                                                                        "DataType": "java.lang.String",
                                                                                        "GroupName": ""},
                                                          "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                                            "Name": "NODE_INITIATED_DISCOVERY_SET_TRAP_"
                                                                                                                    "DESTINATION",
                                                                                                            "DefaultValue": "false",
                                                                                                            "Value": "true",
                                                                                                            "DataType": "java.lang.Boolean",
                                                                                                            "GroupName": ""},
                                                          "DEVICE_PREFERRED_NAME": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                    "Name": "DEVICE_PREFERRED_NAME",
                                                                                    "DefaultValue": "HOST_NAME",
                                                                                    "Value": "PREFER_DNS,PREFER_IDRAC_HOSTNAME",
                                                                                    "DataType": "java.lang.String",
                                                                                    "GroupName": "DISCOVERY_SETTING"},
                                                          "INVALID_DEVICE_HOSTNAME": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                      "Name": "INVALID_DEVICE_HOSTNAME",
                                                                                      "DefaultValue": "",
                                                                                      "Value": "localhost",
                                                                                      "DataType": "java.lang.String",
                                                                                      "GroupName": "DISCOVERY_SETTING"},
                                                          "COMMON_MAC_ADDRESSES": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                   "Name": "COMMON_MAC_ADDRESSES",
                                                                                   "DefaultValue": "",
                                                                                   "Value": "::",
                                                                                   "DataType": "java.lang.String",
                                                                                   "GroupName": "DISCOVERY_SETTING"},
                                                          "MIN_PROTOCOL_VERSION": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                   "Name": "MIN_PROTOCOL_VERSION",
                                                                                   "DefaultValue": "V2",
                                                                                   "Value": "V2",
                                                                                   "DataType": "java.lang.String",
                                                                                   "GroupName": "CIFS_PROTOCOL_SETTINGS"},
                                                          "CONSOLE_CONNECTION_SETTING": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                                         "Name": "CONSOLE_CONNECTION_SETTING",
                                                                                         "DefaultValue": "last_known",
                                                                                         "Value": "last_known",
                                                                                         "DataType": "java.lang.String",
                                                                                         "GroupName": "CONSOLE_CONNECTION_SETTING"},
                                                          "SHARE_TYPE": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                         "Name": "SHARE_TYPE",
                                                                         "DefaultValue": "CIFS",
                                                                         "Value": "CIFS",
                                                                         "DataType": "java.lang.String",
                                                                         "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"}},
                                         "json_data": {"value": [{"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "DATA_PURGE_INTERVAL",
                                                                  "DefaultValue": "365",
                                                                  "Value": "361",
                                                                  "DataType": "java.lang.Integer",
                                                                  "GroupName": ""},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "TRAP_FORWARDING_SETTING",
                                                                  "DefaultValue": "AsIs",
                                                                  "Value": "Normalized",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": ""},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "MX7000_ONBOARDING_PREF",
                                                                  "DefaultValue": "all",
                                                                  "Value": "all",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": ""},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "REPORTS_MAX_RESULTS_LIMIT",
                                                                  "DefaultValue": "0",
                                                                  "Value": "123",
                                                                  "DataType": "java.lang.Integer",
                                                                  "GroupName": ""},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "EMAIL_SENDER",
                                                                  "DefaultValue": "omcadmin@dell.com",
                                                                  "Value": "admin@dell.com",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": ""},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "DISCOVERY_APPROVAL_POLICY",
                                                                  "DefaultValue": "Automatic",
                                                                  "Value": "Automatic",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": ""},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION",
                                                                  "DefaultValue": "false",
                                                                  "Value": "true",
                                                                  "DataType": "java.lang.Boolean",
                                                                  "GroupName": ""},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "DEVICE_PREFERRED_NAME",
                                                                  "DefaultValue": "HOST_NAME",
                                                                  "Value": "PREFER_DNS,PREFER_IDRAC_HOSTNAME",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": "DISCOVERY_SETTING"},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "INVALID_DEVICE_HOSTNAME",
                                                                  "DefaultValue": "",
                                                                  "Value": "localhost",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": "DISCOVERY_SETTING"},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "COMMON_MAC_ADDRESSES",
                                                                  "DefaultValue": "",
                                                                  "Value": "::",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": "DISCOVERY_SETTING"},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "MIN_PROTOCOL_VERSION",
                                                                  "DefaultValue": "V2",
                                                                  "Value": "V2",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": "CIFS_PROTOCOL_SETTINGS"},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "CONSOLE_CONNECTION_SETTING",
                                                                  "DefaultValue": "last_known",
                                                                  "Value": "last_known",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": "CONSOLE_CONNECTION_SETTING"},
                                                                 {"@odata.type": "#ApplicationService.ConsoleSetting",
                                                                  "Name": "SHARE_TYPE",
                                                                  "DefaultValue": "CIFS",
                                                                  "Value": "CIFS",
                                                                  "DataType": "java.lang.String",
                                                                  "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"}]}, }])
    def test_create_cifs_payload(self, params, ome_connection_mock_for_application_console_preferences,
                                 ome_response_mock, ome_default_args, mocker):
        ome_response_mock.success = True
        ome_response_mock.json_data = {"value": [params["payload"]]}
        f_module = self.get_module_mock(params=params['module_args'])
        curr_payload = params["json_data"]["value"]
        ret_payload = self.module.create_cifs_payload(ome_connection_mock_for_application_console_preferences,
                                                      curr_payload)
        assert ret_payload.get("ConsoleSetting")[0]["Name"] == params["payload"]["ConsoleSetting"][0]["Name"]

    @pytest.mark.parametrize("params", [{"module_args": {"device_health": {"health_check_interval": 50,
                                                                           "health_check_interval_unit": "Minutes"}},
                                         "job_payload": {"Id": 0,
                                                         "JobName": "Global Health Task",
                                                         "JobDescription": "Global Health Task",
                                                         "Schedule": None,
                                                         "State": "Enabled",
                                                         "JobType": {"Id": 6, "Name": "Health_Task"},
                                                         "Params": [{"Key": "metricType", "Value": "40, 50"}],
                                                         "Targets": [{"Id": 500, "Data": "", "TargetType": {"Id": 6000, "Name": "GROUP"}}]}}])
    def test_create_job(self, params, ome_connection_mock_for_application_console_preferences,
                        ome_response_mock, ome_default_args, mocker):
        ome_response_mock.success = True
        ome_response_mock.json_data = params["job_payload"]
        ome_default_args.update(params['module_args'])
        job_payload, schedule = self.module.create_job(ome_connection_mock_for_application_console_preferences)
        assert job_payload == params["job_payload"]

    @pytest.mark.parametrize("params", [{"module_args": {"device_health": {"health_check_interval": 5,
                                                                           "health_check_interval_unit": "Hourly"}},
                                         "job_payload": {"Id": 0,
                                                         "JobName": "Global Health Task",
                                                         "JobDescription": "Global Health Task",
                                                         "Schedule": "0 0 0/5 1/1 * ? *",
                                                         "State": "Enabled",
                                                         "JobType": {"Id": 6, "Name": "Health_Task"},
                                                         "Params": [{"Key": "metricType", "Value": "40, 50"}],
                                                         "Targets": [{"Id": 500, "Data": "", "TargetType": {"Id": 6000, "Name": "GROUP"}}]},
                                         "schedule": "0 0 0/5 1/1 * ? *"}])
    def test_create_job_case02(self, params, ome_connection_mock_for_application_console_preferences,
                               ome_response_mock, ome_default_args, mocker):
        ome_response_mock.success = True
        f_module = self.get_module_mock(params=params['module_args'])
        ome_response_mock.json_data = params["job_payload"]
        ome_default_args.update(params['module_args'])
        job_payload, schedule = self.module.create_job(f_module)
        assert schedule == params["schedule"]

    @pytest.mark.parametrize("params", [{"module_args": {"device_health": {"health_check_interval": 5,
                                                                           "health_check_interval_unit": "Minutes"}},
                                         "job_payload": {"Id": 0,
                                                         "JobName": "Global Health Task",
                                                         "JobDescription": "Global Health Task",
                                                         "Schedule": "0 0/5 * 1/1 * ? *",
                                                         "State": "Enabled",
                                                         "JobType": {"Id": 6, "Name": "Health_Task"},
                                                         "Params": [{"Key": "metricType", "Value": "40, 50"}],
                                                         "Targets": [{"Id": 500, "Data": "", "TargetType": {"Id": 6000, "Name": "GROUP"}}]},
                                         "schedule": "0 0/5 * 1/1 * ? *"}])
    def test_create_job_case03(self, params, ome_connection_mock_for_application_console_preferences,
                               ome_response_mock, ome_default_args, mocker):
        ome_response_mock.success = True
        f_module = self.get_module_mock(params=params['module_args'])
        ome_response_mock.json_data = params["job_payload"]
        ome_default_args.update(params['module_args'])
        job_payload, schedule = self.module.create_job(f_module)
        assert schedule == params["schedule"]

    @pytest.mark.parametrize("params", [
        {
            "module_args": {"metrics_collection_settings": 361},
            "cifs_payload": {"ConsoleSetting": [{"@odata.type": "#ApplicationService.ConsoleSetting",
                                                 "Name": "SHARE_TYPE",
                                                 "DefaultValue": "CIFS",
                                                 "Value": "CIFS",
                                                 "DataType": "java.lang.String",
                                                 "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"}]},
            "cp_data": {"value": [{"@odata.type": "#ApplicationService.ConsoleSetting",
                                   "Name": "DATA_PURGE_INTERVAL",
                                   "DefaultValue": "365",
                                   "Value": "361",
                                   "DataType": "java.lang.Integer",
                                   "GroupName": ""},
                                  {"@odata.type": "#ApplicationService.ConsoleSetting",
                                   "Name": "TRAP_FORWARDING_SETTING",
                                   "DefaultValue": "AsIs",
                                   "Value": "Normalized",
                                   "DataType": "java.lang.String",
                                   "GroupName": ""},
                                  {"@odata.type": "#ApplicationService.ConsoleSetting",
                                   "Name": "MX7000_ONBOARDING_PREF",
                                   "DefaultValue": "all",
                                   "Value": "all",
                                   "DataType": "java.lang.String",
                                   "GroupName": ""},
                                  {"@odata.type": "#ApplicationService.ConsoleSetting",
                                   "Name": "REPORTS_MAX_RESULTS_LIMIT",
                                   "DefaultValue": "0",
                                   "Value": "123",
                                   "DataType": "java.lang.Integer",
                                   "GroupName": ""},
                                  {"@odata.type": "#ApplicationService.ConsoleSetting",
                                   "Name": "EMAIL_SENDER",
                                   "DefaultValue": "omcadmin@dell.com",
                                   "Value": "admin@dell.com",
                                   "DataType": "java.lang.String",
                                   "GroupName": ""}, ]},
            "payload": {"ConsoleSetting": [{"@odata.type": "#ApplicationService.ConsoleSetting",
                                            "Name": "DATA_PURGE_INTERVAL",
                                            "DefaultValue": "365",
                                            "Value": "361",
                                            "DataType": "java.lang.Integer",
                                            "GroupName": ""}]}, }])
    def test_module_idempotent(self, mocker, params, ome_connection_mock_for_application_console_preferences,
                               ome_response_mock, ome_default_args):
        curr_resp = params["cp_data"]["value"]
        payload = params["payload"]
        cifs_payload = params["cifs_payload"]
        schedule = None
        job = None
        diff = self.module._diff_payload(curr_resp, payload, cifs_payload, schedule, job)
        assert diff == 0

    @pytest.mark.parametrize("params", [
        {
            "module_args": {"metrics_collection_settings": 361},
            "cifs_payload": {"ConsoleSetting": [{"@odata.type": "#ApplicationService.ConsoleSetting",
                                                 "Name": "SHARE_TYPE",
                                                 "DefaultValue": "CIFS",
                                                 "Value": "CIFS",
                                                 "DataType": "java.lang.String",
                                                 "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"}]},
            "cp_data": {"value": [{"@odata.type": "#ApplicationService.ConsoleSetting",
                                   "Name": "DATA_PURGE_INTERVAL",
                                   "DefaultValue": "365",
                                   "Value": "361",
                                   "DataType": "java.lang.Integer",
                                   "GroupName": ""},
                                  {"@odata.type": "#ApplicationService.ConsoleSetting",
                                   "Name": "TRAP_FORWARDING_SETTING",
                                   "DefaultValue": "AsIs",
                                   "Value": "Normalized",
                                   "DataType": "java.lang.String",
                                   "GroupName": ""},
                                  {"@odata.type": "#ApplicationService.ConsoleSetting",
                                   "Name": "MX7000_ONBOARDING_PREF",
                                   "DefaultValue": "all",
                                   "Value": "all",
                                   "DataType": "java.lang.String",
                                   "GroupName": ""},
                                  {"@odata.type": "#ApplicationService.ConsoleSetting",
                                   "Name": "REPORTS_MAX_RESULTS_LIMIT",
                                   "DefaultValue": "0",
                                   "Value": "123",
                                   "DataType": "java.lang.Integer",
                                   "GroupName": ""},
                                  {"@odata.type": "#ApplicationService.ConsoleSetting",
                                   "Name": "EMAIL_SENDER",
                                   "DefaultValue": "omcadmin@dell.com",
                                   "Value": "admin@dell.com",
                                   "DataType": "java.lang.String",
                                   "GroupName": ""}, ]},
            "payload": {"ConsoleSetting": [{"@odata.type": "#ApplicationService.ConsoleSetting",
                                            "Name": "DATA_PURGE_INTERVAL",
                                            "DefaultValue": "365",
                                            "Value": "365",
                                            "DataType": "java.lang.Integer",
                                            "GroupName": ""}]}, }])
    def test_module_idempotent_case02(self, mocker, params, ome_connection_mock_for_application_console_preferences,
                                      ome_response_mock, ome_default_args):
        curr_resp = params["cp_data"]["value"]
        payload = params["payload"]
        cifs_payload = params["cifs_payload"]
        schedule = None
        job = None
        diff = self.module._diff_payload(curr_resp, payload, cifs_payload, schedule, job)
        assert diff == 1

    @pytest.mark.parametrize("params", [
        {
            "module_args": {"device_health": {"health_check_interval": 5,
                                              "health_check_interval_unit": "Hourly"}},
            "json_data": {"@odata.type": "#JobService.Job",
                          "@odata.id": "/api/JobService/Jobs(10093)",
                          "Id": 10093,
                          "JobName": "Global Health Task",
                          "JobDescription": "Global Health Task",
                          "NextRun": "2022-03-15 05:25:00.0",
                          "LastRun": "2022-03-15 05:24:00.043",
                          "StartTime": None,
                          "EndTime": None,
                          "Schedule": "0 0 0/5 1/1 * ? *",
                          "State": "Enabled",
                          "CreatedBy": "admin",
                          "UpdatedBy": None,
                          "Visible": None,
                          "Editable": None,
                          "Builtin": False,
                          "UserGenerated": True,
                          "Targets": [{"JobId": 10093, "Id": 500, "Data": "", "TargetType": {"Id": 6000, "Name": "GROUP"}}],
                          "Params": [{"JobId": 10093, "Key": "metricType", "Value": "40, 50"}],
                          "LastRunStatus": {"@odata.type": "#JobService.JobStatus", "Id": 2060, "Name": "Completed"},
                          "JobType": {"@odata.type": "#JobService.JobType", "Id": 6, "Name": "Health_Task", "Internal": False},
                          "JobStatus": {"@odata.type": "#JobService.JobStatus", "Id": 2020, "Name": "Scheduled"},
                          "ExecutionHistories@odata.navigationLink": "/api/JobService/Jobs(10093)/ExecutionHistories",
                          "LastExecutionDetail": {"@odata.id": "/api/JobService/Jobs(10093)/LastExecutionDetail"}},
            "cp_data":
                {"value": [{"@odata.type": "#ApplicationService.ConsoleSetting",
                            "Name": "DATA_PURGE_INTERVAL",
                            "DefaultValue": "365",
                            "Value": "361",
                            "DataType": "java.lang.Integer",
                            "GroupName": ""},
                           {"@odata.type": "#ApplicationService.ConsoleSetting",
                            "Name": "TRAP_FORWARDING_SETTING",
                            "DefaultValue": "AsIs",
                            "Value": "Normalized",
                            "DataType": "java.lang.String",
                            "GroupName": ""},
                           {"@odata.type": "#ApplicationService.ConsoleSetting",
                            "Name": "MX7000_ONBOARDING_PREF",
                            "DefaultValue": "all",
                            "Value": "all",
                            "DataType": "java.lang.String",
                            "GroupName": ""},
                           {"@odata.type": "#ApplicationService.ConsoleSetting",
                            "Name": "REPORTS_MAX_RESULTS_LIMIT",
                            "DefaultValue": "0",
                            "Value": "123",
                            "DataType": "java.lang.Integer",
                            "GroupName": ""},
                           {"@odata.type": "#ApplicationService.ConsoleSetting",
                            "Name": "EMAIL_SENDER",
                            "DefaultValue": "omcadmin@dell.com",
                            "Value": "admin@dell.com",
                            "DataType": "java.lang.String",
                            "GroupName": ""}, ]},
            "schedule": "0 0 0/5 1/1 * ? *",
            "payload": {"ConsoleSetting": [{"@odata.type": "#ApplicationService.ConsoleSetting",
                                            "Name": "DATA_PURGE_INTERVAL",
                                            "DefaultValue": "365",
                                            "Value": "365",
                                            "DataType": "java.lang.Integer",
                                            "GroupName": ""}]},
            "cifs_payload": {"ConsoleSetting": [{"@odata.type": "#ApplicationService.ConsoleSetting",
                                                 "Name": "SHARE_TYPE",
                                                 "DefaultValue": "CIFS",
                                                 "Value": "CIFS",
                                                 "DataType": "java.lang.String",
                                                 "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"}]}}])
    def test_module_idempotent_case03(self, mocker, params, ome_connection_mock_for_application_console_preferences,
                                      ome_response_mock, ome_default_args):
        curr_resp = params["cp_data"]["value"]
        payload = params["payload"]
        cifs_payload = params["cifs_payload"]
        schedule = params["schedule"]
        job = params["json_data"]
        diff = self.module._diff_payload(curr_resp, payload, cifs_payload, schedule, job)
        assert diff == 1

    @pytest.mark.parametrize("params", [
        {
            "module_args": {"device_health": {"health_check_interval": 100,
                                              "health_check_interval_unit": "Minutes"}
                            }}])
    def test__validate_params_fail_case01(self, params, ome_connection_mock_for_application_console_preferences):
        health = params['module_args'].get("device_health").get("health_check_interval_unit")
        f_module = self.get_module_mock(params=params['module_args'])
        with pytest.raises(Exception) as exc:
            self.module._validate_params(f_module)
        assert exc.value.args[0] == HEALTH_CHECK_INTERVAL_INVALID.format(health)

    @pytest.mark.parametrize("params", [
        {
            "module_args": {"device_health": {"health_check_interval_unit": "Minutes"}
                            }}])
    def test__validate_params_fail_case02(self, params, ome_connection_mock_for_application_console_preferences):
        f_module = self.get_module_mock(params=params['module_args'])
        with pytest.raises(Exception) as exc:
            self.module._validate_params(f_module)
        assert exc.value.args[0] == HEALTH_CHECK_INTERVAL_REQUIRED

    @pytest.mark.parametrize("params", [
        {
            "module_args": {"device_health": {"health_check_interval": 50}
                            }}])
    def test__validate_params_fail_case03(self, params, ome_connection_mock_for_application_console_preferences):
        f_module = self.get_module_mock(params=params['module_args'])
        with pytest.raises(Exception) as exc:
            self.module._validate_params(f_module)
        assert exc.value.args[0] == HEALTH_CHECK_UNIT_REQUIRED

    @pytest.mark.parametrize("params", [
        {
            "module_args": {"device_health": {"health_check_interval": 100,
                                              "health_check_interval_unit": "Hourly"}
                            }}])
    def test__validate_params_fail_case04(self, params, ome_connection_mock_for_application_console_preferences):
        health = params['module_args'].get("device_health").get("health_check_interval_unit")
        f_module = self.get_module_mock(params=params['module_args'])
        with pytest.raises(Exception) as exc:
            self.module._validate_params(f_module)
        assert exc.value.args[0] == HEALTH_CHECK_INTERVAL_INVALID.format(health)

    @pytest.mark.parametrize("params", [
        {
            "module_args": {"report_row_limit": 123,
                            "mx7000_onboarding_preferences": "all",
                            "email_sender_settings": "admin@dell.com",
                            "trap_forwarding_format": "Normalized",
                            "metrics_collection_settings": 361
                            },
            "json_data": {"value": [{"@odata.type": "#ApplicationService.ConsoleSetting",
                                     "Name": "DATA_PURGE_INTERVAL",
                                     "DefaultValue": "365",
                                     "Value": "361",
                                     "DataType": "java.lang.Integer",
                                     "GroupName": ""},
                                    {"@odata.type": "#ApplicationService.ConsoleSetting",
                                     "Name": "TRAP_FORWARDING_SETTING",
                                     "DefaultValue": "AsIs",
                                     "Value": "Normalized",
                                     "DataType": "java.lang.String",
                                     "GroupName": ""},
                                    {"@odata.type": "#ApplicationService.ConsoleSetting",
                                     "Name": "MX7000_ONBOARDING_PREF",
                                     "DefaultValue": "all",
                                     "Value": "all",
                                     "DataType": "java.lang.String",
                                     "GroupName": ""},
                                    {"@odata.type": "#ApplicationService.ConsoleSetting",
                                     "Name": "REPORTS_MAX_RESULTS_LIMIT",
                                     "DefaultValue": "0",
                                     "Value": "123",
                                     "DataType": "java.lang.Integer",
                                     "GroupName": ""},
                                    {"@odata.type": "#ApplicationService.ConsoleSetting",
                                     "Name": "EMAIL_SENDER",
                                     "DefaultValue": "omcadmin@dell.com",
                                     "Value": "admin@dell.com",
                                     "DataType": "java.lang.String",
                                     "GroupName": ""}, ]}, }])
    def test_module_check_mode(self, mocker, params, ome_connection_mock_for_application_console_preferences,
                               ome_response_mock, ome_default_args):
        ome_response_mock.success = True
        ome_response_mock.status_code = 201
        ome_response_mock.json_data = {"value": [params["json_data"]]}
        ome_default_args.update(params['module_args'])
        f_module = self.get_module_mock(params=ome_default_args)
        get_json_data = params["json_data"]
        update_json_data = params["json_data"]

        f_module.check_mode = True

        with pytest.raises(Exception) as err:
            self.module.process_check_mode(f_module, 0)
        assert err.value.args[0] == NO_CHANGES

        with pytest.raises(Exception) as err:
            self.module.process_check_mode(f_module, 1)
        assert err.value.args[0] == CHANGES_FOUND

        f_module.check_mode = False

        with pytest.raises(Exception) as err:
            self.module.process_check_mode(f_module, 0)
        assert err.value.args[0] == NO_CHANGES

    @pytest.mark.parametrize("params", [
        {
            "job_details": {
                "@odata.type": "#JobService.Job",
                "@odata.id": "/api/JobService/Jobs(10093)",
                "Id": 10093,
                "JobName": "Global Health Task",
                "JobDescription": "Global Health Task",
                "NextRun": "2022-03-15 05:25:00.0",
                "LastRun": "2022-03-15 05:24:00.043",
                "StartTime": None,
                "EndTime": None,
                "Schedule": "0 0/1 * 1/1 * ? *",
                "State": "Enabled",
                "CreatedBy": "admin",
                "UpdatedBy": None,
                "Visible": None,
                "Editable": None,
                "Builtin": False,
                "UserGenerated": True,
                "Targets": [{"JobId": 10093, "Id": 500, "Data": "", "TargetType": {"Id": 6000, "Name": "GROUP"}}],
                "Params": [{"JobId": 10093, "Key": "metricType", "Value": "40, 50"}],
                "LastRunStatus": {"@odata.type": "#JobService.JobStatus", "Id": 2060, "Name": "Completed"},
                "JobType": {"@odata.type": "#JobService.JobType", "Id": 6, "Name": "Health_Task", "Internal": False},
                "JobStatus": {"@odata.type": "#JobService.JobStatus", "Id": 2020, "Name": "Scheduled"},
                "ExecutionHistories@odata.navigationLink": "/api/JobService/Jobs(10093)/ExecutionHistories",
                "LastExecutionDetail": {"@odata.id": "/api/JobService/Jobs(10093)/LastExecutionDetail"}
            },
            "job_payload": {"Id": 0,
                            "JobName": "Global Health Task",
                            "JobDescription": "Global Health Task",
                            "Schedule": None,
                            "State": "Enabled",
                            "JobType": {"Id": 6, "Name": "Health_Task"},
                            "Params": [{"Key": "metricType", "Value": "40, 50"}],
                            "Targets": [{"Id": 500, "Data": "", "TargetType": {"Id": 6000, "Name": "GROUP"}}]},
            "cp_data": {"value": [{"@odata.type": "#ApplicationService.ConsoleSetting",
                                   "Name": "DATA_PURGE_INTERVAL",
                                   "DefaultValue": "365",
                                   "Value": "361",
                                   "DataType": "java.lang.Integer",
                                   "GroupName": ""},
                                  {"@odata.type": "#ApplicationService.ConsoleSetting",
                                   "Name": "TRAP_FORWARDING_SETTING",
                                   "DefaultValue": "AsIs",
                                   "Value": "Normalized",
                                   "DataType": "java.lang.String",
                                   "GroupName": ""},
                                  {"@odata.type": "#ApplicationService.ConsoleSetting",
                                   "Name": "MX7000_ONBOARDING_PREF",
                                   "DefaultValue": "all",
                                   "Value": "all",
                                   "DataType": "java.lang.String",
                                   "GroupName": ""},
                                  {"@odata.type": "#ApplicationService.ConsoleSetting",
                                   "Name": "REPORTS_MAX_RESULTS_LIMIT",
                                   "DefaultValue": "0",
                                   "Value": "123",
                                   "DataType": "java.lang.Integer",
                                   "GroupName": ""},
                                  {"@odata.type": "#ApplicationService.ConsoleSetting",
                                   "Name": "EMAIL_SENDER",
                                   "DefaultValue": "omcadmin@dell.com",
                                   "Value": "admin@dell.com",
                                   "DataType": "java.lang.String",
                                   "GroupName": ""}, ]},
            "payload_dict":
                {"DATA_PURGE_INTERVAL": {"@odata.type": "#ApplicationService.ConsoleSetting",
                                         "Name": "DATA_PURGE_INTERVAL",
                                         "DefaultValue": "365",
                                         "Value": "361",
                                         "DataType": "java.lang.Integer",
                                         "GroupName": ""},
                 "TRAP_FORWARDING_SETTING":
                     {"@odata.type": "#ApplicationService.ConsoleSetting",
                      "Name": "TRAP_FORWARDING_SETTING",
                      "DefaultValue": "AsIs",
                      "Value": "Normalized",
                      "DataType": "java.lang.String",
                      "GroupName": ""},
                 "MX7000_ONBOARDING_PREF":
                     {"@odata.type": "#ApplicationService.ConsoleSetting",
                      "Name": "MX7000_ONBOARDING_PREF",
                      "DefaultValue": "all",
                      "Value": "all",
                      "DataType": "java.lang.String",
                      "GroupName": ""},
                 "REPORTS_MAX_RESULTS_LIMIT":
                     {"@odata.type": "#ApplicationService.ConsoleSetting",
                      "Name": "REPORTS_MAX_RESULTS_LIMIT",
                      "DefaultValue": "0",
                      "Value": "123",
                      "DataType": "java.lang.Integer",
                      "GroupName": ""},
                 "EMAIL_SENDER":
                     {"@odata.type": "#ApplicationService.ConsoleSetting",
                      "Name": "EMAIL_SENDER",
                      "DefaultValue": "omcadmin@dell.com",
                      "Value": "admin@dell.com",
                      "DataType": "java.lang.String",
                      "GroupName": ""},
                 "DISCOVERY_APPROVAL_POLICY":
                     {"@odata.type": "#ApplicationService.ConsoleSetting",
                      "Name": "DISCOVERY_APPROVAL_POLICY",
                      "DefaultValue": "Automatic",
                      "Value": "Automatic",
                      "DataType": "java.lang.String",
                      "GroupName": ""},
                 "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION":
                     {"@odata.type": "#ApplicationService.ConsoleSetting",
                      "Name": "NODE_INITIATED_DISCOVERY_SET_TRAP_DESTINATION",
                      "DefaultValue": "false",
                      "Value": "true",
                      "DataType": "java.lang.Boolean",
                      "GroupName": ""},
                 "DEVICE_PREFERRED_NAME":
                     {"@odata.type": "#ApplicationService.ConsoleSetting",
                      "Name": "DEVICE_PREFERRED_NAME",
                      "DefaultValue": "HOST_NAME",
                      "Value": "PREFER_DNS,PREFER_IDRAC_HOSTNAME",
                      "DataType": "java.lang.String",
                      "GroupName": "DISCOVERY_SETTING"},
                 "INVALID_DEVICE_HOSTNAME":
                     {"@odata.type": "#ApplicationService.ConsoleSetting",
                      "Name": "INVALID_DEVICE_HOSTNAME",
                      "DefaultValue": "",
                      "Value": "localhost",
                      "DataType": "java.lang.String",
                      "GroupName": "DISCOVERY_SETTING"},
                 "COMMON_MAC_ADDRESSES":
                     {"@odata.type": "#ApplicationService.ConsoleSetting",
                      "Name": "COMMON_MAC_ADDRESSES",
                      "DefaultValue": "",
                      "Value": "::",
                      "DataType": "java.lang.String",
                      "GroupName": "DISCOVERY_SETTING"},
                 "MIN_PROTOCOL_VERSION": {
                     "@odata.type": "#ApplicationService.ConsoleSetting",
                     "Name": "MIN_PROTOCOL_VERSION",
                     "DefaultValue": "V2",
                     "Value": "V2",
                     "DataType": "java.lang.String",
                     "GroupName": "CIFS_PROTOCOL_SETTINGS"},
                 "CONSOLE_CONNECTION_SETTING": {
                     "@odata.type": "#ApplicationService.ConsoleSetting",
                     "Name": "CONSOLE_CONNECTION_SETTING",
                     "DefaultValue": "last_known",
                     "Value": "last_known",
                     "DataType": "java.lang.String",
                     "GroupName": "CONSOLE_CONNECTION_SETTING"},
                 "SHARE_TYPE": {
                     "@odata.type": "#ApplicationService.ConsoleSetting",
                     "Name": "SHARE_TYPE",
                     "DefaultValue": "CIFS",
                     "Value": "CIFS",
                     "DataType": "java.lang.String",
                     "GroupName": "BUILT_IN_APPLIANCE_SHARE_SETTINGS"}},
            "payload":
                {"ConsoleSetting":
                    [
                        {
                            "@odata.type": "#ApplicationService.ConsoleSetting",
                            "Name": "DATA_PURGE_INTERVAL",
                            "DefaultValue": "365",
                            "Value": "361",
                            "DataType": "java.lang.Integer",
                            "GroupName": ""
                        }]},
            "cifs_payload":
                {"ConsoleSetting": []},
            "module_args": {"metrics_collection_settings": 300},
            "json_data": {"value": [{"@odata.type": "#ApplicationService.ConsoleSetting",
                                     "Name": "DATA_PURGE_INTERVAL",
                                     "DefaultValue": "365",
                                     "Value": "361",
                                     "DataType": "java.lang.Integer",
                                     "GroupName": ""
                                     },
                                    {"@odata.type": "#ApplicationService.ConsoleSetting",
                                     "Name": "TRAP_FORWARDING_SETTING",
                                     "DefaultValue": "AsIs",
                                     "Value": "Normalized",
                                     "DataType": "java.lang.String",
                                     "GroupName": ""
                                     },
                                    {"@odata.type": "#ApplicationService.ConsoleSetting",
                                     "Name": "MX7000_ONBOARDING_PREF",
                                     "DefaultValue": "all",
                                     "Value": "all",
                                     "DataType": "java.lang.String",
                                     "GroupName": ""
                                     },
                                    {"@odata.type": "#ApplicationService.ConsoleSetting",
                                     "Name": "REPORTS_MAX_RESULTS_LIMIT",
                                     "DefaultValue": "0",
                                     "Value": "123",
                                     "DataType": "java.lang.Integer",
                                     "GroupName": ""
                                     },
                                    {"@odata.type": "#ApplicationService.ConsoleSetting",
                                     "Name": "EMAIL_SENDER",
                                     "DefaultValue": "omcadmin@dell.com",
                                     "Value": "admin@dell.com",
                                     "DataType": "java.lang.String",
                                     "GroupName": ""
                                     }, ]}, }])
    def test_module_success(self, mocker, params, ome_connection_mock_for_application_console_preferences,
                            ome_response_mock, ome_default_args):
        ome_response_mock.success = True
        ome_response_mock.status_code = 201
        # ome_response_mock.json_data = params["json_data"]
        ome_default_args.update(params['module_args'])
        mocker.patch(MODULE_PATH + 'job_details', return_value=params["job_details"])
        mocker.patch(MODULE_PATH + 'create_job', return_value=(None, None))
        mocker.patch(MODULE_PATH + 'fetch_cp_settings', return_value=params["cp_data"]["value"])
        mocker.patch(MODULE_PATH + 'create_payload', return_value=(params["payload"], params["payload_dict"]))
        mocker.patch(MODULE_PATH + 'create_cifs_payload', return_value=params["cifs_payload"])
        mocker.patch(MODULE_PATH + '_diff_payload', return_value=1)
        # mocker.patch(MODULE_PATH + 'update_payload', return_value=update_json_data)
        # mocker.patch(MODULE_PATH + '_diff_payload', return_value=1)
        result = self._run_module(ome_default_args)
        assert result["msg"] == SUCCESS_MSG

    @pytest.mark.parametrize("exc_type", [HTTPError, URLError])
    def test_cp_main_exception_case(self, mocker, exc_type, ome_connection_mock_for_application_console_preferences,
                                    ome_response_mock, ome_default_args):
        ome_default_args.update({"device_health": {"health_check_interval": 65,
                                                   "health_check_interval_unit": "Minutes"}})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + '_validate_params', side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + '_validate_params', side_effect=exc_type("exception message"))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + '_validate_params',
                         side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result
