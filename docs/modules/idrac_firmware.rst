.. _idrac_firmware_module:


idrac_firmware -- Firmware update from a repository on a network share (CIFS, NFS, HTTP, HTTPS, FTP)
====================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Update the Firmware by connecting to a network share (CIFS, NFS, HTTP, HTTPS, FTP) that contains a catalog of available updates.

Network share should contain a valid repository of Update Packages (DUPs) and a catalog file describing the DUPs.

All applicable updates contained in the repository are applied to the system.

This feature is available only with iDRAC Enterprise License.



Requirements
------------
The below requirements are needed on the host that executes this module.

- omsdk \>= 1.2.503
- python \>= 3.9.6



Parameters
----------

  share_name (True, str, None)
    Network share path of update repository. CIFS, NFS, HTTP, HTTPS and FTP share types are supported.


  share_user (optional, str, None)
    Network share user in the format 'user@domain' or 'domain\\\\user' if user is part of a domain else 'user'. This option is mandatory for CIFS Network Share.


  share_password (optional, str, None)
    Network share user password. This option is mandatory for CIFS Network Share.


  share_mnt (optional, str, None)
    Local mount path of the network share with read-write permission for ansible user.

    This option is not applicable for HTTP, HTTPS, and FTP shares.


  job_wait (optional, bool, True)
    Whether to wait for job completion or not.


  catalog_file_name (optional, str, Catalog.xml)
    Catalog file name relative to the \ :emphasis:`share\_name`\ .


  ignore_cert_warning (optional, bool, True)
    Specifies if certificate warnings are ignored when HTTPS share is used. If \ :literal:`true`\  option is set, then the certificate warnings are ignored.


  apply_update (optional, bool, True)
    If \ :emphasis:`apply\_update`\  is set to \ :literal:`true`\ , then the packages are applied.

    If \ :emphasis:`apply\_update`\  is set to \ :literal:`false`\ , no updates are applied, and a catalog report of packages is generated and returned.


  reboot (optional, bool, False)
    Provides the option to apply the update packages immediately or in the next reboot.

    If \ :emphasis:`reboot`\  is set to \ :literal:`true`\ ,  then the packages  are applied immediately.

    If \ :emphasis:`reboot`\  is set to \ :literal:`false`\ , then the packages are staged and applied in the next reboot.

    Packages that do not require a reboot are applied immediately irrespective of I (reboot).


  proxy_support (optional, str, Off)
    Specifies if a proxy should be used.

    Proxy parameters are applicable on \ :literal:`HTTP`\ , \ :literal:`HTTPS`\ , and \ :literal:`FTP`\  share type of repositories.

    \ :literal:`ParametersProxy`\ , sets the proxy parameters for the current firmware operation.

    \ :literal:`DefaultProxy`\ , iDRAC uses the proxy values set by default.

    Default Proxy can be set in the Lifecycle Controller attributes using \ :ref:`dellemc.openmanage.idrac\_attributes <ansible_collections.dellemc.openmanage.idrac_attributes_module>`\ .

    \ :literal:`Off`\ , will not use the proxy.

    For iDRAC8 based servers, use proxy server with basic authentication.

    For iDRAC9 based servers, ensure that you use digest authentication for the proxy server, basic authentication is not supported.


  proxy_server (optional, str, None)
    The IP address of the proxy server.

    This IP will not be validated. The download job will be created even for invalid \ :emphasis:`proxy\_server`\ . Please check the results of the job for error details.

    This is required when \ :emphasis:`proxy\_support`\  is \ :literal:`ParametersProxy`\ .


  proxy_port (optional, int, None)
    The Port for the proxy server.

    This is required when \ :emphasis:`proxy\_support`\  is \ :literal:`ParametersProxy`\ .


  proxy_type (optional, str, None)
    The proxy type of the proxy server.

    This is required when \ :emphasis:`proxy\_support`\  is \ :literal:`ParametersProxy`\ .

    Note: SOCKS4 proxy does not support IPv6 address.


  proxy_uname (optional, str, None)
    The user name for the proxy server.


  proxy_passwd (optional, str, None)
    The password for the proxy server.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.

    If the username is not provided, then the environment variable \ :envvar:`IDRAC\_USERNAME`\  is used.

    Example: export IDRAC\_USERNAME=username


  idrac_password (True, str, None)
    iDRAC user password.

    If the password is not provided, then the environment variable \ :envvar:`IDRAC\_PASSWORD`\  is used.

    Example: export IDRAC\_PASSWORD=password


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
   - Module will report success based on the iDRAC firmware update parent job status if there are no individual component jobs present.
   - For server with iDRAC firmware 5.00.00.00 and later, if the repository contains unsupported packages, then the module will return success with a proper message.
   - This module supports both IPv4 and IPv6 address for \ :emphasis:`idrac\_ip`\  and \ :emphasis:`share\_name`\ .
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Update firmware from repository on a NFS Share
      dellemc.openmanage.idrac_firmware:
           idrac_ip: "192.168.0.1"
           idrac_user: "user_name"
           idrac_password: "user_password"
           ca_path: "/path/to/ca_cert.pem"
           share_name: "192.168.0.0:/share"
           reboot: true
           job_wait: true
           apply_update: true
           catalog_file_name: "Catalog.xml"

    - name: Update firmware from repository on a CIFS Share
      dellemc.openmanage.idrac_firmware:
           idrac_ip: "192.168.0.1"
           idrac_user: "user_name"
           idrac_password: "user_password"
           ca_path: "/path/to/ca_cert.pem"
           share_name: "full_cifs_path"
           share_user: "share_user"
           share_password: "share_password"
           reboot: true
           job_wait: true
           apply_update: true
           catalog_file_name: "Catalog.xml"

    - name: Update firmware from repository on a HTTP
      dellemc.openmanage.idrac_firmware:
           idrac_ip: "192.168.0.1"
           idrac_user: "user_name"
           idrac_password: "user_password"
           ca_path: "/path/to/ca_cert.pem"
           share_name: "http://downloads.dell.com"
           reboot: true
           job_wait: true
           apply_update: true

    - name: Update firmware from repository on a HTTPS
      dellemc.openmanage.idrac_firmware:
           idrac_ip: "192.168.0.1"
           idrac_user: "user_name"
           idrac_password: "user_password"
           ca_path: "/path/to/ca_cert.pem"
           share_name: "https://downloads.dell.com"
           reboot: true
           job_wait: true
           apply_update: true

    - name: Update firmware from repository on a HTTPS via proxy
      dellemc.openmanage.idrac_firmware:
           idrac_ip: "192.168.0.1"
           idrac_user: "user_name"
           idrac_password: "user_password"
           ca_path: "/path/to/ca_cert.pem"
           share_name: "https://downloads.dell.com"
           reboot: true
           job_wait: true
           apply_update: true
           proxy_support: ParametersProxy
           proxy_server: 192.168.1.10
           proxy_type: HTTP
           proxy_port: 80
           proxy_uname: "proxy_user"
           proxy_passwd: "proxy_pwd"

    - name: Update firmware from repository on a FTP
      dellemc.openmanage.idrac_firmware:
           idrac_ip: "192.168.0.1"
           idrac_user: "user_name"
           idrac_password: "user_password"
           ca_path: "/path/to/ca_cert.pem"
           share_name: "ftp://ftp.mydomain.com"
           reboot: true
           job_wait: true
           apply_update: true



Return Values
-------------

msg (always, str, Successfully updated the firmware.)
  Overall firmware update status.


update_status (success, dict, {'InstanceID': 'JID_XXXXXXXXXXXX', 'JobState': 'Completed', 'Message': 'Job completed successfully.', 'MessageId': 'REDXXX', 'Name': 'Repository Update', 'JobStartTime': 'NA', 'Status': 'Success'})
  Firmware Update job and progress details from the iDRAC.





Status
------





Authors
~~~~~~~

- Rajeev Arakkal (@rajeevarakkal)
- Felix Stephen (@felixs88)
- Jagadeesh N V (@jagadeeshnv)

