.. _ome_user_info_module:


ome_user_info -- Retrieves details of all accounts or a specific account on OpenManage Enterprise
=================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves the list and basic details of all accounts or details of a specific account on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7.5



Parameters
----------

  account_id (optional, int, None)
    Unique Id of the account.


  system_query_options (optional, dict, None)
    Options for filtering the output.


    filter (optional, str, None)
      Filter records for the supported values.



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
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Retrieve basic details of all accounts
      dellemc.openmanage.ome_user_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"

    - name: Retrieve details of a specific account identified by its account ID
      dellemc.openmanage.ome_user_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        account_id: 1

    - name: Get filtered user info based on user name
      dellemc.openmanage.ome_user_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        system_query_options:
          filter: "UserName eq 'test'"



Return Values
-------------

msg (on error, str, Unable to retrieve the account details.)
  Over all status of fetching user facts.


user_info (success, dict, {'192.168.0.1': {'Id': '1814', 'UserTypeId': 1, 'DirectoryServiceId': 0, 'Description': 'user name description', 'Name': 'user_name', 'Password': None, 'UserName': 'user_name', 'RoleId': '10', 'Locked': False, 'IsBuiltin': True, 'Enabled': True}})
  Details of the user.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

