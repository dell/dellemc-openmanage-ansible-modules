.. _ome_network_vlan_module:


ome_network_vlan -- Create, modify & delete a VLAN
==================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to,

Create a VLAN on OpenManage Enterprise.

Modify or delete an existing VLAN on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  state (optional, str, present)
    \ :literal:`present`\  creates a new VLAN or modifies an existing VLAN.

    \ :literal:`absent`\  deletes an existing VLAN.

    \ :emphasis:`WARNING`\  Deleting a VLAN can impact the network infrastructure.


  name (True, str, None)
    Provide the \ :emphasis:`name`\  of the VLAN to be created, deleted or modified.


  new_name (optional, str, None)
    Provide the \ :emphasis:`name`\  of the VLAN to be modified.


  description (optional, str, None)
    Short description of the VLAN to be created or modified.


  vlan_minimum (optional, int, None)
    The minimum VLAN value of the range.


  vlan_maximum (optional, int, None)
    The maximum VLAN value of the range.

    A single value VLAN is created if the vlan\_maximum and vlan\_minmum values are the same.


  type (optional, str, None)
    Types of supported VLAN networks.

    For the description of each network type, use API \ https://I(hostname\ /api/NetworkConfigurationService/NetworkTypes).


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




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create a VLAN range
      dellemc.openmanage.ome_network_vlan:
        hostname: "{{hostname}}"
        username: "{{username}}"
        password: "{{password}}"
        ca_path: "/path/to/ca_cert.pem"
        state: present
        name: "vlan1"
        description: "VLAN desc"
        type: "General Purpose (Bronze)"
        vlan_minimum: 35
        vlan_maximum: 40
      tags: create_vlan_range

    - name: Create a VLAN with a single value
      dellemc.openmanage.ome_network_vlan:
        hostname: "{{hostname}}"
        username: "{{username}}"
        password: "{{password}}"
        ca_path: "/path/to/ca_cert.pem"
        state: present
        name: "vlan2"
        description: "VLAN desc"
        type: "General Purpose (Bronze)"
        vlan_minimum: 127
        vlan_maximum: 127
      tags: create_vlan_single

    - name: Modify a VLAN
      dellemc.openmanage.ome_network_vlan:
        hostname: "{{hostname}}"
        username: "{{username}}"
        password: "{{password}}"
        ca_path: "/path/to/ca_cert.pem"
        state: present
        name: "vlan1"
        new_name: "vlan_gold1"
        description: "new description"
        type: "General Purpose (Gold)"
        vlan_minimum: 45
        vlan_maximum: 50
      tags: modify_vlan

    - name: Delete a VLAN
      dellemc.openmanage.ome_network_vlan:
        hostname: "{{hostname}}"
        username: "{{username}}"
        password: "{{password}}"
        ca_path: "/path/to/ca_cert.pem"
        state: "absent"
        name: "vlan1"
      tags: delete_vlan



Return Values
-------------

msg (always, str, Successfully created the VLAN.)
  Overall status of the VLAN operation.


vlan_status (when I(state=present), dict, {'@odata.context': '/api/$metadata#NetworkConfigurationService.Network', '@odata.type': '#NetworkConfigurationService.Network', '@odata.id': '/api/NetworkConfigurationService/Networks(1234)', 'Id': 1234, 'Name': 'vlan1', 'Description': 'VLAN description', 'VlanMaximum': 130, 'VlanMinimum': 140, 'Type': 1, 'CreatedBy': 'admin', 'CreationTime': '2020-01-01 05:54:36.113', 'UpdatedBy': None, 'UpdatedTime': '2020-01-01 05:54:36.113', 'InternalRefNWUUId': '6d6effcc-eca4-44bd-be07-1234ab5cd67e'})
  Details of the VLAN that is either created or modified.


error_info (on HTTP error, dict, {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'CTEM1043', 'RelatedProperties': [], 'Message': 'Unable to create or update the network because the entered VLAN minimum 0 is not within a valid range ( 1  -  4000  or  4021  -  4094 ).', 'MessageArgs': ['0', '1', '4000', '4021', '4094'], 'Severity': 'Warning', 'Resolution': 'Enter a valid VLAN minimum as identified in the message and retry the operation.'}]})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

