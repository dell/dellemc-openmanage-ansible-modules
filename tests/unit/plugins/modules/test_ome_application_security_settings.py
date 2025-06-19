# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.2.0
# Copyright (C) 2021-2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
from io import StringIO

import pytest
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import ome_application_security_settings
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_application_security_settings.'

SEC_JOB_TRIGGERED = "Successfully triggered the job to apply security settings."
SEC_JOB_COMPLETE = "Successfully applied the security settings."
FIPS_TOGGLED = "Successfully {0} the FIPS mode."
FIPS_CONN_RESET = "The network connection may have changed. Verify the connection and try again."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The value for the 'job_wait_timeout' parameter cannot be negative or zero."


@pytest.fixture
def ome_connection_mock_for_security_settings(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeSecuritySettings(FakeAnsibleModule):
    module = ome_application_security_settings

    @pytest.mark.parametrize("params", [
        {"module_args": {
            "job_wait": False, "job_wait_timeout": 120,
            "login_lockout_policy": {
                "by_ip_address": False, "by_user_name": False, "lockout_fail_count": 5,
                "lockout_fail_window": 30, "lockout_penalty_time": 900},
            "restrict_allowed_ip_range": {
                "enable_ip_range": False, "ip_range": None},
        },
            "json_data": {
                "JobId": 1234,
                "SystemConfiguration": {
                    "Comments": ["Export type is Normal,JSON"],
                    "Model": "", "ServiceTag": "",
                    "Components": [
                        {
                            "FQDD": "MM.Embedded.1",
                            "Attributes": [
                                {
                                    "Name": "LoginSecurity.1#Id",
                                    "Value": "10"
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutFailCount",
                                    "Value": 3
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutFailCountTime",
                                    "Value": 32
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutPenaltyTime",
                                    "Value": 850
                                },
                                {
                                    "Name": "LoginSecurity.1#IPRangeAddr",
                                    "Value": None
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutByUsernameEnable",
                                    "Value": True
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutByIPEnable",
                                    "Value": True
                                },
                                {
                                    "Name": "LoginSecurity.1#IPRangeEnable",
                                    "Value": False
                                }
                            ]
                        }
                    ]
                }
        }, "msg": SEC_JOB_TRIGGERED},
        {"module_args": {
            "job_wait": False, "job_wait_timeout": 120,
            "login_lockout_policy": {
                "by_ip_address": False, "by_user_name": False, "lockout_fail_count": 5,
                "lockout_fail_window": 30, "lockout_penalty_time": 900},
            "restrict_allowed_ip_range": {
                "enable_ip_range": False, "ip_range": None},
        },
            "json_data": {
                "JobId": 1234,
                "SystemConfiguration": {
                    "Comments": ["Export type is Normal,JSON"],
                    "Model": "", "ServiceTag": "",
                    "Components": [
                        {
                            "FQDD": "MM.Embedded.1",
                            "Attributes": [
                                {
                                    "Name": "LoginSecurity.1#Id",
                                    "Value": "10"
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutFailCount",
                                    "Value": 5
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutFailCountTime",
                                    "Value": 30
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutPenaltyTime",
                                    "Value": 900
                                },
                                {
                                    "Name": "LoginSecurity.1#IPRangeAddr",
                                    "Value": None
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutByUsernameEnable",
                                    "Value": False
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutByIPEnable",
                                    "Value": False
                                },
                                {
                                    "Name": "LoginSecurity.1#IPRangeEnable",
                                    "Value": False
                                }
                            ]
                        }
                    ]
                }
        }, "msg": NO_CHANGES_MSG},
        {"module_args": {
            "job_wait": False, "job_wait_timeout": 120,
            "login_lockout_policy": {
                "by_ip_address": False, "by_user_name": False, "lockout_fail_count": 5,
                "lockout_fail_window": 30, "lockout_penalty_time": 900},
            "restrict_allowed_ip_range": {
                "enable_ip_range": False, "ip_range": None},
        }, "check_mode": True,
            "json_data": {
                "JobId": 1234,
                "SystemConfiguration": {
                    "Comments": ["Export type is Normal,JSON"],
                    "Model": "", "ServiceTag": "",
                    "Components": [
                        {
                            "FQDD": "MM.Embedded.1",
                            "Attributes": [
                                {
                                    "Name": "LoginSecurity.1#Id",
                                    "Value": "10"
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutFailCount",
                                    "Value": 3
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutFailCountTime",
                                    "Value": 32
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutPenaltyTime",
                                    "Value": 850
                                },
                                {
                                    "Name": "LoginSecurity.1#IPRangeAddr",
                                    "Value": None
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutByUsernameEnable",
                                    "Value": True
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutByIPEnable",
                                    "Value": True
                                },
                                {
                                    "Name": "LoginSecurity.1#IPRangeEnable",
                                    "Value": False
                                }
                            ]
                        }
                    ]
                }
        }, "msg": CHANGES_FOUND},
        {"module_args": {
            "job_wait": True, "job_wait_timeout": 120,
            "login_lockout_policy": {
                "by_ip_address": False, "by_user_name": False, "lockout_fail_count": 5,
                "lockout_fail_window": 30, "lockout_penalty_time": 900},
            "restrict_allowed_ip_range": {
                "enable_ip_range": False, "ip_range": None},
        },
            "job_failed": False, "job_message": "job_message",
            "json_data": {
                "JobId": 1234,
                "SystemConfiguration": {
                    "Comments": ["Export type is Normal,JSON"],
                    "Model": "", "ServiceTag": "",
                    "Components": [
                        {
                            "FQDD": "MM.Embedded.1",
                            "Attributes": [
                                {
                                    "Name": "LoginSecurity.1#Id",
                                    "Value": "10"
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutFailCount",
                                    "Value": 3
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutFailCountTime",
                                    "Value": 32
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutPenaltyTime",
                                    "Value": 850
                                },
                                {
                                    "Name": "LoginSecurity.1#IPRangeAddr",
                                    "Value": None
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutByUsernameEnable",
                                    "Value": True
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutByIPEnable",
                                    "Value": True
                                },
                                {
                                    "Name": "LoginSecurity.1#IPRangeEnable",
                                    "Value": False
                                }
                            ]
                        }
                    ]
                }
        }, "msg": SEC_JOB_COMPLETE},
        {"module_args": {
            "job_wait": True, "job_wait_timeout": 120,
            "login_lockout_policy": {
                "by_ip_address": False, "by_user_name": False, "lockout_fail_count": 5,
                "lockout_fail_window": 30, "lockout_penalty_time": 900},
            "restrict_allowed_ip_range": {
                "enable_ip_range": False, "ip_range": None},
        },
            "job_failed": True, "job_message": "job_failed",
            "json_data": {
                "JobId": 1234,
                "value": [
                    {
                        "Id": 1234,
                        "StartTime": "2021-01-01 09:54:08.721",
                        "EndTime": "2021-01-01 09:54:09.022",
                        "Key": "This Chassis",
                        "Value": "job_failed_exec"
                    }
                ],
                "SystemConfiguration": {
                    "Comments": ["Export type is Normal,JSON"],
                    "Model": "", "ServiceTag": "",
                    "Components": [
                        {
                            "FQDD": "MM.Embedded.1",
                            "Attributes": [
                                {
                                    "Name": "LoginSecurity.1#Id",
                                    "Value": "10"
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutFailCount",
                                    "Value": 3
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutFailCountTime",
                                    "Value": 32
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutPenaltyTime",
                                    "Value": 850
                                },
                                {
                                    "Name": "LoginSecurity.1#IPRangeAddr",
                                    "Value": None
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutByUsernameEnable",
                                    "Value": True
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutByIPEnable",
                                    "Value": True
                                },
                                {
                                    "Name": "LoginSecurity.1#IPRangeEnable",
                                    "Value": False
                                }
                            ]
                        }
                    ]
                }
        }, "msg": "job_failed_exec"},
        {"module_args": {"fips_mode_enable": True},
         "json_data": {"FipsMode": "OFF"},
         "msg": FIPS_TOGGLED.format("enabled")},
        {"module_args": {"fips_mode_enable": False},
         "json_data": {"FipsMode": "ON"},
         "msg": FIPS_TOGGLED.format("disabled")},
        {"module_args": {"fips_mode_enable": True},
         "json_data": {"FipsMode": "ON"},
         "msg": NO_CHANGES_MSG},
        {"module_args": {"fips_mode_enable": False},
         "json_data": {"FipsMode": "ON"},
         "msg": CHANGES_FOUND, "check_mode": True},
        {"module_args": {
            "job_wait": True, "job_wait_timeout": -120,
            "login_lockout_policy": {
                "by_ip_address": False, "by_user_name": True, "lockout_fail_count": 5,
                "lockout_fail_window": 30, "lockout_penalty_time": 900},
        },
            "json_data": {
                "JobId": 1234,
                "SystemConfiguration": {
                    "Comments": ["Export type is Normal,JSON"],
                    "Model": "", "ServiceTag": "",
                    "Components": [
                        {
                            "FQDD": "MM.Embedded.1",
                            "Attributes": [
                                {
                                    "Name": "LoginSecurity.1#Id",
                                    "Value": "10"
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutFailCount",
                                    "Value": 7
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutFailCountTime",
                                    "Value": 27
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutPenaltyTime",
                                    "Value": 859
                                },
                                {
                                    "Name": "LoginSecurity.1#IPRangeAddr",
                                    "Value": None
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutByUsernameEnable",
                                    "Value": False
                                },
                                {
                                    "Name": "LoginSecurity.1#LockoutByIPEnable",
                                    "Value": False
                                },
                                {
                                    "Name": "LoginSecurity.1#IPRangeEnable",
                                    "Value": False
                                }
                            ]
                        }
                    ]
                }
        }, "msg": TIMEOUT_NEGATIVE_OR_ZERO_MSG}
    ])
    def test_ome_application_security_success(
            self,
            params,
            ome_connection_mock_for_security_settings,
            ome_response_mock,
            ome_default_args,
            mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params.get("json_data")
        ome_default_args.update(params['module_args'])
        ome_connection_mock_for_security_settings.job_tracking.return_value = \
            (params.get('job_failed'), params.get('job_message'))
        mocker.patch(MODULE_PATH + 'time.sleep', return_value=None)
        result = self._run_module(
            ome_default_args, check_mode=params.get(
                'check_mode', False))
        assert result['msg'] == params['msg']

    @pytest.mark.parametrize("exc_type",
                             [IOError,
                              ValueError,
                              SSLValidationError,
                              TypeError,
                              ConnectionError,
                              HTTPError,
                              URLError])
    def test_security_settings_main_exception_case(
            self,
            exc_type,
            mocker,
            ome_default_args,
            ome_connection_mock_for_security_settings,
            ome_response_mock):
        ome_default_args.update({"restrict_allowed_ip_range": {
            "enable_ip_range": False
        }})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(
                MODULE_PATH + 'login_security_setting',
                side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(
                MODULE_PATH + 'login_security_setting',
                side_effect=exc_type("exception message"))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'login_security_setting',
                         side_effect=exc_type('https://testhost.com',
                                              400,
                                              'http error message',
                                              {"accept-type": "application/json"},
                                              StringIO(json_str)))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result
