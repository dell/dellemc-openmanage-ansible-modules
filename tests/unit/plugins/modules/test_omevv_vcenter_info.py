# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.8.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import omevv_vcenter_info
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from io import StringIO
from mock import MagicMock
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
SUCCESS_MSG = "Successfully fetched the vCenter information."
NO_VCENTER_MSG = "Unable to complete the operation because the '{vcenter_hostname}' is not a valid 'vcenter_hostname'."
FAILED_MSG = "Unable to fetch the vCenter information."
INVOKE_REQ_KEY = "omevv_vcenter_info.RestOMEVV.invoke_request"


class TestOMEVVVCENTERINFO(FakeAnsibleModule):
    module = omevv_vcenter_info

    @pytest.fixture
    def omevv_vcenter_info_mock(self):
        omevv_obj = MagicMock()
        return omevv_obj

    @pytest.fixture
    def omevv_connection_vcenter_info(self, mocker, omevv_vcenter_info_mock):
        omevv_conn_mock = mocker.patch(MODULE_PATH + 'omevv_vcenter_info.RestOMEVV',
                                       return_value=omevv_vcenter_info_mock)
        omevv_conn_mock.return_value.__enter__.return_value = omevv_vcenter_info_mock
        return omevv_conn_mock

    def test_perform_operation(self, ome_default_args, omevv_connection_vcenter_info,
                               omevv_vcenter_info_mock, mocker):
        sample_resp = [
            {
                "uuid": "77373c7e-d2b0-453b-9567-102484519bd1",
                "consoleAddress": "hostname1",
                "description": "vCenter 8.0",
                "registeredExtensions": [
                    "PHM",
                    "WEBCLIENT",
                    "PHA",
                    "VLCM"
                ]
            },
            {
                "uuid": "77373c7e-d2b0-453b-9567-102484519bd2",
                "consoleAddress": "hostname2",
                "description": "vCenter 8.1",
                "registeredExtensions": [
                    "PHM",
                    "WEBCLIENT",
                    "PHA",
                    "VLCM"
                ]
            }
        ]
        # Scenario 1: Retrieve all vcenter information
        obj = MagicMock()
        obj.success = 'OK'
        obj.json_data = sample_resp
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, return_value=obj)
        resp = self._run_module(ome_default_args)
        assert resp['msg'] == SUCCESS_MSG
        assert resp['changed'] is False

        # Scenario 2: Retrieve not successfull vcenter information
        ome_default_args.update({'vcenter_hostname': 'hostname1'})
        mocker.patch(MODULE_PATH + "omevv_vcenter_info.RestOMEVV.get_all_vcenter_info", return_value={"msg": SUCCESS_MSG,
                                                                                                      "vcenter_info": sample_resp,
                                                                                                      "op": "success"})
        resp = self._run_module(ome_default_args)
        assert resp['msg'] == "Unable to complete the operation because the 'hostname1' is not a valid 'vcenter_hostname'."
        assert resp['skipped'] is True

        # Scenario 3: Retrieve single vcenter information
        ome_default_args.update({'vcenter_hostname': 'hostname1'})
        mocker.patch(MODULE_PATH + "omevv_vcenter_info.OMEVVVCenterInfo.get_all_vcenter_info", return_value={"msg": SUCCESS_MSG,
                                                                                                             "vcenter_info": sample_resp,
                                                                                                             "op": "success"})
        resp = self._run_module(ome_default_args)
        assert resp['msg'] == SUCCESS_MSG
        assert resp['changed'] is False

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_omevv_vcenter_info_main_exception_handling_case(self, exc_type, mocker, ome_default_args,
                                                             omevv_connection_vcenter_info, omevv_vcenter_info_mock):
        omevv_vcenter_info_mock.status_code = 400
        omevv_vcenter_info_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + "omevv_vcenter_info.OMEVVVCenterInfo.perform_module_operation",
                         side_effect=exc_type('https://testhost.com', 400,
                                              'http error message',
                                              {"accept-type": "application/json"},
                                              StringIO(json_str)))
        else:
            mocker.patch(MODULE_PATH + "omevv_vcenter_info.OMEVVVCenterInfo.perform_module_operation",
                         side_effect=exc_type('test'))
        result = self._run_module(ome_default_args)
        if exc_type == URLError:
            assert result['unreachable'] is True
        else:
            assert result['failed'] is True
        assert 'msg' in result
