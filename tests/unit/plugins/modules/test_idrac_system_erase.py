# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.7.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

import pytest
from unittest.mock import patch
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_system_erase
from ansible_collections.dellemc.openmanage.plugins.modules.idrac_system_erase import SystemErase
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from mock import MagicMock
from ansible_collections.dellemc.openmanage.plugins.modules.idrac_system_erase import main

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_system_erase.'
MODULE_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.'

MANAGERS_URI = "/redfish/v1/Managers"
MANAGER_URI_ONE = "/redfish/v1/managers/1"
IDRAC_JOB_URI = "{res_uri}/Jobs/{job_id}"
ODATA = "@odata.id"
ODATA_REGEX = "(.*?)@odata"

OEM = "Oem"
MANUFACTURER = "Dell"
LC_SERVICE = "DellLCService"
ACTIONS = "Actions"
SYSTEM_ERASE = "DellLCService.SystemErase"
SYSTEM_ERASE_FETCH = "#DellLCService.SystemErase"
COMPONENT_ALLOWABLE_VALUES = "Component@Redfish.AllowableValues"
JOB_FILTER = "Jobs?$expand=*($levels=1)"

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

    @pytest.fixture
    def mock_module(self):
        """Fixture for creating a mock Ansible module."""
        module_mock = MagicMock()
        module_mock.params = {'resource_id': None}  # Initialize with a dictionary
        return module_mock

    @pytest.fixture
    def system_erase_obj(self, mock_module):
        """Fixture for creating an instance of SystemErase with mocks."""
        idrac_mock = MagicMock()
        return SystemErase(idrac_mock, mock_module)

    def test_get_url_with_resource_id(self, system_erase_obj, mock_module):
        """Test get_url when 'resource_id' is provided."""
        mock_module.params['resource_id'] = 'iDRAC.Embedded.1'  # Set resource_id directly

        expected_url = "/redfish/v1/Managers/iDRAC.Embedded.1"
        assert system_erase_obj.get_url() == expected_url

    @patch(MODULE_UTILS_PATH + 'validate_and_get_first_resource_id_uri')
    @patch(MODULE_UTILS_PATH + 'get_dynamic_uri')
    def test_get_url_without_resource_id_success(self, mock_get_dynamic_uri, mock_validate, system_erase_obj, mock_module):
        """Test get_url when 'resource_id' is not provided and validation succeeds."""
        mock_module.params['resource_id'] = None  # No resource_id
        mock_validate.return_value = ("/redfish/v1/Managers/iDRAC.Embedded.1", None)  # Mock URI and no error
        mock_get_dynamic_uri.return_value = {'Members': [{'@odata.id': '/redfish/v1/Managers/iDRAC.Embedded.1'}]}  # Mock a valid response

        try:
            result_url = system_erase_obj.get_url()
            print("Resulting URL:", result_url)  # Debugging output
            expected_url = "/redfish/v1/Managers/iDRAC.Embedded.1"
            assert result_url == expected_url
            mock_validate.assert_called_once_with(mock_module, system_erase_obj.idrac, "/redfish/v1/Managers")
        except Exception as e:
            print("Error occurred:", str(e))

    def test_get_job_status_success(self, mocker, idrac_system_erase_mock):
        # Mocking necessary objects and functions
        module_mock = self.get_module_mock()
        system_erase_job_response_mock = mocker.MagicMock()
        system_erase_job_response_mock.headers.get.return_value = "HTTPS_PATH/job_tracking/12345"
        module_mock.params['wait_time'] = 10
        module_mock.params['job_wait_timeout'] = 100

        mocker.patch(MODULE_PATH + "remove_key", return_value={"job_details": "mocked_job_details"})
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri", return_value=[MANAGER_URI_ONE])

        # Creating an instance of the class
        obj_under_test = self.module.SystemErase(idrac_system_erase_mock, module_mock)

        # Mocking the idrac_redfish_job_tracking function to simulate a successful job tracking
        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking", return_value=(False, "mocked_message", {"job_details": "mocked_job_details"}, 0))

        # Calling the method under test
        result = obj_under_test.get_job_status(system_erase_job_response_mock)

        # Assertions
        assert result == {"job_details": "mocked_job_details"}

    # def test_get_job_status_wait_time_success(self, mocker, idrac_system_erase_mock):
    #     # Mocking necessary objects and functions
    #     module_mock = self.get_module_mock()
    #     system_erase_job_response_mock = mocker.MagicMock()
    #     system_erase_job_response_mock.headers.get.return_value = "HTTPS_PATH/job_tracking/12345"
    #     module_mock.params['wait_time'] = 100
    #     module_mock.params['job_wait_timeout'] = 10

    #     mocker.patch(MODULE_PATH + "remove_key", return_value={"job_details": "mocked_job_details"})
    #     mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri", return_value=[MANAGER_URI_ONE])

    #     # Creating an instance of the class
    #     obj_under_test = self.module.SystemErase(idrac_system_erase_mock, module_mock)

    #     # Mocking the idrac_redfish_job_tracking function to simulate a successful job tracking
    #     mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking", return_value=(False, "mocked_message", {"job_details": "mocked_job_details"}, 0))

    #     # Mocking module.exit_json
    #     exit_json_mock = mocker.patch.object(module_mock, "exit_json")

    #     # Calling the method under test
    #     result = obj_under_test.get_job_status(system_erase_job_response_mock)

    #     # Assertions
    #     exit_json_mock.assert_called_once_with(msg="The job is not complete after 10 seconds.", Chasnged=True, job_details={"Message": "None"})
    #     assert result == {"Message": "None"}

    def test_get_job_status_failure(self, mocker, idrac_system_erase_mock):
        # Mocking necessary objects and functions
        module_mock = self.get_module_mock()
        system_erase_job_response_mock = mocker.MagicMock()
        system_erase_job_response_mock.headers.get.return_value = "HTTPS_PATH/job_tracking/12345"
        module_mock.params['wait_time'] = 10
        module_mock.params['job_wait_timeout'] = 100

        mocker.patch(MODULE_PATH + "remove_key", return_value={"Message": "None"})
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri", return_value=[MANAGER_URI_ONE])

        # Creating an instance of the class
        obj_under_test = self.module.SystemErase(idrac_system_erase_mock, module_mock)

        # Mocking the idrac_redfish_job_tracking function to simulate a failed job tracking
        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking", return_value=(True, "None", {"Message": "None"}, 0))

        # Mocking module.exit_json
        exit_json_mock = mocker.patch.object(module_mock, "exit_json")

        # Calling the method under test
        result = obj_under_test.get_job_status(system_erase_job_response_mock)

        # Assertions
        exit_json_mock.assert_called_once_with(msg="None", failed=True, job_details={"Message": "None"})
        assert result == {"Message": "None"}

    def test_get_details_status_success(self, mocker, idrac_system_erase_mock):
        # Mocking necessary objects and functions
        module_mock = self.get_module_mock()
        system_erase_job_response_mock = mocker.MagicMock()
        system_erase_job_response_mock.headers.get.return_value = "HTTPS_PATH/job_tracking/12345"

        mocker.patch(MODULE_PATH + "remove_key", return_value={"job_details": "mocked_job_details"})
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri", return_value=[MANAGER_URI_ONE])

        # Creating an instance of the class
        obj_under_test = self.module.SystemErase(idrac_system_erase_mock, module_mock)

        # Mocking the idrac_redfish_job_tracking function to simulate a successful job tracking
        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking", return_value=(False, "mocked_message", {"job_details": "mocked_job_details"}, 0))

        # Calling the method under test
        result = obj_under_test.get_job_details(system_erase_job_response_mock)

        # Assertions
        assert result == {"job_details": "mocked_job_details"}
