.. _idrac_diagnostics_module:


idrac_diagnostics -- Run and Export iDRAC diagnostics
=====================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows you to run and export diagnostics on iDRAC.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  run (optional, bool, None)
    Run the diagnostics job on iDRAC.

    Run the diagnostics job based on the \ :emphasis:`run\_mode`\  and save the report in the internal storage. \ :emphasis:`reboot\_type`\  is applicable.


  export (optional, bool, None)
    Exports the diagnostics information to the given share.

    This operation requires \ :emphasis:`share\_parameters`\ .

    When \ :emphasis:`run`\  is \ :literal:`true`\  and \ :emphasis:`job\_wait`\  is \ :literal:`false`\ , only then the run diagnostics job is triggered. \ :emphasis:`export`\  is ignored.


  run_mode (optional, str, express)
    This option provides the choices to run the diagnostics.

    \ :literal:`express`\  The express diagnostics runs a test package for each server subsystem. However, it does not run the complete set of tests available in the package for each subsystem.

    \ :literal:`extended`\  The extended diagnostics run all available tests in each test package for all subsystems.

    \ :literal:`long\_run`\  The long-run diagnostics runs express and extended tests.


  reboot_type (optional, str, graceful)
    This option provides the choice to reboot the host immediately to run the diagnostics.

    This is applicable when \ :emphasis:`run`\  is \ :literal:`true`\ .

    \ :literal:`force`\  Forced graceful shutdown signals the operating system to turn off and wait for ten minutes. If the operating system does not turn off, the iDRAC power cycles the system.

    \ :literal:`graceful`\  Graceful shutdown waits for the operating system to turn off and wait for the system to restart.

    \ :literal:`power\_cycle`\  performs a power cycle for a hard reset on the device.


  scheduled_start_time (optional, str, None)
    Schedules the job at the specified time.

    The accepted formats are yyyymmddhhmmss and YYYY-MM-DDThh:mm:ss+HH:MM.

    This is applicable when \ :emphasis:`run`\  is \ :literal:`true`\  and \ :emphasis:`reboot\_type`\  is power\_cycle.


  scheduled_end_time (optional, str, None)
    Run the diagnostic until the specified end date and end time after the \ :emphasis:`scheduled\_start\_time`\ .

    The accepted formats are yyyymmddhhmmss and YYYY-MM-DDThh:mm:ss+HH:MM.

    If the run operation does not complete before the specified end time, then the operation fails.

    This is applicable when \ :emphasis:`run`\  is \ :literal:`True`\  and \ :emphasis:`reboot\_type`\  is \ :literal:`power\_cycle`\ .


  job_wait (optional, bool, True)
    Provides the option to wait for job completion.

    This is applicable when \ :emphasis:`run`\  is \ :literal:`true`\  and \ :emphasis:`reboot\_type`\  is \ :literal:`power\_cycle`\ .

    This is applicable only to run the diagnostics job.


  job_wait_timeout (optional, int, 1200)
    Time in seconds to wait for job completion.

    This is applicable when \ :emphasis:`job\_wait`\  is \ :literal:`true`\ .


  share_parameters (optional, dict, None)
    Parameters that are required for the export operation of diagnostics.

    \ :emphasis:`share\_parameters`\  is required when \ :emphasis:`export`\  is \ :literal:`true`\ .


    share_type (optional, str, local)
      Share type of the network share.

      \ :literal:`local`\  uses local path for \ :emphasis:`export`\  operation.

      \ :literal:`nfs`\  uses NFS share for \ :emphasis:`export`\  operation.

      \ :literal:`cifs`\  uses CIFS share for \ :emphasis:`export`\  operation.

      \ :literal:`http`\  uses HTTP share for \ :emphasis:`export`\  operation.

      \ :literal:`https`\  uses HTTPS share for \ :emphasis:`export`\  operation.


    file_name (optional, str, None)
      Diagnostics file name for \ :emphasis:`export`\  operation.


    ip_address (optional, str, None)
      IP address of the network share.

      \ :emphasis:`ip\_address`\  is required when \ :emphasis:`share\_type`\  is \ :literal:`nfs`\ , \ :literal:`cifs`\ , \ :literal:`http`\  or \ :literal:`https`\ .


    share_name (optional, str, None)
      Network share or local path of the diagnostics file.


    workgroup (optional, str, None)
      Workgroup of the network share.

      \ :emphasis:`workgroup`\  is applicable only when \ :emphasis:`share\_type`\  is \ :literal:`cifs`\ .


    username (optional, str, None)
      Username of the network share.

      \ :emphasis:`username`\  is required when \ :emphasis:`share\_type`\  is \ :literal:`cifs`\ .


    password (optional, str, None)
      Password of the network share.

      \ :emphasis:`password`\  is required when \ :emphasis:`share\_type`\  is \ :literal:`cifs`\ .


    ignore_certificate_warning (optional, str, off)
      Ignores the certificate warning while connecting to Share and is only applicable when \ :emphasis:`share\_type`\  is \ :literal:`https`\ .

      \ :literal:`on`\  ignores the certificate warning.

      \ :literal:`off`\  does not ignore the certificate warning.


    proxy_support (optional, str, off)
      Specifies if proxy support must be used or not.

      \ :literal:`off`\  does not use proxy settings.

      \ :literal:`default\_proxy`\  uses the default proxy settings.

      \ :literal:`parameters\_proxy`\  uses the specified proxy settings. \ :emphasis:`proxy\_server`\  is required when \ :emphasis:`proxy\_support`\  is \ :literal:`parameters\_proxy`\ .

      \ :emphasis:`proxy\_support`\  is only applicable when \ :emphasis:`share\_type`\  is \ :literal:`http`\  or \ :literal:`https`\ .


    proxy_type (optional, str, http)
      The proxy type of the proxy server.

      \ :literal:`http`\  to select HTTP proxy.

      \ :literal:`socks`\  to select SOCKS proxy.

      \ :emphasis:`proxy\_type`\  is only applicable when \ :emphasis:`share\_type`\  is \ :literal:`http`\  or \ :literal:`https`\  and when \ :emphasis:`proxy\_support`\  is \ :literal:`parameters\_proxy`\ .


    proxy_server (optional, str, None)
      The IP address of the proxy server.

      \ :emphasis:`proxy\_server`\  is required when \ :emphasis:`proxy\_support`\  is \ :literal:`parameters\_proxy`\ .

      \ :emphasis:`proxy\_server`\  is only applicable when \ :emphasis:`share\_type`\  is \ :literal:`http`\  or \ :literal:`https`\  and when \ :emphasis:`proxy\_support`\  is \ :literal:`parameters\_proxy`\ .


    proxy_port (optional, int, 80)
      The port of the proxy server.

      \ :emphasis:`proxy\_port`\  is only applicable when \ :emphasis:`share\_type`\  is \ :literal:`http`\  or \ :literal:`https`\  and when \ :emphasis:`proxy\_support`\  is \ :literal:`parameters\_proxy`\ .


    proxy_username (optional, str, None)
      The username of the proxy server.

      \ :emphasis:`proxy\_username`\  is only applicable when \ :emphasis:`share\_type`\  is \ :literal:`http`\  or \ :literal:`https`\  and when \ :emphasis:`proxy\_support`\  is \ :literal:`parameters\_proxy`\ .


    proxy_password (optional, str, None)
      The password of the proxy server.

      \ :emphasis:`proxy\_password`\  is only applicable when \ :emphasis:`share\_type`\  is \ :literal:`http`\  or \ :literal:`https`\  and when \ :emphasis:`proxy\_support`\  is \ :literal:`parameters\_proxy`\ .



  resource_id (optional, str, None)
    Id of the resource.

    If the value for resource ID is not provided, the module picks the first resource ID available from the list of system resources returned by the iDRAC.


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
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports only iDRAC9 and above.
   - This module supports IPv4 and IPv6 addresses.
   - This module supports \ :literal:`check\_mode`\ .
   - This module requires 'Dell Diagnostics' firmware package to be present on the server.
   - When \ :emphasis:`share\_type`\  is \ :literal:`local`\  for \ :emphasis:`export`\  operation, job\_details are not displayed.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Run and export the diagnostics to local path
      dellemc.openmanage.idrac_diagnostics:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "path/to/ca_file"
        run: true
        export: true
        share_parameters:
          share_type: "local"
          share_path: "/opt/local/diagnostics/"
          file_name: "diagnostics.txt"

    - name: Run the diagnostics with power cycle reboot on schedule
      dellemc.openmanage.idrac_diagnostics:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "path/to/ca_file"
        run: true
        run_mode: "express"
        reboot_type: "power_cycle"
        scheduled_start_time: 20240101101015

    - name: Run and export the diagnostics to HTTPS share
      dellemc.openmanage.idrac_diagnostics:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "path/to/ca_file"
        run: true
        export: true
        share_parameters:
          share_type: "HTTPS"
          ignore_certificate_warning: "on"
          share_name: "/share_path/diagnostics_collection_path"
          ip_address: "192.168.0.2"
          file_name: "diagnostics.txt"

    - name: Run and export the diagnostics to NFS share
      dellemc.openmanage.idrac_diagnostics:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "path/to/ca_file"
        run: true
        export: true
        share_parameters:
          share_type: "NFS"
          share_name: "nfsshare/diagnostics_collection_path/"
          ip_address: "192.168.0.3"
          file_name: "diagnostics.txt"

    - name: Export the diagnostics to CIFS share
      dellemc.openmanage.idrac_diagnostics:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "path/to/ca_file"
        export: true
        share_parameters:
          share_type: "CIFS"
          share_name: "/cifsshare/diagnostics_collection_path/"
          ip_address: "192.168.0.4"
          file_name: "diagnostics.txt"

    - name: Export the diagnostics to HTTPS share via proxy
      dellemc.openmanage.idrac_diagnostics:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "path/to/ca_file"
        export: true
        share_parameters:
          share_type: "HTTPS"
          share_name: "/share_path/diagnostics_collection_path"
          ignore_certificate_warning: "on"
          ip_address: "192.168.0.2"
          file_name: "diagnostics.txt"
          proxy_support: parameters_proxy
          proxy_type: http
          proxy_server: "192.168.0.5"
          proxy_port: 1080
          proxy_username: "proxy_user"
          proxy_password: "proxy_password"



Return Values
-------------

msg (always, str, Successfully ran and exported the diagnostics.)
  Status of the diagnostics operation.


job_details (For run and export operations, dict, {'ActualRunningStartTime': '2024-01-10T10:14:31', 'ActualRunningStopTime': '2024-01-10T10:26:34', 'CompletionTime': '2024-01-10T10:26:34', 'Description': 'Job Instance', 'EndTime': '2024-01-10T10:30:15', 'Id': 'JID_XXXXXXXXXXXX', 'JobState': 'Completed', 'JobType': 'RemoteDiagnostics', 'Message': 'Job completed successfully.', 'MessageArgs': [], 'MessageArgs@odata.count': 0, 'MessageId': 'SYS018', 'Name': 'Remote Diagnostics', 'PercentComplete': 100, 'StartTime': '2024-01-10T10:12:15', 'TargetSettingsURI': None})
  Returns the output for status of the job.


diagnostics_file_path (For export operation, str, /share_path/diagnostics_collection_path/diagnostics.txt)
  Returns the full path of the diagnostics file.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.12.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'Message': 'A Remote Diagnostic (ePSA) job already exists.', 'MessageArgs': [], 'MessageArgs@odata.count': 0, 'MessageId': 'IDRAC.2.9.SYS098', 'RelatedProperties': [], 'RelatedProperties@odata.count': 0, 'Resolution': 'A response action is not required if the scheduled start time of the existing Remote Diagnostic (ePSA) job is ok. Else, delete the existing Diagnostics (ePSA) job and recreate another with an appropriate start time.', 'Severity': 'Informational'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Shivam Sharma(@ShivamSh3)

