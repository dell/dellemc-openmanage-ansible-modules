.. _ome_server_interface_profile_info_module:


ome_server_interface_profile_info -- Retrieves the information of server interface profile on OpenManage Enterprise Modular.
============================================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to retrieves the information of server interface profile on OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  device_id (optional, list, None)
    The ID of the device.

    *device_id* is mutually exclusive with *device_service_tag*.


  device_service_tag (optional, list, None)
    The service tag of the device.

    *device_service_tag* is mutually exclusive with *device_id*.


  hostname (True, str, None)
    OpenManage Enterprise Modular IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise Modular username.


  password (True, str, None)
    OpenManage Enterprise Modular password.


  port (optional, int, 443)
    OpenManage Enterprise Modular HTTPS port.


  validate_certs (optional, bool, True)
    If ``False``, the SSL certificates will not be validated.

    Configure ``False`` only on personally controlled sites where self-signed certificates are used.

    Prior to collection version ``5.0.0``, the *validate_certs* is ``False`` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to OpenManage Enterprise Modular.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Retrieves the server interface profiles of all the device using device ID.
      dellemc.openmanage.ome_server_interface_profile_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_id:
          - 10001
          - 10002

    - name: Retrieves the server interface profiles of all the device using device service tag.
      dellemc.openmanage.ome_server_interface_profile_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_service_tag:
          - 6GHH6H2
          - 6KHH6H3



Return Values
-------------

msg (on success, str, Successfully retrieved the server interface profile information.)
  Overall status of the server interface profile information.


server_profiles (success, list, [{'BondingTechnology': 'LACP', 'Id': '6KZK6K2', 'ServerInterfaceProfile': [{'FabricId': '1ea6bf64-3cf0-4e06-a136-5046d874d1e7', 'Id': 'NIC.Mezzanine.1A-1-1', 'NativeVLAN': 0, 'Networks': [{'CreatedBy': 'system', 'CreationTime': '2018-11-27 10:22:14.140', 'Description': 'VLAN 1', 'Id': 10001, 'InternalRefNWUUId': 'add035b9-a971-400d-a3fa-bb365df1d476', 'Name"': 'VLAN 1', 'Type': 2, 'UpdatedBy': None, 'UpdatedTime': '2018-11-27 10:22:14.140', 'VlanMaximum': 1, 'VlanMinimum': 1}], 'NicBonded': True, 'OnboardedPort': '59HW8X2:ethernet1/1/1'}, {'FabricId': '3ea6be04-5cf0-4e05-a136-5046d874d1e6', 'Id': 'NIC.Mezzanine.1A-2-1', 'NativeVLAN': 0, 'Networks': [{'CreatedBy': 'system', 'CreationTime': '2018-09-25 14:46:12.374', 'Description': None, 'Id': 10155, 'InternalRefNWUUId': 'f15a36b6-e3d3-46b2-9e7d-bf9cd66e180d', 'Name': 'jagvlan', 'Type': 1, 'UpdatedBy': None, 'UpdatedTime': '2018-09-25 14:46:12.374', 'VlanMaximum': 143, 'VlanMinimum': 143}], 'NicBonded': False, 'OnboardedPort': '6H7J6Z2:ethernet1/1/1'}]}])
  Returns the information of collected server interface profile information.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)

