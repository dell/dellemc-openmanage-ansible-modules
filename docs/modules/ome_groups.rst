.. _ome_groups_module:


ome_groups -- Manages static device groups on OpenManage Enterprise
===================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to create, modify, and delete static device groups on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  state (optional, str, present)
    ``present`` allows to create or modify a device group.

    ``absent`` allows to delete a device group.


  name (optional, list, None)
    Name of the device group to be created, modified, or deleted.

    If *state* is absent, multiple names can be provided.

    This option is case insensitive.

    This option is mutually exclusive with *group_id*.


  group_id (optional, list, None)
    ID of the device group to be created, modified, or deleted.

    If *state* is absent, multiple IDs can be provided.

    This option is mutually exclusive with *name*.


  new_name (optional, str, None)
    New name for the existing device group.

    This is applicable only when *state* is ``present``.


  description (optional, str, None)
    Description for the device group.

    This is applicable only when *state* is ``present``.


  parent_group_name (optional, str, Static Groups)
    Name of the parent device group under which the device group to be created or modified.

    This is applicable only when *state* is ``present``.

    ``NOTE`` If device group with such a name does not exist, device group with *parent_group_name* is created.

    This option is case insensitive.

    This option is mutually exclusive with *parent_group_id*.


  parent_group_id (optional, int, None)
    ID of the parent device group under which the device group to be created or modified.

    This is applicable only when *state* is ``present``.

    This option is mutually exclusive with *parent_group_name*.


  hostname (True, str, None)
    OpenManage Enterprise IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise username.


  password (True, str, None)
    OpenManage Enterprise password.


  port (optional, int, 443)
    OpenManage Enterprise HTTPS port.


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
   - This module manages only static device groups on Dell OpenManage Enterprise.
   - If a device group with the name *parent_group_name* does not exist, a new device group with the same name is created.
   - Make sure the entered parent group is not the descendant of the provided group.
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create a new device group
      dellemc.openmanage.ome_groups:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        name: "group 1"
        description: "Group 1 description"
        parent_group_name: "group parent 1"

    - name: Modify a device group using the group ID
      dellemc.openmanage.ome_groups:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        group_id: 1234
        description: "Group description updated"
        parent_group_name: "group parent 2"

    - name: Delete a device group using the device group name
      dellemc.openmanage.ome_groups:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: absent
        name: "group 1"

    - name: Delete multiple device groups using the group IDs
      dellemc.openmanage.ome_groups:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: absent
        group_id:
          - 1234
          - 5678



Return Values
-------------

msg (always, str, Successfully deleted the device group(s).)
  Overall status of the device group operation.


group_status (success, dict, {'Description': 'my group description', 'Id': 12123, 'MembershipTypeId': 12, 'Name': 'group 1', 'ParentId': 12345, 'TypeId': 3000, 'IdOwner': 30, 'CreatedBy': 'admin', 'CreationTime': '2021-01-01 10:10:10.100', 'DefinitionDescription': 'UserDefined', 'DefinitionId': 400, 'GlobalStatus': 5000, 'HasAttributes': False, 'UpdatedBy': '', 'UpdatedTime': '2021-01-01 11:11:10.100', 'Visible': True})
  Details of the device group operation status.


group_ids (when I(state) is C(absent), list, [1234, 5678])
  List of the deleted device group IDs.


invalid_groups (when I(state) is C(absent), list, [1234, 5678])
  List of the invalid device group IDs or names.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'CGRP9013', 'RelatedProperties': [], 'Message': 'Unable to update group  12345  with the provided parent  54321  because a group/parent relationship already exists.', 'MessageArgs': ['12345', '54321'], 'Severity': 'Warning', 'Resolution': 'Make sure the entered parent ID does not create a bidirectional relationship and retry the operation.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

