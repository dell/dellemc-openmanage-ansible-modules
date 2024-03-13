# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.0.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

from copy import deepcopy

import pytest
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_storage_volume
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from mock import MagicMock

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
INVALID_VALUE_MSG = "The value for the `{parameter}` parameter are invalid."
ID_AND_LOCATION_BOTH_DEFINED = "Either id or location is allowed."
ID_AND_LOCATION_BOTH_NOT_DEFINED = "Either id or location should be specified."
DRIVES_NOT_DEFINED = "Drives must be defined for volume creation."
NOT_ENOUGH_DRIVES = "Number of sufficient disks not found in Controller '{controller_id}'!"
WAIT_TIMEOUT_MSG = "The job is not complete after {0} seconds."
ODATA_ID = "@odata.id"
ODATA_REGEX = "(.*?)@odata"
ATTRIBUTE = "</Attribute>"
VIEW_OPERATION_FAILED = "Failed to fetch storage details."
VIEW_CONTROLLER_DETAILS_NOT_FOUND = "Failed to find the controller {controller_id}."
VIEW_OPERATION_CONTROLLER_NOT_SPECIFIED = "Controller identifier parameter is missing."
VIEW_VIRTUAL_DISK_DETAILS_NOT_FOUND = "Failed to find the volume : {volume_id} in controller : {controller_id}."
SUCCESS_STATUS = "Success"
FAILED_STATUS = "Failed"

REDFISH = "/redfish/v1"
API_INVOKE_MOCKER = "iDRACRedfishAPI.invoke_request"


class TestStorageData(FakeAnsibleModule):
    module = idrac_storage_volume
    storage_controllers = {
        "@odata.id": "/redfish/v1/Systems/System.Embedded.1/Storage"
    }
    volumes_list = [
        {
            "@odata.id": "/redfish/v1/Systems/System.Embedded.1/Storage/RAID.SL.5-1/Volumes/Disk.Virtual.0:RAID.SL.5-1"
        },
        {
            "@odata.id": "/redfish/v1/Systems/System.Embedded.1/Storage/RAID.SL.5-1/Volumes/Disk.Virtual.1:RAID.SL.5-1"
        }]
    controllers_list = {
        "Members": [
            {
                "Controllers": {
                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1/Storage/RAID.SL.5-1/Controllers"
                },
                "Drives": [
                    {
                        "@odata.id": "/redfish/v1/Systems/System.Embedded.1/Storage/RAID.SL.5-1/Drives/Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1"
                    }
                ],
                "Id": "RAID.SL.5-1",
                "Links": {
                    "Enclosures": [
                        {
                            "@odata.id": "/redfish/v1/Chassis/Enclosure.Internal.0-1:RAID.SL.5-1"
                        },
                        {
                            "@odata.id": "/redfish/v1/Chassis/System.Embedded.1"
                        }
                    ]
                },
                "Volumes": {
                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1/Storage/RAID.SL.5-1/Volumes"
                },
                "Oem": {
                    "Dell": {
                        "DellControllerBattery": {
                            "Id": "Battery.Integrated.1:RAID.SL.5-1"
                        }}
                }
            },
            {
                "Drives": [
                    {
                        "@odata.id": "/redfish/v1/Systems/System.Embedded.1/Storage/CPU.1/Drives/Disk.Bay.23:Enclosure.Internal.0-3"
                    }
                ],
                "Drives@odata.count": 1,
                "Id": "CPU.1",
                "Links": {
                    "Enclosures": [
                        {
                            "@odata.id": "/redfish/v1/Chassis/Enclosure.Internal.0-3"
                        },
                        {
                            "@odata.id": "/redfish/v1/Chassis/System.Embedded.1"
                        }
                    ],
                },
                "Volumes": {
                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1/Storage/CPU.1/Volumes"
                }
            },
            {
                "Controllers": {
                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1/Storage/AHCI.Embedded.1-1/Controllers"
                },
                "Drives": [],
                "Id": "AHCI.Embedded.1-1",
                "Links": {
                    "Enclosures": [
                        {
                            "@odata.id": "/redfish/v1/Chassis/System.Embedded.1"
                        }
                    ]
                },
                "Volumes": {
                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1/Storage/AHCI.Embedded.1-1/Volumes"
                }
            }
        ]
    }

    storage_data = {
        'Controllers': {
            'AHCI.Embedded.1-1': {
                'Controllers': {
                    '@odata.id': '/redfish/v1/Systems/System.Embedded.1/Storage/AHCI.Embedded.1-1/Controllers',
                },
                'Drives': {},
                'Id': 'AHCI.Embedded.1-1',
                'Links': {
                    'Enclosures': {
                        'System.Embedded.1': "/redfish/v1/Chassis/System.Embedded.1",
                    },
                },
                'Volumes': {},
                "Oem": {
                    "Dell": {
                        "@odata.type": "#DellOem.v1_3_0.DellOemLinks",
                        "CPUAffinity": [],
                        "CPUAffinity@odata.count": 0
                    }
                }
            },
            'AHCI.Embedded.1-2': {
                'Controllers': {
                    '@odata.id': '/redfish/v1/Systems/System.Embedded.1/Storage/AHCI.Embedded.1-2/Controllers',
                },
                'Drives': {
                    'Disk.Bay.0:Enclosure.Internal.0-1:AHCI.Embedded.1-2': '/redfish/v1/\
                    Systems/System.Embedded.1/Storage/RAID.SL.5-1/Drives/Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1',
                },
                'Id': 'AHCI.Embedded.1-2',
                'Links': {
                    'Enclosures': {
                        'System.Embedded.1': "/redfish/v1/Chassis/System.Embedded.1",
                    },
                },
                'Volumes': {},
                "Oem": {
                    "Dell": {
                        "@odata.type": "#DellOem.v1_3_0.DellOemLinks",
                        "CPUAffinity": [],
                        "CPUAffinity@odata.count": 0
                    }
                }
            },
            'AHCI.Embedded.1-3': {
                'Controllers': {
                    '@odata.id': '/redfish/v1/Systems/System.Embedded.1/Storage/AHCI.Embedded.1-2/Controllers',
                },
                'Drives': {
                    'Disk.Bay.0:Enclosure.Internal.0-1:AHCI.Embedded.1-3': '/redfish/v1/\
                    Systems/System.Embedded.1/Storage/AHCI.Embedded.1-3/Drives/Disk.Bay.0:Enclosure.Internal.0-1:AHCI.Embedded.1-3',
                },
                'Id': 'AHCI.Embedded.1-3',
                'Links': {
                    'Enclosures': {
                        'Enclosure.Internal.0-1:RAID.SL.5-1': {
                            "Links": {
                                "Drives": []
                            },
                            'System.Embedded.1': "/redfish/v1/Chassis/System.Embedded.1"
                        },
                    },
                },
                'Volumes': {},
                "Oem": {
                    "Dell": {
                        "@odata.type": "#DellOem.v1_3_0.DellOemLinks",
                        "CPUAffinity": [],
                        "CPUAffinity@odata.count": 0
                    }
                }
            },
            'RAID.SL.5-1': {
                'Controllers': {
                    '@odata.id': '/redfish/v1/Systems/System.Embedded.1/Storage/RAID.SL.5-1/Controllers',
                },
                'Drives': {
                    'Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1': '/redfish/v1/Systems\
                        /System.Embedded.1/Storage/RAID.SL.5-1/Drives/Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1',
                },
                'Id': 'RAID.SL.5-1',
                'Links': {
                    'Enclosures': {
                        'Enclosure.Internal.0-1:RAID.SL.5-1': {"Links": {
                            "Drives": [
                                {
                                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1\
                                        /Storage/RAID.SL.5-1/Drives/Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1"
                                }
                            ]}},
                        'System.Embedded.1': "/redfish/v1/Chassis/System.Embedded.1",
                    },
                },
                'Volumes': {
                    'Disk.Virtual.0:RAID.SL.5-1': {
                        "Links": {
                            "Drives": [
                                {
                                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1\
                                        /Storage/RAID.SL.5-1/Drives/Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1"
                                }
                            ]
                        },
                    },
                    'Disk.Virtual.1:RAID.SL.5-1': {
                        "Links": {
                            "Drives": [
                                {
                                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1\
                                        /Storage/RAID.SL.5-1/Drives/Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1"
                                }
                            ]
                        },
                    },
                },
                "Oem": {
                    "Dell": {
                        "DellControllerBattery": {
                            "Id": "Battery.Integrated.1:RAID.SL.5-1"
                        }}
                }
            }
        }
    }

    storage_data_expected = {
        'Controller': {
            'AHCI.Embedded.1-1': {
                'ControllerSensor': {
                    'AHCI.Embedded.1-1': {},
                },
            },
            'AHCI.Embedded.1-2': {
                'ControllerSensor': {
                    'AHCI.Embedded.1-2': {},
                },
                'PhysicalDisk': [
                    'Disk.Bay.0:Enclosure.Internal.0-1:AHCI.Embedded.1-2',
                ],
            },
            'AHCI.Embedded.1-3': {
                'ControllerSensor': {
                    'AHCI.Embedded.1-3': {}
                },
                'Enclosure': {
                    'Enclosure.Internal.0-1:RAID.SL.5-1': {
                        'EnclosureSensor': {
                            'Enclosure.Internal.0-1:RAID.SL.5-1': {},
                        },
                    },
                },
            },
            'RAID.SL.5-1': {
                'ControllerSensor': {
                    'RAID.SL.5-1': {
                        'ControllerBattery': [
                            'Battery.Integrated.1:RAID.SL.5-1',
                        ],
                    },
                },
                'Enclosure': {
                    'Enclosure.Internal.0-1:RAID.SL.5-1': {
                        'EnclosureSensor': {
                            'Enclosure.Internal.0-1:RAID.SL.5-1': {},
                        },
                        'PhysicalDisk': [
                            'Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1',
                        ],
                    },
                },
                'VirtualDisk': {
                    'Disk.Virtual.0:RAID.SL.5-1': {
                        'PhysicalDisk': [
                            'Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1',
                        ],
                    },
                    'Disk.Virtual.1:RAID.SL.5-1': {
                        'PhysicalDisk': [
                            'Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1',
                        ],
                    },
                },
            },
        }
    }

    storage_data_idrac8 = {
        'Controllers': {
            'RAID.SL.5-1': {
                'Controllers': {
                    '@odata.id': '/redfish/v1/Systems/System.Embedded.1/Storage/RAID.SL.5-1/Controllers',
                },
                'Drives': {
                    'Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1': '/redfish/v1/Systems\
                        /System.Embedded.1/Storage/RAID.SL.5-1/Drives/Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1',
                },
                'Id': 'RAID.SL.5-1',
                'Links': {
                    'Enclosures': {
                        'Enclosure.Internal.0-1:RAID.SL.5-1': {"Links": {
                            "Drives": [
                                {
                                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1\
                                        /Storage/RAID.SL.5-1/Drives/Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1"
                                }
                            ]}},
                        'System.Embedded.1': "/redfish/v1/Chassis/System.Embedded.1",
                    },
                },
                'Volumes': {
                    'Disk.Virtual.0:RAID.SL.5-1': {
                        "Links": {
                            "Drives": [
                                {
                                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1\
                                        /Storage/RAID.SL.5-1/Drives/Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1"
                                }
                            ]
                        },
                    },
                    'Disk.Virtual.1:RAID.SL.5-1': {
                        "Links": {
                            "Drives": [
                                {
                                    "@odata.id": "/redfish/v1/Systems/System.Embedded.1\
                                        /Storage/RAID.SL.5-1/Drives/Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1"
                                }
                            ]
                        },
                    },
                },
                "Oem": {
                    "Dell": {
                        "DellControllerBattery": {
                            "Id": "Battery.Integrated.1:RAID.SL.5-1"
                        }}
                }
            }
        }
    }

    storage_data_expected_idrac8 = {
        'Controller': {
            'RAID.SL.5-1': {
                'ControllerSensor': {
                    'RAID.SL.5-1': {},
                },
                'Enclosure': {
                    'Enclosure.Internal.0-1:RAID.SL.5-1': {
                        'EnclosureSensor': {
                            'Enclosure.Internal.0-1:RAID.SL.5-1': {},
                        },
                        'PhysicalDisk': [
                            'Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1',
                        ],
                    },
                },
                'VirtualDisk': {
                    'Disk.Virtual.0:RAID.SL.5-1': {
                        'PhysicalDisk': [
                            'Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1',
                        ],
                    },
                    'Disk.Virtual.1:RAID.SL.5-1': {
                        'PhysicalDisk': [
                            'Disk.Bay.0:Enclosure.Internal.0-1:RAID.SL.5-1',
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
                     return_value=('System.Embedded.1', ''))
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
        key_out, uri_data_out = idr_obj.fetch_api_data(self.storage_controllers["@odata.id"], -1)
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
        assert set(storage_info["Controllers"].keys()) == {'AHCI.Embedded.1-1', 'RAID.SL.5-1'}

    def test_fetch_storage_data(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        mocker.patch(MODULE_PATH + "StorageData.all_storage_data",
                     return_value=self.storage_data)
        mocker.patch(MODULE_PATH + "get_idrac_firmware_version",
                     return_value="3.00")
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        idr_obj = self.module.StorageData(idrac_connection_storage_volume_mock, f_module)
        storage_info = idr_obj.fetch_storage_data()
        assert storage_info == self.storage_data_expected

        # Scenario - for idrac 8
        mocker.patch(MODULE_PATH + "StorageData.all_storage_data",
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
        mocker.patch(MODULE_PATH + "StorageData.fetch_storage_data",
                     return_value=TestStorageData.storage_data_expected)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        idr_obj = self.module.StorageView(idrac_connection_storage_volume_mock, f_module)
        out = idr_obj.execute()
        assert out == {"Message": TestStorageData.storage_data_expected, "Status": SUCCESS_STATUS}

        # Scenario - When controller_id is passed
        data_when_controller_id_passed = deepcopy(TestStorageData.storage_data_expected)
        mocker.patch(MODULE_PATH + "StorageData.fetch_storage_data",
                     return_value=data_when_controller_id_passed)
        idrac_default_args.update({"controller_id": "AHCI.Embedded.1-1"})
        out = idr_obj.execute()
        assert out == {"Message": data_when_controller_id_passed, "Status": SUCCESS_STATUS}

        # Scenario - When invalid controller_id is passed
        data_when_invlid_controller_id_passed = deepcopy(TestStorageData.storage_data_expected)
        mocker.patch(MODULE_PATH + "StorageData.fetch_storage_data",
                     return_value=data_when_invlid_controller_id_passed)
        controller_id = "AHCI.Embedded.1-invalid"
        idrac_default_args.update({"controller_id": controller_id})
        with pytest.raises(Exception) as exc:
            idr_obj.execute()
        assert exc.value.args[0] == VIEW_OPERATION_FAILED

        # Scenario - When volume_id and invalid controller_id is passed
        data_when_invlid_volume_id_passed = deepcopy(TestStorageData.storage_data_expected)
        mocker.patch(MODULE_PATH + "StorageData.fetch_storage_data",
                     return_value=data_when_invlid_volume_id_passed)
        idrac_default_args.update({"volume_id": "Disk.Virtual.0:RAID.SL.5-1"})
        with pytest.raises(Exception) as exc:
            idr_obj.execute()
        assert exc.value.args[0] == VIEW_OPERATION_FAILED
        # VIEW_CONTROLLER_DETAILS_NOT_FOUND.format(controller_id=controller_id)

        # Scenario - When volume_id and valid controller_id is passed
        data_when_controller_id_and_volume_id_passed = deepcopy(TestStorageData.storage_data_expected)
        mocker.patch(MODULE_PATH + "StorageData.fetch_storage_data",
                     return_value=data_when_controller_id_and_volume_id_passed)
        idrac_default_args.update({"controller_id": "RAID.SL.5-1", "volume_id": "Disk.Virtual.0:RAID.SL.5-1"})
        out = idr_obj.execute()
        assert out == {"Message": data_when_controller_id_and_volume_id_passed, "Status": SUCCESS_STATUS}

        # Scenario - When invalid volume_id and valid controller_id is passed
        data_when_controller_id_and_volume_id_passed = deepcopy(TestStorageData.storage_data_expected)
        mocker.patch(MODULE_PATH + "StorageData.fetch_storage_data",
                     return_value=data_when_controller_id_and_volume_id_passed)
        idrac_default_args.update({"controller_id": "AHCI.Embedded.1-1", "volume_id": "Disk.Virtual.0:RAID.SL.5-1"})
        with pytest.raises(Exception) as exc:
            idr_obj.execute()
        assert exc.value.args[0] == VIEW_OPERATION_FAILED

        # Scenario - When volume_id is passed
        data_when_volume_id_passed = deepcopy(TestStorageData.storage_data_expected)
        mocker.patch(MODULE_PATH + "StorageData.fetch_storage_data",
                     return_value=data_when_volume_id_passed)
        del idrac_default_args["controller_id"]
        idrac_default_args.update({"volume_id": "Disk.Virtual.0:RAID.SL.5-1"})
        with pytest.raises(Exception) as exc:
            idr_obj.execute()
        assert exc.value.args[0] == VIEW_OPERATION_FAILED


class TestStorageBase:
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


class TestStorageValidation(FakeAnsibleModule, TestStorageBase):
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
        mocker.patch(MODULE_PATH + "StorageData.all_storage_data",
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
        controller_id = "AHCI.Embedded.1-1"
        idrac_default_args.update({"controller_id": controller_id})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.StorageValidation(idrac_connection_storage_volume_mock, f_module)
        idr_obj.validate_controller_exists()

    def test_validate_job_wait_negative_values(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        # Scenario - when job_wait_timeout is negative
        mocker.patch(MODULE_PATH + "StorageData.all_storage_data",
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

    @pytest.mark.parametrize("params", [
        {"span_depth": -1, "span_length": 2, "capacity": 200, "strip_size": 131072},
        {"span_depth": 1, "span_length": -1, "capacity": 200, "strip_size": 131072},
        {"span_depth": 1, "span_length": 2, "capacity": -1, "strip_size": 131072},
        {"span_depth": 1, "span_length": 2, "capacity": 200, "strip_size": -131072},
    ])
    def test_validate_negative_values_for_volume_params(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker, params):
        # Scenario - when job_wait_timeout is negative
        mocker.patch(MODULE_PATH + "StorageData.all_storage_data",
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
        mocker.patch(MODULE_PATH + "StorageData.all_storage_data",
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
        mocker.patch(MODULE_PATH + "StorageData.all_storage_data",
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
                    "Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1",
                    "Disk.Bay.2:Enclosure.Internal.0-1:RAID.Slot.1-1"
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
                "Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1": {}
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
                    "Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1",
                    "Disk.Bay.2:Enclosure.Internal.0-1:RAID.Slot.1-1"
                ]
            }
        }
        mocker.patch(MODULE_PATH + "StorageValidation.raid_std_validation",
                     return_value=True)
        out = idr_obj.validate_volume_drives(volumes)
        assert out is True

    # @pytest.mark.parametrize("params", [
    #     {"span_depth": 4, "span_length": 1, "pd_count": 3, "volume_type": "RAID 1"},
    #     # {"span_depth": 1, "span_length": 2, "pd_count": -1, "volume_type": 131072},
    #     # {"span_depth": 1, "span_length": 2, "pd_count": 200, "volume_type": -131072},
    # ])
    def test_raid_std_validation(self, idrac_default_args, idrac_connection_storage_volume_mock, mocker):
        mocker.patch(MODULE_PATH + "StorageData.all_storage_data",
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
        params = {"span_depth": 6, "span_length": 2, "pd_count": 9, "volume_type": "RAID 10"}
        with pytest.raises(Exception) as exc:
            idr_obj.raid_std_validation(params["span_length"],
                                        params["span_depth"],
                                        params["volume_type"],
                                        params["pd_count"])
        assert exc.value.args[0] == INVALID_VALUE_MSG.format(parameter="span_depth")

        # Scenario - Invalid drive count
        params = {"span_depth": 1, "span_length": 2, "pd_count": 1, "volume_type": "RAID 10"}
        with pytest.raises(Exception) as exc:
            idr_obj.raid_std_validation(params["span_length"],
                                        params["span_depth"],
                                        params["volume_type"],
                                        params["pd_count"])
        assert exc.value.args[0] == INVALID_VALUE_MSG.format(parameter="drives")

        # Scenario - Valid
        params = {"span_depth": 1, "span_length": 2, "pd_count": 2, "volume_type": "RAID 10"}
        out = idr_obj.raid_std_validation(params["span_length"],
                                          params["span_depth"],
                                          params["volume_type"],
                                          params["pd_count"])
        assert out is True
