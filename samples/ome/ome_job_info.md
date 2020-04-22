Get job details for id.:

"job_info": {
	"@odata.context": "/api/$metadata#JobService.Job/$entity",
	"@odata.id": "/api/JobService/Jobs(10016)",
	"@odata.type": "#JobService.Job",
	"Builtin": true,
	"CreatedBy": "admin",
	"Editable": false,
	"EndTime": null,
	"ExecutionHistories@odata.navigationLink": "/api/JobService/Jobs(10016)/ExecutionHistories",
	"Id": 10016,
	"JobDescription": "Default Inventory Task",
	"JobName": "Default Inventory Task",
	"JobStatus": {
		"@odata.type": "#JobService.JobStatus",
		"Id": 2020,
		"Name": "Scheduled"
	},
	"JobType": {
		"@odata.type": "#JobService.JobType",
		"Id": 8,
		"Internal": false,
		"Name": "Inventory_Task"
	},
	"LastRun": "2019-01-31 08:30:00.206",
	"LastRunStatus": {
		"@odata.type": "#JobService.JobStatus",
		"Id": 2060,
		"Name": "Completed"
	},
	"NextRun": "2019-01-31 09:00:00.0",
	"Params": [
		{
			"JobId": 10016,
			"Key": "defaultInventoryTask",
			"Value": "TRUE"
		}
	],
	"Schedule": "0 0/30 * 1/1 * ? *",
	"StartTime": null,
	"State": "Enabled",
	"Targets": [
		{
			"Data": "All-Devices",
			"Id": 500,
			"JobId": 10016,
			"TargetType": {
				"Id": 6000,
				"Name": "GROUP"
			}
		}
	],
	"UpdatedBy": null,
	"Visible": false
},
"msg": "Successfully fetched the job info"

Get all job details filtered.:

"job_info": {
	"@odata.context": "/api/$metadata#Collection(JobService.Job)",
	"@odata.count": 687,
	"@odata.nextLink": "/api/JobService/Jobs?$skip=3&$top=2",
	"value": [
		{
			"@odata.id": "/api/JobService/Jobs(35910)",
			"@odata.type": "#JobService.Job",
			"Builtin": false,
			"CreatedBy": "system",
			"Editable": true,
			"EndTime": null,
			"ExecutionHistories@odata.navigationLink": "/api/JobService/Jobs(35910)/ExecutionHistories",
			"Id": 35910,
			"JobDescription": "Refresh Inventory for Device",
			"JobName": "Refresh Inventory for Device",
			"JobStatus": {
				"@odata.type": "#JobService.JobStatus",
				"Id": 2080,
				"Name": "New"
			},
			"JobType": {
				"@odata.type": "#JobService.JobType",
				"Id": 8,
				"Internal": false,
				"Name": "Inventory_Task"
			},
			"LastRun": "2019-01-29 10:51:34.776",
			"LastRunStatus": {
				"@odata.type": "#JobService.JobStatus",
				"Id": 2060,
				"Name": "Completed"
			},
			"NextRun": null,
			"Params": [],
			"Schedule": "",
			"StartTime": null,
			"State": "Enabled",
			"Targets": [
				{
					"Data": "''",
					"Id": 25010,
					"JobId": 35910,
					"TargetType": {
						"Id": 1000,
						"Name": "DEVICE"
					}
				}
			],
			"UpdatedBy": null,
			"Visible": true
		},
		{
			"@odata.id": "/api/JobService/Jobs(35909)",
			"@odata.type": "#JobService.Job",
			"Builtin": false,
			"CreatedBy": "system",
			"Editable": true,
			"EndTime": null,
			"ExecutionHistories@odata.navigationLink": "/api/JobService/Jobs(35909)/ExecutionHistories",
			"Id": 35909,
			"JobDescription": "Refresh Inventory for Device",
			"JobName": "Refresh Inventory for Device",
			"JobStatus": {
				"@odata.type": "#JobService.JobStatus",
				"Id": 2080,
				"Name": "New"
			},
			"JobType": {
				"@odata.type": "#JobService.JobType",
				"Id": 8,
				"Internal": false,
				"Name": "Inventory_Task"
			},
			"LastRun": "2019-01-29 10:51:29.84",
			"LastRunStatus": {
				"@odata.type": "#JobService.JobStatus",
				"Id": 2060,
				"Name": "Completed"
			},
			"NextRun": null,
			"Params": [],
			"Schedule": "",
			"StartTime": null,
			"State": "Enabled",
			"Targets": [
				{
					"Data": "''",
					"Id": 25010,
					"JobId": 35909,
					"TargetType": {
						"Id": 1000,
						"Name": "DEVICE"
					}
				}
			],
			"UpdatedBy": null,
			"Visible": true
		}
	]
},
"msg": "Successfully fetched the job info"