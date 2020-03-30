Update proxy configuration and enable authentication:
{
    "changed": true,
    "msg": "Successfully updated network proxy configuration.",
    "proxy_setting": {
        "EnableAuthentication": true,
        "EnableProxy": true,
        "IpAddress": "192.168.0.2",
        "Password": null,
        "PortNumber": 444,
        "Username": "root"
    }

}


Disable proxy authentication:
{
    "changed": true,
    "msg": "Successfully updated network proxy configuration.",
    "proxy_setting": {
        "EnableAuthentication": false,
        "EnableProxy": true,
        "IpAddress": "192.168.0.2",
        "Password": null,
        "PortNumber": 444,
        "Username": "root"
    }
}


Reset proxy configuration.:
{
    "changed": true,
    "msg": "Successfully updated network proxy configuration.",
    "proxy_setting": {
        "EnableAuthentication": false,
        "EnableProxy": false,
        "IpAddress": null,
        "Password": null,
        "PortNumber": 0,
        "Username": null
    }

}