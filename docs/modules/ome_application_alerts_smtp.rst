.. _ome_application_alerts_smtp_module:


ome_application_alerts_smtp -- This module allows to configure SMTP or email configurations
===========================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to configure SMTP or email configurations on OpenManage Enterprise and OpenManage Enterprise Modular.






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

    The *credentials* are mandatory if *enable_authentication* is ``True``.

    The module will always report change when this is ``True``.


  credentials (optional, dict, None)
    The credentials for the SMTP server


    username (True, str, None)
      The username to access the SMTP server.


    password (True, str, None)
      The password to access the SMTP server.



  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.


  password (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.





Notes
-----

.. note::
   - The module will always report change when *enable_authentication* is ``True``.
   - Run this module from a system that has direct access to Dell EMC OpenManage Enterprise or OpenManage Enterprise Modular.
   - This module support ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Update SMTP destination server configuration with authentication
      dellemc.openmanage.ome_application_alerts_smtp:
        hostname: "192.168.0.1"
        username: "user_name"
        password: "user_password"
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

