.. _ome_alert_policies_message_id_info_module:


ome_alert_policies_message_id_info -- Get message ID information of alert policies for OpenManage Enterprise.
=============================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves the message ID information of alert policies for OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.9.6



Parameters
----------

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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.
   - This module supports both IPv4 and IPv6 address for *hostname*.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Get message ID details of all alert policies
      dellemc.openmanage.ome_alert_policies_message_id_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"



Return Values
-------------

msg (on error, str, HTTP Error 501: 501)
  Error description in case of error.


message_ids (success, dict, [{'Category': 'System Health', 'DetailedDescription': 'The current sensor identified in the message has failed. This condition can cause system performance issues and degradation in the monitoring capability of the system.', 'Message': 'The ${0} sensor has failed, and the last recorded value by the sensor was ${1} A.', 'MessageId': 'AMP400', 'Prefix': 'AMP', 'RecommendedAction': 'Check the Embedded System Management (ESM) Log for any sensor related faults. If there is a failed sensor, replace the system board. For more information, contact your service provider.', 'SequenceNo': 400, 'Severity': 'Critical', 'SubCategory': 'Amperage'}, {'Category': 'System Health', 'DetailedDescription': 'The current sensor identified in the message has failed. This condition can cause system performance issues and degradation in the monitoring capability of the system.', 'Message': 'Unable to read the ${0} sensor value.', 'MessageId': 'AMP401', 'Prefix': 'AMP', 'RecommendedAction': 'Check the Embedded System Management (ESM) Log for any sensor related faults. If there is a failed sensor, replace the system board. For more information, contact your service provider.', 'SequenceNo': 401, 'Severity': 'Warning', 'SubCategory': 'Amperage'}, {'Category': 'System Health', 'DetailedDescription': 'The current sensor identified in the message has returned to a normal state.', 'Message': 'The ${0} sensor returned to a normal state with a value of ${1} A.', 'MessageId': 'AMP402', 'Prefix': 'AMP', 'RecommendedAction': 'No response action is required.', 'SequenceNo': 402, 'Severity': 'Informational', 'SubCategory': 'Amperage'}, {'Category': 'System Health', 'DetailedDescription': 'The current sensor identified in the message is faulty or the current drawn by the system exceeds the warning threshold. This condition can cause system performance issues and degradation in the monitoring capability of the system.', 'Message': 'The ${0} sensor state has changed to a warning state with a value of ${1} A.', 'MessageId': 'AMP403', 'Prefix': 'AMP', 'RecommendedAction': 'Verify the Embedded System Management (ESM) Log for any sensor related faults. If there is a failed sensor, replace the system board. For more information, contact your service provider. Otherwise, change the warning threshold for the current sensor such that it corresponds to the hardware configuration.', 'SequenceNo': 403, 'Severity': 'Warning', 'SubCategory': 'Amperage'}, {'Category': 'System Health', 'DetailedDescription': 'The current sensor identified in the message is faulty or the current drawn by the system exceed the critical threshold. This condition can cause system performance issues and degradation in the monitoring capability of the system.', 'Message': 'The ${0} sensor detected an error with a value of ${1} A.', 'MessageId': 'AMP404', 'Prefix': 'AMP', 'RecommendedAction': 'Review system power policy, check system logs for power related failures, and review system configuration changes. For more information, contact your service provider.', 'SequenceNo': 404, 'Severity': 'Warning', 'SubCategory': 'Amperage'}])
  Details of the message ids.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Shivam Sharma (@ShivamSh3)

