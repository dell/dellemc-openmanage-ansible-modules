.. _ome_alert_policies_info_module:


ome_alert_policies_info -- Retrieves information of one or more OME alert policies.
===================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves the information of alert policies for OpenManage Enterprise and OpenManage Enterprise Modular.

A list of information about a specific OME alert policy using the policy name.

A list of all the OME alert policies with their information when the policy name is not provided.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.9.6



Parameters
----------

  policy_name (optional, str, None)
    Name of the policy.


  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.


  password (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.


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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise or OpenManage Enterprise Modular.
   - This module supports both IPv4 and IPv6 addresses.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Retrieve information about all OME alert policies.
      dellemc.openmanage.ome_alert_policies_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"

    - name: Retrieve information about a specific OME alert policy using the policy name.
      dellemc.openmanage.ome_alert_policies_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        policy_name: "Mobile Push Notification - Critical Alerts"



Return Values
-------------

msg (always, str, Successfully retrieved all the OME alert policies information.)
  Status of the alert policies info fetch operation.


policies (success, list, [{'Id': 10006, 'Name': 'Mobile Push Notification - Critical Alerts', 'Description': 'This policy is applicable to critical alerts. Associated actions will be taken when a critical alert is received.', 'Enabled': True, 'DefaultPolicy': True, 'PolicyData': {'Catalogs': [], 'Severities': [16], 'MessageIds': [], 'Devices': [], 'DeviceTypes': [], 'Groups': [], 'AllTargets': False, 'Schedule': {'StartTime': None, 'EndTime': None, 'CronString': None, 'Interval': False}, 'Actions': [{'Id': 5, 'Name': 'Mobile', 'ParameterDetails': [], 'TemplateId': 112}], 'UndiscoveredTargets': []}, 'State': True, 'Visible': True, 'Owner': None}])
  Retrieve information about all the OME alert policies.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Abhishek Sinha(@ABHISHEK-SINHA10)

