.. _idrac_secure_boot_module:


idrac_secure_boot -- Configures the iDRAC secure boot
=====================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows you to configure the secure boot.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  import_certificates (optional, bool, None)
    Import all the specified key certificates.

    \ :emphasis:`import\_certificates`\  is \ :literal:`true`\  either of \ :emphasis:`platform\_key`\  or i(key\_exchange\_key) or \ :emphasis:`database`\  or \ :emphasis:`disallow\_database`\  is required.


  platform_key (optional, path, None)
    Platform Key policy certificate path for UEFI Secure Boot.

    Absolute path of the certificate file \ :emphasis:`import\_certificates`\  is \ :literal:`true`\ .


  key_exchange_key (optional, list, None)
    Key exchange key policy certificate paths for UEFI Secure Boot.

    Absolute path of the certificate file if \ :emphasis:`import\_certificates`\  is \ :literal:`import`\ .


  database (optional, list, None)
    Databases certificate paths for UEFI Secure Boot.

    Absolute path of the certificate file if \ :emphasis:`import\_certificates`\  is \ :literal:`import`\ .


  disallow_database (optional, list, None)
    Disallow database certificate paths for UEFI Secure Boot.

    Absolute path of the certificate file if \ :emphasis:`import\_certificates`\  is \ :literal:`import`\ .


  restart (optional, bool, False)
    Restart the server to apply the secure boot settings.

    \ :emphasis:`restart`\  will be ignored only when \ :emphasis:`export\_certificates`\  is \ :literal:`true`\ .


  restart_type (optional, str, GracefulRestart)
    Reset type

    \ :literal:`ForceRestart`\  Forcefully reboot the host system.

    \ :literal:`GracefulRestart`\  Gracefully reboot the host system.

    \ :literal:`GracefulRestart`\  Gracefully reboot the host system.

    \ :emphasis:`restart\_type`\  is applicable when i(restart) is \ :literal:`true`\ .


  job_wait (optional, bool, True)
    Provides the option to wait for job completion.


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
   - This module reports changes found when ran in check\_mode for \ :emphasis:`import\_certificates`\ .
   - This module does not support idempotency when \ :emphasis:`import\_certificates`\  is provided.
   - This module supports both IPv4 and IPv6 address.
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Import a SecureBoot certificate.
      dellemc.openmanage.idrac_secureboot:
        import: true
        platform_key: /user/name/certificates/pk.pem
        key_exchange_key:
          - /user/name/certificates/kek1.pem
          - /user/name/certificates/kek2.pem
        database:
          - /user/name/certificates/db1.pem
          - /user/name/certificates/db2.pem
        disallow_database:
          - /user/name/certificates/dbx1.pem
          - /user/name/certificates/dbx2.pem



Return Values
-------------

msg (always, str, The Secure Boot Certificate Import operation has completed successfully.)
  Status of the secure boot operation.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Abhishek Sinha(@ABHISHEK-SINHA10)

