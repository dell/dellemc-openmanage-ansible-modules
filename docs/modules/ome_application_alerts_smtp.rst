.. _ome_application_alerts_smtp_module:


ome_application_alerts_smtp -- This module allows to configure SMTP or email configurations
===========================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to configure SMTP or email configurations on OpenManage Enterprise and OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  destination_address (True, str, None)
    The IP address or FQDN of the SMTP destination server.


  port_number (optional, int, None)
    The port number of the SMTP destination server.


  use_ssl (optional, bool, None)
    Use SSL to connect with the SMTP server.


  enable_authentication (True, bool, None)
    Enable or disable authentication to access the SMTP server.

    The \ :emphasis:`credentials`\  are mandatory if \ :emphasis:`enable\_authentication`\  is \ :literal:`true`\ .

    The module will always report change when this is \ :literal:`true`\ .


  credentials (optional, dict, None)
    The credentials for the SMTP server


    username (True, str, None)
      The username to access the SMTP server.


    password (True, str, None)
      The password to access the SMTP server.



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
   - The module will always report change when \ :emphasis:`enable\_authentication`\  is \ :literal:`true`\ .
   - Run this module from a system that has direct access to Dell OpenManage Enterprise or OpenManage Enterprise Modular.
   - This module support \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Update SMTP destination server configuration with authentication
      dellemc.openmanage.ome_application_alerts_smtp:
        hostname: "192.168.0.1"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        destination_address: "localhost"
        port_number: 25
        use_ssl: true
        enable_authentication: true
        credentials:
          username: "username"
          password: "password"
    - name: Update SMTP destination server configuration without authentication
      dellemc.openmanage.ome_application_alerts_smtp:
        hostname: "192.168.0.1"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        destination_address: "localhost"
        port_number: 25
        use_ssl: false
        enable_authentication: false



Return Values
-------------

msg (always, str, Successfully updated the SMTP settings.)
  Overall status of the SMTP settings update.


smtp_details (success, dict, {'DestinationAddress': 'localhost', 'PortNumber': 25, 'UseCredentials': True, 'UseSSL': False, 'Credential': {'User': 'admin', 'Password': None}})
  returned when SMTP settings are updated successfully.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'CAPP1106', 'RelatedProperties': [], 'Message': 'Unable to update the SMTP settings because the entered credential is invalid or empty.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Either enter valid credentials or disable the Use Credentials option and retry the operation.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Sachin Apagundi(@sachin-apa)

