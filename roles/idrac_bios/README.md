# idrac_bios

This role allows to modify BIOS attributes, clear pending BIOS attributes, and reset the BIOS to default settings.

## Requirements

---

Requirements to develop and contribute to the role.

### Development

```text
ansible
docker
molecule
python
```

### Production

Requirements to use the role.

```text
ansible
python
```

## Ansible collections

Collections required to use the role.

```text
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
    <td>iDRAC user password</td>
  </tr>
  <tr>
    <td>https_port</td>
    <td>false</td>
    <td>443</td>
    <td></td>
    <td>int</td>
    <td>iDRAC port</td>
  </tr>
  <tr>
    <td>validate_certs</td>
    <td>false</td>
    <td>true</td>
    <td></td>
    <td>bool</td>
    <td>
      - If C(false), the SSL certificates will not be validated. <br>
      - Configure C(false) only on personally controlled sites where self-signed certificates are used
    </td>
  </tr>
  <tr>
    <td>ca_path</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>path</td>
    <td>
      - The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.
    </td>
  </tr>
  <tr>
    <td>https_timeout</td>
    <td>false</td>
    <td>30</td>
    <td></td>
    <td>int</td>
    <td>The socket level timeout in seconds.</td>
  </tr>
  <tr>
    <td>attributes</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>dict</td>
    <td>
      - "Dictionary of BIOS attributes and value pair. Attributes should be part of the Redfish Dell BIOS Attribute Registry. Use U(https://I(idrac_ip)/redfish/v1/Systems/System.Embedded.1/Bios) to view the Redfish URI." <br>
      - This is mutually exclusive with I(reset_bios).
    </td>
  </tr>
  <tr>
    <td>apply_time</td>
    <td>false</td>
    <td>Immediate</td>
    <td>Immediate, OnReset, AtMaintenanceWindowStart, InMaintenanceWindowOnReset</td>
    <td>str</td>
    <td>
      - Apply time of the I(attributes). <br>
      - This is applicable only to I(attributes). <br>
      - C(Immediate) Allows the user to immediately reboot the host and apply the changes.
        I(job_wait) is applicable. <br>
      - C(OnReset) Allows the user to apply the changes on the next reboot of the host server. <br>
      - C(AtMaintenanceWindowStart) Allows the user to apply the changes at the start of a maintenance window as specifiedin
        I(maintenance_window). A reboot job will be scheduled. <br>
      - C(InMaintenanceWindowOnReset) Allows to apply the changes after a manual reset but within the maintenance window as specified in  
        I(maintenance_window).
    </td>
  </tr>
  <tr>
    <td>maintenance_window</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>dict</td>
    <td>
      - Option to schedule the maintenance window. <br>
      - This is required when I(apply_time) is C(AtMaintenanceWindowStart) or  
        C(InMaintenanceWindowOnReset).
    </td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;start_time</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>
      - The start time for the maintenance window to be scheduled. <br>
      - The format is YYYY-MM-DDThh:mm:ss<offset>, <offset> is the time offset from UTC that  
        the current time zone set in iDRAC in the format: +05:30 for IST.
    </td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;duration</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>int</td>
    <td>
      - The duration in seconds for the maintenance window. <br>
    </td>
  </tr>
  <tr>
  <td>clear_pending</td>
  <td>false</td>
  <td></td>
  <td></td>
  <td>bool</td>
  <td>
    - Allows the user to clear all pending BIOS attributes changes. <br>
    - C(true) discards any pending changes to BIOS attributes or removes the job if in  
      scheduled state. <br>
    - This operation will not create any job. <br>
    - C(false) does not perform any operation. <br>
    - This is mutually exclusive with I(reset_bios). <br>
    - C(Note) Any BIOS job scheduled will not be cleared because of boot sources configuration. <br>
  </td>
</tr>
  <tr>
    <td>reset_bios</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>bool</td>
    <td>
      - Resets the BIOS to default settings and triggers a reboot of host system. <br>
      - This is applied to the host after the restart. <br>
      - This operation will not create any job. <br>
      - C(false) does not perform any operation. <br>
      - This is mutually exclusive with I(attributes), and I(clear_pending). <br>
      - When C(true), this action will always report as changes found to be applicable.
    </td>
  </tr>
  <tr>
    <td>reset_type</td>
    <td>false</td>
    <td>graceful_restart</td>
    <td>graceful_restart <br> force_restart</td>
    <td>str</td>
    <td>
      - C(force_restart) Forcefully reboot the host system. <br>
      - C(graceful_restart) Gracefully reboot the host system. <br>
      - This is applicable for I(reset_bios), and I(attributes) when I(apply_time) is  
        C(Immediate).
    </td>
  </tr>
  <tr>
    <td>job_wait</td>
    <td>false</td>
    <td>true</td>
    <td></td>
    <td>bool</td>
    <td>
      - Provides the option to wait for job completion. <br>
      - This is applicable for I(attributes) when I(apply_time) is C(Immediate). <br>
    </td>
  </tr>
  <tr>
    <td>job_wait_timeout</td>
    <td>false</td>
    <td>1200</td>
    <td></td>
    <td>int</td>
    <td>
      - The maximum wait time of I(job_wait) in seconds. <br>
        The job is tracked only for this duration. <br>
      - This option is applicable when I(job_wait) is C(True). <br>
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
      <td>idrac_bios_out</td>
      <td>{
  "attributes": {
    "ansible_facts": {},
    "changed": true,
    "failed": false,
    "job_id": "JID_XXXXXXXXXXXX",
    "msg": {
      "ActualRunningStartTime": "2023-05-19T04:55:01",
      "ActualRunningStopTime": "2023-05-19T04:59:21",
      "CompletionTime": "2023-05-19T04:59:21",
      "Description": "Job Instance",
      "EndTime": "TIME_NA",
      "Id": "JID_844899049402",
      "JobState": "Completed",
      "JobType": "BIOSConfiguration",
      "Message": "Job completed successfully.",
      "MessageArgs": [],
      "MessageId": "PR19",
      "Name": "Configure: BIOS.Setup.1-1",
      "PercentComplete": 100,
      "StartTime": "2023-05-19T04:51:44",
      "TargetSettingsURI": null
    },
    "status_msg": "Successfully applied the BIOS attributes update."
  },
  "clear_pending": {
    "changed": false,
    "skip_reason": "Conditional result was False",
    "skipped": true
  },
  "reset_bios": {
    "changed": false,
    "skip_reason": "Conditional result was False",
    "skipped": true
  }
}</td>
      <td>Module output of the idrac_bios job.</td>
    </tr>
  </tbody>
</table>

## Examples

---

```yaml
- name: Configure generic attributes of the BIOS
  ansible.builtin.import_role:
    name: idrac_bios
  vars:
    hostname: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    attributes:
      BootMode : "Bios"
      OneTimeBootMode: "Enabled"
      BootSeqRetry: "Enabled"
```

```yaml
- name: Configure BIOS attributes at Maintenance window.
  ansible.builtin.import_role:
    name: idrac_bios
  vars:
    hostname: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    apply_time: AtMaintenanceWindowStart
    maintenance_window:
      start_time: "2022-09-30T05:15:40-05:00"
      duration: 600
    attributes:
      BootMode : "Bios"
      OneTimeBootMode: "Enabled"
      BootSeqRetry: "Enabled"
```

```yaml
- name: Clear pending BIOS attributes.
  ansible.builtin.import_role:
    name: idrac_bios
  vars:
    hostname: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    clear_pending: true
```

```yaml
- name: Reset BIOS attributes to default settings.
  ansible.builtin.import_role:
    name: idrac_bios
  vars:
    hostname: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    reset_bios: true
```

## Author Information

---

Dell Technologies <br>
Abhishek Sinha (Abhishek.Sinha10@Dell.com) 2023
