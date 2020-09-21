# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.2
# Copyright (C) 2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_server_config_profile
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible_collections.dellemc.openmanage.tests.unit.compat.mock import MagicMock, patch, Mock
from pytest import importorskip

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
    def idrac_connection_server_configure_profile_mock(self, mocker, idrac_server_configure_profile_mock):
        idrac_conn_class_mock = mocker.patch(MODULE_PATH + 'idrac_server_config_profile.iDRACConnection',
                                             return_value=idrac_server_configure_profile_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_server_configure_profile_mock
        return idrac_server_configure_profile_mock

    def test_main_idrac_server_config_profile_import_success_Case01(
            self, idrac_connection_server_configure_profile_mock, idrac_default_args, mocker,
            idrac_file_manager_server_config_profile_mock):
        idrac_default_args.update({"share_name": "sharename", "share_user": "sharename", "share_password": "sharepswd",
                                   "command": "import", "job_wait": True, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml"})
        message = {"Status": "Success"}
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.run_import_server_config_profile',
                     return_value=message)
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.run_export_server_config_profile',
                     return_value=("export_status"))
        result = self._run_module(idrac_default_args)
        assert result == {'msg': 'Successfully imported the Server Configuration Profile.',
                          'scp_status': {'Status': 'Success'},
                          'changed': True}

    def test_main_idrac_server_config_profile_import_success_Case02(
            self, idrac_connection_server_configure_profile_mock, idrac_default_args, mocker,
            idrac_file_manager_server_config_profile_mock):
        idrac_default_args.update({"share_name": "sharename", "share_user": "sharename", "share_password": "sharepswd",
                                   "command": "import", "job_wait": False, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml"})
        message = {"Status": "Success"}
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.run_import_server_config_profile',
                     return_value=message)
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.run_export_server_config_profile',
                     return_value=("export_status"))
        result = self._run_module(idrac_default_args)
        assert result == {'changed': True,
                          'msg': 'Successfully triggered the job to import the Server Configuration Profile.',
                          'scp_status': {'Status': 'Success'}}

    def test_main_idrac_server_config_profile_export_success_Case01(
            self, idrac_connection_server_configure_profile_mock, idrac_default_args, mocker,
            idrac_file_manager_server_config_profile_mock):
        idrac_default_args.update({"share_name": "sharename", "share_user": "sharename", "share_password": "sharepswd",
                                   "command": "export", "job_wait": True, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml"})
        message = {"Status": "Success"}
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.run_import_server_config_profile',
                     return_value=("import_status"))
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.run_export_server_config_profile',
                     return_value=message)
        result = self._run_module(idrac_default_args)
        assert result == {'msg': 'Successfully exported the Server Configuration Profile.',
                          'scp_status': {'Status': 'Success'},
                          'changed': False}

    def test_main_idrac_server_config_profile_export_success_Case02(
            self, idrac_connection_server_configure_profile_mock, idrac_default_args, mocker,
            idrac_file_manager_server_config_profile_mock):
        idrac_default_args.update({"share_name": "sharename", "share_user": "sharename", "share_password": "sharepswd",
                                   "command": "export", "job_wait": False, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml"})
        message = {"Status": "Success"}
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.run_import_server_config_profile',
                     return_value=("import_status"))
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.run_export_server_config_profile',
                     return_value=message)
        result = self._run_module(idrac_default_args)
        assert result == {'changed': False,
                          'msg': 'Successfully triggered the job to export the Server Configuration Profile.',
                          'scp_status': {'Status': 'Success'}}

    @pytest.mark.parametrize("exc_type", [ImportError, ValueError, RuntimeError])
    def test_main_idrac_server_config_profile_exception_handling_case(
            self, exc_type, mocker, idrac_default_args, idrac_connection_server_configure_profile_mock,
            idrac_file_manager_server_config_profile_mock):
        idrac_default_args.update({"share_name": "sharename", "share_user": "sharename", "share_password": "sharepswd",
                                   "command": "export", "job_wait": True, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml"})
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.run_import_server_config_profile',
                     side_effect=exc_type('test'))
        mocker.patch(MODULE_PATH + 'idrac_server_config_profile.run_export_server_config_profile',
                     side_effect=exc_type('test'))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True

    def test_run_import_server_config_profile_success_case(
            self, idrac_connection_server_configure_profile_mock, idrac_default_args,
            idrac_file_manager_server_config_profile_mock):
        idrac_default_args.update({"share_name": "sharename", "share_user": "sharename", "share_password": "sharepswd",
                                   "command": "export", "job_wait": True, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml", "end_host_power_state": "On",
                                   "shutdown_type": "Graceful"})
        message = {"Status": "Success"}
        f_module = self.get_module_mock(params=idrac_default_args)
        idrac_connection_server_configure_profile_mock.config_mgr.scp_import.return_value = message
        result = self.module.run_import_server_config_profile(idrac_connection_server_configure_profile_mock, f_module)
        assert result == {"Status": "Success"}

    def test_run_import_server_config_profile_runtimeerror_case(
            self, idrac_connection_server_configure_profile_mock, idrac_default_args,
            idrac_file_manager_server_config_profile_mock):
        idrac_default_args.update({"share_name": "sharename", "share_user": "sharename", "share_password": "sharepswd",
                                   "command": "export", "job_wait": True, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml", "end_host_power_state": "On",
                                   "shutdown_type": "Graceful"})
        message = {"Status": "Failed"}
        f_module = self.get_module_mock(params=idrac_default_args)
        obj = MagicMock()
        idrac_connection_server_configure_profile_mock.config_mgr = obj
        obj.scp_import = Mock(return_value=message)
        with pytest.raises(Exception) as ex:
            self.module.run_import_server_config_profile(idrac_connection_server_configure_profile_mock, f_module)
        assert "Failed to import scp." == str(ex.value)

    def test_run_export_server_config_profile_success_case(
            self, idrac_connection_server_configure_profile_mock, idrac_default_args,
            idrac_file_manager_server_config_profile_mock):
        idrac_default_args.update({"share_name": "sharename", "share_user": "sharename", "share_password": "sharepswd",
                                   "command": "export", "job_wait": True, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml", "end_host_power_state": "On",
                                   "shutdown_type": "Graceful", "export_format": "XML", "export_use": "Default"})
        message = {"Status": "Success"}
        f_module = self.get_module_mock(params=idrac_default_args)
        idrac_connection_server_configure_profile_mock.config_mgr.scp_export.return_value = message
        result = self.module.run_export_server_config_profile(idrac_connection_server_configure_profile_mock, f_module)
        assert result == {"Status": "Success"}

    def test_run_export_server_config_profile_runtimeerror_case(
            self, idrac_connection_server_configure_profile_mock, idrac_default_args,
            idrac_file_manager_server_config_profile_mock):
        idrac_default_args.update({"share_name": "sharename", "share_user": "sharename", "share_password": "sharepswd",
                                   "command": "export", "job_wait": True, "scp_components": "IDRAC",
                                   "scp_file": "scp_file.xml", "end_host_power_state": "On",
                                   "shutdown_type": "Graceful", "export_format": "XML", "export_use": "Default"})
        message = {"Status": "Failed"}
        f_module = self.get_module_mock(params=idrac_default_args)
        obj = MagicMock()
        idrac_connection_server_configure_profile_mock.config_mgr = obj
        obj.scp_export = Mock(return_value=message)
        with pytest.raises(Exception) as ex:
            self.module.run_export_server_config_profile(idrac_connection_server_configure_profile_mock, f_module)
        assert "Failed to export scp." == str(ex.value)
