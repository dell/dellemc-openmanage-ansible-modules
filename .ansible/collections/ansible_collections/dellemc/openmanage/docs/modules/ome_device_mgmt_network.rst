.. _ome_device_mgmt_network_module:


ome_device_mgmt_network -- Configure network settings of devices on OpenManage Enterprise Modular
=================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to configure network settings on Chassis, Servers, and I/O Modules on OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  device_service_tag (optional, str, None)
    Service tag of the device.

    This option is mutually exclusive with \ :emphasis:`device\_id`\ .


  device_id (optional, int, None)
    ID of the device.

    This option is mutually exclusive with \ :emphasis:`device\_service\_tag`\ .


  enable_nic (optional, bool, True)
    Enable or disable Network Interface Card (NIC) configuration of the device.

    This option is not applicable to I/O Module.


  delay (optional, int, 0)
    The time in seconds, after which settings are applied.

    This option is applicable only for Chassis.


  ipv4_configuration (optional, dict, None)
    IPv4 network configuration.

    \ :literal:`WARNING`\  Ensure that you have an alternate interface to access OpenManage Enterprise Modular because these options can change the current IPv4 address for \ :emphasis:`hostname`\ .


    enable_ipv4 (True, bool, None)
      Enable or disable access to the network using IPv4.


    enable_dhcp (optional, bool, None)
      Enable or disable the automatic request to obtain an IPv4 address from the IPv4 Dynamic Host Configuration Protocol (DHCP) server.

      \ :literal:`NOTE`\  If this option is \ :literal:`true`\ , the values provided for \ :emphasis:`static\_ip\_address`\ , \ :emphasis:`static\_subnet\_mask`\ , and \ :emphasis:`static\_gateway`\  are not applied for these fields. However, the module may report changes.


    static_ip_address (optional, str, None)
      Static IPv4 address

      This option is applicable when \ :emphasis:`enable\_dhcp`\  is false.


    static_subnet_mask (optional, str, None)
      Static IPv4 subnet mask address

      This option is applicable when \ :emphasis:`enable\_dhcp`\  is false.


    static_gateway (optional, str, None)
      Static IPv4 gateway address

      This option is applicable when \ :emphasis:`enable\_dhcp`\  is false.


    use_dhcp_to_obtain_dns_server_address (optional, bool, None)
      This option allows to automatically request and obtain IPv4 address for the DNS Server from the DHCP server.

      This option is applicable when \ :emphasis:`enable\_dhcp`\  is true.

      \ :literal:`NOTE`\  If this option is \ :literal:`true`\ , the values provided for \ :emphasis:`static\_preferred\_dns\_server`\  and \ :emphasis:`static\_alternate\_dns\_server`\  are not applied for these fields. However, the module may report changes.


    static_preferred_dns_server (optional, str, None)
      Static IPv4 DNS preferred server

      This option is applicable when \ :emphasis:`use\_dhcp\_for\_dns\_server\_names`\  is false.


    static_alternate_dns_server (optional, str, None)
      Static IPv4 DNS alternate server

      This option is applicable when \ :emphasis:`use\_dhcp\_for\_dns\_server\_names`\  is false.



  ipv6_configuration (optional, dict, None)
    IPv6 network configuration.

    \ :literal:`WARNING`\  Ensure that you have an alternate interface to access OpenManage Enterprise Modular because these options can change the current IPv6 address for \ :emphasis:`hostname`\ .


    enable_ipv6 (True, bool, None)
      Enable or disable access to the network using the IPv6.


    enable_auto_configuration (optional, bool, None)
      Enable or disable the automatic request to obtain an IPv6 address from the IPv6 DHCP server or router advertisements(RA)

      If \ :emphasis:`enable\_auto\_configuration`\  is \ :literal:`true`\ , OpenManage Enterprise Modular retrieves IP configuration (IPv6 address, prefix, and gateway address) from a DHCPv6 server on the existing network.

      \ :literal:`NOTE`\  If this option is \ :literal:`true`\ , the values provided for \ :emphasis:`static\_ip\_address`\ , \ :emphasis:`static\_prefix\_length`\ , and \ :emphasis:`static\_gateway`\  are not applied for these fields. However, the module may report changes.


    static_ip_address (optional, str, None)
      Static IPv6 address

      This option is applicable when \ :emphasis:`enable\_auto\_configuration`\  is false.


    static_prefix_length (optional, int, None)
      Static IPv6 prefix length

      This option is applicable when \ :emphasis:`enable\_auto\_configuration`\  is false.


    static_gateway (optional, str, None)
      Static IPv6 gateway address

      This option is applicable when \ :emphasis:`enable\_auto\_configuration`\  is false.


    use_dhcpv6_to_obtain_dns_server_address (optional, bool, None)
      This option allows to automatically request and obtain a IPv6 address for the DNS server from the DHCP server.

      This option is applicable when \ :emphasis:`enable\_auto\_configuration`\  is true

      \ :literal:`NOTE`\  If this option is \ :literal:`true`\ , the values provided for \ :emphasis:`static\_preferred\_dns\_server`\  and \ :emphasis:`static\_alternate\_dns\_server`\  are not applied for these fields. However, the module may report changes.


    static_preferred_dns_server (optional, str, None)
      Static IPv6 DNS preferred server

      This option is applicable when \ :emphasis:`use\_dhcp\_for\_dns\_server\_names`\  is false.


    static_alternate_dns_server (optional, str, None)
      Static IPv6 DNS alternate server

      This option is applicable when \ :emphasis:`use\_dhcp\_for\_dns\_server\_names`\  is false.



  management_vlan (optional, dict, None)
    VLAN configuration.


    enable_vlan (True, bool, None)
      Enable or disable VLAN for management.

      The VLAN configuration cannot be updated if the \ :emphasis:`register\_with\_dns`\  field under \ :emphasis:`dns\_configuration`\  is true.

      \ :literal:`WARNING`\  Ensure that the network cable is connected to the correct port after the VLAN configuration is changed. If not, the VLAN configuration changes may not be applied.


    vlan_id (optional, int, None)
      VLAN ID.

      The valid VLAN IDs are: 1 to 4000, and 4021 to 4094.

      This option is applicable when \ :emphasis:`enable\_vlan`\  is true.



  dns_configuration (optional, dict, None)
    Domain Name System(DNS) settings.


    register_with_dns (optional, bool, None)
      Register/Unregister \ :emphasis:`dns\_name`\  on the DNS Server.

      \ :literal:`WARNING`\  This option cannot be updated if VLAN configuration changes.


    use_dhcp_for_dns_domain_name (optional, bool, None)
      Get the \ :emphasis:`dns\_domain\_name`\  using a DHCP server.


    dns_name (optional, str, None)
      DNS name for \ :emphasis:`hostname`\ 

      This is applicable when \ :emphasis:`register\_with\_dns`\  is true.


    dns_domain_name (optional, str, None)
      Static DNS domain name

      This is applicable when \ :emphasis:`use\_dhcp\_for\_dns\_domain\_name`\  is false.


    auto_negotiation (optional, bool, None)
      Enables or disables the auto negation of the network speed.

      \ :literal:`NOTE`\ : Setting \ :emphasis:`auto\_negotiation`\  to false and choosing a network port speed may result in the chassis loosing link to the top of rack network switch, or to the neighboring chassis in case of MCM mode. It is recommended that the \ :emphasis:`auto\_negotiation`\  is set to \ :literal:`true`\  for most use cases.

      This is applicable when \ :emphasis:`use\_dhcp\_for\_dns\_domain\_name`\  is false.

      This is applicable only for Chassis.


    network_speed (optional, str, None)
      The speed of the network port.

      This is applicable when \ :emphasis:`auto\_negotiation`\  is false.

      \ :literal:`10\_MB`\  to select network speed of 10 MB.

      \ :literal:`100\_MB`\  to select network speed of 100 MB.

      This is applicable only for Chassis.



  dns_server_settings (optional, dict, None)
    DNS server settings.

    This is applicable only for I/O Module.


    preferred_dns_server (optional, str, None)
      Enter the IP address of the preferred DNS server.


    alternate_dns_server1 (optional, str, None)
      Enter the IP address of the first alternate DNS server.


    alternate_dns_server2 (optional, str, None)
      Enter the IP address of the second alternate DNS server.



  hostname (True, str, None)
    OpenManage Enterprise Modular IP address or hostname.


  username (False, str, None)
    OpenManage Enterprise Modular username.

    If the username is not provided, then the environment variable \ :envvar:`OME\_USERNAME`\  is used.

    Example: export OME\_USERNAME=username


  password (False, str, None)
    OpenManage Enterprise Modular password.

    If the password is not provided, then the environment variable \ :envvar:`OME\_PASSWORD`\  is used.

    Example: export OME\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`OME\_X\_AUTH\_TOKEN`\  is used.

    Example: export OME\_X\_AUTH\_TOKEN=x\_auth\_token


  port (optional, int, 443)
    OpenManage Enterprise Modular HTTPS port.


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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise Modular.
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Network settings for chassis
      dellemc.openmanage.ome_device_mgmt_network:
        hostname: 192.168.0.1
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_service_tag: CHAS123
        ipv4_configuration:
          enable_ipv4: true
          enable_dhcp: false
          static_ip_address: 192.168.0.2
          static_subnet_mask: 255.255.254.0
          static_gateway: 192.168.0.3
          use_dhcp_to_obtain_dns_server_address: false
          static_preferred_dns_server: 192.168.0.4
          static_alternate_dns_server: 192.168.0.5
        ipv6_configuration:
          enable_ipv6: true
          enable_auto_configuration: false
          static_ip_address: 2626:f2f2:f081:9:1c1c:f1f1:4747:1
          static_prefix_length: 10
          static_gateway: ffff::2607:f2b1:f081:9
          use_dhcpv6_to_obtain_dns_server_address: false
          static_preferred_dns_server: 2626:f2f2:f081:9:1c1c:f1f1:4747:3
          static_alternate_dns_server: 2626:f2f2:f081:9:1c1c:f1f1:4747:4
        dns_configuration:
          register_with_dns: true
          use_dhcp_for_dns_domain_name: false
          dns_name: "MX-SVCTAG"
          dns_domain_name: "dnslocaldomain"
          auto_negotiation: false
          network_speed: 100_MB

    - name: Network settings for server
      dellemc.openmanage.ome_device_mgmt_network:
        hostname: 192.168.0.1
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_service_tag: SRVR123
        ipv4_configuration:
          enable_ipv4: true
          enable_dhcp: false
          static_ip_address: 192.168.0.2
          static_subnet_mask: 255.255.254.0
          static_gateway: 192.168.0.3
          use_dhcp_to_obtain_dns_server_address: false
          static_preferred_dns_server: 192.168.0.4
          static_alternate_dns_server: 192.168.0.5
        ipv6_configuration:
          enable_ipv6: true
          enable_auto_configuration: false
          static_ip_address: 2626:f2f2:f081:9:1c1c:f1f1:4747:1
          static_prefix_length: 10
          static_gateway: ffff::2607:f2b1:f081:9
          use_dhcpv6_to_obtain_dns_server_address: false
          static_preferred_dns_server: 2626:f2f2:f081:9:1c1c:f1f1:4747:3
          static_alternate_dns_server: 2626:f2f2:f081:9:1c1c:f1f1:4747:4

    - name: Network settings for I/O module
      dellemc.openmanage.ome_device_mgmt_network:
        hostname: 192.168.0.1
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_service_tag: IOM1234
        ipv4_configuration:
          enable_ipv4: true
          enable_dhcp: false
          static_ip_address: 192.168.0.2
          static_subnet_mask: 255.255.254.0
          static_gateway: 192.168.0.3
        ipv6_configuration:
          enable_ipv6: true
          enable_auto_configuration: false
          static_ip_address: 2626:f2f2:f081:9:1c1c:f1f1:4747:1
          static_prefix_length: 10
          static_gateway: ffff::2607:f2b1:f081:9
        dns_server_settings:
          preferred_dns_server: 192.168.0.4
          alternate_dns_server1: 192.168.0.5

    - name: Management VLAN configuration of chassis using device id
      dellemc.openmanage.ome_device_mgmt_network:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_id: 12345
        management_vlan:
          enable_vlan: true
          vlan_id: 2345
        dns_configuration:
          register_with_dns: false



Return Values
-------------

msg (always, str, Successfully applied the network settings.)
  Overall status of the network config operation.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'CGEN1004', 'RelatedProperties': [], 'Message': 'Unable to complete the request because IPV4 Settings Capability is not Supported does not exist or is not applicable for the resource URI.', 'MessageArgs': ['IPV4 Settings Capability is not Supported'], 'Severity': 'Critical', 'Resolution': "Check the request resource URI. Refer to the OpenManage Enterprise-Modular User's Guide for more information about resource URI and its properties."}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

