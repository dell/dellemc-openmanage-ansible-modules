#!/usr/bin/python
# _*_ coding: utf-8 _*_

#
# Dell EMC OpenManage Ansible Modules
# Version 1.0
# Copyright (C) 2018 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc.
# or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#


from __future__ import (absolute_import, division, print_function)


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_idrac_storage_volume
short_description: Configures the RAID configuration attributes.
version_added: "2.4"
description:
    - This module is responsible for configuring the RAID attributes.
options:
    idrac_ip:
        required: True
        description: iDRAC IP Address.
    idrac_user:
        required: True
        description: iDRAC username.
    idrac_pwd:
        required: True
        description: iDRAC user password.
    idrac_port:
        required: False
        description: iDRAC port.
        default: 443
    span_depth:
        required: False
        description: Span Depth.
        default: 1
    span_length:
        required: False
        description: Span Length.
        default: 1
    number_dedicated_hot_spare:
        required: False
        description: Number of Dedicated Hot Spare.
        default: 0 
    raid_level:
        required: False
        description: Provide the the required RAID level.
        choices: ['RAID 0', 'RAID 1', 'RAID 5', 'RAID 6', 'RAID 10', 'RAID 50', 'RAID 60']
        default: "RAID 0"
    disk_cache_policy:
        required: False
        description: Disk Cache Policy.
        choices: ["Default", "Enabled", "Disabled"]
        default: Default
    write_cache_policy:
        required: False
        description: Write cache policy.
        choices: ["WriteThrough", "WriteBack", "WriteBackForce"]
        default: WriteThrough
    read_cache_policy:
        required: False
        description: Read cache policy.
        choices: ["NoReadAhead", "ReadAhead", "AdaptiveReadAhead"]
        default: NoReadAhead
    stripe_size:
        required: False
        description: Stripe size value to be provided in multiples of 64 * 1024.
        default: 65536
    controller_fqdd:
        required: False
        description: Fully Qualified Device Descriptor (FQDD) of 
            the storage controller, for e.g. 'RAID.Integrated.1-1'.
            Controller FQDD is required for C(create) RAID configuration.
        default: None
    vd_fqdd:
        required: False
        description: Fully Qualified Device Descriptor (FQDD) of 
            the virtual disk, for e.g. 'Disk.virtual.0:RAID.Slot.1-1'.
            This option is used to get the virtual disk information.
        default: None
    media_type:
        required:  False
        description: Media type.
        choices: ['HDD', 'SSD']
        default: None
    bus_protocol:
        required:  False
        description: Bus protocol.
        choices: ['SAS', 'SATA']
        default: None
    state:
        required: True
        description:
          - If C(create), will perform create operations.
          - If C(delete), will perform remove operations.
          - If C(view), will return storage view.
        choices: ['create', 'delete', 'view']
        default: 'view'
    vd_values:
        required: False
        description: A list of virtual disk specific iDRAC attributes.
            This is applicable for C(create) and C(delete) operations.
            - For C(create) operation, vd_name and pd_slots are applicable options,
                other volume options can also be specified.
            - For C(delete) operation, only vd_name option is applicable.
            See the examples for more details. 
    size:
        required: False
        description: Virtual disk size in GB.
    raid_reset_config:
        required: False
        description: This option represents whether a reset config operation
            needs to be performed on the RAID controller. Reset Config
            operation deletes all the virtual disks present on the
            RAID controller.
        choices: [True, False]
        default: False
    raid_init_operation:
        required: False
        description: This option represents initialization configuration
            operation to be performed on the virtual disk.
        choices: [None, Fast]
        default: None
        

requirements:
    - "omsdk"
    - "python >= 2.7.5"
author: "Rajeev Arakkal (@rajeevarakkal)"

"""

EXAMPLES = """
---
- name: Create single volume with default values.
  dellemc_idrac_storage_volume:
     idrac_ip:    "xx.xxx.xx.xx"
     idrac_user:  "xxxx"
     idrac_pwd:   "xxxxxxxx"
     state: "create"
     controller_fqdd: "RAID.Slot.1-1"

- name: Create multiple volume.
  dellemc_idrac_storage_volume:
     idrac_ip:    "xx.xxx.xx.xx"
     idrac_user:  "xxxx"
     idrac_pwd:   "xxxxxxxx"
     raid_reset_config: "True"
     state: "create"
     controller_fqdd: "RAID.Slot.1-1"
     raid_level: "RAID 1"
     span_depth: 1
     span_length: 2
     number_dedicated_hot_spare: 1
     disk_cache_policy: "Enabled"
     write_cache_policy: "WriteBackForce"
     read_cache_policy: "ReadAhead"
     stripe_size: 65536
     size: 100
     raid_init_operation: "Fast"
     vd_values:
       - vd_name: "volume_1"
         pd_slots: [2,1]
       - vd_name: "volume_2"
         raid_level: "RAID 5"
         span_length: 3
         span_depth: 1 
         pd_slots: [7,3,5]
         disk_cache_policy: "Disabled"
         write_cache_policy: "WriteBack"
         read_cache_policy: "NoReadAhead"
         stripe_size: 131072
         size: "200"
         raid_init_operation: "None"

- name: View all volume details.
  dellemc_idrac_storage_volume:
     idrac_ip:    "xx.xxx.xx.xx"
     idrac_user:  "xxxx"
     idrac_pwd:   "xxxxxxxx"
     state: "view"

- name: View specific volume details.
  dellemc_idrac_storage_volume:
     idrac_ip:    "xx.xxx.xx.xx"
     idrac_user:  "xxxx"
     idrac_pwd:   "xxxxxxxx"
     state: "view"
     controller_fqdd: "RAID.Slot.1-1"
     vd_fqdd: "Disk.Virtual.0:RAID.Slot.1-1"

- name: Delete single volume.
  dellemc_idrac_storage_volume:
     idrac_ip:    "xx.xxx.xx.xx"
     idrac_user:  "xxxx"
     idrac_pwd:   "xxxxxxxx"
     state: "delete"
     vd_values:
       - vd_name: "volume_1"

- name: Delete multiple volume.
  dellemc_idrac_storage_volume:
     idrac_ip:    "xx.xxx.xx.xx"
     idrac_user:  "xxxx"
     idrac_pwd:   "xxxxxxxx"
     state: "delete"
     vd_values:
       - vd_name: "volume_1"
       - vd_name: "volume_2"
"""

RETURNS = """
dest:
    description: Configures the Raid configuration attributes.
    returned: success
    type: string
"""


import re
import copy
from ansible.module_utils.dellemc_idrac import iDRACConnection, Constants
from ansible.module_utils.basic import AnsibleModule
from omdrivers.types.iDRAC.RAID import (RAIDactionTypes, RAIDdefaultReadPolicyTypes,
                                        RAIDinitOperationTypes,
                                        DiskCachePolicyTypes, RAIDresetConfigTypes)
from omsdk.sdkfile import file_share_manager


def view_storage(idrac, module):
    """
    Storage view as JSON
    :param idrac:iDRAC handle
    :param module:Ansible module
    :return: JSON
    """
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    err = False
    msg['msg'] = idrac.config_mgr.RaidHelper.view_storage(controller=module.params['controller_fqdd'],
                                                          virtual_disk=module.params['vd_fqdd'])
    return msg


def multiple_vd_config(mod_args={}, pd_filter="", each_vd={}):
    """
    configuration of Multiple Virtual disk
    :param mod_args:
    :param pd_filter:
    :param each_vd:
    :return: {}
    """
    if each_vd:
        mod_args.update(each_vd)
    disk_size = None
    span_length = mod_args['span_length']
    pd_slots = None
    if mod_args.get('pd_slots') is not None:
        pd_slots = mod_args['pd_slots']
    size = mod_args['size']
    if mod_args['media_type'] is not None:
        pd_filter += ' and disk.MediaType == "{0}"'.format(mod_args['media_type'])
    if mod_args['bus_protocol'] is not None:
        pd_filter += ' and disk.BusProtocol == "{0}"'.format(mod_args['bus_protocol'])

    if size is not None:
        size = re.match(r"[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?", size).group()
        disk_size = "{}".format(int(float(size) * 1073741824))
    pd_selection = pd_filter

    if not (span_length or pd_slots):
        err = True
        msg = {}
        msg['msg'] = "Either span_length or pd_slots must be defined for VD creation"
        msg['failed'] = True
        return msg, err
    elif pd_slots is not None:
        slots = ""
        for i in pd_slots:
            slots += "\"" + str(i) + "\","
        slots_list = "[" + slots[0:-1] + "]"
        pd_selection += " and disk.Slot._value in " + slots_list

    raid_init_operation, raid_reset_config = "None", "False"
    if mod_args['raid_init_operation'] == "None":
        raid_init_operation = RAIDinitOperationTypes.T_None
    if mod_args['raid_init_operation'] == "Fast":
        raid_init_operation = RAIDinitOperationTypes.Fast

    if mod_args['raid_reset_config'] == "False":
        raid_reset_config = RAIDresetConfigTypes.T_False
    if mod_args['raid_reset_config'] == "True":
        raid_reset_config = RAIDresetConfigTypes.T_True

    vd_value = dict(
        Name=mod_args.get('vd_name'),
        SpanDepth=int(mod_args['span_depth']),
        SpanLength=int(mod_args['span_length']),
        NumberDedicatedHotSpare=int(mod_args['number_dedicated_hot_spare']),
        RAIDTypes=mod_args['raid_level'],
        DiskCachePolicy=DiskCachePolicyTypes[mod_args['disk_cache_policy']],
        RAIDdefaultWritePolicy=mod_args['write_cache_policy'],
        RAIDdefaultReadPolicy=RAIDdefaultReadPolicyTypes[mod_args['read_cache_policy']],
        StripeSize=int(mod_args['stripe_size']),
        RAIDforeignConfig="Clear",
        RAIDaction=RAIDactionTypes.Create,
        PhysicalDiskFilter=pd_selection,
        Size=disk_size,
        RAIDresetConfig=raid_reset_config,
        RAIDinitOperation=raid_init_operation,
        PDSlots=pd_slots,
        ControllerFQDD=mod_args.get("controller_fqdd"),
        mediatype=mod_args['media_type'],
        busprotocol=mod_args['bus_protocol']
    )
    return vd_value


def run_server_raid_config(idrac, module):
    """
    Get Lifecycle Controller status

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    err = False
    share_name = Constants.share_name
    try:
        if module.params['state'] == "view":
            msg = view_storage(idrac, module)
            if msg['msg']['Status'] == 'Failed':
                msg['msg']['failed'] = True
                err = True
            return msg, err

        idrac.use_redfish = True
        upd_share = file_share_manager.create_share_obj(share_path=share_name,
                                                        isFolder=True)
        set_liason = idrac.config_mgr.set_liason_share(upd_share)
        if set_liason['Status'] == "Failed":
            try:
                message = set_liason['Data']['Message']
            except (IndexError, KeyError):
                message = set_liason['Message']
            err = True
            msg['msg'] = "{}".format(message)
            msg['failed'] = True
            return msg, err

        if module.params['state'] == "create":
            # Create VD
            # Physical Disk filter

            if module.params['controller_fqdd'] is None or module.params['controller_fqdd'] is "":
                err = True
                msg['msg'] = 'Controller FQDD is required.'
                msg['failed'] = True
                return msg, err

            pd_filter = '((disk.parent.parent is Controller and ' \
                        'disk.parent.parent.FQDD._value == "{0}")'\
                .format(module.params['controller_fqdd'])
            pd_filter += ' or (disk.parent is Controller and ' \
                         'disk.parent.FQDD._value == "{0}"))'\
                .format(module.params['controller_fqdd'])

            vd_values = []
            if module.params['vd_values'] != None:
                for each in module.params['vd_values']:
                    mod_args = copy.deepcopy(module.params)
                    each_vd = multiple_vd_config(mod_args=mod_args,
                                                 each_vd=each,
                                                 pd_filter=pd_filter)
                    vd_values.append(each_vd)
            else:
                each_vd = multiple_vd_config(mod_args=module.params,
                                             pd_filter=pd_filter)
                vd_values.append(each_vd)
            msg['msg'] = idrac.config_mgr.RaidHelper.new_virtual_disk(multiple_vd=vd_values,
                                                                      apply_changes=not module.check_mode)
        if module.params['state'] == "delete":
            # Remove VD
            message = 'Virtual disk name is a required parameter for remove virtual disk operations.'
            if module.params['vd_values'] is None or None in module.params['vd_values']:
                message = message
                err = True
                msg['msg'] = "{}".format(message)
                msg['failed'] = True
                return msg, err
            elif module.params['vd_values']:
                if not all("vd_name" in each for each in module.params['vd_values']):
                    err = True
                    msg['msg'] = message
                    msg['failed'] = True
                    return msg, err
                names = [key.get('vd_name') for key in module.params['vd_values']]
            msg['msg'] = idrac.config_mgr.RaidHelper.delete_virtual_disk(vd_names=names,
                                                                         apply_changes=not module.check_mode)
        if 'changes_applicable' in msg['msg']:
            msg['changed'] = msg['msg']['changes_applicable']
        else:
            if "Status" in msg["msg"]:
                if msg["msg"]["Status"] == "Success":
                    msg["changed"] = True
                    if "Message" in msg["msg"]:
                        if msg["msg"]["Message"] == "No changes found to commit!" \
                                or msg["msg"]["Message"] == "Unable to find the virtual disk":
                            msg["changed"] = False
                else:
                    msg["failed"] = True
    except Exception as e:
        err = True
        msg["msg"] = "Error: %s" % str(e)
        msg["failed"] = True
    return msg, err


# Main
def main():
    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC Handle
            idrac=dict(required=False, type='dict'),

            # iDRAC credentials
            idrac_ip=dict(required=True, default=None, type='str'),
            idrac_user=dict(required=True, default=None, type='str'),
            idrac_pwd=dict(required=True, default=None,
                           type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # conditional variable for create or remove.
            state=dict(required=False, type="str",
                       choices=['create', 'delete', 'view'], default='view'),

            # Raid configuration Attributes
            vd_fqdd=dict(required=False, type='str', default=None),
            span_depth=dict(required=False, type='int', default=1),
            span_length=dict(required=False, type='int', default=1),
            number_dedicated_hot_spare=dict(required=False, type='int', default=0),
            raid_level=dict(required=False, type='str',
                            choices=['RAID 0', 'RAID 1', 'RAID 5', 'RAID 6', 'RAID 10', 'RAID 50', 'RAID 60'],
                            default="RAID 0"),
            disk_cache_policy=dict(required=False, type='str', choices=["Default", "Enabled", "Disabled"],
                                   default="Default"),
            write_cache_policy=dict(required=False, type='str', choices=["WriteThrough", "WriteBack", "WriteBackForce"],
                                    default="WriteThrough"),
            read_cache_policy=dict(required=False, type='str', choices=["NoReadAhead", "ReadAhead",
                                                                        "AdaptiveReadAhead"],
                                   default="NoReadAhead"),
            stripe_size=dict(required=False, type='int', default=64 * 1024),

            # pd_filter parameter
            controller_fqdd=dict(required=False, type='str', default=None),
            media_type=dict(required=False, choices=['HDD', 'SSD'], default=None, type='str'),
            bus_protocol=dict(required=False, choices=['SAS', 'SATA'], default=None, type='str'),
            vd_values=dict(required=False, type='list', default=None),
            size=dict(required=False, type='str', default=None),
            raid_reset_config=dict(required=False, type='str', choices=['True', 'False'], default='False'),
            raid_init_operation=dict(required=False, type='str', choices=['None', 'Fast'], default=None)
        ),

        supports_check_mode=True)
    # Connect to iDRAC
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    # Export Server Configuration Profile
    msg, err = run_server_raid_config(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)


if __name__ == '__main__':
    main()
