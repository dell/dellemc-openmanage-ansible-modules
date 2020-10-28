# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.3
# Copyright (C) 2019-2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_redfish_storage_controller
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text
from ansible.module_utils.urls import urllib_error

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


@pytest.fixture
def idrac_connection_mock_for_redfish_storage_controller(mocker, redfish_response_mock):
    connection_class_mock = mocker.patch(
        MODULE_PATH + 'idrac_redfish_storage_controller.Redfish')
    idrac_redfish_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    idrac_redfish_connection_mock_obj.invoke_request.return_value = redfish_response_mock
    return idrac_redfish_connection_mock_obj


class TestIdracRedfishStorageController(FakeAnsibleModule):
    module = idrac_redfish_storage_controller

    msg = "All of the following: key, key_id and old_key are required for ReKey operation."

    @pytest.mark.parametrize("input",
                             [{"param": {"command": "ReKey", "mode": "LKM", "key_id": "myid"}, "msg": msg},
                              {"param": {"command": "ReKey", "mode": "LKM", "old_key": "mykey"}, "msg": msg},
                              {"param": {"command": "ReKey", "mode": "LKM", "key": "mykey"}, "msg": msg}
                              ])
    def test_validate_inputs_error_case_01(self, input):
        f_module = self.get_module_mock(params=input["param"])
        with pytest.raises(Exception) as exc:
            self.module.validate_inputs(f_module)
        assert exc.value.args[0] == input["msg"]

    @pytest.mark.parametrize("input", [{"controller_id": "c1"}])
    def test_check_encryption_capability_failure(self, idrac_connection_mock_for_redfish_storage_controller,
                                                 redfish_response_mock, input):
        f_module = self.get_module_mock(params=input)
        msg = "Encryption is not supported on the storage controller: c1"
        redfish_response_mock.success = True
        redfish_response_mock.json_data = {
            'Oem': {'Dell': {'DellController': {'SecurityStatus': "EncryptionNotCapable"}}}}
        with pytest.raises(Exception) as exc:
            self.module.check_encryption_capability(f_module, idrac_connection_mock_for_redfish_storage_controller)
        assert exc.value.args[0] == msg

    def test_check_raid_service(self, idrac_connection_mock_for_redfish_storage_controller,
                                redfish_response_mock):
        f_module = self.get_module_mock()
        msg = "Installed version of iDRAC does not support this feature using Redfish API"
        redfish_response_mock.success = False
        with pytest.raises(Exception) as exc:
            self.module.check_raid_service(f_module, idrac_connection_mock_for_redfish_storage_controller)
        assert exc.value.args[0] == msg

    @pytest.mark.parametrize("input",
                             [
                                 {"error": urllib_error.URLError("TESTS")}
                             ])
    def test_check_raid_service_exceptions(self, idrac_connection_mock_for_redfish_storage_controller, input):
        f_module = self.get_module_mock(params=input)
        idrac_connection_mock_for_redfish_storage_controller.invoke_request.side_effect = input["error"]
        with pytest.raises(Exception) as exc:
            self.module.check_raid_service(f_module, idrac_connection_mock_for_redfish_storage_controller)
        assert "TESTS" in exc.value.args[0]

    def test_check_raid_service_HttpError_exception(self, idrac_connection_mock_for_redfish_storage_controller,
                                                    redfish_default_args):
        f_module = self.get_module_mock(params=redfish_default_args)
        json_str = to_text(json.dumps({"data": "out"}))
        idrac_connection_mock_for_redfish_storage_controller.invoke_request.side_effect = HTTPError(
            'http://testhost.com', 400, 'http error message',
            {"accept-type": "application/json"}, StringIO(json_str))
        with pytest.raises(Exception) as exc:
            self.module.check_raid_service(f_module, idrac_connection_mock_for_redfish_storage_controller)
        assert exc.value.args[0] == "Installed version of iDRAC does not support this feature using Redfish API"

    @pytest.mark.parametrize("input", [{"volume_id": ["v1"]}])
    def test_check_volume_array_exists(self, idrac_connection_mock_for_redfish_storage_controller,
                                       redfish_response_mock, input):
        f_module = self.get_module_mock(params=input)
        msg = "Unable to locate the virtual disk with the ID: v1"
        redfish_response_mock.success = False
        with pytest.raises(Exception) as exc:
            self.module.check_volume_array_exists(f_module,
                                                  idrac_connection_mock_for_redfish_storage_controller)
        assert exc.value.args[0] == msg

    def test_check_volume_array_exists_HttpError_exceptions(self, redfish_response_mock, redfish_default_args,
                                                            idrac_connection_mock_for_redfish_storage_controller):
        redfish_default_args.update({"volume_id": ["v1"]})
        redfish_response_mock.json_data = {"volume_id": ["v1"]}
        f_module = self.get_module_mock(params=redfish_default_args)
        json_str = to_text(json.dumps({"data": "out"}))
        idrac_connection_mock_for_redfish_storage_controller.invoke_request.side_effect = HTTPError(
            'http://testhost.com', 400, 'http error message',
            {"accept-type": "application/json"}, StringIO(json_str))
        with pytest.raises(Exception) as exc:
            self.module.check_volume_array_exists(f_module, idrac_connection_mock_for_redfish_storage_controller)
        assert exc.value.args[0] == "Unable to locate the virtual disk with the ID: v1"

    def test_check_volume_array_exists_exceptions(self, redfish_response_mock, redfish_default_args,
                                                  idrac_connection_mock_for_redfish_storage_controller):
        redfish_default_args.update({"volume_id": ["v1"]})
        redfish_response_mock.json_data = {"volume_id": ["v1"]}
        f_module = self.get_module_mock(params=redfish_default_args)
        idrac_connection_mock_for_redfish_storage_controller.invoke_request.side_effect = urllib_error.URLError('TESTS')
        with pytest.raises(Exception) as exc:
            self.module.check_volume_array_exists(f_module, idrac_connection_mock_for_redfish_storage_controller)
        assert "TESTS" in exc.value.args[0]

    @pytest.mark.parametrize("input", [{"item": "x1"}])
    def test_check_id_exists(self,
                             idrac_connection_mock_for_redfish_storage_controller,
                             redfish_response_mock, input):
        f_module = self.get_module_mock(params=input)
        msg = "item with id x1 not found in system"
        redfish_response_mock.success = False
        with pytest.raises(Exception) as exc:
            self.module.check_id_exists(f_module,
                                        idrac_connection_mock_for_redfish_storage_controller,
                                        "item", "uri")
        assert exc.value.args[0] == msg

    def test_check_id_exists_exceptions(self, idrac_connection_mock_for_redfish_storage_controller):
        f_module = self.get_module_mock()
        idrac_connection_mock_for_redfish_storage_controller.invoke_request.side_effect = urllib_error.URLError('TESTS')
        with pytest.raises(Exception) as exc:
            self.module.check_id_exists(f_module,
                                        idrac_connection_mock_for_redfish_storage_controller,
                                        "item", "uri")
        assert "TESTS" in exc.value.args[0]

    def test_check_id_exists_HttpError_exceptions(self, idrac_connection_mock_for_redfish_storage_controller,
                                                  redfish_default_args):
        f_module = self.get_module_mock(params=redfish_default_args)
        f_module = self.get_module_mock(params=redfish_default_args)
        json_str = to_text(json.dumps({"data": "out"}))
        idrac_connection_mock_for_redfish_storage_controller.invoke_request.side_effect = HTTPError(
            'http://testhost.com', 400, 'http error message',
            {"accept-type": "application/json"}, StringIO(json_str))
        with pytest.raises(Exception) as exc:
            self.module.check_id_exists(f_module,
                                        idrac_connection_mock_for_redfish_storage_controller,
                                        "item", "uri")
        assert exc.value.args[0] == "item with id None not found in system"

    arg_list1 = [{"command": "ResetConfig", "controller_id": "c1"},
                 {"command": "RemoveControllerKey", "controller_id": "c1"},
                 {"command": "ReKey", "controller_id": "c1"},
                 {"command": "SetControllerKey", "controller_id": "c1", "key": "key", "key_id": "key_id"},
                 {"command": "AssignSpare", "volume_id": ["v1"], "target": "target"}]

    @pytest.mark.parametrize("param", arg_list1)
    def test_idrac_redfish_storage_controller_main_success_case_01(self,
                                                                   mocker,
                                                                   redfish_default_args,
                                                                   redfish_response_mock,
                                                                   idrac_connection_mock_for_redfish_storage_controller,
                                                                   param):
        mocker.patch(
            MODULE_PATH + 'idrac_redfish_storage_controller.validate_inputs')
        mocker.patch(
            MODULE_PATH + 'idrac_redfish_storage_controller.check_raid_service')
        mocker.patch(
            MODULE_PATH + 'idrac_redfish_storage_controller.check_id_exists')
        mocker.patch(
            MODULE_PATH + 'idrac_redfish_storage_controller.check_volume_array_exists')
        mocker.patch(
            MODULE_PATH + 'idrac_redfish_storage_controller.check_encryption_capability')
        f_module = self.get_module_mock(params=param)
        redfish_response_mock.success = True
        redfish_response_mock.headers = {"Location": "Jobs/1234"}
        redfish_default_args.update(param)
        result = self._run_module(redfish_default_args)
        assert result["changed"] is True
        assert result['msg'] == "Successfully submitted the job that performs the {0} operation".format(
            param["command"])
        assert result["task"]["id"] == "1234"
        assert result["task"]["uri"] == "Jobs/1234"

    arg_list1 = [{"command": "ResetConfig", "controller_id": "c1"},
                 {"command": "RemoveControllerKey", "controller_id": "c1"},
                 {"command": "ReKey", "controller_id": "c1"},
                 {"command": "SetControllerKey", "controller_id": "c1", "key": "key", "key_id": "key_id"},
                 {"command": "AssignSpare", "target": "target"}]

    @pytest.mark.parametrize("param", arg_list1)
    def test_idrac_redfish_storage_controller_main_success_case_02(self,
                                                                   mocker,
                                                                   redfish_default_args,
                                                                   redfish_response_mock,
                                                                   idrac_connection_mock_for_redfish_storage_controller,
                                                                   param):
        mocker.patch(
            MODULE_PATH + 'idrac_redfish_storage_controller.validate_inputs')
        mocker.patch(
            MODULE_PATH + 'idrac_redfish_storage_controller.check_raid_service')
        mocker.patch(
            MODULE_PATH + 'idrac_redfish_storage_controller.check_id_exists')
        mocker.patch(
            MODULE_PATH + 'idrac_redfish_storage_controller.check_volume_array_exists')
        mocker.patch(
            MODULE_PATH + 'idrac_redfish_storage_controller.check_encryption_capability')
        f_module = self.get_module_mock(params=param)
        redfish_response_mock.success = True
        redfish_response_mock.headers = {"Location": "Jobs/1234"}
        redfish_default_args.update(param)
        result = self._run_module(redfish_default_args)
        assert result["changed"] is True
        assert result['msg'] == "Successfully submitted the job that performs the {0} operation".format(
            param["command"])
        assert result["task"]["id"] == "1234"
        assert result["task"]["uri"] == "Jobs/1234"

    @pytest.mark.parametrize("exc_type",
                             [RuntimeError, urllib_error.URLError, SSLValidationError, ConnectionError, KeyError,
                              ImportError,
                              ValueError, TypeError])
    def test_idrac_redfish_storage_controller_main_exception_case(self, exc_type, mocker,
                                                                  redfish_default_args,
                                                                  redfish_response_mock,
                                                                  idrac_connection_mock_for_redfish_storage_controller):
        mocker.patch(
            MODULE_PATH + 'idrac_redfish_storage_controller.check_encryption_capability',
            side_effect=exc_type('test'))
        mocker.patch(
            MODULE_PATH + 'idrac_redfish_storage_controller.check_raid_service',
            side_effect=exc_type('test'))
        mocker.patch(
            MODULE_PATH + 'idrac_redfish_storage_controller.check_id_exists',
            side_effect=exc_type('test'))
        mocker.patch(
            MODULE_PATH + 'idrac_redfish_storage_controller.check_volume_array_exists',
            side_effect=exc_type('test'))
        mocker.patch(
            MODULE_PATH + 'idrac_redfish_storage_controller.validate_inputs',
            side_effect=exc_type('test'))
        result = self._run_module_with_fail_json(redfish_default_args)
        assert 'power_state' not in result
        assert 'msg' in result
        assert result['failed'] is True

    arg_list1 = [{"command": "ResetConfig", "controller_id": "c1"},
                 {"command": "RemoveControllerKey", "controller_id": "c1"},
                 {"command": "ReKey", "controller_id": "c1"},
                 {"command": "SetControllerKey", "controller_id": "c1", "key": "key", "key_id": "key_id"},
                 {"command": "AssignSpare", "target": "target"}]

    @pytest.mark.parametrize("param", arg_list1)
    def test_idrac_redfish_main_HTTPError_case(self, param, idrac_connection_mock_for_redfish_storage_controller,
                                               redfish_default_args, mocker):
        redfish_default_args.update(param)
        json_str = to_text(json.dumps({"data": "out"}))
        mocker.patch(
            MODULE_PATH + 'idrac_redfish_storage_controller.check_raid_service',
            side_effect=HTTPError('http://testhost.com', 400, 'http error message',
                                  {"accept-type": "application/json"}, StringIO(json_str)))
        result = self._run_module_with_fail_json(redfish_default_args)
        assert 'msg' in result
        assert result['failed'] is True
