# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.0.0
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from copy import deepcopy
from ansible_collections.dellemc.openmanage.plugins.modules import ome_network_vlan_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
ACCESS_TYPE = "application/json"
HTTP_ADDRESS = 'https://testhost.com'

response = {
    '@odata.context': '/api/$metadata#Collection(NetworkConfigurationService.Network)',
    '@odata.count': 1,
    'value': [
        {
            '@odata.type': '#NetworkConfigurationService.Network',
            '@odata.id': '/api/NetworkConfigurationService/Networks(20057)',
            'Id': 20057,
            'Name': 'Logical Network - 1',
            'Description': 'Description of Logical Network - 1',
            'VlanMaximum': 111,
            'VlanMinimum': 111,
            "Type": 1,
            'CreatedBy': 'admin',
            'CreationTime': '2020-09-02 18:48:42.129',
            'UpdatedBy': None,
            'UpdatedTime': '2020-09-02 18:48:42.129',
            'InternalRefNWUUId': '42b9903d-93f8-4184-adcf-0772e4492f71'
        }
    ]
}

network_type_qos_type_dict_reponse = {1: {'Id': 1, 'Name': 'General Purpose (Bronze)',
                                          'Description':
                                              'This is the network for general purpose traffic. QOS Priority : Bronze.',
                                          'VendorCode': 'GeneralPurpose', 'NetworkTrafficType': 'Ethernet',
                                          'QosType': {'Id': 4, 'Name': 'Bronze'}}}

network_type_dict_response = {1: {'Id': 1, 'Name': 'General Purpose (Bronze)',
                                  'Description':
                                      'This is the network for general purpose traffic. QOS Priority : Bronze.',
                                  'VendorCode': 'GeneralPurpose', 'NetworkTrafficType': 'Ethernet',
                                  'QosType': 4}}

qos_type_dict_response = {4: {'Id': 4, 'Name': 'Bronze'}}

type_dict_ome_reponse = {'@odata.context': '/api/$metadata#Collection(NetworkConfigurationService.Network)',
                         '@odata.count': 1,
                         'value': [
                             {'@odata.type': '#NetworkConfigurationService.NetworkType',
                              '@odata.id': '/api/NetworkConfigurationService/NetworkTypes(1)',
                              'Id': 1,
                              'Name': 'General Purpose (Bronze)',
                              'Description': 'This is the network for general purpose traffic. QOS Priority : Bronze.',
                              'VendorCode': 'GeneralPurpose', 'NetworkTrafficType': 'Ethernet',
                              'QosType': 4}]}


class TestOmeNetworkVlanInfo(FakeAnsibleModule):
    """Pytest class for ome_network_vlan_info module."""
    module = ome_network_vlan_info

    @pytest.fixture
    def ome_connection_network_vlan_info_mock(self, mocker, ome_response_mock):
        connection_class_mock = mocker.patch(
            'ansible_collections.dellemc.openmanage.plugins.modules.ome_network_vlan_info.RestOME')
        ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
        ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
        return ome_connection_mock_obj

    def test_get_network_vlan_info_success_case(self, mocker, ome_default_args, ome_connection_network_vlan_info_mock,
                                                ome_response_mock):
        ome_response_mock.json_data = deepcopy(response)
        ome_response_mock.status_code = 200
        mocker.patch(
            MODULE_PATH + 'ome_network_vlan_info.get_network_type_and_qos_type_information',
            return_value=network_type_qos_type_dict_reponse)
        result = self._run_module(ome_default_args)
        print(result)
        assert 'network_vlan_info' in result
        assert result['msg'] == "Successfully retrieved the network VLAN information."

    def test_get_network_vlan_info_by_id_success_case(self, mocker, ome_default_args,
                                                      ome_connection_network_vlan_info_mock, ome_response_mock):
        ome_default_args.update({"id": 20057})
        ome_response_mock.success = True
        ome_response_mock.json_data = deepcopy(response)
        ome_response_mock.status_code = 200
        mocker.patch(
            MODULE_PATH + 'ome_network_vlan_info.get_network_type_and_qos_type_information',
            return_value=network_type_qos_type_dict_reponse)
        result = self._run_module(ome_default_args)
        assert result['changed'] is False
        assert 'network_vlan_info' in result
        assert result['msg'] == "Successfully retrieved the network VLAN information."

    def test_get_network_vlan_info_by_name_success_case(self, mocker, ome_default_args,
                                                        ome_connection_network_vlan_info_mock, ome_response_mock):
        ome_default_args.update({"name": "Logical Network - 1"})
        ome_response_mock.success = True
        ome_response_mock.json_data = deepcopy(response)
        ome_response_mock.status_code = 200
        mocker.patch(
            MODULE_PATH + 'ome_network_vlan_info.get_network_type_and_qos_type_information',
            return_value=network_type_qos_type_dict_reponse)
        result = self._run_module(ome_default_args)
        assert result['changed'] is False
        assert 'network_vlan_info' in result
        assert result['msg'] == "Successfully retrieved the network VLAN information."

    def test_get_network_type_and_qos_type_information(self, mocker, ome_connection_network_vlan_info_mock):
        mocker.patch(MODULE_PATH + 'ome_network_vlan_info.get_type_information',
                     side_effect=[network_type_dict_response, qos_type_dict_response])
        result = self.module.get_network_type_and_qos_type_information(ome_connection_network_vlan_info_mock)
        assert result[1]['QosType']['Id'] == 4

    def test_get_type_information(self, mocker, ome_default_args,
                                  ome_connection_network_vlan_info_mock, ome_response_mock):
        ome_response_mock.success = True
        ome_response_mock.json_data = type_dict_ome_reponse
        ome_response_mock.status_code = 200
        result = self.module.get_type_information(ome_connection_network_vlan_info_mock, '')
        assert result[1]['QosType'] == 4

    def test_network_vlan_info_failure_case(self, ome_default_args, ome_connection_network_vlan_info_mock,
                                            ome_response_mock):
        ome_response_mock.status_code = 500
        result = self._run_module_with_fail_json(ome_default_args)
        assert result['msg'] == "Failed to retrieve the network VLAN information."

    def test_network_vlan_info_name_failure_case(self, ome_default_args, ome_connection_network_vlan_info_mock,
                                                 ome_response_mock):
        ome_default_args.update({"name": "non-existing vlan"})
        ome_response_mock.success = True
        ome_response_mock.json_data = response
        ome_response_mock.status_code = 200
        result = self._run_module_with_fail_json(ome_default_args)
        assert result['failed'] is True
        assert 'network_vlan_info' not in result
        assert result['msg'] == "Provided network VLAN with name - 'non-existing vlan' does not exist."

    @pytest.mark.parametrize("exc_type", [URLError, HTTPError, SSLValidationError, ConnectionError,
                                          TypeError, ValueError])
    def test_network_vlan_info_info_main_exception_case(self, exc_type, mocker, ome_default_args,
                                                        ome_connection_network_vlan_info_mock, ome_response_mock):
        ome_response_mock.status_code = 404
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type == URLError:
            ome_connection_network_vlan_info_mock.invoke_request.side_effect = exc_type(
                "ansible.module_utils.urls.open_url error")
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type == HTTPError:
            ome_connection_network_vlan_info_mock.invoke_request.side_effect = exc_type(
                HTTP_ADDRESS, 400, '<400 bad request>', {"accept-type": ACCESS_TYPE},
                StringIO(json_str))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
            assert 'msg' in result
            assert 'error_info' in result

            ome_connection_network_vlan_info_mock.invoke_request.side_effect = exc_type(
                HTTP_ADDRESS, 404, '<404 not found>', {"accept-type": ACCESS_TYPE}, StringIO(json_str))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
            assert 'msg' in result
        elif exc_type != SSLValidationError:
            mocker.patch(MODULE_PATH + 'ome_network_vlan_info.get_network_type_and_qos_type_information',
                         side_effect=exc_type('test'))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
            assert 'msg' in result
        else:
            mocker.patch(MODULE_PATH + 'ome_network_vlan_info.get_network_type_and_qos_type_information',
                         side_effect=exc_type(HTTP_ADDRESS, 404, 'http error message',
                                              {"accept-type": ACCESS_TYPE}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
            assert 'msg' in result
