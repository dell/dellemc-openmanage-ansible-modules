Configure System time.
{
    "changed": true,
    "msg": "Successfully configured network time.",
    "time_configuration": {
        "EnableNTP": false,
        "JobId": null,
        "PrimaryNTPAddress": null,
        "SecondaryNTPAddress1": null,
        "SecondaryNTPAddress2": null,
        "SystemTime": null,
        "TimeSource": "Local Clock",
        "TimeZone": "TZ_ID_1",
        "TimeZoneIdLinux": null,
        "TimeZoneIdWindows": null,
        "UtcTime": null
    }
}


Configure NTP Server for time synchronization.
{
    "changed": true,
    "msg": "Successfully configured network time.",
    "proxy_setting": {
        "EnableNTP": true,
        "JobId": null,
        "PrimaryNTPAddress": "192.168.0.2",
        "SecondaryNTPAddress1": "192.168.0.3",
        "SecondaryNTPAddress2": "192.168.0.4",
        "SystemTime": null,
        "TimeSource": "192.168.0.4",
        "TimeZone": "TZ_ID_66",
        "TimeZoneIdLinux": null,
        "TimeZoneIdWindows": null,
        "UtcTime": null
    }
}

