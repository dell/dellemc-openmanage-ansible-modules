# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.0.0
# Copyright (C) 2019-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json

import pytest
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.modules import ome_application_network_time
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


@pytest.fixture
def ome_connection_mock_for_application_network_time(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'ome_application_network_time.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    ome_connection_mock_obj.get_all_report_details.return_value = {"report_list": []}
    return ome_connection_mock_obj


class TestOmeTemplate(FakeAnsibleModule):
    module = ome_application_network_time

    sub_param1 = {"enable_ntp": False, "time_zone": "TZ_ID_3"}
    sub_param2 = {"enable_ntp": False, "system_time": "2020-03-31 21:35:19"}
    sub_param3 = {"enable_ntp": False, "time_zone": "TZ_ID_3", "system_time": "2020-03-31 21:35:19"}

    @pytest.mark.parametrize("param1", [sub_param2, sub_param3])
    def test_ome_application_network_time_main_enable_ntp_false_success_case_01(self, mocker, ome_default_args, param1,
                                                                                ome_connection_mock_for_application_network_time,
                                                                                ome_response_mock):
        ome_default_args.update(param1)
        mocker.patch(MODULE_PATH + "ome_application_network_time.validate_input")
        mocker.patch(MODULE_PATH + "ome_application_network_time.validate_time_zone")
        mocker.patch(MODULE_PATH + "ome_application_network_time.get_payload", return_value={"key": "val"})
        mocker.patch(MODULE_PATH + "ome_application_network_time.get_updated_payload", return_value={"key": "val"})
        time_data = {
            "EnableNTP": False,
            "JobId": None,
            "PrimaryNTPAddress": None,
            "SecondaryNTPAddress1": None,
            "SecondaryNTPAddress2": None,
            "SystemTime": None,
            "TimeSource": "Local Clock",
            "TimeZone": "TZ_ID_3",
            "TimeZoneIdLinux": None,
            "TimeZoneIdWindows": None,
            "UtcTime": None
        }
        ome_response_mock.json_data = time_data
        result = self.execute_module(ome_default_args)
        assert result['changed'] is True
        assert "msg" in result
        assert "time_configuration" in result and result["time_configuration"] == time_data
        assert result["msg"] == "Successfully configured network time."

    @pytest.mark.parametrize("param1", [{"enable_ntp": True, "time_zone": "TZ_ID_66"}])
    @pytest.mark.parametrize("param2", [{"primary_ntp_address": "192.168.0.2"},
                                        {"secondary_ntp_address1": "192.168.0.3"},
                                        {"secondary_ntp_address2": "192.168.0.4"},
                                        {"primary_ntp_address": "192.168.0.2", "secondary_ntp_address1": "192.168.0.3"},
                                        {"primary_ntp_address": "192.168.0.2", "secondary_ntp_address2": "192.168.0.4"},
                                        {"primary_ntp_address": "192.168.0.2", "secondary_ntp_address1": "192.168.0.3",
                                         "secondary_ntp_address2": "192.168.0.4"}
                                        ])
    def test_ome_application_network_time_main_enable_ntp_true_success_case_01(self, mocker, ome_default_args, param1,
                                                                               param2,
                                                                               ome_connection_mock_for_application_network_time,
                                                                               ome_response_mock):
        ome_default_args.update(param1)
        ome_default_args.update(param2)
        mocker.patch(MODULE_PATH + "ome_application_network_time.validate_input")
        mocker.patch(MODULE_PATH + "ome_application_network_time.validate_time_zone")
        mocker.patch(MODULE_PATH + "ome_application_network_time.get_payload", return_value={"key": "val"})
        mocker.patch(MODULE_PATH + "ome_application_network_time.get_updated_payload", return_value={"key": "val"})
        time_data = {
            "EnableNTP": True,
            "JobId": None,
            "PrimaryNTPAddress": "192.168.0.2",
            "SecondaryNTPAddress1": "192.168.0.3",
            "SecondaryNTPAddress2": "192.168.0.4",
            "SystemTime": None,
            "TimeSource": "10.136.112.222",
            "TimeZone": "TZ_ID_66",
            "TimeZoneIdLinux": None,
            "TimeZoneIdWindows": None,
            "UtcTime": None
        }
        ome_response_mock.json_data = time_data
        result = self.execute_module(ome_default_args)
        assert result['changed'] is True
        assert "msg" in result
        assert "time_configuration" in result and result["time_configuration"] == time_data
        assert result["msg"] == "Successfully configured network time."

    sub_param1 = {
        "param": {"enable_ntp": True, "primary_ntp_address": "255.0.0.0", "system_time": "2020-03-31 21:35:19"}, "msg":
            'parameters are mutually exclusive: system_time|primary_ntp_address'}
    sub_param2 = {"param": {}, "msg": 'missing required arguments: enable_ntp'}
    sub_param3 = {"param": {"enable_ntp": False},
                  "msg": "enable_ntp is False but any of the following are missing: time_zone, system_time"}
    sub_param4 = {"param": {"enable_ntp": True},
                  "msg": "enable_ntp is True but any of the following are missing:"
                         " time_zone, primary_ntp_address, secondary_ntp_address1, secondary_ntp_address2"}
    sub_param5 = {
        "param": {
            "enable_ntp": False,
            "primary_ntp_address": "10.136.112.220"
        },
        "msg": "enable_ntp is False but any of the following are missing:"
               " time_zone, system_time"
    }
    sub_param6 = {
        "param": {
            "enable_ntp": False,
            "secondary_ntp_address1": "10.136.112.220",
            "system_time": "2020-03-31 21:35:19"
        },
        "msg": "parameters are mutually exclusive: system_time|secondary_ntp_address1"
    }
    sub_param7 = {
        "param": {
            "enable_ntp": False,
            "secondary_ntp_address2": "10.136.112.220",
            "system_time": "2020-03-31 21:35:19"
        },
        "msg": "parameters are mutually exclusive: system_time|secondary_ntp_address2"
    }
    sub_param8 = {"param": {"enable_ntp": False, "primary_ntp_address": "10.136.112.220",
                            "secondary_ntp_address1": "10.136.112.220", "system_time": "2020-03-31 21:35:19"},
                  "msg": "parameters are mutually exclusive: system_time|primary_ntp_address,"
                         " system_time|secondary_ntp_address1"}
    sub_param9 = {
        "param": {"enable_ntp": False, "system_time": "2020-03-31 21:35:19", "primary_ntp_address": "10.136.112.220",
                  "secondary_ntp_address2": "10.136.112.220"},
        "msg": "parameters are mutually exclusive: system_time|primary_ntp_address, system_time|secondary_ntp_address2"}
    sub_param10 = {
        "param": {"enable_ntp": False, "system_time": "2020-03-31 21:35:19", "primary_ntp_address": "10.136.112.220",
                  "secondary_ntp_address2": "10.136.112.220", "secondary_ntp_address1": "10.136.112.220"},
        "msg": "parameters are mutually exclusive: system_time|primary_ntp_address,"
               " system_time|secondary_ntp_address1, system_time|secondary_ntp_address2"}
    sub_param11 = {
        "param": {"enable_ntp": False, "primary_ntp_address": "255.0.0.0", "system_time": "2020-03-31 21:35:19"},
        "msg": 'parameters are mutually exclusive: system_time|primary_ntp_address'}

    @pytest.mark.parametrize("param",
                             [sub_param1, sub_param2, sub_param3, sub_param4, sub_param5, sub_param6, sub_param7,
                              sub_param8,
                              sub_param9, sub_param10, sub_param11])
    def test_ome_application_network_time_main_failure_case_01(self, mocker, ome_default_args, param,
                                                               ome_connection_mock_for_application_network_time,
                                                               ome_response_mock):
        sub_param = param["param"]
        msg = param["msg"]
        ome_default_args.update(sub_param)
        result = self._run_module_with_fail_json(ome_default_args)
        assert result["msg"] == msg
        assert "time_configuration" not in result
        assert result["failed"] is True

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_application_network_time_main_success_exception_case3(self, exc_type, mocker, ome_default_args,
                                                                       ome_connection_mock_for_application_network_time,
                                                                       ome_response_mock):
        mocker.patch(MODULE_PATH + "ome_application_network_time.validate_time_zone")
        ome_default_args.update({"enable_ntp": False, "system_time": "2020-03-31 21:35:18"})
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'ome_application_network_time.get_payload', side_effect=URLError('TESTS'))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
            assert 'TESTS' in result['msg']
            assert result['changed'] is False
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'ome_application_network_time.get_payload',
                         side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'ome_application_network_time.get_payload',
                         side_effect=exc_type('http://testhost.com', 400,
                                              'http error message',
                                              {"accept-type": "application/json"},
                                              StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'time_configuration' not in result
        assert 'msg' in result

    def test_remove_unwanted_keys_default_keys_time(self, ome_default_args):
        removable_keys = list(ome_default_args.keys())
        new_param = {
            "enable_ntp": True,
            "time_zone": "TimeZone",
            "primary_ntp_address": "192.168.0.2",
            "secondary_ntp_address1": "192.168.0.3",
            "secondary_ntp_address2": "192.168.0.4"
        }
        ome_default_args.update(new_param)
        self.module.remove_unwanted_keys(removable_keys, ome_default_args)
        assert len(set(new_param.keys()) - set(ome_default_args.keys())) == 0

    def test_remove_unwanted_keys_unwanted_keys_time(self):
        """when key not exists should not throw error"""
        current_setting = {"@odata.context": "/api/$metadata#Network.TimeConfiguration",
                           "@odata.type": "#Network.TimeConfiguration",
                           "@odata.id": "/api/ApplicationService/Network/TimeConfiguration", "TimeZone": "TZ_ID_1",
                           "TimeZoneIdLinux": "Etc/GMT+12", "TimeZoneIdWindows": "Dateline Standard Time",
                           "EnableNTP": False, "PrimaryNTPAddress": None, "SecondaryNTPAddress1": None,
                           "SecondaryNTPAddress2": None, "SystemTime": "2020-03-31 21:37:08.897",
                           "TimeSource": "Local Clock", "UtcTime": "2020-04-01 09:37:08.897"}
        removable_keys = ["@odata.context", "@odata.type", "@odata.id", "TimeZoneIdLinux", "TimeZoneIdWindows",
                          "TimeSource", "UtcTime"]
        self.module.remove_unwanted_keys(removable_keys, current_setting)
        assert current_setting == {"TimeZone": "TZ_ID_1", "EnableNTP": False, "PrimaryNTPAddress": None,
                                   "SecondaryNTPAddress1": None, "SecondaryNTPAddress2": None,
                                   "SystemTime": "2020-03-31 21:37:08.897"}

    def test_get_payload_time_case1(self, ome_default_args):
        new_param = {
            "enable_ntp": False,
            "primary_ntp_address": None,
            "secondary_ntp_address1": None,
            "secondary_ntp_address2": None,
            "system_time": "2020-03-31 21:35:19",
            "time_zone": "TZ_ID_1",
        }
        ome_default_args.update(new_param)
        f_module = self.get_module_mock(params=ome_default_args)
        payload = self.module.get_payload(f_module)
        assert f_module.params == ome_default_args
        assert payload == {"EnableNTP": False, "TimeZone": "TZ_ID_1", "SystemTime": "2020-03-31 21:35:19"}

    def test_get_payload_time_case2(self, ome_default_args):
        new_param = {
            "enable_ntp": True,
            "primary_ntp_address": "10.136.112.220",
            "secondary_ntp_address1": "10.136.112.221",
            "secondary_ntp_address2": "10.136.112.222",
            "system_time": None,
            "time_zone": "TZ_ID_66"
        }
        ome_default_args.update(new_param)
        f_module = self.get_module_mock(params=ome_default_args)
        payload = self.module.get_payload(f_module)
        assert ome_default_args == {
            "enable_ntp": True,
            "primary_ntp_address": "10.136.112.220",
            "secondary_ntp_address1": "10.136.112.221",
            "secondary_ntp_address2": "10.136.112.222",
            "system_time": None,
            "time_zone": "TZ_ID_66",
            "hostname": "192.168.0.1",
            "username": "username",
            "password": "password",
            "ca_path": "/path/ca_bundle"}
        assert payload == {"EnableNTP": True, "TimeZone": "TZ_ID_66", "PrimaryNTPAddress": "10.136.112.220",
                           "SecondaryNTPAddress1": "10.136.112.221",
                           "SecondaryNTPAddress2": "10.136.112.222"
                           }

    def test_get_updated_payload_success_case(self, ome_default_args, ome_connection_mock_for_application_network_time,
                                              ome_response_mock):
        current_setting = {"@odata.context": "/api/$metadata#Network.TimeConfiguration",
                           "@odata.type": "#Network.TimeConfiguration",
                           "@odata.id": "/api/ApplicationService/Network/TimeConfiguration", "TimeZone": "TZ_ID_02",
                           "TimeZoneIdLinux": "Asia/Colombo", "TimeZoneIdWindows": "Sri Lanka Standard Time",
                           "EnableNTP": True, "PrimaryNTPAddress": "10.136.112.220",
                           "SecondaryNTPAddress1": "10.136.112.221", "SecondaryNTPAddress2": "10.136.112.222",
                           "SystemTime": "2020-04-01 15:39:23.825", "TimeSource": "10.136.112.222",
                           "UtcTime": "2020-04-01 10:09:23.825"}
        payload = {"EnableNTP": True, "TimeZone": "TZ_ID_66",
                   "SecondaryNTPAddress1": "10.136.112.02",
                   "SecondaryNTPAddress2": "10.136.112.03"
                   }
        f_module = self.get_module_mock(params=ome_default_args)
        ome_response_mock.json_data = current_setting
        setting = self.module.get_updated_payload(ome_connection_mock_for_application_network_time,
                                                  f_module, payload)
        expected_payload = {"EnableNTP": True, "TimeZone": "TZ_ID_66",
                            "SecondaryNTPAddress1": "10.136.112.02",
                            "SecondaryNTPAddress2": "10.136.112.03",
                            "PrimaryNTPAddress": "10.136.112.220",  # updated not given key from current_setting
                            "SystemTime": "2020-04-01 15:39:23.825",  # system will be ignore from ome
                            }
        assert setting == expected_payload

    def test_get_updated_payload_check_mode_success_case1(self, ome_default_args,
                                                          ome_connection_mock_for_application_network_time,
                                                          ome_response_mock):
        current_setting = {"@odata.context": "/api/$metadata#Network.TimeConfiguration",
                           "@odata.type": "#Network.TimeConfiguration",
                           "@odata.id": "/api/ApplicationService/Network/TimeConfiguration",
                           "TimeZone": "TZ_ID_02", "TimeZoneIdLinux": "Asia/Colombo",
                           "TimeZoneIdWindows": "Sri Lanka Standard Time",
                           "EnableNTP": True,
                           "PrimaryNTPAddress": "10.136.112.220",
                           "SecondaryNTPAddress1": "10.136.112.221",
                           "SecondaryNTPAddress2": "10.136.112.222",
                           "SystemTime": "2020-04-01 15:39:23.825",
                           "TimeSource": "10.136.112.222", "UtcTime": "2020-04-01 10:09:23.825"}
        payload = {"EnableNTP": True, "TimeZone": "TZ_ID_02",
                   "PrimaryNTPAddress": "10.136.112.220",
                   "SecondaryNTPAddress1": "10.136.112.221",
                   "SecondaryNTPAddress2": "10.136.112.222"
                   }
        ome_response_mock.json_data = current_setting
        check_mode_no_diff_msg = "No changes found to be applied to the time configuration."
        f_module = self.get_module_mock(params=ome_default_args, check_mode=True)
        with pytest.raises(Exception, match=check_mode_no_diff_msg):
            self.module.get_updated_payload(ome_connection_mock_for_application_network_time,
                                            f_module, payload)

    def test_get_updated_payload_check_mode_success_case2(self, ome_default_args,
                                                          ome_connection_mock_for_application_network_time,
                                                          ome_response_mock):
        current_setting = {"@odata.context": "/api/$metadata#Network.TimeConfiguration",
                           "@odata.type": "#Network.TimeConfiguration",
                           "@odata.id": "/api/ApplicationService/Network/TimeConfiguration",
                           "TimeZone": "TZ_ID_02", "TimeZoneIdLinux": "Asia/Colombo",
                           "TimeZoneIdWindows": "Sri Lanka Standard Time",
                           "EnableNTP": True,
                           "PrimaryNTPAddress": "10.136.112.220",
                           "SecondaryNTPAddress1": "10.136.112.221",
                           "SecondaryNTPAddress2": "10.136.112.222",
                           "SystemTime": "2020-04-01 15:39:23.825",
                           "TimeSource": "10.136.112.222", "UtcTime": "2020-04-01 10:09:23.825"}
        payload = {"EnableNTP": True, "PrimaryNTPAddress": "10.136.112.220"}
        ome_response_mock.json_data = current_setting
        check_mode_no_diff_msg = "No changes found to be applied to the time configuration."
        f_module = self.get_module_mock(params=ome_default_args, check_mode=True)
        with pytest.raises(Exception, match=check_mode_no_diff_msg) as err:
            self.module.get_updated_payload(ome_connection_mock_for_application_network_time,
                                            f_module, payload)

    def test_get_updated_payload_check_mode_success_case3(self, ome_default_args,
                                                          ome_connection_mock_for_application_network_time,
                                                          ome_response_mock):
        current_setting = {"@odata.context": "/api/$metadata#Network.TimeConfiguration",
                           "@odata.type": "#Network.TimeConfiguration",
                           "@odata.id": "/api/ApplicationService/Network/TimeConfiguration",
                           "TimeZone": "TZ_ID_02", "TimeZoneIdLinux": "Asia/Colombo",
                           "TimeZoneIdWindows": "Sri Lanka Standard Time",
                           "EnableNTP": True,
                           "PrimaryNTPAddress": "10.136.112.220",
                           "SecondaryNTPAddress1": "10.136.112.221",
                           "SecondaryNTPAddress2": "10.136.112.222",
                           "SystemTime": "2020-04-01 15:39:23.825",
                           "TimeSource": "10.136.112.222", "UtcTime": "2020-04-01 10:09:23.825"}
        payload = {"EnableNTP": True, "PrimaryNTPAddress": "10.136.112.221"}  # change in value
        ome_response_mock.json_data = current_setting
        check_mode_no_diff_msg = "Changes found to be applied to the time configuration."
        f_module = self.get_module_mock(params=ome_default_args, check_mode=True)
        with pytest.raises(Exception, match=check_mode_no_diff_msg):
            self.module.get_updated_payload(ome_connection_mock_for_application_network_time,
                                            f_module, payload)

    def test_get_updated_payload_without_check_mode_success_case(self, ome_default_args,
                                                                 ome_connection_mock_for_application_network_time,
                                                                 ome_response_mock):
        """without check even there is no difference no exception thrown"""
        current_setting = {"@odata.context": "/api/$metadata#Network.TimeConfiguration",
                           "@odata.type": "#Network.TimeConfiguration",
                           "@odata.id": "/api/ApplicationService/Network/TimeConfiguration",
                           "TimeZone": "TZ_ID_02", "TimeZoneIdLinux": " Asia/Colombo",
                           "TimeZoneIdWindows": "Sri Lanka Standard Time",
                           "EnableNTP": True,
                           "PrimaryNTPAddress": "10.136.112.220",
                           "SecondaryNTPAddress1": "10.136.112.221",
                           "SecondaryNTPAddress2": "10.136.112.222",
                           "SystemTime": "2020-04-01 15:39:23.825",
                           "TimeSource": "10.136.112.222", "UtcTime": "2020-04-01 10:09:23.825"}
        payload = {'EnableNTP': True,
                   'PrimaryNTPAddress': '10.136.112.220',
                   'SecondaryNTPAddress1': '10.136.112.221',
                   'SecondaryNTPAddress2': '10.136.112.222',
                   'SystemTime': '2020-04-01 15:39:23.826',
                   'TimeZone': 'TZ_ID_02'}
        ome_response_mock.json_data = current_setting
        f_module = self.get_module_mock(params=ome_default_args, check_mode=False)
        current_setting = self.module.get_updated_payload(ome_connection_mock_for_application_network_time,
                                                          f_module, payload)
        assert current_setting == payload

    @pytest.mark.parametrize("time_zone_val", ["", 0, "invalid", "TZ_ID_100001"])
    def test_validate_time_zone_failure_case01(self, ome_default_args, time_zone_val, ome_response_mock,
                                               ome_connection_mock_for_application_network_time):
        param = {"time_zone": time_zone_val}
        ome_default_args.update(param)
        f_module = self.get_module_mock(params=ome_default_args)
        ome_response_mock.json_data = {"@odata.context": "/api/$metadata#Collection(Network.TimeZone)",
                                       "@odata.count": 3,
                                       "value": [{"@odata.type": "#Network.TimeZone", "Utcoffsetminutes": 60,
                                                  "Id": "TZ_ID_38", "Name":
                                                      "(GMT+01:00) Brussels, Copenhagen, Madrid, Paris"},
                                                 {"@odata.type": "#Network.TimeZone", "Utcoffsetminutes": 60,
                                                  "Id": "TZ_ID_39", "Name":
                                                      "(GMT+01:00) Sarajevo, Skopje, Warsaw, Zagreb"},
                                                 {"@odata.type": "#Network.TimeZone", "Utcoffsetminutes": 360,
                                                  "Id": "TZ_ID_70", "Name": "(GMT+06:00) Novosibirsk"}]}
        msg = "Provide valid time zone.Choices are TZ_ID_38,TZ_ID_39,TZ_ID_70"
        with pytest.raises(Exception, match=msg):
            self.module.validate_time_zone(f_module, ome_connection_mock_for_application_network_time)

    def test_validate_time_zone_successcase01(self, ome_default_args, ome_response_mock,
                                              ome_connection_mock_for_application_network_time):
        param = {"time_zone": "TZ_ID_38"}
        ome_default_args.update(param)
        f_module = self.get_module_mock(params=ome_default_args)
        ome_response_mock.json_data = {"@odata.context": "/api/$metadata#Collection(Network.TimeZone)",
                                       "@odata.count": 3,
                                       "value": [{"@odata.type": "#Network.TimeZone", "Utcoffsetminutes": 60,
                                                  "Id": "TZ_ID_38",
                                                  "Name": "(GMT+01:00) Brussels, Copenhagen, Madrid, Paris"},
                                                 {"@odata.type": "#Network.TimeZone", "Utcoffsetminutes": 60,
                                                  "Id": "TZ_ID_39",
                                                  "Name": "(GMT+01:00) Sarajevo, Skopje, Warsaw, Zagreb"},
                                                 {"@odata.type": "#Network.TimeZone", "Utcoffsetminutes": 360,
                                                  "Id": "TZ_ID_70", "Name": "(GMT+06:00) Novosibirsk"}]}
        self.module.validate_time_zone(f_module, ome_connection_mock_for_application_network_time)
        assert ome_connection_mock_for_application_network_time.invoke_request.called

    def test_validate_time_zone_successcase02(self, ome_default_args, ome_response_mock,
                                              ome_connection_mock_for_application_network_time):
        param = {"enable_ntp": True}
        ome_default_args.update(param)
        f_module = self.get_module_mock(params=ome_default_args)
        self.module.validate_time_zone(f_module, ome_connection_mock_for_application_network_time)
        assert not ome_connection_mock_for_application_network_time.invoke_request.called

    def test_validate_time_zone_successcase03(self, ome_default_args, ome_response_mock,
                                              ome_connection_mock_for_application_network_time):
        param = {"time_zone": None}
        ome_default_args.update(param)
        f_module = self.get_module_mock(params=ome_default_args)
        self.module.validate_time_zone(f_module, ome_connection_mock_for_application_network_time)
        assert not ome_connection_mock_for_application_network_time.invoke_request.called

    def test_validate_input_time_enable_true_case_01(self, ome_default_args):
        params = {"enable_ntp": True, "system_time": "2020-04-01 15:39:23.825"}
        ome_default_args.update(params)
        f_module = self.get_module_mock(params=ome_default_args)
        msg = 'When enable NTP is true,the option system time is not accepted.'
        with pytest.raises(Exception) as exc:
            self.module.validate_input(f_module)
        assert exc.value.args[0] == msg

    @pytest.mark.parametrize("sub_param", [
        {"primary_ntp_address": "192.168.02.1", "secondary_ntp_address1": "192.168.02.3",
         "secondary_ntp_address2": "192.168.02.2"},
        {"secondary_ntp_address1": "192.168.02.1"},
        {"secondary_ntp_address2": "192.168.02.1"},
        {"primary_ntp_address": "192.168.02.1", "time_zone": "TZ_01"},
        {"primary_ntp_address": "192.168.02.1"},
        {"secondary_ntp_address1": "192.168.02.1", "time_zone": "TZ_01"},
    ])
    def test_validate_input_time_enable_false_case_01(self, ome_default_args, sub_param):
        params = {"enable_ntp": False}
        params.update(sub_param)
        ome_default_args.update(params)
        f_module = self.get_module_mock(params=ome_default_args)
        msg = "When enable NTP is false,the option(s) primary_ntp_address, secondary_ntp_address1 and secondary_ntp_address2 is not accepted."
        with pytest.raises(Exception) as exc:
            self.module.validate_input(f_module)
        assert exc.value.args[0] == msg

    @pytest.mark.parametrize("sub_param", [{"time_zone": "TZ_01"}, {"primary_ntp_address": "192.168.02.1"},
                                           {"secondary_ntp_address1": "192.168.02.1"},
                                           {"secondary_ntp_address2": "192.168.02.1"},
                                           {"primary_ntp_address": "192.168.02.1", "time_zone": "TZ_01"}, {}
                                           ])
    def test_validate_input_time_enable_true_case_04(self, ome_default_args, sub_param):
        """
            exception should not be raised
        """
        params = {"enable_ntp": True}
        params.update(sub_param)
        ome_default_args.update(params)
        f_module = self.get_module_mock(params=ome_default_args)
        self.module.validate_input(f_module)

    @pytest.mark.parametrize("sub_param", [{"time_zone": "TZI_01"}, {"system_time": "2020-04-01 15:39:23.825"},
                                           {"time_zone": "TZI_01", "system_time": "2020-04-01 15:39:23.825"}, {}])
    def test_validate_input_time_enable_false_case_03(self, ome_default_args, sub_param):
        """success case. if required options passed no exception thrown"""
        params = {"enable_ntp": False}
        params.update(sub_param)
        ome_default_args.update(params)
        f_module = self.get_module_mock(params=ome_default_args)
        self.module.validate_input(f_module)

    def test_get_updated_payload_non_check_mode_success_case1(self, ome_default_args,
                                                              ome_connection_mock_for_application_network_time,
                                                              ome_response_mock):
        current_setting = {"@odata.context": "/api/$metadata#Network.TimeConfiguration",
                           "@odata.type": "#Network.TimeConfiguration",
                           "@odata.id": "/api/ApplicationService/Network/TimeConfiguration",
                           "TimeZone": "TZ_ID_02", "TimeZoneIdLinux": "Asia/Colombo",
                           "TimeZoneIdWindows": "Sri Lanka Standard Time",
                           "EnableNTP": True,
                           "PrimaryNTPAddress": "10.136.112.220",
                           "SecondaryNTPAddress1": "10.136.112.221",
                           "SecondaryNTPAddress2": "10.136.112.222",
                           "SystemTime": "2020-04-01 15:39:23.825",
                           "TimeSource": "10.136.112.222", "UtcTime": "2020-04-01 10:09:23.825"}
        payload = {"EnableNTP": True, "TimeZone": "TZ_ID_02",
                   "PrimaryNTPAddress": "10.136.112.220",
                   "SecondaryNTPAddress1": "10.136.112.221",
                   "SecondaryNTPAddress2": "10.136.112.222"
                   }
        ome_response_mock.json_data = current_setting
        check_mode_no_diff_msg = "No changes made to the time configuration as the entered values are the same as the current configuration."
        f_module = self.get_module_mock(params=ome_default_args, check_mode=False)
        with pytest.raises(Exception, match=check_mode_no_diff_msg):
            self.module.get_updated_payload(ome_connection_mock_for_application_network_time,
                                            f_module, payload)

    def test_get_updated_payload_non_check_mode_success_case2(self, ome_default_args,
                                                              ome_connection_mock_for_application_network_time,
                                                              ome_response_mock):
        current_setting = {"@odata.context": "/api/$metadata#Network.TimeConfiguration",
                           "@odata.type": "#Network.TimeConfiguration",
                           "@odata.id": "/api/ApplicationService/Network/TimeConfiguration",
                           "TimeZone": "TZ_ID_02", "TimeZoneIdLinux": "Asia/Colombo",
                           "TimeZoneIdWindows": "Sri Lanka Standard Time",
                           "EnableNTP": True,
                           "PrimaryNTPAddress": "10.136.112.220",
                           "SecondaryNTPAddress1": "10.136.112.221",
                           "SecondaryNTPAddress2": "10.136.112.222",
                           "SystemTime": "2020-04-01 15:39:23.825",
                           "TimeSource": "10.136.112.222", "UtcTime": "2020-04-01 10:09:23.825"}
        payload = {"EnableNTP": True, "PrimaryNTPAddress": "10.136.112.220"}
        ome_response_mock.json_data = current_setting
        check_mode_no_diff_msg = "No changes made to the time configuration as the entered values are the same as the current configuration."
        f_module = self.get_module_mock(params=ome_default_args, check_mode=False)
        with pytest.raises(Exception, match=check_mode_no_diff_msg) as err:
            self.module.get_updated_payload(ome_connection_mock_for_application_network_time,
                                            f_module, payload)

    def test_update_time_config_output(self):
        backup_setting = {"@odata.context": "/api/$metadata#Network.TimeConfiguration",
                          "@odata.type": "#Network.TimeConfiguration",
                          "@odata.id": "/api/ApplicationService/Network/TimeConfiguration",
                          "TimeZone": "TZ_ID_1",
                          "TimeZoneIdLinux": "Etc/GMT+12",
                          "TimeZoneIdWindows": "Dateline Standard Time",
                          "EnableNTP": False,
                          "PrimaryNTPAddress": None,
                          "SecondaryNTPAddress1": None,
                          "SecondaryNTPAddress2": None,
                          "SystemTime": "2020-03-31 21:37:08.897",
                          "TimeSource": "Local Clock",
                          "UtcTime": "2020-04-01 09:37:08.897"}
        self.module.update_time_config_output(backup_setting)
        assert backup_setting == {
            "EnableNTP": False,
            "JobId": None,
            "PrimaryNTPAddress": None,
            "SecondaryNTPAddress1": None,
            "SecondaryNTPAddress2": None,
            "SystemTime": "2020-03-31 21:37:08.897",
            "TimeSource": "Local Clock",
            "TimeZone": "TZ_ID_1",
            "TimeZoneIdLinux": "Etc/GMT+12",
            "TimeZoneIdWindows": "Dateline Standard Time",
            "UtcTime": "2020-04-01 09:37:08.897"}
