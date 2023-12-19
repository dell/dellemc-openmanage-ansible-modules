# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.0.0
# Copyright (C) 2021-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

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
from ansible_collections.dellemc.openmanage.plugins.modules import ome_application_alerts_smtp
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

SUCCESS_MSG = "Successfully updated the SMTP settings."
SMTP_URL = "AlertService/AlertDestinations/SMTPConfiguration"
NO_CHANGES = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_application_alerts_smtp.'
MODULE_UTIL_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.ome.'


@pytest.fixture
def ome_connection_mock_for_smtp(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestAppAlertsSMTP(FakeAnsibleModule):
    module = ome_application_alerts_smtp

    @pytest.mark.parametrize("params", [
        {
            "module_args": {
                "destination_address": "localhost", "port_number": 25, "use_ssl": True,
                "enable_authentication": True,
                "credentials": {"username": "username", "password": "password"}
            },
            "json_data": {
                "@odata.context": "/api/$metadata#Collection(AlertDestinations.SMTPConfiguration)",
                "@odata.count": 1,
                "value": [
                    {
                        "@odata.type": "#AlertDestinations.SMTPConfiguration",
                        "DestinationAddress": "localhost",
                        "UseCredentials": True,
                        "PortNumber": 25,
                        "UseSSL": True,
                        "Credential": {
                            "User": "username",
                            "Password": ""
                        }
                    }
                ]
            }
        }
    ])
    def test_fetch_smtp_settings(self, params, ome_connection_mock_for_smtp, ome_response_mock):
        ome_response_mock.success = True
        f_module = self.get_module_mock(params=params['module_args'])
        ome_response_mock.json_data = params["json_data"]
        ret_data = self.module.fetch_smtp_settings(ome_connection_mock_for_smtp)
        assert ret_data.get("DestinationAddress") == "localhost"

    @pytest.mark.parametrize("params", [
        {
            "module_args": {
                "destination_address": "localhost", "port_number": 25, "use_ssl": True,
                "enable_authentication": True,
                "credentials": {"username": "username", "password": "password"}
            },

            "json_data": {
                "DestinationAddress": "localhost",
                "PortNumber": 25,
                "UseCredentials": True,
                "UseSSL": True,
                "Credential": {
                    "User": "username",
                    "Password": None
                }
            },
            "payload": {
                "DestinationAddress": "localhost",
                "UseCredentials": True,
                "PortNumber": 25,
                "UseSSL": True,
                "Credential": {
                    "User": "username",
                    "Password": "password"
                }
            }
        }
    ])
    def test_update_smtp_settings(self, params, ome_connection_mock_for_smtp, ome_response_mock):
        ome_response_mock.success = True
        ome_response_mock.status_code = 201
        f_module = self.get_module_mock(params=params['module_args'])
        ome_response_mock.json_data = params["json_data"]
        payload = params["payload"]
        ret_data = self.module.update_smtp_settings(ome_connection_mock_for_smtp, payload)
        assert ret_data.json_data.get("DestinationAddress") == "localhost"

    @pytest.mark.parametrize("params", [
        {
            "module_args": {
                "destination_address": "localhost", "port_number": 25, "use_ssl": True,
                "enable_authentication": True,
                "credentials": {"username": "username", "password": "password"}
            },
            "payload": {
                "DestinationAddress": "localhost",
                "UseCredentials": True,
                "PortNumber": 25,
                "UseSSL": True,
                "Credential": {
                    "User": "username",
                    "Password": None
                }
            }
        }
    ])
    def test_update_payload_auth(self, params, ome_connection_mock_for_smtp, ome_response_mock):
        f_module = self.get_module_mock(params=params['module_args'])
        payload = params["payload"]
        ret_data = self.module.update_payload(f_module, payload)
        assert ret_data.get("DestinationAddress") == "localhost"
        assert ret_data.get("UseCredentials") is True
        assert ret_data.get("Credential") is not None

    @pytest.mark.parametrize("params", [
        {
            "module_args": {
                "destination_address": "localhost", "port_number": 25, "use_ssl": True,
                "enable_authentication": False,
                "credentials": {"username": "username", "password": "password"}
            },
            "payload": {
                "DestinationAddress": "localhost",
                "UseCredentials": True,
                "PortNumber": 25,
                "UseSSL": True,
                "Credential": {
                    "User": "username",
                    "Password": None
                }
            }
        }
    ])
    def test_update_payload_without_auth(self, params, ome_connection_mock_for_smtp, ome_response_mock):
        f_module = self.get_module_mock(params=params['module_args'])
        payload = params["payload"]
        ret_data = self.module.update_payload(f_module, payload)
        assert ret_data.get("DestinationAddress") == "localhost"
        assert ret_data.get("UseCredentials") is False
        assert ret_data.get("Credential") is None

    @pytest.mark.parametrize("params", [
        {
            "module_args": {
                "destination_address": "localhost", "port_number": 25, "use_ssl": True,
                "enable_authentication": False,
                "credentials": {"username": "username", "password": "password"}
            },
            "payload": {
                "DestinationAddress": "",
                "UseCredentials": True,
                "PortNumber": 26,
                "UseSSL": True,
                "Credential": {
                    "User": "username",
                    "Password": None
                }
            }
        },
        {
            "module_args": {
                "destination_address": "localhost", "use_ssl": True,
                "enable_authentication": False,
                "credentials": {"username": "username", "password": "password"}
            },
            "payload": {
                "DestinationAddress": "",
                "UseCredentials": True,
                "PortNumber": 25,
                "UseSSL": True,
                "Credential": {
                    "User": "username",
                    "Password": None
                }
            }
        },
    ])
    def test_get_value(self, params, ome_connection_mock_for_smtp, ome_response_mock):
        f_module = self.get_module_mock(params=params['module_args'])
        payload = params["payload"]
        ret_data = self.module.get_value(f_module, payload, "port_number", "PortNumber")
        assert ret_data == 25

    @pytest.mark.parametrize("params", [
        {
            "payload1": {
                "DestinationAddress": "localhost",
                "UseCredentials": True,
                "PortNumber": 25,
                "UseSSL": True,
                "Credential": {
                    "User": "username",
                    "Password": "password"
                }
            },
            "payload2": {
                "DestinationAddress": "localhost",
                "UseCredentials": True,
                "PortNumber": 25,
                "UseSSL": True,
                "Credential": {
                    "User": "username",
                    "Password": "password"
                }
            }
        },
    ])
    def test_diff_payload_same(self, params, ome_connection_mock_for_smtp, ome_response_mock):
        payload1 = params["payload1"]
        payload2 = params["payload2"]
        diff = self.module._diff_payload(payload1, payload2)
        assert diff == 0

    @pytest.mark.parametrize("params", [
        {
            "payload1": {
                "DestinationAddress": "localhost",
                "UseCredentials": True,
                "PortNumber": 25,
                "UseSSL": True,
            },
            "payload2": {
                "DestinationAddress": "localhost",
                "UseCredentials": True,
                "PortNumber": 25,
                "UseSSL": True,
                "Credential": {
                    "User": "username",
                    "Password": "password"
                }
            }
        },
    ])
    def test_diff_payload_diff(self, params, ome_connection_mock_for_smtp, ome_response_mock):
        payload1 = params["payload1"]
        payload2 = params["payload2"]
        diff = self.module._diff_payload(payload1, payload2)
        assert diff is True

    def test_diff_payload_none(self, ome_connection_mock_for_smtp, ome_response_mock):
        diff = self.module._diff_payload(None, None)
        assert diff is False

    @pytest.mark.parametrize("params", [
        {
            "module_args": {
                "destination_address": "localhost", "port_number": 25, "use_ssl": True,
                "enable_authentication": True,
                "credentials": {"username": "username", "password": "password"}
            },
            "json_data": {
                "DestinationAddress": "localhost1",
                "PortNumber": 25,
                "UseCredentials": True,
                "UseSSL": True,
                "Credential": {
                    "User": "username",
                    "Password": None
                }
            },
        }
    ])
    def test_module_success(self, mocker, params, ome_connection_mock_for_smtp, ome_response_mock, ome_default_args):
        ome_response_mock.success = True
        ome_response_mock.status_code = 201
        ome_response_mock.json_data = params["json_data"]
        ome_default_args.update(params['module_args'])

        get_json_data = {
            "DestinationAddress": "localhost",
            "UseCredentials": True,
            "PortNumber": 25,
            "UseSSL": True,
            "Credential": {
                "User": "username",
                "Password": ""
            }
        }

        update_json_data = params["json_data"]
        mocker.patch(MODULE_PATH + 'fetch_smtp_settings', return_value=get_json_data)
        mocker.patch(MODULE_PATH + 'update_payload', return_value=update_json_data)
        mocker.patch(MODULE_PATH + '_diff_payload', return_value=1)
        result = self._run_module(ome_default_args)
        assert result["msg"] == SUCCESS_MSG

    @pytest.mark.parametrize("params", [
        {
            "module_args": {
                "destination_address": "localhost", "port_number": 25, "use_ssl": True,
                "enable_authentication": True,
                "credentials": {"username": "username", "password": "password"}
            },
            "json_data": {
                "DestinationAddress": "localhost1",
                "PortNumber": 25,
                "UseCredentials": True,
                "UseSSL": True,
                "Credential": {
                    "User": "username",
                    "Password": None
                }
            },
        }
    ])
    def test_module_success_no_auth(self, mocker, params, ome_connection_mock_for_smtp, ome_response_mock,
                                    ome_default_args):
        ome_response_mock.success = True
        ome_response_mock.status_code = 201
        ome_response_mock.json_data = params["json_data"]
        ome_default_args.update(params['module_args'])

        get_json_data = {
            "DestinationAddress": "localhost",
            "UseCredentials": True,
            "PortNumber": 25,
            "UseSSL": False
        }

        update_json_data = params["json_data"]
        mocker.patch(MODULE_PATH + 'fetch_smtp_settings', return_value=get_json_data)
        mocker.patch(MODULE_PATH + 'update_payload', return_value=update_json_data)
        mocker.patch(MODULE_PATH + '_diff_payload', return_value=1)
        result = self._run_module(ome_default_args)
        assert result["msg"] == SUCCESS_MSG

    @pytest.mark.parametrize("params", [
        {
            "module_args": {
                "destination_address": "localhost", "port_number": 25, "use_ssl": True,
                "enable_authentication": True,
                "credentials": {"username": "username", "password": "password"}
            },
            "json_data": {
                "DestinationAddress": "localhost1",
                "PortNumber": 25,
                "UseCredentials": True,
                "UseSSL": True,
                "Credential": {
                    "User": "username",
                    "Password": None
                }
            },
        }
    ])
    def test_module_idempotent(self, mocker, params, ome_connection_mock_for_smtp, ome_response_mock, ome_default_args):
        ome_response_mock.success = True
        ome_response_mock.status_code = 201
        ome_response_mock.json_data = params["json_data"]
        ome_default_args.update(params['module_args'])
        get_json_data = params["json_data"]
        update_json_data = params["json_data"]
        mocker.patch(MODULE_PATH + 'fetch_smtp_settings', return_value=get_json_data)
        mocker.patch(MODULE_PATH + 'update_payload', return_value=update_json_data)
        mocker.patch(MODULE_PATH + '_diff_payload', return_value=0)
        result = self._run_module(ome_default_args)
        assert result["msg"] == NO_CHANGES

    @pytest.mark.parametrize("params", [
        {
            "module_args": {
                "destination_address": "localhost", "port_number": 25, "use_ssl": True,
                "enable_authentication": True,
                "credentials": {"username": "username", "password": "password"}
            },
            "json_data": {
                "DestinationAddress": "localhost1",
                "PortNumber": 25,
                "UseCredentials": True,
                "UseSSL": True,
                "Credential": {
                    "User": "username",
                    "Password": None
                }
            },
        }
    ])
    def test_module_check_mode(self, mocker, params, ome_connection_mock_for_smtp, ome_response_mock,
                               ome_default_args):
        ome_response_mock.success = True
        ome_response_mock.status_code = 201
        ome_response_mock.json_data = params["json_data"]
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

    @pytest.mark.parametrize("exc_type",
                             [HTTPError, URLError])
    def test_smtp_main_exception_case(self, mocker, exc_type, ome_connection_mock_for_smtp, ome_response_mock,
                                      ome_default_args):
        ome_default_args.update({"destination_address": "localhost", "port_number": 25, "use_ssl": True,
                                 "enable_authentication": True,
                                 "credentials": {"username": "username", "password": "password"}
                                 })
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'fetch_smtp_settings', side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'fetch_smtp_settings', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'fetch_smtp_settings',
                         side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
