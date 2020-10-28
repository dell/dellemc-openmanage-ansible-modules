# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.3
# Copyright (C) 2019 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible_collections.dellemc.openmanage.plugins.modules import ome_firmware_catalog
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from io import StringIO
from ansible.module_utils._text import to_text
from ansible.module_utils.urls import ConnectionError, SSLValidationError
import json
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


@pytest.fixture
def ome_connection_catalog_mock(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'ome_firmware_catalog.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeFirmwareCatalog(FakeAnsibleModule):
    module = ome_firmware_catalog

    @pytest.fixture
    def mock__get_catalog_payload(self, mocker):
        mock_payload = mocker.patch(
            MODULE_PATH + 'ome_firmware_catalog._get_catalog_payload',
            return_value={"Repistory": "Dummy val"})
        return mock_payload

    def test_main_ome_firmware_catalog_success_case1(self, ome_default_args, mock__get_catalog_payload,
                                                     ome_connection_catalog_mock, module_mock, ome_response_mock):
        ome_default_args.update({"catalog_name": "catalog_name"})
        ome_response_mock.json_data = {"data": "dummy data", "TaskId": 1234}
        ome_response_mock.status_code = 200
        result = self._run_module(ome_default_args)
        assert result['changed'] is True
        assert 'catalog_status' in result and "msg" in result
        assert result["msg"] == "Successfully triggered the job to create a catalog with Task Id : 1234"

    def test_main_ome_firmware_catalog_failure_case1(self, ome_default_args, mock__get_catalog_payload,
                                                     ome_connection_catalog_mock, module_mock, ome_response_mock):
        ome_default_args.update({"catalog_name": "catalog_name"})
        ome_response_mock.status_code = 500
        ome_response_mock.success = False
        result = self._run_module_with_fail_json(ome_default_args)
        assert 'catalog_status' not in result
        assert 'msg' in result
        assert result['failed'] is True
        assert result["msg"] == "Failed to trigger the job to create catalog."

    def test_main_ome_firmware_catalog_no_mandatory_arg_passed_failuer_case(self, ome_default_args, module_mock,
                                                                            mock__get_catalog_payload,
                                                                            ome_connection_catalog_mock):
        result = self._run_module_with_fail_json(ome_default_args)
        assert 'catalog_status' not in result

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_main_catalog_httperror_case(self, exc_type, ome_default_args, mock__get_catalog_payload,
                                         ome_connection_catalog_mock, ome_response_mock):
        ome_default_args.update({"catalog_name": "catalog_name"})
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            ome_connection_catalog_mock.invoke_request.side_effect = exc_type("exception message")
        else:
            ome_connection_catalog_mock.invoke_request.side_effect = exc_type('http://testhost.com', 400,
                                                                              'http error message',
                                                                              {"accept-type": "application/json"},
                                                                              StringIO(json_str))
        ome_response_mock.status_code = 400
        result = self._run_module_with_fail_json(ome_default_args)
        assert 'catalog_status' not in result
        assert 'msg' in result
        assert result['failed'] is True
        if exc_type == HTTPError:
            assert 'error_info' in result

    inp_param1 = {"hostname": "host ip", "username": "username",
                  "password": "password", "port": 443, "catalog_name": "catalog_name"}
    inp_param2 = {"hostname": "host ip", "username": "username",
                  "password": "password", "port": 443, "catalog_name": "catalog_name", "catalog_description": "desc",
                  "source": "10.255.2.128:2607", "source_path": "source_path", "file_name": "file_name",
                  "repository_type": "HTTPS",
                  "repository_username": "repository_username",
                  "repository_password": "repository_password",
                  "repository_domain": "repository_domain",
                  "check_certificate": True}
    inp_param3 = {"hostname": "host ip", "username": "username",
                  "password": "password", "port": 443, "catalog_name": " ", "catalog_description": None}
    out1 = {"Repository": {"Name": "catalog_name"}}
    out2 = {'Filename': 'file_name', 'SourcePath': 'source_path',
            'Repository': {'Name': 'catalog_name', 'Description': 'desc',
                           'Source': '10.255.2.128:2607', 'RepositoryType': 'HTTPS', 'Username': 'repository_username',
                           'Password': 'repository_password', 'DomainName': 'repository_domain',
                           'CheckCertificate': True}}

    out3 = {"Repository": {"Name": " "}}

    @pytest.mark.parametrize("params", [{"inp": inp_param1, "out": out1},
                                        {"inp": inp_param2, "out": out2},
                                        {"inp": inp_param3, "out": out3}
                                        ])
    def test__get_catalog_payload_success_case(self, params):
        payload = self.module._get_catalog_payload(params["inp"])
        assert payload == params["out"]
