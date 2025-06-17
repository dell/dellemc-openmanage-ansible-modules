.. _idrac_system_erase_module:


idrac_system_erase -- Erase system and storage components of the server
=======================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows you to erase system components such as iDRAC, BIOS, DIAG, and so forth. You can also erase storage components such as PERC NV cache, non-volatile memory, cryptographic erase of physical disks, and so on of the server



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  component (True, list, None)
    List of system and storage components that can be deleted.

    The following are the supported components. AllApps BIOS CryptographicErasePD DIAG DPU DrvPack IDRAC LCData NonVolatileMemory OverwritePD PERCNVCache ReinstallFW vFlash


  power_on (optional, bool, False)
    This parameter allows you to power on the server after the erase operation is completed. This is applicable when :emphasis:`job\_wait` is :literal:`true`.

    :literal:`true` power on the server.

    :literal:`false` does not power on the server.


  job_wait (optional, bool, True)
    Whether to wait till completion of the job. This is applicable when :emphasis:`power\_on` is :literal:`true`.

    :literal:`true` waits for job completion.

    :literal:`false` does not wait for job completion.


  job_wait_timeout (optional, int, 1200)
    The maximum wait time of :emphasis:`job\_wait` in seconds. The job is tracked only for this duration.

    This option is applicable when :emphasis:`job\_wait` is :literal:`true`.


  resource_id (optional, str, None)
    Manager ID of the iDRAC.


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
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports only iDRAC9 and above.
   - This module supports IPv4 and IPv6 addresses.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Erase a single component and power on the server
      dellemc.openmanage.idrac_system_erase:
        idrac_ip: 198.162.0.1
        idrac_user: username
        idrac_password: passw0rd
        ca_path: "/path/to/ca_cert.pem"
        component: ["BIOS"]
        power_on: true

    - name: Erase multiple components and do not power on the server after the erase operation is completed
      dellemc.openmanage.idrac_system_erase:
        idrac_ip: 198.162.0.1
        idrac_user: username
        idrac_password: passw0rd
        ca_path: "/path/to/ca_cert.pem"
        component: ["BIOS", "DIAG", "PERCNVCache"]

    - name: Erase multiple components and do not wait for the job completion
      dellemc.openmanage.idrac_system_erase:
        idrac_ip: 198.162.0.1
        idrac_user: username
        idrac_password: passw0rd
        ca_path: "/path/to/ca_cert.pem"
        component: ["IDRAC", "DPU", "LCData"]
        job_wait: false



Return Values
-------------

msg (always, str, Successfully completed the system erase operation.)
  Status of the component system erase operation.


job_details (For system erase operation, dict, {'ActualRunningStartTime': None, 'ActualRunningStopTime': None, 'CompletionTime': '2024-08-06T19:55:01', 'Description': 'Job Instance', 'EndTime': 'TIME_NA', 'Id': 'JID_229917427823', 'JobState': 'Completed', 'JobType': 'SystemErase', 'Message': 'Job completed successfully.', 'MessageArgs': [], 'MessageArgs@odata.count': 0, 'MessageId': 'SYS018', 'Name': 'System_Erase', 'PercentComplete': 100, 'StartTime': '2024-08-06T19:49:02', 'TargetSettingsURI': None})
  Returns the output for status of the job.


error_info (On HTTP error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to complete the operation because the value NonVolatileMemor entered for the property Component is not in the list of acceptable values.', 'MessageArgs': ['NonVolatileMemor', 'Component'], 'MessageArgs@odata.count': 2, 'MessageId': 'IDRAC.2.9.SYS426', 'RelatedProperties': [], 'RelatedProperties@odata.count': 0, 'Resolution': "Enter a valid value from the enumeration list that Redfish service supports and retry the operation.For information about valid values, see the iDRAC User's Guide available on the support site.", 'Severity': 'Warning'}, {'Message': "The value 'NonVolatileMemor' for the property Component is not in the list of acceptable values.", 'MessageArgs': ['NonVolatileMemor', 'Component'], 'MessageArgs@odata.count': 2, 'MessageId': 'Base.1.12.PropertyValueNotInList', 'RelatedProperties': [], 'RelatedProperties@odata.count': 0, 'Resolution': 'Choose a value from the enumeration list that the implementation can support and resubmit the request if the operation failed.', 'Severity': 'Warning'}], 'code': 'Base.1.12.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information'}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Rajshekar P(@rajshekarp87)
- Saksham Nautiyal (@Saksham-Nautiyal)

