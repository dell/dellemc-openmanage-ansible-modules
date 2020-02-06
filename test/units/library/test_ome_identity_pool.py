# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0.8
# Copyright (C) 2020 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

from __future__ import absolute_import

import pytest
from ansible.modules.remote_management.dellemc import ome_identity_pool
from units.modules.remote_management.dellemc.common import FakeAnsibleModule, Constants
from units.compat.mock import MagicMock
from units.modules.remote_management.dellemc.common import AnsibleFailJSonException
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from units.modules.utils import AnsibleExitJson
from ssl import SSLError
from io import StringIO
from ansible.module_utils._text import to_text
import json


@pytest.fixture
def ome_connection_mock_for_identity_pool(mocker, ome_response_mock):
    connection_class_mock = mocker.patch('ansible.modules.remote_management.dellemc.ome_identity_pool.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOMeIdentityPool(FakeAnsibleModule):
    module = ome_identity_pool

    def test_main_ome_identity_pool_success_case1(self, mocker, ome_default_args,
                                                  ome_connection_mock_for_identity_pool, ome_response_mock):
        sub_param = {"pool_name":  "pool1",
                     "pool_description": "Identity pool with ethernet and fcoe settings",
                     "ethernet_settings": {
                         "starting_mac_address": "50-50-50-50-50-00",
                         "identity_count": 60},
                     "fcoe_settings": {
                         "starting_mac_address":  "70-70-70-70-70-00",
                         "identity_count": 75
                     }}
        message_return = {"msg": "Successfully created an identity pool.",
                          "result": {"Id": 36, "IsSuccessful": True, "Issues": []}}
        mocker.patch('ansible.modules.remote_management.dellemc.ome_identity_pool.pool_create_modify', return_value=message_return)
        ome_default_args.update(sub_param)
        result = self._run_module(ome_default_args)
        assert result['changed'] is True
        assert 'pool_status' in result and "msg" in result
        assert result["msg"] == "Successfully created an identity pool."
        assert result['pool_status'] == {
                "Id": 36,
                "IsSuccessful": True,
                "Issues": []
            }

    @pytest.mark.parametrize("exc_type", [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_main_ome_identity_pool_failure_case1(self, exc_type, mocker, ome_default_args,
                                                  ome_connection_mock_for_identity_pool, ome_response_mock):
        ome_default_args.update({"pool_name": "pool1"})
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch('ansible.modules.remote_management.dellemc.ome_identity_pool.pool_create_modify', side_effect=exc_type("urlopen error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch('ansible.modules.remote_management.dellemc.ome_identity_pool.pool_create_modify', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch('ansible.modules.remote_management.dellemc.ome_identity_pool.pool_create_modify',
                         side_effect=exc_type('http://testhost.com', 400,
                                              'http error message',
                                              {"accept-type": "application/json"},
                                              StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'pool_status' not in result
        assert 'msg' in result

    def test_main_ome_identity_pool_no_mandatory_arg_passed_failure_case(self, ome_default_args, ome_connection_mock_for_identity_pool):
        result = self._run_module_with_fail_json(ome_default_args)
        assert 'pool_status' not in result

    @pytest.mark.parametrize("param", [{"ethernet_settings": {"invalid_key": "value"}},
                                       {"fcoe_settings": {"invalid_key": "value"}},
                                       {"name": "name1"}])
    def test_main_ome_identity_pool_invalid_settings(self, param, ome_default_args, ome_connection_mock_for_identity_pool):
        ome_default_args.update(param)
        result = self._run_module_with_fail_json(ome_default_args)
        assert 'pool_status' not in result

    @pytest.mark.parametrize("action", ["create", "modify"])
    def test_get_success_message(self, action):
        json_data = {
                "Id": 36,
                "IsSuccessful": True,
                "Issues": []
            }
        message = self.module.get_success_message(action, json_data)
        if action == "create":
            assert message["msg"] == "Successfully created an identity pool."
        else:
            assert message["msg"] == "Successfully modified the identity pool."
        assert message["result"] == {
                "Id": 36,
                "IsSuccessful": True,
                "Issues": []
            }

    def test_pool_create_modify_success_case_01(self, mocker, ome_connection_mock_for_identity_pool, ome_response_mock):
        params = {"pool_name": "pool_name"}
        mocker.patch('ansible.modules.remote_management.dellemc.ome_identity_pool.get_identity_pool_id_by_name', return_value=(10, {"paylaod": "value"}))
        mocker.patch('ansible.modules.remote_management.dellemc.ome_identity_pool.get_payload', return_value={"Name": "name"})
        mocker.patch('ansible.modules.remote_management.dellemc.ome_identity_pool.get_success_message',
                     return_value={"msg": "Successfully modified the identity pool"})
        mocker.patch('ansible.modules.remote_management.dellemc.ome_identity_pool.update_modify_payload')
        mocker.patch('ansible.modules.remote_management.dellemc.ome_identity_pool.compare_nested_dict', return_value=False)
        f_module = self.get_module_mock(params=params)
        message = self.module.pool_create_modify(f_module, ome_connection_mock_for_identity_pool)
        assert message == {"msg": "Successfully modified the identity pool"}

    def test_pool_create_modify_success_case_02(self, mocker, ome_connection_mock_for_identity_pool, ome_response_mock):
        params = {"pool_name": "pool_name"}
        mocker.patch('ansible.modules.remote_management.dellemc.ome_identity_pool.get_identity_pool_id_by_name', return_value=(0, None))
        mocker.patch('ansible.modules.remote_management.dellemc.ome_identity_pool.get_payload', return_value={"Name": "name"})
        mocker.patch('ansible.modules.remote_management.dellemc.ome_identity_pool.get_success_message',
                     return_value={"msg": "Successfully created an identity pool"})
        f_module = self.get_module_mock(params=params)
        message = self.module.pool_create_modify(f_module, ome_connection_mock_for_identity_pool)
        assert message == {"msg": "Successfully created an identity pool"}

    def test_pool_create_modify_success_case_03(self, mocker, ome_connection_mock_for_identity_pool, ome_response_mock):
        params = {"pool_name": "pool_name"}
        mocker.patch('ansible.modules.remote_management.dellemc.ome_identity_pool.get_identity_pool_id_by_name', return_value=(10, {"payload":"value"}))
        mocker.patch('ansible.modules.remote_management.dellemc.ome_identity_pool.get_payload', return_value={"Name": "pool1"})
        mocker.patch('ansible.modules.remote_management.dellemc.ome_identity_pool.get_success_message',
                     return_value={"msg": "Successfully modified the identity pool"})
        mocker.patch('ansible.modules.remote_management.dellemc.ome_identity_pool.update_modify_payload')
        mocker.patch('ansible.modules.remote_management.dellemc.ome_identity_pool.compare_nested_dict', return_value=True)
        f_module = self.get_module_mock(params=params)
        with pytest.raises(Exception) as exc:
             self.module.pool_create_modify(f_module, ome_connection_mock_for_identity_pool)
        return exc.value.args[0] == "No changes are to be applied for specified pool name: pool1, as" \
                                    " requested setting values are the same as the current setting values."

    def test_pool_create_modify_error_case_01(self, mocker, ome_connection_mock_for_identity_pool, ome_response_mock):
        msg = "identity pool parameters are is not valid"
        params = {"pool_name": "pool_name"}
        mocker.patch('ansible.modules.remote_management.dellemc.ome_identity_pool.get_identity_pool_id_by_name', return_value=(0, None))
        mocker.patch('ansible.modules.remote_management.dellemc.ome_identity_pool.get_payload', return_value={"Name": "name"})
        f_module = self.get_module_mock(params=params)
        ome_connection_mock_for_identity_pool.invoke_request.side_effect = HTTPError('http://testhost.com', 404, json.dumps(msg), {}, None)
        with pytest.raises(Exception, match=msg) as exc:
            self.module.pool_create_modify(f_module, ome_connection_mock_for_identity_pool)

    def test_get_payload_create_case01(self):
        params = {"pool_name": "pool1",
                  "pool_description": "Identity pool with ethernet and fcoe settings",
                  "ethernet_settings": {
                      "starting_mac_address": "50-50-50-50-50-00",
                      "identity_count": 60},
                  "fcoe_settings": {
                      "starting_mac_address": "70-70-70-70-70-00",
                      "identity_count": 75
                  }
                  }
        f_module = self.get_module_mock(params=params)
        payload = self.module.get_payload(f_module)
        assert payload == {
            "Name": "pool1",
            "Description": "Identity pool with ethernet and fcoe settings",
            "EthernetSettings": {"Mac": {
                "StartingMacAddress": "UFBQUFAA",
                "IdentityCount": 60}},
            "FcoeSettings": {"Mac": {
                "StartingMacAddress": "cHBwcHAA",
                "IdentityCount": 75}},
        }

    def test_get_payload_create_case02(self):
        """new_pool_name should be ignored for create action"""
        params = {"pool_name": "pool1",
                  "new_pool_name": "pool2",
                  "pool_description": "Identity pool with ethernet and fcoe settings",
                  "ethernet_settings": {
                      "starting_mac_address": "50-50-50-50-50-00",
                      "identity_count": 60},
                  "fcoe_settings": {
                      "starting_mac_address": "70-70-70-70-70-00",
                      "identity_count": 75
                  }
                  }
        f_module = self.get_module_mock(params=params)
        payload = self.module.get_payload(f_module)
        assert payload == {
            "Name": "pool1",
            "Description": "Identity pool with ethernet and fcoe settings",
            "EthernetSettings": {"Mac": {
                "StartingMacAddress": "UFBQUFAA",
                "IdentityCount": 60}},
            "FcoeSettings": {"Mac": {
                "StartingMacAddress": "cHBwcHAA",
                "IdentityCount": 75}},
        }
        assert payload["Name"] == "pool1"

    def test_get_payload_modify_case03(self):
        """moify action Name should be updated with ne_pool_name and Id has to be updated"""
        params = {"pool_name": "pool1",
                  "new_pool_name": "pool2",
                  "pool_description": "Identity pool with ethernet and fcoe settings",
                  "ethernet_settings": {"starting_mac_address": "50-50-50-50-50-00",
                                        "identity_count": 60},
                  "fcoe_settings": {
                      "starting_mac_address": "70-70-70-70-70-00",
                      "identity_count": 75
                  }
                  }
        f_module = self.get_module_mock(params=params)
        payload = self.module.get_payload(f_module, 10)
        assert payload == {
            "Id": 10,
            "Name": "pool2",
            "Description": "Identity pool with ethernet and fcoe settings",
            "EthernetSettings": {"Mac": {
                "StartingMacAddress": "UFBQUFAA",
                "IdentityCount": 60}},
            "FcoeSettings": {"Mac": {
                "StartingMacAddress": "cHBwcHAA",
                "IdentityCount": 75}},
        }
        assert payload["Name"] == "pool2"
        assert payload["Id"] == 10

    def test_get_payload_modify_case04(self):
        """payload for only ethernet setting
        if ne_ppol_name not passed payload Name should be updated with I(pool_name)
        """
        params = {"pool_name": "pool1",
                  "pool_description": "Identity pool with ethernet and fcoe settings",
                  "ethernet_settings": {"starting_mac_address": "50-50-50-50-50-00",
                                        "identity_count": 60
                                        }
                  }
        f_module = self.get_module_mock(params=params)
        payload = self.module.get_payload(f_module, 10)
        assert payload["Name"] == "pool1"
        assert payload["Id"] == 10
        assert "FcoeSettings" not in payload
        assert "EthernetSettings" in payload
        assert payload == {'Description': 'Identity pool with ethernet and fcoe settings',
                           'Name': 'pool1',
                           'Id': 10,
                           'EthernetSettings': {
                               'Mac':
                                   {'StartingMacAddress': 'UFBQUFAA', 'IdentityCount': 60
                                    }
                           }
                           }

    def test_get_payload_create_case05(self):
        params = {"pool_name": "pool1",
                  "pool_description": "Identity pool with ethernet and fcoe settings",
                  "fcoe_settings": {"starting_mac_address": "70-70-70-70-70-00",
                                    "identity_count": 75
                                    }}
        f_module = self.get_module_mock(params=params)
        payload = self.module.get_payload(f_module)
        assert payload["Name"] == "pool1"
        assert "Id" not in payload
        assert "FcoeSettings" in payload
        assert "Ethernet_Settings" not in payload

    def test_get_payload_create_case06(self):
        # case when new_pool_name not passed
        params = {"pool_name": "pool1",
                  "pool_description": "Identity pool with ethernet and fcoe settings"}
        f_module = self.get_module_mock(params=params)
        payload = self.module.get_payload(f_module, 11)
        assert payload["Name"] == "pool1"
        assert "Id" in payload
        assert "FcoeSettings" not in payload
        assert "Ethernet_Settings" not in payload

    def test_get_payload_modify_case07(self):
        params = {"pool_name": "pool1", "new_pool_name": "pool2"}
        f_module = self.get_module_mock(params=params)
        payload = self.module.get_payload(f_module, 11)
        assert payload["Name"] == "pool2"
        assert payload["Id"] == 11
        assert "Description" not in payload
        assert "FcoeSettings" not in payload
        assert "Ethernet_Settings" not in payload

    def test_get_payload_modify_case08(self):
        """check case when I(new_pool_name) is empty string
        ome is accepting it"""
        params = {"pool_name": "pool1", "new_pool_name": ""}
        f_module = self.get_module_mock(params=params)
        payload = self.module.get_payload(f_module, 11)
        assert payload["Name"] == ""
        assert payload["Id"] == 11
        assert "Description" not in payload
        assert "FcoeSettings" not in payload
        assert "Ethernet_Settings" not in payload

    def test_update_ethernet_fcoe_settings_case_01(self):
        f_module = self.get_module_mock()
        settings_params = {"starting_mac_address": "70-70-70-70-70-00", "identity_count": 10}
        payload = {"Name": "pool1"}
        self.module.update_ethernet_fcoe_settings(payload, settings_params, "Ethernet_Settings", f_module)
        assert payload == {
            "Name": "pool1",
            "Ethernet_Settings": {"Mac": {"StartingMacAddress": "cHBwcHAA", "IdentityCount": 10}}
        }

    def test_update_ethernet_fcoe_settings_case_01(self):
        f_module = self.get_module_mock()
        settings_params = {"starting_mac_address": "70-70-70-70-70-xx", "identity_count": 10}
        payload = {"Name": "pool1"}
        with pytest.raises(Exception) as exc:
            self.module.update_ethernet_fcoe_settings(payload, settings_params, "Ethernet_Settings", f_module)
        return exc.value.args[0] == "please provide valid mac address format for ethernetsettings"


    def test_update_ethernet_fcoe_settings_case_02(self):
        """case when no sub settting exists"""
        settings_params = {}
        payload = {"Name": "pool1"}
        f_module = self.get_module_mock()
        self.module.update_ethernet_fcoe_settings(payload, settings_params, "Ethernet_Settings", f_module)
        assert payload == {
            "Name": "pool1"
        }

    def test_get_identity_pool_id_by_name_exist_case(self, mocker, ome_connection_mock_for_identity_pool, ome_response_mock):
        pool_list = {"resp_obj": ome_response_mock, "report_list": [{"Name": "pool1", "Id": 10},
                                                                    {"Name": "pool11", "Id": 11}]}
        ome_connection_mock_for_identity_pool.get_all_report_details.return_value = pool_list
        pool_id, attributes = self.module.get_identity_pool_id_by_name("pool1", ome_connection_mock_for_identity_pool)
        assert pool_id == 10

    def test_get_identity_pool_id_by_name_non_exist_case(self, mocker, ome_connection_mock_for_identity_pool, ome_response_mock):
        pool_list = {"resp_obj": ome_response_mock, "report_list": [{"Name": "pool2", "Id": 10}]}
        ome_connection_mock_for_identity_pool.get_all_report_details.return_value = pool_list
        pool_id, attributes = self.module.get_identity_pool_id_by_name("pool1", ome_connection_mock_for_identity_pool)
        assert pool_id == 0 and attributes is None


    def test_compare_payload_attributes_false_case_for_dummy_pool_setting(self):
        """this put opeartion always gives success result without applying changes because identity count is not passed as pat of it"""
        modify_setting_payload = {'Name': 'pool4', 'EthernetSettings': {'Mac': {'StartingMacAddress': 'qrvM3e6q'}}, 'Id': 33}
        existing_setting_payload =  {"@odata.context":"/api/$metadata#IdentityPoolService.IdentityPool","@odata.type":"#IdentityPoolService.IdentityPool","@odata.id":"/api/IdentityPoolService/IdentityPools(33)","Id":33,"Name":"pool4","Description":None,"CreatedBy":"admin","CreationTime":"2020-01-31 14:53:18.59163","LastUpdatedBy":"admin","LastUpdateTime":"2020-01-31 15:22:08.34596","EthernetSettings":None,"IscsiSettings":None,"FcoeSettings":None,"FcSettings":None,"UsageCounts":{"@odata.id":"/api/IdentityPoolService/IdentityPools(33)/UsageCounts"},"UsageIdentitySets@odata.navigationLink":"/api/IdentityPoolService/IdentityPools(33)/UsageIdentitySets"}
        val = self.module.compare_nested_dict(modify_setting_payload, existing_setting_payload)
        assert val is False

    @pytest.mark.parametrize("modify_setting_payload", [{"Description": "Identity pool with ethernet and fcoe settings2"}, {"Name": "pool2"}, {"EthernetSettings":{"Mac":{"IdentityCount":61,"StartingMacAddress":"UFBQUFAA"}}},
                                                        {"EthernetSettings": {"Mac": {"IdentityCount": 60, "StartingMacAddress": "qrvM3e6q"}}},
                                                        {"FcoeSettings":{"Mac":{"IdentityCount":70,"StartingMacAddress":"abcdfe"}}},
                                                        {"FcoeSettings": {"Mac": {"IdentityCount": 71, "StartingMacAddress": "cHBwcHAA"}}},
                                                        {"EthernetSettings":{"Mac":{"IdentityCount":60,"StartingMacAddress":"cHBwcHAA"}}, "FcoeSettings":{"Mac":{"IdentityCount":70,"StartingMacAddress":"qrvM3e6q"}}},
                                                        {"Description": "Identity pool with ethernet and fcoe settings2", "EthernetSettings": {"Mac": {"IdentityCount": 60, "StartingMacAddress": "UFBQUFAA"}},
                                                         "FcoeSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "cHBwcHAA"}}}])
    def test_compare_payload_attributes_case_false(self, modify_setting_payload):
        """case when chages are exists and payload can be used for modify opeartion"""
        modify_setting_payload = modify_setting_payload
        existing_setting_payload =  {"@odata.context":"/api/$metadata#IdentityPoolService.IdentityPool","@odata.type":"#IdentityPoolService.IdentityPool","@odata.id":"/api/IdentityPoolService/IdentityPools(23)","Id":23,"Name":"pool1","Description":"Identity pool with ethernet and fcoe settings1","CreatedBy":"admin","CreationTime":"2020-01-31 09:28:16.491424","LastUpdatedBy":"admin","LastUpdateTime":"2020-01-31 09:49:59.012549","EthernetSettings":{"Mac":{"IdentityCount":60,"StartingMacAddress":"UFBQUFAA"}},"IscsiSettings":None,"FcoeSettings":{"Mac":{"IdentityCount":70,"StartingMacAddress":"cHBwcHAA"}},"FcSettings":None,"UsageCounts":{"@odata.id":"/api/IdentityPoolService/IdentityPools(23)/UsageCounts"},"UsageIdentitySets@odata.navigationLink":"/api/IdentityPoolService/IdentityPools(23)/UsageIdentitySets"}
        val = self.module.compare_nested_dict(modify_setting_payload, existing_setting_payload)
        assert val is False

    @pytest.mark.parametrize("modify_setting_payload", [
                                                        {"Name": "pool1", "EthernetSettings": {"Mac": {"StartingMacAddress": "qrvM3e6q"}}},
                                                        {"Name": "pool1", "EthernetSettings": {"Mac": {"IdentityCount": 70}}},
                                                        {"Name": "pool1", "EthernetSettings": {"Mac": {"StartingMacAddress": "qrvM3e6q"}}},
                                                        {"Name": "pool1", "EthernetSettings": {"Mac": {"StartingMacAddress": "qrvM3e6q"}}, "FcoeSettings": {"Mac":{"StartingMacAddress":"cHBwcHAA"}}},
                                                        {"EthernetSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "qrvM3e6q"}}},
                                                        {"Description": "Identity pool with ethernet setting"},
                                                         {"Name": "pool1"},
                                                        {"FcoeSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "cHBwcHAA"}}},
                                                        {"EthernetSettings":{"Mac":{"IdentityCount": 70,"StartingMacAddress": "qrvM3e6q"}}, "FcoeSettings":{"Mac":{"IdentityCount":70,"StartingMacAddress":"cHBwcHAA"}}},
                                                        {"Description": "Identity pool with ethernet setting", "EthernetSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "qrvM3e6q"}},
                                                         "FcoeSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "cHBwcHAA"}}}])
    def test_compare_payload_attributes_case_true(self, modify_setting_payload):
        """setting values are same as existing payload and no need to apply the changes again"""
        modify_setting_payload = modify_setting_payload
        existing_setting_payload = {"@odata.context":"/api/$metadata#IdentityPoolService.IdentityPool","@odata.type":"#IdentityPoolService.IdentityPool","@odata.id":"/api/IdentityPoolService/IdentityPools(30)","Id":30,"Name":"pool1","Description":"Identity pool with ethernet setting","CreatedBy":"admin","CreationTime":"2020-01-31 11:31:13.621182","LastUpdatedBy":"admin","LastUpdateTime":"2020-01-31 11:34:28.00876","EthernetSettings": {"Mac": {"IdentityCount": 70,"StartingMacAddress": "qrvM3e6q"}},"IscsiSettings": None,"FcoeSettings":{"Mac":{"IdentityCount":70,"StartingMacAddress":"cHBwcHAA"}},"FcSettings":None,"UsageCounts":{"@odata.id":"/api/IdentityPoolService/IdentityPools(30)/UsageCounts"},"UsageIdentitySets@odata.navigationLink":"/api/IdentityPoolService/IdentityPools(30)/UsageIdentitySets"}
        val = self.module.compare_nested_dict(modify_setting_payload, existing_setting_payload)
        assert val is True


    def test_update_modify_payload_case_01(self):
        """when setting not exists in current requested payload, update payload from existing setting value if exists"""
        payload = {"Name": "pool1"}
        existing_setting_payload = {"@odata.context":"/api/$metadata#IdentityPoolService.IdentityPool","@odata.type":"#IdentityPoolService.IdentityPool","@odata.id":"/api/IdentityPoolService/IdentityPools(30)","Id":30,"Name":"pool1","Description":"Identity pool with ethernet setting","CreatedBy":"admin","CreationTime":"2020-01-31 11:31:13.621182","LastUpdatedBy":"admin","LastUpdateTime":"2020-01-31 11:34:28.00876","EthernetSettings": {"Mac": {"IdentityCount": 70,"StartingMacAddress": "qrvM3e6q"}},"IscsiSettings": None,"FcoeSettings":{"Mac":{"IdentityCount":70,"StartingMacAddress":"cHBwcHAA"}},"FcSettings":None,"UsageCounts":{"@odata.id":"/api/IdentityPoolService/IdentityPools(30)/UsageCounts"},"UsageIdentitySets@odata.navigationLink":"/api/IdentityPoolService/IdentityPools(30)/UsageIdentitySets"}
        self.module.update_modify_payload(payload, existing_setting_payload)
        assert payload["Description"] == "Identity pool with ethernet setting"
        assert payload["EthernetSettings"]["Mac"]["IdentityCount"] == 70
        assert payload["EthernetSettings"]["Mac"]["StartingMacAddress"] == "qrvM3e6q"
        assert payload["FcoeSettings"]["Mac"]["IdentityCount"] == 70
        assert payload["FcoeSettings"]["Mac"]["StartingMacAddress"] == "cHBwcHAA"

    def test_update_modify_payload_case_02(self):
        """when setting exists in current requested payload, don't update payload from existing setting value if exists"""
        payload = {"Name": "pool1", "EthernetSettings": {"Mac": {"IdentityCount": 55, "StartingMacAddress": "abcd"}},
                   "FcoeSettings": {"Mac": {"IdentityCount": 65, "StartingMacAddress": "xyz"}}}
        existing_setting_payload = {"@odata.context":"/api/$metadata#IdentityPoolService.IdentityPool","@odata.type":"#IdentityPoolService.IdentityPool","@odata.id":"/api/IdentityPoolService/IdentityPools(30)","Id":30,"Name":"pool1","Description":"Identity pool with ethernet setting","CreatedBy":"admin","CreationTime":"2020-01-31 11:31:13.621182","LastUpdatedBy":"admin","LastUpdateTime":"2020-01-31 11:34:28.00876","EthernetSettings": {"Mac": {"IdentityCount": 70,"StartingMacAddress": "qrvM3e6q"}},"IscsiSettings": None,"FcoeSettings":{"Mac":{"IdentityCount":70,"StartingMacAddress":"cHBwcHAA"}},"FcSettings":None,"UsageCounts":{"@odata.id":"/api/IdentityPoolService/IdentityPools(30)/UsageCounts"},"UsageIdentitySets@odata.navigationLink":"/api/IdentityPoolService/IdentityPools(30)/UsageIdentitySets"}
        self.module.update_modify_payload(payload, existing_setting_payload)
        assert payload["Description"] == "Identity pool with ethernet setting"
        assert payload["EthernetSettings"]["Mac"]["IdentityCount"] == 55
        assert payload["EthernetSettings"]["Mac"]["StartingMacAddress"] == "abcd"
        assert payload["FcoeSettings"]["Mac"]["IdentityCount"] == 65
        assert payload["FcoeSettings"]["Mac"]["StartingMacAddress"] == "xyz"

    def test_update_modify_payload_case_03(self):
        """update new description"""
        payload = {"Name": "pool1", "Description": "new description"}
        existing_setting_payload = {"@odata.context":"/api/$metadata#IdentityPoolService.IdentityPool","@odata.type":"#IdentityPoolService.IdentityPool","@odata.id":"/api/IdentityPoolService/IdentityPools(30)","Id":30,"Name":"pool1","Description":"Identity pool with ethernet setting","CreatedBy":"admin","CreationTime":"2020-01-31 11:31:13.621182","LastUpdatedBy":"admin","LastUpdateTime":"2020-01-31 11:34:28.00876","EthernetSettings": None,"IscsiSettings": None,"FcoeSettings": None,"FcSettings":None,"UsageCounts":{"@odata.id":"/api/IdentityPoolService/IdentityPools(30)/UsageCounts"},"UsageIdentitySets@odata.navigationLink":"/api/IdentityPoolService/IdentityPools(30)/UsageIdentitySets"}
        self.module.update_modify_payload(payload, existing_setting_payload)
        assert payload["Description"] == "new description"
        assert "EthernetSettings" not in payload
        assert "FcoeSettings" not in payload

    def test_update_modify_payload_case_04(self):
        """update remaining parameter of ethernet and fcoe setting if not exists in payload but exists in existing setting payload"""
        payload = {"Name": "pool1", "EthernetSettings": {"Mac": {"StartingMacAddress": "abcd"}},
                   "FcoeSettings": {"Mac": {"IdentityCount": 65}}}
        existing_setting_payload = {"@odata.context":"/api/$metadata#IdentityPoolService.IdentityPool","@odata.type":"#IdentityPoolService.IdentityPool","@odata.id":"/api/IdentityPoolService/IdentityPools(30)","Id":30,"Name":"pool1","Description":"Identity pool with ethernet setting","CreatedBy":"admin","CreationTime":"2020-01-31 11:31:13.621182","LastUpdatedBy":"admin","LastUpdateTime":"2020-01-31 11:34:28.00876","EthernetSettings": {"Mac": {"IdentityCount": 70,"StartingMacAddress": "qrvM3e6q"}},"IscsiSettings": None,"FcoeSettings":{"Mac":{"IdentityCount":70,"StartingMacAddress":"cHBwcHAA"}},"FcSettings":None,"UsageCounts":{"@odata.id":"/api/IdentityPoolService/IdentityPools(30)/UsageCounts"},"UsageIdentitySets@odata.navigationLink":"/api/IdentityPoolService/IdentityPools(30)/UsageIdentitySets"}
        self.module.update_modify_payload(payload, existing_setting_payload)
        assert payload["Description"] == "Identity pool with ethernet setting"
        assert payload["EthernetSettings"]["Mac"]["IdentityCount"] == 70
        assert payload["EthernetSettings"]["Mac"]["StartingMacAddress"] == "abcd"
        assert payload["FcoeSettings"]["Mac"]["IdentityCount"] == 65
        assert payload["FcoeSettings"]["Mac"]["StartingMacAddress"] == "cHBwcHAA"

    def test_update_modify_payload_case_05(self):
        """update remaining parameter of ethernet and fcoe setting will be null if not exists in existing payload"""
        payload = {"Name": "pool1", "EthernetSettings": {"Mac": {"StartingMacAddress": "abcd"}},}
        existing_setting_payload = {"@odata.context":"/api/$metadata#IdentityPoolService.IdentityPool","@odata.type":"#IdentityPoolService.IdentityPool","@odata.id":"/api/IdentityPoolService/IdentityPools(30)","Id":30,"Name":"pool1","Description":"Identity pool with ethernet setting","CreatedBy":"admin","CreationTime":"2020-01-31 11:31:13.621182","LastUpdatedBy":"admin","LastUpdateTime":"2020-01-31 11:34:28.00876","EthernetSettings": {"Mac": {"StartingMacAddress": "qrvM3e6q"}},"IscsiSettings": None,"FcoeSettings":{"Mac":{"StartingMacAddress":"cHBwcHAA"}},"FcSettings":None,"UsageCounts":{"@odata.id":"/api/IdentityPoolService/IdentityPools(30)/UsageCounts"},"UsageIdentitySets@odata.navigationLink":"/api/IdentityPoolService/IdentityPools(30)/UsageIdentitySets"}
        self.module.update_modify_payload(payload, existing_setting_payload)
        assert payload["Description"] == "Identity pool with ethernet setting"
        assert payload["EthernetSettings"]["Mac"]["StartingMacAddress"] == "abcd"
        assert "IdentityCount" not in payload["EthernetSettings"]["Mac"]

    @pytest.mark.parametrize("setting", ["EthernetSettings", "FcoeSettings"])
    def test_update_modify_payload_case_06(self, setting):
        modify_payload = {"Name": "pool1", "EthernetSettings": {"Mac": {"StartingMacAddress": "abcd"}}, }
        existing_payload = {"@odata.context":"/api/$metadata#IdentityPoolService.IdentityPool",
                                    "@odata.type":"#IdentityPoolService.IdentityPool",
                                    "@odata.id":"/api/IdentityPoolService/IdentityPools(35)",
                                    "Id":35,"Name":"pool1",
                                    "Description":"Identity pool with ethernet and fcoe settings1",
                                    "CreatedBy":"admin","CreationTime":"2020-02-01 07:55:59.923838",
                                    "LastUpdatedBy":"admin","LastUpdateTime":"2020-02-01 07:55:59.923838",
                                    "EthernetSettings":{"Mac":{"IdentityCount":60,"StartingMacAddress":"UFBQUFAA"}},
                                    "IscsiSettings":None,"FcoeSettings":{"Mac":{"IdentityCount":70,"StartingMacAddress":"cHBwcHAA"}},
                                    "FcSettings":None,"UsageCounts":{"@odata.id":"/api/IdentityPoolService/IdentityPools(35)/UsageCounts"},
                                    "UsageIdentitySets@odata.navigationLink":"/api/IdentityPoolService/IdentityPools(35)/UsageIdentitySets"}
        self.module.update_modify_payload(modify_payload, existing_payload)
        assert modify_payload["EthernetSettings"]["Mac"]["StartingMacAddress"] == "abcd"
        assert modify_payload["EthernetSettings"]["Mac"]["IdentityCount"] == 60
        assert modify_payload["FcoeSettings"]["Mac"]["StartingMacAddress"] == "cHBwcHAA"
        assert modify_payload["FcoeSettings"]["Mac"]["IdentityCount"] == 70

    @pytest.mark.parametrize("setting", ["EthernetSettings", "FcoeSettings"])
    def test_update_modify_setting_case_success(self, setting):
        modify_payload = {"Name": "pool1", "EthernetSettings": {"Mac": {"StartingMacAddress": "abcd"}}, "FcoeSettings": {"Mac": {"IdentityCount": 55}}}
        existing_payload = {"@odata.context":"/api/$metadata#IdentityPoolService.IdentityPool",
                                    "@odata.type":"#IdentityPoolService.IdentityPool",
                                    "@odata.id":"/api/IdentityPoolService/IdentityPools(35)",
                                    "Id":35,"Name":"pool1",
                                    "Description":"Identity pool with ethernet and fcoe settings1",
                                    "CreatedBy":"admin","CreationTime":"2020-02-01 07:55:59.923838",
                                    "LastUpdatedBy":"admin","LastUpdateTime":"2020-02-01 07:55:59.923838",
                                    "EthernetSettings":{"Mac":{"IdentityCount":60,"StartingMacAddress":"UFBQUFAA"}},
                                    "IscsiSettings":None,"FcoeSettings":{"Mac":{"IdentityCount":70,"StartingMacAddress":"cHBwcHAA"}},
                                    "FcSettings":None,"UsageCounts":{"@odata.id":"/api/IdentityPoolService/IdentityPools(35)/UsageCounts"},
                                    "UsageIdentitySets@odata.navigationLink":"/api/IdentityPoolService/IdentityPools(35)/UsageIdentitySets"}
        if setting == "EthernetSettings":
            self.module.update_modify_setting(modify_payload, existing_payload, setting)
            assert modify_payload["EthernetSettings"]["Mac"]["StartingMacAddress"] == "abcd"
            assert modify_payload["EthernetSettings"]["Mac"]["IdentityCount"] == 60
        else:
            self.module.update_modify_setting(modify_payload, existing_payload, setting)
            assert modify_payload["FcoeSettings"]["Mac"]["StartingMacAddress"] == "cHBwcHAA"
            assert modify_payload["FcoeSettings"]["Mac"]["IdentityCount"] == 55

    @pytest.mark.parametrize("mac_address", ['50-50-50-50-50-50','50:50:50:50:50:50', '5050.5050.5050', 'ab:cd:ef:70:80:70'])
    def test_mac_validation_match_case(self, mac_address):
        match = self.module.mac_validation(mac_address)
        assert match is not None

    @pytest.mark.parametrize("mac_address", ['50--50--50--50--50-50',
                                             '50::50::50::50::50::50',
                                             '5050..5050..5050',
                                             'ab/cd/ef/70/80/70',
                                             '50-50:50.50-50-50',
                                             'xy:gh:yk:lm:30:10',
                                             '50-50-50-50-50',
                                             '50-50-50-50-50-50-50-50'])
    def test_mac_validation_match_case(self, mac_address):
        match = self.module.mac_validation(mac_address)
        assert match is None

    @pytest.mark.parametrize("mac_address_base64_map", [{'50-50-50-50-50-50': 'UFBQUFBQ'},
                                             {'50:50:50:50:50:50': 'UFBQUFBQ'},
                                             {'5050.5050.5050': 'UFBQUFBQ'},
                                             {'ab:cd:ef:70:80:70':'q83vcIBw'}])
    def test_mac_to_base64_conversion(self, mac_address_base64_map):
        f_module = self.get_module_mock()
        mac_address = list(mac_address_base64_map.keys())[0]
        base_64_val_expected = list(mac_address_base64_map.values())[0]
        base_64_val = self.module.mac_to_base64_conversion(mac_address, f_module)
        assert base_64_val == base_64_val_expected













