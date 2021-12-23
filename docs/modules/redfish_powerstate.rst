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

- python >= 2.7.5



Parameters
----------

  resource_id (False, str, None)
    The unique identifier of the device being managed. For example- https://<*baseuri*>/redfish/v1/Systems/<*resource_id*>.

    This option is mandatory for *base_uri* with multiple devices.

    To get the device details, use the API https://<*baseuri*>/redfish/v1/Systems.


  reset_type (True, str, None)
    This option resets the device.

    If ``ForceOff``, Turns off the device immediately.

    If ``ForceOn``, Turns on the device immediately.

    If ``ForceRestart``, Turns off the device immediately, and then restarts the device.

    If ``GracefulRestart``, Performs graceful shutdown of the device, and then restarts the device.

    If ``GracefulShutdown``, Performs a graceful shutdown of the device, and the turns off the device.

    If ``Nmi``, Sends a diagnostic interrupt to the device. This is usually a non-maskable interrupt (NMI) on x86 device.

    If ``On``, Turns on the device.

    If ``PowerCycle``, Performs power cycle on the device.

    If ``PushPowerButton``, Simulates the pressing of a physical power button on the device.

    When a power control operation is performed, which is not supported on the device, an error message is displayed with the list of operations that can be performed.


  baseuri (True, str, None)
    IP address of the target out-of-band controller. For example- <ipaddress>:<port>.


  username (True, str, None)
    Username of the target out-of-band controller.


  password (True, str, None)
    Password of the target out-of-band controller.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Redfish APIs.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Manage power state of the first device
      dellemc.openmanage.redfish_powerstate:
           baseuri: "192.168.0.1"
           username: "username"
           password: "password"
           reset_type: "On"

    - name: Manage power state of a specified device
      dellemc.openmanage.redfish_powerstate:
           baseuri: "192.168.0.1"
           username: "username"
           password: "password"
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

