.. _idrac_network_module:


idrac_network -- Configures the iDRAC network attributes
========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to configure iDRAC network settings.



Requirements
------------
The below requirements are needed on the host that executes this module.

- omsdk \>= 1.2.488
- python \>= 3.9.6



Parameters
----------

  share_name (optional, str, None)
    (deprecated)Network share or a local path.

    This option is deprecated and will be removed in the later version.


  share_user (optional, str, None)
    (deprecated)Network share user name. Use the format 'user@domain' or 'domain\\user' if user is part of a domain. This option is mandatory for CIFS share.

    This option is deprecated and will be removed in the later version.


  share_password (optional, str, None)
    (deprecated)Network share user password. This option is mandatory for CIFS share.

    This option is deprecated and will be removed in the later version.


  share_mnt (optional, str, None)
    (deprecated)Local mount path of the network share with read-write permission for ansible user. This option is mandatory for network shares.

    This option is deprecated and will be removed in the later version.


  setup_idrac_nic_vlan (optional, str, None)
    Allows to configure VLAN on iDRAC.


  register_idrac_on_dns (optional, str, None)
    Registers iDRAC on a Domain Name System (DNS).


  dns_idrac_name (optional, str, None)
    Name of the DNS to register iDRAC.


  auto_config (optional, str, None)
    Allows to enable or disable auto-provisioning to automatically acquire domain name from DHCP.


  static_dns (optional, str, None)
    Enter the static DNS domain name.


  vlan_id (optional, int, None)
    Enter the VLAN ID.  The VLAN ID must be a number from 1 through 4094.


  vlan_priority (optional, int, None)
    Enter the priority for the VLAN ID. The priority value must be a number from 0 through 7.


  enable_nic (optional, str, None)
    Allows to enable or disable the Network Interface Controller (NIC) used by iDRAC.


  nic_selection (optional, str, None)
    Select one of the available NICs.


  failover_network (optional, str, None)
    Select one of the remaining LOMs. If a network fails, the traffic is routed through the failover network.


  auto_detect (optional, str, None)
    Allows to auto detect the available NIC types used by iDRAC.


  auto_negotiation (optional, str, None)
    Allows iDRAC to automatically set the duplex mode and network speed.


  network_speed (optional, str, None)
    Select the network speed for the selected NIC.


  duplex_mode (optional, str, None)
    Select the type of data transmission for the NIC.


  nic_mtu (optional, int, None)
    Maximum Transmission Unit of the NIC.


  ip_address (optional, str, None)
    Enter a valid iDRAC static IPv4 address.


  enable_dhcp (optional, str, None)
    Allows to enable or disable Dynamic Host Configuration Protocol (DHCP) in iDRAC.


  enable_ipv4 (optional, str, None)
    Allows to enable or disable IPv4 configuration.


  dns_from_dhcp (optional, str, None)
    Allows to enable DHCP to obtain DNS server address.


  static_dns_1 (optional, str, None)
    Enter the preferred static DNS server IPv4 address.


  static_dns_2 (optional, str, None)
    Enter the preferred static DNS server IPv4 address.


  static_gateway (optional, str, None)
    Enter the static IPv4 gateway address to iDRAC.


  static_net_mask (optional, str, None)
    Enter the static IP subnet mask to iDRAC.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.

    If the username is not provided, then the environment variable \ :envvar:`IDRAC\_USERNAME`\  is used.

    Example: export IDRAC\_USERNAME=username


  idrac_password (True, str, None)
    iDRAC user password.

    If the password is not provided, then the environment variable \ :envvar:`IDRAC\_PASSWORD`\  is used.

    Example: export IDRAC\_PASSWORD=password


  idrac_port (optional, int, 443)
    iDRAC port.


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
   - This module requires 'Administrator' privilege for \ :emphasis:`idrac\_user`\ .
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports both IPv4 and IPv6 address for \ :emphasis:`idrac\_ip`\ .
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Configure iDRAC network settings
      dellemc.openmanage.idrac_network:
           idrac_ip: "192.168.0.1"
           idrac_user: "user_name"
           idrac_password: "user_password"
           ca_path: "/path/to/ca_cert.pem"
           register_idrac_on_dns: Enabled
           dns_idrac_name: None
           auto_config: None
           static_dns: None
           setup_idrac_nic_vlan: Enabled
           vlan_id: 0
           vlan_priority: 1
           enable_nic: Enabled
           nic_selection: Dedicated
           failover_network: T_None
           auto_detect: Disabled
           auto_negotiation: Enabled
           network_speed: T_1000
           duplex_mode: Full
           nic_mtu: 1500
           ip_address: "192.168.0.1"
           enable_dhcp: Enabled
           enable_ipv4: Enabled
           static_dns_1: "192.168.0.1"
           static_dns_2: "192.168.0.1"
           dns_from_dhcp: Enabled
           static_gateway: None
           static_net_mask: None



Return Values
-------------

msg (always, str, Successfully configured the idrac network settings.)
  Successfully configured the idrac network settings.


network_status (success, dict, {'@odata.context': '/redfish/v1/$metadata#DellJob.DellJob', '@odata.id': '/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_856418531008', '@odata.type': '#DellJob.v1_0_2.DellJob', 'CompletionTime': '2020-03-31T03:04:15', 'Description': 'Job Instance', 'EndTime': None, 'Id': 'JID_856418531008', 'JobState': 'Completed', 'JobType': 'ImportConfiguration', 'Message': 'Successfully imported and applied Server Configuration Profile.', 'MessageArgs': [], 'MessageArgs@odata.count': 0, 'MessageId': 'SYS053', 'Name': 'Import Configuration', 'PercentComplete': 100, 'StartTime': 'TIME_NOW', 'Status': 'Success', 'TargetSettingsURI': None, 'retval': True})
  Status of the Network settings operation job.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------


- This module will be removed in version
  .
  *[deprecated]*


Authors
~~~~~~~

- Felix Stephen (@felixs88)
- Anooja Vardhineni (@anooja-vardhineni)

