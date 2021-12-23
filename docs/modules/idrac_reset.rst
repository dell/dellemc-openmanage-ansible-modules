.. _idrac_reset_module:


idrac_reset -- Reset iDRAC
==========================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module resets iDRAC.

iDRAC is not accessible for some time after running this module. It is recommended to wait for some time, before trying to connect to iDRAC.



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
    - name: Reset iDRAC
      dellemc.openmanage.idrac_reset:
           idrac_ip: "192.168.0.1"
           idrac_user: "user_name"
           idrac_password: "user_password"
           idrac_port: 443



Return Values
-------------

msg (always, str, Successfully performed iDRAC reset.)
  Status of the iDRAC reset operation.


reset_status (always, dict, {'idracreset': {'Data': {'StatusCode': 204}, 'Message': 'none', 'Status': 'Success', 'StatusCode': 204, 'retval': True}})
  Details of iDRAC reset operation.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)
- Anooja Vardhineni (@anooja-vardhineni)

