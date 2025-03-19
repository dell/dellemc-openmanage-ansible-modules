.. _dellemc_idrac_storage_volume_module:


dellemc_idrac_storage_volume -- Configures the RAID configuration attributes
============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module is responsible for configuring the RAID attributes.



Requirements
------------
The below requirements are needed on the host that executes this module.

- omsdk >= 1.2.488
- python >= 3.9.6



Parameters
----------

  state (optional, str, view)
    ``create``, performs create volume operation.

    ``delete``, performs remove volume operation.

    ``view``, returns storage view.


  span_depth (optional, int, 1)
    Number of spans in the RAID configuration.

    *span_depth* is required for ``create`` and its value depends on *volume_type*.


  span_length (optional, int, 1)
    Number of disks in a span.

    *span_length* is required for ``create`` and its value depends on *volume_type*.


  number_dedicated_hot_spare (optional, int, 0)
    Number of Dedicated Hot Spare.


  volume_type (optional, str, RAID 0)
    Provide the the required RAID level.


  disk_cache_policy (optional, str, Default)
    Disk Cache Policy.


  write_cache_policy (optional, str, WriteThrough)
    Write cache policy.


  read_cache_policy (optional, str, NoReadAhead)
    Read cache policy.


  stripe_size (optional, int, 65536)
    Stripe size value to be provided in multiples of 64 * 1024.


  controller_id (optional, str, None)
    Fully Qualified Device Descriptor (FQDD) of the storage controller, for example 'RAID.Integrated.1-1'. Controller FQDD is required for ``create`` RAID configuration.


  media_type (optional, str, None)
    Media type.


  protocol (optional, str, None)
    Bus protocol.


  volume_id (optional, str, None)
    Fully Qualified Device Descriptor (FQDD) of the virtual disk, for example 'Disk.virtual.0:RAID.Slot.1-1'. This option is used to get the virtual disk information.


  volumes (optional, list, None)
    A list of virtual disk specific iDRAC attributes. This is applicable for ``create`` and ``delete`` operations.

    For ``create`` operation, name and drives are applicable options, other volume options can also be specified.

    The drives is a required option for ``create`` operation and accepts either location (list of drive slot) or id (list of drive fqdd).

    For ``delete`` operation, only name option is applicable.

    See the examples for more details.


  capacity (optional, float, None)
    Virtual disk size in GB.


  raid_reset_config (optional, str, False)
    This option represents whether a reset config operation needs to be performed on the RAID controller. Reset Config operation deletes all the virtual disks present on the RAID controller.


  raid_init_operation (optional, str, None)
    This option represents initialization configuration operation to be performed on the virtual disk.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.


  idrac_password (True, str, None)
    iDRAC user password.


  idrac_port (optional, int, 443)
    iDRAC port.


  validate_certs (optional, bool, True)
    If ``false``, the SSL certificates will not be validated.

    Configure ``false`` only on personally controlled sites where self-signed certificates are used.

    Prior to collection version ``5.0.0``, the *validate_certs* is ``false`` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports both IPv4 and IPv6 address for *idrac_ip*.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create single volume
      dellemc.openmanage.dellemc_idrac_storage_volume:
        idrac_ip: "192.168.0.1"
        idrac_user: "username"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "create"
        controller_id: "RAID.Slot.1-1"
        volumes:
          - drives:
            location: [5]

    - name: Create multiple volume
      dellemc.openmanage.dellemc_idrac_storage_volume:
        idrac_ip: "192.168.0.1"
        idrac_user: "username"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        raid_reset_config: "True"
        state: "create"
        controller_id: "RAID.Slot.1-1"
        volume_type: "RAID 1"
        span_depth: 1
        span_length: 2
        number_dedicated_hot_spare: 1
        disk_cache_policy: "Enabled"
        write_cache_policy: "WriteBackForce"
        read_cache_policy: "ReadAhead"
        stripe_size: 65536
        capacity: 100
        raid_init_operation: "Fast"
        volumes:
          - name: "volume_1"
            drives:
              id: ["Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1", "Disk.Bay.2:Enclosure.Internal.0-1:RAID.Slot.1-1"]
          - name: "volume_2"
            volume_type: "RAID 5"
            span_length: 3
            span_depth: 1
            drives:
              location: [7, 3, 5]
            disk_cache_policy: "Disabled"
            write_cache_policy: "WriteBack"
            read_cache_policy: "NoReadAhead"
            stripe_size: 131072
            capacity: "200"
            raid_init_operation: "None"

    - name: View all volume details
      dellemc.openmanage.dellemc_idrac_storage_volume:
        idrac_ip: "192.168.0.1"
        idrac_user: "username"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "view"

    - name: View specific volume details
      dellemc.openmanage.dellemc_idrac_storage_volume:
        idrac_ip: "192.168.0.1"
        idrac_user: "username"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "view"
        controller_id: "RAID.Slot.1-1"
        volume_id: "Disk.Virtual.0:RAID.Slot.1-1"

    - name: Delete single volume
      dellemc.openmanage.dellemc_idrac_storage_volume:
        idrac_ip: "192.168.0.1"
        idrac_user: "username"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "delete"
        volumes:
          - name: "volume_1"

    - name: Delete multiple volume
      dellemc.openmanage.dellemc_idrac_storage_volume:
        idrac_ip: "192.168.0.1"
        idrac_user: "username"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "delete"
        volumes:
          - name: "volume_1"
          - name: "volume_2"



Return Values
-------------

msg (always, str, Successfully completed the view storage volume operation)
  Overall status of the storage configuration operation.


storage_status (success, dict, {'Id': 'JID_XXXXXXXXX', 'JobState': 'Completed', 'JobType': 'ImportConfiguration', 'Message': 'Successfully imported and applied Server Configuration Profile.', 'MessageId': 'XXX123', 'Name': 'Import Configuration', 'PercentComplete': 100, 'StartTime': 'TIME_NOW', 'Status': 'Success', 'TargetSettingsURI': None, 'retval': True})
  Storage configuration job and progress details from the iDRAC.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)

