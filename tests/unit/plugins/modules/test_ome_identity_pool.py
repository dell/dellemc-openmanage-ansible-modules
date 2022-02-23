# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.1.0
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible_collections.dellemc.openmanage.plugins.modules import ome_identity_pool
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ssl import SSLError
from io import StringIO
from ansible.module_utils._text import to_text
import json

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


@pytest.fixture
def ome_connection_mock_for_identity_pool(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(
        MODULE_PATH + 'ome_identity_pool.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOMeIdentityPool(FakeAnsibleModule):
    module = ome_identity_pool

    def test_main_ome_identity_pool_success_case1(self, mocker, ome_default_args,
                                                  ome_connection_mock_for_identity_pool, ome_response_mock):
        sub_param = {"pool_name": "pool1",
                     "pool_description": "Identity pool with ethernet and fcoe settings",
                     "ethernet_settings": {
                         "starting_mac_address": "50-50-50-50-50-00",
                         "identity_count": 60},
                     "fcoe_settings": {
                         "starting_mac_address": "70-70-70-70-70-00",
                         "identity_count": 75
                     },
                     "iscsi_settings": {
                         "identity_count": 30,
                         "initiator_config": {
                             "iqn_prefix": "iqn.myprefix."
                         },
                         "initiator_ip_pool_settings": {
                             "gateway": "192.168.4.1",
                             "ip_range": "10.33.0.1-10.33.0.255",
                             "primary_dns_server": "10.8.8.8",
                             "secondary_dns_server": "8.8.8.8",
                             "subnet_mask": "255.255.255.0"
                         },
                         "starting_mac_address": "60:60:60:60:60:00"
                     },
                     "fc_settings": {
                         "identity_count": 45,
                         "starting_address": "10-10-10-10-10-10"
                     }
                     }
        message_return = {"msg": "Successfully created an identity pool.",
                          "result": {"Id": 36, "IsSuccessful": True, "Issues": []}}
        mocker.patch(MODULE_PATH + 'ome_identity_pool.pool_create_modify',
                     return_value=message_return)
        ome_default_args.update(sub_param)
        result = self.execute_module(ome_default_args)
        assert result['changed'] is True
        assert 'pool_status' in result and "msg" in result
        assert result["msg"] == "Successfully created an identity pool."
        assert result['pool_status'] == {
            "Id": 36,
            "IsSuccessful": True,
            "Issues": []
        }

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_main_ome_identity_pool_failure_case1(self, exc_type, mocker, ome_default_args,
                                                  ome_connection_mock_for_identity_pool, ome_response_mock):
        ome_default_args.update({"pool_name": "pool1"})
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'ome_identity_pool.pool_create_modify',
                         side_effect=exc_type("ansible.module_utils.urls.open_url error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'ome_identity_pool.pool_create_modify',
                         side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'ome_identity_pool.pool_create_modify',
                         side_effect=exc_type('http://testhost.com', 400,
                                              'http error message',
                                              {"accept-type": "application/json"},
                                              StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'pool_status' not in result
        assert 'msg' in result

    def test_main_ome_identity_pool_no_mandatory_arg_passed_failure_case(self, ome_default_args,
                                                                         ome_connection_mock_for_identity_pool):
        result = self._run_module_with_fail_json(ome_default_args)
        assert 'pool_status' not in result

    @pytest.mark.parametrize("param", [{"ethernet_settings": {"invalid_key": "value"}},
                                       {"fcoe_settings": {"invalid_key": "value"}},
                                       {"iscsi_settings": {"invalid_key": "value"}},
                                       {"iscsi_settings": {"initiator_config": {"invalid_key": "value"}}},
                                       {"iscsi_settings": {"initiator_ip_pool_settings": {"gateway1": "192.168.4.1"}}},
                                       {"iscsi_settings": {
                                           "initiator_ip_pool_settings": {"primary_dns_server": "192.168.4.1",
                                                                          "ip_range1": "value"}}},
                                       {"fc_settings": {"invalid_key": "value"}},
                                       {"name": "name1"}])
    def test_main_ome_identity_pool_invalid_settings(self, param, ome_default_args,
                                                     ome_connection_mock_for_identity_pool):
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
        mocker.patch(
            MODULE_PATH + 'ome_identity_pool.validate_modify_create_payload')
        mocker.patch(
            MODULE_PATH + 'ome_identity_pool.get_identity_pool_id_by_name',
            return_value=(10, {"paylaod": "value"}))
        mocker.patch(MODULE_PATH + 'ome_identity_pool.get_payload',
                     return_value={"Name": "name"})
        mocker.patch(MODULE_PATH + 'ome_identity_pool.get_success_message',
                     return_value={"msg": "Successfully modified the identity pool"})
        mocker.patch(
            MODULE_PATH + 'ome_identity_pool.get_updated_modify_payload')
        mocker.patch(MODULE_PATH + 'ome_identity_pool.compare_nested_dict',
                     return_value=False)
        f_module = self.get_module_mock(params=params)
        message = self.module.pool_create_modify(f_module, ome_connection_mock_for_identity_pool)
        assert message == {"msg": "Successfully modified the identity pool"}

    def test_pool_create_modify_success_case_02(self, mocker, ome_connection_mock_for_identity_pool, ome_response_mock):
        params = {"pool_name": "pool_name"}
        mocker.patch(
            MODULE_PATH + 'ome_identity_pool.validate_modify_create_payload')
        mocker.patch(
            MODULE_PATH + 'ome_identity_pool.get_identity_pool_id_by_name',
            return_value=(0, None))
        mocker.patch(MODULE_PATH + 'ome_identity_pool.get_payload',
                     return_value={"Name": "name"})
        mocker.patch(MODULE_PATH + 'ome_identity_pool.get_success_message',
                     return_value={"msg": "Successfully created an identity pool"})
        f_module = self.get_module_mock(params=params)
        message = self.module.pool_create_modify(f_module, ome_connection_mock_for_identity_pool)
        assert message == {"msg": "Successfully created an identity pool"}

    def test_pool_create_modify_success_case_03(self, mocker, ome_connection_mock_for_identity_pool, ome_response_mock):
        params = {"pool_name": "pool_name"}
        mocker.patch(
            MODULE_PATH + 'ome_identity_pool.get_identity_pool_id_by_name',
            return_value=(10, {"payload": "value"}))
        mocker.patch(MODULE_PATH + 'ome_identity_pool.get_payload',
                     return_value={"Name": "pool1"})
        mocker.patch(MODULE_PATH + 'ome_identity_pool.get_success_message',
                     return_value={"msg": "Successfully modified the identity pool"})
        mocker.patch(
            MODULE_PATH + 'ome_identity_pool.get_updated_modify_payload')
        mocker.patch(MODULE_PATH + 'ome_identity_pool.compare_nested_dict',
                     return_value=True)
        f_module = self.get_module_mock(params=params)
        with pytest.raises(Exception) as exc:
            self.module.pool_create_modify(f_module, ome_connection_mock_for_identity_pool)
        return exc.value.args[0] == "No changes are made to the specified pool name: pool1, as" \
                                    " as the entered values are the same as the current configuration."

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

    def test_get_payload_create_case03(self):
        """new_pool_name should be ignored for create action"""
        params = {
            "ethernet_settings": {
                "identity_count": 60,
                "starting_mac_address": "50:50:50:50:50:00"
            },
            "fc_settings": {
                "identity_count": 45,
                "starting_address": "10-10-10-10-10-10"
            },
            "fcoe_settings": {
                "identity_count": 75,
                "starting_mac_address": "aabb.ccdd.7070"
            },
            "hostname": "192.168.0.1",
            "iscsi_settings": {
                "identity_count": 30,
                "initiator_config": {
                    "iqn_prefix": "iqn.myprefix."
                },
                "initiator_ip_pool_settings": {
                    "gateway": "192.168.4.1",
                    "ip_range": "10.33.0.1-10.33.0.255",
                    "primary_dns_server": "10.8.8.8",
                    "secondary_dns_server": "8.8.8.8",
                    "subnet_mask": "255.255.255.0"
                },
                "starting_mac_address": "60:60:60:60:60:00"
            },
            "new_pool_name": None,
            "password": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
            "pool_description": "Identity pool with Ethernet, FCoE, ISCSI and FC settings",
            "pool_name": "pool1",
            "port": 443,
            "state": "present",
            "username": "admin"
        }
        f_module = self.get_module_mock(params=params)
        payload = self.module.get_payload(f_module)
        assert payload == {
            "Name": "pool1",
            "Description": "Identity pool with Ethernet, FCoE, ISCSI and FC settings",
            "EthernetSettings": {
                "Mac": {
                    "IdentityCount": 60,
                    "StartingMacAddress": "UFBQUFAA"
                }
            },
            "IscsiSettings": {
                "Mac": {
                    "IdentityCount": 30,
                    "StartingMacAddress": "YGBgYGAA"
                },
                "InitiatorConfig": {
                    "IqnPrefix": "iqn.myprefix."
                },
                "InitiatorIpPoolSettings": {
                    "IpRange": "10.33.0.1-10.33.0.255",
                    "SubnetMask": "255.255.255.0",
                    "Gateway": "192.168.4.1",
                    "PrimaryDnsServer": "10.8.8.8",
                    "SecondaryDnsServer": "8.8.8.8"
                }
            },
            "FcoeSettings": {
                "Mac": {
                    "IdentityCount": 75,
                    "StartingMacAddress": "qrvM3XBw"
                }
            },
            "FcSettings": {
                "Wwnn": {
                    "IdentityCount": 45,
                    "StartingAddress": "IAAQEBAQEBA="
                },
                "Wwpn": {
                    "IdentityCount": 45,
                    "StartingAddress": "IAEQEBAQEBA="
                }
            }
        }
        assert payload["FcSettings"]["Wwnn"] == {"IdentityCount": 45, "StartingAddress": "IAAQEBAQEBA="}
        assert payload["FcSettings"]["Wwpn"] == {"IdentityCount": 45, "StartingAddress": "IAEQEBAQEBA="}
        assert payload["IscsiSettings"]["Mac"] == {"IdentityCount": 30, "StartingMacAddress": "YGBgYGAA"}
        assert payload["IscsiSettings"]["InitiatorIpPoolSettings"] == {
            "IpRange": "10.33.0.1-10.33.0.255",
            "SubnetMask": "255.255.255.0",
            "Gateway": "192.168.4.1",
            "PrimaryDnsServer": "10.8.8.8",
            "SecondaryDnsServer": "8.8.8.8"
        }
        assert payload["IscsiSettings"]["InitiatorConfig"] == {
            "IqnPrefix": "iqn.myprefix."
        }

    @pytest.mark.parametrize("state", ["create", "modify"])
    def test_get_payload_create_modify_case04(self, state):
        """new_pool_name should be ignored for create action"""
        params = {"pool_name": "pool3",
                  "new_pool_name": "pool4",
                  "pool_description": "Identity pool with iscsi",
                  "iscsi_settings": {
                      "identity_count": 30,
                      "initiator_config": {
                          "iqn_prefix": "iqn.myprefix."
                      },
                      "initiator_ip_pool_settings": {
                          "gateway": "192.168.4.1",
                          "ip_range": "20.33.0.1-20.33.0.255",
                          "primary_dns_server": "10.8.8.8",
                          "secondary_dns_server": "8.8.8.8",
                          "subnet_mask": "255.255.255.0"
                      },
                      "starting_mac_address": "10:10:10:10:10:00"
                  }
                  }
        f_module = self.get_module_mock(params=params)
        if state == "create":
            payload = self.module.get_payload(f_module)
        else:
            payload = self.module.get_payload(f_module, 11)
        assert "FcSettings" not in payload
        assert "FcoeSettings" not in payload
        assert payload["IscsiSettings"]["Mac"] == {"IdentityCount": 30, "StartingMacAddress": "EBAQEBAA"}
        assert payload["IscsiSettings"]["InitiatorIpPoolSettings"] == {
            "IpRange": "20.33.0.1-20.33.0.255",
            "SubnetMask": "255.255.255.0",
            "Gateway": "192.168.4.1",
            "PrimaryDnsServer": "10.8.8.8",
            "SecondaryDnsServer": "8.8.8.8"
        }
        assert payload["IscsiSettings"]["InitiatorConfig"] == {
            "IqnPrefix": "iqn.myprefix."
        }
        if state == "create":
            assert payload["Name"] == "pool3"
            assert "Id" not in payload
        else:
            assert payload["Name"] == "pool4"
            assert payload["Id"] == 11

    @pytest.mark.parametrize("state", ["create", "modify"])
    def test_get_payload_create_case05(self, state):
        """new_pool_name should be ignored for create action and considered in modify"""
        params = {"pool_name": "pool3",
                  "new_pool_name": "pool4",
                  "pool_description": "Identity pool with iscsi",
                  "fc_settings": {
                      "identity_count": 48,
                      "starting_address": "40:40:40:40:40:22"
                  }
                  }
        f_module = self.get_module_mock(params=params)
        if state == "create":
            payload = self.module.get_payload(f_module)
        else:
            payload = self.module.get_payload(f_module, 11)
        return_setting = {
            "Name": "pool2",
            "Description": "Identity pool with fc_settings",
            "EthernetSettings": None,
            "IscsiSettings": None,
            "FcoeSettings": None,
            "FcSettings": {
                "Wwnn": {
                    "IdentityCount": 48,
                    "StartingAddress": "IABAQEBAQCI="
                },
                "Wwpn": {
                    "IdentityCount": 48,
                    "StartingAddress": "IAFAQEBAQCI="
                }
            }
        }

        assert payload["FcSettings"]["Wwnn"]["StartingAddress"] == "IABAQEBAQCI="
        assert payload["FcSettings"]["Wwpn"]["StartingAddress"] == "IAFAQEBAQCI="
        assert payload["FcSettings"]["Wwnn"]["IdentityCount"] == 48
        assert payload["FcSettings"]["Wwpn"]["IdentityCount"] == 48
        if state == "create":
            assert payload["Name"] == "pool3"
            assert "Id" not in payload
        else:
            assert payload["Name"] == "pool4"
            assert payload["Id"] == 11

    def test_get_payload_create_case06(self):
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

    @pytest.mark.parametrize("state", ["create", "modify"])
    def test_get_payload_create_case07(self, state):
        # case when new_pool_name not passed
        params = {"pool_name": "pool1",
                  "pool_description": "Identity pool with ethernet and fcoe settings"}
        f_module = self.get_module_mock(params=params)
        if state == "create":
            payload = self.module.get_payload(f_module, None)
        else:
            payload = self.module.get_payload(f_module, 11)
        assert payload["Name"] == "pool1"
        if state == "modify":
            assert "Id" in payload
        else:
            assert "Id" not in payload
        assert "FcoeSettings" not in payload
        assert "Ethernet_Settings" not in payload
        assert "Ethernet_Settings" not in payload
        assert "Ethernet_Settings" not in payload

    def test_get_payload_modify_case01(self):
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

    def test_get_payload_modify_case02(self):
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

    def test_get_payload_modify_case03(self):
        params = {"pool_name": "pool1", "new_pool_name": "pool2"}
        f_module = self.get_module_mock(params=params)
        payload = self.module.get_payload(f_module, 11)
        assert payload["Name"] == "pool2"
        assert payload["Id"] == 11
        assert "Description" not in payload
        assert "FcoeSettings" not in payload
        assert "Ethernet_Settings" not in payload

    def test_get_payload_modify_case04(self):
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

    def test_update_mac_settings_case_01(self):
        f_module = self.get_module_mock()
        settings_params = {"starting_mac_address": "70-70-70-70-70-00", "identity_count": 10}
        payload = {"Name": "pool1"}
        self.module.update_mac_settings(payload, settings_params, "Ethernet_Settings", f_module)
        assert payload == {
            "Name": "pool1",
            "Ethernet_Settings": {"Mac": {"StartingMacAddress": "cHBwcHAA", "IdentityCount": 10}}
        }

    def test_update_mac_settings_case_02(self):
        f_module = self.get_module_mock()
        settings_params = {"starting_mac_address": "70-70-70-70-70-xx", "identity_count": 10}
        payload = {"Name": "pool1"}
        with pytest.raises(Exception) as exc:
            self.module.update_mac_settings(payload, settings_params, "EthernetSettings", f_module)
        assert exc.value.args[0] == "Please provide the valid MAC address format for Ethernet settings."

    def test_update_mac_settings_case_03(self):
        """case when no sub settting exists"""
        settings_params = {}
        payload = {"Name": "pool1"}
        f_module = self.get_module_mock()
        self.module.update_mac_settings(payload, settings_params, "Ethernet_Settings", f_module)
        assert payload == {
            "Name": "pool1"
        }

    def test_get_identity_pool_id_by_name_exist_case(self, mocker, ome_connection_mock_for_identity_pool,
                                                     ome_response_mock):
        pool_list = {"resp_obj": ome_response_mock, "report_list": [{"Name": "pool1", "Id": 10},
                                                                    {"Name": "pool11", "Id": 11}]}
        ome_connection_mock_for_identity_pool.get_all_report_details.return_value = pool_list
        pool_id, attributes = self.module.get_identity_pool_id_by_name("pool1", ome_connection_mock_for_identity_pool)
        assert pool_id == 10

    def test_get_identity_pool_id_by_name_non_exist_case(self, mocker, ome_connection_mock_for_identity_pool,
                                                         ome_response_mock):
        pool_list = {"resp_obj": ome_response_mock, "report_list": [{"Name": "pool2", "Id": 10}]}
        ome_connection_mock_for_identity_pool.get_all_report_details.return_value = pool_list
        pool_id, attributes = self.module.get_identity_pool_id_by_name("pool1", ome_connection_mock_for_identity_pool)
        assert pool_id == 0 and attributes is None

    def test_compare_payload_attributes_false_case_for_dummy_pool_setting(self):
        """this put opeartion always gives success result without applying
         changes because identity count is not passed as pat of it"""
        modify_setting_payload = {'Name': 'pool4', 'EthernetSettings': {'Mac': {'StartingMacAddress': 'qrvM3e6q'}},
                                  'Id': 33}
        existing_setting_payload = {
            "@odata.context": "/api/$metadata#IdentityPoolService.IdentityPool",
            "@odata.type": "#IdentityPoolService.IdentityPool",
            "@odata.id": "/api/IdentityPoolService/IdentityPools(33)",
            "Id": 33,
            "Name": "pool4",
            "Description": None,
            "CreatedBy": "admin",
            "CreationTime": "2020-01-31 14:53:18.59163",
            "LastUpdatedBy": "admin",
            "LastUpdateTime": "2020-01-31 15:22:08.34596",
            "EthernetSettings": None,
            "IscsiSettings": None,
            "FcoeSettings": None,
            "FcSettings": None,
            "UsageCounts": {
                "@odata.id": "/api/IdentityPoolService/IdentityPools(33)/UsageCounts"
            },
            "UsageIdentitySets@odata.navigationLink": "/api/IdentityPoolService/IdentityPools(33)/UsageIdentitySets"
        }
        val = self.module.compare_nested_dict(modify_setting_payload, existing_setting_payload)
        assert val is False

    @pytest.mark.parametrize("modify_payload",
                             [{"Description": "Identity pool with ethernet and fcoe settings2"}, {"Name": "pool2"},
                              {"EthernetSettings": {"Mac": {"IdentityCount": 61, "StartingMacAddress": "UFBQUFAA"}}},
                              {"EthernetSettings": {"Mac": {"IdentityCount": 60, "StartingMacAddress": "qrvM3e6q"}}},
                              {"FcoeSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "abcdfe"}}},
                              {"FcoeSettings": {"Mac": {"IdentityCount": 71, "StartingMacAddress": "cHBwcHAA"}}},
                              {"EthernetSettings": {"Mac": {"IdentityCount": 60, "StartingMacAddress": "cHBwcHAA"}},
                               "FcoeSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "qrvM3e6q"}}},
                              {"Description": "Identity pool with ethernet and fcoe settings2",
                               "EthernetSettings": {"Mac": {"IdentityCount": 60, "StartingMacAddress": "UFBQUFAA"}},
                               "FcoeSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "cHBwcHAA"}}}])
    def test_compare_payload_attributes_case_false(self, modify_payload):
        """case when chages are exists and payload can be used for modify opeartion"""
        modify_setting_payload = modify_payload
        existing_setting_payload = {
            "@odata.context": "/api/$metadata#IdentityPoolService.IdentityPool",
            "@odata.type": "#IdentityPoolService.IdentityPool",
            "@odata.id": "/api/IdentityPoolService/IdentityPools(23)",
            "Id": 23,
            "Name": "pool1",
            "Description": "Identity pool with ethernet and fcoe settings1",
            "CreatedBy": "admin",
            "CreationTime": "2020-01-31 09:28:16.491424",
            "LastUpdatedBy": "admin",
            "LastUpdateTime": "2020-01-31 09:49:59.012549",
            "EthernetSettings": {
                "Mac": {
                    "IdentityCount": 60,
                    "StartingMacAddress": "UFBQUFAA"
                }
            },
            "IscsiSettings": None,
            "FcoeSettings": {
                "Mac": {
                    "IdentityCount": 70,
                    "StartingMacAddress": "cHBwcHAA"
                }
            },
            "FcSettings": None,
            "UsageCounts": {
                "@odata.id": "/api/IdentityPoolService/IdentityPools(23)/UsageCounts"
            },
            "UsageIdentitySets@odata.navigationLink": "/api/IdentityPoolService/IdentityPools(23)/UsageIdentitySets"
        }
        val = self.module.compare_nested_dict(modify_setting_payload, existing_setting_payload)
        assert val is False

    @pytest.mark.parametrize("modify_payload", [
        {"Name": "pool1", "EthernetSettings": {"Mac": {"StartingMacAddress": "qrvM3e6q"}}},
        {"Name": "pool1", "EthernetSettings": {"Mac": {"IdentityCount": 70}}},
        {"Name": "pool1", "EthernetSettings": {"Mac": {"StartingMacAddress": "qrvM3e6q"}}},
        {"Name": "pool1", "EthernetSettings": {"Mac": {"StartingMacAddress": "qrvM3e6q"}},
         "FcoeSettings": {"Mac": {"StartingMacAddress": "cHBwcHAA"}}},
        {"EthernetSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "qrvM3e6q"}}},
        {"Description": "Identity pool with ethernet setting"},
        {"Name": "pool1"},
        {"FcoeSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "cHBwcHAA"}}},
        {"EthernetSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "qrvM3e6q"}},
         "FcoeSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "cHBwcHAA"}}},
        {"Description": "Identity pool with ethernet setting",
         "EthernetSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "qrvM3e6q"}},
         "FcoeSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "cHBwcHAA"}}}])
    def test_compare_payload_attributes_case_true(self, modify_payload):
        """setting values are same as existing payload and no need to apply the changes again"""
        modify_setting_payload = modify_payload
        existing_setting_payload = {
            "@odata.context": "/api/$metadata#IdentityPoolService.IdentityPool",
            "@odata.type": "#IdentityPoolService.IdentityPool",
            "@odata.id": "/api/IdentityPoolService/IdentityPools(30)",
            "Id": 30,
            "Name": "pool1",
            "Description": "Identity pool with ethernet setting",
            "CreatedBy": "admin",
            "CreationTime": "2020-01-31 11:31:13.621182",
            "LastUpdatedBy": "admin",
            "LastUpdateTime": "2020-01-31 11:34:28.00876",
            "EthernetSettings": {
                "Mac": {
                    "IdentityCount": 70,
                    "StartingMacAddress": "qrvM3e6q"
                }
            },
            "IscsiSettings": None,
            "FcoeSettings": {
                "Mac": {
                    "IdentityCount": 70,
                    "StartingMacAddress": "cHBwcHAA"
                }
            },
            "FcSettings": None,
            "UsageCounts": {
                "@odata.id": "/api/IdentityPoolService/IdentityPools(30)/UsageCounts"
            },
            "UsageIdentitySets@odata.navigationLink": "/api/IdentityPoolService/IdentityPools(30)/UsageIdentitySets"
        }
        val = self.module.compare_nested_dict(modify_setting_payload, existing_setting_payload)
        assert val is True

    def test_get_updated_modify_payload_case_01(self):
        """when setting not exists in current requested payload, update payload from existing setting value if exists"""
        payload = {"Name": "pool1"}
        existing_setting_payload = {
            "@odata.context": "/api/$metadata#IdentityPoolService.IdentityPool",
            "@odata.type": "#IdentityPoolService.IdentityPool",
            "@odata.id": "/api/IdentityPoolService/IdentityPools(30)",
            "Id": 30,
            "Name": "pool1",
            "Description": "Identity pool with ethernet setting",
            "CreatedBy": "admin",
            "CreationTime": "2020-01-31 11:31:13.621182",
            "LastUpdatedBy": "admin",
            "LastUpdateTime": "2020-01-31 11:34:28.00876",
            "EthernetSettings": {
                "Mac": {
                    "IdentityCount": 70,
                    "StartingMacAddress": "qrvM3e6q"
                }
            },
            "IscsiSettings": None,
            "FcoeSettings": {
                "Mac": {
                    "IdentityCount": 70,
                    "StartingMacAddress": "cHBwcHAA"
                }
            },
            "FcSettings": None,
            "UsageCounts": {
                "@odata.id": "/api/IdentityPoolService/IdentityPools(30)/UsageCounts"
            },
            "UsageIdentitySets@odata.navigationLink": "/api/IdentityPoolService/IdentityPools(30)/UsageIdentitySets"
        }
        payload = self.module.get_updated_modify_payload(payload, existing_setting_payload)
        assert payload["Description"] == "Identity pool with ethernet setting"
        assert payload["EthernetSettings"]["Mac"]["IdentityCount"] == 70
        assert payload["EthernetSettings"]["Mac"]["StartingMacAddress"] == "qrvM3e6q"
        assert payload["FcoeSettings"]["Mac"]["IdentityCount"] == 70
        assert payload["FcoeSettings"]["Mac"]["StartingMacAddress"] == "cHBwcHAA"

    def test_get_updated_modify_payload_case_02(self):
        """when setting exists in current requested payload, do not
         update payload from existing setting value if exists"""
        payload = {"Name": "pool1", "EthernetSettings": {"Mac": {"IdentityCount": 55, "StartingMacAddress": "abcd"}},
                   "FcoeSettings": {"Mac": {"IdentityCount": 65, "StartingMacAddress": "xyz"}}}
        existing_setting_payload = {
            "@odata.context": "/api/$metadata#IdentityPoolService.IdentityPool",
            "@odata.type": "#IdentityPoolService.IdentityPool",
            "@odata.id": "/api/IdentityPoolService/IdentityPools(30)",
            "Id": 30,
            "Name": "pool1",
            "Description": "Identity pool with ethernet setting",
            "CreatedBy": "admin",
            "CreationTime": "2020-01-31 11:31:13.621182",
            "LastUpdatedBy": "admin",
            "LastUpdateTime": "2020-01-31 11:34:28.00876",
            "EthernetSettings": {
                "Mac": {
                    "IdentityCount": 70,
                    "StartingMacAddress": "qrvM3e6q"
                }
            },
            "IscsiSettings": None,
            "FcoeSettings": {
                "Mac": {
                    "IdentityCount": 70,
                    "StartingMacAddress": "cHBwcHAA"
                }
            },
            "FcSettings": None,
            "UsageCounts": {
                "@odata.id": "/api/IdentityPoolService/IdentityPools(30)/UsageCounts"
            },
            "UsageIdentitySets@odata.navigationLink": "/api/IdentityPoolService/IdentityPools(30)/UsageIdentitySets"
        }
        payload = self.module.get_updated_modify_payload(payload, existing_setting_payload)
        assert payload["Description"] == "Identity pool with ethernet setting"
        assert payload["EthernetSettings"]["Mac"]["IdentityCount"] == 55
        assert payload["EthernetSettings"]["Mac"]["StartingMacAddress"] == "abcd"
        assert payload["FcoeSettings"]["Mac"]["IdentityCount"] == 65
        assert payload["FcoeSettings"]["Mac"]["StartingMacAddress"] == "xyz"

    def test_get_updated_modify_payload_case_03(self):
        """update new description"""
        payload = {"Name": "pool1", "Description": "new description"}
        existing_setting_payload = {
            "@odata.context": "/api/$metadata#IdentityPoolService.IdentityPool",
            "@odata.type": "#IdentityPoolService.IdentityPool",
            "@odata.id": "/api/IdentityPoolService/IdentityPools(30)",
            "Id": 30,
            "Name": "pool1",
            "Description": "Identity pool with ethernet setting",
            "CreatedBy": "admin",
            "CreationTime": "2020-01-31 11:31:13.621182",
            "LastUpdatedBy": "admin",
            "LastUpdateTime": "2020-01-31 11:34:28.00876",
            "EthernetSettings": None,
            "IscsiSettings": None,
            "FcoeSettings": None,
            "FcSettings": None,
            "UsageCounts": {
                "@odata.id": "/api/IdentityPoolService/IdentityPools(30)/UsageCounts"
            },
            "UsageIdentitySets@odata.navigationLink": "/api/IdentityPoolService/IdentityPools(30)/UsageIdentitySets"
        }
        payload = self.module.get_updated_modify_payload(payload, existing_setting_payload)
        assert payload["Description"] == "new description"
        assert "EthernetSettings" not in payload
        assert "FcoeSettings" not in payload

    def test_get_updated_modify_payload_case_04(self):
        """update remaining parameter of ethernet and fcoe setting
         if not exists in payload but exists in existing setting payload"""
        payload = {"Name": "pool1", "EthernetSettings": {"Mac": {"StartingMacAddress": "abcd"}},
                   "FcoeSettings": {"Mac": {"IdentityCount": 65}}}
        existing_setting_payload = {
            "@odata.context": "/api/$metadata#IdentityPoolService.IdentityPool",
            "@odata.type": "#IdentityPoolService.IdentityPool",
            "@odata.id": "/api/IdentityPoolService/IdentityPools(30)",
            "Id": 30,
            "Name": "pool1",
            "Description": "Identity pool with ethernet setting",
            "CreatedBy": "admin",
            "CreationTime": "2020-01-31 11:31:13.621182",
            "LastUpdatedBy": "admin",
            "LastUpdateTime": "2020-01-31 11:34:28.00876",
            "EthernetSettings": {
                "Mac": {
                    "IdentityCount": 70,
                    "StartingMacAddress": "qrvM3e6q"
                }
            },
            "IscsiSettings": None,
            "FcoeSettings": {
                "Mac": {
                    "IdentityCount": 70,
                    "StartingMacAddress": "cHBwcHAA"
                }
            },
            "FcSettings": None,
            "UsageCounts": {
                "@odata.id": "/api/IdentityPoolService/IdentityPools(30)/UsageCounts"
            },
            "UsageIdentitySets@odata.navigationLink": "/api/IdentityPoolService/IdentityPools(30)/UsageIdentitySets"
        }
        payload = self.module.get_updated_modify_payload(payload, existing_setting_payload)
        assert payload["Description"] == "Identity pool with ethernet setting"
        assert payload["EthernetSettings"]["Mac"]["IdentityCount"] == 70
        assert payload["EthernetSettings"]["Mac"]["StartingMacAddress"] == "abcd"
        assert payload["FcoeSettings"]["Mac"]["IdentityCount"] == 65
        assert payload["FcoeSettings"]["Mac"]["StartingMacAddress"] == "cHBwcHAA"

    def test_get_updated_modify_payload_case_05(self):
        """update remaining parameter of ethernet and fcoe setting will be null if not exists in existing payload"""
        payload = {"Name": "pool1", "EthernetSettings": {"Mac": {"StartingMacAddress": "abcd"}}, }
        existing_setting_payload = {"@odata.context": "/api/$metadata#IdentityPoolService.IdentityPool",
                                    "@odata.type": "#IdentityPoolService.IdentityPool",
                                    "@odata.id": "/api/IdentityPoolService/IdentityPools(30)", "Id": 30,
                                    "Name": "pool1",
                                    "Description": "Identity pool with ethernet setting", "CreatedBy": "admin",
                                    "CreationTime": "2020-01-31 11:31:13.621182",
                                    "LastUpdatedBy": "admin", "LastUpdateTime": "2020-01-31 11:34:28.00876",
                                    "EthernetSettings": {"Mac": {"StartingMacAddress": "qrvM3e6q"}},
                                    "IscsiSettings": None,
                                    "FcoeSettings": {"Mac": {"StartingMacAddress": "cHBwcHAA"}}, "FcSettings": None,
                                    "UsageCounts": {
                                        "@odata.id": "/api/IdentityPoolService/IdentityPools(30)/UsageCounts"},
                                    "UsageIdentitySets@odata.navigationLink": "/api/IdentityPoolService/IdentityPools(30)/UsageIdentitySets"}
        payload = self.module.get_updated_modify_payload(payload, existing_setting_payload)
        assert payload["Description"] == "Identity pool with ethernet setting"
        assert payload["EthernetSettings"]["Mac"]["StartingMacAddress"] == "abcd"
        assert "IdentityCount" not in payload["EthernetSettings"]["Mac"]

    @pytest.mark.parametrize("setting", ["EthernetSettings", "FcoeSettings"])
    def test_get_updated_modify_payload_case_06(self, setting):
        modify_payload = {"Name": "pool1", "EthernetSettings": {"Mac": {"StartingMacAddress": "abcd"}}, }
        existing_payload = {"@odata.context": "/api/$metadata#IdentityPoolService.IdentityPool",
                            "@odata.type": "#IdentityPoolService.IdentityPool",
                            "@odata.id": "/api/IdentityPoolService/IdentityPools(35)",
                            "Id": 35, "Name": "pool1",
                            "Description": "Identity pool with ethernet and fcoe settings1",
                            "CreatedBy": "admin", "CreationTime": "2020-02-01 07:55:59.923838",
                            "LastUpdatedBy": "admin", "LastUpdateTime": "2020-02-01 07:55:59.923838",
                            "EthernetSettings": {"Mac": {"IdentityCount": 60, "StartingMacAddress": "UFBQUFAA"}},
                            "IscsiSettings": None,
                            "FcoeSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "cHBwcHAA"}},
                            "FcSettings": None,
                            "UsageCounts": {"@odata.id": "/api/IdentityPoolService/IdentityPools(35)/UsageCounts"},
                            "UsageIdentitySets@odata.navigationLink": "/api/IdentityPoolService/IdentityPools(35)/UsageIdentitySets"}
        modify_payload = self.module.get_updated_modify_payload(modify_payload, existing_payload)
        assert modify_payload["EthernetSettings"]["Mac"]["StartingMacAddress"] == "abcd"
        assert modify_payload["EthernetSettings"]["Mac"]["IdentityCount"] == 60
        assert modify_payload["FcoeSettings"]["Mac"]["StartingMacAddress"] == "cHBwcHAA"
        assert modify_payload["FcoeSettings"]["Mac"]["IdentityCount"] == 70

    @pytest.mark.parametrize("setting", ["EthernetSettings", "FcoeSettings"])
    def test_update_modify_setting_case_success(self, setting):
        modify_payload = {"Name": "pool1", "EthernetSettings": {"Mac": {"StartingMacAddress": "abcd"}},
                          "FcoeSettings": {"Mac": {"IdentityCount": 55}}}
        existing_payload = {"@odata.context": "/api/$metadata#IdentityPoolService.IdentityPool",
                            "@odata.type": "#IdentityPoolService.IdentityPool",
                            "@odata.id": "/api/IdentityPoolService/IdentityPools(35)",
                            "Id": 35, "Name": "pool1",
                            "Description": "Identity pool with ethernet and fcoe settings1",
                            "CreatedBy": "admin", "CreationTime": "2020-02-01 07:55:59.923838",
                            "LastUpdatedBy": "admin", "LastUpdateTime": "2020-02-01 07:55:59.923838",
                            "EthernetSettings": {"Mac": {"IdentityCount": 60, "StartingMacAddress": "UFBQUFAA"}},
                            "IscsiSettings": None,
                            "FcoeSettings": {"Mac": {"IdentityCount": 70, "StartingMacAddress": "cHBwcHAA"}},
                            "FcSettings": None,
                            "UsageCounts": {"@odata.id": "/api/IdentityPoolService/IdentityPools(35)/UsageCounts"},
                            "UsageIdentitySets@odata.navigationLink": "/api/IdentityPoolService/IdentityPools(35)/UsageIdentitySets"}
        if setting == "EthernetSettings":
            self.module.update_modify_setting(modify_payload, existing_payload, setting, ["Mac"])
            assert modify_payload["EthernetSettings"]["Mac"]["StartingMacAddress"] == "abcd"
            assert modify_payload["EthernetSettings"]["Mac"]["IdentityCount"] == 60
        else:
            self.module.update_modify_setting(modify_payload, existing_payload, setting, ["Mac"])
            assert modify_payload["FcoeSettings"]["Mac"]["StartingMacAddress"] == "cHBwcHAA"
            assert modify_payload["FcoeSettings"]["Mac"]["IdentityCount"] == 55

    @pytest.mark.parametrize("mac_address",
                             ['50-50-50-50-50-50', '50:50:50:50:50:50', '5050.5050.5050', 'ab:cd:ef:70:80:70',
                              'aabb.ccdd.7070'])
    def test_mac_validation_match_case(self, mac_address):
        """valid MAC address formats"""
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
                                                        {'ab:cd:ef:70:80:70': 'q83vcIBw'},
                                                        {'20-00-50-50-50-50-50-50': 'IABQUFBQUFA='},
                                                        {'20-01-50-50-50-50-50-50': 'IAFQUFBQUFA='},
                                                        {'20:00:50:50:50:50:50:50': 'IABQUFBQUFA='},
                                                        {'20:01:50:50:50:50:50:50': 'IAFQUFBQUFA='},
                                                        {'2000.5050.5050.5050': 'IABQUFBQUFA='},
                                                        {'2001.5050.5050.5050': 'IAFQUFBQUFA='},
                                                        {'20:00:ab:cd:ef:70:80:70': 'IACrze9wgHA='},
                                                        {'20:01:ab:cd:ef:70:80:70': 'IAGrze9wgHA='},
                                                        ])
    def test_mac_to_base64_conversion(self, mac_address_base64_map):
        f_module = self.get_module_mock()
        mac_address = list(mac_address_base64_map.keys())[0]
        base_64_val_expected = list(mac_address_base64_map.values())[0]
        base_64_val = self.module.mac_to_base64_conversion(mac_address, f_module)
        assert base_64_val == base_64_val_expected

    def test_pool_delete_case_01(self, ome_connection_mock_for_identity_pool, mocker):
        params = {"pool_name": "pool_name"}
        mocker.patch(
            MODULE_PATH + 'ome_identity_pool.get_identity_pool_id_by_name',
            return_value=(1, {"value": "data"}))
        f_module = self.get_module_mock(params=params)
        message = self.module.pool_delete(f_module, ome_connection_mock_for_identity_pool)
        assert message["msg"] == "Successfully deleted the identity pool."

    def test_pool_delete_case_02(self, ome_connection_mock_for_identity_pool, mocker):
        params = {"pool_name": "pool_name"}
        mocker.patch(
            MODULE_PATH + 'ome_identity_pool.get_identity_pool_id_by_name',
            return_value=(0, {}))
        f_module = self.get_module_mock(params=params)
        with pytest.raises(Exception) as exc:
            self.module.pool_delete(f_module, ome_connection_mock_for_identity_pool)
        assert exc.value.args[0] == "The identity pool '{0}' is not present in the system.".format(params["pool_name"])

    def test_pool_delete_error_case_02(self, mocker, ome_connection_mock_for_identity_pool, ome_response_mock):
        msg = "exception message"
        params = {"pool_name": "pool_name"}
        mocker.patch(
            MODULE_PATH + 'ome_identity_pool.get_identity_pool_id_by_name',
            return_value=(1, "data"))
        f_module = self.get_module_mock(params=params)
        ome_connection_mock_for_identity_pool.invoke_request.side_effect = Exception(msg)
        with pytest.raises(Exception, match=msg) as exc:
            self.module.pool_delete(f_module, ome_connection_mock_for_identity_pool)

    def test_main_ome_identity_pool_delete_success_case1(self, mocker, ome_default_args,
                                                         ome_connection_mock_for_identity_pool, ome_response_mock):
        sub_param = {"pool_name": "pool1",
                     "state": "absent", }
        message_return = {"msg": "Successfully deleted the identity pool."}
        mocker.patch(MODULE_PATH + 'ome_identity_pool.pool_delete',
                     return_value=message_return)
        ome_default_args.update(sub_param)
        result = self.execute_module(ome_default_args)
        assert 'pool_status' not in result
        assert result["msg"] == "Successfully deleted the identity pool."

    def test_validate_modify_create_payload_no_exception_case(self):
        modify_payload = {
            "Id": 59,
            "Name": "pool_new",
            "EthernetSettings": {
                "Mac": {
                    "IdentityCount": 61,
                    "StartingMacAddress": "kJCQkJCQ"
                }
            },
            "IscsiSettings": {
                "Mac": {
                    "IdentityCount": 30,
                    "StartingMacAddress": "YGBgYGAA"
                },
                "InitiatorConfig": {
                    "IqnPrefix": "iqn.myprefix."
                },
                "InitiatorIpPoolSettings": {
                    "IpRange": "10.33.0.1-10.33.0.255",
                    "SubnetMask": "255.255.255.0",
                    "Gateway": "192.168.4.1",
                    "PrimaryDnsServer": "10.8.8.8",
                    "SecondaryDnsServer": "8.8.8.8"
                }
            },
            "FcoeSettings": {
                "Mac": {
                    "IdentityCount": 77,
                    "StartingMacAddress": "qrvM3VBQ"
                }
            },
            "FcSettings": {
                "Wwnn": {
                    "IdentityCount": 45,
                    "StartingAddress": "IAAQEBAQEBA="
                },
                "Wwpn": {
                    "IdentityCount": 45,
                    "StartingAddress": "IAEQEBAQEBA="
                }
            }
        }
        f_module = self.get_module_mock()
        self.module.validate_modify_create_payload(modify_payload, f_module, "create")

    modify_payload1 = {
        "Mac": {
            "IdentityCount": 61,
        }
    }
    modify_payload2 = {
        "Mac": {
            "StartingMacAddress": "kJCQkJCQ"
        }
    }

    modify_payload3 = {
        "Mac": {
        }
    }

    modify_payload4 = {
        "Mac": None
    }

    @pytest.mark.parametrize("setting", ["EthernetSettings", "FcoeSettings"])
    @pytest.mark.parametrize("action", ["create", "modify"])
    @pytest.mark.parametrize("payload", [modify_payload1, modify_payload2, modify_payload3, modify_payload4])
    def test_validate_modify_create_payload_failure_case1(self, payload, action, setting):
        modify_payload = {"Id": 59, "Name": "pool_new"}
        modify_payload[setting] = payload
        f_module = self.get_module_mock()
        msg = "Both starting MAC address and identity count is required to {0} an identity pool using {1} settings.".format(
            action, ''.join(setting.split('Settings')))
        with pytest.raises(Exception, match=msg) as exc:
            self.module.validate_modify_create_payload(modify_payload, f_module, action)

    modify_fc_setting1 = {"FcSettings": {
        "Wwnn": {
            "IdentityCount": 45,
        },
        "Wwpn": {
            "IdentityCount": 45,
        }
    }}
    modify_fc_setting2 = {"FcSettings": {
        "Wwnn": {
            "StartingAddress": "IAAQEBAQEBA="
        },
        "Wwpn": {
            "IdentityCount": 45,
            "StartingAddress": "IAEQEBAQEBA="
        }
    }}
    modify_fc_setting3 = {"FcSettings": {
        "Wwnn": {
            "StartingAddress": "IAAQEBAQEBA="
        },
        "Wwpn": {
            "StartingAddress": "IAEQEBAQEBA="
        }
    }}
    modify_fc_setting4 = {"FcSettings": {
        "Wwnn": {
        },
        "Wwpn": {
        }
    }}
    modify_fc_setting5 = {"FcSettings": {
        "Wwnn": None,
        "Wwpn": None}}

    @pytest.mark.parametrize("action", ["create", "modify"])
    @pytest.mark.parametrize("modify_payload",
                             [modify_fc_setting1, modify_fc_setting2, modify_fc_setting3, modify_fc_setting4,
                              modify_fc_setting5])
    def test_validate_modify_create_payload_failure_fc_setting_case(self, modify_payload, action):
        payload = {"Id": 59, "Name": "pool_new"}
        modify_payload.update(payload)
        f_module = self.get_module_mock()
        msg = "Both starting MAC address and identity count is required to {0} an identity pool using Fc settings.".format(
            action)
        with pytest.raises(Exception, match=msg) as exc:
            self.module.validate_modify_create_payload(modify_payload, f_module, action)

    @pytest.mark.parametrize("action", ["create", "modify"])
    @pytest.mark.parametrize("modify_payload",
                             [modify_fc_setting1, modify_fc_setting2, modify_fc_setting3, modify_fc_setting4,
                              modify_fc_setting5])
    # @pytest.mark.parametrize("modify_payload", [modify_fc_setting1])
    def test_validate_modify_create_payload_failure_fc_setting_case(self, modify_payload, action):
        payload = {"Id": 59, "Name": "pool_new"}
        modify_payload.update(payload)
        f_module = self.get_module_mock()
        msg = "Both starting MAC address and identity count is required to {0} an identity pool using Fc settings.".format(
            action)
        with pytest.raises(Exception, match=msg) as exc:
            self.module.validate_modify_create_payload(modify_payload, f_module, action)

    payload_iscsi1 = {"IscsiSettings": {
        "Mac": {
            "IdentityCount": 30
        }}}

    payload_iscsi2 = {"IscsiSettings": {
        "Mac": {
            "StartingMacAddress": "kJCQkJCQ"
        }}}
    payload_iscsi3 = {"IscsiSettings": {
        "Mac": {
        }}}

    @pytest.mark.parametrize("action", ["create", "modify"])
    @pytest.mark.parametrize("modify_payload", [payload_iscsi1, payload_iscsi2, payload_iscsi3])
    def test_validate_modify_create_payload_failure_iscsi_setting_case1(self, modify_payload, action):
        payload = {"Id": 59, "Name": "pool_new"}
        modify_payload.update(payload)
        f_module = self.get_module_mock()
        msg = "Both starting MAC address and identity count is required to {0} an identity pool using Iscsi settings.".format(
            action)
        with pytest.raises(Exception, match=msg) as exc:
            self.module.validate_modify_create_payload(modify_payload, f_module, action)

    payload_iscsi3 = {
        "SubnetMask": "255.255.255.0",
        "Gateway": "192.168.4.1",
        "PrimaryDnsServer": "10.8.8.8",
        "SecondaryDnsServer": "8.8.8.8"
    }

    payload_iscsi4 = {
        "IpRange": "10.33.0.1-10.33.0.255",
        "Gateway": "192.168.4.1",
        "PrimaryDnsServer": "10.8.8.8",
        "SecondaryDnsServer": "8.8.8.8"
    }
    payload_iscsi5 = {
        "PrimaryDnsServer": "10.8.8.8",
        "SecondaryDnsServer": "8.8.8.8"
    }

    @pytest.mark.parametrize("action", ["create", "modify"])
    @pytest.mark.parametrize("initiatorip_payload",
                             [payload_iscsi3, payload_iscsi4, payload_iscsi5])
    def test_validate_modify_create_payload_failure_iscsi_setting_case2(self, initiatorip_payload, action):
        modify_payload = {"Id": 59, "Name": "pool_new",
                          "IscsiSettings": {"Mac": {
                              "IdentityCount": 30,
                              "StartingMacAddress": "kJCQkJCQ"
                          },
                              "InitiatorConfig": {"IqnPrefix": "abc"}},
                          }
        modify_payload["IscsiSettings"]["InitiatorIpPoolSettings"] = initiatorip_payload
        f_module = self.get_module_mock()
        msg = "Both ip range and subnet mask in required to {0} an identity pool using iSCSI settings.".format(action)
        with pytest.raises(Exception, match=msg):
            self.module.validate_modify_create_payload(modify_payload, f_module, action)

    def test_update_fc_settings_success_case1(self):
        setting_params = {
            "identity_count": 45,
            "starting_address": "10-10-10-10-10-10"
        }
        payload = {"Name": "pool_name"}
        f_module = self.get_module_mock()
        self.module.update_fc_settings(payload, setting_params, "FcSettings", f_module)
        assert payload == {
            "Name": "pool_name",
            'FcSettings': {'Wwnn': {'IdentityCount': 45, 'StartingAddress': 'IAAQEBAQEBA='},
                           'Wwpn': {'IdentityCount': 45, 'StartingAddress': 'IAEQEBAQEBA='}
                           }
        }

    def test_update_fc_settings_success_case2(self):
        setting_params = {
            "identity_count": 45
        }
        payload = {"Name": "pool_name"}
        f_module = self.get_module_mock()
        self.module.update_fc_settings(payload, setting_params, "FcSettings", f_module)
        assert payload == {
            "Name": "pool_name",
            'FcSettings': {'Wwnn': {'IdentityCount': 45},
                           'Wwpn': {'IdentityCount': 45}}
        }

    def test_update_fc_settings_success_case3(self):
        setting_params = {
            "starting_address": "10-10-10-10-10-10"
        }
        payload = {"Name": "pool_name"}
        f_module = self.get_module_mock()
        self.module.update_fc_settings(payload, setting_params, "FcSettings", f_module)
        assert payload == {
            "Name": "pool_name",
            'FcSettings': {'Wwnn': {'StartingAddress': 'IAAQEBAQEBA='},
                           'Wwpn': {'StartingAddress': 'IAEQEBAQEBA='}
                           }
        }

    def test_update_fc_settings_mac_failure_case1(self):
        setting_params = {
            "identity_count": 45,
            "starting_address": "abcd.1010:1010"
        }
        payload = {"Name": "pool_name"}
        setting_type = "FcSettings"
        f_module = self.get_module_mock()
        msg = "Please provide the valid starting address format for FC settings."
        with pytest.raises(Exception, match=msg) as exc:
            self.module.update_fc_settings(payload, setting_params, setting_type, f_module)

    @pytest.mark.parametrize("mac", [{'50-50-50-50-50-50': ['20-00-', '20-01-']},
                                     {'50:50:50:50:50:50': ['20:00:', '20:01:']},
                                     {'5050.5050.5050': ['2000.', '2001.']},
                                     {'ab:cd:ef:70:80:70': ['20:00:', '20:01:']},
                                     {'aabb.ccdd.7070': ['2000.', '2001.']}])
    def test_get_wwn_address(self, mac):
        mac_address = list(mac.keys())[0]
        expected_values = list(mac.values())[0]
        wwnn_address_expected = expected_values[0]
        wwpn_address_expected = expected_values[1]
        wwnn_address, wwpn_address = self.module.get_wwn_address_prefix(mac_address)
        assert wwnn_address == wwnn_address_expected
        assert wwpn_address == wwpn_address_expected

    def test_update_iscsi_specific_settings_case1(self):
        setting_type = "IscsiSettings"
        payload = {"Name": "pool_new", setting_type: {"Mac": {"IdentityCount": 30, "StartingMacAddress": "YGBgYGAA"}}}
        settings_params = {
            "identity_count": 30,
            "initiator_config": {
                "iqn_prefix": "iqn.myprefix."
            },
            "initiator_ip_pool_settings": {
                "gateway": "192.168.4.1",
                "ip_range": "10.33.0.1-10.33.0.255",
                "primary_dns_server": "10.8.8.8",
                "secondary_dns_server": "8.8.8.8",
                "subnet_mask": "255.255.255.0"
            },
            "starting_mac_address": "60:60:60:60:60:00"
        }
        self.module.update_iscsi_specific_settings(payload, settings_params, setting_type)
        assert payload == {
            "Name": "pool_new",
            "IscsiSettings": {
                "Mac": {
                    "IdentityCount": 30,
                    "StartingMacAddress": "YGBgYGAA"
                },
                "InitiatorConfig": {
                    "IqnPrefix": "iqn.myprefix."
                },
                "InitiatorIpPoolSettings": {
                    "IpRange": "10.33.0.1-10.33.0.255",
                    "SubnetMask": "255.255.255.0",
                    "Gateway": "192.168.4.1",
                    "PrimaryDnsServer": "10.8.8.8",
                    "SecondaryDnsServer": "8.8.8.8"
                }
            }}

    def test_update_iscsi_specific_settings_case2(self):
        setting_type = "IscsiSettings"
        payload = {"Name": "pool_new", "Description": "description"}
        settings_params = {
            "initiator_ip_pool_settings": {
                "gateway": "192.168.4.1",
                "ip_range": "10.33.0.1-10.33.0.255",
                "subnet_mask": "255.255.255.0"
            }
        }
        self.module.update_iscsi_specific_settings(payload, settings_params, setting_type)
        assert payload == {
            "Name": "pool_new", "Description": "description",
            "IscsiSettings": {
                "InitiatorIpPoolSettings": {
                    "IpRange": "10.33.0.1-10.33.0.255",
                    "SubnetMask": "255.255.255.0",
                    "Gateway": "192.168.4.1"
                }
            }}
