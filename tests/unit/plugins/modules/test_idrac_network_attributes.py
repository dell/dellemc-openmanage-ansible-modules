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
INVALID_ATTR_MSG = "Unable to update the network attributes because invalid values are entered. \
    Enter the valid values for the network attributes and retry the operation."
VALID_AND_INVALID_ATTR_MSG = "Successfully updated the network attributes for valid values. \
    Unable to update other attributes because invalid values are entered. Enter the valid values and retry the operation."
NO_CHANGES_FOUND_MSG = "No changes found to be applied."
CHANGES_FOUND_MSG = "Changes found to be applied."
INVALID_ID_MSG = "Unable to complete the operation because the value `{0}` for the input  `{1}` parameter is invalid."
JOB_RUNNING_CLEAR_PENDING_ATTR = "{0} Config job is running. Wait for the job to complete. Currently can not clear pending attributes."


class TestIDRACNetworkAttributes(FakeAnsibleModule):
    module = idrac_network_attributes
    uri = '/redfish/v1/api'
    resp_mock = {}
    network_adapter_id_resp_mock = {'Members': [
        {
            "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A"
        },
        {
            "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1B"
        }
    ]}
    network_device_function_id_resp_mock = {"Members": [
        {
            "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A"
        },
        {
            "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A/NetworkDeviceFunctions/NIC.Mezzanine.1A-1-1"
        },
        {
            "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/NIC.Mezzanine.1A/NetworkDeviceFunctions/NIC.Mezzanine.1A-2-1"
        }
    ]}

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
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        ver = idr_obj._IDRACNetworkAttributes__get_idrac_firmware_version()
        assert ver == '1.2.3.4'

    def test_resource_id(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
                                             idrac_ntwrk_attr_mock, mocker):
        resource_id_list =  [
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
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        sys_id = idr_obj._IDRACNetworkAttributes__get_resource_id()
        assert sys_id == "/redfish/v1/Chassis/System.Embedded.1"

        # Scenario-2: Provide resource_id which is in list, Expectation: should pick uri from list
        idrac_default_args.update({'resource_id': 'Enclosure.Internal.0-0'})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        sys_id = idr_obj._IDRACNetworkAttributes__get_resource_id()
        assert sys_id == "/redfish/v1/Chassis/Enclosure.Internal.0-0"

        # Scenario-3: Provide invalid resource_id which is not in list, Expectation: Throw valid error msg
        idrac_default_args.update({'resource_id': 'abcdef'})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj._IDRACNetworkAttributes__get_resource_id()
        assert exc.value.args[0] == INVALID_ID_MSG.format('abcdef', 'resource_id')
    
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
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(idrac_connection_ntwrk_attr_mock, f_module, self.uri)
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
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(idrac_connection_ntwrk_attr_mock, f_module, self.uri)
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
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(idrac_connection_ntwrk_attr_mock, f_module, self.uri)
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
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj._IDRACNetworkAttributes__validate_time(m_time)
        assert exc.value.args[0] == MAINTENACE_OFFSET_DIFF_MSG.format(resp[1])

        # Scenario 2: When mtime is less than current time
        m_time = "2021-09-14T05:59:35-05:00"
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj._IDRACNetworkAttributes__validate_time(m_time)
        assert exc.value.args[0] == MAINTENACE_OFFSET_BEHIND_MSG

        # Scenario 2: When mtime is greater than current time
        m_time = "2024-09-14T05:59:35-05:00"
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(idrac_connection_ntwrk_attr_mock, f_module, self.uri)
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
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj._IDRACNetworkAttributes__get_redfish_apply_time('AtMaintenanceWindowStart', rf_settings)
        assert exc.value.args[0] == APPLY_TIME_NOT_SUPPORTED_MSG.format('AtMaintenanceWindowStart')

        # Scenario 2: When Maintenance is not supported but 'InMaintenanceWindowOnReset' is passed
        idrac_default_args.update({'apply_time': 'InMaintenanceWindowOnReset'})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        with pytest.raises(Exception) as exc:
            idr_obj._IDRACNetworkAttributes__get_redfish_apply_time('InMaintenanceWindowOnReset', rf_settings)
        assert exc.value.args[0] == APPLY_TIME_NOT_SUPPORTED_MSG.format('InMaintenanceWindowOnReset')

        # Scenario 3: When ApplyTime does not support Maintenance
        rf_settings.append('InMaintenanceWindowOnReset')
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        data = idr_obj._IDRACNetworkAttributes__get_redfish_apply_time('InMaintenanceWindowOnReset', rf_settings)
        assert data == ({'ApplyTime': 'InMaintenanceWindowOnReset',
                         'MaintenanceWindowDurationInSeconds': 600,
                         'MaintenanceWindowStartTime': '2022-09-14T06:59:35-05:00'},
                         False)
        
        # Scenario 4: When ApplyTime is Immediate
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        data = idr_obj._IDRACNetworkAttributes__get_redfish_apply_time('Immediate', rf_settings)
        assert data == ({'ApplyTime': 'Immediate'}, False)

        # Scenario 5: When ApplyTime does not support Immediate
        rf_settings.remove('Immediate')
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        data = idr_obj._IDRACNetworkAttributes__get_redfish_apply_time('Immediate', rf_settings)
        assert data == ({'ApplyTime': 'OnReset'}, True)

        # Scenario 6: When AppyTime is empty
        rf_settings = []
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.IDRACNetworkAttributes(idrac_connection_ntwrk_attr_mock, f_module, self.uri)
        data = idr_obj._IDRACNetworkAttributes__get_redfish_apply_time('Immediate', rf_settings)
        assert data == ({}, False)




        



    # def test_invalid_network_device_function_id_case(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
    #                                          idrac_ntwrk_attr_mock, mocker):
    #     obj = MagicMock()
    #     network_device_function_id = 'xyz'
    #     obj.json_data = self.network_device_function_id_resp_mock
    #     idrac_default_args.update({'network_adapter_id': 'NIC.Mezzanine.1A',
    #                                'network_device_function_id': network_device_function_id,
    #                                'apply_time': 'Immediate'})
    #     mocker.patch(MODULE_PATH + "idrac_network_attributes.iDRACRedfishAPI.invoke_request",
    #                  return_value=(obj))
    #     resp = self._run_module(idrac_default_args)
    #     assert resp['msg'] == INVALID_ID_MSG.format(network_device_function_id, 'network_device_function_id')
    
    # def test_get_user_id_accounts(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
    #                               idrac_ntwrk_attr_mock, mocker):
    #     json_str = to_text(json.dumps({"data": "out"}))
    #     idrac_default_args.update({"username": "test"})
    #     obj = MagicMock()
    #     obj.json_data = {"UserName": "test"}
    #     f_module = self.get_module_mock(
    #         params=idrac_default_args, check_mode=False)
    #     mocker.patch(MODULE_PATH + "idrac_network_attributes.iDRACRedfishAPI.invoke_request",
    #                  return_value=(obj))
    #     mocker.patch(MODULE_PATH + "idrac_network_attributes.strip_substr_dict",
    #                  return_value=({"UserName": "test"}))
    #     resp = self.module.get_user_id_accounts(
    #         idrac_connection_ntwrk_attr_mock, f_module, "/acounts/accdetails", 1)
    #     assert resp.get("UserName") == "test"

    #     obj = MagicMock()
    #     obj.json_data = {"UserName": "test", "Oem": {"Dell": "test"}}
    #     mocker.patch(MODULE_PATH + "idrac_network_attributes.iDRACRedfishAPI.invoke_request",
    #                  return_value=(obj))
    #     mocker.patch(MODULE_PATH + "idrac_network_attributes.strip_substr_dict",
    #                  return_value=({"UserName": "test", "Oem": {"Dell": "test"}}))
    #     resp = self.module.get_user_id_accounts(
    #         idrac_connection_ntwrk_attr_mock, f_module, "/acounts/accdetails", 1)
    #     assert resp.get("UserName") == "test"

    #     idrac_connection_ntwrk_attr_mock.invoke_request.side_effect = HTTPError(
    #         'http://testhost.com', 400,
    #         'http error message',
    #         {"accept-type": "application/json"},
    #         StringIO(json_str))
    #     with pytest.raises(Exception) as exc:
    #         self.module.get_user_id_accounts(
    #             idrac_connection_ntwrk_attr_mock, f_module, "/acounts/accdetails", 1)
    #     assert exc.value.args[0] == "'user_id' is not valid."

    # def test_get_user_name_accounts(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
    #                                 idrac_ntwrk_attr_mock, mocker):
    #     idrac_default_args.update({"username": "test"})
    #     mocker.patch(MODULE_PATH + "idrac_network_attributes.fetch_all_accounts",
    #                  return_value=([{"UserName": "test"}]))
    #     mocker.patch(MODULE_PATH + "idrac_network_attributes.strip_substr_dict",
    #                  return_value=({"UserName": "test"}))
    #     f_module = self.get_module_mock(
    #         params=idrac_default_args, check_mode=False)
    #     resp = self.module.get_user_name_accounts(
    #         idrac_connection_ntwrk_attr_mock, f_module, "/acounts/accdetails", "test")
    #     assert resp.get("UserName") == "test"

    #     mocker.patch(MODULE_PATH + "idrac_network_attributes.strip_substr_dict",
    #                  return_value=({"UserName": "test", "Oem": {"Dell": "test"}}))
    #     resp = self.module.get_user_name_accounts(
    #         idrac_connection_ntwrk_attr_mock, f_module, "/acounts/accdetails", "test")
    #     assert resp.get("UserName") == "test"

    #     with pytest.raises(Exception) as exc:
    #         self.module.get_user_name_accounts(
    #             idrac_connection_ntwrk_attr_mock, f_module, "/acounts/accdetails", "test1")
    #     assert exc.value.args[0] == "'username' is not valid."

    # def test_get_all_accounts_single(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
    #                                  idrac_ntwrk_attr_mock, mocker):
    #     idrac_default_args.update({"username": "test"})
    #     mocker.patch(MODULE_PATH + "idrac_network_attributes.fetch_all_accounts",
    #                  return_value=([{"UserName": "test", "Oem": {"Dell": "test"}}]))
    #     mocker.patch(MODULE_PATH + "idrac_network_attributes.strip_substr_dict",
    #                  return_value=({"UserName": "test", "Oem": {"Dell": "test"}}))
    #     resp = self.module.get_all_accounts(
    #         idrac_connection_ntwrk_attr_mock, "/acounts/accdetails")
    #     assert resp[0].get("UserName") == "test"

    #     mocker.patch(MODULE_PATH + "idrac_network_attributes.fetch_all_accounts",
    #                  return_value=([{"UserName": ""}]))
    #     resp = self.module.get_all_accounts(
    #         idrac_connection_ntwrk_attr_mock, "/acounts/accdetails")
    #     assert resp == []

    #     mocker.patch(MODULE_PATH + "idrac_network_attributes.fetch_all_accounts",
    #                  return_value=([]))
    #     resp = self.module.get_all_accounts(
    #         idrac_connection_ntwrk_attr_mock, "/acounts/accdetails")
    #     assert resp == []

    # def test_get_all_accounts_multiple(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
    #                                    idrac_ntwrk_attr_mock, mocker):
    #     def strip_substr_dict_mock(acc):
    #         if acc.get("UserName") == "test":
    #             return {"UserName": "test"}
    #         else:
    #             return {"UserName": "test1"}
    #     mocker.side_effect = strip_substr_dict_mock

    #     mocker.patch(MODULE_PATH + "idrac_network_attributes.fetch_all_accounts",
    #                  return_value=([{"UserName": "test"}, {"UserName": "test1"}]))
    #     resp = self.module.get_all_accounts(
    #         idrac_connection_ntwrk_attr_mock, "/acounts/accdetails")
    #     assert resp[0].get("UserName") == "test"
    #     assert resp[1].get("UserName") == "test1"

    # def test_get_accounts_uri(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
    #                           idrac_ntwrk_attr_mock, mocker):
    #     acc_service_uri = MagicMock()
    #     acc_service_uri.json_data = {"AccountService": {
    #         "@odata.id": "/account"}, "Accounts": {"@odata.id": "/account/accountdetails"}}
    #     acc_service = MagicMock()
    #     acc_service.json_data = {"Accounts": {
    #         "@odata.id": "/account/accountdetails"}}

    #     mocker.patch(MODULE_PATH + "idrac_network_attributes.iDRACRedfishAPI.invoke_request",
    #                  return_value=(acc_service_uri))
    #     resp = self.module.get_accounts_uri(idrac_connection_ntwrk_attr_mock)
    #     assert resp == "/account/accountdetails"

    #     json_str = to_text(json.dumps({"data": "out"}))
    #     idrac_connection_ntwrk_attr_mock.invoke_request.side_effect = HTTPError(
    #         'http://testhost.com', 400,
    #         'http error message',
    #         {"accept-type": "application/json"},
    #         StringIO(json_str))

    #     resp = self.module.get_accounts_uri(idrac_connection_ntwrk_attr_mock)
    #     assert resp == "/redfish/v1/AccountService/Accounts"

    # def test_user_info_main_success_case_all(self, idrac_default_args, idrac_connection_ntwrk_attr_mock,
    #                                          idrac_ntwrk_attr_mock, mocker):
    #     idrac_default_args.update({"username": "test"})
    #     mocker.patch(MODULE_PATH + "idrac_network_attributes.get_accounts_uri",
    #                  return_value=("/acounts/accdetails"))
    #     mocker.patch(MODULE_PATH + "idrac_network_attributes.get_user_name_accounts",
    #                  return_value=({"UserName": "test"}))
    #     idrac_ntwrk_attr_mock.status_code = 200
    #     idrac_ntwrk_attr_mock.success = True
    #     resp = self._run_module(idrac_default_args)
    #     assert resp['msg'] == "Successfully retrieved the user information."
    #     assert resp['user_info'][0].get("UserName") == "test"

    #     mocker.patch(MODULE_PATH + "idrac_network_attributes.get_user_id_accounts",
    #                  return_value=({"UserName": "test"}))
    #     idrac_default_args.update({"user_id": "1234"})
    #     idrac_default_args.pop("username")
    #     resp = self._run_module(idrac_default_args)
    #     assert resp['msg'] == "Successfully retrieved the user information."
    #     assert resp['user_info'][0].get("UserName") == "test"

    #     mocker.patch(MODULE_PATH + "idrac_network_attributes.get_all_accounts",
    #                  return_value=([{"UserName": "test"}]))
    #     idrac_default_args.pop("user_id")
    #     resp = self._run_module(idrac_default_args)
    #     assert resp['msg'] == "Successfully retrieved the information of 1 user(s)."
    #     assert resp['user_info'][0].get("UserName") == "test"

    #     mocker.patch(MODULE_PATH + "idrac_network_attributes.get_all_accounts",
    #                  return_value=([]))
    #     resp = self._run_module_with_fail_json(idrac_default_args)
    #     assert resp['failed'] is True
    #     assert resp['msg'] == "Unable to retrieve the user information."

    # @pytest.mark.parametrize("exc_type",
    #                          [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    # def test_idrac_network_attributes_main_exception_handling_case(self, exc_type, mocker, idrac_default_args,
    #                                                       idrac_connection_ntwrk_attr_mock, idrac_ntwrk_attr_mock):
    #     idrac_ntwrk_attr_mock.status_code = 400
    #     idrac_ntwrk_attr_mock.success = False
    #     json_str = to_text(json.dumps({"data": "out"}))
    #     if exc_type not in [HTTPError, SSLValidationError]:
    #         mocker.patch(MODULE_PATH + "idrac_network_attributes.get_accounts_uri",
    #                      side_effect=exc_type('test'))
    #     else:
    #         mocker.patch(MODULE_PATH + "idrac_network_attributes.get_accounts_uri",
    #                      side_effect=exc_type('http://testhost.com', 400,
    #                                           'http error message',
    #                                           {"accept-type": "application/json"},
    #                                           StringIO(json_str)))
    #     if exc_type != URLError:
    #         result = self._run_module_with_fail_json(idrac_default_args)
    #         assert result['failed'] is True
    #     else:
    #         result = self._run_module(idrac_default_args)
    #     assert 'msg' in result
