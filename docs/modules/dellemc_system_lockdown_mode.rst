.. _dellemc_system_lockdown_mode_module:


dellemc_system_lockdown_mode -- Configures system lockdown mode for iDRAC
=========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module is allows to Enable or Disable System lockdown Mode.



Requirements
------------
The below requirements are needed on the host that executes this module.

- omsdk
- python >= 2.7.5



Parameters
----------

  share_name (True, str, None)
    Network share or a local path.


  share_user (optional, str, None)
    Network share user in the format 'user@domain' or 'domain\user' if user is part of a domain else 'user'. This option is mandatory for CIFS Network Share.


  share_password (optional, str, None)
    Network share user password. This option is mandatory for CIFS Network Share.


  share_mnt (optional, str, None)
    Local mount path of the network share with read-write permission for ansible user. This option is mandatory for Network Share.


  lockdown_mode (True, str, None)
    Whether to Enable or Disable system lockdown mode.


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
   - This module requires 'Administrator' privilege for *idrac_user*.
   - Run this module from a system that has direct access to Dell EMC iDRAC.
   - This module does not support ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Check System  Lockdown Mode
      dellemc.openmanage.dellemc_system_lockdown_mode:
           idrac_ip:   "192.168.0.1"
           idrac_user: "user_name"
           idrac_password:  "user_password"
           share_name: "192.168.0.1:/share"
           share_mnt: "/mnt/share"
           lockdown_mode: "Disabled"



Return Values
-------------

msg (always, str, Successfully completed the lockdown mode operations.)
  Lockdown mode of the system is configured.


system_lockdown_status (success, dict, {'Data': {'StatusCode': 200, 'body': {'@Message.ExtendedInfo': [{'Message': 'Successfully Completed Request', 'MessageArgs': [], 'MessageArgs@odata.count': 0, 'MessageId': 'Base.1.0.Success', 'RelatedProperties': [], 'RelatedProperties@odata.count': 0, 'Resolution': 'None', 'Severity': 'OK'}]}}, 'Message': 'none', 'Status': 'Success', 'StatusCode': 200, 'retval': True})
  Storage configuration job and progress details from the iDRAC.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)

