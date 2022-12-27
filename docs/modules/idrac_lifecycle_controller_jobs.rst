.. _idrac_lifecycle_controller_jobs_module:


idrac_lifecycle_controller_jobs -- Delete the Lifecycle Controller Jobs
=======================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Delete a Lifecycle Controller job using its job ID or delete all jobs.



Requirements
------------
The below requirements are needed on the host that executes this module.

- omsdk >= 1.2.488
- python >= 3.9.6



Parameters
----------

  job_id (optional, str, None)
    Job ID of the specific job to be deleted.

    All the jobs in the job queue are deleted if this option is not specified.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.


  idrac_password (True, str, None)
    iDRAC user password.


  idrac_port (optional, int, 443)
    iDRAC port.


  validate_certs (optional, bool, True)
    If ``False``, the SSL certificates will not be validated.

    Configure ``False`` only on personally controlled sites where self-signed certificates are used.

    Prior to collection version ``5.0.0``, the *validate_certs* is ``False`` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports both IPv4 and IPv6 address for *idrac_ip*.
   - This module does not support ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Delete Lifecycle Controller job queue
      dellemc.openmanage.idrac_lifecycle_controller_jobs:
           idrac_ip: "192.168.0.1"
           idrac_user: "user_name"
           idrac_password: "user_password"
           ca_path: "/path/to/ca_cert.pem"

    - name: Delete Lifecycle Controller job using a job ID
      dellemc.openmanage.idrac_lifecycle_controller_jobs:
           idrac_ip: "192.168.0.1"
           idrac_user: "user_name"
           idrac_password: "user_password"
           ca_path: "/path/to/ca_cert.pem"
           job_id: "JID_801841929470"



Return Values
-------------

msg (always, str, Successfully deleted the job.)
  Status of the delete operation.


status (success, dict, {'Message': 'The specified job was deleted', 'MessageID': 'SUP020', 'ReturnValue': '0'})
  Details of the delete operation.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)
- Anooja Vardhineni (@anooja-vardhineni)

