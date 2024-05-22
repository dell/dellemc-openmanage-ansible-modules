.. _ome_alert_policies_actions_info_module:


ome_alert_policies_actions_info -- Get information on actions of alert policies.
================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves the information on actions of alert policies for OpenManage Enterprise and OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (False, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.

    If the username is not provided, then the environment variable \ :envvar:`OME\_USERNAME`\  is used.

    Example: export OME\_USERNAME=username


  password (False, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.

    If the password is not provided, then the environment variable \ :envvar:`OME\_PASSWORD`\  is used.

    Example: export OME\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`OME\_X\_AUTH\_TOKEN`\  is used.

    Example: export OME\_X\_AUTH\_TOKEN=x\_auth\_token


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.


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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise or OpenManage Enterprise Modular.
   - This module supports both IPv4 and IPv6 addresses.
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Get action details of all alert policies.
      dellemc.openmanage.ome_alert_policies_actions_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"



Return Values
-------------

actions (success, list, [{'Name': 'Email', 'Description': 'Email', 'Disabled': False, 'ParameterDetails': [{'Id': 1, 'Name': 'subject', 'Value': 'Device Name: $name,  Device IP Address: $ip,  Severity: $severity', 'Type': 'string', 'TemplateParameterTypeDetails': [{'Name': 'maxLength', 'Value': '255'}]}, {'Id': 2, 'Name': 'to', 'Value': '', 'Type': 'string', 'TemplateParameterTypeDetails': [{'Name': 'maxLength', 'Value': '255'}]}, {'Id': 3, 'Name': 'from', 'Value': 'admin1@dell.com', 'Type': 'string', 'TemplateParameterTypeDetails': [{'Name': 'maxLength', 'Value': '255'}]}, {'Id': 4, 'Name': 'message', 'Value': 'Event occurred for Device Name: $name, Device IP Address: $ip, Service Tag: $identifier, UTC Time: $time, Severity: $severity, Message ID: $messageId, $message', 'Type': 'string', 'TemplateParameterTypeDetails': [{'Name': 'maxLength', 'Value': '255'}]}, {'Id': 60, 'Name': 'Trap', 'Description': 'Trap', 'Disabled': False, 'ParameterDetails': [{'Id': 1, 'Name': 'localhost:162', 'Value': 'true', 'Type': 'boolean', 'TemplateParameterTypeDetails': []}]}, {'Id': 90, 'Name': 'Syslog', 'Description': 'Syslog', 'Disabled': False, 'ParameterDetails': [{'Id': 1, 'Name': 'localhost.scomdev.com:555', 'Value': 'true', 'Type': 'boolean', 'TemplateParameterTypeDetails': []}, {'Id': 2, 'Name': 'localhost.scomdev.com:555', 'Value': 'true', 'Type': 'boolean', 'TemplateParameterTypeDetails': []}]}, {'Id': 100, 'Name': 'Ignore', 'Description': 'Ignore', 'Disabled': False, 'ParameterDetails': []}, {'Id': 70, 'Name': 'SMS', 'Description': 'SMS', 'Disabled': False, 'ParameterDetails': [{'Id': 1, 'Name': 'to', 'Value': '', 'Type': 'string', 'TemplateParameterTypeDetails': [{'Name': 'maxLength', 'Value': '255'}]}]}, {'Id': 110, 'Name': 'PowerControl', 'Description': 'Power Control Action Template', 'Disabled': False, 'ParameterDetails': [{'Id': 1, 'Name': 'powercontrolaction', 'Value': 'poweroff', 'Type': 'singleSelect', 'TemplateParameterTypeDetails': [{'Name': 'option', 'Value': 'powercycle'}, {'Name': 'option', 'Value': 'poweroff'}, {'Name': 'option', 'Value': 'poweron'}, {'Name': 'option', 'Value': 'gracefulshutdown'}]}]}, {'Id': 111, 'Name': 'RemoteCommand', 'Description': 'RemoteCommand', 'Disabled': True, 'ParameterDetails': [{'Id': 1, 'Name': 'remotecommandaction', 'Value': None, 'Type': 'singleSelect', 'TemplateParameterTypeDetails': []}]}, {'Id': 112, 'Name': 'Mobile', 'Description': 'Mobile', 'Disabled': False, 'ParameterDetails': []}]}])
  Returns the alert policies action information collected from the Device.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.


msg (always, str, Successfully retrieved alert policies actions information.)
  Status of the alert policies actions fetch operation.





Status
------





Authors
~~~~~~~

- Kritika Bhateja (@Kritika-Bhateja-03)

