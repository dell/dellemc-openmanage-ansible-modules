# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.4.0
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import sys
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_server_config_profile
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants,\
    AnsibleExitJson
from mock import MagicMock, patch, Mock, mock_open
from pytest import importorskip
from ansible.module_utils.six.moves.urllib.parse import urlparse, ParseResult
MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")


class TestServerConfigProfile(FakeAnsibleModule):
    module = idrac_server_config_profile

    @pytest.fixture
    def idrac_server_configure_profile_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.file_share_manager = idrac_obj
        omsdk_mock.config_mgr = idrac_obj
        return idrac_obj

    @pytest.fixture
    def idrac_file_manager_server_config_profile_mock(self, mocker):
        try:
            file_manager_obj = mocker.patch(
                MODULE_PATH + 'idrac_server_config_profile.file_share_manager')
        except AttributeError:
            file_manager_obj = MagicMock()
        obj = MagicMock()
        file_manager_obj.create_share_obj.return_value = obj
        return file_manager_obj

    @pytest.fixture
    def idrac_scp_redfish_mock(self, mocker, idrac_server_configure_profile_mock):
        idrac_conn_class_mock = mocker.patch(MODULE_PATH + 'idrac_server_config_profile.iDRACRedfishAPI',
                                             return_value=idrac_server_configure_profile_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_server_configure_profile_mock
        return idrac_server_configure_profile_mock

    def test_run_export_import_http(self, idrac_scp_redfish_mock, idrac_default_args, mocker):
        idrac_default_args.update({"share_name": "192.168.0.1:/share", "share_user": "sharename",
                                   "share_password": "sharepswd", "command": "export",
                                   "job_wait": True, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml", "end_host_power_state": "On",
                                   "shutdown_type": "Graceful", "export_format": "XML", "export_use": "Default"})
        f_module = self.get_module_mock(params=idrac_default_args)
        export_response = {"msg": "Successfully exported the Server Configuration Profile.",
                           "scp_status": {"Name": "Export: Server Configuration Profile", "PercentComplete": 100,
                                          "TaskState": "Completed", "TaskStatus": "OK", "Id": "JID_236654661194"}}
        mocker.patch(MODULE_PATH + "idrac_server_config_profile.urlparse",
                     return_value=ParseResult(scheme='http', netloc='192.168.0.1',
                                              path='/share/',
                                              params='', query='', fragment=''))
        mocker.patch(MODULE_PATH + "idrac_server_config_profile.response_format_change",
                     return_value=export_response)
        result = self.module.run_export_import_scp_http(idrac_scp_redfish_mock, f_module)
        assert result["msg"] == "Successfully exported the Server Configuration Profile."
        idrac_default_args.update({"command": "import"})
        f_module = self.get_module_mock(params=idrac_default_args)
        import_response = {"msg": "Successfully imported the Server Configuration Profile.",
                           "scp_status": {"Name": "Import: Server Configuration Profile", "PercentComplete": 100,
                                          "TaskState": "Completed", "TaskStatus": "OK", "Id": "JID_236654661194"}}
        mocker.patch(MODULE_PATH + "idrac_server_config_profile.response_format_change",
                     return_value=import_response)
        result = self.module.run_export_import_scp_http(idrac_scp_redfish_mock, f_module)
        assert result["msg"] == "Successfully imported the Server Configuration Profile."

    def test_http_share_msg_main(self, idrac_scp_redfish_mock, idrac_default_args, mocker):
        idrac_default_args.update({"share_name": "http://192.168.0.1:/share", "share_user": "sharename",
                                   "share_password": "sharepswd", "command": "import",
                                   "job_wait": False, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml", "end_host_power_state": "On",
                                   "shutdown_type": "Graceful", "export_format": "XML",
                                   "export_use": "Default", "validate_certs": False})
        share_return = {"Oem": {"Dell": {"MessageId": "SYS069"}}}
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.run_export_import_scp_http',
                     return_value=share_return)
        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Successfully triggered the job to import the Server Configuration Profile."
        share_return = {"Oem": {"Dell": {"MessageId": "SYS053"}}}
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.run_export_import_scp_http',
                     return_value=share_return)
        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Successfully triggered the job to import the Server Configuration Profile."
        idrac_default_args.update({"command": "export"})
        share_return = {"Oem": {"Dell": {"MessageId": "SYS043"}}}
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.run_export_import_scp_http',
                     return_value=share_return)
        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Successfully triggered the job to export the Server Configuration Profile."

    def test_export_scp_redfish(self, idrac_scp_redfish_mock, idrac_default_args, mocker):
        idrac_default_args.update({"share_name": "192.168.0.1:/share", "share_user": "sharename",
                                   "share_password": "sharepswd", "command": "import",
                                   "job_wait": False, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml", "end_host_power_state": "On",
                                   "shutdown_type": "Graceful", "export_format": "XML",
                                   "export_use": "Default", "validate_certs": False})
        f_module = self.get_module_mock(params=idrac_default_args)
        share_return = {"Oem": {"Dell": {"MessageId": "SYS069"}}}
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.run_export_import_scp_http',
                     return_value=share_return)
        f_module.check_mode = False
        result = self.module.export_scp_redfish(f_module, idrac_scp_redfish_mock)
        assert result["file"] == "192.168.0.1:/share/scp_file.xml"
        idrac_default_args.update({"share_name": "\\\\100.96.16.123\\cifsshare"})
        result = self.module.export_scp_redfish(f_module, idrac_scp_redfish_mock)
        assert result["file"] == "\\\\100.96.16.123\\cifsshare\\scp_file.xml"
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.response_format_change',
                     return_value={"TaskStatus": "Critical"})
        with pytest.raises(Exception) as ex:
            self.module.export_scp_redfish(f_module, idrac_scp_redfish_mock)
        assert ex.value.args[0] == "Failed to import scp."

    def test_response_format_change(self, idrac_scp_redfish_mock, idrac_default_args):
        idrac_default_args.update({"share_name": "192.168.0.1:/share", "share_user": "sharename",
                                   "share_password": "sharepswd", "command": "import",
                                   "job_wait": True, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml", "end_host_power_state": "On",
                                   "shutdown_type": "Graceful", "export_format": "XML",
                                   "export_use": "Default", "validate_certs": False})
        f_module = self.get_module_mock(params=idrac_default_args)
        idrac_scp_redfish_mock.json_data = {"Oem": {"Dell": {"key": "value"}}}
        result = self.module.response_format_change(idrac_scp_redfish_mock, f_module, "export_scp.yml")
        assert result["key"] == "value"
        idrac_default_args.update({"command": "export"})
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.response_format_change(idrac_scp_redfish_mock, f_module, "export_scp.yml")
        assert result["key"] == "value"

    def test_preview_scp_redfish(self, idrac_scp_redfish_mock, idrac_default_args, mocker):
        idrac_default_args.update({"share_name": "192.168.0.1:/nfsshare", "share_user": "sharename",
                                   "share_password": "sharepswd", "command": "preview", "job_wait": True,
                                   "scp_components": "IDRAC", "scp_file": "scp_file.xml",
                                   "end_host_power_state": "On", "shutdown_type": "Graceful", "export_format": "XML",
                                   "export_use": "Default", "validate_certs": False, "idrac_port": 443})
        f_module = self.get_module_mock(params=idrac_default_args)
        share = {"share_ip": "192.168.0.1", "share_user": "sharename", "share_password": "password",
                 "job_wait": True}
        f_module.check_mode = False
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.get_scp_share_details',
                     return_value=(share, "scp_file.xml"))
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.response_format_change',
                     return_value={"Status": "Success"})
        result = self.module.preview_scp_redfish(f_module, idrac_scp_redfish_mock, True, import_job_wait=False)
        assert result["Status"] == "Success"
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.response_format_change',
                     return_value={"TaskStatus": "Critical"})
        with pytest.raises(Exception) as ex:
            self.module.import_scp_redfish(f_module, idrac_scp_redfish_mock, True)
        assert ex.value.args[0] == "Failed to preview scp."
        idrac_default_args.update({"share_name": "192.168.0.1:/nfsshare", "share_user": "sharename",
                                   "share_password": "sharepswd", "command": "preview", "job_wait": True,
                                   "scp_components": "IDRAC", "scp_file": "scp_file.xml",
                                   "end_host_power_state": "On", "shutdown_type": "Graceful", "export_format": "XML",
                                   "export_use": "Default", "validate_certs": False, "idrac_port": 443})
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        share = {"share_ip": "192.168.0.1", "share_user": "sharename", "share_password": "password",
                 "job_wait": True, "share_type": "LOCAL", "share_name": "share_name"}
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.get_scp_share_details',
                     return_value=(share, "scp_file.xml"))
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.exists',
                     return_value=False)
        with pytest.raises(Exception) as ex:
            self.module.import_scp_redfish(f_module, idrac_scp_redfish_mock, False)
        assert ex.value.args[0] == "Invalid file path provided."

    def test_import_scp_redfish(self, idrac_scp_redfish_mock, idrac_default_args, mocker):
        idrac_default_args.update({"share_name": "192.168.0.1:/share", "share_user": "sharename",
                                   "share_password": "sharepswd", "command": "import",
                                   "job_wait": True, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml", "end_host_power_state": "On",
                                   "shutdown_type": "Graceful", "export_format": "XML",
                                   "export_use": "Default", "validate_certs": False, "idrac_port": 443})
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = True
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.preview_scp_redfish',
                     return_value={"MessageId": "SYS081"})
        with pytest.raises(Exception) as ex:
            self.module.import_scp_redfish(f_module, idrac_scp_redfish_mock, True)
        assert ex.value.args[0] == "Changes found to be applied."
        idrac_default_args.update({"share_name": "http://192.168.0.1/http-share", "share_user": "sharename",
                                   "share_password": "sharepswd", "command": "import",
                                   "job_wait": True, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml", "end_host_power_state": "On",
                                   "shutdown_type": "Graceful", "export_format": "XML",
                                   "export_use": "Default", "validate_certs": False, "idrac_port": 443})
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.response_format_change',
                     return_value={"Status": "Success"})
        result = self.module.import_scp_redfish(f_module, idrac_scp_redfish_mock, True)
        assert result["Status"] == "Success"
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.response_format_change',
                     return_value={"TaskStatus": "Critical"})
        with pytest.raises(Exception) as ex:
            self.module.import_scp_redfish(f_module, idrac_scp_redfish_mock, True)
        assert ex.value.args[0] == "Failed to import scp."
        idrac_default_args.update({"share_name": "local-share", "share_user": "sharename",
                                   "share_password": "sharepswd", "command": "import",
                                   "job_wait": True, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml", "end_host_power_state": "On",
                                   "shutdown_type": "Graceful", "export_format": "XML",
                                   "export_use": "Default", "validate_certs": False, "idrac_port": 443})
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        share = {"share_ip": "192.168.0.1", "share_user": "sharename", "share_password": "password",
                 "job_wait": True, "share_type": "LOCAL", "share_name": "share_name"}
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.get_scp_share_details',
                     return_value=(share, "scp_file.xml"))
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.exists',
                     return_value=False)
        with pytest.raises(Exception) as ex:
            self.module.import_scp_redfish(f_module, idrac_scp_redfish_mock, False)
        assert ex.value.args[0] == "Invalid file path provided."

    def test_get_scp_file_format(self, idrac_scp_redfish_mock, idrac_default_args):
        idrac_default_args.update({"share_name": "192.168.0.1:/share", "share_user": "sharename",
                                   "share_password": "sharepswd", "command": "import",
                                   "job_wait": True, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml", "end_host_power_state": "On",
                                   "shutdown_type": "Graceful", "export_format": "XML",
                                   "export_use": "Default", "validate_certs": False, "idrac_port": 443})
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.get_scp_file_format(f_module)
        assert result == "scp_file.xml"
        idrac_default_args.update({"scp_file": None})
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.get_scp_file_format(f_module)
        assert result.startswith("idrac_ip_") is True

    def test_main_success_case(self, idrac_scp_redfish_mock, idrac_default_args, mocker):
        idrac_default_args.update({"share_name": "http://192.168.0.1/http-share", "share_user": "sharename",
                                   "share_password": "sharepswd", "command": "import",
                                   "job_wait": True, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml", "end_host_power_state": "On",
                                   "shutdown_type": "Graceful", "export_format": "XML",
                                   "export_use": "Default", "validate_certs": False, "idrac_port": 443})
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.run_export_import_scp_http',
                     return_value={"MessageId": "SYS069"})
        result = self._run_module(idrac_default_args)
        assert result["scp_status"] == {'MessageId': 'SYS069'}
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.run_export_import_scp_http',
                     return_value={"MessageId": "SYS053"})
        result = self._run_module(idrac_default_args)
        assert result["scp_status"] == {'MessageId': 'SYS053'}
        idrac_default_args.update({"share_name": "192.168.0.1:/nfsshare"})
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.import_scp_redfish',
                     return_value={"Message": "No changes were applied since the current component configuration "
                                              "matched the requested configuration"})
        result = self._run_module(idrac_default_args)
        assert result["changed"] is False
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.import_scp_redfish',
                     return_value={"MessageId": "SYS043"})
        result = self._run_module(idrac_default_args)
        assert result["scp_status"] == {'MessageId': 'SYS043'}
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.import_scp_redfish',
                     return_value={"MessageId": "SYS069"})
        result = self._run_module(idrac_default_args)
        assert result["scp_status"] == {'MessageId': 'SYS069'}
        idrac_default_args.update({"command": "export"})
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.export_scp_redfish',
                     return_value={"Status": "Success"})
        result = self._run_module(idrac_default_args)
        assert result["scp_status"] == {'Status': 'Success'}
        idrac_default_args.update({"command": "preview"})
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.preview_scp_redfish',
                     return_value={"MessageId": "SYS081"})
        result = self._run_module(idrac_default_args)
        assert result["scp_status"] == {"MessageId": "SYS081"}

    def test_get_scp_share_details(self, idrac_scp_redfish_mock, idrac_default_args, mocker):
        idrac_default_args.update({"share_name": "/local-share", "share_user": "sharename",
                                   "share_password": "sharepswd", "command": "export",
                                   "job_wait": True, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml", "end_host_power_state": "On",
                                   "shutdown_type": "Graceful", "export_format": "XML",
                                   "export_use": "Default", "validate_certs": False, "idrac_port": 443})
        f_module = self.get_module_mock(params=idrac_default_args)
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.get_scp_file_format',
                     return_value="export_scp.xml")
        result = self.module.get_scp_share_details(f_module)
        assert result[1] == "export_scp.xml"

    def test_wait_for_response(self, idrac_scp_redfish_mock, idrac_default_args, mocker):
        idrac_default_args.update({"share_name": "/local-share", "share_user": "sharename",
                                   "share_password": "sharepswd", "command": "export",
                                   "job_wait": False, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml", "end_host_power_state": "On",
                                   "shutdown_type": "Graceful", "export_format": "XML",
                                   "export_use": "Default", "validate_certs": False, "idrac_port": 443})
        f_module = self.get_module_mock(params=idrac_default_args)
        idrac_scp_redfish_mock.headers = {"Location": "/redfish/v1/TaskService/Tasks/JID_123456789"}
        resp_return_value = {"return_data": b"<SystemConfiguration Model='PowerEdge MX840c'>"
                                            b"<Component FQDD='System.Embedded.1'>"
                                            b"<Attribute Name='Backplane.1#BackplaneSplitMode'>0</Attribute>"
                                            b"</Component> </SystemConfiguration>",
                             "return_job": {"JobState": "Completed", "JobType": "ExportConfiguration",
                                            "PercentComplete": 100, "Status": "Success"}}
        idrac_scp_redfish_mock.wait_for_job_complete.return_value = resp_return_value["return_data"]
        idrac_scp_redfish_mock.job_resp = resp_return_value["return_job"]
        share = {"share_name": "/local_share", "file_name": "export_file.xml"}
        if sys.version_info.major == 3:
            builtin_module_name = 'builtins'
        else:
            builtin_module_name = '__builtin__'
        with patch("{0}.open".format(builtin_module_name), mock_open(read_data=resp_return_value["return_data"])) as mock_file:
            result = self.module.wait_for_response(idrac_scp_redfish_mock, f_module, share, idrac_scp_redfish_mock)
        assert result.job_resp == resp_return_value["return_job"]

    def test_wait_for_response_json(self, idrac_scp_redfish_mock, idrac_default_args, mocker):
        idrac_default_args.update({"share_name": "/local-share", "share_user": "sharename",
                                   "share_password": "sharepswd", "command": "export",
                                   "job_wait": False, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml", "end_host_power_state": "On",
                                   "shutdown_type": "Graceful", "export_format": "JSON",
                                   "export_use": "Default", "validate_certs": False, "idrac_port": 443})
        f_module = self.get_module_mock(params=idrac_default_args)
        resp_return_value = {"return_data": {
            "SystemConfiguration": {"Components": [
                {"FQDD": "SupportAssist.Embedded.1",
                 "Attributes": [{"Name": "SupportAssist.1#SupportAssistEULAAccepted"}]
                 }]}
        },
            "return_job": {"JobState": "Completed", "JobType": "ExportConfiguration",
                           "PercentComplete": 100, "Status": "Success"}}
        mock_scp_json_data = idrac_scp_redfish_mock
        mock_scp_json_data.json_data = resp_return_value["return_data"]
        idrac_scp_redfish_mock.wait_for_job_complete.return_value = mock_scp_json_data
        idrac_scp_redfish_mock.job_resp = resp_return_value["return_job"]
        share = {"share_name": "/local_share", "file_name": "export_file.xml"}
        if sys.version_info.major == 3:
            builtin_module_name = 'builtins'
        else:
            builtin_module_name = '__builtin__'
        with patch("{0}.open".format(builtin_module_name), mock_open(read_data=str(resp_return_value["return_data"]))) as mock_file:
            result = self.module.wait_for_response(idrac_scp_redfish_mock, f_module, share, idrac_scp_redfish_mock)
        assert result.job_resp == resp_return_value["return_job"]
