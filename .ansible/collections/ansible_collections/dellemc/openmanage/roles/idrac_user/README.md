# idrac_user

Role to manage local users for iDRAC.

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
    <td>- IPv4, IPv6 Address or hostname of the iDRAC.</td>
  </tr>
  <tr>
    <td>username</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- iDRAC username with 'Administrator' privilege.</td>
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
    <td>state</td>
    <td>false</td>
    <td>present</td>
    <td>[present, absent]</td>
    <td>str</td>
    <td>- Select C(present) to create or modify a user account.</br>- Select C(absent) to remove a user account.</td>
  </tr>
  <tr>
    <td>user_name</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Provide username of the iDRAC user account that is created, deleted, or modified.</td>
  </tr>
  <tr>
    <td>user_password</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Provide password for the iDRAC user account that is created, or modified. The password can be changed when the user account is modified.</br>- To ensure security, the I(user_password) must be at least eight characters long and must contain
    lowercase and upper-case characters, numbers, and special characters.
</td>
  </tr>
  <tr>
    <td>new_user_name</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Provide the I(user_name) for the iDRAC user account that is modified.</td>
  </tr>
  <tr>
    <td>privilege</td>
    <td>false</td>
    <td></td>
    <td>["Administrator","ReadOnly","Operator","None"]</td>
    <td>str</td>
    <td>- Following are the role-based privileges.</br>- A user with C(Administrator) privilege can log in to iDRAC, and then configure iDRAC, configure users,clear logs, control and configure system, access virtual console, access virtual media, test alerts, and execute debug commands.
    </br>- A user with C(Operator) privilege can log in to iDRAC, and then configure iDRAC, control and configure system, access virtual console, access virtual media, and execute debug commands.</br>- A user with C(ReadOnly) privilege can only log in to iDRAC.</br>- A user with C(None), no privileges assigned.</br>- Will be ignored, if I(custom_privilege) parameter is provided.</td>
  </tr>
  </tr>
  <tr>
    <td>custom_privilege</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>int</td>
    <td>- Provide the custom role-based authority privileges allowed for the user.</br>- To create a custom privilege, add up the privilege decimal values as defined below.</br>Login - 1</br>Configure - 2</br>Configure Users - 4</br>Logs - 8</br>System Control - 16</br>Access Virtual Console - 32</br>Access Virtual Media - 64</br>System Operations - 128</br>Debug - 256</br>- The value has to be in the range 0-511.</td>
  </tr>
  <tr>
    <td>ipmi_lan_privilege</td>
    <td>false</td>
    <td></td>
    <td>["Administrator","ReadOnly","Operator","No Access"]</td>
    <td>str</td>
    <td>- The Intelligent Platform Management Interface LAN privilege level assigned to the user.</td>
  </tr>
  <tr>
    <td>ipmi_serial_privilege</td>
    <td>false</td>
    <td></td>
    <td>["Administrator","ReadOnly","Operator","No Access"]</td>
    <td>str</td>
    <td>- The Intelligent Platform Management Interface Serial Port privilege level assigned to the user.</br>- This option is only applicable for rack and tower servers.</td>
  </tr>
  <tr>
    <td>enable</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>bool</td>
    <td>Provide the option to enable or disable a user from logging in to iDRAC.</td>
  </tr>
   <tr>
    <td>sol_enable</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>bool</td>
    <td>Enables Serial Over Lan (SOL) for an iDRAC user.</td>
  </tr>
   <tr>
    <td>protocol_enable</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>bool</td>
    <td>Enables SNMPv3 protocol for the iDRAC user.</td>
  </tr>
  <tr>
    <td>authentication_protocol</td>
    <td>false</td>
    <td></td>
    <td>["None","SHA5","MD5"]</td>
    <td>str</td>
    <td>- This option allows to configure one of the following authentication protocol types to authenticate the iDRAC user.</br>- Secure Hash Algorithm C(SHA).</br>- Message Digest 5 C(MD5).</br>- If C(None) is selected, then the authentication protocol is not configured.</td>
  </tr>
  <tr>
    <td>privacy_protocol</td>
    <td>false</td>
    <td></td>
    <td>["None","DES","AES"]</td>
    <td>str</td>
    <td>- This option allows to configure one of the following privacy encryption protocols for the iDRAC user.</br>- Data Encryption Standard C(DES).</br>- Advanced Encryption Standard C(AES).</br>- If C(None) is selected, then the privacy protocol is not configured.</td>
  </tr>

  
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
      <td>idrac_user_out</td>
      <td>{"changed": true,
           "failed": false,
           "msg": "Successfully created user account details."
}</td>
<td>Output of the iDRAC user role</td>
</tr>
<tr>
  <td>idrac_user_account</td>
  <td>
  {"changed": true,
       "failed": false,
       {
    "AccountTypes": [
        "Redfish",
        "SNMP",
        "OEM",
        "HostConsole",
        "ManagerConsole",
        "IPMI",
        "KVMIP",
        "VirtualMedia",
        "WebUI"
    ],
    "Description": "User Account",
    "Enabled": true,
    "Id": "2",
    "Locked": false,
    "Name": "User Account",
    "OEMAccountTypes": [
        "IPMI",
        "SOL",
        "WSMAN",
        "UI",
        "RACADM"
    ],
    "Oem": {
        "Dell": {
            "SNMPv3PassphraseEnabled": "Disabled"
        }
    },
    "Password": null,
    "PasswordChangeRequired": false,
    "PasswordExpiration": null,
    "RoleId": "Administrator",
    "SNMP": {
        "AuthenticationKey": null,
        "AuthenticationKeySet": true,
        "AuthenticationProtocol": "HMAC_MD5",
        "EncryptionKey": null,
        "EncryptionKeySet": true,
        "EncryptionProtocol": "CBC_DES"
    },
    "StrictAccountTypes": false,
    "UserName": "root"
}"
}</td>
<td>Details of the iDRAC user account that is created or modified.</td>
</tr>
</tbody>
</table>

## Examples

---

```yml
- name: Configure a new iDRAC user
  ansible.builtin.import_role:
    name: idrac_user
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: present
    user_name: user_name
    user_password: user_password
    privilege: Administrator
    ipmi_lan_privilege: Administrator
    ipmi_serial_privilege: Administrator
    enable: true
    sol_enable: true
    protocol_enable: true
    authentication_protocol: SHA
    privacy_protocol: AES
```

```yml
- name: Modify username and password for the existing iDRAC user
  ansible.builtin.import_role:
    name: idrac_user
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password" 
    ca_path: "/path/to/ca_cert.pem"
    state: present
    user_name: user_name
    new_user_name: new_user_name
    user_password: user_password
```

```yml
-- name: Delete existing iDRAC user account   
  ansible.builtin.import_role:
    name: idrac_user
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"      
    ca_path: "/path/to/ca_cert.pem"
    state: absent
    user_name: user_name
```
## Author Information

---

Dell Technologies <br>
Kritika Bhateja (Kritika.Bhateja@Dell.com) 2024
