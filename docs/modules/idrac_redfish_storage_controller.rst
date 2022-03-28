.. _idrac_redfish_storage_controller_module:


idrac_redfish_storage_controller -- Configures the physical disk, virtual disk, and storage controller settings
===============================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows the users to configure the settings of the physical disk, virtual disk, and storage controller.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  command (optional, str, AssignSpare)
    These actions may require a system reset, depending on the capabilities of the controller.

    ``ResetConfig`` - Deletes all the virtual disks and unassigns all hot spares on physical disks. *controller_id* is required for this operation.

    ``AssignSpare`` - Assigns a physical disk as a dedicated or global hot spare for a virtual disk. *target* is required for this operation.

    ``SetControllerKey`` - Sets the key on controllers, which is used to encrypt the drives in Local Key Management(LKM). *controller_id*, *key*, and *key_id* are required for this operation.

    ``RemoveControllerKey`` - Deletes the encryption key on the controller. *controller_id* is required for this operation.

    ``ReKey`` - Resets the key on the controller and it always reports as changes found when check mode is enabled. *controller_id*, *old_key*, *key_id*, and *key* is required for this operation.

    ``UnassignSpare`` - To unassign the Global or Dedicated hot spare. *target* is required for this operation.

    ``EnableControllerEncryption`` - To enable Local Key Management (LKM) or Secure Enterprise Key Manager (SEKM) on controllers that support encryption of the drives. *controller_id*, *key*, and *key_id* are required for this operation.

    ``BlinkTarget`` - Blinks the target virtual drive or physical disk and it always reports as changes found when check mode is enabled. *target* or *volume_id* is required for this operation.

    ``UnBlinkTarget`` - Unblink the target virtual drive or physical disk and and it always reports as changes found when check mode is enabled. *target* or *volume_id* is required for this operation.

    ``ConvertToRAID`` - Converts the disk form non-Raid to Raid. *target* is required for this operation.

    ``ConvertToNonRAID`` - Converts the disk form Raid to non-Raid. *target* is required for this operation.

    ``ChangePDStateToOnline`` - To set the disk status to online. *target* is required for this operation.

    ``ChangePDStateToOffline`` - To set the disk status to offline. *target* is required for this operation.


  target (optional, list, None)
    Fully Qualified Device Descriptor (FQDD) of the target physical drive.

    This is mandatory when *command* is ``AssignSpare``, ``UnassisgnSpare``, ``ChangePDStateToOnline``, ``ChangePDStateToOffline``, ``ConvertToRAID``, or ``ConvertToNonRAID``.

    If *volume_id* is not specified or empty, this physical drive will be assigned as a global hot spare when *command* is ``AssignSpare``.

    Notes: Global or Dedicated hot spare can be assigned only once for a physical disk, Re-assign cannot be done when *command* is ``AssignSpare``.


  volume_id (optional, list, None)
    Fully Qualified Device Descriptor (FQDD) of the volume.

    Applicable if *command* is ``AssignSpare``, ``BlinkTarget``, and ``UnBlinkTarget``.

    *volume_id* or *target* is required when the *command* is ``BlinkTarget`` or ``UnBlinkTarget``, if both are specified *target* is considered.

    To know the number of volumes to which a hot spare can be assigned, refer iDRAC Redfish API documentation.


  controller_id (optional, str, None)
    Fully Qualified Device Descriptor (FQDD) of the storage controller. For example-'RAID.Slot.1-1'.

    This option is mandatory when *command* is ``ResetConfig``, ``SetControllerKey``, ``RemoveControllerKey``, ``ReKey``, or ``EnableControllerEncryption``.


  key (optional, str, None)
    A new security key passphrase that the encryption-capable controller uses to create the encryption key. The controller uses the encryption key to lock or unlock access to the Self-Encrypting Drive (SED). Only one encryption key can be created for each controller.

    This is mandatory when *command* is ``SetControllerKey``, ``ReKey``, or ``EnableControllerEncryption`` and when *mode* is ``LKM``.

    The length of the key can be a maximum of 32 characters in length, where the expanded form of the special character is counted as a single character.

    The key must contain at least one character from each of the character classes: uppercase, lowercase, number, and special character.


  key_id (optional, str, None)
    This is a user supplied text label associated with the passphrase.

    This is mandatory when *command* is ``SetControllerKey``, ``ReKey``, or ``EnableControllerEncryption`` and when *mode* is ``LKM``.

    The length of *key_id* can be a maximum of 32 characters in length and should not have any spaces.


  old_key (optional, str, None)
    Security key passphrase used by the encryption-capable controller.

    This option is mandatory when *command* is ``ReKey`` and *mode* is ``LKM``.


  mode (optional, str, LKM)
    Encryption mode of the encryption capable controller.

    This option is applicable only when *command* is ``ReKey`` or ``EnableControllerEncryption``.

    ``SEKM`` requires secure enterprise key manager license on the iDRAC.

    ``LKM`` to choose mode as local key mode.


  job_wait (optional, bool, False)
    Provides the option if the module has to wait for the job to be completed.


  job_wait_timeout (optional, int, 120)
    The maximum wait time of job completion in seconds before the job tracking is stopped.

    This option is applicable when *job_wait* is ``True``.


  baseuri (True, str, None)
    IP address of the target out-of-band controller. For example- <ipaddress>:<port>.


  username (True, str, None)
    Username of the target out-of-band controller.


  password (True, str, None)
    Password of the target out-of-band controller.


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
   - Run this module from a system that has direct access to Dell EMC iDRAC.
   - This module always reports as changes found when ``ReKey``, ``BlinkTarget``, and ``UnBlinkTarget``.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Assign dedicated hot spare
      dellemc.openmanage.idrac_redfish_storage_controller:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
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
        ca_path: "/path/to/ca_cert.pem"
        target: "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1"
      tags:
        - assign_global_hot_spare

    - name: Unassign hot spare
      dellemc.openmanage.idrac_redfish_storage_controller:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        target: "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1"
        command: UnassignSpare
      tags:
        - un-assign-hot-spare

    - name: Set controller encryption key
      dellemc.openmanage.idrac_redfish_storage_controller:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
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
        ca_path: "/path/to/ca_cert.pem"
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
        ca_path: "/path/to/ca_cert.pem"
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
        ca_path: "/path/to/ca_cert.pem"
        command: "RemoveControllerKey"
        controller_id: "RAID.Slot.1-1"
      tags:
        - remove_controller_key

    - name: Reset controller configuration
      dellemc.openmanage.idrac_redfish_storage_controller:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        command: "ResetConfig"
        controller_id: "RAID.Slot.1-1"
      tags:
        - reset_config

    - name: Enable controller encryption
      idrac_redfish_storage_controller:
        baseuri: "{{ baseuri }}"
        username: "{{ username }}"
        password: "{{ password }}"
        ca_path: "/path/to/ca_cert.pem"
        command: "EnableControllerEncryption"
        controller_id: "RAID.Slot.1-1"
        mode: "LKM"
        key: "your_Key@123"
        key_id: "your_Keyid@123"
      tags:
        - enable-encrypt

    - name: Blink physical disk.
      dellemc.openmanage.idrac_redfish_storage_controller:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        command: BlinkTarget
        target: "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1"
      tags:
        - blink-target

    - name: Blink virtual drive.
      dellemc.openmanage.idrac_redfish_storage_controller:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        command: BlinkTarget
        volume_id: "Disk.Virtual.0:RAID.Slot.1-1"
      tags:
        - blink-volume

    - name: Unblink physical disk.
      dellemc.openmanage.idrac_redfish_storage_controller:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        command: UnBlinkTarget
        target: "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1"
      tags:
        - unblink-target

    - name: Unblink virtual drive.
      dellemc.openmanage.idrac_redfish_storage_controller:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        command: UnBlinkTarget
        volume_id: "Disk.Virtual.0:RAID.Slot.1-1"
      tags:
        - unblink-drive

    - name: Convert physical disk to RAID
      dellemc.openmanage.idrac_redfish_storage_controller:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        command: "ConvertToRAID"
        target: "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1"
      tags:
        - convert-raid

    - name: Convert physical disk to non-RAID
      dellemc.openmanage.idrac_redfish_storage_controller:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        command: "ConvertToNonRAID"
        target: "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1"
      tags:
        - convert-non-raid

    - name: Change physical disk state to online.
      dellemc.openmanage.idrac_redfish_storage_controller:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        command: "ChangePDStateToOnline"
        target: "Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1"
      tags:
        - pd-state-online

    - name: Change physical disk state to offline.
      dellemc.openmanage.idrac_redfish_storage_controller:
        baseuri: "192.168.0.1:443"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        command: "ChangePDStateToOnline"
        target: "Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1"
      tags:
        - pd-state-offline



Return Values
-------------

msg (always, str, Successfully submitted the job that performs the AssignSpare operation)
  Overall status of the storage controller configuration operation.


task (success, dict, AnsibleMapping([('id', 'JID_XXXXXXXXXXXXX'), ('uri', '/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_XXXXXXXXXXXXX')]))
  ID and URI resource of the job created.


status (always, dict, AnsibleMapping([('ActualRunningStartTime', '2022-02-09T04:42:41'), ('ActualRunningStopTime', '2022-02-09T04:44:00'), ('CompletionTime', '2022-02-09T04:44:00'), ('Description', 'Job Instance'), ('EndTime', 'TIME_NA'), ('Id', 'JID_444033604418'), ('JobState', 'Completed'), ('JobType', 'RealTimeNoRebootConfiguration'), ('Message', 'Job completed successfully.'), ('MessageArgs', []), ('MessageId', 'PR19'), ('Name', 'Configure: RAID.Integrated.1-1'), ('PercentComplete', 100), ('StartTime', '2022-02-09T04:42:40'), ('TargetSettingsURI', None)]))
  status of the submitted job.


error_info (on http error, dict, AnsibleMapping([('error', AnsibleMapping([('@Message.ExtendedInfo', [AnsibleMapping([('Message', 'Unable to run the method because the requested HTTP method is not allowed.'), ('MessageArgs', []), ('MessageArgs@odata.count', 0), ('MessageId', 'iDRAC.1.6.SYS402'), ('RelatedProperties', []), ('RelatedProperties@odata.count', 0), ('Resolution', 'Enter a valid HTTP method and retry the operation. For information about valid methods, see the Redfish Users Guide available on the support site.'), ('Severity', 'Informational')])]), ('code', 'Base.1.0.GeneralError'), ('message', 'A general error has occurred. See ExtendedInfo for more information')]))]))
  Details of a http error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V (@jagadeeshnv)
- Felix Stephen (@felixs88)

