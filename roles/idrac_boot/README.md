# idrac_boot

Role to configure the boot order settings

## Requirements

### Development
Requirements to develop and contribute to the role
```
ansible
docker
molecule
python
```

### Production
Requirements to use the role
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
    <td>boot_options</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>list</td>
    <td>- Options to enable or disable the boot devices.<br>- This is mutually exclusive with I(boot_order), I(boot_source_override_mode), I(boot_source_override_enabled), I(boot_source_override_target), and I(uefi_target_boot_source_override).</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;boot_option_reference</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- FQDD of the boot device.<br>- This is mutually exclusive with I(display_name).</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;display_name</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Display name of the boot source device.<br>- This is mutually exclusive with I(boot_option_reference).</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;enabled</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>bool</td>
    <td>- Enable or disable the boot device.</td>
  </tr>
  <tr>
    <td>boot_order</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>list</td>
    <td>- This option allows to set the boot devices in the required boot order sequence.<br>- This is mutually exclusive with I(boot_options).</td>
  </tr>
  <tr>
    <td>boot_source_override_mode</td>
    <td>false</td>
    <td></td>
    <td>'legacy', 'uefi'</td>
    <td>str</td>
    <td>- The BIOS boot mode (either Legacy or UEFI) to be used when I(boot_source_override_target) boot source is booted.<br>- C(legacy) The system boot in non-UEFI(Legacy) boot mode to the I(boot_source_override_target).<br>- C(uefi) The system boot in UEFI boot mode to the I(boot_source_override_target).<br>- This is read-only property for iDRAC 17G and later.<br>- This is mutually exclusive with I(boot_options).</td>
  </tr>
  <tr>
    <td>boot_source_override_enabled</td>
    <td>false</td>
    <td></td>
    <td>'continuous', 'disabled', 'once'</td>
    <td>str</td>
    <td>- The state of the Boot Source Override feature.<br>- C(disabled), the system boots normally.<br>- C(once), the system boots 1 time to the I(boot_source_override_target).<br>- C(continuous), the system boots to the target specified in the I(boot_source_override_target) until this property is set to Disabled.<br>- The state is set to C(once) for the 1 time boot override and C(continuous) for the remain-active-until—cancelled override. If the state is set C(once) or C(continuous), the value is reset to C(disabled) after the I(boot_source_override_target) actions have completed successfully.<br>- Changes to these options do not alter the BIOS persistent boot order configuration.<br>- This is mutually exclusive with I(boot_options).</td>
  </tr>
  <tr>
    <td>boot_source_override_target</td>
    <td>false</td>
    <td></td>
    <td>'uefi_http', 'sd_card', 'uefi_target', 'utilities', 'bios_setup', 'hdd', 'cd', 'floppy', 'pxe', 'none'</td>
    <td>str</td>
    <td>- The boot source override targets the device to use during the next boot instead of the normal boot device.<br>- C(pxe) performs PXE boot from the primary NIC.<br>- C(floppy), C(cd), C(hdd), and C(sd_card) performs boot from their devices respectively.<br>- C(bios_setup) performs boot into the native BIOS setup.<br>- C(uefi_http) performs boot from a URI over HTTP.<br>- C(utilities) performs boot from the local utilities.<br>- C(uefi_target) performs boot from the UEFI device path found in I(uefi_target_boot_source_override).<br>- C(none) if the I(boot_source_override_target) is set to a value other than C(none) then the I(boot_source_override_enabled) is automatically set to C(once) if I(boot_source_override_enabled) is not provided.<br>- Changes to these options do not alter the BIOS persistent boot order configuration.<br>- This is required if I(boot_source_override_enabled) is C(once) or C(continuous) for iDRAC 17G and later.<br>- This is mutually exclusive with I(boot_options).</td>
  </tr>
  <tr>
    <td>uefi_target_boot_source_override</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- The UEFI device path of the device from which to boot when I(boot_source_override_target) is C(uefi_target).<br>- If I(boot_source_override_target) is set to C(uefi_target), then I(boot_source_override_enabled) cannot be set to c(continuous) because this setting is defined in UEFI as a one-time-boot setting.<br>- Changes to these options do not alter the BIOS persistent boot order configuration.<br>- This is required if I(boot_source_override_target) is C(uefi_target).<br>- This is mutually exclusive with I(boot_options).</td>
  </tr>
  <tr>
    <td>reset_type</td>
    <td>false</td>
    <td>graceful_restart</td>
    <td>'graceful_restart', 'force_restart', 'none'</td>
    <td>str</td>
    <td>- C(none) Host system is not rebooted and I(job_wait) is not applicable.<br>- C(force_restart) Forcefully reboot the Host system.<br>- C(graceful_restart) Gracefully reboot the Host system.</td>
  </tr>
  <tr>
    <td>job_wait</td>
    <td>false</td>
    <td>true</td>
    <td></td>
    <td>bool</td>
    <td>- Provides the option to wait for job completion.<br>- This is applicable when I(reset_type) is C(force_reset) or C(graceful_reset).</td>
  </tr>
  <tr>
    <td>job_wait_timeout</td>
    <td>false</td>
    <td>900</td>
    <td></td>
    <td>int</td>
    <td>- The maximum wait time of I(job_wait) in seconds. The job is tracked only for this duration.<br>- This option is applicable when I(job_wait) is C(True).</td>
  </tr>
  <tr>
    <td>resource_id</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Redfish ID of the resource.</td>
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
      <td>idrac_boot_out</td>
      <td>{
    "boot": {
        "BootOptions": {
            "Description": "Collection of BootOptions",
            "Members": [
                {
                    "BootOptionEnabled": true,
                    "BootOptionReference": "Boot0005",
                    "Description": "Current settings of the UEFI Boot option",
                    "DisplayName": "Integrated RAID Controller 1: VMware ESXi",
                    "Id": "Boot0005",
                    "Name": "Uefi Boot Option",
                    "UefiDevicePath": "HD(1,GPT,740C46A9-4A43-47AA-9C09-65E821376E48,0x40,0x32000)/\\EFI\\VMware\\safeboot64.efi"
                },
                {
                    "BootOptionEnabled": false,
                    "BootOptionReference": "Boot0004",
                    "Description": "Current settings of the UEFI Boot option",
                    "DisplayName": "Unavailable: Windows Boot Manager",
                    "Id": "Boot0004",
                    "Name": "Uefi Boot Option",
                    "UefiDevicePath": "HD(1,GPT,AEB2A96B-5C31-4F8F-9927-B48B08D907BE,0x800,0xF9800)/\\EFI\\Microsoft\\Boot\\bootmgfw.efi"
                },
                {
                    "BootOptionEnabled": true,
                    "BootOptionReference": "Boot0006",
                    "Description": "Current settings of the UEFI Boot option",
                    "DisplayName": "Unavailable: Red Hat Enterprise Linux",
                    "Id": "Boot0006",
                    "Name": "Uefi Boot Option",
                    "UefiDevicePath": "HD(1,GPT,14759088-1AE7-4EA4-A60B-BE82546E21B6,0x800,0x12C000)/\\EFI\\redhat\\shimx64.efi"
                },
                {
                    "BootOptionEnabled": true,
                    "BootOptionReference": "Boot0003",
                    "Description": "Current settings of the UEFI Boot option",
                    "DisplayName": "Unavailable: Rocky Linux",
                    "Id": "Boot0003",
                    "Name": "Uefi Boot Option",
                    "UefiDevicePath": "HD(1,GPT,ADC59C44-A0D3-4917-9376-33EE44DE96F0,0x800,0x12C000)/\\EFI\\rocky\\shimx64.efi"
                }
            ],
            "Name": "Boot Options Collection"
        },
        "BootOrder": [
            "Boot0005",
            "Boot0004",
            "Boot0006",
            "Boot0003"
        ],
        "BootSourceOverrideEnabled": "Disabled",
        "BootSourceOverrideMode": "UEFI",
        "BootSourceOverrideTarget": "None",
        "UefiTargetBootSourceOverride": null
    },
    "job": {
        "ActualRunningStartTime": "2023-06-19T09:48:41",
        "ActualRunningStopTime": "2023-06-19T09:51:53",
        "CompletionTime": "2023-06-19T09:51:53",
        "Description": "Job Instance",
        "EndTime": "TIME_NA",
        "Id": "JID_871679370016",
        "JobState": "Completed",
        "JobType": "BIOSConfiguration",
        "Message": "Job completed successfully.",
        "MessageArgs": [],
        "MessageId": "PR19",
        "Name": "Configure: BIOS.Setup.1-1",
        "PercentComplete": 100,
        "StartTime": "2023-06-19T09:45:36",
        "TargetSettingsURI": null
    },
    "msg": "Successfully updated the boot settings."
}</td>
      <td>Role output of the idrac_boot job.</td>
    </tr>
  </tbody>
</table>

## Example Playbook

```
- name: Configure the system boot options settings.
  ansible.builtin.include_role:
    name: dellemc.openmanage.idrac_boot
  vars:
    hostname: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    boot_options:
      - display_name: Hard drive C
        enabled: true
      - boot_option_reference: NIC.PxeDevice.2-1
        enabled: true
```

```
- name: Configure the boot order settings.
  ansible.builtin.include_role:
    name: dellemc.openmanage.idrac_boot
  vars:
    hostname: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    boot_order:
      - Boot0001
      - Boot0002
      - Boot0004
      - Boot0003
```

```
- name: Configure the boot source override mode.
  ansible.builtin.include_role:
    name: dellemc.openmanage.idrac_boot
  vars:
    hostname: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    boot_source_override_mode: legacy
    boot_source_override_target: cd
    boot_source_override_enabled: once
```

```
- name: Configure the UEFI target settings.
  ansible.builtin.include_role:
    name: dellemc.openmanage.idrac_boot
  vars:
    hostname: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    boot_source_override_mode: uefi
    boot_source_override_target: uefi_target
    uefi_target_boot_source_override: "VenHw(3A191845-5F86-4E78-8FCE-C4CFF59F9DAA)"
```

```
- name: Configure the boot source override mode as pxe.
  ansible.builtin.include_role:
    name: dellemc.openmanage.idrac_boot
  vars:
    hostname: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    boot_source_override_mode: legacy
    boot_source_override_target: pxe
    boot_source_override_enabled: continuous
```

Author Information
------------------

Dell Technologies <br>
Felix Stephen (felix_s@dell.com) 2023
