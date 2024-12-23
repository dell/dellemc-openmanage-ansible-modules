# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.0.0
# Copyright (C) 2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_user_info
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from unittest.mock import MagicMock
from ansible.module_utils._text import to_text
from io import StringIO

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
HTTPS_ADDRESS = 'https://testhost.com'


class TestIDRACUserInfo(FakeAnsibleModule):
    module = idrac_user_info

    @pytest.fixture
    def idrac_user_info_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_user_info_mock(self, mocker, idrac_user_info_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'idrac_user_info.iDRACRedfishAPI',
                                       return_value=idrac_user_info_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_user_info_mock
        return idrac_conn_mock

    def test_fetch_all_accounts_success_case(self, idrac_default_args, idrac_connection_user_info_mock,
                                             idrac_user_info_mock, mocker):
        obj = MagicMock()
        obj.json_data = {"Members": [
            {"UserName": "test", "Oem": {"Dell": "test"}}]}
        mocker.patch(MODULE_PATH + "idrac_user_info.iDRACRedfishAPI.invoke_request",
                     return_value=(obj))
        resp = self.module.fetch_all_accounts(idrac_connection_user_info_mock, "/acounts/accdetails")
        assert resp[0].get("UserName") == "test"

    def test_get_user_id_accounts(self, idrac_default_args, idrac_connection_user_info_mock,
                                  idrac_user_info_mock, mocker):
        json_str = to_text(json.dumps({"data": "out"}))
        idrac_default_args.update({"username": "test"})
        obj = MagicMock()
        obj.json_data = {"UserName": "test"}
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        mocker.patch(MODULE_PATH + "idrac_user_info.iDRACRedfishAPI.invoke_request",
                     return_value=(obj))
        mocker.patch(MODULE_PATH + "idrac_user_info.strip_substr_dict",
                     return_value=({"UserName": "test"}))
        resp = self.module.get_user_id_accounts(
            idrac_connection_user_info_mock, f_module, "/acounts/accdetails", 1)
        assert resp.get("UserName") == "test"

        obj = MagicMock()
        obj.json_data = {"UserName": "test", "Oem": {"Dell": "test"}}
        mocker.patch(MODULE_PATH + "idrac_user_info.iDRACRedfishAPI.invoke_request",
                     return_value=(obj))
        mocker.patch(MODULE_PATH + "idrac_user_info.strip_substr_dict",
                     return_value=({"UserName": "test", "Oem": {"Dell": "test"}}))
        resp = self.module.get_user_id_accounts(
            idrac_connection_user_info_mock, f_module, "/acounts/accdetails", 1)
        assert resp.get("UserName") == "test"

        idrac_connection_user_info_mock.invoke_request.side_effect = HTTPError(
            HTTPS_ADDRESS, 400,
            'http error message',
            {"accept-type": "application/json"},
            StringIO(json_str))
        with pytest.raises(Exception) as exc:
            self.module.get_user_id_accounts(
                idrac_connection_user_info_mock, f_module, "/acounts/accdetails", 1)
        assert exc.value.args[0] == "'user_id' is not valid."

    def test_get_user_name_accounts(self, idrac_default_args, idrac_connection_user_info_mock,
                                    idrac_user_info_mock, mocker):
        idrac_default_args.update({"username": "test"})
        mocker.patch(MODULE_PATH + "idrac_user_info.fetch_all_accounts",
                     return_value=([{"UserName": "test"}]))
        mocker.patch(MODULE_PATH + "idrac_user_info.strip_substr_dict",
                     return_value=({"UserName": "test"}))
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        resp = self.module.get_user_name_accounts(
            idrac_connection_user_info_mock, f_module, "/acounts/accdetails", "test")
        assert resp.get("UserName") == "test"

        mocker.patch(MODULE_PATH + "idrac_user_info.strip_substr_dict",
                     return_value=({"UserName": "test", "Oem": {"Dell": "test"}}))
        resp = self.module.get_user_name_accounts(
            idrac_connection_user_info_mock, f_module, "/acounts/accdetails", "test")
        assert resp.get("UserName") == "test"

        with pytest.raises(Exception) as exc:
            self.module.get_user_name_accounts(
                idrac_connection_user_info_mock, f_module, "/acounts/accdetails", "test1")
        assert exc.value.args[0] == "'username' is not valid."

    def test_get_all_accounts_single(self, idrac_default_args, idrac_connection_user_info_mock,
                                     idrac_user_info_mock, mocker):
        idrac_default_args.update({"username": "test"})
        mocker.patch(MODULE_PATH + "idrac_user_info.fetch_all_accounts",
                     return_value=([{"UserName": "test", "Oem": {"Dell": "test"}}]))
        mocker.patch(MODULE_PATH + "idrac_user_info.strip_substr_dict",
                     return_value=({"UserName": "test", "Oem": {"Dell": "test"}}))
        resp = self.module.get_all_accounts(
            idrac_connection_user_info_mock, "/acounts/accdetails")
        assert resp[0].get("UserName") == "test"

        mocker.patch(MODULE_PATH + "idrac_user_info.fetch_all_accounts",
                     return_value=([{"UserName": ""}]))
        resp = self.module.get_all_accounts(
            idrac_connection_user_info_mock, "/acounts/accdetails")
        assert resp == []

        mocker.patch(MODULE_PATH + "idrac_user_info.fetch_all_accounts",
                     return_value=([]))
        resp = self.module.get_all_accounts(
            idrac_connection_user_info_mock, "/acounts/accdetails")
        assert resp == []

    def test_get_all_accounts_multiple(self, idrac_default_args, idrac_connection_user_info_mock,
                                       idrac_user_info_mock, mocker):
        def strip_substr_dict_mock(acc):
            if acc.get("UserName") == "test":
                return {"UserName": "test"}
            else:
                return {"UserName": "test1"}
        mocker.side_effect = strip_substr_dict_mock

        mocker.patch(MODULE_PATH + "idrac_user_info.fetch_all_accounts",
                     return_value=([{"UserName": "test"}, {"UserName": "test1"}]))
        resp = self.module.get_all_accounts(
            idrac_connection_user_info_mock, "/acounts/accdetails")
        assert resp[0].get("UserName") == "test"
        assert resp[1].get("UserName") == "test1"

    def test_get_accounts_uri(self, idrac_default_args, idrac_connection_user_info_mock,
                              idrac_user_info_mock, mocker):
        acc_service_uri = MagicMock()
        acc_service_uri.json_data = {"AccountService": {
            "@odata.id": "/account"}, "Accounts": {"@odata.id": "/account/accountdetails"}}
        acc_service = MagicMock()
        acc_service.json_data = {"Accounts": {
            "@odata.id": "/account/accountdetails"}}

        mocker.patch(MODULE_PATH + "idrac_user_info.iDRACRedfishAPI.invoke_request",
                     return_value=(acc_service_uri))
        resp = self.module.get_accounts_uri(idrac_connection_user_info_mock)
        assert resp == "/account/accountdetails"

        json_str = to_text(json.dumps({"data": "out"}))
        idrac_connection_user_info_mock.invoke_request.side_effect = HTTPError(
            HTTPS_ADDRESS, 400,
            'http error message',
            {"accept-type": "application/json"},
            StringIO(json_str))

        resp = self.module.get_accounts_uri(idrac_connection_user_info_mock)
        assert resp == "/redfish/v1/AccountService/Accounts"

    def test_user_info_main_success_case_all(self, idrac_default_args, idrac_connection_user_info_mock,
                                             idrac_user_info_mock, mocker):
        idrac_default_args.update({"username": "test"})
        mocker.patch(MODULE_PATH + "idrac_user_info.get_accounts_uri",
                     return_value=("/acounts/accdetails"))
        mocker.patch(MODULE_PATH + "idrac_user_info.get_user_name_accounts",
                     return_value=({"UserName": "test"}))
        idrac_user_info_mock.status_code = 200
        idrac_user_info_mock.success = True
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == "Successfully retrieved the user information."
        assert resp['user_info'][0].get("UserName") == "test"

        mocker.patch(MODULE_PATH + "idrac_user_info.get_user_id_accounts",
                     return_value=({"UserName": "test"}))
        idrac_default_args.update({"user_id": "1234"})
        idrac_default_args.pop("username")
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == "Successfully retrieved the user information."
        assert resp['user_info'][0].get("UserName") == "test"

        mocker.patch(MODULE_PATH + "idrac_user_info.get_all_accounts",
                     return_value=([{"UserName": "test"}]))
        idrac_default_args.pop("user_id")
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == "Successfully retrieved the information of 1 user(s)."
        assert resp['user_info'][0].get("UserName") == "test"

        mocker.patch(MODULE_PATH + "idrac_user_info.get_all_accounts",
                     return_value=([]))
        resp = self._run_module_with_fail_json(idrac_default_args)
        assert resp['failed'] is True
        assert resp['msg'] == "Unable to retrieve the user information."

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_idrac_user_info_main_exception_handling_case(self, exc_type, mocker, idrac_default_args,
                                                          idrac_connection_user_info_mock, idrac_user_info_mock):
        idrac_user_info_mock.status_code = 400
        idrac_user_info_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + "idrac_user_info.get_accounts_uri",
                         side_effect=exc_type('test'))
        else:
            mocker.patch(MODULE_PATH + "idrac_user_info.get_accounts_uri",
                         side_effect=exc_type(HTTPS_ADDRESS, 400,
                                              'http error message',
                                              {"accept-type": "application/json"},
                                              StringIO(json_str)))
        if exc_type != URLError:
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result
