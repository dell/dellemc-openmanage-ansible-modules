.. _idrac_network_info_module:


idrac_network_info -- Discover network device functions (NICs) on iDRAC
=======================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Discover all network device functions (NICs) on an iDRAC via the chassis\-scoped Redfish NetworkAdapters endpoint.

Returns rich metadata per NIC including ID, link status, MAC address, NIC type, speed capability, and media type.

Supports both iDRAC9 (16G) and iDRAC10 (17G) via dynamic URI resolution.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  force_refresh (False, bool, False)
    Force refresh of NIC discovery results, bypassing the in\-memory cache.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.

    If the username is not provided, then the environment variable :envvar:`IDRAC\_USERNAME` is used.

    Example: export IDRAC\_USERNAME=username


  idrac_password (True, str, None)
    iDRAC user password.

    If the password is not provided, then the environment variable :envvar:`IDRAC\_PASSWORD` is used.

    Example: export IDRAC\_PASSWORD=password


  idrac_port (optional, int, 443)
    iDRAC port.


  validate_certs (optional, bool, True)
    If :literal:`false`\ , the SSL certificates will not be validated.

    Configure :literal:`false` only on personally controlled sites where self\-signed certificates are used.

    Prior to collection version :literal:`5.0.0`\ , the :emphasis:`validate\_certs` is :literal:`false` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports both IPv4 and IPv6 address for :emphasis:`idrac\_ip`.
   - This module is read\-only and always returns changed=false.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Discover all NICs on iDRAC
      dellemc.openmanage.idrac_network_info:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"

    - name: Discover NICs with forced cache refresh
      dellemc.openmanage.idrac_network_info:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        force_refresh: true

    - name: Discover NICs and use results in subsequent tasks
      hosts: idrac_hosts
      tasks:
        - name: Get all NICs
          dellemc.openmanage.idrac_network_info:
            idrac_ip: "{{ idrac_ip }}"
            idrac_user: "{{ idrac_user }}"
            idrac_password: "{{ idrac_password }}"
          register: nic_result

        - name: Display NIC IDs
          ansible.builtin.debug:
            msg: "Found NIC: {{ item.id }}"
          loop: "{{ nic_result.network_device_functions }}"



Return Values
-------------

msg (always, str, Successfully discovered network device functions.)
  Overall status message.


network_device_functions (success, list, [{'id': 'NIC.Embedded.1-1-1', 'net_dev_func_type': 'Ethernet', 'mac_address': 'B0:26:28:E4:95:60', 'link_status': 'LinkUp', 'device_description': 'Embedded NIC 1 Port 1 Partition 1', 'link_speed': '10000 Mbps', 'media_type': 'Base-T'}])
  List of network device functions with rich metadata.


idrac_generation (success, int, 16)
  PowerEdge server generation (14G\-16G for iDRAC9, 17G+ for iDRAC10).


idrac_firmware_version (success, str, 7.30.30.50)
  iDRAC firmware version.


idrac_model (success, str, iDRAC 9)
  iDRAC model identifier.


redfish_error (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred.'}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Mangirish Kenkare(@MangirishK)

