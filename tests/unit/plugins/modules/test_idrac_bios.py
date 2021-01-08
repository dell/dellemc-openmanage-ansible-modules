# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.0.0
# Copyright (C) 2018-2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_bios
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible_collections.dellemc.openmanage.tests.unit.compat.mock import MagicMock, patch, Mock
from ansible_collections.dellemc.openmanage.tests.unit.compat.mock import PropertyMock
from io import StringIO
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestConfigBios(FakeAnsibleModule):
    module = idrac_bios

    @pytest.fixture
    def idrac_configure_bios_mock(self):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.file_share_manager = idrac_obj
        omsdk_mock.config_mgr = idrac_obj
        return idrac_obj

    @pytest.fixture
    def idrac_file_manager_config_bios_mock(self, mocker):
        try:
            file_manager_obj = mocker.patch(
                MODULE_PATH + 'idrac_bios.file_share_manager')
        except AttributeError:
            file_manager_obj = MagicMock()
        obj = MagicMock()
        file_manager_obj.create_share_obj.return_value = obj
        return file_manager_obj

    @pytest.fixture
    def idrac_connection_configure_bios_mock(self, mocker, idrac_configure_bios_mock):
        idrac_conn_class_mock = mocker.patch(MODULE_PATH +
                                             'idrac_bios.iDRACConnection',
                                             return_value=idrac_configure_bios_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_configure_bios_mock
        return idrac_configure_bios_mock

    def test_main_idrac_config_bios_success_Case(self, idrac_connection_configure_bios_mock, idrac_default_args,
                                                 mocker, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename"})
        message = {'changed': False, 'msg': {'Status': "Success", "message": "No changes found to commit!"}}
        mocker.patch(MODULE_PATH +
                     'idrac_bios.run_server_bios_config', return_value=message)
        result = self._run_module(idrac_default_args)
        assert result == {
            'msg': {'changed': False, 'msg': {'Status': 'Success', 'message': 'No changes found to commit!'}},
            'changed': False, 'failed': False}

    @pytest.mark.parametrize("exc_type", [RuntimeError, SSLValidationError, ConnectionError, KeyError,
                                          ImportError, ValueError, TypeError, HTTPError, URLError])
    def test_main_idrac_config_bios_exception_handling_case(self, exc_type, mocker,
                                                            idrac_connection_configure_bios_mock,
                                                            idrac_default_args, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename"})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(
                MODULE_PATH + 'idrac_bios.run_server_bios_config',
                side_effect=exc_type('test'))
        else:
            mocker.patch(
                MODULE_PATH + 'idrac_bios.run_server_bios_config',
                side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                     {"accept-type": "application/json"}, StringIO(json_str)))
        if not exc_type == URLError:
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result

    def test_run_idrac_bios_config_success_case01(self, idrac_connection_configure_bios_mock,
                                                  idrac_default_args, mocker, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": "bootsources"})
        message = {"changes_applicable": True, "message": "changes are applicable"}
        mocker.patch(MODULE_PATH +
                     'idrac_bios._validate_params', return_value=(False, "message of validate params"))
        idrac_connection_configure_bios_mock.config_mgr.is_change_applicabl.return_value = message
        idrac_connection_configure_bios_mock.config_mgr.configure_boot_sources.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = True
        msg = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'changes_applicable': True, 'message': 'changes are applicable'}

    def test_run_idrac_bios_config_success_case02(self, idrac_connection_configure_bios_mock, idrac_default_args,
                                                  mocker, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": "bootsources"})
        message = {"changes_applicable": True, "Status": "Success", "message": "changes found to commit!"}
        mocker.patch(MODULE_PATH +
                     'idrac_bios._validate_params', return_value=(False, "message of validate params"))
        idrac_connection_configure_bios_mock.config_mgr.is_change_applicabl.return_value = message
        idrac_connection_configure_bios_mock.config_mgr.configure_boot_sources.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'Status': 'Success',
                       'changes_applicable': True,
                       'message': 'changes found to commit!'}

    def test_run_idrac_bios_config_success_case03(self, idrac_connection_configure_bios_mock, idrac_default_args,
                                                  mocker, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": "bootsources"})
        message = {"changes_applicable": False, "Status": "Success", "Message": "No changes found to commit!"}
        mocker.patch(MODULE_PATH +
                     'idrac_bios._validate_params', return_value=(False, "message of validate params"))
        idrac_connection_configure_bios_mock.config_mgr.is_change_applicabl.return_value = message
        idrac_connection_configure_bios_mock.config_mgr.configure_boot_sources.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'Message': 'No changes found to commit!',
                       'Status': 'Success',
                       'changes_applicable': False}

    def test_run_idrac_bios_config_success_case04(self, idrac_connection_configure_bios_mock, idrac_default_args,
                                                  mocker, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": "bootsources"})
        message = {"changes_applicable": False, "Status": "Success", "Message": "No changes found to apply."}
        mocker.patch(MODULE_PATH +
                     'idrac_bios._validate_params', return_value=(False, "message of validate params"))
        idrac_connection_configure_bios_mock.config_mgr.is_change_applicabl.return_value = message
        idrac_connection_configure_bios_mock.config_mgr.configure_boot_sources.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'Message': 'No changes found to apply.',
                       'Status': 'Success',
                       'changes_applicable': False}

    def test_run_idrac_bios_config_bootmode_failed_case0(self, idrac_connection_configure_bios_mock,
                                                         idrac_default_args,
                                                         mocker, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": "bootsources"})
        message = {"changes_applicable": False, "Status": "failed", "Message": "No changes found to apply."}
        mocker.patch(MODULE_PATH +
                     'idrac_bios._validate_params', return_value=(False, "message of validate params"))
        idrac_connection_configure_bios_mock.config_mgr.is_change_applicabl.return_value = message
        idrac_connection_configure_bios_mock.config_mgr.configure_boot_sources.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'Message': 'No changes found to apply.',
                       'Status': 'failed',
                       'changes_applicable': False}

    def test_run_idrac_bios_config_errorhandle_failed_case0(self, idrac_connection_configure_bios_mock,
                                                            idrac_default_args,
                                                            mocker, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": "bootsources"})
        mocker.patch(MODULE_PATH +
                     'idrac_bios._validate_params', return_value=(True, "Error occurs"))
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == idrac_connection_configure_bios_mock.config_mgr.configure_boot_sources()

    def test_run_idrac_bios_config_status_failed_case01(self, idrac_connection_configure_bios_mock, idrac_default_args,
                                                        mocker, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": "bootsources"})
        message = {'Status': 'Failed', 'Message': 'message of validate params'}
        mocker.patch(MODULE_PATH +
                     'idrac_bios._validate_params', return_value=(True, "Error occurs"))
        idrac_connection_configure_bios_mock.config_mgr.set_liason_share.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == idrac_connection_configure_bios_mock.config_mgr.configure_boot_sources()

    def test_run_idrac_bios_config_status_success_case01(self, idrac_connection_configure_bios_mock, idrac_default_args,
                                                         mocker, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": "bootsources",
                                   "attributes": {"boot_mode": "BootMode", "nvme_mode": "NvmeMode"}})
        message = {'Status': 'Successs', 'Message': 'message of validate params'}
        mocker.patch(MODULE_PATH +
                     'idrac_bios._validate_params', return_value=(False, "Error did not occurs"))
        idrac_connection_configure_bios_mock.config_mgr.configure_bios.return_value = message
        idrac_connection_configure_bios_mock.config_mgr.configure_boot_sources.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        msg = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'Message': 'message of validate params', 'Status': 'Successs'}

    def test_run_bios_config_status_boot_sources_failed_case(self, idrac_connection_configure_bios_mock, mocker,
                                                             idrac_default_args, idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": "bootsources",
                                   "boot_mode": "Bios",
                                   "nvme_mode": "Raid", 'secure_boot_mode': "AuditMode",
                                   'onetime_boot_mode': "OneTimeBootSeq",
                                   "attributes": {"boot_mode": "BootMode", "nvme_mode": "NvmeMode"}})
        message = {'Status': 'Failed', "Data": {'Message': 'message of validate params'}}
        idrac_connection_configure_bios_mock.config_mgr.set_liason_share.return_value = message
        f_module = self.get_module_mock(params=idrac_default_args)
        msg = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == idrac_connection_configure_bios_mock.config_mgr.configure_boot_sources()

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
        msg = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'Status': 'Success', 'changes_applicable': True}

    def test_run_bios_config_status_success_changed_true_case(self, idrac_connection_configure_bios_mock, mocker,
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
        msg = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'Status': 'Success'}

    def test_run_bios_config_status_success_changed_false_case01(self, idrac_connection_configure_bios_mock, mocker,
                                                                 idrac_default_args,
                                                                 idrac_file_manager_config_bios_mock):
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
        msg = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'Message': 'No changes found to commit!', 'Status': 'Success'}

    def test_run_bios_config_status_success_changed_false_case02(self, idrac_connection_configure_bios_mock, mocker,
                                                                 idrac_default_args,
                                                                 idrac_file_manager_config_bios_mock):
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
        msg = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == {'Message': 'No changes found to apply.', 'Status': 'Success'}

    def test_run_bios_config_status_attribute_failed_error_case(self, idrac_connection_configure_bios_mock, mocker,
                                                                idrac_default_args,
                                                                idrac_file_manager_config_bios_mock):
        idrac_default_args.update({"share_name": "sharename", "share_mnt": "mountname", "share_user": "shareuser",
                                   "share_password": "sharepassword", "boot_sources": None, "boot_mode": "Bios",
                                   "nvme_mode": "NonRaid", "secure_boot_mode": "AuditMode",
                                   "onetime_boot_mode": "OneTimeBootSeq", "attributes": [""], "boot_sequence": None})
        message = {"Status": "Failed"}
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
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
        msg = self.module.run_server_bios_config(idrac_connection_configure_bios_mock, f_module)
        assert msg == idrac_connection_configure_bios_mock.config_mgr.is_change_applicable()

    def test__validate_params_error_case(self, idrac_connection_configure_bios_mock, idrac_default_args,
                                         idrac_file_manager_config_bios_mock):
        idrac_default_args.update({})
        attr = {"name": "Name"}
        msg = self.module._validate_params(attr)
        assert msg == "attribute values must be of type: {0}. name ({1}) provided.".format(dict, str)

    def test__validate_params_error_keys_case(self, idrac_connection_configure_bios_mock, idrac_default_args,
                                              idrac_file_manager_config_bios_mock, mocker):
        idrac_default_args.update({})
        attr = [{"name": "Name"}, {"index": "Index"}, {"enabled": "Enabled"}]
        msg = self.module._validate_params(attr)
        assert msg == "attribute keys must be one of the ['Name', 'Index', 'Enabled']."

    def test__validate_params_check_params_case(self, idrac_connection_configure_bios_mock, mocker,
                                                idrac_file_manager_config_bios_mock, idrac_default_args):
        mocker.patch(MODULE_PATH +
                     'idrac_bios.check_params', return_value=(True, "Error occurs in check params"))
        attr = [{"name": "name1"}, {"Index": "index1"}]
        msg = self.module._validate_params(attr)
        assert msg == "attribute keys must be one of the ['Name', 'Index', 'Enabled']."

    def test__validate_params_empty_params_case(self, idrac_connection_configure_bios_mock, mocker,
                                                idrac_file_manager_config_bios_mock, idrac_default_args):
        mocker.patch(MODULE_PATH +
                     'idrac_bios._validate_name_index_duplication', return_value=(True, "Error occurs in "
                                                                                        "validate name"))
        msg = self.module._validate_params([])
        assert msg == (True, 'Error occurs in validate name')

    def test__validate_name_index_duplication_error_true_case(self, idrac_connection_configure_bios_mock,
                                                              idrac_default_args):
        result = self.module._validate_name_index_duplication([{"Name": "Name1"}, {"Name": "Name1"}])
        assert result == 'duplicate name  Name1'

    def test__validate_name_index_duplication_error_false_case(self, idrac_connection_configure_bios_mock,
                                                               idrac_default_args):
        result = self.module._validate_name_index_duplication([{"Name": "Name1"}, {"Name": "Name2"}])
        assert result == ''

    def test_check_params_false_case(self, idrac_connection_configure_bios_mock, idrac_default_args):
        result = self.module.check_params({"required": False}, [{"name": "Name1", "required": False},
                                                                {"name": "Name2", "required": False}])
        assert result == ''

    def test_check_params_required_true_case(self, idrac_connection_configure_bios_mock, idrac_default_args):
        result = self.module.check_params({"required": True},
                                          [{"name": "Name0", "type": {}, "required": True},
                                           {"name": "Name2", "required": False}])
        assert result == 'Name0 is required and must be of type: {}'
