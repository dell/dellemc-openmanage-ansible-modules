Retrieve user account details:


"ansible_facts": {
    "192.168.0.1": {
        "@odata.context": "/api/$metadata#Collection(AccountService.Account)",
        "@odata.count": 1,
        "value": [
            {
                "@odata.id": "/api/AccountService/Accounts('111')",
                "@odata.type": "#AccountService.Account",
                "Description": "user name description",
                "DirectoryServiceId": 0,
                "Enabled": true,
                "Id": "111",
                "IsBuiltin": true,
                "Locked": false,
                "Name": "user_name",
                "Password": null,
                "RoleId": "11",
                "UserName": "user_name",
                "UserTypeId": 1
            }
        ]
    }
}
