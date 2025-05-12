.. _idrac_lifecycle_controller_job_status_info_module:


idrac_lifecycle_controller_job_status_info -- Get the status of a Lifecycle Controller job
==========================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module shows the status of a specific Lifecycle Controller job using its job ID.



Requirements
------------
The below requirements are needed on the host that executes this module.

- omsdk \>= 1.2.488
- python \>= 3.9.6



Parameters
----------

  job_id (True, str, None)
    JOB ID in the format "JID\_123456789012".


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.

    If the username is not provided, then the environment variable :envvar:`IDRAC\_USERNAME` is used.

    Example: export IDRAC\_USERNAME=username


  idrac_password (True, str, None)
    iDRAC user password.

    If the password is not provided, then the environment variable :envvar:`IDRAC\_PASSWORD` is used.

    Example: export IDRAC\_PASSWORD=password


  idrac_port (optional, int, 443)
    iDRAC port.


  validate_certs (optional, bool, True)
    If :literal:`false`\ , the SSL certificates will not be validated.

    Configure :literal:`false` only on personally controlled sites where self-signed certificates are used.

    Prior to collection version :literal:`5.0.0`\ , the :emphasis:`validate\_certs` is :literal:`false` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports both IPv4 and IPv6 address for :emphasis:`idrac\_ip`.
   - This module supports :literal:`check\_mode`.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Show status of a Lifecycle Control job
      dellemc.openmanage.idrac_lifecycle_controller_job_status_info:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        job_id: "JID_1234567890"



Return Values
-------------

msg (always, str, Successfully fetched the job info.)
  Overall status of the job facts operation.


job_info (success, dict, {'ElapsedTimeSinceCompletion': '8742', 'InstanceID': 'JID_844222910040', 'JobStartTime': 'NA', 'JobStatus': 'Completed', 'JobUntilTime': 'NA', 'Message': 'Job completed successfully.', 'MessageArguments': 'NA', 'MessageID': 'RED001', 'Name': 'update:DCIM:INSTALLED#iDRAC.Embedded.1-1#IDRACinfo', 'PercentComplete': '100', 'Status': 'Success'})
  Displays the status of a Lifecycle Controller job.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Rajeev Arakkal (@rajeevarakkal)
- Anooja Vardhineni (@anooja-vardhineni)
- Trisha Datta (@trisha-dell)

