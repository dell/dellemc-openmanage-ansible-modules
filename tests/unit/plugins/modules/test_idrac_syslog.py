# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.0.0
# Copyright (C) 2018-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_syslog
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible_collections.dellemc.openmanage.tests.unit.compat.mock import MagicMock, patch, Mock
from io import StringIO
from ansible.module_utils._text import to_text
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestSetupSyslog(FakeAnsibleModule):
    module = idrac_syslog

    @pytest.fixture
    def idrac_setup_syslog_mock(self):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.file_share_manager = idrac_obj
        omsdk_mock.config_mgr = idrac_obj
        return idrac_obj

    @pytest.fixture
    def idrac_file_manager_mock(self, mocker):
        try:
            file_manager_obj = mocker.patch(
                MODULE_PATH + 'idrac_syslog.file_share_manager')
        except AttributeError:
            file_manager_obj = MagicMock()
        obj = MagicMock()
        file_manager_obj.create_share_obj.return_value = obj
        return file_manager_obj

    @pytest.fixture
    def idrac_connection_setup_syslog_mock(self, mocker, idrac_setup_syslog_mock):
        idrac_conn_class_mock = mocker.patch(MODULE_PATH +
                                             'idrac_syslog.iDRACConnection', return_value=idrac_setup_syslog_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_setup_syslog_mock
        return idrac_setup_syslog_mock

    def test_main_setup_syslog_success_case01(self, idrac_connection_setup_syslog_mock, idrac_default_args, mocker,
                                              idrac_file_manager_mock):
        idrac_default_args.update({"share_name": "sharename", 'share_password': None, "syslog": "Enabled",
                                   'share_mnt': None, 'share_user': None})
        message = {'changed': False, 'msg': {'Status': "Success", "message": "No changes found to commit!"}}
        mocker.patch(MODULE_PATH +
                     'idrac_syslog.run_setup_idrac_syslog',
                     return_value=message)
        result = self._run_module(idrac_default_args)
        assert result == {'msg': 'Successfully fetch the syslogs.',
                          'syslog_status': {
                              'changed': False,
                              'msg': {'Status': 'Success', 'message': 'No changes found to commit!'}},
                          'changed': False}

    def test_run_setup_idrac_syslog_success_case01(self, idrac_connection_setup_syslog_mock, idrac_default_args,
                                                   idrac_file_manager_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "syslog": "Enabled", "share_password": "sharepassword"})
        message = {"changes_applicable": True, "message": "changes are applicable"}
        idrac_connection_setup_syslog_mock.config_mgr.is_change_applicable.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        msg = self.module.run_setup_idrac_syslog(idrac_connection_setup_syslog_mock, f_module)
        assert msg == {'changes_applicable': True, 'message': 'changes are applicable'}

    def test_run_setup_idrac_syslog_success_case02(self, idrac_connection_setup_syslog_mock, idrac_default_args,
                                                   idrac_file_manager_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "syslog": "Enabled", "share_password": "sharepassword"})
        message = {"changes_applicable": True, "message": "changes found to commit!", "changed": True,
                   "Status": "Success"}
        idrac_connection_setup_syslog_mock.config_mgr.enable_syslog.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_setup_idrac_syslog(idrac_connection_setup_syslog_mock, f_module)
        assert msg == {'Status': 'Success',
                       'changed': True,
                       'changes_applicable': True,
                       'message': 'changes found to commit!'}

    def test_run_setup_idrac_syslog_success_case03(self, idrac_connection_setup_syslog_mock, idrac_default_args,
                                                   idrac_file_manager_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "syslog": "Enabled", "share_password": "sharepassword"})
        message = {"changes_applicable": True, "Message": "No changes found to commit!", "changed": False,
                   "Status": "Success"}
        idrac_connection_setup_syslog_mock.config_mgr.enable_syslog.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_setup_idrac_syslog(idrac_connection_setup_syslog_mock, f_module)
        assert msg == {'Message': 'No changes found to commit!',
                       'Status': 'Success',
                       'changed': False,
                       'changes_applicable': True}

    def test_run_setup_idrac_syslog_success_case04(self, idrac_connection_setup_syslog_mock, idrac_default_args,
                                                   idrac_file_manager_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "syslog": "Disabled", "share_password": "sharepassword"})
        message = {"changes_applicable": True, "Message": "No Changes found to commit!", "changed": False,
                   "Status": "Success"}
        idrac_connection_setup_syslog_mock.config_mgr.disable_syslog.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_setup_idrac_syslog(idrac_connection_setup_syslog_mock, f_module)
        assert msg == {'Message': 'No Changes found to commit!', 'Status': 'Success',
                       'changed': False, 'changes_applicable': True}

    def test_run_setup_syslog_disable_case(self, idrac_connection_setup_syslog_mock, idrac_default_args,
                                           idrac_file_manager_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "syslog": 'Disabled'})
        message = "Disabled"
        idrac_connection_setup_syslog_mock.config_mgr.disable_syslog.return_value = message
        idrac_connection_setup_syslog_mock.config_mgr.is_change_applicable.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        msg = self.module.run_setup_idrac_syslog(idrac_connection_setup_syslog_mock, f_module)
        assert msg == 'Disabled'

    def test_run_setup_syslog_enable_case(self, idrac_connection_setup_syslog_mock, idrac_default_args,
                                          idrac_file_manager_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "syslog": 'Enabled'})
        message = "Enabled"
        idrac_connection_setup_syslog_mock.config_mgr.enable_syslog.return_value = message
        idrac_connection_setup_syslog_mock.config_mgr.is_change_applicable.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        msg = self.module.run_setup_idrac_syslog(idrac_connection_setup_syslog_mock, f_module)
        assert msg == "Enabled"

    def test_run_setup_idrac_syslog_failed_case01(self, idrac_connection_setup_syslog_mock, idrac_default_args,
                                                  idrac_file_manager_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "syslog": "Enable", "share_password": "sharepassword"})
        message = {'Status': 'Failed', "Data": {'Message': 'status failed in checking Data'}}
        idrac_connection_setup_syslog_mock.file_share_manager.create_share_obj.return_value = "mnt/iso"
        idrac_connection_setup_syslog_mock.config_mgr.set_liason_share.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        result = self.module.run_setup_idrac_syslog(idrac_connection_setup_syslog_mock, f_module)
        assert result == idrac_connection_setup_syslog_mock.config_mgr.is_change_applicable()

    def test_run_setup_idrac_syslog_failed_case03(self, idrac_connection_setup_syslog_mock, idrac_default_args,
                                                  idrac_file_manager_mock):
        idrac_default_args.update(
            {"share_name": "dummy_share_name", "share_mnt": "mountname", "share_user": "shareuser",
             "syslog": "Disabled", "share_password": "sharepassword"})
        message = {"message": "No changes were applied", "changed": False,
                   "Status": "failed"}
        idrac_connection_setup_syslog_mock.config_mgr.enable_syslog.return_value = message
        idrac_connection_setup_syslog_mock.config_mgr.disable_syslog.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_setup_idrac_syslog(idrac_connection_setup_syslog_mock, f_module)
        assert msg == {'Status': 'failed', 'changed': False, 'message': 'No changes were applied'}

    @pytest.mark.parametrize("exc_type", [SSLValidationError, URLError, ValueError, TypeError,
                                          ConnectionError, HTTPError])
    def test_main_setup_syslog_exception_handling_case(self, exc_type, mocker, idrac_connection_setup_syslog_mock,
                                                       idrac_default_args, idrac_file_manager_mock):
        idrac_default_args.update({"share_name": "sharename", 'share_password': None,
                                   "syslog": "Enabled", 'share_mnt': None, 'share_user': None})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH +
                         'idrac_syslog.run_setup_idrac_syslog',
                         side_effect=exc_type('test'))
        else:
            mocker.patch(MODULE_PATH +
                         'idrac_syslog.run_setup_idrac_syslog',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
        if not exc_type == URLError:
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result
