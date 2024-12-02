# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.2.0
# Copyright (C) 2024 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import os
import json
import pytest
from unittest.mock import MagicMock
from ansible.module_utils.urls import SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible_collections.dellemc.openmanage.plugins.module_utils.session_utils import SessionAPI, OpenURLResponse

MODULE_UTIL_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.'
OPEN_URL = 'session_utils.open_url'
TEST_PATH = "/testpath"
INVOKE_REQUEST = 'session_utils.SessionAPI.invoke_request'
JOB_COMPLETE = 'session_utils.SessionAPI.wait_for_job_complete'
API_TASK = '/api/tasks'
SLEEP_TIME = 'session_utils.time.sleep'


class TestSessionRest(object):
    """
    Main class for testing the SessionUtils class.
    """
    @pytest.fixture
    def mock_response(self):
        """
        Returns a MagicMock object representing a mock HTTP response.

        The mock response has the following properties:
        - `getcode()` method returns 200
        - `headers` property is a dictionary containing the headers of the response
        - `getheaders()` method returns the same dictionary as `headers`
        - `read()` method returns a JSON string representing a dictionary with a "value" key and
        "data" as its value

        :return: A MagicMock object representing a mock HTTP response.
        :rtype: MagicMock
        """
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = mock_response.getheaders.return_value = {
            'X-Auth-Token': 'token_id'}
        mock_response.read.return_value = json.dumps({"value": "data"})
        return mock_response

    @pytest.fixture
    def module_params(self):
        """
        Fixture that returns a dictionary containing module parameters.

        :return: A dictionary with the following keys:
                 - 'hostname': The hostname of the module.
                 - 'username': The username for authentication.
                 - 'password': The password for authentication.
                 - 'port': The port number for the module.
        """
        module_parameters = {'hostname': 'xxx.xxx.x.x', 'username': 'username',
                             'password': 'password', 'port': '443'}
        return module_parameters

    @pytest.fixture
    def session_utils_object(self, module_params):
        """
        Creates a SessionAPI object using the provided `module_params` and returns it.

        :param module_params: A dictionary containing the parameters for the SessionAPI object.
        :type module_params: dict
        :return: A SessionAPI object.
        :rtype: SessionAPI
        """
        session_utils_obj = SessionAPI(module_params)
        return session_utils_obj

    def test_invoke_request_with_session(self, mock_response, mocker, module_params):
        """
        Test the invoke_request method of the SessionAPI class with a session.

        Args:
            mock_response (MagicMock): A mocked response object.
            mocker (MockerFixture): A fixture for mocking objects.
            module_params (dict): The parameters for the module.

        Returns:
            None

        Assertions:
            - Asserts that the response status code is 200.
            - Asserts that the response JSON data is {"value": "data"}.
            - Asserts that the response success attribute is True.
        """
        mocker.patch(MODULE_UTIL_PATH + OPEN_URL,
                     return_value=mock_response)
        obj = SessionAPI(module_params)
        response = obj.invoke_request(TEST_PATH, "GET")
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    def test_invoke_request_without_session(self, mock_response, mocker):
        """
        Test the `invoke_request` method of the `SessionAPI` class without using a session.

        This test case mocks the `open_url` function from the `MODULE_UTIL_PATH` module to return a
        mock response.
        It then creates an instance of the `SessionAPI` class with mock module parameters.
        The `invoke_request` method is called with a test path and a GET method.
        The test asserts that the response status code is 200, the response JSON data is
        {"value": "data"},
        and the response success flag is True.

        Parameters:
            - mock_response (MagicMock): A mock response object to be returned by the `open_url`
            function.
            - mocker (MockerFixture): A fixture provided by the pytest library for mocking
            functions.

        Returns:
            None
        """
        mocker.patch(MODULE_UTIL_PATH + OPEN_URL,
                     return_value=mock_response)
        module_params = {'hostname': 'XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX', 'username':
                         'username',
                         'password': 'password', "port": '443'}
        obj = SessionAPI(module_params)
        response = obj.invoke_request(TEST_PATH, "GET")
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    def test_invoke_request_without_session_with_header(self, mock_response, mocker,
                                                        module_params):
        """
        Test the `invoke_request` method of the `SessionAPI` class when a session is not used and a
        header is provided.

        This test method mocks the `open_url` function from the `module_utils` module to return a
        mock response object. It then creates an instance of the `SessionAPI` class with the
        provided `module_params`. The `invoke_request` method is called with a test path, a request
        method of "POST", and a headers dictionary containing a single key-value pair.

        The test asserts that the response status code is 200, the response JSON data is
        `{"value": "data"}`, and the response success flag is `True`.

        Parameters:
            - `mock_response` (MagicMock): A mock response object to be returned by the `open_url`
            function.
            - `mocker` (MockerFixture): A fixture for patching and mocking objects.
            - `module_params` (dict): A dictionary containing the module parameters.

        Returns:
            None
        """
        mocker.patch(MODULE_UTIL_PATH + OPEN_URL,
                     return_value=mock_response)
        obj = SessionAPI(module_params)
        response = obj.invoke_request(TEST_PATH, "POST", headers={"application": "octstream"})
        assert response.status_code == 200
        assert response.json_data == {"value": "data"}
        assert response.success is True

    @pytest.mark.parametrize("exc", [URLError, SSLValidationError, ConnectionError])
    def test_invoke_request_error_case_handling(self, exc, mocker, module_params):
        """
        Test the error handling in the `invoke_request` method of the `SessionAPI` class.

        This function tests the handling of different types of exceptions that can occur during an
        HTTP request. It uses the `pytest.mark.parametrize` decorator to run the test multiple
        times with different exception types. The test mocks the `open_url` method of the
        `SessionAPI` class to raise the specified exception. It then asserts that the correct
        exception is raised when calling the `invoke_request` method.

        Args:
            exc (Exception): The exception type to test.
            mocker (MockerFixture): The mocker fixture used for mocking dependencies.
            module_params (dict): The parameters for the `SessionAPI` object.

        Raises:
            exc: The specified exception type if it is raised during the `invoke_request` call.
        """
        mocker.patch(MODULE_UTIL_PATH + OPEN_URL,
                     side_effect=exc("test"))
        with pytest.raises(exc):
            obj = SessionAPI(module_params)
            obj.invoke_request(TEST_PATH, "GET")

    def test_invoke_request_http_error_handling(self, mock_response, mocker, module_params):
        """
        Test the HTTP error handling in the `invoke_request` method of the `SessionAPI` class.

        Args:
            mock_response (Mock): A mock object representing the response from the HTTP request.
            mocker (MockerFixture): A fixture for mocking objects.
            module_params (dict): The parameters for the module.

        Raises:
            HTTPError: If an HTTP error occurs during the invocation of the request.

        Returns:
            None
        """
        open_url_mock = mocker.patch(MODULE_UTIL_PATH + OPEN_URL,
                                     return_value=mock_response)
        open_url_mock.side_effect = HTTPError('https://testhost.com/', 400,
                                              'Bad Request Error', {}, None)
        with pytest.raises(HTTPError):
            obj = SessionAPI(module_params)
            obj.invoke_request(TEST_PATH, "GET")

    @pytest.mark.parametrize("query_params", [
        {"inp": {"$filter": "UserName eq 'admin'"},
            "out": "%24filter=UserName+eq+%27admin%27"},
        {"inp": {"$top": 1, "$skip": 2, "$filter": "JobType/Id eq 8"}, "out":
            "%24top=1&%24skip=2&%24filter=JobType%2FId+eq+8"},
        {"inp": {"$top": 1, "$skip": 3}, "out": "%24top=1&%24skip=3"}
    ])
    def test_build_url(self, query_params, mocker, session_utils_object):
        """
        builds complete url
        """
        base_uri = 'https://xxx.xxx.x.x:443/api'
        path = "/AccountService/Accounts"
        mocker.patch(MODULE_UTIL_PATH + 'session_utils.SessionAPI._get_url',
                     return_value=base_uri + path)
        inp = query_params["inp"]
        out = query_params["out"]
        url = session_utils_object._build_url(
            path, query_param=inp)
        assert url == base_uri + path + "?" + out

    def test_build_url_none(self, mocker, session_utils_object):
        """
        builds complete url
        """
        base_uri = 'https://xxx.xxx.x.x:443/api'
        mocker.patch(MODULE_UTIL_PATH + 'redfish.Redfish._get_base_url',
                     return_value=base_uri)
        url = session_utils_object._build_url("", None)
        assert url == ""

    def test_invalid_json_openurlresp(self):
        """
        Test the behavior when an invalid JSON string is passed to the `OpenURLResponse` object.

        This test case creates an instance of the `OpenURLResponse` class with an empty dictionary
        as the initial data.
        Then, it sets the `body` attribute of the object to an invalid JSON string.
        Finally, it asserts that calling the `json_data` attribute raises a `ValueError` with the
        message "Unable to parse json".

        Parameters:
            self (TestCase): The current test case instance.

        Returns:
            None
        """
        obj = OpenURLResponse({})
        obj.body = 'invalid json'
        with pytest.raises(ValueError) as e:
            obj.json_data
        assert e.value.args[0] == "Unable to parse json"

    def test_reason(self):
        """
        Test the `reason` property of the `OpenURLResponse` class.

        This test case mocks the `read` method of the `obj` object to return an empty JSON string.
        It then creates an instance of the `OpenURLResponse` class with the mocked `obj` object.
        The `reason` property of the `OpenURLResponse` instance is then accessed and stored in the
        `reason_ret` variable. Finally, the test asserts that the value of `reason_ret` is equal to
        the expected value of "returning reason".

        Parameters:
            self (TestCase): The test case object.

        Returns:
            None
        """
        def mock_read():
            return "{}"
        obj = MagicMock()
        obj.reason = "returning reason"
        obj.read = mock_read
        ourl = OpenURLResponse(obj)
        reason_ret = ourl.reason
        assert reason_ret == "returning reason"

    def test_requests_ca_bundle_set(self, mocker, mock_response, session_utils_object):
        """
        Test if the `REQUESTS_CA_BUNDLE` environment variable is set correctly.

        This function tests if the `REQUESTS_CA_BUNDLE` environment variable is set to the expected
        value. It does this by setting the environment variable to a specific path, patching the
        `invoke_request` method of the `session_utils_object` to return a mock response, and then
        calling the `_get_omam_ca_env` method of the `session_utils_object`. Finally, it asserts
        that the result of the `_get_omam_ca_env` method is equal to the expected path.

        Parameters:
            - mocker (MockerFixture): A fixture provided by the pytest library used to patch the
            `invoke_request` method.
            - mock_response (Mock): A mock object representing the response returned by the
            `invoke_request` method.
            - session_utils_object (SessionUtils): An instance of the `SessionUtils` class.

        Returns:
            None
        """
        os.environ["REQUESTS_CA_BUNDLE"] = "/path/to/requests_ca_bundle.pem"
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        result = session_utils_object._get_omam_ca_env()
        assert result == "/path/to/requests_ca_bundle.pem"
        del os.environ["REQUESTS_CA_BUNDLE"]

    def test_curl_ca_bundle_set(self, mocker, mock_response, session_utils_object):
        """
        Test the functionality of the `curl_ca_bundle_set` method.

        This test case verifies that the `curl_ca_bundle_set` method correctly sets the
        `CURL_CA_BUNDLE` environment variable and retrieves the value using the `_get_omam_ca_env`
        method.

        Parameters:
            - mocker (MockerFixture): A fixture provided by the pytest-mock library used to patch
            the `invoke_request` method.
            - mock_response (MagicMock): A mock object representing the response returned by the
            `invoke_request` method.
            - session_utils_object (SessionUtils): An instance of the `SessionUtils` class.

        Returns:
            None

        Raises:
            AssertionError: If the retrieved value from `_get_omam_ca_env` does not match the
            expected value.

        Note:
            - The test case sets the `CURL_CA_BUNDLE` environment variable to
            "/path/to/curl_ca_bundle.pem" before executing the test.
            - The test case deletes the `CURL_CA_BUNDLE` environment variable after the test is
            completed.
        """
        os.environ["CURL_CA_BUNDLE"] = "/path/to/curl_ca_bundle.pem"
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        result = session_utils_object._get_omam_ca_env()
        assert result == "/path/to/curl_ca_bundle.pem"
        del os.environ["CURL_CA_BUNDLE"]

    def test_omam_ca_bundle_set(self, mocker, mock_response, session_utils_object):
        """
        Test the functionality of the `_get_omam_ca_env` method in the `SessionUtils` class.

        This test case verifies that the `_get_omam_ca_env` method correctly retrieves the value of
        the `OMAM_CA_BUNDLE` environment variable and returns it.

        Parameters:
            - mocker (MockerFixture): A fixture provided by the pytest library used for mocking
            objects.
            - mock_response (MagicMock): A mock object representing the response returned by the
            `invoke_request` method.
            - session_utils_object (SessionUtils): An instance of the `SessionUtils` class.

        Returns:
            None

        Raises:
            AssertionError: If the returned value from `_get_omam_ca_env` does not match the
            expected value.

        Side Effects:
            - Sets the value of the `OMAM_CA_BUNDLE` environment variable to
            "/path/to/omam_ca_bundle.pem".
            - Deletes the `OMAM_CA_BUNDLE` environment variable after the test case is complete.
        """
        os.environ["OMAM_CA_BUNDLE"] = "/path/to/omam_ca_bundle.pem"
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        result = session_utils_object._get_omam_ca_env()
        assert result == "/path/to/omam_ca_bundle.pem"
        del os.environ["OMAM_CA_BUNDLE"]

    def test_no_env_variable_set(self, mocker, mock_response, session_utils_object):
        """
        Test the case when no environment variable is set.

        Args:
            mocker (MockerFixture): The mocker fixture used to mock functions and objects.
            mock_response (MagicMock): The mock response object used to simulate API responses.
            session_utils_object (SessionUtils): The SessionUtils object under test.

        Returns:
            None

        Asserts:
            - The result of the _get_omam_ca_env() method is None.
        """
        mocker.patch(MODULE_UTIL_PATH + INVOKE_REQUEST,
                     return_value=mock_response)
        result = session_utils_object._get_omam_ca_env()
        assert result is None
