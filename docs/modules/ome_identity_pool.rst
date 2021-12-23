.. _ome_identity_pool_module:


ome_identity_pool -- Manages identity pool settings on OpenManage Enterprise
============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to create, modify, or delete a single identity pool on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7.5



Parameters
----------

  state (optional, str, present)
    ``present`` modifies an existing identity pool. If the provided I (pool_name) does not exist, it creates an identity pool. - ``absent`` deletes an existing identity pool.


  pool_name (True, str, None)
    This option is mandatory for *state* when creating, modifying and deleting an identity pool.


  new_pool_name (optional, str, None)
    After creating an identity pool, *pool_name* can be changed to *new_pool_name*.

    This option is ignored when creating an identity pool.


  pool_description (optional, str, None)
    Description of the identity pool.


  ethernet_settings (optional, dict, None)
    Applicable for creating and modifying an identity pool using Ethernet settings.

    *starting_mac_address* and *identity_count* are required to create an identity pool.


    starting_mac_address (optional, str, None)
      Starting MAC address of the ethernet setting.


    identity_count (optional, int, None)
      Number of MAC addresses.



  fcoe_settings (optional, dict, None)
    Applicable for creating and modifying an identity pool using FCoE settings.

    *starting_mac_address* and *identity_count* are required to create an identity pool.


    starting_mac_address (optional, str, None)
      Starting MAC Address of the FCoE setting.


    identity_count (optional, int, None)
      Number of MAC addresses.



  iscsi_settings (optional, dict, None)
    Applicable for creating and modifying an identity pool using ISCSI settings.

    *starting_mac_address*, *identity_count*, *iqn_prefix*, *ip_range* and *subnet_mask* are required to create an identity pool.


    starting_mac_address (optional, str, None)
      Starting MAC address of the iSCSI setting.This is required option for iSCSI setting.


    identity_count (optional, int, None)
      Number of MAC addresses.


    initiator_config (optional, dict, None)
      Applicable for creating and modifying an identity pool using iSCSI Initiator settings.


      iqn_prefix (optional, str, None)
        IQN prefix addresses.



    initiator_ip_pool_settings (optional, dict, None)
      Applicable for creating and modifying an identity pool using ISCSI Initiator IP pool settings.


      ip_range (optional, str, None)
        Range of non-multicast IP addresses.


      subnet_mask (optional, str, None)
        Subnet mask for *ip_range*.


      gateway (optional, str, None)
        IP address of gateway.


      primary_dns_server (optional, str, None)
        IP address of the primary DNS server.


      secondary_dns_server (optional, str, None)
        IP address of the secondary DNS server.




  fc_settings (optional, dict, None)
    Applicable for creating and modifying an identity pool using fibre channel(FC) settings.

    This option allows OpenManage Enterprise to generate a Worldwide port name (WWPN) and Worldwide node name (WWNN) address.

    The value 0x2001 is beginning to the starting address for the generation of a WWPN, and 0x2000 for a WWNN.

    *starting_address* and *identity_count* are required to create an identity pool.


    starting_address (optional, str, None)
      Starting MAC Address of FC setting.*starting_address* is required to option to create FC settings.


    identity_count (optional, int, None)
      Number of MAC addresses.*identity_count* is required to option to create FC settings.



  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.


  password (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.





Notes
-----

.. note::
   - Run this module from a system that has direct access to DellEMC OpenManage Enterprise.
   - This module does not support ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create an identity pool using ethernet, FCoE, iSCSI and FC settings
      dellemc.openmanage.ome_identity_pool:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        state: present
        pool_name: "pool1"
        pool_description: "Identity pool with Ethernet, FCoE, iSCSI and FC settings"
        ethernet_settings:
            starting_mac_address: "50:50:50:50:50:00"
            identity_count: 60
        fcoe_settings:
            starting_mac_address: "70:70:70:70:70:00"
            identity_count: 75
        iscsi_settings:
            starting_mac_address: "60:60:60:60:60:00"
            identity_count: 30
            initiator_config:
                iqn_prefix: "iqn.myprefix."
            initiator_ip_pool_settings:
                ip_range: "10.33.0.1-10.33.0.255"
                subnet_mask: "255.255.255.0"
                gateway: "192.168.4.1"
                primary_dns_server : "10.8.8.8"
                secondary_dns_server : "8.8.8.8"
        fc_settings:
            starting_address: "30:30:30:30:30:00"
            identity_count: 45

    - name: Create an identity pool using only ethernet settings
      dellemc.openmanage.ome_identity_pool:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        pool_name: "pool2"
        pool_description: "create identity pool with ethernet"
        ethernet_settings:
            starting_mac_address: "aa-bb-cc-dd-ee-aa"
            identity_count: 80

    - name: Modify an identity pool
      dellemc.openmanage.ome_identity_pool:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        pool_name: "pool2"
        new_pool_name: "pool3"
        pool_description: "modifying identity pool with ethernet and fcoe settings"
        ethernet_settings:
            starting_mac_address: "90-90-90-90-90-90"
            identity_count: 61
        fcoe_settings:
            starting_mac_address: "aabb.ccdd.5050"
            identity_count: 77

    - name: Modify an identity pool using iSCSI and FC settings
      dellemc.openmanage.ome_identity_pool:
        hostname: "{{hostname}}"
        username: "{{username}}"
        password: "{{password}}"
        pool_name: "pool_new"
        new_pool_name: "pool_new2"
        pool_description: "modifying identity pool with iscsi and fc settings"
        iscsi_settings:
          identity_count: 99
          initiator_config:
            iqn_prefix: "iqn1.myprefix2."
          initiator_ip_pool_settings:
            gateway: "192.168.4.5"
        fc_settings:
          starting_address: "10:10:10:10:10:10"
          identity_count: 98

    - name: Delete an identity pool
      dellemc.openmanage.ome_identity_pool:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        state: "absent"
        pool_name: "pool2"



Return Values
-------------

msg (always, str, Successfully created an identity pool.)
  Overall status of the identity pool operation.


pool_status (success, dict, {'Id': 29, 'IsSuccessful': True, 'Issues': []})
  Details of the user operation, when *state* is ``present``.


error_info (on HTTP error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to process the request because an error occurred: Ethernet-MAC Range overlap found (in this Identity Pool or in a different one) .', 'MessageArgs': ['Ethernet-MAC Range overlap found (in this Identity Pool or in a different one)"'], 'MessageId': 'CGEN6001', 'RelatedProperties': [], 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.', 'Severity': 'Critical'}], 'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.'}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Sajna Shetty(@Sajna-Shetty)
- Deepak Joshi(@Dell-Deepak-Joshi))

