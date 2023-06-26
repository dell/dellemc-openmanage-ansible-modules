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

- python >= 3.8.6



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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.
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
        ca_path: "/path/to/ca_cert.pem"

    - name: Retrieve details of a specific account identified by its account ID
      dellemc.openmanage.ome_user_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        account_id: 1

    - name: Get filtered user info based on user name
      dellemc.openmanage.ome_user_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
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

