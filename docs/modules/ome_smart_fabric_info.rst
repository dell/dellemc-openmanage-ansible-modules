.. _ome_smart_fabric_info_module:


ome_smart_fabric_info -- Retrieves the information of smart fabrics inventoried by OpenManage Enterprise Modular
================================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves the list of smart fabrics in the inventory of OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  fabric_id (optional, str, None)
    Unique Id of the fabric.

    \ :emphasis:`fabric\_id`\  is mutually exclusive with \ :emphasis:`fabric\_name`\ .


  fabric_name (optional, str, None)
    Name of the fabric.

    \ :emphasis:`fabric\_name`\  is mutually exclusive with \ :emphasis:`fabric\_id`\ .


  hostname (True, str, None)
    OpenManage Enterprise Modular IP address or hostname.


  username (False, str, None)
    OpenManage Enterprise Modular username.

    If the username is not provided, then the environment variable \ :envvar:`OME\_USERNAME`\  is used.

    Example: export OME\_USERNAME=username


  password (False, str, None)
    OpenManage Enterprise Modular password.

    If the password is not provided, then the environment variable \ :envvar:`OME\_PASSWORD`\  is used.

    Example: export OME\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`OME\_X\_AUTH\_TOKEN`\  is used.

    Example: export OME\_X\_AUTH\_TOKEN=x\_auth\_token


  port (optional, int, 443)
    OpenManage Enterprise Modular HTTPS port.


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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise Modular.
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Retrieve details of all smart fabrics
      dellemc.openmanage.ome_smart_fabric_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"

    - name: Retrieve details of a specific smart fabric identified by its fabric ID
      dellemc.openmanage.ome_smart_fabric_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        fabric_id: "61c20a59-9ed5-4ae5-b850-5e5acf42d2f2"

    - name: Retrieve details of a specific smart fabric identified by its fabric name
      dellemc.openmanage.ome_smart_fabric_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        fabric_name: "f1"



Return Values
-------------

msg (always, str, Successfully retrieved the smart fabric information.)
  Status of smart fabric information retrieval.


smart_fabric_info (success, list, [{'Description': 'Fabric f1', 'FabricDesign': [{'Actions': {'#NetworkService.GetApplicableNodes': {'target': "/api/NetworkService/Fabrics('61c20a59-9ed5-4ae5-b850-5e5acf42d2f2')/FabricDesign/NetworkService.GetApplicableNodes"}, 'Oem': {}}, 'FabricDesignNode': [{'ChassisName': 'Chassis-X', 'NodeName': 'Switch-B', 'Slot': 'Slot-A2', 'Type': 'WeaverSwitch'}, {'ChassisName': 'Chassis-X', 'NodeName': 'Switch-A', 'Slot': 'Slot-A1', 'Type': 'WeaverSwitch'}], 'Name': '2xMX9116n_Fabric_Switching_Engines_in_same_chassis', 'NetworkLink': [{'DestinationInterface': 'ethernet1/1/38', 'DestinationNode': 'Switch-B', 'SourceInterface': 'ethernet1/1/38', 'SourceNode': 'Switch-A'}, {'DestinationInterface': 'ethernet1/1/37', 'DestinationNode': 'Switch-B', 'SourceInterface': 'ethernet1/1/37', 'SourceNode': 'Switch-A'}, {'DestinationInterface': 'ethernet1/1/39', 'DestinationNode': 'Switch-B', 'SourceInterface': 'ethernet1/1/39', 'SourceNode': 'Switch-A'}, {'DestinationInterface': 'ethernet1/1/40', 'DestinationNode': 'Switch-B', 'SourceInterface': 'ethernet1/1/40', 'SourceNode': 'Switch-A'}]}], 'FabricDesignMapping': [{'DesignNode': 'Switch-A', 'PhysicalNode': 'NODEID1'}, {'DesignNode': 'Switch-B', 'PhysicalNode': 'NODEID2'}], 'Health': {'Issues': [{'Category': 'Audit', 'DetailedDescription': 'The SmartFabric is not healthy because the interface for an uplink mentioned in the message is not in operational status.', 'Message': 'The SmartFabric is not healthy because the interface JRWSV43:ethernet1/1/35 for uplink 1ad54420-b145-49a1-9779-21a579ef6f2d is not in operational status.', 'MessageArgs': [], 'MessageId': 'NFAB0016', 'Resolution': 'Make sure that all the uplink interfaces are in operational status.', 'Severity': 'Warning', 'TimeStamp': '2019-09-25T11:50:06Z'}, {'Category': 'Audit', 'DetailedDescription': 'The SmartFabric is not healthy because one or more VLTi links are not connected.', 'Message': 'The SmartFabric is not healthy because all InterSwitch Links are not connected.', 'MessageArgs': [], 'MessageId': 'NFAB0017', 'Resolution': 'Make sure that the VLTi cables for all ISLs are connected and operational as per the selected fabric design.', 'Severity': 'Warning', 'TimeStamp': '2019-09-25T11:50:06Z'}, {'Category': 'Audit', 'DetailedDescription': 'The SmartFabric is not healthy because the interface for an uplink mentioned in the message is not in operational status.', 'Message': 'The SmartFabric is not healthy because the interface 6H7J6Z2:ethernet1/1/35 for uplink 1ad54420-b145-49a1-9779-21a579ef6f2d is not in operational status.', 'MessageArgs': [], 'MessageId': 'NFAB0016', 'Resolution': 'Make sure that all the uplink interfaces are in operational status.', 'Severity': 'Warning', 'TimeStamp': '2019-09-25T11:50:06Z'}, {'Category': 'Audit', 'DetailedDescription': 'The SmartFabric is not healthy because one or more of the uplink interfaces are not bonded.', 'Message': 'The SmartFabric is not healthy because the uplink 1ad54420-b145-49a1-9779-21a579ef6f2d interface 6H7J6Z2:ethernet1/1/35 is not bonded to the other interfaces in the uplink.', 'MessageArgs': [], 'MessageId': 'NFAB0019', 'Resolution': 'Make sure that the Link Aggregation Control Protocol (LACP) is enabled on all ports on the remote switch to which the uplink ports from the fabric are connected.', 'Severity': 'Warning', 'TimeStamp': '2019-09-25T11:50:06Z'}, {'Category': 'Audit', 'DetailedDescription': 'The SmartFabric is not healthy because one or more of the uplink interfaces are not bonded.', 'Message': 'The SmartFabric is not healthy because the uplink 1ad54420-b145-49a1-9779-21a579ef6f2d interface JRWSV43:ethernet1/1/35 is not bonded to the other interfaces in the uplink.', 'MessageArgs': [], 'MessageId': 'NFAB0019', 'Resolution': 'Make sure that the Link Aggregation Control Protocol (LACP) is enabled on all ports on the remote switch to which the uplink ports from the fabric are connected.', 'Severity': 'Warning', 'TimeStamp': '2019-09-25T11:50:06Z'}], 'Status': '4000'}, 'Id': '61c20a59-9ed5-4ae5-b850-5e5acf42d2f2', 'LifeCycleStatus': [{'Activity': 'Create', 'Status': '2060'}], 'Multicast': [{'FloodRestrict': True, 'IgmpVersion': '3', 'MldVersion': '2'}], 'Name': 'f1', 'OverrideLLDPConfiguration': 'Disabled', 'ScaleVLANProfile': 'Enabled', 'Servers': [{'ChassisServiceTag': '6H5S6Z2', 'ConnectionState': True, 'ConnectionStateReason': 101, 'DeviceCapabilities': [1, 2, 3, 4, 7, 8, 9, 41, 10, 11, 12, 13, 14, 15, 208, 16, 17, 18, 212, 30, 31], 'DeviceManagement': [{'DnsName': 'iDRAC-6GZK6Z2', 'InstrumentationName': '', 'MacAddress': '4c:d9:8f:7a:7c:43', 'ManagementId': 135185, 'ManagementProfile': [{'AgentName': 'iDRAC', 'HasCreds': 0, 'ManagementId': 135185, 'ManagementProfileId': 135185, 'ManagementURL': 'https://[2607:f2b1:f081:9:4ed9:8fff:fe7a:7c43]:443/', 'ProfileId': 'WSMAN_OOB', 'Status': 1000, 'StatusDateTime': '2019-10-29 09:30:38.552', 'Version': '3.20.21.20'}], 'ManagementType': 2, 'NetworkAddress': '100.96.24.28'}, {'DnsName': 'iDRAC-6GZK6Z2', 'InstrumentationName': '', 'MacAddress': '4c:d9:8f:7a:7c:43', 'ManagementId': 135186, 'ManagementProfile': [{'AgentName': 'iDRAC', 'HasCreds': 0, 'ManagementId': 135186, 'ManagementProfileId': 135186, 'ManagementURL': 'https://[2607:f2b1:f081:9:4ed9:8fff:fe7a:7c43]:443/', 'ProfileId': 'WSMAN_OOB', 'Status': 1000, 'StatusDateTime': '2019-10-29 09:30:38.552', 'Version': '3.20.21.20'}], 'ManagementType': 2, 'NetworkAddress': '[2607:f2b1:f081:9:4ed9:8fff:fe7a:7c43]'}], 'DeviceName': 'MX-6H5S6Z2:Sled-1', 'DeviceServiceTag': '6GZK6Z2', 'Enabled': True, 'Id': 10071, 'Identifier': '6GZK6Z2', 'LastInventoryTime': '2019-10-29 09:30:38.552', 'LastStatusTime': '2019-10-29 09:41:51.051', 'ManagedState': 3000, 'Model': 'PowerEdge MX840c', 'PowerState': 17, 'SlotConfiguration': {'ChassisId': '10072', 'ChassisName': 'MX-6H5S6Z2', 'ChassisServiceTag': '6H5S6Z2', 'DeviceType': '1000', 'SledBlockPowerOn': 'None blocking', 'SlotId': '10084', 'SlotName': 'Sled-1', 'SlotNumber': '1', 'SlotType': '2000'}, 'Status': 1000, 'SystemId': 1894, 'Type': 1000}], 'Summary': {'NodeCount': 2, 'ServerCount': 1, 'UplinkCount': 1}, 'Switches': [{'ChassisServiceTag': '6H5S6Z2', 'ConnectionState': True, 'ConnectionStateReason': 101, 'DeviceCapabilities': [1, 2, 3, 5, 7, 8, 9, 207, 18, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622], 'DeviceManagement': [{'DnsName': '', 'InstrumentationName': 'MX9116n Fabric Engine', 'MacAddress': '20:04:0F:4F:4E:04', 'ManagementId': 135181, 'ManagementProfile': [{'HasCreds': 0, 'ManagementId': 135181, 'ManagementProfileId': 135181, 'ManagementURL': '', 'ProfileId': '', 'Status': 1000, 'StatusDateTime': '2019-10-29 09:30:36.273'}], 'ManagementType': 2, 'NetworkAddress': '100.96.24.36'}, {'DnsName': '', 'InstrumentationName': 'MX9116n Fabric Engine', 'MacAddress': '20:04:0F:4F:4E:04', 'ManagementId': 135182, 'ManagementProfile': [{'HasCreds': 0, 'ManagementId': 135182, 'ManagementProfileId': 135182, 'ManagementURL': '', 'ProfileId': '', 'Status': 1000, 'StatusDateTime': '2019-10-29 09:30:36.273'}], 'ManagementType': 2, 'NetworkAddress': ''}], 'DeviceName': 'MX-6H5S6Z2:IOM-A2', 'DeviceServiceTag': '6H7J6Z2', 'Enabled': True, 'Id': 10074, 'Identifier': '6H7J6Z2', 'LastInventoryTime': '2019-10-29 09:30:36.332', 'LastStatusTime': '2019-10-29 09:31:00.931', 'ManagedState': 3000, 'Model': 'MX9116n Fabric Engine', 'PowerState': 17, 'SlotConfiguration': {'ChassisId': '10072', 'ChassisName': 'MX-6H5S6Z2', 'ChassisServiceTag': '6H5S6Z2', 'DeviceType': '4000', 'SledBlockPowerOn': 'null', 'SlotId': '10079', 'SlotName': 'IOM-A2', 'SlotNumber': '2', 'SlotType': '4000'}, 'Status': 1000, 'SystemId': 2031, 'Type': 4000}, {'ChassisServiceTag': '6H5S6Z2', 'ConnectionState': True, 'ConnectionStateReason': 101, 'DeviceCapabilities': [1, 2, 3, 5, 7, 8, 9, 207, 18, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622], 'DeviceManagement': [{'DnsName': '', 'InstrumentationName': 'MX9116n Fabric Engine', 'MacAddress': 'E8:B5:D0:52:61:46', 'ManagementId': 135183, 'ManagementProfile': [{'HasCreds': 0, 'ManagementId': 135183, 'ManagementProfileId': 135183, 'ManagementURL': '', 'ProfileId': '', 'Status': 1000, 'StatusDateTime': '2019-10-29 09:30:37.115'}], 'ManagementType': 2, 'NetworkAddress': '100.96.24.37'}, {'DnsName': '', 'InstrumentationName': 'MX9116n Fabric Engine', 'MacAddress': 'E8:B5:D0:52:61:46', 'ManagementId': 135184, 'ManagementProfile': [{'HasCreds': 0, 'ManagementId': 135184, 'ManagementProfileId': 135184, 'ManagementURL': '', 'ProfileId': '', 'Status': 1000, 'StatusDateTime': '2019-10-29 09:30:37.115'}], 'ManagementType': 2, 'NetworkAddress': ''}], 'DeviceName': 'MX-6H5S6Z2:IOM-A1', 'DeviceServiceTag': 'JRWSV43', 'Enabled': True, 'Id': 20881, 'Identifier': 'JRWSV43', 'LastInventoryTime': '2019-10-29 09:30:37.172', 'LastStatusTime': '2019-10-29 09:31:00.244', 'ManagedState': 3000, 'Model': 'MX9116n Fabric Engine', 'PowerState': 17, 'SlotConfiguration': {'ChassisId': '10072', 'ChassisName': 'MX-6H5S6Z2', 'ChassisServiceTag': '6H5S6Z2', 'DeviceType': '4000', 'SledBlockPowerOn': 'null', 'SlotId': '10078', 'SlotName': 'IOM-A1', 'SlotNumber': '1', 'SlotType': '4000'}, 'Status': 1000, 'SystemId': 2031, 'Type': 4000}], 'Uplinks': [{'Id': '1ad54420-b145-49a1-9779-21a579ef6f2d', 'MediaType': 'Ethernet', 'Name': 'u1', 'NativeVLAN': 1, 'Summary': {'NetworkCount': 1, 'PortCount': 2}, 'UfdEnable': 'Disabled'}]}])
  Returns the information about smart fabric.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'CGEN1006', 'RelatedProperties': [], 'Message': 'Unable to complete the request because the resource URI does not exist or is not implemented.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': "Check the request resource URI. Refer to the OpenManage Enterprise-Modular User's Guide for more information about resource URI and its properties."}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Kritika Bhateja(@Kritka-Bhateja)

