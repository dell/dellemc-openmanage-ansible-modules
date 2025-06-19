# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.2.0
# Copyright (C) 2020-2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_user
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from unittest.mock import MagicMock
from ansible.module_utils._text import to_text
from io import StringIO
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.utils \
    import AnsibleFailJson

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
VERSION = "3.60.60.60"
VERSION13G = "2.70.70.70"
HARDWARE_13G = 13
HARDWARE_14G = 14
SLOT_API = "/redfish/v1/Managers/iDRAC.Embedded.1/Accounts/{0}/"
CHANGES_FOUND = "Changes found to commit!"
SLEEP_PATH = 'idrac_user.time.sleep'
USERNAME2 = "Users.2#UserName"
GET_PAYLOAD = "idrac_user.get_payload"
PAYLOAD_XML = "idrac_user.convert_payload_xml"
XML_DATA = "<xml-data>"
USERNAME1 = "Users.1#UserName"
IMPORT_SCP = "idrac_user.iDRACRedfishAPI.import_scp"
USER2 = "User.2#UserName"
SUCCESS_CREATED = "Successfully created a request."
SUCCESS_MSG = "Successfully created user account."
SUCCESS_UPDATED = "Successfully updated user account."
INVOKE_REQUEST = "idrac_user.iDRACRedfishAPI.invoke_request"
CM_ACCOUNT = "idrac_user.create_or_modify_account"
USER_PRIVILAGE = "Users.1#Privilege"
MAX_USERS_MSG = "Maximum number of users reached. Delete a user \
account and retry the operation."


class TestIDRACUser(FakeAnsibleModule):
    module = idrac_user

    @pytest.fixture
    def idrac_user_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_user_mock(self, mocker, idrac_user_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'idrac_user.iDRACRedfishAPI',
                                       return_value=idrac_user_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_user_mock
        return idrac_conn_mock

    def test_get_payload(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "present", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        f_module = self.get_module_mock(params=idrac_default_args)
        resp = self.module.get_payload(f_module, 1, action="update")
        assert resp["Users.1.UserName"] == idrac_default_args["new_user_name"]

    def test_get_payload_2(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "present", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "custom_privilege": 17, "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        f_module = self.get_module_mock(params=idrac_default_args)
        resp = self.module.get_payload(f_module, 1)
        assert resp["Users.1.Privilege"] == idrac_default_args["custom_privilege"]

    def test_convert_payload_xml(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "present", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        payload = {"Users.1.UserName": idrac_default_args["user_name"],
                   "Users.1.Password": idrac_default_args["user_password"],
                   "Users.1.Enable": idrac_default_args["enable"],
                   "Users.1.Privilege": idrac_default_args["privilege"],
                   "Users.1.IpmiLanPrivilege": idrac_default_args["ipmi_lan_privilege"],
                   "Users.1.IpmiSerialPrivilege": idrac_default_args["ipmi_serial_privilege"],
                   "Users.1.SolEnable": idrac_default_args["sol_enable"],
                   "Users.1.ProtocolEnable": idrac_default_args["protocol_enable"],
                   "Users.1.AuthenticationProtocol": idrac_default_args["authentication_protocol"],
                   "Users.1.PrivacyProtocol": idrac_default_args["privacy_protocol"]}
        _xml, json_payload = self.module.convert_payload_xml(payload)
        assert json_payload["Users.1#SolEnable"] is True

    def test_remove_user_account_check_mode_1(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "absent", "user_name": "user_name", "new_user_name": None,
                                   "user_password": None, "privilege": None, "ipmi_lan_privilege": None,
                                   "ipmi_serial_privilege": None, "enable": False, "sol_enable": False,
                                   "protocol_enable": False, "authentication_protocol": "SHA",
                                   "privacy_protocol": "AES"})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        slot_id = 1
        slot_uri = SLOT_API.format(slot_id)
        with pytest.raises(Exception) as exc:
            self.module.remove_user_account(
                f_module, idrac_connection_user_mock, slot_uri, slot_id)
        assert exc.value.args[0] == CHANGES_FOUND

    def test_remove_user_account_check_mode_2(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "absent", "user_name": "user_name", "new_user_name": None,
                                   "user_password": None, "privilege": None, "ipmi_lan_privilege": None,
                                   "ipmi_serial_privilege": None, "enable": False, "sol_enable": False,
                                   "protocol_enable": False, "authentication_protocol": "SHA",
                                   "privacy_protocol": "AES"})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        with pytest.raises(Exception) as exc:
            self.module.remove_user_account(
                f_module, idrac_connection_user_mock, None, None)
        assert exc.value.args[0] == "No changes found to commit!"

    def test_remove_user_account_check_mode_3(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "absent", "user_name": "user_name", "new_user_name": None,
                                   "user_password": None, "privilege": None, "ipmi_lan_privilege": None,
                                   "ipmi_serial_privilege": None, "enable": False, "sol_enable": False,
                                   "protocol_enable": False, "authentication_protocol": "SHA",
                                   "privacy_protocol": "AES"})
        idrac_connection_user_mock.remove_user_account.return_value = {
            "success": True}
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        slot_id = 1
        slot_uri = SLOT_API.format(slot_id)
        mocker.patch(MODULE_PATH + SLEEP_PATH, return_value=None)
        self.module.remove_user_account(
            f_module, idrac_connection_user_mock, slot_uri, slot_id)

    def test_remove_user_account_check_mode_4(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "absent", "user_name": "user_name", "new_user_name": None,
                                   "user_password": None, "privilege": None, "ipmi_lan_privilege": None,
                                   "ipmi_serial_privilege": None, "enable": False, "sol_enable": False,
                                   "protocol_enable": False, "authentication_protocol": "SHA",
                                   "privacy_protocol": "AES"})
        idrac_connection_user_mock.remove_user_account.return_value = {
            "success": True}
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        with pytest.raises(Exception) as exc:
            self.module.remove_user_account(
                f_module, idrac_connection_user_mock, None, None)
        assert exc.value.args[0] == 'The user account is absent.'

    def test_get_user_account_1(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "present", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        mocker.patch(MODULE_PATH + "idrac_user.iDRACRedfishAPI.export_scp",
                     return_value=MagicMock())
        mocker.patch(MODULE_PATH + "idrac_user.iDRACRedfishAPI.get_idrac_local_account_attr",
                     return_value={USERNAME2: "test_user", "Users.3#UserName": ""})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        response = self.module.get_user_account(
            f_module, idrac_connection_user_mock)
        assert response[0][USERNAME2] == "test_user"
        assert response[3] == 3
        assert response[4] == "/redfish/v1/Managers/iDRAC.Embedded.1/Accounts/3"

    def test_get_user_account_2(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "present", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        mocker.patch(MODULE_PATH + "idrac_user.iDRACRedfishAPI.export_scp",
                     return_value=MagicMock())
        mocker.patch(MODULE_PATH + "idrac_user.iDRACRedfishAPI.get_idrac_local_account_attr",
                     return_value={USERNAME2: "test_user", "Users.3#UserName": "test"})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        response = self.module.get_user_account(
            f_module, idrac_connection_user_mock)
        assert response[2] == 3
        assert response[1] == "/redfish/v1/Managers/iDRAC.Embedded.1/Accounts/3"

    def test_get_user_account_invalid_name(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "present", "new_user_name": "new_user_name",
                                   "user_name": "", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        with pytest.raises(Exception) as err:
            self.module.get_user_account(f_module, idrac_connection_user_mock)
        assert err.value.args[0] == "User name is not valid."

    @pytest.mark.parametrize("params", [
        {"ret_val": SUCCESS_MSG, "empty_slot_id": 2,
            "empty_slot_uri": SLOT_API.format(2)},
        {"ret_val": SUCCESS_UPDATED, "slot_id": 2,
            "slot_uri": SLOT_API.format(2)},
        {"firm_ver": (14, VERSION, HARDWARE_14G), "ret_val": SUCCESS_MSG,
         "empty_slot_id": 2, "empty_slot_uri": SLOT_API.format(2)},
        {"firm_ver": (14, VERSION, HARDWARE_14G), "ret_val": SUCCESS_UPDATED,
         "slot_id": 2, "slot_uri": SLOT_API.format(2)},
        {"firm_ver": (14, VERSION, HARDWARE_14G), "ret_val": SUCCESS_UPDATED, "slot_id": 2, "slot_uri": SLOT_API.format(2),
         "empty_slot_id": 2, "empty_slot_uri": SLOT_API.format(2)},
    ])
    def test_create_or_modify_account(self, idrac_connection_user_mock, idrac_default_args, mocker, params):
        idrac_default_args.update({"state": "present", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idrac_connection_user_mock.get_server_generation = params.get(
            "firm_ver", (13, VERSION13G, HARDWARE_13G))
        mocker.patch(MODULE_PATH + GET_PAYLOAD,
                     return_value={USERNAME2: "test_user"})
        mocker.patch(MODULE_PATH + PAYLOAD_XML,
                     return_value=(XML_DATA, {USERNAME2: "test_user"}))
        mocker.patch(MODULE_PATH + IMPORT_SCP,
                     return_value={"Message": SUCCESS_CREATED})
        mocker.patch(MODULE_PATH + SLEEP_PATH, return_value=None)
        mocker.patch(MODULE_PATH + INVOKE_REQUEST,
                     return_value={"Message": SUCCESS_CREATED})

        empty_slot_id = params.get("empty_slot_id", None)
        empty_slot_uri = params.get("empty_slot_uri", None)
        slot_id = params.get("slot_id", None)
        slot_uri = params.get("slot_uri", None)
        user_attr = {USER2: "test_user"}

        response = self.module.create_or_modify_account(f_module, idrac_connection_user_mock, slot_uri, slot_id,
                                                        empty_slot_id, empty_slot_uri, user_attr)
        assert response[1] == params.get("ret_val")

    @pytest.mark.parametrize("params", [
        {"ret_val": "Requested changes are already present in the user slot."},
        {"firm_ver": (14, VERSION, HARDWARE_14G), "slot_id": None, "slot_uri": None,
         "ret_val": MAX_USERS_MSG},
        {"check_mode": True, "ret_val": "No changes found to commit!"},
        {"check_mode": True, "user_attr": {
            USERNAME1: "test_user"}, "ret_val": CHANGES_FOUND},
        {"check_mode": True, "user_attr": {USERNAME1: "test_user"}, "ret_val":
         CHANGES_FOUND, "empty_slot_id": 2, "empty_slot_uri": SLOT_API.format(2)},
    ])
    def test_create_or_modify_account_exception(self, idrac_connection_user_mock, idrac_default_args, mocker, params):
        idrac_default_args.update({"state": "present", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=params.get("check_mode", False))
        idrac_connection_user_mock.get_server_generation = params.get(
            "firm_ver", (13, VERSION13G, HARDWARE_13G))
        mocker.patch(MODULE_PATH + GET_PAYLOAD,
                     return_value={USERNAME2: "test_user"})
        mocker.patch(MODULE_PATH + PAYLOAD_XML,
                     return_value=(XML_DATA, {USERNAME2: "test_user"}))
        mocker.patch(MODULE_PATH + IMPORT_SCP,
                     return_value={"Message": SUCCESS_CREATED})
        mocker.patch(MODULE_PATH + INVOKE_REQUEST,
                     return_value={"Message": SUCCESS_CREATED})
        slot_id = params.get("slot_id", 2)
        slot_uri = params.get("slot_uri", SLOT_API.format(2))
        empty_slot_id = params.get("empty_slot_id", None)
        empty_slot_uri = params.get("empty_slot_uri", None)
        user_attr = params.get("user_attr", {USERNAME2: "test_user"})
        with pytest.raises(Exception) as exc:
            self.module.create_or_modify_account(f_module, idrac_connection_user_mock, slot_uri, slot_id,
                                                 empty_slot_id, empty_slot_uri, user_attr)
        assert exc.value.args[0] == params.get("ret_val")

    @pytest.mark.parametrize("exc_type", [SSLValidationError, URLError, ValueError, TypeError,
                                          ConnectionError, HTTPError, ImportError, RuntimeError])
    def test_main_execptions(self, exc_type, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "present", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + CM_ACCOUNT,
                         side_effect=exc_type('test'))
        else:
            mocker.patch(MODULE_PATH + CM_ACCOUNT,
                         side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
        if exc_type != URLError:
            result = self._run_module(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result

    def test_main_error(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "absent", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        obj = MagicMock()
        obj.json_data = {"error": {"message": "Some Error Occured"}}
        mocker.patch(MODULE_PATH + "idrac_user.remove_user_account",
                     return_value=(obj, "error"))
        result = self._run_module(idrac_default_args)
        assert result['failed'] is True
        assert result['msg'] == "Some Error Occured"

    def test_main_error_oem(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "absent", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        obj = MagicMock()
        obj.json_data = {"Oem": {"Dell": {
            "Message": "Unable to complete application of configuration profile values."}}}
        mocker.patch(MODULE_PATH + "idrac_user.remove_user_account",
                     return_value=(obj, "error"))
        result = self._run_module(idrac_default_args)
        assert result['failed'] is True
        assert result['msg'] == "Unable to complete application of configuration profile values."

    def test_main_create_oem(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "present", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        obj = MagicMock()
        obj.json_data = {
            "Oem": {"Dell": {"Message": "This Message Does Not Exists"}}}
        mocker.patch(MODULE_PATH + CM_ACCOUNT, return_value=(obj, "created"))
        # with pytest.raises(Exception) as exc:
        result = self._run_module(idrac_default_args)
        assert result['changed'] is True
        assert result['msg'] == "created"

    def test_main_state_some(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "some", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        try:
            self._run_module(idrac_default_args)
        except AnsibleFailJson as err:
            assert err.args[0]["msg"] == "value of state must be one of: present, absent, got: some"
            assert err.args[0].get('failed') is True

    def test_validate_input(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "present", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "custom_privilege": 512, "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        with pytest.raises(Exception) as err:
            self.module.validate_input(f_module)
        assert err.value.args[0] == "custom_privilege value should be from 0 to 511."

        idrac_default_args.update({"state": "absent"})
        ret = self.module.validate_input(f_module)
        assert ret is None

    def test_compare_payload(self, idrac_connection_user_mock, idrac_default_args, mocker):
        json_payload = {"Users.1#Password": "MyDummyPassword"}
        is_change_required = self.module.compare_payload(json_payload, None)
        assert is_change_required is True

        json_payload = {USER_PRIVILAGE: "123"}
        idrac_attr = {USER_PRIVILAGE: "123"}
        is_change_required = self.module.compare_payload(
            json_payload, idrac_attr)
        assert is_change_required is False

        json_payload = {USER_PRIVILAGE: "123"}
        idrac_attr = {USER_PRIVILAGE: "124"}
        is_change_required = self.module.compare_payload(
            json_payload, idrac_attr)
        assert is_change_required is True
