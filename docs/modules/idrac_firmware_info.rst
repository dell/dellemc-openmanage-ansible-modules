.. _idrac_firmware_info_module:


idrac_firmware_info -- Get Firmware Inventory
=============================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get Firmware Inventory.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

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

    Configure :literal:`false` only on personally controlled sites where self-signed certificates are used.

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
   - This module supports :literal:`check\_mode`.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Get Installed Firmware Inventory
      dellemc.openmanage.idrac_firmware_info:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"



Return Values
-------------

msg (always, str, Successfully fetched the firmware inventory details.)
  Fetching the firmware inventory details.


firmware_info (success, dict, {'Firmware': [{'BuildNumber': '0', 'Classifications': '10', 'ComponentID': '102573', 'ComponentType': 'FRMW', 'DeviceID': None, 'ElementName': 'Power Supply.Slot.1', 'FQDD': 'PSU.Slot.1', 'HashValue': None, 'IdentityInfoType': 'OrgID:ComponentType:ComponentID', 'IdentityInfoValue': 'DCIM:firmware:102573', 'InstallationDate': '2018-11-22T03:58:23Z', 'InstanceID': 'DCIM:INSTALLED#0x15__PSU.Slot.1', 'IsEntity': 'true', 'Key': 'DCIM:INSTALLED#0x15__PSU.Slot.1', 'MajorVersion': '0', 'MinorVersion': '3', 'RevisionNumber': '67', 'RevisionString': None, 'Status': 'Installed', 'SubDeviceID': None, 'SubVendorID': None, 'Updateable': 'true', 'VendorID': None, 'VersionString': '00.3D.67', 'impactsTPMmeasurements': 'false'}]})
  Details of the firmware.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Rajeev Arakkal (@rajeevarakkal)
- Saksham Nautiyal (@Saksham-Nautiyal)

