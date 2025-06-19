# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.2
# Copyright (C) 2024-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

from io import StringIO
import json
import tempfile
import os

import pytest
from urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils._text import to_text
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_license
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from unittest.mock import MagicMock
from ansible_collections.dellemc.openmanage.plugins.modules.idrac_license import main

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_license.'
MODULE_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.'

INVALID_LICENSE_MSG = "License with ID '{license_id}' does not exist on the iDRAC."
SUCCESS_EXPORT_MSG = "Successfully exported the license."
SUCCESS_DELETE_MSG = "Successfully deleted the license."
SUCCESS_IMPORT_MSG = "Successfully imported the license."
FAILURE_MSG = "Unable to '{operation}' the license with id '{license_id}' as it does not exist."
FAILURE_IMPORT_MSG = "Unable to import the license."
NO_FILE_MSG = "License file not found."
UNSUPPORTED_FIRMWARE_MSG = "iDRAC firmware version is not supported."
NO_OPERATION_SKIP_MSG = "Task is skipped as none of import, export or delete is specified."
INVALID_FILE_MSG = "File extension is invalid. Supported extensions for local 'share_type' " \
                   "are: .txt and .xml, and for network 'share_type' is: .xml."
INVALID_DIRECTORY_MSG = "Provided directory path '{path}' is not valid."
INSUFFICIENT_DIRECTORY_PERMISSION_MSG = "Provided directory path '{path}' is not writable. " \
                                        "Please check if the directory has appropriate permissions"
MISSING_FILE_NAME_PARAMETER_MSG = "Missing required parameter 'file_name'."
REDFISH = "/redfish/v1"

LIC_GET_LICENSE_URL = "License.get_license_url"
REDFISH_LICENSE_URL = "/redfish/v1/license"
REDFISH_BASE_API = '/redfish/v1/api'
MANAGER_URI_ONE = "/redfish/v1/managers/1"
API_ONE = "/local/action"
EXPORT_URL_MOCK = '/redfish/v1/export_license'
IMPORT_URL_MOCK = '/redfish/v1/import_license'
API_INVOKE_MOCKER = "iDRACRedfishAPI.invoke_request"
ODATA = "@odata.id"
IDRAC_ID = "iDRAC.Embedded.1"
LIC_FILE_NAME = 'test_lic.txt'
HTTPS_PATH = "https://testhost.com"
HTTP_ERROR = "http error message"
APPLICATION_JSON = "application/json"


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
        mocker.patch(MODULE_PATH + LIC_GET_LICENSE_URL,
                     return_value=REDFISH_LICENSE_URL)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        lic_obj = self.module.License(
            idrac_connection_license_mock, f_module)

        idr_obj = MagicMock()
        idr_obj.json_data = {"license_id": "1234"}
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     return_value=idr_obj)
        data = lic_obj.check_license_id(license_id="1234")
        assert data.json_data == {"license_id": "1234"}

        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     side_effect=HTTPError(HTTPS_PATH, 400,
                                           HTTP_ERROR,
                                           {"accept-type": APPLICATION_JSON},
                                           StringIO("json_str")))
        with pytest.raises(Exception) as exc:
            lic_obj.check_license_id(license_id="1234")
        assert exc.value.args[0] == INVALID_LICENSE_MSG.format(license_id="1234")

    def test_get_license_url(self, idrac_default_args, idrac_connection_license_mock, mocker):
        v1_resp = {"LicenseService": {ODATA: "/redfish/v1/LicenseService"},
                   "Licenses": {ODATA: "/redfish/v1/LicenseService/Licenses"}}
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value=v1_resp)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        lic_obj = self.module.License(
            idrac_connection_license_mock, f_module)
        data = lic_obj.get_license_url()
        assert data == "/redfish/v1/LicenseService/Licenses"

    def test_get_job_status_success(self, mocker, idrac_license_mock):
        # Mocking necessary objects and functions
        module_mock = self.get_module_mock()
        license_job_response_mock = mocker.MagicMock()
        license_job_response_mock.headers.get.return_value = "HTTPS_PATH/job_tracking/12345"

        mocker.patch(MODULE_PATH + "remove_key", return_value={"job_details": "mocked_job_details"})
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri", return_value=[MANAGER_URI_ONE])

        # Creating an instance of the class
        obj_under_test = self.module.License(idrac_license_mock, module_mock)

        # Mocking the idrac_redfish_job_tracking function to simulate a successful job tracking
        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking", return_value=(False, "mocked_message", {"job_details": "mocked_job_details"}, 0))

        # Calling the method under test
        result = obj_under_test.get_job_status(license_job_response_mock)

        # Assertions
        assert result == {"job_details": "mocked_job_details"}

    def test_get_job_status_failure(self, mocker, idrac_license_mock):
        # Mocking necessary objects and functions
        module_mock = self.get_module_mock()
        license_job_response_mock = mocker.MagicMock()
        license_job_response_mock.headers.get.return_value = "HTTPS_PATH/job_tracking/12345"

        mocker.patch(MODULE_PATH + "remove_key", return_value={"Message": "None"})
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri", return_value=[MANAGER_URI_ONE])

        # Creating an instance of the class
        obj_under_test = self.module.License(idrac_license_mock, module_mock)

        # Mocking the idrac_redfish_job_tracking function to simulate a failed job tracking
        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking", return_value=(True, "None", {"Message": "None"}, 0))

        # Mocking module.exit_json
        exit_json_mock = mocker.patch.object(module_mock, "exit_json")

        # Calling the method under test
        result = obj_under_test.get_job_status(license_job_response_mock)

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
        result = lic_obj.get_share_details()

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
        result = lic_obj.get_proxy_details()

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
        mocker.patch(MODULE_PATH + LIC_GET_LICENSE_URL,
                     return_value=REDFISH_LICENSE_URL)
        f_module = MagicMock()
        f_module.params = {'license_id': '1234'}
        delete_license_obj = idrac_license.DeleteLicense(idrac_connection_license_mock, f_module)
        delete_license_obj.idrac.invoke_request.return_value.status_code = 204
        delete_license_obj.execute()
        f_module.exit_json.assert_called_once_with(msg=SUCCESS_DELETE_MSG, changed=True)

    def test_execute_delete_license_failure(self, mocker, idrac_connection_license_mock):
        mocker.patch(MODULE_PATH + LIC_GET_LICENSE_URL,
                     return_value=REDFISH_LICENSE_URL)
        f_module = MagicMock()
        f_module.params = {'license_id': '5678'}
        delete_license_obj = idrac_license.DeleteLicense(idrac_connection_license_mock, f_module)
        delete_license_obj.idrac.invoke_request.return_value.status_code = 404
        delete_license_obj.execute()
        f_module.exit_json.assert_called_once_with(msg=FAILURE_MSG.format(operation="delete", license_id="5678"), failed=True)


class TestExportLicense(FakeAnsibleModule):
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

    def test_export_license_local(self, idrac_default_args, idrac_connection_license_mock, mocker):
        tmp_path = tempfile.gettempdir()
        export_params = {
            'license_id': 'test_license_id',
            'share_parameters': {
                'share_name': str(tmp_path),
                'file_name': 'test_lic.xml'
            }
        }
        idr_obj = MagicMock()
        idr_obj.json_data = {"license_id": "1234", "LicenseFile": "dGVzdF9saWNlbnNlX2NvbnRlbnQK"}
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     return_value=idr_obj)
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        export_license_obj = self.module.ExportLicense(idrac_connection_license_mock, f_module)
        result = export_license_obj._ExportLicense__export_license_local(EXPORT_URL_MOCK)
        assert result.json_data == {'LicenseFile': 'dGVzdF9saWNlbnNlX2NvbnRlbnQK', 'license_id': '1234'}
        assert os.path.exists(f"{tmp_path}/test_lic.xml")
        if os.path.exists(f"{tmp_path}/test_lic.xml"):
            os.remove(f"{tmp_path}/test_lic.xml")

        export_params = {
            'license_id': 'test_license_id',
            'share_parameters': {
                'share_name': str(tmp_path),
            }
        }
        idrac_default_args.update(export_params)
        result = export_license_obj._ExportLicense__export_license_local(EXPORT_URL_MOCK)
        assert result.json_data == {'LicenseFile': 'dGVzdF9saWNlbnNlX2NvbnRlbnQK', 'license_id': '1234'}
        assert os.path.exists(f"{tmp_path}/test_license_id_iDRAC_license.xml")
        if os.path.exists(f"{tmp_path}/test_license_id_iDRAC_license.xml"):
            os.remove(f"{tmp_path}/test_license_id_iDRAC_license.xml")

    def test_export_license_http(self, idrac_default_args, idrac_connection_license_mock, mocker):
        export_params = {
            'license_id': 'test_license_id',
            'share_parameters': {
                'file_name': 'test_lic',
                'share_type': 'http',
                'ignore_certificate_warning': 'off'
            }
        }
        idr_obj = MagicMock()
        idr_obj.json_data = {"license_id": "1234", "LicenseFile": "test_license_content"}
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     return_value=idr_obj)
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        export_license_obj = self.module.ExportLicense(idrac_connection_license_mock, f_module)
        result = export_license_obj._ExportLicense__export_license_http(EXPORT_URL_MOCK)
        assert result.json_data == {'LicenseFile': 'test_license_content', 'license_id': '1234'}

    def test_export_license_cifs(self, idrac_default_args, idrac_connection_license_mock, mocker):
        export_params = {
            'license_id': 'test_license_id',
            'share_parameters': {
                'file_name': 'test_lic',
                'share_type': 'cifs',
                'ignore_certificate_warning': 'off',
                'workgroup': "mydomain"
            }
        }
        idr_obj = MagicMock()
        idr_obj.json_data = {"license_id": "1234", "LicenseFile": "test_license_content"}
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     return_value=idr_obj)
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        export_license_obj = self.module.ExportLicense(idrac_connection_license_mock, f_module)
        result = export_license_obj._ExportLicense__export_license_cifs(EXPORT_URL_MOCK)
        assert result.json_data == {'LicenseFile': 'test_license_content', 'license_id': '1234'}

    def test_export_license_nfs(self, idrac_default_args, idrac_connection_license_mock, mocker):
        export_params = {
            'license_id': 'test_license_id',
            'share_parameters': {
                'file_name': 'test_lic',
                'share_type': 'nfs',
                'ignore_certificate_warning': 'off'
            }
        }
        idr_obj = MagicMock()
        idr_obj.json_data = {"license_id": "1234", "LicenseFile": "test_license_content"}
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     return_value=idr_obj)
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        export_license_obj = self.module.ExportLicense(idrac_connection_license_mock, f_module)
        result = export_license_obj._ExportLicense__export_license_nfs(EXPORT_URL_MOCK)
        assert result.json_data == {'LicenseFile': 'test_license_content', 'license_id': '1234'}

    def test_get_export_license_url(self, idrac_default_args, idrac_connection_license_mock, mocker):
        export_params = {
            'license_id': 'test_license_id',
            'share_parameters': {
                'file_name': 'test_lic',
                'share_type': 'local',
                'ignore_certificate_warning': 'off'
            }
        }
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value={"Links": {"Oem": {"Dell": {"DellLicenseManagementService": {ODATA: "/LicenseService"}}}},
                                   "Actions": {"#DellLicenseManagementService.ExportLicense": {"target": API_ONE}}})
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        export_license_obj = self.module.ExportLicense(idrac_connection_license_mock, f_module)
        result = export_license_obj._ExportLicense__get_export_license_url()
        assert result == API_ONE

        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, "error"))
        with pytest.raises(Exception) as exc:
            export_license_obj._ExportLicense__get_export_license_url()
        assert exc.value.args[0] == "error"

    def test_execute(self, idrac_default_args, idrac_connection_license_mock, mocker):
        share_type = 'local'
        export_params = {
            'license_id': 'test_license_id',
            'share_parameters': {
                'file_name': 'test_lic',
                'share_type': share_type
            }
        }
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        mocker.patch(MODULE_PATH + "License.check_license_id")
        mocker.patch(MODULE_PATH + "ExportLicense._ExportLicense__get_export_license_url",
                     return_value="/License/url")
        mocker.patch(MODULE_PATH + "ExportLicense.get_job_status",
                     return_value={"JobId": "JID1234"})
        idr_obj = MagicMock()
        idr_obj.status_code = 200

        mocker.patch(MODULE_PATH + "ExportLicense._ExportLicense__export_license_local",
                     return_value=idr_obj)
        export_license_obj = self.module.ExportLicense(idrac_connection_license_mock, f_module)
        with pytest.raises(Exception) as exc:
            export_license_obj.execute()
        assert exc.value.args[0] == SUCCESS_EXPORT_MSG

        export_params.get('share_parameters')["share_type"] = "http"
        mocker.patch(MODULE_PATH + "ExportLicense._ExportLicense__export_license_http",
                     return_value=idr_obj)
        with pytest.raises(Exception) as exc:
            export_license_obj.execute()
        assert exc.value.args[0] == SUCCESS_EXPORT_MSG

        export_params.get('share_parameters')["share_type"] = "cifs"
        mocker.patch(MODULE_PATH + "ExportLicense._ExportLicense__export_license_cifs",
                     return_value=idr_obj)
        with pytest.raises(Exception) as exc:
            export_license_obj.execute()
        assert exc.value.args[0] == SUCCESS_EXPORT_MSG

        export_params.get('share_parameters')["share_type"] = "nfs"
        mocker.patch(MODULE_PATH + "ExportLicense._ExportLicense__export_license_nfs",
                     return_value=idr_obj)
        with pytest.raises(Exception) as exc:
            export_license_obj.execute()
        assert exc.value.args[0] == SUCCESS_EXPORT_MSG

        export_params.get('share_parameters')["share_type"] = "https"
        idr_obj.status_code = 400
        mocker.patch(MODULE_PATH + "ExportLicense._ExportLicense__export_license_http",
                     return_value=idr_obj)
        with pytest.raises(Exception) as exc:
            export_license_obj.execute()
        assert exc.value.args[0] == FAILURE_MSG.format(operation="export", license_id="test_license_id")


class TestImportLicense(FakeAnsibleModule):
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

    def test_execute(self, idrac_default_args, idrac_connection_license_mock, mocker):
        share_type = 'local'
        import_params = {
            'license_id': 'test_license_id',
            'share_parameters': {
                'file_name': 'test_lic.xml',
                'share_type': share_type
            }
        }
        idrac_default_args.update(import_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        mocker.patch(MODULE_PATH + "ImportLicense._ImportLicense__get_import_license_url",
                     return_value="/License/url")
        mocker.patch(MODULE_PATH + "get_manager_res_id",
                     return_value=IDRAC_ID)
        mocker.patch(MODULE_PATH + "ImportLicense.get_job_status",
                     return_value={"JobId": "JID1234"})
        idr_obj = MagicMock()
        idr_obj.status_code = 200

        mocker.patch(MODULE_PATH + "ImportLicense._ImportLicense__import_license_local",
                     return_value=idr_obj)
        import_license_obj = self.module.ImportLicense(idrac_connection_license_mock, f_module)
        with pytest.raises(Exception) as exc:
            import_license_obj.execute()
        assert exc.value.args[0] == SUCCESS_IMPORT_MSG

        import_params.get('share_parameters')["share_type"] = "http"
        mocker.patch(MODULE_PATH + "ImportLicense._ImportLicense__import_license_http",
                     return_value=idr_obj)
        with pytest.raises(Exception) as exc:
            import_license_obj.execute()
        assert exc.value.args[0] == SUCCESS_IMPORT_MSG

        import_params.get('share_parameters')["share_type"] = "cifs"
        mocker.patch(MODULE_PATH + "ImportLicense._ImportLicense__import_license_cifs",
                     return_value=idr_obj)
        with pytest.raises(Exception) as exc:
            import_license_obj.execute()
        assert exc.value.args[0] == SUCCESS_IMPORT_MSG

        import_params.get('share_parameters')["share_type"] = "nfs"
        mocker.patch(MODULE_PATH + "ImportLicense._ImportLicense__import_license_nfs",
                     return_value=idr_obj)
        with pytest.raises(Exception) as exc:
            import_license_obj.execute()
        assert exc.value.args[0] == SUCCESS_IMPORT_MSG

        import_params.get('share_parameters')["share_type"] = "https"
        idr_obj.status_code = 400
        mocker.patch(MODULE_PATH + "ImportLicense._ImportLicense__import_license_http",
                     return_value=idr_obj)
        with pytest.raises(Exception) as exc:
            import_license_obj.execute()
        assert exc.value.args[0] == FAILURE_IMPORT_MSG

    def test_import_license_local(self, idrac_default_args, idrac_connection_license_mock, mocker):
        tmp_path = tempfile.gettempdir()
        import_params = {
            'license_id': 'test_license_id',
            'share_parameters': {
                'share_name': 'doesnotexistpath',
                'file_name': LIC_FILE_NAME
            }
        }
        idrac_default_args.update(import_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        import_license_obj = self.module.ImportLicense(idrac_connection_license_mock, f_module)
        with pytest.raises(Exception) as exc:
            import_license_obj._ImportLicense__import_license_local(EXPORT_URL_MOCK, IDRAC_ID)
        assert exc.value.args[0] == INVALID_DIRECTORY_MSG.format(path='doesnotexistpath')

        import_params = {
            'license_id': 'test_license_id',
            'share_parameters': {
                'share_name': str(tmp_path),
                'file_name': LIC_FILE_NAME
            }
        }
        file_name = os.path.join(tmp_path, LIC_FILE_NAME)
        with open(file_name, "w") as fp:
            fp.writelines("license_file")
        idr_obj = MagicMock()
        idr_obj.json_data = {"license_id": "1234", "LicenseFile": "test_license_content"}
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     return_value=idr_obj)
        idrac_default_args.update(import_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        import_license_obj = self.module.ImportLicense(idrac_connection_license_mock, f_module)
        result = import_license_obj._ImportLicense__import_license_local(EXPORT_URL_MOCK, IDRAC_ID)
        assert result.json_data == {'LicenseFile': 'test_license_content', 'license_id': '1234'}
        assert os.path.exists(file_name)

        json_str = to_text(json.dumps({"error": {'@Message.ExtendedInfo': [
            {
                'MessageId': "LIC018",
                "Message": "Already imported"
            }
        ]}}))
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     side_effect=HTTPError(HTTPS_PATH, 400, HTTP_ERROR,
                                           {"accept-type": APPLICATION_JSON}, StringIO(json_str)))
        with pytest.raises(Exception) as exc:
            import_license_obj._ImportLicense__import_license_local(EXPORT_URL_MOCK, IDRAC_ID)
        assert exc.value.args[0] == "Already imported"

        if os.path.exists(file_name):
            os.remove(file_name)

    def test_import_license_http(self, idrac_default_args, idrac_connection_license_mock, mocker):
        import_params = {
            'license_id': 'test_license_id',
            'share_parameters': {
                'file_name': 'test_lic',
                'share_type': 'http',
                'ignore_certificate_warning': 'off'
            }
        }
        idr_obj = MagicMock()
        idr_obj.json_data = {"license_id": "1234", "LicenseFile": "test_license_content"}
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     return_value=idr_obj)
        idrac_default_args.update(import_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        import_license_obj = self.module.ImportLicense(idrac_connection_license_mock, f_module)
        result = import_license_obj._ImportLicense__import_license_http(IMPORT_URL_MOCK, IDRAC_ID)
        assert result.json_data == {'LicenseFile': 'test_license_content', 'license_id': '1234'}

    def test_import_license_cifs(self, idrac_default_args, idrac_connection_license_mock, mocker):
        import_params = {
            'license_id': 'test_license_id',
            'share_parameters': {
                'file_name': 'test_lic',
                'share_type': 'cifs',
                'ignore_certificate_warning': 'off',
                'workgroup': 'mydomain'
            }
        }
        idr_obj = MagicMock()
        idr_obj.json_data = {"license_id": "1234", "LicenseFile": "test_license_content"}
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     return_value=idr_obj)
        idrac_default_args.update(import_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        import_license_obj = self.module.ImportLicense(idrac_connection_license_mock, f_module)
        result = import_license_obj._ImportLicense__import_license_cifs(IMPORT_URL_MOCK, IDRAC_ID)
        assert result.json_data == {'LicenseFile': 'test_license_content', 'license_id': '1234'}

    def test_import_license_nfs(self, idrac_default_args, idrac_connection_license_mock, mocker):
        import_params = {
            'license_id': 'test_license_id',
            'share_parameters': {
                'file_name': 'test_lic',
                'share_type': 'nfs',
                'ignore_certificate_warning': 'off',
                'workgroup': 'mydomain'
            }
        }
        idr_obj = MagicMock()
        idr_obj.json_data = {"license_id": "1234", "LicenseFile": "test_license_content"}
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER,
                     return_value=idr_obj)
        idrac_default_args.update(import_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        import_license_obj = self.module.ImportLicense(idrac_connection_license_mock, f_module)
        result = import_license_obj._ImportLicense__import_license_nfs(IMPORT_URL_MOCK, IDRAC_ID)
        assert result.json_data == {'LicenseFile': 'test_license_content', 'license_id': '1234'}

    def test_get_import_license_url(self, idrac_default_args, idrac_connection_license_mock, mocker):
        export_params = {
            'license_id': 'test_license_id',
            'share_parameters': {
                'file_name': 'test_lic',
                'share_type': 'local',
                'ignore_certificate_warning': 'off'
            }
        }
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, None))
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value={"Links": {"Oem": {"Dell": {"DellLicenseManagementService": {ODATA: "/LicenseService"}}}},
                                   "Actions": {"#DellLicenseManagementService.ImportLicense": {"target": API_ONE}}})
        idrac_default_args.update(export_params)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        import_license_obj = self.module.ImportLicense(idrac_connection_license_mock, f_module)
        result = import_license_obj._ImportLicense__get_import_license_url()
        assert result == API_ONE

    def test_get_job_status(self, idrac_default_args, idrac_connection_license_mock, mocker):
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri", return_value=[MANAGER_URI_ONE])
        lic_job_resp_obj = MagicMock()
        lic_job_resp_obj.headers = {"Location": "idrac_internal"}
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        import_license_obj = self.module.ImportLicense(idrac_connection_license_mock, f_module)

        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking", return_value=(False, "None", {"JobId": "JID1234"}, 0))
        result = import_license_obj.get_job_status(lic_job_resp_obj)
        assert result == {"JobId": "JID1234"}

        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking", return_value=(True, "None", {"Message": "Got LIC018",
                                                                                              "MessageId": "LIC018"}, 0))
        with pytest.raises(Exception) as exc:
            import_license_obj.get_job_status(lic_job_resp_obj)
        assert exc.value.args[0] == "Got LIC018"

        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking", return_value=(True, "None", {"Message": "Got LIC019",
                                                                                              "MessageId": "LIC019"}, 0))
        with pytest.raises(Exception) as exc:
            import_license_obj.get_job_status(lic_job_resp_obj)
        assert exc.value.args[0] == "Got LIC019"


class TestLicenseType(FakeAnsibleModule):
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

    def test_license_operation(self, idrac_default_args, idrac_connection_license_mock, mocker):
        idrac_default_args.update({"import": False, "export": False, "delete": True})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        lic_class = self.module.LicenseType.license_operation(idrac_connection_license_mock, f_module)
        assert isinstance(lic_class, self.module.DeleteLicense)

        idrac_default_args.update({"import": False, "export": True, "delete": False})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        lic_class = self.module.LicenseType.license_operation(idrac_connection_license_mock, f_module)
        assert isinstance(lic_class, self.module.ExportLicense)

        idrac_default_args.update({"import": True, "export": False, "delete": False})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        lic_class = self.module.LicenseType.license_operation(idrac_connection_license_mock, f_module)
        assert isinstance(lic_class, self.module.ImportLicense)

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_idrac_license_main_exception_handling_case(self, exc_type, mocker, idrac_default_args, idrac_connection_license_mock):
        idrac_default_args.update({"delete": True, "license_id": "1234"})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + "get_idrac_firmware_version",
                         side_effect=exc_type(HTTPS_PATH, 400,
                                              HTTP_ERROR,
                                              {"accept-type": APPLICATION_JSON},
                                              StringIO(json_str)))
        else:
            mocker.patch(MODULE_PATH + "get_idrac_firmware_version",
                         side_effect=exc_type('test'))
        result = self._run_module(idrac_default_args)
        if exc_type == URLError:
            assert result['unreachable'] is True
            assert "unreachable iDRAC IP" in result['msg']
            assert idrac_default_args["idrac_ip"] in result['msg']
        else:
            assert result['failed'] is True
        assert 'msg' in result

    def test_main(self, mocker):
        module_mock = mocker.MagicMock()
        idrac_mock = mocker.MagicMock()
        license_mock = mocker.MagicMock()

        # Mock the necessary functions and objects
        mocker.patch(MODULE_PATH + 'get_argument_spec', return_value={})
        mocker.patch(MODULE_PATH + 'IdracAnsibleModule', return_value=module_mock)
        mocker.patch(MODULE_PATH + 'iDRACRedfishAPI', return_value=idrac_mock)
        mocker.patch(MODULE_PATH + 'get_idrac_firmware_version', return_value='3.1')
        mocker.patch(MODULE_PATH + 'LicenseType.license_operation', return_value=license_mock)
        main()
        mocker.patch(MODULE_PATH + 'get_idrac_firmware_version', return_value='2.9')
        main()
