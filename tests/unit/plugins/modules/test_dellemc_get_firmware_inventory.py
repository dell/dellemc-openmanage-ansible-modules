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
from ansible_collections.dellemc.openmanage.plugins.modules import dellemc_get_firmware_inventory
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from mock import MagicMock, PropertyMock
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")


class TestFirmware(FakeAnsibleModule):
    module = dellemc_get_firmware_inventory

    @pytest.fixture
    def idrac_firmware_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.update_mgr = idrac_obj
        type(idrac_obj).InstalledFirmware = PropertyMock(return_value="msg")
        return idrac_obj

    @pytest.fixture
    def idrac_get_firmware_inventory_connection_mock(self, mocker, idrac_firmware_mock):
        idrac_conn_class_mock = mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                                             'dellemc_get_firmware_inventory.iDRACConnection',
                                             return_value=idrac_firmware_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_firmware_mock
        return idrac_firmware_mock

    def test_main_idrac_get_firmware_inventory_success_case01(self, idrac_get_firmware_inventory_connection_mock,
                                                              idrac_default_args):
        idrac_get_firmware_inventory_connection_mock.update_mgr.InstalledFirmware.return_value = {"Status": "Success"}
        result = self._run_module(idrac_default_args)
        assert result == {'ansible_facts': {
            idrac_get_firmware_inventory_connection_mock.ipaddr: {
                'Firmware Inventory': idrac_get_firmware_inventory_connection_mock.update_mgr.InstalledFirmware}},
            "changed": False}

    def test_run_get_firmware_inventory_success_case01(self, idrac_get_firmware_inventory_connection_mock,
                                                       idrac_default_args):
        obj2 = MagicMock()
        idrac_get_firmware_inventory_connection_mock.update_mgr = obj2
        type(obj2).InstalledFirmware = PropertyMock(return_value="msg")
        f_module = self.get_module_mock(params=idrac_default_args)
        msg, err = self.module.run_get_firmware_inventory(idrac_get_firmware_inventory_connection_mock, f_module)
        assert msg == {'failed': False,
                       'msg': idrac_get_firmware_inventory_connection_mock.update_mgr.InstalledFirmware}
        assert msg['failed'] is False
        assert err is False

    def test_run_get_firmware_inventory_failed_case01(self, idrac_get_firmware_inventory_connection_mock,
                                                      idrac_default_args):
        f_module = self.get_module_mock(params=idrac_default_args)
        error_msg = "Error in Runtime"
        obj2 = MagicMock()
        idrac_get_firmware_inventory_connection_mock.update_mgr = obj2
        type(obj2).InstalledFirmware = PropertyMock(side_effect=Exception(error_msg))
        msg, err = self.module.run_get_firmware_inventory(idrac_get_firmware_inventory_connection_mock, f_module)
        assert msg['failed'] is True
        assert msg['msg'] == "Error: {0}".format(error_msg)
        assert err is True

    def test_run_get_firmware_inventory_failed_case02(self, idrac_get_firmware_inventory_connection_mock,
                                                      idrac_default_args):
        message = {'Status': "Failed", "Message": "Fetched..."}
        obj2 = MagicMock()
        idrac_get_firmware_inventory_connection_mock.update_mgr = obj2
        type(obj2).InstalledFirmware = PropertyMock(return_value=message)
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.run_get_firmware_inventory(idrac_get_firmware_inventory_connection_mock, f_module)
        assert result == ({'msg': {'Status': 'Failed', 'Message': 'Fetched...'}, 'failed': True}, False)
        if "Status" in result[0]['msg']:
            if not result[0]['msg']['Status'] == "Success":
                assert result[0]['failed'] is True

    def test_main_idrac_get_firmware_inventory_faild_case01(self, idrac_get_firmware_inventory_connection_mock,
                                                            idrac_default_args):
        error_msg = "Error occurs"
        obj2 = MagicMock()
        idrac_get_firmware_inventory_connection_mock.update_mgr = obj2
        type(obj2).InstalledFirmware = PropertyMock(side_effect=Exception(error_msg))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result['failed'] is True
        assert result['msg'] == "Error: {0}".format(error_msg)

    @pytest.mark.parametrize("exc_type", [ImportError, ValueError, RuntimeError])
    def test_main_idrac_get_firmware_inventory_exception_handling_case(self, exc_type, mocker,
                                                                       idrac_get_firmware_inventory_connection_mock,
                                                                       idrac_default_args):
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.dellemc_get_firmware_inventory.'
                     'run_get_firmware_inventory', side_effect=exc_type('test'))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True
