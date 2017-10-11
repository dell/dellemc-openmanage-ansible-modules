#! /usr/bin/python
# _*_ coding: utf-8 _*_
#
# Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved.
# Dell, EMC, and other trademarks are trademarks of Dell Inc. or its
# subsidiaries. Other trademarks may be trademarks of their respective owners.

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
    type: 'str'
  idrac_user:
    required: True
    description:
      - iDRAC user name
    type: 'str'
  idrac_pwd:
    required: True
    description:
      - iDRAC user password
    type: 'str'
  idrac_port:
    required: False
    description:
      - iDRAC port
    default: 443
    type: 'int'
  share_name:
    required: True
    description:
      - Network file share (CIFS, NFS)
    type: 'str'
  share_user:
    required: True
    description:
      - Network share user in the format "user@domain" if user is part of a domain else "user"
    type: 'str'
  share_pwd:
    required: True
    description:
      - Network share user password
    type: 'str'
  share_mnt:
    required: True
    description:
      - Local mount path of the network file share specified in I(share_name) with read-write permission for ansible user
    type: 'path'
  boot_mode:
    required: False
    choices: ['Bios', 'Uefi']
    description:
      - if C(Bios), will set the boot mode to BIOS
      - if C(Uefi), will set the boot mode to UEFI
    default: None
  boot_seq_retry:
    required: False
    choices: ['Enabled', 'Disabled']
    description:
      - if C(Enabled), and the system fails to boot, the system will re-attempt the boot sequence after 30 seconds
      - if C(Disabled), will disable the Boot Sequence retry feature
    default: None
  bios_boot_seq:
    required: False
    description:
      - List of boot devices' FQDDs in the sequential order for BIOS Boot Sequence. Please make sure that the boot mode is set to C(Bios) before setting the BIOS boot sequence.
      - Changing the BIOS Boot Sequence will restart the server
    default: []
    type: 'list'
  one_time_bios_boot_seq:
    required: False
    description:
      - List of boot devices' FQDDs in the sequential order for the One-Time Boot only
    default: []
    type: 'list'
  uefi_boot_seq:
    required: False
    description:
      - List of boot devices' FQDDs in the sequential order for Uefi Boot Sequence. Please make sure that the boot mode is set to C(Uefi) before setting the Uefi boot sequence
    default: []
    type: 'list'
  one_time_uefi_boot_seq:
    required: False
    description:
      - List of boot devices's FQDDs in the sequential order for One-Time Boot only
    default: []
    type: 'list'
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


def _filter_sequence(new_seq_list, old_seq_str):

    old_seq_list = []
    new_seq = []
    new_seq_str = ''

    if old_seq_str:
        old_seq_list = map(str.strip, [item for item in old_seq_str.split(',') if item])
        new_seq = [item for item in new_seq_list if item in old_seq_list]
        new_seq.extend([item for item in old_seq_list if item not in new_seq])

    if new_seq:
        new_seq_str = ", ".join([item for item in new_seq if item.strip()])

    return new_seq_str


def _setup_boot_mode(idrac, module):
    """
    Setup boot mode - reboot is imminent if you change the boot mode

    Keyword arguments:
    idrac  -- idrac, module
    module -- Ansible module
    """

    if module.params['boot_mode']:
        idrac.config_mgr._sysconfig.BIOS.BootMode = TypeHelper.convert_to_enum(
            module.params['boot_mode'], BootModeTypes)


def _setup_hdd_seq(idrac, module):

    if module.params['hdd_seq']:
        hdd_seq = _filter_sequence(module.params['hdd_seq'],
                                   idrac.config_mgr._sysconfig.BIOS.HddSeq.get_value())

        if hdd_seq:
            idrac.config_mgr._sysconfig.BIOS.HddSeq = hdd_seq

    if module.params['one_time_hdd_seq']:
        one_time_hdd_seq = _filter_sequence(module.params['one_time_hdd_seq'],
                                            idrac.config_mgr._sysconfig.BIOS.OneTimeHddSeq)

        if one_time_hdd_seq:
            idrac.config_mgr._sysconfig.BIOS.OneTimeHddSeq = one_time_hdd_seq


def _setup_bios_boot_settings(idrac, module):

    if module.params['bios_boot_seq']:
        bios_boot_seq = _filter_sequence(module.params['bios_boot_seq'],
                                         idrac.config_mgr._sysconfig.BIOS.BiosBootSeq.get_value())

        if bios_boot_seq:
            idrac.config_mgr._sysconfig.BIOS.BiosBootSeq = bios_boot_seq

    if module.params['one_time_bios_boot_seq']:
        one_time_boot_seq = _filter_sequence(
            module.params['one_time_bios_boot_seq'],
            idrac.config_mgr._sysconfig.BIOS.OneTimeBiosBootSeq.get_value())

        if one_time_boot_seq:
            idrac.config_mgr._sysconfig.BIOS.OneTimeBiosBootSeq = one_time_boot_seq


def _setup_uefi_boot_settings(idrac, module):

    if module.params['uefi_boot_seq']:
        uefi_boot_seq = _filter_sequence(module.params['uefi_boot_seq'],
                                         idrac.config_mgr._sysconfig.BIOS.UefiBootSeq.get_value())

        if uefi_boot_seq:
            idrac.config_mgr._sysconfig.BIOS.UefiBootSeq = uefi_boot_seq

    if module.params['one_time_uefi_boot_seq']:
        one_time_uefi_boot_seq = _filter_sequence(
            module.params['one_time_uefi_boot_seq'],
            idrac.config_mgr._sysconfig.BIOS.OneTimeUefiBootSeq.get_value())

        if one_time_uefi_boot_seq:
            idrac.config_mgr._sysconfig.BIOS.OneTimeUefiBootSeq = one_time_uefi_boot_seq


def _setup_idrac_boot_settings(idrac, module):

    # First boot device
    first_boot_device = module.params['first_boot_device']
    if first_boot_device:
        idrac.config_mgr._sysconfig.iDRAC.ServerBoot.FirstBootDevice_ServerBoot = \
            TypeHelper.convert_to_enum(first_boot_device,
                                       FirstBootDevice_ServerBootTypes)

    # Boot Once
    boot_once = TypeHelper.convert_to_enum(module.params['boot_once'],
                                           BootOnce_ServerBootTypes)
    if first_boot_device and first_boot_device in ['BIOS', 'F10', 'F11', 'UEFIDevicePath']:
        boot_once = TypeHelper.convert_to_enum('Enabled', BootOnce_ServerBootTypes)
    idrac.config_mgr._sysconfig.iDRAC.ServerBoot.BootOnce_ServerBoot = boot_once


def setup_boot_settings(idrac, module):
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
        curr_boot_mode = idrac.config_mgr._sysconfig.BIOS.BootMode

        # Boot Mode - reboot imminent
        _setup_boot_mode(idrac, module)

        # Boot Seq retry
        if module.params['boot_seq_retry']:
            idrac.config_mgr._sysconfig.BIOS.BootSeqRetry = \
                TypeHelper.convert_to_enum(module.params['boot_seq_retry'],
                                           BootSeqRetryTypes)

        # Setup HDD Sequence
        _setup_hdd_seq(idrac, module)

        # Setup BIOS Boot Settings
        if curr_boot_mode == BootModeTypes.Bios:
            _setup_bios_boot_settings(idrac, module)

        # Setup Uefi Boot Settings
        if curr_boot_mode == BootModeTypes.Uefi:
            _setup_uefi_boot_settings(idrac, module)

        # Setup iDRAC Boot configuration parameters
        _setup_idrac_boot_settings(idrac, module)

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
                                default=None, type='str'),
            bios_boot_seq=dict(required=False, default=[], type='list'),
            one_time_bios_boot_seq=dict(required=False, default=[], type='list'),
            uefi_boot_seq=dict(required=False, default=[], type='list'),
            one_time_uefi_boot_seq=dict(required=False, default=[], type='list'),
            hdd_seq=dict(required=False, default=[], type='list'),
            one_time_hdd_seq=dict(required=False, default=[], type='list'),
            first_boot_device=dict(required=False,
                                   choices=['BIOS', 'CD-DVD', 'F10', 'F11',
                                            'FDD', 'HDD', 'Normal', 'PXE', 'SD',
                                            'UEFIDevicePath', 'VCD-DVD', 'vFDD'],
                                   default='Normal', type='str'),
            boot_once=dict(required=False, choices=['Enabled', 'Disabled'],
                           default='Enabled', type='str')
        ),
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
    msg, err = setup_boot_settings(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()
