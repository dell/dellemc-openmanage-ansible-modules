# idrac_attributes

Role to configure the iDRAC system, manager and lifecycle attributes for Dell PowerEdge servers.

## Requirements

### Development
Requirements to develop and contribute to the role.
```
ansible
docker
molecule
python
```
### Production
Requirements to use the role.
```
ansible
python
```

### Ansible collections
Collections required to use the role
```
dellemc.openmanage
```

## Role Variables

<table>
<thead>
  <tr>
    <th>Name</th>
    <th>Required</th>
    <th>Default Value</th>
    <th>Choices</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>hostname</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- iDRAC IP Address or hostname.</td>
  </tr>
  <tr>
    <td>username</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- iDRAC username with admin privileges</td>
  </tr>
  <tr>
    <td>password</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- iDRAC user password.</td>
  </tr>
  <tr>
    <td>https_port</td>
    <td>false</td>
    <td>443</td>
    <td></td>
    <td>int</td>
    <td>- iDRAC port.</td>
  </tr>
  <tr>
    <td>validate_certs</td>
    <td>false</td>
    <td>true</td>
    <td></td>
    <td>bool</td>
    <td>- If C(false), the SSL certificates will not be validated.<br>- Configure C(false) only on personally controlled sites where self-signed certificates are used.</td>
  </tr>
  <tr>
    <td>ca_path</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>path</td>
    <td>- The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.</td>
  </tr>
  <tr>
    <td>https_timeout</td>
    <td>false</td>
    <td>30</td>
    <td></td>
    <td>int</td>
    <td>- The HTTPS socket level timeout in seconds.</td>
  </tr>
  <tr>
    <td>idrac_attributes</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>dict</td>
    <td>- Dictionary of iDRAC attributes and value. The attributes should be part of the Integrated Dell Remote Access Controller Attribute Registry.<br>- To view the list of attributes in Attribute Registry for iDRAC9 and above, use the Role idrac_gather_facts with idrac components.<br>- For iDRAC8 based servers, derive the manager attribute name from Server Configuration Profile.<br>- If the manager attribute name in Server Configuration Profile is <GroupName><Instance>#<AttributeName>(for Example, 'SNMP.1#AgentCommunity') then the equivalent attribute name for Redfish is <GroupName>.<Instance>.<AttributeName> (for Example, 'SNMP.1.AgentCommunity').</td>
  </tr>
  <tr>
    <td>system_attributes</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>dict</td>
    <td>- Dictionary of System attributes and value. The attributes should be part of the Integrated Dell Remote Access Controller Attribute Registry.<br>- To view the list of attributes in Attribute Registry for iDRAC9 and above, use the Role idrac_gather_facts with idrac components.<br>- For iDRAC8 based servers, derive the manager attribute name from Server Configuration Profile.<br>- If the manager attribute name in Server Configuration Profile is <GroupName><Instance>#<AttributeName> for Example, 'ThermalSettings.1#ThermalProfile') then the equivalent attribute name for Redfish is <GroupName>.<Instance>.<AttributeName> (for Example, 'ThermalSettings.1.ThermalProfile').</td>
  </tr>
  <tr>
    <td>lifecycle_controller_attributes</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>dict</td>
    <td>- Dictionary of Lifecycle Controller attributes and value. The attributes should be part of the Integrated Dell Remote Access Controller Attribute Registry.<br>- To view the list of attributes in Attribute Registry for iDRAC9 and above, use the Role idrac_gather_facts with idrac components.<br>- For iDRAC8 based servers, derive the manager attribute name from Server Configuration Profile.<br>- If the manager attribute name in Server Configuration Profile is <GroupName>.<Instance>#<AttributeName>(for Example, 'LCAttributes.1#AutoUpdate') then the equivalent attribute name for Redfish is <GroupName>.<Instance>.<AttributeName>(for Example, 'LCAttributes.1.AutoUpdate')</td>
  <tr>
    <td>manager_id</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Redfish ID of the resource. If the Redfish ID of the resource is not specified, then the first ID from the Manager IDs list will be picked up.</td>
  </tr>
</tbody>
</table>

## Fact variables

<table>
<thead>
  <tr>
    <th>Name</th>
    <th>Sample</th>
    <th>Description</th>
  </tr>
</thead>
  <tbody>
    <tr>
      <td>idrac_attributes_out</td>
      <td>{"changed": true,
        "failed": false,
        "msg": "Successfully updated the attributes."
}</td>
<td>Module output of idrac attributes</td>
</tbody>
</table>

## Examples 
-----

```
- name: Configure iDRAC attributes
   ansible.builtin.include_role:
    name:  idrac_attributes
   vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    idrac_attributes:
      SNMP.1.AgentCommunity: public
 
- name: Configure System attributes
   ansible.builtin.include_role:
    name:  idrac_attributes
   vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    system_attributes:
      ThermalSettings.1.ThermalProfile: Sound Cap
 
- name: Configure Lifecycle Controller attributes
   ansible.builtin.include_role:
    name:  idrac_attributes
   vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    lifecycle_controller_attributes:
      LCAttributes.1.AutoUpdate: Enabled
 
- name: Configure the iDRAC attributes for email alert settings.
   ansible.builtin.include_role:
    name:  idrac_attributes
   vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    idrac_attributes:
      EmailAlert.1.CustomMsg: Display Message
      EmailAlert.1.Enable: Enabled
      EmailAlert.1.Address: test@test.com
 
- name: Configure the iDRAC attributes for SNMP alert settings.
   ansible.builtin.include_role:
    name:  idrac_attributes
   vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    idrac_attributes:
      SNMPAlert.1.Destination: 192.168.0.2
      SNMPAlert.1.State: Enabled
      SNMPAlert.1.SNMPv3Username: username
 
- name: Configure the iDRAC attributes for SMTP alert settings.
   ansible.builtin.include_role:
    name:  idrac_attributes
   vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    idrac_attributes:
      RemoteHosts.1.SMTPServerIPAddress: 192.168.0.3
      RemoteHosts.1.SMTPAuthentication: Enabled
      RemoteHosts.1.SMTPPort: 25
      RemoteHosts.1.SMTPUserName: username
      RemoteHosts.1.SMTPPassword: password
 
- name: Configure the iDRAC attributes for webserver settings.
   ansible.builtin.include_role:
    name:  idrac_attributes
   vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    idrac_attributes:
      WebServer.1.SSLEncryptionBitLength: 128-Bit or higher
      WebServer.1.TLSProtocol: TLS 1.1 and Higher
 
- name: Configure the iDRAC attributes for SNMP settings.
   ansible.builtin.include_role:
    name:  idrac_attributes
   vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    idrac_attributes:
      SNMP.1.SNMPProtocol: All
      SNMP.1.AgentEnable: Enabled
      SNMP.1.TrapFormat: SNMPv1
      SNMP.1.AlertPort: 162
      SNMP.1.AgentCommunity: public
 
- name: Configure the iDRAC LC attributes for collecting system inventory.
   ansible.builtin.include_role:
    name:  idrac_attributes
   vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    lifecycle_controller_attributes:
      LCAttributes.1.CollectSystemInventoryOnRestart: Enabled
 
- name: Configure the iDRAC system attributes for LCD configuration.
   ansible.builtin.include_role:
    name:  idrac_attributes
   vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    system_attributes:
      LCD.1.Configuration: Service Tag
      LCD.1.vConsoleIndication: Enabled
      LCD.1.FrontPanelLocking: Full-Access
      LCD.1.UserDefinedString: custom string
 
- name: Configure the iDRAC attributes for Timezone settings.
   ansible.builtin.include_role:
    name:  idrac_attributes
   vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    idrac_attributes:
      Time.1.Timezone: CST6CDT
      NTPConfigGroup.1.NTPEnable: Enabled
      NTPConfigGroup.1.NTP1: 192.168.0.5
      NTPConfigGroup.1.NTP2: 192.168.0.6
      NTPConfigGroup.1.NTP3: 192.168.0.7
 
- name: Configure all attributes
   ansible.builtin.include_role:
    name:  idrac_attributes
   vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    idrac_attributes:
      SNMP.1.AgentCommunity: test
      SNMP.1.AgentEnable: Enabled
      SNMP.1.DiscoveryPort: 161
    system_attributes:
      ServerOS.1.HostName: demohostname
    lifecycle_controller_attributes:
      LCAttributes.1.AutoUpdate: Disabled
```

## Author Information
------------------

Dell Technologies <br>
Kritika Bhateja (Kritika.Bhateja@Dell.com)  2023