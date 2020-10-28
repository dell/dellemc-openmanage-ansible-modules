# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.3
# Copyright (C) 2019-2020 Dell Inc. or its subsidiaries. All Rights Reserved.

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
from ansible_collections.dellemc.openmanage.plugins.modules import ome_application_network_webserver
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


@pytest.fixture
def ome_connection_mock_for_application_network_webserver(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(
        MODULE_PATH + 'ome_application_network_webserver.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeAppNetwork(FakeAnsibleModule):
    module = ome_application_network_webserver

    sub_param1 = {"webserver_port": 443, "webserver_timeout": 20}

    @pytest.mark.parametrize("sub_param", [sub_param1])
    def test_ome_application_network_webserver_main_success_case_01(self, mocker, ome_default_args, sub_param,
                                                                    ome_connection_mock_for_application_network_webserver,
                                                                    ome_response_mock):
        ome_default_args.update(sub_param)
        resp = {"TimeOut": 25, "PortNumber": 443, "EnableWebServer": True}
        port_change = 0
        mocker.patch(MODULE_PATH + "ome_application_network_webserver.get_updated_payload",
                     return_value=(resp, port_change))
        ome_response_mock.json_data = resp
        result = self.execute_module(ome_default_args)
        assert result['changed'] is True
        assert "msg" in result
        assert "webserver_configuration" in result and result["webserver_configuration"] == resp
        assert result["msg"] == "Successfully updated network web server configuration."

    in1 = {"webserver_port": 443, "webserver_timeout": 25}
    in2 = {"webserver_timeout": 25}
    out1 = {"TimeOut": 25, "PortNumber": 443, "EnableWebServer": True}
    out2 = {"TimeOut": 25, "PortNumber": 1443, "EnableWebServer": True}

    @pytest.mark.parametrize("sub_param", [{"in": in1, "out": out1},
                                           {"in": in2, "out": out2}])
    def test_get_updated_payload_success1(self, sub_param, ome_default_args,
                                          ome_connection_mock_for_application_network_webserver,
                                          ome_response_mock):
        ome_default_args.update(sub_param["in"])
        ome_response_mock.json_data = {"TimeOut": 20, "PortNumber": 1443, "EnableWebServer": True,
                                       "@odata.context": "$metadata#Network.WebServerConfiguration/$entity",
                                       "@odata.id": "/api/ApplicationService/Network/WebServerConfiguration"}
        f_module = self.get_module_mock(params=ome_default_args)
        payload, port = self.module.get_updated_payload(ome_connection_mock_for_application_network_webserver, f_module)
        assert payload == sub_param["out"]

    def _test_get_updated_payload_when_same_setting_failure_case(self, ome_default_args,
                                                                 ome_connection_mock_for_application_network_webserver,
                                                                 ome_response_mock):
        new_param = {"webserver_port": 443, "webserver_timeout": 25}
        ome_default_args.update(new_param)
        ome_response_mock.json_data = {"TimeOut": 25, "PortNumber": 443, "EnableWebServer": True,
                                       "@odata.context": "$metadata#Network.WebServerConfiguration/$entity",
                                       "@odata.id": "/api/ApplicationService/Network/WebServerConfiguration"}
        f_module = self.get_module_mock(params=ome_default_args)
        error_message = "No changes made to the web server configuration as the entered values are the same as the" \
                        " current configuration."
        with pytest.raises(Exception, match=error_message) as err:
            self.module.get_updated_payload(ome_connection_mock_for_application_network_webserver, f_module)

    in1 = {"check_mode": True, "timeout": 25}
    in2 = {"check_mode": True, "timeout": 30}
    in3 = {"check_mode": False, "timeout": 25}
    out1 = "No changes found to be applied to the web server."
    out2 = "Changes found to be applied to the web server."
    out3 = "No changes made to the web server configuration as the entered values" \
           " are the same as the current configuration."

    @pytest.mark.parametrize("sub_param", [{"in": in1, "out": out1},
                                           {"in": in2, "out": out2},
                                           {"in": in3, "out": out3}])
    def test_get_updated_payload_check_mode(self, sub_param, ome_default_args,
                                            ome_connection_mock_for_application_network_webserver, ome_response_mock):
        new_param = {"webserver_port": 443, "webserver_timeout": sub_param["in"]["timeout"]}
        ome_default_args.update(new_param)
        ome_response_mock.json_data = {"TimeOut": 25, "PortNumber": 443, "EnableWebServer": True,
                                       "@odata.context": "$metadata#Network.WebServerConfiguration/$entity",
                                       "@odata.id": "/api/ApplicationService/Network/WebServerConfiguration"}
        f_module = self.get_module_mock(params=ome_default_args, check_mode=sub_param["in"]["check_mode"])
        error_message = sub_param["out"]
        with pytest.raises(Exception, match=error_message) as err:
            self.module.get_updated_payload(ome_connection_mock_for_application_network_webserver, f_module)

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_application_network_webserver_main_error_cases(self, exc_type, mocker, ome_default_args,
                                                                ome_connection_mock_for_application_network_webserver,
                                                                ome_response_mock):
        json_str = to_text(json.dumps({"info": "error_details"}))
        ome_default_args.update({"webserver_port": 443, "webserver_timeout": 25})
        if exc_type == URLError:
            mocker.patch(
                MODULE_PATH + 'ome_application_network_webserver.get_updated_payload',
                side_effect=exc_type("test"))
            ome_default_args.update({"webserver_port": 443, "webserver_timeout": 25})
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(
                MODULE_PATH + 'ome_application_network_webserver.get_updated_payload',
                side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(
                MODULE_PATH + 'ome_application_network_webserver.get_updated_payload',
                side_effect=exc_type('http://testhost.com', 400,
                                     'http error message',
                                     {"accept-type": "application/json"},
                                     StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'webserver_configuration' not in result
        assert 'msg' in result
