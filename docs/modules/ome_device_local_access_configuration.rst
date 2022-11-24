.. _ome_device_local_access_configuration_module:


ome_device_local_access_configuration -- Configure local access settings on OpenManage Enterprise Modular.
==========================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to configure the local access settings of the power button, quick sync, KVM, LCD, and chassis direct access on OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  device_id (optional, int, None)
    The ID of the chassis for which the local access configuration to be updated.

    If the device ID is not specified, this module updates the local access settings for the *hostname*.

    *device_id* is mutually exclusive with *device_service_tag*.


  device_service_tag (optional, str, None)
    The service tag of the chassis for which the local access settings needs to be updated.

    If the device service tag is not specified, this module updates the local access settings for the *hostname*.

    *device_service_tag* is mutually exclusive with *device_id*.


  enable_kvm_access (optional, bool, None)
    Enables or disables the keyboard, video, and mouse (KVM) interfaces.


  enable_chassis_direct_access (optional, bool, None)
    Enables or disables the access to management consoles such as iDRAC and the management module of the device on the chassis.


  chassis_power_button (optional, dict, None)
    The settings for the chassis power button.


    enable_chassis_power_button (True, bool, None)
      Enables or disables the chassis power button.

      If ``False``, the chassis cannot be turn on or turn off using the power button.


    enable_lcd_override_pin (optional, bool, None)
      Enables or disables the LCD override pin.

      This is required when *enable_chassis_power_button* is ``False``.


    disabled_button_lcd_override_pin (optional, int, None)
      The six digit LCD override pin to change the power state of the chassis.

      This is required when *enable_lcd_override_pin* is ``True``.

      The module will always report change when *disabled_button_lcd_override_pin* is ``True``.



  quick_sync (optional, dict, None)
    The settings for quick sync.

    The *quick_sync* options are ignored if the quick sync hardware is not present.


    quick_sync_access (optional, str, None)
      Users with administrator privileges can set the following types of *quick_sync_access*.

      ``READ_WRITE`` enables writing configuration using quick sync.

      ``READ_ONLY`` enables read only access to Wi-Fi and Bluetooth Low Energy(BLE).

      ``DISABLED`` disables reading or writing configuration through quick sync.


    enable_inactivity_timeout (optional, bool, None)
      Enables or disables the inactivity timeout.


    timeout_limit (optional, int, None)
      Inactivity timeout in seconds or minutes.

      The range is 120 to 3600 in seconds, or 2 to 60 in minutes.

      This option is required when *enable_inactivity_timeout* is ``True``.


    timeout_limit_unit (optional, str, None)
      Inactivity timeout limit unit.

      ``SECONDS`` to set *timeout_limit* in seconds.

      ``MINUTES`` to set *timeout_limit* in minutes.

      This option is required when *enable_inactivity_timeout* is ``True``.


    enable_read_authentication (optional, bool, None)
      Enables or disables the option to log in using your user credentials and to read the inventory in a secure data center.


    enable_quick_sync_wifi (optional, bool, None)
      Enables or disables the Wi-Fi communication path to the chassis.



  lcd (optional, dict, None)
    The settings for LCD.

    The *lcd* options are ignored if the LCD hardware is not present in the chassis.


    lcd_access (optional, str, None)
      Option to configure the quick sync settings using LCD.

      ``VIEW_AND_MODIFY`` to set access level to view and modify.

      ``VIEW_ONLY`` to set access level to view.

      ``DISABLED`` to disable the access.


    user_defined (optional, str, None)
      The text to display on the LCD Home screen. The LCD Home screen is displayed when the system is reset to factory default settings. The user-defined text can have a maximum of 62 characters.


    lcd_language (optional, str, None)
      The language code in which the text on the LCD must be displayed.

      en to set English language.

      fr to set French language.

      de to set German language.

      es to set Spanish language.

      ja to set Japanese language.

      zh to set Chinese language.



  hostname (True, str, None)
    OpenManage Enterprise Modular IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise Modular username.


  password (True, str, None)
    OpenManage Enterprise Modular password.


  port (optional, int, 443)
    OpenManage Enterprise Modular HTTPS port.


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
   - Run this module from a system that has direct access to OpenManage Enterprise Modular.
   - This module supports ``check_mode``.
   - The module will always report change when *enable_chassis_power_button* is ``True``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Configure KVM, direct access and power button settings of the chassis using device ID.
      dellemc.openmanage.ome_device_local_access_configuration:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_id: 25011
        enable_kvm_access: true
        enable_chassis_direct_access: false
        chassis_power_button:
          enable_chassis_power_button: false
          enable_lcd_override_pin: true
          disabled_button_lcd_override_pin: 123456

    - name: Configure Quick sync and LCD settings of the chassis using device service tag.
      dellemc.openmanage.ome_device_local_access_configuration:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_service_tag: GHRT2RL
        quick_sync:
          quick_sync_access: READ_ONLY
          enable_read_authentication: true
          enable_quick_sync_wifi: true
          enable_inactivity_timeout: true
          timeout_limit: 10
          timeout_limit_unit: MINUTES
        lcd:
          lcd_access: VIEW_ONLY
          lcd_language: en
          user_defined: "LCD Text"

    - name: Configure all local access settings of the host chassis.
      dellemc.openmanage.ome_device_local_access_configuration:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        enable_kvm_access: true
        enable_chassis_direct_access: false
        chassis_power_button:
          enable_chassis_power_button: false
          enable_lcd_override_pin: true
          disabled_button_lcd_override_pin: 123456
        quick_sync:
          quick_sync_access: READ_WRITE
          enable_read_authentication: true
          enable_quick_sync_wifi: true
          enable_inactivity_timeout: true
          timeout_limit: 120
          timeout_limit_unit: SECONDS
        lcd:
          lcd_access: VIEW_MODIFY
          lcd_language: en
          user_defined: "LCD Text"



Return Values
-------------

msg (always, str, Successfully updated the local access settings.)
  Overall status of the device local access settings.


location_details (success, dict, {'SettingType': 'LocalAccessConfiguration', 'EnableChassisDirect': False, 'EnableChassisPowerButton': False, 'EnableKvmAccess': True, 'EnableLcdOverridePin': False, 'LcdAccess': 'VIEW_ONLY', 'LcdCustomString': 'LCD Text', 'LcdLanguage': 'en', 'LcdOverridePin': '', 'LcdPinLength': None, 'LcdPresence': 'Present', 'LedPresence': None, 'QuickSync': {'EnableInactivityTimeout': True, 'EnableQuickSyncWifi': False, 'EnableReadAuthentication': False, 'QuickSyncAccess': 'READ_ONLY', 'QuickSyncHardware': 'Present', 'TimeoutLimit': 7, 'TimeoutLimitUnit': 'MINUTES'}})
  returned when local access settings are updated successfully.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)

