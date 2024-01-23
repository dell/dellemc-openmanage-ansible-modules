# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.7.0
# Copyright (C) 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

from io import StringIO

import pytest
from urllib.error import HTTPError
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_license
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from mock import MagicMock

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_license.'

INVALID_LICENSE_MSG = "License id '{license_id}' is invalid."
SUCCESS_EXPORT_MSG = "Successfully exported the license."
SUCCESS_DELETE_MSG = "Successfully deleted the license."
SUCCESS_IMPORT_MSG = "Successfully imported the license."
FAILURE_MSG = "Unable to '{operation}' the license with id '{license_id}' as it does not exist."
FAILURE_IMPORT_MSG = "Unable to import the license."
NO_FILE_MSG = "License file not found."
INVALID_FILE_MSG = "File extension is invalid. Supported extensions for local 'share_type' " \
                   "is: .txt and .xml, and for network 'share_type' is: .xml."
INVALID_DIRECTORY_MSG = "Provided directory path '{path}' is not valid."
INSUFFICIENT_DIRECTORY_PERMISSION_MSG = "Provided directory path '{path}' is not writable. " \
                                        "Please check if the directory has appropriate permissions"
MISSING_PARAMETER_MSG = "Missing required parameter 'file_name'."


class TestLicense(FakeAnsibleModule):
    module = idrac_license

    @pytest.fixture
    def idrac_license_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_license_mock(self, mocker, idrac_license_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_license_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_license_mock
        return idrac_conn_mock

    def test_check_license_id(self, idrac_default_args, idrac_connection_license_mock,
                              idrac_license_mock, mocker):
        mocker.patch(MODULE_PATH + "License.get_license_url",
                     return_value="/redfish/v1/license")
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        lic_obj = self.module.License(
            idrac_connection_license_mock, f_module)

        idr_obj = MagicMock()
        idr_obj.json_data = {"license_id" : "1234"}
        mocker.patch(MODULE_PATH + "iDRACRedfishAPI.invoke_request",
                     return_value=idr_obj)
        data = lic_obj.check_license_id(module=f_module, license_id="1234", operation="delete")
        assert data.json_data == {"license_id" : "1234"}

        mocker.patch(MODULE_PATH + "iDRACRedfishAPI.invoke_request",
                     side_effect=HTTPError('https://testhost.com', 400,
                                           'http error message',
                                           {"accept-type": "application/json"},
                                           StringIO("json_str")))
        with pytest.raises(Exception) as exc:
            lic_obj.check_license_id(module=f_module, license_id="1234", operation="delete")
        assert exc.value.args[0] == FAILURE_MSG.format(operation="delete", license_id="1234")
