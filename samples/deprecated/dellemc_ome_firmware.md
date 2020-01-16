
"update_status": {
    "Builtin": false,
    "CreatedBy": "user",
    "Editable": true,
    "EndTime": null,
    "Id": 11111,
    "JobDescription": "dup test",
    "JobName": "Firmware Update Task",
    "JobStatus": {
        "Id": 1111,
        "Name": "New"
    },
    "JobType": {
        "Id": 5,
        "Internal": false,
        "Name": "Update_Task"
    },
    "LastRun": null,
    "LastRunStatus": {
        "Id": 1111,
        "Name": "NotRun"
    },
    "NextRun": null,
    "Params": [
        {
            "JobId": 11111,
            "Key": "signVerify",
            "Value": "true"
        },
        {
            "JobId": 11111,
            "Key": "stagingValue",
            "Value": "false"
        },
        {
            "JobId": 11111,
            "Key": "complianceUpdate",
            "Value": "false"
        },
        {
            "JobId": 11111,
            "Key": "operationName",
            "Value": "INSTALL_FIRMWARE"
        }
    ],
    "Schedule": "startnow",
    "StartTime": null,
    "State": "Enabled",
    "Targets": [
        {
            "Data": "DCIM:INSTALLED#701__NIC.Mezzanine.1A-1-1=1111111111111",
            "Id": 11111,
            "JobId": 11111,
            "TargetType": {
                "Id": 1000,
                "Name": "DEVICE"
            }
        },
        {
            "Data": "DCIM:INSTALLED#701__NIC.Mezzanine.1A-1-1=1111111111111",
            "Id": 11111,
            "JobId": 11111,
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