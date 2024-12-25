# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


from io import StringIO
import json


from urllib.error import HTTPError, URLError
import pytest
from unittest.mock import MagicMock
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_session
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import AnsibleFailJSonException
from ansible.module_utils.urls import SSLValidationError
from ansible.module_utils._text import to_text


MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_session.'
MODULE_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.'

REDFISH = "/redfish/v1"
SESSIONS = "Sessions"
ODATA = "@odata.id"
ODATA_REGEX = "(.*?)@odata"

SESSION_URL = "/redfish/v1/SessionService/Sessions"
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
    Main class for testing the idrac_session module.
    """
    module = idrac_session

    @pytest.fixture
    def idrac_session_mock(self):
        """
        Creates a mock object for the `idrac_session` fixture.

        This function uses the `MagicMock` class from the `unittest.mock` module to create a mock
        object. The mock object is then returned by the function.

        Returns:
            MagicMock: A mock object representing the `idrac_session`.
        """
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_session_mock(self, mocker, idrac_session_mock):
        """
        Returns a mock object for the `SessionAPI` class from the `MODULE_PATH` module.
        The mock object is initialized with the `idrac_session_mock` as the return value.
        The `__enter__` method of the mock object is also mocked to return `idrac_session_mock`.

        :param mocker: The pytest fixture for mocking objects.
        :type mocker: pytest_mock.plugin.MockerFixture
        :param idrac_session_mock: The mock object for the `idrac_session_mock`.
        :type idrac_session_mock: Any
        :return: The mock object for the `SessionAPI` class.
        :rtype: MagicMock
        """
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'SessionAPI',
                                       return_value=idrac_session_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_session_mock
        return idrac_conn_mock

    def test_get_session_url(self, idrac_default_args, idrac_connection_session_mock, mocker):
        """
        Test the `get_session_url` method of the `Session` class.

        This test function mocks the `get_dynamic_uri` function to return a dictionary
        containing the session URL. It then creates a `f_module` object with the
        `idrac_default_args` and `check_mode` set to `False`. It initializes a
        `session_obj` with the `idrac_connection_session_mock` and `f_module`.
        Finally, it calls the `get_session_url` method on the `session_obj` and
        asserts that the returned session URL is equal to the `SESSION_URL` constant.

        Args:
            self (TestGetSessionUrl): The test case object.
            idrac_default_args (dict): The default arguments for the IDRAC connection.
            idrac_connection_session_mock (MagicMock): The mock object for the IDRAC
                connection session.
            mocker (MagicMock): The mocker object for mocking functions and modules.

        Returns:
            None
        """
        v1_resp = {'Links': {'Sessions': {'@odata.id': SESSION_URL}}}
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     return_value=v1_resp)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        session_obj = self.module.Session(
            idrac_connection_session_mock, f_module)
        sessions_url = session_obj.get_session_url()
        assert sessions_url == SESSION_URL


class TestCreateSession(FakeAnsibleModule):
    """
    Main class for testing the create_session module.
    """
    module = idrac_session

    @pytest.fixture
    def create_session_mock(self):
        """
        Creates a mock object for the `idrac_session` fixture.

        This function is a pytest fixture that creates a mock object of type `MagicMock` and
        assigns it to the variable `idrac_obj`. The `idrac_obj` mock object is then returned
        by the fixture.

        Returns:
            MagicMock: A mock object representing the `idrac_session` fixture.
        """
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_session_mock(self, mocker, create_session_mock):
        """
        Creates a fixture for mocking the IDRAC connection session.

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
            - `idrac_conn_mock` (MagicMock): The mock object of the `SessionAPI` class.
        """
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'SessionAPI',
                                       return_value=create_session_mock)
        idrac_conn_mock.return_value.__enter__.return_value = create_session_mock
        return idrac_conn_mock

    def test_session_operation(self, idrac_default_args, idrac_connection_session_mock):
        """
        Test the session operation of the module.

        Args:
            idrac_default_args (dict): The default arguments for the IDRAC connection.
            idrac_connection_session_mock (MagicMock): The mock object for the IDRAC
            connection session.

        Returns:
            None

        This function tests the session operation of the module by creating a session and deleting
        a session.
        It updates the `idrac_default_args` dictionary with the appropriate state parameter and
        creates a `f_module` object with the updated arguments. It then creates a
        `session_operation_obj` object using the `CreateSession` class of the module and asserts
        that it is an instance of `CreateSession`.
        It repeats the same process for deleting a session by updating the `idrac_default_args`
        dictionary with the state parameter set to "absent" and creating a `session_operation_obj`
        object using the
        `DeleteSession` class of the module. It asserts that it is an instance of `DeleteSession`.
        """
        idrac_default_args.update({"state": "present"})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        session_operation_obj = self.module.CreateSession(idrac_connection_session_mock, f_module)
        assert isinstance(session_operation_obj, self.module.CreateSession)

        idrac_default_args.update({"state": "absent"})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        session_operation_obj = self.module.DeleteSession(idrac_connection_session_mock, f_module)
        assert isinstance(session_operation_obj, self.module.DeleteSession)

    def test_create_session_failure(self, idrac_connection_session_mock, mocker):
        """
        Test the failure scenario of creating a session.

        Args:
            idrac_connection_session_mock (MagicMock): A mock object for the
            idrac_connection_session.
            mocker (MockerFixture): A fixture for mocking objects.

        Returns:
            None

        This test function creates a session object using the `idrac_connection_session_mock` and
        `f_module` objects.
        It sets the `session_obj.get_session_url` to return a session URL.
        It sets the `f_module.check_mode` to False and `f_module.params` to a dictionary containing
        the username and password.
        It mocks the `idrac_connection_session_mock.invoke_request` method to return a response
        with a status code of 201.
        It calls the `session_obj.execute()` method to create the session.
        It asserts that the `f_module.exit_json` method is called once with the message "Unable to
        'create' a session." and `failed` set to True.
        """
        f_module = MagicMock()
        session_obj = idrac_session.CreateSession(
            idrac_connection_session_mock, f_module)
        session_obj.get_session_url = MagicMock(return_value=SESSION_URL)
        f_module.check_mode = False
        f_module.params = {
            "username": "admin",
            "password": "password"
        }
        response_mock = MagicMock()
        response_mock.status_code = 201
        mocker.patch.object(idrac_connection_session_mock.return_value, 'invoke_request',
                            return_value=response_mock)

        session_obj.execute()
        f_module.exit_json.assert_called_once_with(
            msg="Unable to 'create' a session.",
            failed=True
        )

    def test_create_session_check_mode(self, idrac_connection_session_mock):
        """
        Test the create session functionality in check mode.

        Args:
            idrac_connection_session_mock (MagicMock): A mock object for the IDRAC connection
            session.

        Returns:
            None

        This function tests the create session functionality in check mode. It creates an instance
        of the `CreateSession` class with the provided `idrac_connection_session_mock` and a mock
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
        session_obj = idrac_session.CreateSession(
            idrac_connection_session_mock, f_module)
        f_module = self.get_module_mock(
            params={"session_id": "1234", "hostname": "X.X.X.X"}, check_mode=True)
        session_obj.get_session_url = MagicMock(return_value=SESSION_URL)
        f_module.exit_json = MagicMock()

        session_obj.execute()

    def test_create_session_success(self, idrac_connection_session_mock):
        """
        Test the successful creation of a session.

        Args:
            idrac_connection_session_mock (MagicMock): A mock object representing the IDRAC
            connection session.

        This test case verifies the successful creation of a session by mocking the necessary
        objects and invoking the `execute()` method of the `CreateSession` class. It sets the
        parameters for the `f_module` object, initializes the `session_obj` with the mocked
        `idrac_connection_session_mock` and `f_module`, and mocks the necessary methods and
        attributes of the `idrac` object. It then asserts that the `exit_json` method of the
        `f_module` object is called with the expected arguments.

        Returns:
            None
        """
        f_module = self.get_module_mock(
            params={"username": "admin", "password": "password"}, check_mode=False)
        session_obj = idrac_session.CreateSession(idrac_connection_session_mock, f_module)
        session_obj.get_session_url = MagicMock(return_value=SESSION_URL)
        session_obj.idrac.invoke_request.return_value.status_code = 201
        session_obj.idrac.invoke_request.return_value.json_data = {"SessionID": "123456"}
        session_obj.idrac.invoke_request.return_value.headers.get.return_value = "token123"
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
    module = idrac_session

    @pytest.fixture
    def idrac_session_mock(self):
        """
        Creates a mock object for the `idrac_session` fixture.

        This function uses the `MagicMock` class from the `unittest.mock` module to create a mock
        object.
        The mock object is then returned by the function.

        Returns:
            MagicMock: A mock object representing the `idrac_session`.
        """
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_session_mock(self, mocker, idrac_session_mock):
        """
        Returns a mocked instance of the SessionAPI class from the specified module path.
        The mocked instance is created using the `mocker.patch` function. The `idrac_session_mock`
        parameter is passed as the return value of the mocked instance. The `__enter__` method
        of the mocked instance is also mocked to return the `idrac_session_mock`.
        :param mocker: The mocker fixture provided by the pytest framework.
        :type mocker: _pytest.monkeypatch.MonkeyPatch
        :param idrac_session_mock: The mocked instance of the idrac session.
        :type idrac_session_mock: Any
        :return: The mocked instance of the SessionAPI class.
        :rtype: MagicMock
        """
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'SessionAPI',
                                       return_value=idrac_session_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_session_mock
        return idrac_conn_mock

    def test_delete_session_success_check_mode_changes(self, idrac_connection_session_mock):
        """
        Test the `delete_session_success_check_mode_changes` method of the `DeleteSession` class.

        This method is responsible for testing the success case when the `delete_session` method
        is called in check mode.
        It verifies that the `exit_json` method of the `f_module` object is called with the
        appropriate arguments when the session is successfully deleted.

        Parameters:
            - idrac_connection_session_mock (MagicMock): A mock object representing the
            `idrac_connection_session` object.

        Returns:
            None
        """
        f_module = MagicMock()
        delete_session_obj = idrac_session.DeleteSession(idrac_connection_session_mock, f_module)
        delete_session_obj.idrac.invoke_request.return_value.status_code = 200
        delete_session_obj.execute()
        f_module.exit_json.assert_called_once_with(msg=CHANGES_FOUND_MSG, changed=True)

    def test_delete_session_success_check_mode_no_changes(self, idrac_connection_session_mock):
        """
        Test the success case of deleting a session in check mode when no changes are expected.

        Args:
            idrac_connection_session_mock (MagicMock): A mock object representing the IDRAC
            connection session.

        This function tests the scenario where the deletion of a session is successful in check
        mode and no changes are expected. It sets up the necessary mock objects and asserts that
        the `exit_json` method of the `f_module` object is called once with the `msg` parameter
        set to `NO_CHANGES_FOUND_MSG`.

        Returns:
            None
        """
        f_module = MagicMock()
        delete_session_obj = idrac_session.DeleteSession(idrac_connection_session_mock, f_module)
        delete_session_obj.idrac.invoke_request.return_value.status_code = 201
        delete_session_obj.execute()
        f_module.exit_json.assert_called_once_with(msg=NO_CHANGES_FOUND_MSG)

    def test_delete_session_success(self, idrac_connection_session_mock):
        """
        Test the successful deletion of a session.

        This test function verifies the behavior of the `DeleteSession` class when a session is
        successfully deleted. It mocks the `idrac_connection_session_mock` object and sets up the
        necessary parameters for the `f_module` object. It then creates an instance of the
        `DeleteSession` class with the mocked `idrac_connection_session_mock` and the
        `f_module` object.

        The `get_session_url` method of the `session_obj` is mocked to return a specific session
        URL. The `invoke_request` method of the `idrac` object of the `session_obj` is also mocked
        to return a response with a status code of 200. The `exit_json` method of the `f_module`
        object is mocked as well.

        The `execute` method of the `session_obj` is called to execute the deletion of the session.
        Finally, the `exit_json` method of the `f_module` object is asserted to have been called
        with the expected arguments, including the success message and the changed flag set to
        `True`.

        Parameters:
            - idrac_connection_session_mock (MagicMock): A mocked object representing the
            `idrac_connection_session_mock` object.

        Returns:
            None
        """
        f_module = self.get_module_mock(
            params={"session_id": "1234", "hostname": "X.X.X.X"}, check_mode=False)
        session_obj = idrac_session.DeleteSession(idrac_connection_session_mock, f_module)
        session_obj.get_session_url = MagicMock(return_value=SESSION_URL)
        session_obj.idrac.invoke_request.return_value.status_code = 200
        f_module.exit_json = MagicMock()
        session_obj.execute()
        f_module.exit_json.assert_called_once_with(msg=DELETE_SUCCESS_MSG, changed=True)

    def test_delete_session_check_mode_false_no_changes(self, idrac_connection_session_mock):
        """
        Test the scenario where the delete session is executed in check mode with `check_mode` set
        to False and no changes are expected.

        Args:
            idrac_connection_session_mock (MagicMock): A mock object representing the IDRAC
            connection session.

        Returns:
            None

        This function creates a mock module object with the specified parameters and
        initializes the `DeleteSession` object with the mock IDRAC connection and module. It sets
        the `get_session_url` method of the session object to return a specific session URL. It
        sets the status code of the invoke request to 201. It then asserts that the `exit_json`
        method of the module object is called once with the `msg` parameter set to the
        `NO_CHANGES_FOUND_MSG` constant.
        """
        f_module = self.get_module_mock(
            params={"session_id": "1234", "hostname": "X.X.X.X"}, check_mode=False)
        session_obj = idrac_session.DeleteSession(idrac_connection_session_mock, f_module)
        session_obj.get_session_url = MagicMock(return_value=SESSION_URL)
        session_obj.idrac.invoke_request.return_value.status_code = 201
        f_module.exit_json = MagicMock()
        session_obj.execute()
        f_module.exit_json.assert_called_once_with(msg=NO_CHANGES_FOUND_MSG)

    def test_delete_session_http_error(self, idrac_connection_session_mock):
        """
        Test the behavior of the `DeleteSession` class when an HTTP error occurs during the
        deletion of a session.

        This test case creates a mock `f_module` object with the necessary parameters and
        initializes a `DeleteSession` object with the mock `idrac_connection_session_mock` and the
        `f_module` object. It then sets up the necessary mock functions and side effects to
        simulate an HTTP error during the deletion of a session. Finally, it executes the
        `execute()` method of the `DeleteSession` object and asserts that an
        `AnsibleFailJSonException` is raised with the expected failure message and error
        information.

        Parameters:
            - idrac_connection_session_mock (MagicMock): A mock object representing the
            `idrac_connection_session_mock` parameter.

        Raises:
            - AssertionError: If the expected failure message or error information is not present
            in the raised exception.

        Returns:
            None
        """
        f_module = self.get_module_mock(
            params={"session_id": "1234", "hostname": "X.X.X.X"}, check_mode=False)
        session_obj = idrac_session.DeleteSession(idrac_connection_session_mock, f_module)
        session_obj.get_session_url = MagicMock(return_value=SESSION_URL)
        session_obj.get_session_status = MagicMock(return_value=200)
        json_str = to_text(json.dumps({"data": "out"}))
        session_obj.idrac.invoke_request.side_effect = HTTPError(HTTPS_PATH, 200,
                                                                 HTTP_ERROR,
                                                                 {"accept-type": APPLICATION_JSON},
                                                                 StringIO(json_str))
        try:
            session_obj.execute()
        except AnsibleFailJSonException as ex:
            assert ex.fail_msg == "Unable to 'delete' a session."
            assert ex.fail_kwargs == {'error_info': {'data': 'out'}, 'failed': True}


class TestMain(FakeAnsibleModule):
    """
    Class for testing the main.
    """
    module = idrac_session

    @pytest.fixture
    def idrac_session_mock(self):
        """
        Creates a mock object for the `idrac_session` fixture.

        This function uses the `MagicMock` class from the `unittest.mock` module to create a mock
        object.
        The mock object is then returned by the function.

        Returns:
            MagicMock: A mock object representing the `idrac_session`.
        """
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_session_mock(self, mocker, idrac_session_mock):
        """
        Returns a mock object for the `SessionAPI` class from the `MODULE_PATH` module.
        The mock object is initialized with the `idrac_session_mock` as the return value.
        The `__enter__` method of the mock object is also mocked to return `idrac_session_mock`.

        :param mocker: The pytest fixture for mocking objects.
        :type mocker: pytest_mock.plugin.MockerFixture
        :param idrac_session_mock: The mock object for the `idrac_session_mock`.
        :type idrac_session_mock: Any
        :return: The mock object for the `SessionAPI` class.
        :rtype: MagicMock
        """
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'SessionAPI',
                                       return_value=idrac_session_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_session_mock
        return idrac_conn_mock

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError,
                              TypeError, ValueError])
    def test_idrac_session_main_exception_handling_case(self, exc_type, ome_default_args, mocker):
        """
        Test the exception handling of the `idrac_session_main` module.

        This function tests the exception handling of the `idrac_session_main` module by mocking
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
            mocker.patch(MODULE_PATH + "CreateSession.get_session_url",
                         side_effect=exc_type(HTTPS_PATH, 400,
                                              HTTP_ERROR,
                                              {"accept-type": APPLICATION_JSON},
                                              StringIO(json_str)))
        else:
            ome_default_args.update({"state": "absent", "session_id": "1234",
                                    "x_auth_token": "token123"})
            mocker.patch(MODULE_PATH + "DeleteSession.get_session_url",
                         side_effect=exc_type('test'))
        result = self._run_module(ome_default_args)
        if exc_type == URLError:
            assert result['unreachable'] is True
        else:
            assert result['failed'] is True
        assert 'msg' in result
