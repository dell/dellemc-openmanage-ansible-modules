# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.9.0
# Copyright (C) 2026 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

import json
import pytest
from io import StringIO
from ansible.module_utils._text import to_text
from urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_storage_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_storage_info.'
CONTROLLER_ID_REQUIRED_MSG = "controller_id is required when resource_type is '{resource_type}'."
SUCCESS_MSG = "Successfully fetched the storage information."


class TestStorageInfo(FakeAnsibleModule):
    module = idrac_storage_info

    @pytest.fixture
    def idrac_storage_info_mock(self, mocker):
        idrac_obj = mocker.MagicMock()
        idrac_obj.get_server_generation = (17, "7.10.90.00", "iDRAC 9")
        return idrac_obj

    @pytest.fixture
    def idrac_connection_storage_info_mock(self, mocker, idrac_storage_info_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                        return_value=idrac_storage_info_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_storage_info_mock
        return idrac_conn_mock

    def test_main_controller_resource_type_success(self, idrac_connection_storage_info_mock, idrac_default_args):
        idrac_default_args.update({"resource_type": "controller"})
        result = self._run_module(idrac_default_args)
        assert result["msg"] == SUCCESS_MSG
        assert result["storage_info"] == {"resource_count": 0, "resources": []}

    def test_main_physical_disk_missing_controller_id(self, idrac_connection_storage_info_mock, idrac_default_args):
        idrac_default_args.update({"resource_type": "physical_disk"})
        result = self._run_module(idrac_default_args)
        assert result["msg"] == CONTROLLER_ID_REQUIRED_MSG.format(resource_type="physical_disk")
        assert result["failed"] is True

    def test_main_virtual_disk_missing_controller_id(self, idrac_connection_storage_info_mock, idrac_default_args):
        idrac_default_args.update({"resource_type": "virtual_disk"})
        result = self._run_module(idrac_default_args)
        assert result["msg"] == CONTROLLER_ID_REQUIRED_MSG.format(resource_type="virtual_disk")
        assert result["failed"] is True

    def test_main_virtual_disk_with_controller_id_success(self, idrac_connection_storage_info_mock, idrac_default_args):
        idrac_default_args.update({"resource_type": "virtual_disk", "controller_id": "RAID.Slot.1-1"})
        result = self._run_module(idrac_default_args)
        assert result["msg"] == SUCCESS_MSG

    def test_main_http_error_case(self, idrac_connection_storage_info_mock, idrac_default_args, mocker):
        json_str = to_text(json.dumps({"data": "out"}))
        idrac_default_args.update({"resource_type": "controller"})
        mocker.patch(MODULE_PATH + 'StorageInfo.validate_params',
                     side_effect=HTTPError('https://testhost.com', 400, 'http error message',
                                           {"accept-type": "application/json"}, StringIO(json_str)))
        result = self._run_module(idrac_default_args)
        assert result['failed'] is True
        assert 'error_info' in result

    def test_main_url_error_case(self, idrac_connection_storage_info_mock, idrac_default_args, mocker):
        idrac_default_args.update({"resource_type": "controller"})
        mocker.patch(MODULE_PATH + 'StorageInfo.validate_params',
                     side_effect=URLError('url error message'))
        result = self._run_module(idrac_default_args)
        assert result.get('unreachable') is True

    def test_main_connection_error_case(self, idrac_connection_storage_info_mock, idrac_default_args, mocker):
        idrac_default_args.update({"resource_type": "controller"})
        mocker.patch(MODULE_PATH + 'StorageInfo.validate_params',
                     side_effect=ConnectionError('connection error message'))
        result = self._run_module(idrac_default_args)
        assert result['failed'] is True

    def test_main_authentication_failure_401(self, idrac_connection_storage_info_mock, idrac_default_args, mocker):
        json_str = to_text(json.dumps({"data": "out"}))
        idrac_default_args.update({"resource_type": "controller"})
        mocker.patch(MODULE_PATH + 'StorageInfo.validate_params',
                     side_effect=HTTPError('https://testhost.com', 401, 'Unauthorized',
                                           {"accept-type": "application/json"}, StringIO(json_str)))
        result = self._run_module(idrac_default_args)
        assert result['failed'] is True
        assert 'error_info' in result

    def test_main_authentication_failure_403(self, idrac_connection_storage_info_mock, idrac_default_args, mocker):
        json_str = to_text(json.dumps({"data": "out"}))
        idrac_default_args.update({"resource_type": "controller"})
        mocker.patch(MODULE_PATH + 'StorageInfo.validate_params',
                     side_effect=HTTPError('https://testhost.com', 403, 'Forbidden',
                                           {"accept-type": "application/json"}, StringIO(json_str)))
        result = self._run_module(idrac_default_args)
        assert result['failed'] is True
        assert 'error_info' in result

    def test_main_network_timeout_case(self, idrac_connection_storage_info_mock, idrac_default_args, mocker):
        idrac_default_args.update({"resource_type": "controller"})
        mocker.patch(MODULE_PATH + 'StorageInfo.validate_params',
                     side_effect=URLError('timed out'))
        result = self._run_module(idrac_default_args)
        assert result.get('unreachable') is True

    def test_firmware_validation_idrac9_supported(self, idrac_connection_storage_info_mock, idrac_storage_info_mock,
                                                   idrac_default_args):
        idrac_storage_info_mock.get_server_generation = (16, "7.10.90.00", "iDRAC 9")
        idrac_default_args.update({"resource_type": "controller"})
        result = self._run_module(idrac_default_args)
        assert result["msg"] == SUCCESS_MSG

    def test_firmware_validation_idrac9_unsupported(self, idrac_connection_storage_info_mock, idrac_storage_info_mock,
                                                     idrac_default_args):
        idrac_storage_info_mock.get_server_generation = (16, "7.10.80.00", "iDRAC 9")
        idrac_default_args.update({"resource_type": "controller"})
        result = self._run_module(idrac_default_args)
        assert result["failed"] is True
        assert "does not meet the minimum required version" in result["msg"]

    def test_firmware_validation_idrac10_supported(self, idrac_connection_storage_info_mock, idrac_storage_info_mock,
                                                    idrac_default_args):
        idrac_storage_info_mock.get_server_generation = (17, "1.20.50.50", "iDRAC 10")
        idrac_default_args.update({"resource_type": "controller"})
        result = self._run_module(idrac_default_args)
        assert result["msg"] == SUCCESS_MSG

    def test_firmware_validation_idrac10_unsupported(self, idrac_connection_storage_info_mock, idrac_storage_info_mock,
                                                      idrac_default_args):
        idrac_storage_info_mock.get_server_generation = (17, "1.20.40.00", "iDRAC 10")
        idrac_default_args.update({"resource_type": "controller"})
        result = self._run_module(idrac_default_args)
        assert result["failed"] is True
        assert "does not meet the minimum required version" in result["msg"]

    def test_firmware_validation_unsupported_generation(self, idrac_connection_storage_info_mock,
                                                          idrac_storage_info_mock, idrac_default_args):
        idrac_storage_info_mock.get_server_generation = (14, "2.75.75.75", "iDRAC 8")
        idrac_default_args.update({"resource_type": "controller"})
        result = self._run_module(idrac_default_args)
        assert result["failed"] is True
        assert result["msg"] == "This module is not supported on iDRAC 8."

    @pytest.mark.parametrize("current,minimum,expected", [
        ("7.10.90.00", "7.10.90.00", True),
        ("7.10.90.01", "7.10.90.00", True),
        ("7.10.89.99", "7.10.90.00", False),
        ("1.20.50.50", "1.20.50.50", True),
        ("1.20.50.49", "1.20.50.50", False),
        ("8.0.0.0", "7.10.90.00", True),
    ])
    def test_version_meets_minimum(self, current, minimum, expected):
        assert idrac_storage_info.StorageInfo._version_meets_minimum(current, minimum) is expected


@pytest.fixture
def idrac_default_args():
    return {
        "idrac_ip": "192.168.0.1",
        "idrac_user": "username",
        "idrac_password": "password",
        "idrac_port": 443,
    }
