# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.3.0
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import redfish_storage_volume
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


@pytest.fixture
def redfish_connection_mock_for_storage_volume(mocker, redfish_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'redfish_storage_volume.Redfish')
    redfish_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    redfish_connection_mock_obj.invoke_request.return_value = redfish_response_mock
    return redfish_connection_mock_obj


class TestStorageVolume(FakeAnsibleModule):
    module = redfish_storage_volume

    @pytest.fixture
    def storage_volume_base_uri(self):
        self.module.storage_collection_map.update({"storage_base_uri": "/redfish/v1/Systems/System.Embedded.1/Storage"})

    arg_list1 = [{"state": "present"}, {"state": "present", "volume_id": "volume_id"},
                 {"state": "absent", "volume_id": "volume_id"},
                 {"command": "initialize", "volume_id": "volume_id"},
                 {"state": "present", "volume_type": "NonRedundant",
                  "name": "name", "controller_id": "controller_id",
                  "drives": ["drive1"],
                  "block_size_bytes": 123,
                  "capacity_bytes": "1234567",
                  "optimum_io_size_bytes": "1024",
                  "encryption_types": "NativeDriveEncryption",
                  "encrypted": False,
                  "volume_id": "volume_id", "oem": {"Dell": "DellAttributes"},
                  "initialize_type": "Slow"
                  }]

    @pytest.mark.parametrize("param", arg_list1)
    def test_redfish_storage_volume_main_success_case_01(self, mocker, redfish_default_args, module_mock,
                                                         redfish_connection_mock_for_storage_volume, param):
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.validate_inputs')
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.fetch_storage_resource')
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.configure_raid_operation',
                     return_value={"msg": "Successfully submitted volume task.",
                                   "task_uri": "task_uri",
                                   "task_id": 1234})
        redfish_default_args.update(param)
        result = self._run_module(redfish_default_args)
        assert result["changed"] is True
        assert result['msg'] == "Successfully submitted volume task."
        assert result["task"]["id"] == 1234
        assert result["task"]["uri"] == "task_uri"

    arg_list2 = [
        {"state": "absent"},
        {"command": "initialize"}, {}]

    @pytest.mark.parametrize("param", arg_list2)
    def test_redfish_storage_volume_main_failure_case_01(self, param, redfish_default_args, module_mock):
        """required parameter is not passed along with specified report_type"""
        redfish_default_args.update(param)
        result = self._run_module_with_fail_json(redfish_default_args)
        assert 'msg' in result
        assert "task" not in result
        assert result['failed'] is True

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_redfish_storage_volume_main_exception_handling_case(self, exc_type, mocker, redfish_default_args,
                                                                 redfish_connection_mock_for_storage_volume,
                                                                 redfish_response_mock):
        redfish_default_args.update({"state": "present"})
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.validate_inputs')
        redfish_response_mock.status_code = 400
        redfish_response_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))

        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'redfish_storage_volume.configure_raid_operation',
                         side_effect=exc_type('test'))
        else:
            mocker.patch(MODULE_PATH + 'redfish_storage_volume.configure_raid_operation',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
        result = self._run_module_with_fail_json(redfish_default_args)
        assert 'task' not in result
        assert 'msg' in result
        assert result['failed'] is True
        if exc_type == HTTPError:
            assert 'error_info' in result

    msg1 = "Either state or command should be provided to further actions."
    msg2 = "When state is present, either controller_id or volume_id must be specified to perform further actions."

    @pytest.mark.parametrize("input",
                             [{"param": {"xyz": 123}, "msg": msg1}, {"param": {"state": "present"}, "msg": msg2}])
    def test_validate_inputs_error_case_01(self, input):
        f_module = self.get_module_mock(params=input["param"])
        with pytest.raises(Exception) as exc:
            self.module.validate_inputs(f_module)
        assert exc.value.args[0] == input["msg"]

    def test_get_success_message_case_01(self):
        action = "create"
        message = self.module.get_success_message(action, "JobService/Jobs/JID_1234")
        assert message["msg"] == "Successfully submitted {0} volume task.".format(action)
        assert message["task_uri"] == "JobService/Jobs/JID_1234"
        assert message["task_id"] == "JID_1234"

    def test_get_success_message_case_02(self):
        action = "create"
        message = self.module.get_success_message(action, None)
        assert message["msg"] == "Successfully submitted {0} volume task.".format(action)

    @pytest.mark.parametrize("input", [{"state": "present"}, {"state": "absent"}, {"command": "initialize"}])
    def test_configure_raid_operation(self, input, redfish_connection_mock_for_storage_volume, mocker):
        f_module = self.get_module_mock(params=input)
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.perform_volume_create_modify',
                     return_value={"msg": "Successfully submitted create volume task.",
                                   "task_uri": "JobService/Jobs",
                                   "task_id": "JID_123"})
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.perform_volume_deletion',
                     return_value={"msg": "Successfully submitted delete volume task.",
                                   "task_uri": "JobService/Jobs",
                                   "task_id": "JID_456"})
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.perform_volume_initialization',
                     return_value={"msg": "Successfully submitted initialize volume task.",
                                   "task_uri": "JobService/Jobs",
                                   "task_id": "JID_789"})
        message = self.module.configure_raid_operation(f_module, redfish_connection_mock_for_storage_volume)
        val = list(input.values())
        if val[0] == "present":
            assert message["msg"] == "Successfully submitted create volume task."
            assert message["task_id"] == "JID_123"
        if val[0] == "absent":
            assert message["msg"] == "Successfully submitted delete volume task."
            assert message["task_id"] == "JID_456"
        if val[0] == "initialize":
            assert message["msg"] == "Successfully submitted initialize volume task."
            assert message["task_id"] == "JID_789"

    def test_perform_volume_initialization_success_case_01(self, mocker, redfish_connection_mock_for_storage_volume,
                                                           storage_volume_base_uri):
        message = {"msg": "Successfully submitted initialize volume task.", "task_uri": "JobService/Jobs",
                   "task_id": "JID_789"}
        f_module = self.get_module_mock(params={"initialize_type": "Fast", "volume_id": "volume_id"})
        obj1 = mocker.patch(MODULE_PATH + 'redfish_storage_volume.check_initialization_progress', return_value=[])
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.perform_storage_volume_action', return_value=message)
        message = self.module.perform_volume_initialization(f_module, redfish_connection_mock_for_storage_volume)
        assert message["msg"] == "Successfully submitted initialize volume task."
        assert message["task_id"] == "JID_789"

    @pytest.mark.parametrize("operations", [[{"OperationName": "initialize", "PercentageComplete": 70}],
                                            [{"OperationName": "initialize"}]])
    def test_perform_volume_initialization_failure_case_01(self, mocker, operations,
                                                           redfish_connection_mock_for_storage_volume):
        f_module = self.get_module_mock(params={"volume_id": "volume_id"})
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.check_initialization_progress', return_value=operations)
        percentage_complete = operations[0].get("PercentageComplete")
        with pytest.raises(Exception) as exc:
            self.module.perform_volume_initialization(f_module, redfish_connection_mock_for_storage_volume)
        if percentage_complete:
            assert exc.value.args[0] == "Cannot perform the configuration operation because the configuration" \
                                        " job 'initialize' in progress is at '70' percentage."
        else:
            assert exc.value.args[0] == "Cannot perform the configuration operations because a" \
                                        " configuration job for the device already exists."

    def test_perform_volume_initialization_failure_case_02(self, mocker, redfish_connection_mock_for_storage_volume):
        f_module = self.get_module_mock(params={})
        with pytest.raises(Exception) as exc:
            self.module.perform_volume_initialization(f_module, redfish_connection_mock_for_storage_volume)
        assert exc.value.args[0] == "'volume_id' option is a required property for initializing a volume."

    def test_perform_volume_deletion_success_case_01(self, mocker, redfish_connection_mock_for_storage_volume,
                                                     redfish_response_mock, storage_volume_base_uri):
        redfish_response_mock.success = True
        f_module = self.get_module_mock(params={"volume_id": "volume_id"})
        message = {"msg": "Successfully submitted delete volume task.", "task_uri": "JobService/Jobs",
                   "task_id": "JID_456"}
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.check_volume_id_exists', return_value=redfish_response_mock)
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.perform_storage_volume_action',
                     return_value=redfish_response_mock)
        self.module.perform_volume_deletion(f_module, redfish_connection_mock_for_storage_volume)
        assert message["msg"] == "Successfully submitted delete volume task."
        assert message["task_id"] == "JID_456"

    def testperform_volume_deletion_failure_case_01(self, mocker, redfish_connection_mock_for_storage_volume):
        f_module = self.get_module_mock(params={})
        with pytest.raises(Exception) as exc:
            self.module.perform_volume_deletion(f_module, redfish_connection_mock_for_storage_volume)
        assert exc.value.args[0] == "'volume_id' option is a required property for deleting a volume."

    def test_perform_volume_create_modify_success_case_01(self, mocker, storage_volume_base_uri,
                                                          redfish_connection_mock_for_storage_volume):
        f_module = self.get_module_mock(params={"volume_id": "volume_id", "controller_id": "controller_id"})
        message = {"msg": "Successfully submitted create volume task.", "task_uri": "JobService/Jobs",
                   "task_id": "JID_123"}
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.check_controller_id_exists', return_value=True)
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.volume_payload', return_value={"payload": "value"})
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.perform_storage_volume_action', return_value=message)
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.check_mode_validation', return_value=None)
        message = self.module.perform_volume_create_modify(f_module, redfish_connection_mock_for_storage_volume)
        assert message["msg"] == "Successfully submitted create volume task."
        assert message["task_id"] == "JID_123"

    def test_perform_volume_create_modify_success_case_02(self, mocker, storage_volume_base_uri,
                                                          redfish_connection_mock_for_storage_volume,
                                                          redfish_response_mock):
        f_module = self.get_module_mock(params={"volume_id": "volume_id"})
        message = {"msg": "Successfully submitted modify volume task.", "task_uri": "JobService/Jobs",
                   "task_id": "JID_123"}
        redfish_response_mock.success = True
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.check_volume_id_exists', return_value=redfish_response_mock)
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.volume_payload', return_value={"payload": "value"})
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.perform_storage_volume_action', return_value=message)
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.check_mode_validation', return_value=None)
        message = self.module.perform_volume_create_modify(f_module, redfish_connection_mock_for_storage_volume)
        assert message["msg"] == "Successfully submitted modify volume task."
        assert message["task_id"] == "JID_123"

    def test_perform_volume_create_modify_failure_case_01(self, mocker, storage_volume_base_uri,
                                                          redfish_connection_mock_for_storage_volume,
                                                          redfish_response_mock):
        f_module = self.get_module_mock(params={"volume_id": "volume_id"})
        message = {"msg": "Successfully submitted modify volume task.", "task_uri": "JobService/Jobs",
                   "task_id": "JID_123"}
        redfish_response_mock.success = True
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.check_volume_id_exists', return_value=redfish_response_mock)
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.volume_payload', return_value={})
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.perform_storage_volume_action', return_value=message)
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.check_mode_validation', return_value=None)
        with pytest.raises(Exception) as exc:
            self.module.perform_volume_create_modify(f_module, redfish_connection_mock_for_storage_volume)
        assert exc.value.args[0] == "Input options are not provided for the modify volume task."

    def test_perform_storage_volume_action_success_case(self, mocker, redfish_response_mock,
                                                        redfish_connection_mock_for_storage_volume):
        redfish_response_mock.headers.update({"Location": "JobService/Jobs/JID_123"})
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.get_success_message', return_value="message")
        msg = self.module.perform_storage_volume_action("POST", "uri", redfish_connection_mock_for_storage_volume,
                                                        "create", payload={"payload": "value"})
        assert msg == "message"

    def test_perform_storage_volume_action_exception_case(self, redfish_response_mock,
                                                          redfish_connection_mock_for_storage_volume):
        redfish_response_mock.headers.update({"Location": "JobService/Jobs/JID_123"})
        redfish_connection_mock_for_storage_volume.invoke_request.side_effect = HTTPError('http://testhost.com', 400,
                                                                                          '', {}, None)
        with pytest.raises(HTTPError) as ex:
            self.module.perform_storage_volume_action("POST", "uri", redfish_connection_mock_for_storage_volume,
                                                      "create", payload={"payload": "value"})

    def test_check_initialization_progress_case_01(self, mocker, redfish_connection_mock_for_storage_volume,
                                                   redfish_response_mock):
        f_module = self.get_module_mock()
        redfish_response_mock.success = False
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.check_volume_id_exists', return_value=redfish_response_mock)
        opeartion_data = self.module.check_initialization_progress(f_module, redfish_connection_mock_for_storage_volume,
                                                                   "volume_id")
        assert opeartion_data == []

    def test_check_initialization_progress_case_02(self, mocker, redfish_connection_mock_for_storage_volume,
                                                   redfish_response_mock):
        f_module = self.get_module_mock()
        redfish_response_mock.success = True
        redfish_response_mock.json_data = {"Operations": "operation_value"}
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.check_volume_id_exists', return_value=redfish_response_mock)
        opeartion_data = self.module.check_initialization_progress(f_module, redfish_connection_mock_for_storage_volume,
                                                                   "volume_id")
        assert opeartion_data == "operation_value"

    def test_check_volume_id_exists(self, mocker, redfish_connection_mock_for_storage_volume, storage_volume_base_uri,
                                    redfish_response_mock):
        f_module = self.get_module_mock()
        redfish_response_mock.status_code = 200
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.check_specified_identifier_exists_in_the_system',
                     return_value=redfish_response_mock)
        resp = self.module.check_volume_id_exists(f_module, redfish_connection_mock_for_storage_volume, "volume_id")
        assert resp.status_code == 200

    def test_check_controller_id_exists_success_case_01(self, mocker, redfish_connection_mock_for_storage_volume,
                                                        storage_volume_base_uri,
                                                        redfish_response_mock):
        f_module = self.get_module_mock(params={"controller_id": "controller_id"})
        redfish_response_mock.success = True
        redfish_response_mock.json_data = {"Drives": "drive1"}
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.check_specified_identifier_exists_in_the_system',
                     return_value=redfish_response_mock)
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.check_physical_disk_exists',
                     return_value=True)
        output = self.module.check_controller_id_exists(f_module, redfish_connection_mock_for_storage_volume)
        assert output is True

    def test_check_controller_id_exists_failure_case_01(self, mocker, redfish_connection_mock_for_storage_volume,
                                                        storage_volume_base_uri,
                                                        redfish_response_mock):
        f_module = self.get_module_mock(params={"controller_id": "1234"})
        redfish_response_mock.success = False
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.check_specified_identifier_exists_in_the_system',
                     return_value=redfish_response_mock)
        mocker.patch(MODULE_PATH + 'redfish_storage_volume.check_physical_disk_exists',
                     return_value=True)
        with pytest.raises(Exception) as exc:
            self.module.check_controller_id_exists(f_module, redfish_connection_mock_for_storage_volume)
        assert exc.value.args[0] == "Failed to retrieve the details of the specified Controller Id 1234."

    def test_check_specified_identifier_exists_in_the_system_success_case(self,
                                                                          redfish_connection_mock_for_storage_volume,
                                                                          redfish_response_mock):
        f_module = self.get_module_mock(params={"controller_id": "1234"})
        redfish_response_mock.status_code = True
        redfish_response_mock.json_data = {"id": "data"}
        resp = self.module.check_specified_identifier_exists_in_the_system(f_module,
                                                                           redfish_connection_mock_for_storage_volume,
                                                                           "uri",
                                                                           "Specified Controller 123"
                                                                           " does not exist in the System.")
        assert resp.json_data == {"id": "data"}

    def test_check_specified_identifier_exists_in_the_system_exception_case_01(self,
                                                                               redfish_connection_mock_for_storage_volume,
                                                                               redfish_response_mock):
        f_module = self.get_module_mock(params={"controller_id": "1234"})
        redfish_connection_mock_for_storage_volume.invoke_request.side_effect = HTTPError('http://testhost.com',
                                                                                          404,
                                                                                          "Specified Controller 123 does"
                                                                                          " not exist in the System.",
                                                                                          {}, None)
        with pytest.raises(Exception) as exc:
            self.module.check_specified_identifier_exists_in_the_system(f_module,
                                                                        redfish_connection_mock_for_storage_volume,
                                                                        "uri",
                                                                        "Specified Controller 123"
                                                                        " does not exist in the System.")
        assert exc.value.args[0] == "Specified Controller 123 does not exist in the System."

    def test_check_specified_identifier_exists_in_the_system_exception_case_02(self,
                                                                               redfish_connection_mock_for_storage_volume,
                                                                               redfish_response_mock):
        f_module = self.get_module_mock(params={"controller_id": "1234"})
        msg = "http error"
        redfish_connection_mock_for_storage_volume.invoke_request.side_effect = HTTPError('http://testhost.com', 400,
                                                                                          msg, {}, None)
        with pytest.raises(Exception, match=msg) as exc:
            self.module.check_specified_identifier_exists_in_the_system(f_module,
                                                                        redfish_connection_mock_for_storage_volume,
                                                                        "uri",
                                                                        "Specified Controller 123 does not exist in the System.")

    def test_check_specified_identifier_exists_in_the_system_exception_case_03(self,
                                                                               redfish_connection_mock_for_storage_volume,
                                                                               redfish_response_mock):
        f_module = self.get_module_mock(params={"controller_id": "1234"})
        redfish_connection_mock_for_storage_volume.invoke_request.side_effect = URLError('test')
        with pytest.raises(URLError) as exc:
            self.module.check_specified_identifier_exists_in_the_system(f_module,
                                                                        redfish_connection_mock_for_storage_volume,
                                                                        "uri",
                                                                        "Specified Controller"
                                                                        " 123 does not exist in the System.")

    def test_check_physical_disk_exists_success_case_01(self):
        drive = [
            {
                "@odata.id": "/redfish/v1/Systems/System.Embedded.1/"
                             "Storage/Drives/Disk.Bay.0:Enclosure.Internal.0-0:RAID.Mezzanine.1C-1"
            }
        ]
        f_module = self.get_module_mock(params={"controller_id": "RAID.Mezzanine.1C-1",
                                                "drives": ["Disk.Bay.0:Enclosure.Internal.0-0:RAID.Mezzanine.1C-1"]})
        val = self.module.check_physical_disk_exists(f_module, drive)
        assert val is True

    def test_check_physical_disk_exists_success_case_02(self):
        drive = [
            {
                "@odata.id": "/redfish/v1/Systems/System.Embedded.1/Storage/"
                             "Drives/Disk.Bay.0:Enclosure.Internal.0-0:RAID.Mezzanine.1C-1"
            }
        ]
        f_module = self.get_module_mock(params={"controller_id": "RAID.Mezzanine.1C-1", "drives": []})
        val = self.module.check_physical_disk_exists(f_module, drive)
        assert val is True

    def test_check_physical_disk_exists_error_case_01(self):
        drive = [
            {
                "@odata.id": "/redfish/v1/Systems/System.Embedded.1/"
                             "Storage/Drives/Disk.Bay.0:Enclosure.Internal.0-0:RAID.Mezzanine.1C-1"
            }
        ]
        f_module = self.get_module_mock(params={"controller_id": "RAID.Mezzanine.1C-1", "drives": ["invalid_drive"]})
        with pytest.raises(Exception) as exc:
            self.module.check_physical_disk_exists(f_module, drive)
        assert exc.value.args[0] == "Following Drive(s) invalid_drive are not attached to the specified" \
                                    " Controller Id: RAID.Mezzanine.1C-1."

    def test_check_physical_disk_exists_error_case_02(self):
        drive = [
        ]
        f_module = self.get_module_mock(params={"controller_id": "RAID.Mezzanine.1C-1",
                                                "drives": ["Disk.Bay.0:Enclosure.Internal.0-0:RAID.Mezzanine.1C-1"]})
        with pytest.raises(Exception) as exc:
            self.module.check_physical_disk_exists(f_module, drive)
        assert exc.value.args[0] == "No Drive(s) are attached to the specified Controller Id: RAID.Mezzanine.1C-1."

    def test_volume_payload_case_01(self, storage_volume_base_uri):
        param = {
            "drives": ["Disk.Bay.0:Enclosure.Internal.0-0:RAID.Mezzanine.1C-1"],
            "capacity_bytes": 299439751168,
            "block_size_bytes": 512,
            "encryption_types": "NativeDriveEncryption",
            "encrypted": True,
            "volume_type": "NonRedundant",
            "name": "VD1",
            "optimum_io_size_bytes": 65536,
            "oem": {"Dell": {"DellVirtualDisk": {"BusProtocol": "SAS", "Cachecade": "NonCachecadeVD",
                                                 "DiskCachePolicy": "Disabled",
                                                 "LockStatus": "Unlocked",
                                                 "MediaType": "HardDiskDrive",
                                                 "ReadCachePolicy": "NoReadAhead",
                                                 "SpanDepth": 1,
                                                 "SpanLength": 2,
                                                 "WriteCachePolicy": "WriteThrough"}}}}
        f_module = self.get_module_mock(params=param)
        payload = self.module.volume_payload(f_module)
        assert payload["Drives"][0]["@odata.id"] == "/redfish/v1/Systems/System.Embedded.1/Storage/" \
                                                    "Drives/Disk.Bay.0:Enclosure.Internal.0-0:RAID.Mezzanine.1C-1"
        assert payload["VolumeType"] == "NonRedundant"
        assert payload["Name"] == "VD1"
        assert payload["BlockSizeBytes"] == 512
        assert payload["CapacityBytes"] == 299439751168
        assert payload["OptimumIOSizeBytes"] == 65536
        assert payload["Encrypted"] is True
        assert payload["EncryptionTypes"] == ["NativeDriveEncryption"]
        assert payload["Dell"]["DellVirtualDisk"]["ReadCachePolicy"] == "NoReadAhead"

    def test_volume_payload_case_02(self):
        param = {"block_size_bytes": 512,
                 "volume_type": "NonRedundant",
                 "name": "VD1",
                 "optimum_io_size_bytes": 65536}
        f_module = self.get_module_mock(params=param)
        payload = self.module.volume_payload(f_module)
        assert payload["VolumeType"] == "NonRedundant"
        assert payload["Name"] == "VD1"
        assert payload["BlockSizeBytes"] == 512
        assert payload["OptimumIOSizeBytes"] == 65536

    def test_volume_payload_case_03(self, storage_volume_base_uri):
        """Testing encrypted value in case value is passed false"""
        param = {
            "drives": ["Disk.Bay.0:Enclosure.Internal.0-0:RAID.Mezzanine.1C-1"],
            "capacity_bytes": 299439751168,
            "block_size_bytes": 512,
            "encryption_types": "NativeDriveEncryption",
            "encrypted": False,
            "volume_type": "NonRedundant",
            "name": "VD1",
            "optimum_io_size_bytes": 65536,
            "oem": {"Dell": {"DellVirtualDisk": {"BusProtocol": "SAS", "Cachecade": "NonCachecadeVD",
                                                 "DiskCachePolicy": "Disabled",
                                                 "LockStatus": "Unlocked",
                                                 "MediaType": "HardDiskDrive",
                                                 "ReadCachePolicy": "NoReadAhead",
                                                 "SpanDepth": 1,
                                                 "SpanLength": 2,
                                                 "WriteCachePolicy": "WriteThrough"}}}}
        f_module = self.get_module_mock(params=param)
        payload = self.module.volume_payload(f_module)
        assert payload["Drives"][0]["@odata.id"] == "/redfish/v1/Systems/System.Embedded.1/" \
                                                    "Storage/Drives/Disk.Bay.0:Enclosure.Internal.0-0:RAID.Mezzanine.1C-1"
        assert payload["VolumeType"] == "NonRedundant"
        assert payload["Name"] == "VD1"
        assert payload["BlockSizeBytes"] == 512
        assert payload["CapacityBytes"] == 299439751168
        assert payload["OptimumIOSizeBytes"] == 65536
        assert payload["Encrypted"] is False
        assert payload["EncryptionTypes"] == ["NativeDriveEncryption"]
        assert payload["Dell"]["DellVirtualDisk"]["ReadCachePolicy"] == "NoReadAhead"

    def test_fetch_storage_resource_success_case_01(self, redfish_connection_mock_for_storage_volume,
                                                    redfish_response_mock):
        f_module = self.get_module_mock()
        redfish_response_mock.json_data = {
            "@odata.id": "/redfish/v1/Systems",
            "Members": [
                {
                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1"
                }
            ],
            "Storage": {
                "@odata.id": "/redfish/v1/Systems/System.Embedded.1/Storage"
            },
        }
        redfish_connection_mock_for_storage_volume.root_uri = "/redfish/v1/"
        self.module.fetch_storage_resource(f_module, redfish_connection_mock_for_storage_volume)
        assert self.module.storage_collection_map["storage_base_uri"] == "/redfish/v1/Systems/System.Embedded.1/Storage"

    def test_fetch_storage_resource_error_case_01(self, redfish_connection_mock_for_storage_volume,
                                                  redfish_response_mock):
        f_module = self.get_module_mock()
        redfish_response_mock.json_data = {
            "@odata.id": "/redfish/v1/Systems",
            "Members": [
                {
                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1"
                }
            ],
        }
        redfish_connection_mock_for_storage_volume.root_uri = "/redfish/v1/"
        with pytest.raises(Exception) as exc:
            self.module.fetch_storage_resource(f_module, redfish_connection_mock_for_storage_volume)
        assert exc.value.args[0] == "Target out-of-band controller does not support storage feature using Redfish API."

    def test_fetch_storage_resource_error_case_02(self, redfish_connection_mock_for_storage_volume,
                                                  redfish_response_mock):
        f_module = self.get_module_mock()
        redfish_response_mock.json_data = {
            "@odata.id": "/redfish/v1/Systems",
            "Members": [
            ],
        }
        redfish_connection_mock_for_storage_volume.root_uri = "/redfish/v1/"
        with pytest.raises(Exception) as exc:
            self.module.fetch_storage_resource(f_module, redfish_connection_mock_for_storage_volume)
        assert exc.value.args[0] == "Target out-of-band controller does not support storage feature using Redfish API."

    def test_fetch_storage_resource_error_case_03(self, redfish_connection_mock_for_storage_volume,
                                                  redfish_response_mock):
        f_module = self.get_module_mock()
        msg = "Target out-of-band controller does not support storage feature using Redfish API."
        redfish_connection_mock_for_storage_volume.root_uri = "/redfish/v1/"
        redfish_connection_mock_for_storage_volume.invoke_request.side_effect = HTTPError('http://testhost.com', 404,
                                                                                          json.dumps(msg), {}, None)
        with pytest.raises(Exception) as exc:
            self.module.fetch_storage_resource(f_module, redfish_connection_mock_for_storage_volume)

    def test_fetch_storage_resource_error_case_04(self, redfish_connection_mock_for_storage_volume,
                                                  redfish_response_mock):
        f_module = self.get_module_mock()
        msg = "http error"
        redfish_connection_mock_for_storage_volume.root_uri = "/redfish/v1/"
        redfish_connection_mock_for_storage_volume.invoke_request.side_effect = HTTPError('http://testhost.com', 400,
                                                                                          msg, {}, None)
        with pytest.raises(Exception, match=msg) as exc:
            self.module.fetch_storage_resource(f_module, redfish_connection_mock_for_storage_volume)

    def test_fetch_storage_resource_error_case_05(self, redfish_connection_mock_for_storage_volume,
                                                  redfish_response_mock):
        f_module = self.get_module_mock()
        msg = "connection error"
        redfish_connection_mock_for_storage_volume.root_uri = "/redfish/v1/"
        redfish_connection_mock_for_storage_volume.invoke_request.side_effect = URLError(msg)
        with pytest.raises(Exception, match=msg) as exc:
            self.module.fetch_storage_resource(f_module, redfish_connection_mock_for_storage_volume)

    def test_check_mode_validation(self, redfish_connection_mock_for_storage_volume,
                                   redfish_response_mock, storage_volume_base_uri):
        param = {"drives": ["Disk.Bay.0:Enclosure.Internal.0-0:RAID.Integrated.1-1"],
                 "capacity_bytes": 214748364800, "block_size_bytes": 512, "encryption_types": "NativeDriveEncryption",
                 "encrypted": False, "volume_type": "NonRedundant", "optimum_io_size_bytes": 65536}
        f_module = self.get_module_mock(params=param)
        f_module.check_mode = True
        with pytest.raises(Exception) as exc:
            self.module.check_mode_validation(
                f_module, redfish_connection_mock_for_storage_volume, "create",
                "/redfish/v1/Systems/System.Embedded.1/Storage/RAID.Integrated.1-1/Volumes/")
        assert exc.value.args[0] == "Changes found to be applied."
        redfish_response_mock.json_data = {"Members@odata.count": 0}
        with pytest.raises(Exception) as exc:
            self.module.check_mode_validation(
                f_module, redfish_connection_mock_for_storage_volume, "create",
                "/redfish/v1/Systems/System.Embedded.1/Storage/RAID.Integrated.1-1/Volumes/")
        assert exc.value.args[0] == "Changes found to be applied."
        redfish_response_mock.json_data = {
            "Members@odata.count": 1, "Id": "Disk.Virtual.0:RAID.Integrated.1-1",
            "Members": [{"@odata.id": "/redfish/v1/Systems/System.Embedded.1/Storage/"
                                      "RAID.Integrated.1-1/Volumes/Disk.Virtual.0:RAID.Integrated.1-1"}],
            "Name": "VD0", "BlockSizeBytes": 512, "CapacityBytes": 214748364800, "Encrypted": False,
            "EncryptionTypes": ["NativeDriveEncryption"], "OptimumIOSizeBytes": 65536, "VolumeType": "NonRedundant",
            "Links": {"Drives": [{"@odata.id": "Drives/Disk.Bay.0:Enclosure.Internal.0-0:RAID.Integrated.1-1"}]}}
        param.update({"name": "VD0"})
        f_module = self.get_module_mock(params=param)
        f_module.check_mode = True
        with pytest.raises(Exception) as exc:
            self.module.check_mode_validation(
                f_module, redfish_connection_mock_for_storage_volume, "create",
                "/redfish/v1/Systems/System.Embedded.1/Storage/RAID.Integrated.1-1/Volumes/")
        assert exc.value.args[0] == "No changes found to be applied."
