# idrac_export_server_config_profile

Role to Export the Server Configuration Profile (SCP) from the iDRAC to a network share (CIFS, NFS, HTTP, HTTPS) or a local path.

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
    <td>idrac_ip</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- iDRAC IP Address</td>
  </tr>
  <tr>
    <td>idrac_user</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- iDRAC username</td>
  </tr>
  <tr>
    <td>idrac_password</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- iDRAC user password.</td>
  </tr>
  <tr>
    <td>idrac_port</td>
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
    <td>idrac_timeout</td>
    <td>false</td>
    <td>30</td>
    <td></td>
    <td>int</td>
    <td>- The HTTPS socket level timeout in seconds.</td>
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
    <td>true</td>
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
      <td>- Network share user in the format 'user@domain' or 'domain\\user' if user is part of a domain else 'user'. This option is mandatory for CIFS Network Share..</td>
    </tr>
    <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;share_password</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Network share user password. This option is mandatory for CIFS Network Share.</td>
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
    <td>- If C(ignore), it ignores the certificate warnings.</br>- If C(showerror), it shows the certificate warnings.</br>- I(ignore_certificate_warning) is considered only when I(share_name) is of type HTTPS and is supported only on iDRAC9.</td>
  </tr>
    <tr>
    <td>include_in_export</td>
    <td>false</td>
    <td>default</td>
    <td>default, readonly, passwordhashvalues, customtelemetry</td>
    <td>str</td>
    <td>- This option is applicable when I(command) is C(export).<br>- If C(default), it exports the default Server Configuration Profile.<br>- If C(readonly), it exports the SCP with readonly attributes.<br>- If C(passwordhashvalues), it exports the SCP with password hash values.<br>- If C(customtelemetry), exports the SCP with custom telemetry attributes supported only in the iDRAC9.</td>
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
    <td>export_format</td>
    <td>false</td>
    <td>'XML'</td>
    <td>'JSON', 'XML'</td>
    <td>str</td>
    <td>- Specify the output file format. This option is applicable for C(export) command.</td>
  </tr>
  <tr>
    <td>export_use</td>
    <td>false</td>
    <td>'Default'</td>
    <td>'Default', 'Clone', 'Replace'</td>
    <td></td>
    <td>- Specify the type of Server Configuration Profile (SCP) to be exported.<br>- This option is applicable when I(command) is C(export).<br>- C(Default) Creates a non-destructive snapshot of the configuration.<br>- C(Replace) Replaces a server with another or restores the servers settings to a known baseline.<br>- C(Clone) Clones settings from one server to another server with the identical hardware setup.</td>
  </tr>
</tbody>
</table>

## Fact varaibles

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
      <td>out_scp</td>
      <td>{
        "changed": false,
        "failed": false,
        "msg": "Successfully exported the Server Configuration Profile.",
        "scp_status": {
            "ActualRunningStartTime": "2023-02-21T10:59:50",
            "ActualRunningStopTime": "2023-02-21T11:00:08",
            "CompletionTime": "2023-02-21T11:00:08",
            "Id": "JID_769771903262",
            "JobState": "Completed",
            "JobType": "ExportConfiguration",
            "Message": "Successfully exported Server Configuration Profile",
            "MessageArgs": [],
            "MessageId": "SYS043",
            "PercentComplete": 100,
            "TargetSettingsURI": null,
            "file": ".\\192.1.2.1_2023221_16301_scp.xml",
            "retval": true
        }
    }</td>
      <td>Module output of the Server Configuration Job</td>
    </tr>
    <tr>
      <td>share_type</td>
      <td>NFS</td>
      <td>Stores the share type sent as part of the role variables</td>
    </tr>
  </tbody>
</table>

## Examples 
-----

```
- name: Exporting SCP local path with all components
  ansible.builtin.import_role:
    name: idrac_export_server_config_profile
  vars:
    idrac_ip: "192.1.2.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    share_parameters:
      share_name: "/root/tmp"
      scp_file: "file.xml"
```
```
- name: "Exporting SCP to NFS with iDRAC components"
  ansible.builtin.import_role:
    name: "idrac_export_server_config_profile"
  vars:
    idrac_ip: "192.1.2.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    target: ['IDRAC']
    share_parameters:
      share_name: "191.2.1.1:/nfs"
      scp_file: "file.json"
```
```
- name: "Exporting SCP to CIFS with BIOS components"
  ansible.builtin.import_role:
    name: "idrac_export_server_config_profile"
  vars:
    idrac_ip: "192.1.2.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    target: ['BIOS']
    share_parameters:
      share_name: "\\\\191.1.1.1\\cifs"
      share_user: "username"
      share_password: "password"
      scp_file: "file.xml"
```
```
- name: "Exporting SCP to HTTPS with RAID components"
  ansible.builtin.import_role:
    name: "idrac_export_server_config_profile"
  vars:
    idrac_ip: "192.1.2.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    target: ['RAID']
    share_parameters:
      share_name: "https://192.1.1.1/share"
      share_user: "username"
      share_password: "password"
      scp_file: "filename.json"
```
```
- name: "Exporting SCP to HTTP with NIC components"
  ansible.builtin.import_role:
    name: "idrac_export_server_config_profile"
  vars:
    idrac_ip: "192.1.2.1"
    idrac_user: "username"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    target: ['NIC']
    share_parameters:
      share_name: "http://192.1.1.1/share"
      share_user: "username"
      share_password: "password"
      scp_file: "filename.xml"
```
```
- name: Export SCP
  hosts: idrac
  roles:
    - role: idrac_export_server_config_profile
```

## Author Information
------------------

Dell Technologies <br>
Abhishek Sinha (Abhishek.Sinha10@Dell.com)  2023