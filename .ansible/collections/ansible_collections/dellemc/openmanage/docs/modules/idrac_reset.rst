.. _idrac_reset_module:


idrac_reset -- Factory reset the iDRACs
=======================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module resets the iDRAC to factory default settings.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  reset_to_default (optional, str, None)
    If this value is not set the default behaviour is to restart the iDRAC.

    \ :literal:`All`\  Discards all settings and reset to default credentials.

    \ :literal:`ResetAllWithRootDefaults`\  Discards all settings and reset the default username to root and password to the shipping value.

    \ :literal:`Default`\  Discards all settings, but preserves user and network settings.

    \ :literal:`CustomDefaults`\  All configuration is set to custom defaults.This option is supported on firmware version 7.00.00.00 and newer versions.


  custom_defaults_file (optional, str, None)
    Name of the custom default configuration file in the XML format.

    This option is applicable when \ :emphasis:`reset\_to\_default`\  is \ :literal:`CustomDefaults`\ .

    \ :emphasis:`custom\_defaults\_file`\  is mutually exclusive with \ :emphasis:`custom\_defaults\_buffer`\ .


  custom_defaults_buffer (optional, str, None)
    This parameter provides the option to import the buffer input in XML format as a custom default configuration.

    This option is applicable when \ :emphasis:`reset\_to\_default`\  is \ :literal:`CustomDefaults`\ .

    \ :emphasis:`custom\_defaults\_buffer`\  is mutually exclusive with \ :emphasis:`custom\_defaults\_file`\ .


  wait_for_idrac (optional, bool, True)
    This parameter provides the option to wait for the iDRAC to reset and lifecycle controller status to be ready.


  job_wait_timeout (optional, int, 600)
    Time in seconds to wait for job completion.

    This is applicable when \ :emphasis:`wait\_for\_idrac`\  is \ :literal:`true`\ .


  force_reset (optional, bool, False)
    This parameter provides the option to force reset the iDRAC without checking the iDRAC lifecycle controller status.

    This option is applicable only for iDRAC9.


  default_username (optional, str, None)
    This parameter is only applied when \ :emphasis:`reset\_to\_default`\  is \ :literal:`All`\  or \ :literal:`ResetAllWithRootDefaults`\ .

    This parameter is required to track LifeCycle status of the server after the reset operation is performed. If this parameter is not provided, then the LifeCycle status is not tracked after the reset operation.


  default_password (optional, str, None)
    This parameter is only applied when \ :emphasis:`reset\_to\_default`\  is \ :literal:`All`\  or \ :literal:`ResetAllWithRootDefaults`\ .

    This parameter is required to track LifeCycle status of the server after the reset operation is performed. If this parameter is not provided, then the LifeCycle status is not tracked after the reset operation.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (False, str, None)
    iDRAC username.

    If the username is not provided, then the environment variable \ :envvar:`IDRAC\_USERNAME`\  is used.

    Example: export IDRAC\_USERNAME=username


  idrac_password (False, str, None)
    iDRAC user password.

    If the password is not provided, then the environment variable \ :envvar:`IDRAC\_PASSWORD`\  is used.

    Example: export IDRAC\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`IDRAC\_X\_AUTH\_TOKEN`\  is used.

    Example: export IDRAC\_X\_AUTH\_TOKEN=x\_auth\_token


  idrac_port (optional, int, 443)
    iDRAC port.


  validate_certs (optional, bool, True)
    If \ :literal:`false`\ , the SSL certificates will not be validated.

    Configure \ :literal:`false`\  only on personally controlled sites where self-signed certificates are used.

    Prior to collection version \ :literal:`5.0.0`\ , the \ :emphasis:`validate\_certs`\  is \ :literal:`false`\  by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports both IPv4 and IPv6 address for \ :emphasis:`idrac\_ip`\ .
   - This module supports \ :literal:`check\_mode`\ .
   - If reset\_to\_default option is not specified, then this module triggers a graceful restart.
   - This module skips the execution if reset options are not supported by the iDRAC.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Reset the iDRAC to default and do not wait till the iDRAC is accessible.
      dellemc.openmanage.idrac_reset:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       ca_path: "/path/to/ca_cert.pem"
       reset_to_default: "Default"
       wait_for_idrac: false

    - name: Reset the iDRAC to All and wait for lifecycle controller status to be ready.
      dellemc.openmanage.idrac_reset:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       ca_path: "/path/to/ca_cert.pem"
       reset_to_default: "All"
       wait_for_idrac: true
       default_username: "user_name"
       default_password: "user_password"

    - name: Force reset the iDRAC to default.
      dellemc.openmanage.idrac_reset:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       ca_path: "/path/to/ca_cert.pem"
       reset_to_default: "Default"
       force_reset: true

    - name: Gracefully restart the iDRAC.
      dellemc.openmanage.idrac_reset:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       ca_path: "/path/to/ca_cert.pem"

    - name: Reset the iDRAC to custom defaults XML and do not wait till the iDRAC is accessible.
      dellemc.openmanage.idrac_reset:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       ca_path: "/path/to/ca_cert.pem"
       reset_to_default: "CustomDefaults"
       custom_defaults_file: "/path/to/custom_defaults.xml"

    - name: Reset the iDRAC to custom defaults buffer input and do not wait till the iDRAC is accessible.
      dellemc.openmanage.idrac_reset:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       ca_path: "/path/to/ca_cert.pem"
       reset_to_default: "CustomDefaults"
       custom_defaults_buffer: "<SystemConfiguration Model=\"PowerEdge R7525\" ServiceTag=\"ABCD123\">\n<Component FQDD=\"iDRAC.Embedded.1\">\n
                                   <Attribute Name=\"IPMILan.1#Enable\">Disabled</Attribute>\n </Component>\n\n</SystemConfiguration>"



Return Values
-------------

msg (always, str, Successfully performed iDRAC reset.)
  Status of the iDRAC reset operation.


reset_status (reset operation is triggered., dict, {'idracreset': {'Data': {'StatusCode': 204}, 'Message': 'none', 'Status': 'Success', 'StatusCode': 204, 'retval': True}})
  Details of iDRAC reset operation.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)
- Anooja Vardhineni (@anooja-vardhineni)
- Lovepreet Singh (@singh-lovepreet1)
- Abhishek Sinha (@ABHISHEK-SINHA10)

