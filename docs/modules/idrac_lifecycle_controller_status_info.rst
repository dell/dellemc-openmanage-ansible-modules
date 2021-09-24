.. _idrac_lifecycle_controller_status_info_module:


idrac_lifecycle_controller_status_info -- Get the status of the Lifecycle Controller
====================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module shows the status of the Lifecycle Controller on a Dell EMC PowerEdge server.



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
    - name: Show status of the Lifecycle Controller
      dellemc.openmanage.idrac_lifecycle_controller_status_info:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"



Return Values
-------------

msg (always, str, Successfully fetched the lifecycle controller status.)
  Overall status of fetching lifecycle controller status.


lc_status_info (success, dict, {'msg': {'LCReady': True, 'LCStatus': 'Ready'}})
  Displays the status of the Lifecycle Controller on a Dell EMC PowerEdge server.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Rajeev Arakkal (@rajeevarakkal)
- Anooja Vardhineni (@anooja-vardhineni)

