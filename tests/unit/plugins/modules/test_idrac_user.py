# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.2
# Copyright (C) 2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_user
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible_collections.dellemc.openmanage.tests.unit.compat.mock import MagicMock, patch, Mock
from ansible.module_utils._text import to_text
from io import StringIO

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


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
        xml_payload, json_payload = self.module.convert_payload_xml(payload)
        assert json_payload["Users.1#SolEnable"] is True

    def test_remove_user_account_check_mode_1(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "absent", "user_name": "user_name", "new_user_name": None,
                                   "user_password": None, "privilege": None, "ipmi_lan_privilege": None,
                                   "ipmi_serial_privilege": None, "enable": False, "sol_enable": False,
                                   "protocol_enable": False, "authentication_protocol": "SHA",
                                   "privacy_protocol": "AES"})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        slot_id = 1
        slot_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/Accounts/{0}/".format(slot_id)
        with pytest.raises(Exception) as exc:
            self.module.remove_user_account(f_module, idrac_connection_user_mock, slot_uri, slot_id)
        assert exc.value.args[0] == "Changes found to commit!"

    def test_remove_user_account_check_mode_2(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "absent", "user_name": "user_name", "new_user_name": None,
                                   "user_password": None, "privilege": None, "ipmi_lan_privilege": None,
                                   "ipmi_serial_privilege": None, "enable": False, "sol_enable": False,
                                   "protocol_enable": False, "authentication_protocol": "SHA",
                                   "privacy_protocol": "AES"})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        with pytest.raises(Exception) as exc:
            self.module.remove_user_account(f_module, idrac_connection_user_mock, None, None)
        assert exc.value.args[0] == "No changes found to commit!"

    def test_remove_user_account_check_mode_3(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "absent", "user_name": "user_name", "new_user_name": None,
                                   "user_password": None, "privilege": None, "ipmi_lan_privilege": None,
                                   "ipmi_serial_privilege": None, "enable": False, "sol_enable": False,
                                   "protocol_enable": False, "authentication_protocol": "SHA",
                                   "privacy_protocol": "AES"})
        idrac_connection_user_mock.remove_user_account.return_value = {"success": True}
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        slot_id = 1
        slot_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/Accounts/{0}/".format(slot_id)
        mocker.patch(MODULE_PATH + 'idrac_user.time.sleep', return_value=None)
        self.module.remove_user_account(f_module, idrac_connection_user_mock, slot_uri, slot_id)

    def test_remove_user_account_check_mode_4(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "absent", "user_name": "user_name", "new_user_name": None,
                                   "user_password": None, "privilege": None, "ipmi_lan_privilege": None,
                                   "ipmi_serial_privilege": None, "enable": False, "sol_enable": False,
                                   "protocol_enable": False, "authentication_protocol": "SHA",
                                   "privacy_protocol": "AES"})
        idrac_connection_user_mock.remove_user_account.return_value = {"success": True}
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        with pytest.raises(Exception) as exc:
            self.module.remove_user_account(f_module, idrac_connection_user_mock, None, None)
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
                     return_value={"Users.2#UserName": "test_user", "Users.3#UserName": ""})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        response = self.module.get_user_account(f_module, idrac_connection_user_mock)
        assert response[0]["Users.2#UserName"] == "test_user"
        assert response[3] == 3

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
                     return_value={"Users.2#UserName": "test_user", "Users.3#UserName": ""})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        response = self.module.get_user_account(f_module, idrac_connection_user_mock)
        assert response[3] == 3
        assert response[4] == "/redfish/v1/Managers/iDRAC.Embedded.1/Accounts/3"

    def test_create_or_modify_account_1(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "present", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idrac_connection_user_mock.get_server_generation = (13, "2.70.70.70")
        mocker.patch(MODULE_PATH + "idrac_user.get_payload", return_value={"Users.2#UserName": "test_user"})
        mocker.patch(MODULE_PATH + "idrac_user.convert_payload_xml",
                     return_value=("<xml-data>", {"Users.1#UserName": "test_user"}))
        mocker.patch(MODULE_PATH + "idrac_user.iDRACRedfishAPI.import_scp",
                     return_value={"Message": "Successfully created a request."})
        empty_slot_id = 2
        empty_slot_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/Accounts/{0}/".format(empty_slot_id)
        user_attr = {"User.2#UserName": "test_user"}
        mocker.patch(MODULE_PATH + 'idrac_user.time.sleep', return_value=None)
        response = self.module.create_or_modify_account(f_module, idrac_connection_user_mock, None, None,
                                                        empty_slot_id, empty_slot_uri, user_attr)
        assert response[1] == "Successfully created user account."

    def test_create_or_modify_account_2(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "present", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idrac_connection_user_mock.get_server_generation = (13, "2.70.70.70")
        mocker.patch(MODULE_PATH + 'idrac_user.time.sleep', return_value=None)
        mocker.patch(MODULE_PATH + "idrac_user.get_payload", return_value={"Users.2#UserName": "test_user"})
        mocker.patch(MODULE_PATH + "idrac_user.convert_payload_xml",
                     return_value=("<xml-data>", {"Users.1#UserName": "test_user"}))
        mocker.patch(MODULE_PATH + "idrac_user.iDRACRedfishAPI.import_scp",
                     return_value={"Message": "Successfully created a request."})
        slot_id = 2
        slot_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/Accounts/{0}/".format(slot_id)
        user_attr = {"User.2#UserName": "test_user"}
        response = self.module.create_or_modify_account(f_module, idrac_connection_user_mock, slot_uri, slot_id,
                                                        None, None, user_attr)
        assert response[1] == "Successfully updated user account."

    def test_create_or_modify_account_3(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "present", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idrac_connection_user_mock.get_server_generation = (13, "2.70.70.70")
        mocker.patch(MODULE_PATH + "idrac_user.get_payload", return_value={"Users.2#UserName": "test_user"})
        mocker.patch(MODULE_PATH + "idrac_user.convert_payload_xml",
                     return_value=("<xml-data>", {"Users.1#UserName": "test_user"}))
        mocker.patch(MODULE_PATH + "idrac_user.iDRACRedfishAPI.import_scp",
                     return_value={"Message": "Successfully created a request."})
        slot_id = 2
        slot_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/Accounts/{0}/".format(slot_id)
        user_attr = {"Users.1#UserName": "test_user"}
        with pytest.raises(Exception) as exc:
            self.module.create_or_modify_account(f_module, idrac_connection_user_mock, slot_uri, slot_id,
                                                 None, None, user_attr)
        assert exc.value.args[0] == "Requested changes are already present in the user slot."

    def test_create_or_modify_account_4(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "present", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        idrac_connection_user_mock.get_server_generation = (13, "2.70.70.70")
        mocker.patch(MODULE_PATH + "idrac_user.get_payload", return_value={"Users.2#UserName": "test_user"})
        mocker.patch(MODULE_PATH + "idrac_user.convert_payload_xml",
                     return_value=("<xml-data>", {"Users.1#UserName": "test_user"}))
        mocker.patch(MODULE_PATH + "idrac_user.iDRACRedfishAPI.import_scp",
                     return_value={"Message": "Successfully created a request."})
        slot_id = 2
        slot_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/Accounts/{0}/".format(slot_id)
        user_attr = {"Users.1#UserName": "test_user"}
        with pytest.raises(Exception) as exc:
            self.module.create_or_modify_account(f_module, idrac_connection_user_mock, slot_uri, slot_id,
                                                 None, None, user_attr)
        assert exc.value.args[0] == "No changes found to commit!"

    def test_create_or_modify_account_5(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "present", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        idrac_connection_user_mock.get_server_generation = (13, "2.70.70.70")
        mocker.patch(MODULE_PATH + "idrac_user.get_payload", return_value={"Users.2#UserName": "test_user"})
        mocker.patch(MODULE_PATH + "idrac_user.convert_payload_xml",
                     return_value=("<xml-data>", {"Users.2#UserName": "test_user"}))
        mocker.patch(MODULE_PATH + "idrac_user.iDRACRedfishAPI.import_scp",
                     return_value={"Message": "Successfully created a request."})
        slot_id = 2
        slot_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/Accounts/{0}/".format(slot_id)
        user_attr = {"Users.1#UserName": "test_user"}
        with pytest.raises(Exception) as exc:
            self.module.create_or_modify_account(f_module, idrac_connection_user_mock, slot_uri, slot_id,
                                                 None, None, user_attr)
        assert exc.value.args[0] == "Changes found to commit!"

    def test_create_or_modify_account_6(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "present", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idrac_connection_user_mock.get_server_generation = (14, "3.60.60.60")
        mocker.patch(MODULE_PATH + "idrac_user.get_payload", return_value={"Users.2#UserName": "test_user"})
        mocker.patch(MODULE_PATH + "idrac_user.convert_payload_xml",
                     return_value=("<xml-data>", {"Users.1#UserName": "test_user"}))
        mocker.patch(MODULE_PATH + "idrac_user.iDRACRedfishAPI.invoke_request",
                     return_value={"Message": "Successfully created a request."})
        slot_id = 2
        slot_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/Accounts/{0}/".format(slot_id)
        user_attr = {"User.2#UserName": "test_user"}
        response = self.module.create_or_modify_account(f_module, idrac_connection_user_mock, None, None,
                                                        slot_id, slot_uri, user_attr)
        assert response[1] == "Successfully created user account."

    def test_create_or_modify_account_7(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "present", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        idrac_connection_user_mock.get_server_generation = (14, "3.60.60.60")
        mocker.patch(MODULE_PATH + "idrac_user.get_payload", return_value={"Users.2#UserName": "test_user"})
        mocker.patch(MODULE_PATH + "idrac_user.convert_payload_xml",
                     return_value=("<xml-data>", {"Users.1#UserName": "test_user"}))
        mocker.patch(MODULE_PATH + "idrac_user.iDRACRedfishAPI.invoke_request",
                     return_value={"Message": "Successfully created a request."})
        slot_id = 2
        slot_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/Accounts/{0}/".format(slot_id)
        user_attr = {"User.2#UserName": "test_user"}
        with pytest.raises(Exception) as exc:
            self.module.create_or_modify_account(f_module, idrac_connection_user_mock, None, None,
                                                 slot_id, slot_uri, user_attr)
        assert exc.value.args[0] == "Changes found to commit!"

    def test_create_or_modify_account_8(self, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "present", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idrac_connection_user_mock.get_server_generation = (14, "3.60.60.60")
        mocker.patch(MODULE_PATH + "idrac_user.get_payload", return_value={"Users.2#UserName": "test_user"})
        mocker.patch(MODULE_PATH + "idrac_user.convert_payload_xml",
                     return_value=("<xml-data>", {"Users.1#UserName": "test_user"}))
        mocker.patch(MODULE_PATH + "idrac_user.iDRACRedfishAPI.invoke_request",
                     return_value={"Message": "Successfully created a request."})
        slot_id = 2
        slot_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/Accounts/{0}/".format(slot_id)
        user_attr = {"User.2#UserName": "test_user"}
        response = self.module.create_or_modify_account(f_module, idrac_connection_user_mock, slot_uri, slot_id,
                                                        None, None, user_attr)
        assert response[1] == "Successfully updated user account."

    @pytest.mark.parametrize("exc_type", [SSLValidationError, URLError, ValueError, TypeError,
                                          ConnectionError, HTTPError, ImportError, RuntimeError])
    def test_main(self, exc_type, idrac_connection_user_mock, idrac_default_args, mocker):
        idrac_default_args.update({"state": "present", "new_user_name": "new_user_name",
                                   "user_name": "test", "user_password": "password",
                                   "privilege": "Administrator", "ipmi_lan_privilege": "Administrator",
                                   "ipmi_serial_privilege": "Administrator", "enable": True,
                                   "sol_enable": True, "protocol_enable": True,
                                   "authentication_protocol": "SHA", "privacy_protocol": "AES"})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + "idrac_user.create_or_modify_account",
                         side_effect=exc_type('test'))
        else:
            mocker.patch(MODULE_PATH + "idrac_user.create_or_modify_account",
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
        if not exc_type == URLError:
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result
