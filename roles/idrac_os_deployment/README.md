# idrac_os_deployment

Role to deploy operating system and version on the servers.</br>

The role perform the following operations:
1. Downloads the source ISO as a local copy in the ansible controller machine.
1. Create a mount and extract the ISO using the `xorriso` library.
1. Create a kickstart file using jinja template based on the os name and version .
1. Enable the extracted ISO to use kickstart file by modifying the boot configurations for bios and uefi.
1. Compile the iso to generate a custom iso by embedding the kickstart file in an iso using the `mkisofs`, `isohybrid` and `implantisomd5` commands.
1. Copy the custom ISO generated to destination share location as specfied to the role input. Based on the input a following method is used to copy the destination to a shared repository.
    - CIFS/NFS  uses the file mount to copy the ISO to a destination location.
    - HTTP/HTTPS uses the SSH to copy/transfer the ISO to a location where the web server content is served.
1. Using an iDRAC `idrac_virtual_media` module mount the custom ISO as virtual media (virtual CD) in an iDRAC.
1.  Using an iDRAC `idrac_boot` module set the boot target to CD and enable a reboot to CD once.
1. Track for the OS deployment for the specified amount of user input time.
1. Eject the virtual media after the specfied time is finished.

## Requirements

### Prereq
To Support the HTTP/HTTPS repository as a destination an ssh to a target machine should be enabled to copy the custom iso into a https share location.

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
    <td>The operating system version to match the jinja template of the kickstart file.</td>
  </tr>
  </tr>
    <tr>
    <td>os_version</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>The operating system name to match the jinja template of the kickstart file.<br>Supported versions for RHEL are 9.x and 8.x and for ESXi is 8.x.</td>
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
      <td>Local path or network share path of the ISO.<br>CIFS, NFS, HTTP and HTTPS shares are supported.</td>
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
    <td>Local path or network path to place the custom ISO.<br>Share need to have a write permission to copy the generated ISO.<br>When the path is of HTTP/HTTPS we use ssh to copy the custom iso into a destination location/folder where the web server content is served.<br>When the path is of CIFS/NFS we mount the folders and copy the custom iso into the shared location.</br>CIFS, NFS, HTTP and HTTPS shares are supported.<br></td>
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
  <tr>
    <td>http_path</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>Path to the web server where the custom iso has to be transfered via ssh</br> this is required in case the destination path is HTTP/HTTPS</td>
  </tr>
  <tr>
    <td>ssh_user</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>Username for SSH login into the target machine where the custom iso will be copied to serve from the http/https repository.</br> This is required in case the destination path is HTTP/HTTPS</td>
  </tr>
  <tr>
    <td>ssh_pass</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>Password for SSH login into the target machine where the custom iso will be copied to serve from the http/https repository.</br> This is required in case the destination path is HTTP/HTTPS</td>
  </tr>
    <tr>
    <td>dest_os</td>
    <td>false</td>
    <td>linux</td>
    <td>linux <br> windows</td>
    <td>str</td>
    <td>Operating system in which the custom iso will be transfered using ssh.</br>This is used custom ISO is tranfered via ssh to the destination folder from where http/https web server serves the content.</td>
  </tr>
</tbody>
</table>

## Variables
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
      <td>dest_owner</td>
      <td>user</td>
      <td>Custom iso file owner.</br>This is used custom ISO is tranfered via ssh to the destination folder from where http/https web server serves the content.</td>
    </tr>
     <tr>
      <td>dest_group</td>
      <td>group</td>
      <td>Custom iso file group.</br>This is used custom ISO is tranfered via ssh to the destination folder from where http/https web server serves the content.</td>
    </tr>
    <tr>
      <td>dest_mode</td>
      <td>0644</td>
      <td>Custom iso file permission.</br>This is used custom ISO is tranfered via ssh to the destination folder from where http/https web server serves the content.</td>
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

## Env Varaibles

When we have to SSH into a machine a fingerprint has to be added into the ansible controller machine for it to connect succesfully, if you trust the machine you are copying you use the below environment variable disable the fingerprint check.

```export ANSIBLE_HOST_KEY_CHECKING=False```

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

- name: Install ESXi OS with kickstart file
  ansible.builtin.import_role:
    name: idrac_os_deployment
  vars:
    hostname: 192.168.0.1
    username: root
    password: password
    ca_path: path/to/ca
    os_name: ESXi
    os_version: 8
    kickstart_file: "/path/to/esxi_ks.cfg"
    source_iso:
      path: //192.168.0.2/cifs_share/path/to/VMware-Installer-8.x-86_64.iso
      username: administrator
      password: password
    destination_path:
      path: 192.1.2.3:/path/to/nfshare
```

## Author Information
------------------

Dell Technologies <br>
Jagadeesh N V (Jagadeesh.N.V@Dell.com) 2023 <br>
Abhishek Sinha (Abhishek.Sinha10@Dell.com) 2023
