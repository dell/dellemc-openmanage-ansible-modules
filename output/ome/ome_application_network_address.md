Complete network settings for ome 3.3+
{
    "changed": true,
    "msg": "Successfully triggered job to update network address configuration"
    "network_configuration": {
        "Delay": 0,
        "DnsConfiguration": {
            "DnsDomainName": "",
            "DnsName": "MX-SVCTAG",
            "RegisterWithDNS": false,
            "UseDHCPForDNSDomainName": true
        },
        "EnableNIC": true,
        "Ipv4Configuration": {
            "Enable": true,
            "EnableDHCP": false,
            "StaticAlternateDNSServer": "",
            "StaticGateway": "192.168.0.2",
            "StaticIPAddress": "192.168.0.3",
            "StaticPreferredDNSServer": "192.168.0.4",
            "StaticSubnetMask": "255.255.254.0",
            "UseDHCPForDNSServerNames": false
        },
        "Ipv6Configuration": {
            "Enable": true,
            "EnableAutoConfiguration": true,
            "StaticAlternateDNSServer": "",
            "StaticGateway": "",
            "StaticIPAddress": "",
            "StaticPreferredDNSServer": "",
            "StaticPrefixLength": 0,
            "UseDHCPForDNSServerNames": true
        },
        "ManagementVLAN": {
            "EnableVLAN": false,
            "Id": 1
        }
    },
    "job_info": {
        "Builtin": false,
        "CreatedBy": "system",
        "Editable": true,
        "EndTime": null,
        "Id": 14902,
        "JobDescription": "Generic OME runtime task",
        "JobName": "OMERealtime_Task",
        "JobStatus": {
            "Id": 2080,
            "Name": "New"
        },
        "JobType": {
            "Id": 207,
            "Internal": true,
            "Name": "OMERealtime_Task"
        },
        "LastRun": null,
        "LastRunStatus": {
            "Id": 2080,
            "Name": "New"
        },
        "NextRun": null,
        "Params": [
            {
                "JobId": 14902,
                "Key": "Nmcli_Update",
                "Value": "{\"interfaceName\":\"eth0\",\"profileName\":\"eth0\",\"enableNIC\":true,\"ipv4Configuration\":{\"enable\":true,\"enableDHCP\":true,\"staticIPAddress\":\"\",\"staticSubnetMask\":\"\",\"staticGateway\":\"\",\"useDHCPForDNSServerNames\":true,\"staticPreferredDNSServer\":\"\",\"staticAlternateDNSServer\":\"\"},\"ipv6Configuration\":{\"enable\":false,\"enableAutoConfiguration\":true,\"staticIPAddress\":\"\",\"staticPrefixLength\":0,\"staticGateway\":\"\",\"useDHCPForDNSServerNames\":false,\"staticPreferredDNSServer\":\"\",\"staticAlternateDNSServer\":\"\"},\"managementVLAN\":{\"enableVLAN\":false,\"id\":0},\"dnsConfiguration\":{\"registerWithDNS\":false,\"dnsName\":\"\",\"useDHCPForDNSDomainName\":false,\"dnsDomainName\":\"\",\"fqdndomainName\":\"\",\"ipv4CurrentPreferredDNSServer\":\"\",\"ipv4CurrentAlternateDNSServer\":\"\",\"ipv6CurrentPreferredDNSServer\":\"\",\"ipv6CurrentAlternateDNSServer\":\"\"},\"currentSettings\":{\"ipv4Address\":[],\"ipv4Gateway\":\"\",\"ipv4Dns\":[],\"ipv4Domain\":\"\",\"ipv6Address\":[],\"ipv6LinkLocalAddress\":\"\",\"ipv6Gateway\":\"\",\"ipv6Dns\":[],\"ipv6Domain\":\"\"},\"delay\":0,\"primaryInterface\":true,\"modifiedConfigs\":{}}"
            }
        ],
        "Schedule": "startnow",
        "StartTime": null,
        "State": "Enabled",
        "Targets": [],
        "UpdatedBy": null,
        "Visible": true
    }
}

When no changes required
{
    "msg": "No changes made to network configuration as entered values are the same as current configured values"
    "network_configuration": {
        "Delay": 0,
        "DnsConfiguration": {
            "DnsDomainName": "",
            "DnsName": "MX-SVCTAG",
            "RegisterWithDNS": false,
            "UseDHCPForDNSDomainName": true
        },
        "EnableNIC": true,
        "Ipv4Configuration": {
            "Enable": true,
            "EnableDHCP": false,
            "StaticAlternateDNSServer": "",
            "StaticGateway": "192.168.0.2",
            "StaticIPAddress": "192.168.0.3",
            "StaticPreferredDNSServer": "192.168.0.4",
            "StaticSubnetMask": "255.255.254.0",
            "UseDHCPForDNSServerNames": false
        },
        "Ipv6Configuration": {
            "Enable": true,
            "EnableAutoConfiguration": true,
            "StaticAlternateDNSServer": "",
            "StaticGateway": "",
            "StaticIPAddress": "",
            "StaticPreferredDNSServer": "",
            "StaticPrefixLength": 0,
            "UseDHCPForDNSServerNames": true
        },
        "ManagementVLAN": {
            "EnableVLAN": false,
            "Id": 1
        }
    }
}