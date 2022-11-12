.. _ome_application_alerts_syslog_module:


ome_application_alerts_syslog -- Configure syslog forwarding settings on OpenManage Enterprise and OpenManage Enterprise Modular
================================================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to configure syslog forwarding settings on OpenManage Enterprise and OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  syslog_servers (optional, list, None)
    List of servers to forward syslog.


    id (True, int, None)
      The ID of the syslog server.


    enabled (optional, bool, None)
      Enable or disable syslog forwarding.


    destination_address (optional, str, None)
      The IP address, FQDN or hostname of the syslog server.

      This is required if *enabled* is ``True``.


    port_number (optional, int, None)
      The UDP port number of the syslog server.



  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.


  password (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.


  validate_certs (optional, bool, True)
    If ``False``, the SSL certificates will not be validated.

    Configure ``False`` only on personally controlled sites where self-signed certificates are used.

    Prior to collection version ``5.0.0``, the *validate_certs* is ``False`` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell OpenManage Enterprise or Dell OpenManage Enterprise Modular.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Configure single server to forward syslog
      dellemc.openmanage.ome_application_alerts_syslog:
        hostname: 192.168.0.1
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        syslog_servers:
          - id: 1
            enabled: true
            destination_address: 192.168.0.2
            port_number: 514

    - name: Configure multiple server to forward syslog
      dellemc.openmanage.ome_application_alerts_syslog:
        hostname: 192.168.0.1
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        syslog_servers:
          - id: 1
            port_number: 523
          - id: 2
            enabled: true
            destination_address: sysloghost1.lab.com
          - id: 3
            enabled: false
          - id: 4
            enabled: true
            destination_address: 192.168.0.4
            port_number: 514



Return Values
-------------

msg (always, str, Successfully updated the syslog forwarding settings.)
  Overall status of the syslog forwarding operation.


syslog_details (on success, list, [{'DestinationAddress': '192.168.10.43', 'Enabled': False, 'Id': 1, 'PortNumber': 514}, {'DestinationAddress': '192.168.10.46', 'Enabled': True, 'Id': 2, 'PortNumber': 514}, {'DestinationAddress': '192.168.10.44', 'Enabled': True, 'Id': 3, 'PortNumber': 514}, {'DestinationAddress': '192.168.10.42', 'Enabled': True, 'Id': 4, 'PortNumber': 515}])
  Syslog forwarding settings list applied.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'CAPP1108', 'RelatedProperties': [], 'Message': 'Unable to update the Syslog settings because the request contains an invalid number of configurations. The request must contain no more than 4 configurations but contains 5.', 'MessageArgs': ['4', '5'], 'Severity': 'Warning', 'Resolution': 'Enter only the required number of configurations as identified in the message and retry the operation.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

