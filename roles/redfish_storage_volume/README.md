# redfish_storage_volume

Role to create, modify, initialize, or delete a single storage volume.

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
    <td>controller_id</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Fully Qualified Device Descriptor (FQDD) of the storage controller.For example- RAID.Slot.1-1.</br>This option is mandatory when I(state) is C(present) while creating a volume.</td>
  </tr>
  <tr>
    <td>volume_id</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- FQDD of existing volume.For example- Disk.Virtual.4:RAID.Slot.1-1. </br>- This option is mandatory in the following scenarios, I(state) is C(present), when updating a volume. I(state) is C(absent), when deleting a volume.I(command) is C(initialize), when initializing a volume.</td>
  </tr>
  <tr>
    <td>state</td>
    <td>false</td>
    <td>present</td>
    <td>[present, absent]</td>
    <td>str</td>
    <td>- C(present) creates a storage volume for the specified I (controller_id), or modifies the storage volume for the specified I (volume_id). "Note: Modification of an existing volume properties depends on drive and controller capabilities". </br> C(absent) deletes the volume for the specified I(volume_id).</td>
  </tr>
  <tr>
    <td>command</td>
    <td>false</td>
    <td></td>
    <td>[initialize]</td>
    <td>str</td>
    <td>- C(initialize) initializes an existing storage volume for a specified I(volume_id).</td>
  </tr>
  <tr>
    <td>raid_type</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- One of the following raid types must be selected to create a volume.</br>
        -  C(RAID0) to create a RAID0 type volume.</br>
        -  C(RAID1) to create a RAID1 type volume.</br>
        -  C(RAID5) to create a RAID5 type volume.</br>
        -  C(RAID6) to create a RAID6 type volume.</br>
        -  C(RAID10) to create a RAID10 type volume.</br>
        -  C(RAID50) to create a RAID50 type volume.</br>
        -  C(RAID60) to create a RAID60 type volume.</td>
  </tr>
  <tr>
    <td>name</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Name of the volume to be created.</br>
- Only applicable when I(state) is C(present).</br>
- This will be deprecated. Please use I(volume_name) for specifying the volume name.</td>
  </tr>
  <tr>
    <td>volume_name</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Name of the volume to be created.</br>
- Only applicable when I(state) is C(present).</td>
  </tr>
  <tr>
    <td>drives</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>list</td>
    <td>- FQDD of the Physical disks. For example- Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1. </br>- Only applicable when I(state) is C(present) when creating a new volume.</td>
  </tr>
  <tr>
    <td>block_size_bytes</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>int</td>
    <td>- Block size in bytes.Only applicable when I(state) is C(present).</td>
  </tr>
  </tr>
    <tr>
    <td>capacity_bytes</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Volume size in bytes.</br>- Only applicable when I(state) is C(present).</td>
  </tr>
  <tr>
    <td>optimum_io_size_bytes</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Stripe size value must be in multiples of 64 * 1024.</br>- Only applicable when I(state) is C(present).</td>
  </tr>
  <tr>
    <td>encryption_types</td>
    <td>false</td>
    <td></td>
    <td>[NativeDriveEncryption, ControllerAssisted, SoftwareAssisted]</td>
    <td>str</td>
    <td>- The following encryption types can be selected.</br>
C(ControllerAssisted) The volume is encrypted by the storage controller entity.</br>
C(NativeDriveEncryption) The volume utilizes the native drive encryption capabilities of the drive hardware.</br>
C(SoftwareAssisted) The volume is encrypted by the software running on the system or the operating system.</br>
Only applicable when I(state) is C(present).</td>
  </tr>
  <tr>
    <td>encrypted</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>bool</td>
    <td>- Indicates whether volume is currently utilizing encryption or not.</br>- Only applicable when I(state) is C(present).</td>
  </tr>
  <tr>
    <td>oem</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>dict</td>
    <td>- Includes OEM extended payloads.</br>- Only applicable when I(state) is I(present).</td>
  </tr>
  <tr>
    <td>initialize_type</td>
    <td>false</td>
    <td>Fast</td>
    <td>[Fast, Slow]</td>
    <td>str</td>
    <td>- Initialization type of existing volume.</br> Only applicable when I(command) is C(initialize).</td>
  </tr>
  <tr>
    <td>job_wait</td>
    <td>false</td>
    <td>true</td>
    <td></td>
    <td>bool</td>
    <td>- Determines whether to wait for the job completion or not.</td>
  </tr>
  <tr>
    <td>job_wait_timeout</td>
    <td>false</td>
    <td></td>
    <td>300</td>
    <td>int</td>
    <td>- The maximum wait time of I(job_wait) in seconds. The job is tracked only for this duration.</br>- This option is applicable when I(job_wait) is C(True).</td>
  </tr>
  <tr>
    <td>apply_time</td>
    <td>false</td>
    <td></td>
    <td>[Immediate, OnReset]</td>
    <td>str</td>
    <td>- Apply time of the Volume configuration.</br>
- C(Immediate) allows you to apply the volume configuration on the host server immediately and apply the changes. This is applicable for I(job_wait).</br>
- C(OnReset) allows you to apply the changes on the next reboot of the host server.</br>
- I(apply_time) has a default value based on the different types of the controller.</br>
- For example, BOSS-S1 and BOSS-N1 controllers have a default value of I(apply_time) as C(OnReset).</br>
- PERC controllers have a default value of I(apply_time) as C(Immediate).</td>
  </tr>
  <tr>
    <td>reboot_server</td>
    <td></td>
    <td>false</td>
    <td></td>
    <td>bool</td>
    <td>- Reboot the server to apply the changes.</br>
- I(reboot_server) is applicable only when I(apply_timeout) is C(OnReset) or when the default value for the apply time of the controller is C(OnReset).</td>
  </tr>
  <tr>
    <td>force_reboot</td>
    <td></td>
    <td>false</td>
    <td></td>
    <td>bool</td>
    <td>- Reboot the server forcefully to apply the changes when the normal reboot fails.</br>
- I(force_reboot) is applicable only when I(reboot_server) is C(true).</td>
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
      <td>redfish_storage_volume_out</td>
      <td>{"changed": true,
        "failed": false,
         "msg": "Successfully submitted create volume task."
}</td>
<td>Module output of the redfish storage volume</td>
</tbody>
</table>

## Examples

---

```yml
- name: Create a volume with supported options
  ansible.builtin.include_role:
    name: redfish_storage_volume
  vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    state: "present"
    raid_type: "RAID1"
    volume_name: "VD0"
    controller_id: "RAID.Slot.1-1"
    drives:
      - Disk.Bay.5:Enclosure.Internal.0-1:RAID.Slot.1-1
      - Disk.Bay.6:Enclosure.Internal.0-1:RAID.Slot.1-1
    block_size_bytes: 512
    capacity_bytes: 299439751168
    optimum_io_size_bytes: 65536
    encryption_types: NativeDriveEncryption
    encrypted: true
```

```yml
- name: Create a volume with apply time
  ansible.builtin.include_role:
    name: redfish_storage_volume
  vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    state: "present"
    raid_type: "RAID6"
    volume_name: "Raid6_VD"
    controller_id: "RAID.Slot.1-1"
    drives:
      - Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1
      - Disk.Bay.2:Enclosure.Internal.0-1:RAID.Slot.1-1
      - Disk.Bay.5:Enclosure.Internal.0-1:RAID.Slot.1-1
      - Disk.Bay.6:Enclosure.Internal.0-1:RAID.Slot.1-1
    apply_time: OnReset
    reboot_server: true
    force_reboot: true
```

```yml
- name: Create a volume with minimum options
  ansible.builtin.include_role:
    name: redfish_storage_volume
  vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    state: "present"
    controller_id: "RAID.Slot.1-1"
    raid_type: "RAID0"
    drives:
       - Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.1-1
```

```yml
- name: Modify a volume's encryption type settings
  ansible.builtin.include_role:
    name: redfish_storage_volume
  vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    state: "present"
    volume_id: "Disk.Virtual.5:RAID.Slot.1-1"
    encryption_types: "ControllerAssisted"
    encrypted: true
```

```yml
- name: Delete an existing volume
  ansible.builtin.include_role:
    name: redfish_storage_volume
  vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    state: "absent"
    volume_id: "Disk.Virtual.5:RAID.Slot.1-1"
```

```yml
- name: Initialize an existing volume
  ansible.builtin.include_role:
    name: redfish_storage_volume
  vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    command: "initialize"
    volume_id: "Disk.Virtual.6:RAID.Slot.1-1"
    initialize_type: "Slow"
```
## Author Information

---

Dell Technologies <br>
Kritika Bhateja (Kritika.Bhateja@Dell.com) 2023
