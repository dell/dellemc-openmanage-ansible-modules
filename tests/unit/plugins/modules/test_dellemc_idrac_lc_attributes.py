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
from ansible_collections.dellemc.openmanage.plugins.modules import dellemc_idrac_lc_attributes
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from mock import MagicMock, patch, Mock
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")


class TestLcAttributes(FakeAnsibleModule):
    module = dellemc_idrac_lc_attributes

    @pytest.fixture
    def idrac_lc_attributes_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.file_share_manager = idrac_obj
        omsdk_mock.config_mgr = idrac_obj
        type(idrac_obj).create_share_obj = Mock(return_value="Status")
        type(idrac_obj).set_liason_share = Mock(return_value="Status")
        return idrac_obj

    @pytest.fixture
    def idrac_connection_lc_attribute_mock(self, mocker, idrac_lc_attributes_mock):
        idrac_conn_class_mock = mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                                             'dellemc_idrac_lc_attributes.iDRACConnection',
                                             return_value=idrac_lc_attributes_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_lc_attributes_mock
        return idrac_lc_attributes_mock

    @pytest.fixture
    def idrac_file_manager_lc_attribute_mock(self, mocker):
        try:
            file_manager_obj = mocker.patch(
                'ansible_collections.dellemc.openmanage.plugins.modules.dellemc_idrac_lc_attributes.file_share_manager')
        except AttributeError:
            file_manager_obj = MagicMock()
        obj = MagicMock()
        file_manager_obj.create_share_obj.return_value = obj
        return file_manager_obj

    def test_main_lc_attributes_success_case01(self, idrac_connection_lc_attribute_mock,
                                               idrac_default_args, mocker, idrac_file_manager_lc_attribute_mock):
        idrac_default_args.update({"share_name": "sharename", 'share_password': None,
                                   'csior': 'Enabled', 'share_mnt': None, 'share_user': None})
        message = {'changed': False, 'msg': {'Status': "Success", "message": "No changes found to commit!"}}
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.dellemc_idrac_lc_attributes.run_setup_idrac_csior',
                     return_value=message)
        with pytest.raises(Exception) as ex:
            self._run_module(idrac_default_args)
        assert ex.value.args[0]['msg'] == "Failed to configure the iDRAC LC attributes."

    def test_run_setup_idrac_csior_success_case01(self, idrac_connection_lc_attribute_mock, idrac_default_args,
                                                  idrac_file_manager_lc_attribute_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "csior": "csior"})
        message = {"changes_applicable": True, "message": "changes are applicable"}
        idrac_connection_lc_attribute_mock.config_mgr.is_change_applicable.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        with pytest.raises(Exception) as ex:
            self.module.run_setup_idrac_csior(idrac_connection_lc_attribute_mock, f_module)
        assert ex.value.args[0] == "Changes found to commit!"

    def test_run_setup_idrac_csior_success_case02(self, idrac_connection_lc_attribute_mock, idrac_default_args,
                                                  idrac_file_manager_lc_attribute_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "csior": "scr"})
        message = {"changes_applicable": True, "message": "changes found to commit!", "changed": True,
                   "Status": "Success"}
        idrac_connection_lc_attribute_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_setup_idrac_csior(idrac_connection_lc_attribute_mock, f_module)
        assert msg == {'changes_applicable': True, 'message': 'changes found to commit!',
                       'changed': True, 'Status': 'Success'}

    def test_run_setup_idrac_csior_success_case03(self, idrac_connection_lc_attribute_mock, idrac_default_args,
                                                  idrac_file_manager_lc_attribute_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "csior": "scr"})
        message = {"changes_applicable": True, "Message": "No changes found to commit!", "changed": False,
                   "Status": "Success"}
        idrac_connection_lc_attribute_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_setup_idrac_csior(idrac_connection_lc_attribute_mock, f_module)
        assert msg == {'changes_applicable': True, 'Message': 'No changes found to commit!',
                       'changed': False, 'Status': 'Success'}

    def test_run_setup_csior_disable_case(self, idrac_connection_lc_attribute_mock, idrac_default_args,
                                          idrac_file_manager_lc_attribute_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "csior": 'Disabled'})
        message = {"changes_applicable": True}
        obj = MagicMock()
        idrac_connection_lc_attribute_mock.config_mgr = obj
        type(obj).disable_csior = Mock(return_value=message)
        idrac_connection_lc_attribute_mock.config_mgr.is_change_applicable.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        with pytest.raises(Exception) as ex:
            self.module.run_setup_idrac_csior(idrac_connection_lc_attribute_mock, f_module)
        assert ex.value.args[0] == "Changes found to commit!"

    def test_run_setup_csior_enable_case(self, idrac_connection_lc_attribute_mock, idrac_default_args,
                                         idrac_file_manager_lc_attribute_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "csior": 'Enabled'})
        message = {"changes_applicable": True}
        obj = MagicMock()
        idrac_connection_lc_attribute_mock.config_mgr = obj
        type(obj).enable_csior = Mock(return_value='Enabled')
        idrac_connection_lc_attribute_mock.config_mgr.is_change_applicable.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        with pytest.raises(Exception) as ex:
            self.module.run_setup_idrac_csior(idrac_connection_lc_attribute_mock, f_module)
        assert ex.value.args[0] == "Changes found to commit!"

    def test_run_setup_csior_failed_case01(self, idrac_connection_lc_attribute_mock, idrac_default_args,
                                           idrac_file_manager_lc_attribute_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "csior": "csior"})
        message = {'Status': 'Failed', "Data": {'Message': 'status failed in checking Data'}}
        idrac_connection_lc_attribute_mock.file_share_manager.create_share_obj.return_value = "mnt/iso"
        idrac_connection_lc_attribute_mock.config_mgr.set_liason_share.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as ex:
            self.module.run_setup_idrac_csior(idrac_connection_lc_attribute_mock, f_module)
        assert ex.value.args[0] == "status failed in checking Data"

    def test_run_setup_idrac_csior_failed_case03(self, idrac_connection_lc_attribute_mock, idrac_default_args,
                                                 idrac_file_manager_lc_attribute_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "csior": "scr"})
        message = {"changes_applicable": False, "Message": "Failed to found changes", "changed": False,
                   "Status": "Failed", "failed": True}
        idrac_connection_lc_attribute_mock.config_mgr.apply_changes.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_setup_idrac_csior(idrac_connection_lc_attribute_mock, f_module)
        assert msg == {'changes_applicable': False, 'Message': 'Failed to found changes',
                       'changed': False, 'Status': 'Failed', "failed": True}
        assert msg['changed'] is False
        assert msg['failed'] is True

    @pytest.mark.parametrize("exc_type", [ImportError, ValueError, RuntimeError])
    def test_main_lc_attribute_exception_handling_case(self, exc_type, mocker, idrac_connection_lc_attribute_mock,
                                                       idrac_default_args, idrac_file_manager_lc_attribute_mock):
        idrac_default_args.update({"share_name": "sharename", 'share_password': None,
                                   'csior': 'Enabled', 'share_mnt': None, 'share_user': None})
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.dellemc_idrac_lc_attributes.run_setup_idrac_csior',
                     side_effect=exc_type('test'))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True
