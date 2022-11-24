.. _ome_profile_module:


ome_profile -- Create, modify, delete, assign, unassign and migrate a profile on OpenManage Enterprise
======================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to create, modify, delete, assign, unassign, and migrate a profile on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  command (optional, str, create)
    ``create`` creates new profiles.

    ``modify`` modifies an existing profile. Only *name*, *description*, *boot_to_network_iso*, and *attributes* can be modified.

    ``delete`` deletes an existing profile.

    ``assign`` Deploys an existing profile on a target device and returns a task ID.

    ``unassign`` unassigns a profile from a specified target and returns a task ID.

    ``migrate`` migrates an existing profile and returns a task ID.


  name_prefix (optional, str, Profile)
    The name provided when creating a profile is used a prefix followed by the number assigned to it by OpenManage Enterprise.

    This is applicable only for a create operation.

    This option is mutually exclusive with *name*.


  name (optional, str, None)
    Name of the profile.

    This is applicable for modify, delete, assign, unassign, and migrate operations.

    This option is mutually exclusive with *name_prefix* and *number_of_profiles*.


  new_name (optional, str, None)
    New name of the profile.

    Applicable when *command* is ``modify``.


  number_of_profiles (optional, int, 1)
    Provide the number of profiles to be created.

    This is applicable when *name_prefix* is used with ``create``.

    This option is mutually exclusive with *name*.

    Openmanage Enterprise can create a maximum of 100 profiles.


  template_name (optional, str, None)
    Name of the template for creating the profile(s).

    This is applicable when *command* is ``create``.

    This option is mutually exclusive with *template_id*.


  template_id (optional, int, None)
    ID of the template.

    This is applicable when *command* is ``create``.

    This option is mutually exclusive with *template_name*.


  device_id (optional, int, None)
    ID of the target device.

    This is applicable when *command* is ``assign`` and ``migrate``.

    This option is mutually exclusive with *device_service_tag*.


  device_service_tag (optional, str, None)
    Identifier of the target device.

    This is typically 7 to 8 characters in length.

    Applicable when *command* is ``assign``, and ``migrate``.

    This option is mutually exclusive with *device_id*.

    If the device does not exist when *command* is ``assign`` then the profile is auto-deployed.


  description (optional, str, None)
    Description of the profile.


  boot_to_network_iso (optional, dict, None)
    Details of the Share iso.

    Applicable when *command* is ``create``, ``assign``, and ``modify``.


    boot_to_network (True, bool, None)
      Enable or disable a network share.


    share_type (optional, str, None)
      Type of network share.


    share_ip (optional, str, None)
      IP address of the network share.


    share_user (optional, str, None)
      User name when *share_type* is ``CIFS``.


    share_password (optional, str, None)
      User password when *share_type* is ``CIFS``.


    workgroup (optional, str, None)
      User workgroup when *share_type* is ``CIFS``.


    iso_path (optional, str, None)
      Specify the full ISO path including the share name.


    iso_timeout (optional, int, 4)
      Set the number of hours that the network ISO file will remain mapped to the target device(s).



  filters (optional, dict, None)
    Filters the profiles based on selected criteria.

    This is applicable when *command* is ``delete`` or ``unassign``.

    This supports suboption *ProfileIds* which takes a list of profile IDs.

    This also supports OData filter expressions with the suboption *Filters*.

    See OpenManage Enterprise REST API guide for the filtering options available.

    *WARNING* When this option is used in case of ``unassign``, task ID is not returned for any of the profiles affected.


  force (optional, bool, False)
    Provides the option to force the migration of a profile even if the source device cannot be contacted.

    This option is applicable when *command* is ``migrate``.


  attributes (optional, dict, None)
    Attributes for ``modify`` and ``assign``.


    Attributes (optional, list, None)
      List of attributes to be modified, when *command* is ``modify``.

      List of attributes to be overridden when *command* is ``assign``.

      Use the *Id* If the attribute Id is available. If not, use the comma separated I (DisplayName). For more details about using the *DisplayName*, see the example provided.


    Options (optional, dict, None)
      Provides the different shut down options.

      This is applicable when *command* is ``assign``.


    Schedule (optional, dict, None)
      Schedule for profile deployment.

      This is applicable when *command* is ``assign``.



  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.


  password (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.


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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.
   - This module supports ``check_mode``.
   - ``assign`` operation on a already assigned profile will not redeploy.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create two profiles from a template
      dellemc.openmanage.ome_profile:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        template_name: "template 1"
        name_prefix: "omam_profile"
        number_of_profiles: 2

    - name: Create profile with NFS share
      dellemc.openmanage.ome_profile:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: create
        template_name: "template 1"
        name_prefix: "omam_profile"
        number_of_profiles: 1
        boot_to_network_iso:
          boot_to_network: True
          share_type: NFS
          share_ip: "192.168.0.1"
          iso_path: "path/to/my_iso.iso"
          iso_timeout: 8

    - name: Create profile with CIFS share
      dellemc.openmanage.ome_profile:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: create
        template_name: "template 1"
        name_prefix: "omam_profile"
        number_of_profiles: 1
        boot_to_network_iso:
          boot_to_network: True
          share_type: CIFS
          share_ip: "192.168.0.2"
          share_user: "username"
          share_password: "password"
          workgroup: "workgroup"
          iso_path: "\\path\\to\\my_iso.iso"
          iso_timeout: 8

    - name: Modify profile name with NFS share and attributes
      dellemc.openmanage.ome_profile:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: modify
        name: "Profile 00001"
        new_name: "modified profile"
        description: "new description"
        boot_to_network_iso:
          boot_to_network: True
          share_type: NFS
          share_ip: "192.168.0.3"
          iso_path: "path/to/my_iso.iso"
          iso_timeout: 8
        attributes:
          Attributes:
            - Id: 4506
              Value: "server attr 1"
              IsIgnored: false
            - Id: 4507
              Value: "server attr 2"
              IsIgnored: false
            # Enter the comma separated string as appearing in the Detailed view on GUI
            # System -> Server Topology -> ServerTopology 1 Aisle Name
            - DisplayName: 'System, Server Topology, ServerTopology 1 Aisle Name'
              Value: Aisle 5
              IsIgnored: false

    - name: Delete a profile using profile name
      dellemc.openmanage.ome_profile:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: "delete"
        name: "Profile 00001"

    - name: Delete profiles using filters
      dellemc.openmanage.ome_profile:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: "delete"
        filters:
          SelectAll: True
          Filters: =contains(ProfileName,'Profile 00002')

    - name: Delete profiles using profile list filter
      dellemc.openmanage.ome_profile:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: "delete"
        filters:
          ProfileIds:
            - 17123
            - 16124

    - name: Assign a profile to target along with network share
      dellemc.openmanage.ome_profile:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: assign
        name: "Profile 00001"
        device_id: 12456
        boot_to_network_iso:
          boot_to_network: True
          share_type: NFS
          share_ip: "192.168.0.1"
          iso_path: "path/to/my_iso.iso"
          iso_timeout: 8
        attributes:
          Attributes:
            - Id: 4506
              Value: "server attr 1"
              IsIgnored: true
          Options:
            ShutdownType: 0
            TimeToWaitBeforeShutdown: 300
            EndHostPowerState: 1
            StrictCheckingVlan: True
          Schedule:
            RunNow: True
            RunLater: False

    - name: Unassign a profile using profile name
      dellemc.openmanage.ome_profile:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: "unassign"
        name: "Profile 00003"

    - name: Unassign profiles using filters
      dellemc.openmanage.ome_profile:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: "unassign"
        filters:
          SelectAll: True
          Filters: =contains(ProfileName,'Profile 00003')

    - name: Unassign profiles using profile list filter
      dellemc.openmanage.ome_profile:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: "unassign"
        filters:
          ProfileIds:
            - 17123
            - 16123

    - name: Migrate a profile
      dellemc.openmanage.ome_profile:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: "migrate"
        name: "Profile 00001"
        device_id: 12456



Return Values
-------------

msg (always, str, Successfully created 2 profile(s).)
  Overall status of the profile operation.


profile_ids (when I(command) is C(create), list, [1234, 5678])
  IDs of the profiles created.


job_id (when I(command) is C(assign), C(migrate) or C(unassign), int, 14123)
  Task ID created when *command* is ``assign``, ``migrate`` or ``unassign``.

  ``assign`` and ``unassign`` operations do not trigger a task if a profile is auto-deployed.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V (@jagadeeshnv)

