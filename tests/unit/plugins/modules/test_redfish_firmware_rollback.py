# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.2.0
# Copyright (C) 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import redfish_firmware_rollback
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from unittest.mock import MagicMock
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
ACCESS_TYPE = "application/json"
HTTP_ERROR_MSG = 'http error message'
HTTPS_ADDRESS = 'https://testhost.com'


@pytest.fixture
def redfish_connection_mock(mocker, redfish_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'redfish_firmware_rollback.Redfish')
    redfish_connection_obj = connection_class_mock.return_value.__enter__.return_value
    redfish_connection_obj.invoke_request.return_value = redfish_response_mock
    return redfish_connection_obj


class TestRedfishFirmware(FakeAnsibleModule):

    module = redfish_firmware_rollback

    @pytest.mark.parametrize("exc_type", [URLError, HTTPError, TypeError])
    def test_wait_for_redfish_idrac_reset_http(self, exc_type, redfish_connection_mock, redfish_response_mock,
                                               redfish_default_args, mocker):
        redfish_default_args.update({"name": "BIOS", "reboot": True, "reboot_timeout": 900})
        f_module = self.get_module_mock(params=redfish_default_args)
        mocker.patch(MODULE_PATH + 'redfish_firmware_rollback.time.sleep', return_value=None)
        mocker.patch(MODULE_PATH + 'redfish_firmware_rollback.Redfish', return_value=MagicMock())
        mocker.patch(MODULE_PATH + 'redfish_firmware_rollback.require_session', return_value=(1, "secret token"))
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type == HTTPError:
            redfish_connection_mock.invoke_request.side_effect = exc_type(
                HTTPS_ADDRESS, 401, HTTP_ERROR_MSG, {"accept-type": ACCESS_TYPE},
                StringIO(json_str)
            )
            result = self.module.wait_for_redfish_idrac_reset(f_module, redfish_connection_mock, 5)
            assert result[0] is False
            assert result[1] is True
            assert result[2] == "iDRAC reset is in progress. Until the iDRAC is reset, the changes would not apply."
            redfish_connection_mock.invoke_request.side_effect = exc_type(
                HTTPS_ADDRESS, 400, HTTP_ERROR_MSG, {"accept-type": ACCESS_TYPE},
                StringIO(json_str)
            )
            result = self.module.wait_for_redfish_idrac_reset(f_module, redfish_connection_mock, 5)
            assert result[0] is True
            assert result[1] is True
            assert result[2] == "iDRAC reset is in progress. Until the iDRAC is reset, the changes would not apply."
        elif exc_type == URLError:
            redfish_connection_mock.invoke_request.side_effect = exc_type("exception message")
            result = self.module.wait_for_redfish_idrac_reset(f_module, redfish_connection_mock, 5)
            assert result[0] is True
            assert result[1] is True
            assert result[2] == "iDRAC reset is in progress. Until the iDRAC is reset, the changes would not apply."
        else:
            redfish_connection_mock.invoke_request.side_effect = exc_type("exception message")
            result = self.module.wait_for_redfish_idrac_reset(f_module, redfish_connection_mock, 5)
            assert result[0] is True
            assert result[1] is True

    def test_wait_for_redfish_idrac_reset(self, redfish_connection_mock, redfish_response_mock,
                                          redfish_default_args, mocker):
        redfish_default_args.update({"name": "BIOS", "reboot": True, "reboot_timeout": 900})
        f_module = self.get_module_mock(params=redfish_default_args)
        mocker.patch(MODULE_PATH + 'redfish_firmware_rollback.time.sleep', return_value=None)
        result = self.module.wait_for_redfish_idrac_reset(f_module, redfish_connection_mock, 900)
        assert result[0] is False
        assert result[1] is False
        assert result[2] == "iDRAC has been reset successfully."

    def test_rollback_firmware(self, redfish_connection_mock, redfish_response_mock, redfish_default_args, mocker):
        redfish_default_args.update({"name": "BIOS", "reboot": True, "reboot_timeout": 900})
        mocker.patch(MODULE_PATH + "redfish_firmware_rollback.simple_update", return_value=["JID_12345678"])
        mocker.patch(MODULE_PATH + "redfish_firmware_rollback.wait_for_redfish_reboot_job",
                     return_value=({"Id": "JID_123456789"}, True, ""))
        job_resp_mock = MagicMock()
        job_resp_mock.json_data = {"JobState": "RebootFailed"}
        mocker.patch(MODULE_PATH + "redfish_firmware_rollback.wait_for_redfish_job_complete",
                     return_value=(job_resp_mock, ""))
        f_module = self.get_module_mock(params=redfish_default_args)
        preview_uri = ["/redfish/v1/Previous1.1"]
        reboot_uri = ["/redfish/v1/Previous.life_cycle.1.1"]
        update_uri = "/redfish/v1/SimpleUpdate"
        with pytest.raises(Exception) as ex:
            self.module.rollback_firmware(redfish_connection_mock, f_module, preview_uri, reboot_uri, update_uri)
        assert ex.value.args[0] == "Failed to reboot the server."
        mocker.patch(MODULE_PATH + "redfish_firmware_rollback.wait_for_redfish_job_complete",
                     return_value=(job_resp_mock, "Failed message."))
        with pytest.raises(Exception) as ex:
            self.module.rollback_firmware(redfish_connection_mock, f_module, preview_uri, reboot_uri, update_uri)
        assert ex.value.args[0] == "Task excited after waiting for 900 seconds. " \
                                   "Check console for firmware rollback status."
        mocker.patch(MODULE_PATH + "redfish_firmware_rollback.wait_for_redfish_reboot_job",
                     return_value=({}, False, "Reset operation is failed."))
        with pytest.raises(Exception) as ex:
            self.module.rollback_firmware(redfish_connection_mock, f_module, preview_uri, reboot_uri, update_uri)
        assert ex.value.args[0] == "Reset operation is failed."
        mocker.patch(MODULE_PATH + "redfish_firmware_rollback.get_job_status",
                     return_value=({"JobState": "Completed"}, False))
        mocker.patch(MODULE_PATH + "redfish_firmware_rollback.wait_for_redfish_reboot_job",
                     return_value=({"JobState": "Completed", "Id": "JID_123456789"}, True, ""))
        job_resp_mock.json_data = {"JobState": "RebootCompleted"}
        mocker.patch(MODULE_PATH + "redfish_firmware_rollback.wait_for_redfish_job_complete",
                     return_value=(job_resp_mock, ""))
        mocker.patch(MODULE_PATH + "redfish_firmware_rollback.simple_update", return_value=["JID_12345678"])
        mocker.patch(MODULE_PATH + "redfish_firmware_rollback.wait_for_redfish_idrac_reset",
                     return_value=(False, True, ""))
        mocker.patch(MODULE_PATH + "redfish_firmware_rollback.get_job_status",
                     return_value=([{"JobState": "Completed"}], 0))
        result = self.module.rollback_firmware(redfish_connection_mock, f_module, preview_uri, reboot_uri, update_uri)
        assert result[0] == [{'JobState': 'Completed'}, {'JobState': 'Completed'}]
        assert result[1] == 0

        redfish_default_args.update({"name": "BIOS", "reboot": False, "reboot_timeout": 900})
        f_module = self.get_module_mock(params=redfish_default_args)
        mocker.patch(MODULE_PATH + "redfish_firmware_rollback.get_job_status",
                     return_value=([{"JobState": "Scheduled"}], 0))
        result = self.module.rollback_firmware(redfish_connection_mock, f_module, preview_uri, [], update_uri)
        assert result[0] == [{"JobState": "Scheduled"}]
        assert result[1] == 0

    def test_main(self, redfish_connection_mock, redfish_response_mock, redfish_default_args, mocker):
        redfish_default_args.update({"reboot": True, "name": "BIOS"})
        mocker.patch(MODULE_PATH + "redfish_firmware_rollback.get_rollback_preview_target",
                     return_value=(["Previous/URI/1"], [], "/redfish/SimpleUpdate"))
        job_status = {"ActualRunningStartTime": "2023-08-07T05:09:08", "ActualRunningStopTime": "2023-08-07T05:12:41",
                      "CompletionTime": "2023-08-07T05:12:41", "Description": "Job Instance", "EndTime": "TIME_NA",
                      "Id": "JID_914026562845", "JobState": "Completed", "JobType": "FirmwareUpdate",
                      "Message": "Job completed successfully.", "MessageArgs": [], "MessageId": "PR19",
                      "Name": "Firmware Rollback: Network", "PercentComplete": 100, "StartTime": "2023-08-07T05:04:16",
                      "TargetSettingsURI": None}
        mocker.patch(MODULE_PATH + "redfish_firmware_rollback.rollback_firmware", return_value=(job_status, 0, False))
        result = self._run_module(redfish_default_args)
        assert result["msg"] == "Successfully completed the job for firmware rollback."
        assert result["job_status"]["JobState"] == "Completed"
        job_status.update({"JobState": "Failed"})
        mocker.patch(MODULE_PATH + "redfish_firmware_rollback.rollback_firmware", return_value=(job_status, 1, False))
        result = self._run_module(redfish_default_args)
        assert result["msg"] == "The job for firmware rollback has been completed with error(s)."
        assert result["job_status"]["JobState"] == "Failed"
        redfish_default_args.update({"reboot": False, "name": "BIOS"})
        mocker.patch(MODULE_PATH + "redfish_firmware_rollback.rollback_firmware", return_value=(job_status, 1, False))
        result = self._run_module(redfish_default_args)
        assert result["msg"] == "The job for firmware rollback has been scheduled with error(s)."
        assert result["job_status"]["JobState"] == "Failed"
        job_status.update({"JobState": "Scheduled"})
        mocker.patch(MODULE_PATH + "redfish_firmware_rollback.rollback_firmware", return_value=(job_status, 0, False))
        result = self._run_module(redfish_default_args)
        assert result["msg"] == "Successfully scheduled the job for firmware rollback."
        assert result["job_status"]["JobState"] == "Scheduled"
        job_status = {}
        mocker.patch(MODULE_PATH + "redfish_firmware_rollback.rollback_firmware", return_value=(job_status, 0, False))
        result = self._run_module(redfish_default_args)
        assert result["msg"] == "Failed to complete the job for firmware rollback."
        redfish_default_args.update({"reboot": True, "name": "BIOS", "reboot_timeout": -1})
        result = self._run_module_with_fail_json(redfish_default_args)
        assert result["msg"] == "The parameter reboot_timeout value cannot be negative or zero."
        redfish_default_args.update({"reboot": False, "name": "BIOS", "reboot_timeout": 900})
        job_status.update({"JobState": "Completed"})
        mocker.patch(MODULE_PATH + "redfish_firmware_rollback.rollback_firmware", return_value=(job_status, 0, True))
        result = self._run_module(redfish_default_args)
        assert result["msg"] == "Successfully completed the job for firmware rollback."

    def test_get_rollback_preview_target(self, redfish_connection_mock, redfish_response_mock, redfish_default_args):
        redfish_default_args.update({"username": "user", "password": "pwd", "baseuri": "XX.XX.XX.XX",
                                     "name": "BIOS", "reboot_timeout": 3600})
        f_module = self.get_module_mock(params=redfish_default_args)
        redfish_response_mock.json_data = {"Actions": {"#UpdateService.SimpleUpdate": {}}}
        with pytest.raises(Exception) as ex:
            self.module.get_rollback_preview_target(redfish_connection_mock, f_module)
        assert ex.value.args[0] == "The target firmware version does not support the firmware rollback."
        redfish_response_mock.json_data = {
            "Actions": {"#UpdateService.SimpleUpdate": {"target": "/redfish/v1/SimpleUpdate"}},
            "FirmwareInventory": {"@odata.id": "/redfish/v1/FirmwareInventory"},
            "Members": [
                {"@odata.id": "uri/1", "Id": "Previous.1", "Name": "QLogic.1", "Version": "1.2"},
                {"@odata.id": "uri/2", "Id": "Previous.2", "Name": "QLogic.2", "Version": "1.2"},
                {"@odata.id": "uri/3", "Id": "Previous.3", "Name": "QLogic.3", "Version": "1.2"},
                {"@odata.id": "uri/4", "Id": "Previous.4", "Name": "QLogic.4", "Version": "1.2"}]
        }
        with pytest.raises(Exception) as ex:
            self.module.get_rollback_preview_target(redfish_connection_mock, f_module)
        assert ex.value.args[0] == "No changes found to be applied."
        f_module.check_mode = True
        with pytest.raises(Exception) as ex:
            self.module.get_rollback_preview_target(redfish_connection_mock, f_module)
        assert ex.value.args[0] == "No changes found to be applied."
        redfish_response_mock.json_data["Members"] = [
            {"@odata.id": "uri/1", "Id": "Previous.1", "Name": "QLogic.1", "Version": "1.2"},
            {"@odata.id": "uri/2", "Id": "Previous.2", "Name": "QLogic.2", "Version": "1.2"},
            {"@odata.id": "uri/3", "Id": "Previous.3", "Name": "QLogic.3", "Version": "1.2"},
            {"@odata.id": "uri/4", "Id": "Previous.4", "Name": "BIOS", "Version": "1.2"}
        ]
        with pytest.raises(Exception) as ex:
            self.module.get_rollback_preview_target(redfish_connection_mock, f_module)
        assert ex.value.args[0] == "Changes found to be applied."
        f_module.check_mode = False
        result = self.module.get_rollback_preview_target(redfish_connection_mock, f_module)
        assert result[0] == ["uri/4"]
        assert result[2] == "/redfish/v1/SimpleUpdate"

    def test_get_job_status(self, redfish_connection_mock, redfish_response_mock, redfish_default_args, mocker):
        redfish_default_args.update({"username": "user", "password": "pwd", "baseuri": "XX.XX.XX.XX", "Name": "BIOS",
                                     "reboot_timeout": 900})
        f_module = self.get_module_mock(params=redfish_default_args)
        redfish_response_mock.json_data = {"JobState": "Completed", "JobType": "FirmwareUpdate",
                                           "Name": "Firmware Rollback: Network", "PercentComplete": 100}
        mocker.patch(MODULE_PATH + 'redfish_firmware_rollback.wait_for_redfish_job_complete',
                     return_value=(redfish_response_mock, ""))
        mocker.patch(MODULE_PATH + 'redfish_firmware_rollback.strip_substr_dict',
                     return_value={"JobState": "Completed", "JobType": "FirmwareUpdate",
                                   "Name": "Firmware Rollback: Network", "PercentComplete": 100})
        result = self.module.get_job_status(redfish_connection_mock, f_module, ["JID_123456789"], job_wait=True)
        assert result[0] == [{'JobState': 'Completed', 'JobType': 'FirmwareUpdate',
                              'Name': 'Firmware Rollback: Network', 'PercentComplete': 100}]
        assert result[1] == 0
        redfish_response_mock.json_data = {"JobState": "Failed", "JobType": "FirmwareUpdate",
                                           "Name": "Firmware Rollback: Network", "PercentComplete": 100}
        mocker.patch(MODULE_PATH + 'redfish_firmware_rollback.wait_for_redfish_job_complete',
                     return_value=(redfish_response_mock, ""))
        mocker.patch(MODULE_PATH + 'redfish_firmware_rollback.strip_substr_dict',
                     return_value={"JobState": "Failed", "JobType": "FirmwareUpdate",
                                   "Name": "Firmware Rollback: Network", "PercentComplete": 100})
        result = self.module.get_job_status(redfish_connection_mock, f_module, ["JID_123456789"], job_wait=True)
        assert result[0] == [{'JobState': 'Failed', 'JobType': 'FirmwareUpdate',
                              'Name': 'Firmware Rollback: Network', 'PercentComplete': 100}]
        assert result[1] == 1

        mocker.patch(MODULE_PATH + 'redfish_firmware_rollback.wait_for_redfish_job_complete',
                     return_value=(redfish_response_mock, "some error message"))
        with pytest.raises(Exception) as ex:
            self.module.get_job_status(redfish_connection_mock, f_module, ["JID_123456789"], job_wait=True)
        assert ex.value.args[0] == "Task excited after waiting for 900 seconds. Check console for " \
                                   "firmware rollback status."

    def test_simple_update(self, redfish_connection_mock, redfish_response_mock, redfish_default_args, mocker):
        mocker.patch(MODULE_PATH + 'redfish_firmware_rollback.time.sleep', return_value=None)
        preview_uri, update_uri = ["/uri/1"], ["/uri/SimpleUpdate"]
        redfish_response_mock.headers = {"Location": "/job/JID_123456789"}
        result = self.module.simple_update(redfish_connection_mock, preview_uri, update_uri)
        assert result == ["JID_123456789"]

    def test_require_session(self, redfish_connection_mock, redfish_response_mock, redfish_default_args):
        redfish_default_args.update({"username": "user", "password": "pwd", "baseuri": "XX.XX.XX.XX", "Name": "BIOS"})
        f_module = self.get_module_mock(params=redfish_default_args)
        redfish_response_mock.success = True
        redfish_response_mock.json_data = {"Id": 1}
        redfish_response_mock.headers = {"X-Auth-Token": "token_key"}
        result = self.module.require_session(redfish_connection_mock, f_module)
        assert result[0] == 1
        assert result[1] == "token_key"

    @pytest.mark.parametrize("exc_type", [RuntimeError, URLError, SSLValidationError, ConnectionError, KeyError,
                                          ImportError, ValueError, TypeError, IOError, AssertionError, OSError])
    def test_main_rollback_exception_handling_case(self, exc_type, mocker, redfish_default_args,
                                                   redfish_connection_mock, redfish_response_mock):
        redfish_default_args.update({"name": "BIOS"})
        redfish_response_mock.status_code = 400
        redfish_response_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'redfish_firmware_rollback.get_rollback_preview_target',
                         side_effect=exc_type('test'))
        else:
            mocker.patch(MODULE_PATH + 'redfish_firmware_rollback.get_rollback_preview_target',
                         side_effect=exc_type(HTTPS_ADDRESS, 400, HTTP_ERROR_MSG,
                                              {"accept-type": ACCESS_TYPE}, StringIO(json_str)))
        if exc_type == HTTPError:
            result = self._run_module(redfish_default_args)
            assert result['failed'] is True
        elif exc_type == URLError:
            result = self._run_module(redfish_default_args)
            assert result['unreachable'] is True
        else:
            result = self._run_module_with_fail_json(redfish_default_args)
            assert result['failed'] is True
        if exc_type == HTTPError:
            assert 'error_info' in result
        assert 'msg' in result
