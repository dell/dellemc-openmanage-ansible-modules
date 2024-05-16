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

- python \>= 3.8.6



Parameters
----------

  resource_id (False, str, None)
    The unique identifier of the device being managed. For example- \ https://%3CI(baseuri\ \>/redfish/v1/Systems/\<\ :emphasis:`resource\_id`\ \>).

    This option is mandatory for \ :emphasis:`base\_uri`\  with multiple devices.

    To get the device details, use the API \ https://%3CI(baseuri\ \>/redfish/v1/Systems).


  reset_type (True, str, None)
    This option resets the device.

    If \ :literal:`ForceOff`\ , Turns off the device immediately.

    If \ :literal:`ForceOn`\ , Turns on the device immediately.

    If \ :literal:`ForceRestart`\ , Turns off the device immediately, and then restarts the device.

    If \ :literal:`GracefulRestart`\ , Performs graceful shutdown of the device, and then restarts the device.

    If \ :literal:`GracefulShutdown`\ , Performs a graceful shutdown of the device, and the turns off the device.

    If \ :literal:`Nmi`\ , Sends a diagnostic interrupt to the device. This is usually a non-maskable interrupt (NMI) on x86 device.

    If \ :literal:`On`\ , Turns on the device.

    If \ :literal:`PowerCycle`\ , Performs power cycle on the device.

    If \ :literal:`PushPowerButton`\ , Simulates the pressing of a physical power button on the device.

    When a power control operation is performed, which is not supported on the device, an error message is displayed with the list of operations that can be performed.


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

