# idrac_reset

Role to reset and restart iDRAC (iDRAC8 and iDRAC9 only) for Dell PowerEdge servers. 

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
    <td>- iDRAC IP Address</td>
  </tr>
  <tr>
    <td>username</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- iDRAC username</td>
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
    <td>wait_for_idrac</td>
    <td>false</td>
    <td>true</td>
    <td></td>
    <td>bool</td>
    <td>- Wait for the iDRAC to restart and LC status to be ready.<br>- When I(reset_to_default) is C(All), the IP address of iDRAC might not be accessible because of the change in network settings.<br>- When I(reset_to_default) is C(ResetAllWithRootDefaults), the IP address of iDRAC might not be accessible because of the change in network settings.</td>
  </tr>
  <tr>
    <td>force_reset</td>
    <td>false</td>
    <td>false</td>
    <td></td>
    <td>bool</td>
    <td>- Force restart the idrac without checking the idrac lifecycle controller status.</td>
  </tr>
  <tr>
  reset_to_default:
    <td>reset_to_default</td>
    <td>false</td>
    <td></td>
    <td>["All", "ResetAllWithRootDefaults", "Default"]</td>
    <td>str</td>
    <td>- Reset the iDRAC to factory default settings.<br>- If this value is not set, then the default behaviour is to restart the iDRAC.<br>- C(All)This action will reset your iDRAC to the factory defaults. SupportAssist settings including registration information will be permanently removed. Username and password will reset to default credentials.<br>- C(ResetAllWithRootDefaults)This action will reset your iDRAC to the factory defaults. SupportAssist settings including registration information will be permanently removed. Default username will reset to root and password to the shipping value (root/shipping value).<br>- C(Default)This action will reset your iDRAC to the factory defaults. SupportAssist settings including registration information will be permanently removed. User and network settings will be preserved.<br>- "Note: Supported only for iDRAC9."</td>         
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
      <td>idrac_reset_out</td>
      <td>{"msg": "iDRAC reset operation completed successfully"
}</td>
<td>Module output of idrac reset</td>
</tbody>
</table>

## Examples 
-----

```
- name: Restart the idrac and wait for the idrac to be ready
  ansible.builtin.include_role:
    name: idrac_reset       
  vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
 
- name: Restart the idrac and do not wait for the idrac to be ready
  ansible.builtin.include_role:
    name: idrac_reset       
  vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    wait_for_idrac: false
 
- name: Reset the idrac and wait for the idrac to be ready
  ansible.builtin.include_role:
    name: idrac_reset       
  vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    reset_to_default: "All"
```

## Author Information
------------------

Dell Technologies <br>
Kritika Bhateja (Kritika.Bhateja@Dell.com)  2023