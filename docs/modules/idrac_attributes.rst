.. _idrac_attributes_module:


idrac_attributes -- Configure the iDRAC attributes.
===================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to configure the iDRAC attributes.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  idrac_attributes (optional, dict, None)
    Dictionary of iDRAC attributes and value. The attributes should be part of the Integrated Dell Remote Access Controller Attribute Registry. To view the list of attributes in Attribute Registry for iDRAC9 and above, see, \ `https://I(idrac\_ip <https://I(idrac_ip>`__\ /redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/iDRAC.Embedded.1) and \ `https://I(idrac\_ip <https://I(idrac_ip>`__\ /redfish/v1/Registries/ManagerAttributeRegistry).

    For iDRAC8 based servers, derive the manager attribute name from Server Configuration Profile. If the manager attribute name in Server Configuration Profile is \<GroupName\>.\<Instance\>#\<AttributeName\> (for Example, 'SNMP.1#AgentCommunity') then the equivalent attribute name for Redfish is \<GroupName\>.\<Instance\>.\<AttributeName\> (for Example, 'SNMP.1.AgentCommunity').


  system_attributes (optional, dict, None)
    Dictionary of System attributes and value. The attributes should be part of the Integrated Dell Remote Access Controller Attribute Registry. To view the list of attributes in Attribute Registry for iDRAC9 and above, see, \ `https://I(idrac\_ip <https://I(idrac_ip>`__\ /redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/System.Embedded.1) and \ `https://I(idrac\_ip <https://I(idrac_ip>`__\ /redfish/v1/Registries/ManagerAttributeRegistry).

    For iDRAC8 based servers, derive the manager attribute name from Server Configuration Profile. If the manager attribute name in Server Configuration Profile is \<GroupName\>.\<Instance\>#\<AttributeName\> (for Example, 'ThermalSettings.1#ThermalProfile') then the equivalent attribute name for Redfish is \<GroupName\>.\<Instance\>.\<AttributeName\> (for Example, 'ThermalSettings.1.ThermalProfile').


  lifecycle_controller_attributes (optional, dict, None)
    Dictionary of Lifecycle Controller attributes and value. The attributes should be part of the Integrated Dell Remote Access Controller Attribute Registry.To view the list of attributes in Attribute Registry for iDRAC9 and above, see, \ `https://I(idrac\_ip <https://I(idrac_ip>`__\ /redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/LifecycleController.Embedded.1) and \ `https://I(idrac\_ip <https://I(idrac_ip>`__\ /redfish/v1/Registries/ManagerAttributeRegistry).

    For iDRAC8 based servers, derive the manager attribute name from Server Configuration Profile. If the manager attribute name in Server Configuration Profile is \<GroupName\>.\<Instance\>#\<AttributeName\> (for Example, 'LCAttributes.1#AutoUpdate') then the equivalent attribute name for Redfish is \<GroupName\>.\<Instance\>.\<AttributeName\> (for Example, 'LCAttributes.1.AutoUpdate').


  resource_id (optional, str, None)
    Redfish ID of the resource.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (False, str, None)
    iDRAC username.

    If the username is not provided, then the environment variable :envvar:`IDRAC\_USERNAME` is used.

    Example: export IDRAC\_USERNAME=username


  idrac_password (False, str, None)
    iDRAC user password.

    If the password is not provided, then the environment variable :envvar:`IDRAC\_PASSWORD` is used.

    Example: export IDRAC\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable :envvar:`IDRAC\_X\_AUTH\_TOKEN` is used.

    Example: export IDRAC\_X\_AUTH\_TOKEN=x\_auth\_token


  idrac_port (optional, int, 443)
    iDRAC port.


  validate_certs (optional, bool, True)
    If :literal:`false`\ , the SSL certificates will not be validated.

    Configure :literal:`false` only on personally controlled sites where self-signed certificates are used.

    Prior to collection version :literal:`5.0.0`\ , the :emphasis:`validate\_certs` is :literal:`false` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports :literal:`check\_mode`.
   - For iDRAC8 based servers, the value provided for the attributes are not be validated. Ensure appropriate values are passed.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Configure iDRAC attributes
      dellemc.openmanage.idrac_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        idrac_attributes:
          SNMP.1.AgentCommunity: public

    - name: Configure System attributes
      dellemc.openmanage.idrac_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        system_attributes:
          ThermalSettings.1.ThermalProfile: Sound Cap

    - name: Configure Lifecycle Controller attributes
      dellemc.openmanage.idrac_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        lifecycle_controller_attributes:
          LCAttributes.1.AutoUpdate: Enabled

    - name: Configure the iDRAC attributes for email alert settings.
      dellemc.openmanage.idrac_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        idrac_attributes:
          EmailAlert.1.CustomMsg: Display Message
          EmailAlert.1.Enable: Enabled
          EmailAlert.1.Address: test@test.com

    - name: Configure the iDRAC attributes for SNMP alert settings.
      dellemc.openmanage.idrac_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        idrac_attributes:
          SNMPAlert.1.Destination: 192.168.0.2
          SNMPAlert.1.State: Enabled
          SNMPAlert.1.SNMPv3Username: username

    - name: Configure the iDRAC attributes for SMTP alert settings.
      dellemc.openmanage.idrac_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        idrac_attributes:
          RemoteHosts.1.SMTPServerIPAddress: 192.168.0.3
          RemoteHosts.1.SMTPAuthentication: Enabled
          RemoteHosts.1.SMTPPort: 25
          RemoteHosts.1.SMTPUserName: username
          RemoteHosts.1.SMTPPassword: password

    - name: Configure the iDRAC attributes for webserver settings.
      dellemc.openmanage.idrac_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        idrac_attributes:
          WebServer.1.SSLEncryptionBitLength: 128-Bit or higher
          WebServer.1.TLSProtocol: TLS 1.1 and Higher

    - name: Configure the iDRAC attributes for SNMP settings.
      dellemc.openmanage.idrac_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        idrac_attributes:
          SNMP.1.SNMPProtocol: All
          SNMP.1.AgentEnable: Enabled
          SNMP.1.TrapFormat: SNMPv1
          SNMP.1.AlertPort: 162
          SNMP.1.AgentCommunity: public

    - name: Configure the iDRAC LC attributes for collecting system inventory.
      dellemc.openmanage.idrac_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        lifecycle_controller_attributes:
          LCAttributes.1.CollectSystemInventoryOnRestart: Enabled

    - name: Configure the iDRAC system attributes for LCD configuration.
      dellemc.openmanage.idrac_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        system_attributes:
          LCD.1.Configuration: Service Tag
          LCD.1.vConsoleIndication: Enabled
          LCD.1.FrontPanelLocking: Full-Access
          LCD.1.UserDefinedString: custom string

    - name: Configure the iDRAC attributes for Timezone settings.
      dellemc.openmanage.idrac_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        idrac_attributes:
          Time.1.Timezone: CST6CDT
          NTPConfigGroup.1.NTPEnable: Enabled
          NTPConfigGroup.1.NTP1: 192.168.0.5
          NTPConfigGroup.1.NTP2: 192.168.0.6
          NTPConfigGroup.1.NTP3: 192.168.0.7

    - name: Configure all attributes
      dellemc.openmanage.idrac_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        idrac_attributes:
          SNMP.1.AgentCommunity: test
          SNMP.1.AgentEnable: Enabled
          SNMP.1.DiscoveryPort: 161
        system_attributes:
          ServerOS.1.HostName: demohostname
        lifecycle_controller_attributes:
          LCAttributes.1.AutoUpdate: Disabled

    - name: Enable idrac basic syslog
      dellemc.openmanage.idrac_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        idrac_attributes:
          SysLog.1.SysLogEnable: Enabled
          SysLog.1.Server1: 192.168.0.2
          SysLog.1.Server2: 192.168.0.3
          SysLog.1.Server3: 192.168.0.4
          SysLog.1.Port: 514

    - name: Disable idrac basic syslog
      dellemc.openmanage.idrac_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        idrac_attributes:
          SysLog.1.SysLogEnable: Disabled

    - name: Enable idrac secure syslog
      dellemc.openmanage.idrac_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        idrac_attributes:
          SysLog.1.securesyslogenable: Enabled
          SysLog.1.secureserver1: 192.168.0.2
          SysLog.1.secureport: 6511
          SysLog.1.secureclientauth: Anonymous

    - name: Disable idrac secure syslog
      dellemc.openmanage.idrac_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        idrac_attributes:
          SysLog.1.securesyslogenable: Disabled



Return Values
-------------

msg (always, str, Successfully updated the attributes.)
  Status of the attribute update operation.


invalid_attributes (on invalid attributes or values., dict, {'LCAttributes.1.AutoUpdate': 'Invalid value for Enumeration.', 'LCAttributes.1.StorageHealthRollupStatus': 'Read only Attribute cannot be modified.', 'SNMP.1.AlertPort': 'Not a valid integer.', 'SNMP.1.AlertPorty': 'Attribute does not exist.', 'SysLog.1.PowerLogInterval': 'Integer out of valid range.', 'ThermalSettings.1.AirExhaustTemp': 'Invalid value for Enumeration.'})
  Dict of invalid attributes provided.


error_info (when attribute value is invalid., dict, {'error': {'@Message.ExtendedInfo': [{'Message': "The value 'false' for the property LCAttributes.1.BIOSRTDRequested is of a different type than the property can accept.", 'MessageArgs': ['false', 'LCAttributes.1.BIOSRTDRequested'], 'MessageArgs@odata.count': 2, 'MessageId': 'Base.1.12.PropertyValueTypeError', 'RelatedProperties': ['#/Attributes/LCAttributes.1.BIOSRTDRequested'], 'RelatedProperties@odata.count': 1, 'Resolution': 'Correct the value for the property in the request body and resubmit the request if the operation failed.', 'Severity': 'Warning'}], 'code': 'Base.1.12.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information'}})
  Error information of the operation.





Status
------





Authors
~~~~~~~

- Husniya Abdul Hameed (@husniya-hameed)
- Felix Stephen (@felixs88)

