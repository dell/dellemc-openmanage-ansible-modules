.. _redfish_storage_volume_module:


redfish_storage_volume -- Manages the storage volume configuration
==================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to create, modify, initialize, or delete a single storage volume.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  controller_id (optional, str, None)
    Fully Qualified Device Descriptor (FQDD) of the storage controller.

    For example- RAID.Slot.1-1.

    This option is mandatory when *state* is ``present`` while creating a volume.


  volume_id (optional, str, None)
    FQDD of existing volume.

    For example- Disk.Virtual.4:RAID.Slot.1-1.

    This option is mandatory in the following scenarios,

    *state* is ``present``, when updating a volume.

    *state* is ``absent``, when deleting a volume.

    *command* is ``initialize``, when initializing a volume.


  state (optional, str, None)
    ``present`` creates a storage volume for the specified I (controller_id), or modifies the storage volume for the specified I (volume_id). "Note: Modification of an existing volume properties depends on drive and controller capabilities".

    ``absent`` deletes the volume for the specified *volume_id*.


  command (optional, str, None)
    ``initialize`` initializes an existing storage volume for a specified *volume_id*.


  volume_type (optional, str, None)
    One of the following volume types must be selected to create a volume.

    ``Mirrored`` The volume is a mirrored device.

    ``NonRedundant`` The volume is a non-redundant storage device.

    ``SpannedMirrors`` The volume is a spanned set of mirrored devices.

    ``SpannedStripesWithParity`` The volume is a spanned set of devices which uses parity to retain redundant information.

    ``StripedWithParity`` The volume is a device which uses parity to retain redundant information.


  name (optional, str, None)
    Name of the volume to be created.

    Only applicable when *state* is ``present``.


  drives (optional, list, None)
    FQDD of the Physical disks.

    For example- Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1.

    Only applicable when *state* is ``present`` when creating a new volume.


  block_size_bytes (optional, int, None)
    Block size in bytes.Only applicable when *state* is ``present``.


  capacity_bytes (optional, str, None)
    Volume size in bytes.

    Only applicable when *state* is ``present``.


  optimum_io_size_bytes (optional, int, None)
    Stripe size value must be in multiples of 64 * 1024.

    Only applicable when *state* is ``present``.


  encryption_types (optional, str, None)
    The following encryption types can be selected.

    ``ControllerAssisted`` The volume is encrypted by the storage controller entity.

    ``NativeDriveEncryption`` The volume utilizes the native drive encryption capabilities of the drive hardware.

    ``SoftwareAssisted`` The volume is encrypted by the software running on the system or the operating system.

    Only applicable when *state* is ``present``.


  encrypted (optional, bool, None)
    Indicates whether volume is currently utilizing encryption or not.

    Only applicable when *state* is ``present``.


  oem (optional, dict, None)
    Includes OEM extended payloads.

    Only applicable when *state* is *present*.


  initialize_type (optional, str, Fast)
    Initialization type of existing volume.

    Only applicable when *command* is ``initialize``.


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
   - Run this module from a system that has direct access to Redfish APIs.
   - This module supports ``check_mode``.
   - This module always reports changes when *name* and *volume_id* are not specified. Either *name* or *volume_id* is required to support ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create a volume with supported options
      dellemc.openmanage.redfish_storage_volume:
        baseuri: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "present"
        volume_type: "Mirrored"
        name: "VD0"
        controller_id: "RAID.Slot.1-1"
        drives:
          - Disk.Bay.5:Enclosure.Internal.0-1:RAID.Slot.1-1
          - Disk.Bay.6:Enclosure.Internal.0-1:RAID.Slot.1-1
        block_size_bytes: 512
        capacity_bytes: 299439751168
        optimum_io_size_bytes: 65536
        encryption_types: NativeDriveEncryption
        encrypted: true

    - name: Create a volume with minimum options
      dellemc.openmanage.redfish_storage_volume:
        baseuri: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "present"
        controller_id: "RAID.Slot.1-1"
        volume_type: "NonRedundant"
        drives:
           - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1

    - name: Modify a volume's encryption type settings
      dellemc.openmanage.redfish_storage_volume:
        baseuri: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "present"
        volume_id: "Disk.Virtual.5:RAID.Slot.1-1"
        encryption_types: "ControllerAssisted"
        encrypted: true

    - name: Delete an existing volume
      dellemc.openmanage.redfish_storage_volume:
        baseuri: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "absent"
        volume_id: "Disk.Virtual.5:RAID.Slot.1-1"

    - name: Initialize an existing volume
      dellemc.openmanage.redfish_storage_volume:
        baseuri: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: "initialize"
        volume_id: "Disk.Virtual.6:RAID.Slot.1-1"
        initialize_type: "Slow"



Return Values
-------------

msg (always, str, Successfully submitted create volume task.)
  Overall status of the storage configuration operation.


task (success, dict, {'id': 'JID_XXXXXXXXXXXXX', 'uri': '/redfish/v1/TaskService/Tasks/JID_XXXXXXXXXXXXX'})
  Returns ID and URI of the created task.


error_info (on http error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to perform configuration operations because a configuration job for the device already exists.', 'MessageArgs': [], 'MessageArgs@odata.count': 0, 'MessageId': 'IDRAC.1.6.STOR023', 'RelatedProperties': [], 'RelatedProperties@odata.count': 0, 'Resolution': 'Wait for the current job for the device to complete or cancel the current job before attempting more configuration operations on the device.', 'Severity': 'Informational'}], 'code': 'Base.1.2.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information'}})
  Details of a http error.





Status
------





Authors
~~~~~~~

- Sajna Shetty(@Sajna-Shetty)

