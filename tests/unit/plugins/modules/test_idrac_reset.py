# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.2.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest
from urllib.error import URLError
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_reset
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from mock import MagicMock

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_reset.'
MODULE_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.'


MANAGERS_URI = "/redfish/v1/Managers"
REDFISH = "/redfish/v1"
OEM = "Oem"
MANUFACTURER = "Dell"
LC_SERVICE = "DellLCService"
ACTIONS = "Actions"
GETREMOTELCSTATUS = "#DellLCService.GetRemoteServicesAPIStatus"
RESET_TO_DEFAULT_KEY = "#DellManager.ResetToDefaults"
RESTART_KEY = "#Manager.Reset"
GET_BASE_URI_KEY = "Validation.get_base_uri"
INVOKE_REQ_KEY = "iDRACRedfishAPI.invoke_request"
GET_CUSTOM_DEFAULT_KEY = "CustomDefaultsDownloadURI"
SET_CUSTOM_DEFAULT_KEY = "#DellManager.SetCustomDefaults"
IDRAC_RESET_RETRIES = 10
RESET_ALLOWABLE_KEY = "ResetType@Redfish.AllowableValues"
LC_STATUS_CHECK_SLEEP = 30
IDRAC_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"
IDRAC_JOB_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/{job_id}"
RESET_TO_DEFAULT_ERROR = "{reset_to_default} is not supported. The supported values are {supported_values}. \
                        Enter the valid values and retry the operation."
IDRAC_RESET_RESTART_SUCCESS_MSG = "iDRAC restart operation completed successfully."
IDRAC_RESET_SUCCESS_MSG = "Successfully performed iDRAC reset."
IDRAC_RESET_RESET_TRIGGER_MSG = "iDRAC reset operation triggered successfully."
IDRAC_RESET_RESTART_TRIGGER_MSG = "iDRAC restart operation triggered successfully."
INVALID_DIRECTORY_MSG = "Provided directory path '{path}' is invalid."
FAILED_RESET_MSG = "Failed to perform the reset operation."
RESET_UNTRACK = "iDRAC reset is in progress. Changes will apply once the iDRAC reset operation is susccessfully completed."
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The value of `job_wait_timeout` parameter cannot be negative or zero. Enter the valid value and retry the operation."
INVALID_FILE_MSG = "File extension is invalid. Supported extension for 'custom_default_file' is: .xml."
LC_STATUS_MSG = "LC status check is {lc_status} after {retries} number of retries, Exiting.."
INSUFFICIENT_DIRECTORY_PERMISSION_MSG = "Provided directory path '{path}' is not writable. " \
                                        "Please check if the directory has appropriate permissions."
UNSUPPORTED_LC_STATUS_MSG = "LC status check is not supported."
CHANGES_NOT_FOUND = "No changes found to commit!"
CHANGES_FOUND = "Changes found to commit!"
ODATA_ID = "@odata.id"
ODATA_REGEX = "(.*?)@odata"
ATTRIBUTE = "</Attribute>"
SUCCESS_STATUS = "Success"
FAILED_STATUS = "Failed"
RESET_KEY = "Oem.#DellManager.ResetToDefaults"


class TestStorageValidation(FakeAnsibleModule):
    module = idrac_reset

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
        # Secnario - when validate_and_get_first_resource_id_uri return proper uri
        mocker.patch(MODULE_PATH + "validate_and_get_first_resource_id_uri",
                     return_value=(IDRAC_URI, ''))
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idr_obj = self.module.Validation(
            idrac_connection_reset_mock, f_module)
        data = idr_obj.get_base_uri()
        assert data == IDRAC_URI

    def test_validate_job_wait_negative_values(self, idrac_default_args, idrac_connection_reset_mock, mocker):
        # Scenario - when job_wait_timeout is negative
        mocker.patch(MODULE_PATH + 'Validation.get_base_uri',
                     return_value=IDRAC_URI)
        idrac_default_args.update({"wait_for_idrac": True, "job_wait_timeout": -120})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.Validation(idrac_connection_reset_mock, f_module)
        with pytest.raises(Exception) as exc:
            idr_obj.validate_job_timeout()
        assert exc.value.args[0] == TIMEOUT_NEGATIVE_OR_ZERO_MSG

        # Scenario - when job_wait_timeout is positive
        idrac_default_args.update({"job_wait": True, "job_wait_timeout": 120})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        idr_obj = self.module.Validation(idrac_connection_reset_mock, f_module)
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

    def test_execute(self, idrac_default_args, idrac_connection_reset_mock, mocker):
        # Scenario: when success message is returned for graceful restart for IDRAC8 or IDRAC9
        obj = MagicMock()
        obj.status_code = 204
        obj.json_data = self.lc_status_invoke

        def mock_get_dynamic_uri_request(*args, **kwargs):
            if len(args) > 2 and args[2] == 'Links':
                return self.lc_status_api_links
            elif len(args) > 2 and args[2] == 'Actions':
                return self.action_api_resp_restart
            return self.action_api_resp
        allowed_values = ["All", "Default", "ResetAllWithRootDefaults"]
        mocker.patch(MODULE_PATH + "FactoryReset.is_check_idrac_latest", return_value=True)
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, return_value=obj)
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        reset_obj = self.module.FactoryReset(idrac_connection_reset_mock, f_module, allowed_choices=allowed_values)
        msg_resp, resp = reset_obj.execute()
        assert msg_resp['msg'] == IDRAC_RESET_SUCCESS_MSG

        # Scenario: when success message reset_to_default is passed as 'Default' for idrac9 with job_wait set to True
        obj2 = MagicMock()
        obj2.json_data = self.validate_allowed_values

        def mock_get_dynamic_uri_request(*args, **kwargs):
            if len(args) > 2 and args[2] == 'Links':
                return self.lc_status_api_links
            elif len(args) > 2 and args[2] == 'Actions':
                return self.action_api_resp_restart
            return self.action_api_resp
        allowed_values = ["All", "Default", "ResetAllWithRootDefaults"]
        mocker.patch(MODULE_PATH + "get_idrac_firmware_version", return_value="7.10.05")
        mocker.patch(MODULE_PATH + "FactoryReset.is_check_idrac_latest", return_value=True)
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, side_effect=[obj, obj2, obj])
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)
        idrac_default_args.update({"reset_to_default": "Default"})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        reset_obj = self.module.FactoryReset(idrac_connection_reset_mock, f_module, allowed_choices=allowed_values)
        msg_resp, resp = reset_obj.execute()
        assert msg_resp['msg'] == IDRAC_RESET_SUCCESS_MSG

        # Scenario: when success message reset_to_default is passed as 'CustomDefaults' with custom_default_buffer set
        obj3 = MagicMock()
        obj3.json_data = {'LCStatus': 'NOTINITIALIZED'}
        obj2.headers = {'Location': "/joburl/JID12345"}
        obj2.status_code = 200
        allowed_values = ["All", "Default", "ResetAllWithRootDefaults"]
        job_resp_completed = {'JobStatus': 'Completed'}
        idrac_redfish_resp = (False, 'Job Success', job_resp_completed, 1200)
        mocker.patch(MODULE_PATH + "get_idrac_firmware_version", return_value="7.10.05")
        mocker.patch(MODULE_PATH + GET_BASE_URI_KEY, return_value=IDRAC_URI)
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, side_effect=[obj, obj2, obj, obj2, obj, obj3,
                                                                URLError('URL error occurred'), obj])
        mocker.patch(MODULE_PATH + 'idrac_redfish_job_tracking', return_value=idrac_redfish_resp)
        mocker.patch(MODULE_PATH + "get_dynamic_uri",
                     side_effect=[self.lc_status_api_links, self.action_api_resp_restart,
                                  self.validate_allowed_values, self.validate_allowed_values,
                                  self.validate_allowed_values])
        idrac_default_args.update({"reset_to_default": "CustomDefaults", "custom_defaults_buffer": self.custom_default_content})
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        reset_obj = self.module.FactoryReset(idrac_connection_reset_mock, f_module, allowed_choices=allowed_values)
        msg_resp, resp = reset_obj.execute()
        assert msg_resp['msg'] == IDRAC_RESET_SUCCESS_MSG
