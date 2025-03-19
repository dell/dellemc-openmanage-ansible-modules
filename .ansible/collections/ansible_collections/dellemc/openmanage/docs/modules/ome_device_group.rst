.. _ome_device_group_module:


ome_device_group -- Add or remove device(s) from a static device group on OpenManage Enterprise
===============================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to add or remove device(s) from a static device group on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6
- netaddr \>= 0.7.19



Parameters
----------

  state (optional, str, present)
    \ :literal:`present`\  allows to add the device(s) to a static device group.

    \ :literal:`absent`\  allows to remove the device(s) from a static device group.


  name (optional, str, None)
    Name of the static group.

    \ :emphasis:`name`\  is mutually exclusive with \ :emphasis:`group\_id`\ .


  group_id (optional, int, None)
    ID of the static device.

    \ :emphasis:`group\_id`\  is mutually exclusive with \ :emphasis:`name`\ .


  device_ids (optional, list, None)
    List of ID(s) of the device(s) to be added or removed from the device group.

    \ :emphasis:`device\_ids`\  is mutually exclusive with \ :emphasis:`device\_service\_tags`\  and \ :emphasis:`ip\_addresses`\ .


  device_service_tags (optional, list, None)
    List of service tag(s) of the device(s) to be added or removed from the device group.

    \ :emphasis:`device\_service\_tags`\  is mutually exclusive with \ :emphasis:`device\_ids`\  and \ :emphasis:`ip\_addresses`\ .


  ip_addresses (optional, list, None)
    List of IPs of the device(s) to be added or removed from the device group.

    \ :emphasis:`ip\_addresses`\  is mutually exclusive with \ :emphasis:`device\_ids`\  and \ :emphasis:`device\_service\_tags`\ .

    Supported  IP address range formats:

        - 192.35.0.1

        - 10.36.0.0-192.36.0.255

        - 192.37.0.0/24

        - fe80::ffff:ffff:ffff:ffff

        - fe80::ffff:192.0.2.0/125

        - fe80::ffff:ffff:ffff:1111-fe80::ffff:ffff:ffff:ffff

    \ :literal:`NOTE`\  Hostname is not supported.

    \ :literal:`NOTE`\  \ :emphasis:`ip\_addresses`\  requires python's netaddr packages to work on IP Addresses.

    \ :literal:`NOTE`\  This module reports success even if one of the IP addresses provided in the \ :emphasis:`ip\_addresses`\  list is available in OpenManage Enterprise.The module reports failure only if none of the IP addresses provided in the list are available in OpenManage Enterprise.


  hostname (True, str, None)
    OpenManage Enterprise IP address or hostname.


  username (False, str, None)
    OpenManage Enterprise username.

    If the username is not provided, then the environment variable \ :envvar:`OME\_USERNAME`\  is used.

    Example: export OME\_USERNAME=username


  password (False, str, None)
    OpenManage Enterprise password.

    If the password is not provided, then the environment variable \ :envvar:`OME\_PASSWORD`\  is used.

    Example: export OME\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`OME\_X\_AUTH\_TOKEN`\  is used.

    Example: export OME\_X\_AUTH\_TOKEN=x\_auth\_token


  port (optional, int, 443)
    OpenManage Enterprise HTTPS port.


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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Add devices to a static device group by using the group name and device IDs
      dellemc.openmanage.ome_device_group:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
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
        ca_path: "/path/to/ca_cert.pem"
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
        ca_path: "/path/to/ca_cert.pem"
        group_id: 12345
        device_service_tags:
          - GHRT2RL
          - KJHDF3S

    - name: Add devices to a static device group by using the group name and IPv4 addresses
      dellemc.openmanage.ome_device_group:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        name: "Storage Services"
        ip_addresses:
          - 192.35.0.1
          - 192.35.0.5

    - name: Add devices to a static device group by using the group ID and IPv6 addresses
      dellemc.openmanage.ome_device_group:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        group_id: 12345
        ip_addresses:
          - fe80::ffff:ffff:ffff:ffff
          - fe80::ffff:ffff:ffff:2222

    - name: Add devices to a static device group by using the group ID and supported IPv4 and IPv6 address formats.
      dellemc.openmanage.ome_device_group:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        group_id: 12345
        ip_addresses:
          - 192.35.0.1
          - 10.36.0.0-192.36.0.255
          - 192.37.0.0/24
          - fe80::ffff:ffff:ffff:ffff
          - ::ffff:192.0.2.0/125
          - fe80::ffff:ffff:ffff:1111-fe80::ffff:ffff:ffff:ffff

    - name: Remove devices from a static device group by using the group name and device IDs
      dellemc.openmanage.ome_device_group:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "absent"
        name: "Storage Services"
        device_ids:
          - 11111
          - 11112
          - 11113

    - name: Remove devices from a static device group by using the group name and device service tags
      dellemc.openmanage.ome_device_group:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "absent"
        name: "Storage Services"
        device_service_tags:
          - GHRT2RL
          - KJHDF3S
          - LKIJNG6

    - name: Remove devices from a static device group by using the group ID and device service tags
      dellemc.openmanage.ome_device_group:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "absent"
        group_id: 12345
        device_service_tags:
          - GHRT2RL
          - KJHDF3S

    - name: Remove devices from a static device group by using the group name and IPv4 addresses
      dellemc.openmanage.ome_device_group:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "absent"
        name: "Storage Services"
        ip_addresses:
          - 192.35.0.1
          - 192.35.0.5

    - name: Remove devices from a static device group by using the group ID and IPv6 addresses
      dellemc.openmanage.ome_device_group:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "absent"
        group_id: 12345
        ip_addresses:
          - fe80::ffff:ffff:ffff:ffff
          - fe80::ffff:ffff:ffff:2222

    - name: Remove devices from a static device group by using the group ID and supported IPv4 and IPv6 address formats.
      dellemc.openmanage.ome_device_group:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "absent"
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

msg (always, str, ['Successfully added member(s) to the device group.'])
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
- Abhishek Sinha (@Abhishek-Dell)

