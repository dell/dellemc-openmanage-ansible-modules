# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.3.0
# Copyright (C) 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
import os
import tempfile
from datetime import datetime, timedelta
from io import StringIO

import pytest
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import ome_alert_policies
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_alert_policies.'

SUCCESS_MSG = "Successfully {0}d the alert policy."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_MSG = "Changes found to be applied."
INVALID_TIME = "The specified {0} date or {0} time `{1}` to schedule the policy is not valid. Enter a valid date and time."
END_START_TIME = "The end time `{0}` to schedule the policy must be greater than the start time `{1}`."
CATEGORY_FETCH_FAILED = "Unable to retrieve the category details from OpenManage Enterprise."
INVALID_TARGETS = "Specify target devices to apply the alert policy."
INVALID_CATEGORY_MESSAGE = "Specify  categories or message to create the alert policy."
INVALID_SCHEDULE = "Specify a date and time to schedule the alert policy."
INVALID_ACTIONS = "Specify alert actions for the alert policy."
INVALID_SEVERITY = "Specify the severity to create the alert policy."
MULTIPLE_POLICIES = "Unable to update the alert policies because the number of alert policies entered are more than " \
                    "one. The update policy operation supports only one alert policy at a time."
DISABLED_ACTION = "Action {0} is disabled. Enable it before applying to the alert policy."
ACTION_INVALID_PARAM = "The Action {0} attribute contains invalid parameter name {1}. The valid values are {2}."
ACTION_INVALID_VALUE = "The Action {0} attribute contains invalid value for {1} for parameter name {2}. The valid " \
                       "values are {3}."
ACTION_DIS_EXIST = "Action {0} does not exist."
SUBCAT_IN_CATEGORY = "The subcategory {0} does not exist in the category {1}."
CATEGORY_IN_CATALOG = "The category {0} does not exist in the catalog {1}."
OME_DATA_MSG = "The {0} with the following {1} do not exist: {2}."
CATALOG_DIS_EXIST = "The catalog {0} does not exist."
CSV_PATH = "The message file {0} does not exist."
DEFAULT_POLICY_DELETE = "The following default policies cannot be deleted: {0}."
POLICY_ENABLE_MISSING = "Unable to {0} the alert policies {1} because the policy names are invalid. Enter the valid " \
                        "alert policy names and retry the operation."
NO_POLICY_EXIST = "The alert policy does not exist."
SEPARATOR = ", "


@pytest.fixture
def ome_connection_mock_for_alert_policies(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeAlertPolicies(FakeAnsibleModule):
    module = ome_alert_policies

    @pytest.mark.parametrize("params", [
        {"message": SUCCESS_MSG.format("enable"), "success": True,
         "json_data": {"value": [{'Name': "new alert policy", "Id": 12, "Enabled": False}]},
         "mparams": {"name": "new alert policy", "enable": True}},
        {"message": CHANGES_MSG, "success": True, "check_mode": True,
         "json_data": {"value": [{'Name': "new alert policy", "Id": 12, "Enabled": False}]},
         "mparams": {"name": "new alert policy", "enable": True}},
        {"message": MULTIPLE_POLICIES, "success": True,
         "json_data": {"value": [{'Name': "alert policy1", "Id": 12, "Enabled": True},
                                 {'Name': "alert policy2", "Id": 13, "Enabled": True}]},
         "mparams": {"name": ["alert policy1", "alert policy2"], "enable": False, "description": 'Update case failed'}},
        {"message": POLICY_ENABLE_MISSING.format("disable", "alert policy3"), "success": True,
         "json_data": {"value": [{'Name': "alert policy1", "Id": 12, "Enabled": True},
                                 {'Name': "alert policy2", "Id": 13, "Enabled": True}]},
         "mparams": {"name": ["alert policy3", "alert policy2"], "enable": False}},
        {"message": NO_CHANGES_MSG, "success": True, "check_mode": True,
         "json_data": {"value": [{'Name': "new alert policy", "Id": 12, "Enabled": False}]},
         "mparams": {"name": "new alert policy", "enable": False}},
        {"message": SUCCESS_MSG.format("delete"), "success": True,
         "json_data": {"report_list": [{'Name': "new alert policy", "Id": 12, "DefaultPolicy": False}],
                       "value": [{'Name': "new alert policy", "Id": 12, "DefaultPolicy": False}]},
         "mparams": {"name": "new alert policy", "state": "absent"}},
        {"message": CHANGES_MSG, "success": True, "check_mode": True,
         "json_data": {"report_list": [{'Name': "new alert policy", "Id": 12, "DefaultPolicy": False}],
                       "value": [{'Name': "new alert policy", "Id": 12, "DefaultPolicy": False}]},
         "mparams": {"name": "new alert policy", "state": "absent"}},
        {"message": DEFAULT_POLICY_DELETE.format("new alert policy"), "success": True,
         "json_data": {"report_list": [{'Name': "new alert policy", "Id": 12, "DefaultPolicy": False}],
                       "value": [{'Name': "new alert policy", "Id": 12, "DefaultPolicy": True}]},
         "mparams": {"name": "new alert policy", "state": "absent"}},
        {"message": NO_POLICY_EXIST, "success": True, "check_mode": True,
         "json_data": {"report_list": [{'Name': "new alert policy", "Id": 12, "DefaultPolicy": False}],
                       "value": [{'Name': "new alert policy 1", "Id": 12, "DefaultPolicy": False}]},
         "mparams": {"name": "new alert policy", "state": "absent"}},
        {"message": NO_POLICY_EXIST, "success": True,
         "json_data": {"report_list": [{'Name': "new alert policy", "Id": 12, "DefaultPolicy": False}],
                       "value": [{'Name': "new alert policy 1", "Id": 12, "DefaultPolicy": False}]},
         "mparams": {"name": "new alert policy", "state": "absent"}},
    ])
    def test_ome_alert_policies_enable_delete(self, params, ome_connection_mock_for_alert_policies,
                                              ome_response_mock, ome_default_args, module_mock, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['json_data']
        ome_connection_mock_for_alert_policies.get_all_items_with_pagination.return_value = params[
            'json_data']
        ome_default_args.update(params['mparams'])
        result = self._run_module(
            ome_default_args, check_mode=params.get('check_mode', False))
        assert result['msg'] == params['message']

    trap_ip1 = "traphost1:162"
    trap_ip2 = "traphost2:162"
    trap_ip3 = "traphost3:514"
    actions = [
        {
            "action_name": "Trap",
            "parameters": [
                {
                    "name": trap_ip2,
                    "value": "True"
                }
            ]
        },
        {
            "action_name": "Mobile",
            "parameters": []
        },
        {
            "action_name": "Email",
            "parameters": [
                {
                    "name": "to",
                    "value": "email2@address.x"
                },
                {
                    "name": "from",
                    "value": "emailr@address.y"
                },
                {
                    "name": "subject",
                    "value": "test subject"
                },
                {
                    "name": "message",
                    "value": "test message"
                }
            ]
        },
        {
            "action_name": "SMS",
            "parameters": [
                {
                    "name": "to",
                    "value": "1234567890"
                }
            ]
        }
    ]
    create_input = {
        "actions": actions,
        "date_and_time": {
            "date_from": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "date_to": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
            "days": [
                "sunday",
                "monday"
            ],
            "time_from": "11:00",
            "time_to": "12:00",
            "time_interval": True
        },
        "description": "Description of Alert Policy One",
        "device_group": [
            "AX",
            "Linux Servers"
        ],
        "enable": True,
        "message_ids": [
            "AMP400",
            "CTL201",
            "AMP401"
        ],
        "name": [
            "Alert Policy One"
        ],
        "severity": [
            "unknown"
        ],
        "state": "present"
    }
    get_alert_policy = [{
        "Id": 24792,
        "Name": "Alert Policy One",
                "Description": "CREATIOn of Alert Policy One",
                "Enabled": True,
                "DefaultPolicy": False,
                "Editable": True,
                "Visible": True,
                "PolicyData": {
                    "Catalogs": [],
                    "Severities": [
                        1
                    ],
                    "MessageIds": [
                        "'AMP401'",
                        "'AMP400'",
                        "'CTL201'"
                    ],
                    "Devices": [],
                    "DeviceTypes": [],
                    "Groups": [
                        1011,
                        1033
                    ],
                    "Schedule": {
                        "StartTime": "2023-10-09 00:00:00.000",
                        "EndTime": "2023-10-11 00:00:00.000",
                        "CronString": "* * * ? * mon,sun *",
                        "Interval": False
                    },
                    "Actions": [
                        {
                            "Id": 499,
                            "Name": "RemoteCommand",
                            "ParameterDetails": [
                                {
                                    "Id": 0,
                                    "Name": "remotecommandaction1",
                                    "Value": "test",
                                    "Type": "singleSelect",
                                    "TypeParams": [
                                        {
                                            "Name": "option",
                                            "Value": "test"
                                        }
                                    ]
                                }
                            ],
                            "TemplateId": 111
                        }
                    ],
                    "AllTargets": False,
                    "UndiscoveredTargets": []
                },
        "State": True,
        "Owner": 10078
    }]
    get_all_actions = {
        "Email": {
            "Disabled": False,
            "Id": 50,
            "Parameters": {
                "from": "admin@dell.com",
                "message": "Event occurred for Device Name",
                "subject": "Device Name: $name,  Device IP Address: $ip,  Severity: $severity",
                "to": ""
            },
            "Type": {
                "from": [],
                "message": [],
                "subject": [],
                "to": []
            }
        },
        "Ignore": {
            "Disabled": False,
            "Id": 100,
            "Parameters": {},
            "Type": {}
        },
        "Mobile": {
            "Disabled": False,
            "Id": 112,
            "Parameters": {},
            "Type": {}
        },
        "PowerControl": {
            "Disabled": False,
            "Id": 110,
            "Parameters": {
                "powercontrolaction": "poweroff"
            },
            "Type": {
                "powercontrolaction": [
                    "powercycle",
                    "poweroff",
                    "poweron",
                    "gracefulshutdown"
                ]
            }
        },
        "RemoteCommand": {
            "Disabled": False,
            "Id": 111,
            "Parameters": {
                "remotecommandaction": "test"
            },
            "Type": {
                "remotecommandaction": [
                    "test",
                    "cmd2 : XX.XX.XX.XX"
                ]
            }
        },
        "SMS": {
            "Disabled": False,
            "Id": 70,
            "Parameters": {
                "to": ""
            },
            "Type": {
                "to": []
            }
        },
        "Syslog": {
            "Disabled": False,
            "Id": 90,
            "Parameters": {
                trap_ip3: "true"
            },
            "Type": {
                trap_ip3: [
                    "true",
                    "false"
                ]
            }
        },
        "Trap": {
            "Disabled": False,
            "Id": 60,
            "Parameters": {
                trap_ip1: "true",
                trap_ip2: "true"
            },
            "Type": {
                trap_ip1: [
                    "true",
                    "false"
                ],
                trap_ip2: [
                    "true",
                    "false"
                ]
            }
        }
    }
    get_category_data_tree = {
        'Application': {
            'Audit': {
                4: {
                    'Devices': 90,
                    'Generic': 10,
                    'Power Configuration': 151,
                    'Users': 35
                }
            },
            'Configuration': {
                5: {
                    'Application': 85,
                    'Device Warranty': 116,
                    'Devices': 90,
                    'Discovery': 36,
                    'Generic': 10,
                    'Users': 35
                }
            },
            'Miscellaneous': {
                7: {
                    'Miscellaneous': 20
                }
            },
            'Storage': {
                2: {
                    'Devices': 90
                }
            },
            'System Health': {
                1: {
                    'Devices': 90,
                    'Health Status of Managed device': 7400,
                    'Job': 47,
                    'Metrics': 118,
                    'Power Configuration': 151
                }
            },
            'Updates': {
                3: {
                    'Application': 85,
                    'Firmware': 112
                }
            }
        },
        'Dell Storage': {
            'Storage': {
                2: {
                    'Other': 7700
                }
            },
            'System Health': {
                1: {
                    'Other': 7700,
                    'Storage': 18
                }
            }
        },
        'Storage': {'Audit': {
            4: {
                'Interface': 101
            }
        }},
        'iDRAC': {
            'Audit': {
                4: {
                    'Interface': 101
                }
            }
        },
    }

    @pytest.mark.parametrize("params", [
        {"message": SUCCESS_MSG.format("create"), "success": True,
         "mparams": create_input,
            "get_alert_policies": [],
            "validate_ome_data": (["AMP400", "AMP401", "CTL201"],),
            "get_severity_payload": {"Severities": ["unknown"]},
            "get_all_actions": get_all_actions,
            "json_data": {"value": [{'Name': "new alert policy 1", "Id": 12, "DefaultPolicy": False}]}},
        {"message": CHANGES_MSG, "success": True,
         "check_mode": True,
         "mparams": create_input,
         "get_alert_policies": [],
         "validate_ome_data": (["AMP400", "AMP401", "CTL201"],),
         "get_severity_payload": {"Severities": ["unknown"]},
         "get_all_actions": get_all_actions,
         "json_data": {"value": [{'Name': "new alert policy 1", "Id": 12, "DefaultPolicy": False}]}},
        {"message": SUCCESS_MSG.format("update"), "success": True,
         "mparams": create_input,
            "get_alert_policies": get_alert_policy,
            "validate_ome_data": (["AMP400", "AMP401", "CTL201"],),
            "get_category_data_tree": get_category_data_tree,
            "get_all_actions": get_all_actions,
            "json_data": {
            "value": [
                {

                    "Id": 1,
                    "Name": "Unknown",
                    "Description": "Unknown"
                },
                {
                    "Id": 2,
                    "Name": "Info",
                    "Description": "Info"
                },
                {
                    "Id": 4,
                    "Name": "Normal",
                    "Description": "Normal"
                },
                {
                    "Id": 8,
                    "Name": "Warning",
                    "Description": "Warning"
                },
                {
                    "Id": 16,
                    "Name": "Critical",
                    "Description": "Critical"
                }
            ]
        }},
        {"message": SUCCESS_MSG.format("update"), "success": True,
         "mparams": {
             "actions": [
                 {
                     "action_name": "Ignore",
                     "parameters": []
                 }
             ],
             "description": "Description of Alert Policy One",
             "specific_undiscovered_devices": [
                 "host1",
                 "192.1.2.3-192.1.2.10"
             ],
             "enable": True,
             "category": [
                 {
                     "catalog_category": [
                         {
                             "category_name": "Audit",
                             "sub_category_names": [
                                 "Users",
                                 "Generic"
                             ]
                         }
                     ],
                     "catalog_name": "Application"
                 },
                 {
                     "catalog_category": [
                         {
                             "category_name": "Storage",
                             "sub_category_names": [
                                 "Other"
                             ]
                         }
                     ],
                     "catalog_name": "Dell Storage"
                 },
                 {"catalog_name": "Storage"},
                 {
                     "catalog_category": [
                         {
                             "category_name": "Audit",
                             "sub_category_names": []
                         }
                     ],
                     "catalog_name": "iDRAC"
                 }
             ],
             "name": [
                 "Alert Policy One"
             ],
             "new_name": "Alert Policy Renamed",
             "severity": [
                 "unknown"
             ],
             "state": "present"
        },
            "get_alert_policies": get_alert_policy,
            "validate_ome_data": (["AMP400", "AMP401", "CTL201"],),
            "get_category_data_tree": get_category_data_tree,
            "get_all_actions": get_all_actions,
            "json_data": {"value": []}
        },
        {"message": OME_DATA_MSG.format("groups", "Name", "Linux Servers"), "success": True,
         "mparams": {
             "device_group": [
                 "AX",
                 "Linux Servers"
             ],
             "state": "present",
             "name": "Test alert policy"
        },
            "get_alert_policies": get_alert_policy,
            "json_data": {
             "@odata.count": 102,
             "@odata.nextLink": "/AlertPolicies",
             "value": [{"Name": "AX", "Id": 121},
                       {"Name": "Group2", "Id": 122}]}
        },
        {"message": OME_DATA_MSG.format("groups", "Name", "Linux Servers"), "success": True,
         "mparams": {
             "device_group": [
                 "AX",
                 "Linux Servers"
             ],
             "state": "present",
             "name": "Test alert policy",
             "description": "Coverage for filter block in validate_ome_data"
        },
            "get_alert_policies": [{
                "Id": 1234,
                "Name": "Alert Policy Two",
                "Description": "Alert Policy Two described",
                "Enabled": True,
                "DefaultPolicy": False,
                "Editable": True,
                "Visible": True,
                "PolicyData": {
                    "Catalogs": [],
                    "Severities": [
                        16
                    ],
                    "MessageIds": [
                        "'AMP403'",
                        "'AMP400'",
                        "'BIOS108'"
                    ],
                    "Devices": [],
                    "DeviceTypes": [],
                    "Groups": [
                        111,
                        133
                    ],
                    "Schedule": {
                        "StartTime": "2023-11-09 00:00:00.000",
                        "EndTime": "2023-11-11 00:00:00.000",
                        "CronString": "* * * ? * mon,sun *",
                        "Interval": False
                    },
                    "Actions": [
                        {
                            "Id": 499,
                            "Name": "RemoteCommand",
                            "ParameterDetails": [
                                {
                                    "Id": 0,
                                    "Name": "remotecommandaction1",
                                    "Value": "test",
                                    "Type": "singleSelect",
                                    "TypeParams": [
                                        {
                                            "Name": "option",
                                            "Value": "test"
                                        }
                                    ]
                                }
                            ],
                            "TemplateId": 111
                        }
                    ],
                    "AllTargets": False,
                    "UndiscoveredTargets": []
                },
                "State": True,
                "Owner": 10078
            }],
            "json_data": {
             "@odata.count": 300,
             "value": [{"Name": "AX", "Id": 121},
                       {"Name": "Group2", "Id": 122}]}
        },
        {"message": INVALID_CATEGORY_MESSAGE, "success": True,
         "mparams": {
             "device_service_tag": [
                 "ABC1234",
                 "SVCTAG1"
             ],
             "state": "present",
             "name": "Test alert policy",
             "description": "Coverage for filter block in validate_ome_data"
         },
         "get_alert_policies": [],
         "json_data": {
             "@odata.count": 300,
             "value": [{"DeviceServiceTag": "ABC1234", "Id": 121, "Type": 1000},
                       {"DeviceServiceTag": "SVCTAG1", "Id": 122, "Type": 1000}]}
         },
        {"message": INVALID_CATEGORY_MESSAGE, "success": True,
         "mparams": {
             "all_devices": True,
             "state": "present",
             "name": "Test alert policy",
             "description": "all devices coverage"
         },
         "get_alert_policies": [],
         "json_data": {
             "@odata.count": 300,
             "value": [{"DeviceServiceTag": "ABC1234", "Id": 121, "Type": 1000},
                       {"DeviceServiceTag": "SVCTAG1", "Id": 122, "Type": 1000}]}
         },
        {"message": INVALID_CATEGORY_MESSAGE, "success": True,
         "mparams": {
             "any_undiscovered_devices": True,
             "state": "present",
             "name": "Test alert policy",
             "description": "all devices coverage"
         },
         "get_alert_policies": [],
         "json_data": {
             "@odata.count": 300,
             "value": [{"DeviceServiceTag": "ABC1234", "Id": 121, "Type": 1000},
                       {"DeviceServiceTag": "SVCTAG1", "Id": 122, "Type": 1000}]}
         },
        {"message": INVALID_CATEGORY_MESSAGE, "success": True,
         "mparams": {
             "specific_undiscovered_devices": [
                 "192.1.2.3-192.1.2.10",
                 "hostforpolicy.domain.com"
             ],
             "state": "present",
             "name": "Test alert policy",
             "description": "all devices coverage"
         },
         "get_alert_policies": [],
         "json_data": {
             "@odata.count": 300,
             "value": [{"DeviceServiceTag": "ABC1234", "Id": 121, "Type": 1000},
                       {"DeviceServiceTag": "SVCTAG1", "Id": 122, "Type": 1000}]}
         },
        {"message": INVALID_SCHEDULE, "success": True,
         "mparams": {
             "all_devices": True,
             "message_file": "{0}/{1}".format(tempfile.gettempdir(), "myfile.csv"),
             "state": "present",
             "name": "Test alert policy",
             "description": "all devices coverage"
         },
         "get_alert_policies": [],
         "create_temp_file": "MessageIds\nMSGID1",
         "json_data": {
             "@odata.count": 300,
             "value": [{"MessageId": "MSGID1", "Id": 121, "Type": 1000},
                       {"MessageId": "MSGID2", "Id": 122, "Type": 1000}]}
         },
        {"message": INVALID_SCHEDULE, "success": True,
         "mparams": {
             "all_devices": True,
             "category": [
                 {
                     "catalog_category": [
                         {
                             "category_name": "Audit",
                             "sub_category_names": [
                                 "Users",
                                 "Generic"
                             ]
                         }
                     ],
                     "catalog_name": "Application"
                 },
                 {
                     "catalog_category": [
                         {
                             "category_name": "Storage",
                             "sub_category_names": [
                                 "Other"
                             ]
                         }
                     ],
                     "catalog_name": "Dell Storage"
                 }
             ],
             "state": "present",
             "name": "Test alert policy",
             "description": "get_category_data_tree coverage"
         },
         "get_alert_policies": [],
         "get_target_payload": {"Groups": [123, 124]},
         "json_data": {
             "value": [
                 {
                     "Name": "Application",
                     "IsBuiltIn": True,
                     "CategoriesDetails": [
                         {
                             "Id": 4,
                             "Name": "Audit",
                             "CatalogName": "Application",
                             "SubCategoryDetails": [
                                 {
                                     "Id": 90,
                                     "Name": "Devices",
                                     "Description": "Devices description"
                                 },
                                 {
                                     "Id": 10,
                                     "Name": "Generic",
                                     "Description": "Generic description"
                                 },
                                 {
                                     "Id": 151,
                                     "Name": "Power Configuration",
                                     "Description": "Power Configuration description"
                                 },
                                 {
                                     "Id": 35,
                                     "Name": "Users",
                                     "Description": "Users description"
                                 }
                             ]
                         },
                         {
                             "Id": 7,
                             "Name": "Miscellaneous",
                             "CatalogName": "Application",
                             "SubCategoryDetails": [
                                 {
                                     "Id": 20,
                                     "Name": "Miscellaneous",
                                     "Description": "Miscellaneous description"
                                 }
                             ]
                         },
                         {
                             "Id": 2,
                             "Name": "Storage",
                             "CatalogName": "Application",
                             "SubCategoryDetails": [
                                 {
                                     "Id": 90,
                                     "Name": "Devices",
                                     "Description": "Devices description"
                                 }
                             ]
                         },
                         {
                             "Id": 1,
                             "Name": "System Health",
                             "CatalogName": "Application",
                             "SubCategoryDetails": [
                                 {
                                     "Id": 90,
                                     "Name": "Devices",
                                     "Description": "Devices description"
                                 },
                                 {
                                     "Id": 7400,
                                     "Name": "Health Status of Managed device",
                                     "Description": "Health Status of Managed device description"
                                 },
                                 {
                                     "Id": 47,
                                     "Name": "Job",
                                     "Description": "Job description"
                                 },
                                 {
                                     "Id": 118,
                                     "Name": "Metrics",
                                     "Description": "Metrics description"
                                 },
                                 {
                                     "Id": 151,
                                     "Name": "Power Configuration",
                                     "Description": "Power Configuration description"
                                 }
                             ]
                         },
                         {
                             "Id": 3,
                             "Name": "Updates",
                             "CatalogName": "Application",
                             "SubCategoryDetails": [
                                 {
                                     "Id": 85,
                                     "Name": "Application",
                                     "Description": "Application description"
                                 },
                                 {
                                     "Id": 112,
                                     "Name": "Firmware",
                                     "Description": "Firmware description"
                                 }
                             ]
                         }
                     ]
                 },
                 {
                     "Name": "Dell Storage",
                     "IsBuiltIn": True,
                     "CategoriesDetails": [
                         {
                             "Id": 2,
                             "Name": "Storage",
                             "CatalogName": "Dell Storage",
                             "SubCategoryDetails": [
                                 {
                                     "Id": 7700,
                                     "Name": "Other",
                                     "Description": "Other description"
                                 }
                             ]
                         },
                         {
                             "Id": 1,
                             "Name": "System Health",
                             "CatalogName": "Dell Storage",
                             "SubCategoryDetails": [
                                 {
                                     "Id": 7700,
                                     "Name": "Other",
                                     "Description": "Other description"
                                 },
                                 {
                                     "Id": 18,
                                     "Name": "Storage",
                                     "Description": "Storage description"
                                 }
                             ]
                         }
                     ]
                 }
             ]
         }
         },
        {"message": INVALID_SEVERITY, "success": True,
         "mparams": {
             "actions": actions,
             "all_devices": True,
             "message_ids": ["MSG01", "MSG02"],
             "state": "present",
             "name": "Test alert policy",
             "description": "get_all_actions coverage"
         },
         "get_alert_policies": [],
         "get_target_payload": {"Groups": [123, 124]},
         "get_category_or_message": {"MessageIds": ["MSG01", "MSG02"]},
         "get_schedule_payload": {"StartTime": "", "EndTime": ""},
         "get_severity_payload": {},
         "json_data": {
             "value": [
                 {
                     "Name": "Email",
                     "Description": "Email",
                     "Disabled": False,
                     "ParameterDetails": [
                         {
                             "Id": 1,
                             "Name": "subject",
                             "Value": "Device Name: $name,  Device IP Address: $ip,  Severity: $severity",
                             "Type": "string",
                             "TemplateParameterTypeDetails": [
                                 {
                                     "Name": "maxLength",
                                     "Value": "255"
                                 }
                             ]
                         },
                         {
                             "Id": 2,
                             "Name": "to",
                             "Value": "",
                             "Type": "string",
                             "TemplateParameterTypeDetails": [
                                 {
                                     "Name": "maxLength",
                                     "Value": "255"
                                 }
                             ]
                         },
                         {
                             "Id": 3,
                             "Name": "from",
                             "Value": "admin@dell.com",
                             "Type": "string",
                             "TemplateParameterTypeDetails": [
                                 {
                                     "Name": "maxLength",
                                     "Value": "255"
                                 }
                             ]
                         },
                         {
                             "Id": 4,
                             "Name": "message",
                             "Value": "Event occurred for Device Name",
                             "Type": "string",
                             "TemplateParameterTypeDetails": [
                                 {
                                     "Name": "maxLength",
                                     "Value": "255"
                                 }
                             ]
                         }
                     ]
                 },
                 {
                     "@odata.type": "#AlertService.AlertActionTemplate",
                     "@odata.id": "/api/AlertService/AlertActionTemplates(60)",
                     "Id": 60,
                     "Name": "Trap",
                     "Description": "Trap",
                     "Disabled": False,
                     "ParameterDetails": [
                         {
                             "Id": 1,
                             "Name": trap_ip1,
                             "Value": "true",
                             "Type": "boolean",
                             "TemplateParameterTypeDetails": []
                         },
                         {
                             "Id": 2,
                             "Name": trap_ip2,
                             "Value": "true",
                             "Type": "boolean",
                             "TemplateParameterTypeDetails": []
                         }
                     ]
                 },
                 {
                     "@odata.type": "#AlertService.AlertActionTemplate",
                     "@odata.id": "/api/AlertService/AlertActionTemplates(90)",
                     "Id": 90,
                     "Name": "Syslog",
                     "Description": "Syslog",
                     "Disabled": False,
                     "ParameterDetails": [
                         {
                             "Id": 1,
                             "Name": trap_ip3,
                             "Value": "true",
                             "Type": "boolean",
                             "TemplateParameterTypeDetails": []
                         }
                     ]
                 },
                 {
                     "@odata.type": "#AlertService.AlertActionTemplate",
                     "@odata.id": "/api/AlertService/AlertActionTemplates(100)",
                     "Id": 100,
                     "Name": "Ignore",
                     "Description": "Ignore",
                     "Disabled": False,
                     "ParameterDetails": []
                 },
                 {
                     "@odata.type": "#AlertService.AlertActionTemplate",
                     "@odata.id": "/api/AlertService/AlertActionTemplates(70)",
                     "Id": 70,
                     "Name": "SMS",
                     "Description": "SMS",
                     "Disabled": False,
                     "ParameterDetails": [
                         {
                             "Id": 1,
                             "Name": "to",
                             "Value": "",
                             "Type": "string",
                             "TemplateParameterTypeDetails": [
                                 {
                                     "Name": "maxLength",
                                     "Value": "255"
                                 }
                             ]
                         }
                     ]
                 },
                 {
                     "@odata.type": "#AlertService.AlertActionTemplate",
                     "@odata.id": "/api/AlertService/AlertActionTemplates(110)",
                     "Id": 110,
                     "Name": "PowerControl",
                     "Description": "Power Control Action Template",
                     "Disabled": False,
                     "ParameterDetails": [
                         {
                             "Id": 1,
                             "Name": "powercontrolaction",
                             "Value": "poweroff",
                             "Type": "singleSelect",
                             "TemplateParameterTypeDetails": [
                                 {
                                     "Name": "option",
                                     "Value": "powercycle"
                                 },
                                 {
                                     "Name": "option",
                                     "Value": "poweroff"
                                 },
                                 {
                                     "Name": "option",
                                     "Value": "poweron"
                                 },
                                 {
                                     "Name": "option",
                                     "Value": "gracefulshutdown"
                                 }
                             ]
                         }
                     ]
                 },
                 {
                     "@odata.type": "#AlertService.AlertActionTemplate",
                     "@odata.id": "/api/AlertService/AlertActionTemplates(111)",
                     "Id": 111,
                     "Name": "RemoteCommand",
                     "Description": "RemoteCommand",
                     "Disabled": False,
                     "ParameterDetails": [
                         {
                             "Id": 1,
                             "Name": "remotecommandaction",
                             "Value": "test",
                             "Type": "singleSelect",
                             "TemplateParameterTypeDetails": [
                                 {
                                     "Name": "option",
                                     "Value": "test"
                                 }
                             ]
                         }
                     ]
                 },
                 {
                     "@odata.type": "#AlertService.AlertActionTemplate",
                     "@odata.id": "/api/AlertService/AlertActionTemplates(112)",
                     "Id": 112,
                     "Name": "Mobile",
                     "Description": "Mobile",
                     "Disabled": False,
                     "ParameterDetails": []
                 }
             ]
         }
         },
        {"message": DISABLED_ACTION.format("SMS"), "success": True,
         "mparams": {
             "actions": [{
                 "action_name": "SMS",
                 "parameters": [
                    {
                        "name": "to",
                        "value": "1234567890"
                    }
                 ]
             }],
             "all_devices": True,
             "message_ids": ["MSG01", "MSG02"],
             "state": "present",
             "name": "Test alert policy",
             "description": "get_all_actions coverage"
        },
            "get_alert_policies": [],
            "get_target_payload": {"Groups": [123, 124]},
            "get_category_or_message": {"MessageIds": ["MSG01", "MSG02"]},
            "get_schedule_payload": {"StartTime": "", "EndTime": ""},
            "get_severity_payload": {},
            "json_data": {
             "value": [
                 {
                     "Id": 70,
                     "Name": "SMS",
                     "Description": "SMS",
                     "Disabled": True,
                     "ParameterDetails": [
                         {
                             "Id": 1,
                             "Name": "to",
                             "Value": "",
                             "Type": "string",
                             "TemplateParameterTypeDetails": [
                                 {
                                     "Name": "maxLength",
                                     "Value": "255"
                                 }
                             ]
                         }
                     ]
                 },
                 {
                     "Id": 112,
                     "Name": "Mobile",
                     "Description": "Mobile",
                     "Disabled": False,
                     "ParameterDetails": []
                 }
             ]
        }
        },
        {"message": ACTION_INVALID_PARAM.format("Trap", "traphost2:162", "traphost1:162"), "success": True,
         "mparams": {
             "actions": [{
                 "action_name": "Trap",
                 "parameters": [
                    {
                        "name": trap_ip2,
                        "value": "True"
                    }
                 ]
             }],
             "all_devices": True,
             "message_ids": ["MSG01", "MSG02"],
             "state": "present",
             "name": "Test alert policy",
             "description": "get_all_actions coverage"
        },
            "get_alert_policies": [],
            "get_target_payload": {"Groups": [123, 124]},
            "get_category_or_message": {"MessageIds": ["MSG01", "MSG02"]},
            "get_schedule_payload": {"StartTime": "", "EndTime": ""},
            "get_severity_payload": {},
            "json_data": {
             "value": [
                 {
                     "Id": 100,
                     "Name": "SMS",
                     "Description": "Ignore",
                     "Disabled": False,
                     "ParameterDetails": []
                 },
                 {
                     "Id": 60,
                     "Name": "Trap",
                     "Description": "Trap",
                     "Disabled": False,
                     "ParameterDetails": [
                         {
                             "Id": 1,
                             "Name": trap_ip1,
                             "Value": "true",
                             "Type": "boolean",
                             "TemplateParameterTypeDetails": []
                         }
                     ]
                 }
             ]
        }
        },
        {"message": ACTION_INVALID_VALUE.format("Trap", "Truthy", "traphost1:162", "true, false"), "success": True,
         "mparams": {
             "actions": [{
                 "action_name": "Trap",
                 "parameters": [
                    {
                        "name": trap_ip1,
                        "value": "Truthy"
                    }
                 ]
             }],
             "all_devices": True,
             "message_ids": ["AMP01", "CTL201"],
             "state": "present",
             "name": "Test alert policy",
             "description": "actions invalid coverage"
        },
            "get_alert_policies": [],
            "get_target_payload": {"Devices": [123, 124]},
            "get_category_or_message": {"MessageIds": ["AMP01", "CTL201"]},
            "get_schedule_payload": {"StartTime": "2023-11-01 11:00:00.000", "EndTime": "2023-12-01 12:00:00.000"},
            "get_severity_payload": {},
            "json_data": {
             "value": [
                 {
                     "Id": 60,
                     "Name": "Trap",
                     "Description": "Trap",
                     "Disabled": False,
                     "ParameterDetails": [
                         {
                             "Id": 1,
                             "Name": trap_ip1,
                             "Value": "true",
                             "Type": "boolean",
                             "TemplateParameterTypeDetails": []
                         }
                     ]
                 }]
        }
        },
        {"message": ACTION_DIS_EXIST.format("SNMPTrap"), "success": True,
         "mparams": {
             "actions": [{
                 "action_name": "SNMPTrap",
                 "parameters": [
                    {
                        "name": trap_ip1,
                        "value": "true"
                    }
                 ]
             }],
             "all_devices": True,
             "message_ids": ["BIOS101", "RND123"],
             "state": "present",
             "name": "Test alert policy",
             "description": "No existing action coverage"
        },
            "get_alert_policies": [],
            "get_target_payload": {"Groups": [123, 124]},
            "get_category_or_message": {"MessageIds": ["MSG23", "MSG46"]},
            "get_schedule_payload": {"StartTime": "2023-11-01 11:00:00.000", "EndTime": "2023-12-01 12:00:00.000"},
            "get_severity_payload": {},
            "json_data": {
             "value": [
                 {
                     "Id": 60,
                     "Name": "Trap",
                     "Description": "Trap",
                     "Disabled": False,
                     "ParameterDetails": [
                         {
                             "Id": 1,
                             "Name": trap_ip1,
                             "Value": "true",
                             "Type": "boolean",
                             "TemplateParameterTypeDetails": []
                         }
                     ]
                 }]
        }
        },
        {"message": INVALID_TIME.format("from", "2023-20-01 11:00:00.000"), "success": True,
         "mparams": {
             "date_and_time": {
                 "date_from": "2023-20-01",
                 "date_to": "2023-10-02",
                 "days": [
                     "sunday",
                     "monday"
                 ],
                 "time_from": "11:00",
                 "time_to": "12:00",
                 "time_interval": True
             },
             "all_devices": True,
             "message_ids": ["MSG01", "MSG02"],
             "state": "present",
             "name": "Test alert policy",
             "description": "get_schedule coverage"
        },
            "get_alert_policies": [],
            "get_target_payload": {"Groups": [123, 124]},
            "get_category_or_message": {"MessageIds": ["MSG01", "MSG02"]},
            "json_data": {
             "value": []
        }
        },
        {"message": INVALID_TIME.format("from", "2023-10-01 31:00:00.000"), "success": True,
         "mparams": {
             "date_and_time": {
                 "date_from": "2023-10-01",
                 "date_to": "2023-10-02",
                 "days": [
                     "sunday",
                     "monday"
                 ],
                 "time_from": "31:00",
                 "time_to": "12:00",
                 "time_interval": True
             },
             "all_devices": True,
             "message_ids": ["MSG01", "MSG02"],
             "state": "present",
             "name": "Test alert policy",
             "description": "get_schedule coverage"
        },
            "get_alert_policies": [],
            "get_target_payload": {"Groups": [123, 124]},
            "get_category_or_message": {"MessageIds": ["MSG01", "MSG02"]},
            "json_data": {
             "value": []
        }
        },
        {"message": END_START_TIME.format("2023-10-01 12:00:00", "2023-10-02 11:00:00"), "success": True,
         "mparams": {
             "date_and_time": {
                 "date_from": "2023-10-02",
                 "date_to": "2023-10-01",
                 "days": [
                     "sunday",
                     "monday"
                 ],
                 "time_from": "11:00",
                 "time_to": "12:00",
                 "time_interval": True
             },
             "all_devices": True,
             "message_ids": ["MSG01", "MSG02"],
             "state": "present",
             "name": "Test alert policy",
             "description": "get_schedule coverage"
        },
            "get_alert_policies": [],
            "get_target_payload": {"Groups": [123, 124]},
            "get_category_or_message": {"MessageIds": ["MSG01", "MSG02"]},
            "json_data": {
             "value": []
        }
        },
        {"message": INVALID_TIME.format("to", "2023-10-32 32:00:00.000"), "success": True,
         "mparams": {
             "date_and_time": {
                 "date_from": "2023-10-01",
                 "date_to": "2023-10-32",
                 "days": [
                     "sunday",
                     "monday"
                 ],
                 "time_from": "11:00",
                 "time_to": "32:00",
                 "time_interval": True
             },
             "all_devices": True,
             "message_ids": ["MSG01", "MSG02"],
             "state": "present",
             "name": "Test alert policy",
             "description": "get_schedule coverage"
        },
            "get_alert_policies": [],
            "get_target_payload": {"Groups": [123, 124]},
            "get_category_or_message": {"MessageIds": ["MSG01", "MSG02"]},
            "json_data": {
             "value": []
        }
        },
        {"message": INVALID_TARGETS, "success": True,
         "mparams": {
             "all_devices": True,
             "message_ids": ["MSG01", "MSG02"],
             "state": "present",
             "name": "Test alert policy",
             "description": "INVALID_TARGETS coverage"
         },
            "get_alert_policies": [],
            "get_target_payload": {},
            "json_data": {
             "value": []
         }
         },
        {"message": INVALID_ACTIONS, "success": True,
         "mparams": {
             "all_devices": True,
             "message_ids": ["MSG01", "MSG02"],
             "state": "present",
             "name": "Test alert policy",
             "description": "get_schedule coverage",
             "date_and_time": {
                 "date_from": "2023-10-01",
                 "days": [
                     "sunday",
                     "monday"
                 ],
                 "time_from": "11:00",
                 "time_to": "12:00",
                 "time_interval": True
             },
         },
            "get_alert_policies": [],
            "get_target_payload": {"Groups": [123, 124]},
            "get_category_or_message": {"MessageIds": ["MSG01", "MSG02"]},
            "get_actions_payload": {},
            "json_data": {
             "value": []
         }
         },
        {"message": CATEGORY_FETCH_FAILED, "success": True,
         "mparams": {
             "all_devices": True,
             "category": [
                 {
                     "catalog_category": [
                         {
                             "category_name": "Audit",
                             "sub_category_names": [
                                 "Users",
                                 "Generic"
                             ]
                         }
                     ],
                     "catalog_name": "Application"
                 }
             ],
             "state": "present",
             "name": "Test alert policy",
             "description": "get_schedule coverage"
         },
            "get_alert_policies": [],
            "get_target_payload": {"Groups": [123, 124]},
            "get_category_data_tree": {},
            "json_data": {
             "value": []
         }
         },
        {"message": SUBCAT_IN_CATEGORY.format("General", "Audit"), "success": True,
         "mparams": {
             "all_devices": True,
             "category": [
                 {
                     "catalog_category": [
                         {
                             "category_name": "Audit",
                             "sub_category_names": [
                                 "General",
                                 "Generic"
                             ]
                         }
                     ],
                     "catalog_name": "Application"
                 }
             ],
             "state": "present",
             "name": "Test alert policy",
             "description": "get_schedule coverage"
        },
            "get_alert_policies": [],
            "get_target_payload": {"Groups": [123, 124]},
            "get_category_data_tree": get_category_data_tree,
            "json_data": {
             "value": []
        }
        },
        {"message": CATEGORY_IN_CATALOG.format("Audi", "Application"), "success": True,
         "mparams": {
             "all_devices": True,
             "category": [
                 {
                     "catalog_category": [
                         {
                             "category_name": "Audi",
                             "sub_category_names": [
                                 "General",
                                 "Generic"
                             ]
                         }
                     ],
                     "catalog_name": "Application"
                 }
             ],
             "state": "present",
             "name": "Test alert policy",
             "description": "get_schedule coverage"
        },
            "get_alert_policies": [],
            "get_target_payload": {"Groups": [123, 124]},
            "get_category_data_tree": get_category_data_tree,
            "json_data": {
             "value": []
        }
        },
        {"message": CATALOG_DIS_EXIST.format("Alpha"), "success": True,
         "mparams": {
             "all_devices": True,
             "category": [
                 {
                     "catalog_name": "Alpha"
                 }
             ],
             "state": "present",
             "name": "Test alert policy",
             "description": "get_schedule coverage"
        },
            "get_alert_policies": [],
            "get_target_payload": {"Groups": [123, 124]},
            "get_category_data_tree": get_category_data_tree,
            "json_data": {
             "value": []
        }
        }
    ])
    def test_ome_alert_policies_state_present(self, params, ome_connection_mock_for_alert_policies,
                                              ome_response_mock, ome_default_args, module_mock, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['json_data']
        ome_connection_mock_for_alert_policies.get_all_items_with_pagination.return_value = params[
            'json_data']
        ome_default_args.update(params['mparams'])
        mocks = ["get_alert_policies", "validate_ome_data", "get_target_payload",
                 "get_all_actions", "get_severity_payload", "get_category_data_tree",
                 "get_schedule_payload", "get_category_or_message"]
        for m in mocks:
            if m in params:
                mocker.patch(MODULE_PATH + m, return_value=params.get(m, {}))
        if "create_temp_file" in params:
            with open(f"{params['mparams'].get('message_file')}", 'w', encoding='utf-8') as fp:
                fp.write(params["create_temp_file"])
        result = self._run_module(
            ome_default_args, check_mode=params.get('check_mode', False))
        if "create_temp_file" in params:
            fpath = f"{params['mparams'].get('message_file')}"
            if os.path.exists(fpath):
                os.remove(fpath)
        assert result['msg'] == params['message']

    @pytest.mark.parametrize("exc_type",
                             [SSLValidationError, ConnectionError, TypeError, ValueError, OSError, HTTPError, URLError])
    def test_ome_alert_policies_category_info_main_exception_failure_case(self, exc_type, mocker, ome_default_args,
                                                                          ome_connection_mock_for_alert_policies,
                                                                          ome_response_mock):
        json_str = to_text(json.dumps({"data": "out"}))
        ome_default_args.update({"name": "new alert policy", "enable": True})
        if exc_type == HTTPError:
            mocker.patch(MODULE_PATH + 'get_alert_policies', side_effect=exc_type(
                'https://testhost.com', 401, 'http error message', {
                    "accept-type": "application/json"},
                StringIO(json_str)))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
        elif exc_type == URLError:
            mocker.patch(MODULE_PATH + 'get_alert_policies',
                         side_effect=exc_type("exception message"))
            result = self._run_module(ome_default_args)
            assert result['unreachable'] is True
        else:
            mocker.patch(MODULE_PATH + 'get_alert_policies',
                         side_effect=exc_type("exception message"))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
