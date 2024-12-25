# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.5.0
# Copyright (C) 2019-2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from unittest.mock import MagicMock
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_redfish_storage_controller
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
HTTPS_ADDRESS = 'https://testhost.com'
HTTP_ERROR_MSG = 'http error message'
RAID_INTEGRATED_1_1 = "RAID.Integrated.1-1"
ODATA_ID = "@odata.id"


@pytest.fixture
def redfish_str_controller_conn(mocker, redfish_response_mock):
    connection_class_mock = mocker.patch(
        MODULE_PATH + 'idrac_redfish_storage_controller.Redfish')
    idrac_redfish_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    idrac_redfish_connection_mock_obj.invoke_request.return_value = redfish_response_mock
    return idrac_redfish_connection_mock_obj


class TestIdracRedfishStorageController(FakeAnsibleModule):
    module = idrac_redfish_storage_controller

    def test_check_id_exists(self, redfish_str_controller_conn, redfish_response_mock):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password"}
        uri = "/redfish/v1/Dell/Systems/{system_id}/Storage/DellController/{controller_id}"
        f_module = self.get_module_mock(params=param)
        redfish_response_mock.success = True
        redfish_response_mock.status_code = 200
        result = self.module.check_id_exists(f_module, redfish_str_controller_conn, "controller_id",
                                             RAID_INTEGRATED_1_1, uri)
        assert result is None

        redfish_response_mock.success = False
        redfish_response_mock.status_code = 400
        with pytest.raises(Exception) as ex:
            self.module.check_id_exists(f_module, redfish_str_controller_conn, "controller_id",
                                        RAID_INTEGRATED_1_1, uri)
        assert ex.value.args[0] == "controller_id with id 'RAID.Integrated.1-1' not found in system"

        json_str = to_text(json.dumps({"data": "out"}))
        redfish_str_controller_conn.invoke_request.side_effect = HTTPError(
            HTTPS_ADDRESS, 400,
            HTTP_ERROR_MSG,
            {"accept-type": "application/json"},
            StringIO(json_str))
        with pytest.raises(Exception) as ex:
            self.module.check_id_exists(f_module, redfish_str_controller_conn, "controller_id",
                                        RAID_INTEGRATED_1_1, uri)
        assert ex.value.args[0] == "controller_id with id 'RAID.Integrated.1-1' not found in system"

    def test_validate_inputs(self, redfish_str_controller_conn, redfish_response_mock):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "command": "ReKey", "mode": "LKM"}
        f_module = self.get_module_mock(params=param)
        with pytest.raises(Exception) as ex:
            self.module.validate_inputs(f_module)
        assert ex.value.args[0] == "All of the following: key, key_id and old_key are required for 'ReKey' operation."

        param.update({"command": "AssignSpare", "target": ["Disk.Bay.0:Enclosure.Internal.0-2:RAID.Integrated.1-1",
                                                           "Disk.Bay.1:Enclosure.Internal.0-2:RAID.Integrated.1-1"]})
        f_module = self.get_module_mock(params=param)
        with pytest.raises(Exception) as ex:
            self.module.validate_inputs(f_module)
        assert ex.value.args[0] == "The Fully Qualified Device Descriptor (FQDD) of the target " \
                                   "physical disk must be only one."

        param.update({"volume_id": ["Disk.Virtual.0:RAID.Mezzanine.1C-0",
                                    "Disk.Virtual.0:RAID.Mezzanine.1C-1"], "target": None})
        with pytest.raises(Exception) as ex:
            self.module.validate_inputs(f_module)
        assert ex.value.args[0] == "The Fully Qualified Device Descriptor (FQDD) of the target " \
                                   "virtual drive must be only one."

        param.update({"command": "EnableControllerEncryption"})
        f_module = self.get_module_mock(params=param)
        with pytest.raises(Exception) as ex:
            self.module.validate_inputs(f_module)
        assert ex.value.args[0] == "All of the following: key, key_id are " \
                                   "required for 'EnableControllerEncryption' operation."

        param.update({"command": "ChangePDStateToOnline",
                      "target": ["Disk.Bay.0:Enclosure.Internal.0-2:RAID.Integrated.1-1",
                                 "Disk.Bay.0:Enclosure.Internal.0-2:RAID.Integrated.1-1"]})
        with pytest.raises(Exception) as ex:
            self.module.validate_inputs(f_module)
        assert ex.value.args[0] == "The Fully Qualified Device Descriptor (FQDD) of the target " \
                                   "physical disk must be only one."

        param.update({"key": "Key@123", "key_id": 123, "old_key": "abc",
                      "command": "ReKey", "mode": "LKM"})
        f_module = self.get_module_mock(params=param)
        result = self.module.validate_inputs(f_module)
        assert result is None

        param.update({"key": "Key@123", "key_id": 123,
                      "command": "EnableControllerEncryption", "mode": "LKM"})
        f_module = self.get_module_mock(params=param)
        result = self.module.validate_inputs(f_module)
        assert result is None

        param.update({"volume_id": None, "command": "AssignSpare",
                      "target": ["Disk.Bay.0:Enclosure.Internal.0-2:RAID.Integrated.1-1"]})
        f_module = self.get_module_mock(params=param)
        result = self.module.validate_inputs(f_module)
        assert result is None

        param.update({"command": "ChangePDStateToOnline",
                      "target": None})
        f_module = self.get_module_mock(params=param)
        result = self.module.validate_inputs(f_module)
        assert result is None

        param.update({"command": "NoCommand"})
        f_module = self.get_module_mock(params=param)
        result = self.module.validate_inputs(f_module)
        assert result is None

    def test_target_identify_pattern(self, redfish_str_controller_conn, redfish_response_mock):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "command": "BlinkTarget", "target": "Disk.Bay.1:Enclosure.Internal.0-0:RAID.Mezzanine.1C-1",
                 "volume_id": "Disk.Virtual.0:RAID.Mezzanine.1C-1"}
        f_module = self.get_module_mock(params=param)
        redfish_response_mock.success = True
        redfish_response_mock.status_code = 200
        result = self.module.target_identify_pattern(f_module, redfish_str_controller_conn)
        assert result.status_code == 200

        f_module.check_mode = True
        with pytest.raises(Exception) as ex:
            self.module.target_identify_pattern(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Changes found to be applied."

        param.update({"volume_id": None})
        f_module = self.get_module_mock(params=param)
        result = self.module.target_identify_pattern(f_module, redfish_str_controller_conn)
        assert result.status_code == 200

        param.update({"target": None})
        f_module = self.get_module_mock(params=param)
        result = self.module.target_identify_pattern(f_module, redfish_str_controller_conn)
        assert result.status_code == 200

        param.update({"volume_id": "Disk.Virtual.0:RAID.Mezzanine.1C-1"})
        f_module = self.get_module_mock(params=param)
        result = self.module.target_identify_pattern(f_module, redfish_str_controller_conn)
        assert result.status_code == 200

    def test_ctrl_reset_config(self, redfish_str_controller_conn, redfish_response_mock, mocker):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "controller_id": "RAID.Mezzanine.1C-1", "command": "ResetConfig"}
        f_module = self.get_module_mock(params=param)
        mocker.patch(MODULE_PATH + "idrac_redfish_storage_controller.check_id_exists", return_value=None)
        redfish_str_controller_conn.json_data = {"Members": ["virtual_drive"]}
        redfish_response_mock.headers = {"Location": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_XXXXXXXXXXXXX"}
        result = self.module.ctrl_reset_config(f_module, redfish_str_controller_conn)
        assert result[2] == "JID_XXXXXXXXXXXXX"
        f_module.check_mode = True
        with pytest.raises(Exception) as ex:
            self.module.ctrl_reset_config(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Changes found to be applied."
        redfish_response_mock.json_data = {"Members": []}
        with pytest.raises(Exception) as ex:
            self.module.ctrl_reset_config(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "No changes found to be applied."

    def test_hot_spare_config(self, redfish_str_controller_conn, redfish_response_mock):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "command": "AssignSpare", "target": ["Disk.Bay.1:Enclosure.Internal.0-2:RAID.Integrated.1-1"]}
        f_module = self.get_module_mock(params=param)
        redfish_response_mock.json_data = {"HotspareType": "None"}
        redfish_response_mock.headers = {"Location": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_XXXXXXXXXXXXX"}
        result = self.module.hot_spare_config(f_module, redfish_str_controller_conn)
        assert result[2] == "JID_XXXXXXXXXXXXX"

        param.update({"volume_id": 'Disk.Virtual.0:RAID.Slot.1-1'})
        f_module = self.get_module_mock(params=param)
        result = self.module.hot_spare_config(f_module, redfish_str_controller_conn)
        assert result[2] == "JID_XXXXXXXXXXXXX"

        f_module.check_mode = True
        with pytest.raises(Exception) as ex:
            self.module.hot_spare_config(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Changes found to be applied."

        redfish_response_mock.json_data = {"HotspareType": "Global"}
        with pytest.raises(Exception) as ex:
            self.module.hot_spare_config(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "No changes found to be applied."

        json_str = to_text(json.dumps({"data": "out"}))
        redfish_str_controller_conn.invoke_request.side_effect = HTTPError(
            HTTPS_ADDRESS, 400,
            HTTP_ERROR_MSG,
            {"accept-type": "application/json"},
            StringIO(json_str))
        with pytest.raises(Exception) as ex:
            self.module.hot_spare_config(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Unable to locate the physical disk with the ID: Disk.Bay.1:Enclosure.Internal.0-2:RAID.Integrated.1-1"

    def test_ctrl_key(self, redfish_str_controller_conn, redfish_response_mock, mocker):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "command": "SetControllerKey", "controller_id": RAID_INTEGRATED_1_1, "mode": "LKM"}
        mocker.patch(MODULE_PATH + "idrac_redfish_storage_controller.check_id_exists", return_value=None)
        f_module = self.get_module_mock(params=param)
        redfish_response_mock.json_data = {"SecurityStatus": "EncryptionNotCapable", "KeyID": None}
        with pytest.raises(Exception) as ex:
            self.module.ctrl_key(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "The storage controller 'RAID.Integrated.1-1' does not support encryption."

        f_module.check_mode = True
        redfish_response_mock.json_data = {"SecurityStatus": "EncryptionCapable", "KeyID": None}
        with pytest.raises(Exception) as ex:
            self.module.ctrl_key(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Changes found to be applied."

        redfish_response_mock.json_data = {"SecurityStatus": "EncryptionCapable", "KeyID": "Key@123"}
        with pytest.raises(Exception) as ex:
            self.module.ctrl_key(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "No changes found to be applied."

        param.update({"command": "ReKey"})
        f_module = self.get_module_mock(params=param)
        f_module.check_mode = True
        with pytest.raises(Exception) as ex:
            self.module.ctrl_key(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Changes found to be applied."

        f_module.check_mode = False
        redfish_response_mock.json_data = {"SecurityStatus": "EncryptionCapable", "KeyID": None}
        redfish_response_mock.headers = {"Location": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_XXXXXXXXXXXXX"}
        result = self.module.ctrl_key(f_module, redfish_str_controller_conn)
        assert result[2] == "JID_XXXXXXXXXXXXX"

        param.update({"mode": "LKM_"})
        f_module.check_mode = False
        redfish_response_mock.json_data = {"SecurityStatus": "EncryptionCapable", "KeyID": None}
        redfish_response_mock.headers = {"Location": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_XXXXXXXXXXXXX"}
        result = self.module.ctrl_key(f_module, redfish_str_controller_conn)
        assert result[2] == "JID_XXXXXXXXXXXXX"

        param.update({"command": "RemoveControllerKey"})
        redfish_response_mock.json_data = {"SecurityStatus": "EncryptionCapable", "KeyID": 'Key@123'}
        f_module = self.get_module_mock(params=param)
        f_module.check_mode = True
        with pytest.raises(Exception) as ex:
            self.module.ctrl_key(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Changes found to be applied."

        redfish_response_mock.json_data = {"SecurityStatus": "EncryptionCapable", "KeyID": None}
        with pytest.raises(Exception) as ex:
            self.module.ctrl_key(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "No changes found to be applied."

        param.update({"command": "EnableControllerEncryption", "mode": "LKM"})
        f_module = self.get_module_mock(params=param)
        f_module.check_mode = True
        with pytest.raises(Exception) as ex:
            self.module.ctrl_key(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Changes found to be applied."

        redfish_response_mock.json_data = {"SecurityStatus": "SecurityKeyAssigned", "KeyID": None}
        with pytest.raises(Exception) as ex:
            self.module.ctrl_key(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "No changes found to be applied."

        f_module.check_mode = False
        redfish_response_mock.json_data = {"SecurityStatus": "EncryptionCapable", "KeyID": None}
        redfish_response_mock.headers = {"Location": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_XXXXXXXXXXXXX"}
        result = self.module.ctrl_key(f_module, redfish_str_controller_conn)
        assert result[2] == "JID_XXXXXXXXXXXXX"

        param.update({"mode": "LKM_"})
        result = self.module.ctrl_key(f_module, redfish_str_controller_conn)
        assert result[2] == "JID_XXXXXXXXXXXXX"

        param.update({"command": "wrongCommand", "mode": "LKM"})
        f_module = self.get_module_mock(params=param)
        f_module.check_mode = True
        result = self.module.ctrl_key(f_module, redfish_str_controller_conn)
        assert result[2] == "JID_XXXXXXXXXXXXX"

    def test_convert_raid_status(self, redfish_str_controller_conn, redfish_response_mock):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "command": "ConvertToRAID", "target": ["Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                                        "Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1"]}
        f_module = self.get_module_mock(params=param)
        redfish_response_mock.json_data = {"Oem": {"Dell": {"DellPhysicalDisk": {"RaidStatus": "NonRAID"}}}}
        redfish_response_mock.headers = {"Location": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_XXXXXXXXXXXXX"}
        result = self.module.convert_raid_status(f_module, redfish_str_controller_conn)
        assert result[2] == "JID_XXXXXXXXXXXXX"

        f_module.check_mode = True
        with pytest.raises(Exception) as ex:
            self.module.convert_raid_status(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Changes found to be applied."

        f_module.check_mode = False
        redfish_response_mock.json_data = {"Oem": {"Dell": {"DellPhysicalDisk": {"RaidStatus": "Ready"}}}}
        with pytest.raises(Exception) as ex:
            self.module.convert_raid_status(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "No changes found to be applied."

        json_str = to_text(json.dumps({"data": "out"}))
        redfish_str_controller_conn.invoke_request.side_effect = HTTPError(
            HTTPS_ADDRESS, 400,
            HTTP_ERROR_MSG,
            {"accept-type": "application/json"},
            StringIO(json_str))
        with pytest.raises(Exception) as ex:
            self.module.convert_raid_status(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Unable to locate the physical disk with the ID: Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1"

    def test_change_pd_status(self, redfish_str_controller_conn, redfish_response_mock):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "command": "ChangePDStateToOnline",
                 "target": ["Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1",
                            "Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1"]}
        f_module = self.get_module_mock(params=param)
        redfish_response_mock.json_data = {"Oem": {"Dell": {"DellPhysicalDisk": {"RaidStatus": "NonRAID"}}}}
        redfish_response_mock.headers = {"Location": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_XXXXXXXXXXXXX"}
        result = self.module.change_pd_status(f_module, redfish_str_controller_conn)
        assert result[2] == "JID_XXXXXXXXXXXXX"

        f_module.check_mode = True
        with pytest.raises(Exception) as ex:
            self.module.change_pd_status(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Changes found to be applied."

        f_module.check_mode = False
        redfish_response_mock.json_data = {"Oem": {"Dell": {"DellPhysicalDisk": {"RaidStatus": "Online"}}}}
        with pytest.raises(Exception) as ex:
            self.module.change_pd_status(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "No changes found to be applied."

        json_str = to_text(json.dumps({"data": "out"}))
        redfish_str_controller_conn.invoke_request.side_effect = HTTPError(
            HTTPS_ADDRESS, 400,
            HTTP_ERROR_MSG,
            {"accept-type": "application/json"},
            StringIO(json_str))
        with pytest.raises(Exception) as ex:
            self.module.change_pd_status(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Unable to locate the physical disk with the ID: Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1"

    def test_lock_virtual_disk(self, redfish_str_controller_conn, redfish_response_mock, mocker):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "command": "LockVirtualDisk",
                 "volume_id": ["Disk.Virtual.0:RAID.SL.3-1"]
                 }
        f_module = self.get_module_mock(params=param)
        mocker.patch(MODULE_PATH + "idrac_redfish_storage_controller.check_id_exists", return_value=None)
        redfish_response_mock.json_data = {"Oem": {"Dell": {"DellVolume": {"LockStatus": "Unlocked"}}}}
        redfish_response_mock.headers = {"Location": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_XXXXXXXXXXXXX"}
        result = self.module.lock_virtual_disk(f_module, redfish_str_controller_conn)
        assert result[2] == "JID_XXXXXXXXXXXXX"

        f_module.check_mode = True
        with pytest.raises(Exception) as ex:
            self.module.lock_virtual_disk(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Changes found to be applied."

        f_module.check_mode = False
        redfish_response_mock.json_data = {"Oem": {"Dell": {"DellVolume": {"LockStatus": "Locked"}}}}
        with pytest.raises(Exception) as ex:
            self.module.lock_virtual_disk(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "No changes found to be applied."

        redfish_response_mock.json_data = {"Oem": {"Dell": {"DellVolume": {"LockStatus": "Unlocked"}}},
                                           "Links": {
                                               "Drives": [
                                                   {
                                                       ODATA_ID: "/redfish/v1/Systems/System.Embedded.1/"
                                                   },
                                                   {
                                                       ODATA_ID: "/redfish/v1/Systems/System.Embedded.1/"
                                                   }],
                                               "Drives@odata.count": 2}}
        with pytest.raises(Exception) as ex:
            self.module.lock_virtual_disk(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Volume is not encryption capable."

        json_str = to_text(json.dumps({"data": "out"}))
        redfish_str_controller_conn.invoke_request.side_effect = HTTPError(
            HTTPS_ADDRESS, 400,
            HTTP_ERROR_MSG,
            {"accept-type": "application/json"},
            StringIO(json_str))
        with pytest.raises(Exception) as ex:
            self.module.lock_virtual_disk(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Unable to locate the physical disk with the ID: RAID.SL.3-1"

    def test_online_capacity_expansion_raid_type_error(self, redfish_str_controller_conn, redfish_response_mock, mocker):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "command": "OnlineCapacityExpansion",
                 "volume_id": ["Disk.Virtual.0:RAID.SL.3-1"],
                 "target": ["Disk.Bay.2:Enclosure.Internal.0-0:RAID.Integrated.1-1"]}
        f_module = self.get_module_mock(params=param)
        mocker.patch(MODULE_PATH + "idrac_redfish_storage_controller.check_id_exists", return_value=None)
        redfish_response_mock.json_data = {"RAIDType": "RAID50"}
        with pytest.raises(Exception) as ex:
            self.module.online_capacity_expansion(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Online Capacity Expansion is not supported for RAID50 virtual disks."

        redfish_response_mock.json_data = {"RAIDType": "RAID1"}
        with pytest.raises(Exception) as ex:
            self.module.online_capacity_expansion(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Cannot add more than two disks to RAID1 virtual disk."

        json_str = to_text(json.dumps({"data": "out"}))
        redfish_str_controller_conn.invoke_request.side_effect = HTTPError(
            HTTPS_ADDRESS, 400,
            HTTP_ERROR_MSG,
            {"accept-type": "application/json"},
            StringIO(json_str))
        with pytest.raises(Exception) as ex:
            self.module.online_capacity_expansion(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Unable to locate the virtual disk with the ID: Disk.Virtual.0:RAID.SL.3-1"

    def test_online_capacity_expansion_empty_target(self, redfish_str_controller_conn, redfish_response_mock, mocker):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "command": "OnlineCapacityExpansion",
                 "volume_id": ["Disk.Virtual.0:RAID.SL.3-1"],
                 "target": []}
        f_module = self.get_module_mock(params=param)
        mocker.patch(MODULE_PATH + "idrac_redfish_storage_controller.check_id_exists", return_value=None)
        redfish_response_mock.json_data = {"Links": {"Drives": [{ODATA_ID: "Drives/Disk.Bay.0:Enclosure.Internal.0-0:RAID.Integrated.1-1"}]}}
        with pytest.raises(Exception) as ex:
            self.module.online_capacity_expansion(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Provided list of targets is empty."

        param.update({"volume_id": [], "target": None, "size": 3500})
        f_module = self.get_module_mock(params=param)
        with pytest.raises(Exception) as ex:
            self.module.online_capacity_expansion(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "The Fully Qualified Device Descriptor (FQDD) of the target virtual drive must be only one."

    def test_online_capacity_expansion_valid_target(self, redfish_str_controller_conn, redfish_response_mock, mocker):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "command": "OnlineCapacityExpansion",
                 "volume_id": "Disk.Virtual.0:RAID.SL.3-1",
                 "target": ["Disk.Bay.2:Enclosure.Internal.0-0:RAID.Integrated.1-1",
                            "Disk.Bay.3:Enclosure.Internal.0-0:RAID.Integrated.1-1",
                            "Disk.Bay.4:Enclosure.Internal.0-0:RAID.Integrated.1-1"]}
        f_module = self.get_module_mock(params=param)
        mocker.patch(MODULE_PATH + "idrac_redfish_storage_controller.check_id_exists", return_value=None)
        redfish_response_mock.json_data = {"Links": {"Drives": [{ODATA_ID: "/Drives/Disk.Bay.0:Enclosure.Internal.0-0:RAID.Integrated.1-1"}]},
                                           "RAIDType": "RAID0"}
        redfish_response_mock.headers = {"Location": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_XXXXXXXXXXXXX"}
        f_module.check_mode = True
        with pytest.raises(Exception) as ex:
            self.module.online_capacity_expansion(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Changes found to be applied."

        f_module.check_mode = False
        result = self.module.online_capacity_expansion(f_module, redfish_str_controller_conn)
        assert result[2] == "JID_XXXXXXXXXXXXX"

        param.update({"target": ["Disk.Bay.0:Enclosure.Internal.0-0:RAID.Integrated.1-1"]})
        with pytest.raises(Exception) as ex:
            self.module.online_capacity_expansion(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "No changes found to be applied."

        f_module = self.get_module_mock(params=param)
        redfish_response_mock.json_data = {"RAIDType": "RAID10"}
        with pytest.raises(Exception) as ex:
            self.module.online_capacity_expansion(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "No changes found to be applied."

    def test_online_capacity_expansion_size(self, redfish_str_controller_conn, redfish_response_mock, mocker):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "command": "OnlineCapacityExpansion",
                 "volume_id": ["Disk.Virtual.0:RAID.SL.3-1"],
                 "size": 3010}
        f_module = self.get_module_mock(params=param)
        mocker.patch(MODULE_PATH + "idrac_redfish_storage_controller.check_id_exists", return_value=None)
        redfish_response_mock.json_data = {"CapacityBytes": 3145728000}
        redfish_response_mock.headers = {"Location": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_XXXXXXXXXXXXX"}
        with pytest.raises(Exception) as ex:
            self.module.online_capacity_expansion(f_module, redfish_str_controller_conn)
        assert ex.value.args[0] == "Minimum Online Capacity Expansion size must be greater than 100 MB of the current size 3000."

        param.update({"size": 3500})
        result = self.module.online_capacity_expansion(f_module, redfish_str_controller_conn)
        assert result[2] == "JID_XXXXXXXXXXXXX"

        param.update({"size": None})
        result = self.module.online_capacity_expansion(f_module, redfish_str_controller_conn)
        assert result[2] == "JID_XXXXXXXXXXXXX"

    def test_get_current_time(self, redfish_str_controller_conn, redfish_response_mock):
        redfish_response_mock.success = True
        redfish_response_mock.json_data = {"DateTime": "2023-01-09T01:23:40-06:00", "DateTimeLocalOffset": "-06:00"}
        resp = self.module.get_current_time(redfish_str_controller_conn)
        assert resp[0] == "2023-01-09T01:23:40-06:00"
        assert resp[1] == "-06:00"

        json_str = to_text(json.dumps({"data": "out"}))
        redfish_str_controller_conn.invoke_request.side_effect = HTTPError(
            HTTPS_ADDRESS, 400,
            HTTP_ERROR_MSG,
            {"accept-type": "application/json"},
            StringIO(json_str))
        resp = self.module.get_current_time(redfish_str_controller_conn)
        assert resp[0] is None
        assert resp[1] is None

    def test_validate_time(self, redfish_str_controller_conn, redfish_response_mock, redfish_default_args):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "controller_id": RAID_INTEGRATED_1_1,
                 "attributes": {"ControllerMode": "RAID", "CheckConsistencyMode": "Normal"},
                 "job_wait": True, "apply_time": "InMaintenanceWindowOnReset",
                 "maintenance_window": {"start_time": "2023-09-30T05:15:40-06:00", "duration": 900}}
        redfish_default_args.update(param)
        f_module = self.get_module_mock(params=param)
        redfish_response_mock.success = True
        redfish_response_mock.json_data = {"DateTime": "2023-01-09T01:23:40-06:00", "DateTimeLocalOffset": "-06:00"}
        with pytest.raises(Exception):
            result = self.module.validate_time(f_module, redfish_str_controller_conn, "2023-01-09T01:23:40-05:00")
            assert result["msg"] == "The maintenance time must be post-fixed with local offset to -05:00."

        redfish_response_mock.json_data = {"DateTime": "2023-01-09T01:23:40-06:00", "DateTimeLocalOffset": "-06:00"}
        with pytest.raises(Exception):
            result = self.module.validate_time(f_module, redfish_str_controller_conn, "2022-01-09T01:23:40-05:00")
            assert result["msg"] == "The specified maintenance time window occurs in the past, provide a future time" \
                                    " to schedule the maintenance window."

        redfish_response_mock.json_data = {"DateTime": "2023-10-09T01:23:40+06:00", "DateTimeLocalOffset": "+06:00"}
        with pytest.raises(Exception):
            result = self.module.validate_time(f_module, redfish_str_controller_conn, "2023-09-09T01:23:40+06:00")
            assert result["msg"] == "The specified maintenance time window occurs in the past, provide a future time" \
                                    " to schedule the maintenance window."

    def test_check_attr_exists(self, redfish_str_controller_conn, redfish_response_mock):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "controller_id": RAID_INTEGRATED_1_1,
                 "attributes": {"ControllerMode": "RAID", "CheckConsistencyMode": "Normal"},
                 "job_wait": True, "apply_time": "InMaintenanceWindowOnReset",
                 "maintenance_window": {"start_time": "2023-09-30T05:15:40-06:00", "duration": 900}}
        curr_attr = {"ControllerMode": "RAID", "CheckConsistencyMode": "StopOnError", "LoadBalanceMode": "Automatic"}
        f_module = self.get_module_mock(params=param)
        redfish_response_mock.success = True
        redfish_response_mock.status_code = 200
        result = self.module.check_attr_exists(f_module, curr_attr, param["attributes"])
        assert result["CheckConsistencyMode"] == "Normal"
        f_module.check_mode = True
        with pytest.raises(Exception) as ex:
            self.module.check_attr_exists(f_module, curr_attr, param["attributes"])
        assert ex.value.args[0] == "Changes found to be applied."
        f_module.check_mode = False
        with pytest.raises(Exception) as ex:
            self.module.check_attr_exists(f_module, curr_attr, {"ControllerMode": "RAID",
                                                                "CheckConsistencyMode": "StopOnError"})
        assert ex.value.args[0] == "No changes found to be applied."
        f_module.check_mode = False
        with pytest.raises(Exception) as ex:
            self.module.check_attr_exists(f_module, curr_attr, {"ControllerMode": "RAID",
                                                                "CheckConsistency": "StopOnError"})
        assert ex.value.args[0] == "The following attributes are invalid: ['CheckConsistency']"

    def test_get_attributes(self, redfish_str_controller_conn, redfish_response_mock):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "controller_id": RAID_INTEGRATED_1_1,
                 "attributes": {"ControllerMode": "RAID", "CheckConsistencyMode": "Normal"},
                 "job_wait": True, "apply_time": "InMaintenanceWindowOnReset",
                 "maintenance_window": {"start_time": "2023-09-30T05:15:40-06:00", "duration": 900}}
        resp = {"@Redfish.Settings": {"SupportedApplyTimes": ["Immediate", "OnReset", "AtMaintenanceWindowStart",
                                                              "InMaintenanceWindowOnReset"]},
                "Id": RAID_INTEGRATED_1_1,
                "Oem": {
                    "Dell": {
                        "DellStorageController": {
                            "AlarmState": "AlarmNotPresent",
                            "AutoConfigBehavior": "NotApplicable",
                            "BackgroundInitializationRatePercent": 30,
                            "BatteryLearnMode": "null",
                            "BootVirtualDiskFQDD": "null",
                            "CacheSizeInMB": 2048,
                            "CachecadeCapability": "NotSupported",
                            "CheckConsistencyMode": "StopOnError",
                            "ConnectorCount": 2,
                            "ControllerBootMode": "ContinueBootOnError",
                            "ControllerFirmwareVersion": "25.5.9.0001",
                            "ControllerMode": "RAID",
                            "CopybackMode": "OnWithSMART",
                            "CurrentControllerMode": "RAID",
                            "Device": "0",
                            "DeviceCardDataBusWidth": "Unknown",
                            "DeviceCardSlotLength": "Unknown",
                            "DeviceCardSlotType": "Unknown",
                            "DriverVersion": "6.706.06.00",
                            "EncryptionCapability": "LocalKeyManagementCapable",
                            "EncryptionMode": "LocalKeyManagement",
                            "EnhancedAutoImportForeignConfigurationMode": "Disabled",
                            "KeyID": "MyNewKey@123",
                            "LastSystemInventoryTime": "2022-12-23T04:59:41+00:00",
                            "LastUpdateTime": "2022-12-23T17:59:44+00:00",
                            "LoadBalanceMode": "Automatic",
                            "MaxAvailablePCILinkSpeed": "Generation 3",
                            "MaxDrivesInSpanCount": 32,
                            "MaxPossiblePCILinkSpeed": "Generation 3",
                            "MaxSpansInVolumeCount": 8,
                            "MaxSupportedVolumesCount": 64,
                            "PCISlot": "null",
                            "PatrolReadIterationsCount": 0,
                            "PatrolReadMode": "Automatic",
                            "PatrolReadRatePercent": 30,
                            "PatrolReadState": "Stopped",
                            "PatrolReadUnconfiguredAreaMode": "Enabled",
                            "PersistentHotspare": "Disabled",
                            "PersistentHotspareMode": "Disabled",
                            "RAIDMode": "None",
                            "RealtimeCapability": "Capable",
                            "ReconstructRatePercent": 30,
                            "RollupStatus": "OK",
                            "SASAddress": "54CD98F0760C3D00",
                            "SecurityStatus": "SecurityKeyAssigned",
                            "SharedSlotAssignmentAllowed": "NotApplicable",
                            "SlicedVDCapability": "Supported",
                            "SpindownIdleTimeSeconds": 30,
                            "SupportControllerBootMode": "Supported",
                            "SupportEnhancedAutoForeignImport": "Supported",
                            "SupportRAID10UnevenSpans": "Supported",
                            "SupportedInitializationTypes": [
                                "Slow",
                                "Fast"],
                            "SupportedInitializationTypes@odata.count": 2,
                            "SupportsLKMtoSEKMTransition": "No",
                            "T10PICapability": "NotSupported"
                        }
                    }}}
        f_module = self.get_module_mock(params=param)
        redfish_response_mock.success = True
        redfish_response_mock.json_data = resp
        result = self.module.get_attributes(f_module, redfish_str_controller_conn)
        assert result == resp

        json_str = to_text(json.dumps({"data": "out"}))
        redfish_str_controller_conn.invoke_request.side_effect = HTTPError(
            HTTPS_ADDRESS, 400,
            HTTP_ERROR_MSG,
            {"accept-type": "application/json"},
            StringIO(json_str))
        resp = self.module.get_attributes(f_module, redfish_str_controller_conn)
        assert resp == {}

    def test_get_redfish_apply_time(self, redfish_str_controller_conn, redfish_response_mock):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "controller_id": RAID_INTEGRATED_1_1,
                 "attributes": {"ControllerMode": "RAID", "CheckConsistencyMode": "Normal"},
                 "job_wait": True, "apply_time": "InMaintenanceWindowOnReset",
                 "maintenance_window": {"start_time": "2023-09-30T05:15:40-06:00", "duration": 900}}
        time_settings = ["Immediate", "OnReset", "AtMaintenanceWindowStart", "InMaintenanceWindowOnReset"]
        f_module = self.get_module_mock(params=param)
        redfish_response_mock.success = True
        redfish_response_mock.json_data = {"DateTime": "2023-01-09T01:23:40-06:00", "DateTimeLocalOffset": "-06:00"}
        result = self.module.get_redfish_apply_time(f_module, redfish_str_controller_conn, param["apply_time"],
                                                    time_settings)
        assert result['ApplyTime'] == param['apply_time']
        assert result['MaintenanceWindowDurationInSeconds'] == 900
        assert result['MaintenanceWindowStartTime'] == '2023-09-30T05:15:40-06:00'

        param1 = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                  "controller_id": RAID_INTEGRATED_1_1,
                  "attributes": {"ControllerMode": "RAID", "CheckConsistencyMode": "Normal"},
                  "job_wait": True, "apply_time": "InMaintenanceWindowOnReset",
                  "maintenance_window": {"start_time": "2023-09-30T05:15:40-06:00", "duration": 900}}
        f_module = self.get_module_mock(params=param1)
        redfish_response_mock.json_data = {"DateTime": "2023-01-09T01:23:40-06:00", "DateTimeLocalOffset": "-06:00"}
        result = self.module.get_redfish_apply_time(f_module, redfish_str_controller_conn, param1["apply_time"],
                                                    time_settings)
        assert result['ApplyTime'] == param1['apply_time']

        result = self.module.get_redfish_apply_time(f_module, redfish_str_controller_conn,
                                                    param1["apply_time"], [])
        assert result == {}

        with pytest.raises(Exception):
            result = self.module.get_redfish_apply_time(f_module, redfish_str_controller_conn,
                                                        param1["apply_time"], ['NotEmpty'])
            assert result["status_msg"] == "Apply time InMaintenanceWindowOnReset is not supported."

    def test_apply_attributes(self, redfish_str_controller_conn, redfish_response_mock):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "controller_id": RAID_INTEGRATED_1_1,
                 "attributes": {"ControllerMode": "RAID", "CheckConsistencyMode": "Normal"},
                 "job_wait": True, "apply_time": "Immediate"}
        time_settings = ["Immediate", "OnReset", "AtMaintenanceWindowStart", "InMaintenanceWindowOnReset"]
        f_module = self.get_module_mock(params=param)
        redfish_response_mock.success = True
        redfish_response_mock.json_data = {"DateTime": "2023-01-09T01:23:40-06:00", "DateTimeLocalOffset": "-06:00"}
        redfish_response_mock.headers = {"Location": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_XXXXXXXXXXXXX"}
        job_id, time_set = self.module.apply_attributes(f_module, redfish_str_controller_conn,
                                                        {"CheckConsistencyMode": "StopOnError"},
                                                        time_settings)
        assert job_id == "JID_XXXXXXXXXXXXX"
        assert time_set == {'ApplyTime': "Immediate"}

        redfish_response_mock.status_code = 202
        redfish_response_mock.json_data = {"error": {"@Message.ExtendedInfo": [
            {"Message": "The value 'abcd' for the property PatrolReadMode is not in the list of acceptable values.",
             "MessageArgs": ["abcd", "PatrolReadMode"], "MessageArgs@odata.count": 2,
             "MessageId": "Base.1.12.PropertyValueNotInList",
             "RelatedProperties": ["#/Oem/Dell/DellStorageController/PatrolReadMode"],
             "RelatedProperties@odata.count": 1,
             "Resolution": "Choose a value from the enumeration list that the implementation can support and"
                           "resubmit the request if the operation failed.", "Severity": "Warning"}
        ]}}
        with pytest.raises(Exception) as ex:
            self.module.apply_attributes(f_module, redfish_str_controller_conn, {"CheckConsistencyMode": "StopOnError"},
                                         time_settings)
        assert ex.value.args[0] == "Unable to configure the controller attribute(s) settings."

        time_settings = []
        with pytest.raises(Exception) as ex:
            job_id, time_set = self.module.apply_attributes(f_module, redfish_str_controller_conn,
                                                            {"CheckConsistencyMode": "StopOnError"},
                                                            time_settings)
            assert job_id == "JID_XXXXXXXXXXXXX"
            assert time_set == {}

        json_str = to_text(json.dumps({"data": "out"}))
        redfish_str_controller_conn.invoke_request.side_effect = HTTPError(
            HTTPS_ADDRESS, 400,
            HTTP_ERROR_MSG,
            {"accept-type": "application/json"},
            StringIO(json_str))
        with pytest.raises(Exception) as ex:
            self.module.apply_attributes(f_module, redfish_str_controller_conn, {"CheckConsistencyMode": "StopOnError"},
                                         time_settings)
        assert ex.value.args[0] == "Unable to configure the controller attribute(s) settings."

    def test_set_attributes(self, redfish_str_controller_conn, redfish_response_mock):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "controller_id": RAID_INTEGRATED_1_1, "attributes": {"ControllerMode": "HBA"},
                 "job_wait": True, "apply_time": "Immediate"}
        resp = {"@Redfish.Settings": {"SupportedApplyTimes": ["Immediate", "OnReset", "AtMaintenanceWindowStart",
                                                              "InMaintenanceWindowOnReset"]},
                "Id": RAID_INTEGRATED_1_1,
                "Oem": {
                    "Dell": {
                        "DellStorageController": {
                            "AlarmState": "AlarmNotPresent",
                            "AutoConfigBehavior": "NotApplicable",
                            "BackgroundInitializationRatePercent": 30,
                            "BatteryLearnMode": "null",
                            "BootVirtualDiskFQDD": "null",
                            "CacheSizeInMB": 2048,
                            "CachecadeCapability": "NotSupported",
                            "CheckConsistencyMode": "StopOnError",
                            "ConnectorCount": 2,
                            "ControllerBootMode": "ContinueBootOnError",
                            "ControllerFirmwareVersion": "25.5.9.0001",
                            "ControllerMode": "RAID",
                            "CopybackMode": "OnWithSMART",
                            "CurrentControllerMode": "RAID",
                            "Device": "0",
                            "DeviceCardDataBusWidth": "Unknown",
                            "DeviceCardSlotLength": "Unknown",
                            "DeviceCardSlotType": "Unknown",
                            "DriverVersion": "6.706.06.00",
                            "EncryptionCapability": "LocalKeyManagementCapable",
                            "EncryptionMode": "LocalKeyManagement",
                            "EnhancedAutoImportForeignConfigurationMode": "Disabled",
                            "KeyID": "MyNewKey@123",
                            "LastSystemInventoryTime": "2022-12-23T04:59:41+00:00",
                            "LastUpdateTime": "2022-12-23T17:59:44+00:00",
                            "LoadBalanceMode": "Automatic",
                            "MaxAvailablePCILinkSpeed": "Generation 3",
                            "MaxDrivesInSpanCount": 32,
                            "MaxPossiblePCILinkSpeed": "Generation 3",
                            "MaxSpansInVolumeCount": 8,
                            "MaxSupportedVolumesCount": 64,
                            "PCISlot": "null",
                            "PatrolReadIterationsCount": 0,
                            "PatrolReadMode": "Automatic",
                            "PatrolReadRatePercent": 30,
                            "PatrolReadState": "Stopped",
                            "PatrolReadUnconfiguredAreaMode": "Enabled",
                            "PersistentHotspare": "Disabled",
                            "PersistentHotspareMode": "Disabled",
                            "RAIDMode": "None",
                            "RealtimeCapability": "Capable",
                            "ReconstructRatePercent": 30,
                            "RollupStatus": "OK",
                            "SASAddress": "54CD98F0760C3D00",
                            "SecurityStatus": "SecurityKeyAssigned",
                            "SharedSlotAssignmentAllowed": "NotApplicable",
                            "SlicedVDCapability": "Supported",
                            "SpindownIdleTimeSeconds": 30,
                            "SupportControllerBootMode": "Supported",
                            "SupportEnhancedAutoForeignImport": "Supported",
                            "SupportRAID10UnevenSpans": "Supported",
                            "SupportedInitializationTypes": [
                                "Slow",
                                "Fast"
                            ],
                            "SupportedInitializationTypes@odata.count": 2,
                            "SupportsLKMtoSEKMTransition": "No",
                            "T10PICapability": "NotSupported"
                        }
                    }}}
        f_module = self.get_module_mock(params=param)
        redfish_response_mock.success = True
        redfish_response_mock.json_data = resp
        redfish_response_mock.headers = {"Location": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_XXXXXXXXXXXXX"}
        job_id, time_set = self.module.set_attributes(f_module, redfish_str_controller_conn)
        assert job_id == "JID_XXXXXXXXXXXXX"
        assert time_set == {'ApplyTime': "Immediate"}

        param.update({"attributes": {"ControllerMode": "HBA", 'RandomKey': 123}})
        f_module = self.get_module_mock(params=param)
        with pytest.raises(Exception):
            result = self.module.set_attributes(f_module, redfish_str_controller_conn)
            assert result['msg'] == "Other attributes cannot be updated when ControllerMode is provided as input."

    def test_secure_erase(self, redfish_str_controller_conn, redfish_response_mock, redfish_default_args, mocker):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password", "command": "SecureErase"}
        module = 'idrac_redfish_storage_controller.'
        redfish_default_args.update(param)
        drive_id_1 = "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Integrated.1-1"

        def common_data_in_mock_dynamic_request(args):
            odata = ODATA_ID
            storage_uri = "/redfish/v1/Systems/System.Embedded.1/Storage"
            drive_uri = storage_uri + "/RAID.Integrated.1-1/Drives/" + drive_id_1
            if args[2] == "Storage":
                return {odata: storage_uri}
            elif args[2] == "Members":
                return [{odata: storage_uri + "/RAID.Integrated.1-1"},
                        {odata: storage_uri + "/AHCI.Embedded.2-1"}]
            elif args[2] == "Drives":
                return [{odata: storage_uri + drive_uri},
                        {odata: storage_uri + "/RAID.Integrated.1-1/Drives/Disk.Bay.1:Enclosure.Internal.0-1:RAID.Integrated.1-1"}]
            elif args[2] == "Actions":
                return {"#Drive.SecureErase": {"target": drive_uri + "/Actions/Drive.SecureErase"}}

        def mock_get_dynamic_uri_request_1(*args, **kwargs):
            if len(args) > 2:
                return common_data_in_mock_dynamic_request(args)
            return {"Oem": {"Dell": {"DellPhysicalDisk": {"RaidStatus": "Online",
                                                          "SystemEraseCapability": "NotSupported"}}}}

        mocker.patch(MODULE_PATH + module + "get_dynamic_uri", side_effect=mock_get_dynamic_uri_request_1)
        mocker.patch(MODULE_PATH + module + "validate_and_get_first_resource_id_uri",
                     return_value=("/redfish/v1/Systems", None))

        # Scenario 1: When command is set to SecureErase but controller_id and target is not provided
        with pytest.raises(Exception) as ex:
            self._run_module(redfish_default_args)
        assert ex.value.args[0]["msg"] == "command is SecureErase but all of the following are missing: controller_id, target"

        # Scenario 2: When command is set to SecureErase and only controller_id is provided
        redfish_default_args.update({"controller_id": RAID_INTEGRATED_1_1})
        with pytest.raises(Exception) as ex:
            self._run_module(redfish_default_args)
        assert ex.value.args[0]["msg"] == "command is SecureErase but all of the following are missing: target"

        # Scenario 3: When command is set to SecureErase and wrong controller_id is provided
        redfish_default_args.update({"controller_id": "xyz",
                                     "target": drive_id_1})
        result = self._run_module(redfish_default_args)
        assert result["msg"] == "Unable to locate the storage controller with the ID: xyz"

        # Scenario 3A: When command is set to SecureErase and partial controller_id is provided
        redfish_default_args.update({"controller_id": "RAID.Integrated",
                                     "target": drive_id_1})
        result = self._run_module(redfish_default_args)
        assert result["msg"] == "Unable to locate the storage controller with the ID: RAID.Integrated"

        # Scenario 4: When command is set to SecureErase and wrong target is provided
        redfish_default_args.update({"controller_id": RAID_INTEGRATED_1_1,
                                     "target": "target"})
        result = self._run_module(redfish_default_args)
        assert result["msg"] == "Unable to locate the physical disk with the ID: target"

        # Scenario 4A: When command is set to SecureErase and partial target is provided
        redfish_default_args.update({"controller_id": RAID_INTEGRATED_1_1,
                                     "target": "Disk.Bay"})
        result = self._run_module(redfish_default_args)
        assert result["msg"] == "Unable to locate the physical disk with the ID: Disk.Bay"

        # Scenario 5: When drive is not ready, in Online state
        redfish_default_args.update({"controller_id": RAID_INTEGRATED_1_1,
                                     "target": drive_id_1})
        mocker.patch(MODULE_PATH + module + "get_idrac_firmware_version", return_value='7.10')
        mocker.patch(MODULE_PATH + module + "get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request_1)
        result = self._run_module(redfish_default_args)
        assert result["msg"] == "Drive {0} is not in ready state.".format(drive_id_1)

        # Scneario 6: When drive is ready but not support secure erase
        def mock_get_dynamic_uri_request_2(*args, **kwargs):
            if len(args) > 2:
                return common_data_in_mock_dynamic_request(args)
            return {"Oem": {"Dell": {"DellPhysicalDisk": {"RaidStatus": "Ready",
                                                          "SystemEraseCapability": "NotSupported"}}}}

        redfish_default_args.update({"controller_id": RAID_INTEGRATED_1_1,
                                     "target": drive_id_1})
        mocker.patch(MODULE_PATH + module + "get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request_2)
        result = self._run_module(redfish_default_args)
        assert result["msg"] == "Drive {0} does not support secure erase operation.".format(drive_id_1)

        # Scenario 7: When drive is ready and support secure erase, job_wait is false
        def mock_get_dynamic_uri_request_3(*args, **kwargs):
            if len(args) > 2:
                return common_data_in_mock_dynamic_request(args)
            return {"Oem": {"Dell": {"DellPhysicalDisk": {"RaidStatus": "Ready",
                                                          "SystemEraseCapability": "CryptographicErasePD"}}}}
        redfish_default_args.update({"controller_id": RAID_INTEGRATED_1_1,
                                     "target": drive_id_1,
                                     "job_wait": False})
        mocker.patch(MODULE_PATH + module + "get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request_3)
        result = self._run_module(redfish_default_args)
        assert result["msg"] == "Successfully submitted the job that performs the 'SecureErase' operation."

        # Scenario 8: When drive is ready and support secure erase, job_wait is true
        redfish_default_args.update({"controller_id": RAID_INTEGRATED_1_1,
                                     "target": drive_id_1,
                                     "job_wait": True,
                                     "job_wait_timeout": 2})
        obj = MagicMock()
        obj.json_data = {'JobState': 'Completed'}
        mocker.patch(MODULE_PATH + module + "wait_for_job_completion", return_value=(obj, ''))
        result = self._run_module(redfish_default_args)
        assert result["msg"] == "Successfully performed the 'SecureErase' operation."

        # Scenario 9: When one Job is already running, and another trigger
        redfish_default_args.update({"controller_id": RAID_INTEGRATED_1_1,
                                     "target": drive_id_1})
        mocker.patch(MODULE_PATH + module + "get_scheduled_job_resp", return_value={"Id": 'JOB_XXXX'})
        result = self._run_module(redfish_default_args)
        assert result["msg"] == "Unable to complete the operation because another job already exists." + \
            " Wait for the pending job to complete and retry the operation."

    def test_main_success_attributes(self, redfish_str_controller_conn, redfish_response_mock, redfish_default_args, mocker):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "controller_id": None,
                 "attributes": {"ControllerMode": "RAID", "CheckConsistencyMode": "Normal"},
                 "job_wait": True, "apply_time": "Immediate"}
        resp = {"@Redfish.Settings": {"SupportedApplyTimes": ["Immediate", "OnReset", "AtMaintenanceWindowStart",
                                                              "InMaintenanceWindowOnReset"]},
                "Id": RAID_INTEGRATED_1_1,
                "Oem": {
                    "Dell": {
                        "DellStorageController": {
                            "AlarmState": "AlarmNotPresent",
                            "AutoConfigBehavior": "NotApplicable",
                            "BackgroundInitializationRatePercent": 30,
                            "BatteryLearnMode": "null",
                            "BootVirtualDiskFQDD": "null",
                            "CacheSizeInMB": 2048,
                            "CachecadeCapability": "NotSupported",
                            "CheckConsistencyMode": "StopOnError",
                            "ConnectorCount": 2,
                            "ControllerBootMode": "ContinueBootOnError",
                            "ControllerFirmwareVersion": "25.5.9.0001",
                            "ControllerMode": "RAID",
                            "CopybackMode": "OnWithSMART",
                            "CurrentControllerMode": "RAID",
                            "Device": "0",
                            "DeviceCardDataBusWidth": "Unknown",
                            "DeviceCardSlotLength": "Unknown",
                            "DeviceCardSlotType": "Unknown",
                            "DriverVersion": "6.706.06.00",
                            "EncryptionCapability": "LocalKeyManagementCapable",
                            "EncryptionMode": "LocalKeyManagement",
                            "EnhancedAutoImportForeignConfigurationMode": "Disabled",
                            "KeyID": "MyNewKey@123",
                            "LastSystemInventoryTime": "2022-12-23T04:59:41+00:00",
                            "LastUpdateTime": "2022-12-23T17:59:44+00:00",
                            "LoadBalanceMode": "Automatic",
                            "MaxAvailablePCILinkSpeed": "Generation 3",
                            "MaxDrivesInSpanCount": 32,
                            "MaxPossiblePCILinkSpeed": "Generation 3",
                            "MaxSpansInVolumeCount": 8,
                            "MaxSupportedVolumesCount": 64,
                            "PCISlot": "null",
                            "PatrolReadIterationsCount": 0,
                            "PatrolReadMode": "Automatic",
                            "PatrolReadRatePercent": 30,
                            "PatrolReadState": "Stopped",
                            "PatrolReadUnconfiguredAreaMode": "Enabled",
                            "PersistentHotspare": "Disabled",
                            "PersistentHotspareMode": "Disabled",
                            "RAIDMode": "None",
                            "RealtimeCapability": "Capable",
                            "ReconstructRatePercent": 30,
                            "RollupStatus": "OK",
                            "SASAddress": "54CD98F0760C3D00",
                            "SecurityStatus": "SecurityKeyAssigned",
                            "SharedSlotAssignmentAllowed": "NotApplicable",
                            "SlicedVDCapability": "Supported",
                            "SpindownIdleTimeSeconds": 30,
                            "SupportControllerBootMode": "Supported",
                            "SupportEnhancedAutoForeignImport": "Supported",
                            "SupportRAID10UnevenSpans": "Supported",
                            "SupportedInitializationTypes": [
                                "Slow",
                                "Fast"
                            ],
                            "SupportedInitializationTypes@odata.count": 2,
                            "SupportsLKMtoSEKMTransition": "No",
                            "T10PICapability": "NotSupported"
                        }
                    }}}
        redfish_default_args.update(param)
        mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.check_id_exists', return_value=None)
        result = self._run_module(redfish_default_args)
        assert result['msg'] == "controller_id is required to perform this operation."
        param.update({"controller_id": RAID_INTEGRATED_1_1})
        param.update({"job_wait": False})
        redfish_default_args.update(param)
        mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.check_id_exists', return_value=None)
        mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.set_attributes',
                     return_value=("JID_XXXXXXXXXXXXX", {'ApplyTime': "Immediate"}))
        result = self._run_module(redfish_default_args)
        assert result["task"]["id"] == "JID_XXXXXXXXXXXXX"
        param.update({"job_wait": True})
        redfish_default_args.update(param)
        redfish_response_mock.json_data = {"JobState": "Completed"}
        mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.check_id_exists', return_value=None)
        mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.set_attributes',
                     return_value=("JID_XXXXXXXXXXXXX", {'ApplyTime': "Immediate"}))
        mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.wait_for_job_completion',
                     return_value=(redfish_response_mock, "Success"))
        result = self._run_module(redfish_default_args)
        assert result['msg'] == "Successfully applied the controller attributes."

        redfish_response_mock.json_data = {"JobState": "Failed"}
        result = self._run_module(redfish_default_args)
        assert result['msg'] == "Successfully applied the controller attributes."

    @pytest.mark.parametrize("exc_type", [RuntimeError, URLError, SSLValidationError, ConnectionError, KeyError,
                                          ImportError, ValueError, TypeError, HTTPError])
    def test_main_error(self, redfish_str_controller_conn, redfish_response_mock, mocker,
                        exc_type, redfish_default_args):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "command": "ResetConfig", "controller_id": RAID_INTEGRATED_1_1}
        redfish_default_args.update(param)
        mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.validate_inputs', return_value=None)
        redfish_response_mock.success = False
        redfish_response_mock.status_code = 400
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.ctrl_reset_config',
                         side_effect=exc_type("url open error"))
            result = self._run_module(redfish_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.ctrl_reset_config',
                         side_effect=exc_type('exception message'))
            result = self._run_module(redfish_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.ctrl_reset_config',
                         side_effect=exc_type(HTTPS_ADDRESS, 400, HTTP_ERROR_MSG,
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module(redfish_default_args)
            assert result['failed'] is True
        assert 'msg' in result

    def test_main_success(self, redfish_str_controller_conn, redfish_response_mock, redfish_default_args, mocker):
        param = {"baseuri": "XX.XX.XX.XX", "username": "username", "password": "password",
                 "command": "SetControllerKey", "key": "Key@123", "key_id": "keyid@123",
                 "controller_id": RAID_INTEGRATED_1_1,
                 "target": ["Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1"]}
        redfish_default_args.update(param)
        mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.validate_inputs', return_value=None)
        mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.ctrl_key',
                     return_value=("", "", "JID_XXXXXXXXXXXXX"))
        result = self._run_module(redfish_default_args)
        assert result["task"]["id"] == "JID_XXXXXXXXXXXXX"
        param.update({"command": "AssignSpare"})
        redfish_default_args.update(param)
        mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.hot_spare_config',
                     return_value=("", "", "JID_XXXXXXXXXXXXX"))
        result = self._run_module(redfish_default_args)
        assert result["task"]["id"] == "JID_XXXXXXXXXXXXX"
        param.update({"command": "BlinkTarget"})
        redfish_default_args.update(param)
        redfish_response_mock.status_code = 200
        mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.target_identify_pattern',
                     return_value=redfish_response_mock)
        result = self._run_module(redfish_default_args)
        assert result["msg"] == "Successfully performed the 'BlinkTarget' operation."
        param.update({"command": "ConvertToRAID"})
        redfish_default_args.update(param)
        mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.convert_raid_status',
                     return_value=("", "", "JID_XXXXXXXXXXXXX"))
        result = self._run_module(redfish_default_args)
        assert result["task"]["id"] == "JID_XXXXXXXXXXXXX"
        param.update({"command": "ChangePDStateToOnline", "job_wait": True})
        redfish_default_args.update(param)
        mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.change_pd_status',
                     return_value=("", "", "JID_XXXXXXXXXXXXX"))
        mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.wait_for_job_completion',
                     return_value=(redfish_response_mock, ""))
        mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.strip_substr_dict',
                     return_value={"JobState": "Failed"})
        result = self._run_module(redfish_default_args)
        assert result["task"]["id"] == "JID_XXXXXXXXXXXXX"
        mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.strip_substr_dict',
                     return_value={"JobState": "Completed"})
        result = self._run_module(redfish_default_args)
        assert result["task"]["id"] == "JID_XXXXXXXXXXXXX"
        param.update({"command": "OnlineCapacityExpansion", "job_wait": True, "volume_id": ['123']})
        redfish_default_args.update(param)
        mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.online_capacity_expansion',
                     return_value=("", "", "JID_XXXXXXXXXXXXX"))
        result = self._run_module(redfish_default_args)
        assert result["task"]["id"] == "JID_XXXXXXXXXXXXX"
        param.update({"command": "LockVirtualDisk", "job_wait": True, "volume_id": ['123']})
        redfish_default_args.update(param)
        mocker.patch(MODULE_PATH + 'idrac_redfish_storage_controller.lock_virtual_disk',
                     return_value=("", "", "JID_XXXXXXXXXXXXX"))
        result = self._run_module(redfish_default_args)
        assert result["task"]["id"] == "JID_XXXXXXXXXXXXX"
