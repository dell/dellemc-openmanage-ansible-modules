# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.3
# Copyright (C) 2020 Dell Inc. or its subsidiaries. All Rights Reserved.

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
from ansible_collections.dellemc.openmanage.plugins.modules import ome_network_vlan
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_network_vlan.'


@pytest.fixture
def ome_connection_mock_for_network_vlan(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeNetworkVlan(FakeAnsibleModule):
    module = ome_network_vlan

    @pytest.mark.parametrize("params",
                             [{"success": True, "json_data": {"value": [{"Name": "vlan_name", "Id": 123}]}, "id": 123},
                              {"success": True, "json_data": {"value": []}, "id": 0},
                              {"success": False, "json_data": {"value": [{"Name": "vlan_name", "Id": 123}]}, "id": 0},
                              {"success": True, "json_data": {"value": [{"Name": "vlan_name1", "Id": 123}]}, "id": 0}])
    def test_get_item_id(self, params, ome_connection_mock_for_network_vlan, ome_response_mock):
        ome_response_mock.success = params["success"]
        ome_response_mock.json_data = params["json_data"]
        id, vlans = self.module.get_item_id(ome_connection_mock_for_network_vlan, "vlan_name", "uri")
        assert id == params["id"]

    @pytest.mark.parametrize("vlan_param",
                             [{"in": {"name": "vlan1", "type": 1, "vlan_maximum": 40, "vlan_minimum": 35},
                               "out": {"Name": "vlan1", "Type": 1, "VlanMaximum": 40, "VlanMinimum": 35}},
                              {"in": None, "out": None}])
    def test_format_payload(self, vlan_param):
        result = self.module.format_payload(vlan_param["in"])
        assert result == vlan_param["out"]

    def test_delete_vlan(self, ome_connection_mock_for_network_vlan, ome_response_mock):
        ome_response_mock.success = True
        ome_response_mock.json_data = {}
        f_module = self.get_module_mock(params={"name": "vlan1"})
        with pytest.raises(Exception, match="Successfully deleted the VLAN.") as err:
            self.module.delete_vlan(f_module, ome_connection_mock_for_network_vlan, 12)

    @pytest.mark.parametrize("params",
                             [{"format_payload": {"VlanMaximum": None, "VlanMinimum": 35},
                               "error_msg": "The vlan_minimum, vlan_maximum and type values are required for creating"
                                            " a VLAN.", "overlap": {}},
                              {"format_payload": {"VlanMaximum": 40, "VlanMinimum": 45}, "overlap": {},
                               "error_msg": "VLAN-minimum value is greater than VLAN-maximum value."},
                              {"format_payload": {"VlanMaximum": 40, "VlanMinimum": 35},
                               "overlap": {"Name": "vlan1", "Type": 1, "VlanMaximum": 40, "VlanMinimum": 35},
                               "error_msg": "Unable to create or update the VLAN because the entered range"
                                            " overlaps with vlan1 with the range 35-40."},
                              {"format_payload": {"VlanMaximum": 40, "VlanMinimum": 35},
                               "error_msg": "Network type 'General Purpose (Silver)' not found.",
                               "overlap": {}},
                              {"format_payload": {"VlanMaximum": 40, "VlanMinimum": 35}, "item": 1, "overlap": {},
                               "check_mode": True, "error_msg": "Changes found to be applied."},
                              ])
    def test_create_vlan(self, mocker, params, ome_connection_mock_for_network_vlan, ome_response_mock):
        f_module = self.get_module_mock(params={"name": "vlan1", "vlan_maximum": 40, "vlan_minimum": 35,
                                                "type": "General Purpose (Silver)"}, check_mode=params.get("check_mode", False))
        mocker.patch(MODULE_PATH + "format_payload", return_value=(params["format_payload"]))
        mocker.patch(MODULE_PATH + "check_overlapping_vlan_range", return_value=(params["overlap"]))
        mocker.patch(MODULE_PATH + "get_item_id", return_value=(0, []))
        error_message = params["error_msg"]
        with pytest.raises(Exception) as err:
            self.module.create_vlan(f_module, ome_connection_mock_for_network_vlan, [])
        assert err.value.args[0] == error_message

    @pytest.mark.parametrize("params",
                             [{"format_payload": {"VlanMaximum": 40, "VlanMinimum": 35},
                               "error_msg": "Network type 'General Purpose (Silver)' not found.",
                               "overlap": {}},
                              {"format_payload": {"Name": "vlan11", "Type": 1, "VlanMaximum": 40, "VlanMinimum": 45},
                               "overlap": {}, "item": 1,
                               "error_msg": "VLAN-minimum value is greater than VLAN-maximum value."},
                              {"format_payload": {"VlanMaximum": 40, "VlanMinimum": 35}, "item": 1,
                               "overlap": {"Name": "vlan1", "Type": 1, "VlanMaximum": 40, "VlanMinimum": 35},
                               "error_msg": "Unable to create or update the VLAN because the entered range"
                                            " overlaps with vlan1 with the range 35-40."},
                              {"format_payload": {"Name": "vlan11", "Type": 1, "VlanMaximum": 45, "VlanMinimum": 40},
                               "item": 1, "overlap": {},
                               "check_mode": True, "error_msg": "Changes found to be applied."},
                              ])
    def test_modify_vlan(self, mocker, params, ome_connection_mock_for_network_vlan, ome_response_mock):
        f_module = self.get_module_mock(params={"name": "vlan1", "vlan_maximum": 40, "vlan_minimum": 45,
                                                "type": "General Purpose (Silver)"},
                                        check_mode=params.get("check_mode", False))
        mocker.patch(MODULE_PATH + "format_payload", return_value=(params["format_payload"]))
        mocker.patch(MODULE_PATH + "check_overlapping_vlan_range", return_value=(params["overlap"]))
        mocker.patch(MODULE_PATH + "get_item_id", return_value=(params.get("item", 0), []))
        error_message = params["error_msg"]
        with pytest.raises(Exception) as err:
            self.module.modify_vlan(f_module, ome_connection_mock_for_network_vlan, 123,
                                    [{"Id": 13, "Name": "vlan11", "Type": 1, "VlanMaximum": 140, "VlanMinimum": 135},
                                     {"Id": 123, "Name": "vlan1", "Type": 1, "VlanMaximum": 40, "VlanMinimum": 35,
                                      'Description': None}])
        assert err.value.args[0] == error_message

    def test_main_case_create_success(self, mocker, ome_default_args, ome_connection_mock_for_network_vlan, ome_response_mock):
        mocker.patch(MODULE_PATH + "check_existing_vlan", return_value=(0, [{"VlanMaximum": 40, "VlanMinimum": 35}]))
        mocker.patch(MODULE_PATH + "get_item_id", return_value=(1, []))
        mocker.patch(MODULE_PATH + "check_overlapping_vlan_range", return_value=None)
        ome_default_args.update(
            {"name": "vlan1", "state": "present", "type": "General Purpose (Bronze)",
             "vlan_maximum": 40, "vlan_minimum": 35})
        ome_response_mock.json_data = {"Id": 14227, "Name": "vlan1", "Type": 1,
                                       "VlanMaximum": 40, "VlanMinimum": 35}
        result = self.execute_module(ome_default_args)
        assert result['changed'] is True
        assert "msg" in result
        assert result['vlan_status'] == {"Id": 14227, "Name": "vlan1", "Type": 1,
                                         "VlanMaximum": 40, "VlanMinimum": 35}
        assert result["msg"] == "Successfully created the VLAN."

    def test_main_case_modify_success(self, mocker, ome_default_args, ome_connection_mock_for_network_vlan, ome_response_mock):
        mocker.patch(MODULE_PATH + "check_existing_vlan", return_value=(1, [{"Id": 1, "VlanMaximum": 40, "VlanMinimum": 35}]))
        mocker.patch(MODULE_PATH + "get_item_id", return_value=(2, []))
        mocker.patch(MODULE_PATH + "check_overlapping_vlan_range", return_value=None)
        ome_default_args.update(
            {"name": "vlan1", "state": "present", "type": "General Purpose (Bronze)",
             "vlan_maximum": 40, "vlan_minimum": 35})
        ome_response_mock.json_data = {"Id": 14227, "Name": "vlan1", "Type": 2, "VlanMaximum": 40, "VlanMinimum": 35}
        result = self.execute_module(ome_default_args)
        assert result['changed'] is True
        assert "msg" in result
        assert result['vlan_status'] == {"Id": 14227, "Name": "vlan1", "Type": 2, "VlanMaximum": 40, "VlanMinimum": 35}
        assert result["msg"] == "Successfully updated the VLAN."

    @pytest.mark.parametrize("params",
                             [{"payload": {"VlanMaximum": 40, "VlanMinimum": 35},
                               "vlans": [{"VlanMaximum": 40, "VlanMinimum": 35}],
                               "current_vlan": {"VlanMaximum": 40, "VlanMinimum": 35}}])
    def test_check_overlapping_vlan_range(self, params, ome_connection_mock_for_network_vlan, ome_response_mock):
        result = self.module.check_overlapping_vlan_range(params["payload"], params["vlans"])
        assert result == params["current_vlan"]

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_application_network_vlan_main_exception_failure_case(self, exc_type, mocker, ome_default_args,
                                                                      ome_connection_mock_for_network_vlan,
                                                                      ome_response_mock):
        ome_default_args.update({"name": "vlan1", "state": "present", "type": "General Purpose (Bronze)",
                                 "vlan_maximum": 40, "vlan_minimum": 35})
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'check_existing_vlan', side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'check_existing_vlan', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'check_existing_vlan',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'vlan_status' not in result
        assert 'msg' in result
