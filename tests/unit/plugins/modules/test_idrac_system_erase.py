# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.7.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

import pytest
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_system_erase
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from mock import MagicMock
from ansible_collections.dellemc.openmanage.plugins.modules.idrac_system_erase import main

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_system_erase.'
MODULE_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.'

ERASE_SUCCESS_COMPLETION_MSG = "Successfully completed the system erase operation."
ERASE_SUCCESS_SCHEDULED_MSG = "Successfully submitted the job for system erase operation."
ERASE_SUCCESS_POWER_ON_MSG = "Successfully completed the system erase operation and powered on " \
                             "the server."
NO_COMPONENT_MATCH = "Unable to complete the operation because the value entered for the " \
                     "'component' is not in the list of acceptable values."
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The value for the 'job_wait_timeout' parameter cannot be " \
                               "negative or zero."
WAIT_TIMEOUT_MSG = "The job is not complete after {0} seconds."
INVALID_COMPONENT_WARN_MSG = "Erase operation is not performed on these components - " \
                             "{unmatching_components_str_format} as they are either invalid or " \
                             "inapplicable."
FAILURE_MSG = "Unable to complete the system erase operation."
CHANGES_FOUND_MSG = "Changes found to be applied."
NO_CHANGES_FOUND_MSG = "No changes found to be applied."


class TestSystemErase(FakeAnsibleModule):
    module = idrac_system_erase

    @pytest.fixture
    def idrac_system_erase_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_system_erase_mock(self, mocker, idrac_system_erase_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_system_erase_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_system_erase_mock
        return idrac_conn_mock

    def test_main(self, mocker):
        module_mock = mocker.MagicMock()
        idrac_mock = mocker.MagicMock()
        license_mock = mocker.MagicMock()

        # Mock the necessary functions and objects
        mocker.patch(MODULE_PATH + 'get_argument_spec', return_value={})
        mocker.patch(MODULE_PATH + 'IdracAnsibleModule', return_value=module_mock)
        mocker.patch(MODULE_PATH + 'iDRACRedfishAPI', return_value=idrac_mock)
        mocker.patch(MODULE_PATH + 'EraseComponent', return_value=license_mock)
        main()
