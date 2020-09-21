
For 14 generation server response:

    "msg": {
        "@Message.ExtendedInfo": [
            {
                "Message": "Successfully Completed Request",
                "MessageArgs": [],
                "MessageArgs@odata.count": 0,
                "MessageId": "Base.1.0.Success",
                "RelatedProperties": [],
                "RelatedProperties@odata.count": 0,
                "Resolution": "None",
                "Severity": "OK"
            },
            {
                "Message": "The operation successfully completed.",
                "MessageArgs": [],
                "MessageArgs@odata.count": 0,
                "MessageId": "IDRAC.1.6.SYS413",
                "RelatedProperties": [],
                "RelatedProperties@odata.count": 0,
                "Resolution": "No response action is required.",
                "Severity": "Informational"
            }
        ]
    }

For 12 generation and 13 generation server response:

    "msg": {
        "@odata.context": "/redfish/v1/$metadata#Task.Task",
        "@odata.id": "/redfish/v1/TaskService/Tasks/JID_991107662746",
        "@odata.type": "#Task.v1_0_2.Task",
        "Description": "Server Configuration and other Tasks running on iDRAC are listed here",
        "EndTime": "2020-09-03T00:26:17-05:00",
        "Id": "JID_991107662746",
        "Messages": [
            {
                "Oem": {
                    "Dell": {
                        "@odata.type": "#DellManager.v1_0_0.ServerConfigurationProfileResults",
                        "DisplayValue": "SNMP V3 Protocol Enable",
                        "ErrCode": "0",
                        "Name": "Users.6#ProtocolEnable",
                        "NewValue": "Enabled",
                        "OldValue": "Disabled"
                    }
                },
                "Severity": "OK"
            },
            {
                "Oem": {
                    "Dell": {
                        "@odata.type": "#DellManager.v1_0_0.ServerConfigurationProfileResults",
                        "DisplayValue": "User Admin IPMI LAN Privilege",
                        "ErrCode": "0",
                        "Name": "Users.6#IpmiLanPrivilege",
                        "NewValue": "User",
                        "OldValue": "No Access"
                    }
                },
                "Severity": "OK"
            },
            {
                "Oem": {
                    "Dell": {
                        "@odata.type": "#DellManager.v1_0_0.ServerConfigurationProfileResults",
                        "DisplayValue": "SNMP V3 Authentication Protocol",
                        "ErrCode": "0",
                        "Name": "Users.6#AuthenticationProtocol",
                        "NewValue": "MD5",
                        "OldValue": "SHA"
                    }
                },
                "Severity": "OK"
            },
            {
                "Oem": {
                    "Dell": {
                        "@odata.type": "#DellManager.v1_0_0.ServerConfigurationProfileResults",
                        "DisplayValue": "SNMP V3 Privacy Protocol",
                        "ErrCode": "0",
                        "Name": "Users.6#PrivacyProtocol",
                        "NewValue": "DES",
                        "OldValue": "AES"
                    }
                },
                "Severity": "OK"
            },
            {
                "Oem": {
                    "Dell": {
                        "@odata.type": "#DellManager.v1_0_0.ServerConfigurationProfileResults",
                        "DisplayValue": "User Admin Enable",
                        "ErrCode": "0",
                        "Name": "Users.6#Enable",
                        "NewValue": "Enabled",
                        "OldValue": "Disabled"
                    }
                },
                "Severity": "OK"
            },
            {
                "Oem": {
                    "Dell": {
                        "@odata.type": "#DellManager.v1_0_0.ServerConfigurationProfileResults",
                        "DisplayValue": "User Admin SOL Enable",
                        "ErrCode": "0",
                        "Name": "Users.6#SolEnable",
                        "NewValue": "Enabled",
                        "OldValue": "Disabled"
                    }
                },
                "Severity": "OK"
            },
            {
                "Oem": {
                    "Dell": {
                        "@odata.type": "#DellManager.v1_0_0.ServerConfigurationProfileResults",
                        "DisplayValue": "User Admin Privilege",
                        "ErrCode": "0",
                        "Name": "Users.6#Privilege",
                        "NewValue": "1",
                        "OldValue": "0"
                    }
                },
                "Severity": "OK"
            },
            {
                "Oem": {
                    "Dell": {
                        "@odata.type": "#DellManager.v1_0_0.ServerConfigurationProfileResults",
                        "DisplayValue": "User Admin User Name",
                        "ErrCode": "0",
                        "Name": "Users.6#UserName",
                        "NewValue": "test"
                    }
                },
                "Severity": "OK"
            },
            {
                "Oem": {
                    "Dell": {
                        "@odata.type": "#DellManager.v1_0_0.ServerConfigurationProfileResults",
                        "DisplayValue": "User Admin Password",
                        "ErrCode": "0",
                        "Name": "Users.6#Password",
                        "NewValue": "******",
                        "OldValue": "******"
                    }
                },
                "Severity": "OK"
            },
            {
                "Message": "Successfully imported and applied Server Configuration Profile.",
                "MessageArgs": [],
                "MessageArgs@odata.count": 0,
                "MessageId": "SYS053"
            }
        ],
        "Messages@odata.count": 10,
        "Name": "Import Configuration",
        "Oem": {
            "Dell": {
                "@odata.type": "#DellJob.v1_0_0.DellJob",
                "CompletionTime": "2020-09-03T00:26:17",
                "Description": "Job Instance",
                "EndTime": null,
                "Id": "JID_991107662746",
                "JobState": "Completed",
                "JobType": "ImportConfiguration",
                "Message": "Successfully imported and applied Server Configuration Profile.",
                "MessageArgs": [],
                "MessageId": "SYS053",
                "Name": "Import Configuration",
                "PercentComplete": 100,
                "StartTime": "TIME_NOW",
                "TargetSettingsURI": null
            }
        },
        "StartTime": "2020-09-03T00:26:06-05:00",
        "TaskState": "Completed",
        "TaskStatus": "OK"
