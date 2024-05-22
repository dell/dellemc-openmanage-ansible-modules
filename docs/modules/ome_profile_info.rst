.. _ome_profile_info_module:


ome_profile_info -- Retrieve profiles with attribute details
============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieve profiles with attributes on OpenManage Enterprise or OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  profile_id (optional, int, None)
    Id of the profile.

    This is mutually exclusive with \ :emphasis:`profile\_name`\ , \ :emphasis:`system\_query\_options`\ , \ :emphasis:`template\_id`\ , and \ :emphasis:`template\_name`\ .


  profile_name (optional, str, None)
    Name of the profile.

    This is mutually exclusive with \ :emphasis:`template\_id`\ , \ :emphasis:`profile\_id`\ , \ :emphasis:`system\_query\_options`\ , and \ :emphasis:`template\_name`\ .


  template_id (optional, int, None)
    Provide the ID of the template to retrieve the list of profile(s) linked to it.

    This is mutually exclusive with \ :emphasis:`profile\_name`\ , \ :emphasis:`profile\_id`\ , \ :emphasis:`system\_query\_options`\ , and \ :emphasis:`template\_name`\ .


  template_name (optional, str, None)
    Provide the name of the template to retrieve the list of profile(s) linked to it.

    This is mutually exclusive with \ :emphasis:`profile\_name`\ , \ :emphasis:`profile\_id`\ , \ :emphasis:`template\_id`\ , and \ :emphasis:`system\_query\_options`\ .


  system_query_options (optional, dict, None)
    Option for providing supported odata filters.

    The profile list can be fetched and sorted based on ProfileName, TemplateName, TargetTypeId, TargetName, ChassisName, ProfileState, LastRunStatus, or ProfileModified.

    This is mutually exclusive with \ :emphasis:`profile\_name`\ , \ :emphasis:`profile\_id`\ , \ :emphasis:`template\_id`\ , and \ :emphasis:`template\_name`\ .

    \ :literal:`Note`\  If \ :emphasis:`profile\_name`\ , \ :emphasis:`profile\_id`\ , \ :emphasis:`template\_id`\ , or \ :emphasis:`template\_name`\  option is not provided, the module retrieves all the profiles.


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
   - Run this module on a system that has direct access to Dell OpenManage Enterprise.
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Retrieve all profiles
      dellemc.openmanage.ome_profile_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"

    - name: Retrieve profile using the name
      dellemc.openmanage.ome_profile_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        profile_name: eprof 00001

    - name: Retrieve profile using the id
      dellemc.openmanage.ome_profile_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        profile_id: 10129

    - name: Retrieve the profiles using the template name
      dellemc.openmanage.ome_profile_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        template_name: t2

    - name: Retrieve the profiles using the template id
      dellemc.openmanage.ome_profile_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        template_id: 11

    - name: Retrieve the profiles based on the odata filters
      dellemc.openmanage.ome_profile_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        system_query_options:
          filter: TemplateName eq 'mytemplate'
          orderby: ProfileState



Return Values
-------------

msg (always, str, Successfully retrieved the profile information.)
  Status of profile information retrieval.


profile_info (success, list, [{'Id': 71460, 'ProfileName': 'Profile 00001', 'ProfileDescription': 'from source template: (Template)', 'TemplateId': 8, 'TemplateName': 'Template', 'DataSchemaId': 8, 'TargetId': 0, 'TargetName': None, 'TargetTypeId': 0, 'DeviceIdInSlot': 0, 'ChassisId': 0, 'ChassisName': None, 'GroupId': 0, 'GroupName': None, 'NetworkBootToIso': None, 'ProfileState': 0, 'DeploymentTaskId': 0, 'LastRunStatus': 2200, 'ProfileModified': 0, 'CreatedBy': 'admin', 'EditedBy': None, 'CreatedDate': '2019-09-26 13:56:41.924966', 'LastEditDate': '2020-12-11 08:27:20.500564', 'LastDeployDate': '', 'AttributeIdMap': {'4965': {'Value': 'hostname', 'IsReadOnly': False, 'IsIgnored': True}, '4963': {'Value': 'second floor', 'IsReadOnly': False, 'IsIgnored': True}, '4960': {'Value': '10A', 'IsReadOnly': False, 'IsIgnored': True}, '4959': {'Value': 'OMAMDEV', 'IsReadOnly': False, 'IsIgnored': True}, '4957': {'Value': 'Dell LAB', 'IsReadOnly': False, 'IsIgnored': True}, '4958': {'Value': None, 'IsReadOnly': False, 'IsIgnored': True}, '4066': {'Value': None, 'IsReadOnly': False, 'IsIgnored': True}, '4231': {'Value': '1', 'IsReadOnly': False, 'IsIgnored': False}, '4229': {'Value': 'Disabled', 'IsReadOnly': False, 'IsIgnored': False}}, 'AttributeDetails': {'System': {'Server Operating System': {'ServerOS 1 Server Host Name': 4965}, 'Server Topology': {'ServerTopology 1 Room Name': 4963, 'ServerTopology 1 Rack Slot': 4960, 'ServerTopology 1 Rack Name': 4959, 'ServerTopology 1 Data Center Name': 4957, 'ServerTopology 1 Aisle Name': 4958}}, 'iDRAC': {'Active Directory': {'ActiveDirectory 1 Active Directory RAC Name': 4066}, 'NIC Information': {'NIC 1 VLAN ID': 4231, 'NIC 1 Enable VLAN': 4229}}}}])
  Information about the profile.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

