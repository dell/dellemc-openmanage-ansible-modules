# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.2.0
# Copyright (C) 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
import random
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_network_attributes
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from mock import MagicMock
from ansible.module_utils._text import to_text
from io import StringIO

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'

SUCCESS_MSG = "Successfully updated the network attributes."
SUCCESS_CLEAR_PENDING_ATTR_MSG = "Successfully cleared the pending network attributes."
SCHEDULE_MSG = "Successfully scheduled the job for network attributes update."
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The value for the `job_wait_timeout` parameter cannot be negative or zero."
MAINTENACE_OFFSET_DIFF_MSG = "The maintenance time must be post-fixed with local offset to {0}."
MAINTENACE_OFFSET_BEHIND_MSG = "The specified maintenance time window occurs in the past, provide a future time to schedule the maintenance window."
APPLY_TIME_NOT_SUPPORTED_MSG = "Apply time {0} is not supported."
INVALID_ATTR_MSG = "Unable to update the network attributes because invalid values are entered." + \
    "Enter the valid values for the network attributes and retry the operation."
VALID_AND_INVALID_ATTR_MSG = "Successfully updated the network attributes for valid values." + \
    "Unable to update other attributes because invalid values are entered. Enter the valid values and retry the operation."
NO_CHANGES_FOUND_MSG = "No changes found to be applied."
CHANGES_FOUND_MSG = "Changes found to be applied."
INVALID_ID_MSG = "Unable to complete the operation because the value `{0}` for the input  `{1}` parameter is invalid."
JOB_RUNNING_CLEAR_PENDING_ATTR = "{0} Config job is running. Wait for the job to complete. Currently can not clear pending attributes."


class TestIDRACNetworkAttributes(FakeAnsibleModule):
    module = idrac_network_attributes
    uri = '/redfish/v1/api'

    @pytest.fixture
    def idrac_ntwrk_attr_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_ntwrk_attr_mock(self, mocker, idrac_ntwrk_attr_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'idrac_network_attributes.iDRACRedfishAPI',
                                       return_value=idrac_ntwrk_attr_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_ntwrk_attr_mock
        return idrac_conn_mock

    def test_idrac_firmware_version(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                                    idrac_ntwrk_attr_mock, mocker):
        resp = MagicMock()
        resp.json_data = {'@odata.id': '/some/odata/value',
                          'FirmwareVersion': '1.2.3.4'}
        mocker.patch(MODULE_PATH + "idrac_network_attributes.iDRACRedfishAPI.invoke_request",
                     return_value=resp)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        ver = idr_obj._IDRACNetworkAttributes__get_idrac_firmware_version()
        assert ver == '1.2.3.4'

    def test_resource_id(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                         idrac_ntwrk_attr_mock, mocker):
        resource_id_list = [
            {
                "@odata.id": "/redfish/v1/Chassis/System.Embedded.1"
            },
            {
                "@odata.id": "/redfish/v1/Chassis/Chassis.Embedded.1"
            },
            {
                "@odata.id": "/redfish/v1/Chassis/Enclosure.Internal.0-0:RAID.Integrated.1-1"
            },
            {
                "@odata.id": "/redfish/v1/Chassis/Enclosure.Modular.4:NonRAID.Mezzanine.1C-1"
            },
            {
                "@odata.id": "/redfish/v1/Chassis/Enclosure.Internal.0-0"
            }
        ]
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_dynamic_uri",
                     return_value=resource_id_list)
        idrac_default_args.update({'network_adapter_id': 'NIC.Mezzanine.1A',
                                   'network_device_function_id': 'NIC.Mezzanine.1A-1-1',
                                   'apply_time': 'Immediate'})
        # Scenario-1: Default resource_id, Expectation: should pick first uri from list
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        sys_id = idr_obj._IDRACNetworkAttributes__get_resource_id()
        assert sys_id == "/redfish/v1/Chassis/System.Embedded.1"

        # Scenario-2: Provide resource_id which is in list, Expectation: should pick uri from list
        idrac_default_args.update({'resource_id': 'Enclosure.Internal.0-0'})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        sys_id = idr_obj._IDRACNetworkAttributes__get_resource_id()
        assert sys_id == "/redfish/v1/Chassis/Enclosure.Internal.0-0"

        # Scenario-3: Provide invalid resource_id which is not in list, Expectation: Throw valid error msg
        idrac_default_args.update({'resource_id': 'abcdef'})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj._IDRACNetworkAttributes__get_resource_id()
        assert exc.value.args[0] == INVALID_ID_MSG.format(
            'abcdef', 'resource_id')

    def test_get_registry_fw_less_than_6_more_than_3(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                                                     idrac_ntwrk_attr_mock, mocker):
        registry_list = [
            {
                "@odata.id": "/redfish/v1/Registries/BaseMessages"
            },
            {
                "@odata.id": "/redfish/v1/Registries/NetworkAttributesRegistry_NIC.Mezzanine.1A-1-1"
            }]
        location = [{'Uri': self.uri}]
        registry_response = {'Attributes': [{
                                            "AttributeName": "DeviceName",
                                            "CurrentValue": None
                                            },
                                            {"AttributeName": "ChipMdl",
                                                "CurrentValue": None
                                             }
                                            ]}
        # Scenario 1: Got the registry Members list, Got Location, Got Attributes

        def mock_get_dynamic_uri_request(*args, **kwargs):
            if args[2] == 'Members':
                return registry_list
            elif args[2] == 'Location':
                return location
            else:
                return registry_response

        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)
        idrac_default_args.update({'network_adapter_id': 'NIC.Mezzanine.1A',
                                   'network_device_function_id': 'NIC.Mezzanine.1A-1-1',
                                   'apply_time': 'Immediate'})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        data = idr_obj._IDRACNetworkAttributes__get_registry_fw_less_than_6_more_than_3()
        assert data == {'ChipMdl': None, 'DeviceName': None}

        # Scenario 2: Got the regisry Members empty
        def mock_get_dynamic_uri_request(*args, **kwargs):
            if args[2] == 'Members':
                return {}
            elif args[2] == 'Location':
                return location
            else:
                return registry_response

        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)
        idrac_default_args.update({'network_adapter_id': 'NIC.Mezzanine.1A',
                                   'network_device_function_id': 'NIC.Mezzanine.1A-1-1',
                                   'apply_time': 'Immediate'})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        data = idr_obj._IDRACNetworkAttributes__get_registry_fw_less_than_6_more_than_3()
        assert data == {}

        # Scenario 3: Got the regisry Member but does not contain Location
        def mock_get_dynamic_uri_request(*args, **kwargs):
            if args[2] == 'Members':
                return registry_list
            elif args[2] == 'Location':
                return {}
            else:
                return registry_response

        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)
        idrac_default_args.update({'network_adapter_id': 'NIC.Mezzanine.1A',
                                   'network_device_function_id': 'NIC.Mezzanine.1A-1-1',
                                   'apply_time': 'Immediate'})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        data = idr_obj._IDRACNetworkAttributes__get_registry_fw_less_than_6_more_than_3()
        assert data == {}

    def test_validate_time(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                           idrac_ntwrk_attr_mock, mocker):
        resp = ("2022-09-14T05:59:35-05:00", "-05:00")
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_current_time",
                     return_value=resp)
        idrac_default_args.update({'network_adapter_id': 'NIC.Mezzanine.1A',
                                   'network_device_function_id': 'NIC.Mezzanine.1A-1-1',
                                   'apply_time': 'Immediate'})
        # Scenario 1: When mtime does not end with offset
        m_time = "2022-09-14T05:59:35+05:00"
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj._IDRACNetworkAttributes__validate_time(m_time)
        assert exc.value.args[0] == MAINTENACE_OFFSET_DIFF_MSG.format(resp[1])

        # Scenario 2: When mtime is less than current time
        m_time = "2021-09-14T05:59:35-05:00"
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj._IDRACNetworkAttributes__validate_time(m_time)
        assert exc.value.args[0] == MAINTENACE_OFFSET_BEHIND_MSG

        # Scenario 2: When mtime is greater than current time
        m_time = "2024-09-14T05:59:35-05:00"
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        data = idr_obj._IDRACNetworkAttributes__validate_time(m_time)
        assert data is None

    def test_get_redfish_apply_time(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                                    idrac_ntwrk_attr_mock, mocker):
        resp = ("2022-09-14T05:59:35-05:00", "-05:00")
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes._IDRACNetworkAttributes__validate_time",
                     return_value=resp)
        rf_settings = [
            "OnReset",
            "Immediate"
        ]
        idrac_default_args.update({'network_adapter_id': 'NIC.Mezzanine.1A',
                                   'network_device_function_id': 'NIC.Mezzanine.1A-1-1',
                                   'apply_time': 'AtMaintenanceWindowStart',
                                   'maintenance_window': {"start_time": "2022-09-14T06:59:35-05:00",
                                                          "duration": 600}})

        # Scenario 1: When Maintenance is not supported but 'AtMaintenanceWindowStart' is passed
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj._IDRACNetworkAttributes__get_redfish_apply_time(
                'AtMaintenanceWindowStart', rf_settings)
        assert exc.value.args[0] == APPLY_TIME_NOT_SUPPORTED_MSG.format(
            'AtMaintenanceWindowStart')

        # Scenario 2: When Maintenance is not supported but 'InMaintenanceWindowOnReset' is passed
        idrac_default_args.update({'apply_time': 'InMaintenanceWindowOnReset'})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj._IDRACNetworkAttributes__get_redfish_apply_time(
                'InMaintenanceWindowOnReset', rf_settings)
        assert exc.value.args[0] == APPLY_TIME_NOT_SUPPORTED_MSG.format(
            'InMaintenanceWindowOnReset')

        # Scenario 3: When ApplyTime does not support Maintenance
        rf_settings.append('InMaintenanceWindowOnReset')
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        data = idr_obj._IDRACNetworkAttributes__get_redfish_apply_time(
            'InMaintenanceWindowOnReset', rf_settings)
        assert data == ({'ApplyTime': 'InMaintenanceWindowOnReset',
                         'MaintenanceWindowDurationInSeconds': 600,
                         'MaintenanceWindowStartTime': '2022-09-14T06:59:35-05:00'},
                        False)

        # Scenario 4: When ApplyTime is Immediate
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        data = idr_obj._IDRACNetworkAttributes__get_redfish_apply_time(
            'Immediate', rf_settings)
        assert data == ({'ApplyTime': 'Immediate'}, False)

        # Scenario 5: When ApplyTime does not support Immediate
        rf_settings.remove('Immediate')
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        data = idr_obj._IDRACNetworkAttributes__get_redfish_apply_time(
            'Immediate', rf_settings)
        assert data == ({'ApplyTime': 'OnReset'}, True)

        # Scenario 6: When AppyTime is empty
        rf_settings = []
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        data = idr_obj._IDRACNetworkAttributes__get_redfish_apply_time(
            'Immediate', rf_settings)
        assert data == ({}, False)

    def test_current_server_registry(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                                     idrac_ntwrk_attr_mock, mocker):
        links = {
            "PhysicalPortAssignment": {
                "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A/NetworkPorts/NIC.Mezzanine.1A-1"
            },
            "Oem": {
                "Dell": {
                    "@odata.type": "#DellOem.v1_3_0.DellOemLinks",
                    "DellNetworkAttributes": {
                        "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A/" +
                                     "NetworkDeviceFunctions/NIC.Mezzanine.1A-1-1/Oem/Dell/DellNetworkAttributes/NIC.Mezzanine.1A-1-1"
                    },
                    "CPUAffinity": [],
                    "CPUAffinity@odata.count": 0
                }
            }
        }
        reg_greater_than_6 = {'Attributes': {'abc': False}}
        reg_less_than_6 = {'xyz': True}

        def mock_get_dynamic_uri_request(*args, **kwargs):
            if len(args) > 2 and args[2] == 'Links':
                return links
            return reg_greater_than_6
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes._IDRACNetworkAttributes__get_registry_fw_less_than_6_more_than_3",
                     return_value=reg_less_than_6)
        idrac_default_args.update({'network_adapter_id': 'NIC.Mezzanine.1A',
                                   'network_device_function_id': 'NIC.Mezzanine.1A-1-1',
                                   'apply_time': 'AtMaintenanceWindowStart',
                                   'maintenance_window': {"start_time": "2022-09-14T06:59:35-05:00",
                                                          "duration": 600}})

        # Scenario 1: When Firmware version is greater and equal to 6.0 and oem_network_attributes is not given
        firm_ver = '6.1'
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes._IDRACNetworkAttributes__get_idrac_firmware_version",
                     return_value=firm_ver)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        data = idr_obj.get_current_server_registry()
        assert data == {}

        # Scenario 2: When Firmware version is greater and equal to 6.0 and oem_network_attributes is given
        firm_ver = '6.1'
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes._IDRACNetworkAttributes__get_idrac_firmware_version",
                     return_value=firm_ver)
        idrac_default_args.update({'oem_network_attributes': 'some value'})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        data = idr_obj.get_current_server_registry()
        assert data == {'abc': False}

        # Scenario 3: When Firmware version is less than 6.0 and oem_network_attributes is given
        firm_ver = '4.0'
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes._IDRACNetworkAttributes__get_idrac_firmware_version",
                     return_value=firm_ver)
        idrac_default_args.update({'oem_network_attributes': 'some value'})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        data = idr_obj.get_current_server_registry()
        assert data == {'xyz': True}

    def test_extract_error_info(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                                idrac_ntwrk_attr_mock, mocker):
        error_info = {
            "error": {
                "@Message.ExtendedInfo": [
                    {
                        "Message": "AttributeValue cannot be changed to read only AttributeName BusDeviceFunction.",
                        "MessageArgs": [
                            "BusDeviceFunction"
                        ]
                    },
                    {
                        "Message": "AttributeValue cannot be changed to read only AttributeName ChipMdl.",
                        "MessageArgs": [
                            "ChipMdl"
                        ]
                    },
                    {
                        "Message": "AttributeValue cannot be changed to read only AttributeName ControllerBIOSVersion.",
                        "MessageArgs": [
                            "ControllerBIOSVersion"
                        ]
                    },
                    {
                        "Message": "some random message",
                        "MessageArgs": [
                            "ControllerBIOSVersion"
                        ]
                    }]}}
        obj = MagicMock()
        obj.json_data = error_info
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        data = idr_obj.extract_error_msg(obj)
        assert data == {'BusDeviceFunction': 'AttributeValue cannot be changed to read only AttributeName BusDeviceFunction.',
                        'ChipMdl': 'AttributeValue cannot be changed to read only AttributeName ChipMdl.',
                        'ControllerBIOSVersion': 'AttributeValue cannot be changed to read only AttributeName ControllerBIOSVersion.'
                        }

    def test_get_diff_between_current_and_module_input(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                                                       idrac_ntwrk_attr_mock, mocker):
        module_attr = {'a': 123, 'b': 456}
        server_attr = {'c': 789, 'b': 456}
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        data = idr_obj.get_diff_between_current_and_module_input(
            module_attr, server_attr)
        assert data == (({'a': 123}, {'c': 789}), {
                        'a': 'Attribute does not exist.'})

    def test_perform_validation_for_network_adapter_id(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                                                       idrac_ntwrk_attr_mock, mocker):
        netwkr_adapters = {
            "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters"
        }
        network_adapter_list = [
            {
                "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A"
            },
            {
                "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1B"
            }
        ]

        def mock_get_dynamic_uri_request(*args, **kwargs):
            if args[2] == 'NetworkAdapters':
                return netwkr_adapters
            return network_adapter_list
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes._IDRACNetworkAttributes__get_resource_id",
                     return_value='System.Embedded.1')
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)

        # Scenario 1: When network_adapter_id is in server network adapter list
        idrac_default_args.update({'network_adapter_id': 'NIC.Mezzanine.1B'})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        idr_obj.perform_validation_for_network_adapter_id()
        assert idr_obj.network_adapter_id_uri == "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1B"

        # Scenario 2: When network_adapter_id is not in server network adapter list
        network_adapter_id = 'random value'
        idrac_default_args.update({'network_adapter_id': network_adapter_id})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj.perform_validation_for_network_adapter_id()
        assert exc.value.args[0] == INVALID_ID_MSG.format(
            network_adapter_id, 'network_adapter_id')

    def test_perform_validation_for_network_device_function_id(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                                                               idrac_ntwrk_attr_mock, mocker):
        netwkr_devices = {
            "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A/NetworkDeviceFunctions"
        }
        network_device_function_list = [
            {
                "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A/NetworkDeviceFunctions/NIC.Mezzanine.1A-1-1"
            },
            {
                "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A/NetworkDeviceFunctions/NIC.Mezzanine.1A-2-1"
            }
        ]

        def mock_get_dynamic_uri_request(*args, **kwargs):
            if args[2] == 'NetworkDeviceFunctions':
                return netwkr_devices
            return network_device_function_list
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes._IDRACNetworkAttributes__get_resource_id",
                     return_value='System.Embedded.1')
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)

        # Scenario 1: When network_adapter_id is in server network adapter list
        device_uri = "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A/NetworkDeviceFunctions/NIC.Mezzanine.1A-2-1"
        idrac_default_args.update(
            {'network_device_function_id': 'NIC.Mezzanine.1A-2-1'})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        idr_obj.perform_validation_for_network_device_function_id()
        assert idr_obj.network_device_function_id_uri == device_uri

        # Scenario 2: When network_adapter_id is not in server network adapter list
        network_device_function_id = 'random value'
        idrac_default_args.update(
            {'network_device_function_id': network_device_function_id})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj.perform_validation_for_network_device_function_id()
        assert exc.value.args[0] == INVALID_ID_MSG.format(
            network_device_function_id, 'network_device_function_id')

    def test_validate_job_timeout(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                                  idrac_ntwrk_attr_mock, mocker):

        # Scenario 1: when job_wait is True and job_wait_timeout is in negative
        idrac_default_args.update({'job_wait': True, 'job_wait_timeout': -120})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj.validate_job_timeout()
        assert exc.value.args[0] == TIMEOUT_NEGATIVE_OR_ZERO_MSG

        # Scenario 2: when job_wait is False
        idrac_default_args.update(
            {'job_wait': False, 'job_wait_timeout': -120})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        data = idr_obj.validate_job_timeout()
        assert data is None

    def test_apply_time(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                        idrac_ntwrk_attr_mock, mocker):
        redfish_settings = {
            "SettingsObject": {
                "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A/NetworkDeviceFunctions/NIC.Mezzanine.1A-1-1/" +
                             "Oem/Dell/DellNetworkAttributes/NIC.Mezzanine.1A-1-1/Settings"
            }
        }
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_dynamic_uri",
                     return_value=redfish_settings)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes._IDRACNetworkAttributes__get_redfish_apply_time",
                     return_value=('abc', False))
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        rf_set = idr_obj.apply_time(self.uri)
        assert rf_set == 'abc'

    def test_clear_pending(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                           idrac_ntwrk_attr_mock, mocker):
        links = {
            "PhysicalPortAssignment": {
                "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A/NetworkPorts/NIC.Mezzanine.1A-1"
            },
            "Oem": {
                "Dell": {
                    "@odata.type": "#DellOem.v1_3_0.DellOemLinks",
                    "DellNetworkAttributes": {
                        "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A/NetworkDeviceFunctions/NIC.Mezzanine.1A-1-1/" +
                                     "Oem/Dell/DellNetworkAttributes/NIC.Mezzanine.1A-1-1"
                    },
                    "CPUAffinity": [],
                    "CPUAffinity@odata.count": 0
                }
            }
        }
        redfish_settings = {
            "SettingsObject": {
                "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A/NetworkDeviceFunctions/NIC.Mezzanine.1A-1-1/Oem/Dell/" +
                             "DellNetworkAttributes/NIC.Mezzanine.1A-1-1/Settings"
            }
        }
        action_setting_uri_resp = {
            "Actions": {
                "#DellManager.ClearPending": {
                    "target": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A/NetworkDeviceFunctions/NIC.Mezzanine.1A-1-1/Oem/Dell/" +
                              "DellNetworkAttributes/NIC.Mezzanine.1A-1-1/Settings/Actions/DellManager.ClearPending"
                }
            },
            "Attributes": {}
        }

        def mock_get_dynamic_uri_request(*args, **kwargs):
            if len(args) > 2:
                if args[2] == 'Links':
                    return links
                return redfish_settings
            return action_setting_uri_resp
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)

        # Scenario 1: When there's no pending attributes
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.OEMNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj.clear_pending()
        assert exc.value.args[0] == NO_CHANGES_FOUND_MSG

        # Scenario 2: When there's pending attributes and scheduled_job is running in normal mode
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_scheduled_job_resp",
                     return_value={'Id': 'JIDXXXXXX', 'JobState': 'Running'})
        action_setting_uri_resp.update({'Attributes': {'VLanId': 10}})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.OEMNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj.clear_pending()
        assert exc.value.args[0] == JOB_RUNNING_CLEAR_PENDING_ATTR.format(
            'NICConfiguration')

        # Scenario 3: When there's pending attributes and scheduled_job is Starting in normal mode
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_scheduled_job_resp",
                     return_value={'Id': 'JIDXXXXXX', 'JobState': 'Starting'})
        action_setting_uri_resp.update({'Attributes': {'VLanId': 10}})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.OEMNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj.clear_pending()
        assert exc.value.args[0] == SUCCESS_CLEAR_PENDING_ATTR_MSG

        # Scenario 4: Scenario 3 in check mode
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        idr_obj = self.module.OEMNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj.clear_pending()
        assert exc.value.args[0] == CHANGES_FOUND_MSG

        # Scenario 5: When there's pending attribute but no job id is present in normal mode
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_scheduled_job_resp",
                     return_value={'Id': '', 'JobState': 'Starting'})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.OEMNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj.clear_pending()
        assert exc.value.args[0] == SUCCESS_CLEAR_PENDING_ATTR_MSG

        # Scenario 6: Scenario 5 in check_mode
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        idr_obj = self.module.OEMNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj.clear_pending()
        assert exc.value.args[0] == CHANGES_FOUND_MSG

        # Scenario 7: When Job is completed in check mode, ideally won't get this condition
        #             as function will return only scheduled job
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_scheduled_job_resp",
                     return_value={'Id': 'JIDXXXXXX', 'JobState': 'Completed'})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        idr_obj = self.module.OEMNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj.clear_pending()
        assert exc.value.args[0] == CHANGES_FOUND_MSG

    def test_perform_operation_OEMNetworkAttributes(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                                                    idrac_ntwrk_attr_mock, mocker):
        obj = MagicMock()
        obj.headers = {'Location': self.uri}
        obj.json_data = {'data': 'some value'}
        links = {
            "PhysicalPortAssignment": {
                "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A/NetworkPorts/NIC.Mezzanine.1A-1"
            },
            "Oem": {
                "Dell": {
                    "@odata.type": "#DellOem.v1_3_0.DellOemLinks",
                    "DellNetworkAttributes": {
                        "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A/NetworkDeviceFunctions/NIC.Mezzanine.1A-1-1/Oem/" +
                                     "Dell/DellNetworkAttributes/NIC.Mezzanine.1A-1-1"
                    },
                    "CPUAffinity": [],
                    "CPUAffinity@odata.count": 0
                }
            }
        }
        apply_time = {'ApplyTime': 'Immediate'}
        redfish_settings = {"@Redfish.Settings": {
            "SettingsObject": {
                "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A/NetworkDeviceFunctions/NIC.Mezzanine.1A-1-1/Oem/Dell/" +
                             "DellNetworkAttributes/NIC.Mezzanine.1A-1-1/Settings"
            }
        }
        }
        error_info = {'abc': 'Attribute does not exit.'}

        def mock_get_dynamic_uri_request(*args, **kwargs):
            if len(args) > 2 and args[2] == 'Links':
                return links
            return redfish_settings
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.iDRACRedfishAPI.invoke_request",
                     return_value=obj)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes.apply_time",
                     return_value=apply_time)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes.extract_error_msg",
                     return_value=error_info)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.wait_for_idrac_job_completion",
                     return_value=(obj, False))

        idrac_default_args.update({'oem_network_attributes': {'VlanId': 1},
                                   'job_wait': True,
                                   'job_wait_timout': 1200})
        # Scenario 1: When Job has returned successfully and not error msg is there
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        idr_obj = self.module.OEMNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        data = idr_obj.perform_operation()
        assert data == ({'data': 'some value'}, {
                        'abc': 'Attribute does not exit.'})

        # Scenario 2: When Job has returned error msg
        error_msg = 'No job is found.'
        mocker.patch(MODULE_PATH + "idrac_network_attributes.wait_for_idrac_job_completion",
                     return_value=(obj, error_msg))
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        idr_obj = self.module.OEMNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj.perform_operation()
        assert exc.value.args[0] == error_msg

        # Scenario 2: When apply_time_settings is {} and job is returning error msg
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes.apply_time",
                     return_value={})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        idr_obj = self.module.OEMNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj.perform_operation()
        assert exc.value.args[0] == error_msg

    def test_perform_operation_for_main(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                                        idrac_ntwrk_attr_mock, mocker):
        obj = MagicMock()
        invalid_attr = {'a': 'Attribute does not exist.'}
        # Scenario 1: When diff is false
        diff = ()
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        with pytest.raises(Exception) as exc:
            self.module.perform_operation_for_main(
                f_module, obj, diff, invalid_attr)
        assert exc.value.args[0] == NO_CHANGES_FOUND_MSG

        # Scenario 2: When diff is True and check mode is True
        diff = ({'a': 123}, {'c': 789})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        with pytest.raises(Exception) as exc:
            self.module.perform_operation_for_main(
                f_module, obj, diff, invalid_attr)
        assert exc.value.args[0] == CHANGES_FOUND_MSG

        # Scenario 3: When diff is True and JobState is completed and
        #             There is invalid_attr in normal mode
        def return_data():
            return ({'JobState': "Completed"}, invalid_attr)
        obj.perform_operation = return_data
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        with pytest.raises(Exception) as exc:
            self.module.perform_operation_for_main(
                f_module, obj, diff, invalid_attr)
        assert exc.value.args[0] == VALID_AND_INVALID_ATTR_MSG

        # Scenario 4: When diff is True and JobState is completed and
        #             There is no invalid_attr in normal mode
        invalid_attr = {}
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        with pytest.raises(Exception) as exc:
            self.module.perform_operation_for_main(
                f_module, obj, diff, invalid_attr)
        assert exc.value.args[0] == SUCCESS_MSG

        # Scenario 5: When diff is True and JobState is not completed and
        #             There is no invalid_attr in normal mode
        invalid_attr = {}

        def return_data():
            return ({'JobState': "Starting"}, invalid_attr)
        obj.perform_operation = return_data
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        with pytest.raises(Exception) as exc:
            self.module.perform_operation_for_main(
                f_module, obj, diff, invalid_attr)
        assert exc.value.args[0] == SCHEDULE_MSG

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_idrac_network_attributes_main_exception_handling_case(self, exc_type, mocker, idrac_default_args,
                                                                   idrac_connection_ntwrk_attr_mock, idrac_ntwrk_attr_mock):
        obj = MagicMock()
        obj.perform_validation_for_network_adapter_id.return_value = None
        obj.perform_validation_for_network_device_function_id.return_value = None
        obj.get_diff_between_current_and_module_input.return_value = (
            None, None)
        obj.clear_pending.return_value = None
        idrac_ntwrk_attr_mock.status_code = 400
        idrac_ntwrk_attr_mock.success = False
        idrac_default_args.update({'apply_time': "Immediate",
                                   'network_adapter_id': 'Some_adapter_id',
                                   'network_device_function_id': 'some_device_id',
                                   'clear_pending': random.choice([True, False])})
        mocker.patch(
            MODULE_PATH + "idrac_network_attributes.OEMNetworkAttributes", return_value=obj)
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            tmp = {'oem_network_attributes': {'VlanId': 10}}
            mocker.patch(MODULE_PATH + "idrac_network_attributes.perform_operation_for_main",
                         side_effect=exc_type('test'))
        else:
            tmp = {'network_attributes': {'abc': 10}}
            mocker.patch(MODULE_PATH + "idrac_network_attributes.perform_operation_for_main",
                         side_effect=exc_type('http://testhost.com', 400,
                                              'http error message',
                                              {"accept-type": "application/json"},
                                              StringIO(json_str)))
        idrac_default_args.update(tmp)
        if exc_type != URLError:
            result = self._run_module(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
            assert result['unreachable'] is True
        assert 'msg' in result
