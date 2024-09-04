.. _idrac_secure_boot_module:


idrac_secure_boot -- Configure attributes, import or export secure boot certificate and Reset keys
==================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to import/export the secure boot certificates.

This module allows to enable/disable secure boot, boot mode.

This modules also allows to configure Policies PK, KEK and configure DB, DBX certificates.

This module allows to reset the UEFI Secure Boot keys..



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  boot_mode (optional, str, None)
    Boot Mode of the idrac.

    \ :emphasis:`Uefi`\  Enables the secure boot in uefi mode.

    \ :emphasis:`Bios`\  Enables the secure boot in bios mode.


  secure_boot (optional, str, None)
    UEFI Secure Boot.

    The \ :emphasis:`secure\_boot\_mode`\  can be \ :literal:`Enabled`\  only if \ :emphasis:`boot\_mode`\  is \ :literal:`Uefi`\  and \ :emphasis:`force\_int\_10`\  is \ :literal:`Disabled`\ .

    \ :emphasis:`Enabled`\  enables the Secureboot mode.

    \ :emphasis:`Disabled`\  disables the Secureboot mode.


  secure_boot_mode (optional, str, None)
    The UEFI Secure Boot Mode configures how the Secure Boot Policy are used.

    \ :emphasis:`UserMode`\  set the secure boot mode into an user mode where PK must be installed, and BIOS performs signature verification on programmatic attempts to update policy objects.

    \ :emphasis:`DeployedMode`\  set the secure boot mode into an deployed mode where PK is present, and BIOS performs signature verification on programmatic attempts to update policy objects

    \ :emphasis:`AuditMode`\  set the secure boot mode into an audit mode where PK is not present. The BIOS does not authenticate programmatic updates to the policy objects, and transitions between modes. The BIOS performs a signature verification on pre-boot images and logs the results in the image Execution Information Table, but executes the images whether they pass or fail verification.


  secure_boot_policy (optional, str, None)
    Following are the secure boot policy.

    C (Standard) indicates that the system has default certificates and image digests, or hash loaded from the factory.

    \ :literal:`Custom`\  inherits the standard certificates and image digests that are loaded in the system by default, which you can modify.

    Secure Boot Policy configured as Custom allows you to perform operations such as View, Export, Import, Delete, Delete All, Reset, and Reset.


  force_int_10 (optional, str, None)
    Determines whether the system BIOS will load the legacy video (INT 10h) option ROM from the video controller.

    This field is supported only in UEFI boot mode. This field cannot be set to Enabled if UEFI SecureBoot is enabled.

    \ :literal:`Enabled`\  if the operating system does not support UEFI video output standards.

    \ :literal:`Disabled`\  if the operating system support UEFI video output standards.


  export_certificates (optional, bool, None)
    Export all the available certificates in the specified directory for the given keys.

    \ :emphasis:`export\_cetificates`\  is mutually exclusive with \ :emphasis:`import`\ .

    \ :emphasis:`export\_cetificates`\  is \ :literal:`true`\  either of \ :emphasis:`platform\_key`\  or i(key\_exchange\_key) or \ :emphasis:`database`\  - or \ :emphasis:`disallow\_database`\  is required.


  import_certificates (optional, bool, None)
    Import all the specified key certificates.

    When \ :emphasis:`import\_certificates`\  is \ :literal:`true`\ , then either \ :emphasis:`platform\_key`\ , \ :emphasis:`KEK`\ , \ :emphasis:`database`\ , or \ :emphasis:`disallow\_database`\  is required.


  platform_key (optional, path, None)
    The absolute path of the Platform key certificate file for UEFI secure boot.

    Directory path with write permissions if \ :emphasis:`export\_certificates`\  is \ :literal:`true`\ .


  KEK (optional, list, None)
    A list of absolute paths of the Key Exchange Key (KEK) certificate file for UEFI secure boot.

    Directory path with write permissions if \ :emphasis:`export\_certificates`\  is \ :literal:`true`\ .


  database (optional, list, None)
    A list of absolute paths of the Database certificate file for UEFI secure boot.

    Directory path with write permissions if \ :emphasis:`export\_certificates`\  is \ :literal:`true`\ .


  disallow_database (optional, list, None)
    A list of absolute paths of the Disallow Database certificate file for UEFI secure boot.

    Directory path with write permissions if \ :emphasis:`export\_certificates`\  is \ :literal:`true`\ .


  reset_keys (optional, str, None)
    Resets the UEFI Secure Boot keys.

    \ :literal:`ResetAllKeysToDefault`\  - Reset the content of all UEFI Secure Boot key databases (PK, KEK, DB, DBX) to their default values.

    \ :literal:`DeletePK`\  - Delete the content of the PK UEFI Secure Boot database. This puts the system in Setup Mode.

    \ :literal:`DeleteAllKeys`\  - Delete the content of all UEFI Secure Boot key databases (PK, KEK, DB, DBX). This puts the system in Setup Mode

    \ :literal:`ResetPK`\  - Reset the content of PK UEFI Secure Boot database to their default values.

    \ :literal:`ResetKEK`\ - Reset the content of KEK UEFI Secure Boot database to their default values.

    \ :literal:`ResetDB`\ - Reset the content of DB UEFI Secure Boot database to their default values.

    \ :literal:`ResetDBX`\ - Reset the content of DBX UEFI Secure Boot database to their default values.


  restart (optional, bool, False)
    Secure boot certificate import operation requires a server restart. This parameter provides an option to restart the server.

    \ :literal:`true`\  restarts the server.

    \ :literal:`false`\  does not restart the server.

    \ :emphasis:`restart`\  is applicable when \ :emphasis:`import\_certificates`\  is \ :literal:`true`\ .

    \ :emphasis:`restart`\  will be ignored only when \ :emphasis:`export\_certificates`\  is \ :literal:`true`\ .


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
   - This module does not support idempotency when \ :emphasis:`reset\_type`\  or \ :emphasis:`export\_certificates`\  or \ :emphasis:`import\_certificates`\  is provided.
   - The order of operations set secure boot settings (boot\_mode, secure\_boot, secure\_boot\_mode, secure\_boot\_policy, force\_int\_10),  export,  certificate reset,  import, idrac reset.
   - \ :emphasis:`export\_certificate`\  will export all the certificates of the key defined in the playbook.
   - This module supports IPv4 and IPv6 addresses.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Enable Secureboot.
      dellemc.openmanage.idrac_secure_boot:
        idrac_ip: "192.168.1.2"
        idrac_user: "user"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        secure_boot: "Enabled"

    - name: Set SecureBootMode and SecureBootPolicy and reset iDRAC.
      dellemc.openmanage.idrac_secure_boot:
        idrac_ip: "192.168.1.2"
        idrac_user: "user"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        secure_boot: "Enabled"
        secure_boot_mode: "UserMode"
        secure_boot_policy: "Custom"
        restart: true
        restart_type: "GracefulRestart"

    - name: Reset Secure Boot certificates.
      dellemc.openmanage.idrac_secure_boot:
        idrac_ip: "192.168.1.2"
        idrac_user: "user"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        reset_keys: "ResetAllKeysToDefault"

    - name: Export multiple SecureBoot certificate.
      dellemc.openmanage.idrac_secure_boot:
        idrac_ip: "192.168.1.2"
        idrac_user: "user"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        export_certificates: true
        platform_key: /user/name/export_cert/pk
        KEK:
          - /user/name/export_cert/kek
        database:
          - /user/name/export_cert/db
        disallow_database:
          - /user/name/export_cert/dbx

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
- Lovepreet Singh (@singh-lovepreet1)

