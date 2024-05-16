.. _ome_network_port_breakout_module:


ome_network_port_breakout -- This module allows to automate the port portioning or port breakout to logical sub ports
=====================================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to automate breaking out of IOMs in fabric mode into logical sub ports.

The port breakout operation is only supported in OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  target_port (True, str, None)
    The ID of the port in the switch to breakout. Enter the port ID in the format: service tag:port. For example, 2HB7NX2:ethernet1/1/13.


  breakout_type (True, str, None)
    The preferred breakout type. For example, 4X10GE.

    To revoke the default breakout configuration, enter 'HardwareDefault'.


  hostname (True, str, None)
    OpenManage Enterprise Modular IP address or hostname.


  username (False, str, None)
    OpenManage Enterprise Modular username.

    If the username is not provided, then the environment variable \ :envvar:`OME\_USERNAME`\  is used.

    Example: export OME\_USERNAME=username


  password (False, str, None)
    OpenManage Enterprise Modular password.

    If the password is not provided, then the environment variable \ :envvar:`OME\_PASSWORD`\  is used.

    Example: export OME\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`OME\_X\_AUTH\_TOKEN`\  is used.

    Example: export OME\_X\_AUTH\_TOKEN=x\_auth\_token


  port (optional, int, 443)
    OpenManage Enterprise Modular HTTPS port.


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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise Modular.
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Port breakout configuration
      dellemc.openmanage.ome_network_port_breakout:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        target_port: "2HB7NX2:phy-port1/1/11"
        breakout_type: "1X40GE"

    - name: Revoke the default breakout configuration
      dellemc.openmanage.ome_network_port_breakout:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        target_port: "2HB7NX2:phy-port1/1/11"
        breakout_type: "HardwareDefault"



Return Values
-------------

msg (always, str, Port breakout configuration job submitted successfully.)
  Overall status of the port configuration.


breakout_status (success, dict, {'Builtin': False, 'CreatedBy': 'root', 'Editable': True, 'EndTime': None, 'Id': 11111, 'JobDescription': '', 'JobName': 'Breakout Port', 'JobStatus': {'Id': 1112, 'Name': 'New'}, 'JobType': {'Id': 3, 'Internal': False, 'Name': 'DeviceAction_Task'}, 'LastRun': None, 'LastRunStatus': {'Id': 1113, 'Name': 'NotRun'}, 'NextRun': None, 'Params': [{'JobId': 11111, 'Key': 'operationName', 'Value': 'CONFIGURE_PORT_BREAK_OUT'}, {'JobId': 11111, 'Key': 'interfaceId', 'Value': '2HB7NX2:phy-port1/1/11'}, {'JobId': 11111, 'Key': 'breakoutType', 'Value': '1X40GE'}], 'Schedule': 'startnow', 'StartTime': None, 'State': 'Enabled', 'Targets': [{'Data': '', 'Id': 11112, 'JobId': 34206, 'TargetType': {'Id': 1000, 'Name': 'DEVICE'}}], 'UpdatedBy': None, 'UserGenerated': True, 'Visible': True})
  Details of the OpenManage Enterprise jobs.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)

