# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.2.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

from io import StringIO
import json

from urllib.error import HTTPError, URLError
import pytest
from mock import MagicMock
from ansible_collections.dellemc.openmanage.plugins.modules import ome_session
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import AnsibleFailJSonException
from ansible.module_utils.urls import SSLValidationError
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_session.'
MODULE_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.'

REDFISH = "/redfish/v1"
SESSIONS = "Sessions"
ODATA = "@odata.id"
ODATA_REGEX = "(.*?)@odata"

SESSION_URL = "/api/SessionService/Sessions"
GET_SESSION_URL = "Session.get_session_url"

CREATE_SUCCESS_MSG = "The session has been created successfully."
DELETE_SUCCESS_MSG = "The session has been deleted successfully."
FAILURE_MSG = "Unable to '{operation}' a session."
CHANGES_FOUND_MSG = "Changes found to be applied."
NO_CHANGES_FOUND_MSG = "No changes found to be applied."
HTTPS_PATH = "https://testhost.com"
HTTP_ERROR = "http error message"
APPLICATION_JSON = "application/json"


class TestOMESession(FakeAnsibleModule):
    """
    Main class for testing the ome_session module.
    """
    module = ome_session

    @pytest.fixture
    def ome_session_mock(self):
        """
        Creates a mock object for the `ome_session` fixture.

        This function uses the `MagicMock` class from the `unittest.mock` module to create a mock
        object. The mock object is then returned by the function.

        Returns:
            MagicMock: A mock object representing the `ome_session`.
        """
        ome_obj = MagicMock()
        return ome_obj

    @pytest.fixture
    def ome_connection_session_mock(self, mocker, ome_session_mock):
        """
        Returns a mock object for the `SessionAPI` class from the `MODULE_PATH` module.
        The mock object is initialized with the `ome_session_mock` as the return value.
        The `__enter__` method of the mock object is also mocked to return `ome_session_mock`.

        :param mocker: The pytest fixture for mocking objects.
        :type mocker: pytest_mock.plugin.MockerFixture
        :param ome_session_mock: The mock object for the `ome_session_mock`.
        :type ome_session_mock: Any
        :return: The mock object for the `SessionAPI` class.
        :rtype: MagicMock
        """
        ome_conn_mock = mocker.patch(MODULE_PATH + 'OMESession', return_value=ome_session_mock)
        ome_conn_mock.return_value.__enter__.return_value = ome_session_mock
        return ome_conn_mock

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_ome_session_main_exception_handling_case(self, exc_type, ome_default_args, mocker):
        """
        Test the exception handling of the `ome_session_main` module.

        This function tests the exception handling of the `ome_session_main` module by mocking
        different exceptions and verifying the expected behavior.

        Parameters:
            - exc_type (Exception): The type of exception to be raised.
            - ome_default_args (dict): The default arguments for the module.
            - mocker (MockerFixture): The mocker fixture for mocking functions.

        Returns:
            None

        Raises:
            AssertionError: If the expected result does not match the actual result.

        Notes:
            - The function uses the `pytest.mark.parametrize` decorator to parameterize the test
            cases.
            - The `exc_type` parameter represents the type of exception to be raised.
            - The `ome_default_args` parameter contains the default arguments for the module.
            - The `mocker` parameter is used to mock functions and simulate different exceptions.
            - The function calls the `_run_module` method with the `ome_default_args` to execute
            the module.
            - The function verifies the expected result based on the raised exception type.

        """
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + "OMESession.get_session_url",
                         side_effect=exc_type(HTTPS_PATH, 400,
                                              HTTP_ERROR,
                                              {"accept-type": APPLICATION_JSON},
                                              StringIO(json_str)))
        else:
            ome_default_args.update({"state": "absent", "session_id": "abcd",
                                    "x_auth_token": "token123"})
            mocker.patch(MODULE_PATH + "OMESession.get_session_url",
                         side_effect=exc_type('test'))
        result = self._run_module(ome_default_args)
        if exc_type == URLError:
            assert result['unreachable'] is True
        else:
            assert result['failed'] is True
        assert 'msg' in result
