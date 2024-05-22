.. _idrac_storage_volume_module:


idrac_storage_volume -- Configures the RAID configuration attributes
====================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module is responsible for configuring the RAID attributes.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  state (optional, str, view)
    \ :literal:`create`\ , performs create volume operation.

    \ :literal:`delete`\ , performs remove volume operation.

    \ :literal:`view`\ , returns storage view.


  span_depth (optional, int, 1)
    Number of spans in the RAID configuration.

    \ :emphasis:`span\_depth`\  is required for \ :literal:`create`\  and its value depends on \ :emphasis:`volume\_type`\ .


  span_length (optional, int, 1)
    Number of disks in a span.

    \ :emphasis:`span\_length`\  is required for \ :literal:`create`\  and its value depends on \ :emphasis:`volume\_type`\ .


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
    Stripe size value to be provided in multiples of 64 \* 1024.


  controller_id (optional, str, None)
    Fully Qualified Device Descriptor (FQDD) of the storage controller, for example 'RAID.Integrated.1-1'. Controller FQDD is required for \ :literal:`create`\  RAID configuration.


  media_type (optional, str, None)
    Media type.


  protocol (optional, str, None)
    Bus protocol.


  volume_id (optional, str, None)
    Fully Qualified Device Descriptor (FQDD) of the virtual disk, for example 'Disk.virtual.0:RAID.Slot.1-1'. This option is used to get the virtual disk information.


  volumes (optional, list, None)
    A list of virtual disk specific iDRAC attributes. This is applicable for \ :literal:`create`\  and \ :literal:`delete`\  operations.

    For \ :literal:`create`\  operation, name and drives are applicable options, other volume options can also be specified.

    The drives is a required option for \ :literal:`create`\  operation and accepts either location (list of drive slot) or id (list of drive fqdd).

    In iDRAC8, there is no pre-validation for the state of drives. The disk ID or slot number of the drive provided may or may not be in Ready state. Enter the disk ID or slot number of the drive that is already in Ready state.

    For \ :literal:`delete`\  operation, only name option is applicable.

    See the examples for more details.


  capacity (optional, float, None)
    Virtual disk size in GB.


  raid_reset_config (optional, str, false)
    This option represents whether a reset config operation needs to be performed on the RAID controller. Reset Config operation deletes all the virtual disks present on the RAID controller.


  raid_init_operation (optional, str, None)
    This option represents initialization configuration operation to be performed on the virtual disk.


  job_wait (optional, bool, True)
    This parameter provides the option to wait for the job completion.

    This is applicable when \ :emphasis:`state`\  is \ :literal:`create`\  or \ :literal:`delete`\ .


  job_wait_timeout (optional, int, 900)
    This parameter is the maximum wait time of \ :emphasis:`job\_wait`\  in seconds.

    This option is applicable when \ :emphasis:`job\_wait`\  is \ :literal:`true`\ .


  time_to_wait (optional, int, 300)
    The maximum wait time before shutdown in seconds for the Server Configuration Profile (SCP) import operation.

    This option is applicable when \ :emphasis:`state`\  is \ :literal:`create`\  or \ :literal:`delete`\ .


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (False, str, None)
    iDRAC username.

    If the username is not provided, then the environment variable \ :envvar:`IDRAC\_USERNAME`\  is used.

    Example: export IDRAC\_USERNAME=username


  idrac_password (False, str, None)
    iDRAC user password.

    If the password is not provided, then the environment variable \ :envvar:`IDRAC\_PASSWORD`\  is used.

    Example: export IDRAC\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`IDRAC\_X\_AUTH\_TOKEN`\  is used.

    Example: export IDRAC\_X\_AUTH\_TOKEN=x\_auth\_token


  idrac_port (optional, int, 443)
    iDRAC port.


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
   - Run this module from a system that has direct access to Integrated Dell Remote Access Controller.
   - This module supports both IPv4 and IPv6 address for \ :emphasis:`idrac\_ip`\ .
   - This module supports \ :literal:`check\_mode`\ .
   - This module does not display the controller battery details for the \ :literal:`view`\  operation of the storage in iDRAC8.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create single volume
      dellemc.openmanage.idrac_storage_volume:
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
      dellemc.openmanage.idrac_storage_volume:
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
      dellemc.openmanage.idrac_storage_volume:
        idrac_ip: "192.168.0.1"
        idrac_user: "username"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "view"

    - name: View specific volume details
      dellemc.openmanage.idrac_storage_volume:
        idrac_ip: "192.168.0.1"
        idrac_user: "username"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "view"
        controller_id: "RAID.Slot.1-1"
        volume_id: "Disk.Virtual.0:RAID.Slot.1-1"

    - name: Delete single volume
      dellemc.openmanage.idrac_storage_volume:
        idrac_ip: "192.168.0.1"
        idrac_user: "username"
        idrac_password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "delete"
        volumes:
          - name: "volume_1"

    - name: Delete multiple volume
      dellemc.openmanage.idrac_storage_volume:
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


storage_status (success, dict, {'Id': 'JID_XXXXXXXXX', 'JobState': 'Completed', 'JobType': 'ImportConfiguration', 'Message': 'Successfully imported and applied Server Configuration Profile.', 'MessageId': 'XXX123', 'Name': 'Import Configuration', 'PercentComplete': 100, 'StartTime': 'TIME_NOW', 'TargetSettingsURI': None})
  Storage configuration job and progress details from the iDRAC.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)
- Kritika Bhateja (@Kritika-Bhateja-03)
- Abhishek Sinha(@ABHISHEK-SINHA10)

