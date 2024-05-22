.. _ome_device_network_services_module:


ome_device_network_services -- Configure chassis network services settings on OpenManage Enterprise Modular
===========================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to configure the network services on OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  device_id (optional, int, None)
    The ID of the chassis for which the settings need to be updated.

    If the device ID is not specified, this module updates the network services settings for the \ :emphasis:`hostname`\ .

    \ :emphasis:`device\_id`\  is mutually exclusive with \ :emphasis:`device\_service\_tag`\ .


  device_service_tag (optional, str, None)
    The service tag of the chassis for which the setting needs to be updated.

    If the device service tag is not specified, this module updates the network services settings for the \ :emphasis:`hostname`\ .

    \ :emphasis:`device\_service\_tag`\  is mutually exclusive with \ :emphasis:`device\_id`\ .


  snmp_settings (optional, dict, None)
    The settings for SNMP configuration.


    enabled (True, bool, None)
      Enables or disables the SNMP settings.


    port_number (optional, int, None)
      The SNMP port number.


    community_name (optional, str, None)
      The SNMP community string.

      Required when \ :emphasis:`enabled`\  is \ :literal:`true`\ .



  ssh_settings (optional, dict, None)
    The settings for SSH configuration.


    enabled (True, bool, None)
      Enables or disables the SSH settings.


    port_number (optional, int, None)
      The port number for SSH service.


    max_sessions (optional, int, None)
      Number of SSH sessions.


    max_auth_retries (optional, int, None)
      The number of retries when the SSH session fails.


    idle_timeout (optional, float, None)
      SSH idle timeout in minutes.



  remote_racadm_settings (optional, dict, None)
    The settings for remote RACADM configuration.


    enabled (True, bool, None)
      Enables or disables the remote RACADM settings.



  hostname (True, str, None)
    OpenManage Enterprise Modular IP address or hostname.


  username (False, str, None)
    OpenManage Enterprise Modular username.

    If the username is not provided, then the environment variable \ :envvar:`OME\_USERNAME`\  is used.

    Example: export OME\_USERNAME=username


  password (False, str, None)
    OpenManage Enterprise Modular password.

    If the password is not provided, then the environment variable \ :envvar:`OME\_PASSWORD`\  is used.

    Example: export OME\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`OME\_X\_AUTH\_TOKEN`\  is used.

    Example: export OME\_X\_AUTH\_TOKEN=x\_auth\_token


  port (optional, int, 443)
    OpenManage Enterprise Modular HTTPS port.


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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise Modular.
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Update network services settings of a chassis using the device ID
      dellemc.openmanage.ome_device_network_services:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_id: 25011
        snmp_settings:
          enabled: true
          port_number: 161
          community_name: public
        ssh_settings:
          enabled: false
        remote_racadm_settings:
          enabled: false

    - name: Update network services settings of a chassis using the device service tag.
      dellemc.openmanage.ome_device_network_services:
        hostname: "192.168.0.2"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_service_tag: GHRT2RL
        snmp_settings:
          enabled: false
        ssh_settings:
          enabled: true
          port_number: 22
          max_sessions: 1
          max_auth_retries: 3
          idle_timeout: 1
        remote_racadm_settings:
          enabled: false

    - name: Update network services settings of the host chassis.
      dellemc.openmanage.ome_device_network_services:
        hostname: "192.168.0.3"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        snmp_settings:
          enabled: false
        ssh_settings:
          enabled: false
        remote_racadm_settings:
          enabled: true



Return Values
-------------

msg (always, str, Successfully updated the network services settings.)
  Overall status of the network services settings.


network_services_details (success, dict, {'EnableRemoteRacadm': True, 'SettingType': 'NetworkServices', 'SnmpConfiguration': {'PortNumber': 161, 'SnmpEnabled': True, 'SnmpV1V2Credential': {'CommunityName': 'public'}}, 'SshConfiguration': {'IdleTimeout': 60, 'MaxAuthRetries': 3, 'MaxSessions': 1, 'PortNumber': 22, 'SshEnabled': False}})
  returned when network services settings are updated successfully.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'CAPP1042', 'RelatedProperties': [], 'Message': 'Unable to update the network configuration because the SNMP PortNumber is already in use.', 'MessageArgs': ['SNMP PortNumber'], 'Severity': 'Informational', 'Resolution': 'Enter a different port number and retry the operation.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)

