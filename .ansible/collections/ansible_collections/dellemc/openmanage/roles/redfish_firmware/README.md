# redfish_firmware

To perform a component firmware update using the image file available on the local or remote system.

## Requirements

---


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

## Ansible collections

Collections required to use the role.

```
dellemc.openmanage
```

## Role Variables

---

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
    <td>- The socket level timeout in seconds.</td>
  </tr>
    <tr>
    <td>image_uri</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Firmware Image location URI or local path.
    <br>- For example- U(http://<web_address>/components.exe) or /home/firmware_repo/component.exe.
    </td>
  </tr>
  <tr>
    <td>transfer_protocol</td>
    <td>false</td>
    <td>HTTP</td>
    <td>"CIFS", "FTP", "HTTP", "HTTPS", "NSF", "OEM", "SCP", "SFTP", "TFTP"</td>
    <td>str</td>
    <td>- Protocol used to transfer the firmware image file. Applicable for URI based update.</td>
  </tr>
  <tr>
    <td>job_wait</td>
    <td>false</td>
    <td>true</td>
    <td></td>
    <td>str</td>
    <td>- Provides the option to wait for job completion.</td>
  </tr>
  <tr>
    <td>job_wait_timeout</td>
    <td>false</td>
    <td>3600</td>
    <td></td>
    <td>str</td>
    <td>- The maximum wait time of I(job_wait) in seconds. The job is tracked only for this duration.
    <br>- This option is applicable when I(job_wait) is C(True).
    </td>
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
      <td>redfish_firmware_out</td>
      <td>{
        msg: Successfully submitted the firmware update task.
        task: {
        "id": "JID_XXXXXXXXXXXX",
        "uri": "/redfish/v1/TaskService/Tasks/JID_XXXXXXXXXXXX"
    }
  }</td>
      <td>Returns the output of the firmware update status.</td>
    </tr>
  </tbody>
</table>

## Examples

---

```
- name: Update the firmware from a single executable file available in HTTP protocol
  ansible.builtin.include_role:
    name: redfish_firmware:
  vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    image_uri: "http://192.168.0.2/firmware_repo/component.exe"
    transfer_protocol: "HTTP"
```

```
- name: Update the firmware from a single executable file available in a local path
  ansible.builtin.include_role:
    name: redfish_firmware:
  vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    image_uri: "/home/firmware_repo/component.exe"
```

```
- name: Update the firmware from a single executable file available in a HTTP protocol with job_wait_timeout
  ansible.builtin.include_role:
      name: redfish_firmware:
  vars:
    hostname: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    image_uri: "http://192.168.0.2/firmware_repo/component.exe"
    transfer_protocol: "HTTP"
    job_wait_timeout: 600
```

## Author Information

---

Dell Technologies <br>
Shivam Sharma (Shivam.Sharma3@Dell.com) 2023
