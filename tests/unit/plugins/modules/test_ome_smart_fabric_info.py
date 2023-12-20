# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.1.0
# Copyright (C) 2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import ome_smart_fabric_info
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from io import StringIO
from ssl import SSLError
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


@pytest.fixture
def ome_connection_smart_fabric_info_mock(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(
        MODULE_PATH + 'ome_smart_fabric_info.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOMESmartFabricInfo(FakeAnsibleModule):
    module = ome_smart_fabric_info

    smart_fabric_details_dict = [{"Description": "Fabric f1",
                                  "FabricDesignMapping": [
                                      {
                                          "DesignNode": "Switch-A",
                                          "PhysicalNode": "NODEID1"
                                      },
                                      {
                                          "DesignNode": "Switch-B",
                                          "PhysicalNode": "NODEID2"
                                      }],
                                  "Id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2",
                                  "LifeCycleStatus": [
                                      {
                                        "Activity": "Create",
                                        "Status": "2060"
                                      }
                                  ],
                                  "Uplinks": [
                                      {
                                          "Id": "1ad54420-b145-49a1-9779-21a579ef6f2d",
                                          "MediaType": "Ethernet",
                                          "Name": "u1",
                                          "NativeVLAN": 1}],
                                  "Switches": [
                                      {
                                          "ChassisServiceTag": "6H5S6Z2",
                                          "ConnectionState": True}],
                                  "Servers": [
                                      {
                                          "ChassisServiceTag": "6H5S6Z2",
                                          "ConnectionState": True,
                                          "ConnectionStateReason": 101}],

                                  "Multicast": [
                                      {
                                          "FloodRestrict": True,
                                          "IgmpVersion": "3",
                                          "MldVersion": "2"
                                      }
                                  ],
                                  "FabricDesign": [
                                      {
                                          "FabricDesignNode": [
                                              {
                                                  "ChassisName": "Chassis-X",
                                                  "NodeName": "Switch-B",
                                                  "Slot": "Slot-A2",
                                                  "Type": "WeaverSwitch"
                                              },
                                              {
                                                  "ChassisName": "Chassis-X",
                                                  "NodeName": "Switch-A",
                                                  "Slot": "Slot-A1",
                                                  "Type": "WeaverSwitch"
                                              }
                                          ],
                                          "Name": "2xMX9116n_Fabric_Switching_Engines_in_same_chassis",
                                      }
                                  ],
                                  "Name": "f2",
                                  "OverrideLLDPConfiguration": "Disabled",
                                  "ScaleVLANProfile": "Enabled",
                                  "Summary": {
                                      "NodeCount": 2,
                                      "ServerCount": 1,
                                      "UplinkCount": 1
                                  }}]

    @pytest.mark.parametrize("params", [{"json_data": {"Multicast": {
        "@odata.id": "/api/NetworkService/Fabrics('61c20a59-9ed5-4ae5-b850-5e5acf42d2f2')/Multicast",
        "Id": "123hg"}}, "json_data_two": {"Multicast": {
            "@odata.id": "/api/NetworkService/Fabrics('61c20a59-9ed5-4ae5-b850-5e5acf42d2f2')/Multicast"}},
        "json_data_three": {"Id": 123},
        "output_one": {'Multicast': {'Id': "123hg"}}, "output_two": {}, "output_three": {"Id": 123}}])
    def test_clean_data(self, params):
        result_one = self.module.clean_data(params.get("json_data"))
        result_two = self.module.clean_data(params.get("json_data_two"))
        result_three = self.module.clean_data(params.get("json_data_three"))
        assert result_one == params.get("output_one")
        assert result_two == params.get("output_two")
        assert result_three == params.get("output_three")

    @pytest.mark.parametrize("params", [{"json_data": {
        "Id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2",
        "Name": "f1",
        "Description": "Fabric f1",
        "Switches@odata.navigationLink": "/api/NetworkService/Fabrics('61c20a59-9ed5-4ae5-b850-5e5acf42d2f2')/Switches",
        "Servers@odata.navigationLink": "/api/NetworkService/Fabrics('61c20a59-9ed5-4ae5-b850-5e5acf42d2f2')/Servers",
        "FabricDesign": {
                "@odata.id": "/api/NetworkService/Fabrics('61c20a59-9ed5-4ae5-b850-5e5acf42d2f2')/FabricDesign"
        },
        "ValidationErrors@odata.navigationLink": "/api/NetworkService/Fabrics('61c20a59-9ed5-4ae5-b850-5e5acf42d2f2')/ValidationErrors",
        "Uplinks@odata.navigationLink": "/api/NetworkService/Fabrics('61c20a59-9ed5-4ae5-b850-5e5acf42d2f2')/Uplinks",
        "Topology": {
            "@odata.id": "/api/NetworkService/Fabrics('61c20a59-9ed5-4ae5-b850-5e5acf42d2f2')/Topology"
        },
        "ISLLinks@odata.navigationLink": "/api/NetworkService/Fabrics('61c20a59-9ed5-4ae5-b850-5e5acf42d2f2')/ISLLinks",
        "Multicast": {
            "@odata.id": "/api/NetworkService/Fabrics('61c20a59-9ed5-4ae5-b850-5e5acf42d2f2')/Multicast"
        }
    }}])
    def test_fetch_smart_fabric_link_details(self, params, ome_connection_mock):
        f_module = self.get_module_mock()
        result = self.module.fetch_smart_fabric_link_details(
            f_module, ome_connection_mock, params.get('json_data'))
        assert result is not None

    @pytest.mark.parametrize("params", [{"json_data": {
        "Id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2",
        "Name": "f1",
        "Description": "Fabric f1",
        "Switches@odata.navigationLink": "/api/NetworkService/Fabrics('61c20a59-9ed5-4ae5-b850-5e5acf42d2f2')/Switches",
        "Servers@odata.navigationLink": "/api/NetworkService/Fabrics('61c20a59-9ed5-4ae5-b850-5e5acf42d2f2')/Servers",
        "FabricDesign": {
                "@odata.id": "/api/NetworkService/Fabrics('61c20a59-9ed5-4ae5-b850-5e5acf42d2f2')/FabricDesign"
        },
        "ValidationErrors@odata.navigationLink": "/api/NetworkService/Fabrics('61c20a59-9ed5-4ae5-b850-5e5acf42d2f2')/ValidationErrors",
        "Uplinks@odata.navigationLink": "/api/NetworkService/Fabrics('61c20a59-9ed5-4ae5-b850-5e5acf42d2f2')/Uplinks",
        "Topology": {
            "@odata.id": "/api/NetworkService/Fabrics('61c20a59-9ed5-4ae5-b850-5e5acf42d2f2')/Topology"
        },
        "ISLLinks@odata.navigationLink": "/api/NetworkService/Fabrics('61c20a59-9ed5-4ae5-b850-5e5acf42d2f2')/ISLLinks",
        "Multicast": {
            "@odata.id": "/api/NetworkService/Fabrics('61c20a59-9ed5-4ae5-b850-5e5acf42d2f2')/Multicast"
        }
    }}])
    def test_fetch_smart_fabric_link_details_HTTPError_error_case(self, params, ome_default_args, mocker, ome_connection_mock):
        json_str = to_text(json.dumps({"info": "error_details"}))
        error_msg = "Unable to retrieve smart fabric information."
        ome_connection_mock.invoke_request.side_effect = HTTPError('https://testdell.com', 404,
                                                                   error_msg,
                                                                   {"accept-type": "application/json"},
                                                                   StringIO(json_str))
        f_module = self.get_module_mock()
        with pytest.raises(Exception) as exc:
            self.module.fetch_smart_fabric_link_details(
                f_module, ome_connection_mock, params.get('json_data'))
        assert exc.value.args[0] == error_msg

    def test_ome_smart_fabric_info_main_success_case_all(self, ome_default_args, ome_connection_smart_fabric_info_mock,
                                                         ome_response_mock):
        ome_response_mock.status_code = 200
        result = self._run_module(ome_default_args)
        assert 'smart_fabric_info' in result
        assert result['msg'] == "Successfully retrieved the smart fabric information."

    def test_ome_smart_fabric_main_success_case_fabric_id(self, mocker, ome_default_args, ome_connection_smart_fabric_info_mock,
                                                          ome_response_mock):
        ome_default_args.update({"fabric_id": "1"})
        ome_response_mock.success = True
        ome_response_mock.json_data = {"value": [{"fabric_id": "1"}]}
        ome_response_mock.status_code = 200
        mocker.patch(
            MODULE_PATH + 'ome_smart_fabric_info.strip_smart_fabric_info',
            return_value=self.smart_fabric_details_dict)
        result = self._run_module(ome_default_args)
        assert 'smart_fabric_info' in result
        assert result['msg'] == "Successfully retrieved the smart fabric information."

    @pytest.mark.parametrize("params", [{"fabric_name": "f1",
                                        "json_data": {"value": [{"Description": "Fabric f1",
                                                                 "FabricDesignMapping": [
                                                                     {
                                                                         "DesignNode": "Switch-A",
                                                                         "PhysicalNode": "NODEID1"
                                                                     },
                                                                     {
                                                                         "DesignNode": "Switch-B",
                                                                         "PhysicalNode": "NODEID2"
                                                                     }],
                                                                 "Id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2",
                                                                 "LifeCycleStatus": [
                                                                     {
                                                                         "Activity": "Create",
                                                                         "Status": "2060"
                                                                     }
                                                                 ],
                                                                 "Name": "f1",
                                                                 "OverrideLLDPConfiguration": "Disabled",
                                                                 "ScaleVLANProfile": "Enabled",
                                                                 "Summary": {
                                                                     "NodeCount": 2,
                                                                     "ServerCount": 1,
                                                                     "UplinkCount": 1
                                                                 }}]
                                                      }}])
    def test_ome_smart_fabric_main_success_case_fabric_name(self, mocker, params, ome_default_args, ome_connection_smart_fabric_info_mock,
                                                            ome_response_mock):
        ome_default_args.update({"fabric_name": params["fabric_name"]})
        ome_response_mock.success = True
        ome_response_mock.status_code = 200
        ome_response_mock.json_data = params["json_data"]
        mocker.patch(
            MODULE_PATH + 'ome_smart_fabric_info.strip_smart_fabric_info',
            return_value=self.smart_fabric_details_dict)
        result = self._run_module(ome_default_args)
        assert 'smart_fabric_info' in result
        assert result['msg'] == "Successfully retrieved the smart fabric information."

    @pytest.mark.parametrize("params", [{"fabric_name": "f1",
                                        "json_data": {"value": [{"Description": "Fabric f1",
                                                                 "FabricDesignMapping": [
                                                                     {
                                                                         "DesignNode": "Switch-A",
                                                                         "PhysicalNode": "NODEID1"
                                                                     },
                                                                     {
                                                                         "DesignNode": "Switch-B",
                                                                         "PhysicalNode": "NODEID2"
                                                                     }],
                                                                 "Id": "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2",
                                                                 "LifeCycleStatus": [
                                                                     {
                                                                         "Activity": "Create",
                                                                         "Status": "2060"
                                                                     }
                                                                 ],
                                                                 "Name": "f2",
                                                                 "OverrideLLDPConfiguration": "Disabled",
                                                                 "ScaleVLANProfile": "Enabled",
                                                                 "Summary": {
                                                                     "NodeCount": 2,
                                                                     "ServerCount": 1,
                                                                     "UplinkCount": 1
                                                                 }}]
                                                      }}])
    def test_ome_smart_fabric_main_failure_case_fabric_name(self, params, ome_default_args, ome_connection_smart_fabric_info_mock,
                                                            ome_response_mock):
        ome_default_args.update({"fabric_name": params["fabric_name"]})
        ome_response_mock.success = True
        ome_response_mock.status_code = 200
        ome_response_mock.json_data = params["json_data"]
        result = self._run_module(ome_default_args)
        assert result['msg'] == 'Unable to retrieve smart fabric information with fabric name {0}.'.format(
            params["fabric_name"])

    def test_ome_smart_fabric_main_failure_case(self, ome_default_args, ome_connection_smart_fabric_info_mock,
                                                ome_response_mock):
        ome_response_mock.success = True
        ome_response_mock.status_code = 200
        ome_response_mock.json_data = {}
        result = self._run_module(ome_default_args)
        assert 'smart_fabric_info' not in result
        assert result['msg'] == "Unable to retrieve smart fabric information."

    @pytest.mark.parametrize("params", [{"fabric_id": "f1"}])
    def test_get_smart_fabric_details_via_id_HTTPError_error_case(self, params, ome_default_args, mocker, ome_connection_mock):
        json_str = to_text(json.dumps({"info": "error_details"}))
        error_msg = "Unable to retrieve smart fabric information with fabric ID {0}.".format(
            params.get('fabric_id'))
        ome_connection_mock.invoke_request.side_effect = HTTPError('https://testdell.com', 404,
                                                                   error_msg,
                                                                   {"accept-type": "application/json"},
                                                                   StringIO(json_str))
        f_module = self.get_module_mock()
        with pytest.raises(Exception) as exc:
            self.module.get_smart_fabric_details_via_id(
                f_module, ome_connection_mock, params.get('fabric_id'))
        assert exc.value.args[0] == error_msg

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_smart_fabric_info_main_exception_failure_case(self, exc_type, mocker, ome_default_args,
                                                               ome_connection_smart_fabric_info_mock,
                                                               ome_response_mock):
        ome_response_mock.status_code = 404
        ome_response_mock.success = False
        fabric_name_dict = {"fabric_name": "f1"}
        ome_default_args.update(fabric_name_dict)
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            ome_connection_smart_fabric_info_mock.invoke_request.side_effect = exc_type(
                'test')
        else:
            ome_connection_smart_fabric_info_mock.invoke_request.side_effect = exc_type('https://testhost.com', 400,
                                                                                        'http error message',
                                                                                        {"accept-type": "application/json"},
                                                                                        StringIO(json_str))
        if not exc_type == URLError:
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(ome_default_args)
        assert 'smart_fabric_info' not in result
        assert 'msg' in result
