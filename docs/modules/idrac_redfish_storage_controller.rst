.. _idrac_redfish_storage_controller_module:


idrac_redfish_storage_controller -- Configures the storage controller settings
==============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module configures the settings of the storage controller using Redfish.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7.5



Parameters
----------

  command (optional, str, AssignSpare)
    These actions may require a system reset, depending on the controller's capabilities.

    ``ResetConfig`` - Deletes all the virtual disks and unassigns all hot spares on physical disks.

    ``AssignSpare`` - Assigns a physical disk as a dedicated or global hot spare for a virtual disk.

    ``SetControllerKey`` - Sets the key on controllers, which is used to encrypt the drives in Local key Management(LKM).

    ``RemoveControllerKey`` - Erases the encryption key on the controller.

    ``ReKey`` - Resets the key on the controller.


  target (optional, str, None)
    Fully Qualified Device Descriptor (FQDD) of the target physical drive that is assigned as a spare.

    This is mandatory when *command* is ``AssignSpare``.

    If *volume_id* is not specified or empty, this physical drive will be assigned as a global hot spare.


  volume_id (optional, list, None)
    FQDD of the volumes to which a hot spare is assigned.

    Applicable if *command* is ``AssignSpare``.

    To know the number of volumes to which a hot spare can be assigned, refer iDRAC Redfish API guide.


  controller_id (optional, str, None)
    FQDD of the storage controller. For example- 'RAID.Slot.1-1'.

    This option is mandatory when *command* is ``ResetConfig``, ``SetControllerKey``, ``RemoveControllerKey`` and ``ReKey``.


  key (optional, str, None)
    A new security key passphrase that the encryption-capable controller uses to create the encryption key. The controller uses the encryption key to lock or unlock access to the Self Encryption Disk(SED). Only one encryption key can be created for each controller.

    This is mandatory when *command* is ``SetControllerKey`` or ``ReKey``, and when *mode* is ``LKM``.


  key_id (optional, str, None)
    This is a user supplied text label associated with the passphrase.

    This is mandatory when *command* is ``SetControllerKey`` or ``ReKey``, and when *mode* is ``LKM``.


  old_key (optional, str, None)
    Security key passphrase used by the encryption-capable controller..

    This option is mandatory when *command* is ``ReKey`` and *mode* is ``LKM``.


  mode (optional, str, LKM)
    Encryption mode of the encryption-capable controller: 1 - Local Key Management (LKM), 2 - Security Enterprise Key Manager(SEKM).

    This option is applicable only when *command* is ``ReKey``.

    ``SEKM`` requires secure enterprise key manager license on the iDRAC.


  baseuri (True, str, None)
    IP address of the target out-of-band controller. For example- <ipaddress>:<port>.


  username (True, str, None)
    Username of the target out-of-band controller.


  password (True, str, None)
    Password of the target out-of-band controller.





Notes
-----

.. note::
   - Run this module from a system that has direct access to DellEMC iDRAC.
   - This module does not support ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Assign dedicated hot spare
      dellemc.openmanage.idrac_redfish_storage_controller:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        volume_id:
          - "Disk.Virtual.0:RAID.Slot.1-1"
        target: "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1"
      tags:
        - assign_dedicated_hot_spare

    - name: Assign global hot spare
      dellemc.openmanage.idrac_redfish_storage_controller:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        target: "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1"
      tags:
        - assign_global_hot_spare

    - name: Set controller encryption key
      dellemc.openmanage.idrac_redfish_storage_controller:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        command: "SetControllerKey"
        controller_id: "RAID.Slot.1-1"
        key: "PassPhrase@123"
        key_id: "mykeyid123"
      tags:
        - set_controller_key

    - name: Rekey in LKM mode
      dellemc.openmanage.idrac_redfish_storage_controller:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        command: "ReKey"
        controller_id: "RAID.Slot.1-1"
        key: "NewPassPhrase@123"
        key_id: "newkeyid123"
        old_key: "OldPassPhrase@123"
      tags:
        - rekey_lkm

    - name: Rekey in SEKM mode
      dellemc.openmanage.idrac_redfish_storage_controller:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        command: "ReKey"
        controller_id: "RAID.Slot.1-1"
        mode: "SEKM"
      tags:
        - rekey_sekm

    - name: Remove controller key
      dellemc.openmanage.idrac_redfish_storage_controller:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        command: "RemoveControllerKey"
        controller_id: "RAID.Slot.1-1"
      tags:
        - remove_controller_key

    - name: Reset controller configuration
      dellemc.openmanage.idrac_redfish_storage_controller:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        command: "ResetConfig"
        controller_id: "RAID.Slot.1-1"
      tags:
        - reset_config



Return Values
-------------

msg (always, str, Successfully submitted the job that performs the AssignSpare operation)
  Overall status of the storage controller configuration operation.


task (success, dict, {'id': 'JID_XXXXXXXXXXXXX', 'uri': '/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_XXXXXXXXXXXXX'})
  ID and URI resource of the job created.


error_info (on http error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to run the method because the requested HTTP method is not allowed.', 'MessageArgs': [], 'MessageArgs@odata.count': 0, 'MessageId': 'iDRAC.1.6.SYS402', 'RelatedProperties': [], 'RelatedProperties@odata.count': 0, 'Resolution': 'Enter a valid HTTP method and retry the operation. For information about valid methods, see the Redfish Users Guide available on the support site.', 'Severity': 'Informational'}], 'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information'}})
  Details of a http error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V (@jagadeeshnv)

