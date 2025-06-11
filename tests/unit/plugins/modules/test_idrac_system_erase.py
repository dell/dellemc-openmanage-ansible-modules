# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.7.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

import pytest
from unittest.mock import patch, MagicMock
from urllib.error import HTTPError, URLError
from ansible.module_utils._text import to_text
from io import StringIO
import json
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_system_erase
from ansible_collections.dellemc.openmanage.plugins.modules.idrac_system_erase import SystemErase, main
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_system_erase.'
MODULE_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.'
HTTPS_PATH = 'HTTPS_PATH/job_tracking/12345'

MANAGERS_URI = "/redfish/v1/Managers"
MANAGER_URI_ONE = "/redfish/v1/managers/1"
REDFISH_MOCK_URL = "/redfish/v1/Managers/1234"
MANAGER_URI_RESOURCE = "/redfish/v1/Managers/iDRAC.Embedded.1"
IDRAC_JOB_URI = "{res_uri}/Jobs/{job_id}"
ODATA = "@odata.id"
ODATA_REGEX = "(.*?)@odata"
OEM = "Oem"
MANUFACTURER = "Dell"
LC_SERVICE = "DellLCService"
ACTIONS = "Actions"
SYSTEM_ERASE = "DellLCService.SystemErase"
SYSTEM_ERASE_FETCH = "#DellLCService.SystemErase"
SYSTEM_ERASE_URL = "SystemErase.get_system_erase_url"
SYSTEM_ERASE_JOB_STATUS = "SystemErase.get_job_status"
COMPONENT_ALLOWABLE_VALUES = "Component@Redfish.AllowableValues"
JOB_FILTER = "Jobs?$expand=*($levels=1)"
API_ONE = "/local/action"
API_INVOKE_MOCKER = "iDRACRedfishAPI.invoke_request"
ALLOWABLE_VALUE_FUNC = "SystemErase.check_allowable_value"
REDFISH_API = "iDRACRedfishAPI"
HTTPS_PATH = "https://testhost.com"
HTTP_ERROR = "http error message"
APPLICATION_JSON = "application/json"
MESSAGE_EXTENDED = "@Message.ExtendedInfo"

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
        idrac_conn_mock = mocker.patch(MODULE_PATH + REDFISH_API,
                                       return_value=idrac_system_erase_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_system_erase_mock
        return idrac_conn_mock

    @pytest.fixture
    def mock_module(self):
        """Fixture for creating a mock Ansible module."""
        module_mock = MagicMock()
        # Initialize with a dictionary
        module_mock.params = {'resource_id': None}
        return module_mock

    @pytest.fixture
    def system_erase_obj(self, mock_module):
        """Fixture for creating an instance of SystemErase with mocks."""
        idrac_mock = MagicMock()
        return SystemErase(idrac_mock, mock_module)

    def test_get_url_with_resource_id(self, system_erase_obj, mock_module):
        """Test get_url when 'resource_id' is provided."""
        mock_module.params['resource_id'] = 'iDRAC.Embedded.1'  # Set resource_id directly

        expected_url = MANAGER_URI_RESOURCE
        assert system_erase_obj.get_url() == expected_url

    @patch(MODULE_UTILS_PATH + 'validate_and_get_first_resource_id_uri')
    @patch(MODULE_UTILS_PATH + 'get_dynamic_uri')
    def test_get_url_without_resource_id_success(self, mock_get_dynamic_uri, mock_validate, system_erase_obj, mock_module):
        """Test get_url when 'resource_id' is not provided and validation succeeds."""
        mock_module.params['resource_id'] = None  # No resource_id
        mock_validate.return_value = (
            MANAGER_URI_RESOURCE, None)  # Mock URI and no error
        mock_get_dynamic_uri.return_value = {'Members': [
            {'@odata.id': 'MANAGER_URI_RESOURCE'}]}  # Mock a valid response
        try:
            result_url = system_erase_obj.get_url()
            expected_url = MANAGER_URI_RESOURCE
            assert result_url == expected_url
            mock_validate.assert_called_once_with(
                mock_module, system_erase_obj.idrac, "/redfish/v1/Managers")
        except Exception as e:
            print("Error occurred:", str(e))

    def test_get_job_status_success(self, mocker, idrac_system_erase_mock):
        # Mocking necessary objects and functions
        module_mock = self.get_module_mock()
        system_erase_job_response_mock = mocker.MagicMock()
        system_erase_job_response_mock.headers.get.return_value = HTTPS_PATH
        module_mock.params['wait_time'] = 10
        module_mock.params['job_wait_timeout'] = 100

        mocker.patch(MODULE_PATH + "remove_key",
                     return_value={"job_details": "mocked_job_details"})
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=[MANAGER_URI_ONE])

        # Creating an instance of the class
        obj_under_test = self.module.SystemErase(
            idrac_system_erase_mock, module_mock)

        # Mocking the idrac_redfish_job_tracking function to simulate a successful job tracking
        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking", return_value=(
            False, "mocked_message", {"job_details": "mocked_job_details"}, 0))

        # Calling the method under test
        result = obj_under_test.get_job_status(system_erase_job_response_mock)

        # Assertions
        assert result == {"job_details": "mocked_job_details"}

    def test_get_job_status_failure(self, mocker, idrac_system_erase_mock):
        # Mocking necessary objects and functions
        module_mock = self.get_module_mock()
        system_erase_job_response_mock = mocker.MagicMock()
        system_erase_job_response_mock.headers.get.return_value = HTTPS_PATH
        module_mock.params['wait_time'] = 10
        module_mock.params['job_wait_timeout'] = 100

        mocker.patch(MODULE_PATH + "remove_key",
                     return_value={"Message": "None"})
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=[MANAGER_URI_ONE])

        # Creating an instance of the class
        obj_under_test = self.module.SystemErase(
            idrac_system_erase_mock, module_mock)

        # Mocking the idrac_redfish_job_tracking function to simulate a failed job tracking
        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking",
                     return_value=(True, "None", {"Message": "None"}, 0))

        # Mocking module.exit_json
        exit_json_mock = mocker.patch.object(module_mock, "exit_json")

        # Calling the method under test
        result = obj_under_test.get_job_status(system_erase_job_response_mock)

        # Assertions
        exit_json_mock.assert_called_once_with(
            msg="None", failed=True, job_details={"Message": "None"})
        assert result == {"Message": "None"}

    def test_get_details_status_success(self, mocker, idrac_system_erase_mock):
        # Mocking necessary objects and functions
        module_mock = self.get_module_mock()
        system_erase_job_response_mock = mocker.MagicMock()
        system_erase_job_response_mock.headers.get.return_value = HTTPS_PATH

        mocker.patch(MODULE_PATH + "remove_key",
                     return_value={"job_details": "mocked_job_details"})
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=[MANAGER_URI_ONE])

        # Creating an instance of the class
        obj_under_test = self.module.SystemErase(
            idrac_system_erase_mock, module_mock)

        # Mocking the idrac_redfish_job_tracking function to simulate a successful job tracking
        mocker.patch(MODULE_PATH + "idrac_redfish_job_tracking", return_value=(
            False, "mocked_message", {"job_details": "mocked_job_details"}, 0))

        # Calling the method under test
        result = obj_under_test.get_job_details(system_erase_job_response_mock)

        # Assertions
        assert result == {"job_details": "mocked_job_details"}

    @patch(MODULE_UTILS_PATH + 'get_dynamic_uri')
    def test_get_system_erase_url(self, mock_get_dynamic_uri, system_erase_obj, mock_module):
        """Test get_system_erase_url retrieves the correct URL for the system erase operation."""
        mock_module.params['resource_id'] = "iDRAC.Embedded.1"

        # Mock the response of get_dynamic_uri
        mock_get_dynamic_uri.return_value = {
            'Links': {
                'Oem': {
                    'Dell': {
                        'DellLCService': {
                            '@odata.id': 'MANAGER_URI_RESOURCE/Oem/DellLCService'
                        }
                    }
                }
            }
        }

        expected_system_erase_url = 'MANAGER_URI_RESOURCE/Oem/DellLCService'

        try:
            # Call the method under test
            result_url = system_erase_obj.get_system_erase_url()

            # Assert the expected outcome
            assert result_url == expected_system_erase_url

        except Exception as e:
            print("Error occurred:", str(e))

    @patch(MODULE_PATH + 'SystemErase.get_url')
    def test_check_system_erase_job_success(self, mock_get_url, mock_module):
        """Test check_system_erase_job when a SystemErase job is found with a valid state."""
        mock_url = REDFISH_MOCK_URL
        mock_get_url.return_value = mock_url

        # Create a mock idrac object
        mock_idrac = MagicMock()
        mock_idrac.invoke_request.return_value = MagicMock(
            json_data={
                'Members': [
                    {'JobType': 'SystemErase', 'JobState': 'New'},
                    {'JobType': 'SystemErase', 'JobState': 'Completed'}
                ]
            }
        )

        # Initialize SystemErase object with mock idrac
        system_erase_obj = SystemErase(module=mock_module, idrac=mock_idrac)

        result = system_erase_obj.check_system_erase_job()
        assert result == 'Completed'

    @patch(MODULE_PATH + 'SystemErase.get_url')
    def test_check_system_erase_job_failed(self, mock_get_url, mock_module):
        """Test check_system_erase_job when a SystemErase job is found with 'Failed' state."""
        mock_url = REDFISH_MOCK_URL
        mock_get_url.return_value = mock_url

        # Create a mock idrac object
        mock_idrac = MagicMock()
        mock_idrac.invoke_request.return_value = MagicMock(
            json_data={
                'Members': [
                    {'JobType': 'SystemErase', 'JobState': 'New'},
                    {'JobType': 'SystemErase', 'JobState': 'Failed'}
                ]
            }
        )

        # Initialize SystemErase object with mock idrac
        system_erase_obj = SystemErase(module=mock_module, idrac=mock_idrac)

        result = system_erase_obj.check_system_erase_job()
        assert result == 'Failed'

    @patch(MODULE_PATH + 'SystemErase.get_url')
    def test_check_system_erase_job_multiple_states(self, mock_get_url, mock_module):
        """Test check_system_erase_job with multiple jobs having different states."""
        mock_url = REDFISH_MOCK_URL
        mock_get_url.return_value = mock_url

        # Create a mock idrac object
        mock_idrac = MagicMock()
        mock_idrac.invoke_request.return_value = MagicMock(
            json_data={
                'Members': [
                    {'JobType': 'SystemErase', 'JobState': 'Running'},
                    {'JobType': 'SystemErase', 'JobState': 'New'},
                    {'JobType': 'SystemErase', 'JobState': 'Completed'}
                ]
            }
        )

        # Initialize SystemErase object with mock idrac
        system_erase_obj = SystemErase(module=mock_module, idrac=mock_idrac)

        result = system_erase_obj.check_system_erase_job()
        assert result == 'Completed'

    @patch(MODULE_PATH + 'SystemErase.get_url')
    def test_check_system_erase_job_no_jobs(self, mock_get_url, mock_module):
        """Test check_system_erase_job when no SystemErase jobs are found."""
        mock_url = REDFISH_MOCK_URL
        mock_get_url.return_value = mock_url

        # Create a mock idrac object
        mock_idrac = MagicMock()
        mock_idrac.invoke_request.return_value = MagicMock(
            json_data={'Members': []})

        # Initialize SystemErase object with mock idrac
        system_erase_obj = SystemErase(module=mock_module, idrac=mock_idrac)

        result = system_erase_obj.check_system_erase_job()
        assert result == 'Unknown'

    @patch(MODULE_PATH + 'SystemErase.get_url')
    def test_check_system_erase_job_no_system_erase_type(self, mock_get_url, mock_module):
        """Test check_system_erase_job when there are jobs but none of type 'SystemErase'."""
        mock_url = REDFISH_MOCK_URL
        mock_get_url.return_value = mock_url

        # Create a mock idrac object
        mock_idrac = MagicMock()
        mock_idrac.invoke_request.return_value = MagicMock(
            json_data={
                'Members': [
                    {'JobType': 'OtherType', 'JobState': 'Completed'},
                    {'JobType': 'OtherType', 'JobState': 'New'}
                ]
            }
        )

        # Initialize SystemErase object with mock idrac
        system_erase_obj = SystemErase(module=mock_module, idrac=mock_idrac)

        result = system_erase_obj.check_system_erase_job()
        assert result == 'Unknown'

    @patch(MODULE_PATH + 'SystemErase.get_url')
    def test_check_system_erase_job_partial_states(self, mock_get_url, mock_module):
        """Test check_system_erase_job with a mix of SystemErase and other jobs."""
        mock_url = REDFISH_MOCK_URL
        mock_get_url.return_value = mock_url

        # Create a mock idrac object
        mock_idrac = MagicMock()
        mock_idrac.invoke_request.return_value = MagicMock(
            json_data={
                'Members': [
                    {'JobType': 'OtherType', 'JobState': 'Completed'},
                    {'JobType': 'SystemErase', 'JobState': 'New'},
                    {'JobType': 'SystemErase', 'JobState': 'Scheduling'},
                    {'JobType': 'OtherType', 'JobState': 'Failed'}
                ]
            }
        )

        # Initialize SystemErase object with mock idrac
        system_erase_obj = SystemErase(module=mock_module, idrac=mock_idrac)

        result = system_erase_obj.check_system_erase_job()
        assert result == 'Scheduling'

    def test_validate_job_wait(self, idrac_default_args, idrac_connection_system_erase_mock, mocker):
        # Scenario 1: Negative timeout
        idrac_default_args.update({'job_wait': True, 'job_wait_timeout': -120})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        system_erase_obj = self.module.SystemErase(
            idrac_connection_system_erase_mock, f_module)
        with pytest.raises(Exception) as exc:
            system_erase_obj.validate_job_wait()
        assert exc.value.args[0] == TIMEOUT_NEGATIVE_OR_ZERO_MSG

        # Scenario 2: Valid timeout
        idrac_default_args.update({'job_wait': True, 'job_wait_timeout': 120})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        system_erase_obj = self.module.SystemErase(
            idrac_connection_system_erase_mock, f_module)
        resp = system_erase_obj.validate_job_wait()
        assert resp is None

    def test_check_allowable_value(self, idrac_default_args, idrac_connection_system_erase_mock, mocker):
        obj = MagicMock()
        obj.json_data = {
            "Actions": {
                "#DellLCService.SystemErase": {
                    "Component@Redfish.AllowableValues": [
                        "AllApps",
                        "BIOS",
                        "CryptographicErasePD",
                        "DIAG",
                        "DPU",
                        "DrvPack",
                        "IDRAC",
                        "LCData",
                        "NonVolatileMemory",
                        "OverwritePD",
                        "PERCNVCache",
                        "ReinstallFW",
                        "vFlash"
                    ]}}}
        # Scenario 1: Valid component
        mocker.patch(
            MODULE_PATH + SYSTEM_ERASE_URL, return_value=API_ONE)
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        system_erase_obj = self.module.SystemErase(
            idrac_connection_system_erase_mock, f_module)
        component = ["BIOS", "vFlash"]
        resp = system_erase_obj.check_allowable_value(component)
        assert resp == (['BIOS', 'vFlash'], [])

        # Scenario 2: Invalid component
        mocker.patch(
            MODULE_PATH + SYSTEM_ERASE_URL, return_value=API_ONE)
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        system_erase_obj = self.module.SystemErase(
            idrac_connection_system_erase_mock, f_module)
        component = ["invalid"]
        with pytest.raises(Exception) as exc:
            system_erase_obj.check_allowable_value(component)
        assert exc.value.args[0] == NO_COMPONENT_MATCH

        # Scenario 3: Invalid component in check_mode
        mocker.patch(
            MODULE_PATH + SYSTEM_ERASE_URL, return_value=API_ONE)
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        system_erase_obj = self.module.SystemErase(
            idrac_connection_system_erase_mock, f_module)
        component = ["invalid"]
        with pytest.raises(Exception) as exc:
            system_erase_obj.check_allowable_value(component)
        assert exc.value.args[0] == NO_CHANGES_FOUND_MSG

        # Scenario 4: Mixed components in check_mode
        mocker.patch(
            MODULE_PATH + SYSTEM_ERASE_URL, return_value=API_ONE)
        mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=True)
        system_erase_obj = self.module.SystemErase(
            idrac_connection_system_erase_mock, f_module)
        component = ["BIOS", "invalid"]
        with pytest.raises(Exception) as exc:
            system_erase_obj.check_allowable_value(component)
        assert exc.value.args[0] == CHANGES_FOUND_MSG

    def test_warn_unmatching_components(self, mocker):
        # Setup: mock module and warn method
        f_module = MagicMock()
        system_erase_obj = self.module.SystemErase(None, f_module)
        # Sample unmatching component list
        unmatching_components = ["invalid1", "invalid2"]
        warn_mock = mocker.patch.object(f_module, "warn")
        system_erase_obj.warn_unmatching_components(unmatching_components)

        expected_str = "invalid1', 'invalid2'"
        expected_msg = INVALID_COMPONENT_WARN_MSG.format(
            unmatching_components_str_format=expected_str)

        warn_mock.assert_called_once_with(expected_msg)

    @pytest.mark.parametrize("exc",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_idrac_system_erase_main_exception_handling_case(self, exc, mocker, idrac_default_args):
        idrac_default_args.update(
            {"component": ['BIOS']})
        # Scenario 1: HTTPError with random message id
        error_string = to_text(json.dumps({"error": {MESSAGE_EXTENDED: [
            {
                'MessageId': "123",
                "Message": HTTP_ERROR
            }
        ]}}))
        if exc in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + "SystemErase.execute",
                         side_effect=exc(HTTPS_PATH, 400,
                                         HTTP_ERROR,
                                         {"accept-type": APPLICATION_JSON},
                                         StringIO(error_string)))
        res_out = self._run_module(idrac_default_args)
        assert 'msg' in res_out

    def test_main(self, mocker):
        mock_module = mocker.MagicMock()
        mock_idrac = mocker.MagicMock()
        system_erase_mock = mocker.MagicMock()
        system_erase_mock.execute.return_value = (None, None)
        mocker.patch(MODULE_PATH + 'get_argument_spec', return_value={})
        mocker.patch(MODULE_PATH + 'IdracAnsibleModule',
                     return_value=mock_module)
        mocker.patch(MODULE_PATH + REDFISH_API, return_value=mock_idrac)
        mocker.patch(MODULE_PATH + 'SystemErase.validate_job_wait',
                     return_value=system_erase_mock)
        main()
        system_erase_mock.execute.return_value = (None, None)
        mocker.patch(MODULE_PATH + 'SystemErase.validate_job_wait',
                     return_value=system_erase_mock)
        main()

    class TestEraseComponent(FakeAnsibleModule):
        module = idrac_system_erase

        @pytest.fixture
        def idrac_system_erase_mock(self):
            idrac_obj = MagicMock()
            return idrac_obj

        @pytest.fixture
        def idrac_connection_system_erase_mock(self, mocker, idrac_system_erase_mock):
            idrac_conn_mock = mocker.patch(MODULE_PATH + REDFISH_API,
                                           return_value=idrac_system_erase_mock)
            idrac_conn_mock.return_value.__enter__.return_value = idrac_system_erase_mock
            return idrac_conn_mock

        def test_execute(self, idrac_default_args, idrac_connection_system_erase_mock, mocker):
            obj = MagicMock()
            obj.status_code = 202
            # Scenario 1: Status is success and job_wait as false
            idrac_default_args.update(
                {'component': ['DIAG'], 'job_wait': False})
            mocker.patch(
                MODULE_PATH + ALLOWABLE_VALUE_FUNC, return_value=(["DIAG"], []))
            mocker.patch(
                MODULE_PATH + SYSTEM_ERASE_URL, return_value=API_ONE)
            mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
            mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                         return_value=("/redfish/v1", None))
            f_module = self.get_module_mock(
                params=idrac_default_args, check_mode=False)
            erase_component_obj = self.module.EraseComponent(
                idrac_connection_system_erase_mock, f_module)
            with pytest.raises(Exception) as exc:
                erase_component_obj.execute()
            assert exc.value.args[0] == ERASE_SUCCESS_SCHEDULED_MSG

            # Scenario 2: Status is success and job_wait as true with power_on as true
            job = {"JobState": "Completed"}
            idrac_default_args.update(
                {'component': ['DIAG'], 'power_on': True, 'job_wait': True, 'job_wait_timeout': 1})
            mocker.patch(
                MODULE_PATH + ALLOWABLE_VALUE_FUNC, return_value=(["DIAG"], []))
            mocker.patch(
                MODULE_PATH + SYSTEM_ERASE_URL, return_value=API_ONE)
            mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
            mocker.patch(
                MODULE_PATH + SYSTEM_ERASE_JOB_STATUS, return_value=job)
            mocker.patch(MODULE_UTILS_PATH + "validate_and_get_first_resource_id_uri",
                         return_value=([MANAGER_URI_ONE], None))
            mocker.patch(MODULE_UTILS_PATH + "get_dynamic_uri",
                         return_value={"Actions": {"#ComputerSystem.Reset": {"target": API_ONE}}})
            mocker.patch(
                MODULE_UTILS_PATH + "trigger_restart_operation", return_value=(None, None))
            f_module = self.get_module_mock(
                params=idrac_default_args, check_mode=False)
            erase_component_obj = self.module.EraseComponent(
                idrac_connection_system_erase_mock, f_module)
            with pytest.raises(Exception) as exc:
                erase_component_obj.execute()
            assert exc.value.args[0] == ERASE_SUCCESS_POWER_ON_MSG

            # Scenario 3: Status is failure
            obj.status_code = 404
            job = {"JobState": "Failed"}
            idrac_default_args.update(
                {'component': ['DIAG']})
            mocker.patch(
                MODULE_PATH + ALLOWABLE_VALUE_FUNC, return_value=(["DIAG"], []))
            mocker.patch(
                MODULE_PATH + SYSTEM_ERASE_URL, return_value=API_ONE)
            mocker.patch(MODULE_PATH + API_INVOKE_MOCKER, return_value=obj)
            mocker.patch(
                MODULE_PATH + SYSTEM_ERASE_JOB_STATUS, return_value=job)
            f_module = self.get_module_mock(
                params=idrac_default_args, check_mode=False)
            erase_component_obj = self.module.EraseComponent(
                idrac_connection_system_erase_mock, f_module)
            with pytest.raises(Exception) as exc:
                erase_component_obj.execute()
            assert exc.value.args[0] == FAILURE_MSG
