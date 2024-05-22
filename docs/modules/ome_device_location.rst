.. _ome_device_location_module:


ome_device_location -- Configure device location settings on OpenManage Enterprise Modular
==========================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to configure the device location settings of the chassis on OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  device_id (optional, int, None)
    The ID of the chassis for which the settings need to be updated.

    If the device ID is not specified, this module updates the location settings for the \ :emphasis:`hostname`\ .

    \ :emphasis:`device\_id`\  is mutually exclusive with \ :emphasis:`device\_service\_tag`\ .


  device_service_tag (optional, str, None)
    The service tag of the chassis for which the settings need to be updated.

    If the device service tag is not specified, this module updates the location settings for the \ :emphasis:`hostname`\ .

    \ :emphasis:`device\_service\_tag`\  is mutually exclusive with \ :emphasis:`device\_id`\ .


  data_center (optional, str, None)
    The data center name of the chassis.


  room (optional, str, None)
    The room of the chassis.


  aisle (optional, str, None)
    The aisle of the chassis.


  rack (optional, str, None)
    The rack name of the chassis.


  rack_slot (optional, int, None)
    The rack slot number of the chassis.


  location (optional, str, None)
    The physical location of the chassis.


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
    - name: Update device location settings of a chassis using the device ID.
      dellemc.openmanage.ome_device_location:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_id: 25011
        data_center: data center 1
        room: room 1
        aisle: aisle 1
        rack: rack 1
        rack_slot: 2
        location: location 1

    - name: Update device location settings of a chassis using the device service tag.
      dellemc.openmanage.ome_device_location:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_service_tag: GHRT2RL
        data_center: data center 2
        room: room 7
        aisle: aisle 4
        rack: rack 6
        rack_slot: 22
        location: location 5

    - name: Update device location settings of the host chassis.
      dellemc.openmanage.ome_device_location:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        data_center: data center 3
        room: room 3
        aisle: aisle 1
        rack: rack 7
        rack_slot: 10
        location: location 9



Return Values
-------------

msg (always, str, Successfully updated the location settings.)
  Overall status of the device location settings.


location_details (success, dict, {'Aisle': 'aisle 1', 'DataCenter': 'data center 1', 'Location': 'location 1', 'RackName': 'rack 1', 'RackSlot': 2, 'Room': 'room 1', 'SettingType': 'Location'})
  returned when location settings are updated successfully.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)

