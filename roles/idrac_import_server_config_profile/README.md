# idrac_import_server_config_profile

Role to import the Server Configuration Profile (SCP) from the iDRAC to a network share (CIFS, NFS, HTTP, HTTPS) or a local path.

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
    <td>iDRAC IP Address</td>
  </tr>
  <tr>
    <td>username</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>iDRAC username</td>
  </tr>
  <tr>
    <td>password</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>iDRAC user password.</td>
  </tr>
  <tr>
    <td>https_port</td>
    <td>false</td>
    <td>443</td>
    <td></td>
    <td>int</td>
    <td>iDRAC port.</td>
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
    <td>The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.</td>
  </tr>
  <tr>
    <td>https_timeout</td>
    <td>false</td>
    <td>30</td>
    <td></td>
    <td>int</td>
    <td> The HTTPS socket level timeout in seconds.</td>
  </tr>
  <tr>
    <td>share_parameters</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>dict</td>
    <td>Network share parameters.</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;share_name</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Network share or local path.<br>- CIFS, NFS, HTTP, and HTTPS network share types are supported.</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;scp_file</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Name of the server configuration profile (SCP) file.</br>- The default format `idrac_ip_YYMMDD_HHMMSS_scp` is used if this option is not specified.</br>- I(export_format) is used if the valid extension file is not provided.</td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;share_user</td>
      <td>false</td>
      <td></td>
      <td></td>
      <td>str</td>
      <td>Network share user in the format 'user@domain' or 'domain\\user' if user is part of a domain else 'user'. This option is mandatory for CIFS Network Share..</td>
    </tr>
    <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;share_password</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>Network share user password. This option is mandatory for CIFS Network Share.</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;proxy_support</td>
    <td>false</td>
    <td>false</td>
    <td></td>
    <td>bool</td>
    <td>- Proxy to be enabled or disabled.</br>- I(proxy_support) is considered only when I(share_name) is of type HTTP or HTTPS and is supported only on iDRAC9.</td>
    </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;proxy_type</td>
    <td>false</td>
    <td>http</td>
    <td>http, socks4</td>
    <td>str</td>
    <td>- C(http) to select HTTP type proxy.</br>- C(socks4) to select SOCKS4 type proxy.</br>- I(proxy_type) is considered only when I(share_name) is of type HTTP or HTTPS and is supported only on iDRAC9.</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;proxy_server</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td> - I(proxy_server) is required when I(share_name) is of type HTTPS or HTTP and I(proxy_support) is C(true).</br>- I(proxy_server) is considered only when I(share_name) is of type HTTP or HTTPS and is supported only on iDRAC9.</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;proxy_port</td>
    <td>false</td>
    <td>80</td>
    <td></td>
    <td>str</td>
    <td>- Proxy port to authenticate.</br> - I(proxy_port) is required when I(share_name) is of type HTTPS or HTTP and I(proxy_support) is C(true).</br>- I(proxy_port) is considered only when I(share_name) is of type HTTP or HTTPS and is supported only on iDRAC9.</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;proxy_username</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Proxy username to authenticate.</br>- I(proxy_username) is considered only when I(share_name) is of type HTTP or HTTPS and is supported only on iDRAC9.</td>
    </tr>
     <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;proxy_password</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Proxy password to authenticate.</br>- I(proxy_password) is considered only when I(share_name) is of type HTTP or HTTPS and is supported only on iDRAC9.</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ignore_certificate_warning</td>
    <td>false</td>
    <td>ignore</td>
    <td>ignore, showerror</td>
    <td>str</td>
    <td>- If C(ignore), it ignores the certificate warnings.</br>- If C(showerror), it shows the certificate warnings.</br>
        - I(ignore_certificate_warning) is considered only when I(share_name) is of type HTTPS and is supported only on iDRAC9.</td>
  </tr>
  <tr>
    <td>target</td>
    <td>false</td>
    <td>['ALL']</td>
    <td>'ALL', 'IDRAC', 'BIOS', 'NIC', 'RAID'</td>
    <td>str</td>
    <td>- If C(ALL), this module exports or imports all components configurations from SCP file.<br>- If C(IDRAC), this module exports or imports iDRAC configuration from SCP file.<br>- If C(BIOS), this module exports or imports BIOS configuration from SCP file.<br>- If C(NIC), this module exports or imports NIC configuration from SCP file.<br>- If C(RAID), this module exports or imports RAID configuration from SCP file.</br>- When I(command) is C(export) or C(import) I(target) with multiple components is supported only on iDRAC9 with firmware 6.10.00.00 and above.</td>
  </tr>
  <tr>
    <td>import_buffer</td>
    <td>false</td>
    <td></td>
    <td>'Enabled', 'Disabled'</td>
    <td>str</td>
    <td> - SCP content buffer.<br>
         - This is mutually exclusive with share_parameters.scp_file.
    </td>
  </tr>
  <tr>
    <td>end_host_power_state</td>
    <td>false</td>
    <td>'On'</td>
    <td>'On', 'Off'</td>
    <td>str</td>
    <td> Host power state after import of server configuration profile.</td>
  </tr>
  <tr>
    <td>shutdown_type</td>
    <td>false</td>
    <td>'Graceful'</td>
    <td>'Graceful', 'Forced', 'NoReboot'</td>
    <td>str</td>
    <td> Server shutdown type.</td>
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
      <td>idrac_import_server_config_profile_out</td>
      <td>{
    "changed": false,
    "msg": "Successfully imported the Server Configuration Profile.",
    "scp_status": {
        "CompletionTime": "2023-02-21T04:12:37",
        "Description": "Job Instance",
        "EndTime": null,
        "Id": "JID_774927528227",
        "JobState": "Completed",
        "JobType": "ImportConfiguration",
        "Message": "No changes were applied since the current component configuration matched the requested configuration.",
        "MessageArgs": [],
        "MessageId": "IDRAC.2.8.SYS069",
        "Name": "Configure: Import Server Configuration Profile",
        "PercentComplete": 100,
        "StartTime": "TIME_NOW",
        "TargetSettingsURI": null,
        "TaskStatus": "OK",
        "file": ".\\192.1.2.1_2023221_5549_scp.xml",
        "retval": true
    }
}</td>
      <td>Module output of the Server Configuration Job</td>
    </tr>
  </tbody>
</table>

## Examples 
-----

```
- name: Importing SCP from local path with all components
  ansible.builtin.import_role:
    name: idrac_import_server_config_profile
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    share_parameters:
      share_name: "/root/tmp"
      scp_file: "file.xml"
```
```
- name: Importing SCP from NFS with iDRAC components
  ansible.builtin.import_role:
    name: idrac_import_server_config_profile
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    target: ['IDRAC']
    share_parameters:
      share_name: "191.2.1.1:/nfs"
      scp_file: "file.json"
```
```
- name: Importing SCP from CIFS with BIOS components
  ansible.builtin.import_role:
    name: "idrac_import_server_config_profile"
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    target: ['BIOS']
    share_parameters:
      share_name: "\\\\191.1.1.1\\cifs"
      share_user: "username"
      share_password: "password"
      scp_file: "file.xml"
```
```
- name: Importing SCP from HTTPS with RAID components
  ansible.builtin.import_role:
    name: "idrac_import_server_config_profile"
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    target: ['RAID']
    share_parameters:
      share_name: "https://192.1.1.1/share"
      share_user: "username"
      share_password: "password"
      scp_file: "filename.json"
```
```
- name: "Importing SCP from HTTP with NIC components"
  ansible.builtin.import_role:
    name: "idrac_import_server_config_profile"
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    target: ['NIC']
    share_parameters:
      share_name: "http://192.1.1.1/share"
      share_user: "username"
      share_password: "password"
      scp_file: "filename.xml"
```
```
- name: "Importing SCP using import buffer with NIC components"
  ansible.builtin.import_role:
    name: "idrac_import_server_config_profile"
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    target: ['NIC']
    import_buffer: "<SystemConfiguration><Component FQDD='iDRAC.Embedded.1'><Attribute Name='IPMILan.1#Enable'> Disabled</Attribute></Component></SystemConfiguration>"
```
```
- name: "Importing SCP from HTTP with NIC components using proxy"
  ansible.builtin.import_role:
    name: "idrac_import_server_config_profile"
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    target: ['NIC']
    share_parameters:
      share_name: "http://192.1.1.1/share"
      share_user: "username"
      share_password: "password"
      scp_file: "filename.xml"
      proxy_support: true
      proxy_server: 192.168.0.6
      proxy_port: 8080
      proxy_type: socks4
```
```
- name: Import SCP
  hosts: idrac
  roles:
    - role: idrac_import_server_config_profile
```

## Author Information
------------------

Dell Technologies <br>
Abhishek Sinha (Abhishek.Sinha10@Dell.com) 2023
