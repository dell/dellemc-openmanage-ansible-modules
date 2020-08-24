Get all available firmware baseline infomation:
{
    "baseline_info": {
        "@odata.context": "/api/$metadata#Collection(UpdateService.Baselines)",
        "@odata.count": 3,
        "value": [
            {
                "@odata.id": "/api/UpdateService/Baselines(229)",
                "@odata.type": "#UpdateService.Baselines",
                "CatalogId": 22,
                "ComplianceSummary": {
                    "ComplianceStatus": "DOWNGRADE",
                    "NumberOfCritical": 0,
                    "NumberOfDowngrade": 1,
                    "NumberOfNormal": 0,
                    "NumberOfWarning": 0
                },
                "Description": "Description for Dell EMC Ansible Demo Baseline 2",
                "DeviceComplianceReports@odata.navigationLink": "/api/UpdateService/Baselines(229)/DeviceComplianceReports",
                "DowngradeEnabled": true,
                "Id": 229,
                "Is64Bit": true,
                "LastRun": "2020-05-22 16:42:40.178",
                "Name": "Dell EMC Ansible Demo Baseline 2",
                "RepositoryId": 12,
                "RepositoryName": "HTTP DELL",
                "RepositoryType": "DELL_ONLINE",
                "Targets": [
                    {
                        "Id": 10085,
                        "Type": {
                            "Id": 1000,
                            "Name": "DEVICE"
                        }
                    }
                ],
                "TaskId": 10167,
                "TaskStatusId": 2060
            },
            {
                "@odata.id": "/api/UpdateService/Baselines(230)",
                "@odata.type": "#UpdateService.Baselines",
                "CatalogId": 22,
                "ComplianceSummary": {
                    "ComplianceStatus": "DOWNGRADE",
                    "NumberOfCritical": 0,
                    "NumberOfDowngrade": 1,
                    "NumberOfNormal": 0,
                    "NumberOfWarning": 0
                },
                "Description": "Baseline Description 1",
                "DeviceComplianceReports@odata.navigationLink": "/api/UpdateService/Baselines(230)/DeviceComplianceReports",
                "DowngradeEnabled": true,
                "Id": 230,
                "Is64Bit": true,
                "LastRun": "2020-05-22 16:42:40.278",
                "Name": "Baseline 1",
                "RepositoryId": 12,
                "RepositoryName": "HTTP DELL",
                "RepositoryType": "DELL_ONLINE",
                "Targets": [
                    {
                        "Id": 10085,
                        "Type": {
                            "Id": 1000,
                            "Name": "DEVICE"
                        }
                    }
                ],
                "TaskId": 10964,
                "TaskStatusId": 2060
            },
            {
                "@odata.id": "/api/UpdateService/Baselines(239)",
                "@odata.type": "#UpdateService.Baselines",
                "CatalogId": 22,
                "ComplianceSummary": {
                    "ComplianceStatus": "CRITICAL",
                    "NumberOfCritical": 1,
                    "NumberOfDowngrade": 0,
                    "NumberOfNormal": 0,
                    "NumberOfWarning": 0
                },
                "Description": "baseline_description",
                "DeviceComplianceReports@odata.navigationLink": "/api/UpdateService/Baselines(239)/DeviceComplianceReports",
                "DowngradeEnabled": true,
                "Id": 239,
                "Is64Bit": true,
                "LastRun": "2020-05-22 16:42:40.307",
                "Name": "baseline_name",
                "RepositoryId": 12,
                "RepositoryName": "HTTP DELL",
                "RepositoryType": "DELL_ONLINE",
                "Targets": [
                    {
                        "Id": 10342,
                        "Type": {
                            "Id": 1000,
                            "Name": "DEVICE"
                        }
                    }
                ],
                "TaskId": 41415,
                "TaskStatusId": 2060
            },
        ]
    },
    "changed": false,
    "msg": "Successfully fetched firmware baseline information."
}



Get specified firmware baseline infomation:
 {
    "baseline_info": {
        "@odata.id": "/api/UpdateService/Baselines(239)",
        "@odata.type": "#UpdateService.Baselines",
        "CatalogId": 22,
        "ComplianceSummary": {
            "ComplianceStatus": "CRITICAL",
            "NumberOfCritical": 1,
            "NumberOfDowngrade": 0,
            "NumberOfNormal": 0,
            "NumberOfWarning": 0
        },
        "Description": "baseline_description",
        "DeviceComplianceReports@odata.navigationLink": "/api/UpdateService/Baselines(239)/DeviceComplianceReports",
        "DowngradeEnabled": true,
        "Id": 239,
        "Is64Bit": true,
        "LastRun": "2020-05-22 16:42:40.307",
        "Name": "baseline_name",
        "RepositoryId": 12,
        "RepositoryName": "HTTP DELL",
        "RepositoryType": "DELL_ONLINE",
        "Targets": [
            {
                "Id": 10342,
                "Type": {
                    "Id": 1000,
                    "Name": "DEVICE"
                }
            }
        ],
        "TaskId": 41415,
        "TaskStatusId": 2060
    },
    "changed": false,
    "msg": "Successfully fetched firmware baseline information."
}
