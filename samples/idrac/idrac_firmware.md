
{
    "msg": "Successfully updated the firmware.",
    "update_status": {
        "@odata.context": "/redfish/v1/$metadata#DellJob.DellJob",
        "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_844222726048",
        "@odata.type": "#DellJob.v1_0_1.DellJob",
        "CompletionTime": "2020-03-17T00:18:10",
        "Description": "Job Instance",
        "EndTime": null,
        "Id": "JID_844222726048",
        "JobState": "Completed",
        "JobType": "RepositoryUpdate",
        "Message": "Job completed successfully.",
        "MessageArgs": [
            "NA"
        ],
        "MessageId": "RED001",
        "Name": "Repository Update",
        "PercentComplete": 100,
        "StartTime": "TIME_NOW",
        "Status": "Success",
        "TargetSettingsURI": null,
        "job_details": {
            "@Message.ExtendedInfo": [
                {
                    "Message": "Successfully Completed Request",
                    "MessageArgs": [],
                    "MessageArgs@odata.count": 0,
                    "MessageId": "Base.1.2.Success",
                    "RelatedProperties": [],
                    "RelatedProperties@odata.count": 0,
                    "Resolution": "None",
                    "Severity": "OK"
                }
            ],
            "PackageList": [
                {
                    "BaseLocation": null,
                    "ComponentID": "25227",
                    "ComponentType": "FRMW",
                    "Criticality": "1",
                    "DisplayName": "iDRAC with Lifecycle Controller, 4.00.00.00",
                    "JobID": "JID_844222910040",
                    "PackageName": "iDRAC-with-Lifecycle-Controller_Firmware_4JCPK_WN64_4.00.00.00_A00.EXE",
                    "PackagePath": "FOLDER05945466M/2/iDRAC-with-Lifecycle-Controller_Firmware_4JCPK_WN64_4.00.00.00_A00.EXE",
                    "PackageVersion": "4.00.00.00",
                    "RebootType": "IDRAC",
                    "Target": "DCIM:INSTALLED#iDRAC.Embedded.1-1#IDRACinfo"
                }
            ]
        },
        "retval": true
    }
}
