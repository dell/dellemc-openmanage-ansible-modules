.. _idrac_system_info_module:


idrac_system_info -- Get the PowerEdge Server System Inventory
==============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get the PowerEdge Server System Inventory.



Requirements
------------
The below requirements are needed on the host that executes this module.

- omsdk \>= 1.2.488
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
   - The functionality to get :emphasis:`temperature\_sensors`\ , :emphasis:`fan\_sensors`\ , :emphasis:`controller\_sensor`\ , :emphasis:`controller\_battery`\ , :emphasis:`system\_metrics`\ , :emphasis:`system\_board\_metrics`\ , :emphasis:`sensors\_amperage` and :emphasis:`video` component is not available through iDRAC10.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Get System Inventory
      dellemc.openmanage.idrac_system_info:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"



Return Values
-------------

msg (always, str, Successfully fetched the system inventory details.)
  Overall system inventory information status.


system_info (success, dict, {'BIOS': [{'BIOSReleaseDate': '11/26/2019', 'FQDD': 'BIOS.Setup.1-1', 'InstanceID': 'DCIM:INSTALLED#741__BIOS.Setup.1-1', 'Key': 'DCIM:INSTALLED#741__BIOS.Setup.1-1', 'SMBIOSPresent': 'True', 'VersionString': '2.4.8'}]})
  Details of the PowerEdge Server System Inventory.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Rajeev Arakkal (@rajeevarakkal)
- Kritika Bhateja (@Kritika-Bhateja-03)
- Abhishek Sinha (@ABHISHEK-SINHA10)

