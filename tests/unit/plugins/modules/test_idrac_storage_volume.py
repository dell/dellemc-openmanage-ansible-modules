# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

import json
import pytest
from io import StringIO
from ansible.module_utils._text import to_text
from urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_storage_volume
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from unittest.mock import MagicMock
from copy import deepcopy

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_storage_volume.'
MODULE_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.'

SYSTEMS_URI = "/redfish/v1/Systems"
iDRAC_JOB_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/{job_id}"
CONTROLLER_NOT_EXIST_ERROR = "Specified Controller {controller_id} does not exist in the System."
CONTROLLER_NOT_DEFINED = "Controller ID is required."
SUCCESSFUL_OPERATION_MSG = "Successfully completed the {operation} storage volume operation."
DRIVES_NOT_EXIST_ERROR = "No Drive(s) are attached to the specified Controller Id: {controller_id}."
DRIVES_NOT_MATCHED = "Following Drive(s) {specified_drives} are not attached to the specified Controller Id: {controller_id}."
NEGATIVE_OR_ZERO_MSG = "The value for the `{parameter}` parameter cannot be negative or zero."
NEGATIVE_MSG = "The value for the `{parameter}` parameter cannot be negative."
INVALID_VALUE_MSG = "The value for the `{parameter}` parameter is invalid."
ID_AND_LOCATION_BOTH_DEFINED = "Either id or location is allowed."
ID_AND_LOCATION_BOTH_NOT_DEFINED = "Either id or location should be specified."
DRIVES_NOT_DEFINED = "Drives must be defined for volume creation."
NOT_ENOUGH_DRIVES = "Number of sufficient disks not found in Controller '{controller_id}'!"
WAIT_TIMEOUT_MSG = "The job is not complete after {0} seconds."
TIME_TO_WAIT_MSG = "Time to wait value is invalid. Minimum value is 300 and Maximum is 3600 seconds."
JOB_TRIGERRED = "Successfully triggered the {0} storage volume operation."
VOLUME_NAME_REQUIRED_FOR_DELETE = "Virtual disk name is a required parameter for remove virtual disk operations."
VOLUME_NOT_FOUND = "Unable to find the virtual disk."
CHANGES_NOT_FOUND = "No changes found to commit!"
CHANGES_FOUND = "Changes found to commit!"
ODATA_ID = "@odata.id"
ODATA_REGEX = "(.*?)@odata"
ATTRIBUTE = "</Attribute>"
VIEW_OPERATION_FAILED = "Failed to fetch storage details."
VIEW_CONTROLLER_DETAILS_NOT_FOUND = "Failed to find the controller {controller_id}."
VIEW_OPERATION_CONTROLLER_NOT_SPECIFIED = "Controller identifier parameter is missing."
VIEW_VIRTUAL_DISK_DETAILS_NOT_FOUND = "Failed to find the volume : {volume_id} in controller : {controller_id}."
SUCCESS_STATUS = "Success"
FAILED_STATUS = "Failed"
CONTROLLER_BATTERY = "Battery.Integrated.1:RAID.SL.5-1"
CONTROLLER_ID_FIRST = "AHCI.Embedded.1-1"
CONTROLLER_ID_SECOND = "AHCI.Embedded.1-2"
CONTROLLER_ID_THIRD = "AHCI.Embedded.1-3"
CONTROLLER_ID_FOURTH = "RAID.SL.5-1"
CONTROLLER_ID_FIFTH = "RAID.SL.5-3"
SYSTEM = 'System.Embedded.1'
ENCLOSURE_ID = 'Enclosure.Internal.0-1:RAID.SL.5-1'
PHYSICAL_DISK_FIRST = 'Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1'
PHYSICAL_DISK_SECOND = 'Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-3'
VIRTUAL_DISK_FIRST = 'Disk.Virtual.0:RAID.SL.5-1'
VIRTUAL_DISK_SECOND = 'Disk.Virtual.1:RAID.SL.5-1'
ALL_STORAGE_DATA_METHOD = "StorageData.all_storage_data"
FETCH_STORAGE_DATA_METHOD = "StorageData.fetch_storage_data"
FILTER_DISK = 'StorageCreate.filter_disk'
VIEW_EXECUTE = 'StorageView.execute'
DATA_XML = '<Data></Data>'
REDFISH = "/redfish/v1"
API_INVOKE_MOCKER = "iDRACRedfishAPI.invoke_request"
BASE_IDRAC_API = "/redfish/v1/Chassis/System.Embedded.1"


class TestStorageData(FakeAnsibleModule):
    module = idrac_storage_volume
    storage_controllers = {
        ODATA_ID: "/redfish/v1/Systems/System.Embedded.1/Storage"
    }
    volumes_list = [
        {
            ODATA_ID: "/redfish/v1/Systems/System.Embedded.1/Storage/RAID.SL.5-1/Volumes/Disk.Virtual.0:RAID.SL.5-1"
        },
        {
            ODATA_ID: "/redfish/v1/Systems/System.Embedded.1/Storage/RAID.SL.5-1/Volumes/Disk.Virtual.1:RAID.SL.5-1"
        }]
    controllers_list = {
        "Members": [
            {
                "Controllers": {
                    ODATA_ID: "/redfish/v1/Systems/System.Embedded.1/Storage/RAID.SL.5-1/Controllers"
                },
                "Drives": [
                    {
                        ODATA_ID: "/redfish/v1/Systems/System.Embedded.1/Storage/RAID.SL.5-1/Drives/Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1"
                    }
                ],
                "Id": CONTROLLER_ID_FOURTH,
                "Links": {
                    "Enclosures": [
                        {
                            ODATA_ID: "/redfish/v1/Chassis/Enclosure.Internal.0-1:RAID.SL.5-1"
                        }
                    ]
                },
                "Volumes": {
                    ODATA_ID: "/redfish/v1/Systems/System.Embedded.1/Storage/RAID.SL.5-1/Volumes"
                },
                "Oem": {
                    "Dell": {
                        "DellControllerBattery": {
                            "Id": CONTROLLER_BATTERY
                        }}
                }
            },
            {
                "Drives": [
                    {
                        ODATA_ID: "/redfish/v1/Systems/System.Embedded.1/Storage/CPU.1/Drives/Disk.Bay.23:Enclosure.Internal.0-3"
                    }
                ],
                "Drives@odata.count": 1,
                "Id": "CPU.1",
                "Links": {
                    "Enclosures": [
                        {
                            ODATA_ID: "/redfish/v1/Chassis/Enclosure.Internal.0-3"
                        }
                    ],
                },
                "Volumes": {
                    ODATA_ID: "/redfish/v1/Systems/System.Embedded.1/Storage/CPU.1/Volumes"
                }
            },
            {
                "Controllers": {
                    ODATA_ID: "/redfish/v1/Systems/System.Embedded.1/Storage/AHCI.Embedded.1-1/Controllers"
                },
                "Drives": [],
                "Id": CONTROLLER_ID_FIRST,
                "Links": {
                    "Enclosures": [
                        {
                            ODATA_ID: BASE_IDRAC_API
                        }
                    ]
                },
                "Volumes": {
                    ODATA_ID: "/redfish/v1/Systems/System.Embedded.1/Storage/AHCI.Embedded.1-1/Volumes"
                }
            }
        ]
    }

    storage_data = {
        'Controllers': {
            CONTROLLER_ID_FIRST: {
                'Controllers': {
                    ODATA_ID: '/redfish/v1/Systems/System.Embedded.1/Storage/AHCI.Embedded.1-1/Controllers',
                },
                'Drives': {},
                'Id': CONTROLLER_ID_FIRST,
                'Links': {
                    'Enclosures': {
                        SYSTEM: BASE_IDRAC_API,
                    },
                },
                'Volumes': {},
                "Oem": {
                    "Dell": {
                        "CPUAffinity": []
                    }
                }
            },
            CONTROLLER_ID_SECOND: {
                'Controllers': {
                    ODATA_ID: '/redfish/v1/Systems/System.Embedded.1/Storage/AHCI.Embedded.1-2/Controllers',
                },
                'Drives': {
                    'Disk.Bay.0:Enclosure.Internal.0-1:AHCI.Embedded.1-2': '/redfish/v1/\
                    Systems/System.Embedded.1/Storage/RAID.SL.5-1/Drives/Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1',
                },
                'Id': CONTROLLER_ID_SECOND,
                'Links': {
                    'Enclosures': {
                        SYSTEM: BASE_IDRAC_API,
                    },
                },
                'Volumes': {},
                "Oem": {
                    "Dell": {
                        "CPUAffinity": []
                    }
                }
            },
            CONTROLLER_ID_THIRD: {
                'Controllers': {
                    ODATA_ID: '/redfish/v1/Systems/System.Embedded.1/Storage/AHCI.Embedded.1-2/Controllers',
                },
                'Drives': {
                    'Disk.Bay.0:Enclosure.Internal.0-1:AHCI.Embedded.1-3': '/redfish/v1/\
                    Systems/System.Embedded.1/Storage/AHCI.Embedded.1-3/Drives/Disk.Bay.0:Enclosure.Internal.0-1:AHCI.Embedded.1-3',
                },
                'Id': CONTROLLER_ID_THIRD,
                'Links': {
                    'Enclosures': {
                        ENCLOSURE_ID: {
                            "Links": {
                                "Drives": []
                            }
                        },
                    },
                },
                'Volumes': {},
                "Oem": {
                    "Dell": {
                        "CPUAffinity": []
                    }
                }
            },
            CONTROLLER_ID_FOURTH: {
                'Controllers': {
                    ODATA_ID: '/redfish/v1/Systems/System.Embedded.1/Storage/RAID.SL.5-1/Controllers',
                },
                'Drives': {
                    PHYSICAL_DISK_FIRST: '/redfish/v1/Systems\
                        /System.Embedded.1/Storage/RAID.SL.5-1/Drives/Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1',
                },
                'Id': CONTROLLER_ID_FOURTH,
                'Links': {
                    'Enclosures': {
                        ENCLOSURE_ID: {"Links": {
                            "Drives": [
                                {
                                    ODATA_ID: PHYSICAL_DISK_FIRST
                                }
                            ]}}
                    },
                },
                'Volumes': {
                    VIRTUAL_DISK_FIRST: {
                        "Links": {
                            "Drives": [
                                {
                                    ODATA_ID: PHYSICAL_DISK_FIRST
                                }
                            ]
                        },
                    },
                    VIRTUAL_DISK_SECOND: {
                        "Links": {
                            "Drives": [
                                {
                                    ODATA_ID: PHYSICAL_DISK_FIRST
                                }
                            ]
                        },
                    },
                },
                "Oem": {
                    "Dell": {
                        "DellControllerBattery": {
                            "Id": CONTROLLER_BATTERY
                        }}
                }
            }
        }
    }

    storage_data_expected = {
        'Controller': {
            CONTROLLER_ID_FIRST: {
                'ControllerSensor': {
                    CONTROLLER_ID_FIRST: {},
                },
            },
            CONTROLLER_ID_SECOND: {
                'ControllerSensor': {
                    CONTROLLER_ID_SECOND: {},
                },
                'PhysicalDisk': [
                    'Disk.Bay.0:Enclosure.Internal.0-1:AHCI.Embedded.1-2',
                ],
            },
            CONTROLLER_ID_THIRD: {
                'ControllerSensor': {
                    CONTROLLER_ID_THIRD: {}
                },
                'Enclosure': {
                    ENCLOSURE_ID: {
                        'EnclosureSensor': {
                            ENCLOSURE_ID: {},
                        },
                    },
                },
            },
            CONTROLLER_ID_FOURTH: {
                'ControllerSensor': {
                    CONTROLLER_ID_FOURTH: {
                        'ControllerBattery': [
                            'Battery.Integrated.1:RAID.SL.5-1',
                        ],
                    },
                },
                'Enclosure': {
                    ENCLOSURE_ID: {
                        'EnclosureSensor': {
                            ENCLOSURE_ID: {},
                        },
                        'PhysicalDisk': [
                            PHYSICAL_DISK_FIRST,
                        ],
                    },
                },
                'VirtualDisk': {
                    VIRTUAL_DISK_FIRST: {
                        'PhysicalDisk': [
                            PHYSICAL_DISK_FIRST,
                        ],
                    },
                    VIRTUAL_DISK_SECOND: {
                        'PhysicalDisk': [
                            PHYSICAL_DISK_FIRST,
                        ],
                    },
                },
            },
        }
    }

    storage_data_idrac8 = {
        'Controllers': {
            CONTROLLER_ID_FIFTH: {
                'Controllers': {
                    ODATA_ID: '/redfish/v1/Systems/System.Embedded.1/Storage/RAID.SL.5-3/Controllers',
                },
                'Drives': {
                    PHYSICAL_DISK_SECOND: '/redfish/v1/Systems\
                        /System.Embedded.1/Storage/RAID.SL.5-3/Drives/Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-3',
                },
                'Id': CONTROLLER_ID_FIFTH,
                'Links': {
                    'Enclosures': {
                        ENCLOSURE_ID: {"Links": {
                            "Drives": [
                                {
                                    ODATA_ID: PHYSICAL_DISK_SECOND
                                }
                            ]}}
                    },
                },
                'Volumes': {
                    'Disk.Virtual.0:RAID.SL.5-3': {
                        "Links": {
                            "Drives": [
                                {
                                    ODATA_ID: PHYSICAL_DISK_SECOND
                                }
                            ]
                        },
                    },
                    'Disk.Virtual.1:RAID.SL.5-3': {
                        "Links": {
                            "Drives": [
                                {
                                    ODATA_ID: PHYSICAL_DISK_SECOND
                                }
                            ]
                        },
                    },
                },
                "Oem": {
                    "Dell": {
                        "DellControllerBattery": {
                            "Id": "Battery.Integrated.1:RAID.SL.5-3"
                        }}
                }
            }
        }
    }

    storage_data_expected_idrac8 = {
        'Controller': {
            CONTROLLER_ID_FIFTH: {
                'ControllerSensor': {
                    CONTROLLER_ID_FIFTH: {},
                },
                'Enclosure': {
                    ENCLOSURE_ID: {
                        'EnclosureSensor': {
                            ENCLOSURE_ID: {},
                        },
                        'PhysicalDisk': [
                            PHYSICAL_DISK_SECOND,
                        ],
                    },
                },
                'VirtualDisk': {
                    'Disk.Virtual.0:RAID.SL.5-3': {
                        'PhysicalDisk': [
                            PHYSICAL_DISK_SECOND,
                        ],
                    },
                    'Disk.Virtual.1:RAID.SL.5-3': {
                        'PhysicalDisk': [
                            PHYSICAL_DISK_SECOND,
                        ],
                    },
                },
            },
        }
    }

    @pytest.fixture
    def idrac_storage_volume_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_storage_volume_mock(self, mocker, idrac_storage_volume_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_storage_volume_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_storage_volume_mock
        return idrac_conn_mock

    def test_fetch_controllers_uri(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        def mock_get_dynamic_uri_request(*args, **kwargs):
            return self.storage_controllers

        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(SYSTEM, ''))
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageData(
            idrac_connection_storage_volume_mock, f_module)
        data = idr_obj.fetch_controllers_uri()
        assert data == self.storage_controllers

        # Scenario 2: for error message
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(REDFISH, "Error"))
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        idr_obj = self.module.StorageData(
            idrac_connection_storage_volume_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj.fetch_controllers_uri()
        assert exc.value.args[0] == "Error"

    def test_fetch_api_data(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        key = "Storage"
        obj = MagicMock()
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        idr_obj = self.module.StorageData(idrac_connection_storage_volume_mock, f_module)
        key_out, uri_data_out = idr_obj.fetch_api_data(self.storage_controllers[ODATA_ID], -1)
        assert key == key_out
        assert obj == uri_data_out

    def test_all_storage_data(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        def mock_get_dynamic_uri_request(*args, **kwargs):
            if len(args) == 3 and args[2] == "Members":
                return self.volumes_list
            else:
                return self.controllers_list
        mocker.patch(MODULE_PATH + "StorageData.fetch_controllers_uri",
                     return_value=self.storage_controllers)
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        idr_obj = self.module.StorageData(idrac_connection_storage_volume_mock, f_module)
        storage_info = idr_obj.all_storage_data()
        assert set(storage_info.keys()) == {'Controllers'}
        assert set(storage_info["Controllers"].keys()) == {CONTROLLER_ID_FIRST, CONTROLLER_ID_FOURTH}

    def test_fetch_storage_data(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        mocker.patch(MODULE_PATH + ALL_STORAGE_DATA_METHOD,
                     return_value=self.storage_data)
        mocker.patch(MODULE_PATH + "get_idrac_firmware_version",
                     return_value="3.20.00")
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        idr_obj = self.module.StorageData(idrac_connection_storage_volume_mock, f_module)
        storage_info = idr_obj.fetch_storage_data()
        assert storage_info == self.storage_data_expected

        # Scenario - for idrac 8
        mocker.patch(MODULE_PATH + ALL_STORAGE_DATA_METHOD,
                     return_value=self.storage_data_idrac8)
        mocker.patch(MODULE_PATH + "get_idrac_firmware_version",
                     return_value="2.00")
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        idr_obj = self.module.StorageData(idrac_connection_storage_volume_mock, f_module)
        storage_info = idr_obj.fetch_storage_data()
        assert storage_info == self.storage_data_expected_idrac8


class TestStorageView(TestStorageData):
    module = idrac_storage_volume

    @pytest.fixture
    def idrac_storage_volume_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_storage_volume_mock(self, mocker, idrac_storage_volume_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_storage_volume_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_storage_volume_mock
        return idrac_conn_mock

    def test_execute(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        mocker.patch(MODULE_PATH + FETCH_STORAGE_DATA_METHOD,
                     return_value=TestStorageData.storage_data_expected)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        idr_obj = self.module.StorageView(idrac_connection_storage_volume_mock, f_module)
        out = idr_obj.execute()
        assert out == {"Message": TestStorageData.storage_data_expected, "Status": SUCCESS_STATUS}

        # Scenario - When controller_id is passed
        data_when_controller_id_passed = deepcopy(TestStorageData.storage_data_expected)
        mocker.patch(MODULE_PATH + FETCH_STORAGE_DATA_METHOD,
                     return_value=data_when_controller_id_passed)
        idrac_default_args.update({"controller_id": CONTROLLER_ID_FIRST})
        out = idr_obj.execute()
        assert out == {"Message": data_when_controller_id_passed, "Status": SUCCESS_STATUS}

        # Scenario - When invalid controller_id is passed
        data_when_invlid_controller_id_passed = deepcopy(TestStorageData.storage_data_expected)
        mocker.patch(MODULE_PATH + FETCH_STORAGE_DATA_METHOD,
                     return_value=data_when_invlid_controller_id_passed)
        controller_id = "AHCI.Embedded.1-invalid"
        idrac_default_args.update({"controller_id": controller_id})
        with pytest.raises(Exception) as exc:
            idr_obj.execute()
        assert exc.value.args[0] == VIEW_OPERATION_FAILED

        # Scenario - When volume_id and invalid controller_id is passed
        data_when_invlid_volume_id_passed = deepcopy(TestStorageData.storage_data_expected)
        mocker.patch(MODULE_PATH + FETCH_STORAGE_DATA_METHOD,
                     return_value=data_when_invlid_volume_id_passed)
        idrac_default_args.update({"volume_id": VIRTUAL_DISK_FIRST})
        with pytest.raises(Exception) as exc:
            idr_obj.execute()
        assert exc.value.args[0] == VIEW_OPERATION_FAILED
        # VIEW_CONTROLLER_DETAILS_NOT_FOUND.format(controller_id=controller_id)

        # Scenario - When volume_id and valid controller_id is passed
        data_when_controller_id_and_volume_id_passed = deepcopy(TestStorageData.storage_data_expected)
        mocker.patch(MODULE_PATH + FETCH_STORAGE_DATA_METHOD,
                     return_value=data_when_controller_id_and_volume_id_passed)
        idrac_default_args.update({"controller_id": CONTROLLER_ID_FOURTH, "volume_id": VIRTUAL_DISK_FIRST})
        out = idr_obj.execute()
        assert out == {"Message": data_when_controller_id_and_volume_id_passed, "Status": SUCCESS_STATUS}

        # Scenario - When invalid volume_id and valid controller_id is passed
        data_when_controller_id_and_volume_id_passed = deepcopy(TestStorageData.storage_data_expected)
        mocker.patch(MODULE_PATH + FETCH_STORAGE_DATA_METHOD,
                     return_value=data_when_controller_id_and_volume_id_passed)
        idrac_default_args.update({"controller_id": CONTROLLER_ID_FIRST, "volume_id": VIRTUAL_DISK_FIRST})
        with pytest.raises(Exception) as exc:
            idr_obj.execute()
        assert exc.value.args[0] == VIEW_OPERATION_FAILED

        # Scenario - When volume_id is passed
        data_when_volume_id_passed = deepcopy(TestStorageData.storage_data_expected)
        mocker.patch(MODULE_PATH + FETCH_STORAGE_DATA_METHOD,
                     return_value=data_when_volume_id_passed)
        del idrac_default_args["controller_id"]
        idrac_default_args.update({"volume_id": VIRTUAL_DISK_FIRST})
        with pytest.raises(Exception) as exc:
            idr_obj.execute()
        assert exc.value.args[0] == VIEW_OPERATION_FAILED


class TestStorageBase(FakeAnsibleModule):
    module = idrac_storage_volume

    @pytest.fixture
    def idrac_storage_volume_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_storage_volume_mock(self, mocker, idrac_storage_volume_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_storage_volume_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_storage_volume_mock
        return idrac_conn_mock

    def test_module_extend_input(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        mocker.patch(MODULE_PATH + 'StorageBase.data_conversion', return_value={})
        idrac_default_args.update({'span_length': 1, 'span_depth': 1})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageBase(idrac_connection_storage_volume_mock, f_module)
        data = idr_obj.module_extend_input(f_module)
        # Scenario 1: when volumes is None
        assert data['volumes'] == [{'drives': {'id': [-1]}}]

        # Scenario 2: when volumes is given
        idrac_default_args.update({'volumes': [{"drives": {'location': [3]}, 'span_length': '1'}]})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        mocker.patch(MODULE_PATH + 'StorageBase.data_conversion', return_value={"drives": {'location': [3]}, 'span_length': '1'})

        idr_obj = self.module.StorageBase(idrac_connection_storage_volume_mock, f_module)
        data = idr_obj.module_extend_input(f_module)
        assert data['volumes'] == [{"drives": {'location': [3]}, 'span_length': 1}]

    def test_payload_for_disk(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageBase(idrac_connection_storage_volume_mock, f_module)
        # Scenario 1: When drives is given
        data = idr_obj.payload_for_disk({'drives': {'id': [1, 2]}})
        assert data == '<Attribute Name="IncludedPhysicalDiskID">1</Attribute><Attribute Name="IncludedPhysicalDiskID">2</Attribute>'

        # Scenario 2: When dedicate_hot_spare is in each_volume
        data = idr_obj.payload_for_disk({'dedicated_hot_spare': [3, 5]})
        assert data == '<Attribute Name="RAIDdedicatedSpare">3</Attribute><Attribute Name="RAIDdedicatedSpare">5</Attribute>'

    def test_construct_volume_payloadk(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        mocker.patch(MODULE_PATH + 'xml_data_conversion', return_value=DATA_XML)
        mocker.patch(MODULE_PATH + 'StorageBase.payload_for_disk', return_value='payload_detail_in_xml')
        # Scenario 1: When state is create
        idrac_default_args.update({'state': 'create'})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageBase(idrac_connection_storage_volume_mock, f_module)
        data = idr_obj.construct_volume_payload(1, {})
        assert data == DATA_XML

    def test_constuct_payload(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        mocker.patch(MODULE_PATH + 'xml_data_conversion', return_value=DATA_XML)
        mocker.patch(MODULE_PATH + 'StorageBase.construct_volume_payload', return_value='<Volume></Volume>')
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageBase(idrac_connection_storage_volume_mock, f_module)
        # Scenario 1: Default
        data = idr_obj.constuct_payload({})
        assert data == DATA_XML

        # Scenario 2: When raid_reset_config is 'true'
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageBase(idrac_connection_storage_volume_mock, f_module)
        idr_obj.module_ext_params.update({'raid_reset_config': 'true'})
        data = idr_obj.constuct_payload({})
        assert data == DATA_XML

    def test_wait_for_job_completion(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        obj = MagicMock()
        obj.headers = {'Location': "/joburl/JID12345"}
        job = {"job_wait": True, "job_wait_timeout": 1200}
        idrac_default_args.update(job)
        job_resp_completed = {'JobStatus': 'Completed'}
        idrac_redfish_resp = (False, 'Job Success', job_resp_completed, 1200)
        mocker.patch(MODULE_PATH + 'idrac_redfish_job_tracking', return_value=idrac_redfish_resp)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageBase(idrac_connection_storage_volume_mock, f_module)
        # Scenario 1: Job_wait is True, job_wait_timeout match with default
        with pytest.raises(Exception) as exc:
            idr_obj.wait_for_job_completion(obj)
        assert exc.value.args[0] == WAIT_TIMEOUT_MSG.format(1200)

        # Scenario 2: Job_wait is True, job_wait_timeout less than default
        idrac_redfish_resp = (False, 'Job Success', job_resp_completed, 1000)
        mocker.patch(MODULE_PATH + 'idrac_redfish_job_tracking', return_value=idrac_redfish_resp)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageBase(idrac_connection_storage_volume_mock, f_module)
        data = idr_obj.wait_for_job_completion(obj)
        assert data == job_resp_completed

        # Scenario 3: Job failed in resp
        job_resp_failed = {'JobStatus': 'Failed', 'Message': 'Job failed.'}
        idrac_redfish_resp = (True, 'Job Failed', job_resp_failed, 1000)
        mocker.patch(MODULE_PATH + 'idrac_redfish_job_tracking', return_value=idrac_redfish_resp)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageBase(idrac_connection_storage_volume_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj.wait_for_job_completion(obj)
        assert exc.value.args[0] == 'Job failed.'

        # Scenario 4: Job wait is false
        obj.json_data = {'JobStatus': 'Running'}
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        job = {"job_wait": False, "job_wait_timeout": 1200}
        idrac_default_args.update(job)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        f_module.params.update({'state': 'create'})
        idr_obj = self.module.StorageBase(idrac_connection_storage_volume_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj.wait_for_job_completion(obj)
        assert exc.value.args[0] == JOB_TRIGERRED.format('create')


class TestStorageValidation(TestStorageBase):
    module = idrac_storage_volume

    @pytest.fixture
    def idrac_storage_volume_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_storage_volume_mock(self, mocker, idrac_storage_volume_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_storage_volume_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_storage_volume_mock
        return idrac_conn_mock

    def test_validate_controller_exists(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        # Scenario - when controller_id is not passed
        mocker.patch(MODULE_PATH + ALL_STORAGE_DATA_METHOD,
                     return_value=TestStorageData.storage_data)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageValidation(idrac_connection_storage_volume_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj.validate_controller_exists()
        assert exc.value.args[0] == CONTROLLER_NOT_DEFINED

        # Scenario - when invalid controller_id is passed
        controller_id = "AHCI.Embedded.1-invalid"
        idrac_default_args.update({"controller_id": controller_id})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageValidation(idrac_connection_storage_volume_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj.validate_controller_exists()
        assert exc.value.args[0] == CONTROLLER_NOT_EXIST_ERROR.format(controller_id=controller_id)

        # Scenario - when controller_id is passed
        controller_id = CONTROLLER_ID_FIRST
        idrac_default_args.update({"controller_id": controller_id})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageValidation(idrac_connection_storage_volume_mock, f_module)
        idr_obj.validate_controller_exists()

    def test_validate_job_wait_negative_values(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        # Scenario - when job_wait_timeout is negative
        mocker.patch(MODULE_PATH + ALL_STORAGE_DATA_METHOD,
                     return_value=TestStorageData.storage_data)
        idrac_default_args.update({"job_wait": True, "job_wait_timeout": -120})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageValidation(idrac_connection_storage_volume_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj.validate_job_wait_negative_values()
        assert exc.value.args[0] == NEGATIVE_OR_ZERO_MSG.format(parameter="job_wait_timeout")

        # Scenario - when job_wait_timeout is positive
        idrac_default_args.update({"job_wait": True, "job_wait_timeout": 120})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageValidation(idrac_connection_storage_volume_mock, f_module)
        idr_obj.validate_job_wait_negative_values()

    def test_validate_time_to_wait(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        # Scenario - when time_to_wait < 300
        mocker.patch(MODULE_PATH + ALL_STORAGE_DATA_METHOD,
                     return_value=TestStorageData.storage_data)
        idrac_default_args.update({"time_to_wait": 299})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageValidation(idrac_connection_storage_volume_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj.validate_time_to_wait()
        assert exc.value.args[0] == TIME_TO_WAIT_MSG

        # Scenario - when time_to_wait > 3600
        idrac_default_args.update({"time_to_wait": 3601})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageValidation(idrac_connection_storage_volume_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj.validate_time_to_wait()
        assert exc.value.args[0] == TIME_TO_WAIT_MSG

    @pytest.mark.parametrize("params", [
        {"span_depth": -1, "span_length": 2, "capacity": 200, "strip_size": 131072},
        {"span_depth": 1, "span_length": -1, "capacity": 200, "strip_size": 131072},
        {"span_depth": 1, "span_length": 2, "capacity": -1, "strip_size": 131072},
        {"span_depth": 1, "span_length": 2, "capacity": 200, "strip_size": -131072},
    ])
    def test_validate_negative_values_for_volume_params(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker, params):
        # Scenario - when job_wait_timeout is negative
        mocker.patch(MODULE_PATH + ALL_STORAGE_DATA_METHOD,
                     return_value=TestStorageData.storage_data)
        # idrac_default_args.update(params)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageValidation(idrac_connection_storage_volume_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj.validate_negative_values_for_volume_params(params)
        # TO DO replace job_wait_timeout with key in params which has negative value
        negative_key = next((k for k, v in params.items() if v < 0), None)
        assert exc.value.args[0] == NEGATIVE_OR_ZERO_MSG.format(parameter=negative_key)

    def test_validate_negative_values_for_volume_params_with_different_parameter(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        # Scenario - passing different parameter
        mocker.patch(MODULE_PATH + ALL_STORAGE_DATA_METHOD,
                     return_value=TestStorageData.storage_data)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageValidation(idrac_connection_storage_volume_mock, f_module)
        idr_obj.validate_negative_values_for_volume_params({"volume_type": "RAID 0", "number_dedicated_hot_spare": 0})

        # Scenario - when number_dedicated_hot_spare is negative
        with pytest.raises(Exception) as exc:
            idr_obj.validate_negative_values_for_volume_params({"number_dedicated_hot_spare": -1})
        assert exc.value.args[0] == NEGATIVE_MSG.format(parameter="number_dedicated_hot_spare")

        # Scenario - when number_dedicated_hot_spare is not negative
        idr_obj.validate_negative_values_for_volume_params({"number_dedicated_hot_spare": 0})

    def test_validate_volume_drives(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        # Scenario - when volume drives are not defined
        volumes = {
            "name": "volume_1"
        }
        mocker.patch(MODULE_PATH + ALL_STORAGE_DATA_METHOD,
                     return_value=TestStorageData.storage_data)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageValidation(idrac_connection_storage_volume_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj.validate_volume_drives(volumes)
        assert exc.value.args[0] == DRIVES_NOT_DEFINED

        # Scenario - when in volume drives id and location both defined
        volumes = {
            "name": "volume_1",
            "drives": {
                "id": [
                    PHYSICAL_DISK_FIRST,
                    PHYSICAL_DISK_SECOND
                ],
                "location": [7, 3]
            }
        }
        with pytest.raises(Exception) as exc:
            idr_obj.validate_volume_drives(volumes)
        assert exc.value.args[0] == ID_AND_LOCATION_BOTH_DEFINED

        # Scenario - when in volume drives id and location both not defined
        volumes = {
            "name": "volume_1",
            "drives": {
                PHYSICAL_DISK_FIRST: {}
            }
        }
        with pytest.raises(Exception) as exc:
            idr_obj.validate_volume_drives(volumes)
        assert exc.value.args[0] == ID_AND_LOCATION_BOTH_NOT_DEFINED

        # Scenario - when in volume drives id is defined
        volumes = {
            "name": "volume_1",
            "drives": {
                "id": [
                    PHYSICAL_DISK_FIRST,
                    PHYSICAL_DISK_SECOND
                ]
            }
        }
        mocker.patch(MODULE_PATH + "StorageValidation.raid_std_validation",
                     return_value=True)
        out = idr_obj.validate_volume_drives(volumes)
        assert out is True

    def test_raid_std_validation(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        mocker.patch(MODULE_PATH + ALL_STORAGE_DATA_METHOD,
                     return_value=TestStorageData.storage_data)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageValidation(idrac_connection_storage_volume_mock, f_module)
        # Scenario - Invalid span_length
        params = {"span_depth": 1, "span_length": 4, "pd_count": 2, "volume_type": "RAID 1"}
        with pytest.raises(Exception) as exc:
            idr_obj.raid_std_validation(params["span_length"],
                                        params["span_depth"],
                                        params["volume_type"],
                                        params["pd_count"])
        assert exc.value.args[0] == INVALID_VALUE_MSG.format(parameter="span_length")

        # Scenario - Invalid span_depth for RAID 1
        params = {"span_depth": 4, "span_length": 2, "pd_count": 3, "volume_type": "RAID 1"}
        with pytest.raises(Exception) as exc:
            idr_obj.raid_std_validation(params["span_length"],
                                        params["span_depth"],
                                        params["volume_type"],
                                        params["pd_count"])
        assert exc.value.args[0] == INVALID_VALUE_MSG.format(parameter="span_depth")

        # Scenario - Invalid span_depth for RAID 10
        params = {"span_depth": 1, "span_length": 2, "pd_count": 9, "volume_type": "RAID 10"}
        with pytest.raises(Exception) as exc:
            idr_obj.raid_std_validation(params["span_length"],
                                        params["span_depth"],
                                        params["volume_type"],
                                        params["pd_count"])
        assert exc.value.args[0] == INVALID_VALUE_MSG.format(parameter="span_depth")

        # Scenario - Invalid drive count
        params = {"span_depth": 3, "span_length": 2, "pd_count": 1, "volume_type": "RAID 10"}
        with pytest.raises(Exception) as exc:
            idr_obj.raid_std_validation(params["span_length"],
                                        params["span_depth"],
                                        params["volume_type"],
                                        params["pd_count"])
        assert exc.value.args[0] == INVALID_VALUE_MSG.format(parameter="drives")

        # Scenario - Valid
        params = {"span_depth": 2, "span_length": 2, "pd_count": 4, "volume_type": "RAID 10"}
        out = idr_obj.raid_std_validation(params["span_length"],
                                          params["span_depth"],
                                          params["volume_type"],
                                          params["pd_count"])
        assert out is True


class TestStorageCreate(TestStorageBase):
    module = idrac_storage_volume

    @pytest.fixture
    def idrac_storage_volume_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_storage_volume_mock(self, mocker, idrac_storage_volume_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_storage_volume_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_storage_volume_mock
        return idrac_conn_mock

    def test_disk_slot_id_conversion(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        mocker.patch(MODULE_PATH + ALL_STORAGE_DATA_METHOD, return_value=TestStorageData.storage_data)
        # Scenario 1: location is given in drives
        volume = {'drives': {'location': [0, 1]}}
        idrac_default_args.update({"controller_id": CONTROLLER_ID_SECOND})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageCreate(idrac_connection_storage_volume_mock, f_module)
        data = idr_obj.disk_slot_location_to_id_conversion(volume)
        assert data['id'] == TestStorageData.storage_data_expected['Controller'][CONTROLLER_ID_SECOND]['PhysicalDisk']

        # Scenario 2: id is given in drives
        id_list = ['Disk.Bay.3:Enclosure.Internal.0-1:AHCI.Embedded.1-2',
                   'Disk.Bay.2:Enclosure.Internal.0-1:AHCI.Embedded.1-2']
        volume = {'drives': {'id': id_list}}
        idrac_default_args.update({"controller_id": CONTROLLER_ID_SECOND})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageCreate(idrac_connection_storage_volume_mock, f_module)
        data = idr_obj.disk_slot_location_to_id_conversion(volume)
        assert data['id'] == id_list

        # Scenario 3: When id and location is not given in drives
        volume = {'drives': {}}
        data = idr_obj.disk_slot_location_to_id_conversion(volume)
        assert data == {}

    def test_perform_intersection_on_disk(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        # Scenario 1: When iDRAC has firmware version greater than 3.00.00.00
        mocker.patch(MODULE_PATH + ALL_STORAGE_DATA_METHOD, return_value=TestStorageData.storage_data)
        mocker.patch(MODULE_PATH + "get_idrac_firmware_version", return_value="3.10.00")
        volume = {'media_type': 'HDD', 'protocol': 'SATA'}
        healthy_disk, available_disk, media_disk, protocol_disk = {1, 2, 3, 4, 5}, {1, 2, 3, 5}, {2, 3, 4, 5}, {1, 5}
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageCreate(idrac_connection_storage_volume_mock, f_module)
        data = idr_obj.perform_intersection_on_disk(volume, healthy_disk, available_disk, media_disk, protocol_disk)
        assert data == [5]

        # Scenario 1: When iDRAC has firmware version less than 3.00.00.00
        mocker.patch(MODULE_PATH + "get_idrac_firmware_version", return_value="2.00.00")
        volume = {'media_type': None, 'protocol': None}
        data = idr_obj.perform_intersection_on_disk(volume, healthy_disk, available_disk, media_disk, protocol_disk)
        assert data == [1, 2, 3, 4, 5]

    def test_filter_disk(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        drive_resp = {'DriveID1': {'MediaType': 'HDD', 'Protocol': 'SAS', 'Status': {'Health': 'OK'},
                                   'Oem': {'Dell': {'DellPhysicalDisk': {'RaidStatus': 'Ready'}}}},
                      'DriveID2': {'MediaType': 'SSD', 'Protocol': 'SATA', 'Status': {'Health': 'Not OK'}}}
        idrac_data = {'Controllers': {CONTROLLER_ID_FIRST: {'Drives': drive_resp}}}
        # Scenario 1: When iDRAC has firmware version equal to 3.00.00.00
        mocker.patch(MODULE_PATH + ALL_STORAGE_DATA_METHOD, return_value=idrac_data)
        mocker.patch(MODULE_PATH + "get_idrac_firmware_version", return_value="3.05.00")
        volume = {'media_type': 'HDD', 'protocol': 'SAS'}
        idrac_default_args.update({"controller_id": CONTROLLER_ID_FIRST})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageCreate(idrac_connection_storage_volume_mock, f_module)
        data = idr_obj.filter_disk(volume)
        assert data == ['DriveID1']

    def test_updating_drives_module_input_when_given(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        mocker.patch(MODULE_PATH + ALL_STORAGE_DATA_METHOD, return_value=TestStorageData.storage_data)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageCreate(idrac_connection_storage_volume_mock, f_module)
        # Scenario 1: When id is in drives
        volume = {'drives': {'id': [2, 3, 4, 5]}}
        filter_disk_output = [1, 3, 5]
        data = idr_obj.updating_drives_module_input_when_given(volume, filter_disk_output)
        assert data == [3, 5]

        # Scenario 2: When id is not in drives
        volume = {'drives': {'location': [2, 3, 4, 5]}}
        data = idr_obj.updating_drives_module_input_when_given(volume, filter_disk_output)
        assert data == []

    def test_updating_volume_module_input_for_hotspare(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        mocker.patch(MODULE_PATH + ALL_STORAGE_DATA_METHOD, return_value=TestStorageData.storage_data)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageCreate(idrac_connection_storage_volume_mock, f_module)
        # Scenario 1: number_dedicated_hot_spare is in volume and greator than zero
        volume = {'number_dedicated_hot_spare': 2}
        filter_disk_output = [1, 3, 5, 4, 2]
        reserved_pd = [1]
        drive_exists_in_id = [3, 5]
        data = idr_obj.updating_volume_module_input_for_hotspare(volume, filter_disk_output, reserved_pd, drive_exists_in_id)
        assert data == [4, 2]

        # Scenario 2: number_dedicated_hot_spare is in volume and equal to zero
        volume = {'number_dedicated_hot_spare': 0}
        data = idr_obj.updating_volume_module_input_for_hotspare(volume, filter_disk_output, reserved_pd, drive_exists_in_id)
        assert data == []

    def test_updating_volume_module_input(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        mocker.patch(MODULE_PATH + ALL_STORAGE_DATA_METHOD, return_value=TestStorageData.storage_data)
        mocker.patch(MODULE_PATH + FILTER_DISK, return_value=[1, 2, 3, 4, 5])
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageCreate(idrac_connection_storage_volume_mock, f_module)
        # Scenario 1: When required pd is less than available pd
        volume = {'volumes': [{'span_depth': 1, 'span_length': 1, 'stripe_size': 65536, 'capacity': 50.45,
                               'drives': {'id': [2, 3, 4]},
                               'number_dedicated_hot_spare': 1}]}
        idr_obj.module_ext_params.update(volume)
        drive_exists_in_id = [1, 2]
        idr_obj.updating_volume_module_input(drive_exists_in_id)
        assert idr_obj.module_ext_params['volumes'][0]['drives']['id'] == [1]

        # Scenario 2: When required pd is less than available pd with check_mode
        volume = {'volumes': [{'span_depth': 1, 'span_length': 1, 'stripe_size': 65536, 'capacity': 50.45,
                               'drives': {'id': [2, 3, 4]},
                               'number_dedicated_hot_spare': 1}]}
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        idr_obj = self.module.StorageCreate(idrac_connection_storage_volume_mock, f_module)
        idr_obj.module_ext_params.update(volume)
        drive_exists_in_id = [1, 2]
        with pytest.raises(Exception) as exc:
            idr_obj.updating_volume_module_input(drive_exists_in_id)
        assert exc.value.args[0] == CHANGES_FOUND

        # Scenario 3: When required pd is greater than available pd
        mocker.patch(MODULE_PATH + FILTER_DISK, return_value=[1])
        controller_id = 'Qwerty'
        volume = {'volumes': [{'span_depth': 2, 'span_length': 1,
                               'drives': {'id': [1]}, 'number_dedicated_hot_spare': 0}],
                  'controller_id': controller_id}
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageCreate(idrac_connection_storage_volume_mock, f_module)
        idr_obj.module_ext_params.update(volume)
        drive_exists_in_id = [1, 2]
        with pytest.raises(Exception) as exc:
            idr_obj.updating_volume_module_input(drive_exists_in_id)
        assert exc.value.args[0] == NOT_ENOUGH_DRIVES.format(controller_id=controller_id)

        # Scenario 4: When required pd is greater than available pd with check_mode
        mocker.patch(MODULE_PATH + FILTER_DISK, return_value=[1])
        controller_id = 'Qwerty'
        volume = {'volumes': [{'span_depth': 2, 'span_length': 1,
                               'drives': {'id': [1, 2]}, 'number_dedicated_hot_spare': 0}],
                  'controller_id': controller_id}
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        idr_obj = self.module.StorageCreate(idrac_connection_storage_volume_mock, f_module)
        idr_obj.module_ext_params.update(volume)
        drive_exists_in_id = [1]
        with pytest.raises(Exception) as exc:
            idr_obj.updating_volume_module_input(drive_exists_in_id)
        assert exc.value.args[0] == CHANGES_NOT_FOUND

    def test_validate_create(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        mocker.patch(MODULE_PATH + ALL_STORAGE_DATA_METHOD, return_value=TestStorageData.storage_data)
        mocker.patch(MODULE_PATH + 'StorageValidation.validate_time_to_wait', return_value=None)
        mocker.patch(MODULE_PATH + 'StorageValidation.validate_controller_exists', return_value=None)
        mocker.patch(MODULE_PATH + 'StorageValidation.validate_job_wait_negative_values', return_value=None)
        mocker.patch(MODULE_PATH + 'StorageValidation.validate_negative_values_for_volume_params', return_value=None)
        mocker.patch(MODULE_PATH + 'StorageValidation.validate_volume_drives', return_value=None)
        mocker.patch(MODULE_PATH + 'StorageCreate.updating_volume_module_input', return_value=None)
        mocker.patch(MODULE_PATH + 'StorageCreate.disk_slot_location_to_id_conversion', return_value={'id': []})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageCreate(idrac_connection_storage_volume_mock, f_module)
        # Scenario 1: When required pd is less than available pd
        volume = {'volumes': [{'drives': {'location': [2, 3, 4]}},
                              {'drives': {'id': [1]}}]}
        idr_obj.module_ext_params.update(volume)
        idr_obj.validate()
        assert idr_obj.module_ext_params['volumes'][0]['drives']['id'] == []

    def test_execute_create(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        mocker.patch(MODULE_PATH + ALL_STORAGE_DATA_METHOD, return_value=TestStorageData.storage_data)
        mocker.patch(MODULE_PATH + 'StorageCreate.validate', return_value=None)
        mocker.patch(MODULE_PATH + 'StorageBase.constuct_payload', return_value=None)
        mocker.patch(MODULE_PATH + 'iDRACRedfishAPI.import_scp', return_value=None)
        mocker.patch(MODULE_PATH + 'StorageBase.wait_for_job_completion', return_value={})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageCreate(idrac_connection_storage_volume_mock, f_module)
        idr_obj.controller_id = CONTROLLER_ID_FOURTH
        data = idr_obj.execute()
        assert data == {}


class TestStorageDelete(TestStorageBase):
    module = idrac_storage_volume

    @pytest.fixture
    def idrac_storage_volume_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_storage_volume_mock(self, mocker, idrac_storage_volume_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_storage_volume_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_storage_volume_mock
        return idrac_conn_mock

    def test_execute_delete(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        idrac_resp = {'Controllers': {'Cntrl1': {'Volumes': {'Volume_ID1': {'Name': 'Volume Name 1'}}}}}
        mocker.patch(MODULE_PATH + ALL_STORAGE_DATA_METHOD, return_value=idrac_resp)
        mocker.patch(MODULE_PATH + 'StorageDelete.validate', return_value=None)
        mocker.patch(MODULE_PATH + 'iDRACRedfishAPI.import_scp', return_value=None)
        mocker.patch(MODULE_PATH + 'StorageBase.wait_for_job_completion', return_value={})
        mocker.patch(MODULE_PATH + 'StorageBase.module_extend_input', return_value={})

        # Scenario 1: When Non existing volume is passed as input
        volume = {'volumes': [{'name': 'volume-1', 'span_depth': 1, 'span_length': 1},
                              {'name': 'volume-2', 'span_depth': 1, 'span_length': 1}]}
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageDelete(idrac_connection_storage_volume_mock, f_module)
        idr_obj.module.params.update(volume)
        with pytest.raises(Exception) as exc:
            idr_obj.execute()
        assert exc.value.args[0] == VOLUME_NOT_FOUND

        # Scenario 2: When Non existing volume is passed as input with check_mode
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        idr_obj = self.module.StorageDelete(idrac_connection_storage_volume_mock, f_module)
        idr_obj.module.params.update(volume)
        with pytest.raises(Exception) as exc:
            idr_obj.execute()
        assert exc.value.args[0] == VOLUME_NOT_FOUND

        # Scenario 3: When Existing volume is passed as input
        volume = {'volumes': [{'name': 'Volume Name 1', 'span_depth': 1, 'span_length': 1}]}
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageDelete(idrac_connection_storage_volume_mock, f_module)
        idr_obj.module.params.update(volume)
        idr_obj.module_ext_params.update({'state': 'delete', 'volumes': volume})
        data = idr_obj.execute()
        assert data == {}

        # Scenario 3: When Existing volume is passed as input with check_mode
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        idr_obj = self.module.StorageDelete(idrac_connection_storage_volume_mock, f_module)
        idr_obj.module.params.update(volume)
        idr_obj.module_ext_params.update({'state': 'delete', 'volumes': volume})
        with pytest.raises(Exception) as exc:
            idr_obj.execute()
        assert exc.value.args[0] == CHANGES_FOUND

    def test_idrac_storage_volume_main_positive_case(self, idrac_default_args,
                                                     idrac_connection_storage_volume_mock, mocker):
        def returning_none():
            return None
        mocker.patch(MODULE_PATH + VIEW_EXECUTE, return_value=returning_none)
        view = 'view'
        idrac_default_args.update({'state': view})
        data = self._run_module(idrac_default_args)
        assert data['msg'] == SUCCESSFUL_OPERATION_MSG.format(operation=view)

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_idrac_storage_volume_main_exception_handling_case(self, exc_type, idrac_default_args,
                                                               idrac_connection_storage_volume_mock, mocker):

        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + VIEW_EXECUTE,
                         side_effect=exc_type('https://testhost.com', 400,
                                              'http error message',
                                              {"accept-type": "application/json"},
                                              StringIO(json_str)))
        else:
            mocker.patch(MODULE_PATH + VIEW_EXECUTE,
                         side_effect=exc_type('test'))
        result = self._run_module(idrac_default_args)
        if exc_type == URLError:
            assert result['unreachable'] is True
        else:
            assert result['failed'] is True
        assert 'msg' in result
