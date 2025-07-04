# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.4
# Copyright (C) 2021-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

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
from ansible_collections.dellemc.openmanage.plugins.modules import ome_application_alerts_syslog
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_application_alerts_syslog.'

SUCCESS_MSG = "Successfully updated the syslog forwarding settings."
DUP_ID_MSG = "Duplicate server IDs are provided."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."


@pytest.fixture
def ome_connection_mock_for_syslog(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeAlertSyslog(FakeAnsibleModule):
    module = ome_application_alerts_syslog

    @pytest.mark.parametrize("params", [
        {"module_args": {
            "syslog_servers": [
                {
                    "destination_address": "XX.XX.XX.XX",
                    "enabled": True,
                    "id": 1,
                    "port_number": 514
                },
                {
                    "destination_address": "XY.XY.XY.XY",
                    "enabled": False,
                    "id": 2,
                    "port_number": 514
                },
                {
                    "destination_address": "YY.YY.YY.YY",
                    "enabled": False,
                    "id": 3,
                    "port_number": 514
                },
                {
                    "destination_address": "ZZ.ZZ.ZZ.ZZ",
                    "enabled": True,
                    "id": 4,
                    "port_number": 514
                }
            ]
        }, "json_data": {
            "@odata.context": "/api/$metadata#Collection(AlertDestinations.SyslogConfiguration)",
            "@odata.count": 4,
            "value": [
                {
                    "@odata.type": "#AlertDestinations.SyslogConfiguration",
                    "Id": 1,
                    "Enabled": True,
                    "DestinationAddress": "XX.XX.XX.XX",
                    "PortNumber": 514
                },
                {
                    "@odata.type": "#AlertDestinations.SyslogConfiguration",
                    "Id": 2,
                    "Enabled": False,
                    "DestinationAddress": "XY.XY.XY.XY",
                    "PortNumber": 0
                },
                {
                    "@odata.type": "#AlertDestinations.SyslogConfiguration",
                    "Id": 3,
                    "Enabled": False,
                    "DestinationAddress": "YY.YY.YY.YY",
                    "PortNumber": 514
                },
                {
                    "@odata.type": "#AlertDestinations.SyslogConfiguration",
                    "Id": 4,
                    "Enabled": True,
                    "DestinationAddress": "ZZ.ZZ.ZZ.ZZ",
                    "PortNumber": 514
                }
            ]
        }, "msg": NO_CHANGES_MSG},
        {"module_args": {
            "syslog_servers": [
                {
                    "destination_address": "XX.XX.XX.XX",
                    "enabled": True,
                    "id": 1,
                    "port_number": 514
                },
                {
                    "destination_address": "XY.XY.XY.XY",
                    "enabled": False,
                    "id": 2,
                    "port_number": 514
                }
            ]
        }, "json_data": {
            "@odata.context": "/api/$metadata#Collection(AlertDestinations.SyslogConfiguration)",
            "@odata.count": 4,
            "value": [
                {
                    "@odata.type": "#AlertDestinations.SyslogConfiguration",
                    "Id": 1,
                    "Enabled": True,
                    "DestinationAddress": "XX.XX.XX.XX",
                    "PortNumber": 511
                },
                {
                    "@odata.type": "#AlertDestinations.SyslogConfiguration",
                    "Id": 2,
                    "Enabled": True,
                    "DestinationAddress": "XY.XY.XY.XY",
                    "PortNumber": 514
                }
            ]
        }, "msg": SUCCESS_MSG},
        {"check_mode": True, "module_args": {
            "syslog_servers": [
                {
                    "destination_address": "XX.XX.XX.XX",
                    "enabled": True,
                    "id": 1,
                    "port_number": 514
                },
                {
                    "destination_address": "XY.XY.XY.XY",
                    "enabled": False,
                    "id": 2,
                    "port_number": 514
                }
            ]
        }, "json_data": {
            "@odata.context": "/api/$metadata#Collection(AlertDestinations.SyslogConfiguration)",
            "@odata.count": 4,
            "value": [
                {
                    "@odata.type": "#AlertDestinations.SyslogConfiguration",
                    "Id": 1,
                    "Enabled": True,
                    "DestinationAddress": "XX.XX.XX.XX",
                    "PortNumber": 511
                },
                {
                    "@odata.type": "#AlertDestinations.SyslogConfiguration",
                    "Id": 2,
                    "Enabled": True,
                    "DestinationAddress": "XY.XY.XY.XY",
                    "PortNumber": 514
                }
            ]
        }, "msg": CHANGES_FOUND},
        {"module_args": {
            "syslog_servers": []
        }, "json_data": {}, "msg": NO_CHANGES_MSG},
        {"module_args": {
            "syslog_servers": [
                {
                    "destination_address": "XX.XX.XX.XX",
                    "enabled": True,
                    "id": 1,
                    "port_number": 514
                },
                {
                    "destination_address": "XY.XY.XY.XY",
                    "enabled": False,
                    "id": 2,
                    "port_number": 514
                },
                {
                    "destination_address": "YY.YY.YY.YY",
                    "enabled": False,
                    "id": 3,
                    "port_number": 514
                },
                {
                    "destination_address": "ZZ.ZZ.ZZ.ZZ",
                    "enabled": True,
                    "id": 4,
                    "port_number": 514
                },
                {
                    "destination_address": "ZZ.ZZ.ZZ.ZZ",
                    "enabled": True,
                    "id": 4,
                    "port_number": 514
                }
            ]
        }, "json_data": {
            "@odata.context": "/api/$metadata#Collection(AlertDestinations.SyslogConfiguration)",
            "@odata.count": 4,
            "value": []
        }, "msg": DUP_ID_MSG},
    ])
    def test_ome_alert_syslog_success(self, params, ome_connection_mock_for_syslog,
                                      ome_response_mock, ome_default_args, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params.get("json_data")
        ome_connection_mock_for_syslog.strip_substr_dict.return_value = params.get("json_data")
        ome_default_args.update(params['module_args'])
        result = self._run_module(ome_default_args, check_mode=params.get('check_mode', False))
        assert result['msg'] == params['msg']

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLValidationError, TypeError, ConnectionError, HTTPError, URLError])
    def test_alert_syslog_main_exception_case(self, exc_type, mocker, ome_default_args,
                                              ome_connection_mock_for_syslog, ome_response_mock):
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'validate_input', side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'validate_input', side_effect=exc_type("exception message"))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'validate_input',
                         side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result
