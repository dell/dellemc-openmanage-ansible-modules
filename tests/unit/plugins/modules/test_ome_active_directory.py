# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 4.0.0
# Copyright (C) 2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
from io import StringIO
from ssl import SSLError

import pytest
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import ome_active_directory
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

AD_URI = "AccountService/ExternalAccountProvider/ADAccountProvider"
TEST_CONNECTION = "AccountService/ExternalAccountProvider/Actions/ExternalAccountProvider.TestADConnection"
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."
MAX_AD_MSG = "Unable to add the account provider because the maximum number of configurations allowed for an" \
             " Active Directory service is {0}."
CREATE_SUCCESS = "Successfully added the Active Directory service."
MODIFY_SUCCESS = "Successfully modified the Active Directory service."
DELETE_SUCCESS = "Successfully deleted the Active Directory service."
DOM_SERVER_MSG = "Specify the domain server. Domain server is required to create an Active Directory service."
GRP_DOM_MSG = "Specify the group domain. Group domain is required to create an Active Directory service."
CERT_INVALID = "The provided certificate file path is invalid or not readable."
DOMAIN_ALLOWED_COUNT = "Maximum entries allowed for {0} lookup type is {1}."
TEST_CONNECTION_SUCCESS = "Test Connection is successful. "
TEST_CONNECTION_FAIL = "Test Connection has failed. "
ERR_READ_FAIL = "Unable to retrieve the error details."
INVALID_ID = "The provided Active Directory ID is invalid."
TIMEOUT_RANGE = "The {0} value is not in the range of {1} to {2}."
MAX_AD = 2
MIN_TIMEOUT = 15
MAX_TIMEOUT = 300

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_active_directory.'
MODULE_UTIL_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.ome.'


@pytest.fixture
def ome_connection_mock_for_ad(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeAD(FakeAnsibleModule):
    module = ome_active_directory

    @pytest.mark.parametrize("params", [
        {"module_args": {"name": "domdev"}, "json_data": {"value": [{'Name': 'domdev', 'Id': 12}]},
         "ad": {'Name': 'domdev', 'Id': 12}, "ad_cnt": 1},
        {"module_args": {"id": 12}, "json_data": {"value": [{'Name': 'domdev', 'Id': 12}]},
         "ad": {'Name': 'domdev', 'Id': 12}, "ad_cnt": 1},
        {"module_args": {"id": 11}, "json_data": {"value": [
            {'Name': 'domdev', 'Id': 12}, {'Name': 'domdev', 'Id': 13}]}, "ad": {}, "ad_cnt": 2}])
    def test_get_ad(self, params, ome_connection_mock_for_ad, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        f_module = self.get_module_mock(params=params['module_args'])
        ome_response_mock.json_data = params["json_data"]
        ad, ad_cnt = self.module.get_ad(f_module, ome_connection_mock_for_ad)
        assert ad == params['ad']
        assert ad_cnt == params['ad_cnt']

    @pytest.mark.parametrize("params", [{
        "module_args": {"domain_controller_lookup": "MANUAL", "domain_server": ["192.96.20.181"],
                        "group_domain": "domain.com", "name": "domdev"}, "msg": CREATE_SUCCESS}, {
        "module_args": {"domain_controller_lookup": "MANUAL", "domain_server": ["192.96.20.181"],
                        "group_domain": "domain.com", "name": "domdev"}, "msg": CHANGES_FOUND, "check_mode": True}, {
        "module_args": {"domain_controller_lookup": "MANUAL", "domain_server": ["192.96.20.181"],
                        "group_domain": "domain.com", "name": "domdev", "test_connection": True,
                        "domain_username": "user", "domain_password": "passwd"},
        "msg": "{0}{1}".format(TEST_CONNECTION_SUCCESS, CREATE_SUCCESS)}
    ])
    def test_ome_active_directory_create_success(self, params, ome_connection_mock_for_ad, ome_response_mock,
                                                 ome_default_args, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = {"Name": "AD1"}
        mocker.patch(MODULE_PATH + 'get_ad', return_value=params.get("get_ad", (None, 1)))
        ome_default_args.update(params['module_args'])
        result = self._run_module(ome_default_args, check_mode=params.get('check_mode', False))
        assert result['msg'] == params['msg']

    @pytest.mark.parametrize("params", [{
        "module_args": {"domain_controller_lookup": "MANUAL", "domain_server": ["192.96.20.181"],
                        "group_domain": "domain.com", "name": "domdev"},
        "get_ad": ({"Name": "ad_test", "Id": 21789, "ServerType": "MANUAL", "ServerName": ["192.168.20.181"],
                    "DnsServer": [], "GroupDomain": "dellemcdomain.com", "NetworkTimeOut": 120, "SearchTimeOut": 120,
                    "ServerPort": 3269, "CertificateValidation": False}, 1),
        "msg": MODIFY_SUCCESS}, {
        "module_args": {"domain_controller_lookup": "MANUAL", "domain_server": ["192.96.20.181"],
                        "group_domain": "domain.com", "name": "domdev", "test_connection": True,
                        "domain_username": "user", "domain_password": "passwd"}, "get_ad":
            ({"Name": "ad_test", "Id": 21789, "ServerType": "MANUAL", "ServerName": ["192.168.20.181"], "DnsServer": [],
              "GroupDomain": "dellemcdomain.com", "NetworkTimeOut": 120, "SearchTimeOut": 120, "ServerPort": 3269,
              "CertificateValidation": False}, 1),
        "msg": "{0}{1}".format(TEST_CONNECTION_SUCCESS, MODIFY_SUCCESS)},
        {"module_args": {"domain_controller_lookup": "MANUAL", "domain_server": ["192.96.20.181"],
                         "group_domain": "dellemcdomain.com", "name": "domdev"},
         "get_ad": ({"Name": "domdev", "Id": 21789, "ServerType": "MANUAL", "ServerName": ["192.96.20.181"],
                     "DnsServer": [], "GroupDomain": "dellemcdomain.com", "NetworkTimeOut": 120, "SearchTimeOut": 120,
                     "ServerPort": 3269, "CertificateValidation": False}, 1),
         "msg": NO_CHANGES_MSG}, {
            "module_args": {"domain_controller_lookup": "MANUAL", "domain_server": ["192.96.20.181"],
                            "group_domain": "dellemcdomain.com", "name": "domdev"},
            "get_ad": ({"Name": "domdev", "Id": 21789, "ServerType": "MANUAL", "ServerName": ["192.168.20.181"],
                        "DnsServer": [], "GroupDomain": "dellemcdomain.com", "NetworkTimeOut": 120,
                        "SearchTimeOut": 120, "ServerPort": 3269, "CertificateValidation": False}, 1),
            "msg": CHANGES_FOUND, "check_mode": True}
    ])
    def test_ome_active_directory_modify_success(self, params, ome_connection_mock_for_ad, ome_response_mock,
                                                 ome_default_args, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = {"Name": "AD1"}
        ome_connection_mock_for_ad.strip_substr_dict.return_value = params.get("get_ad", (None, 1))[0]
        mocker.patch(MODULE_PATH + 'get_ad', return_value=params.get("get_ad", (None, 1)))
        ome_default_args.update(params['module_args'])
        result = self._run_module(ome_default_args, check_mode=params.get('check_mode', False))
        assert result['msg'] == params['msg']

    @pytest.mark.parametrize("params", [{
        "module_args": {"domain_controller_lookup": "MANUAL", "domain_server": ["192.96.20.181"],
                        "group_domain": "domain.com", "name": "domdev", "state": "absent"},
        "get_ad": ({"Name": "domdev", "Id": 21789, "ServerType": "MANUAL", "ServerName": ["192.168.20.181"],
                    "DnsServer": [], "GroupDomain": "dellemcdomain.com", "NetworkTimeOut": 120, "SearchTimeOut": 120,
                    "ServerPort": 3269, "CertificateValidation": False}, 1),
        "msg": DELETE_SUCCESS},
        {"module_args": {"domain_controller_lookup": "MANUAL", "domain_server": ["192.96.20.181"],
                         "group_domain": "dellemcdomain.com", "name": "domdev1", "state": "absent"},
         "msg": NO_CHANGES_MSG}, {
            "module_args": {"domain_controller_lookup": "MANUAL", "domain_server": ["192.96.20.181"],
                            "group_domain": "dellemcdomain.com", "name": "domdev", "state": "absent"},
            "get_ad": ({"Name": "domdev", "Id": 21789, "ServerType": "MANUAL", "ServerName": ["192.168.20.181"],
                        "DnsServer": [], "GroupDomain": "dellemcdomain.com", "NetworkTimeOut": 120,
                        "SearchTimeOut": 120, "ServerPort": 3269, "CertificateValidation": False}, 1),
            "msg": CHANGES_FOUND, "check_mode": True}
    ])
    def test_ome_active_directory_delete_success(self, params, ome_connection_mock_for_ad, ome_response_mock,
                                                 ome_default_args, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = {"Name": "AD1"}
        ome_connection_mock_for_ad.strip_substr_dict.return_value = params.get("get_ad", (None, 1))[0]
        mocker.patch(MODULE_PATH + 'get_ad', return_value=params.get("get_ad", (None, 1)))
        ome_default_args.update(params['module_args'])
        result = self._run_module(ome_default_args, check_mode=params.get('check_mode', False))
        assert result['msg'] == params['msg']

    @pytest.mark.parametrize("params", [
        {"module_args": {"domain_controller_lookup": "MANUAL", "group_domain": "domain.com", "name": "domdev"},
         "msg": DOM_SERVER_MSG}, {"module_args": {"domain_controller_lookup": "MANUAL",
                                                  "domain_server": ["192.96.20.181", "192.96.20.182", "192.96.20.183",
                                                                    "192.96.20.184"], "group_domain": "domain.com",
                                                  "name": "domdev"}, "msg": DOMAIN_ALLOWED_COUNT.format("MANUAL", 3)},
        {"module_args": {"domain_server": ["dom1.com1", "dom2.com"], "group_domain": "domain.com", "name": "domdev"},
         "msg": DOMAIN_ALLOWED_COUNT.format("DNS", 1)},
        {"module_args": {"domain_controller_lookup": "MANUAL", "domain_server": ["192.96.20.181"], "name": "domdev"},
         "msg": GRP_DOM_MSG}, {"module_args": {"domain_controller_lookup": "MANUAL", "domain_server": ["192.96.20.181"],
                                               "group_domain": "domain.com", "name": "domdev", "network_timeout": 1},
                               "msg": TIMEOUT_RANGE.format("NetworkTimeOut", MIN_TIMEOUT, MAX_TIMEOUT)}, {
            "module_args": {"domain_controller_lookup": "MANUAL", "domain_server": ["192.96.20.181"],
                            "group_domain": "domain.com", "name": "domdev", "search_timeout": 301},
            "msg": TIMEOUT_RANGE.format("SearchTimeOut", MIN_TIMEOUT, MAX_TIMEOUT)}, {
            "module_args": {"domain_controller_lookup": "MANUAL", "domain_server": ["192.96.20.181"],
                            "group_domain": "domain.com", "name": "domdev"}, "ad_cnt": 2,
            "msg": MAX_AD_MSG.format(MAX_AD)}, {
            "module_args": {"domain_controller_lookup": "MANUAL", "domain_server": ["192.96.20.181"],
                            "group_domain": "domain.com", "name": "domdev", "validate_certificate": True,
                            "certificate_file": "nonexistingcert.crt"}, "msg": CERT_INVALID}, {
            "module_args": {"domain_controller_lookup": "MANUAL", "domain_server": ["192.96.20.181"],
                            "group_domain": "domain.com", "id": 1234, "validate_certificate": True,
                            "certificate_file": "nonexistingcert.crt"}, "msg": INVALID_ID}
    ])
    def test_ome_active_directory_create_fails(self, params, ome_connection_mock_for_ad, ome_response_mock,
                                               ome_default_args, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = {"Name": "AD1"}
        mocker.patch(MODULE_PATH + 'get_ad', return_value=(None, params.get("ad_cnt", 1)))
        ome_default_args.update(params['module_args'])
        result = self._run_module_with_fail_json(ome_default_args)
        assert result['msg'] == params['msg']

    @pytest.mark.parametrize("params", [{
        "module_args": {"domain_controller_lookup": "MANUAL", "domain_server": ["192.96.20.181"],
                        "group_domain": "testconnectionfail.com", "name": "domdev", "test_connection": True,
                        "domain_username": "user", "domain_password": "passwd"},
        "msg": "{0}{1}".format(TEST_CONNECTION_FAIL, "Unable to connect to the LDAP or AD server."), "is_http": True,
        "error_info": {
            "error": {"@Message.ExtendedInfo": [{"Message": "Unable to connect to the LDAP or AD server."}], }}}, {
        "module_args": {"domain_controller_lookup": "MANUAL", "domain_server": ["192.96.20.181"],
                        "group_domain": "testconnectionfail.com", "name": "domdev", "test_connection": True,
                        "domain_username": "user", "domain_password": "passwd"},
        "msg": "{0}{1}".format(TEST_CONNECTION_FAIL, ERR_READ_FAIL), "is_http": True, "error_info": {
            "error1": {"@Message.ExtendedInfo": [{"Message": "Unable to connect to the LDAP or AD server."}], }}}, {
        "module_args": {"domain_controller_lookup": "MANUAL", "domain_server": ["192.96.20.181"],
                        "group_domain": "testconnectionfail.com", "name": "domdev", "test_connection": True,
                        "domain_username": "user", "domain_password": "passwd"},
        "msg": "{0}{1}".format(TEST_CONNECTION_FAIL, "Exception occurrence success."),
        "error_info": "Exception occurrence success."}, ])
    def test_ome_active_directory_create_test_conenction_fail(self, params, ome_default_args, mocker):
        mocker.patch(MODULE_PATH + 'get_ad', return_value=(None, params.get("ad_cnt", 1)))
        rest_obj_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
        ome_connection_mock_obj = rest_obj_class_mock.return_value.__enter__.return_value
        if params.get("is_http"):
            json_str = to_text(json.dumps(params['error_info']))
            ome_connection_mock_obj.invoke_request.side_effect = HTTPError('http://testdellemcomead.com', 404,
                                                                           'http error message',
                                                                           {"accept-type": "application/json"},
                                                                           StringIO(json_str))
        else:
            ome_connection_mock_obj.invoke_request.side_effect = Exception(params['error_info'])
        ome_default_args.update(params['module_args'])
        result = self._run_module_with_fail_json(ome_default_args)
        assert result['msg'] == params['msg']

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_active_directory_main_exception_failure_case(self, exc_type, mocker, ome_default_args,
                                                              ome_connection_mock_for_ad, ome_response_mock):
        ome_default_args.update({"state": "absent", "name": "t1"})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'get_ad', side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'get_ad', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'get_ad', side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                                                      {"accept-type": "application/json"},
                                                                      StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result
