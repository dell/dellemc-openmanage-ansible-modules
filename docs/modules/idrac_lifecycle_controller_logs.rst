.. _idrac_lifecycle_controller_logs_module:


idrac_lifecycle_controller_logs -- Export Lifecycle Controller logs to a network share or local path.
=====================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Export Lifecycle Controller logs to a given network share or local path.



Requirements
------------
The below requirements are needed on the host that executes this module.

- omsdk \>= 1.2.488
- python \>= 3.9.6



Parameters
----------

  share_name (True, str, None)
    Network share or local path.

    CIFS, NFS network share types are supported.


  share_user (optional, str, None)
    Network share user in the format 'user@domain' or 'domain\\user' if user is part of a domain else 'user'. This option is mandatory for CIFS Network Share.


  share_password (optional, str, None)
    Network share user password. This option is mandatory for CIFS Network Share.


  job_wait (optional, bool, True)
    Whether to wait for the running job completion or not.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.

    If the username is not provided, then the environment variable \ :envvar:`IDRAC\_USERNAME`\  is used.

    Example: export IDRAC\_USERNAME=username


  idrac_password (True, str, None)
    iDRAC user password.

    If the password is not provided, then the environment variable \ :envvar:`IDRAC\_PASSWORD`\  is used.

    Example: export IDRAC\_PASSWORD=password


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
   - This module requires 'Administrator' privilege for \ :emphasis:`idrac\_user`\ .
   - Exporting data to a local share is supported only on iDRAC9-based PowerEdge Servers and later.
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports both IPv4 and IPv6 address for \ :emphasis:`idrac\_ip`\ .
   - This module does not support \ :literal:`check\_mode`\ .
   - No job will be created when exporting data to a local share in iDRAC9 and iDRAC 10.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Export lifecycle controller logs to NFS share.
      dellemc.openmanage.idrac_lifecycle_controller_logs:
        idrac_ip: "190.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        share_name: "192.168.0.0:/nfsfileshare"

    - name: Export lifecycle controller logs to CIFS share.
      dellemc.openmanage.idrac_lifecycle_controller_logs:
        idrac_ip: "190.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        share_name: "\\\\192.168.0.2\\share"
        share_user: "share_user_name"
        share_password: "share_user_pwd"

    - name: Export lifecycle controller logs to LOCAL path.
      dellemc.openmanage.idrac_lifecycle_controller_logs:
        idrac_ip: "190.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        share_name: "/example/export_lc"



Return Values
-------------

msg (always, str, Successfully exported the lifecycle controller logs.)
  Status of the export lifecycle controller logs job.


lc_logs_status (success, dict, {'ElapsedTimeSinceCompletion': '0', 'InstanceID': 'JID_274774785395', 'JobStartTime': 'NA', 'JobStatus': 'Completed', 'JobUntilTime': 'NA', 'Message': 'LCL Export was successful', 'MessageArguments': 'NA', 'MessageID': 'LC022', 'Name': 'LC Export', 'PercentComplete': '100', 'Status': 'Success', 'file': '192.168.0.0:/nfsfileshare/190.168.0.1_20210728_133437_LC_Log.log', 'retval': True})
  Status of the export operation along with job details and file path.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Rajeev Arakkal (@rajeevarakkal)
- Anooja Vardhineni (@anooja-vardhineni)

