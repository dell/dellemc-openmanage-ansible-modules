# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 4.4.0
# Copyright (C) 2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json

import pytest
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.modules import ome_application_network_settings
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants

SUCCESS_MSG = "Successfully updated the session timeout settings."
NO_CHANGES = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_application_network_settings.'
MODULE_UTIL_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.ome.'


@pytest.fixture
def ome_connection_mock_for_ns(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeApplicationNetworkSettings(FakeAnsibleModule):
    module = ome_application_network_settings

    responseData = {
        "value": [
            {
                "@odata.type": "#SessionService.SessionConfiguration",
                "SessionType": "GUI",
                "MaxSessions": 5,
                "SessionTimeout": 1380000,
                "MinSessionTimeout": 60000,
                "MaxSessionTimeout": 86400000,
                "MinSessionsAllowed": 1,
                "MaxSessionsAllowed": 100,
                "MaxSessionsConfigurable": True,
                "SessionTimeoutConfigurable": True
            },
            {
                "@odata.type": "#SessionService.SessionConfiguration",
                "SessionType": "API",
                "MaxSessions": 100,
                "SessionTimeout": 1380000,
                "MinSessionTimeout": 60000,
                "MaxSessionTimeout": 86400000,
                "MinSessionsAllowed": 1,
                "MaxSessionsAllowed": 100,
                "MaxSessionsConfigurable": True,
                "SessionTimeoutConfigurable": True
            },
            {
                "@odata.type": "#SessionService.SessionConfiguration",
                "SessionType": "UniversalTimeout",
                "MaxSessions": 0,
                "SessionTimeout": 1380000,
                "MinSessionTimeout": -1,
                "MaxSessionTimeout": 86400000,
                "MinSessionsAllowed": 0,
                "MaxSessionsAllowed": 0,
                "MaxSessionsConfigurable": False,
                "SessionTimeoutConfigurable": True
            }
        ]
    }

    @pytest.mark.parametrize("params", [
        {
            "module_args": {
                "destination_address": "localhost", "port_number": 25, "use_ssl": True,
                "enable_authentication": True,
                "credentials": {"username": "username", "password": "password"}
            },
            "json_data": responseData
        }
    ])
    def test_fetch_session_inactivity_settings(self, params, ome_connection_mock_for_ns, ome_response_mock):
        ome_response_mock.success = True
        ome_response_mock.json_data = params["json_data"]
        ret_data = self.module.fetch_session_inactivity_settings(ome_connection_mock_for_ns)
        assert ret_data[0].get("SessionType") == "GUI"
        assert ret_data[0].get("MaxSessions") == 5
        assert ret_data[0].get("SessionTimeout") == 1380000

    @pytest.mark.parametrize("params", [
        {
            "json_data": responseData.get("value"),
            "payload": responseData.get("value"),
        }
    ])
    def test_update_session_inactivity_settings(self, params, ome_connection_mock_for_ns, ome_response_mock):
        ome_response_mock.success = True
        ome_response_mock.status_code = 201
        ome_response_mock.json_data = params["json_data"]
        payload = params["payload"]
        ret_value = self.module.update_session_inactivity_settings(ome_connection_mock_for_ns, payload)
        ret_data = ret_value.json_data
        assert ret_data[0].get("SessionType") == "GUI"
        assert ret_data[0].get("MaxSessions") == 5
        assert ret_data[0].get("SessionTimeout") == 1380000

    @pytest.mark.parametrize("params", [
        {
            "module_args": {
                "session_inactivity_timeout": {
                    "enable_universal_timeout": True,
                    "universal_timeout": 2
                }
            },
            "payload": responseData.get("value")
        }
    ])
    def test_update_payload_ut_enable(self, params, ome_connection_mock_for_ns, ome_response_mock):
        f_module = self.get_module_mock(params=params['module_args'])
        payload = params["payload"]
        ret_data, diff = self.module.update_payload(f_module, payload)
        assert ret_data[2].get("SessionType") == "UniversalTimeout"
        assert ret_data[2].get("SessionTimeout") == 120000
        assert diff == 1

    @pytest.mark.parametrize("params", [
        {
            "module_args": {
                "session_inactivity_timeout": {
                    "enable_universal_timeout": False,
                    "universal_timeout": 2
                }
            },
            "payload": responseData.get("value")
        }
    ])
    def test_update_payload_ut_disable(self, params, ome_connection_mock_for_ns, ome_response_mock):
        f_module = self.get_module_mock(params=params['module_args'])
        payload = params["payload"]
        ret_data, diff = self.module.update_payload(f_module, payload)
        assert ret_data[2].get("SessionType") == "UniversalTimeout"
        assert ret_data[2].get("SessionTimeout") == -1
        assert diff == 1

    @pytest.mark.parametrize("params", [
        {
            "module_args": {
                "session_inactivity_timeout": {
                    "universal_timeout": 2
                }
            },
            "payload": responseData.get("value")
        }
    ])
    def test_update_payload_no_change(self, params, ome_connection_mock_for_ns, ome_response_mock):
        f_module = self.get_module_mock(params=params['module_args'])
        payload = params["payload"]
        ret_data, diff = self.module.update_payload(f_module, payload)
        assert diff == 0

    @pytest.mark.parametrize("params", [
        {
            "module_args": {
                "session_inactivity_timeout": {
                    "api_timeout": 2
                }
            },
            "payload": responseData.get("value")
        }
    ])
    def test_update_payload_timeout_change(self, params, ome_connection_mock_for_ns, ome_response_mock):
        f_module = self.get_module_mock(params=params['module_args'])
        payload = params["payload"]
        ret_data, diff = self.module.update_payload(f_module, payload)
        assert ret_data[1].get("SessionTimeout") == 1380000
        assert diff == 0

    @pytest.mark.parametrize("params", [
        {
            "module_args": {
                "session_inactivity_timeout": {
                    "api_sessions": 90
                }
            },
            "payload": responseData.get("value")
        }
    ])
    def test_update_payload_max_sessions_change(self, params, ome_connection_mock_for_ns, ome_response_mock):
        f_module = self.get_module_mock(params=params['module_args'])
        payload = params["payload"]
        ret_data, diff = self.module.update_payload(f_module, payload)
        assert ret_data[1].get("MaxSessions") == 90
        assert diff == 1

    @pytest.mark.parametrize("params", [
        {
            "module_args": {
                "session_inactivity_timeout": {
                    "api_timeout": 2,
                    "api_sessions": 90
                }
            },
            "payload": responseData.get("value")
        }
    ])
    def test_update_payload_timeout_and_max_session_change(self, params, ome_connection_mock_for_ns, ome_response_mock):
        f_module = self.get_module_mock(params=params['module_args'])
        payload = params["payload"]
        ret_data, diff = self.module.update_payload(f_module, payload)
        assert ret_data[1].get("SessionTimeout") == 1380000
        assert ret_data[1].get("MaxSessions") == 90
        assert diff == 1

    @pytest.mark.parametrize("params", [
        {
            "session_inactivity_timeout": {
                "api_timeout": 2,
                "api_sessions": 90
            },
            "payload": responseData.get("value")[0]
        }
    ])
    def test_get_value_s1(self, params, ome_connection_mock_for_ns, ome_response_mock):
        payload = params["payload"]
        ret_data = self.module.get_value(params.get("session_inactivity_timeout"),
                                         payload, "api_timeout", "SessionTimeout")
        assert ret_data == 120000

    @pytest.mark.parametrize("params", [
        {
            "session_inactivity_timeout": {
                "api_sessions": 90
            },
            "payload": responseData.get("value")[0]
        }
    ])
    def test_get_value_s2(self, params, ome_connection_mock_for_ns, ome_response_mock):
        payload = params["payload"]
        ret_data = self.module.get_value(params.get("session_inactivity_timeout"),
                                         payload, "api_timeout", "SessionTimeout")
        assert ret_data == 1380000

    @pytest.mark.parametrize("params", [
        {
            "session_inactivity_timeout": {
                "universal_timeout": -1
            },
            "payload": responseData.get("value")[2]
        }
    ])
    def test_get_value_s3(self, params, ome_connection_mock_for_ns, ome_response_mock):
        payload = params["payload"]
        ret_data = self.module.get_value(params.get("session_inactivity_timeout"),
                                         payload, "universal_timeout", "SessionTimeout")
        assert ret_data == -1

    @pytest.mark.parametrize("params", [
        {
            "module_args": {
                "session_inactivity_timeout": {
                    "enable_universal_timeout": True,
                    "universal_timeout": 2
                },
            },
            "json_data": responseData.get("value"),
            "get_json_data": responseData.get("value"),
            "update_payload": responseData.get("value"),
        }
    ])
    def test_module_success(self, mocker, params, ome_connection_mock_for_ns, ome_response_mock, ome_default_args):
        ome_response_mock.success = True
        ome_response_mock.status_code = 201
        ome_response_mock.json_data = params["json_data"]
        ome_default_args.update(params['module_args'])
        update_json_data = params["update_payload"]
        update_json_data[2]["SessionTimeout"] = 120000
        mocker.patch(MODULE_PATH + 'fetch_session_inactivity_settings', return_value=params["get_json_data"])
        mocker.patch(MODULE_PATH + 'update_payload', return_value=[update_json_data, 1])
        result = self._run_module(ome_default_args)
        assert result["msg"] == SUCCESS_MSG

    @pytest.mark.parametrize("params", [
        {
            "module_args": {
                "session_inactivity_timeout": {
                    "enable_universal_timeout": True,
                    "universal_timeout": 2
                },
            },
            "json_data": responseData.get("value"),
            "get_json_data": responseData.get("value"),
            "update_payload": responseData.get("value"),
        }
    ])
    def test_module_no_idempotent(self, mocker, params, ome_connection_mock_for_ns, ome_response_mock,
                                  ome_default_args):
        ome_response_mock.success = True
        ome_response_mock.status_code = 201
        ome_response_mock.json_data = params["json_data"]
        ome_default_args.update(params['module_args'])
        update_json_data = params["update_payload"]
        mocker.patch(MODULE_PATH + 'fetch_session_inactivity_settings', return_value=params["get_json_data"])
        mocker.patch(MODULE_PATH + 'update_payload', return_value=[update_json_data, 0])
        result = self._run_module(ome_default_args)
        assert result["msg"] == NO_CHANGES

    @pytest.mark.parametrize("params", [
        {
            "module_args": {
                "session_inactivity_timeout": {
                    "enable_universal_timeout": True,
                    "universal_timeout": 2
                },
            },
            "json_data": responseData.get("value"),
            "get_json_data": responseData.get("value"),
            "update_payload": responseData.get("value"),
        }
    ])
    def test_module_check_mode(self, mocker, params, ome_connection_mock_for_ns, ome_response_mock, ome_default_args):
        ome_response_mock.success = True
        ome_response_mock.status_code = 201
        ome_response_mock.json_data = params["json_data"]
        ome_default_args.update(params['module_args'])
        f_module = self.get_module_mock(params=ome_default_args)

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

    @pytest.mark.parametrize("exc_type",
                             [HTTPError, URLError])
    def test_session_inactivity_settings_main_exception_case(self, mocker, exc_type, ome_connection_mock_for_ns,
                                                             ome_response_mock,
                                                             ome_default_args):
        ome_default_args.update({"session_inactivity_timeout": {
            "enable_universal_timeout": True,
            "universal_timeout": 2
        }})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'fetch_session_inactivity_settings', side_effect=exc_type("url open"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'fetch_session_inactivity_settings', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'fetch_session_inactivity_settings',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
