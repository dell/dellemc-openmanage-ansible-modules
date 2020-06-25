#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0.14
# Copyright (C) 2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import

import pytest
from ansible.modules.remote_management.dellemc import dellemc_configure_bios
from units.modules.remote_management.dellemc.common import FakeAnsibleModule, Constants
from units.compat.mock import MagicMock, patch, Mock
from units.modules.utils import set_module_args, exit_json, fail_json, AnsibleFailJson, AnsibleExitJson
from units.compat.mock import PropertyMock
from pytest import importorskip
import sys

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")


class TestConfigBios(FakeAnsibleModule):
    module = dellemc_configure_bios

    @pytest.fixture
    def idrac_configure_bios_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.file_share_manager = idrac_obj
        omsdk_mock.config_mgr = idrac_obj
        return idrac_obj

    @pytest.fixture
    def idrac_file_manager_config_bios_mock(self, mocker):
        try:
            file_manager_obj = mocker.patch(
                'ansible.modules.remote_management.dellemc.dellemc_configure_bios.file_share_manager')
        except AttributeError:
            file_manager_obj = MagicMock()
        obj = MagicMock()
        file_manager_obj.create_share_obj.return_value = obj
        return file_manager_obj

    @pytest.fixture
    def idrac_connection_configure_bios_mock(self, mocker, idrac_configure_bios_mock):
        idrac_conn_class_mock = mocker.patch('ansible.modules.remote_management.dellemc.'
                                             'dellemc_configure_bios.iDRACConnection',
                                             return_value=idrac_configure_bios_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_configure_bios_mock
        return idrac_configure_bios_mock

    def test_main_idrac_config_bios_success_Case(self, idrac_connection_configure_bios_mock, idrac_default_args,
                                                 mocker, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename"})
        message = {'changed': False, 'msg': {'Status': "Success", "message": "No changes found to commit!"}}
        mocker.patch('ansible.modules.remote_management.dellemc.'
                     'dellemc_configure_bios.run_server_bios_config', return_value=(message, False))
        result = self._run_module(idrac_default_args)
        assert result == {'changed': False, 'msg': {'Status': 'Success', "message": "No changes found to commit!"}}

    @pytest.mark.parametrize("exc_type", [ImportError, ValueError, RuntimeError])
    def test_main_idrac_config_bios_exception_handling_case(self, exc_type, mocker,
                                                            idrac_connection_configure_bios_mock,
                                                            idrac_default_args, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename"})
        mocker.patch('ansible.modules.remote_management.dellemc.'
                     'dellemc_configure_bios.run_server_bios_config', side_effect=exc_type('test'))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True

    def test_main_config_bios_fail_case(self,idrac_connection_configure_bios_mock, idrac_default_args, mocker,
                                             idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename"})
        message = {"Status": "Failed"}
        mocker.patch('ansible.modules.remote_management.dellemc.dellemc_configure_bios.run_server_bios_config',
                     return_value=(message, True))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result == {'Status': 'Failed', 'failed': True}

    def test_run_idrac_bios_config_success_case01(self, idrac_connection_configure_bios_mock,
                                                  idrac_default_args, mocker, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": "bootsources"})
        message = {"changes_applicable": True, "message": "changes are applicable"}
        mocker.patch('ansible.modules.remote_management.dellemc.'
                     'dellemc_configure_bios._validate_params', return_value=(False, "message of validate params"))
        idrac_connection_configure_bios_mock.config_mgr.is_change_applicable.return_value = message
        idrac_connection_configure_bios_mock.config_mgr.configure_boot_sources.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = True
        msg, err = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'changed': True,
           'failed': False,
           'msg': {'changes_applicable': True, 'message': 'changes are applicable'}}

    def test_run_idrac_bios_config_success_case02(self, idrac_connection_configure_bios_mock, idrac_default_args,
                                                  mocker, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": "bootsources"})
        message = {"changes_applicable": True, "Status": "Success", "message": "changes found to commit!"}
        mocker.patch('ansible.modules.remote_management.dellemc.'
                     'dellemc_configure_bios._validate_params', return_value=(False, "message of validate params"))
        idrac_connection_configure_bios_mock.config_mgr.is_change_applicable.return_value = message
        idrac_connection_configure_bios_mock.config_mgr.configure_boot_sources.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg, err = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {"changed": True, "failed": False, "msg": {"changes_applicable": True, "Status": "Success",
                                                                "message": "changes found to commit!"}}
        assert msg['changed'] is True
        assert msg['failed'] is False

    def test_run_idrac_bios_config_success_case03(self, idrac_connection_configure_bios_mock, idrac_default_args,
                                                  mocker, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": "bootsources"})
        message = {"changes_applicable": False, "Status": "Success", "Message": "No changes found to commit!"}
        mocker.patch('ansible.modules.remote_management.dellemc.'
                     'dellemc_configure_bios._validate_params', return_value=(False, "message of validate params"))
        idrac_connection_configure_bios_mock.config_mgr.is_change_applicable.return_value = message
        idrac_connection_configure_bios_mock.config_mgr.configure_boot_sources.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg, err = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'changed': False, 'failed': False, "msg": {"Message": "No changes found to commit!",
                                                                  "changes_applicable": False, "Status": "Success"}}
        assert msg['changed'] is False
        assert msg['failed'] is False

    def test_run_idrac_bios_config_success_case04(self, idrac_connection_configure_bios_mock, idrac_default_args,
                                                  mocker, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": "bootsources"})
        message = {"changes_applicable": False, "Status": "Success", "Message": "No changes found to apply."}
        mocker.patch('ansible.modules.remote_management.dellemc.'
                     'dellemc_configure_bios._validate_params', return_value=(False, "message of validate params"))
        idrac_connection_configure_bios_mock.config_mgr.is_change_applicable.return_value = message
        idrac_connection_configure_bios_mock.config_mgr.configure_boot_sources.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg, err = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'changed': False, 'failed': False, "msg": {"Message": "No changes found to apply.",
                                                                  "changes_applicable": False, "Status": "Success"}}
        assert msg['changed'] is False
        assert msg['failed'] is False

    def test_run_idrac_bios_config_bootmode_failed_case0(self, idrac_connection_configure_bios_mock,
                                                         idrac_default_args,
                                                         mocker, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": "bootsources"})
        message = {"changes_applicable": False, "Status": "failed", "Message": "No changes found to apply."}
        mocker.patch('ansible.modules.remote_management.dellemc.'
                     'dellemc_configure_bios._validate_params', return_value=(False, "message of validate params"))
        idrac_connection_configure_bios_mock.config_mgr.is_change_applicable.return_value = message
        idrac_connection_configure_bios_mock.config_mgr.configure_boot_sources.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg, err = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'changed': False, 'failed': True, "msg": {"Message": "No changes found to apply.",
                                                                "changes_applicable": False, "Status": "failed"}}
        assert msg['changed'] is False
        assert msg['failed'] is True

    def test_run_idrac_bios_config_bootmode_exception_failed_case0(self, idrac_connection_configure_bios_mock,
                                                         idrac_default_args,
                                                         mocker, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": "bootsources"})
        mocker.patch('ansible.modules.remote_management.dellemc.'
                     'dellemc_configure_bios._validate_params', return_value=(False, "Error"))
        error_msg = "Error in Runtime"
        obj2 = MagicMock()
        obj3 = MagicMock()
        idrac_connection_configure_bios_mock.config_mgr = obj2
        idrac_connection_configure_bios_mock.config_mgr = obj3
        type(obj2).is_change_applicable = Mock(side_effect=Exception(error_msg))
        type(obj3).configure_boot_sources = Mock(side_effect=Exception(error_msg))
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        result, err = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert result['failed'] is True
        assert result['msg'] == "Error: {0}".format(error_msg)

    def test_run_idrac_bios_config_errorhandle_failed_case0(self, idrac_connection_configure_bios_mock,
                                                            idrac_default_args,
                                                            mocker, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": "bootsources"})
        mocker.patch('ansible.modules.remote_management.dellemc.'
                     'dellemc_configure_bios._validate_params', return_value=(True, "Error occurs"))
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg, err = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'changed': False, 'failed': True, "msg": {'Status': 'Failed', 'Message': 'Error occurs'}}
        assert msg['changed'] is False
        assert msg['failed'] is True
        assert err is True

    def test_run_idrac_bios_config_status_failed_case01(self, idrac_connection_configure_bios_mock, idrac_default_args,
                                                        mocker, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": "bootsources"})
        message = {'Status': 'Failed', 'Message': 'message of validate params'}
        mocker.patch('ansible.modules.remote_management.dellemc.'
                     'dellemc_configure_bios._validate_params', return_value=(True, "Error occurs"))
        idrac_connection_configure_bios_mock.config_mgr.set_liason_share.return_value = message
        # idrac_connection_configure_bios_mock.config_mgr.configure_boot_sources.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg, err = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'changed': False, 'failed': True, "msg": {'Status': 'Failed', 'Message': 'Error occurs'}}
        assert msg['changed'] is False
        assert msg['failed'] is True
        assert err is True

    def test_run_idrac_bios_config_status_success_case01(self, idrac_connection_configure_bios_mock, idrac_default_args,
                                                         mocker, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": "bootsources",
                                   "attributes": {"boot_mode": "BootMode", "nvme_mode": "NvmeMode"}})
        message = {'Status': 'Successs', 'Message': 'message of validate params'}
        mocker.patch('ansible.modules.remote_management.dellemc.'
                     'dellemc_configure_bios._validate_params', return_value=(False, "Error didn't occurs"))
        idrac_connection_configure_bios_mock.config_mgr.configure_bios.return_value = message
        idrac_connection_configure_bios_mock.config_mgr.configure_boot_sources.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg, err = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'changed': False, 'failed': True, "msg": {'Status': 'Successs',
                                                                 'Message': 'message of validate params'}}
        assert msg['changed'] is False
        assert msg['failed'] is True
        assert err is True

    def test_run_bios_config_status_boot_sources_failed_case(self, idrac_connection_configure_bios_mock, mocker,
                                                              idrac_default_args, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": None,
                                   "attributes": {"boot_mode": "BootMode", "nvme_mode": "NvmeMode"}})
        message = {'Status': 'Failed', "Data": {'Message': 'message of validate params'}}
        idrac_connection_configure_bios_mock.config_mgr.set_liason_share.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        msg, err = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'msg': 'Error: message of validate params', 'failed': True, 'changed': False}
        assert err is True

    @pytest.mark.parametrize("exc_type", [IndexError, KeyError])
    def test_run_bios_config_status_boot_sources_indexError_failed_case(self, exc_type,
                                                                        idrac_connection_configure_bios_mock, mocker,
                                                              idrac_default_args, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": None,
                                   "attributes": {"boot_mode": "BootMode", "nvme_mode": "NvmeMode"}})
        message = {'Status': 'Failed', 'Message': 'message of keyerror and indexerror'}
        idrac_connection_configure_bios_mock.config_mgr.set_liason_share.return_value = message
        idrac_connection_configure_bios_mock.config_mgr.set_liason.side_effect = exc_type
        f_module = self.get_module_mock(params=idrac_default_args)
        msg, err = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'msg': 'Error: message of keyerror and indexerror', 'failed': True, 'changed': False}
        assert err is True

    def test_run_bios_config_status_boot_success_case(self, idrac_connection_configure_bios_mock, mocker,
                                                           idrac_default_args, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": None, "boot_mode": "Bios",
                                   "nvme_mode": "NonRaid", "secure_boot_mode": "AuditMode",
                                   "onetime_boot_mode": "OneTimeBootSeq", "attributes": [""], "boot_sequence": None})
        message = {"Status": "Success", "changes_applicable": True}
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.deprecate.return_value = "boot_mode, nvme_mode, secure_boot_mode, onetime_boot_mode and " \
                                          "boot_sequence options have been deprecated, and will be removed. ' \
                                  'Please use the attributes option for Bios attributes configuration instead."
        f_module.check_mode = True
        obj = MagicMock()
        obj1 = MagicMock()
        obj2 = MagicMock()
        obj3 = MagicMock()
        idrac_connection_configure_bios_mock.config_mgr.configure_boot_mode = obj
        type(obj).BootModeTypes = PropertyMock(return_value="Bios")
        idrac_connection_configure_bios_mock.config_mgr.configure_nvme_mode = obj1
        type(obj).NvmeModeTypes = PropertyMock(return_value="NonRaid")
        idrac_connection_configure_bios_mock.config_mgr.configure_secure_boot_mode = obj2
        type(obj).SecureBootModeTypes = PropertyMock(return_value="AuditMode")
        idrac_connection_configure_bios_mock.config_mgr.configure_onetime_boot_mode = obj3
        type(obj).OneTimeBootModeTypes = PropertyMock(return_value="OneTimeBootSeq")
        idrac_connection_configure_bios_mock.config_mgr.configure_bios.return_value = message
        idrac_connection_configure_bios_mock.config_mgr.is_change_applicable.return_value = message
        msg, err = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'msg': {'Status': 'Success', 'changes_applicable': True}, 'failed': False, 'changed': True}
        assert err is False
        assert msg['changed'] is True

    def test_run_bios_config_status_success_changed_true_case(self,idrac_connection_configure_bios_mock, mocker,
                                                           idrac_default_args, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": None, "boot_mode": "Bios",
                                   "nvme_mode": "NonRaid", "secure_boot_mode": "AuditMode",
                                   "onetime_boot_mode": "OneTimeBootSeq", "attributes": [""], "boot_sequence": None})
        message = {"Status": "Success"}
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.deprecate.return_value = "boot_mode, nvme_mode, secure_boot_mode, onetime_boot_mode and " \
                                          "boot_sequence options have been deprecated, and will be removed. ' \
                                  'Please use the attributes option for Bios attributes configuration instead."
        f_module.check_mode = False
        obj = MagicMock()
        obj1 = MagicMock()
        obj2 = MagicMock()
        obj3 = MagicMock()
        idrac_connection_configure_bios_mock.config_mgr.configure_boot_mode = obj
        type(obj).BootModeTypes = PropertyMock(return_value="Bios")
        idrac_connection_configure_bios_mock.config_mgr.configure_nvme_mode = obj1
        type(obj).NvmeModeTypes = PropertyMock(return_value="NonRaid")
        idrac_connection_configure_bios_mock.config_mgr.configure_secure_boot_mode = obj2
        type(obj).SecureBootModeTypes = PropertyMock(return_value="AuditMode")
        idrac_connection_configure_bios_mock.config_mgr.configure_onetime_boot_mode = obj3
        type(obj).OneTimeBootModeTypes = PropertyMock(return_value="OneTimeBootSeq")
        idrac_connection_configure_bios_mock.config_mgr.configure_bios.return_value = message
        idrac_connection_configure_bios_mock.config_mgr.apply_changes.return_value = message
        msg, err = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'msg': {'Status': 'Success'}, 'failed': False, 'changed': True}
        assert err is False
        assert msg['changed'] is True

    def test_run_bios_config_status_success_changed_false_case01(self,idrac_connection_configure_bios_mock, mocker,
                                                           idrac_default_args, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": None, "boot_mode": "Bios",
                                   "nvme_mode": "NonRaid", "secure_boot_mode": "AuditMode",
                                   "onetime_boot_mode": "OneTimeBootSeq", "attributes": [""], "boot_sequence": None})
        message = {"Status": "Success", "Message": "No changes found to commit!"}
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.deprecate.return_value = "boot_mode, nvme_mode, secure_boot_mode, onetime_boot_mode and " \
                                          "boot_sequence options have been deprecated, and will be removed. ' \
                                  'Please use the attributes option for Bios attributes configuration instead."
        f_module.check_mode = False
        obj = MagicMock()
        obj1 = MagicMock()
        obj2 = MagicMock()
        obj3 = MagicMock()
        idrac_connection_configure_bios_mock.config_mgr.configure_boot_mode = obj
        type(obj).BootModeTypes = PropertyMock(return_value="Bios")
        idrac_connection_configure_bios_mock.config_mgr.configure_nvme_mode = obj1
        type(obj).NvmeModeTypes = PropertyMock(return_value="NonRaid")
        idrac_connection_configure_bios_mock.config_mgr.configure_secure_boot_mode = obj2
        type(obj).SecureBootModeTypes = PropertyMock(return_value="AuditMode")
        idrac_connection_configure_bios_mock.config_mgr.configure_onetime_boot_mode = obj3
        type(obj).OneTimeBootModeTypes = PropertyMock(return_value="OneTimeBootSeq")
        idrac_connection_configure_bios_mock.config_mgr.configure_bios.return_value = message
        idrac_connection_configure_bios_mock.config_mgr.apply_changes.return_value = message
        msg, err = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'msg': {'Status': 'Success', "Message": "No changes found to commit!"}, 'failed': False,
                       'changed': False}
        assert err is False
        assert msg['changed'] is False

    def test_run_bios_config_status_success_changed_false_case02(self,idrac_connection_configure_bios_mock, mocker,
                                                           idrac_default_args, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": None, "boot_mode": "Bios",
                                   "nvme_mode": "NonRaid", "secure_boot_mode": "AuditMode",
                                   "onetime_boot_mode": "OneTimeBootSeq", "attributes": [""], "boot_sequence": None})
        message = {"Status": "Success", "Message": "No changes found to apply."}
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.deprecate.return_value = "boot_mode, nvme_mode, secure_boot_mode, onetime_boot_mode and " \
                                          "boot_sequence options have been deprecated, and will be removed. ' \
                                  'Please use the attributes option for Bios attributes configuration instead."
        f_module.check_mode = False
        obj = MagicMock()
        obj1 = MagicMock()
        obj2 = MagicMock()
        obj3 = MagicMock()
        idrac_connection_configure_bios_mock.config_mgr.configure_boot_mode = obj
        type(obj).BootModeTypes = PropertyMock(return_value="Bios")
        idrac_connection_configure_bios_mock.config_mgr.configure_nvme_mode = obj1
        type(obj).NvmeModeTypes = PropertyMock(return_value="NonRaid")
        idrac_connection_configure_bios_mock.config_mgr.configure_secure_boot_mode = obj2
        type(obj).SecureBootModeTypes = PropertyMock(return_value="AuditMode")
        idrac_connection_configure_bios_mock.config_mgr.configure_onetime_boot_mode = obj3
        type(obj).OneTimeBootModeTypes = PropertyMock(return_value="OneTimeBootSeq")
        idrac_connection_configure_bios_mock.config_mgr.configure_bios.return_value = message
        idrac_connection_configure_bios_mock.config_mgr.apply_changes.return_value = message
        msg, err = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'msg': {'Status': 'Success', "Message": "No changes found to apply."}, 'failed': False,
                       'changed': False}
        assert err is False
        assert msg['changed'] is False

    def test_run_bios_config_status_attribute_failed_error_case(self, idrac_connection_configure_bios_mock, mocker,
                                                           idrac_default_args, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": None, "boot_mode": "Bios",
                                   "nvme_mode": "NonRaid", "secure_boot_mode": "AuditMode",
                                   "onetime_boot_mode": "OneTimeBootSeq", "attributes": [""], "boot_sequence": None})
        message = {"Status": "Failed"}
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.deprecate.return_value = "boot_mode, nvme_mode, secure_boot_mode, onetime_boot_mode and " \
                                          "boot_sequence options have been deprecated, and will be removed. ' \
                                  'Please use the attributes option for Bios attributes configuration instead."
        obj = MagicMock()
        obj1 = MagicMock()
        obj2 = MagicMock()
        obj3 = MagicMock()
        idrac_connection_configure_bios_mock.config_mgr.configure_boot_mode = obj
        type(obj).BootModeTypes = PropertyMock(return_value="Bios")
        idrac_connection_configure_bios_mock.config_mgr.configure_nvme_mode = obj1
        type(obj).NvmeModeTypes = PropertyMock(return_value="NonRaid")
        idrac_connection_configure_bios_mock.config_mgr.configure_secure_boot_mode = obj2
        type(obj).SecureBootModeTypes = PropertyMock(return_value="AuditMode")
        idrac_connection_configure_bios_mock.config_mgr.configure_onetime_boot_mode = obj3
        type(obj).OneTimeBootModeTypes = PropertyMock(return_value="OneTimeBootSeq")
        idrac_connection_configure_bios_mock.config_mgr.configure_bios.return_value = message
        msg, err = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'msg': {'Status': 'Failed'}, 'failed': True, 'changed': False}
        assert err is True

    def test__validate_params_error_case(self, idrac_connection_configure_bios_mock, idrac_default_args,
                                         idrac_file_manager_config_bios_mock):
        idrac_default_args.update({})
        attr = "b"
        err, msg = self.module._validate_params(attr)
        assert msg == "{} must be of type: {}. {} ({}) provided.".format(
                "attribute values", dict, attr, type(attr))
        assert err is True

    def test__validate_params_error_keys_case(self, idrac_connection_configure_bios_mock, idrac_default_args,
                                         idrac_file_manager_config_bios_mock, mocker):
        idrac_default_args.update({})
        attr = [{"name": "Name"}, {"index": "Index"}, {"enabled": "Enabled"}]
        default = ['Name', 'Index', 'Enabled']
        err, msg = self.module._validate_params(attr)
        assert msg == "attribute keys must be one of the {}.".format(default)
        assert err is True

    def test__validate_params_check_params_case(self, idrac_connection_configure_bios_mock, mocker,
                                                idrac_file_manager_config_bios_mock, idrac_default_args):
        mocker.patch('ansible.modules.remote_management.dellemc.'
                     'dellemc_configure_bios.check_params', return_value=(True, "Error occurs in check params"))
        attr = [{"Name": "name1"}, {"Index": "index1"}]
        err, msg = self.module._validate_params(attr)
        assert msg == "Error occurs in check params"
        assert err is True

    def test__validate_params_empty_params_case(self, idrac_connection_configure_bios_mock, mocker,
                                                idrac_file_manager_config_bios_mock, idrac_default_args):
        mocker.patch('ansible.modules.remote_management.dellemc.'
                     'dellemc_configure_bios._validate_name_index_duplication', return_value=(True, "Error occurs in "
                                                                                                    "validate name"))
        err, msg = self.module._validate_params([])
        assert msg == "Error occurs in validate name"
        assert err is True

    def test__validate_name_index_duplication_error_true_case(self, idrac_connection_configure_bios_mock,
                                                              idrac_default_args):
        result = self.module._validate_name_index_duplication([{"Name": "Name1"}, {"Name": "Name1"}])
        assert result == (True, 'duplicate name  Name1')

    def test__validate_name_index_duplication_error_false_case(self, idrac_connection_configure_bios_mock,
                                                               idrac_default_args):
        result = self.module._validate_name_index_duplication([{"Name": "Name1"}, {"Name": "Name2"}])
        assert result == (False, '')

    def test_check_params_false_case(self, idrac_connection_configure_bios_mock, idrac_default_args):
        result = self.module.check_params({"required": False}, [{"name": "Name1", "required": False},
                                                                {"name": "Name2", "required": False}])
        assert result == (False, "")

    def test_check_params_required_true_case(self, idrac_connection_configure_bios_mock, idrac_default_args):
        result = self.module.check_params({"required": True},
                                          [{"name": "Name0", "type": {}, "required": True},
                                           {"name": "Name2", "required": False}])
        assert result == (True, 'Name0 is required and must be of type: {}')

    def test_check_params_true_case_type(self, idrac_connection_configure_bios_mock, idrac_default_args):
        result = self.module.check_params({"required": True, 'name': ("type"), 'type': ("type")},
                                          [{"name": ("type"), 'type': (list), "required": None}])
        if sys.version_info[0] == 2:
            assert result == (True, "type must be of type: <type 'list'>. type (<type 'str'>) provided.")
        else:
            assert result == (True, "type must be of type: <class 'list'>. type (<class 'str'>) provided.")

    def test_check_params_true_case_name(self, idrac_connection_configure_bios_mock, idrac_default_args):
        result = self.module.check_params({"required": True, 'name': 4, 'min': 7},
                                          [{"name": "name", 'min': 6, 'type': (int), "required": False}])
        assert result == (True, 'name must be greater than or equal to: 6')
