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

- python \>= 3.9.6



Parameters
----------

  controller_id (optional, str, None)
    Fully Qualified Device Descriptor (FQDD) of the storage controller.

    For example- RAID.Slot.1-1.

    This option is mandatory when \ :emphasis:`state`\  is \ :literal:`present`\  while creating a volume.


  volume_id (optional, str, None)
    FQDD of existing volume.

    For example- Disk.Virtual.4:RAID.Slot.1-1.

    This option is mandatory in the following scenarios,

    \ :emphasis:`state`\  is \ :literal:`present`\ , when updating a volume.

    \ :emphasis:`state`\  is \ :literal:`absent`\ , when deleting a volume.

    \ :emphasis:`command`\  is \ :literal:`initialize`\ , when initializing a volume.


  state (optional, str, None)
    \ :literal:`present`\  creates a storage volume for the specified I (controller\_id), or modifies the storage volume for the specified I (volume\_id). "Note: Modification of an existing volume properties depends on drive and controller capabilities".

    \ :literal:`absent`\  deletes the volume for the specified \ :emphasis:`volume\_id`\ .


  command (optional, str, None)
    \ :literal:`initialize`\  initializes an existing storage volume for a specified \ :emphasis:`volume\_id`\ .


  volume_type (optional, str, None)
    One of the following volume types must be selected to create a volume.

    \ :literal:`NonRedundant`\  The volume is a non-redundant storage device.

    \ :literal:`Mirrored`\  The volume is a mirrored device.

    \ :literal:`StripedWithParity`\  The volume is a device which uses parity to retain redundant information.

    \ :literal:`SpannedMirrors`\  The volume is a spanned set of mirrored devices.

    \ :literal:`SpannedStripesWithParity`\  The volume is a spanned set of devices which uses parity to retain redundant information.

    \ :emphasis:`volume\_type`\  is mutually exclusive with \ :emphasis:`raid\_type`\ .


  name (optional, str, None)
    Name of the volume to be created.

    Only applicable when \ :emphasis:`state`\  is \ :literal:`present`\ .


  drives (optional, list, None)
    FQDD of the Physical disks.

    For example- Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1.

    Only applicable when \ :emphasis:`state`\  is \ :literal:`present`\  when creating a new volume.


  block_size_bytes (optional, int, None)
    Block size in bytes.Only applicable when \ :emphasis:`state`\  is \ :literal:`present`\ .


  capacity_bytes (optional, str, None)
    Volume size in bytes.

    Only applicable when \ :emphasis:`state`\  is \ :literal:`present`\ .


  optimum_io_size_bytes (optional, int, None)
    Stripe size value must be in multiples of 64 \* 1024.

    Only applicable when \ :emphasis:`state`\  is \ :literal:`present`\ .


  encryption_types (optional, str, None)
    The following encryption types can be selected.

    \ :literal:`ControllerAssisted`\  The volume is encrypted by the storage controller entity.

    \ :literal:`NativeDriveEncryption`\  The volume utilizes the native drive encryption capabilities of the drive hardware.

    \ :literal:`SoftwareAssisted`\  The volume is encrypted by the software running on the system or the operating system.

    Only applicable when \ :emphasis:`state`\  is \ :literal:`present`\ .


  encrypted (optional, bool, None)
    Indicates whether volume is currently utilizing encryption or not.

    Only applicable when \ :emphasis:`state`\  is \ :literal:`present`\ .


  oem (optional, dict, None)
    Includes OEM extended payloads.

    Only applicable when \ :emphasis:`state`\  is \ :emphasis:`present`\ .


  initialize_type (optional, str, Fast)
    Initialization type of existing volume.

    Only applicable when \ :emphasis:`command`\  is \ :literal:`initialize`\ .


  raid_type (optional, str, None)
    \ :literal:`RAID0`\  to create a RAID0 type volume.

    \ :literal:`RAID1`\  to create a RAID1 type volume.

    \ :literal:`RAID5`\  to create a RAID5 type volume.

    \ :literal:`RAID6`\  to create a RAID6 type volume.

    \ :literal:`RAID10`\  to create a RAID10 type volume.

    \ :literal:`RAID50`\  to create a RAID50 type volume.

    \ :literal:`RAID60`\  to create a RAID60 type volume.

    \ :emphasis:`raid\_type`\  is mutually exclusive with \ :emphasis:`volume\_type`\ .


  apply_time (optional, str, None)
    Apply time of the Volume configuration.

    \ :literal:`Immediate`\  allows you to apply the volume configuration on the host server immediately and apply the changes. This is applicable for \ :emphasis:`job\_wait`\ .

    \ :literal:`OnReset`\  allows you to apply the changes on the next reboot of the host server.

    \ :emphasis:`apply\_time`\  has a default value based on the different types of the controller. For example, BOSS-S1 and BOSS-N1 controllers have a default value of \ :emphasis:`apply\_time`\  as \ :literal:`OnReset`\ , and PERC controllers have a default value of \ :emphasis:`apply\_time`\  as \ :literal:`Immediate`\ .


  reboot_server (optional, bool, False)
    Reboot the server to apply the changes.

    \ :emphasis:`reboot\_server`\  is applicable only when \ :emphasis:`apply\_timeout`\  is \ :literal:`OnReset`\  or when the default value for the apply time of the controller is \ :literal:`OnReset`\ .


  force_reboot (optional, bool, False)
    Reboot the server forcefully to apply the changes when the normal reboot fails.

    \ :emphasis:`force\_reboot`\  is applicable only when \ :emphasis:`reboot\_server`\  is \ :literal:`true`\ .


  job_wait (optional, bool, False)
    This parameter provides the option to wait for the job completion.

    This is applicable when \ :emphasis:`apply\_time`\  is \ :literal:`Immediate`\ .

    This is applicable when \ :emphasis:`apply\_time`\  is \ :literal:`OnReset`\  and \ :emphasis:`reboot\_server`\  is \ :literal:`true`\ .


  job_wait_timeout (optional, int, 1200)
    This parameter is the maximum wait time of \ :emphasis:`job\_wait`\  in seconds.

    This option is applicable when \ :emphasis:`job\_wait`\  is \ :literal:`true`\ .


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
   - This module always reports changes when \ :emphasis:`name`\  and \ :emphasis:`volume\_id`\  are not specified. Either \ :emphasis:`name`\  or \ :emphasis:`volume\_id`\  is required to support \ :literal:`check\_mode`\ .
   - This module does not support the create operation of RAID6 and RAID60 storage volume on iDRAC8
   - This module supports IPv4 and IPv6 addresses.




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

    - name: Create a RAID0 on PERC controller on reset
      dellemc.openmanage.redfish_storage_volume:
        baseuri: "192.168.0.1"
        username: "username"
        password: "password"
        state: "present"
        controller_id: "RAID.Slot.1-1"
        raid_type: "RAID0"
        drives:
          - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1
          - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-2
        apply_time: OnReset

    - name: Create a RAID0 on BOSS controller with restart
      dellemc.openmanage.redfish_storage_volume:
        baseuri: "192.168.0.1"
        username: "username"
        password: "password"
        state: "present"
        controller_id: "RAID.Slot.1-1"
        raid_type: "RAID0"
        drives:
          - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1
          - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-2
        apply_time: OnReset
        reboot_server: true

    - name: Create a RAID0 on BOSS controller with force restart
      dellemc.openmanage.redfish_storage_volume:
        baseuri: "192.168.0.1"
        username: "username"
        password: "password"
        state: "present"
        controller_id: "RAID.Slot.1-1"
        raid_type: "RAID0"
        drives:
          - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1
          - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-2
        reboot_server: true
        force_reboot: true

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

    - name: Create a RAID6 volume
      dellemc.openmanage.redfish_storage_volume:
        baseuri: "192.168.0.1"
        username: "username"
        password: "password"
        state: "present"
        controller_id: "RAID.Slot.1-1"
        raid_type: "RAID6"
        drives:
          - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1
          - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-2
          - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-3
          - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-4

    - name: Create a RAID60 volume
      dellemc.openmanage.redfish_storage_volume:
        baseuri: "192.168.0.1"
        username: "username"
        password: "password"
        state: "present"
        controller_id: "RAID.Slot.1-1"
        raid_type: "RAID60"
        drives:
          - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1
          - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-2
          - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-3
          - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-4
          - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-5
          - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-6
          - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-7
          - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-8



Return Values
-------------

msg (always, str, Successfully submitted create volume task.)
  Overall status of the storage configuration operation.


task (success, dict, {'id': 'JID_XXXXXXXXXXXXX', 'uri': '/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_XXXXXXXXXXXXX'})
  Returns ID and URI of the created task.


error_info (on http error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to perform configuration operations because a configuration job for the device already exists.', 'MessageArgs': [], 'MessageArgs@odata.count': 0, 'MessageId': 'IDRAC.1.6.STOR023', 'RelatedProperties': [], 'RelatedProperties@odata.count': 0, 'Resolution': 'Wait for the current job for the device to complete or cancel the current job before attempting more configuration operations on the device.', 'Severity': 'Informational'}], 'code': 'Base.1.2.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information'}})
  Details of a http error.





Status
------





Authors
~~~~~~~

- Sajna Shetty(@Sajna-Shetty)
- Kritika Bhateja(@Kritika-Bhateja-03)
- Shivam Sharma(@ShivamSh3)

