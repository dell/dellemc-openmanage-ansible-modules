.. _redfish_firmware_rollback_module:


redfish_firmware_rollback -- To perform a component firmware rollback using component name
==========================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to rollback the firmware of different server components.

Depending on the component, the firmware update is applied after an automatic or manual reboot.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  name (True, str, None)
    The name or regular expression of the component to match and is case-sensitive.


  reboot (optional, bool, True)
    Reboot the server to apply the previous version of the firmware.

    \ :literal:`true`\  reboots the server to rollback the firmware to the available version.

    \ :literal:`false`\  schedules the rollback of firmware until the next restart.

    When \ :emphasis:`reboot`\  is \ :literal:`false`\ , some components update immediately, and the server may reboot. So, the module must wait till the server is accessible.


  reboot_timeout (optional, int, 900)
    Wait time in seconds. The module waits for this duration till the server reboots.


  baseuri (True, str, None)
    IP address of the target out-of-band controller. For example- \<ipaddress\>:\<port\>.


  username (False, str, None)
    Username of the target out-of-band controller.

    If the username is not provided, then the environment variable \ :envvar:`IDRAC\_USERNAME`\  is used.

    Example: export IDRAC\_USERNAME=username


  password (False, str, None)
    Password of the target out-of-band controller.

    If the password is not provided, then the environment variable \ :envvar:`IDRAC\_PASSWORD`\  is used.

    Example: export IDRAC\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`IDRAC\_X\_AUTH\_TOKEN`\  is used.

    Example: export IDRAC\_X\_AUTH\_TOKEN=x\_auth\_token


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
   - Run this module from a system that has direct access to Redfish APIs.
   - For components that do not require a reboot, firmware rollback proceeds irrespective of \ :emphasis:`reboot`\  is \ :literal:`true`\  or \ :literal:`false`\ .
   - This module supports IPv4 and IPv6 addresses.
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Rollback a BIOS component firmware
      dellemc.openmanage.redfish_firmware_rollback:
        baseuri: "192.168.0.1"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        name: "BIOS"

    - name: Rollback all NIC cards with a name starting from 'Broadcom Gigabit'.
      dellemc.openmanage.redfish_firmware_rollback:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        name: "Broadcom Gigabit Ethernet.*"

    - name: Rollback all the component firmware except BIOS component.
      dellemc.openmanage.redfish_firmware_rollback:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        name: "(?!BIOS).*"

    - name: Rollback all the available firmware component.
      dellemc.openmanage.redfish_firmware_rollback:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        name: ".*"



Return Values
-------------

msg (always, str, Successfully completed the job for firmware rollback.)
  Overall firmware rollback status.


status (success, list, [{'ActualRunningStartTime': '2023-08-04T12:26:55', 'ActualRunningStopTime': '2023-08-04T12:32:35', 'CompletionTime': '2023-08-04T12:32:35', 'Description': 'Job Instance', 'EndTime': 'TIME_NA', 'Id': 'JID_911698303631', 'JobState': 'Completed', 'JobType': 'FirmwareUpdate', 'Message': 'Job completed successfully.', 'MessageArgs': [], 'MessageId': 'PR19', 'Name': 'Firmware Rollback: Firmware', 'PercentComplete': 100, 'StartTime': '2023-08-04T12:23:50', 'TargetSettingsURI': None}])
  Firmware rollback job and progress details from the iDRAC.


error_info (on http error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'InstanceID value provided for the update operation is invalid', 'MessageArgs': [], 'MessageArgs@odata.count': 0, 'MessageId': 'IDRAC.2.8.SUP024', 'RelatedProperties': [], 'RelatedProperties@odata.count': 0, 'Resolution': 'Enumerate inventory, copy the InstanceID value and provide that value for the update operation.', 'Severity': 'Warning'}], 'code': 'Base.1.12.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information'}})
  Details of the HTTP error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)

