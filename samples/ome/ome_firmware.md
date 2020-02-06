Firmware Update Job:

{
    "msg": "Successfully submitted the firmware update job.",
    "update_status": {
        "Builtin": false,
        "CreatedBy": "admin",
        "Editable": true,
        "EndTime": null,
        "Id": 29348,
        "JobDescription": "Firmware Update Task",
        "JobName": "Firmware Update Task",
        "JobStatus": {
            "Id": 2080,
            "Name": "New"
        },
        "JobType": {
            "Id": 5,
            "Internal": false,
            "Name": "Update_Task"
        },
        "LastRun": null,
        "LastRunStatus": {
            "Id": 2200,
            "Name": "NotRun"
        },
        "NextRun": null,
        "Params": [
            {
                "JobId": 29348,
                "Key": "signVerify",
                "Value": "true"
            },
            {
                "JobId": 29348,
                "Key": "stagingValue",
                "Value": "false"
            },
            {
                "JobId": 29348,
                "Key": "complianceUpdate",
                "Value": "false"
            },
            {
                "JobId": 29348,
                "Key": "operationName",
                "Value": "INSTALL_FIRMWARE"
            }
        ],
        "Schedule": "startnow",
        "StartTime": null,
        "State": "Enabled",
        "Targets": [
            {
                "Data": "DCIM:INSTALLED#741__BIOS.Setup.1-1=1579159285481",
                "Id": 28628,
                "JobId": 29348,
                "TargetType": {
                    "Id": 1000,
                    "Name": "DEVICE"
                }
            }
        ],
        "UpdatedBy": null,
        "Visible": true
    }
}