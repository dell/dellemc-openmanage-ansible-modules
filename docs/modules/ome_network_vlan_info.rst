.. _ome_network_vlan_info_module:


ome_network_vlan_info -- Retrieves the information about networks VLAN(s) present in OpenManage Enterprise
==========================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to retrieve the following. - A list of all the network VLANs with their detailed information. - Information about a specific network VLAN using VLAN *id* or VLAN *name*.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7.5



Parameters
----------

  id (optional, int, None)
    A unique identifier of the network VLAN available in the device.

    *id* and *name* are mutually exclusive.


  name (optional, str, None)
    A unique name of the network VLAN available in the device.

    *name* and *id* are mutually exclusive.


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
    - name: Retrieve information about all network VLANs(s) available in the device
      dellemc.openmanage.ome_network_vlan_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"

    - name: Retrieve information about a network VLAN using the VLAN ID
      dellemc.openmanage.ome_network_vlan_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        id: 12345

    - name: Retrieve information about a network VLAN using the VLAN name
      dellemc.openmanage.ome_network_vlan_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        name: "Network VLAN - 1"



Return Values
-------------

msg (success, str, {'msg': 'Successfully retrieved the network VLAN information.', 'network_vlan_info': [{'CreatedBy': 'admin', 'CreationTime': '2020-09-02 18:48:42.129', 'Description': 'Description of Logical Network - 1', 'Id': 20057, 'InternalRefNWUUId': '42b9903d-93f8-4184-adcf-0772e4492f71', 'Name': 'Network VLAN - 1', 'Type': {'Description': 'This is the network for general purpose traffic. QOS Priority : Bronze.', 'Id': 1, 'Name': 'General Purpose (Bronze)', 'NetworkTrafficType': 'Ethernet', 'QosType': {'Id': 4, 'Name': 'Bronze'}, 'VendorCode': 'GeneralPurpose'}, 'UpdatedBy': None, 'UpdatedTime': '2020-09-02 18:48:42.129', 'VlanMaximum': 111, 'VlanMinimum': 111}, {'CreatedBy': 'admin', 'CreationTime': '2020-09-02 18:49:11.507', 'Description': 'Description of Logical Network - 2', 'Id': 20058, 'InternalRefNWUUId': 'e46ccb3f-ef57-4617-ac76-46c56594005c', 'Name': 'Network VLAN - 2', 'Type': {'Description': 'This is the network for general purpose traffic. QOS Priority : Silver.', 'Id': 2, 'Name': 'General Purpose (Silver)', 'NetworkTrafficType': 'Ethernet', 'QosType': {'Id': 3, 'Name': 'Silver'}, 'VendorCode': 'GeneralPurpose'}, 'UpdatedBy': None, 'UpdatedTime': '2020-09-02 18:49:11.507', 'VlanMaximum': 112, 'VlanMinimum': 112}]})
  Detailed information of the network VLAN(s).


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Deepak Joshi(@deepakjoshishri)

