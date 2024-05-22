.. _ome_device_quick_deploy_module:


ome_device_quick_deploy -- Configure Quick Deploy settings on OpenManage Enterprise Modular.
============================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to configure the Quick Deploy settings of the server or IOM on OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  device_id (optional, int, None)
    The ID of the chassis for which the Quick Deploy settings to be deployed.

    If the device ID is not specified, this module updates the Quick Deploy settings for the \ :emphasis:`hostname`\ .

    \ :emphasis:`device\_id`\  is mutually exclusive with \ :emphasis:`device\_service\_tag`\ .


  device_service_tag (optional, str, None)
    The service tag of the chassis for which the Quick Deploy settings to be deployed.

    If the device service tag is not specified, this module updates the Quick Deploy settings for the \ :emphasis:`hostname`\ .

    \ :emphasis:`device\_service\_tag`\  is mutually exclusive with \ :emphasis:`device\_id`\ .


  setting_type (True, str, None)
    The type of the Quick Deploy settings to be applied.

    \ :literal:`ServerQuickDeploy`\  to apply the server Quick Deploy settings.

    \ :literal:`IOMQuickDeploy`\  to apply the IOM Quick Deploy settings.


  job_wait (optional, bool, True)
    Determines whether to wait for the job completion or not.


  job_wait_timeout (optional, int, 120)
    The maximum wait time of \ :emphasis:`job\_wait`\  in seconds. The job is tracked only for this duration.

    This option is applicable when \ :emphasis:`job\_wait`\  is \ :literal:`true`\ .


  quick_deploy_options (True, dict, None)
    The Quick Deploy settings for server and IOM quick deploy.


    password (optional, str, None)
      The password to login to the server or IOM.

      The module will always report change when \ :emphasis:`password`\  option is added.


    ipv4_enabled (optional, bool, None)
      Enables or disables the IPv4 network.


    ipv4_network_type (optional, str, None)
      IPv4 network type.

      \ :emphasis:`ipv4\_network\_type`\  is required if \ :emphasis:`ipv4\_enabled`\  is \ :literal:`true`\ .

      \ :literal:`Static`\  to configure the static IP settings.

      \ :literal:`DHCP`\  to configure the Dynamic IP settings.


    ipv4_subnet_mask (optional, str, None)
      IPv4 subnet mask.

      \ :emphasis:`ipv4\_subnet\_mask`\  is required if \ :emphasis:`ipv4\_network\_type`\  is \ :literal:`Static`\ .


    ipv4_gateway (optional, str, None)
      IPv4 gateway.

      \ :emphasis:`ipv4\_gateway`\  is required if \ :emphasis:`ipv4\_network\_type`\  is \ :literal:`Static`\ .


    ipv6_enabled (optional, bool, None)
      Enables or disables the IPv6 network.


    ipv6_network_type (optional, str, None)
      IPv6 network type.

      \ :emphasis:`ipv6\_network\_type`\  is required if \ :emphasis:`ipv6\_enabled`\  is \ :literal:`true`\ .

      \ :literal:`Static`\  to configure the static IP settings.

      \ :literal:`DHCP`\  to configure the Dynamic IP settings.


    ipv6_prefix_length (optional, int, None)
      IPV6 prefix length.

      \ :emphasis:`ipv6\_prefix\_length`\  is required if \ :emphasis:`ipv6\_network\_type`\  is \ :literal:`Static`\ .


    ipv6_gateway (optional, str, None)
      IPv6 gateway.

      \ :emphasis:`ipv6\_gateway`\  is required if \ :emphasis:`ipv6\_network\_type`\  is \ :literal:`Static`\ .


    slots (optional, list, None)
      The slot configuration for the server or IOM.


      slot_id (True, int, None)
        The ID of the slot.


      slot_ipv4_address (optional, str, None)
        The IPv4 address of the slot.


      slot_ipv6_address (optional, str, None)
        The IPv6 address of the slot.


      vlan_id (optional, int, None)
        The ID of the VLAN.




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
   - Run this module from a system that has direct access to OpenManage Enterprise Modular.
   - This module supports \ :literal:`check\_mode`\ .
   - The module will always report change when \ :emphasis:`password`\  option is added.
   - If the chassis is a member of a multi-chassis group and it is assigned as a backup lead chassis, the operations performed on the chassis using this module may conflict with the management operations performed on the chassis through the lead chassis.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Configure server Quick Deploy settings of the chassis using device ID.
      dellemc.openmanage.ome_device_quick_deploy:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        device_id: 25011
        setting_type: ServerQuickDeploy
        ca_path: "/path/to/ca_cert.pem"
        quick_deploy_options:
          password: "password"
          ipv4_enabled: true
          ipv4_network_type: Static
          ipv4_subnet_mask: 255.255.255.0
          ipv4_gateway: 192.168.0.1
          ipv6_enabled: true
          ipv6_network_type: Static
          ipv6_prefix_length: 1
          ipv6_gateway: "::"
          slots:
            - slot_id: 1
              slot_ipv4_address: 192.168.0.2
              slot_ipv6_address: "::"
              vlan_id: 1
            - slot_id: 2
              slot_ipv4_address: 192.168.0.3
              slot_ipv6_address: "::"
              vlan_id: 2

    - name: Configure server Quick Deploy settings of the chassis using device service tag.
      dellemc.openmanage.ome_device_quick_deploy:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        device_service_tag: GHRT2RL
        setting_type: IOMQuickDeploy
        ca_path: "/path/to/ca_cert.pem"
        quick_deploy_options:
          password: "password"
          ipv4_enabled: true
          ipv4_network_type: Static
          ipv4_subnet_mask: 255.255.255.0
          ipv4_gateway: 192.168.0.1
          ipv6_enabled: true
          ipv6_network_type: Static
          ipv6_prefix_length: 1
          ipv6_gateway: "::"
          slots:
            - slot_id: 1
              slot_ipv4_address: 192.168.0.2
              slot_ipv6_address: "::"
              vlan_id: 1
            - slot_id: 2
              slot_ipv4_address: 192.168.0.3
              slot_ipv6_address: "::"
              vlan_id: 2



Return Values
-------------

msg (always, str, Successfully deployed the quick deploy settings.)
  Overall status of the device quick deploy settings.


job_id (when quick deploy job is submitted., int, 1234)
  The job ID of the submitted quick deploy job.


quick_deploy_settings (success, dict, {'DeviceId': 25011, 'SettingType': 'ServerQuickDeploy', 'ProtocolTypeV4': True, 'NetworkTypeV4': 'Static', 'IpV4Gateway': '192.168.0.1', 'IpV4SubnetMask': '255.255.255.0', 'ProtocolTypeV6': True, 'NetworkTypeV6': 'Static', 'PrefixLength': '2', 'IpV6Gateway': '::', 'slots': [{'DeviceId': 25011, 'DeviceCapabilities': [18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 41, 8, 7, 4, 3, 2, 1, 31, 30], 'DeviceIPV4Address': '192.168.0.2', 'DeviceIPV6Address': '::', 'Dhcpipv4': 'Disabled', 'Dhcpipv6': 'Disabled', 'Ipv4Enabled': 'Enabled', 'Ipv6Enabled': 'Enabled', 'Model': 'PowerEdge MX840c', 'SlotIPV4Address': '192.168.0.2', 'SlotIPV6Address': '::', 'SlotId': 1, 'SlotSelected': True, 'SlotSettingsApplied': True, 'SlotType': '2000', 'Type': '1000', 'VlanId': '1'}, {'DeviceId': 0, 'Model': '', 'SlotIPV4Address': '0.0.0.0', 'SlotIPV6Address': '::', 'SlotId': 2, 'SlotSelected': False, 'SlotSettingsApplied': False, 'SlotType': '2000', 'Type': '0'}, {'DeviceId': 0, 'Model': '', 'SlotIPV4Address': '0.0.0.0', 'SlotIPV6Address': '::', 'SlotId': 3, 'SlotSelected': False, 'SlotSettingsApplied': False, 'SlotType': '2000', 'Type': '0'}, {'DeviceId': 0, 'Model': '', 'SlotIPV4Address': '0.0.0.0', 'SlotIPV6Address': '::', 'SlotId': 4, 'SlotSelected': False, 'SlotSettingsApplied': False, 'SlotType': '2000', 'Type': '0'}, {'DeviceId': 0, 'Model': '', 'SlotIPV4Address': '0.0.0.0', 'SlotIPV6Address': '::', 'SlotId': 5, 'SlotSelected': False, 'SlotSettingsApplied': False, 'SlotType': '2000', 'Type': '0'}, {'DeviceId': 0, 'Model': '', 'SlotIPV4Address': '0.0.0.0', 'SlotIPV6Address': '::', 'SlotId': 6, 'SlotSelected': False, 'SlotSettingsApplied': False, 'SlotType': '2000', 'Type': '0'}, {'DeviceId': 0, 'Model': '', 'SlotIPV4Address': '0.0.0.0', 'SlotIPV6Address': '::', 'SlotId': 7, 'SlotSelected': False, 'SlotSettingsApplied': False, 'SlotType': '2000', 'Type': '0'}, {'DeviceId': 0, 'Model': '', 'SlotIPV4Address': '0.0.0.0', 'SlotIPV6Address': '::', 'SlotId': 8, 'SlotSelected': False, 'SlotSettingsApplied': False, 'SlotType': '2000', 'Type': '0'}]})
  returned when quick deploy settings are deployed successfully.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)
- Shivam Sharma (@ShivamSh3)
- Kritika Bhateja (@Kritika-Bhateja-03)

