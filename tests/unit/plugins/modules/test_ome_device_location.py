# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.2.0
# Copyright (C) 2021-2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
from io import StringIO
from ssl import SSLError

import pytest
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import ome_device_location
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_device_location.'
PARAM_DATA_CENTER = "data center 1"
PARAM_ROOM = "room 1"
PARAM_AISLE = "aisle 1"
PARAM_RACK = "rack 1"
PARAM_LOCATION = "location 1"


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
        result = self.module.check_domain_service(
            f_module, ome_conn_mock_location)
        assert result is None

    def test_standalone_chassis(self, ome_conn_mock_location, ome_default_args, mocker, ome_response_mock):
        mocker.patch(MODULE_PATH + "get_ip_from_host",
                     return_value="X.X.X.X")
        ome_response_mock.json_data = {"value": [{"DeviceId": 25011, "DomainRoleTypeValue": "LEAD",
                                                  "PublicAddress": ["XX.XX.XX.XX"]},
                                                 {"DeviceId": 25012, "DomainRoleTypeValue": "STANDALONE",
                                                  "PublicAddress": ["YY.YY.YY.YY"]}]}

        param = {"data_center": PARAM_DATA_CENTER, "rack_slot": 2, "device_id": 25012, "hostname": "XY.XY.XY.XY",
                 "room": PARAM_ROOM, "aisle": PARAM_AISLE, "rack": PARAM_RACK, "location": PARAM_LOCATION}
        f_module = self.get_module_mock(params=param)
        with pytest.raises(Exception) as err:
            self.module.standalone_chassis(f_module, ome_conn_mock_location)
        assert err.value.args[0] == "Failed to fetch the device information."

    def test_validate_dictionary(self, ome_conn_mock_location, ome_default_args, mocker):
        param = {"data_center": PARAM_DATA_CENTER, "rack_slot": 2,
                 "room": PARAM_ROOM, "aisle": PARAM_AISLE, "rack": PARAM_RACK, "location": PARAM_LOCATION}
        f_module = self.get_module_mock(params=param)
        f_module.check_mode = True
        loc_resp = {"DataCenter": PARAM_DATA_CENTER, "RackSlot": 2, "Room": PARAM_ROOM,
                    "Aisle": PARAM_AISLE, "RackName": PARAM_RACK, "Location": PARAM_LOCATION}
        with pytest.raises(Exception) as err:
            self.module.validate_dictionary(f_module, loc_resp)
        loc_resp = {"DataCenter": PARAM_DATA_CENTER, "RackSlot": 3, "Room": PARAM_ROOM,
                    "Aisle": PARAM_AISLE, "RackName": PARAM_RACK, "Location": PARAM_LOCATION}
        with pytest.raises(Exception) as err:
            self.module.validate_dictionary(f_module, loc_resp)
        assert err.value.args[0] == "Changes found to be applied."
        loc_resp = {"DataCenter": PARAM_DATA_CENTER, "RackSlot": 2, "Room": PARAM_ROOM,
                    "Aisle": PARAM_AISLE, "RackName": PARAM_RACK, "Location": PARAM_LOCATION}
        f_module.check_mode = False
        with pytest.raises(Exception) as err:
            self.module.validate_dictionary(f_module, loc_resp)
        assert err.value.args[0] == "No changes found to be applied."
        loc_resp = {"DataCenter": PARAM_DATA_CENTER, "RackSlot": 3, "Room": PARAM_ROOM,
                    "Aisle": PARAM_AISLE, "RackName": PARAM_RACK, "Location": PARAM_LOCATION}
        result = self.module.validate_dictionary(f_module, loc_resp)
        assert result == {"DataCenter": PARAM_DATA_CENTER, "RackSlot": 2,
                          "Room": PARAM_ROOM, "Aisle": PARAM_AISLE, "RackName": PARAM_RACK,
                          "Location": PARAM_LOCATION, "SettingType": "Location"}

    def test_device_validation(self, ome_conn_mock_location, ome_default_args, mocker, ome_response_mock):
        mocker.patch(MODULE_PATH + "validate_dictionary",
                     return_value={"DataCenter": PARAM_DATA_CENTER, "RackSlot": 2, "Room": PARAM_ROOM,
                                   "Aisle": PARAM_AISLE, "RackName": PARAM_RACK, "Location": PARAM_LOCATION,
                                   "SettingType": "Location"})
        param = {"data_center": PARAM_DATA_CENTER, "rack_slot": 2, "device_id": 25012,
                 "room": PARAM_ROOM, "aisle": PARAM_AISLE, "rack": PARAM_RACK, "location": PARAM_LOCATION}
        ome_default_args.update(param)
        f_module = self.get_module_mock(params=param)
        ome_response_mock.status_code = 200
        ome_response_mock.success = True
        ome_response_mock.json_data = {
            "value": [], "DataCenter": PARAM_DATA_CENTER,
            "RackSlot": 3, "Room": PARAM_ROOM, "Aisle": PARAM_AISLE, "RackName": PARAM_RACK,
            "Location": PARAM_LOCATION, "SettingType": "Location", "result": {"RackSlot": 4}}
        with pytest.raises(Exception) as err:
            self.module.device_validation(f_module, ome_conn_mock_location)
        assert err.value.args[0] == "Unable to complete the operation because the entered target " \
                                    "device id '25012' is invalid."

    @pytest.mark.parametrize("params", [
        {"json_data": {"value": [
            {'Id': 1234, 'PublicAddress': "xxx.xxx.x.x",
                'DeviceId': 1234, "Type": 1000},
            {'PublicAddress': "X.X.X.X", 'DeviceId': 1235, "Type": 1000}]},
            'message': "Successfully updated the location settings.",
            'mparams': {"hostname": "xxx.xxx.x.x",
                        "device_id": 1234, "data_center": "data center",
                        "room": "room", "aisle": "aisle", "rack": "rack"}
         },
        {"json_data": {"value": [
            {'Id': 1234, 'DeviceServiceTag': 'ABCD123',
                'PublicAddress': "xxx.xxx.x.x", 'DeviceId': 1234, "Type": 1000},
            {'PublicAddress': "X.X.X.X", 'DeviceId': 1235, "Type": 1000}]},
            'message': "Successfully updated the location settings.",
            'mparams': {"hostname": "xxx.xxx.x.x",
                        "device_service_tag": "ABCD123", "data_center": "data center",
                        "room": "room", "aisle": "aisle", "rack": "rack"}
         },
        {"json_data": {"value": [
            {'Id': 1234, 'PublicAddress': "xxx.xxx.x.x",
                'DeviceId': 1234, "Type": 1000},
            {'PublicAddress': "X.X.X.X", 'DeviceId': 1235, "Type": 1000}]},
            'message': "Successfully updated the location settings.",
            'mparams': {"hostname": "xxx.xxx.x.x",
                        "data_center": "data center",
                        "room": "room", "aisle": "aisle", "rack": "rack"}
         },
        {"json_data": {"value": [
            {'Id': 1234, 'PublicAddress': "dummyhost_shouldnotexist",
                'DeviceId': 1234, "Type": 1000},
            {'PublicAddress': "X.X.X.X", 'DeviceId': 1235, "Type": 1000}]},
            'message': "Successfully updated the location settings.",
            'mparams': {"hostname": "dummyhost_shouldnotexist",
                        "data_center": "data center",
                        "room": "room", "aisle": "aisle", "rack": "rack"}
         }
    ])
    def test_ome_devices_location_success(self, params, ome_conn_mock_location, ome_response_mock,
                                          ome_default_args, module_mock, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['json_data']
        ome_default_args.update(params['mparams'])
        result = self._run_module(
            ome_default_args, check_mode=params.get('check_mode', False))
        assert result['msg'] == params['message']

    @pytest.mark.parametrize("params", [
        {"json_data": {"value": [
            {'Id': 1234, 'PublicAddress': "xxx.xxx.x.x",
                'DeviceId': 1234, "Type": 1000},
            {'PublicAddress': "X.X.X.X", 'DeviceId': 1235, "Type": 1000}]},
            'message': "The device location settings operation is supported only on OpenManage Enterprise Modular systems.",
            'http_error_json': {
                "error": {
                    "code": "Base.1.0.GeneralError",
                    "message": "A general error has occurred. See ExtendedInfo for more information.",
                    "@Message.ExtendedInfo": [
                        {
                            "MessageId": "CGEN1006",
                            "RelatedProperties": [],
                            "Message": "Unable to process the request because an error occurred.",
                            "MessageArgs": [],
                            "Severity": "Critical",
                            "Resolution": "Retry the operation. If the issue persists, contact your system administrator."
                        }
                    ]
                }
        },
            'mparams': {"hostname": "xxx.xxx.x.x",
                        "data_center": "data center",
                        "room": "room", "aisle": "aisle", "rack": "rack"}
        },
        {"json_data": {"value": [
            {'Id': 1234, 'PublicAddress': "xxx.xxx.x.x",
                'DeviceId': 1234, "Type": 1000},
            {'PublicAddress': "X.X.X.X", 'DeviceId': 1235, "Type": 1000}]},
            'message': "Unable to complete the operation because the location settings are not supported on the specified device.",
            'http_error_json': {
                "error": {
                    "code": "Base.1.0.GeneralError",
                    "message": "A general error has occurred. See ExtendedInfo for more information.",
                    "@Message.ExtendedInfo": [
                        {
                            "MessageId": "CGEN1004",
                            "RelatedProperties": [],
                            "Message": "Unable to process the request because an error occurred.",
                            "MessageArgs": [],
                            "Severity": "Critical",
                            "Resolution": "Retry the operation. If the issue persists, contact your system administrator."
                        }
                    ]
                }
        },
            'check_domain_service': 'mocked_check_domain_service',
            'standalone_chassis': ('Id', 1234),
            'mparams': {"hostname": "xxx.xxx.x.x",
                        "data_center": "data center",
                        "room": "room", "aisle": "aisle", "rack": "rack"}
        },
        {"json_data": {"value": [
            {'Id': 1234, 'PublicAddress': "xxx.xxx.x.x",
                'DeviceId': 1234, "Type": 1000},
            {'PublicAddress': "X.X.X.X", 'DeviceId': 1235, "Type": 1000}]},
            'message': "Unable to complete the operation because the entered target device id '123' is invalid.",
            'mparams': {"hostname": "xxx.xxx.x.x.x.x.x.x", "device_id": 123,
                        "data_center": "data center",
                        "room": "room", "aisle": "aisle", "rack": "rack"}
         },
    ])
    def test_ome_devices_location_failure(self, params, ome_conn_mock_location, ome_response_mock,
                                          ome_default_args, module_mock, mocker):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params['json_data']
        mocks = ["check_domain_service", "standalone_chassis"]
        for m in mocks:
            if m in params:
                mocker.patch(MODULE_PATH + m, return_value=params.get(m, {}))
        if 'http_error_json' in params:
            json_str = to_text(json.dumps(params.get('http_error_json', {})))
            ome_conn_mock_location.invoke_request.side_effect = HTTPError(
                'https://testhost.com', 401, 'http error message', {
                    "accept-type": "application/json"},
                StringIO(json_str))
        ome_default_args.update(params['mparams'])
        result = self._run_module_with_fail_json(ome_default_args)
        assert result['msg'] == params['message']

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_device_location_main_exception_case(self, exc_type, mocker, ome_default_args,
                                                     ome_conn_mock_location, ome_response_mock):
        ome_default_args.update({"device_id": 25011, "data_center": PARAM_DATA_CENTER,
                                 "room": PARAM_ROOM, "aisle": PARAM_AISLE, "rack": PARAM_RACK,
                                 "rack_slot": "2", "location": PARAM_LOCATION})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'check_domain_service',
                         side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'check_domain_service',
                         side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'check_domain_service',
                         side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result
