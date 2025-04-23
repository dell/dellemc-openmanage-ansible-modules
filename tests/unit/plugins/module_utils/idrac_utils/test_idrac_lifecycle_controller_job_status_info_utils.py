from ansible_collections.dellemc.openmanage.tests.unit.plugins.\
    module_utils.idrac_utils.test_idrac_utils import TestUtils
from ansible_collections.dellemc.openmanage.plugins.\
    module_utils.idrac_utils.info.lifecycle_controller_job_status import IDRACLifecycleControllerJobStatusInfo
from unittest.mock import MagicMock

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
JOB_LINK = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/job_id"
JOB_MEMBERS = [
    {
        "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/job_id"
    },
]
RESPONSE = {
    "Status": {
        "Health": "OK",
        "State": "Enabled"
    },
    "LastResetTime": "2025-04-15T05:34:47-05:00",
    "DateTime": "2025-04-15T09:39:04-05:00",
    "PowerState": "On",
    "GraphicalConsole": {
        "ServiceEnabled": True,
        "ConnectTypesSupported": [
            "KVMIP"
        ],
        "ConnectTypesSupported@odata.count": 1,
        "MaxConcurrentSessions": 6
    },
    "SerialConsole": {
        "ServiceEnabled": False,
        "ConnectTypesSupported": [
        ],
        "ConnectTypesSupported@odata.count": 0,
        "MaxConcurrentSessions": 0
    },
    "SerialNumber": "CNWS3004A700O2",
    "LogServices": {
        "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/LogServices"
    },
    "DateTimeLocalOffset": "-05:00",
    "Certificates": {
        "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Certificates"
    },
    "EthernetInterfaces": {
        "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/EthernetInterfaces"
    },
    "TimeZoneName": "CST6CDT",
    "ServiceIdentification": "DN04203",
    "Model": "17G Monolithic",
    "Name": "Manager",
    "@odata.type": "#Manager.v1_20_0.Manager",
    "Oem": {
        "Dell": {
            "Jobs": {
                "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs"
            },
        }
    },
    "PartNumber": "03TJR3",
    "ManagerType": "BMC",
    "Redundancy@odata.count": 0,
    "ManagerDiagnosticData": {
        "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/ManagerDiagnosticData"
    },
    "Id": "iDRAC.Embedded.1"
}
JOB_RESPONSE = {
    "Description": "Job Instance",
    "MessageId": "RED106",
    "Message": "Unable to parse the lc_validator_output.xml file because of an internal error.",
    "Name": "update:new",
    "StartTime": "2025-04-15T06:01:03",
    "ActualRunningStopTime": None,
    "@odata.etag": "W/\"gen-31\"",
    "Id": "job_id",
    "EndTime": None,
    "PercentComplete": 100,
    "JobType": "FirmwareUpdate",
    "MessageArgs": [],
    "MessageArgs@odata.count": 0,
    "JobState": "Failed",
    "ActualRunningStartTime": None,
    "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/job_id",
    "TargetSettingsURI": None,
    "@odata.type": "#DellJob.v1_6_0.DellJob",
    "CompletionTime": "2025-04-15T06:01:14",
    "@odata.context": "/redfish/v1/$metadata#DellJob.DellJob"
}


class TestLcJobStatus(TestUtils):

    def test_get_lifecycle_controller_job_status_info(self, idrac_mock):
        idrac_mock.invoke_request.return_value.json_data = RESPONSE
        idrac_lc_job_status_info = IDRACLifecycleControllerJobStatusInfo(idrac_mock)
        idrac_lc_job_status_info.get_lifecycle_controller_job_list = \
            MagicMock(return_value=JOB_RESPONSE)
        result = idrac_lc_job_status_info.get_lifecycle_controller_job_status_info(job_id="job_id")
        expected_result = {
            '@odata.context': '/redfish/v1/$metadata#DellJob.DellJob',
            '@odata.etag': 'W/"gen-31"',
            '@odata.id': '/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/job_id',
            '@odata.type': '#DellJob.v1_6_0.DellJob',
            'ActualRunningStartTime': None,
            'ActualRunningStopTime': None,
            'CompletionTime': '2025-04-15T06:01:14',
            'Description': 'Job Instance',
            'EndTime': None,
            'Id': 'job_id',
            'JobState': 'Failed',
            'JobType': 'FirmwareUpdate',
            'Message': 'Unable to parse the lc_validator_output.xml file because of an internal '
            'error.',
            'MessageArgs': [],
            'MessageArgs@odata.count': 0,
            'MessageId': 'RED106',
            'Name': 'update:new',
            'PercentComplete': 100,
            'StartTime': '2025-04-15T06:01:03',
            'TargetSettingsURI': None,
        }
        assert result == expected_result

    def test_get_lifecycle_controller_job_list(self, idrac_mock):
        JOB_LIST_RESPONSE = {
            "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs",
            "@odata.etag": "W/\"gen-1\"",
            "@odata.context": "/redfish/v1/$metadata#DellJobCollection.DellJobCollection",
            "@odata.type": "#DellJobCollection.DellJobCollection",
            "Description": "Collection of Job Instances",
            "Members": [
                {
                    "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/job_id"
                }
            ],
            "Members@odata.count": 1,
            "Name": "JobQueue"
        }
        idrac_mock.invoke_request.return_value.json_data = JOB_LIST_RESPONSE
        idrac_lc_job_status_info = IDRACLifecycleControllerJobStatusInfo(idrac_mock)
        idrac_lc_job_status_info.get_lifecycle_controller_job_details = \
            MagicMock(return_value=JOB_RESPONSE)
        result = idrac_lc_job_status_info.get_lifecycle_controller_job_list(
            job_id="job_id",
            jobs=RESPONSE["Oem"]["Dell"]["Jobs"]["@odata.id"])
        expected_result = {
            '@odata.context': '/redfish/v1/$metadata#DellJob.DellJob',
            '@odata.etag': 'W/"gen-31"',
            '@odata.id': '/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/job_id',
            '@odata.type': '#DellJob.v1_6_0.DellJob',
            'ActualRunningStartTime': None,
            'ActualRunningStopTime': None,
            'CompletionTime': '2025-04-15T06:01:14',
            'Description': 'Job Instance',
            'EndTime': None,
            'Id': 'job_id',
            'JobState': 'Failed',
            'JobType': 'FirmwareUpdate',
            'Message': 'Unable to parse the lc_validator_output.xml file because of an internal '
            'error.',
            'MessageArgs': [],
            'MessageArgs@odata.count': 0,
            'MessageId': 'RED106',
            'Name': 'update:new',
            'PercentComplete': 100,
            'StartTime': '2025-04-15T06:01:03',
            'TargetSettingsURI': None,
        }
        assert result == expected_result

    def test_get_lifecycle_controller_job_details(self, idrac_mock):
        JOB_MEMBERS_RESPONSE = [
            {
                "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/job_id"
            }
        ]
        idrac_mock.invoke_request.return_value = JOB_RESPONSE
        idrac_lc_job_status_info = IDRACLifecycleControllerJobStatusInfo(idrac_mock)
        result = idrac_lc_job_status_info.get_lifecycle_controller_job_details(
            job_id="job_id",
            members=JOB_MEMBERS_RESPONSE)
        expected_result = {
            '@odata.context': '/redfish/v1/$metadata#DellJob.DellJob',
            '@odata.etag': 'W/"gen-31"',
            '@odata.id': '/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/job_id',
            '@odata.type': '#DellJob.v1_6_0.DellJob',
            'ActualRunningStartTime': None,
            'ActualRunningStopTime': None,
            'CompletionTime': '2025-04-15T06:01:14',
            'Description': 'Job Instance',
            'EndTime': None,
            'Id': 'job_id',
            'JobState': 'Failed',
            'JobType': 'FirmwareUpdate',
            'Message': 'Unable to parse the lc_validator_output.xml file because of an internal '
            'error.',
            'MessageArgs': [],
            'MessageArgs@odata.count': 0,
            'MessageId': 'RED106',
            'Name': 'update:new',
            'PercentComplete': 100,
            'StartTime': '2025-04-15T06:01:03',
            'TargetSettingsURI': None,
        }
        assert result == expected_result

    def test_get_lifecycle_controller_job_status_info_success(self, idrac_mock):
        JOB_SUCCESS_RESPONSE = {
            "Description": "Job Instance",
            "MessageId": "RED106",
            "Message": "Job is successful",
            "Name": "update:new",
            "StartTime": "2025-04-15T06:01:03",
            "ActualRunningStopTime": None,
            "@odata.etag": "W/\"gen-31\"",
            "Id": "job_id",
            "EndTime": None,
            "PercentComplete": 100,
            "JobType": "FirmwareUpdate",
            "MessageArgs": ["Successfully updated the firmware"],
            "MessageArgs@odata.count": 0,
            "JobState": "Success",
            "ActualRunningStartTime": None,
            "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/job_id",
            "TargetSettingsURI": None,
            "@odata.type": "#DellJob.v1_6_0.DellJob",
            "CompletionTime": "2025-04-15T06:01:14",
            "@odata.context": "/redfish/v1/$metadata#DellJob.DellJob"
        }
        idrac_lc_job_status_info = IDRACLifecycleControllerJobStatusInfo(idrac_mock)
        idrac_lc_job_status_info.get_lifecycle_controller_job_status_info = \
            MagicMock(return_value=JOB_SUCCESS_RESPONSE)
        result = idrac_lc_job_status_info.transform_job_status_data(info_data=JOB_SUCCESS_RESPONSE)
        expected_result = {
            "Description": "Job Instance",
            "MessageID": "RED106",
            "Message": "Job is successful",
            "Name": "update:new",
            "JobStartTime": "2025-04-15T06:01:03",
            "ActualRunningStopTime": "None",
            "InstanceID": "job_id",
            "EndTime": "None",
            "PercentComplete": "100",
            "JobType": "FirmwareUpdate",
            "MessageArguments": "Successfully updated the firmware",
            "JobStatus": "Success",
            "ActualRunningStartTime": "None",
            "TargetSettingsURI": "None",
            "CompletionTime": "2025-04-15T06:01:14",
            "ElapsedTimeSinceCompletion": "",
            "JobUntilTime": "NA",
            "Status": "Success"
        }
        assert result == expected_result

    def test_get_lifecycle_controller_job_status_info_failed(self, idrac_mock):
        idrac_lc_job_status_info = IDRACLifecycleControllerJobStatusInfo(idrac_mock)
        idrac_lc_job_status_info.get_lifecycle_controller_job_status_info = \
            MagicMock(return_value=JOB_RESPONSE)
        result = idrac_lc_job_status_info.transform_job_status_data(info_data=JOB_RESPONSE)
        expected_result = {
            "Description": "Job Instance",
            "MessageID": "RED106",
            "Message": "Unable to parse the lc_validator_output.xml file because of an internal error.",
            "Name": "update:new",
            "JobStartTime": "2025-04-15T06:01:03",
            "ActualRunningStopTime": "None",
            "InstanceID": "job_id",
            "EndTime": "None",
            "PercentComplete": "100",
            "JobType": "FirmwareUpdate",
            "MessageArguments": "",
            "JobStatus": "Failed",
            "ActualRunningStartTime": "None",
            "TargetSettingsURI": "None",
            "CompletionTime": "2025-04-15T06:01:14",
            "ElapsedTimeSinceCompletion": "",
            "JobUntilTime": "NA",
            "Status": "Failed"
        }
        assert result == expected_result

    def test_get_lifecycle_controller_job_status_info_pending(self, idrac_mock):
        JOB_PENDING_RESPONSE = {
            "Description": "Job Instance",
            "MessageId": "RED106",
            "Message": "Job is in running state",
            "Name": "update:new",
            "StartTime": "2025-04-15T06:01:03",
            "ActualRunningStopTime": None,
            "@odata.etag": "W/\"gen-31\"",
            "Id": "job_id",
            "EndTime": None,
            "PercentComplete": 80,
            "JobType": "FirmwareUpdate",
            "MessageArgs": [],
            "MessageArgs@odata.count": 0,
            "JobState": "Pending",
            "ActualRunningStartTime": None,
            "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/job_id",
            "TargetSettingsURI": None,
            "@odata.type": "#DellJob.v1_6_0.DellJob",
            "CompletionTime": "",
            "@odata.context": "/redfish/v1/$metadata#DellJob.DellJob"
        }
        idrac_lc_job_status_info = IDRACLifecycleControllerJobStatusInfo(idrac_mock)
        idrac_lc_job_status_info.get_lifecycle_controller_job_status_info = MagicMock(
            return_value=JOB_PENDING_RESPONSE)
        result = idrac_lc_job_status_info.transform_job_status_data(info_data=JOB_PENDING_RESPONSE)
        expected_result = {
            "Description": "Job Instance",
            "MessageID": "RED106",
            "Message": "Job is in running state",
            "Name": "update:new",
            "JobStartTime": "2025-04-15T06:01:03",
            "ActualRunningStopTime": "None",
            "InstanceID": "job_id",
            "EndTime": "None",
            "PercentComplete": "80",
            "JobType": "FirmwareUpdate",
            "MessageArguments": "",
            "JobStatus": "Pending",
            "ActualRunningStartTime": "None",
            "TargetSettingsURI": "None",
            "CompletionTime": "",
            "ElapsedTimeSinceCompletion": "",
            "JobUntilTime": "NA",
            "Status": "InProgress"
        }
        assert result == expected_result
