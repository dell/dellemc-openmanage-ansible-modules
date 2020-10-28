Port breakout configuration status:

"breakout_status": {
    "Builtin": false,
    "CreatedBy": "root",
    "Editable": true,
    "EndTime": null,
    "Id": 11111,
    "JobDescription": "",
    "JobName": "Breakout Port",
    "JobStatus": {
        "Id": 1112,
        "Name": "New"
    },
    "JobType": {
        "Id": 3,
        "Internal": false,
        "Name": "DeviceAction_Task"
    },
    "LastRun": null,
    "LastRunStatus": {
        "Id": 1113,
        "Name": "NotRun"
    },
    "NextRun": null,
    "Params": [
        {
            "JobId": 11112,
            "Key": "operationName",
            "Value": "CONFIGURE_PORT_BREAK_OUT"
        },
        {
            "JobId": 34206,
            "Key": "interfaceId",
            "Value": "2HB7NX2:phy-port1/1/11"
        },
        {
            "JobId": 34206,
            "Key": "breakoutType",
            "Value": "1X40GE"
        }
    ],
    "Schedule": "startnow",
    "StartTime": null,
    "State": "Enabled",
    "Targets": [
        {
            "Data": "",
            "Id": 25017,
            "JobId": 34206,
            "TargetType": {
                "Id": 1000,
                "Name": "DEVICE"
            }
        }
    ],
    "UpdatedBy": null,
    "UserGenerated": true,
    "Visible": true
}