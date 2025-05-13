# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.4.0
# Copyright (C) 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from io import StringIO

import pytest
from ansible.module_utils._text import to_text
from urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import \
    idrac_network_attributes
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import \
    FakeAnsibleModule
from unittest.mock import MagicMock

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'

SUCCESS_MSG = "Successfully updated the network attributes."
SUCCESS_CLEAR_PENDING_ATTR_MSG = "Successfully cleared the pending network attributes."
SCHEDULE_MSG = "Successfully scheduled the job for network attributes update."
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The value for the `job_wait_timeout` parameter cannot be negative or zero."
MAINTENACE_OFFSET_DIFF_MSG = "The maintenance time must be post-fixed with local offset to {0}."
MAINTENACE_OFFSET_BEHIND_MSG = "The specified maintenance time window occurs in the past, provide a future time to schedule the maintenance window."
APPLY_TIME_NOT_SUPPORTED_MSG = "Apply time {0} is not supported."
INVALID_ATTR_MSG = "Unable to update the network attributes because invalid values are entered. " + \
    "Enter the valid values for the network attributes and retry the operation."
VALID_AND_INVALID_ATTR_MSG = "Successfully updated the network attributes for valid values. " + \
    "Unable to update other attributes because invalid values are entered. Enter the valid values and retry the operation."
NO_CHANGES_FOUND_MSG = "No changes found to be applied."
CHANGES_FOUND_MSG = "Changes found to be applied."
INVALID_ID_MSG = "Unable to complete the operation because the value `{0}` for the input `{1}` parameter is invalid."
JOB_RUNNING_CLEAR_PENDING_ATTR = "{0} Config job is running. Wait for the job to complete. Currently can not clear pending attributes."
ATTRIBUTE_NOT_EXIST_CHECK_IDEMPOTENCY_MODE = 'Attribute is not valid.'
CLEAR_PENDING_NOT_SUPPORTED_WITHOUT_ATTR_IDRAC8 = "Clear pending is not supported."
WAIT_TIMEOUT_MSG = "The job is not complete after {0} seconds."
iDRAC_JOB_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/{job_id}"
iDRAC_JOB_URI_10 = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/{job_id}"
HARDWARE_9 = "iDRAC 9"
HARDWARE_8 = "iDRAC 8"
HARDWARE_10 = "iDRAC 10"
GENERATION_13 = 13
GENERATION_14 = 14
GENERATION_15 = 15
GENERATION_17 = 17


class TestIDRACNetworkAttributes(FakeAnsibleModule):
    module = idrac_network_attributes
    uri = '/redfish/v1/api'
    links = {
        "Oem": {
            "Dell": {
                "DellNetworkAttributes": {
                    "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A/NetworkDeviceFunctions/NIC.Mezzanine.1A-1-1/Oem/" +
                    "Dell/DellNetworkAttributes/NIC.Mezzanine.1A-1-1"
                }
            }
        }
    }
    redfish_settings = {"@Redfish.Settings": {
        "SettingsObject": {
            "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A/NetworkDeviceFunctions/NIC.Mezzanine.1A-1-1/Oem/Dell/" +
            "DellNetworkAttributes/NIC.Mezzanine.1A-1-1/Settings"
        }
    }
    }

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
            idrac_connection_ntwrk_attr_mock, f_module)
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
            idrac_connection_ntwrk_attr_mock, f_module)
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
            idrac_connection_ntwrk_attr_mock, f_module)
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
            idrac_connection_ntwrk_attr_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj._IDRACNetworkAttributes__validate_time(m_time)
        assert exc.value.args[0] == MAINTENACE_OFFSET_DIFF_MSG.format(resp[1])

        # Scenario 2: When mtime is less than current time
        m_time = "2021-09-14T05:59:35-05:00"
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj._IDRACNetworkAttributes__validate_time(m_time)
        assert exc.value.args[0] == MAINTENACE_OFFSET_BEHIND_MSG

        # Scenario 2: When mtime is greater than current time
        m_time = "2024-09-14T05:59:35-05:00"
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
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
            idrac_connection_ntwrk_attr_mock, f_module)
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
            idrac_connection_ntwrk_attr_mock, f_module)
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
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj._IDRACNetworkAttributes__get_redfish_apply_time(
            'InMaintenanceWindowOnReset', rf_settings)
        assert data == {'ApplyTime': 'InMaintenanceWindowOnReset',
                        'MaintenanceWindowDurationInSeconds': 600,
                        'MaintenanceWindowStartTime': '2022-09-14T06:59:35-05:00'}

        # Scenario 4: When ApplyTime is Immediate
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj._IDRACNetworkAttributes__get_redfish_apply_time(
            'Immediate', rf_settings)
        assert data == {'ApplyTime': 'Immediate'}

        # Scenario 5: When ApplyTime does not support Immediate
        rf_settings.remove('Immediate')
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj._IDRACNetworkAttributes__get_redfish_apply_time(
                'Immediate', rf_settings)
        assert exc.value.args[0] == APPLY_TIME_NOT_SUPPORTED_MSG.format(
            'Immediate')

        # Scenario 6: When AppyTime is empty
        rf_settings = []
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj._IDRACNetworkAttributes__get_redfish_apply_time(
            'Immediate', rf_settings)
        assert data == {}

    def test_get_registry_fw_less_than_3(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                                         idrac_ntwrk_attr_mock, mocker):
        obj = MagicMock()
        obj.json_data = {'SystemConfiguration': {
            "Components": [
                {'FQDD': 'NIC.Mezzanine.1A-1-1',
                 'Attributes': [{
                     'Name': 'VLanId',
                     'Value': '10'
                 }]}
            ]
        }}
        idrac_default_args.update(
            {'network_device_function_id': 'NIC.Mezzanine.1A-1-1'})
        mocker.patch(MODULE_PATH + "idrac_network_attributes.iDRACRedfishAPI.export_scp",
                     return_value=obj)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj._IDRACNetworkAttributes__get_registry_fw_less_than_3()
        assert data == {'VLanId': '10'}

    def test_get_current_server_registry(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                                         idrac_ntwrk_attr_mock, mocker):
        reg_greater_than_6 = {'abc': False}
        reg_less_than_6 = {'xyz': True}
        reg_less_than_3 = {'Qwerty': False}
        redfish_resp = {'Ethernet': {'abc': 123},
                        'FibreChannel': {},
                        'iSCSIBoot': {'ghi': 789}
                        }

        def mock_get_dynamic_uri_request(*args, **kwargs):
            if len(args) > 2:
                if args[2] == 'Links':
                    return self.links
                elif args[2] == 'Attributes':
                    return reg_greater_than_6
            return redfish_resp
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes._IDRACNetworkAttributes__get_registry_fw_less_than_6_more_than_3",
                     return_value=reg_less_than_6)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes._IDRACNetworkAttributes__get_registry_fw_less_than_3",
                     return_value=reg_less_than_3)
        idrac_default_args.update({'network_adapter_id': 'NIC.Mezzanine.1A',
                                   'network_device_function_id': 'NIC.Mezzanine.1A-1-1',
                                   'apply_time': 'AtMaintenanceWindowStart',
                                   'maintenance_window': {"start_time": "2022-09-14T06:59:35-05:00",
                                                          "duration": 600}})

        # Scenario 1: When Firmware version is greater and equal to 6.0 and oem_network_attributes is not given
        gen = GENERATION_15
        hw_model = HARDWARE_9
        firm_ver = '6.1'
        idrac_connection_ntwrk_attr_mock.get_server_generation = (gen, firm_ver, hw_model)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj.get_current_server_registry()
        assert data == {}

        # Scenario 2: When Firmware version is greater and equal to 6.0 and oem_network_attributes is given
        idrac_default_args.update({'oem_network_attributes': 'some value'})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj.get_current_server_registry()
        assert data == {'abc': False}

        # Scenario 3: When Firmware version is greater and equal to 1.10 and
        # oem_network_attributes is given and model is 17g
        hw_model = HARDWARE_10
        gen = GENERATION_17
        firm_ver = '1.10'
        idrac_connection_ntwrk_attr_mock.get_server_generation = (gen, firm_ver, hw_model)
        idrac_default_args.update({'oem_network_attributes': 'some value'})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj.get_current_server_registry()
        assert data == {'abc': False}

        # Scenario 4: When Firmware version is less than 6.0 and oem_network_attributes is given
        hw_model = HARDWARE_9
        gen = GENERATION_14
        firm_ver = '4.0'
        idrac_connection_ntwrk_attr_mock.get_server_generation = (gen, firm_ver, hw_model)
        idrac_default_args.update({'oem_network_attributes': 'some value'})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj.get_current_server_registry()
        assert data == {'xyz': True}

        # Scenario 5: When Firmware version is less than 3.0 and oem_network_attributes is given
        gen = GENERATION_13
        hw_model = HARDWARE_8
        firm_ver = '2.9'
        idrac_connection_ntwrk_attr_mock.get_server_generation = (gen, firm_ver, hw_model)
        idrac_default_args.update({'oem_network_attributes': 'some value'})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj.get_current_server_registry()
        assert data == {'Qwerty': False}

        # Scenario 6: When network_attributes is given
        gen = GENERATION_15
        hw_model = HARDWARE_9
        firm_ver = '7.0'
        idrac_connection_ntwrk_attr_mock.get_server_generation = (gen, firm_ver, hw_model)
        idrac_default_args.update({'network_attributes': 'some value',
                                   'oem_network_attributes': None})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj.get_current_server_registry()
        assert data == redfish_resp

    def test_extract_error_msg(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
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
        # Scenario 1: When response code is 202 and has response body
        obj.body = obj.json_data = error_info
        obj.status_code = 202
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj.extract_error_msg(obj)
        assert data == {'BusDeviceFunction': 'AttributeValue cannot be changed to read only AttributeName BusDeviceFunction.',
                        'ChipMdl': 'AttributeValue cannot be changed to read only AttributeName ChipMdl.',
                        'ControllerBIOSVersion': 'AttributeValue cannot be changed to read only AttributeName ControllerBIOSVersion.'
                        }

        # Scenario 2: When response code is 200 and no response body
        obj.body = obj.json_data = ''
        obj.status_code = 200
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj.extract_error_msg(obj)
        assert data == {}

    def test_get_diff_between_current_and_module_input(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                                                       idrac_ntwrk_attr_mock, mocker):
        module_attr = {'a': 123, 'b': 456}
        server_attr = {'c': 789, 'b': 456}
        # Scenario 1: Simple attribute which does not contain nested values
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj.get_diff_between_current_and_module_input(
            module_attr, server_attr)
        assert data == (0, {'a': ATTRIBUTE_NOT_EXIST_CHECK_IDEMPOTENCY_MODE})

        # Scenario 2: Complex attribute which contain nested values
        module_attr = {'a': 123, 'b': 456, 'c': {'d': 789}}
        server_attr = {'c': 789, 'b': 457, 'd': {'e': 123}}
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj.get_diff_between_current_and_module_input(
            module_attr, server_attr)
        assert data == (2, {'a': ATTRIBUTE_NOT_EXIST_CHECK_IDEMPOTENCY_MODE})

        # Scenario 3: Complex attribute which contain nested values and value matched
        module_attr = {'a': 123, 'b': 456, 'c': {'d': 789}}
        server_attr = {'c': {'d': 789}, 'b': 457, 'd': {'e': 123}}
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj.get_diff_between_current_and_module_input(
            module_attr, server_attr)
        assert data == (1, {'a': ATTRIBUTE_NOT_EXIST_CHECK_IDEMPOTENCY_MODE})

        # Scenario 3: module attr is None
        module_attr = None
        server_attr = {'a': 123}
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj.get_diff_between_current_and_module_input(
            module_attr, server_attr)
        assert data == (0, {})

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
            if args[2] == 'NetworkInterfaces':
                return netwkr_adapters
            return network_adapter_list
        mocker.patch(MODULE_PATH + "idrac_network_attributes.validate_and_get_first_resource_id_uri",
                     return_value=('System.Embedded.1', ''))
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)

        # Scenario 1: When network_adapter_id is in server network adapter list
        idrac_default_args.update({'network_adapter_id': 'NIC.Mezzanine.1B'})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj._IDRACNetworkAttributes__perform_validation_for_network_adapter_id()
        assert data == "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1B"

        # Scenario 2: When network_adapter_id is not in server network adapter list
        network_adapter_id = 'random value'
        mocker.patch(MODULE_PATH + "idrac_network_attributes.validate_and_get_first_resource_id_uri",
                     return_value=('System.Embedded.1', ''))
        idrac_default_args.update({'network_adapter_id': network_adapter_id})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj._IDRACNetworkAttributes__perform_validation_for_network_adapter_id()
        assert exc.value.args[0] == INVALID_ID_MSG.format(network_adapter_id,
                                                          'network_adapter_id')

        # Scenario 3: When validate_and_get_first_resource_id_uri is returning error_msg
        network_adapter_id = 'random value'
        mocker.patch(MODULE_PATH + "idrac_network_attributes.validate_and_get_first_resource_id_uri",
                     return_value=('System.Embedded.1', 'error_msg'))
        idrac_default_args.update({'network_adapter_id': network_adapter_id})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj._IDRACNetworkAttributes__perform_validation_for_network_adapter_id()
        assert exc.value.args[0] == 'error_msg'

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
        mocker.patch(MODULE_PATH + "idrac_network_attributes.validate_and_get_first_resource_id_uri",
                     return_value=('System.Embedded.1', ''))
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes._IDRACNetworkAttributes__perform_validation_for_network_adapter_id",
                     return_value=self.uri)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)

        # Scenario 1: When network_adapter_id is in server network adapter list
        device_uri = "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A/NetworkDeviceFunctions/NIC.Mezzanine.1A-2-1"
        idrac_default_args.update(
            {'network_device_function_id': 'NIC.Mezzanine.1A-2-1'})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj._IDRACNetworkAttributes__perform_validation_for_network_device_function_id()
        assert data == device_uri

        # Scenario 2: When network_adapter_id is not in server network adapter list
        network_device_function_id = 'random value'
        idrac_default_args.update(
            {'network_device_function_id': network_device_function_id})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj._IDRACNetworkAttributes__perform_validation_for_network_device_function_id()
        assert exc.value.args[0] == INVALID_ID_MSG.format(
            network_device_function_id, 'network_device_function_id')

    def test_validate_job_timeout(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                                  idrac_ntwrk_attr_mock, mocker):

        # Scenario 1: when job_wait is True and job_wait_timeout is in negative
        idrac_default_args.update({'job_wait': True, 'job_wait_timeout': -120})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj.validate_job_timeout()
        assert exc.value.args[0] == TIMEOUT_NEGATIVE_OR_ZERO_MSG

        # Scenario 2: when job_wait is False
        idrac_default_args.update(
            {'job_wait': False, 'job_wait_timeout': -120})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj.validate_job_timeout()
        assert data is None

    def test_apply_time(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                        idrac_ntwrk_attr_mock, mocker):
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_dynamic_uri",
                     return_value=self.redfish_settings)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes._IDRACNetworkAttributes__get_redfish_apply_time",
                     return_value={'AppyTime': "OnReset"})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        rf_set = idr_obj.apply_time(self.uri)
        assert rf_set == {'AppyTime': "OnReset"}

    def test_set_dynamic_base_uri_and_validate_ids(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                                                   idrac_ntwrk_attr_mock, mocker):
        tmp_dict = {}
        tmp_dict.update({'Links': self.links,
                         '@Redfish.Settings': self.redfish_settings.get('@Redfish.Settings')})
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_dynamic_uri",
                     return_value=tmp_dict)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes._IDRACNetworkAttributes__perform_validation_for_network_device_function_id",
                     return_value=self.uri)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj.set_dynamic_base_uri_and_validate_ids()
        assert data is None

    def test_clear_pending(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                           idrac_ntwrk_attr_mock, mocker):
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
            if len(args) > 2 and args[2] == '@Redfish.Settings':
                return self.redfish_settings.get('@Redfish.Settings')
            return action_setting_uri_resp
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)
        hw_model = HARDWARE_9
        gen = GENERATION_14
        firm_ver = '6.1'
        idrac_connection_ntwrk_attr_mock.get_server_generation = (gen, firm_ver, hw_model)

        # Scenario 1: When there's no pending attributes
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.OEMNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
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
            idrac_connection_ntwrk_attr_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj.clear_pending()
        assert exc.value.args[0] == JOB_RUNNING_CLEAR_PENDING_ATTR.format(
            'NICConfiguration')

        # Scenario 3: When there's pending attributes and scheduled_job is Starting in normal mode
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_scheduled_job_resp",
                     return_value={'Id': 'JIDXXXXXX', 'JobState': 'Starting'})
        action_setting_uri_resp.update({'Attributes': {'VLanId': 10}})
        g_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr__obj = self.module.OEMNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, g_module)
        with pytest.raises(Exception) as exc:
            idr__obj.clear_pending()
        assert exc.value.args[0] == SUCCESS_CLEAR_PENDING_ATTR_MSG

        # Scenario 4: Scenario 3 in check mode
        g_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        idr__obj = self.module.OEMNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, g_module)
        with pytest.raises(Exception) as exc:
            idr__obj.clear_pending()
        assert exc.value.args[0] == CHANGES_FOUND_MSG

        # Scenario 5: When there's pending attribute but no job id is present in normal mode
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_scheduled_job_resp",
                     return_value={'Id': '', 'JobState': 'Starting'})
        g_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.OEMNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, g_module)
        with pytest.raises(Exception) as exc:
            idr_obj.clear_pending()
        assert exc.value.args[0] == SUCCESS_CLEAR_PENDING_ATTR_MSG

        # Scenario 6: Scenario 5 in check_mode
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        idr_obj = self.module.OEMNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
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
            idrac_connection_ntwrk_attr_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj.clear_pending()
        assert exc.value.args[0] == CHANGES_FOUND_MSG

        # Scenario 8: When Firmware version is less 3 and oem_network_attribute is not given
        hw_model = HARDWARE_8
        gen = GENERATION_13
        firm_ver = '2.9'
        idrac_connection_ntwrk_attr_mock.get_server_generation = (gen, firm_ver, hw_model)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        idr_obj = self.module.OEMNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj.clear_pending()
        assert exc.value.args[0] == CLEAR_PENDING_NOT_SUPPORTED_WITHOUT_ATTR_IDRAC8

        # Scenario 9: When Firmware version is less 3 and oem_network_attribute is given
        idrac_default_args.update(
            {'oem_network_attributes': {'somedata': 'somevalue'}})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        idr_obj = self.module.OEMNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj.clear_pending()
        assert data is None

        # Scenario 10: When Fw vers is greater than 3, job exists, in starting, normal mode, without oem_network_attribute
        hw_model = HARDWARE_9
        gen = GENERATION_13
        firm_ver = '3.1'
        idrac_connection_ntwrk_attr_mock.get_server_generation = (gen, firm_ver, hw_model)

        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_scheduled_job_resp",
                     return_value={'Id': 'JIDXXXXXX', 'JobState': 'Starting'})
        idrac_default_args.update({'oem_network_attributes': None})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.OEMNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj.clear_pending()
        assert exc.value.args[0] == SUCCESS_CLEAR_PENDING_ATTR_MSG

    def test_perform_operation_OEMNetworkAttributes(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                                                    idrac_ntwrk_attr_mock, mocker):
        obj = MagicMock()
        obj.headers = {'Location': self.uri}
        obj.json_data = {'data': 'some value'}
        apply_time = {'ApplyTime': 'Immediate'}
        error_info = {'abc': ATTRIBUTE_NOT_EXIST_CHECK_IDEMPOTENCY_MODE}

        def mock_get_dynamic_uri_request(*args, **kwargs):
            if len(args) > 2 and args[2] == 'Links':
                return self.links
            return self.redfish_settings
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.iDRACRedfishAPI.invoke_request",
                     return_value=obj)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.iDRACRedfishAPI.import_scp",
                     return_value=obj)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes.apply_time",
                     return_value=apply_time)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes.extract_error_msg",
                     return_value=error_info)
        hw_model = HARDWARE_9
        gen = GENERATION_14
        firm_ver = '6.1'
        idrac_connection_ntwrk_attr_mock.get_server_generation = (gen, firm_ver, hw_model)

        mocker.patch(MODULE_PATH + "idrac_network_attributes.idrac_redfish_job_tracking",
                     return_value=(False, 'msg', obj.json_data, 600))

        idrac_default_args.update({'oem_network_attributes': {'VlanId': 1},
                                   'job_wait': True,
                                   'job_wait_timeout': 1200})
        # Scenario 1: When Job has returned successfully and not error msg is there
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.OEMNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        data = idr_obj.perform_operation()
        assert data == (obj, {
                        'abc': ATTRIBUTE_NOT_EXIST_CHECK_IDEMPOTENCY_MODE}, False)

    def test_perform_operation_NetworkAttributes(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                                                 idrac_ntwrk_attr_mock, mocker):
        obj = MagicMock()
        obj.headers = {'Location': self.uri}
        obj.json_data = {'data': 'some value'}
        apply_time = {'ApplyTime': 'Immediate'}
        error_info = {'abc': ATTRIBUTE_NOT_EXIST_CHECK_IDEMPOTENCY_MODE}

        def mock_get_dynamic_uri_request(*args, **kwargs):
            if len(args) > 2 and args[2] == 'Links':
                return self.links
            return self.redfish_settings
        mocker.patch(MODULE_PATH + "idrac_network_attributes.get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.iDRACRedfishAPI.invoke_request",
                     return_value=obj)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.iDRACRedfishAPI.import_scp",
                     return_value=obj)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes.apply_time",
                     return_value=apply_time)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes.extract_error_msg",
                     return_value=error_info)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.idrac_redfish_job_tracking",
                     return_value=(False, 'msg', obj.json_data, 500))
        hw_model = HARDWARE_9
        gen = GENERATION_15
        firm_ver = '7.0'
        idrac_connection_ntwrk_attr_mock.get_server_generation = (gen, firm_ver, hw_model)

        idrac_default_args.update({'network_attributes': {'VlanId': 1},
                                   'job_wait': True,
                                   'job_wait_timeout': 1200})
        # Scenario 1: When Job has returned successfully and not error msg is there
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.NetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        idr_obj.redfish_uri = self.uri
        data = idr_obj.perform_operation()
        assert data == (obj, {
                        'abc': ATTRIBUTE_NOT_EXIST_CHECK_IDEMPOTENCY_MODE}, False)

    def test_perform_operation_for_main(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                                        idrac_ntwrk_attr_mock, mocker):
        obj = MagicMock()
        obj.json_data = {'some': 'value'}
        job_state = {'JobState': "Completed"}
        invalid_attr = {'a': ATTRIBUTE_NOT_EXIST_CHECK_IDEMPOTENCY_MODE}
        mocker.patch(MODULE_PATH + "idrac_network_attributes.idrac_redfish_job_tracking",
                     return_value=(False, 'some msg', job_state, 700))
        # Scenario 1: When diff is false
        diff = 0
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        with pytest.raises(Exception) as exc:
            self.module.perform_operation_for_main(idrac_connection_ntwrk_attr_mock,
                                                   f_module, obj, diff, invalid_attr)
        assert exc.value.args[0] == NO_CHANGES_FOUND_MSG

        # Scenario 2: When diff is True and check mode is True
        diff = ({'a': 123}, {'c': 789})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        with pytest.raises(Exception) as exc:
            self.module.perform_operation_for_main(idrac_connection_ntwrk_attr_mock,
                                                   f_module, obj, diff, invalid_attr)
        assert exc.value.args[0] == CHANGES_FOUND_MSG

        # Scenario 3: When diff is True and JobState is completed and
        #             There is invalid_attr in normal mode
        resp = MagicMock()
        resp.headers = {'Location': self.uri}
        gen = GENERATION_14
        hw_model = HARDWARE_9
        firm_ver = '7.05'
        idrac_connection_ntwrk_attr_mock.get_server_generation = (gen, firm_ver, hw_model)

        def return_data():
            return (resp, invalid_attr, False)
        obj.perform_operation = return_data
        obj.json_data = {'JobState': 'Completed'}
        mocker.patch(MODULE_PATH + "idrac_network_attributes.iDRACRedfishAPI.invoke_request",
                     return_value=obj)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        with pytest.raises(Exception) as exc:
            self.module.perform_operation_for_main(idrac_connection_ntwrk_attr_mock,
                                                   f_module, obj, diff, invalid_attr)
        assert exc.value.args[0] == VALID_AND_INVALID_ATTR_MSG

        # Scenario 4: When diff is True and JobState is completed and
        #             There is no invalid_attr in normal mode
        invalid_attr = {}
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        with pytest.raises(Exception) as exc:
            self.module.perform_operation_for_main(idrac_connection_ntwrk_attr_mock,
                                                   f_module, obj, diff, invalid_attr)
        assert exc.value.args[0] == SUCCESS_MSG

        # Scenario 5: When diff is True and JobState is not completed and
        #             There is no invalid_attr in normal mode
        invalid_attr = {}

        def return_data():
            return (resp, invalid_attr, False)
        obj.json_data = {'JobState': "Scheduled"}
        mocker.patch(MODULE_PATH + "idrac_network_attributes.iDRACRedfishAPI.invoke_request",
                     return_value=obj)
        obj.perform_operation = return_data
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        with pytest.raises(Exception) as exc:
            self.module.perform_operation_for_main(idrac_connection_ntwrk_attr_mock,
                                                   f_module, obj, diff, invalid_attr)
        assert exc.value.args[0] == SCHEDULE_MSG

        # Scenario 6: When diff is False and check mode is there
        diff = 0
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        with pytest.raises(Exception) as exc:
            self.module.perform_operation_for_main(idrac_connection_ntwrk_attr_mock,
                                                   f_module, obj, diff, invalid_attr)
        assert exc.value.args[0] == NO_CHANGES_FOUND_MSG

        # Scenario 7: When diff is False and check mode is False, invalid is False
        diff = 0
        invalid_attr = {}
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        with pytest.raises(Exception) as exc:
            self.module.perform_operation_for_main(idrac_connection_ntwrk_attr_mock,
                                                   f_module, obj, diff, invalid_attr)
        assert exc.value.args[0] == NO_CHANGES_FOUND_MSG

        # Scenario 8: When Job_wait is True and wait time is less
        diff = 1
        invalid_attr = {}
        resp = MagicMock()
        resp.headers = {'Location': self.uri}

        def return_data():
            return (resp, invalid_attr, True)
        obj.perform_operation = return_data
        mocker.patch(MODULE_PATH + "idrac_network_attributes.idrac_redfish_job_tracking",
                     return_value=(False, 'msg', obj.json_data, 1200))
        idrac_default_args.update({'job_wait_timeout': 1000})
        h_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        with pytest.raises(Exception) as exc:
            self.module.perform_operation_for_main(idrac_connection_ntwrk_attr_mock,
                                                   h_module, obj, diff, invalid_attr)
        assert exc.value.args[0] == WAIT_TIMEOUT_MSG.format(1000)

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_idrac_network_attributes_main_exception_handling_case(self, exc_type, mocker, idrac_default_args,
                                                                   idrac_connection_ntwrk_attr_mock, idrac_ntwrk_attr_mock):
        obj = MagicMock()
        obj.perform_validation_for_network_adapter_id.return_value = None
        obj.perform_validation_for_network_device_function_id.return_value = None
        obj.get_diff_between_current_and_module_input.return_value = (
            None, None)
        obj.validate_job_timeout.return_value = None
        obj.clear_pending.return_value = None
        idrac_default_args.update({'apply_time': "Immediate",
                                   'network_adapter_id': 'Some_adapter_id',
                                   'network_device_function_id': 'some_device_id',
                                   'clear_pending': True if exec == 'URLError' else False})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type in [HTTPError, SSLValidationError]:
            tmp = {'network_attributes': {'VlanId': 10}}
            mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes.set_dynamic_base_uri_and_validate_ids",
                         side_effect=exc_type('https://testhost.com', 400,
                                              'http error message',
                                              {"accept-type": "application/json"},
                                              StringIO(json_str)))
        else:

            tmp = {'oem_network_attributes': {'VlanId': 10}}
            mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes.set_dynamic_base_uri_and_validate_ids",
                         side_effect=exc_type('test'))
        idrac_default_args.update(tmp)
        result = self._run_module(idrac_default_args)
        if exc_type == URLError:
            assert result['unreachable'] is True
        else:
            assert result['failed'] is True
        assert 'msg' in result

    def test_get_job_uri_10(self, idrac_default_args, idrac_connection_ntwrk_attr_mock, mocker):
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes.validate_idrac10_and_above",
                     return_value=True)
        data = idr_obj.get_job_uri()
        assert data == iDRAC_JOB_URI_10

    def test_get_job_uri(self, idrac_default_args, idrac_connection_ntwrk_attr_mock, mocker):
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(
            idrac_connection_ntwrk_attr_mock, f_module)
        mocker.patch(MODULE_PATH + "idrac_network_attributes.IDRACNetworkAttributes.validate_idrac10_and_above",
                     return_value=False)
        data = idr_obj.get_job_uri()
        assert data == iDRAC_JOB_URI
