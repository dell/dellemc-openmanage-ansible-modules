.. _ome_application_network_webserver_module:


ome_application_network_webserver -- Updates the Web server configuration on OpenManage Enterprise
==================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to configure a network web server on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  webserver_port (optional, int, None)
    Port number used by OpenManage Enterprise to establish a secure server connection.

    \ :emphasis:`WARNING`\  A change in port number results in a loss of connectivity in the current session for more than a minute.


  webserver_timeout (optional, int, None)
    The duration in minutes after which a web user interface session is automatically disconnected.

    If a change is made to the session timeout, it will only take effect after the next log in.


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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Update web server port and session time out
      dellemc.openmanage.ome_application_network_webserver:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        webserver_port: 9443
        webserver_timeout: 20

    - name: Update session time out
      dellemc.openmanage.ome_application_network_webserver:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        webserver_timeout: 30

    - name: Update web server port
      dellemc.openmanage.ome_application_network_webserver:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        webserver_port: 8443



Return Values
-------------

msg (always, str, Successfully updated network web server configuration.)
  Overall status of the network web server configuration change.


webserver_configuration (success, dict, {'TimeOut': 20, 'PortNumber': 443, 'EnableWebServer': True})
  Updated application network web server configuration.


error_info (on HTTP error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to complete the request because the input value for  PortNumber  is missing or an invalid value is entered.', 'MessageArgs': ['PortNumber'], 'MessageId': 'CGEN6002', 'RelatedProperties': [], 'Resolution': 'Enter a valid value and retry the operation.', 'Severity': 'Critical'}], 'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.'}})
  Details of the HTTP error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

