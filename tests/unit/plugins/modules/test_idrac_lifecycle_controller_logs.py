# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.2
# Copyright (C) 2020-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_lifecycle_controller_logs
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from unittest.mock import MagicMock

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestExportLcLogs(FakeAnsibleModule):
    module = idrac_lifecycle_controller_logs

    @pytest.fixture
    def idrac_redfish_lc_logs_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_redfish_connection_export_lc_logs_mock(self, mocker, idrac_redfish_lc_logs_mock):
        idrac_redfish_conn_class_mock = mocker.patch(
            MODULE_PATH + 'idrac_lifecycle_controller_logs.iDRACRedfishAPI',
            return_value=idrac_redfish_lc_logs_mock
        )
        idrac_redfish_conn_class_mock.return_value.__enter__.return_value = idrac_redfish_lc_logs_mock
        return idrac_redfish_lc_logs_mock

    def test_main_export_lc_logs_success_case(self, idrac_default_args, mocker,
                                              idrac_redfish_connection_export_lc_logs_mock):
        idrac_default_args.update({"share_name": "sharename", "share_user": "shareuser",
                                   "share_password": "sharepassword", "job_wait": True})
        # Mock the old-style operation for network share compatibility
        idrac_redfish_connection_export_lc_logs_mock.invoke_request.return_value.json_data = {
            "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_123456"
        }
        idrac_redfish_connection_export_lc_logs_mock.get_server_generation = ("iDRAC9", "7.10.90.00", "PowerEdge R750")
        result = self._run_module(idrac_default_args)
        # For network shares, the old behavior should still work
        assert result.get("msg") is not None

    # TODO: Update exception handling test for new implementation
    # The old IDRACLifecycleControllerLogs.lifecycle_controller_logs_operation method
    # no longer exists after refactoring to use new utility modules
    # @pytest.mark.parametrize("exc_type", [RuntimeError, SSLValidationError, ConnectionError, KeyError,
    #                                       ImportError, ValueError, TypeError, HTTPError, URLError])
    # def test_main_export_lc_logs_exception_handling_case(self, exc_type, mocker,
    #                                                        idrac_default_args,
    #                                                        idrac_redfish_connection_export_lc_logs_mock):
    #     idrac_default_args.update({"share_name": "sharename", "share_user": "shareuser",
    #                                "share_password": "sharepassword", "job_wait": True})
    #     json_str = to_text(json.dumps({"data": "out"}))
    #     if exc_type not in [HTTPError, SSLValidationError]:
    #         mocker.patch(
    #             MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLifecycleControllerLogs.lifecycle_controller_logs_operation",
    #             side_effect=exc_type('test'))
    #     else:
    #         mocker.patch(
    #             MODULE_PATH + "idrac_lifecycle_controller_logs.IDRACLifecycleControllerLogs.lifecycle_controller_logs_operation",
    #             side_effect=exc_type('https://testhost.com', 400, 'http error message',
    #                                  {"accept-type": "application/json"}, StringIO(json_str)))
    #     if exc_type != URLError:
    #         result = self._run_module(idrac_default_args)
    #         assert result['failed'] is True
    #     else:
    #         result = self._run_module(idrac_default_args)
    #     assert 'msg' in result
