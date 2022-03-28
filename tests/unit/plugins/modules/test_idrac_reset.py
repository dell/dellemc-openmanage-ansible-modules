# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.2.0
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_reset
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from mock import MagicMock, patch, Mock
from io import StringIO
from ansible.module_utils._text import to_text

from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


@pytest.fixture
def idrac_reset_connection_mock(mocker, idrac_mock):
    idrac_connection_class_mock = mocker.patch(MODULE_PATH + 'idrac_reset.iDRACConnection')
    idrac_connection_class_mock.return_value.__enter__.return_value = idrac_mock
    return idrac_mock


class TestReset(FakeAnsibleModule):
    module = idrac_reset

    @pytest.fixture
    def idrac_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.config_mgr = idrac_obj
        type(idrac_obj).reset_idrac = Mock(return_value="idracreset")
        return idrac_obj

    @pytest.fixture
    def idrac_config_mngr_reset_mock(self, mocker):
        try:
            config_manager_obj = mocker.patch(MODULE_PATH + 'idrac_reset.config_mgr')
        except AttributeError:
            config_manager_obj = MagicMock()
        obj = MagicMock()
        config_manager_obj.config_mgr.return_value = obj
        config_manager_obj.config_mgr.reset_idrac().return_value = obj
        return config_manager_obj

    def test_main_idrac_reset_success_case01(self, idrac_reset_connection_mock, idrac_default_args, mocker):
        mocker.patch(MODULE_PATH + "idrac_reset.run_idrac_reset",
                     return_value=({"Status": "Success"}, False))
        idrac_reset_connection_mock.config_mgr.reset_idrac.return_value = {"Status": "Success"}
        idrac_reset_connection_mock.config_mgr.reset_idrac.return_value = "Success"
        result = self._run_module(idrac_default_args)
        assert result == {'msg': 'Successfully performed iDRAC reset.',
                          'reset_status': ({'Status': 'Success'}, False), 'changed': False}

    def test_run_idrac_reset_success_case01(self, idrac_reset_connection_mock, idrac_default_args):
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.run_idrac_reset(idrac_reset_connection_mock, f_module)
        assert result == idrac_reset_connection_mock.config_mgr.reset_idrac()

    def test_run_idrac_reset_status_success_case02(self, idrac_reset_connection_mock, idrac_default_args):
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        result = self.module.run_idrac_reset(idrac_reset_connection_mock, f_module)
        assert result == {'Message': 'Changes found to commit!', 'Status': 'Success', 'changes_applicable': True}

    @pytest.mark.parametrize("exc_type", [SSLValidationError, URLError, ValueError, TypeError,
                                          ConnectionError, HTTPError])
    def test_main_exception_handling_case(self, exc_type, mocker, idrac_reset_connection_mock, idrac_default_args):
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'idrac_reset.run_idrac_reset', side_effect=exc_type('test'))
        else:
            mocker.patch(MODULE_PATH + 'idrac_reset.run_idrac_reset',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
        if not exc_type == URLError:
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result
