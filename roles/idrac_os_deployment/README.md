# idrac_os_deployment

Role to deploy specified operating system and version on the servers.
This Role performs the following.
1. Download iso as a local copy
2. Create a kickstart file using jinja template
3. Extract ISO
4. Enable to use kickstart file in the extracted ISO
5. Compile custom ISO
6. Copy ISO to destination share location
7. Mount the ISO as virtual media (virtual CD) in idrac
8. Set boot target to cd and enable a reboot to cd once
9. Track for the OS deployment using the specified time
10. Eject the virtual media

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
genisoimage
xorriso
syslinux
isomd5sum
wget
```

### Ansible collections
Collections required to use the role
```
dellemc.openmanage
ansible.posix
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
    <td>If C(false), the SSL certificates will not be validated.<br>Configure C(false) only on personally controlled sites where self-signed certificates are used.</td>
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
    <td>os_name</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>The operating system version to match the jinja template of the kickstart file.<br>Currently only C(RHEL) supported.</td>
  </tr>
  </tr>
    <tr>
    <td>os_version</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>The operating system name to match the jinja template of the kickstart file.<br>Supported versions for C(RHEL) are 9.x and 8.x</td>
  </tr>  
  </tr>
  <tr>
    <td>kickstart_file</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>path</td>
    <td>Local path of the kickstart file.<br>Generation of kickstart file will be ignored if a kickstart file is provided.</td>
  </tr>
  <tr>
    <td>source_iso</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>dict</td>
    <td>Network share or local path of the ISO to download.</td>
  </tr>
    <tr>
      <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;path</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td>path</td>
      <td>Local path or network share path of the ISO.<br>CIFS, NFS, HTTP, HTTPS, and FTP shares are supported.</td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;username</td>
      <td>false</td>
      <td></td>
      <td></td>
      <td>str</td>
      <td>Username of the network share.</td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;password</td>
      <td>false</td>
      <td></td>
      <td></td>
      <td>str</td>
      <td>Password of the network share.</td>
    </tr>
  <tr>
    <td>destination_path</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>dict</td>
    <td>Local path or network path to download the ISO.<br>Share need to have a write permission to copy the generated ISO.<br>Only CIFS and NFS are supported.<br></td>
  </tr>
    <tr>
      <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;path</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td>path</td>
      <td>Path of the network share to copy the customized ISO.</td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;username</td>
      <td>false</td>
      <td></td>
      <td></td>
      <td>str</td>
      <td>Username of the network share destination of customized ISO.</td>
    </tr>
    <tr>
      <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;password</td>
      <td>false</td>
      <td></td>
      <td></td>
      <td>str</td>
      <td>Password of the network share destination of customized ISO.</td>
    </tr>
  <tr>
    <td>os_wait</td>
    <td>false</td>
    <td>true</td>
    <td></td>
    <td>bool</td>
    <td>Wait for the OS deployment to finish.</td>
  </tr>  
  <tr>
    <td>os_wait_time</td>
    <td>false</td>
    <td>30</td>
    <td></td>
    <td>int</td>
    <td>Time in minutes to wait for the OS deployment to finish.</td>
  </tr>
  <tr>
    <td>eject_iso</td>
    <td>false</td>
    <td>true</td>
    <td></td>
    <td>bool</td>
    <td>Eject the virtual media (ISO) after the tracking of OS deployment is finished.</td>
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
      <td>idrac_os_deployment_message</td>
      <td>Successfully deployed the Operating System</td>
      <td>Output of the OS deployment role.</td>
    </tr>
  </tbody>
</table>

## Examples 
-----

```
- name: Install RHEL OS with kickstart file
  ansible.builtin.import_role:
    name: idrac_os_deployment
  vars:
    hostname: 192.168.0.1
    username: root
    password: password
    ca_path: path/to/ca
    os_name: RHEL
    os_version: 9.1
    kickstart_file: "/path/to/rhel_ks.cfg"
    source_iso:
      path: //192.168.0.2/cifs_share/path/to/RHEL_9x.iso
      username: administrator
      password: password
    destination_path:
      path: 192.1.2.3:/path/to/nfshare

- name: Generate Kickstart file and install RHEL OS
  ansible.builtin.import_role:
    name: idrac_os_deployment
  vars:
    hostname: 192.168.0.1
    username: root
    password: password
    ca_path: path/to/ca
    os_name: RHEL
    os_version: 8.1
    source_iso:
      path: https://share_address/to/iso
      username: https_user
      password: password
    destination_path:
      path: //192.168.0.2/path/cifsshare
      username: cifs_user
      password: password
```

## Author Information
------------------

Dell Technologies <br>
Jagadeesh N V (Jagadeesh.N.V@Dell.com)  2023