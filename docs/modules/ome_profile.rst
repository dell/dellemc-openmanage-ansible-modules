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

- python \>= 3.9.6



Parameters
----------

  command (optional, str, create)
    \ :literal:`create`\  creates new profiles.

    \ :literal:`modify`\  modifies an existing profile. Only \ :emphasis:`name`\ , \ :emphasis:`description`\ , \ :emphasis:`boot\_to\_network\_iso`\ , and \ :emphasis:`attributes`\  can be modified.

    \ :literal:`delete`\  deletes an existing profile.

    \ :literal:`assign`\  Deploys an existing profile on a target device and returns a task ID.

    \ :literal:`unassign`\  unassigns a profile from a specified target and returns a task ID.

    \ :literal:`migrate`\  migrates an existing profile and returns a task ID.


  name_prefix (optional, str, Profile)
    The name provided when creating a profile is used a prefix followed by the number assigned to it by OpenManage Enterprise.

    This is applicable only for a create operation.

    This option is mutually exclusive with \ :emphasis:`name`\ .


  name (optional, str, None)
    Name of the profile.

    This is applicable for modify, delete, assign, unassign, and migrate operations.

    This option is mutually exclusive with \ :emphasis:`name\_prefix`\  and \ :emphasis:`number\_of\_profiles`\ .


  new_name (optional, str, None)
    New name of the profile.

    Applicable when \ :emphasis:`command`\  is \ :literal:`modify`\ .


  number_of_profiles (optional, int, 1)
    Provide the number of profiles to be created.

    This is applicable when \ :emphasis:`name\_prefix`\  is used with \ :literal:`create`\ .

    This option is mutually exclusive with \ :emphasis:`name`\ .

    Openmanage Enterprise can create a maximum of 100 profiles.


  template_name (optional, str, None)
    Name of the template for creating the profile(s).

    This is applicable when \ :emphasis:`command`\  is \ :literal:`create`\ .

    This option is mutually exclusive with \ :emphasis:`template\_id`\ .


  template_id (optional, int, None)
    ID of the template.

    This is applicable when \ :emphasis:`command`\  is \ :literal:`create`\ .

    This option is mutually exclusive with \ :emphasis:`template\_name`\ .


  device_id (optional, int, None)
    ID of the target device.

    This is applicable when \ :emphasis:`command`\  is \ :literal:`assign`\  and \ :literal:`migrate`\ .

    This option is mutually exclusive with \ :emphasis:`device\_service\_tag`\ .


  device_service_tag (optional, str, None)
    Identifier of the target device.

    This is typically 7 to 8 characters in length.

    Applicable when \ :emphasis:`command`\  is \ :literal:`assign`\ , and \ :literal:`migrate`\ .

    This option is mutually exclusive with \ :emphasis:`device\_id`\ .

    If the device does not exist when \ :emphasis:`command`\  is \ :literal:`assign`\  then the profile is auto-deployed.


  description (optional, str, None)
    Description of the profile.


  boot_to_network_iso (optional, dict, None)
    Details of the Share iso.

    Applicable when \ :emphasis:`command`\  is \ :literal:`create`\ , \ :literal:`assign`\ , and \ :literal:`modify`\ .


    boot_to_network (True, bool, None)
      Enable or disable a network share.


    share_type (optional, str, None)
      Type of network share.


    share_ip (optional, str, None)
      IP address of the network share.


    share_user (optional, str, None)
      User name when \ :emphasis:`share\_type`\  is \ :literal:`CIFS`\ .


    share_password (optional, str, None)
      User password when \ :emphasis:`share\_type`\  is \ :literal:`CIFS`\ .


    workgroup (optional, str, None)
      User workgroup when \ :emphasis:`share\_type`\  is \ :literal:`CIFS`\ .


    iso_path (optional, str, None)
      Specify the full ISO path including the share name.


    iso_timeout (optional, int, 4)
      Set the number of hours that the network ISO file will remain mapped to the target device(s).



  filters (optional, dict, None)
    Filters the profiles based on selected criteria.

    This is applicable when \ :emphasis:`command`\  is \ :literal:`delete`\  or \ :literal:`unassign`\ .

    This supports suboption \ :emphasis:`ProfileIds`\  which takes a list of profile IDs.

    This also supports OData filter expressions with the suboption \ :emphasis:`Filters`\ .

    See OpenManage Enterprise REST API guide for the filtering options available.

    \ :emphasis:`WARNING`\  When this option is used in case of \ :literal:`unassign`\ , task ID is not returned for any of the profiles affected.


  force (optional, bool, False)
    Provides the option to force the migration of a profile even if the source device cannot be contacted.

    This option is applicable when \ :emphasis:`command`\  is \ :literal:`migrate`\ .


  attributes (optional, dict, None)
    Attributes for \ :literal:`modify`\  and \ :literal:`assign`\ .


    Attributes (optional, list, None)
      List of attributes to be modified, when \ :emphasis:`command`\  is \ :literal:`modify`\ .

      List of attributes to be overridden when \ :emphasis:`command`\  is \ :literal:`assign`\ .

      Use the \ :emphasis:`Id`\  If the attribute Id is available. If not, use the comma separated I (DisplayName). For more details about using the \ :emphasis:`DisplayName`\ , see the example provided.


    Options (optional, dict, None)
      Provides the different shut down options.

      This is applicable when \ :emphasis:`command`\  is \ :literal:`assign`\ .


    Schedule (optional, dict, None)
      Schedule for profile deployment.

      This is applicable when \ :emphasis:`command`\  is \ :literal:`assign`\ .



  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (False, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.

    If the username is not provided, then the environment variable \ :envvar:`OME\_USERNAME`\  is used.

    Example: export OME\_USERNAME=username


  password (False, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.

    If the password is not provided, then the environment variable \ :envvar:`OME\_PASSWORD`\  is used.

    Example: export OME\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`OME\_X\_AUTH\_TOKEN`\  is used.

    Example: export OME\_X\_AUTH\_TOKEN=x\_auth\_token


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.


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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.
   - This module supports \ :literal:`check\_mode`\ .
   - \ :literal:`assign`\  operation on a already assigned profile will not redeploy.




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
          boot_to_network: true
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
          boot_to_network: true
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
          boot_to_network: true
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
          SelectAll: true
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
          boot_to_network: true
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
            StrictCheckingVlan: true
          Schedule:
            RunNow: true
            RunLater: false

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
          SelectAll: true
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
  Task ID created when \ :emphasis:`command`\  is \ :literal:`assign`\ , \ :literal:`migrate`\  or \ :literal:`unassign`\ .

  \ :literal:`assign`\  and \ :literal:`unassign`\  operations do not trigger a task if a profile is auto-deployed.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V (@jagadeeshnv)

