.. _idrac_secure_boot_module:


idrac_secure_boot -- Configure attributes, import, or export secure boot certificate, and reset keys.
=====================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows you to perform the following operations.\`

Import or Export Secure Boot certificate.

Enable or disable Secure Boot mode.

Configure Platform Key (PK) and Key Exchange Key (KEK) policies

Configure Allow Database (DB) and Disallow Database (DBX) certificates.

Reset UEFI Secure Boot keys.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  boot_mode (optional, str, None)
    Boot mode of the iDRAC. Not supported for 17G iDRAC10 and later.

    :literal:`Uefi` enables the secure boot in UEFI mode.

    :literal:`Bios` enables the secure boot in BIOS mode.


  secure_boot (optional, str, None)
    UEFI Secure Boot.

    The :emphasis:`secure\_boot` can be :literal:`Enabled` only if :emphasis:`boot\_mode` is :literal:`UEFI` and :emphasis:`force\_int\_10` is :literal:`Disabled`.

    :literal:`Disabled` disables the secure boot mode.

    :literal:`Enabled` enables the secure boot mode.


  secure_boot_mode (optional, str, None)
    The UEFI Secure Boot mode configures how to use the Secure Boot Policy.

    :literal:`AuditMode` sets the Secure Boot mode to an Audit mode when Platform Key is not installed on the system. The BIOS does not authenticate updates to the policy objects and transition between modes. BIOS performs a signature verification on pre-boot images and logs the results in the Image Execution Information table, where it processes the images whether the status of verification is pass or fail.

    :literal:`DeployedMode` sets the Secure Boot mode to a Deployed mode when Platform Key is installed on the system, and then BIOS performs a signature verification to update the policy objects.

    :literal:`UserMode` sets the Secure Boot mode to a User mode when Platform Key is installed on the system, and then BIOS performs signature verification to update policy objects.


  secure_boot_policy (optional, str, None)
    The following are the types of Secure Boot policy.

    :literal:`Custom` inherits the standard certificates and image digests that are loaded in the system by default. You can modify the certificates and image digests.

    :literal:`Standard` indicates that the system has default certificates, image digests, or hash loaded from the factory.

    When the Secure Boot Policy is set to Custom, you can perform following operations such as viewing, exporting, importing, deleting, deleting all, and resetting policies.


  force_int_10 (optional, str, None)
    Determines whether the system BIOS loads the legacy video (INT 10h) option ROM from the video controller.

    This parameter is supported only in UEFI boot mode. If UEFI Secure Boot mode is enabled, you cannot enable this parameter.

    This parameter is not supported for 17G iDRAC10 and later.

    :literal:`Disabled` if the operating system supports UEFI video output standards.

    :literal:`Enabled` if the operating system does not support UEFI video output standards.


  export_certificates (optional, bool, None)
    Export all the available certificates in the specified directory for the given keys.

    :emphasis:`export\_cetificates` is mutually exclusive with :emphasis:`import`.

    :emphasis:`export\_cetificates` is :literal:`true` either of :emphasis:`platform\_key` or i(key\_exchange\_key) or :emphasis:`database` - or :emphasis:`disallow\_database` is required.


  import_certificates (optional, bool, None)
    Import all the specified key certificates.

    When :emphasis:`import\_certificates` is :literal:`true`\ , then either :emphasis:`platform\_key`\ , :emphasis:`KEK`\ , :emphasis:`database`\ , or :emphasis:`disallow\_database` is required.


  platform_key (optional, path, None)
    The absolute path of the Platform key certificate file for UEFI secure boot.

    Directory path with write permission when :emphasis:`export\_certificates` is :literal:`true`.


  KEK (optional, list, None)
    A list of absolute paths of the Key Exchange Key (KEK) certificate file for UEFI secure boot.

    Directory path with write permission when :emphasis:`export\_certificates` is :literal:`true`.


  database (optional, list, None)
    A list of absolute paths of the Allow Database(DB) certificate file for UEFI secure boot.

    Directory path with write permission when :emphasis:`export\_certificates` is :literal:`true`.


  disallow_database (optional, list, None)
    A list of absolute paths of the Disallow Database(DBX) certificate file for UEFI secure boot.

    Directory path with write permission when :emphasis:`export\_certificates` is :literal:`true`.


  reset_keys (optional, str, None)
    Resets the UEFI Secure Boot keys.

    :literal:`DeleteAllKeys` deletes the content of all UEFI Secure Boot key databases (PK, KEK, DB, and DBX). This choice configures the system in Setup Mode.

    :literal:`DeletePK` deletes the content of the PK UEFI Secure Boot database. This choice configures the system in Setup Mode.

    :literal:`ResetAllKeysToDefault` resets the content of all UEFI Secure Boot key databases (PK, KEK, DB, and DBX) to their default values.

    :literal:`ResetDB` resets the content of the DB UEFI Secure Boot database to its default values.

    :literal:`ResetDBX` resets the content of the DBX UEFI Secure Boot database to its default values.

    :literal:`ResetKEK` resets the content of the KEK UEFI Secure Boot database to its default values.

    :literal:`ResetPK` resets the content of the PK UEFI Secure Boot database to its default values.


  restart (optional, bool, False)
    Secure boot certificate import operation requires a server restart. This parameter provides an option to restart the server.

    :literal:`true` restarts the server.

    :literal:`false` does not restart the server.

    :emphasis:`restart` is applicable when :emphasis:`import\_certificates` is :literal:`true`.

    :emphasis:`restart` will be ignored only when :emphasis:`export\_certificates` is :literal:`true`.


  restart_type (optional, str, GracefulRestart)
    Restart type of the server.

    :literal:`ForceRestart` forcefully restarts the server.

    :literal:`GracefulRestart` gracefully restarts the server.

    :emphasis:`restart\_type` is applicable when :emphasis:`restart` is :literal:`true`.


  job_wait (optional, bool, True)
    Whether to wait till completion of the secure boot certificate operation. This is applicable when :emphasis:`restart` is :literal:`true`.


  job_wait_timeout (optional, int, 1200)
    The maximum wait time of :emphasis:`job\_wait` in seconds. The job is tracked only for this duration.

    This option is applicable when :emphasis:`job\_wait` is :literal:`true`.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (False, str, None)
    iDRAC username.

    If the username is not provided, then the environment variable :envvar:`IDRAC\_USERNAME` is used.

    Example: export IDRAC\_USERNAME=username


  idrac_password (False, str, None)
    iDRAC user password.

    If the password is not provided, then the environment variable :envvar:`IDRAC\_PASSWORD` is used.

    Example: export IDRAC\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable :envvar:`IDRAC\_X\_AUTH\_TOKEN` is used.

    Example: export IDRAC\_X\_AUTH\_TOKEN=x\_auth\_token


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
   - This module will always report changes found to be applied for :emphasis:`import\_certificates` when run in :literal:`check mode`.
   - This module does not support idempotency when :emphasis:`reset\_type` or :emphasis:`export\_certificates` or :emphasis:`import\_certificates` is provided.
   - To configure the secure boot settings, the idrac\_secure\_boot module performs the following order of operations set attributes, export certificate, reset keys, import certificate, and restart iDRAC.
   - :emphasis:`export\_certificate` will export all the certificates of the key defined in the playbook.
   - This module considers values of :emphasis:`restart` and :emphasis:`job\_wait` only for the last operation in the sequence.
   - This module supports IPv4 and IPv6 addresses.
   - Only :emphasis:`reset\_keys` is supported on iDRAC8.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Enable Secure Boot.
      dellemc.openmanage.idrac_secure_boot:
        idrac_ip: "192.168.1.2"
        idrac_user: "user"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        secure_boot: "Enabled"

    - name: Set Secure Boot mode, Secure Boot policy, and restart iDRAC.
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

    - name: Export multiple Secure Boot certificate.
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

    - name: Import multiple Secure Boot certificate without applying to iDRAC.
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

    - name: Import a Secure Boot certificate and restart the server to apply it.
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
- Rounak Adhikary (@rounak-adhikary)

