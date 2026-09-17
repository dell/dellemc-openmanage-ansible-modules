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
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_lifecycle_controller_status_info
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from unittest.mock import MagicMock
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestLcStatus(FakeAnsibleModule):
    module = idrac_lifecycle_controller_status_info

    @pytest.fixture
    def idrac_redfish_lcstatus_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_redfish_lcstatus_connection_mock(self, mocker, idrac_redfish_lcstatus_mock):
        idrac_redfish_conn_class_mock = mocker.patch(
            MODULE_PATH + 'idrac_lifecycle_controller_status_info.iDRACRedfishAPI',
            return_value=idrac_redfish_lcstatus_mock)
        idrac_redfish_conn_class_mock.return_value.__enter__.return_value = idrac_redfish_lcstatus_mock
        return idrac_redfish_lcstatus_mock

    def test_main_get_lcstatus_success_case00(self,
                                              idrac_redfish_lcstatus_connection_mock,
                                              idrac_default_args,
                                              mocker):
        lcstatus = "Ready"
        mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_status_info.IDRACLifecycleControllerStatusInfo.get_lifecycle_controller_status_info",
                     return_value=lcstatus)
        result = self._run_module(idrac_default_args)
        assert result['lc_status_info']['LCReady'] is True
        assert result['lc_status_info']['LCStatus'] == lcstatus

    @pytest.mark.parametrize("exc_type", [RuntimeError, SSLValidationError, ConnectionError, KeyError,
                                          ImportError, ValueError, TypeError, HTTPError, URLError])
    def test_main_get_lcstatus_exception_handling_case(self, exc_type,
                                                       idrac_redfish_lcstatus_connection_mock,
                                                       idrac_default_args, mocker):
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_status_info.IDRACLifecycleControllerStatusInfo.get_lifecycle_controller_status_info",
                         side_effect=exc_type("url open error"))
            result = self._run_module(idrac_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_status_info.IDRACLifecycleControllerStatusInfo.get_lifecycle_controller_status_info",
                         side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
            assert 'msg' in result
        else:
            mocker.patch(MODULE_PATH + "idrac_lifecycle_controller_status_info.IDRACLifecycleControllerStatusInfo.get_lifecycle_controller_status_info",
                         side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"},
                                              StringIO(json_str)))
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
            assert 'msg' in result
