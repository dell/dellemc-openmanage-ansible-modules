# idrac_firmware

Update the Firmware by connecting to a network share (CIFS, NFS, HTTP, HTTPS, FTP) that contains a catalog of available updates. 

## Requirements

### Development
Requirements to develop and contribute to the role.
```
ansible
docker
molecule
python
omsdk
```
### Production
Requirements to use the role.
```
ansible
python
omsdk
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
    <td>share_name</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Network share path of update repository. CIFS, NFS, HTTP, HTTPS and FTP share types are supported.</td>
  </tr>
  <tr>
    <td>share_user</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Network share user in the format 'user@domain' or 'domain\\user' if user is part of a domain else 'user'. This option is mandatory for CIFS Network Share.</td>
  </tr>
  <tr>
    <td>share_password</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Network share user password. This option is mandatory for CIFS Network Share.</td>
  </tr>
    <tr>
    <td>catalog_file_name</td>
    <td>false</td>
    <td>Catalog.xml</td>
    <td></td>
    <td>str</td>
    <td>- Catalog file name relative to the I(share_name</td>
  </tr>
    <tr>
    <td>ignore_cert_warning</td>
    <td>false</td>
    <td>true</td>
    <td></td>
    <td>bool</td>
    <td>- Specifies if certificate warnings are ignored when HTTPS share is used.</br>- If C(true) option is set, then the certificate warnings are ignored.</td>
  </tr>
    <tr>
    <td>apply_update</td>
    <td>false</td>
    <td>true</td>
    <td></td>
    <td>bool</td>
    <td>  - If I(apply_update) is set to C(true), then the packages are applied.</br>- If I(apply_update) is set to C(false), no updates are applied, and a catalog report of packages is generated and returned.</td>
  </tr>
    <tr>
    <td>reboot</td>
    <td>false</td>
    <td>false</td>
    <td></td>
    <td>bool</td>
    <td>- Provides the option to apply the update packages immediately or in the next reboot.</br> - If I(reboot) is set to C(true),  then the packages  are applied immediately.</br>- If I(reboot) is set to C(false), then the packages are staged and applied in the next reboot.</br>- Packages that do not require a reboot are applied immediately irrespective of I (reboot).
    </td>
  </tr>
  <tr>
    <td>proxy_support</td>
    <td>false</td>
    <td>Off</td>
    <td>"ParametersProxy", "DefaultProxy", "Off"</td>
    <td>str</td>
    <td>- Specifies if a proxy should be used.</br>- Proxy parameters are applicable on C(HTTP), C(HTTPS), and C(FTP) share type of repositories.</br> - C(ParametersProxy), sets the proxy parameters for the current firmware operation.</br>- C(DefaultProxy), iDRAC uses the proxy values set by default.</br>- Default Proxy can be set in the Lifecycle Controller attributes using M(dellemc.openmanage.idrac_attributes).</br>- C(Off), will not use the proxy.</br>- For iDRAC8 based servers, use proxy server with basic authentication.</br>- For iDRAC9 based servers, ensure that you use digest authentication for the proxy server, basic authentication is not supported.
    </td>
  </tr>
  <tr>
    <td>proxy_server</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- The IP address of the proxy server.</br>- This IP will not be validated. The download job will be created even for invalid I(proxy_server).</br>- Please check the results of the job for error details.</br>- This is required when I(proxy_support) is C(ParametersProxy).  </td>
  </tr>
  <tr>
    <td>proxy_port</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>int</td>
    <td>- The Port for the proxy server.</br>- This is required when I(proxy_support) is C(ParametersProxy).</td>
  </tr>
  <tr>
    <td>proxy_type</td>
    <td>false</td>
    <td></td>
    <td>HTTP, SOCKS</td>
    <td>str</td>
    <td>- The proxy type of the proxy server.</br>- This is required when I(proxy_support) is C(ParametersProxy).</td>
  </tr>
  <tr>
    <td>proxy_uname</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- The user name for the proxy server.</td>
  </tr>
  <tr>
    <td>proxy_passwd</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- The password for the proxy server.</td>
  </tr>
    <tr>
    <td>job_wait</td>
    <td>false</td>
    <td></td>
    <td>true</td>
    <td>bool</td>
    <td>- Whether to wait for job completion or not.</td>
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
      <td>idrac_firmware_out</td>
      <td>{
msg: "Successfully updated the firmware."
update_status:  {
        'InstanceID': 'JID_XXXXXXXXXXXX',
        'JobState': 'Completed',
        'Message': 'Job completed successfully.',
        'MessageId': 'REDXXX',
        'Name': 'Repository Update',
        'JobStartTime': 'NA',
        'Status': 'Success',
    }
}</td>
<td>Returns the output of the firmware update status</td>
</tbody>
</table>

## Examples 
-----

```yml
- name: Update firmware from repository on a NFS Share
  ansible.builtin.include_role:
    name: idrac_firmware
  vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    share_name: "192.168.0.0:/share"
    reboot: true
    job_wait: true
    apply_update: true
    catalog_file_name: "Catalog.xml"

```
```yml
- name: Update firmware from repository on a CIFS Share
  ansible.builtin.ansible.builtin.include_role:
    name: idrac_firmware
  vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    share_name: "full_cifs_path"
    share_user: "share_user"
    share_password: "share_password"
    reboot: true
    job_wait: true
    apply_update: true
    catalog_file_name: "Catalog.xml"
```
```yml
- name: Update firmware from repository on a HTTP
  ansible.builtin.include_role:
    name: idrac_firmware
  vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    share_name: "http://downloads.dell.com"
    reboot: true
    job_wait: true
    apply_update: true
```
```yml
- name: Update firmware from repository on a HTTPS
  ansible.builtin.include_role:
    name: idrac_firmware
  vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    share_name: "https://downloads.dell.com"
    reboot: true
    job_wait: true
    apply_update: true
 ```
 ```yml
- name: Update firmware from repository on a HTTPS via proxy
  ansible.builtin.include_role:
    name: idrac_firmware
  vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    share_name: "https://downloads.dell.com"
    reboot: true
    job_wait: true
    apply_update: true
    proxy_support: ParametersProxy
    proxy_server: 192.168.1.10
    proxy_type: HTTP
    proxy_port: 80
    proxy_uname: "proxy_user"
    proxy_passwd: "proxy_pwd"
 ```
 ```yml
- name: Update firmware from repository on a FTP
  ansible.builtin.include_role:
    name: idrac_firmware
  vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    share_name: "ftp://ftp.mydomain.com"
    reboot: true
    job_wait: true
    apply_update: true
```
## Author Information
------------------

Dell Technologies <br>
Sachin Apagundi (Sachin.Apagundi@Dell.com)  2023