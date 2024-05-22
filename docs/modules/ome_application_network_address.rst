.. _ome_application_network_address_module:


ome_application_network_address -- Updates the network configuration on OpenManage Enterprise
=============================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows the configuration of a DNS and an IPV4 or IPV6 network on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  enable_nic (optional, bool, True)
    Enable or disable Network Interface Card (NIC) configuration.


  interface_name (optional, str, None)
    If there are multiple interfaces, network configuration changes can be applied to a single interface using the interface name of the NIC.

    If this option is not specified, Primary interface is chosen by default.


  ipv4_configuration (optional, dict, None)
    IPv4 network configuration.

    \ :emphasis:`Warning`\  Ensure that you have an alternate interface to access OpenManage Enterprise as these options can change the current IPv4 address for \ :emphasis:`hostname`\ .


    enable (True, bool, None)
      Enable or disable access to the network using IPv4.


    enable_dhcp (optional, bool, None)
      Enable or disable the automatic request to get an IPv4 address from the IPv4 Dynamic Host Configuration Protocol (DHCP) server

      If \ :emphasis:`enable\_dhcp`\  option is true, OpenManage Enterprise retrieves the IP configuration—IPv4 address, subnet mask, and gateway from a DHCP server on the existing network.


    static_ip_address (optional, str, None)
      Static IPv4 address

      This option is applicable when \ :emphasis:`enable\_dhcp`\  is false.


    static_subnet_mask (optional, str, None)
      Static IPv4 subnet mask address

      This option is applicable when \ :emphasis:`enable\_dhcp`\  is false.


    static_gateway (optional, str, None)
      Static IPv4 gateway address

      This option is applicable when \ :emphasis:`enable\_dhcp`\  is false.


    use_dhcp_for_dns_server_names (optional, bool, None)
      This option allows to automatically request and obtain a DNS server IPv4 address from the DHCP server.

      This option is applicable when \ :emphasis:`enable\_dhcp`\  is true.


    static_preferred_dns_server (optional, str, None)
      Static IPv4 DNS preferred server

      This option is applicable when \ :emphasis:`use\_dhcp\_for\_dns\_server\_names`\  is false.


    static_alternate_dns_server (optional, str, None)
      Static IPv4 DNS alternate server

      This option is applicable when \ :emphasis:`use\_dhcp\_for\_dns\_server\_names`\  is false.



  ipv6_configuration (optional, dict, None)
    IPv6 network configuration.

    \ :emphasis:`Warning`\  Ensure that you have an alternate interface to access OpenManage Enterprise as these options can change the current IPv6 address for \ :emphasis:`hostname`\ .


    enable (True, bool, None)
      Enable or disable access to the network using the IPv6.


    enable_auto_configuration (optional, bool, None)
      Enable or disable the automatic request to get an IPv6 address from the IPv6 DHCP server or router advertisements(RA)

      If \ :emphasis:`enable\_auto\_configuration`\  is true, OME retrieves IP configuration-IPv6 address, prefix, and gateway, from a DHCPv6 server on the existing network


    static_ip_address (optional, str, None)
      Static IPv6 address

      This option is applicable when \ :emphasis:`enable\_auto\_configuration`\  is false.


    static_prefix_length (optional, int, None)
      Static IPv6 prefix length

      This option is applicable when \ :emphasis:`enable\_auto\_configuration`\  is false.


    static_gateway (optional, str, None)
      Static IPv6 gateway address

      This option is applicable when \ :emphasis:`enable\_auto\_configuration`\  is false.


    use_dhcp_for_dns_server_names (optional, bool, None)
      This option allows to automatically request and obtain a DNS server IPv6 address from the DHCP server.

      This option is applicable when \ :emphasis:`enable\_auto\_configuration`\  is true


    static_preferred_dns_server (optional, str, None)
      Static IPv6 DNS preferred server

      This option is applicable when \ :emphasis:`use\_dhcp\_for\_dns\_server\_names`\  is false.


    static_alternate_dns_server (optional, str, None)
      Static IPv6 DNS alternate server

      This option is applicable when \ :emphasis:`use\_dhcp\_for\_dns\_server\_names`\  is false.



  management_vlan (optional, dict, None)
    vLAN configuration.

    These settings are applicable for OpenManage Enterprise Modular.


    enable_vlan (True, bool, None)
      Enable or disable vLAN for management.

      The vLAN configuration cannot be updated if the \ :emphasis:`register\_with\_dns`\  field under \ :emphasis:`dns\_configuration`\  is true.

      \ :emphasis:`WARNING`\  Ensure that the network cable is plugged to the correct port after the vLAN configuration changes have been made. If not, the configuration change may not be effective.


    vlan_id (optional, int, None)
      vLAN ID.

      This option is applicable when \ :emphasis:`enable\_vlan`\  is true.



  dns_configuration (optional, dict, None)
    Domain Name System(DNS) settings.


    register_with_dns (optional, bool, None)
      Register/Unregister \ :emphasis:`dns\_name`\  on the DNS Server.

      This option cannot be updated if vLAN configuration changes.


    use_dhcp_for_dns_domain_name (optional, bool, None)
      Get the \ :emphasis:`dns\_domain\_name`\  using a DHCP server.


    dns_name (optional, str, None)
      DNS name for \ :emphasis:`hostname`\ 

      This is applicable when \ :emphasis:`register\_with\_dns`\  is true.


    dns_domain_name (optional, str, None)
      Static DNS domain name

      This is applicable when \ :emphasis:`use\_dhcp\_for\_dns\_domain\_name`\  is false.



  reboot_delay (optional, int, None)
    The time in seconds, after which settings are applied.

    This option is not mandatory.


  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (False, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.

    If the username is not provided, then the environment variable \ :envvar:`OME\_USERNAME`\  is used.

    Example: export OME\_USERNAME=username


  password (False, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.

    If the password is not provided, then the environment variable \ :envvar:`OME\_PASSWORD`\  is used.

    Example: export OME\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`OME\_X\_AUTH\_TOKEN`\  is used.

    Example: export OME\_X\_AUTH\_TOKEN=x\_auth\_token


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.


  validate_certs (optional, bool, True)
    If \ :literal:`false`\ , the SSL certificates will not be validated.

    Configure \ :literal:`false`\  only on personally controlled sites where self-signed certificates are used.

    Prior to collection version \ :literal:`5.0.0`\ , the \ :emphasis:`validate\_certs`\  is \ :literal:`false`\  by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - The configuration changes can only be applied to one interface at a time.
   - The system management consoles might be unreachable for some time after the configuration changes are applied.
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: IPv4 network configuration for primary interface
      dellemc.openmanage.ome_application_network_address:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        enable_nic: true
        ipv4_configuration:
          enable: true
          enable_dhcp: false
          static_ip_address: 192.168.0.2
          static_subnet_mask: 255.255.254.0
          static_gateway: 192.168.0.3
          use_dhcp_for_dns_server_names: false
          static_preferred_dns_server: 192.168.0.4
          static_alternate_dns_server: 192.168.0.5
        reboot_delay: 5

    - name: IPv6 network configuration for primary interface
      dellemc.openmanage.ome_application_network_address:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        ipv6_configuration:
          enable: true
          enable_auto_configuration: true
          static_ip_address: 2626:f2f2:f081:9:1c1c:f1f1:4747:1
          static_prefix_length: 10
          static_gateway: 2626:f2f2:f081:9:1c1c:f1f1:4747:2
          use_dhcp_for_dns_server_names: true
          static_preferred_dns_server: 2626:f2f2:f081:9:1c1c:f1f1:4747:3
          static_alternate_dns_server: 2626:f2f2:f081:9:1c1c:f1f1:4747:4

    - name: Management vLAN configuration for primary interface
      dellemc.openmanage.ome_application_network_address:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        management_vlan:
          enable_vlan: true
          vlan_id: 3344
        dns_configuration:
          register_with_dns: false
        reboot_delay: 1

    - name: DNS settings
      dellemc.openmanage.ome_application_network_address:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        ipv4_configuration:
          enable: true
          use_dhcp_for_dns_server_names: false
          static_preferred_dns_server: 192.168.0.4
          static_alternate_dns_server: 192.168.0.5
        dns_configuration:
          register_with_dns: true
          use_dhcp_for_dns_domain_name: false
          dns_name: "MX-SVCTAG"
          dns_domain_name: "dnslocaldomain"

    - name: Disbale nic interface eth1
      dellemc.openmanage.ome_application_network_address:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        enable_nic: false
        interface_name: eth1

    - name: Complete network settings for interface eth1
      dellemc.openmanage.ome_application_network_address:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        enable_nic: true
        interface_name: eth1
        ipv4_configuration:
          enable: true
          enable_dhcp: false
          static_ip_address: 192.168.0.2
          static_subnet_mask: 255.255.254.0
          static_gateway: 192.168.0.3
          use_dhcp_for_dns_server_names: false
          static_preferred_dns_server: 192.168.0.4
          static_alternate_dns_server: 192.168.0.5
        ipv6_configuration:
          enable: true
          enable_auto_configuration: true
          static_ip_address: 2626:f2f2:f081:9:1c1c:f1f1:4747:1
          static_prefix_length: 10
          static_gateway: ffff::2607:f2b1:f081:9
          use_dhcp_for_dns_server_names: true
          static_preferred_dns_server: 2626:f2f2:f081:9:1c1c:f1f1:4747:3
          static_alternate_dns_server: 2626:f2f2:f081:9:1c1c:f1f1:4747:4
        dns_configuration:
          register_with_dns: true
          use_dhcp_for_dns_domain_name: false
          dns_name: "MX-SVCTAG"
          dns_domain_name: "dnslocaldomain"
        reboot_delay: 5



Return Values
-------------

msg (always, str, Successfully updated network address configuration)
  Overall status of the network address configuration change.


network_configuration (on success, dict, {'Delay': 0, 'DnsConfiguration': {'DnsDomainName': '', 'DnsName': 'MX-SVCTAG', 'RegisterWithDNS': False, 'UseDHCPForDNSDomainName': True}, 'EnableNIC': True, 'InterfaceName': 'eth0', 'PrimaryInterface': True, 'Ipv4Configuration': {'Enable': True, 'EnableDHCP': False, 'StaticAlternateDNSServer': '', 'StaticGateway': '192.168.0.2', 'StaticIPAddress': '192.168.0.3', 'StaticPreferredDNSServer': '192.168.0.4', 'StaticSubnetMask': '255.255.254.0', 'UseDHCPForDNSServerNames': False}, 'Ipv6Configuration': {'Enable': True, 'EnableAutoConfiguration': True, 'StaticAlternateDNSServer': '', 'StaticGateway': '', 'StaticIPAddress': '', 'StaticPreferredDNSServer': '', 'StaticPrefixLength': 0, 'UseDHCPForDNSServerNames': True}, 'ManagementVLAN': {'EnableVLAN': False, 'Id': 1}})
  Updated application network address configuration.


job_info (on success, dict, {'Builtin': False, 'CreatedBy': 'system', 'Editable': True, 'EndTime': None, 'Id': 14902, 'JobDescription': 'Generic OME runtime task', 'JobName': 'OMERealtime_Task', 'JobStatus': {'Id': 2080, 'Name': 'New'}, 'JobType': {'Id': 207, 'Internal': True, 'Name': 'OMERealtime_Task'}, 'LastRun': None, 'LastRunStatus': {'Id': 2080, 'Name': 'New'}, 'NextRun': None, 'Params': [{'JobId': 14902, 'Key': 'Nmcli_Update', 'Value': '{"interfaceName":"eth0","profileName":"eth0","enableNIC":true, "ipv4Configuration":{"enable":true,"enableDHCP":true,"staticIPAddress":"", "staticSubnetMask":"","staticGateway":"","useDHCPForDNSServerNames":true, "staticPreferredDNSServer":"","staticAlternateDNSServer":""}, "ipv6Configuration":{"enable":false,"enableAutoConfiguration":true,"staticIPAddress":"", "staticPrefixLength":0,"staticGateway":"","useDHCPForDNSServerNames":false, "staticPreferredDNSServer":"","staticAlternateDNSServer":""}, "managementVLAN":{"enableVLAN":false,"id":0},"dnsConfiguration":{"registerWithDNS":false, "dnsName":"","useDHCPForDNSDomainName":false,"dnsDomainName":"","fqdndomainName":"", "ipv4CurrentPreferredDNSServer":"","ipv4CurrentAlternateDNSServer":"", "ipv6CurrentPreferredDNSServer":"","ipv6CurrentAlternateDNSServer":""}, "currentSettings":{"ipv4Address":[],"ipv4Gateway":"","ipv4Dns":[],"ipv4Domain":"", "ipv6Address":[],"ipv6LinkLocalAddress":"","ipv6Gateway":"","ipv6Dns":[], "ipv6Domain":""},"delay":0,"primaryInterface":true,"modifiedConfigs":{}}'}], 'Schedule': 'startnow', 'StartTime': None, 'State': 'Enabled', 'Targets': [], 'UpdatedBy': None, 'Visible': True})
  Details of the job to update in case OME version is \>= 3.3.


error_info (on HTTP error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to update the address configuration because a dependent field is missing for  Use DHCP for DNS Domain Name, Enable DHCP for ipv4 or Enable Autoconfig for ipv6 settings for valid configuration .', 'MessageArgs': ['Use DHCP for DNS Domain Name, Enable DHCP for ipv4 or Enable Autoconfig for ipv6 settings for valid configuration'], 'MessageId': 'CAPP1304', 'RelatedProperties': [], 'Resolution': 'Make sure that all dependent fields contain valid content and retry the operation.', 'Severity': 'Critical'}], 'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.'}})
  Details of the HTTP error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

