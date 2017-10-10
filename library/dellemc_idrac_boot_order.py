#! /usr/bin/python
# _*_ coding: utf-8 _*_
#
# Copyright (c) 2017 Dell Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: dellemc_idrac_boot_order
short_description: Configure BIOS Boot Settings
version_added: "2.3"
description:
    - Configure Bios/Uefi Boot Settings
    - Changing the boot mode, Bios/Uefi boot sequence will reboot the system
options:
  idrac_ip:
    required: True
    description:
      - iDRAC IP Address
  idrac_user:
    required: True
    description:
      - iDRAC user name
  idrac_pwd:
    required: True
    description:
      - iDRAC user password
  idrac_port:
    required: False
    description:
      - iDRAC port
    default: 443
  share_name:
    required: True
    description:
      - Network file share (CIFS, NFS)
  share_user:
    required: True
    description:
      - Network share user in the format "user@domain" if domain is present else "user"
  share_pwd:
    required: True
    description:
      - Network share user password
  share_mnt:
    required: True
    description:
      - Local mount path of the network file share specified in I(share_name) with read-write permission for ansible user
  boot_mode:
    required: False
    choices: ['Bios', 'Uefi']
    description:
      - if C(Bios), will set the boot mode to BIOS
      - if C(Uefi), will set the boot mode to UEFI
    default: 'Bios'
  boot_seq_retry:
    required: False
    choices: ['Enabled', 'Disabled']
    description:
      - if C(Enabled), and the system fails to boot, the system will re-attempt the boot sequence after 30 seconds
      - if C(Disabled), will disable the Boot Sequence retry feature
    default: 'Enabled'
  bios_boot_seq:
    required: False
    description:
      - List of boot devices' FQDDs in the sequential order for BIOS Boot Sequence. Please make sure that the boot mode is set to C(Bios) before setting the BIOS boot sequence.
      - Changing the BIOS Boot Sequence will restart the server
    default: []
  one_time_bios_boot_seq:
    required: False
    description:
      - List of boot devices' FQDDs in the sequential order for the One-Time Boot only
    default: []
  uefi_boot_seq:
    required: False
    description:
      - List of boot devices' FQDDs in the sequential order for Uefi Boot Sequence. Please make sure that the boot mode is set to C(Uefi) before setting the Uefi boot sequence
    default: []
  one_time_uefi_boot_seq:
    required: False
    description:
      - List of boot devices's FQDDs in the sequential order for One-Time Boot only
    default: []
  first_boot_device:
    required: False
    description:
      - Sets the boot device for the next boot operations
      - The system will boot from the selected device on the next and subsequent reboots, and remains as the first boot device in the BIOS boot order, until it is changed again either from the iDRAC Web Interface or from the BIOS boot sequence.
      - If I(boot_once) is set to C(Enabled), the system boots from the selected device only once. Subsequently, the system boots according to the BIOS Boot sequence.
      - The C(F11), C(BIOS), C(F10), and C(UEFIDevicePath) options only support boot once, that is, when any of these devices are set as the boot device, the server boots into the selected device and from the second reboot onwards, the system boots as per the boot order. When any of these options are selected, the I(boot_once) option is set to C(Enabled) by default and you cannot disable it.
    choices: ['BIOS', 'CD-DVD', 'F10', 'F11', 'FDD', 'HDD', 'Normal', 'PXE', 'SD', 'UEFIDevicePath', 'VCD-DVD', 'vFDD']
    default: 'Normal'
  boot_once:
    rquired: False
    description:
      - if C(Enabled), boots from the selected device only once on next reboot. Subsequently, the system will boot according to Bios/Uefi boot sequence
      - if C(Disabled), system will boot from the selected first boot device on next and subsequent reboots
    choices: ['Enabled', 'Disabled']
    default: 'Enabled'

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
'''

EXAMPLES = '''
# Configure UEFI Boot Sequence
- name: Change Boot Mode to UEFI
    dellemc_idrac_boot_order:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      boot_mode:  "Uefi"

- name: Configure UEFI Boot Sequence
    dellemc_idrac_boot_order:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      boot_mode:  "Uefi"
      uefi_boot_seq:  ["Optical.SATAEmbedded.E-1", "NIC.Integrated.1-1-1", "NIC.Integrated.1-2-1", "NIC.Integrated.1-3-1", "NIC.Integrated.1-4-1", "HardDisk.List.1-1"]

- name: Configure First Boot device to PXE
    dellemc_idrac_bot_order:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      first_boot_device: "PXE"
      boot_once:  "Enabled"

'''

RETURN = '''
---
'''

import traceback
from ansible.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
try:
    from omsdk.sdkcenum import TypeHelper
    from omdrivers.enums.iDRAC.BIOS import BootModeTypes, BootSeqRetryTypes
    from omdrivers.enums.iDRAC.iDRAC import (
        FirstBootDevice_ServerBootTypes, BootOnce_ServerBootTypes
    )
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False


def setup_bios_boot_settings(idrac, module):
    """
    Configure Boot Order parameters on PowerEdge Servers

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    error = False

    try:
        current_boot_mode = idrac.config_mgr._sysconfig.BIOS.BootMode

        # Boot Mode - reboot imminent
        if module.params['boot_mode']:
            idrac.config_mgr._sysconfig.BIOS.BootMode = \
                TypeHelper.convert_to_enum(module.params['boot_mode'],
                                           BootModeTypes)

        # Boot Seq retry
        idrac.config_mgr._sysconfig.BIOS.BootSeqRetry = \
            TypeHelper.convert_to_enum(module.params['boot_seq_retry'],
                                       BootSeqRetryTypes)

        # BIOS Boot Sequence - reboot imminent
        if module.params['bios_boot_seq']:
            bios_boot_seq = ", ".join([item for item in \
                module.params['bios_boot_seq'] if item.strip()])

            if bios_boot_seq:
                idrac.config_mgr._sysconfig.BIOS.BiosBootSeq = bios_boot_seq

        # One Time BIOS Boot Sequence - reboot imminent
        if module.params['one_time_bios_boot_seq']:
            one_time_bios_boot_seq = ", ".join([item for item in \
                module.params['one_time_bios_boot_seq'] if item.strip()])

            if one_time_bios_boot_seq:
                idrac.config_mgr._sysconfig.BIOS.OneTimeBiosBootSeq = one_time_bios_boot_seq

        # Uefi Boot Sequence - reboot imminent
        if module.params['uefi_boot_seq']:
            uefi_boot_seq = ", ".join([item for item in \
                module.params['uefi_boot_seq'] if item.strip()])

            if uefi_boot_seq:
                idrac.config_mgr._sysconfig.BIOS.UefiBootSeq = uefi_boot_seq

        # One Time Uefi Boot Sequence - reboot imminent
        if module.params['one_time_uefi_boot_seq']:
            one_time_uefi_boot_seq = ", ".join([item for item in \
                module.params['one_time_uefi_boot_seq'] if item.strip()])
            if one_time_uefi_boot_seq:
                idrac.config_mgr._sysconfig.BIOS.OneTimeUefiBootSeq = one_time_uefi_boot_seq

        # First boot device
        idrac.config_mgr._sysconfig.iDRAC.ServerBoot.FirstBootDevice_ServerBoot = \
            TypeHelper.convert_to_enum(module.params['first_boot_device'],
                                       FirstBootDevice_ServerBootTypes)

        # Boot Once
        boot_once = TypeHelper.convert_to_enum(module.params['boot_once'],
                                               BootOnce_ServerBootTypes)
        if module.params['first_boot_device'] in ['BIOS', 'F10', 'F11', 'UEFIDevicePath']:
            boot_once = TypeHelper.convert_to_enum('Enabled', BootOnce_ServerBootTypes)
        idrac.config_mgr._sysconfig.iDRAC.ServerBoot.BootOnce_ServerBoot = boot_once

        msg['changed'] = idrac.config_mgr._sysconfig.is_changed()

        if module.check_mode:
            # since it is running in check mode, reject the changes
            idrac.config_mgr._sysconfig.reject()
        else:
            msg['msg'] = idrac.config_mgr.apply_changes()

            if "Status" in msg['msg'] and msg['msg']['Status'] != "Success":
                msg['failed'] = True
                msg['changed'] = False

    except Exception as err:
        error = True
        msg['msg'] = "Error: %s" % str(err)
        msg['exception'] = traceback.format_exc()
        msg['failed'] = True

    return msg, error

# Main
def main():

    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC handle
            idrac=dict(required=False, type='dict'),

            # iDRAC Credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_pwd=dict(required=True, type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Network File Share
            share_name=dict(required=True, type='str'),
            share_user=dict(required=True, type='str'),
            share_pwd=dict(required=True, type='str', no_log=True),
            share_mnt=dict(required=True, type='path'),

            boot_mode=dict(required=False, choices=['Bios', 'Uefi'],
                           default=None, type='str'),
            boot_seq_retry=dict(required=False, choices=['Enabled', 'Disabled'],
                                default='Enabled', type='str'),
            bios_boot_seq=dict(required=False, default=[], type='list'),
            one_time_bios_boot_seq=dict(required=False, default=[], type='list'),
            uefi_boot_seq=dict(required=False, default=[], type='list'),
            one_time_uefi_boot_seq=dict(required=False, default=[], type='list'),
            first_boot_device=dict(required=False,
                                   choices=['BIOS', 'CD-DVD', 'F10', 'F11',
                                            'FDD', 'HDD', 'Normal', 'PXE', 'SD',
                                            'UEFIDevicePath', 'VCD-DVD', 'vFDD'],
                                   default='Normal', type='str'),
            boot_once=dict(required=False, choices=['Enabled', 'Disabled'],
                           default='Disabled', type='str')
        ),
        mutually_exclusive=[
            ["bios_boot_seq", "uefi_boot_seq"]
        ],
        supports_check_mode=True)

    if not HAS_OMSDK:
        module.fail_json(msg="Dell EMC OpenManage Python SDK required for this module")

    # Connect to iDRAC
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    # Setup network share as local mount
    if not idrac_conn.setup_nw_share_mount():
        module.fail_json(msg="Failed to setup network share local mount point")

    # Setup BIOS
    msg, err = setup_bios_boot_settings(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()
