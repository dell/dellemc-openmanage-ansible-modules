# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.9.0
# Copyright (C) 2026 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

import json
import pytest
from io import StringIO
from ansible.module_utils._text import to_text
from urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_storage_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_storage_info.'
CONTROLLER_ID_REQUIRED_MSG = "controller_id is required when resource_type is '{resource_type}'."
SUCCESS_MSG = "Successfully fetched the storage information."


class TestStorageInfo(FakeAnsibleModule):
    module = idrac_storage_info

    @pytest.fixture
    def idrac_storage_info_mock(self, mocker):
        idrac_obj = mocker.MagicMock()
        idrac_obj.get_server_generation = (17, "7.10.90.00", "iDRAC 9")
        return idrac_obj

    @pytest.fixture
    def idrac_connection_storage_info_mock(self, mocker, idrac_storage_info_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                        return_value=idrac_storage_info_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_storage_info_mock
        mocker.patch(MODULE_PATH + 'StorageInfo.fetch_resources',
                     return_value={"resource_count": 0, "resources": []})
        return idrac_conn_mock

    def test_main_controller_resource_type_success(self, idrac_connection_storage_info_mock, idrac_default_args):
        idrac_default_args.update({"resource_type": "controller"})
        result = self._run_module(idrac_default_args)
        assert result["msg"] == SUCCESS_MSG
        assert result["storage_info"] == {"resource_count": 0, "resources": []}

    def test_main_physical_disk_missing_controller_id(self, idrac_connection_storage_info_mock, idrac_default_args):
        idrac_default_args.update({"resource_type": "physical_disk"})
        result = self._run_module(idrac_default_args)
        assert result["msg"] == CONTROLLER_ID_REQUIRED_MSG.format(resource_type="physical_disk")
        assert result["failed"] is True

    def test_main_virtual_disk_missing_controller_id(self, idrac_connection_storage_info_mock, idrac_default_args):
        idrac_default_args.update({"resource_type": "virtual_disk"})
        result = self._run_module(idrac_default_args)
        assert result["msg"] == CONTROLLER_ID_REQUIRED_MSG.format(resource_type="virtual_disk")
        assert result["failed"] is True

    def test_main_virtual_disk_with_controller_id_success(self, idrac_connection_storage_info_mock, idrac_default_args):
        idrac_default_args.update({"resource_type": "virtual_disk", "controller_id": "RAID.Slot.1-1"})
        result = self._run_module(idrac_default_args)
        assert result["msg"] == SUCCESS_MSG

    def test_main_http_error_case(self, idrac_connection_storage_info_mock, idrac_default_args, mocker):
        json_str = to_text(json.dumps({"data": "out"}))
        idrac_default_args.update({"resource_type": "controller"})
        mocker.patch(MODULE_PATH + 'StorageInfo.validate_params',
                     side_effect=HTTPError('https://testhost.com', 400, 'http error message',
                                           {"accept-type": "application/json"}, StringIO(json_str)))
        result = self._run_module(idrac_default_args)
        assert result['failed'] is True
        assert 'error_info' in result

    def test_main_url_error_case(self, idrac_connection_storage_info_mock, idrac_default_args, mocker):
        idrac_default_args.update({"resource_type": "controller"})
        mocker.patch(MODULE_PATH + 'StorageInfo.validate_params',
                     side_effect=URLError('url error message'))
        result = self._run_module(idrac_default_args)
        assert result.get('unreachable') is True

    def test_main_connection_error_case(self, idrac_connection_storage_info_mock, idrac_default_args, mocker):
        idrac_default_args.update({"resource_type": "controller"})
        mocker.patch(MODULE_PATH + 'StorageInfo.validate_params',
                     side_effect=ConnectionError('connection error message'))
        result = self._run_module(idrac_default_args)
        assert result['failed'] is True

    def test_main_authentication_failure_401(self, idrac_connection_storage_info_mock, idrac_default_args, mocker):
        json_str = to_text(json.dumps({"data": "out"}))
        idrac_default_args.update({"resource_type": "controller"})
        mocker.patch(MODULE_PATH + 'StorageInfo.validate_params',
                     side_effect=HTTPError('https://testhost.com', 401, 'Unauthorized',
                                           {"accept-type": "application/json"}, StringIO(json_str)))
        result = self._run_module(idrac_default_args)
        assert result['failed'] is True
        assert 'error_info' in result

    def test_main_authentication_failure_403(self, idrac_connection_storage_info_mock, idrac_default_args, mocker):
        json_str = to_text(json.dumps({"data": "out"}))
        idrac_default_args.update({"resource_type": "controller"})
        mocker.patch(MODULE_PATH + 'StorageInfo.validate_params',
                     side_effect=HTTPError('https://testhost.com', 403, 'Forbidden',
                                           {"accept-type": "application/json"}, StringIO(json_str)))
        result = self._run_module(idrac_default_args)
        assert result['failed'] is True
        assert 'error_info' in result

    def test_main_network_timeout_case(self, idrac_connection_storage_info_mock, idrac_default_args, mocker):
        idrac_default_args.update({"resource_type": "controller"})
        mocker.patch(MODULE_PATH + 'StorageInfo.validate_params',
                     side_effect=URLError('timed out'))
        result = self._run_module(idrac_default_args)
        assert result.get('unreachable') is True

    def test_firmware_validation_idrac9_supported(self, idrac_connection_storage_info_mock, idrac_storage_info_mock,
                                                   idrac_default_args):
        idrac_storage_info_mock.get_server_generation = (16, "7.10.90.00", "iDRAC 9")
        idrac_default_args.update({"resource_type": "controller"})
        result = self._run_module(idrac_default_args)
        assert result["msg"] == SUCCESS_MSG

    def test_firmware_validation_idrac9_unsupported(self, idrac_connection_storage_info_mock, idrac_storage_info_mock,
                                                     idrac_default_args):
        idrac_storage_info_mock.get_server_generation = (16, "7.10.80.00", "iDRAC 9")
        idrac_default_args.update({"resource_type": "controller"})
        result = self._run_module(idrac_default_args)
        assert result["failed"] is True
        assert "does not meet the minimum required version" in result["msg"]

    def test_firmware_validation_idrac10_supported(self, idrac_connection_storage_info_mock, idrac_storage_info_mock,
                                                    idrac_default_args):
        idrac_storage_info_mock.get_server_generation = (17, "1.20.50.50", "iDRAC 10")
        idrac_default_args.update({"resource_type": "controller"})
        result = self._run_module(idrac_default_args)
        assert result["msg"] == SUCCESS_MSG

    def test_firmware_validation_idrac10_unsupported(self, idrac_connection_storage_info_mock, idrac_storage_info_mock,
                                                      idrac_default_args):
        idrac_storage_info_mock.get_server_generation = (17, "1.20.40.00", "iDRAC 10")
        idrac_default_args.update({"resource_type": "controller"})
        result = self._run_module(idrac_default_args)
        assert result["failed"] is True
        assert "does not meet the minimum required version" in result["msg"]

    def test_firmware_validation_unsupported_generation(self, idrac_connection_storage_info_mock,
                                                          idrac_storage_info_mock, idrac_default_args):
        idrac_storage_info_mock.get_server_generation = (14, "2.75.75.75", "iDRAC 8")
        idrac_default_args.update({"resource_type": "controller"})
        result = self._run_module(idrac_default_args)
        assert result["failed"] is True
        assert result["msg"] == "This module is not supported on iDRAC 8."

    @pytest.mark.parametrize("current,minimum,expected", [
        ("7.10.90.00", "7.10.90.00", True),
        ("7.10.90.01", "7.10.90.00", True),
        ("7.10.89.99", "7.10.90.00", False),
        ("1.20.50.50", "1.20.50.50", True),
        ("1.20.50.49", "1.20.50.50", False),
        ("8.0.0.0", "7.10.90.00", True),
    ])
    def test_version_meets_minimum(self, current, minimum, expected):
        assert idrac_storage_info.StorageInfo._version_meets_minimum(current, minimum) is expected

    def test_compute_capacity_controller_type(self):
        total, available = idrac_storage_info.StorageInfo._compute_capacity("controller", [{"Id": "RAID.Slot.1-1"}])
        assert total is None
        assert available is None

    def test_compute_capacity_physical_disk_type(self):
        resources = [
            {"CapacityBytes": 1000, "FreeSizeInBytes": 400},
            {"CapacityBytes": 2000, "FreeSizeInBytes": None},
        ]
        total, available = idrac_storage_info.StorageInfo._compute_capacity("physical_disk", resources)
        assert total == 3000
        assert available == 400

    def test_compute_capacity_virtual_disk_type(self):
        resources = [{"CapacityBytes": 1500}, {"CapacityBytes": 2500}]
        total, available = idrac_storage_info.StorageInfo._compute_capacity("virtual_disk", resources)
        assert total == 4000
        assert available is None


class TestRetryOnTransientError:
    def test_succeeds_first_try(self, mocker):
        mocker.patch('time.sleep')
        func = mocker.MagicMock(return_value="ok")
        wrapped = idrac_storage_info.retry_on_transient_error(func)
        assert wrapped() == "ok"
        assert func.call_count == 1

    def test_retries_on_transient_http_503_then_succeeds(self, mocker):
        mocker.patch('time.sleep')
        json_str = to_text(json.dumps({"data": "out"}))
        err = HTTPError('https://testhost.com', 503, 'Service Unavailable',
                        {"accept-type": "application/json"}, StringIO(json_str))
        func = mocker.MagicMock(side_effect=[err, "ok"])
        wrapped = idrac_storage_info.retry_on_transient_error(func)
        assert wrapped() == "ok"
        assert func.call_count == 2

    def test_raises_immediately_on_non_transient_http_error(self, mocker):
        mocker.patch('time.sleep')
        json_str = to_text(json.dumps({"data": "out"}))
        err = HTTPError('https://testhost.com', 400, 'Bad Request',
                        {"accept-type": "application/json"}, StringIO(json_str))
        func = mocker.MagicMock(side_effect=err)
        wrapped = idrac_storage_info.retry_on_transient_error(func)
        with pytest.raises(HTTPError):
            wrapped()
        assert func.call_count == 1

    def test_exhausts_retries_and_raises(self, mocker):
        mocker.patch('time.sleep')
        func = mocker.MagicMock(side_effect=URLError('timed out'))
        wrapped = idrac_storage_info.retry_on_transient_error(func)
        with pytest.raises(URLError):
            wrapped()
        assert func.call_count == idrac_storage_info.MAX_RETRIES


class TestStorageInfoControllerQuery(FakeAnsibleModule):
    module = idrac_storage_info
    SYSTEMS_URI = "/redfish/v1/Systems"
    SYSTEM_URI = "/redfish/v1/Systems/System.Embedded.1"
    STORAGE_URI = "/redfish/v1/Systems/System.Embedded.1/Storage"

    def _idrac_mock(self, mocker, controller_members):
        idrac_obj = mocker.MagicMock()

        def invoke_request_side_effect(*args, **kwargs):
            uri = kwargs.get("uri") or kwargs.get("path") or (args[0] if args else None)
            resp = mocker.MagicMock()
            if uri == self.SYSTEMS_URI:
                resp.json_data = {"Members": [{"@odata.id": self.SYSTEM_URI}]}
            elif uri == self.SYSTEM_URI:
                resp.json_data = {"Storage": {"@odata.id": self.STORAGE_URI}}
            elif uri == self.STORAGE_URI + "?$expand=*($levels=1)":
                resp.json_data = {"Members": controller_members}
            else:
                resp.json_data = {}
            return resp

        idrac_obj.invoke_request.side_effect = invoke_request_side_effect
        return idrac_obj

    def test_get_controllers_maps_redfish_and_oem_fields(self, mocker):
        controller_members = [
            {
                "Id": "RAID.Slot.1-1",
                "Name": "PERC H755",
                "Status": {"Health": "OK", "State": "Enabled"},
                "StorageControllers": [{"Model": "PERC H755", "FirmwareVersion": "25.5.9.0001"}],
                "Oem": {"Dell": {"DellController": {
                    "PatrolReadRatePercent": 30,
                    "RebuildRatePercent": 30,
                    "CopybackMode": "On",
                    "EncryptionCapability": "LocalKeyManagement",
                    "EncryptionMode": "None",
                }}},
            },
            {"Id": "CPU.1", "Name": "CPU Storage", "StorageControllers": []},
        ]
        idrac_obj = self._idrac_mock(mocker, controller_members)
        module = mocker.MagicMock()
        storage_info_obj = idrac_storage_info.StorageInfo(idrac_obj, module)

        controllers = storage_info_obj.get_controllers()

        assert len(controllers) == 1
        assert controllers[0]["Id"] == "RAID.Slot.1-1"
        assert controllers[0]["Model"] == "PERC H755"
        assert controllers[0]["FirmwareVersion"] == "25.5.9.0001"
        assert controllers[0]["Status"] == {"Health": "OK", "State": "Enabled"}
        assert controllers[0]["PatrolReadRatePercent"] == 30
        assert controllers[0]["RebuildRatePercent"] == 30
        assert controllers[0]["CopybackMode"] == "On"
        assert controllers[0]["EncryptionCapability"] == "LocalKeyManagement"
        assert controllers[0]["EncryptionMode"] == "None"

    def test_fetch_resources_controller_type(self, mocker):
        controller_members = [
            {"Id": "RAID.Slot.1-1", "Name": "PERC H755", "Status": {"Health": "OK"},
             "StorageControllers": [{"Model": "PERC H755", "FirmwareVersion": "25.5.9.0001"}], "Oem": {}},
        ]
        idrac_obj = self._idrac_mock(mocker, controller_members)
        idrac_obj.get_server_generation = (17, "7.10.90.00", "iDRAC 9")
        module = mocker.MagicMock()
        module.params = {"resource_type": "controller"}
        storage_info_obj = idrac_storage_info.StorageInfo(idrac_obj, module)

        result = storage_info_obj.fetch_resources()

        assert result["resource_count"] == 1
        assert result["resources"][0]["Id"] == "RAID.Slot.1-1"
        assert result["idrac_generation"] == 17
        assert result["idrac_firmware_version"] == "7.10.90.00"
        assert result["idrac_model"] == "iDRAC 9"
        assert result["total_capacity"] is None
        assert result["available_capacity"] is None



class TestStorageInfoPhysicalDiskQuery(FakeAnsibleModule):
    module = idrac_storage_info
    SYSTEMS_URI = "/redfish/v1/Systems"
    SYSTEM_URI = "/redfish/v1/Systems/System.Embedded.1"
    STORAGE_URI = "/redfish/v1/Systems/System.Embedded.1/Storage"
    DRIVE_URI = "/redfish/v1/Systems/System.Embedded.1/Storage/RAID.Slot.1-1/Drives/Disk.Bay.0"

    def _idrac_mock(self, mocker, controller_members, drive_data_by_uri):
        idrac_obj = mocker.MagicMock()

        def invoke_request_side_effect(*args, **kwargs):
            uri = kwargs.get("uri") or kwargs.get("path") or (args[0] if args else None)
            resp = mocker.MagicMock()
            if uri == self.SYSTEMS_URI:
                resp.json_data = {"Members": [{"@odata.id": self.SYSTEM_URI}]}
            elif uri == self.SYSTEM_URI:
                resp.json_data = {"Storage": {"@odata.id": self.STORAGE_URI}}
            elif uri == self.STORAGE_URI + "?$expand=*($levels=1)":
                resp.json_data = {"Members": controller_members}
            elif uri in drive_data_by_uri:
                resp.json_data = drive_data_by_uri[uri]
            else:
                resp.json_data = {}
            return resp

        idrac_obj.invoke_request.side_effect = invoke_request_side_effect
        return idrac_obj

    def test_get_physical_disks_maps_redfish_and_oem_fields(self, mocker):
        controller_members = [
            {"Id": "RAID.Slot.1-1", "Drives": [{"@odata.id": self.DRIVE_URI}]},
        ]
        drive_data_by_uri = {
            self.DRIVE_URI: {
                "Id": "Disk.Bay.0",
                "Name": "Solid State Disk 0",
                "CapacityBytes": 400088457216,
                "MediaType": "SSD",
                "Protocol": "SAS",
                "Status": {"Health": "OK"},
                "PhysicalLocation": {"PartLocation": {"LocationOrdinalValue": 0}},
                "Oem": {"Dell": {"DellPhysicalDisk": {
                    "RaidStatus": "Ready",
                    "HotSpareStatus": "No",
                    "UsedSizeBytes": 0,
                    "FreeSizeInBytes": 400088457216,
                    "EncryptionCapable": "Yes",
                    "PredictiveFailureState": "Smart Alert Absent",
                }}},
            }
        }
        idrac_obj = self._idrac_mock(mocker, controller_members, drive_data_by_uri)
        module = mocker.MagicMock()
        storage_info_obj = idrac_storage_info.StorageInfo(idrac_obj, module)

        disks = storage_info_obj.get_physical_disks("RAID.Slot.1-1")

        assert len(disks) == 1
        assert disks[0]["Id"] == "Disk.Bay.0"
        assert disks[0]["MediaType"] == "SSD"
        assert disks[0]["Protocol"] == "SAS"
        assert disks[0]["RaidStatus"] == "Ready"
        assert disks[0]["HotSpareStatus"] == "No"
        assert disks[0]["UsedSizeBytes"] == 0
        assert disks[0]["FreeSizeInBytes"] == 400088457216
        assert disks[0]["EncryptionCapable"] == "Yes"
        assert disks[0]["PredictiveFailureState"] == "Smart Alert Absent"

    def test_get_physical_disks_controller_not_found(self, mocker):
        idrac_obj = self._idrac_mock(mocker, [{"Id": "RAID.Slot.1-2", "Drives": []}], {})
        idrac_obj.get_server_generation = (17, "7.10.90.00", "iDRAC 9")
        conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI', return_value=idrac_obj)
        conn_mock.return_value.__enter__.return_value = idrac_obj

        result = self._run_module({
            "idrac_ip": "192.168.0.1", "idrac_user": "username", "idrac_password": "password",
            "idrac_port": 443, "resource_type": "physical_disk", "controller_id": "RAID.Slot.1-1",
        })

        assert result["failed"] is True
        assert result["msg"] == "Specified controller 'RAID.Slot.1-1' does not exist."

    def test_fetch_resources_physical_disk_type(self, mocker):
        controller_members = [{"Id": "RAID.Slot.1-1", "Drives": [{"@odata.id": self.DRIVE_URI}]}]
        drive_data_by_uri = {self.DRIVE_URI: {"Id": "Disk.Bay.0", "CapacityBytes": 1000, "Oem": {
            "Dell": {"DellPhysicalDisk": {"FreeSizeInBytes": 500}}}}}
        idrac_obj = self._idrac_mock(mocker, controller_members, drive_data_by_uri)
        idrac_obj.get_server_generation = (17, "7.10.90.00", "iDRAC 9")
        module = mocker.MagicMock()
        module.params = {"resource_type": "physical_disk", "controller_id": "RAID.Slot.1-1"}
        storage_info_obj = idrac_storage_info.StorageInfo(idrac_obj, module)

        result = storage_info_obj.fetch_resources()

        assert result["resource_count"] == 1
        assert result["resources"][0]["Id"] == "Disk.Bay.0"
        assert result["total_capacity"] == 1000
        assert result["available_capacity"] == 500


class TestStorageInfoVirtualDiskQuery(FakeAnsibleModule):
    module = idrac_storage_info
    SYSTEMS_URI = "/redfish/v1/Systems"
    SYSTEM_URI = "/redfish/v1/Systems/System.Embedded.1"
    STORAGE_URI = "/redfish/v1/Systems/System.Embedded.1/Storage"
    VOLUMES_URI = "/redfish/v1/Systems/System.Embedded.1/Storage/RAID.Slot.1-1/Volumes"
    VOLUME_URI = VOLUMES_URI + "/Disk.Virtual.0:RAID.Slot.1-1"

    def _idrac_mock(self, mocker, controller_members, volumes_members, volume_data_by_uri):
        idrac_obj = mocker.MagicMock()

        def invoke_request_side_effect(*args, **kwargs):
            uri = kwargs.get("uri") or kwargs.get("path") or (args[0] if args else None)
            resp = mocker.MagicMock()
            if uri == self.SYSTEMS_URI:
                resp.json_data = {"Members": [{"@odata.id": self.SYSTEM_URI}]}
            elif uri == self.SYSTEM_URI:
                resp.json_data = {"Storage": {"@odata.id": self.STORAGE_URI}}
            elif uri == self.STORAGE_URI + "?$expand=*($levels=1)":
                resp.json_data = {"Members": controller_members}
            elif uri == self.VOLUMES_URI:
                resp.json_data = {"Members": volumes_members}
            elif uri in volume_data_by_uri:
                resp.json_data = volume_data_by_uri[uri]
            else:
                resp.json_data = {}
            return resp

        idrac_obj.invoke_request.side_effect = invoke_request_side_effect
        return idrac_obj

    def test_get_virtual_disks_maps_redfish_and_oem_fields(self, mocker):
        controller_members = [
            {"Id": "RAID.Slot.1-1", "Volumes": {"@odata.id": self.VOLUMES_URI}},
        ]
        volumes_members = [{"@odata.id": self.VOLUME_URI}]
        volume_data_by_uri = {
            self.VOLUME_URI: {
                "Id": "Disk.Virtual.0:RAID.Slot.1-1",
                "Name": "Virtual Disk 0",
                "RAIDType": "RAID1",
                "CapacityBytes": 400088457216,
                "Status": {"Health": "OK"},
                "Oem": {"Dell": {"DellVirtualDisk": {
                    "RaidStatus": "Online",
                    "ReadCachePolicy": "ReadAhead",
                    "WriteCachePolicy": "WriteBack",
                    "DiskCachePolicy": "Enabled",
                }}},
            }
        }
        idrac_obj = self._idrac_mock(mocker, controller_members, volumes_members, volume_data_by_uri)
        module = mocker.MagicMock()
        storage_info_obj = idrac_storage_info.StorageInfo(idrac_obj, module)

        virtual_disks = storage_info_obj.get_virtual_disks("RAID.Slot.1-1")

        assert len(virtual_disks) == 1
        assert virtual_disks[0]["Id"] == "Disk.Virtual.0:RAID.Slot.1-1"
        assert virtual_disks[0]["RAIDType"] == "RAID1"
        assert virtual_disks[0]["RaidStatus"] == "Online"
        assert virtual_disks[0]["ReadCachePolicy"] == "ReadAhead"
        assert virtual_disks[0]["WriteCachePolicy"] == "WriteBack"
        assert virtual_disks[0]["DiskCachePolicy"] == "Enabled"

    def test_get_virtual_disks_no_volumes(self, mocker):
        controller_members = [{"Id": "RAID.Slot.1-1", "Volumes": {"@odata.id": self.VOLUMES_URI}}]
        idrac_obj = self._idrac_mock(mocker, controller_members, [], {})
        module = mocker.MagicMock()
        storage_info_obj = idrac_storage_info.StorageInfo(idrac_obj, module)

        virtual_disks = storage_info_obj.get_virtual_disks("RAID.Slot.1-1")

        assert virtual_disks == []

    def test_get_virtual_disks_controller_not_found(self, mocker):
        idrac_obj = self._idrac_mock(mocker, [{"Id": "RAID.Slot.1-2", "Volumes": {}}], [], {})
        idrac_obj.get_server_generation = (17, "7.10.90.00", "iDRAC 9")
        conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI', return_value=idrac_obj)
        conn_mock.return_value.__enter__.return_value = idrac_obj

        result = self._run_module({
            "idrac_ip": "192.168.0.1", "idrac_user": "username", "idrac_password": "password",
            "idrac_port": 443, "resource_type": "virtual_disk", "controller_id": "RAID.Slot.1-1",
        })

        assert result["failed"] is True
        assert result["msg"] == "Specified controller 'RAID.Slot.1-1' does not exist."

    def test_fetch_resources_virtual_disk_type(self, mocker):
        controller_members = [{"Id": "RAID.Slot.1-1", "Volumes": {"@odata.id": self.VOLUMES_URI}}]
        volumes_members = [{"@odata.id": self.VOLUME_URI}]
        volume_data_by_uri = {self.VOLUME_URI: {"Id": "Disk.Virtual.0:RAID.Slot.1-1",
                                                 "CapacityBytes": 2000, "Oem": {}}}
        idrac_obj = self._idrac_mock(mocker, controller_members, volumes_members, volume_data_by_uri)
        idrac_obj.get_server_generation = (17, "7.10.90.00", "iDRAC 9")
        module = mocker.MagicMock()
        module.params = {"resource_type": "virtual_disk", "controller_id": "RAID.Slot.1-1"}
        storage_info_obj = idrac_storage_info.StorageInfo(idrac_obj, module)

        result = storage_info_obj.fetch_resources()

        assert result["resource_count"] == 1
        assert result["resources"][0]["Id"] == "Disk.Virtual.0:RAID.Slot.1-1"
        assert result["total_capacity"] == 2000
        assert result["available_capacity"] is None


@pytest.fixture
def idrac_default_args():
    return {
        "idrac_ip": "192.168.0.1",
        "idrac_user": "username",
        "idrac_password": "password",
        "idrac_port": 443,
    }
