.. _idrac_license_module:


idrac_license -- Configure iDRAC licenses
=========================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to import, export and delete licenses on iDRAC.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  license_id (optional, str, None)
    Entitlement ID of the license that is to be imported, exported or deleted.

    \ :emphasis:`license\_id`\  is required when \ :emphasis:`delete`\  is \ :literal:`true`\  or \ :emphasis:`export`\  is \ :literal:`true`\ .


  delete (optional, bool, False)
    Delete the license from the iDRAC.

    When \ :emphasis:`delete`\  is \ :literal:`true`\ , then \ :emphasis:`license\_id`\  is required.

    \ :emphasis:`delete`\  is mutually exclusive with \ :emphasis:`export`\  and \ :emphasis:`import`\ .


  export (optional, bool, False)
    Export the license from the iDRAC.

    When \ :emphasis:`export`\  is \ :literal:`true`\ , \ :emphasis:`license\_id`\  and \ :emphasis:`share\_parameters`\  is required.

    \ :emphasis:`export`\  is mutually exclusive with \ :emphasis:`delete`\  and \ :emphasis:`import`\ .


  import (optional, bool, False)
    Import the license from the iDRAC.

    When \ :emphasis:`import`\  is \ :literal:`true`\ , \ :emphasis:`share\_parameters`\  is required.

    \ :emphasis:`import`\  is mutually exclusive with \ :emphasis:`delete`\  and \ :emphasis:`export`\ .


  share_parameters (optional, dict, None)
    Parameters that are required for the import and export operation of a license.

    \ :emphasis:`share\_parameters`\  is required when \ :emphasis:`export`\  or \ :emphasis:`import`\  is \ :literal:`true`\ .


    share_type (optional, str, local)
      Share type of the network share.

      \ :literal:`local`\  uses local path for \ :emphasis:`import`\  and \ :emphasis:`export`\  operation.

      \ :literal:`nfs`\  uses NFS share for \ :emphasis:`import`\  and \ :emphasis:`export`\  operation.

      \ :literal:`cifs`\  uses CIFS share for \ :emphasis:`import`\  and \ :emphasis:`export`\  operation.

      \ :literal:`http`\  uses HTTP share for \ :emphasis:`import`\  and \ :emphasis:`export`\  operation.

      \ :literal:`https`\  uses HTTPS share for \ :emphasis:`import`\  and \ :emphasis:`export`\  operation.


    file_name (optional, str, None)
      License file name for \ :emphasis:`import`\  and \ :emphasis:`export`\  operation.

      \ :emphasis:`file\_name`\  is required when \ :emphasis:`import`\  is \ :literal:`true`\ .

      For the \ :emphasis:`import`\  operation, when \ :emphasis:`share\_type`\  is \ :literal:`local`\ , the supported extensions for \ :emphasis:`file\_name`\  are '.txt' and '.xml'. For other share types, the supported extension is '.xml'


    ip_address (optional, str, None)
      IP address of the network share.

      \ :emphasis:`ip\_address`\  is required when \ :emphasis:`share\_type`\  is \ :literal:`nfs`\ , \ :literal:`cifs`\ , \ :literal:`http`\  or \ :literal:`https`\ .


    share_name (optional, str, None)
      Network share or local path of the license file.


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
      Specifies if proxy is to be used or not.

      \ :literal:`off`\  does not use proxy settings.

      \ :literal:`default\_proxy`\  uses the default proxy settings.

      \ :literal:`parameters\_proxy`\  uses the specified proxy settings. \ :emphasis:`proxy\_server`\  is required when \ :emphasis:`proxy\_support`\  is \ :literal:`parameters\_proxy`\ .

      \ :emphasis:`proxy\_support`\  is only applicable when \ :emphasis:`share\_type`\  is \ :literal:`https`\  or \ :literal:`https`\ .


    proxy_type (optional, str, http)
      The proxy type of the proxy server.

      \ :literal:`http`\  to select HTTP proxy.

      \ :literal:`socks`\  to select SOCKS proxy.

      \ :emphasis:`proxy\_type`\  is only applicable when \ :emphasis:`share\_type`\  is \ :literal:`https`\  or \ :literal:`https`\  and when \ :emphasis:`proxy\_support`\  is \ :literal:`parameters\_proxy`\ .


    proxy_server (optional, str, None)
      The IP address of the proxy server.

      \ :emphasis:`proxy\_server`\  is required when \ :emphasis:`proxy\_support`\  is \ :literal:`parameters\_proxy`\ .

      \ :emphasis:`proxy\_server`\  is only applicable when \ :emphasis:`share\_type`\  is \ :literal:`https`\  or \ :literal:`https`\  and when \ :emphasis:`proxy\_support`\  is \ :literal:`parameters\_proxy`\ .


    proxy_port (optional, int, 80)
      The port of the proxy server.

      \ :emphasis:`proxy\_port`\  is only applicable when \ :emphasis:`share\_type`\  is \ :literal:`https`\  or \ :literal:`https`\  and when \ :emphasis:`proxy\_support`\  is \ :literal:`parameters\_proxy`\ .


    proxy_username (optional, str, None)
      The username of the proxy server.

      \ :emphasis:`proxy\_username`\  is only applicable when \ :emphasis:`share\_type`\  is \ :literal:`https`\  or \ :literal:`https`\  and when \ :emphasis:`proxy\_support`\  is \ :literal:`parameters\_proxy`\ .


    proxy_password (optional, str, None)
      The password of the proxy server.

      \ :emphasis:`proxy\_password`\  is only applicable when \ :emphasis:`share\_type`\  is \ :literal:`https`\  or \ :literal:`https`\  and when \ :emphasis:`proxy\_support`\  is \ :literal:`parameters\_proxy`\ .



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
   - This module does not support \ :literal:`check\_mode`\ .
   - When \ :emphasis:`share\_type`\  is \ :literal:`local`\  for \ :emphasis:`import`\  and \ :emphasis:`export`\  operations, job\_details are not displayed.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Export a license from iDRAC to local
      dellemc.openmanage.idrac_license:
        idrac_ip: "192.168.0.1"
        idrac_user: "username"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        license_id: "LICENSE_123"
        export: true
        share_parameters:
          share_type: "local"
          share_name: "/path/to/share"
          file_name: "license_file"

    - name: Export a license from iDRAC to NFS share
      dellemc.openmanage.idrac_license:
        idrac_ip: "192.168.0.1"
        idrac_user: "username"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        license_id: "LICENSE_123"
        export: true
        share_parameters:
          share_type: "nfs"
          share_name: "/path/to/share"
          file_name: "license_file"
          ip_address: "192.168.0.1"

    - name: Export a license from iDRAC to CIFS share
      dellemc.openmanage.idrac_license:
        idrac_ip: "192.168.0.1"
        idrac_user: "username"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        license_id: "LICENSE_123"
        export: true
        share_parameters:
          share_type: "cifs"
          share_name: "/path/to/share"
          file_name: "license_file"
          ip_address: "192.168.0.1"
          username: "username"
          password: "password"
          workgroup: "workgroup"

    - name: Export a license from iDRAC to HTTP share via proxy
      dellemc.openmanage.idrac_license:
        idrac_ip: "192.168.0.1"
        idrac_user: "username"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        license_id: "LICENSE_123"
        export: true
        share_parameters:
          share_type: "http"
          share_name: "/path/to/share"
          file_name: "license_file"
          ip_address: "192.168.0.1"
          username: "username"
          password: "password"
          proxy_support: "parameters_proxy"
          proxy_type: socks
          proxy_server: "192.168.0.2"
          proxy_port: 1080
          proxy_username: "proxy_username"
          proxy_password: "proxy_password"

    - name: Export a license from iDRAC to HTTPS share
      dellemc.openmanage.idrac_license:
        idrac_ip: "192.168.0.1"
        idrac_user: "username"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        license_id: "LICENSE_123"
        export: true
        share_parameters:
          share_type: "https"
          share_name: "/path/to/share"
          file_name: "license_file"
          ip_address: "192.168.0.1"
          username: "username"
          password: "password"
          ignore_certificate_warning: "on"

    - name: Import a license to iDRAC from local
      dellemc.openmanage.idrac_license:
        idrac_ip: 198.162.0.1
        idrac_user: "username"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        import: true
        share_parameters:
          file_name: "license_file_name.xml"
          share_type: local
          share_name: "/path/to/share"

    - name: Import a license to iDRAC from NFS share
      dellemc.openmanage.idrac_license:
        idrac_ip: 198.162.0.1
        idrac_user: "username"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        import: true
        share_parameters:
          file_name: "license_file_name.xml"
          share_type: nfs
          ip_address: "192.168.0.1"
          share_name: "/path/to/share"

    - name: Import a license to iDRAC from CIFS share
      dellemc.openmanage.idrac_license:
        idrac_ip: 198.162.0.1
        idrac_user: "username"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        import: true
        share_parameters:
          file_name: "license_file_name.xml"
          share_type: cifs
          ip_address: "192.168.0.1"
          share_name: "/path/to/share"
          username: "username"
          password: "password"

    - name: Import a license to iDRAC from HTTP share
      dellemc.openmanage.idrac_license:
        idrac_ip: 198.162.0.1
        idrac_user: "username"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        import: true
        share_parameters:
          file_name: "license_file_name.xml"
          share_type: http
          ip_address: "192.168.0.1"
          share_name: "/path/to/share"
          username: "username"
          password: "password"

    - name: Import a license to iDRAC from HTTPS share via proxy
      dellemc.openmanage.idrac_license:
        idrac_ip: 198.162.0.1
        idrac_user: "username"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        import: true
        share_parameters:
          file_name: "license_file_name.xml"
          share_type: https
          ip_address: "192.168.0.1"
          share_name: "/path/to/share"
          username: "username"
          password: "password"
          proxy_support: "parameters_proxy"
          proxy_server: "192.168.0.2"
          proxy_port: 808
          proxy_username: "proxy_username"
          proxy_password: "proxy_password"

    - name: Delete a License from iDRAC
      dellemc.openmanage.idrac_license:
        idrac_ip: 198.162.0.1
        idrac_user: "username"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        license_id: "LICENCE_123"
        delete: true



Return Values
-------------

msg (always, str, Successfully exported the license.)
  Status of the license operation.


job_details (For import and export operations, dict, {'ActualRunningStartTime': '2024-01-09T05:16:19', 'ActualRunningStopTime': '2024-01-09T05:16:19', 'CompletionTime': '2024-01-09T05:16:19', 'Description': 'Job Instance', 'EndTime': None, 'Id': 'JID_XXXXXXXXX', 'JobState': 'Completed', 'JobType': 'LicenseExport', 'Message': 'The command was successful.', 'MessageArgs': [], 'MessageId': 'LIC900', 'Name': 'Export: License', 'PercentComplete': 100, 'StartTime': '2024-01-09T05:16:19', 'TargetSettingsURI': None})
  Returns the output for status of the job.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.8.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'Base.1.8.AccessDenied', 'Message': 'The authentication credentials included with this request are missing or invalid.', 'MessageArgs': [], 'RelatedProperties': [], 'Severity': 'Critical', 'Resolution': 'Attempt to ensure that the URI is correct and that the service has the appropriate credentials.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Rajshekar P(@rajshekarp87)

