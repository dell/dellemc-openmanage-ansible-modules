Update webserver port and session time out configuration.
{
    "changed": true,
    "msg": "Successfully updated network web server configuration.",
    "webserver_configuration": {
        "TimeOut": 20,
        "PortNumber": 443,
        "EnableWebServer": true
        }
}

Update webserver port and session time out configuration in check mode
{
    "changed": true,
    "msg": "Changes found to be updated for web server."
}

No Changes found to apply 
{
    "msg": "No changes made to web server configuration as entered values 
    are the same as current configured values",
    "webserver_configuration": {
        "EnableWebServer": true,
        "PortNumber": 443,
        "TimeOut": 25
    }
}

No Changes found to apply in check mode
{
    "changed": true,
    "msg": "No changes found to be updated for web server."
}