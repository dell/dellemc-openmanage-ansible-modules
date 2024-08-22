.. _idrac_secure_boot_module:


idrac_secure_boot -- Import secure boot certificate.
====================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to import the secure boot certificate.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  import_certificates (optional, bool, None)
    Import all the specified key certificates.

    When \ :emphasis:`import\_certificates`\  is \ :literal:`true`\ , then either \ :emphasis:`platform\_key`\ , \ :emphasis:`KEK`\ , \ :emphasis:`database`\ , or \ :emphasis:`disallow\_database`\  is required.


  platform_key (optional, path, None)
    The absolute path of the Platform key certificate file for UEFI secure boot.


  KEK (optional, list, None)
    A list of absolute paths of the Key Exchange Key (KEK) certificate file for UEFI secure boot.


  database (optional, list, None)
    A list of absolute paths of the Database certificate file for UEFI secure boot.


  disallow_database (optional, list, None)
    A list of absolute paths of the Disallow Database certificate file for UEFI secure boot.


  restart (optional, bool, False)
    Secure boot certificate import operation requires a server restart. This parameter provides an option to restart the server.

    \ :literal:`true`\  restarts the server.

    \ :literal:`false`\  does not restart the server.

    \ :emphasis:`restart`\  is applicable when \ :emphasis:`import\_certificates`\  is \ :literal:`true`\ .


  restart_type (optional, str, GracefulRestart)
    Restart type of the server.

    \ :literal:`ForceRestart`\  forcefully restarts the server.

    \ :literal:`GracefulRestart`\  gracefully restarts the server.

    \ :emphasis:`restart\_type`\  is applicable when \ :emphasis:`restart`\  is \ :literal:`true`\ .


  job_wait (optional, bool, True)
    Whether to wait till completion of the secure boot certificate operation. This is applicable when \ :emphasis:`restart`\  is \ :literal:`true`\ .


  job_wait_timeout (optional, int, 1200)
    The maximum wait time of \ :emphasis:`job\_wait`\  in seconds. The job is tracked only for this duration.

    This option is applicable when \ :emphasis:`job\_wait`\  is \ :literal:`true`\ .


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
   - This module will always report changes found to be applied when run in \ :literal:`check mode`\ .
   - This module does not support idempotency when \ :emphasis:`import\_certificates`\  is provided.
   - This module supports IPv4 and IPv6 addresses.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Import multiple SecureBoot certificate without applying to iDRAC.
      dellemc.openmanage.idrac_secure_boot:
        idrac_ip: "192.168.1.2"
        idrac_user: "user"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        import_certificates: true
        platform_key: /user/name/certificates/pk.pem
        KEK:
          - /user/name/certificates/kek1.pem
          - /user/name/certificates/kek2.pem
        database:
          - /user/name/certificates/db1.pem
          - /user/name/certificates/db2.pem
        disallow_database:
          - /user/name/certificates/dbx1.pem
          - /user/name/certificates/dbx2.pem

    - name: Import a SecureBoot certificate and restart the server to apply it.
      dellemc.openmanage.idrac_secure_boot:
        idrac_ip: "192.168.1.2"
        idrac_user: "user"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        import_certificates: true
        platform_key: /user/name/certificates/pk.pem
        restart: true
        job_wait_timeout: 600



Return Values
-------------

msg (always, str, Successfully imported the SecureBoot certificate.)
  Status of the secure boot operation.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Abhishek Sinha(@ABHISHEK-SINHA10)

