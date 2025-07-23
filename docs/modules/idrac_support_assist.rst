.. _idrac_support_assist_module:


idrac_support_assist -- Run and Export iDRAC SupportAssist collection logs
==========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows you to run and export SupportAssist collection logs on iDRAC.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  run (optional, bool, True)
    Run the SupportAssist job based on the different types of logs in the collection on iDRAC.


  export (optional, bool, True)
    Exports the SupportAssist collection to the given network share.

    This operation requires :emphasis:`share\_parameters`.


  accept_eula (optional, bool, None)
    This parameter accepts the EULA terms and conditions that are required for SupportAssist registration.

    If EULA terms and conditions are not accepted, then the SupportAssist collection cannot be run or exported.


  filter_data (optional, bool, False)
    This option provides the choice to filter data for privacy. It does not include hostname, MAC address, thermal data, logs, or registry content.


  data_collector (optional, list, None)
    This option provides the choice of data to keep in SupportAssist collection.

    System Information is available in on the SupportAssist collection by default.

    :literal:`hardware\_data`\ , SupportAssist collection includes data that are related to hardware.

    :literal:`storage\_logs`\ , SupportAssist collection includes logs that are related to storage devices.

    :literal:`os\_app\_data`\ , SupportAssist collection includes data that is related to the operating system and applications.

    :literal:`debug\_logs`\ , SupportAssist collection includes logs that are related to debugging.

    :literal:`telemetry\_reports`\ , SupportAssist collection includes reports that are related to telemetry.

    :literal:`gpu\_logs`\ , SupportAssist collection includes logs that are related to GPUs.


  job_wait (optional, bool, True)
    This option determines whether to wait for the job completion or not.


  job_wait_timeout (optional, int, 3600)
    Time in seconds to wait for job completion.

    This is applicable when :emphasis:`job\_wait` is :literal:`true`.


  share_parameters (optional, dict, None)
    Parameters that are required for the export operation of SupportAssist collection.

    :emphasis:`share\_parameters` is required when :emphasis:`export` is :literal:`true`.


    share_type (optional, str, local)
      Share type of the network share.

      :literal:`local` uses local path for :emphasis:`export` operation.

      :literal:`nfs` uses NFS share for :emphasis:`export` operation.

      :literal:`cifs` uses CIFS share for :emphasis:`export` operation.

      :literal:`http` uses HTTP share for :emphasis:`export` operation.

      :literal:`https` uses HTTPS share for :emphasis:`export` operation.

      :literal:`ftp` uses FTP share for :emphasis:`export` operation.


    ip_address (optional, str, None)
      IP address of the network share.

      :emphasis:`ip\_address` is required when :emphasis:`share\_type` is :literal:`nfs`\ , :literal:`cifs`\ , :literal:`http`\ , or :literal:`https`.

      :emphasis:`ip\_address` is not required when :emphasis:`share\_type` is :literal:`local`.


    share_name (optional, str, None)
      Network share path or full local path of the directory for exporting the SupportAssist collection file.

      The default path will be current directory when :emphasis:`share\_type` is :literal:`local`


    workgroup (optional, str, None)
      -(deprecated) Workgroup of the network share. - :emphasis:`workgroup` is applicable only when :emphasis:`share\_type` is :literal:`cifs`.


    username (optional, str, None)
      Username of the network share.

      :emphasis:`username` is required when :emphasis:`share\_type` is :literal:`cifs`.


    password (optional, str, None)
      Password of the network share.

      :emphasis:`password` is required when :emphasis:`share\_type` is :literal:`cifs`.


    ignore_certificate_warning (optional, str, off)
      Ignores the certificate warning when connecting to the network share and is only applicable when :emphasis:`share\_type` is :literal:`https`.

      :literal:`on` ignores the certificate warning.

      :literal:`off` does not ignore the certificate warning.


    proxy_support (optional, str, off)
      Specifies if proxy support must be used or not.

      :literal:`off` does not use proxy settings.

      :literal:`default\_proxy` uses the default proxy settings.

      :literal:`parameters\_proxy` uses the specified proxy settings. :emphasis:`proxy\_server` is required when :emphasis:`proxy\_support` is :literal:`parameters\_proxy`.

      :emphasis:`proxy\_support` is only applicable when :emphasis:`share\_type` is :literal:`http` or :literal:`https`.


    proxy_type (optional, str, http)
      The proxy type of the proxy server.

      :literal:`http` to select HTTP proxy.

      :literal:`socks` to select SOCKS proxy.

      :emphasis:`proxy\_type` is only applicable when :emphasis:`share\_type` is :literal:`http` or :literal:`https` and when :emphasis:`proxy\_support` is :literal:`parameters\_proxy`.


    proxy_server (optional, str, None)
      The IP address of the proxy server.

      :emphasis:`proxy\_server` is required when :emphasis:`proxy\_support` is :literal:`parameters\_proxy`.

      :emphasis:`proxy\_server` is only applicable when :emphasis:`share\_type` is :literal:`http` or :literal:`https` and when :emphasis:`proxy\_support` is :literal:`parameters\_proxy`.


    proxy_port (optional, int, 80)
      The port of the proxy server.

      :emphasis:`proxy\_port` is only applicable when :emphasis:`share\_type` is :literal:`http` or :literal:`https` and when :emphasis:`proxy\_support` is :literal:`parameters\_proxy`.


    proxy_username (optional, str, None)
      The username of the proxy server.

      :emphasis:`proxy\_username` is only applicable when :emphasis:`share\_type` is :literal:`http` or :literal:`https` and when :emphasis:`proxy\_support` is :literal:`parameters\_proxy`.


    proxy_password (optional, str, None)
      The password of the proxy server.

      :emphasis:`proxy\_password` is only applicable when :emphasis:`share\_type` is :literal:`http` or :literal:`https` and when :emphasis:`proxy\_support` is :literal:`parameters\_proxy`.



  resource_id (optional, str, None)
    Id of the resource.

    If the value for resource ID is not provided, the module picks the first resource ID available from the list of system resources that are returned by the iDRAC.


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
   - :literal:`local` for :emphasis:`share\_type` is applicable only when :emphasis:`run` and :emphasis:`export` is :literal:`true`.
   - When :emphasis:`share\_type` is :literal:`local` for :emphasis:`run` and (export) operation, then job\_wait is not applicable.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Accept the EULA and run and export the SupportAssist Collection to local path
      dellemc.openmanage.idrac_support_assist:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        accept_eula: true
        ca_path: "path/to/ca_file"
        data_collector: ["debug_logs", "hardware_data", "os_app_data", "storage_logs"]
        share_parameters:
          share_type: "local"
          share_path: "/opt/local/support_assist_collections/"

    - name: Run the SupportAssist Collection with with custom data_to_collect with filter_data
      dellemc.openmanage.idrac_support_assist:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "path/to/ca_file"
        export: false
        filter_data: true
        data_collector: ["debug_logs", "hardware_data"]

    - name: Run and export the SupportAssist Collection to HTTPS share
      dellemc.openmanage.idrac_support_assist:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "path/to/ca_file"
        data_collector: ["hardware_data"]
        share_parameters:
          share_type: "HTTPS"
          ignore_certificate_warning: "on"
          share_name: "/share_path/support_assist_collections"
          ip_address: "192.168.0.2"

    - name: Run and export the SupportAssist Collection to NFS share
      dellemc.openmanage.idrac_support_assist:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "path/to/ca_file"
        data_collector: ["debug_logs"]
        share_parameters:
          share_type: "NFS"
          share_name: "nfsshare/support_assist_collections/"
          ip_address: "192.168.0.3"

    - name: Export the last SupportAssist Collection to CIFS share
      dellemc.openmanage.idrac_support_assist:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "path/to/ca_file"
        run: false
        share_parameters:
          share_type: "NFS"
          share_name: "/cifsshare/support_assist_collections/"
          ip_address: "192.168.0.4"

    - name: Export the last SupportAssist Collection to HTTPS share via proxy
      dellemc.openmanage.idrac_support_assist:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "path/to/ca_file"
        run: false
        share_parameters:
          share_type: "HTTPS"
          share_name: "/share_path/support_assist_collections"
          ignore_certificate_warning: "on"
          ip_address: "192.168.0.2"
          proxy_support: parameters_proxy
          proxy_type: http
          proxy_server: "192.168.0.5"
          proxy_port: 1080
          proxy_username: "proxy_user"
          proxy_password: "proxy_password"



Return Values
-------------

msg (always, str, Successfully ran and exported the SupportAssist collection.)
  Status of the SupportAssist operation.


job_details (For run and export operations, dict, {'ActualRunningStartTime': '2024-07-08T01:50:54', 'ActualRunningStopTime': '2024-07-08T01:56:45', 'CompletionTime': '2024-07-08T01:56:45', 'Description': 'Job Instance', 'EndTime': None, 'Id': 'JID_XXXXXXXXXXXX', 'JobState': 'Completed', 'JobType': 'SACollectExportHealthData', 'Message': 'The SupportAssist Collection and Transmission Operation is completed successfully.', 'MessageArgs': [], 'MessageArgs@odata.count': 0, 'MessageId': 'SRV088', 'Name': 'SupportAssist Collection', 'PercentComplete': 100, 'StartTime': '2024-07-08T01:50:54', 'TargetSettingsURI': None})
  Returns the output for status of the job.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.12.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'Message': 'Unable to start the operation because the SupportAssist End User License Agreement (EULA) is not accepted.', 'MessageArgs': [], 'MessageArgs@odata.count': 0, 'MessageId': 'IDRAC.2.8.SRV085', 'RelatedProperties': [], 'RelatedProperties@odata.count': 0, 'Resolution': 'Accept the SupportAssist End User License Agreement (EULA) by navigating to the SupportAssist page on the iDRAC GUI.', 'Severity': 'Warning'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Shivam Sharma(@ShivamSh3)

