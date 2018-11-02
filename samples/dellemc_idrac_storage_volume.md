View Single volume:

"msg": {
        "Message": {
            "RAID.Slot.1-1": {
                "VirtualDisk": {
                    "Disk.Virtual.0:RAID.Slot.1-1": {
                        "PhysicalDisk": [
                            "Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1",
                            "Disk.Bay.2:Enclosure.Internal.0-1:RAID.Slot.1-1",
                            "Disk.Bay.19:Enclosure.Internal.0-1:RAID.Slot.1-1"
                        ]
                    }
                }
            }
        },
        "Status": "Success"
    }
	

View All volume:

"msg": {
        "Message": {
            "Controller": {
                "RAID.Embedded.1-1": {},
                "RAID.Slot.1-1": {
                    "Enclosure": {
                        "Enclosure.Internal.0-1:RAID.Slot.1-1": {
                            "PhysicalDisk": [
                                "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.2:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.3:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.4:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.5:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.6:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.7:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.8:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.9:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.10:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.11:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.12:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.13:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.14:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.15:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.16:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.17:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.18:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.19:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.20:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.21:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.22:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.23:Enclosure.Internal.0-1:RAID.Slot.1-1"
                            ]
                        }
                    },
                    "VirtualDisk": {
                        "Disk.Virtual.0:RAID.Slot.1-1": {
                            "PhysicalDisk": [
                                "Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.2:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.19:Enclosure.Internal.0-1:RAID.Slot.1-1"
                            ]
                        },
                        "Disk.Virtual.1:RAID.Slot.1-1": {
                            "PhysicalDisk": [
                                "Disk.Bay.3:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.5:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.7:Enclosure.Internal.0-1:RAID.Slot.1-1",
                                "Disk.Bay.22:Enclosure.Internal.0-1:RAID.Slot.1-1"
                            ]
                        }
                    }
                }
            }
        },
        "Status": "Success"
    }

Volume Create and Delete:

"msg": {
        "@odata.context": "/redfish/v1/$metadata#DellJob.DellJob",
        "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_XXXXXXXXXXXX",
        "@odata.type": "#DellJob.v1_0_0.DellJob",
        "CompletionTime": "2018-08-02T18:23:48",
        "Description": "Job Instance",
        "EndTime": null,
        "Id": "JID_XXXXXXXXXXXX",
        "JobState": "Completed",
        "JobType": "ImportConfiguration",
        "Message": "Successfully imported and applied Server Configuration Profile.",
        "MessageArgs": [],
        "MessageId": "XXXXXX",
        "Name": "Import Configuration",
        "PercentComplete": 100,
        "StartTime": "TIME_NOW",
        "Status": "Success",
        "TargetSettingsURI": null,
        "retval": true
    }
