.. _ome_user_module:


ome_user -- Create, modify or delete a user on OpenManage Enterprise
====================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module creates, modifies or deletes a user on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7.5



Parameters
----------

  state (optional, str, present)
    ``present`` creates a user in case the *UserName* provided inside *attributes* does not exist.

    ``present`` modifies a user in case the *UserName* provided inside *attributes* exists.

    ``absent`` deletes an existing user.


  user_id (optional, int, None)
    Unique ID of the user to be deleted.

    Either *user_id* or *name* is mandatory for ``absent`` operation.


  name (optional, str, None)
    Unique Name of the user to be deleted.

    Either *user_id* or *name* is mandatory for ``absent`` operation.


  attributes (optional, dict, {})
    Payload data for the user operations. It can take the following attributes for ``present``.

    UserTypeId, DirectoryServiceId, Description, Name, Password, UserName, RoleId, Locked, Enabled.

    OME will throw error if required parameter is not provided for operation.

    Refer OpenManage Enterprise API Reference Guide for more details.


  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.


  password (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.





Notes
-----

.. note::
   - Run this module from a system that has direct access to DellEMC OpenManage Enterprise.
   - This module does not support ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create user with required parameters
      dellemc.openmanage.ome_user:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        attributes:
          UserName: "user1"
          Password: "UserPassword"
          RoleId: "10"
          Enabled: True

    - name: Create user with all parameters
      dellemc.openmanage.ome_user:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        attributes:
          UserName: "user2"
          Description: "user2 description"
          Password: "UserPassword"
          RoleId: "10"
          Enabled: True
          DirectoryServiceId: 0
          UserTypeId: 1
          Locked: False
          Name: "user2"

    - name: Modify existing user
      dellemc.openmanage.ome_user:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        state: "present"
        attributes:
          UserName: "user3"
          RoleId: "10"
          Enabled: True
          Description: "Modify user Description"

    - name: Delete existing user using id
      dellemc.openmanage.ome_user:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        state: "absent"
        user_id: 1234

    - name: Delete existing user using name
      dellemc.openmanage.ome_user:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        state: "absent"
        name: "name"



Return Values
-------------

msg (always, str, Successfully created a User)
  Overall status of the user operation.


user_status (When I(state) is C(present)., dict, {'Description': 'Test user creation', 'DirectoryServiceId': 0, 'Enabled': True, 'Id': '61546', 'IsBuiltin': False, 'Locked': False, 'Name': 'test', 'Password': None, 'PlainTextPassword': None, 'RoleId': '10', 'UserName': 'test', 'UserTypeId': 1})
  Details of the user operation, when *state* is ``present``.





Status
------





Authors
~~~~~~~

- Sajna Shetty(@Sajna-Shetty)

