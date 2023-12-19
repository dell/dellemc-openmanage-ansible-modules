# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.0.0
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import json
import pytest
from ansible_collections.dellemc.openmanage.plugins.modules import ome_network_port_breakout
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from io import StringIO
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


@pytest.fixture
def ome_connection_breakout_mock(mocker, ome_response_mock):
    connection_class_mock = mocker.patch("{0}{1}".format(MODULE_PATH, "ome_network_port_breakout.RestOME"))
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOMEPortBreakout(FakeAnsibleModule):
    module = ome_network_port_breakout

    def test_get_payload(self, ome_connection_breakout_mock, ome_response_mock, ome_default_args):
        payload = self.module.get_breakout_payload("25017", "HardwareDefault", "2HB7NX2:phy-port1/1/11")
        assert payload["JobName"] == "Breakout Port"

    def test_check_mode(self, ome_connection_breakout_mock, ome_response_mock, ome_default_args):
        f_module = self.get_module_mock(check_mode=True)
        with pytest.raises(Exception) as exc:
            self.module.check_mode(f_module, changes=True)
        assert exc.value.args[0] == "Changes found to commit!"

    def test_get_device_id(self, ome_connection_breakout_mock, ome_response_mock, ome_default_args):
        f_module = self.get_module_mock(params={"target_port": "2HB7NX2:phy-port1/1/11", "breakout_type": "1X40GE"})
        ome_response_mock.status_code = 200
        ome_response_mock.json_data = {"value": [{"Id": 25017, "DeviceServiceTag": "2HB7NX2"}]}
        result = self.module.get_device_id(f_module, ome_connection_breakout_mock)
        assert result == 25017

    def test_get_device_id_regex_failed(self, ome_connection_breakout_mock, ome_response_mock, ome_default_args):
        f_module = self.get_module_mock(params={"target_port": "2HB7NX2:phy-:port1/1/11", "breakout_type": "1X40GE"})
        with pytest.raises(Exception) as exc:
            self.module.get_device_id(f_module, ome_connection_breakout_mock)
        assert exc.value.args[0] == "Invalid target port 2HB7NX2:phy-:port1/1/11."

    def test_get_device_id_invalid_status(self, ome_connection_breakout_mock, ome_response_mock, ome_default_args):
        f_module = self.get_module_mock(params={"target_port": "2HB7NX2:phy-port1/1/11", "breakout_type": "1X40GE"})
        ome_response_mock.status_code = 200
        ome_response_mock.json_data = {"value": []}
        with pytest.raises(Exception) as exc:
            self.module.get_device_id(f_module, ome_connection_breakout_mock)
        assert exc.value.args[0] == "Unable to retrieve the device information because the" \
                                    " device with the entered service tag 2HB7NX2 is not present."

    def test_get_port_information(self, ome_connection_breakout_mock, ome_response_mock, ome_default_args):
        f_module = self.get_module_mock(params={"target_port": "2HB7NX2:phy-port1/1/11", "breakout_type": "1X40GE"})
        ome_response_mock.json_data = {"InventoryInfo": [{"Configuration": "HardwareDefault",
                                                         "Id": "2HB7NX2:phy-port1/1/11",
                                                          "PortBreakoutCapabilities": [{"Type": "1X40GE"},
                                                                                       {"Type": "1X10GE"},
                                                                                       {"Type": "HardwareDefault"}]}]}
        config, capability, interface = self.module.get_port_information(f_module, ome_connection_breakout_mock, 25017)
        assert config == "HardwareDefault"

    def test_get_port_information_failed(self, ome_connection_breakout_mock, ome_response_mock, ome_default_args):
        f_module = self.get_module_mock(params={"target_port": "2HB7NX2:phy-port1/1/11", "breakout_type": "1X40GE"})
        ome_response_mock.json_data = {"InventoryInfo": [{"Configuration": "NoBreakout",
                                                         "Id": "2HB7NX2:phy-port1/1/11",
                                                          "PortBreakoutCapabilities": [{"Type": "1X40GE"},
                                                                                       {"Type": "1X10GE"},
                                                                                       {"Type": "HardwareDefault"}]}]}
        with pytest.raises(Exception) as exc:
            self.module.get_port_information(f_module, ome_connection_breakout_mock, 25017)
        assert exc.value.args[0] == "2HB7NX2:phy-port1/1/11 does not support port breakout" \
                                    " or invalid port number entered."

    def test_set_breakout_port(self, ome_connection_breakout_mock, ome_response_mock, ome_default_args, mocker):
        f_module = self.get_module_mock(params={"target_port": "2HB7NX2:phy-port1/1/11", "breakout_type": "1X40GE"})
        capability = [{"Type": "1X40GE"}, {"Type": "1X10GE"}, {"Type": "HardwareDefault"}]
        payload = {
            "Id": 0, "JobName": "Breakout Port", "JobDescription": "",
            "Schedule": "startnow", "State": "Enabled",
            "JobType": {"Id": 3, "Name": "DeviceAction_Task"},
            "Params": [
                {"Key": "breakoutType", "Value": "1X40GE"},
                {"Key": "interfaceId", "Value": "2HB7NX2:phy-port1/1/11"},
                {"Key": "operationName", "Value": "CONFIGURE_PORT_BREAK_OUT"}],
            "Targets": [
                {"JobId": 0, "Id": 25017, "Data": "", "TargetType": {"Id": 4000, "Name": "DEVICE"}}
            ]}
        mocker.patch("{0}{1}".format(MODULE_PATH, "ome_network_port_breakout.get_breakout_payload"),
                     return_value=payload)
        ome_response_mock.status_code = 200
        result = self.module.set_breakout(f_module, ome_connection_breakout_mock, "HardwareDefault",
                                          capability, "2HB7NX2:phy-port1/1/11", 25017)
        assert result.status_code == 200

    def test_set_breakout_port_invalid(self, ome_connection_breakout_mock, ome_response_mock, ome_default_args, mocker):
        f_module = self.get_module_mock(params={"target_port": "2HB7NX2:phy-port1/1/11", "breakout_type": "1X100GE"})
        capability = [{"Type": "1X40GE"}, {"Type": "1X10GE"}, {"Type": "HardwareDefault"}]
        payload = {
            "Id": 0, "JobName": "Breakout Port", "JobDescription": "",
            "Schedule": "startnow", "State": "Enabled",
            "JobType": {"Id": 3, "Name": "DeviceAction_Task"},
            "Params": [
                {"Key": "breakoutType", "Value": "1X40GE"},
                {"Key": "interfaceId", "Value": "2HB7NX2:phy-port1/1/11"},
                {"Key": "operationName", "Value": "CONFIGURE_PORT_BREAK_OUT"}],
            "Targets": [
                {"JobId": 0, "Id": 25017, "Data": "", "TargetType": {"Id": 4000, "Name": "DEVICE"}}
            ]}
        mocker.patch("{0}{1}".format(MODULE_PATH, "ome_network_port_breakout.get_breakout_payload"),
                     return_value=payload)
        with pytest.raises(Exception) as exc:
            self.module.set_breakout(f_module, ome_connection_breakout_mock, "HardwareDefault",
                                     capability, "2HB7NX2:phy-port1/1/11", 25017)
        assert exc.value.args[0] == "Invalid breakout type: 1X100GE, supported values are 1X40GE, " \
                                    "1X10GE, HardwareDefault."

    def test_set_breakout_port_reset(self, ome_connection_breakout_mock, ome_response_mock, ome_default_args, mocker):
        f_module = self.get_module_mock(params={"target_port": "2HB7NX2:phy-port1/1/11",
                                                "breakout_type": "HardwareDefault"})
        capability = [{"Type": "1X40GE"}, {"Type": "1X10GE"}, {"Type": "HardwareDefault"}]
        payload = {
            "Id": 0, "JobName": "Breakout Port", "JobDescription": "",
            "Schedule": "startnow", "State": "Enabled",
            "JobType": {"Id": 3, "Name": "DeviceAction_Task"},
            "Params": [
                {"Key": "breakoutType", "Value": "1X40GE"},
                {"Key": "interfaceId", "Value": "2HB7NX2:phy-port1/1/11"},
                {"Key": "operationName", "Value": "CONFIGURE_PORT_BREAK_OUT"}],
            "Targets": [
                {"JobId": 0, "Id": 25017, "Data": "", "TargetType": {"Id": 4000, "Name": "DEVICE"}}
            ]}
        mocker.patch("{0}{1}".format(MODULE_PATH, "ome_network_port_breakout.get_breakout_payload"),
                     return_value=payload)
        ome_response_mock.status_code = 200
        result = self.module.set_breakout(f_module, ome_connection_breakout_mock, "1X40GE",
                                          capability, "2HB7NX2:phy-port1/1/11", 25017)
        assert result.status_code == 200

    def test_set_breakout_port_symmetry(self, ome_connection_breakout_mock, ome_response_mock, ome_default_args, mocker):
        f_module = self.get_module_mock(params={"target_port": "2HB7NX2:phy-port1/1/11",
                                                "breakout_type": "1X40GE"})
        capability = [{"Type": "1X40GE"}, {"Type": "1X10GE"}, {"Type": "HardwareDefault"}]
        payload = {
            "Id": 0, "JobName": "Breakout Port", "JobDescription": "",
            "Schedule": "startnow", "State": "Enabled",
            "JobType": {"Id": 3, "Name": "DeviceAction_Task"},
            "Params": [
                {"Key": "breakoutType", "Value": "1X40GE"},
                {"Key": "interfaceId", "Value": "2HB7NX2:phy-port1/1/11"},
                {"Key": "operationName", "Value": "CONFIGURE_PORT_BREAK_OUT"}],
            "Targets": [
                {"JobId": 0, "Id": 25017, "Data": "", "TargetType": {"Id": 4000, "Name": "DEVICE"}}
            ]}
        mocker.patch("{0}{1}".format(MODULE_PATH, "ome_network_port_breakout.get_breakout_payload"),
                     return_value=payload)
        with pytest.raises(Exception) as exc:
            self.module.set_breakout(f_module, ome_connection_breakout_mock, "1X40GE",
                                     capability, "2HB7NX2:phy-port1/1/11", 25017)
        assert exc.value.args[0] == "The port is already configured with the selected breakout configuration."

    def test_set_breakout_port_asymmetry(self, ome_connection_breakout_mock, ome_response_mock, ome_default_args, mocker):
        f_module = self.get_module_mock(params={"target_port": "2HB7NX2:phy-port1/1/11", "breakout_type": "1X20GE"})
        capability = [{"Type": "1X40GE"}, {"Type": "1X10GE"}, {"Type": "HardwareDefault"}]
        payload = {
            "Id": 0, "JobName": "Breakout Port", "JobDescription": "",
            "Schedule": "startnow", "State": "Enabled",
            "JobType": {"Id": 3, "Name": "DeviceAction_Task"},
            "Params": [
                {"Key": "breakoutType", "Value": "1X40GE"},
                {"Key": "interfaceId", "Value": "2HB7NX2:phy-port1/1/11"},
                {"Key": "operationName", "Value": "CONFIGURE_PORT_BREAK_OUT"}],
            "Targets": [
                {"JobId": 0, "Id": 25017, "Data": "", "TargetType": {"Id": 4000, "Name": "DEVICE"}}
            ]}
        mocker.patch("{0}{1}".format(MODULE_PATH, "ome_network_port_breakout.get_breakout_payload"),
                     return_value=payload)
        with pytest.raises(Exception) as exc:
            self.module.set_breakout(f_module, ome_connection_breakout_mock, "1X40GE",
                                     capability, "2HB7NX2:phy-port1/1/11", 25017)
        assert exc.value.args[0] == "Device does not support changing a port breakout" \
                                    " configuration to different breakout type. Configure the port to" \
                                    " HardwareDefault and retry the operation."

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_main_exception(self, exc_type, mocker, ome_default_args, ome_connection_breakout_mock, ome_response_mock):
        ome_default_args.update({"target_port": "2HB7NX2:phy-port1/1/11", "breakout_type": "1X20GE"})
        json_str = to_text(json.dumps({"info": "error_details"}))
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        if exc_type not in [HTTPError, SSLValidationError]:
            ome_connection_breakout_mock.invoke_request.side_effect = exc_type('test')
        else:
            ome_connection_breakout_mock.invoke_request.side_effect = exc_type('https://testhost.com', 400,
                                                                               'http error message',
                                                                               {"accept-type": "application/json"},
                                                                               StringIO(json_str))
        if not exc_type == URLError:
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch("{0}{1}".format(MODULE_PATH, "ome_network_port_breakout.get_breakout_payload"),
                         return_value={})
            mocker.patch("{0}{1}".format(MODULE_PATH, "ome_network_port_breakout.get_port_information"),
                         return_value=(None, None, None))
            mocker.patch("{0}{1}".format(MODULE_PATH, "ome_network_port_breakout.set_breakout"),
                         return_value={})
            result = self._run_module(ome_default_args)
        assert 'msg' in result

    def test_main(self, mocker, ome_default_args, ome_connection_breakout_mock, ome_response_mock):
        ome_default_args.update({"target_port": "2HB7NX2:phy-port1/1/11", "breakout_type": "1X20GE"})
        mocker.patch("{0}{1}".format(MODULE_PATH, "ome_network_port_breakout.get_device_id"),
                     return_value=25017)
        mocker.patch("{0}{1}".format(MODULE_PATH, "ome_network_port_breakout.get_breakout_payload"),
                     return_value={})
        mocker.patch("{0}{1}".format(MODULE_PATH, "ome_network_port_breakout.get_port_information"),
                     return_value=("HardwareDefault", [{"Type": "1X40GE"}, {"Type": "1X20GE"}],
                                   "2HB7NX2:phy-port1/1/11"))
        mocker.patch("{0}{1}".format(MODULE_PATH, "ome_network_port_breakout.set_breakout"),
                     return_value=ome_response_mock)
        ome_response_mock.status_code = 200
        result = self._run_module(ome_default_args)
        assert result["msg"] == "Port breakout configuration job submitted successfully."
