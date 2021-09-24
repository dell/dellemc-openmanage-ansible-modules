.. _ome_chassis_slots_module:


ome_chassis_slots -- Rename sled slots on OpenManage Enterprise Modular
=======================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to rename sled slots on OpenManage Enterprise Modular either using device id or device service tag or using chassis service tag and slot number.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7.17



Parameters
----------

  device_options (optional, list, None)
    The ID or service tag of the sled in the slot and the new name for the slot.

    *device_options* is mutually exclusive with *slot_options*.


    device_id (optional, int, None)
      Device ID of the sled in the slot.

      This is mutually exclusive with *device_service_tag*.


    device_service_tag (optional, str, None)
      Service tag of the sled in the slot.

      This is mutually exclusive with *device_id*.


    slot_name (True, str, None)
      Provide name for the slot.



  slot_options (optional, list, None)
    The service tag of the chassis, slot number of the slot to be renamed, and the new name for the slot.

    *slot_options* is mutually exclusive with *device_options*.


    chassis_service_tag (True, str, None)
      Service tag of the chassis.


    slots (True, list, None)
      The slot number and the new name for the slot.


      slot_number (True, int, None)
        The slot number of the slot to be renamed.


      slot_name (True, str, None)
        Provide name for the slot.




  hostname (True, str, None)
    OpenManage Enterprise Modular IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise Modular username.


  password (True, str, None)
    OpenManage Enterprise Modular password.


  port (optional, int, 443)
    OpenManage Enterprise Modular HTTPS port.





Notes
-----

.. note::
   - This module initiates the refresh inventory task. It may take a minute for new names to be reflected. If the task exceeds 300 seconds to refresh, the task times out.
   - Run this module from a system that has direct access to Dell EMC OpenManage Enterprise Modular.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Rename the slots in multiple chassis using slot number and chassis service tag
      dellemc.openmanage.ome_chassis_slots:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        slot_options:
          - chassis_service_tag: ABC1234
            slots:
              - slot_number: 1
                slot_name: sled_name_1
              - slot_number: 2
                slot_name: sled_name_2
          - chassis_service_tag: ABC1235
            slots:
              - slot_number: 1
                slot_name: sled_name_1
              - slot_number: 2
                slot_name: sled_name_2

    - name: Rename single slot name of the sled using sled ID
      dellemc.openmanage.ome_chassis_slots:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        device_options:
          - device_id: 10054
            slot_name: slot_device_name_1

    - name: Rename single slot name of the sled using sled service tag
      dellemc.openmanage.ome_chassis_slots:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        device_options:
          - device_service_tag: ABC1234
            slot_name: service_tag_slot

    - name: Rename multiple slot names of the devices
      dellemc.openmanage.ome_chassis_slots:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        device_options:
          - device_id: 10054
            slot_name: sled_name_1
          - device_service_tag: ABC1234
            slot_name: sled_name_2
          - device_id: 10055
            slot_name: sled_name_3
          - device_service_tag: PQR1234
            slot_name: sled_name_4



Return Values
-------------

msg (always, str, Successfully renamed the slot(s).)
  Overall status of the slot rename operation.


slot_info (if at least one slot renamed, list, [{'ChassisId': 10053, 'ChassisServiceTag': 'ABCD123', 'DeviceName': '', 'DeviceType': 1000, 'JobId': 15746, 'SlotId': '10072', 'SlotName': 'slot_op2', 'SlotNumber': '6', 'SlotType': 2000}, {'ChassisId': 10053, 'ChassisName': 'MX-ABCD123', 'ChassisServiceTag': 'ABCD123', 'DeviceType': '3000', 'JobId': 15747, 'SlotId': '10070', 'SlotName': 'slot_op2', 'SlotNumber': '4', 'SlotType': '2000'}, {'ChassisId': '10053', 'ChassisName': 'MX-PQRS123', 'ChassisServiceTag': 'PQRS123', 'DeviceId': '10054', 'DeviceServiceTag': 'XYZ5678', 'DeviceType': '1000', 'JobId': 15761, 'SlotId': '10067', 'SlotName': 'a1', 'SlotNumber': '1', 'SlotType': '2000'}])
  Information of the slots that are renamed successfully.

  The ``DeviceServiceTag`` and ``DeviceId`` options are available only if *device_options* is used.

  ``NOTE`` Only the slots which were renamed are listed.


rename_failed_slots (if at least one slot renaming fails, list, [{'ChassisId': '12345', 'ChassisName': 'MX-ABCD123', 'ChassisServiceTag': 'ABCD123', 'DeviceType': '4000', 'JobId': 1234, 'JobStatus': 'Aborted', 'SlotId': '10061', 'SlotName': 'c2', 'SlotNumber': '1', 'SlotType': '4000'}, {'ChassisId': '10053', 'ChassisName': 'MX-PQRS123', 'ChassisServiceTag': 'PQRS123', 'DeviceType': '1000', 'JobId': 0, 'JobStatus': 'HTTP Error 400: Bad Request', 'SlotId': '10069', 'SlotName': 'b2', 'SlotNumber': '3', 'SlotType': '2000'}])
  Information of the valid slots that are not renamed.

  ``JobStatus`` is shown if rename job fails.

  ``NOTE`` Only slots which were not renamed are listed.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'CGEN1014', 'RelatedProperties': [], 'Message': 'Unable to complete the operation because an invalid value is entered for the property Invalid json type: STRING for Edm.Int64 property: Id .', 'MessageArgs': ['Invalid json type: STRING for Edm.Int64 property: Id'], 'Severity': 'Critical', 'Resolution': "Enter a valid value for the property and retry the operation. For more information about valid values, see the OpenManage Enterprise-Modular User's Guide available on the support site."}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

