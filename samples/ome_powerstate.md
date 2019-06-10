
"job_status" : {
    "Builtin": false,
    "CreatedBy": "user",
    "Editable": true,
    "EndTime": null,
    "Id": 11111,
    "JobDescription": "DeviceAction_Task",
    "JobName": "DeviceAction_Task_PowerState",
    "JobStatus": {
        "Id": 1111,
        "Name": "New"
        },
    "JobType": {
        "Id": 1,
        "Internal": false,
        "Name": "DeviceAction_Task"
        },
    "LastRun": "2019-04-01 06:39:02.69",
    "LastRunStatus": {
        "Id": 1112,
        "Name": "Running"
        },
    "NextRun": null,
    "Params": [
        {
            "JobId": 11111,
            "Key": "powerState",
            "Value": "2"
        },
        {
            "JobId": 11111,
            "Key": "operationName",
            "Value": "POWER_CONTROL"
        }
    ],
    "Schedule": "",
    "StartTime": null,
    "State": "Enabled",
    "Targets": [
        {
            "Data": "",
            "Id": 11112,
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
