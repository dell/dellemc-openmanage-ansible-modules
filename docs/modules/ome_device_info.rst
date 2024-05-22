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

- python \>= 3.9.6



Parameters
----------

  fact_subset (optional, str, basic_inventory)
    \ :literal:`basic\_inventory`\  returns the list of the devices.

    \ :literal:`detailed\_inventory`\  returns the inventory details of specified devices.

    \ :literal:`subsystem\_health`\  returns the health status of specified devices.


  system_query_options (optional, dict, None)
    \ :emphasis:`system\_query\_options`\  applicable for the choices of the fact\_subset. Either \ :emphasis:`device\_id`\  or \ :emphasis:`device\_service\_tag`\  is mandatory for \ :literal:`detailed\_inventory`\  and \ :literal:`subsystem\_health`\  or both can be applicable.


    device_id (optional, list, None)
      A list of unique identifier is applicable for \ :literal:`detailed\_inventory`\  and \ :literal:`subsystem\_health`\ .


    device_service_tag (optional, list, None)
      A list of service tags are applicable for \ :literal:`detailed\_inventory`\  and \ :literal:`subsystem\_health`\ .


    inventory_type (optional, str, None)
      For \ :literal:`detailed\_inventory`\ , it returns details of the specified inventory type.


    filter (optional, str, None)
      For \ :literal:`basic\_inventory`\ , it filters the collection of devices. \ :emphasis:`filter`\  query format should be aligned with OData standards.



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
    - name: Retrieve basic inventory of all devices
      dellemc.openmanage.ome_device_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"

    - name: Retrieve basic inventory for devices identified by IDs 33333 or 11111 using filtering
      dellemc.openmanage.ome_device_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        fact_subset: "basic_inventory"
        system_query_options:
          filter: "Id eq 33333 or Id eq 11111"

    - name: Retrieve inventory details of specified devices identified by IDs 11111 and 22222
      dellemc.openmanage.ome_device_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
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
        ca_path: "/path/to/ca_cert.pem"
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
        ca_path: "/path/to/ca_cert.pem"
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
        ca_path: "/path/to/ca_cert.pem"
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

- Sajna Shetty (@Sajna-Shetty)
- Felix Stephen (@felixs88)

