.. _ome_device_power_settings_module:


ome_device_power_settings -- Configure chassis power settings on OpenManage Enterprise Modular
==============================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to configure the chassis power settings on OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  device_id (optional, int, None)
    The ID of the chassis for which the settings need to be updated.

    If the device ID is not specified, this module updates the power settings for the *hostname*.

    *device_id* is mutually exclusive with *device_service_tag*.


  device_service_tag (optional, str, None)
    The service tag of the chassis for which the setting needs to be updated.

    If the device service tag is not specified, this module updates the power settings for the *hostname*.

    *device_service_tag* is mutually exclusive with *device_id*.


  power_configuration (optional, dict, None)
    The settings for Power configuration.


    enable_power_cap (True, bool, None)
      Enables or disables the Power Cap Settings.


    power_cap (optional, int, None)
      The maximum power consumption limit of the device. Specify the consumption limit in Watts.

      This is required if *enable_power_cap* is set to true.



  redundancy_configuration (optional, dict, None)
    The settings for Redundancy configuration.


    redundancy_policy (optional, str, NO_REDUNDANCY)
      The choices to configure the redundancy policy.

      ``NO_REDUNDANCY`` no redundancy policy is used.

      ``GRID_REDUNDANCY`` to distributes power by dividing the PSUs into two grids.

      ``PSU_REDUNDANCY`` to distribute power between all the PSUs.



  hot_spare_configuration (optional, dict, None)
    The settings for Hot Spare configuration.


    enable_hot_spare (True, bool, None)
      Enables or disables Hot Spare configuration to facilitate voltage regulation when power utilized by the Power Supply Unit (PSU) is low.


    primary_grid (optional, str, GRID_1)
      The choices for PSU grid.

      ``GRID_1`` Hot Spare on Grid 1.

      ``GRID_2`` Hot Spare on Grid 2.



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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise Modular.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Update power configuration settings of a chassis using the device ID.
      dellemc.openmanage.ome_device_power_settings:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_id: 25011
        power_configuration:
          enable_power_cap: true
          power_cap: 3424

    - name: Update redundancy configuration settings of a chassis using the device service tag.
      dellemc.openmanage.ome_device_power_settings:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_service_tag: GHRT2RL
        redundancy_configuration:
          redundancy_policy: GRID_REDUNDANCY

    - name: Update hot spare configuration settings of a chassis using device ID.
      dellemc.openmanage.ome_device_power_settings:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_id: 25012
        hot_spare_configuration:
          enable_hot_spare: true
          primary_grid: GRID_1



Return Values
-------------

msg (always, str, Successfully updated the power settings.)
  Overall status of the device power settings.


power_details (success, dict, {'EnableHotSpare': True, 'EnablePowerCapSettings': True, 'MaxPowerCap': '3424', 'MinPowerCap': '3291', 'PowerCap': '3425', 'PrimaryGrid': 'GRID_1', 'RedundancyPolicy': 'NO_REDUNDANCY', 'SettingType': 'Power'})
  returned when power settings are updated successfully.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)

