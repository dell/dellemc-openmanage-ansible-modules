# dellemc_idrac_boot_order
Configure BIOS Boot Settings

  * [Synopsis](#Synopsis)
  * [Options](#Options)
  * [Examples](#Examples)

## <a name="Synopsis"></a>Synopsis
 Configure Bios/Uefi Boot Settings
 Changing the boot mode, Bios/Uefi boot sequence will reboot the system

## <a name="Options"></a>Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| share_name  |   yes  |  | |  Network file share (CIFS, NFS)  |
| share_user  |   yes  |  | |  Network share user in the format "user@domain" if user is part of a domain, else "user"  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share specified in I(share_name) with read-write permission for ansible user  |
| boot_mode  |   no  |    | <ul> <li>Bios</li>  <li>Uefi</li> </ul> |  <ul><li>if C(Bios), will set the boot mode to BIOS</li><li>if C(Uefi), will set the boot mode to UEFI</li></ul> <br><strong>NOTE:</strong> Changing the Boot Mode will mmediately restart the server. |
| boot_seq_retry  |   no  |    | <ul> <li>Enabled</li>  <li>Disabled</li> </ul> |  <ul><li>if C(Enabled), and the system fails to boot, the system will re-attempt the boot sequence after 30 seconds</li><li>if C(Disabled), will disable the Boot Sequence retry feature</li></ul>  |
| bios_boot_seq  |   no  |  []  | |  List of boot devices' FQDDs in the sequential order for BIOS Boot Sequence. Please make sure that the boot mode is set to C(Bios) before setting the BIOS boot sequence.  Changing the BIOS Boot Sequence will restart the server  |
| one_time_bios_boot_seq  |   no  |  []  | |  List of boot devices' FQDDs in the sequential order for the One-Time Boot only  |
| uefi_boot_seq  |   no  |  []  | |  List of boot devices' FQDDs in the sequential order for Uefi Boot Sequence. Please make sure that the boot mode is set to C(Uefi) before setting the Uefi boot sequence  |
| one_time_uefi_boot_seq  |   no  |  []  | |  List of boot devices's FQDDs in the sequential order for One-Time Boot only  |
| first_boot_device  |   no  |  Normal  | <ul> <li>BIOS</li>  <li>CD-DVD</li>  <li>F10</li>  <li>F11</li>  <li>FDD</li>  <li>HDD</li>  <li>Normal</li>  <li>PXE</li>  <li>SD</li>  <li>UEFIDevicePath</li>  <li>VCD-DVD</li>  <li>vFDD</li> </ul> |  Sets the boot device for the next boot operations  The system will boot from the selected device on the next and subsequent reboots, and remains as the first boot device in the BIOS boot order, until it is changed again either from the iDRAC Web Interface or from the BIOS boot sequence.  If I(boot_once) is set to C(Enabled), the system boots from the selected device only once. Subsequently, the system boots according to the BIOS Boot sequence.  The C(F11), C(BIOS), C(F10), and C(UEFIDevicePath) options only support boot once, that is, when any of these devices are set as the boot device, the server boots into the selected device and from the second reboot onwards, the system boots as per the boot order. When any of these options are selected, the I(boot_once) option is set to C(Enabled) by default and you cannot disable it.  |
| boot_once  |   |  Enabled  | <ul> <li>Enabled</li>  <li>Disabled</li> </ul> |  <ul><li>if C(Enabled), boots from the selected device only once on next reboot. Subsequently, the system will boot according to Bios/Uefi boot sequence</li><li>if C(Disabled), system will boot from the selected first boot device on next and subsequent reboots</li></ul>  |

## <a name="Examples"></a>Examples

```
# Configure UEFI Boot Mode
- name: Change Boot Mode to UEFI
    dellemc_idrac_boot_order:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      boot_mode:  "Uefi"
```

```
# Configure UEFI Boot Sequence
- name: Configure UEFI Boot Sequence
    dellemc_idrac_boot_order:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      boot_mode:  "Uefi"
      uefi_boot_seq:  ["Optical.SATAEmbedded.E-1", "NIC.Integrated.1-1-1", "NIC.Integrated.1-2-1", "NIC.Integrated.1-3-1", "NIC.Integrated.1-4-1", "HardDisk.List.1-1"]
```

```
- name: Configure First Boot device to PXE
    dellemc_idrac_bot_order:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\192.168.10.10\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      first_boot_device: "PXE"
      boot_once:  "Enabled"
```

---

Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
