.. _redfish_powerstate_module:


redfish_powerstate -- Manage device power state
===============================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to manage the different power states of the specified device.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  resource_id (False, str, None)
    This option is the unique identifier of the device being managed. For example, \ https://%3CI(baseuri\ \>/redfish/v1/Systems/\<\ :emphasis:`resource\_id`\ \>).

    This option is mandatory for \ :emphasis:`base\_uri`\  with multiple devices.

    To get the device details, use the API \ https://%3CI(baseuri\ \>/redfish/v1/Systems) for reset\_type operation and \ https://%3CI(baseuri\ \>/redfish/v1/Chassis) for oem\_reset\_type operation.


  reset_type (False, str, None)
    This option resets the device.

    \ :literal:`ForceOff`\  turns off the device immediately.

    \ :literal:`ForceOn`\  turns on the device immediately.

    \ :literal:`ForceRestart`\  turns off the device immediately, and then restarts the server.

    \ :literal:`GracefulRestart`\  performs graceful shutdown of the device, and then restarts the device.

    \ :literal:`GracefulShutdown`\  performs a graceful shutdown of the device, and then turns off the device.

    \ :literal:`Nmi`\  sends a diagnostic interrupt to the device. This option is usually a nonmaskable interrupt (NMI) on x86 systems.

    \ :literal:`On`\  turns on the device.

    \ :literal:`PowerCycle`\  performs a power cycle on the device.

    \ :literal:`PushPowerButton`\  simulates the pressing of a physical power button on the device.

    \ :emphasis:`reset\_type`\  is mutually exclusive with \ :emphasis:`oem\_reset\_type`\ .

    When a power control operation is performed, which is not supported on the device, an error message is displayed with the list of operations that can be performed.


  oem_reset_type (False, dict, None)
    This parameter initiates a complete Alternate Current (AC) power cycle of the server which is equivalent to disconnecting power cables using OEM API.

    \ :emphasis:`oem\_reset\_type`\  is mutually exclusive with \ :emphasis:`reset\_type`\ .

    If the value of 'final\_power\_state' is not provided, the default value is 'Off'.


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
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Manage power state of the first device
      dellemc.openmanage.redfish_powerstate:
        baseuri: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        reset_type: "On"

    - name: Manage power state of a specified device
      dellemc.openmanage.redfish_powerstate:
        baseuri: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        reset_type: "ForceOff"
        resource_id: "System.Embedded.1"

    - name: Perform AC Power Cycle with final power state On
      dellemc.openmanage.redfish_powerstate:
        baseuri: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        oem_reset_type:
          dell:
            final_power_state: "On"
            reset_type: "PowerCycle"

    - name: Perform AC Power Cycle  with final power state Off
      dellemc.openmanage.redfish_powerstate:
        baseuri: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        oem_reset_type:
          dell:
            final_power_state: "Off"
            reset_type: "PowerCycle"



Return Values
-------------

msg (always, str, Successfully performed the reset type operation 'On'.)
  Overall status of the reset operation.


error_info (on http error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to complete the operation because the resource /redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset entered in not found.', 'MessageArgs': ['/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset'], 'MessageArgs@odata.count': 1, 'MessageId': 'IDRAC.2.1.SYS403', 'RelatedProperties': [], 'RelatedProperties@odata.count': 0, 'Resolution': 'Enter the correct resource and retry the operation. For information about valid resource, see the Redfish Users Guide available on the support site.', 'Severity': 'Critical'}], 'code': 'Base.1.5.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information'}})
  Details of the HTTP error.





Status
------





Authors
~~~~~~~

- Sajna Shetty(@Sajna-Shetty)
- Lovepreet Singh (@singh-lovepreet1)

