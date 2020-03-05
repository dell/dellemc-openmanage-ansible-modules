Export Server Configuration Profile:

{
    "changed": false,
    "msg": "Successfully triggered the job to export the Server Configuration
     Profile.",
    "scp_status": {
        "Data": {
            "StatusCode": 202,
            "jobid": "JID_XXXXXXXXXXXX",
            "next_ruri": "/redfish/v1/TaskService/Tasks/JID_XXXXXXXXXXXX"
        },
        "Job": {
            "JobId": "JID_XXXXXXXXXXXX",
            "ResourceURI": "/redfish/v1/TaskService/Tasks/JID_XXXXXXXXXXXX"
        },
        "Message": "none",
        "Return": "JobCreated",
        "Status": "Success",
        "StatusCode": 202,
        "file": "/tmp/192.168.0.1_20000101_101010_scp.json",
        "retval": true
    }
}

Import SCP from a network share and wait for this job to get completed

{
    "changed": true,
    "msg": "Successfully imported the Server Configuration Profile.",
    "scp_status": {
        "@odata.context": "/redfish/v1/$metadata#DellJob.DellJob",
        "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_XXXXXXXXXXXX",
        "@odata.type": "#DellJob.v1_0_0.DellJob",
        "CompletionTime": "2000-01-101T10:10:10",
        "Description": "Job Instance",
        "EndTime": null,
        "Id": "JID_XXXXXXXXXXXX",
        "JobState": "Completed",
        "JobType": "ImportConfiguration",
        "Message": "Successfully imported and applied Server Configuration Profile.",
        "MessageArgs": [],
        "MessageId": "ABC123",
        "Name": "Import Configuration",
        "PercentComplete": 100,
        "StartTime": "TIME_NOW",
        "Status": "Success",
        "TargetSettingsURI": null,
        "retval": true
    }
}
