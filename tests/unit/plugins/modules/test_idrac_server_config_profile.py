# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.4.0
# Copyright (C) 2020-2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import mock
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_server_config_profile
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from mock import MagicMock
MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
SUCCESS_MSG = 'Successfully {0}ed the Server Configuration Profile'
JOB_SUCCESS_MSG = 'Successfully triggered the job to {0} the Server Configuration Profile'
PREVIEW_SUCCESS_MSG = 'Successfully previewed the Server Configuration Profile'
CHANGES_FOUND = "Changes found to be applied."
NO_CHANGES_FOUND = "No changes found to be applied."
REDFISH_JOB_TRACKING = "idrac_server_config_profile.idrac_redfish_job_tracking"


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
                     "scp_components": "IDRAC", "scp_file": "scp_file.xml",
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
        mocker.patch("builtins.open", mocker.mock_open())
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
        mocker.patch("builtins.open", mocker.mock_open())
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
