import pytest
from ansible_collections.dellemc.openmanage.plugins.module_utils.\
    idrac_utils.idrac_lifecycle_controller_logs_utils \
    import (
        IDRACLifecycleControllerLogs, paginate_lc_logs, date_filter,
        severity_filter, category_filter, message_filter, apply_filters,
        validate_filter_params, validate_lc_log_firmware_version,
        check_lc_log_service_available, fetch_lc_logs, fetch_lc_log_metadata,
        discover_message_registry, enrich_with_message_registry,
        check_storage_threshold, clear_lc_logs, validate_comment,
        insert_lc_log_comment)
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils
from ansible.module_utils.six.moves.urllib.error import HTTPError
from unittest.mock import MagicMock


MANAGER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"
MANAGER_RESPONSE = {
    "Members": [
        {
            "@odata.id": MANAGER_URI
        }
    ]
}
STANDARD_IP = "127.0.0.1"
MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.'
UTILITY_PATH = "ansible_collections.dellemc.openmanage.plugins.module_utils.utils."
EXPORT_LC_LOGS = '/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellLCService/Actions/DellLCService.ExportLCLog'
CIFS_FILE_PATH = "\\\\" + STANDARD_IP + "\\cifsshare\\20250525.log"
BASE_URI = "redfish/v1/"
START_TIME = "2025-05-26T22:39:11"
JOB_TRACKING = "idrac_lifecycle_controller_logs_utils.idrac_redfish_job_tracking"
JOB_NAME = "Export: Lifecycle log"
LOG_FILE_NAME = "20250525.log"
FILE_PATH_1 = "sample/20250525.log"
COMPLETION_TIME = "2025-05-26T22:39:12"
EXPORT_SUCCESS = "LCL Export was successful"
MODULE_SUCCESS = 'Successfully exported the lifecycle controller logs.'
DESCRIPTION = "Job Instance"
EXPECTED_JOB_DATA = {
    "StartTime": START_TIME,
    "CompletionTime": COMPLETION_TIME,
    "PercentComplete": 100,
    "JobType": "LCExport",
    "ActualRunningStopTime": None,
    "MessageId": "LC022",
    "Description": DESCRIPTION,
    "Message": EXPORT_SUCCESS,
    "ActualRunningStartTime": None,
    "JobState": "Completed",
    "EndTime": None,
    "MessageArgs": [],
    "Name": JOB_NAME,
    "Id": "JID_483171510194",
    "TargetSettingsURI": None,
    "Return": "JobCreated",
    "Job": {
        "jobId": "JID_483171510194",
    },
    "JobStatus": "Completed",
    "file": CIFS_FILE_PATH,
    "Status": "Success"
}


class TestIDRACLifecycleControllerLogs(TestUtils):

    def mock_get_dynamic_idrac_invoke_request(self, *args, **kwargs):
        obj = MagicMock()
        obj.status_code = 200
        if 'uri' in kwargs and kwargs['uri'] == EXPORT_LC_LOGS:
            obj.headers = {
                "Location": "/redfish/v1/Dell/lclog.xml"
            }
        else:
            obj.json_data = {
                "StartTime": START_TIME,
                "CompletionTime": COMPLETION_TIME,
                "PercentComplete": 100,
                "JobType": "LCExport",
                "ActualRunningStopTime": None,
                "MessageId": "LC022",
                "Description": DESCRIPTION,
                "@odata.context": "/redfish/v1/$metadata#DellJob.DellJob",
                "Message": EXPORT_SUCCESS,
                "@odata.etag": "W/\"gen-32\"",
                "ActualRunningStartTime": None,
                "JobState": "Completed",
                "@odata.type": "#DellJob.v1_6_0.DellJob",
                "EndTime": None,
                "MessageArgs": [],
                "MessageArgs@odata.count": 0,
                "Name": JOB_NAME,
                "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/JID_483171510194",
                "Id": "JID_483171510194",
                "TargetSettingsURI": None
            }
        return obj

    def mock_get_dynamic_idrac_invoke_request_lc_log(self, *args, **kwargs):
        obj = MagicMock()
        obj.status_code = 200
        if 'uri' in kwargs and kwargs['uri'] == 'redfish/v1/Managers/iDRAC.Embedded.1':
            obj.json_data = {
                "Links": {
                    "Oem": {
                        "Dell": {
                            "DellLCService": {
                                "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellLCService"
                            }
                        }
                    }
                }
            }
        else:
            obj.json_data = {
                "Actions": {
                    "#DellLCService.ExportLCLog": {
                        "target": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellLCService/Actions/DellLCService.ExportLCLog"
                    }
                }
            }
        return obj

    def test_lifecycle_controller_logs_operation(self, idrac_mock):
        module_mock = MagicMock()
        logs_info = IDRACLifecycleControllerLogs(idrac_mock)
        logs_info.get_share_details = MagicMock(
            return_value=("cifsshare", "CIFS", LOG_FILE_NAME, STANDARD_IP, CIFS_FILE_PATH)
        )
        logs_info.export_lc_logs_idrac_9_10 = MagicMock(
            return_value=("Successfully exported", {'file': '\\\\' + STANDARD_IP + '\\cifsshare\\20250525.log'}, False)
        )
        result = logs_info.lifecycle_controller_logs_operation(idrac=idrac_mock, module=module_mock)
        assert result == ("Successfully exported", {'file': '\\\\' + STANDARD_IP + '\\cifsshare\\20250525.log'}, False)

    def test_get_file_name(self, idrac_mock):
        module_mock = MagicMock()
        module_mock.params.get.return_value = STANDARD_IP
        logs_info = IDRACLifecycleControllerLogs(idrac_mock)
        result = logs_info.get_file_name(module=module_mock)
        assert STANDARD_IP in result

    def test_get_share_details_cifs(self, idrac_mock):
        module_mock = MagicMock()
        module_mock.params.get.return_value = "\\\\" + STANDARD_IP + "\\cifsshare"
        logs_info = IDRACLifecycleControllerLogs(idrac_mock)
        idrac_mock.find_ip_address.return_value = STANDARD_IP
        logs_info.get_file_name = MagicMock(
            return_value=LOG_FILE_NAME
        )
        result = logs_info.get_share_details(idrac=idrac_mock, module=module_mock, sharename="\\\\" + STANDARD_IP + "\\cifsshare")
        assert result == ("cifsshare", "CIFS", LOG_FILE_NAME, STANDARD_IP, CIFS_FILE_PATH)

    def test_get_share_details_nfs(self, idrac_mock):
        module_mock = MagicMock()
        module_mock.params.get.return_value = STANDARD_IP + ":/nfsshare"
        logs_info = IDRACLifecycleControllerLogs(idrac_mock)
        idrac_mock.find_ip_address.return_value = STANDARD_IP
        logs_info.get_file_name = MagicMock(
            return_value=LOG_FILE_NAME
        )
        result = logs_info.get_share_details(idrac=idrac_mock, module=module_mock, sharename=STANDARD_IP + ":/nfsshare")
        assert result == ("nfsshare", "NFS", LOG_FILE_NAME, STANDARD_IP, STANDARD_IP + ":/nfsshare/20250525.log")

    def test_get_share_details_local(self, idrac_mock):
        module_mock = MagicMock()
        module_mock.params.get.return_value = "sample"
        logs_info = IDRACLifecycleControllerLogs(idrac_mock)
        idrac_mock.find_ip_address.return_value = None
        logs_info.get_file_name = MagicMock(
            return_value=LOG_FILE_NAME
        )
        result = logs_info.get_share_details(idrac=idrac_mock, module=module_mock, sharename="sample")
        assert result == ("sample", "Local", LOG_FILE_NAME, None, FILE_PATH_1)

    def test_export_logs_job_wait(self, idrac_mock, mocker):
        module_mock = MagicMock()
        mocker.patch(
            UTILS_PATH + JOB_TRACKING,
            return_value=(
                False,
                MODULE_SUCCESS,
                {
                    "JobState": "Completed",
                    "MessageId": "LC022",
                    "Id": "JID_1010101"
                },
                2))
        logs_info = IDRACLifecycleControllerLogs(idrac_mock)
        result = logs_info.export_logs_job_wait(idrac=idrac_mock, module=module_mock, job_uri=BASE_URI, file_path=FILE_PATH_1)
        expected_job = {
            "JobState": "Completed",
            "MessageId": "LC022",
            "Return": "JobCreated",
            "Status": "Success",
            "Job": {"jobId": "JID_1010101"},
            "JobStatus": "Completed",
            "file": FILE_PATH_1,
            "Id": "JID_1010101"
        }
        assert result == (MODULE_SUCCESS, expected_job, False)

    def test_export_logs_job_wait_new_job(self, idrac_mock, mocker):
        module_mock = MagicMock()
        mocker.patch(
            UTILS_PATH + JOB_TRACKING,
            return_value=(
                False,
                MODULE_SUCCESS,
                {
                    "JobState": "New",
                    "MessageId": "LC025",
                    "Id": "JID_1010102"
                },
                2))
        logs_info = IDRACLifecycleControllerLogs(idrac_mock)
        result = logs_info.export_logs_job_wait(idrac=idrac_mock, module=module_mock, job_uri=BASE_URI, file_path=FILE_PATH_1)
        expected_job = {
            "JobState": "New",
            "MessageId": "LC025",
            "Return": "JobCreated",
            "Status": "Success",
            "Job": {"jobId": "JID_1010102"},
            "JobStatus": "New",
            "file": FILE_PATH_1,
            "Id": "JID_1010102"
        }
        assert result == ('The export lifecycle controller log job is submitted successfully.', expected_job, False)

    def test_export_logs_job_wait_job_state_none(self, idrac_mock, mocker):
        module_mock = MagicMock()
        mocker.patch(
            UTILS_PATH + JOB_TRACKING,
            return_value=(
                False,
                MODULE_SUCCESS,
                {
                    "JobState": None,
                    "MessageId": "LC025",
                    "Id": "JID_1010102"
                },
                2))
        logs_info = IDRACLifecycleControllerLogs(idrac_mock)
        result = logs_info.export_logs_job_wait(idrac=idrac_mock, module=module_mock, job_uri=BASE_URI, file_path=FILE_PATH_1)
        expected_job = {
            "JobState": None,
            "MessageId": "LC025",
            "Return": "JobCreated",
            "Status": "Success",
            "Job": {"jobId": "JID_1010102"},
            "JobStatus": None,
            "file": FILE_PATH_1,
            "Id": "JID_1010102"
        }
        assert result == (MODULE_SUCCESS, expected_job, False)

    def test_export_local_logs(self, idrac_mock, mocker):
        module_mock = MagicMock()
        obj = MagicMock()
        obj.success = True
        file_data = MagicMock()
        file_data.body = "log data"
        obj.body = "log data"
        job_resp = MagicMock()
        job_resp.headers = {
            "Location": "/redfish/v1/Dell/lclog.xml"
        }
        FINAL_DATA = {
            "ShareName": "cifsshare",
            "ShareType": "CIFS",
            "UserName": "sample_user",
            "Password": "sample_pass",
            "FileName": "new_LC_Log.log",
            "IPAddress": STANDARD_IP,
            "IgnoreCertWarning": "Off"
        }
        JOB_DICT = {
            "ElapsedTimeSinceCompletion": "0",
            "InstanceID": "",
            "JobStartTime": "NA",
            "JobStatus": "Completed",
            "JobUntilTime": "NA",
            "Message": EXPORT_SUCCESS,
            "MessageArguments": "NA",
            "MessageID": "LC022",
            "Name": "LC Export",
            "PercentComplete": "100",
            "Status": "Success",
            "file": FILE_PATH_1,
            "retval": True
        }
        logs_info = IDRACLifecycleControllerLogs(idrac_mock)
        logs_info.get_export_lc_logs_uri = MagicMock(
            return_value=EXPORT_LC_LOGS)
        idrac_mock.invoke_request.return_value = file_data
        result = logs_info.export_local_logs(idrac=idrac_mock, module=module_mock, file_path=FILE_PATH_1, job_resp=job_resp, final_data=FINAL_DATA)
        assert result == (MODULE_SUCCESS, JOB_DICT, False)

    def test_export_lc_logs_idrac_9_10_job_wait(self, idrac_mock):
        module_mock = MagicMock()
        module_mock.params.get.return_value = True
        logs_info = IDRACLifecycleControllerLogs(idrac_mock)
        logs_info.get_export_lc_logs_uri = MagicMock(
            return_value=EXPORT_LC_LOGS)
        idrac_mock.invoke_request.return_value = self.mock_get_dynamic_idrac_invoke_request()
        result = logs_info.export_lc_logs_idrac_9_10(
            idrac=idrac_mock, module=module_mock, share_name="cifsshare",
            share_type="CIFS", file_name=LOG_FILE_NAME, ip_address=STANDARD_IP,
            file_path=CIFS_FILE_PATH)
        assert result == (MODULE_SUCCESS, EXPECTED_JOB_DATA, False)

    def test_export_lc_logs_idrac_9_10_job_wait_false(self, idrac_mock):
        module_mock = MagicMock()
        module_mock.params.get.return_value = False
        logs_info = IDRACLifecycleControllerLogs(idrac_mock)
        logs_info.get_export_lc_logs_uri = MagicMock(
            return_value=EXPORT_LC_LOGS)
        idrac_mock.invoke_request.return_value = self.mock_get_dynamic_idrac_invoke_request()
        result = logs_info.export_lc_logs_idrac_9_10(
            idrac=idrac_mock, module=module_mock, share_name="cifsshare",
            share_type="CIFS", file_name=LOG_FILE_NAME, ip_address=STANDARD_IP,
            file_path=CIFS_FILE_PATH)
        assert result == ('The export lifecycle controller log job is submitted successfully.', EXPECTED_JOB_DATA, False)

    def test_export_lc_logs_idrac_9_10_local(self, idrac_mock):
        module_mock = MagicMock()
        module_mock.params.get.return_value = True
        logs_info = IDRACLifecycleControllerLogs(idrac_mock)
        logs_info.get_export_lc_logs_uri = MagicMock(
            return_value=EXPORT_LC_LOGS)
        idrac_mock.invoke_request.return_value = self.mock_get_dynamic_idrac_invoke_request()
        local_job_details = {
            "JobState": "Completed",
            "MessageId": "LC022",
            "Return": "JobCreated",
            "Status": "Success",
            "Job": {
                "jobId": "JID_1010101"},
            "JobStatus": "Completed",
            "file": FILE_PATH_1,
            "Id": "JID_1010101"
        }
        logs_info.export_local_logs = MagicMock(
            return_value=(MODULE_SUCCESS, local_job_details, False)
        )
        result = logs_info.export_lc_logs_idrac_9_10(
            idrac=idrac_mock, module=module_mock, share_name="sample",
            share_type="Local", file_name=LOG_FILE_NAME, ip_address=None,
            file_path=FILE_PATH_1)
        assert result == (MODULE_SUCCESS, local_job_details, False)

    def test_get_lc_logs_uri(self, idrac_mock, mocker):
        logs_info = IDRACLifecycleControllerLogs(idrac_mock)
        response_1 = [{'@odata.id': '/redfish/v1/Managers/iDRAC.Embedded.1'}]
        mocker.patch(UTILS_PATH + "idrac_lifecycle_controller_logs_utils.get_dynamic_uri", return_value=response_1)
        idrac_mock.invoke_request.return_value = self.mock_get_dynamic_idrac_invoke_request_lc_log()
        result = logs_info.get_export_lc_logs_uri(idrac=idrac_mock)
        assert result == EXPORT_LC_LOGS


class TestPaginateLcLogs:

    def _page_response(self, members):
        obj = MagicMock()
        obj.json_data = {"Members": members}
        return obj

    def test_paginate_lc_logs_single_page(self):
        idrac_mock = MagicMock()
        entries = [{"Id": str(i), "Created": "2026-01-01T00:00:00Z"} for i in range(5)]
        idrac_mock.invoke_request.return_value = self._page_response(entries)
        result = list(paginate_lc_logs(idrac_mock, page_size=100))
        assert result == entries
        assert idrac_mock.invoke_request.call_count == 1

    def test_paginate_lc_logs_multiple_pages(self):
        idrac_mock = MagicMock()
        page1 = [{"Id": str(i), "Created": "2026-01-01T00:00:00Z"} for i in range(100)]
        page2 = [{"Id": "100", "Created": "2026-01-01T00:00:00Z"}]
        idrac_mock.invoke_request.side_effect = [
            self._page_response(page1), self._page_response(page2)]
        result = list(paginate_lc_logs(idrac_mock, page_size=100))
        assert len(result) == 101
        assert idrac_mock.invoke_request.call_count == 2

    def test_paginate_lc_logs_max_entries_circuit_breaker(self):
        idrac_mock = MagicMock()
        entries = [{"Id": str(i), "Created": "2026-01-01T00:00:00Z"} for i in range(10)]
        idrac_mock.invoke_request.return_value = self._page_response(entries)
        result = list(paginate_lc_logs(idrac_mock, page_size=100, max_entries=3))
        assert len(result) == 3

    def test_paginate_lc_logs_early_termination_on_date_start(self):
        idrac_mock = MagicMock()
        entries = [
            {"Id": "1", "Created": "2026-06-01T00:00:00Z"},
            {"Id": "2", "Created": "2026-01-01T00:00:00Z"},
        ]
        idrac_mock.invoke_request.return_value = self._page_response(entries)
        result = list(paginate_lc_logs(idrac_mock, page_size=100, date_start="2026-03-01T00:00:00Z"))
        assert result == [entries[0]]

    def test_paginate_lc_logs_empty_result(self):
        idrac_mock = MagicMock()
        idrac_mock.invoke_request.return_value = self._page_response([])
        result = list(paginate_lc_logs(idrac_mock, page_size=100))
        assert result == []


class TestFilterPipeline:

    def test_date_filter_within_range(self):
        entry = {"Created": "2026-05-15T00:00:00Z"}
        assert date_filter(entry, date_start="2026-01-01T00:00:00Z", date_end="2026-12-31T00:00:00Z") is True

    def test_date_filter_outside_range(self):
        entry = {"Created": "2025-05-15T00:00:00Z"}
        assert date_filter(entry, date_start="2026-01-01T00:00:00Z") is False

    def test_severity_filter_match(self):
        entry = {"Severity": "Critical"}
        assert severity_filter(entry, severity_list=["Critical", "Warning"]) is True

    def test_severity_filter_no_match(self):
        entry = {"Severity": "OK"}
        assert severity_filter(entry, severity_list=["Critical"]) is False

    def test_severity_filter_no_filter_applied(self):
        entry = {"Severity": "OK"}
        assert severity_filter(entry, severity_list=None) is True

    def test_category_filter_match(self):
        entry = {"Oem": {"Dell": {"DellLCLogEntry": {"Category": "Storage"}}}}
        assert category_filter(entry, category_list=["Storage"]) is True

    def test_category_filter_no_match(self):
        entry = {"Oem": {"Dell": {"DellLCLogEntry": {"Category": "Audit"}}}}
        assert category_filter(entry, category_list=["Storage"]) is False

    def test_message_filter_case_insensitive_match(self):
        entry = {"Message": "Disk Failure Detected"}
        assert message_filter(entry, message_contains="disk failure") is True

    def test_message_filter_no_match(self):
        entry = {"Message": "Normal operation"}
        assert message_filter(entry, message_contains="failure") is False

    def test_validate_filter_params_valid_range(self):
        validate_filter_params(date_start="2026-01-01T00:00:00Z", date_end="2026-02-01T00:00:00Z")

    def test_validate_filter_params_invalid_range_raises(self):
        with pytest.raises(ValueError):
            validate_filter_params(date_start="2026-02-01T00:00:00Z", date_end="2026-01-01T00:00:00Z")

    def test_apply_filters_combined_scenarios(self):
        entry = {
            "Created": "2026-05-15T00:00:00Z",
            "Severity": "Critical",
            "Message": "Disk failure",
            "Oem": {"Dell": {"DellLCLogEntry": {"Category": "Storage"}}},
        }
        assert apply_filters(
            entry, date_start="2026-01-01T00:00:00Z", date_end="2026-12-31T00:00:00Z",
            severity_list=["Critical"], category_list=["Storage"],
            message_contains="disk") is True
        assert apply_filters(entry, severity_list=["OK"]) is False


class TestFirmwareVersionGate:

    def test_idrac9_firmware_meets_minimum(self):
        idrac_mock = MagicMock()
        idrac_mock.get_server_generation = (15, "7.10.90.00", "iDRAC 9")
        validate_lc_log_firmware_version(idrac_mock)

    def test_idrac9_firmware_below_minimum_raises(self):
        idrac_mock = MagicMock()
        idrac_mock.get_server_generation = (15, "7.00.00.00", "iDRAC 9")
        with pytest.raises(ValueError):
            validate_lc_log_firmware_version(idrac_mock)

    def test_idrac10_firmware_meets_minimum(self):
        idrac_mock = MagicMock()
        idrac_mock.get_server_generation = (16, "1.20.50.50", "iDRAC 10")
        validate_lc_log_firmware_version(idrac_mock)

    def test_idrac10_firmware_below_minimum_raises(self):
        idrac_mock = MagicMock()
        idrac_mock.get_server_generation = (16, "1.10.00.00", "iDRAC 10")
        with pytest.raises(ValueError):
            validate_lc_log_firmware_version(idrac_mock)

    def test_none_firmware_version_raises(self):
        idrac_mock = MagicMock()
        idrac_mock.get_server_generation = (0, None, "iDRAC 9")
        with pytest.raises(ValueError):
            validate_lc_log_firmware_version(idrac_mock)


class TestLcLogServiceAvailability:

    def test_service_enabled(self):
        idrac_mock = MagicMock()
        response = MagicMock()
        response.status_code = 200
        response.json_data = {"ServiceEnabled": True}
        idrac_mock.invoke_request.return_value = response
        check_lc_log_service_available(idrac_mock)

    def test_service_disabled_raises(self):
        idrac_mock = MagicMock()
        response = MagicMock()
        response.status_code = 200
        response.json_data = {"ServiceEnabled": False}
        idrac_mock.invoke_request.return_value = response
        with pytest.raises(ValueError):
            check_lc_log_service_available(idrac_mock)

    def test_service_unreachable_raises(self):
        idrac_mock = MagicMock()
        idrac_mock.invoke_request.side_effect = HTTPError(
            "url", 404, "Not Found", {}, None)
        with pytest.raises(ValueError):
            check_lc_log_service_available(idrac_mock)


class TestFetchLcLogsAndMetadata:

    def _page_response(self, members, max_records=None):
        obj = MagicMock()
        obj.json_data = {"Members": members}
        if max_records is not None:
            obj.json_data["MaxNumberOfRecords"] = max_records
        return obj

    def test_fetch_lc_logs_applies_filters(self):
        idrac_mock = MagicMock()
        entries = [
            {"Id": "1", "Created": "2026-01-01T00:00:00Z", "Severity": "Critical", "Message": "Disk failure"},
            {"Id": "2", "Created": "2026-01-02T00:00:00Z", "Severity": "OK", "Message": "Boot complete"},
        ]
        idrac_mock.invoke_request.return_value = self._page_response(entries)
        result = fetch_lc_logs(idrac_mock, severity=["Critical"])
        assert result == [entries[0]]

    def test_fetch_lc_logs_invalid_date_range_raises(self):
        idrac_mock = MagicMock()
        with pytest.raises(ValueError):
            fetch_lc_logs(idrac_mock, date_start="2026-02-01T00:00:00Z", date_end="2026-01-01T00:00:00Z")

    def test_fetch_lc_log_metadata_returns_statistics(self):
        idrac_mock = MagicMock()
        service_response = MagicMock()
        service_response.json_data = {"MaxNumberOfRecords": 4}
        entries = [
            {"Id": "1", "Created": "2026-01-01T00:00:00Z", "Severity": "Critical"},
            {"Id": "2", "Created": "2026-01-02T00:00:00Z", "Severity": "OK"},
        ]
        idrac_mock.invoke_request.side_effect = [
            service_response, self._page_response(entries)]
        result = fetch_lc_log_metadata(idrac_mock)
        assert result["total_entries"] == 2
        assert result["oldest_entry_timestamp"] == "2026-01-01T00:00:00Z"
        assert result["newest_entry_timestamp"] == "2026-01-02T00:00:00Z"
        assert result["storage_utilization_pct"] == 50.0
        assert result["severity_breakdown"]["Critical"] == 1
        assert result["severity_breakdown"]["OK"] == 1

    def test_fetch_lc_log_metadata_zero_max_records(self):
        idrac_mock = MagicMock()
        service_response = MagicMock()
        service_response.json_data = {"MaxNumberOfRecords": 0}
        idrac_mock.invoke_request.side_effect = [
            service_response, self._page_response([])]
        result = fetch_lc_log_metadata(idrac_mock)
        assert result["storage_utilization_pct"] == 0.0
        assert result["total_entries"] == 0
        assert result["oldest_entry_timestamp"] is None


class TestMessageRegistry:

    def _response(self, json_data):
        obj = MagicMock()
        obj.json_data = json_data
        return obj

    def test_discover_message_registry_success(self):
        idrac_mock = MagicMock()
        registries_response = self._response(
            {"Members": [{"@odata.id": "/redfish/v1/Registries/IDRAC.1.0.0"}]})
        location_response = self._response(
            {"Location": [{"Uri": "/redfish/v1/Registries/IDRAC.1.0.0/IDRAC.json"}]})
        data_response = self._response(
            {"Messages": {"STOR001": {"Description": "Disk failure", "Resolution": "Replace disk"}}})
        idrac_mock.invoke_request.side_effect = [
            registries_response, location_response, data_response]
        result = discover_message_registry(idrac_mock)
        assert result == {"STOR001": {"Description": "Disk failure", "Resolution": "Replace disk"}}

    def test_discover_message_registry_no_matching_member(self):
        idrac_mock = MagicMock()
        idrac_mock.invoke_request.return_value = self._response(
            {"Members": [{"@odata.id": "/redfish/v1/Registries/Base.1.0.0"}]})
        result = discover_message_registry(idrac_mock)
        assert result is None

    def test_discover_message_registry_graceful_fallback_on_error(self):
        idrac_mock = MagicMock()
        idrac_mock.invoke_request.side_effect = HTTPError(
            "url", 404, "Not Found", {}, None)
        result = discover_message_registry(idrac_mock)
        assert result is None

    def test_discover_message_registry_no_location_uri(self):
        idrac_mock = MagicMock()
        registries_response = self._response(
            {"Members": [{"@odata.id": "/redfish/v1/Registries/IDRAC.1.0.0"}]})
        location_response = self._response({"Location": []})
        idrac_mock.invoke_request.side_effect = [registries_response, location_response]
        result = discover_message_registry(idrac_mock)
        assert result is None

    def test_enrich_with_message_registry_adds_fields(self):
        entries = [{"Id": "1", "MessageId": "STOR001"}]
        registry = {"STOR001": {"Description": "Disk failure", "Resolution": "Replace disk"}}
        result = enrich_with_message_registry(entries, registry)
        assert result[0]["message_description"] == "Disk failure"
        assert result[0]["message_resolution"] == "Replace disk"

    def test_enrich_with_message_registry_none_registry_sets_none_fields(self):
        entries = [{"Id": "1", "MessageId": "STOR001"}]
        result = enrich_with_message_registry(entries, None)
        assert result[0]["message_description"] is None
        assert result[0]["message_resolution"] is None

    def test_enrich_with_message_registry_unknown_message_id(self):
        entries = [{"Id": "1", "MessageId": "UNKNOWN"}]
        registry = {"STOR001": {"Description": "Disk failure", "Resolution": "Replace disk"}}
        result = enrich_with_message_registry(entries, registry)
        assert result[0]["message_description"] is None
        assert result[0]["message_resolution"] is None


class TestStorageThresholdWarning:

    def test_no_warning_below_threshold(self):
        assert check_storage_threshold(50.0, storage_threshold_pct=80) is None

    def test_warning_above_threshold(self):
        warning = check_storage_threshold(85.0, storage_threshold_pct=80)
        assert warning is not None
        assert "85.0%" in warning
        assert "threshold: 80%" in warning

    def test_no_warning_at_exact_threshold(self):
        assert check_storage_threshold(80.0, storage_threshold_pct=80) is None


class TestClearLcLogs:

    def _metadata_response(self, total_entries, max_records):
        obj = MagicMock()
        obj.json_data = {"MaxNumberOfRecords": max_records}
        return obj

    def _entries_response(self, members):
        obj = MagicMock()
        obj.json_data = {"Members": members}
        return obj

    def test_clear_logs_requires_explicit_confirmation(self):
        idrac_mock = MagicMock()
        with pytest.raises(ValueError):
            clear_lc_logs(idrac_mock, clear_logs=False)

    def test_clear_logs_success_returns_counts(self):
        idrac_mock = MagicMock()
        pre_entries = [{"Id": str(i), "Severity": "OK"} for i in range(5)]
        clear_response = MagicMock()
        clear_response.headers = {}
        idrac_mock.invoke_request.side_effect = [
            self._metadata_response(5, 10),
            self._entries_response(pre_entries),
            clear_response,
            self._metadata_response(0, 10),
            self._entries_response([]),
        ]
        result = clear_lc_logs(idrac_mock, clear_logs=True)
        assert result["pre_clear_count"] == 5
        assert result["post_clear_count"] == 0
        assert result["entries_cleared"] == 5

    def test_clear_logs_with_job_tracking_failure_raises(self, mocker):
        idrac_mock = MagicMock()
        pre_entries = [{"Id": "1", "Severity": "OK"}]
        clear_response = MagicMock()
        clear_response.headers = {"Location": "/redfish/v1/TaskService/Tasks/1"}
        idrac_mock.invoke_request.side_effect = [
            self._metadata_response(1, 10),
            self._entries_response(pre_entries),
            clear_response,
        ]
        mocker.patch(
            "ansible_collections.dellemc.openmanage.plugins.module_utils."
            "idrac_utils.idrac_lifecycle_controller_logs_utils.idrac_redfish_job_tracking",
            return_value=(True, "Task failed", {}, 5))
        with pytest.raises(ValueError):
            clear_lc_logs(idrac_mock, clear_logs=True)


class TestCommentInsertion:

    def test_validate_comment_within_limit(self):
        validate_comment("Maintenance window started")

    def test_validate_comment_exceeds_max_length_raises(self):
        with pytest.raises(ValueError):
            validate_comment("x" * 257)

    def test_validate_comment_control_characters_raise(self):
        with pytest.raises(ValueError):
            validate_comment("bad\x00comment")

    def test_insert_lc_log_comment_success(self):
        idrac_mock = MagicMock()
        response = MagicMock()
        response.json_data = {"Id": "999", "Created": "2026-01-15T10:00:00Z"}
        idrac_mock.invoke_request.return_value = response
        result = insert_lc_log_comment(idrac_mock, "Maintenance window")
        assert result == {"Id": "999", "Created": "2026-01-15T10:00:00Z"}

    def test_insert_lc_log_comment_invalid_raises(self):
        idrac_mock = MagicMock()
        with pytest.raises(ValueError):
            insert_lc_log_comment(idrac_mock, "x" * 300)
