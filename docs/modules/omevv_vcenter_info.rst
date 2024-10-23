.. _omevv_vcenter_info_module:


omevv_vcenter_info -- Retrieve all or specific OpenManage Enterprise vCenter information.
=========================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows you to retrieve all or specific vCenter information from OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  vcenter_hostname (optional, str, None)
    vCenter IP address or hostname.

    If \ :emphasis:`vcenter\_hostname`\  is provided, the module retrieves only specified vCenter information.


  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (False, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.

    If the username is not provided, then the environment variable \ :envvar:`OME\_USERNAME`\  is used.

    Example: export OME\_USERNAME=username


  password (False, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.

    If the password is not provided, then the environment variable \ :envvar:`OME\_PASSWORD`\  is used.

    Example: export OME\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`OME\_X\_AUTH\_TOKEN`\  is used.

    Example: export OME\_X\_AUTH\_TOKEN=x\_auth\_token


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.


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
   - This module supports IPv4 and IPv6 addresses.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Retrieve all vCenter information.
      dellemc.openmanage.omevv_vcenter_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "path/to/ca_file"

    - name: Retrieve specific vCenter information.
      dellemc.openmanage.omevv_vcenter_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "path/to/ca_file"
        vcenter_hostname: xx.xx.xx.xx



Return Values
-------------

msg (always, str, Successfully retrieved the vCenter information.)
  Status of the vCenter information for the retrieve operation.


vcenter_info (success, list, [{'uuid': '77373c7e-d2b0-453b-9888-102499919bd1', 'consoleAddress': 'vcenter_ip_or_hostname', 'description': 'vCenter 8.0', 'registeredExtensions': ['PHM', 'WEBCLIENT', 'PHA', 'VLCM']}, {'uuid': '77373c7e-d2b0-453b-9888-102499919bd2', 'consoleAddress': 'vcenter_ip_or_hostname', 'description': 'vCenter 8.1', 'registeredExtensions': ['PHM', 'WEBCLIENT', 'PHA', 'VLCM']}])
  Information on the vCenter.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Lovepreet Singh (@singh-lovepreet1)

