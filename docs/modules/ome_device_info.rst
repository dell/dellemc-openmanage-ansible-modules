.. _ome_device_info_module:


ome_device_info -- Retrieves the information of devices inventoried by OpenManage Enterprise
============================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves the list of devices in the inventory of OpenManage Enterprise along with the details of each device.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7.5



Parameters
----------

  fact_subset (optional, str, basic_inventory)
    ``basic_inventory`` returns the list of the devices.

    ``detailed_inventory`` returns the inventory details of specified devices.

    ``subsystem_health`` returns the health status of specified devices.


  system_query_options (optional, dict, None)
    *system_query_options* applicable for the choices of the fact_subset. Either *device_id* or *device_service_tag* is mandatory for ``detailed_inventory`` and ``subsystem_health`` or both can be applicable.


    device_id (optional, list, None)
      A list of unique identifier is applicable for ``detailed_inventory`` and ``subsystem_health``.


    device_service_tag (optional, list, None)
      A list of service tags are applicable for ``detailed_inventory`` and ``subsystem_health``.


    inventory_type (optional, str, None)
      For ``detailed_inventory``, it returns details of the specified inventory type.


    filter (optional, str, None)
      For ``basic_inventory``, it filters the collection of devices. *filter* query format should be aligned with OData standards.



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
    - name: Retrieve basic inventory of all devices
      dellemc.openmanage.ome_device_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"

    - name: Retrieve basic inventory for devices identified by IDs 33333 or 11111 using filtering
      dellemc.openmanage.ome_device_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        fact_subset: "basic_inventory"
        system_query_options:
          filter: "Id eq 33333 or Id eq 11111"

    - name: Retrieve inventory details of specified devices identified by IDs 11111 and 22222
      dellemc.openmanage.ome_device_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        fact_subset: "detailed_inventory"
        system_query_options:
          device_id:
            - 11111
            - 22222

    - name: Retrieve inventory details of specified devices identified by service tags MXL1234 and MXL4567
      dellemc.openmanage.ome_device_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        fact_subset: "detailed_inventory"
        system_query_options:
          device_service_tag:
            - MXL1234
            - MXL4567

    - name: Retrieve details of specified inventory type of specified devices identified by ID and service tags
      dellemc.openmanage.ome_device_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        fact_subset: "detailed_inventory"
        system_query_options:
          device_id:
            - 11111
          device_service_tag:
            - MXL1234
            - MXL4567
          inventory_type: "serverDeviceCards"

    - name: Retrieve subsystem health of specified devices identified by service tags
      dellemc.openmanage.ome_device_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        fact_subset: "subsystem_health"
        system_query_options:
          device_service_tag:
            - MXL1234
            - MXL4567




Return Values
-------------

msg (on error, str, Failed to fetch the device information)
  Over all device information status.


device_info (success, dict, {'value': [{'Actions': None, 'AssetTag': None, 'ChassisServiceTag': None, 'ConnectionState': True, 'DeviceManagement': [{'DnsName': 'dnsname.host.com', 'InstrumentationName': 'MX-12345', 'MacAddress': '11:10:11:10:11:10', 'ManagementId': 12345, 'ManagementProfile': [{'HasCreds': 0, 'ManagementId': 12345, 'ManagementProfileId': 12345, 'ManagementURL': 'https://192.168.0.1:443', 'Status': 1000, 'StatusDateTime': '2019-01-21 06:30:08.501'}], 'ManagementType': 2, 'NetworkAddress': '192.168.0.1'}], 'DeviceName': 'MX-0003I', 'DeviceServiceTag': 'MXL1234', 'DeviceSubscription': None, 'LastInventoryTime': '2019-01-21 06:30:08.501', 'LastStatusTime': '2019-01-21 06:30:02.492', 'ManagedState': 3000, 'Model': 'PowerEdge MX7000', 'PowerState': 17, 'SlotConfiguration': {}, 'Status': 4000, 'SystemId': 2031, 'Type': 2000}]})
  Returns the information collected from the Device.





Status
------





Authors
~~~~~~~

- Sajna Shetty(@Sajna-Shetty)

