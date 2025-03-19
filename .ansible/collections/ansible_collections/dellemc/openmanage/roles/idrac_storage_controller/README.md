# idrac_storage_controller

Role to configure the physical disk, virtual disk, and storage controller settings on iDRAC9 based PowerEdge servers.

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
    <td>- iDRAC user password</td>
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
    <td>controller_id</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- The ID of the controller on which the operations need to be performed.</td>
  </tr>
  <tr>
    <td>volumes</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>dict</td>
    <td>- List of volume that belongs to I(controller_id).</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;id</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Fully Qualified Device Descriptor (FQDD) of the volume.</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dedicated_hot_spare</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Fully Qualified Device Descriptor (FQDD) of the physical disk to assign the volume as a dedicated hot spare to a disk.</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;encrypted</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>bool</td>
    <td>- To encrypt the virtual disk.</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;expand_capacity_disk</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Fully Qualified Device Descriptor (FQDD) of the disk for expanding the capacity with the existing disk.<br>- I(expand_capacity_size) is mutually exclusive with I(expand_capacity_disk).</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;expand_capacity_size</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Capacity of the virtual disk to be expanded in MB.<br>- Check mode and Idempotency is not supported for I(expand_capacity_size).<br>- Minimum Online Capacity Expansion size must be greater than 100 MB of the current size.<br>- I(expand_capacity_disk) is mutually exclusive with I(expand_capacity_size).</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;blink</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>bool</td>
    <td>- Blinks the target virtual disk, and it always reports as changes found when check mode is enabled.</td>
  </tr>
  <tr>
    <td>disks</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>dict</td>
    <td>- List of physical disks that belongs to I(controller_id).</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;id</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Fully Qualified Device Descriptor (FQDD) of the physical disk.</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;blink</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>bool</td>
    <td>- Blinks the target physical disk, and it always reports as changes found when check mode is enabled.</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;raid_state</td>
    <td>false</td>
    <td></td>
    <td>'raid', 'nonraid'</td>
    <td>str</td>
    <td>- Converts the disk form Non-Raid to Raid and vice versa.<br>- C(raid) converts the physical disk to Raid.<br>- C(nonraid) converts the physical disk to Non Raid.</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;status</td>
    <td>false</td>
    <td></td>
    <td>'online', 'offline'</td>
    <td>str</td>
    <td>- Converts the disk form online to offline and vice versa.<br>- C(online) converts the physical disk status to online.<br>- C(offline) converts the physical disk status to offline.</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;global_hot_spare</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>bool</td>
    <td>- Assigns a global hot spare or unassigns a hot spare.<br>- C(true) assigns the disk as a global hot spare.<br>- C(false) unassigns the disk as a hot spare.</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;erase</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>bool</td>
    <td>- Securely erase a device. <br>- C(true) securely erase the disk.<br>- C(false) skips the secure erase operation.</td>
  </tr>
  <tr>
    <td>reset_config</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>bool</td>
    <td>- To reset the controller.</td>
  </tr>
  <tr>
    <td>set_controller_key</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>bool</td>
    <td>- Set the security key or enable controller encryption.<br>- If I(mode) is provided controller encryption operation is performed, otherwise sets the controller security key.<br>- I(key), and I(key_id) are required for this operation.</td>
  </tr>
  <tr>
    <td>rekey</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>bool</td>
    <td>- Resets the key on the controller, and it always reports as changes found when check mode is enabled.</td>
  </tr>
  <tr>
    <td>remove_key</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>bool</td>
    <td>- Remove the key on controllers.</td>
  </tr>
  <tr>
    <td>key</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- A new security key passphrase that the encryption-capable controller uses to create the encryption key. The controller uses the encryption key to lock or unlock access to the Self-Encrypting Drive (SED). Only one encryption key can be created for each controller.<br>- This is mandatory when I(set_controller_key) is C(true), I(rekey) is C(true).<br>- The length of the key can be a maximum of 32 characters in length, where the expanded form of the special character is counted as a single character.<br>- The key must contain at least one character from each of the character classes are uppercase, lowercase, number, and special character.</td>
  </tr>
  <tr>
    <td>key_id</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- This is a user supplied text label associated with the passphrase.<br>- This is mandatory when I(set_controller_key) is C(true), I(rekey) is C(true).<br>- The length of I(key_id) can be a maximum of 32 characters in length and should not have any spaces.</td>
  </tr>
  <tr>
    <td>old_key</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Security key passphrase used by the encryption-capable controller.<br>- This option is mandatory when I(rekey) is C(true).</td>
  </tr>
  <tr>
    <td>mode</td>
    <td>false</td>
    <td></td>
    <td>'LKM', 'SEKM'</td>
    <td>str</td>
    <td>- Encryption mode of the encryption capable controller.<br>- This option is mandatory when I(rekey) is C(true) and for enabling controller encryption.<br>- C(SEKM) to choose mode as secure enterprise key manager.<br>- C(LKM) to choose mode as local key management.</td>
  </tr>
  <tr>
    <td>attributes</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>dict</td>
    <td>- Dictionary of controller attributes and value pair.<br>- This feature is only supported for iDRAC9 with firmware version 6.00.00.00 and above.<br>- I(controller_id) is required for this operation.<br>- I(apply_time) and I(maintenance_window) is applicable for I(attributes).<br>- Use U(https://I(idrac_ip)/redfish/v1/Schemas/DellOemStorageController.json) to view the attributes.</td>
  </tr>
  <tr>
    <td>apply_time</td>
    <td>false</td>
    <td>Immediate</td>
    <td>'Immediate', 'OnReset', 'AtMaintenanceWindowStart', 'InMaintenanceWindowOnReset'</td>
    <td>str</td>
    <td>- Apply time of the I(attributes).<br>- This is applicable only to I(attributes).<br>- C(Immediate) Allows the user to immediately reboot the host and apply the changes. I(job_wait) is applicable.<br>- C(OnReset) Allows the user to apply the changes on the next reboot of the host server.<br>- C(AtMaintenanceWindowStart) Allows the user to apply the changes at the start of a maintenance window as specified in I(maintenance_window).<br>- C(InMaintenanceWindowOnReset) Allows the users to apply after a manual reset but within the maintenance window as specified in I(maintenance_window).</td>
  </tr>
  <tr>
    <td>maintenance_window</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>dict</td>
    <td>- Option to schedule the maintenance window.<br>- This is required when I(apply_time) is C(AtMaintenanceWindowStart) or C(InMaintenanceWindowOnReset).</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;start_time</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- The start time for the maintenance window to be scheduled.<br>- The format is YYYY-MM-DDThh:mm:ss<offset>.<br>- <offset> is the time offset from UTC that the current timezone set in iDRAC in the format is +05:30 for IST.</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;duration</td>
    <td>false</td>
    <td>900</td>
    <td></td>
    <td>int</td>
    <td>- The duration in seconds for the maintenance window.</td>
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
      <td>idrac_storage_controller_out</td>
      <td>
      <pre>
        <code class="json">
        {
            "assign_dedicated_spare": {
                "changed": false,
                "false_condition": "volumes.id is defined and volumes.dedicated_hot_spare is defined",
                "skip_reason": "Conditional result was False",
                "skipped": true
            },
            "assign_global_spare": {
                "changed": false,
                "false_condition": "disks.id is defined and disks.global_hot_spare is true",
                "skip_reason": "Conditional result was False",
                "skipped": true
            },
            "blink_pd": {
                "changed": false,
                "false_condition": "disks.blink is defined",
                "skip_reason": "Conditional result was False",
                "skipped": true
            },
            "blink_vd": {
                "changed": false,
                "false_condition": "volumes.blink is defined",
                "skip_reason": "Conditional result was False",
                "skipped": true
            },
            "controller_attributes_config": {
                "changed": false,
                "false_condition": "attributes is defined",
                "skip_reason": "Conditional result was False",
                "skipped": true
            },
            "controller_rekey": {
                "changed": false,
                "false_condition": "rekey is true",
                "skip_reason": "Conditional result was False",
                "skipped": true
            },
            "controller_reset_config": {
                "changed": false,
                "false_condition": "reset_config is true",
                "skip_reason": "Conditional result was False",
                "skipped": true
            },
            "enable_encryption": {
                "changed": false,
                "false_condition": "set_controller_key is true and key is defined and key_id is defined and mode is defined",
                "skip_reason": "Conditional result was False",
                "skipped": true
            },
            "lock_vd": {
                "changed": false,
                "false_condition": "volumes.encrypted is true",
                "skip_reason": "Conditional result was False",
                "skipped": true
            },
            "oce_vd": {
                "changed": false,
                "false_condition": "volumes.expand_capacity_disk is defined or volumes.expand_capacity_size is defined",
                "skip_reason": "Conditional result was False",
                "skipped": true
            },
            "physical_disk_raid_state": {
                "changed": false,
                "false_condition": "disks.raid_state is defined",
                "skip_reason": "Conditional result was False",
                "skipped": true
            },
            "physical_disk_state": {
                "changed": false,
                "false_condition": "disks.status is defined",
                "skip_reason": "Conditional result was False",
                "skipped": true
            },
            "remove_controller_key": {
                "changed": false,
                "false_condition": "remove_key is true",
                "skip_reason": "Conditional result was False",
                "skipped": true
            },
            "secure_erase": {
                "changed": false,
                "failed": false,
                "msg": "Successfully submitted the job that performs the 'SecureErase' operation.",
                "status": {
                    "ActualRunningStartTime": null,
                    "ActualRunningStopTime": null,
                    "CompletionTime": null,
                    "Description": "Job Instance",
                    "EndTime": "TIME_NA",
                    "Id": "JID_XXXXXXXXXXX",
                    "JobState": "ReadyForExecution",
                    "JobType": "RealTimeNoRebootConfiguration",
                    "Message": "New",
                    "MessageArgs": [],
                    "MessageId": "JCP000",
                    "Name": "Configure: RAID.Integrated.1-1",
                    "PercentComplete": 0,
                    "StartTime": "2024-07-09T01:35:18",
                    "TargetSettingsURI": null
                },
                "task": {
                    "id": "JID_XXXXXXXXXXX",
                    "uri": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/JID_XXXXXXXXXXX"
                }
            },
            "set_controller_key": {
                "changed": false,
                "false_condition": "set_controller_key is true and key is defined and key_id is defined and mode is undefined",
                "skip_reason": "Conditional result was False",
                "skipped": true
            },
            "unassign_hotspare": {
                "changed": false,
                "false_condition": "disks.global_hot_spare is false and disks.id is defined",
                "skip_reason": "Conditional result was False",
                "skipped": true
            }
        }
      </code>
    </pre>
    </td>
<td>Returns the output of the idrac_storage_controller</td>
</tbody>
</table>

## Example Playbook

```
- name: Reset controller configuration
  ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.0
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    reset_config: true
```

```
- name: Set controller attributes
  ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    attributes:
      ControllerMode: HBA
    apply_time: Immediate
```

```
- name: Set controller attributes at maintenance window
  ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    attributes:
      CheckConsistencyMode: Normal
      LoadBalanceMode: Disabled
    apply_time: AtMaintenanceWindowStart
    maintenance_window:
      start_time: "2022-09-30T05:15:40-05:00"
      duration: 1200
```

```
- name: Set controller encryption key
  ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    key: PassPhrase@123
    key_id: MyKeyId123
    set_controller_key: true
```

```
- name: Rekey in LKM mode
    ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    rekey: true
    key: PassPhrase@123
    key_id: mykeyid123
    old_key: OldPhassParse@123
    mode: LKM
```

```
- name: Rekey in SEKM mode
    ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    rekey: true
    key: PassPhrase@123
    key_id: mykeyid123
    old_key: OldPhassParse@123
    mode: SEKM
```

```
- name: Remove controller encryption key
    ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    remove_key: true
```

```
- name: Enable controller encryption
    ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    set_controller_key: true
    key: your_key@123
    key_id: your_keyid@123
    mode: LKM
```

```
- name: Change physical disk state to online
    ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    disks:
      id: Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1
      status: online
```

```
- name: Change physical disk state to offline
    ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    disks:
      id: Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1
      status: offline
```

```
- name: Convert physical disk to RAID mode
    ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    disks:
      id: Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1
      raid_state: raid
```

```
- name: Convert physical disk to Non-RAID mode
    ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    disks:
      id: Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1
      raid_state: nonraid
```

```
- name: Assign dedicated hot spare.
    ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    volumes:
      id: Disk.Virtual.0:RAID.Slot.1-1
      dedicated_hot_spare: Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1
```

```
- name: Assign global hot spare.
    ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    disks:
      id: Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1
      global_hot_spare: true
```

```
- name: Unassign hot spare.
    ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    disks:
      id: Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1
      global_hot_spare: false
```

```
- name: Lock virtual drive.
    ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    volumes:
      id: Disk.Virtual.0:RAID.Slot.1-1
      encrypted: true
```

```
- name: Online capacity expansion of volume using size.
    ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    volumes:
      id: Disk.Virtual.0:RAID.Slot.1-1
      expand_capacity_size: 362785
```

```
- name: Online capacity expansion of volume using target.
    ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    volumes:
      id: Disk.Virtual.0:RAID.Slot.1-1
      expand_capacity_disk: Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1
```

```
- name: Blink virtual drive.
    ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    volumes:
      id: Disk.Virtual.0:RAID.Slot.1-1
      blink: true
```

```
- name: Unblink virtual drive.
    ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    volumes:
      id: Disk.Virtual.0:RAID.Slot.1-1
      blink: false
```

```
- name: Blink physical disk.
    ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    disks:
      id: Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1
      blink: true
```

```
- name: Unblink physical disk.
    ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    ca_path: "/path/to/ca_cert.pem"
    controller_id: RAID.Slot.1-1
    disks:
      id: Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1
      blink: false
```

```
- name: Multiple operations on controller.
    ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    validate_certs: false
    controller_id: RAID.Slot.1-1
    disks:
      id: Disk.Bay.3:Enclosure.Internal.0-1:RAID.Slot.1-1
      global_hot_spare: false
    set_controller_key: true
    key: PassPhrase@12341
    key_id: mykeyid123
    mode: LKM
    attributes:
      CheckConsistencyMode: StopOnError
      CopybackMode: OnWithSMART
    apply_time: Immediate
```

```
- name: Perform secure erase on physical disk.
    ansible.builtin.include_role:
    name: idrac_storage_controller
  vars:
    hostname: 192.168.0.1
    username: username
    password: password
    validate_certs: false
    controller_id: RAID.Slot.1-1
    disks:
      id: Disk.Bay.3:Enclosure.Internal.0-1:RAID.Slot.1-1
      erase: true
```

## Author Information
------------------

Dell Technologies <br>
Felix Stephen Anthuvan (felix_s@dell.com) 2023 <br>
Abhishek Sinha
(Abhishek.Sinha10@dell.com) 2024
