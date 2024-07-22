# idrac_server_powerstate

Role to to manage the different power states of the specified device using iDRACs (iDRAC8 and iDRAC9 only) for Dell PowerEdge servers. 

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
    <td>- This option is the unique identifier of the device being managed. For example, U(https://<I(baseuri)>/redfish/v1/Systems/<I(resource_id)>).<br>- This option is mandatory for I(base_uri) with multiple devices.<br>- To get the device details, use the API U(https://<I(baseuri)>/redfish/v1/Systems) for reset_type operation and
    U(https://<I(baseuri)>/redfish/v1/Chassis) for oem_reset_type operation.</td>
  </tr>
  <tr>
    <td>reset_type</td>
    <td>false</td>
    <td></td>
    <td>["ForceOff", "ForceOn", "ForceRestart", "GracefulRestart", "GracefulShutdown", "Nmi", "On", "PowerCycle", "PushPowerButton"]</td>
    <td>str</td>
    <td>- This option resets the device.<br>- C(ForceOff) turns off the device immediately.<br>- C(ForceOn) turns on the device immediately.<br>- C(ForceRestart) turns off the device immediately, and then restarts the server.<br>- C(GracefulRestart) performs graceful shutdown of the device, and then restarts the device.<br>- C(GracefulShutdown) performs a graceful shutdown of the device, and then turns off the device.<br>- C(Nmi) sends a diagnostic interrupt to the device. This option is usually a nonmaskable interrupt (NMI) on x86 systems.<br>- C(On) turns on the device.<br>- C(PowerCycle) performs a power cycle on the device.<br>- C(PushPowerButton) simulates the pressing of a physical power button on the device.<br>- I(reset_type) is mutually exclusive with I(oem_reset_type).<br>- When a power control operation is performed, which is not supported on the device, an error message is displayed with the list of operations that can be performed.</td>
  </tr>
  <tr>
    <td>oem_reset_type</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>dict</td>
    <td>- This parameter initiates a complete Alternate Current (AC) power cycle of the server which is equivalent to disconnecting power cables using OEM API.<br>- I(oem_reset_type) is mutually exclusive with I(reset_type).<br>- If the value of 'final_power_state' is not provided, the default value is 'Off'.</td>
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

- name: "Performing AC Power Cycle operation with final power state On"
  ansible.builtin.include_role:
    name: idrac_server_powerstate
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    oem_reset_type:
      dell:
        final_power_state: "On"
        reset_type: "PowerCycle"

- name: "Performing AC Power Cycle operation with final power state Off"
  ansible.builtin.include_role:
    name: idrac_server_powerstate
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    oem_reset_type:
      dell:
        final_power_state: "Off"
        reset_type: "PowerCycle"
```

## Author Information
------------------

Dell Technologies <br>
Kritika Bhateja (Kritika.Bhateja@Dell.com)  2023 <br>
Lovepreet Singh (lovepreet.singh1@dell.com)  2024
