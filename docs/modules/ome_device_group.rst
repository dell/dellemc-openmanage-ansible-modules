.. _ome_device_group_module:


ome_device_group -- Add devices to a static device group on OpenManage Enterprise
=================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to add devices to a static device group on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7.5
- netaddr >= 0.7.19



Parameters
----------

  state (optional, str, present)
    ``present`` allows to add the device(s) to a static device group.

    ``absent`` currently, this feature is not supported.


  name (optional, str, None)
    Name of the static group to which device(s) need to be added.

    *name* is mutually exclusive with *group_id*.


  group_id (optional, int, None)
    ID of the static device group to which device(s) need to be added.

    *group_id* is mutually exclusive with *name*.


  device_ids (optional, list, None)
    List of ID(s) of the device(s) to be added to the device group.

    *device_ids* is mutually exclusive with *device_service_tags* and *ip_addresses*.


  device_service_tags (optional, list, None)
    List of service tag(s) of the device(s) to be added to the device group.

    *device_service_tags* is mutually exclusive with *device_ids* and *ip_addresses*.


  ip_addresses (optional, list, None)
    List of IPs of the device(s) to be added to the device group.

    *ip_addresses* is mutually exclusive with *device_ids* and *device_service_tags*.

    Supported  IP address range formats:

        - 192.35.0.1

        - 10.36.0.0-192.36.0.255

        - 192.37.0.0/24

        - fe80::ffff:ffff:ffff:ffff

        - fe80::ffff:192.0.2.0/125

        - fe80::ffff:ffff:ffff:1111-fe80::ffff:ffff:ffff:ffff

    ``NOTE`` Hostname is not supported.

    ``NOTE`` *ip_addresses* requires python's netaddr packages to work on IP Addresses.

    ``NOTE`` This module reports success even if one of the IP addresses provided in the *ip_addresses* list is available in OpenManage Enterprise.The module reports failure only if none of the IP addresses provided in the list are available in OpenManage Enterprise.


  hostname (True, str, None)
    OpenManage Enterprise IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise username.


  password (True, str, None)
    OpenManage Enterprise password.


  port (optional, int, 443)
    OpenManage Enterprise HTTPS port.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell EMC OpenManage Enterprise.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Add devices to a static device group by using the group name and device IDs
      dellemc.openmanage.ome_device_group:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        name: "Storage Services"
        device_ids:
          - 11111
          - 11112
          - 11113

    - name: Add devices to a static device group by using the group name and device service tags
      dellemc.openmanage.ome_device_group:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        name: "Storage Services"
        device_service_tags:
          - GHRT2RL
          - KJHDF3S
          - LKIJNG6

    - name: Add devices to a static device group by using the group ID and device service tags
      dellemc.openmanage.ome_device_group:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        group_id: 12345
        device_service_tags:
          - GHRT2RL
          - KJHDF3S

    - name: Add devices to a static device group by using the group name and IPv4 addresses
      dellemc.openmanage.ome_device_group:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        name: "Storage Services"
        ip_addresses:
          - 192.35.0.1
          - 192.35.0.5

    - name: Add devices to a static device group by using the group ID and IPv6 addresses
      dellemc.openmanage.ome_device_group:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        group_id: 12345
        ip_addresses:
          - fe80::ffff:ffff:ffff:ffff
          - fe80::ffff:ffff:ffff:2222

    - name: Add devices to a static device group by using the group ID and supported IPv4 and IPv6 address formats.
      dellemc.openmanage.ome_device_group:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        group_id: 12345
        ip_addresses:
          - 192.35.0.1
          - 10.36.0.0-192.36.0.255
          - 192.37.0.0/24
          - fe80::ffff:ffff:ffff:ffff
          - ::ffff:192.0.2.0/125
          - fe80::ffff:ffff:ffff:1111-fe80::ffff:ffff:ffff:ffff



Return Values
-------------

msg (always, str, Successfully added member(s) to the device group.)
  Overall status of the device group settings.


group_id (success, int, 21078)
  ID of the group.


ip_addresses_added (success, list, 21078)
  IP Addresses which are added to the device group.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)
- Sajna Shetty(@Sajna-Shetty)

