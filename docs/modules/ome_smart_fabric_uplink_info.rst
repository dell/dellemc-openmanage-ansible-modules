.. _ome_smart_fabric_uplink_info_module:


ome_smart_fabric_uplink_info -- Retrieve details of fabric uplink on OpenManage Enterprise Modular.
===================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieve details of fabric uplink on OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.9.6



Parameters
----------

  fabric_id (optional, str, None)
    Unique id of the fabric.

    *fabric_id* is mutually exclusive with *fabric_name*.


  fabric_name (optional, str, None)
    Unique name of the fabric.

    *fabric_name* is mutually exclusive with *fabric_id*.


  uplink_id (optional, str, None)
    Unique id of the uplink.

    *uplink_id* is mutually exclusive with *uplink_name*.

    *fabric_id* or *fabric_name* is required along with *uplink_id*.


  uplink_name (optional, str, None)
    Unique name of the uplink.

    *uplink_name* is mutually exclusive with *uplink_id*.

    *fabric_id* or *fabric_name* is required along with *uplink_name*.


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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise Modular.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Retrieve all fabric uplink information using fabric_id.
      dellemc.openmanage.ome_smart_fabric_uplink_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        fabric_id: "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2"

    - name: Retrieve all fabric uplink information using fabric_name.
      dellemc.openmanage.ome_smart_fabric_uplink_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        fabric_name: "f1"

    - name: Retrieve specific fabric information using uplink_id.
      dellemc.openmanage.ome_smart_fabric_uplink_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        fabric_id: "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2"
        uplink_id: "1ad54420-b145-49a1-9779-21a579ef6f2d"

    - name: Retrieve specific fabric information using uplink_name.
      dellemc.openmanage.ome_smart_fabric_uplink_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        fabric_id: "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2"
        uplink_name: "u1"



Return Values
-------------

msg (always, str, Successfully retrieved the fabric uplink information.)
  Status of fabric uplink information retrieval.


uplink_info (on success, list, [{'Description': '', 'Id': '1ad54420-b145-49a1-9779-21a579ef6f2d', 'MediaType': 'Ethernet', 'Name': 'u1', 'NativeVLAN': 1, 'Networks': [{'CreatedBy': 'system', 'CreationTime': '2018-09-25 14:46:12.374', 'Description': None, 'Id': 10155, 'InternalRefNWUUId': 'f15a36b6-e3d3-46b2-9e7d-bf9cd66e180d', 'Name': 'testvlan', 'Type': 1, 'UpdatedBy': 'root', 'UpdatedTime': '2019-06-27 15:06:22.836', 'VlanMaximum': 143, 'VlanMinimum': 143}], 'Ports': [{'AdminStatus': 'Enabled', 'BlinkStatus': 'OFF', 'ConfiguredSpeed': '0', 'CurrentSpeed': '0', 'Description': '', 'Id': 'SVCTAG1:ethernet1/1/35', 'MaxSpeed': '0', 'MediaType': 'Ethernet', 'Name': '', 'NodeServiceTag': 'SVCTAG1', 'OpticsType': 'NotPresent', 'PortNumber': 'ethernet1/1/35', 'Role': 'Uplink', 'Status': 'Down', 'Type': 'PhysicalEthernet'}, {'AdminStatus': 'Enabled', 'BlinkStatus': 'OFF', 'ConfiguredSpeed': '0', 'CurrentSpeed': '0', 'Description': '', 'Id': 'SVCTAG1:ethernet1/1/35', 'MaxSpeed': '0', 'MediaType': 'Ethernet', 'Name': '', 'NodeServiceTag': 'SVCTAG1', 'OpticsType': 'NotPresent', 'PortNumber': 'ethernet1/1/35', 'Role': 'Uplink', 'Status': 'Down', 'Type': 'PhysicalEthernet'}], 'Summary': {'NetworkCount': 1, 'PortCount': 2}, 'UfdEnable': 'Disabled'}])
  Information about the fabric uplink.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'CGEN1006', 'RelatedProperties': [], 'Message': 'Unable to complete the request because the resource URI does not exist or is not implemented.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': "Check the request resource URI. Refer to the OpenManage Enterprise-Modular User's Guide for more information about resource URI and its properties."}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Husniya Hameed(@husniya_hameed)

