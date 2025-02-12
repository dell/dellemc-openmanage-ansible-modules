# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.4.0
# Copyright (C) 2020-2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import pytest
import mock
from io import StringIO
from ansible.module_utils._text import to_text
from urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_server_config_profile
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from unittest.mock import MagicMock


MODULE_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.'
MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
MODULE_PATH_COMP = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_server_config_profile.'
SUCCESS_MSG = 'Successfully {0}ed the Server Configuration Profile'
SUCCESS_MSG_CD = 'Successfully {0}ed the custom defaults Server Configuration Profile.'
IMPORT_TRIGGERED_SUCCESS_MSG = "Successfully triggered the job to {0} the custom defaults Server Configuration Profile."
JOB_SUCCESS_MSG = 'Successfully triggered the job to {0} the Server Configuration Profile'
PREVIEW_SUCCESS_MSG = 'Successfully previewed the Server Configuration Profile'
CHANGES_FOUND = "Changes found to be applied."
NO_CHANGES_FOUND = "No changes found to be applied."
GET_FIRMWARE_VERSION = "get_idrac_firmware_version"
CHECK_IDRAC_VERSION = "is_check_idrac_latest"
OPEN_KEY = "builtins.open"
FILE_NAME = "scp_file.xml"
HTTP_ERROR_MSG = "http error message"
RETURN_TYPE = "application/json"
INVOKE_REQ_KEY = "iDRACRedfishAPI.invoke_request"
LOCAL_SHARE_NAME = "share/"
EXECUTE_KEY_IMPORT = "ImportCustomDefaultCommand.execute"
REDFISH_JOB_TRACKING = "idrac_server_config_profile.idrac_redfish_job_tracking"
INVALID_SHARE_NAME = "Unable to perform the {command} operation because an invalid Share name is entered. \
Only 'local' share name is supported. Enter the valid Share name and retry the operation."
ERR_STATUS_CODE = [400, 404]
CUSTOM_DEFAULTS_NOT_FOUND = "Custom defaults is not available on the iDRAC."
SHARE_NAME_REQUIRED = "Share name is required. Enter the valid Share name and retry the operation."
NO_CHANGES_FOUND = "No changes found to be applied."
INVALID_FILE = "Invalid file path provided."
HTTP_ERROR_MSG = "http error message"
RETURN_TYPE = "application/json"
INVALID_FILE_FORMAT = "An invalid export format is selected. File format '.xml' is supported. Select a valid file format and retry the operation."
INVALID_XML_CONTENT = "An invalid XML content is provided. Provide custom default content in a valid XML format."
CUSTOM_ERROR = "{command} is not supported on this firmware version of iDRAC. \
Enter the valid values and retry the operation."


class TestServerConfigProfile(FakeAnsibleModule):
    module = idrac_server_config_profile

    @pytest.fixture
    def idrac_server_configure_profile_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_scp_redfish_mock(self, mocker, idrac_server_configure_profile_mock):
        idrac_conn_class_mock = mocker.patch(MODULE_PATH + 'idrac_server_config_profile.iDRACRedfishAPI',
                                             return_value=idrac_server_configure_profile_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_server_configure_profile_mock
        return idrac_server_configure_profile_mock

    @pytest.fixture
    def idrac_redfish_job_tracking_mock(self, mocker, idrac_server_configure_profile_mock):
        idrac_conn_class_mock = mocker.patch(MODULE_PATH + REDFISH_JOB_TRACKING,
                                             return_value=idrac_server_configure_profile_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_server_configure_profile_mock
        idrac_conn_class_mock.headers = {"Location": "/redfish/v1/Managers/iDRAC.Embedded.1/JID_123456789"}
        return idrac_server_configure_profile_mock

    @pytest.mark.parametrize("params", [
        {"message": SUCCESS_MSG.format("export"),
         "mparams": {"share_name": "\\{SCP SHARE IP}\\share", "job_wait": True,
                     "scp_components": "IDRAC", "scp_file": FILE_NAME,
                     "proxy_port": 80, "export_format": "XML"}},
        {"message": SUCCESS_MSG.format("export"),
         "mparams": {"share_name": "https://{SCP SHARE IP}/myshare/", "proxy_type": "socks4",
                     "proxy_support": True, "job_wait": True, "scp_components": "IDRAC",
                     "proxy_port": 80, "export_format": "JSON", "proxy_server": "PROXY_SERVER_IP",
                     "proxy_username": "proxy_username"}},
        {"message": JOB_SUCCESS_MSG.format("export"),
         "mparams": {"share_name": "{SCP SHARE IP}:/nfsshare", "job_wait": False,
                     "scp_components": "IDRAC", "scp_file": "scp_file.txt"}},
        {"message": JOB_SUCCESS_MSG.format("export"),
         "mparams": {"share_name": "/share", "job_wait": False,
                     "scp_components": "IDRAC", "scp_file": "scp_file.json"}},
    ])
    def test_run_export_scp(self, params, idrac_scp_redfish_mock, idrac_redfish_job_tracking_mock, idrac_default_args, mocker):
        idrac_default_args.update({"share_user": "sharename", "command": "export",
                                   "export_use": "Default", "include_in_export": "default"})
        idrac_default_args.update(params['mparams'])
        mocker.patch(OPEN_KEY, mocker.mock_open())
        idrac_redfish_job_tracking_mock.status_code = 202
        idrac_redfish_job_tracking_mock.success = True
        mocker.patch(MODULE_PATH + REDFISH_JOB_TRACKING,
                     return_value=(False, False, {"Status": "Completed"}, {}))
        result = self._run_module(idrac_default_args, check_mode=params.get('check_mode', False))
        assert params['message'] in result['msg']

    @pytest.mark.parametrize("params", [
        {"message": CHANGES_FOUND,
         "json_data": {"Id": "JID_932024672685", "Message": SUCCESS_MSG.format("import"), "MessageId": "SYS081",
                       "PercentComplete": 100, "file": "https://{SCP SHARE PATH}/{SCP FILE NAME}.json"},
         "check_mode": True,
         "mparams": {"share_name": "{SCP SHARE IP}:/nfsshare", "share_user": "sharename",
                     "job_wait": False, "scp_components": "IDRAC",
                     "scp_file": "scp_file1.xml", "end_host_power_state": "On",
                     "shutdown_type": "Graceful"}},
        {"message": NO_CHANGES_FOUND,
         "json_data": {"Id": "JID_932024672685", "Message": SUCCESS_MSG.format("import"), "MessageId": "SYS069",
                       "PercentComplete": 100, "file": "https://{SCP SHARE PATH}/{SCP FILE NAME}.json"},
         "check_mode": True,
         "mparams": {"share_name": "\\{SCP SHARE IP}\\share", "share_user": "sharename",
                     "job_wait": False, "scp_components": "IDRAC",
                     "scp_file": "scp_file1.xml", "end_host_power_state": "On",
                     "shutdown_type": "Graceful"}},
        {"message": SUCCESS_MSG.format("import"),
         "json_data": {"Id": "JID_932024672685", "Message": NO_CHANGES_FOUND, "MessageId": "SYS043",
                       "PercentComplete": 100, "file": "https://{SCP SHARE PATH}/{SCP FILE NAME}.json"},
         "mparams": {"share_name": "/share", "share_user": "sharename",
                     "job_wait": True, "scp_components": "IDRAC",
                     "scp_file": "scp_file1.xml", "end_host_power_state": "On",
                     "shutdown_type": "Graceful"}},
        {"message": SUCCESS_MSG.format("import"),
         "json_data": {"Id": "JID_932024672685", "Message": SUCCESS_MSG.format("import"), "MessageId": "SYS069",
                       "PercentComplete": 100, "file": "https://{SCP SHARE PATH}/{SCP FILE NAME}.json"},
         "mparams": {"share_name": "https://{SCP SHARE IP}/share", "share_user": "sharename",
                     "job_wait": True, "scp_components": "IDRAC",
                     "scp_file": "scp_file1.xml", "end_host_power_state": "On",
                     "shutdown_type": "Graceful"}},
        {"message": SUCCESS_MSG.format("import"),
         "json_data": {"Id": "JID_932024672685", "Message": SUCCESS_MSG.format("import"), "MessageId": "SYS053",
                       "PercentComplete": 100, "file": "https://{SCP SHARE PATH}/{SCP FILE NAME}.json"},
         "mparams": {"share_name": "https://{SCP SHARE IP}/share", "share_user": "sharename",
                     "job_wait": True, "scp_components": "IDRAC",
                     "scp_file": "scp_file1.xml", "end_host_power_state": "On",
                     "shutdown_type": "Graceful"}},
        {"message": SUCCESS_MSG.format("import"),
         "json_data": {"Id": "JID_932024672685", "Message": NO_CHANGES_FOUND, "MessageId": "SYS069",
                       "PercentComplete": 100, "file": "https://{SCP SHARE PATH}/{SCP FILE NAME}.json"},
         "mparams": {"command": "import", "job_wait": True, "scp_components": "IDRAC",
                     "import_buffer": "<SystemConfiguration><Component FQDD='iDRAC.Embedded.1'><Attribute Name='IPMILan.1#Enable'> \
                                       <Value>Disabled</Value></Attribute></Component><Component FQDD='iDRAC.Embedded.1'>"}},
    ])
    @mock.patch(MODULE_PATH + "idrac_server_config_profile.exists", return_value=True)
    def test_run_import_scp(self, mock_exists, params, idrac_scp_redfish_mock, idrac_redfish_job_tracking_mock, idrac_default_args, mocker):
        idrac_default_args.update({"command": "import"})
        idrac_default_args.update(params['mparams'])
        mocker.patch(OPEN_KEY, mocker.mock_open())
        if params.get('check_mode'):
            mocker.patch(MODULE_PATH + 'idrac_server_config_profile.preview_scp_redfish',
                         return_value=params['json_data'])
        elif params['mparams']['job_wait']:
            mocker.patch(MODULE_PATH + REDFISH_JOB_TRACKING,
                         return_value=(False, False, {"Status": "Completed"}, {}))
        else:
            idrac_scp_redfish_mock.import_scp.return_value = params['json_data']
        result = self._run_module(idrac_default_args, check_mode=params.get('check_mode', False))
        assert params['message'] in result['msg']

    @pytest.mark.parametrize("params", [
        {"message": PREVIEW_SUCCESS_MSG,
         "check_mode": True,
         "mparams": {"share_name": "{SCP SHARE IP}:/nfsshare", "share_user": "sharename",
                     "command": "preview", "job_wait": True,
                     "scp_components": "IDRAC", "scp_file": "scp_file4.xml"}},
        {"message": PREVIEW_SUCCESS_MSG,
         "mparams": {"share_name": "https://{SCP SHARE IP}/nfsshare", "share_user": "sharename",
                     "command": "preview", "job_wait": True,
                     "scp_components": "IDRAC", "scp_file": "scp_file4.xml"}},
    ])
    def test_preview_scp(self, params, idrac_scp_redfish_mock, idrac_redfish_job_tracking_mock, idrac_default_args, mocker):
        idrac_default_args.update({"command": "preview"})
        idrac_default_args.update(params['mparams'])
        mocker.patch(MODULE_PATH + REDFISH_JOB_TRACKING,
                     return_value=(False, False, {"Status": "Completed"}, {}))
        result = self._run_module(idrac_default_args, check_mode=params.get('check_mode', False))
        assert params['message'] in result['msg']

    def test_preview_scp_redfish_throws_ex(self, idrac_scp_redfish_mock, idrac_redfish_job_tracking_mock, idrac_default_args, mocker):
        idrac_default_args.update({"share_name": "{SCP SHARE IP}:/nfsshare", "share_user": "sharename",
                                   "command": "preview", "job_wait": True,
                                   "scp_components": "IDRAC", "scp_file": "scp_file5.xml"})
        idrac_redfish_job_tracking_mock.headers = {"Location": "/redfish/v1/Managers/iDRAC.Embedded.1/JID_123456789"}
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.idrac_redfish_job_tracking',
                     return_value=(True, False, {"Status": "Failed"}, {}))
        result = self._run_module(idrac_default_args)
        assert result['failed']

    def test_import_scp_http_throws_exception(self, idrac_scp_redfish_mock, idrac_redfish_job_tracking_mock, idrac_default_args, mocker):
        idrac_default_args.update({"share_name": "https://{SCP SHARE IP}/myshare/", "share_user": "sharename",
                                   "command": "import", "job_wait": True, "scp_components": "IDRAC",
                                   "scp_file": "scp_file2.xml", "end_host_power_state": "On",
                                   "shutdown_type": "Graceful"})
        mocker.patch(MODULE_PATH + REDFISH_JOB_TRACKING,
                     return_value=(True, False, {"Status": "Failed"}, {}))
        result = self._run_module(idrac_default_args)
        assert result['failed']

    @pytest.mark.parametrize("params", [
        {"message": "Invalid file path provided.",
         "mparams": {"share_name": "/share/", "share_user": "sharename",
                     "command": "import", "job_wait": False, "scp_components": "IDRAC",
                     "scp_file": "scp_file3.xml", "end_host_power_state": "On",
                     "shutdown_type": "Graceful"}},
        {"message": "proxy_support is True but all of the following are missing: proxy_server",
         "mparams": {"share_name": "https://{SCP SHARE IP}/myshare/", "proxy_type": "http",
                     "proxy_support": True, "job_wait": True, "scp_components": "IDRAC",
                     "proxy_port": 80, "export_format": "JSON",
                     "proxy_username": "proxy_username"}},
        {"message": "import_buffer is mutually exclusive with share_name",
         "mparams": {"share_name": "{SCP SHARE IP}:/nfsshare", "command": "preview", "job_wait": False,
                     "import_buffer": "<SystemConfiguration><Component FQDD='iDRAC.Embedded.1'><Attribute Name='IPMILan.1#Enable'> \
                                       <Value>Disabled</Value></Attribute></Component><Component FQDD='iDRAC.Embedded.1'>"}},
        {"message": "import_buffer is mutually exclusive with scp_file",
         "mparams": {"scp_file": "example.json", "job_wait": False, "command": "import",
                     "import_buffer": "<SystemConfiguration><Component FQDD='iDRAC.Embedded.1'><Attribute Name='IPMILan.1#Enable'> \
                                       <Value>Disabled</Value></Attribute></Component><Component FQDD='iDRAC.Embedded.1'>"}},
        {"message": "The option ALL cannot be used with options IDRAC, BIOS, NIC, or RAID.",
         "mparams": {"share_name": "https://{SCP SHARE IP}/myshare/", "share_user": "sharename",
                     "command": "import", "job_wait": True, "scp_components": ["IDRAC", "ALL"],
                     "scp_file": "scp_file2.xml", "end_host_power_state": "On",
                     "shutdown_type": "Graceful"}},
    ])
    def test_scp_invalid(self, params, idrac_scp_redfish_mock, idrac_default_args):
        idrac_default_args.update(params['mparams'])
        with pytest.raises(Exception) as ex:
            self._run_module(idrac_default_args)
        assert params['message'] in ex.value.args[0]['msg']

    @pytest.mark.parametrize("params", [
        {"mparams": {"share_name": LOCAL_SHARE_NAME, "job_wait": False,
                     "scp_file": FILE_NAME}}
    ])
    def test_compare_custom_default_configs(self, params, idrac_scp_redfish_mock, idrac_default_args, mocker):
        share_details = {
            "share_type": "LOCAL",
            "share_name": LOCAL_SHARE_NAME
        }
        obj = MagicMock()
        obj.body = "<SystemConfiguration Model=\"\" ServiceTag=\"\">\n<Component FQDD=\"iDRAC.Embedded.1\">\n \
                    <Attribute Name=\"IPMILan.1#Enable\">Disabled</Attribute>\n </Component>\n\n</SystemConfiguration>"
        idrac_default_args.update({"command": "import_custom_defaults"})
        idrac_default_args.update(params['mparams'])
        mocker.patch(MODULE_PATH_COMP + "idrac_custom_option", return_value=obj)
        mocker.patch(MODULE_PATH_COMP + "get_scp_share_details", return_value=(share_details, FILE_NAME))
        mocker.patch(MODULE_PATH_COMP + "get_buffer_text", return_value=obj.body)
        f_module = self.get_module_mock(params=idrac_default_args)
        res = self.module.compare_custom_default_configs(f_module, idrac_scp_redfish_mock)
        assert res is False

    @pytest.mark.parametrize("params", [
        {"api_res": {
            "Dell": {
                "CustomDefaultsDownloadURI": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/CustomDefaultsDownloadURI"
            }},
         "mparams": {"share_name": LOCAL_SHARE_NAME, "job_wait": False,
                     "scp_file": FILE_NAME}}
    ])
    def test_idrac_custom_options(self, params, idrac_scp_redfish_mock, idrac_default_args, mocker):
        share_details = {
            "share_type": "LOCAL",
            "share_name": LOCAL_SHARE_NAME
        }
        json_str = to_text(json.dumps({"data": "out"}))
        idrac_default_args.update({"command": "import_custom_defaults"})
        idrac_default_args.update(params['mparams'])
        mocker.patch(MODULE_UTILS_PATH + "get_dynamic_uri", return_value=params['api_res'])
        mocker.patch(MODULE_PATH_COMP + "get_scp_share_details", return_value=(share_details, FILE_NAME))
        mocker.patch(MODULE_PATH_COMP + INVOKE_REQ_KEY, side_effect=HTTPError("https://test.com", 404, HTTP_ERROR_MSG,
                                                                              {"accept-type": RETURN_TYPE}, StringIO(json_str)))
        res = self.module.idrac_custom_option(idrac_scp_redfish_mock)
        assert res is None

    @pytest.mark.parametrize("firmware_version, expected_result", [
        ("7.00.00", True),
        ("6.99.99", False),
        ("5.99.99", False),
    ])
    def test_is_check_idrac_latest(self, firmware_version, expected_result):
        assert idrac_server_config_profile.is_check_idrac_latest(firmware_version) == expected_result

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_idrac_reset_main_exception_handling_case(self, exc_type, idrac_default_args,
                                                      idrac_scp_redfish_mock, mocker):
        json_str = to_text(json.dumps({"data": "out"}))
        idrac_default_args.update({"command": "import_custom_defaults"})
        idrac_default_args.update({"share_name": LOCAL_SHARE_NAME})
        idrac_default_args.update({"job_wait": False})
        if exc_type in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_UTILS_PATH + GET_FIRMWARE_VERSION, return_value="7.00.00")
            mocker.patch(MODULE_PATH_COMP + EXECUTE_KEY_IMPORT,
                         side_effect=exc_type('https://testhost.com', 400,
                                              HTTP_ERROR_MSG,
                                              {"accept-type": RETURN_TYPE},
                                              StringIO(json_str)))
        else:
            mocker.patch(MODULE_PATH_COMP + GET_FIRMWARE_VERSION,
                         side_effect=exc_type('test'))
        result = self._run_module(idrac_default_args)
        if exc_type == URLError:
            assert result['unreachable'] is True
        else:
            assert result['failed'] is True
        assert 'msg' in result


class TestImportCustomDefaultCommand(FakeAnsibleModule):
    module = idrac_server_config_profile
    validate_allowed_values = {
        "Oem": {
            "Dell": {
                "CustomDefaultsDownloadURI": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/CustomDefaultsDownloadURI"
            }
        }
    }

    share_details = {
        "share_type": "LOCAL",
        "share_name": ""
    }
    custom_default_content = "<SystemConfiguration Model=\"\" ServiceTag=\"\">\n<Component FQDD=\"iDRAC.Embedded.1\">\n \
    <Attribute Name=\"IPMILan.1#Enable\">Disabled</Attribute>\n </Component>\n\n</SystemConfiguration>"

    custom_default_content_enabled = "<SystemConfiguration Model=\"\" ServiceTag=\"\">\n<Component FQDD=\"iDRAC.Embedded.1\">\n \
    <Attribute Name=\"IPMILan.1#Enable\">Enabled</Attribute>\n </Component>\n\n</SystemConfiguration>"

    res_msg = {
        "Data": {
            "StatusCode": 202,
            "jobid": "JID_176997459424",
            "next_uri": "base_uri/Jobs/JID_176997459424"
        },
        "Job": {
            "JobId": "JID_176997459424",
            "ResourceURI": "base_uri/JID_176997459424"
        },
        "Return": "JobCreated",
        "Status": "Success",
        "Message": "none",
        "StatusCode": 202,
        "file": "/share/scp_file3.xml",
        "retval": True
    }
    res_with_job_wait = {
        "ActualRunningStartTime": "star_time",
        "ActualRunningStopTime": "end_time",
        "CompletionTime": "completion_time",
        "Id": "JID_177002621612",
        "JobState": "Completed",
        "JobType": "UploadCustomDefaults",
        "Message": "The Custom Defaults file is successfully uploaded to iDRAC.",
        "MessageArgs": [],
        "MessageId": "SYS332",
        "PercentComplete": 100,
        "TargetSettingsURI": "NULL",
        "file": "/root/collections/xyz.xml",
        "retval": True}

    @pytest.fixture
    def idrac_server_config_profile_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_server_config_profile_mock(self, mocker, idrac_server_config_profile_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH_COMP + 'iDRACRedfishAPI',
                                       return_value=idrac_server_config_profile_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_server_config_profile_mock
        return idrac_conn_mock

    def test_execute_one(self, idrac_default_args, idrac_connection_server_config_profile_mock, mocker):
        # Scenario - When 'Custom defaults' is not supported and iDRAC8
        idrac_default_args.update({"command": "import_custom_defaults"})
        mocker.patch(MODULE_UTILS_PATH + GET_FIRMWARE_VERSION, return_value="2.81.81")
        mocker.patch(MODULE_PATH_COMP + CHECK_IDRAC_VERSION, return_value=False)
        idrac_default_args.update({})
        f_module = self.get_module_mock(params=idrac_default_args)
        scp_obj = self.module.ImportCustomDefaultCommand(idrac_connection_server_config_profile_mock, f_module)
        with pytest.raises(Exception) as exc:
            scp_obj.execute()
        assert exc.value.args[0] == "import_custom_defaults is not supported on this firmware version of iDRAC. Enter the valid values and retry the operation."

        # Scenario - when both share_name and import_buffer are None and command is import_custom_defaults
        idrac_default_args.update({"command": "import_custom_defaults"})
        mocker.patch(MODULE_UTILS_PATH + GET_FIRMWARE_VERSION, return_value="7.00.00")
        mocker.patch(MODULE_PATH_COMP + CHECK_IDRAC_VERSION, return_value=True)
        f_module = self.get_module_mock(params=idrac_default_args)
        scp_obj = self.module.ImportCustomDefaultCommand(idrac_connection_server_config_profile_mock, f_module)
        with pytest.raises(Exception) as exc:
            scp_obj.execute()
        assert exc.value.args[0] == "Share name is required. Enter the valid Share name and retry the operation."

        # Scenario - when both import_buffer and share_name are passed
        idrac_default_args.update({})
        idrac_default_args.update({"share_name": "root/cd"})
        idrac_default_args.update({"import_buffer": self.custom_default_content})
        idrac_default_args.update({"command": "import_custom_defaults"})
        mocker.patch(MODULE_UTILS_PATH + GET_FIRMWARE_VERSION, return_value="7.00.00")
        mocker.patch(MODULE_PATH_COMP + CHECK_IDRAC_VERSION, return_value=True)
        mocker.patch(MODULE_PATH_COMP + "validate_share_name", return_value=None)
        f_module = self.get_module_mock(params=idrac_default_args)
        scp_obj = self.module.ImportCustomDefaultCommand(idrac_connection_server_config_profile_mock, f_module)
        with pytest.raises(Exception) as exc:
            scp_obj.execute()
        assert exc.value.args[0] == "import_buffer is mutually exclusive with share_name."

        # Scenario - when both import_buffer and scp_file are passed
        idrac_default_args.clear()
        idrac_default_args.update({})
        idrac_default_args.update({"scp_file": "xyz.xml"})
        idrac_default_args.update({"share_name": "root/cd"})
        idrac_default_args.update({"import_buffer": self.custom_default_content})
        idrac_default_args.update({"command": "import_custom_defaults"})
        mocker.patch(MODULE_UTILS_PATH + GET_FIRMWARE_VERSION, return_value="7.00.00")
        mocker.patch(MODULE_PATH_COMP + CHECK_IDRAC_VERSION, return_value=True)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        scp_obj = self.module.ImportCustomDefaultCommand(idrac_connection_server_config_profile_mock, f_module)
        with pytest.raises(Exception) as exc:
            scp_obj.execute()
        assert exc.value.args[0] == "import_buffer is mutually exclusive with scp_file."

        # Scenario - when command is import_custom_defaults and check mode with same custom defaults
        idrac_default_args.clear()
        idrac_default_args.update({})
        idrac_default_args.update({"share_name": LOCAL_SHARE_NAME})
        idrac_default_args.update({"job_wait": False})
        idrac_default_args.update({"scp_file": FILE_NAME})
        idrac_default_args.update({"command": "import_custom_defaults"})
        mocker.patch(MODULE_UTILS_PATH + GET_FIRMWARE_VERSION, return_value="7.00.00")
        mocker.patch(MODULE_PATH_COMP + CHECK_IDRAC_VERSION, return_value=True)
        mocker.patch(MODULE_PATH_COMP + "validate_customdefault_input", return_value=None)
        mocker.patch(MODULE_PATH_COMP + "compare_custom_default_configs", return_value=False)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        scp_obj = self.module.ImportCustomDefaultCommand(idrac_connection_server_config_profile_mock, f_module)
        with pytest.raises(Exception) as exc:
            scp_obj.execute()
        assert exc.value.args[0] == NO_CHANGES_FOUND

        # Scenario - when command is import_custom_defaults and check mode with different custom defaults
        idrac_default_args.clear()
        idrac_default_args.update({})
        idrac_default_args.update({"share_name": LOCAL_SHARE_NAME})
        idrac_default_args.update({"job_wait": False})
        idrac_default_args.update({"scp_file": FILE_NAME})
        idrac_default_args.update({"command": "import_custom_defaults"})
        mocker.patch(MODULE_UTILS_PATH + GET_FIRMWARE_VERSION, return_value="7.00.00")
        mocker.patch(MODULE_PATH_COMP + CHECK_IDRAC_VERSION, return_value=True)
        mocker.patch(MODULE_PATH_COMP + "validate_customdefault_input", return_value=None)
        mocker.patch(MODULE_PATH_COMP + "compare_custom_default_configs", return_value=True)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        scp_obj = self.module.ImportCustomDefaultCommand(idrac_connection_server_config_profile_mock, f_module)
        with pytest.raises(Exception) as exc:
            scp_obj.execute()
        assert exc.value.args[0] == CHANGES_FOUND

        # Scenario - [Idempotency] vwhen command is import_custom_defaults and normal mode with same custom defaults
        obj = MagicMock()
        obj.body = self.custom_default_content
        self.share_details["share_name"] = LOCAL_SHARE_NAME
        idrac_default_args.clear()
        idrac_default_args.update({})
        idrac_default_args.update({"share_name": LOCAL_SHARE_NAME})
        idrac_default_args.update({"job_wait": False})
        idrac_default_args.update({"scp_file": FILE_NAME})
        idrac_default_args.update({"command": "import_custom_defaults"})
        mocker.patch(MODULE_UTILS_PATH + GET_FIRMWARE_VERSION, return_value="7.00.00")
        mocker.patch(MODULE_PATH_COMP + CHECK_IDRAC_VERSION, return_value=True)
        mocker.patch(MODULE_PATH_COMP + "validate_customdefault_input", return_value=None)
        mocker.patch(MODULE_PATH_COMP + "idrac_custom_option", return_value=obj)
        mocker.patch(MODULE_PATH_COMP + "get_scp_share_details", return_value=(self.share_details, FILE_NAME))
        mocker.patch(MODULE_PATH_COMP + "get_buffer_text", return_value=self.custom_default_content)
        mocker.patch(MODULE_PATH_COMP + "compare_custom_default_configs", return_value=False)
        f_module = self.get_module_mock(params=idrac_default_args)
        scp_obj = self.module.ImportCustomDefaultCommand(idrac_connection_server_config_profile_mock, f_module)
        with pytest.raises(Exception) as exc:
            scp_obj.execute()
        assert exc.value.args[0] == NO_CHANGES_FOUND

    def test_execute_two(self, idrac_default_args, idrac_connection_server_config_profile_mock, mocker):
        # Scenario - when scp_file content is in invalid XML format
        obj = MagicMock()
        obj.body = self.custom_default_content
        idrac_default_args.clear()
        idrac_default_args.update({})
        idrac_default_args.update({"job_wait": False})
        idrac_default_args.update({"import_buffer": "{'key':'value'}"})
        idrac_default_args.update({"command": "import_custom_defaults"})
        mocker.patch(MODULE_UTILS_PATH + GET_FIRMWARE_VERSION, return_value="7.00.00")
        mocker.patch(MODULE_PATH_COMP + CHECK_IDRAC_VERSION, return_value=True)
        mocker.patch(MODULE_PATH_COMP + "validate_customdefault_input", return_value=None)
        mocker.patch(MODULE_PATH_COMP + "idrac_custom_option", return_value=obj)
        mocker.patch(MODULE_PATH_COMP + "get_buffer_text", return_value={'key': 'value'})
        f_module = self.get_module_mock(params=idrac_default_args)
        scp_obj = self.module.ImportCustomDefaultCommand(idrac_connection_server_config_profile_mock, f_module)
        with pytest.raises(Exception) as exc:
            scp_obj.execute()
        assert exc.value.args[0] == INVALID_XML_CONTENT

    def test_execute_three(self, idrac_default_args, idrac_connection_server_config_profile_mock, mocker):
        # Scenario - when scp_file and share_name are passed for import_custom_defaults with job_wait false
        idrac_default_args.clear()
        idrac_default_args.update({})
        obj1 = MagicMock()
        obj1.body = self.custom_default_content_enabled
        idrac_default_args.update({"job_wait": False})
        idrac_default_args.update({"import_buffer": self.custom_default_content})
        idrac_default_args.update({"command": "import_custom_defaults"})
        mocker.patch(MODULE_UTILS_PATH + GET_FIRMWARE_VERSION, return_value="7.00.00")
        mocker.patch(MODULE_PATH_COMP + CHECK_IDRAC_VERSION, return_value=True)
        mocker.patch(MODULE_PATH_COMP + "validate_share_name", return_value=None)
        mocker.patch(MODULE_PATH_COMP + "exit_on_failure", return_value=None)
        mocker.patch(MODULE_PATH_COMP + "wait_for_job_tracking_redfish", return_value=self.res_msg)
        mocker.patch(MODULE_PATH_COMP + "response_format_change", return_value=self.res_msg)
        mocker.patch(MODULE_PATH_COMP + "get_buffer_text", return_value=self.custom_default_content)
        mocker.patch(MODULE_PATH_COMP + "get_scp_share_details", return_value=({}, "100.XX.XX.XX_202466_82617_scp.xml"))
        mocker.patch(MODULE_UTILS_PATH + "get_dynamic_uri", return_value=self.validate_allowed_values)
        mocker.patch(MODULE_PATH_COMP + INVOKE_REQ_KEY, return_value=obj1)
        mocker.patch(MODULE_PATH_COMP + "exists", return_value=True)
        mocker.patch(OPEN_KEY, mocker.mock_open(read_data=self.custom_default_content))
        f_module = self.get_module_mock(params=idrac_default_args)
        scp_obj = self.module.ImportCustomDefaultCommand(idrac_connection_server_config_profile_mock, f_module)
        msg_resp, resp = scp_obj.execute()
        assert msg_resp == self.res_msg

        # Scenario - when scp_file and share_name are passed for import_custom_defaults with job_wait true
        obj = MagicMock()
        obj.body = self.custom_default_content_enabled
        self.share_details["share_name"] = LOCAL_SHARE_NAME
        idrac_default_args.clear()
        idrac_default_args.update({})
        idrac_default_args.update({"share_name": LOCAL_SHARE_NAME})
        idrac_default_args.update({"job_wait": True})
        idrac_default_args.update({"scp_file": FILE_NAME})
        idrac_default_args.update({"command": "import_custom_defaults"})
        mocker.patch(MODULE_UTILS_PATH + GET_FIRMWARE_VERSION, return_value="7.00.00")
        mocker.patch(MODULE_PATH_COMP + CHECK_IDRAC_VERSION, return_value=True)
        mocker.patch(MODULE_PATH_COMP + "validate_share_name", return_value=None)
        mocker.patch(MODULE_PATH_COMP + "exit_on_failure", return_value=None)
        mocker.patch(MODULE_PATH_COMP + "wait_for_job_tracking_redfish", return_value=self.res_with_job_wait)
        mocker.patch(MODULE_PATH_COMP + "get_scp_share_details", return_value=(self.share_details, FILE_NAME))
        mocker.patch(MODULE_PATH_COMP + "response_format_change", return_value=self.res_with_job_wait)
        mocker.patch(MODULE_PATH_COMP + "get_buffer_text", return_value=self.custom_default_content)
        mocker.patch(MODULE_UTILS_PATH + "get_dynamic_uri", return_value=self.validate_allowed_values)
        mocker.patch(MODULE_PATH_COMP + INVOKE_REQ_KEY, return_value=obj)
        mocker.patch(MODULE_PATH_COMP + "exists", return_value=True)
        mocker.patch(OPEN_KEY, mocker.mock_open(read_data=self.custom_default_content))
        f_module = self.get_module_mock(params=idrac_default_args)
        scp_obj = self.module.ImportCustomDefaultCommand(idrac_connection_server_config_profile_mock, f_module)
        msg_resp, resp = scp_obj.execute()
        assert msg_resp == self.res_with_job_wait
        assert msg_resp['Message'] == "The Custom Defaults file is successfully uploaded to iDRAC."

    def test_execute_four(self, idrac_default_args, idrac_connection_server_config_profile_mock, mocker):
        # Scenario - when both share_name is not 'local' and command is import_custom_defaults
        idrac_default_args.clear()
        idrac_default_args.update({})
        idrac_default_args.update({"scp_file": "xyz.xml"})
        idrac_default_args.update({"job_wait": False})
        idrac_default_args.update({"share_name": "https://abc"})
        idrac_default_args.update({"command": "import_custom_defaults"})
        mocker.patch(MODULE_UTILS_PATH + GET_FIRMWARE_VERSION, return_value="7.00.00")
        mocker.patch(MODULE_PATH_COMP + CHECK_IDRAC_VERSION, return_value=True)
        f_module = self.get_module_mock(params=idrac_default_args)
        scp_obj = self.module.ImportCustomDefaultCommand(idrac_connection_server_config_profile_mock, f_module)
        with pytest.raises(Exception) as exc:
            scp_obj.execute()
        assert exc.value.args[0] == INVALID_SHARE_NAME.format(command="import_custom_defaults")

    def test_idrac_reset_main_positive_case(self, idrac_default_args,
                                            idrac_connection_server_config_profile_mock, mocker):
        # Scenario - When command 'import_custom_defaults' and job_wait is true
        idrac_default_args.update({"command": "import_custom_defaults", "share_name": "share_name"})
        idrac_default_args.update({"job_wait": True})
        mocker.patch(MODULE_PATH_COMP + GET_FIRMWARE_VERSION, return_value="7.10.05")
        mocker.patch(MODULE_PATH_COMP + EXECUTE_KEY_IMPORT, return_value=(self.res_with_job_wait, True))
        data = self._run_module(idrac_default_args)
        assert data['msg'] == SUCCESS_MSG_CD.format("import")
        assert data['scp_status'] == self.res_with_job_wait

        # Scenario - When command 'import_custom_defaults' and job_wait is false
        idrac_default_args.update({"job_wait": False})
        msg_resp = {'msg': IMPORT_TRIGGERED_SUCCESS_MSG.format("import"), 'scp_status': self.res_msg, 'changed': True}
        mocker.patch(MODULE_PATH_COMP + GET_FIRMWARE_VERSION, return_value="7.10.05")
        mocker.patch(MODULE_PATH_COMP + EXECUTE_KEY_IMPORT, return_value=(msg_resp, {}))
        data = self._run_module(idrac_default_args)
        assert data['msg'] == IMPORT_TRIGGERED_SUCCESS_MSG.format("import")


class TestExportCustomDefaultCommand(FakeAnsibleModule):
    module = idrac_server_config_profile
    validate_allowed_values = {
        "Dell": {
            "CustomDefaultsDownloadURI": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/CustomDefaultsDownloadURI"
        }
    }

    share_details = {
        "share_type": "LOCAL",
        "share_name": ""
    }
    custom_default_content = "<SystemConfiguration Model=\"\" ServiceTag=\"\">\n<Component FQDD=\"iDRAC.Embedded.1\">\n \
    <Attribute Name=\"IPMILan.1#Enable\">Disabled</Attribute>\n </Component>\n\n</SystemConfiguration>"

    custom_default_content_enabled = "<SystemConfiguration Model=\"\" ServiceTag=\"\">\n<Component FQDD=\"iDRAC.Embedded.1\">\n \
    <Attribute Name=\"IPMILan.1#Enable\">Enabled</Attribute>\n </Component>\n\n</SystemConfiguration>"

    @pytest.fixture
    def idrac_server_config_profile_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_server_config_profile_mock(self, mocker, idrac_server_config_profile_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH_COMP + 'iDRACRedfishAPI',
                                       return_value=idrac_server_config_profile_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_server_config_profile_mock
        return idrac_conn_mock

    def test_execute_one(self, idrac_default_args, idrac_connection_server_config_profile_mock, mocker):
        # Scenario - When 'Custom defaults' is not supported and iDRAC8
        idrac_default_args.update({"command": "export_custom_defaults"})
        idrac_default_args.update({"share_name": LOCAL_SHARE_NAME})
        mocker.patch(MODULE_UTILS_PATH + GET_FIRMWARE_VERSION, return_value="2.81.81")
        mocker.patch(MODULE_PATH_COMP + CHECK_IDRAC_VERSION, return_value=False)
        f_module = self.get_module_mock(params=idrac_default_args)
        scp_obj = self.module.ExportCustomDefaultCommand(idrac_connection_server_config_profile_mock, f_module)
        with pytest.raises(Exception) as exc:
            scp_obj.execute()
        assert exc.value.args[0] == "export_custom_defaults is not supported on this firmware version of iDRAC. Enter the valid values and retry the operation."

        # Scenario - when  export format provided and is not 'XML'
        idrac_default_args.clear()
        idrac_default_args.update({})
        idrac_default_args.update({"command": "export_custom_defaults"})
        idrac_default_args.update({"export_format": "JSON"})
        idrac_default_args.update({"share_name": LOCAL_SHARE_NAME})
        mocker.patch(MODULE_UTILS_PATH + GET_FIRMWARE_VERSION, return_value="7.00.00")
        mocker.patch(MODULE_PATH_COMP + CHECK_IDRAC_VERSION, return_value=True)
        f_module = self.get_module_mock(params=idrac_default_args)
        scp_obj = self.module.ExportCustomDefaultCommand(idrac_connection_server_config_profile_mock, f_module)
        with pytest.raises(Exception) as exc:
            scp_obj.execute()
        assert exc.value.args[0] == "An invalid export format is selected. File format '.xml' is supported. Select a valid file format and retry the operation."

        # Scenario - Export Custom Defaults is successfull
        obj = MagicMock()
        obj.body = self.custom_default_content_enabled
        self.share_details["share_name"] = LOCAL_SHARE_NAME
        self.share_details["file_name"] = FILE_NAME
        idrac_default_args.clear()
        idrac_default_args.update({})
        idrac_default_args.update({"share_name": LOCAL_SHARE_NAME})
        idrac_default_args.update({"scp_file": FILE_NAME})
        idrac_default_args.update({"command": "export_custom_defaults"})
        mocker.patch(MODULE_UTILS_PATH + GET_FIRMWARE_VERSION, return_value="7.00.00")
        mocker.patch(MODULE_PATH_COMP + CHECK_IDRAC_VERSION, return_value=True)
        mocker.patch(MODULE_PATH_COMP + "validate_customdefault_input", return_value=None)
        mocker.patch(MODULE_PATH_COMP + "get_scp_share_details", return_value=(self.share_details, FILE_NAME))
        mocker.patch(MODULE_PATH_COMP + "get_buffer_text", return_value=self.custom_default_content)
        mocker.patch(MODULE_PATH_COMP + "idrac_custom_option", return_value=obj)
        mocker.patch(OPEN_KEY, mocker.mock_open())
        f_module = self.get_module_mock(params=idrac_default_args)
        scp_obj = self.module.ExportCustomDefaultCommand(idrac_connection_server_config_profile_mock, f_module)
        msg_resp, resp = scp_obj.execute()
        assert msg_resp == {'file': 'share//scp_file.xml'}

        # Scenario - Export Custom Defaults operation is successfull but not available
        mocker.patch(MODULE_UTILS_PATH + GET_FIRMWARE_VERSION, return_value="7.00.00")
        mocker.patch(MODULE_PATH_COMP + CHECK_IDRAC_VERSION, return_value=True)
        mocker.patch(MODULE_PATH_COMP + "validate_customdefault_input", return_value=None)
        mocker.patch(MODULE_PATH_COMP + "get_scp_share_details", return_value=(self.share_details, FILE_NAME))
        mocker.patch(MODULE_UTILS_PATH + "get_dynamic_uri", return_value=self.validate_allowed_values)
        mocker.patch(MODULE_PATH_COMP + "get_buffer_text", return_value=self.custom_default_content)
        mocker.patch(MODULE_PATH_COMP + "idrac_custom_option", return_value=None)
        mocker.patch(OPEN_KEY, mocker.mock_open())
        f_module = self.get_module_mock(params=idrac_default_args)
        scp_obj = self.module.ExportCustomDefaultCommand(idrac_connection_server_config_profile_mock, f_module)
        with pytest.raises(Exception) as exc:
            scp_obj.execute()
        assert exc.value.args[0] == "Custom defaults is not available on the iDRAC."
