# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.3.0
# Copyright (C) 2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
import pytest
from ssl import SSLError
from io import StringIO
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils._text import to_text
from ansible_collections.dellemc.openmanage.plugins.modules import ome_discovery
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_discovery.'
NO_CHANGES_MSG = "No changes found to be applied."
DISC_JOB_RUNNING = "Discovery job '{name}' with ID {id} is running. Please retry after job completion."
DISC_DEL_JOBS_SUCCESS = "Successfully deleted {n} discovery job(s)."
MULTI_DISCOVERY = "Multiple discoveries present. Run the job again using a specific ID."
DISCOVERY_SCHEDULED = "Successfully scheduled the Discovery job."
DISCOVER_JOB_COMPLETE = "Successfully completed the Discovery job."
JOB_TRACK_SUCCESS = "Discovery job has {0}."
JOB_TRACK_FAIL = "No devices discovered, job is in {0} state."
JOB_TRACK_UNABLE = "Unable to track discovery job status of {0}."
JOB_TRACK_INCOMPLETE = "Discovery job {0} incomplete after polling {1} times."
INVALID_DEVICES = "Invalid device types found - {0}."


@pytest.fixture
def ome_connection_mock_for_discovery(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeDiscovery(FakeAnsibleModule):
    module = ome_discovery

    @pytest.mark.parametrize("params", [{"mparams": {"state": "absent", "discovery_job_name": "my_discovery1"},
                                         "discov_list": [{"DiscoveryConfigGroupId": 12,
                                                          "DiscoveryConfigGroupName": "my_discovery1"}],
                                         "job_state_dict": {12: 2010}, "res": DISC_DEL_JOBS_SUCCESS.format(n=1),
                                         "json_data": 1, "success": True},
                                        {"mparams": {"state": "absent", "discovery_job_name": "my_discovery1"},
                                         "discov_list": [{"DiscoveryConfigGroupId": 12,
                                                          "DiscoveryConfigGroupName": "my_discovery1"}],
                                         "job_state_dict": {12: 2050},
                                         "res": DISC_JOB_RUNNING.format(name='my_discovery1', id=12), "json_data": 1,
                                         "success": True}])
    def test_delete_discovery(self, mocker, params, ome_connection_mock_for_discovery, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        mocker.patch(MODULE_PATH + 'get_discovery_states', return_value=params["job_state_dict"])
        f_module = self.get_module_mock(params=params["mparams"])
        error_message = params["res"]
        with pytest.raises(Exception) as err:
            self.module.delete_discovery(f_module, ome_connection_mock_for_discovery, params['discov_list'])
        assert err.value.args[0] == error_message

    @pytest.mark.parametrize("params", [{"mparams": {"state": "absent", "discovery_job_name": "my_discovery1"},
                                         "res": [{"DiscoveryConfigGroupId": 12,
                                                  "DiscoveryConfigGroupName": "my_discovery1"}],
                                         "json_data": {"value": [{"DiscoveryConfigGroupId": 12,
                                                                  "DiscoveryConfigGroupName": "my_discovery1"}]},
                                         "success": True},
                                        {"mparams": {"state": "absent", "discovery_id": 12}, "res": [
                                            {"DiscoveryConfigGroupId": 12,
                                             "DiscoveryConfigGroupName": "my_discovery1"}],
                                         "json_data": {"value": [{"DiscoveryConfigGroupId": 11,
                                                                  "DiscoveryConfigGroupName": "my_discovery2"},
                                                                 {"DiscoveryConfigGroupId": 12,
                                                                  "DiscoveryConfigGroupName": "my_discovery1"}]},
                                         "success": True}])
    def test_check_existing_discovery(self, mocker, params, ome_connection_mock_for_discovery, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params["mparams"])
        res = self.module.check_existing_discovery(f_module, ome_connection_mock_for_discovery)
        assert res == params["res"]

    @pytest.mark.parametrize("params", [
        {"res": {12: 2020}, "json_data": {"value": [{"DiscoveryConfigGroupId": 12, "JobStatusId": 2020}]},
         "success": True}])
    def test_get_discovery_states(self, params, ome_connection_mock_for_discovery, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        res = self.module.get_discovery_states(ome_connection_mock_for_discovery)
        assert res == params["res"]

    @pytest.mark.parametrize("params", [{"mparams": {"schedule": 'RunNow'},
                                         'schedule_payload': {"RunNow": True, "RunLater": False, 'Cron': "startnow"}},
                                        {"mparams": {"schedule": 'RunLater', 'cron': "1 2 3 4 5 *"},
                                         'schedule_payload': {"RunNow": False, "RunLater": True,
                                                              'Cron': "1 2 3 4 5 *"}}, ])
    def test_get_schedule(self, params):
        f_module = self.get_module_mock(params=params["mparams"])
        res = self.module.get_schedule(f_module)
        assert res == params['schedule_payload']

    @pytest.mark.parametrize("params", [{"json_data": {
        "value": [{"ProtocolName": "SNMP", "DeviceTypeId": 1000, "DeviceTypeName": "SERVER"},
                  {"ProtocolName": "SNMP", "DeviceTypeId": 5000, "DeviceTypeName": "DELL STORAGE"},
                  {"ProtocolName": "SNMP", "DeviceTypeId": 7000, "DeviceTypeName": "NETWORK SWITCH"},
                  {"ProtocolName": "WSMAN", "DeviceTypeId": 1000, "DeviceTypeName": "SERVER"},
                  {"ProtocolName": "WSMAN", "DeviceTypeId": 2000, "DeviceTypeName": "CHASSIS"},
                  {"ProtocolName": "REDFISH", "DeviceTypeId": 1000, "DeviceTypeName": "SERVER"},
                  {"ProtocolName": "REDFISH", "DeviceTypeId": 2000, "DeviceTypeName": "CHASSIS", },
                  {"ProtocolName": "IPMI", "DeviceTypeId": 1000, "DeviceTypeName": "SERVER"},
                  {"ProtocolName": "SSH", "DeviceTypeId": 1000, "DeviceTypeName": "SERVER"},
                  {"ProtocolName": "VMWARE", "DeviceTypeId": 1000, "DeviceTypeName": "SERVER"},
                  {"ProtocolName": "STORAGE", "DeviceTypeId": 5000, "DeviceTypeName": "DELL STORAGE"}]},
        "dev_id_map": {"CHASSIS": 2000, "DELL STORAGE": 5000, "NETWORK SWITCH": 7000, "SERVER": 1000, "STORAGE": 5000},
        "proto_dev_map": {"CHASSIS": ["WSMAN", "REDFISH"], "DELL STORAGE": ["SNMP", "STORAGE"],
                          "NETWORK SWITCH": ["SNMP"],
                          "STORAGE": ["SNMP", "STORAGE"],
                          "SERVER": ["SNMP", "WSMAN", "REDFISH", "IPMI", "SSH", "VMWARE"]}}])
    def test_get_protocol_device_map(self, params, ome_connection_mock_for_discovery, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        prot_dev_map, dev_id_map = self.module.get_protocol_device_map(ome_connection_mock_for_discovery)
        assert prot_dev_map == params['proto_dev_map']
        assert dev_id_map == params['dev_id_map']

    @pytest.mark.parametrize("params", [{
        "mparams": {"discovery_job_name": 'd1', 'trap_destination': True, 'community_string': True,
                    'email_recipient': 'abc@email.com', 'description': "d1_desc"},
        'other_dict': {"DiscoveryConfigGroupName": 'd1', "TrapDestination": True, 'CommunityString': True,
                       'DiscoveryStatusEmailRecipient': 'abc@email.com'}}])
    def test_get_other_discovery_payload(self, params):
        f_module = self.get_module_mock(params=params["mparams"])
        res = self.module.get_other_discovery_payload(f_module)
        assert res == params['other_dict']

    @pytest.mark.parametrize("params", [{"json_data": {"value": [{"Id": 1, "StartTime": "2021-04-19 04:54:18.427"},
                                                                 {"Id": 2, "StartTime": "2021-04-19 04:55:18.427"}]},
                                         "ips": {"Failed": ["192.168.1.2"], "Completed": ["192.168.1.3"]},
                                         "pag_ret_val": {
                                             "value": [{"Key": "192.168.1.2", "JobStatus": {"Name": "Failed"}},
                                                       {"Key": "192.168.1.3", "JobStatus": {"Name": "Completed"}}]}}])
    def test_get_execution_details(self, params, ome_connection_mock_for_discovery, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        ome_connection_mock_for_discovery.get_all_items_with_pagination.return_value = params['pag_ret_val']
        f_module = self.get_module_mock()
        ips = self.module.get_execution_details(f_module, ome_connection_mock_for_discovery, 1)
        assert ips == params['ips']

    @pytest.mark.parametrize("params", [{"json_data": {'JobStatusId': 2060}, 'job_wait_sec': 60, 'job_failed': False,
                                         "msg": JOB_TRACK_SUCCESS.format('completed successfully')},
                                        {"json_data": {'JobStatusId': 2070}, 'job_wait_sec': 60, 'job_failed': True,
                                         "msg": JOB_TRACK_FAIL.format('Failed')},
                                        {"json_data": {'JobStatusId': 2050}, 'job_wait_sec': 60, 'job_failed': True,
                                         "msg": JOB_TRACK_INCOMPLETE.format(1, 2)}, ])
    def test_discovery_job_tracking(self, params, mocker, ome_connection_mock_for_discovery, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        mocker.patch(MODULE_PATH + 'time.sleep', return_value=None)
        job_failed, msg = self.module.discovery_job_tracking(ome_connection_mock_for_discovery, 1,
                                                             params['job_wait_sec'])
        assert job_failed == params['job_failed']
        assert msg == params['msg']

    @pytest.mark.parametrize("params", [{"discovery_json": {'DiscoveryConfigTaskParam': [{'TaskId': 12}]},
                                         'job_id': 12, "json_data": {"value": [{"Id": 1}, {"Id": 2}]}},
                                        {"discovery_json": {'DiscoveryConfigGroupId': 123,
                                                            'DiscoveryConfigTaskParam': [{'TaskId': 12},
                                                                                         {'TaskId': 23}]},
                                            'job_id': 12, "json_data": {"value": [{'DiscoveryConfigGroupId': 234,
                                                                                   "JobId": 2},
                                                                                  {'DiscoveryConfigGroupId': 123,
                                                                                   "JobId": 12}, ]}}])
    def test_get_job_data(self, params, ome_connection_mock_for_discovery, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        job_id = self.module.get_job_data(params['discovery_json'], ome_connection_mock_for_discovery)
        assert job_id == params['job_id']

    @pytest.mark.parametrize("params", [{"disc_config": {
        "ipmi": {"kgkey": None, "password": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER", "retries": 3, "timeout": 60,
                 "username": "root"},
        "wsman": {"password": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER", "retries": 3, "timeout": 60, "username": "root"}},
        'conn_profile': {"credentials": [{"authType": "Basic", "credentials": {"kgkey": None,
                                                                               "password": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
                                                                               "retries": 3, "timeout": 60,
                                                                               "username": "root"}, "modified": False,
                                          "type": "IPMI"}], "profileDescription": "", "profileId": 0, "profileName": "",
                         "type": "DISCOVERY"}}])
    def test_get_connection_profile(self, params):
        conn_profile = self.module.get_connection_profile(params['disc_config'])
        assert conn_profile['type'] == params['conn_profile']['type']

    @pytest.mark.parametrize("params", [{"disc_cfg_list": [{
        "ConnectionProfile": "{\"profileDescription\": \"\", \"profileId\": 0, \"type\": \"DISCOVERY\", \"credentials\""
                             ": [{\"credentials\": {\"retries\": 3, \"community\": \"public\", \"timeout\": 3, \"port\""
                             ": 161}, \"authType\": \"Basic\", \"type\": \"SNMP\", \"modified\": False}], "
                             "\"profileName\": \"\"}", "DeviceType": [1000],
        "DiscoveryConfigTargets": [{"NetworkAddressDetail": "196.168.24.17"}]}],
        "get_conn_json": {"profileId": 0, "profileName": "", "profileDescription": "", "type": "DISCOVERY",
                          'credentials': [{'authType': 'Basic',
                                           'credentials': {'community': 'public', 'port': 161, 'retries': 3,
                                                           'timeout': 3}, 'id': 116, 'modified': False,
                                           'type': 'SNMP'}]}, "DeviceType": [1000],
        "DiscoveryConfigTargets": [{"NetworkAddressDetail": "196.168.24.17"}], 'mparams': {'discovery_config_targets': [
            {"device_types": ["SERVER"], "network_address_detail": ["196.168.24.17"],
             "snmp": {"community": "public", "port": 161, "retries": 3, "timeout": 3}}]}}])
    def test_get_discovery_config(self, params, mocker, ome_connection_mock_for_discovery, ):
        dev_id_map = {"CHASSIS": 2000, "DELL STORAGE": 5000, "NETWORK SWITCH": 7000, "SERVER": 1000, "STORAGE": 5000}
        proto_dev_map = {"CHASSIS": ["WSMAN", "REDFISH"], "DELL STORAGE": ["SNMP", "STORAGE"],
                         "NETWORK SWITCH": ["SNMP"], "SERVER": ["SNMP", "WSMAN", "REDFISH", "IPMI", "SSH", "VMWARE"]}
        f_module = self.get_module_mock(params=params['mparams'])
        mocker.patch(MODULE_PATH + 'get_protocol_device_map', return_value=(proto_dev_map, dev_id_map))
        mocker.patch(MODULE_PATH + 'get_connection_profile', return_value=params['get_conn_json'])
        disc_cfg_list = self.module.get_discovery_config(f_module, ome_connection_mock_for_discovery)
        assert disc_cfg_list[0]['DeviceType'] == params['DeviceType']
        assert disc_cfg_list[0]['DiscoveryConfigTargets'] == params[
            'DiscoveryConfigTargets']  # assert disc_cfg_list == params['disc_cfg_list']

    @pytest.mark.parametrize("params", [{"json_data": {"@odata.type": "#DiscoveryConfigService.DiscoveryJob",
                                                       "@odata.id": "/api/DiscoveryConfigService/Jobs(12617)",
                                                       "JobId": 12617, "JobName": "D1", "JobSchedule": "startnow",
                                                       "DiscoveryConfigExpectedDeviceCount": 713,
                                                       "DiscoveryConfigDiscoveredDeviceCount": 0,
                                                       "DiscoveryConfigEmailRecipient": "jag@dell.com", },
                                         "djob": {"JobId": 12617, "JobName": "D1", "JobSchedule": "startnow",
                                                  "DiscoveryConfigExpectedDeviceCount": 713,
                                                  "DiscoveryConfigDiscoveredDeviceCount": 0,
                                                  "DiscoveryConfigEmailRecipient": "jag@dell.com", }}])
    def test_get_discovery_job(self, params, ome_connection_mock_for_discovery, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        djob = self.module.get_discovery_job(ome_connection_mock_for_discovery, 12)
        assert djob == params['djob']

    @pytest.mark.parametrize("params", [
        {"json_data": {"DiscoveryConfigGroupName": 'd1'}, 'job_failed': False, 'job_message': DISCOVER_JOB_COMPLETE,
         'mparams': {'job_wait': True, 'schedule': 'RunNow', 'job_wait_timeout': 1000}},
        {"json_data": {"DiscoveryConfigGroupName": 'd1'}, 'job_failed': True, 'job_message': JOB_TRACK_FAIL,
         'mparams': {'job_wait': True, 'schedule': 'RunNow', 'job_wait_timeout': 1000}},
        {"json_data": {"DiscoveryConfigGroupName": 'd1'}, 'job_failed': True, 'job_message': DISCOVERY_SCHEDULED,
         'mparams': {'job_wait': False, 'schedule': 'RunLater', 'job_wait_timeout': 1000}}])
    def test_create_discovery(self, params, mocker, ome_connection_mock_for_discovery, ome_response_mock):
        mocker.patch(MODULE_PATH + 'get_discovery_config', return_value={})
        mocker.patch(MODULE_PATH + 'get_schedule', return_value={})
        mocker.patch(MODULE_PATH + 'get_other_discovery_payload', return_value={})
        mocker.patch(MODULE_PATH + 'get_job_data', return_value=12)
        mocker.patch(MODULE_PATH + 'get_execution_details', return_value={})
        mocker.patch(MODULE_PATH + 'get_discovery_job', return_value={})
        mocker.patch(MODULE_PATH + 'discovery_job_tracking', return_value=(params['job_failed'], params['job_message']))
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        f_module = self.get_module_mock(params=params['mparams'])
        error_message = params["job_message"]
        with pytest.raises(Exception) as err:
            self.module.create_discovery(f_module, ome_connection_mock_for_discovery)
        assert err.value.args[0] == error_message

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_discovery_main_exception_failure_case(self, exc_type, mocker, ome_default_args,
                                                       ome_connection_mock_for_discovery, ome_response_mock):
        ome_default_args.update({"state": "absent", "discovery_job_name": "t1"})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'check_existing_discovery', side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'check_existing_discovery', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'check_existing_discovery',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result

    @pytest.mark.parametrize(
        "params", [{"json_data": {"DiscoveryConfigGroupName": 'd1'},
                    'job_failed': False, 'job_message': DISCOVER_JOB_COMPLETE,
                    'mparams': {'job_wait': True, 'schedule': 'RunNow', 'job_wait_timeout': 1000}},
                   {"json_data": {"DiscoveryConfigGroupName": 'd1'}, 'job_failed': True,
                    'job_message': JOB_TRACK_FAIL,
                    'mparams': {'job_wait': True, 'schedule': 'RunNow', 'job_wait_timeout': 1000}},
                   {"json_data": {"DiscoveryConfigGroupName": 'd1'}, 'job_failed': True,
                    'job_message': DISCOVERY_SCHEDULED,
                    'mparams': {'job_wait': False, 'schedule': 'RunLater', 'job_wait_timeout': 1000}}])
    def test_modify_discovery(self, params, mocker, ome_connection_mock_for_discovery, ome_response_mock):
        discov_list = [{"DiscoveryConfigGroupId": 12, "DiscoveryConfigGroupName": "my_discovery1"}]
        f_module = self.get_module_mock(params=params['mparams'])
        mocker.patch(MODULE_PATH + 'get_other_discovery_payload', return_value={"DiscoveryConfigGroupId": 10})
        mocker.patch(MODULE_PATH + 'update_modify_payload', return_value=None)
        mocker.patch(MODULE_PATH + 'get_job_data', return_value=12)
        mocker.patch(MODULE_PATH + 'get_execution_details', return_value={})
        mocker.patch(MODULE_PATH + 'get_discovery_job', return_value={})
        mocker.patch(MODULE_PATH + 'get_discovery_config', return_value={})
        mocker.patch(MODULE_PATH + 'get_discovery_states', return_value={12: 15})
        mocker.patch(MODULE_PATH + 'discovery_job_tracking', return_value=(params['job_failed'], params['job_message']))
        error_message = params["job_message"]
        with pytest.raises(Exception) as err:
            self.module.modify_discovery(f_module, ome_connection_mock_for_discovery, discov_list)
        assert err.value.args[0] == error_message

    def test_modify_discovery_failure_case01(self, ome_connection_mock_for_discovery):
        multi_disc_msg = MULTI_DISCOVERY
        f_module = self.get_module_mock(params={'job_wait': True, 'schedule': 'RunNow', 'job_wait_timeout': 1000})
        with pytest.raises(Exception) as err:
            self.module.modify_discovery(f_module, ome_connection_mock_for_discovery,
                                         [{"DiscoveryConfigGroupId": 1, "DiscoveryConfigGroupName": "my_discovery1"},
                                          {"DiscoveryConfigGroupId": 2, "DiscoveryConfigGroupName": "my_discovery2"}])
        assert err.value.args[0] == multi_disc_msg

    def test_modify_discovery_failure_case2(self, mocker, ome_connection_mock_for_discovery):
        f_module = self.get_module_mock(params={'job_wait': True, 'schedule': 'RunNow', 'job_wait_timeout': 1000})
        job_run_msg = DISC_JOB_RUNNING.format(name='my_discovery1', id=12)
        mocker.patch(MODULE_PATH + 'get_discovery_states', return_value={12: 2050})
        with pytest.raises(Exception) as err:
            self.module.modify_discovery(f_module, ome_connection_mock_for_discovery, [
                {"DiscoveryConfigGroupId": 12, "DiscoveryConfigGroupName": "my_discovery1"}])
        assert err.value.args[0] == job_run_msg

    def test_update_modify_payload(self):
        current_payload = {
            "DiscoveryConfigGroupId": 21,
            "DiscoveryConfigGroupName": "Discoverystorage",
            "DiscoveryStatusEmailRecipient": None,
            "DiscoveryConfigModels": [
                {
                    "DiscoveryConfigId": 41,
                    "DiscoveryConfigStatus": None,
                    "DiscoveryConfigTargets": [
                        {
                            "DiscoveryConfigTargetId": 41,
                            "NetworkAddressDetail": "mock_network_address",
                            "SubnetMask": None,
                            "AddressType": 1,
                            "Disabled": False,
                            "Exclude": False
                        }
                    ],
                    "ConnectionProfileId": 21341,
                    "ConnectionProfile": "{\n  \"profileId\" : 21341,\n  \"profileName\" : \"\","
                                         "\n  \"profileDescription\" : \"\",\n  \"type\" : \"DISCOVERY\","
                                         "\n  \"updatedBy\" : null,\n  \"updateTime\" : 1617952521213,"
                                         "\n  \"credentials\" : [ {\n    \"type\" : \"STORAGE\",\n    \"authType\" : "
                                         "\"Basic\",\n    \"modified\" : false,\n    \"id\" : 44,"
                                         "\n    \"credentials\" : {\n      \"username\" : \"root\","
                                         "\n      \"password\" : null,\n      \"domain\" : null,\n      \"caCheck\" : "
                                         "false,\n      \"cnCheck\" : false,\n      \"certificateData\" : null,"
                                         "\n      \"certificateDetail\" : null,\n      \"port\" : 443,"
                                         "\n      \"retries\" : 3,\n      \"timeout\" : 60,\n      \"isHttp\" : "
                                         "false,\n      \"keepAlive\" : true,\n      \"version\" : null\n    }\n  } "
                                         "]\n}",
                    "DeviceType": [
                        5000
                    ]
                }
            ],
            "Schedule": {
                "RunNow": False,
                "RunLater": False,
                "Recurring": None,
                "Cron": "startnow",
                "StartTime": None,
                "EndTime": None
            },
            "TrapDestination": False,
            "CommunityString": False,
            "UseAllProfiles": False,
            "CreateGroup": True
        }
        discovery_modify_payload = {
            "DiscoveryConfigGroupName": "name1"
        }
        self.module.update_modify_payload(discovery_modify_payload, current_payload, new_name="name2")
        assert discovery_modify_payload["DiscoveryConfigGroupName"] == "name2"
        assert discovery_modify_payload["Schedule"]["RunNow"] is True
        assert discovery_modify_payload["Schedule"]["RunLater"] is False
        assert discovery_modify_payload["Schedule"]["Cron"] == "startnow"

    def test_update_modify_payload_case2(self):
        current_payload = {
            "DiscoveryConfigGroupId": 21,
            "DiscoveryConfigGroupName": "Discoverystorage",
            "DiscoveryStatusEmailRecipient": None,
            "DiscoveryConfigModels": [
                {
                    "DiscoveryConfigId": 41,
                    "DiscoveryConfigStatus": None,
                    "DiscoveryConfigTargets": [
                        {
                            "DiscoveryConfigTargetId": 41,
                            "NetworkAddressDetail": "mock_network_address",
                            "SubnetMask": None,
                            "AddressType": 1,
                            "Disabled": False,
                            "Exclude": False
                        }
                    ],
                    "ConnectionProfileId": 21341,
                    "ConnectionProfile": "{\n  \"profileId\" : 21341,\n  \"profileName\" : \"\","
                                         "\n  \"profileDescription\" : \"\",\n  \"type\" : \"DISCOVERY\","
                                         "\n  \"updatedBy\" : null,\n  \"updateTime\" : 1617952521213,"
                                         "\n  \"credentials\" : [ {\n    \"type\" : \"STORAGE\",\n    \"authType\" : "
                                         "\"Basic\",\n    \"modified\" : false,\n    \"id\" : 44,"
                                         "\n    \"credentials\" : {\n      \"username\" : \"root\","
                                         "\n      \"password\" : null,\n      \"domain\" : null,\n      \"caCheck\" : "
                                         "false,\n      \"cnCheck\" : false,\n      \"certificateData\" : null,"
                                         "\n      \"certificateDetail\" : null,\n      \"port\" : 443,"
                                         "\n      \"retries\" : 3,\n      \"timeout\" : 60,\n      \"isHttp\" : "
                                         "false,\n      \"keepAlive\" : true,\n      \"version\" : null\n    }\n  } "
                                         "]\n}",
                    "DeviceType": [
                        5000
                    ]
                }
            ],
            "Schedule": {
                "RunNow": False,
                "RunLater": False,
                "Recurring": None,
                "Cron": "startnow",
                "StartTime": None,
                "EndTime": None
            },
            "TrapDestination": False,
            "CommunityString": False,
            "UseAllProfiles": False,
            "CreateGroup": True
        }
        discovery_modify_payload = {
            "DiscoveryConfigGroupName": "name1",
            "TrapDestination": True,
            "CommunityString": True,
            "Schedule": {
                "Cron": "startlater",
                "RunNow": False,

            }
        }
        self.module.update_modify_payload(discovery_modify_payload, current_payload)
        assert discovery_modify_payload["DiscoveryConfigGroupName"] == "name1"
        assert discovery_modify_payload["TrapDestination"] is True
        assert discovery_modify_payload["CommunityString"] is True
        assert discovery_modify_payload["Schedule"]["Cron"] == "startlater"
        assert discovery_modify_payload["Schedule"]["RunNow"] is False
