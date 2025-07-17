# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.3
# Copyright (C) 2020-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json
import pytest
import uuid
from io import StringIO
from ansible.module_utils._text import to_text
from urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_reset
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from unittest.mock import MagicMock

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_reset.'
MODULE_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.'

MANAGERS_URI = "/redfish/v1/Managers"
OEM = "Oem"
MANUFACTURER = "Dell"
ACTIONS = "Actions"
IDRAC_RESET_RETRIES = 50
LC_STATUS_CHECK_SLEEP = 30
IDRAC_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"
IDRAC_JOB_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/{job_id}"
RESET_TO_DEFAULT_ERROR = "{reset_to_default} is not supported. The supported values are {supported_values}. Enter the valid values and retry the operation."
RESET_TO_DEFAULT_ERROR_MSG = "{reset_to_default} is not supported."
CUSTOM_ERROR = "{reset_to_default} is not supported on this firmware version of iDRAC. The supported values are {supported_values}. \
Enter the valid values and retry the operation."
IDRAC_RESET_RESTART_SUCCESS_MSG = "iDRAC restart operation completed successfully."
IDRAC_RESET_SUCCESS_MSG = "Successfully performed iDRAC reset."
IDRAC_RESET_RESET_TRIGGER_MSG = "iDRAC reset operation triggered successfully."
IDRAC_RESET_RESTART_TRIGGER_MSG = "iDRAC restart operation triggered successfully."
INVALID_DIRECTORY_MSG = "Provided directory path '{path}' is invalid."
FAILED_RESET_MSG = "Failed to perform the reset operation."
RESET_UNTRACK = "iDRAC reset is in progress. Changes will apply once the iDRAC reset operation is successfully completed."
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The value of `job_wait_timeout` parameter cannot be negative or zero. Enter the valid value and retry the operation."
INVALID_FILE_MSG = "File extension is invalid. Supported extension for 'custom_default_file' is: .xml."
LC_STATUS_MSG = "Lifecycle controller status check is {lc_status} after {retries} number of retries, Exiting.."
LC_LOGIN_ERR_MSG = "Login failed after the iDRAC reset. \
Either the iDRAC is taking longer than expected time to come online \
or the iDRAC credentials are invalid."
INSUFFICIENT_DIRECTORY_PERMISSION_MSG = "Provided directory path '{path}' is not writable. Please check if the directory has appropriate permissions."
UNSUPPORTED_LC_STATUS_MSG = "Lifecycle controller status check is not supported."
CHANGES_NOT_FOUND = "No changes found to commit!"
CHANGES_FOUND = "Changes found to commit!"
MINIMUM_SUPPORTED_FIRMWARE_VERSION = "7.00.00"
SUCCESS_STATUS = "Success"
FAILED_STATUS = "Failed"
STATUS_SUCCESS = [200, 202, 204]
ERR_STATUS_CODE = [400, 404]
RESET_KEY = "Oem.#DellManager.ResetToDefaults"
RESTART_KEY = "#Manager.Reset"
SLEEP_KEY = "time.sleep"
GET_SERVER_VERSION_KEY = "_get_server_version"
GET_BASE_URI_KEY = "Validation.get_base_uri"
INVOKE_REQ_KEY = "iDRACRedfishAPI.invoke_request"
GET_CUSTOM_DEFAULT_KEY = "CustomDefaultsDownloadURI"
SET_CUSTOM_DEFAULT_KEY = "#DellManager.SetCustomDefaults"
CHECK_LC_STATUS = "FactoryReset.check_lcstatus"
RESET_ALLOWABLE_KEY = "ResetType@Redfish.AllowableValues"
VALIDATE_RESET_OPTION_KEY = "Validation.validate_reset_options"
FILE_PATH = "/root/custom_default_content.xml"
EXECUTE_KEY = "FactoryReset.execute"
HTTP_ERROR_MSG = "http error message"
RETURN_TYPE = "application/json"
FILE_PATH = "abc/test"


class TestValidation(FakeAnsibleModule):
    module = idrac_reset
    allowed_values = ["All", "Default", "CustomDefaults", "ResetAllWithRootDefaults"]
    allowed_values_api = {
        'Actions':
        {
            "#Manager.Reset": {
                "ResetType@Redfish.AllowableValues": [
                    "Test"
                ]
            },
            "Oem": {
                "#DellManager.ResetToDefaults": {
                    RESET_ALLOWABLE_KEY: [
                        "All",
                        "Default",
                        "ResetAllWithRootDefaults"
                    ]
                }
            }
        },
        "Oem": {
            "Dell": {
                "CustomDefaultsDownloadURI": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/CustomDefaultsDownloadURI"
            }
        }
    }

    @pytest.fixture
    def idrac_reset_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_reset_mock(self, mocker, idrac_reset_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_reset_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_reset_mock
        return idrac_conn_mock

    def test_get_base_uri(self, idrac_default_args, idrac_connection_reset_mock, mocker):
        # Scenario - when validate_and_get_first_resource_id_uri return proper uri
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(IDRAC_URI, ''))
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.Validation(
            idrac_connection_reset_mock, f_module, 16)
        data = idr_obj.get_base_uri()
        assert data == IDRAC_URI

    def test_validate_reset_options(self, idrac_default_args, idrac_connection_reset_mock, mocker):
        # Scenario - when key 'OEM' doesn't exist in output from invoke_request
        obj = MagicMock()
        obj.json_data = {'Actions': {}}
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, return_value=obj)
        # mocker.patch(MODULE_PATH + GET_IDRAC_MODEL_VERSION, return_value=11)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idrac_default_args.update({"reset_to_default": 'All'})
        idr_obj = self.module.Validation(
            idrac_connection_reset_mock, f_module, 11)
        res = idr_obj.validate_reset_options(RESET_KEY)[1]
        assert res is False

        # Scenario - when reset_to_default is not in allowable values
        obj.json_data = self.allowed_values_api
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idrac_default_args.update({"reset_to_default": 'CustomDefaults'})
        idr_obj = self.module.Validation(
            idrac_connection_reset_mock, f_module, 11)
        res = idr_obj.validate_reset_options(RESET_KEY)[1]
        assert res is False

        # Scenario - when reset_to_default is CustomDefaults in 17G
        obj.json_data = self.allowed_values_api
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idrac_default_args.update({"reset_to_default": 'CustomDefaults'})
        idr_obj = self.module.Validation(
            idrac_connection_reset_mock, f_module, 17)
        res = idr_obj.validate_reset_options(RESET_KEY)[1]
        assert res is True

    def test_validate_graceful_restart_option(self, idrac_default_args, idrac_connection_reset_mock, mocker):
        # Scenario - when key doesn't exist in output from invoke_request
        obj = MagicMock()
        obj.json_data = {'Actions': {}}
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.Validation(
            idrac_connection_reset_mock, f_module, 16)
        res = idr_obj.validate_graceful_restart_option(RESTART_KEY)
        assert res is False

        # Scenario - when 'GracefulRestart is not in allowable values
        obj.json_data = self.allowed_values_api
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, return_value=obj)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.Validation(
            idrac_connection_reset_mock, f_module, 16)
        res = idr_obj.validate_graceful_restart_option(RESTART_KEY)
        assert res is False

    def test_validate_path(self, idrac_default_args, idrac_connection_reset_mock, mocker):
        # Scenario - when custom default file path doesn't exist
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + 'os.path.exists', return_value=False)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.Validation(
            idrac_connection_reset_mock, f_module, 16)
        with pytest.raises(Exception) as exc:
            idr_obj.validate_path(FILE_PATH)
        assert exc.value.args[0] == INVALID_DIRECTORY_MSG.format(path=FILE_PATH)

        # Scenario - when custom default file path exist but not accessible
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + 'os.path.exists', return_value=True)
        mocker.patch(MODULE_PATH + 'os.access', return_value=False)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.Validation(
            idrac_connection_reset_mock, f_module, 16)
        with pytest.raises(Exception) as exc:
            idr_obj.validate_path(FILE_PATH)
        assert exc.value.args[0] == INSUFFICIENT_DIRECTORY_PERMISSION_MSG.format(path=FILE_PATH)

    def test_validate_file_format(self, idrac_default_args, idrac_connection_reset_mock, mocker):
        # Scenario - when custom default file is not in XML format
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.Validation(
            idrac_connection_reset_mock, f_module, 16)
        with pytest.raises(Exception) as exc:
            idr_obj.validate_file_format('abc/test.json')
        assert exc.value.args[0] == INVALID_FILE_MSG

    def test_validate_custom_option_exception_case(self, idrac_default_args, idrac_connection_reset_mock, mocker):
        obj = MagicMock()
        obj.json_data = self.allowed_values_api
        json_str = to_text(json.dumps({"data": "out"}))
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + 'get_dynamic_uri', return_value=obj)
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, side_effect=HTTPError("https://test.com", 404, HTTP_ERROR_MSG,
                                                                         {"accept-type": RETURN_TYPE},
                                                                         StringIO(json_str)))
        idrac_default_args.update({"reset_to_default": 'CustomDefaults'})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.Validation(
            idrac_connection_reset_mock, f_module, 16)
        with pytest.raises(Exception) as exc:
            idr_obj.validate_custom_option('CustomDefaults', self.allowed_values)
        assert exc.value.args[0] == RESET_TO_DEFAULT_ERROR.format(reset_to_default='CustomDefaults', supported_values=self.allowed_values)

    def test_validate_job_wait_negative_values(self, idrac_default_args, idrac_connection_reset_mock, mocker):
        # Scenario - when job_wait_timeout is negative
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY,
                     return_value=IDRAC_URI)
        idrac_default_args.update({"wait_for_idrac": True, "job_wait_timeout": -120})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.Validation(idrac_connection_reset_mock, f_module, 16)
        with pytest.raises(Exception) as exc:
            idr_obj.validate_job_timeout()
        assert exc.value.args[0] == TIMEOUT_NEGATIVE_OR_ZERO_MSG

        # Scenario - when job_wait_timeout is positive
        idrac_default_args.update({"job_wait": True, "job_wait_timeout": 120})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.Validation(idrac_connection_reset_mock, f_module, 16)
        idr_obj.validate_job_timeout()


class TestFactoryReset(FakeAnsibleModule):
    module = idrac_reset
    lc_status_api_links = {
        "Oem": {
            "Dell": {
                "DellLCService": {
                    "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellLCService"
                }
            }
        }
    }

    action_api_resp = {
        "Actions": {
            "#DellLCService.GetRemoteServicesAPIStatus": {
                "target": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellLCService/Actions/DellLCService.GetRemoteServicesAPIStatus"
            }
        }
    }

    action_api_resp_restart = {
        RESTART_KEY: {
            RESET_ALLOWABLE_KEY: [
                "GracefulRestart"
            ],
            "target": "/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Manager.Reset"
        }
    }

    lc_status_invoke = {
        "LCStatus": "Ready"
    }
    lc_status_invoke_not_ready = {
        "LCStatus": "Not Initialized"
    }

    validate_allowed_values = {
        "Actions": {
            RESTART_KEY: {
                RESET_ALLOWABLE_KEY: [
                    "GracefulRestart"
                ],
                "target": "/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Manager.Reset"
            },
            "#Manager.ResetToDefaults": {
                RESET_ALLOWABLE_KEY: [
                    "ResetAll",
                    "PreserveNetworkAndUsers"
                ],
                "target": "/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Manager.ResetToDefaults"
            },
            "Oem": {
                "#DellManager.ResetToDefaults": {
                    RESET_ALLOWABLE_KEY: [
                        "All",
                        "CustomDefaults",
                        "Default",
                        "ResetAllWithRootDefaults"
                    ],
                    "target": "/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/DellManager.ResetToDefaults"
                },
                "#DellManager.SetCustomDefaults": {
                    "target": "/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/DellManager.SetCustomDefaults"
                },
            }
        },
        "Oem": {
            "Dell": {
                "CustomDefaultsDownloadURI": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/CustomDefaultsDownloadURI"
            }
        }
    }

    custom_default_content = "<SystemConfiguration Model=\"PowerEdge R7525\" ServiceTag=\"2V4TK93\">\n<Component FQDD=\"iDRAC.Embedded.1\">\n \
    <Attribute Name=\"IPMILan.1#Enable\">Disabled</Attribute>\n </Component>\n\n</SystemConfiguration>"

    @pytest.fixture
    def idrac_reset_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_reset_mock(self, mocker, idrac_reset_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_reset_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_reset_mock
        return idrac_conn_mock

    def test_custom_defaults_supported(self, idrac_default_args, idrac_connection_reset_mock, mocker):
        allowed_values = ["All", "Default", "ResetAllWithRootDefaults"]
        mocker.patch(MODULE_PATH + GET_SERVER_VERSION_KEY, return_value=[16, "7.10.05"])
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        reset_obj = self.module.FactoryReset(idrac_connection_reset_mock, f_module, allowed_choices=allowed_values)
        res = reset_obj.custom_defaults_supported()
        assert res is True

    def test_check_mode_output(self, idrac_default_args, idrac_connection_reset_mock, mocker):
        # Scenario - When Reset to default is not passed and check mode is true
        allowed_values = ["All", "Default", "ResetAllWithRootDefaults"]
        mocker.patch(MODULE_PATH + GET_SERVER_VERSION_KEY, return_value=[16, "7.10.05"])
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + "Validation.validate_graceful_restart_option", return_value=False)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        reset_obj = self.module.FactoryReset(idrac_connection_reset_mock, f_module, allowed_choices=allowed_values)
        with pytest.raises(Exception) as exc:
            reset_obj.check_mode_output()
        assert exc.value.args[0] == CHANGES_NOT_FOUND

    def test_check_lcstatus(self, idrac_default_args, idrac_connection_reset_mock, mocker):
        allowed_values = ["All", "Default", "ResetAllWithRootDefaults", "CustomDefaults"]

        def mock_get_dynamic_uri_request(*args, **kwargs):
            if len(args) > 2 and args[2] == 'Links':
                return {"Oem": {"Dell": {"DellLCService": {}}}}
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(IDRAC_URI, ''))
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)
        # Scenario: When default_username and default_password is not given
        idrac_default_args.update({"reset_to_default": 'All'})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        reset_obj = self.module.FactoryReset(idrac_connection_reset_mock, f_module, allowed_choices=allowed_values)
        data = reset_obj.check_lcstatus()
        assert data is None

        # Scneario: When default_username and default_password is given
        idrac_default_args.update({"reset_to_default": 'All',
                                   "default_username": "admin",
                                   "default_password": str(uuid.uuid4())})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        reset_obj = self.module.FactoryReset(idrac_connection_reset_mock, f_module, allowed_choices=allowed_values)
        mocker.patch(MODULE_PATH + SLEEP_KEY, side_effect=lambda *args, **kwargs: None)
        with pytest.raises(Exception) as exc:
            reset_obj.check_lcstatus()
        assert exc.value.args[0] == UNSUPPORTED_LC_STATUS_MSG

        # Scenario: When wrong default_username and default_password is given
        idrac_default_args.update({"reset_to_default": 'All',
                                   "default_username": "admin",
                                   "default_password": str(uuid.uuid4())})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        reset_obj = self.module.FactoryReset(idrac_connection_reset_mock, f_module, allowed_choices=allowed_values)

        mocker.patch(MODULE_PATH + "wait_after_idrac_reset", return_value=(True, ""))
        mocker.patch(MODULE_PATH + SLEEP_KEY, side_effect=lambda *args, **kwargs: None)
        with pytest.raises(Exception) as exc:
            reset_obj.check_lcstatus()
        assert exc.value.args[0] == LC_LOGIN_ERR_MSG

        # Scenario: When LC status service fails during _check_lcstatus_with_url
        api_mock = MagicMock(**{'invoke_request.side_effect': URLError("urlopen error")})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        reset_obj = self.module.FactoryReset(api_mock, f_module, allowed_choices=allowed_values)
        mocker.patch(MODULE_PATH + SLEEP_KEY, side_effect=lambda *args, **kwargs: None)
        with pytest.raises(Exception) as exc:
            reset_obj._check_lc_status_with_url(lc_url="")
        assert exc.value.args[0] == LC_STATUS_MSG.format(lc_status='unreachable', retries=IDRAC_RESET_RETRIES)

        # Scenario: When LC status never moves to ready state
        api_mock = MagicMock(**{'invoke_request.return_value.json_data': self.lc_status_invoke_not_ready})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        reset_obj = self.module.FactoryReset(api_mock, f_module, allowed_choices=allowed_values)
        mocker.patch(MODULE_PATH + SLEEP_KEY, side_effect=lambda *args, **kwargs: None)
        with pytest.raises(Exception) as exc:
            reset_obj._check_lc_status_with_url(lc_url="")
        assert exc.value.args[0] == LC_STATUS_MSG.format(
            lc_status=self.lc_status_invoke_not_ready['LCStatus'],
            retries=IDRAC_RESET_RETRIES,
        )

    def test_execute(self, idrac_default_args, idrac_connection_reset_mock, mocker):
        allowed_values = ["All", "Default", "ResetAllWithRootDefaults", "CustomDefaults"]
        allowed_values_without_cd = ["All", "Default", "ResetAllWithRootDefaults"]
        # Scenario - When 'GracefulRestart' is not supported and check_mode True
        mocker.patch(MODULE_PATH + GET_SERVER_VERSION_KEY, return_value=[13, "2.81.81"])
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + "Validation.validate_graceful_restart_option", return_value=False)
        idrac_default_args.update({})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        reset_obj = self.module.FactoryReset(idrac_connection_reset_mock, f_module, allowed_choices=allowed_values)
        with pytest.raises(Exception) as exc:
            reset_obj.execute()
        assert exc.value.args[0] == CHANGES_NOT_FOUND

        # Scenario: when success message is returned for graceful restart
        obj = MagicMock()
        obj.status_code = 204
        obj.json_data = self.lc_status_invoke

        def mock_get_dynamic_uri_request(*args, **kwargs):
            if len(args) > 2 and args[2] == 'Links':
                return self.lc_status_api_links
            elif len(args) > 2 and args[2] == 'Actions':
                return self.action_api_resp_restart
            return self.action_api_resp
        mocker.patch(MODULE_PATH + GET_SERVER_VERSION_KEY, return_value=[16, "7.10.05"])
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + SLEEP_KEY, side_effect=lambda *args, **kwargs: None)
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, return_value=obj)
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        reset_obj = self.module.FactoryReset(idrac_connection_reset_mock, f_module, allowed_choices=allowed_values)
        msg_resp, resp = reset_obj.execute()
        assert msg_resp['msg'] == IDRAC_RESET_SUCCESS_MSG

        # Scenario: when success message reset_to_default is passed as 'Default' with job_wait set to True
        obj.status_code = 200
        obj2 = MagicMock()
        obj3 = MagicMock()
        obj2.json_data = self.validate_allowed_values
        obj3.json_data = self.lc_status_invoke_not_ready

        def mock_get_dynamic_uri_request(*args, **kwargs):
            if len(args) > 2 and args[2] == 'Links':
                return self.lc_status_api_links
            elif len(args) > 2 and args[2] == 'Actions':
                return self.validate_allowed_values
            return self.action_api_resp
        mocker.patch(MODULE_PATH + GET_SERVER_VERSION_KEY, return_value=[16, "7.10.05"])
        mocker.patch(MODULE_PATH + SLEEP_KEY, side_effect=lambda *args, **kwargs: None)
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, side_effect=[obj, obj2, obj, URLError('URL error occurred'), obj, URLError('URL error occurred'), obj3, obj])
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)
        idrac_default_args.update({"reset_to_default": "Default"})
        idrac_default_args.update({"wait_for_idrac": True})
        idrac_default_args.update({"job_wait_timeout": 300})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        reset_obj = self.module.FactoryReset(idrac_connection_reset_mock, f_module, allowed_choices=allowed_values)
        msg_resp, resp = reset_obj.execute()
        assert msg_resp['msg'] == IDRAC_RESET_SUCCESS_MSG

        # Scenario: when success message reset_to_default is passed as 'CustomDefaults' with custom_default_buffer
        obj4 = MagicMock()
        obj4.json_data = {'LCStatus': 'NOTINITIALIZED'}
        obj2.headers = {'Location': "/joburl/JID12345"}
        obj2.status_code = 200
        # allowed_values.append("CustomDefaults")
        job_resp_completed = {'JobStatus': 'Completed'}
        idrac_redfish_resp = (False, 'Job Success', job_resp_completed, 1200)
        mocker.patch(MODULE_PATH + GET_SERVER_VERSION_KEY, return_value=[16, "7.10.05"])
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + VALIDATE_RESET_OPTION_KEY, side_effect=[(allowed_values, True), (allowed_values, True)])
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, side_effect=[obj, obj2, obj, obj2])
        mocker.patch(MODULE_PATH + SLEEP_KEY, side_effect=lambda *args, **kwargs: None)
        mocker.patch(MODULE_PATH + 'idrac_redfish_job_tracking', return_value=idrac_redfish_resp)
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     side_effect=[self.lc_status_api_links, self.action_api_resp_restart,
                                  self.validate_allowed_values, self.validate_allowed_values,
                                  self.validate_allowed_values, self.lc_status_api_links, self.action_api_resp_restart])
        idrac_default_args.update({"reset_to_default": "CustomDefaults", "custom_defaults_buffer": self.custom_default_content})
        idrac_default_args.update({"wait_for_idrac": False})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        reset_obj = self.module.FactoryReset(idrac_connection_reset_mock, f_module, allowed_choices=allowed_values)
        msg_resp, resp = reset_obj.execute()
        assert msg_resp['msg'] == IDRAC_RESET_RESET_TRIGGER_MSG

        # Scenario - When reset_to_default is CustomDefaults and iDRAC9 firmware version not supported
        mocker.patch(MODULE_PATH + GET_SERVER_VERSION_KEY, return_value=[16, "6.99.99"])
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + VALIDATE_RESET_OPTION_KEY, return_value=(allowed_values_without_cd, True))
        mocker.patch(MODULE_PATH + CHECK_LC_STATUS, return_value=None)
        # mocker.patch(MODULE_PATH + CHECK_IDRAC_VERSION, return_value=False)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        reset_obj = self.module.FactoryReset(idrac_connection_reset_mock, f_module, allowed_choices=allowed_values)
        with pytest.raises(Exception) as exc:
            reset_obj.execute()
        assert exc.value.args[0] == CUSTOM_ERROR.format(reset_to_default="CustomDefaults",
                                                        supported_values=allowed_values_without_cd)

        # Scenario - When reset_to_default is passed and iDRAC9 and check_mode True
        mocker.patch(MODULE_PATH + GET_SERVER_VERSION_KEY, return_value=[16, "7.10.05"])
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + VALIDATE_RESET_OPTION_KEY, return_value=(allowed_values, False))
        idrac_default_args.update({"reset_to_default": "CustomDefaults", "custom_defaults_buffer": self.custom_default_content})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        reset_obj = self.module.FactoryReset(idrac_connection_reset_mock, f_module, allowed_choices=allowed_values)
        with pytest.raises(Exception) as exc:
            reset_obj.execute()
        assert exc.value.args[0] == CHANGES_FOUND

        # Scenario - When reset_to_default is passed and iDRAC9 with firmware version not supported and check_mode True
        mocker.patch(MODULE_PATH + GET_SERVER_VERSION_KEY, return_value=[16, "6.81.81"])
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        idrac_default_args.update({"reset_to_default": "CustomDefaults", "custom_defaults_buffer": self.custom_default_content})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=True)
        reset_obj = self.module.FactoryReset(idrac_connection_reset_mock, f_module, allowed_choices=allowed_values)
        with pytest.raises(Exception) as exc:
            reset_obj.execute()
        assert exc.value.args[0] == CHANGES_NOT_FOUND

        # Scenario - When reset_to_default is 'CustomDefaults' and iDRAC9 and custom_defaults_file is passed
        json_str = to_text(json.dumps({"data": "out"}))
        mocker.patch(MODULE_PATH + GET_SERVER_VERSION_KEY, return_value=[16, "7.10.05"])
        mocker.patch(MODULE_PATH + CHECK_LC_STATUS, return_value=None)
        mocker.patch(MODULE_PATH + SLEEP_KEY, side_effect=lambda *args, **kwargs: None)
        mocker.patch(MODULE_PATH + "Validation.validate_path", return_value=None)
        mocker.patch(MODULE_PATH + "Validation.validate_file_format", return_value=None)
        mocker.patch(MODULE_PATH + "Validation.validate_custom_option", return_value=None)
        mocker.patch(MODULE_PATH + 'open', mocker.mock_open(read_data=self.custom_default_content))
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + VALIDATE_RESET_OPTION_KEY, side_effect=[(allowed_values, True), (allowed_values, True)])
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, side_effect=[obj2, obj, HTTPError("https://test.com",
                                                                                     401, HTTP_ERROR_MSG, {"accept-type": RETURN_TYPE},
                                                                                     StringIO(json_str))])
        mocker.patch(MODULE_PATH + 'idrac_redfish_job_tracking', return_value=idrac_redfish_resp)
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     side_effect=[self.validate_allowed_values, self.validate_allowed_values,
                                  self.validate_allowed_values, self.lc_status_api_links, self.action_api_resp_restart])
        idrac_default_args.update({"reset_to_default": "CustomDefaults", "custom_defaults_file": FILE_PATH})
        idrac_default_args.update({"wait_for_idrac": True})
        idrac_default_args.update({"job_wait_timeout": 300})
        idrac_default_args.update({"force_reset": True})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        reset_obj = self.module.FactoryReset(idrac_connection_reset_mock, f_module, allowed_choices=allowed_values)
        msg_resp, resp = reset_obj.execute()
        assert msg_resp['msg'] == IDRAC_RESET_SUCCESS_MSG

        # Scenario: Failure - when reset_to_default is passed as 'ResetAllWithRootDefaults' for idrac9 with job_wait set to True
        def mock_get_dynamic_uri_request(*args, **kwargs):
            if len(args) > 2 and args[2] == 'Links':
                return self.lc_status_api_links
            elif len(args) > 2 and args[2] == 'Actions':
                return self.validate_allowed_values
            return self.action_api_resp
        obj.status_code = 400
        mocker.patch(MODULE_PATH + GET_SERVER_VERSION_KEY, return_value=[16, "7.10.05"])
        mocker.patch(MODULE_PATH + CHECK_LC_STATUS, return_value=None)
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + VALIDATE_RESET_OPTION_KEY, return_value=(allowed_values, True))
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, side_effect=[obj])
        mocker.patch(MODULE_PATH + SLEEP_KEY, side_effect=lambda *args, **kwargs: None)
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)
        idrac_default_args.update({"reset_to_default": "ResetAllWithRootDefaults"})
        idrac_default_args.update({"wait_for_idrac": False})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        reset_obj = self.module.FactoryReset(idrac_connection_reset_mock, f_module, allowed_choices=allowed_values)
        msg_resp, resp = reset_obj.execute()
        assert msg_resp['msg'] == FAILED_RESET_MSG

    def test_idrac_reset_main_positive_case(self, idrac_default_args,
                                            idrac_connection_reset_mock, mocker):
        # Scenario - When reset_to_default is passed and successful
        msg_resp = {'msg': "Success", 'changed': True}
        mocker.patch(MODULE_PATH + GET_SERVER_VERSION_KEY, return_value=[16, "7.10.05"])
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + EXECUTE_KEY, return_value=(msg_resp, {}))
        data = self._run_module(idrac_default_args)
        assert data['msg'] == "Success"

        # Scenario - When reset_to_default is passed and Failed
        msg_resp = {'msg': "Failure", 'changed': False}
        mocker.patch(MODULE_PATH + GET_SERVER_VERSION_KEY, return_value=[16, "7.10.05"])
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + EXECUTE_KEY, return_value=(msg_resp, {}))
        data = self._run_module(idrac_default_args)
        assert data['msg'] == "Failure" and data['failed'] is True

        # Scenario - When reset_to_default is None and successful
        msg_resp = {'msg': "Success", 'changed': True}
        output = {
            "reset_status": {
                "idracreset": {
                    "Data": {
                        "StatusCode": 204
                    },
                    "Message": "Success",
                    "Status": "Success",
                    "StatusCode": 204,
                    "retval": True
                }
            }
        }
        mocker.patch(MODULE_PATH + GET_SERVER_VERSION_KEY, return_value=[16, "7.10.05"])
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + EXECUTE_KEY, return_value=(msg_resp, output))
        data = self._run_module(idrac_default_args)
        assert data['msg'] == "Success" and data['reset_status'] == output

        # Scenario - When reset_to_default is None and Failed
        output['reset_status']['idracreset']['Message'] = "Failure"
        output['reset_status']['idracreset']['Status'] = "Failure"
        output['reset_status']['idracreset']['StatusCode'] = 404
        msg_resp = {'msg': "Failure", 'changed': False}
        mocker.patch(MODULE_PATH + GET_SERVER_VERSION_KEY, return_value=[16, "7.10.05"])
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + EXECUTE_KEY, return_value=(msg_resp, output))
        data = self._run_module(idrac_default_args)
        assert data['msg'] == "Failure" and data['reset_status'] == output

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_idrac_reset_main_exception_handling_case(self, exc_type, idrac_default_args,
                                                      idrac_connection_reset_mock, mocker):
        json_str = to_text(json.dumps({"data": "out"}))
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        if exc_type in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + EXECUTE_KEY,
                         side_effect=exc_type('https://testhost.com', 400,
                                              HTTP_ERROR_MSG,
                                              {"accept-type": RETURN_TYPE},
                                              StringIO(json_str)))
        else:
            mocker.patch(MODULE_PATH + GET_SERVER_VERSION_KEY,
                         side_effect=exc_type('test'))
        result = self._run_module(idrac_default_args)
        if exc_type == URLError:
            assert result['unreachable'] is True
        else:
            assert result['failed'] is True
        assert 'msg' in result
