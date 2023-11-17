.. _dellemc_idrac_lc_attributes_module:


dellemc_idrac_lc_attributes -- Enable or disable Collect System Inventory on Restart (CSIOR) property for all iDRAC/LC jobs
===========================================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module is responsible for enabling or disabling of Collect System Inventory on Restart (CSIOR) property for all iDRAC/LC jobs.



Requirements
------------
The below requirements are needed on the host that executes this module.

- omsdk >= 1.2.488
- python >= 3.9.6



Parameters
----------

  share_name (optional, str, None)
    (deprecated)Network share or a local path.

    This option is deprecated and will be removed in the later version.


  share_user (optional, str, None)
    (deprecated)Network share user in the format 'user@domain' or 'domain\user' if user is part of a domain else 'user'. This option is mandatory for CIFS Network Share.

    This option is deprecated and will be removed in the later version.


  share_password (optional, str, None)
    (deprecated)Network share user password. This option is mandatory for CIFS Network Share.

    This option is deprecated and will be removed in the later version.


  share_mnt (optional, str, None)
    (deprecated)Local mount path of the network share with read-write permission for ansible user. This option is mandatory for Network Share.

    This option is deprecated and will be removed in the later version.


  csior (optional, str, Enabled)
    Whether to Enable or Disable Collect System Inventory on Restart (CSIOR) property for all iDRAC/LC jobs.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.


  idrac_password (True, str, None)
    iDRAC user password.


  idrac_port (optional, int, 443)
    iDRAC port.


  validate_certs (optional, bool, True)
    If ``false``, the SSL certificates will not be validated.

    Configure ``false`` only on personally controlled sites where self-signed certificates are used.

    Prior to collection version ``5.0.0``, the *validate_certs* is ``false`` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - This module requires 'Administrator' privilege for *idrac_user*.
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports both IPv4 and IPv6 address for *idrac_ip*.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Set up iDRAC LC Attributes
      dellemc.openmanage.dellemc_idrac_lc_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        csior: "Enabled"



Return Values
-------------

msg (always, str, Successfully configured the iDRAC LC attributes.)
  Overall status of iDRAC LC attributes configuration.


lc_attribute_status (success, dict, {'CompletionTime': '2020-03-30T00:06:53', 'Description': 'Job Instance', 'EndTime': None, 'Id': 'JID_1234512345', 'JobState': 'Completed', 'JobType': 'ImportConfiguration', 'Message': 'Successfully imported and applied Server Configuration Profile.', 'MessageArgs': [], 'MessageArgs@odata.count': 0, 'MessageId': 'SYS053', 'Name': 'Import Configuration', 'PercentComplete': 100, 'StartTime': 'TIME_NOW', 'Status': 'Success', 'TargetSettingsURI': None, 'retval': True})
  Collect System Inventory on Restart (CSIOR) property for all iDRAC/LC jobs is configured.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------


- This module will be removed in version
  .
  *[deprecated]*


Authors
~~~~~~~

- Felix Stephen (@felixs88)

