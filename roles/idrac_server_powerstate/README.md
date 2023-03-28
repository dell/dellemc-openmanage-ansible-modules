# idrac_server_powerstate

Role to to manage the different power states of the specified device using iDRACs (iDRAC7/8 and iDRAC9 only) for Dell PowerEdge servers. 

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
    <td>resource_id</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- The unique identifier of the device being managed.For example- U(https://<I(baseuri)>/redfish/v1/Systems/<I(resource_id)>).<br>- This option is mandatory for I(base_uri) with multiple devices.<br>- To get the device details, use the API U(https://<I(baseuri)>/redfish/v1/Systems).</td>
  </tr>
  <tr>
    <td>reset_type</td>
    <td>false</td>
    <td>'On'</td>
    <td>["ForceOff", "ForceOn", "ForceRestart", "GracefulRestart", "GracefulShutdown", "Nmi", "On", "PowerCycle", "PushPowerButton"]</td>
    <td>str</td>
    <td>- This option resets the device.<br>- If C(ForceOff), Turns off the device immediately.<br>- If C(ForceOn), Turns on the device immediately.<br>- If C(ForceRestart), Turns off the device immediately, and then restarts the device.<br>- If C(GracefulRestart), Performs graceful shutdown of the device, and then restarts the device.<br>- If C(GracefulShutdown), Performs a graceful shutdown of the device, and the turns off the device.<br>- If C(Nmi), Sends a diagnostic interrupt to the device. This is usually a non-maskable interrupt (NMI) on x86 device.<br>- If C(On), Turns on the device.<br>- If C(PowerCycle), Performs power cycle on the device.<br>- If C(PushPowerButton), Simulates the pressing of a physical power button on the device.<br>- When a power control operation is performed, which is not supported on the device, an error message is displayed with the list of operations that can be performed.</td>
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
      <td>idrac_server_powerstate_out</td>
      <td>{"changed": true,
        "failed": false,
        "msg": "Successfully performed the reset type operation 'GracefulRestart'."
}</td>
<td>Module output of the powercycle contol</td>
</tbody>
</table>

## Examples 
-----

```
- name: "Performing force off operation"
  ansible.builtin.include_role:
    name: idrac_server_powerstate
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    reset_type: "ForceOff"
  
- name: "Performing power on operation"
  ansible.builtin.include_role:
    name: idrac_server_powerstate
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    reset_type: "On"

- name: "Performing graceful restart operation"
  ansible.builtin.include_role:
    name: idrac_server_powerstate
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    reset_type: "GracefulRestart"

- name: "Performing graceful shutdown operation"
  ansible.builtin.include_role:
    name: idrac_server_powerstate
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    reset_type: "GracefulShutdown"

- name: "Performing powercycle operation"
  ansible.builtin.include_role:
    name: idrac_server_powerstate
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    reset_type: "PowerCycle"

- name: "Performing push power button operation"
  ansible.builtin.include_role:
    name: idrac_server_powerstate
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    reset_type: "PushPowerButton"

- name: "Performing force restart operation"
  ansible.builtin.include_role:
    name: idrac_server_powerstate
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    reset_type: "ForceRestart"
```

## Author Information
------------------

Dell Technologies <br>
Kritika Bhateja (Kritika.Bhateja@Dell.com)  2023