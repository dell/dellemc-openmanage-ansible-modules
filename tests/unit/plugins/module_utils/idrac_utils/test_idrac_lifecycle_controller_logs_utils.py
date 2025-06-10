from ansible_collections.dellemc.openmanage.plugins.module_utils.\
    idrac_utils.idrac_lifecycle_controller_logs_utils \
    import IDRACLifecycleControllerLogs
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils
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
