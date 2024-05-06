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


class TestSession(FakeAnsibleModule):
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
        ome_conn_mock = mocker.patch(MODULE_PATH + 'SessionAPI',
                                       return_value=ome_session_mock)
        ome_conn_mock.return_value.__enter__.return_value = ome_session_mock
        return ome_conn_mock

    def test_get_session_url(self, ome_default_args, ome_connection_session_mock, mocker):
        """
        Test the `get_session_url` method of the `Session` class.

        This test function mocks the `get_dynamic_uri` function to return a dictionary
        containing the session URL. It then creates a `f_module` object with the
        `ome_default_args` and `check_mode` set to `False`. It initializes a
        `session_obj` with the `ome_connection_session_mock` and `f_module`.
        Finally, it calls the `get_session_url` method on the `session_obj` and
        asserts that the returned session URL is equal to the `SESSION_URL` constant.

        Args:
            self (TestGetSessionUrl): The test case object.
            ome_default_args (dict): The default arguments for the ome connection.
            ome_connection_session_mock (MagicMock): The mock object for the ome
                connection session.
            mocker (MagicMock): The mocker object for mocking functions and modules.

        Returns:
            None
        """
        base_api_resp = { "SessionService" : { "@odata.id": "/api/SessionService"}}
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value=base_api_resp)
        session_service_resp = {"Sessions@odata.navigationLink": "/api/SessionService/Sessions"}
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value=session_service_resp)
        f_module = self.get_module_mock(
            params=ome_default_args, check_mode=False)
        session_obj = self.module.Session(
            ome_connection_session_mock, f_module)
        sessions_url = session_obj.get_session_url()
        assert sessions_url == SESSION_URL


class TestCreateSession(FakeAnsibleModule):
    """
    Main class for testing the create_session module.
    """
    module = ome_session

    @pytest.fixture
    def create_session_mock(self):
        """
        Creates a mock object for the `ome_session` fixture.

        This function is a pytest fixture that creates a mock object of type `MagicMock` and
        assigns it to the variable `ome_obj`. The `ome_obj` mock object is then returned
        by the fixture.

        Returns:
            MagicMock: A mock object representing the `ome_session` fixture.
        """
        ome_obj = MagicMock()
        return ome_obj

    @pytest.fixture
    def ome_connection_session_mock(self, mocker, create_session_mock):
        """
        Creates a fixture for mocking the ome connection session.

        This fixture uses the `mocker` fixture from the `pytest` library to patch the
        `SessionAPI` class from the `MODULE_PATH` module. It returns a mock object of the
        `SessionAPI` class with the `create_session_mock` object as the return value.
        The `__enter__` method of the mock object is also patched to return the
        `create_session_mock` object.

        Parameters:
            - `self` (TestCase): The test case instance.
            - `mocker` (MockerFixture): The `mocker` fixture from the `pytest` library.
            - `create_session_mock` (Mock): The mock object representing the `create_session_mock`.

        Returns:
            - `ome_conn_mock` (MagicMock): The mock object of the `SessionAPI` class.
        """
        ome_conn_mock = mocker.patch(MODULE_PATH + 'SessionAPI',
                                       return_value=create_session_mock)
        ome_conn_mock.return_value.__enter__.return_value = create_session_mock
        return ome_conn_mock

    def test_session_operation(self, ome_default_args, ome_connection_session_mock):
        """
        Test the session operation of the module.

        Args:
            ome_default_args (dict): The default arguments for the ome connection.
            ome_connection_session_mock (MagicMock): The mock object for the ome
            connection session.

        Returns:
            None

        This function tests the session operation of the module by creating a session and deleting
        a session.
        It updates the `ome_default_args` dictionary with the appropriate state parameter and
        creates a `f_module` object with the updated arguments. It then creates a
        `session_operation_obj` object using the `CreateSession` class of the module and asserts
        that it is an instance of `CreateSession`.
        It repeats the same process for deleting a session by updating the `ome_default_args`
        dictionary with the state parameter set to "absent" and creating a `session_operation_obj`
        object using the
        `DeleteSession` class of the module. It asserts that it is an instance of `DeleteSession`.
        """
        ome_default_args.update({"state": "present"})
        f_module = self.get_module_mock(params=ome_default_args, check_mode=False)
        session_operation_obj = self.module.CreateSession(ome_connection_session_mock, f_module)
        assert isinstance(session_operation_obj, self.module.CreateSession)

        ome_default_args.update({"state": "absent"})
        f_module = self.get_module_mock(params=ome_default_args, check_mode=False)
        session_operation_obj = self.module.DeleteSession(ome_connection_session_mock, f_module)
        assert isinstance(session_operation_obj, self.module.DeleteSession)

    def test_create_session_failure(self, ome_connection_session_mock, mocker):
        """
        Test the failure scenario of creating a session.

        Args:
            ome_connection_session_mock (MagicMock): A mock object for the
            ome_connection_session.
            mocker (MockerFixture): A fixture for mocking objects.

        Returns:
            None

        This test function creates a session object using the `ome_connection_session_mock` and
        `f_module` objects.
        It sets the `session_obj.get_session_url` to return a session URL.
        It sets the `f_module.check_mode` to False and `f_module.params` to a dictionary containing
        the username and password.
        It mocks the `ome_connection_session_mock.invoke_request` method to return a response
        with a status code of 201.
        It calls the `session_obj.execute()` method to create the session.
        It asserts that the `f_module.exit_json` method is called once with the message "Unable to
        'create' a session." and `failed` set to True.
        """
        f_module = MagicMock()
        session_obj = ome_session.CreateSession(
            ome_connection_session_mock, f_module)
        session_obj.get_session_url = MagicMock(return_value=SESSION_URL)
        f_module.check_mode = False
        f_module.params = {
            "username": "admin",
            "password": "password"
        }
        response_mock = MagicMock()
        response_mock.status_code = 201
        mocker.patch.object(ome_connection_session_mock.return_value, 'invoke_request',
                            return_value=response_mock)

        session_obj.execute()
        f_module.exit_json.assert_called_once_with(
            msg="Unable to 'create' a session.",
            failed=True
        )

    def test_create_session_check_mode(self, ome_connection_session_mock):
        """
        Test the create session functionality in check mode.

        Args:
            ome_connection_session_mock (MagicMock): A mock object for the ome connection
            session.

        Returns:
            None

        This function tests the create session functionality in check mode. It creates an instance
        of the `CreateSession` class with the provided `ome_connection_session_mock` and a mock
        `f_module` object.
        It sets the required parameters for the `f_module` object and mocks the `get_session_url`
        method of the `session_obj` to return the session URL. It also mocks the `exit_json` method
        of the `f_module` object.

        Finally, it calls the `execute` method of the `session_obj` to execute the create session
        functionality in check mode.

        Note:
            This function assumes that the necessary imports and setup for the test are already
            done.
        """
        f_module = MagicMock()
        session_obj = ome_session.CreateSession(
            ome_connection_session_mock, f_module)
        f_module = self.get_module_mock(
            params={"session_id": "abcd", "hostname": "X.X.X.X"}, check_mode=True)
        session_obj.get_session_url = MagicMock(return_value=SESSION_URL)
        f_module.exit_json = MagicMock()

        session_obj.execute()

    def test_create_session_success(self, ome_connection_session_mock):
        """
        Test the successful creation of a session.

        Args:
            ome_connection_session_mock (MagicMock): A mock object representing the ome
            connection session.

        This test case verifies the successful creation of a session by mocking the necessary
        objects and invoking the `execute()` method of the `CreateSession` class. It sets the
        parameters for the `f_module` object, initializes the `session_obj` with the mocked
        `ome_connection_session_mock` and `f_module`, and mocks the necessary methods and
        attributes of the `ome` object. It then asserts that the `exit_json` method of the
        `f_module` object is called with the expected arguments.

        Returns:
            None
        """
        f_module = self.get_module_mock(
            params={"username": "admin", "password": "password"}, check_mode=False)
        session_obj = ome_session.CreateSession(ome_connection_session_mock, f_module)
        session_obj.get_session_url = MagicMock(return_value=SESSION_URL)
        session_obj.ome.invoke_request.return_value.status_code = 201
        session_obj.ome.invoke_request.return_value.json_data = {"SessionID": "123456"}
        session_obj.ome.invoke_request.return_value.headers.get.return_value = "token123"
        f_module.exit_json = MagicMock()

        session_obj.execute()
        f_module.exit_json.assert_called_once_with(
            msg=CREATE_SUCCESS_MSG,
            changed=True,
            session_data={"SessionID": "123456"},
            x_auth_token="token123"
        )


class TestDeleteSession(FakeAnsibleModule):
    """
    Main class for testing the delete session module.
    """
    module = ome_session

    @pytest.fixture
    def ome_session_mock(self):
        """
        Creates a mock object for the `ome_session` fixture.

        This function uses the `MagicMock` class from the `unittest.mock` module to create a mock
        object.
        The mock object is then returned by the function.

        Returns:
            MagicMock: A mock object representing the `ome_session`.
        """
        ome_obj = MagicMock()
        return ome_obj

    @pytest.fixture
    def ome_connection_session_mock(self, mocker, ome_session_mock):
        """
        Returns a mocked instance of the SessionAPI class from the specified module path.
        The mocked instance is created using the `mocker.patch` function. The `ome_session_mock`
        parameter is passed as the return value of the mocked instance. The `__enter__` method
        of the mocked instance is also mocked to return the `ome_session_mock`.
        :param mocker: The mocker fixture provided by the pytest framework.
        :type mocker: _pytest.monkeypatch.MonkeyPatch
        :param ome_session_mock: The mocked instance of the ome session.
        :type ome_session_mock: Any
        :return: The mocked instance of the SessionAPI class.
        :rtype: MagicMock
        """
        ome_conn_mock = mocker.patch(MODULE_PATH + 'SessionAPI',
                                       return_value=ome_session_mock)
        ome_conn_mock.return_value.__enter__.return_value = ome_session_mock
        return ome_conn_mock

    def test_delete_session_success_check_mode_changes(self, ome_connection_session_mock):
        """
        Test the `delete_session_success_check_mode_changes` method of the `DeleteSession` class.

        This method is responsible for testing the success case when the `delete_session` method
        is called in check mode.
        It verifies that the `exit_json` method of the `f_module` object is called with the
        appropriate arguments when the session is successfully deleted.

        Parameters:
            - ome_connection_session_mock (MagicMock): A mock object representing the
            `ome_connection_session` object.

        Returns:
            None
        """
        f_module = MagicMock()
        delete_session_obj = ome_session.DeleteSession(ome_connection_session_mock, f_module)
        delete_session_obj.ome.invoke_request.return_value.status_code = 200
        delete_session_obj.execute()
        f_module.exit_json.assert_called_once_with(msg=CHANGES_FOUND_MSG, changed=True)

    def test_delete_session_success_check_mode_no_changes(self, ome_connection_session_mock):
        """
        Test the success case of deleting a session in check mode when no changes are expected.

        Args:
            ome_connection_session_mock (MagicMock): A mock object representing the ome
            connection session.

        This function tests the scenario where the deletion of a session is successful in check
        mode and no changes are expected. It sets up the necessary mock objects and asserts that
        the `exit_json` method of the `f_module` object is called once with the `msg` parameter
        set to `NO_CHANGES_FOUND_MSG`.

        Returns:
            None
        """
        f_module = MagicMock()
        delete_session_obj = ome_session.DeleteSession(ome_connection_session_mock, f_module)
        delete_session_obj.ome.invoke_request.return_value.status_code = 201
        delete_session_obj.execute()
        f_module.exit_json.assert_called_once_with(msg=NO_CHANGES_FOUND_MSG)
