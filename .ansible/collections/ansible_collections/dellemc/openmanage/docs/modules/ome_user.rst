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

- python \>= 3.9.6



Parameters
----------

  state (optional, str, present)
    \ :literal:`present`\  creates a user in case the \ :emphasis:`UserName`\  provided inside \ :emphasis:`attributes`\  does not exist.

    \ :literal:`present`\  modifies a user in case the \ :emphasis:`UserName`\  provided inside \ :emphasis:`attributes`\  exists.

    \ :literal:`absent`\  deletes an existing user.


  user_id (optional, int, None)
    Unique ID of the user to be deleted.

    Either \ :emphasis:`user\_id`\  or \ :emphasis:`name`\  is mandatory for \ :literal:`absent`\  operation.


  name (optional, str, None)
    Unique Name of the user to be deleted.

    Either \ :emphasis:`user\_id`\  or \ :emphasis:`name`\  is mandatory for \ :literal:`absent`\  operation.


  attributes (optional, dict, {})
    Payload data for the user operations. It can take the following attributes for \ :literal:`present`\ .

    UserTypeId, DirectoryServiceId, Description, Name, Password, UserName, RoleId, Locked, Enabled.

    OME will throw error if required parameter is not provided for operation.

    Refer OpenManage Enterprise API Reference Guide for more details.


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
   - This module does not support \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create user with required parameters
      dellemc.openmanage.ome_user:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        attributes:
          UserName: "user1"
          Password: "UserPassword"
          RoleId: "10"
          Enabled: true

    - name: Create user with all parameters
      dellemc.openmanage.ome_user:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        attributes:
          UserName: "user2"
          Description: "user2 description"
          Password: "UserPassword"
          RoleId: "10"
          Enabled: true
          DirectoryServiceId: 0
          UserTypeId: 1
          Locked: false
          Name: "user2"

    - name: Modify existing user
      dellemc.openmanage.ome_user:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "present"
        attributes:
          UserName: "user3"
          RoleId: "10"
          Enabled: true
          Description: "Modify user Description"

    - name: Delete existing user using id
      dellemc.openmanage.ome_user:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "absent"
        user_id: 1234

    - name: Delete existing user using name
      dellemc.openmanage.ome_user:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "absent"
        name: "name"



Return Values
-------------

msg (always, str, Successfully created a User)
  Overall status of the user operation.


user_status (When I(state) is C(present)., dict, {'Description': 'Test user creation', 'DirectoryServiceId': 0, 'Enabled': True, 'Id': '61546', 'IsBuiltin': False, 'Locked': False, 'Name': 'test', 'Password': None, 'PlainTextPassword': None, 'RoleId': '10', 'UserName': 'test', 'UserTypeId': 1})
  Details of the user operation, when \ :emphasis:`state`\  is \ :literal:`present`\ .





Status
------





Authors
~~~~~~~

- Sajna Shetty(@Sajna-Shetty)

