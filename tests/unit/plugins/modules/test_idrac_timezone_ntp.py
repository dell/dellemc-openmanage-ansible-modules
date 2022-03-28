# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.2.0
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_timezone_ntp
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from mock import MagicMock, patch, Mock, PropertyMock
from io import StringIO
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestConfigTimezone(FakeAnsibleModule):
    module = idrac_timezone_ntp

    @pytest.fixture
    def idrac_configure_timezone_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.file_share_manager = idrac_obj
        omsdk_mock.config_mgr = idrac_obj
        type(idrac_obj).create_share_obj = Mock(return_value="servicesstatus")
        type(idrac_obj).set_liason_share = Mock(return_value="servicestatus")
        return idrac_obj

    @pytest.fixture
    def idrac_file_manager_config_timesone_mock(self, mocker):
        try:
            file_manager_obj = mocker.patch(
                MODULE_PATH + 'idrac_timezone_ntp.file_share_manager')
        except AttributeError:
            file_manager_obj = MagicMock()
        obj = MagicMock()
        file_manager_obj.create_share_obj.return_value = obj
        return file_manager_obj

    @pytest.fixture
    def idrac_connection_configure_timezone_mock(self, mocker, idrac_configure_timezone_mock):
        idrac_conn_class_mock = mocker.patch(MODULE_PATH +
                                             'idrac_timezone_ntp.iDRACConnection',
                                             return_value=idrac_configure_timezone_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_configure_timezone_mock
        return idrac_configure_timezone_mock

    def test_main_idrac_timezone_config_success_Case(self, idrac_connection_configure_timezone_mock, idrac_default_args,
                                                     mocker, idrac_file_manager_config_timesone_mock):
        idrac_default_args.update({"share_name": "sharename"})
        message = {'changed': False, 'msg': {'Status': "Success", "message": "No changes found to commit!"}}
        mocker.patch(MODULE_PATH +
                     'idrac_timezone_ntp.run_idrac_timezone_config', return_value=(message, False))
        result = self._run_module(idrac_default_args)
        assert result == {'msg': 'Successfully configured the iDRAC time settings.',
                          'timezone_ntp_status': (
                              {'changed': False,
                               'msg': {'Status': 'Success', 'message': 'No changes found to commit!'}},
                              False), 'changed': False}

    def test_run_idrac_timezone_config_success_case01(self, idrac_connection_configure_timezone_mock,
                                                      idrac_default_args, idrac_file_manager_config_timesone_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "setup_idrac_timezone": "setuptimezone",
                                   "enable_ntp": "Enabled", "ntp_server_1": "ntp server1",
                                   "ntp_server_2": "ntp server2", "ntp_server_3": "ntp server3"})
        message = {"changes_applicable": True, "message": "changes are applicable"}
        idrac_connection_configure_timezone_mock.config_mgr.is_change_applicable.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        msg = self.module.run_idrac_timezone_config(idrac_connection_configure_timezone_mock, f_module)
        assert msg == {'changes_applicable': True, 'message': 'changes are applicable'}

    def test_run_idrac_timezone_config_success_case02(self, idrac_connection_configure_timezone_mock,
                                                      idrac_default_args, idrac_file_manager_config_timesone_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "setup_idrac_timezone": "setuptimezone",
                                   "enable_ntp": "Enabled", "ntp_server_1": "ntp server1",
                                   "ntp_server_2": "ntp server2", "ntp_server_3": "ntp server3"})
        message = {"changes_applicable": True, "message": "changes found to commit!", "changed": True,
                   "Status": "Success"}
        idrac_connection_configure_timezone_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_idrac_timezone_config(idrac_connection_configure_timezone_mock, f_module)
        assert msg == {'Status': 'Success',
                       'changed': True,
                       'changes_applicable': True,
                       'message': 'changes found to commit!'}

    def test_run_idrac_timezone_config_success_case03(self, idrac_connection_configure_timezone_mock,
                                                      idrac_default_args, idrac_file_manager_config_timesone_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "setup_idrac_timezone": "setuptimezone",
                                   "enable_ntp": "Enabled", "ntp_server_1": "ntp server1",
                                   "ntp_server_2": "ntp server2", "ntp_server_3": "ntp server3"})
        message = {"changes_applicable": False, "Message": "No changes found to commit!", "changed": False,
                   "Status": "Success"}
        idrac_connection_configure_timezone_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_idrac_timezone_config(idrac_connection_configure_timezone_mock, f_module)
        assert msg == {'Message': 'No changes found to commit!',
                       'Status': 'Success',
                       'changed': False,
                       'changes_applicable': False}

    def test_run_idrac_timezone_config_success_case04(self, idrac_connection_configure_timezone_mock,
                                                      idrac_default_args, idrac_file_manager_config_timesone_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "setup_idrac_timezone": "setuptimezone",
                                   "enable_ntp": "Enabled", "ntp_server_1": "ntp server1",
                                   "ntp_server_2": "ntp server2", "ntp_server_3": "ntp server3"})
        message = {"changes_applicable": False, "Message": "No changes found to commit!", "changed": False,
                   "Status": "Success"}
        idrac_connection_configure_timezone_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_idrac_timezone_config(idrac_connection_configure_timezone_mock, f_module)
        assert msg == {'Message': 'No changes found to commit!',
                       'Status': 'Success',
                       'changed': False,
                       'changes_applicable': False}

    def test_run_idrac_timezone_config_success_case05(self, idrac_connection_configure_timezone_mock,
                                                      idrac_default_args, idrac_file_manager_config_timesone_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "setup_idrac_timezone": None,
                                   "enable_ntp": None, "ntp_server_1": None, "ntp_server_2": None,
                                   "ntp_server_3": None})
        message = {"changes_applicable": False, "Message": "No changes found to commit!", "changed": False,
                   "Status": "Success"}
        idrac_connection_configure_timezone_mock.config_mgr.configure_timezone.return_value = message
        idrac_connection_configure_timezone_mock.config_mgr.configure_ntp.return_value = message
        idrac_connection_configure_timezone_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_idrac_timezone_config(idrac_connection_configure_timezone_mock, f_module)
        assert msg == {'Message': 'No changes found to commit!',
                       'Status': 'Success',
                       'changed': False,
                       'changes_applicable': False}

    def test_run_idrac_timezone_config_failed_case01(self, idrac_connection_configure_timezone_mock,
                                                     idrac_default_args, idrac_file_manager_config_timesone_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "setup_idrac_timezone": "setuptimezone",
                                   "enable_ntp": "Enabled", "ntp_server_1": "ntp server1",
                                   "ntp_server_2": "ntp server2", "ntp_server_3": "ntp server3"})
        message = {'Status': 'Failed', "Data": {'Message': 'status failed in checking Data'}}
        idrac_connection_configure_timezone_mock.file_share_manager.create_share_obj.return_value = "mnt/iso"
        idrac_connection_configure_timezone_mock.config_mgr.set_liason_share.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        result = self.module.run_idrac_timezone_config(idrac_connection_configure_timezone_mock, f_module)
        assert result == idrac_connection_configure_timezone_mock.config_mgr.is_change_applicable()

    def test_run_idrac_timezone_config_failed_case02(self, idrac_connection_configure_timezone_mock,
                                                     idrac_default_args, idrac_file_manager_config_timesone_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "setup_idrac_timezone": "setuptimezone",
                                   "enable_ntp": "Enabled", "ntp_server_1": "ntp server1",
                                   "ntp_server_2": "ntp server2", "ntp_server_3": "ntp server3"})
        message = {"changes_applicable": False, "Message": "No changes were applied", "changed": False,
                   "Status": "failed"}
        idrac_connection_configure_timezone_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_idrac_timezone_config(idrac_connection_configure_timezone_mock, f_module)
        assert msg == {'Message': 'No changes were applied',
                       'Status': 'failed',
                       'changed': False,
                       'changes_applicable': False}

    def test_run_idrac_timezone_config_failed_case03(self, idrac_connection_configure_timezone_mock,
                                                     idrac_default_args, idrac_file_manager_config_timesone_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "setup_idrac_timezone": "setuptimezone",
                                   "enable_ntp": "Enabled", "ntp_server_1": "ntp server1",
                                   "ntp_server_2": "ntp server2", "ntp_server_3": "ntp server3"})
        message = {'Status': 'Failed', "Data": {'Message': "Failed to found changes"}}
        idrac_connection_configure_timezone_mock.file_share_manager.create_share_obj.return_value = "mnt/iso"
        idrac_connection_configure_timezone_mock.config_mgr.set_liason_share.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        msg = self.module.run_idrac_timezone_config(idrac_connection_configure_timezone_mock, f_module)
        assert msg == idrac_connection_configure_timezone_mock.config_mgr.is_change_applicable()

    @pytest.mark.parametrize("exc_type", [RuntimeError, SSLValidationError, ConnectionError, KeyError,
                                          ImportError, ValueError, TypeError, HTTPError, URLError])
    def test_main_idrac_configure_timezone_exception_handling_case(self, exc_type, mocker, idrac_default_args,
                                                                   idrac_connection_configure_timezone_mock,
                                                                   idrac_file_manager_config_timesone_mock):
        idrac_default_args.update({"share_name": "sharename"})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(
                MODULE_PATH + 'idrac_timezone_ntp.run_idrac_timezone_config',
                side_effect=exc_type('test'))
        else:
            mocker.patch(
                MODULE_PATH + 'idrac_timezone_ntp.run_idrac_timezone_config',
                side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                     {"accept-type": "application/json"}, StringIO(json_str)))
        if not exc_type == URLError:
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result
