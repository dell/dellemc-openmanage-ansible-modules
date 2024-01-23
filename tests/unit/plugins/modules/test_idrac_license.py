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

REDFISH = "/redfish/v1"


class TestLicense(FakeAnsibleModule):
    module = idrac_license
    uri = '/redfish/v1/api'

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
        idr_obj.json_data = {"license_id": "1234"}
        mocker.patch(MODULE_PATH + "iDRACRedfishAPI.invoke_request",
                     return_value=idr_obj)
        data = lic_obj.check_license_id(module=f_module, license_id="1234", operation="delete")
        assert data.json_data == {"license_id": "1234"}

        mocker.patch(MODULE_PATH + "iDRACRedfishAPI.invoke_request",
                     side_effect=HTTPError('https://testhost.com', 400,
                                           'http error message',
                                           {"accept-type": "application/json"},
                                           StringIO("json_str")))
        with pytest.raises(Exception) as exc:
            lic_obj.check_license_id(module=f_module, license_id="1234", operation="delete")
        assert exc.value.args[0] == FAILURE_MSG.format(operation="delete", license_id="1234")

    def test_get_license_url(self, idrac_default_args, idrac_connection_license_mock, mocker):
        v1_resp = {"LicenseService": {"@odata.id": "/redfish/v1/LicenseService"},
                   "Licenses": {"@odata.id": "/redfish/v1/LicenseService/Licenses"}}
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value=v1_resp)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        lic_obj = self.module.License(
            idrac_connection_license_mock, f_module)
        data = lic_obj.get_license_url()
        assert data == "/redfish/v1/LicenseService/Licenses"

    @pytest.fixture
    def idrac_mock(self, mocker):
        return mocker.MagicMock()

    def test_get_job_status_success(self, mocker):
        # Mocking necessary objects and functions
        module_mock = self.get_module_mock()
        license_job_response_mock = mocker.MagicMock()
        license_job_response_mock.headers.get.return_value = "https://testhost.com/job_tracking/12345"

        mocker.patch(MODULE_PATH + "remove_key", return_value={"job_details": "mocked_job_details"})
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri", return_value=["/redfish/v1/managers/1"])

        # Creating an instance of the class
        obj_under_test = self.module.License(self.idrac_mock, module_mock)

        # Mocking the idrac_redfish_job_tracking function to simulate a successful job tracking
        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking", return_value=(False, "mocked_message", {"job_details": "mocked_job_details"}, 0))

        # Calling the method under test
        result = obj_under_test.get_job_status(module_mock, license_job_response_mock)

        # Assertions
        assert result == {"job_details": "mocked_job_details"}

    def test_get_job_status_failure(self, mocker):
        # Mocking necessary objects and functions
        module_mock = self.get_module_mock()
        license_job_response_mock = mocker.MagicMock()
        license_job_response_mock.headers.get.return_value = "https://testhost.com/job_tracking/12345"

        mocker.patch(MODULE_PATH + "remove_key", return_value={"Message": "None"})
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri", return_value=["/redfish/v1/managers/1"])

        # Creating an instance of the class
        obj_under_test = self.module.License(self.idrac_mock, module_mock)

        # Mocking the idrac_redfish_job_tracking function to simulate a failed job tracking
        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking", return_value=(True, "None", {"Message": "None"}, 0))

        # Mocking module.exit_json
        exit_json_mock = mocker.patch.object(module_mock, "exit_json")

        # Calling the method under test
        result = obj_under_test.get_job_status(module_mock, license_job_response_mock)

        # Assertions
        exit_json_mock.assert_called_once_with(msg="None", failed=True, job_details={"Message": "None"})
        assert result == {"Message": "None"}

    def test_get_share_details(self, idrac_connection_license_mock):
        # Create a mock module object
        module_mock = MagicMock()
        module_mock.params.get.return_value = {
            'ip_address': 'XX.XX.XX.XX',
            'share_name': 'my_share',
            'username': 'my_user',
            'password': 'my_password'
        }

        # Create an instance of the License class
        lic_obj = self.module.License(idrac_connection_license_mock, module_mock)

        # Call the get_share_details method
        result = lic_obj.get_share_details(module=module_mock)

        # Assert the result
        assert result == {
            'IPAddress': 'XX.XX.XX.XX',
            'ShareName': 'my_share',
            'UserName': 'my_user',
            'Password': 'my_password'
        }

    def test_get_proxy_details(self, idrac_connection_license_mock):
        # Create a mock module object
        module_mock = MagicMock()
        module_mock.params.get.return_value = {
            'ip_address': 'XX.XX.XX.XX',
            'share_name': 'my_share',
            'username': 'my_user',
            'password': 'my_password',
            'share_type': 'http',
            'ignore_certificate_warning': 'off',
            'proxy_support': 'parameters_proxy',
            'proxy_type': 'http',
            'proxy_server': 'proxy.example.com',
            'proxy_port': 8080,
            'proxy_username': 'my_username',
            'proxy_password': 'my_password'
        }

        # Create an instance of the License class
        lic_obj = self.module.License(idrac_connection_license_mock, module_mock)

        # Call the get_proxy_details method
        result = lic_obj.get_proxy_details(module=module_mock)

        # Define the expected result
        expected_result = {
            'IPAddress': 'XX.XX.XX.XX',
            'ShareName': 'my_share',
            'UserName': 'my_user',
            'Password': 'my_password',
            'ShareType': 'HTTP',
            'IgnoreCertWarning': 'Off',
            'ProxySupport': 'ParametersProxy',
            'ProxyType': 'HTTP',
            'ProxyServer': 'proxy.example.com',
            'ProxyPort': '8080',
            'ProxyUname': 'my_username',
            'ProxyPasswd': 'my_password'
        }

        # Assert the result
        assert result == expected_result


class TestDeleteLicense:
    @pytest.fixture
    def delete_license_mock(self):
        delete_license_obj = MagicMock()
        return delete_license_obj

    @pytest.fixture
    def idrac_connection_license_mock(self, mocker, delete_license_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=delete_license_mock)
        idrac_conn_mock.return_value.__enter__.return_value = delete_license_mock
        return idrac_conn_mock

    def test_execute_delete_license_success(self, mocker, idrac_connection_license_mock):
        mocker.patch(MODULE_PATH + "License.get_license_url",
                     return_value="/redfish/v1/license")
        f_module = MagicMock()
        f_module.params = {'license_id': '1234'}
        delete_license_obj = idrac_license.DeleteLicense(idrac_connection_license_mock, f_module)
        delete_license_obj.idrac.invoke_request.return_value.status_code = 204
        delete_license_obj.execute(f_module)
        f_module.exit_json.assert_called_once_with(msg=SUCCESS_DELETE_MSG, changed=True)

    def test_execute_delete_license_failure(self, mocker, idrac_connection_license_mock):
        mocker.patch(MODULE_PATH + "License.get_license_url",
                     return_value="/redfish/v1/license")
        f_module = MagicMock()
        f_module.params = {'license_id': '5678'}
        delete_license_obj = idrac_license.DeleteLicense(idrac_connection_license_mock, f_module)
        delete_license_obj.idrac.invoke_request.return_value.status_code = 404
        delete_license_obj.execute(f_module)
        f_module.exit_json.assert_called_once_with(FAILURE_MSG.format(operation="delete", license_id="5678"), failed=True)


class TestExportLicense(FakeAnsibleModule):
    module = idrac_license
    uri = '/redfish/v1/api'

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

    def test_export_license_local(self, idrac_default_args, idrac_connection_license_mock,
                                  idrac_license_mock, mocker, tmp_path):
        mocker.patch(MODULE_PATH + "License.get_license_url",
                     return_value="/redfish/v1/license")
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        export_license_obj = idrac_license.ExportLicense(idrac_license_mock, f_module)

        mocker.patch(MODULE_PATH + "ExportLicense._ExportLicense__export_license_local",
                     return_value=MagicMock(json_data={"LicenseFile": "Mock License Content"}))

        # Set the necessary parameters in for f_module
        f_module.params = {
            'license_id': 'test_license_id',
            'share_parameters': {
                'share_name': str(tmp_path),
                'file_name': 'test_license'
            }
        }

        result = export_license_obj._ExportLicense__export_license_local(
            f_module, '/redfish/v1/export_license')

        assert result.json_data == {"LicenseFile": "Mock License Content"}
