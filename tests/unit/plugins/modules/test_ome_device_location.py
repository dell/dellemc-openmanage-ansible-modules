# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 4.3.0
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
from ansible_collections.dellemc.openmanage.plugins.modules import ome_device_location
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_device_location.'


@pytest.fixture
def ome_conn_mock_location(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOMEMDeviceLocation(FakeAnsibleModule):

    module = ome_device_location

    def test_check_domain_service(self, ome_conn_mock_location, ome_default_args, mocker):
        f_module = self.get_module_mock()
        result = self.module.check_domain_service(f_module, ome_conn_mock_location)
        assert result is None

    def test_standalone_chassis(self, ome_conn_mock_location, ome_default_args, mocker, ome_response_mock):
        mocker.patch(MODULE_PATH + "get_ip_from_host", return_value="192.18.1.1")
        ome_response_mock.json_data = {"value": [{"DeviceId": 25011, "DomainRoleTypeValue": "LEAD",
                                                  "PublicAddress": ["192.168.1.1"]},
                                                 {"DeviceId": 25012, "DomainRoleTypeValue": "STANDALONE",
                                                  "PublicAddress": ["192.168.1.2"]}]}

        param = {"data_center": "data center 1", "rack_slot": 2, "device_id": 25012, "hostname": "192.168.1.6",
                 "room": "room 1", "aisle": "aisle 1", "rack": "rack 1", "location": "location 1"}
        f_module = self.get_module_mock(params=param)
        with pytest.raises(Exception) as err:
            self.module.standalone_chassis(f_module, ome_conn_mock_location)
        assert err.value.args[0] == "Failed to fetch the device information."

    def test_validate_dictionary(self, ome_conn_mock_location, ome_default_args, mocker):
        param = {"data_center": "data center 1", "rack_slot": 2,
                 "room": "room 1", "aisle": "aisle 1", "rack": "rack 1", "location": "location 1"}
        f_module = self.get_module_mock(params=param)
        f_module.check_mode = True
        loc_resp = {"DataCenter": "data center 1", "RackSlot": 2, "Room": "room 1",
                    "Aisle": "aisle 1", "RackName": "rack 1", "Location": "location 1"}
        with pytest.raises(Exception) as err:
            self.module.validate_dictionary(f_module, loc_resp)
        loc_resp = {"DataCenter": "data center 1", "RackSlot": 3, "Room": "room 1",
                    "Aisle": "aisle 1", "RackName": "rack 1", "Location": "location 1"}
        with pytest.raises(Exception) as err:
            self.module.validate_dictionary(f_module, loc_resp)
        assert err.value.args[0] == "Changes found to be applied."
        loc_resp = {"DataCenter": "data center 1", "RackSlot": 2, "Room": "room 1",
                    "Aisle": "aisle 1", "RackName": "rack 1", "Location": "location 1"}
        f_module.check_mode = False
        with pytest.raises(Exception) as err:
            self.module.validate_dictionary(f_module, loc_resp)
        assert err.value.args[0] == "No changes found to be applied."
        loc_resp = {"DataCenter": "data center 1", "RackSlot": 3, "Room": "room 1",
                    "Aisle": "aisle 1", "RackName": "rack 1", "Location": "location 1"}
        result = self.module.validate_dictionary(f_module, loc_resp)
        assert result == {"DataCenter": "data center 1", "RackSlot": 2,
                          "Room": "room 1", "Aisle": "aisle 1", "RackName": "rack 1",
                          "Location": "location 1", "SettingType": "Location"}

    def test_device_validation(self, ome_conn_mock_location, ome_default_args, mocker, ome_response_mock):
        mocker.patch(MODULE_PATH + "validate_dictionary",
                     return_value={"DataCenter": "data center 1", "RackSlot": 2, "Room": "room 1",
                                   "Aisle": "aisle 1", "RackName": "rack 1", "Location": "location 1",
                                   "SettingType": "Location"})
        param = {"data_center": "data center 1", "rack_slot": 2, "device_id": 25012,
                 "room": "room 1", "aisle": "aisle 1", "rack": "rack 1", "location": "location 1"}
        ome_default_args.update(param)
        f_module = self.get_module_mock(params=param)
        ome_response_mock.status_code = 200
        ome_response_mock.success = True
        ome_response_mock.json_data = {
            "value": [], "DataCenter": "data center 1",
            "RackSlot": 3, "Room": "room 1", "Aisle": "aisle 1", "RackName": "rack 1",
            "Location": "location 1", "SettingType": "Location", "result": {"RackSlot": 4}}
        with pytest.raises(Exception) as err:
            self.module.device_validation(f_module, ome_conn_mock_location)
        assert err.value.args[0] == "Unable to complete the operation because the entered target " \
                                    "device id '25012' is invalid."

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_device_location_main_exception_case(self, exc_type, mocker, ome_default_args,
                                                     ome_conn_mock_location, ome_response_mock):
        ome_default_args.update({"device_id": 25011, "data_center": "data center 1",
                                 "room": "room 1", "aisle": "aisle 1", "rack": "rack 1",
                                 "rack_slot": "2", "location": "location 1"})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'check_domain_service', side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'check_domain_service', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'check_domain_service',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result
