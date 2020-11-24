# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.4
# Copyright (C) 2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import os
from ansible_collections.dellemc.openmanage.plugins.modules import dellemc_idrac_storage_volume
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible_collections.dellemc.openmanage.tests.unit.compat.mock import MagicMock, patch, Mock
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")


class TestStorageVolume(FakeAnsibleModule):
    module = dellemc_idrac_storage_volume

    @pytest.fixture
    def idrac_storage_volume_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.file_share_manager = idrac_obj
        omsdk_mock.config_mgr = idrac_obj
        type(idrac_obj).create_share_obj = Mock(return_value="servicesstatus")
        type(idrac_obj).set_liason_share = Mock(return_value="servicestatus")
        return idrac_obj

    @pytest.fixture
    def idrac_connection_storage_volume_mock(self, mocker, idrac_storage_volume_mock):
        idrac_conn_class_mock = mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                                             'dellemc_idrac_storage_volume.iDRACConnection',
                                             return_value=idrac_storage_volume_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_storage_volume_mock
        return idrac_storage_volume_mock

    @pytest.fixture
    def idrac_file_manager_storage_volume_mock(self, mocker):
        try:
            file_manager_obj = mocker.patch(
                'ansible_collections.dellemc.openmanage.plugins.modules.dellemc_idrac_storage_volume.file_share_manager')
        except AttributeError:
            file_manager_obj = MagicMock()
        obj = MagicMock()
        file_manager_obj.create_share_obj.return_value = obj
        return file_manager_obj

    def test_main_idrac_storage_volume_success_Case(self, idrac_connection_storage_volume_mock, idrac_default_args,
                                                    mocker):
        idrac_default_args.update({"disk_cache_policy": "Default", "capacity": 12.4, "media_type": "HDD",
                                   "number_dedicated_hot_spare": 1, "protocol": "SAS", "raid_init_operation": "None",
                                   "raid_reset_config": True, "read_cache_policy": "ReadAhead", "span_depth": 4,
                                   "span_length": 3, "state": "create", "stripe_size": 2, "volume_type": "RAID 0",
                                   "write_cache_policy": "WriteThrough"})
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume._validate_options', return_value='state')
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume.run_server_raid_config', return_value={"changes_applicable": True})
        msg = self._run_module(idrac_default_args)
        assert msg == {'changed': True, 'msg': 'Successfully completed the create storage volume operation',
                       'storage_status': {'changes_applicable': True}}
        assert msg["msg"] == "Successfully completed the {0} storage volume operation".format("create")

    def test_main_idrac_storage_volume_fail_Case1(self, idrac_connection_storage_volume_mock, idrac_default_args,
                                                  mocker):
        idrac_default_args.update({"disk_cache_policy": "Default", "capacity": 12.4, "media_type": "HDD",
                                   "number_dedicated_hot_spare": 1, "protocol": "SAS", "raid_init_operation": "None",
                                   "raid_reset_config": True, "read_cache_policy": "ReadAhead", "span_depth": 4,
                                   "span_length": 3, "state": "create", "stripe_size": 2, "volume_type": "RAID 0",
                                   "write_cache_policy": "WriteThrough"})
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume._validate_options', return_value='state')
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume.run_server_raid_config', return_value={"storage_status": "pressent"})
        result = self._run_module_with_fail_json(idrac_default_args)
        assert result == {'failed': True, 'msg': 'Failed to perform storage operation'}

    def test_main_idrac_storage_volume_success_case01(self, idrac_connection_storage_volume_mock, idrac_default_args,
                                                      mocker):
        idrac_default_args.update({"disk_cache_policy": "Default", "capacity": 12.4, "media_type": "HDD",
                                   "number_dedicated_hot_spare": 1, "protocol": "SAS", "raid_init_operation": "None",
                                   "raid_reset_config": True, "read_cache_policy": "ReadAhead", "span_depth": 4,
                                   "span_length": 3, "state": "create", "stripe_size": 2, "volume_type": "RAID 0",
                                   "write_cache_policy": "WriteThrough"})
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume._validate_options', return_value='state')
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume.run_server_raid_config', return_value={"Status": "Success",
                                                                                          "changed": True})
        msg = self._run_module(idrac_default_args)
        assert msg == {'changed': True, 'msg': 'Successfully completed the create storage volume operation',
                       'storage_status': {'Status': 'Success', 'changed': True}}

    def test_main_idrac_storage_volume_success_case02(self, idrac_connection_storage_volume_mock, idrac_default_args,
                                                      mocker):
        idrac_default_args.update({"disk_cache_policy": "Default", "capacity": 12.4, "media_type": "HDD",
                                   "number_dedicated_hot_spare": 1, "protocol": "SAS", "raid_init_operation": "None",
                                   "raid_reset_config": True, "read_cache_policy": "ReadAhead", "span_depth": 4,
                                   "span_length": 3, "state": "create", "stripe_size": 2, "volume_type": "RAID 0",
                                   "write_cache_policy": "WriteThrough"})
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume._validate_options', return_value='state')
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume.run_server_raid_config',
                     return_value={"Status": "Success", "changed": False, "Message": "No changes found to commit!"})
        msg = self._run_module(idrac_default_args)
        assert msg == {'changed': False, 'msg': 'No changes found to commit!',
                       'storage_status': {'Message': 'No changes found to commit!',
                                          'Status': 'Success',
                                          'changed': False}}

    def test_main_idrac_storage_volume_success_case03(self, idrac_connection_storage_volume_mock, idrac_default_args,
                                                      mocker):
        idrac_default_args.update({"disk_cache_policy": "Default", "capacity": 12.4,
                                   "media_type": "HDD",
                                   "number_dedicated_hot_spare": 1, "protocol": "SAS", "raid_init_operation": "None",
                                   "raid_reset_config": True, "read_cache_policy": "ReadAhead", "span_depth": 4,
                                   "span_length": 3, "state": "create", "stripe_size": 2, "volume_type": "RAID 0",
                                   "write_cache_policy": "WriteThrough"})
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume._validate_options', return_value='state')
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume.run_server_raid_config',
                     return_value={"Status": "Success", "changed": True, "Message": "Nooo changes found to commit!"})
        msg = self._run_module(idrac_default_args)
        assert msg['msg'] == "Successfully completed the create storage volume operation"

    @pytest.mark.parametrize("exc_type", [ImportError, ValueError, RuntimeError, TypeError])
    def test_main_idrac_storage_volume_exception_handling_case(self, exc_type, mocker,
                                                               idrac_connection_storage_volume_mock,
                                                               idrac_default_args):
        idrac_default_args.update({"share_name": "sharename"})
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume._validate_options', side_effect=exc_type('test'))
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume.run_server_raid_config', side_effect=exc_type('test'))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True
        # with pytest.raises(Exception) as exc:
        #     self._run_module_with_fail_json(idrac_default_args)
        # assert exc.value.args[0] == "msg"

    def test_run_server_raid_config_create_success_case(self, idrac_connection_storage_volume_mock, idrac_default_args,
                                                        mocker):
        idrac_default_args.update({"share_name": "sharename", "state": "create"})
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume.view_storage', return_value="view")
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume.create_storage', return_value="create")
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume.delete_storage', return_value="delete")
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.run_server_raid_config(idrac_connection_storage_volume_mock, f_module)
        assert result == 'create'

    def test_run_server_raid_config_view_success_case(self, idrac_connection_storage_volume_mock, idrac_default_args,
                                                      mocker):
        idrac_default_args.update({"share_name": "sharename", "state": "view"})
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume.view_storage', return_value="view")
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume.create_storage', return_value="create")
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume.delete_storage', return_value="delete")
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.run_server_raid_config(idrac_connection_storage_volume_mock, f_module)
        assert result == 'view'

    def test_run_server_raid_config_delete_success_case(self, idrac_connection_storage_volume_mock, idrac_default_args,
                                                        mocker):
        idrac_default_args.update({"share_name": "sharename", "state": "delete"})
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume.view_storage', return_value="view")
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume.create_storage', return_value="create")
        mocker.patch('ansible_collections.dellemc.openmanage.plugins.modules.'
                     'dellemc_idrac_storage_volume.delete_storage', return_value="delete")
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.run_server_raid_config(idrac_connection_storage_volume_mock, f_module)
        assert result == 'delete'

    def test_validate_options_controller_id_error_case(self, idrac_connection_storage_volume_mock, idrac_default_args,
                                                       mocker):
        idrac_default_args.update({"share_name": "sharename", "state": "create", "controller_id": ""})
        with pytest.raises(ValueError) as ex:
            self.module._validate_options(idrac_default_args)
        assert "Controller ID is required." == str(ex.value)

    def test_validate_options_capacity_error_case(self, idrac_connection_storage_volume_mock, idrac_default_args,
                                                  mocker):
        idrac_default_args.update({"share_name": "sharename", "state": "create", "controller_id": "XYZ123",
                                   "capacity": -1.4})
        mocker.patch("ansible_collections.dellemc.openmanage.plugins.modules.dellemc_idrac_storage_volume."
                     "error_handling_for_negative_num", return_value=("capacity", -3.4))
        with pytest.raises(ValueError) as ex:
            self.module._validate_options(idrac_default_args)
        assert str(("capacity", -3.4)) == str(ex.value)

    def test_validate_options_strip_size_error_case(self, idrac_connection_storage_volume_mock, idrac_default_args,
                                                    mocker):
        idrac_default_args.update({"share_name": "sharename", "state": "create", "controller_id": "XYZ123",
                                   "capacity": 1.4, "stripe_size": -1})
        mocker.patch("ansible_collections.dellemc.openmanage.plugins.modules.dellemc_idrac_storage_volume."
                     "error_handling_for_negative_num", return_value=("stripe_size", -1))
        with pytest.raises(ValueError) as ex:
            self.module._validate_options(idrac_default_args)
        assert str(("stripe_size", -1)) == str(ex.value)

    def test_validate_options_volume_error_case01(self, idrac_connection_storage_volume_mock, idrac_default_args,
                                                  mocker):
        idrac_default_args.update({"share_name": "sharename", "state": "create", "controller_id": "XYZ123",
                                   "capacity": 1.4, "stripe_size": 1, "volumes": [{"drives": {"id": ["data"],
                                                                                              "location":[1]}}]})
        with pytest.raises(ValueError) as ex:
            self.module._validate_options(idrac_default_args)
        assert "Either {0} or {1} is allowed".format("id", "location") == str(ex.value)

    def test_validate_options_volume_error_case02(self, idrac_connection_storage_volume_mock, idrac_default_args,
                                                  mocker):
        idrac_default_args.update({"share_name": "sharename", "state": "create", "controller_id": "XYZ123",
                                   "capacity": 1.4, "stripe_size": 1, "volumes": [{"drives": {}}]})
        with pytest.raises(ValueError) as ex:
            self.module._validate_options(idrac_default_args)
        assert "Drives must be defined for volume creation." == str(ex.value)

    def test_validate_create_success_case(self, idrac_connection_storage_volume_mock, idrac_default_args, mocker):
        idrac_default_args.update({"share_name": "sharename", "state": "create", "controller_id": "XYZ123",
                                   "capacity": 1.4, "stripe_size": 1,
                                   "volumes": [{"drives": {'data': ""}}]})
        with pytest.raises(ValueError) as ex:
            self.module._validate_options(idrac_default_args)
        assert "Either {0} or {1} should be specified".format("id", "location") == str(ex.value)

    def test_validate_create_success_case_volumes_stripe_size(self, idrac_connection_storage_volume_mock,
                                                              idrac_default_args, mocker):
        idrac_default_args.update({"share_name": "sharename", "state": "create", "controller_id": "XYZ123",
                                   "capacity": 1.4, "stripe_size": 1,
                                   "volumes": [{"drives": {'location': [1]}, "stripe_size": -1}]})
        mocker.patch("ansible_collections.dellemc.openmanage.plugins.modules.dellemc_idrac_storage_volume."
                     "error_handling_for_negative_num", return_value=("stripe_size", -1))
        with pytest.raises(ValueError) as ex:
            self.module._validate_options(idrac_default_args)
        assert str(("stripe_size", -1)) == str(ex.value)

    def test_validate_create_success_case_volumes_capacity(self, idrac_connection_storage_volume_mock,
                                                           idrac_default_args, mocker):
        idrac_default_args.update({"share_name": "sharename", "state": "create", "controller_id": "XYZ123",
                                   "capacity": 1.4, "stripe_size": 1,
                                   "volumes": [{"drives": {'location': [0]}, "capacity": -1.1}]})
        mocker.patch("ansible_collections.dellemc.openmanage.plugins.modules.dellemc_idrac_storage_volume."
                     "error_handling_for_negative_num", return_value=("capacity", -1.1))
        with pytest.raises(ValueError) as ex:
            self.module._validate_options(idrac_default_args)
        assert str(("capacity", -1.1)) == str(ex.value)

    def test_validate_option_delete_success_case01(self, idrac_connection_storage_volume_mock, idrac_default_args,
                                                   mocker):
        idrac_default_args.update({"share_name": "sharename", "state": "delete", "controller_id": "XYZ123",
                                   "capacity": 1.4, "stripe_size": 1,
                                   "volumes": {"drives": {"Id": "", "location": ""}, "capacity": 1.4,
                                               "stripe_size": 1}})
        with pytest.raises(ValueError) as ex:
            self.module._validate_options(idrac_default_args)
        assert "Virtual disk name is a required parameter for remove virtual disk operations." == str(ex.value)

    def test_validate_option_delete_success_case02(self, idrac_connection_storage_volume_mock, idrac_default_args,
                                                   mocker):
        idrac_default_args.update({"share_name": "sharename", "state": "delete", "controller_id": "XYZ123",
                                   "capacity": 1.4, "stripe_size": 1,
                                   "volumes": None})
        with pytest.raises(ValueError) as ex:
            self.module._validate_options(idrac_default_args)
        assert "Virtual disk name is a required parameter for remove virtual disk operations." == str(ex.value)

    def test_error_handling_for_negative_num(self, idrac_connection_storage_volume_mock, idrac_default_args):
        msg = self.module.error_handling_for_negative_num("capacity", -1.0)
        assert msg == "{0} cannot be a negative number or zero,got {1}".format("capacity", -1.0)

    def test_set_liason_share_success_case(self, idrac_connection_storage_volume_mock, idrac_default_args,
                                           idrac_file_manager_storage_volume_mock):
        idrac_default_args.update({"share_name": "sharename", "state": "delete", "share_path": "sharpath"})
        message = {"Status": 'Failed', "Data": {'Message': "Failed to set Liason share"}}
        obj = MagicMock()
        idrac_connection_storage_volume_mock.tempfile.gettempdir() + os.sep
        idrac_connection_storage_volume_mock.file_share_manager.create_share_obj.return_value = message
        idrac_connection_storage_volume_mock.config_mgr = obj
        obj.set_liason_share = Mock(return_value=message)
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as ex:
            self.module.set_liason_share(idrac_connection_storage_volume_mock, f_module)
        assert "Failed to set Liason share" == str(ex.value)

    def test_view_storage_success_case(self, idrac_connection_storage_volume_mock, idrac_default_args):
        idrac_default_args.update({"controller_id": "controller", "volume_id": "virtual_disk"})
        msg = {"Status": "Success"}
        obj = MagicMock()
        idrac_connection_storage_volume_mock.config_mgr.RaidHelper = obj
        obj.view_storage = Mock(return_value=msg)
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.view_storage(idrac_connection_storage_volume_mock, f_module)
        assert result == {"Status": "Success"}

    def test_view_storage_failed_case(self, idrac_connection_storage_volume_mock, idrac_default_args):
        idrac_default_args.update({"controller_id": "controller", "volume_id": "virtual_disk"})
        msg = {"Status": "Failed", "msg": "Failed to fetch storage details"}
        obj = MagicMock()
        idrac_connection_storage_volume_mock.config_mgr.RaidHelper = obj
        obj.view_storage = Mock(return_value=msg)
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as ex:
            self.module.view_storage(idrac_connection_storage_volume_mock, f_module)
        assert "Failed to fetch storage details" == str(ex.value)

    def test_delete_storage_case(self, idrac_connection_storage_volume_mock, idrac_default_args):
        idrac_default_args.update({"volumes": [{"name": "nameofvolume"}]})
        msg = {"Status": "Success"}
        obj = MagicMock()
        idrac_connection_storage_volume_mock.config_mgr.RaidHelper = obj
        obj.delete_virtual_disk = Mock(return_value=msg)
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.delete_storage(idrac_connection_storage_volume_mock, f_module)
        assert result == {"Status": "Success"}

    def test_create_storage_success_case01(self, idrac_connection_storage_volume_mock, idrac_default_args, mocker):
        idrac_default_args.update({"volumes": {"name": "volume1"}, "controller_id": "x56y"})
        mocker.patch("ansible_collections.dellemc.openmanage.plugins.modules.dellemc_idrac_storage_volume."
                     "multiple_vd_config", return_value={"name": "volume1", "stripe_size": 1.3})
        obj = MagicMock()
        idrac_connection_storage_volume_mock.config_mgr.RaidHelper = obj
        obj.new_virtual_disk = Mock(return_value=[{"name": "volume1", "stripe_size": 1.3}])
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.create_storage(idrac_connection_storage_volume_mock, f_module)
        assert result == [{'name': 'volume1', 'stripe_size': 1.3}]

    def test_create_storage_success_case02(self, idrac_connection_storage_volume_mock, idrac_default_args, mocker):
        idrac_default_args.update({"volumes": None, "controller_id": "x56y"})
        mocker.patch("ansible_collections.dellemc.openmanage.plugins.modules.dellemc_idrac_storage_volume."
                     "multiple_vd_config", return_value={"name": "volume1", "stripe_size": 1.3})
        obj = MagicMock()
        idrac_connection_storage_volume_mock.config_mgr.RaidHelper = obj
        obj.new_virtual_disk = Mock(return_value=[{"name": "volume1", "stripe_size": 1.3}])
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.create_storage(idrac_connection_storage_volume_mock, f_module)
        assert result == [{'name': 'volume1', 'stripe_size': 1.3}]

    def test_multiple_vd_config_success_case(self, idrac_connection_storage_volume_mock, idrac_default_args, mocker):
        idrac_default_args.update({"name": "name1", "media_type": 'HDD', "protocol": "SAS", "drives": None,
                                   "capacity": 2, "raid_init_operation": 'Fast', 'raid_reset_config': True,
                                   "span_depth": 1, "span_length": 1, "number_dedicated_hot_spare": 0,
                                   "volume_type": 'RAID 0', "disk_cache_policy": "Default",
                                   "write_cache_policy": "WriteThrough", "read_cache_policy": "NoReadAhead",
                                   "stripe_size": 64 * 1024})
        result = self.module.multiple_vd_config({'name': 'volume1', 'stripe_size': 1.3, "capacity": 1,
                                                 "drives": {"id": "id", "location": "location"}}, "",
                                                {"media_type": "HDD", "protocol": "NAS", "raid_init_operation": "Fast",
                                                 'raid_reset_config': True, "span_depth": 1, "span_length": 1,
                                                 "number_dedicated_hot_spare": 0, "volume_type": 'RAID 0',
                                                 "disk_cache_policy": "Default", "write_cache_policy": "WriteThrough",
                                                 "read_cache_policy": "NoReadAhead", "stripe_size": 64 * 1024})
        assert result["mediatype"] == 'HDD'

    def test_multiple_vd_config_capacity_none_case(self, idrac_connection_storage_volume_mock, idrac_default_args,
                                                   mocker):
        idrac_default_args.update({"name": "name1", "media_type": 'HDD', "protocol": "SAS", "drives": {"id": ["id1"],
                                                                                                       "location": [1]},
                                   "capacity": None, "raid_init_operation": 'Fast', 'raid_reset_config': True,
                                   "span_depth": 1, "span_length": 1, "number_dedicated_hot_spare": 0,
                                   "volume_type": 'RAID 0', "disk_cache_policy": "Default", "stripe_size": 64 * 1024,
                                   "write_cache_policy": "WriteThrough", "read_cache_policy": "NoReadAhead"})
        result = self.module.multiple_vd_config({"media_type": 'HDD', "protocol": "SAS", "drives": None,
                                                 "capacity": 2, "raid_init_operation": 'Fast',
                                                 'raid_reset_config': True, "span_depth": 1, "span_length": 1,
                                                 "number_dedicated_hot_spare": 0, "volume_type": 'RAID 0',
                                                 "disk_cache_policy": "Default", "stripe_size": 64 * 1024,
                                                 "write_cache_policy": "WriteThrough",
                                                 "read_cache_policy": "NoReadAhead"}, "", {"protocol": "SAS"})
        assert result["mediatype"] == "HDD"

    def test_multiple_vd_config_capacity_none_case02(self, idrac_connection_storage_volume_mock, idrac_default_args,
                                                     mocker):
        idrac_default_args.update({"name": "name1", "media_type": None, "protocol": "SAS", "drives": {"id": ["id1"]},
                                   "capacity": None, "raid_init_operation": None, 'raid_reset_config': True,
                                   "span_depth": 1, "span_length": 1, "number_dedicated_hot_spare": 0,
                                   "volume_type": 'RAID 0', "disk_cache_policy": "Default", "stripe_size": 64 * 1024,
                                   "write_cache_policy": "WriteThrough", "read_cache_policy": "NoReadAhead"})
        result = self.module.multiple_vd_config({'name': 'volume1', 'stripe_size': 1.3, "capacity": 1,
                                                 "drives": {"id": ["id"]}}, "",
                                                {"media_type": None, "protocol": "SAS", "raid_init_operation": None,
                                                 'raid_reset_config': True, "span_depth": 1, "span_length": 1,
                                                 "number_dedicated_hot_spare": 0, "volume_type": 'RAID 0',
                                                 "disk_cache_policy": "Default", "write_cache_policy": "WriteThrough",
                                                 "read_cache_policy": "NoReadAhead", "stripe_size": 64 * 1024})
        assert result['Name'] == 'volume1'

    def test_multiple_vd_config_capacity_none_case1(self, idrac_connection_storage_volume_mock, idrac_default_args,
                                                    mocker):
        idrac_default_args.update({"name": "name1", "media_type": 'HDD', "protocol": "SAS", "drives": {"id": ["id1"]},
                                   "capacity": None, "raid_init_operation": None, 'raid_reset_config': False,
                                   "span_depth": 1, "span_length": 1, "number_dedicated_hot_spare": 0,
                                   "volume_type": 'RAID 0', "disk_cache_policy": "Default", "stripe_size": 64 * 1024,
                                   "write_cache_policy": "WriteThrough", "read_cache_policy": "NoReadAhead"})
        result = self.module.multiple_vd_config({"media_type": 'HDD', "protocol": "SAS", "drives": None,
                                                 "capacity": None, "raid_init_operation": None,
                                                 'raid_reset_config': False, "span_depth": 1, "span_length": 1,
                                                 "number_dedicated_hot_spare": 0, "volume_type": 'RAID 0',
                                                 "disk_cache_policy": "Default", "stripe_size": 64 * 1024,
                                                 "write_cache_policy": "WriteThrough",
                                                 "read_cache_policy": "NoReadAhead"}, "", {"protocol": "NAS"})
        assert result["StripeSize"] == 65536

    def test_multiple_vd_config_success_case02(self, idrac_connection_storage_volume_mock, idrac_default_args, mocker):
        idrac_default_args.update({"name": "name1", "media_type": 'HDD', "protocol": "SAS", "drives": None,
                                   "capacity": 2, "raid_init_operation": 'Fast', 'raid_reset_config': True,
                                   "span_depth": 1, "span_length": 1, "number_dedicated_hot_spare": 0,
                                   "volume_type": 'RAID 0', "disk_cache_policy": "Default",
                                   "write_cache_policy": "WriteThrough", "read_cache_policy": "NoReadAhead",
                                   "stripe_size": 64 * 1024})
        result = self.module.multiple_vd_config({'name': 'volume1', "capacity": 1,
                                                 "media_type": None, "protocol": None,
                                                 "raid_init_operation": "Fast",
                                                 'raid_reset_config': False, "span_depth": 1, "span_length": 1,
                                                 "number_dedicated_hot_spare": 0, "volume_type": 'RAID 0',
                                                 "disk_cache_policy": "Default", "stripe_size": 64 * 1024,
                                                 "write_cache_policy": "WriteThrough",
                                                 "read_cache_policy": "NoReadAhead"}, "", {})
        assert result["StripeSize"] == 65536
