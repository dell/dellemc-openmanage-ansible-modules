# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.2.0
# Copyright (C) 2022-23 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_boot
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from io import StringIO
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from unittest.mock import MagicMock

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
MODULE_UTIL_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.'


@pytest.fixture
def boot_connection_mock(mocker, redfish_response_mock):
    idrac_conn_mock = mocker.patch(MODULE_PATH + 'idrac_boot.iDRACRedfishAPI')
    idrac_conn_mock_obj = idrac_conn_mock.return_value.__enter__.return_value
    idrac_conn_mock_obj.invoke_request.return_value = redfish_response_mock
    return idrac_conn_mock_obj


class TestConfigBios(FakeAnsibleModule):

    module = idrac_boot

    def test_get_response_attributes(self, boot_connection_mock, redfish_response_mock, idrac_default_args):
        idrac_default_args.update({"boot_options": {"display_name": "Boot001", "enabled": True}})
        f_module = self.get_module_mock(params=idrac_default_args)
        redfish_response_mock.success = True
        redfish_response_mock.json_data = {"Boot": {
            "BootOptions": "", "Certificates": "", "BootOrder": [], "BootOrder@odata.count": 1,
            "BootSourceOverrideEnabled": "Disabled", "BootSourceOverrideMode": "Legacy",
            "BootSourceOverrideTarget": "None", "UefiTargetBootSourceOverride": None,
            "BootSourceOverrideTarget@Redfish.AllowableValues": []},
            "Actions": {"#ComputerSystem.Reset": {"ResetType@Redfish.AllowableValues": ["ForceRestart"]}}}
        result = self.module.get_response_attributes(f_module, boot_connection_mock, "System.Embedded.1")
        assert result["BootSourceOverrideEnabled"] == "Disabled"

        redfish_response_mock.json_data.pop("Actions")
        result = self.module.get_response_attributes(f_module, boot_connection_mock, "System.Embedded.1")
        assert result["BootSourceOverrideEnabled"] == "Disabled"

        redfish_response_mock.json_data["Boot"].pop("BootOptions", None)
        with pytest.raises(Exception) as err:
            self.module.get_response_attributes(f_module, boot_connection_mock, "System.Embedded.1")
        assert err.value.args[0] == "The system does not support the BootOptions feature."

    def test_get_existing_boot_options(self, boot_connection_mock, redfish_response_mock, idrac_default_args):
        redfish_response_mock.success = True
        redfish_response_mock.json_data = {"Members": [
            {"@odata.context": "/redfish/v1/$metadata#BootOption.BootOption",
             "@odata.id": "/redfish/v1/Systems/System.Embedded.1/BootOptions/HardDisk.List.1-1",
             "@odata.type": "#BootOption.v1_0_4.BootOption", "BootOptionEnabled": True,
             "BootOptionReference": "HardDisk.List.1-1",
             "Description": "Current settings of the Legacy Boot option",
             "DisplayName": "Hard drive C:", "Id": "HardDisk.List.1-1", "Name": "Legacy Boot option"}]}
        resp_data = {'Members': [{
            'BootOptionEnabled': True, 'BootOptionReference': 'HardDisk.List.1-1',
            'Description': 'Current settings of the Legacy Boot option',
            'DisplayName': 'Hard drive C:', 'Id': 'HardDisk.List.1-1',
            'Name': 'Legacy Boot option'}]}
        result = self.module.get_existing_boot_options(boot_connection_mock, "System.Embedded.1")
        assert result == resp_data

    @pytest.mark.parametrize("code", [200, 204])
    def test_system_reset(self, boot_connection_mock, redfish_response_mock, idrac_default_args, mocker, code):
        mocker.patch(MODULE_UTIL_PATH + 'time.sleep', return_value=None)
        redfish_response_mock.status_code = code
        idrac_default_args.update({"boot_source_override_mode": "uefi", "reset_type": "force_restart"})
        f_module = self.get_module_mock(params=idrac_default_args)
        reset, track_failed, reset_msg, resp_data = self.module.system_reset(f_module, boot_connection_mock,
                                                                             "System.Embedded.1")
        assert reset is True

    def test_get_scheduled_job(self, boot_connection_mock, redfish_response_mock, idrac_default_args, mocker):
        mocker.patch(MODULE_PATH + 'idrac_boot.time', return_value=None)
        redfish_response_mock.success = True
        redfish_response_mock.json_data = {"Members": [{
            "Description": "Job Instance", "EndTime": "TIME_NA", "Id": "JID_609237056489", "JobState": "Scheduled",
            "JobType": "BIOSConfiguration", "Message": "Job scheduled successfully.", "MessageArgs": [],
            "MessageId": "PR19", "Name": "Configure: BIOS.Setup.1-1", "PercentComplete": 10}]}
        status, job = self.module.get_scheduled_job(boot_connection_mock)
        assert status is True

    def test_get_scheduled_job_job_state_not_none(self, boot_connection_mock, redfish_response_mock, idrac_default_args, mocker):
        mocker.patch(MODULE_PATH + 'idrac_boot.time', return_value=None)
        redfish_response_mock.success = True
        redfish_response_mock.json_data = {"Members": []}
        is_job, progress_job = self.module.get_scheduled_job(boot_connection_mock, ["Scheduled", "New", "Running"])
        print(progress_job)
        assert is_job is False

    def test_get_scheduled_job_progress_job_none(self, boot_connection_mock, redfish_response_mock, idrac_default_args, mocker):
        mocker.patch(MODULE_PATH + 'idrac_boot.time', return_value=None)
        redfish_response_mock.success = True
        redfish_response_mock.json_data = {"Members": [{
            "Description": "Job Instance", "EndTime": "TIME_NA", "Id": "JID_609237056489", "JobState": "Completed",
            "JobType": "BIOSConfiguration", "Message": "Job scheduled successfully.", "MessageArgs": [],
            "MessageId": "PR19", "Name": "Configure: BIOS.Setup.1-1", "PercentComplete": 10}]}
        status, job = self.module.get_scheduled_job(boot_connection_mock)
        assert status is False

    def test_configure_boot_options(self, boot_connection_mock, redfish_response_mock, idrac_default_args, mocker):
        idrac_default_args.update({"boot_source_override_mode": "uefi", "job_wait": True, "reset_type": "none",
                                   "job_wait_timeout": 900})
        obj = MagicMock()
        obj.json_data = {"JobState": "Reset Successful"}

        f_module = self.get_module_mock(params=idrac_default_args)
        mocker.patch(MODULE_PATH + 'idrac_boot.get_scheduled_job', return_value=(True, {}))
        resp_data = {"BootOrder": ["Boot001", "Boot002", "Boot003"], "BootSourceOverrideEnabled": "Disabled",
                     "BootSourceOverrideMode": "Legacy", "BootSourceOverrideTarget": "UefiTarget",
                     "UefiTargetBootSourceOverride": "/0x31/0x33/0x01/0x01"}
        mocker.patch(MODULE_PATH + 'idrac_boot.get_response_attributes', return_value=resp_data)
        with pytest.raises(Exception) as err:
            self.module.configure_boot_options(f_module, boot_connection_mock, "System.Embedded.1", {"Boot001": False})
        assert err.value.args[0] == "Unable to complete the request because the BIOS configuration job already " \
                                    "exists. Wait for the pending job to complete."
        redfish_response_mock.status_code = 202
        redfish_response_mock.success = True
        redfish_response_mock.headers = {"Location": "/redfish/v1/Managers/iDRAC.Embedded.1/JID_123456789"}
        redfish_response_mock.json_data = {"Attributes": {"BootSeq": [{"Name": "Boot001", "Id": 0, "Enabled": True},
                                                                      {"Name": "Boot000", "Id": 1, "Enabled": True}]}}
        mocker.patch(MODULE_PATH + 'idrac_boot.get_scheduled_job', return_value=(False, {}))
        mocker.patch(MODULE_PATH + 'idrac_boot.idrac_system_reset', return_value=(False, False, "Completed", {}))
        mocker.patch(MODULE_PATH + 'idrac_boot.wait_for_idrac_job_completion',
                     return_value=({}, "This job is not complete after 900 seconds."))
        with pytest.raises(Exception) as err:
            self.module.configure_boot_options(f_module, boot_connection_mock, "System.Embedded.1", {"Boot001": False})
        assert err.value.args[0] == "This job is not complete after 900 seconds."
        resp_data = {"BootOrder": ["Boot001", "Boot002", "Boot003"], "BootSourceOverrideEnabled": "Disabled",
                     "BootSourceOverrideMode": "UEFI", "BootSourceOverrideTarget": "UefiTarget",
                     "UefiTargetBootSourceOverride": "/0x31/0x33/0x01/0x01"}
        mocker.patch(MODULE_PATH + 'idrac_boot.get_response_attributes', return_value=resp_data)
        idrac_default_args.update({"boot_source_override_mode": "legacy", "reset_type": "force_restart"})
        f_module = self.get_module_mock(params=idrac_default_args)
        redfish_response_mock.json_data = {"Attributes": {"UefiBootSeq": [
            {"Name": "Boot001", "Id": 0, "Enabled": True}, {"Name": "Boot000", "Id": 1, "Enabled": True}]}}
        with pytest.raises(Exception) as err:
            self.module.configure_boot_options(f_module, boot_connection_mock, "System.Embedded.1", {"Boot001": False})
        assert err.value.args[0] == "This job is not complete after 900 seconds."

        mocker.patch(MODULE_PATH + 'idrac_boot.system_reset', return_value=(False, False, "Completed Reset", None))
        with pytest.raises(Exception) as err:
            self.module.configure_boot_options(f_module, boot_connection_mock, "System.Embedded.1", {"Boot001": False})
        assert err.value.args[0] == "Completed Reset"

        redfish_response_mock.status_code = 201
        redfish_response_mock.success = True
        mocker.patch(MODULE_PATH + 'idrac_boot.get_scheduled_job', return_value=(False, {}))
        job_data = self.module.configure_boot_options(f_module, boot_connection_mock, "System.Embedded.1", {"Boot001": False})
        assert job_data == {}

    def test_configure_boot_options_v2(self, boot_connection_mock, redfish_response_mock, idrac_default_args, mocker):
        idrac_default_args.update({"boot_source_override_mode": "uefi", "job_wait": True, "reset_type": "none",
                                   "job_wait_timeout": 900})
        obj = MagicMock()
        obj.json_data = {"JobState": "Reset Successful"}
        mocker.patch(MODULE_PATH + 'idrac_boot.get_scheduled_job', return_value=(True, {}))
        resp_data = {"BootOrder": ["Boot001", "Boot002", "Boot003"], "BootSourceOverrideEnabled": "Disabled",
                     "BootSourceOverrideMode": "Legacy", "BootSourceOverrideTarget": "UefiTarget",
                     "UefiTargetBootSourceOverride": "/0x31/0x33/0x01/0x01"}
        mocker.patch(MODULE_PATH + 'idrac_boot.get_response_attributes', return_value=resp_data)
        redfish_response_mock.status_code = 202
        redfish_response_mock.success = True
        redfish_response_mock.headers = {"Location": "/redfish/v1/Managers/iDRAC.Embedded.1/JID_123456789"}
        redfish_response_mock.json_data = {"Attributes": {"BootSeq": [{"Name": "Boot001", "Id": 0, "Enabled": True},
                                                                      {"Name": "Boot000", "Id": 1, "Enabled": True}]}}
        mocker.patch(MODULE_PATH + 'idrac_boot.get_scheduled_job', return_value=(False, {}))
        mocker.patch(MODULE_PATH + 'idrac_boot.system_reset', return_value=(True, False, "Completed", obj))
        mocker.patch(MODULE_PATH + 'idrac_boot.wait_for_idrac_job_completion',
                     return_value=(obj, ""))
        f_module = self.get_module_mock(params=idrac_default_args)
        job_data = self.module.configure_boot_options(f_module, boot_connection_mock, "System.Embedded.1", {"Boot001": False})
        assert job_data == {"JobState": "Reset Successful"}

    def test_apply_boot_settings(self, boot_connection_mock, redfish_response_mock, idrac_default_args, mocker):
        idrac_default_args.update({"boot_source_override_mode": "uefi", "job_wait": True, "reset_type": "none",
                                   "job_wait_timeout": 900})
        f_module = self.get_module_mock(params=idrac_default_args)
        payload = {"Boot": {"BootSourceOverrideMode": "UEFI"}}
        redfish_response_mock.success = True
        redfish_response_mock.status_code = 200
        mocker.patch(MODULE_PATH + 'idrac_boot.idrac_system_reset', return_value=(False, False, "Completed", {}))
        mocker.patch(MODULE_PATH + 'idrac_boot.get_scheduled_job', return_value=(True, [{"Id": "JID_123456789"}]))
        mocker.patch(MODULE_PATH + 'idrac_boot.wait_for_idrac_job_completion',
                     return_value=({}, "This job is not complete after 900 seconds."))
        with pytest.raises(Exception) as err:
            self.module.apply_boot_settings(f_module, boot_connection_mock, payload, "System.Embedded.1", 16)
        assert err.value.args[0] == "This job is not complete after 900 seconds."

        redfish_response_mock.status_code = 400
        job_data = self.module.apply_boot_settings(f_module, boot_connection_mock, payload, "System.Embedded.1", 17)
        assert job_data == {}

    def test_apply_boot_settings_reset_type(self, boot_connection_mock, redfish_response_mock, idrac_default_args, mocker):
        idrac_default_args.update({"boot_source_override_mode": "uefi", "job_wait": True, "reset_type": "graceful_restart",
                                   "job_wait_timeout": 900})
        boot_connection_mock.get_server_generation = (17, 'abc', 'iDRAC 10')
        f_module = self.get_module_mock(params=idrac_default_args)
        payload = {"Boot": {"BootSourceOverrideMode": "UEFI"}}
        redfish_response_mock.success = True
        redfish_response_mock.status_code = 200

        obj = MagicMock()
        obj.json_data = {"JobState": "Reset Successful"}
        mocker.patch(MODULE_PATH + 'idrac_boot.system_reset', return_value=(False, False, "Completed", obj))
        mocker.patch(MODULE_PATH + 'idrac_boot.get_scheduled_job', return_value=(False, [{"Id": "JID_123456789"}]))
        job_data = self.module.apply_boot_settings(f_module, boot_connection_mock, payload, "System.Embedded.1", 17)
        assert job_data == {"JobState": "Reset Successful"}

        mocker.patch(MODULE_PATH + 'idrac_boot.system_reset', return_value=(True, False, "Completed", {}))
        mocker.patch(MODULE_PATH + 'idrac_boot.get_scheduled_job', return_value=(True, [{"Id": "JID_123456789"}]))
        mocker.patch(MODULE_PATH + 'idrac_boot.wait_for_idrac_job_completion',
                     return_value=(obj, ""))
        job_data = self.module.apply_boot_settings(f_module, boot_connection_mock, payload, "System.Embedded.1", 16)
        assert job_data == {"JobState": "Reset Successful"}

    def test_configure_boot_settings(self, boot_connection_mock, redfish_response_mock, idrac_default_args, mocker):
        idrac_default_args.update({"boot_order": ["Boot005", "Boot001"], "job_wait": True, "reset_type": "none",
                                   "job_wait_timeout": 900, "boot_source_override_mode": "uefi",
                                   "boot_source_override_enabled": "once", "boot_source_override_target": "cd",
                                   "uefi_target_boot_source_override": "test_uefi_path"})
        f_module = self.get_module_mock(params=idrac_default_args)
        resp_data = {"BootOrder": ["Boot001", "Boot002", "Boot003"], "BootSourceOverrideEnabled": "Disabled",
                     "BootSourceOverrideMode": "Legacy", "BootSourceOverrideTarget": "UefiTarget",
                     "UefiTargetBootSourceOverride": "/0x31/0x33/0x01/0x01"}
        mocker.patch(MODULE_PATH + 'idrac_boot.get_response_attributes', return_value=resp_data)
        boot_connection_mock.get_server_generation = (16, 'abc', 'iDRAC 9')
        with pytest.raises(Exception) as err:
            self.module.configure_boot_settings(f_module, boot_connection_mock, "System.Embedded.1")
        assert err.value.args[0] == "Invalid boot order reference provided."
        idrac_default_args.update({"boot_order": ["Boot001", "Boot001"]})
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as err:
            self.module.configure_boot_settings(f_module, boot_connection_mock, "System.Embedded.1")
        assert err.value.args[0] == "Duplicate boot order reference provided."
        mocker.patch(MODULE_PATH + 'idrac_boot.apply_boot_settings', return_value={"JobStatus": "Completed"})
        idrac_default_args.update({"boot_order": ["Boot001", "Boot003", "Boot002"]})
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.configure_boot_settings(f_module, boot_connection_mock, "System.Embedded.1")
        assert result["JobStatus"] == "Completed"
        f_module.check_mode = True
        with pytest.raises(Exception) as err:
            self.module.configure_boot_settings(f_module, boot_connection_mock, "System.Embedded.1")
        assert err.value.args[0] == "Changes found to be applied."

    def test_configure_boot_settings_v2(self, boot_connection_mock, redfish_response_mock, idrac_default_args, mocker):
        idrac_default_args.update({"boot_order": ["Boot001", "Boot002", "Boot003"], "job_wait": True, "reset_type": "none",
                                   "job_wait_timeout": 900, "boot_source_override_mode": "uefi",
                                   "boot_source_override_enabled": "once", "boot_source_override_target": "cd",
                                   "uefi_target_boot_source_override": "test_uefi_path"})
        f_module = self.get_module_mock(params=idrac_default_args)
        resp_data = {"BootSourceOverrideEnabled": "Disabled",
                     "BootSourceOverrideMode": "Legacy", "BootSourceOverrideTarget": "UefiTarget",
                     "UefiTargetBootSourceOverride": "/0x31/0x33/0x01/0x01", "BootOrder": ["Boot001", "Boot002", "Boot003"]}
        mocker.patch(MODULE_PATH + 'idrac_boot.get_response_attributes', return_value=resp_data)
        mocker.patch(MODULE_PATH + 'idrac_boot.apply_boot_settings', return_value={"JobStatus": "Completed"})

        boot_connection_mock.get_server_generation = (16, 'abc', 'iDRAC 9')
        job_resp = self.module.configure_boot_settings(f_module, boot_connection_mock, "System.Embedded.1")
        assert job_resp["JobStatus"] == "Completed"

        idrac_default_args.update({"boot_order": []})
        with pytest.raises(Exception) as err:
            self.module.configure_boot_settings(f_module, boot_connection_mock, "System.Embedded.1")
        assert err.value.args[0] == "Unable to complete the operation because all boot devices are required for this operation."

        idrac_default_args.pop("boot_order")
        idrac_default_args.pop("boot_source_override_mode")
        idrac_default_args.pop("boot_source_override_enabled")
        job_resp = self.module.configure_boot_settings(f_module, boot_connection_mock, "System.Embedded.1")
        assert job_resp["JobStatus"] == "Completed"

        idrac_default_args.update({"boot_source_override_target": "uefi_target"})
        resp_data.update({"BootSourceOverrideTarget": "cd"})
        job_resp = self.module.configure_boot_settings(f_module, boot_connection_mock, "System.Embedded.1")
        assert job_resp["JobStatus"] == "Completed"

    def test_configure_idrac_boot(self, boot_connection_mock, redfish_response_mock, idrac_default_args, mocker):
        idrac_default_args.update({"job_wait": True, "reset_type": "none", "job_wait_timeout": 900,
                                   "boot_options": [{"boot_option_reference": "HardDisk.List.1-1", "enabled": True}]})
        f_module = self.get_module_mock(params=idrac_default_args)
        boot_return_data = {"Members": [{"BootOptionEnabled": False, "BootOptionReference": "HardDisk.List.1-1",
                                         "Description": "Current settings of the Legacy Boot option",
                                         "DisplayName": "Hard drive C:", "Id": "HardDisk.List.1-1",
                                         "Name": "Legacy Boot option", "UefiDevicePath": "VenHw(D6C0639F-823DE6)"}],
                            "Name": "Boot Options Collection", "Description": "Collection of BootOptions"}
        mocker.patch(MODULE_PATH + 'idrac_boot.get_existing_boot_options', return_value=boot_return_data)
        mocker.patch(MODULE_PATH + 'idrac_boot.configure_boot_options', return_value={"JobType": "Completed"})
        mocker.patch(MODULE_PATH + 'idrac_boot.configure_boot_settings', return_value={"JobType": "Completed"})
        result = self.module.configure_idrac_boot(f_module, boot_connection_mock, "System.Embedded.1")
        assert result["JobType"] == "Completed"
        idrac_default_args.update({"boot_options": [{"boot_option_reference": "HardDisk.List.1-2", "enabled": True}]})
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as err:
            self.module.configure_idrac_boot(f_module, boot_connection_mock, "System.Embedded.1")
        assert err.value.args[0] == "Invalid boot_options provided."
        idrac_default_args.update({"boot_options": [{"boot_option_reference": "HardDisk.List.1-1", "enabled": True},
                                                    {"boot_option_reference": "HardDisk.List.1-1", "enabled": True}]})
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as err:
            self.module.configure_idrac_boot(f_module, boot_connection_mock, "System.Embedded.1")
        assert err.value.args[0] == "Duplicate boot_options provided."
        idrac_default_args.update({"boot_options": [{"boot_option_reference": "HardDisk.List.1-1", "enabled": False}]})
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = True
        with pytest.raises(Exception) as err:
            self.module.configure_idrac_boot(f_module, boot_connection_mock, "System.Embedded.1")
        assert err.value.args[0] == "No changes found to be applied."
        idrac_default_args.update({"boot_options": [{"boot_option_reference": "HardDisk.List.1-1", "enabled": True}]})
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = True
        with pytest.raises(Exception) as err:
            self.module.configure_idrac_boot(f_module, boot_connection_mock, "System.Embedded.1")
        assert err.value.args[0] == "Changes found to be applied."

        f_module = self.get_module_mock(params=idrac_default_args)
        idrac_default_args.pop("boot_options")
        job_resp = self.module.configure_idrac_boot(f_module, boot_connection_mock, "System.Embedded.1")
        assert job_resp == {"JobType": "Completed"}

    @pytest.mark.parametrize("exc_type", [HTTPError, RuntimeError, URLError, SSLValidationError, ConnectionError, KeyError,
                                          ImportError, ValueError, TypeError])
    def test_main_exception(self, boot_connection_mock, redfish_response_mock, idrac_default_args, mocker, exc_type):
        idrac_default_args.update({"boot_source_override_mode": "legacy"})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'idrac_boot.get_system_res_id', side_effect=exc_type('test'))
        else:
            mocker.patch(MODULE_PATH + 'idrac_boot.get_system_res_id',
                         side_effect=exc_type('https://testhost.com', 401, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
        if exc_type != URLError:
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result

    def test_main_success(self, boot_connection_mock, redfish_response_mock, idrac_default_args, mocker):
        idrac_default_args.update({"boot_source_override_mode": "legacy"})
        redfish_response_mock.success = True
        mocker.patch(MODULE_PATH + 'idrac_boot.get_system_res_id', return_value=("System.Embedded.1", ""))
        job_resp = {"Description": "Job Instance", "EndTime": "TIME_NA", "Id": "JID_609237056489",
                    "JobState": "Completed", "JobType": "BIOSConfiguration", "MessageId": "PR19",
                    "Message": "Job scheduled successfully.", "MessageArgs": [],
                    "Name": "Configure: BIOS.Setup.1-1", "PercentComplete": 100}
        mocker.patch(MODULE_PATH + 'idrac_boot.configure_idrac_boot', return_value=job_resp)
        boot_return_data = {"Members": [{"BootOptionEnabled": False, "BootOptionReference": "HardDisk.List.1-1",
                                         "Description": "Current settings of the Legacy Boot option",
                                         "DisplayName": "Hard drive C:", "Id": "HardDisk.List.1-1",
                                         "Name": "Legacy Boot option", "UefiDevicePath": "VenHw(D6C0639F-823DE6)"}],
                            "Name": "Boot Options Collection", "Description": "Collection of BootOptions"}
        mocker.patch(MODULE_PATH + 'idrac_boot.get_existing_boot_options', return_value=boot_return_data)
        resp_data = {"BootOrder": ["Boot001", "Boot002", "Boot003"], "BootSourceOverrideEnabled": "Disabled",
                     "BootSourceOverrideMode": "Legacy", "BootSourceOverrideTarget": "UefiTarget",
                     "UefiTargetBootSourceOverride": "/0x31/0x33/0x01/0x01"}
        mocker.patch(MODULE_PATH + 'idrac_boot.get_response_attributes', return_value=resp_data)
        result = self._run_module(idrac_default_args)
        assert result["msg"] == "Successfully updated the boot settings."

    def test_main_res_id_error(self, boot_connection_mock, redfish_response_mock, idrac_default_args, mocker):
        idrac_default_args.update({"boot_source_override_mode": "legacy"})
        mocker.patch(MODULE_PATH + 'idrac_boot.get_system_res_id', return_value=("System.Embedded.5", "Failed"))
        with pytest.raises(Exception) as err:
            self._run_module(idrac_default_args)
        assert err.value.args[0]["msg"] == "Failed"

    def test_manin_success_v2(self, boot_connection_mock, redfish_response_mock, idrac_default_args, mocker):
        idrac_default_args.update({"boot_source_override_mode": "legacy", "resource_id": "System.Embedded.1"})
        redfish_response_mock.success = True
        job_resp = {"Description": "Job Instance", "EndTime": "TIME_NA", "Id": "JID_609237056489",
                    "JobState": "Failed", "JobType": "BIOSConfiguration", "MessageId": "PR19",
                    "Message": "Job scheduled successfully.", "MessageArgs": [],
                    "Name": "Configure: BIOS.Setup.1-1", "PercentComplete": 100}
        mocker.patch(MODULE_PATH + 'idrac_boot.configure_idrac_boot', return_value=job_resp)
        boot_return_data = {"Members": [{"BootOptionEnabled": False, "BootOptionReference": "HardDisk.List.1-1",
                                         "Description": "Current settings of the Legacy Boot option",
                                         "DisplayName": "Hard drive C:", "Id": "HardDisk.List.1-1",
                                         "Name": "Legacy Boot option", "UefiDevicePath": "VenHw(D6C0639F-823DE6)"}],
                            "Name": "Boot Options Collection", "Description": "Collection of BootOptions"}
        mocker.patch(MODULE_PATH + 'idrac_boot.get_existing_boot_options', return_value=boot_return_data)
        resp_data = {"BootOrder": ["Boot001", "Boot002", "Boot003"], "BootSourceOverrideEnabled": "Disabled",
                     "BootSourceOverrideMode": "Legacy", "BootSourceOverrideTarget": "UefiTarget",
                     "UefiTargetBootSourceOverride": "/0x31/0x33/0x01/0x01"}
        mocker.patch(MODULE_PATH + 'idrac_boot.get_response_attributes', return_value=resp_data)
        mocker.patch(MODULE_PATH + 'idrac_boot.strip_substr_dict', return_value=job_resp)
        with pytest.raises(Exception) as err:
            self._run_module(idrac_default_args)
        assert err.value.args[0]["msg"] == "Failed to update the boot settings."

        idrac_default_args.update({"job_wait": False, "reset_type": "none"})
        job_resp.update({"JobState": "Running"})
        # with pytest.raises(Exception) as err:
        module_return = self._run_module(idrac_default_args)
        assert module_return["msg"] == "The boot settings operation is triggered/submitted successfully."
