# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.3
# Copyright (C) 2020-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.modules import ome_firmware_baseline_info
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from io import StringIO
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestOmeFirmwareBaselineInfo(FakeAnsibleModule):
    module = ome_firmware_baseline_info

    @pytest.fixture
    def ome_connection_ome_firmware_baseline_info_mock(self, mocker, ome_response_mock):
        connection_class_mock = mocker.patch(
            MODULE_PATH + 'ome_firmware_baseline_info.RestOME')
        ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
        ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
        return ome_connection_mock_obj

    def test_ome_firmware_baseline_info_main_success_case_01(self, mocker, ome_response_mock, ome_default_args,
                                                             module_mock,
                                                             ome_connection_ome_firmware_baseline_info_mock):
        ome_response_mock.json_data = {"value": [{"baseline1": "data"}]}
        result = self._run_module(ome_default_args)
        assert result["changed"] is False
        assert 'baseline_info' in result
        assert result['msg'] == "Successfully fetched firmware baseline information."
        assert result['baseline_info'] == {"value": [{"baseline1": "data"}]}

    def test_ome_firmware_baseline_info_main_success_case_02(self, mocker, ome_response_mock, ome_default_args,
                                                             module_mock,
                                                             ome_connection_ome_firmware_baseline_info_mock):
        ome_response_mock.json_data = {"value": []}
        result = self._run_module(ome_default_args)
        assert 'baseline_info' in result
        assert result['baseline_info'] == []

    def test_ome_firmware_baseline_info_main_success_case_03(self, mocker, ome_response_mock, ome_default_args,
                                                             module_mock,
                                                             ome_connection_ome_firmware_baseline_info_mock):
        ome_default_args.update({"baseline_name": "baseline1"})
        ome_response_mock.json_data = {"value": [{"Name": "baseline1", "data": "fake_data"}]}
        mocker.patch(
            MODULE_PATH + 'ome_firmware_baseline_info.get_specific_baseline',
            return_value={"Name": "baseline1", "data": "fake_data"})
        result = self._run_module(ome_default_args)
        assert result["changed"] is False
        assert 'baseline_info' in result
        assert result["baseline_info"] == {"Name": "baseline1", "data": "fake_data"}
        assert result['msg'] == "Successfully fetched firmware baseline information."

    def test_ome_firmware_baseline_info_main_success_case_04(self, mocker, ome_response_mock, ome_default_args,
                                                             module_mock,
                                                             ome_connection_ome_firmware_baseline_info_mock):
        ome_default_args.update({"baseline_name": None})
        ome_response_mock.json_data = {"value": []}
        mocker.patch(
            MODULE_PATH + 'ome_firmware_baseline_info.get_specific_baseline',
            return_value={"baseline1": "fake_data"})
        result = self._run_module(ome_default_args)
        assert result['baseline_info'] == []
        assert result['msg'] == "No baselines present."

    def test_ome_firmware_get_specific_baseline_case_01(self):
        f_module = self.get_module_mock()
        data = {"value": [{"Name": "baseline1", "data": "fakedata1"}, {"Name": "baseline2", "data": "fakedata2"}]}
        val = self.module.get_specific_baseline(f_module, "baseline1", data)
        assert val == {"Name": "baseline1", "data": "fakedata1"}

    def test_ome_firmware_get_specific_baseline_case_02(self):
        f_module = self.get_module_mock()
        baseline_name = "baseline3"
        msg = "Unable to complete the operation because the requested baseline with" \
              " name '{0}' does not exist.".format(baseline_name)
        data = {"value": [{"Name": "baseline1", "data": "fakedata1"}, {"Name": "baseline2", "data": "fakedata2"}]}
        with pytest.raises(Exception) as exc:
            self.module.get_specific_baseline(f_module, baseline_name, data)
        assert exc.value.args[0] == msg

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_main_ome_firmware_baseline_info_failure_case1(self, exc_type, mocker, ome_default_args,
                                                           ome_connection_ome_firmware_baseline_info_mock,
                                                           ome_response_mock):
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            ome_connection_ome_firmware_baseline_info_mock.invoke_request.side_effect = exc_type("TESTS")
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            ome_connection_ome_firmware_baseline_info_mock.invoke_request.side_effect = exc_type("exception message")
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
        else:
            ome_connection_ome_firmware_baseline_info_mock.invoke_request.side_effect = exc_type('https://testhost.com',
                                                                                                 400,
                                                                                                 'http error message',
                                                                                                 {
                                                                                                     "accept-type": "application/json"},
                                                                                                 StringIO(json_str))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
            assert "error_info" in result
            assert result['msg'] == 'HTTP Error 400: http error message'

            ome_connection_ome_firmware_baseline_info_mock.invoke_request.side_effect = exc_type('https://testhost.com',
                                                                                                 404,
                                                                                                 '<404 not found>',
                                                                                                 {
                                                                                                     "accept-type": "application/json"},
                                                                                                 StringIO(json_str))
            result = self._run_module(ome_default_args)
            assert result['failed'] is True
            assert "error_info" not in result
            assert result["msg"] == "404 Not Found.The requested resource is not available."
        assert 'baseline_info' not in result
        assert 'msg' in result
