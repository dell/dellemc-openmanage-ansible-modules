# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.0.0
# Copyright (C) 2021-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_system_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from unittest.mock import MagicMock, Mock
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from io import StringIO
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestSystemInventory(FakeAnsibleModule):
    module = idrac_system_info

    @pytest.fixture
    def idrac_redfish_system_info_mock(self):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.get_entityjson = idrac_obj
        type(idrac_obj).get_json_device = Mock(return_value="msg")
        return idrac_obj

    @pytest.fixture
    def idrac_redfish_system_info_connection_mock(self, mocker, idrac_redfish_system_info_mock):
        idrac_redfish_conn_class_mock = mocker.patch(MODULE_PATH +
                                                     'idrac_system_info.iDRACRedfishAPI',
                                                     return_value=idrac_redfish_system_info_mock)
        idrac_redfish_conn_class_mock.return_value.__enter__.return_value = idrac_redfish_system_info_mock
        return idrac_redfish_system_info_mock

    def test_idrac_system_info_main_success_case02(self,
                                                   idrac_redfish_system_info_mock,
                                                   idrac_redfish_system_info_connection_mock,
                                                   idrac_default_args,
                                                   mocker):
        mocker.patch(MODULE_PATH + "idrac_system_info.IDRACBiosInfo.get_bios_system_info",
                     return_value={'BiosReleaseDate': '02/01/2012'})
        mocker.patch(MODULE_PATH + "idrac_system_info.IDRACCpuInfo.get_cpu_system_info",
                     return_value={'Name': 'CPU-0'})
        mocker.patch(MODULE_PATH + "idrac_system_info.IDRACEnclosureInfo.get_enclosure_system_info",
                     return_value={'ID': 'abcd'})
        mocker.patch(MODULE_PATH + "idrac_system_info.IDRACEnclosureInfo.get_controller_enclosure_sensor_info",
                     return_value={'Key': '12345'})
        idrac_redfish_system_info_mock.get_entityjson.return_value = None
        idrac_redfish_system_info_connection_mock.get_json_device.return_value = ""
        result = self._run_module(idrac_default_args)
        assert result["system_info"]['BIOS'] == {'BiosReleaseDate': '02/01/2012'}
        assert result["system_info"]['CPU'] == {'Name': 'CPU-0'}
        assert result["system_info"]['Enclosure'] == {'ID': 'abcd'}
        assert result["system_info"]['EnclosureSensor'] == {'Key': '12345'}

    @pytest.mark.parametrize("exc_type", [SSLValidationError, URLError, ValueError, TypeError,
                                          ConnectionError, HTTPError])
    def test_idrac_system_info_main_exception_handling_case(self, exc_type,
                                                            idrac_redfish_system_info_connection_mock,
                                                            idrac_default_args,
                                                            mocker):
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            idrac_redfish_system_info_connection_mock.invoke_request.side_effect = exc_type('test')
        elif exc_type in [URLError]:
            idrac_redfish_system_info_connection_mock.invoke_request.side_effect = exc_type('test')
        else:
            idrac_redfish_system_info_connection_mock.invoke_request.side_effect = exc_type('https://testhost.com', 400,
                                                                                            'http error message',
                                                                                            {
                                                                                                "accept-type": "application/json"},
                                                                                            StringIO(json_str))
        if exc_type != URLError:
            result = self._run_module(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result
