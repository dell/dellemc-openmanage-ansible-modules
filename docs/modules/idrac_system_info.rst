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

- omsdk
- python >= 2.7.5



Parameters
----------

  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.


  idrac_password (True, str, None)
    iDRAC user password.


  idrac_port (optional, int, 443)
    iDRAC port.





Notes
-----

.. note::
   - Run this module from a system that has direct access to DellEMC iDRAC.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Get System Inventory
      dellemc.openmanage.idrac_system_info:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"



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

