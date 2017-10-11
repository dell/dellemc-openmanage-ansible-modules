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
module: dellemc_idrac_sw_inventory
short_description: Get Firmware Inventory
version_added: "2.3"
description: 
    - Get Firmware Inventory
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
  share_mnt:
    required: False
    description: 
      - Locally mounted absolute path of the Network share (CIFS, NFS) where the inventory file is going to be saved. You can also provide a local folder if you want to save the firmware inventory on local file system
      - Required if I(serialize = True)
    default: None
    type: 'path'
  choice:
    required: False
    description:
      - if C(all), get both installed and available (if any) firmware inventory
      - if C(installed), get installed firmware inventory
    default: 'installed'
  serialize:
    required: False
    description:
      - if C(True), create '_inventory' and '_master' folders relative to I(share_mnt) and save the installed firmware inventory in a file named 'config.xml' in the '_inventory' directory
      - if C(True), then I(share_mnt) must be provided 
    default: False

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
'''

EXAMPLES = '''
---
- name: Get Installed Firmware Inventory
    dellemc_idrac_sw_inventory:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_mnt:  "/mnt/NFS/"
      choice:     "installed"
'''

RETURN = '''
---
Firmware:
  type: list
  description: 
    - Components and their Firmware versions. List of dictionaries, one dict per Firmware
  returned: always
  sample: "Firmware": [
              {
                  "BuildNumber": "40", 
                  "Classifications": "10", 
                  "ComponentID": "25227", 
                  "ComponentType": "FRMW", 
                  "DeviceID": null, 
                  "ElementName": "Integrated Dell Remote Access Controller", 
                  "FQDD": "iDRAC.Embedded.1-1", 
                  "IdentityInfoType": "OrgID:ComponentType:ComponentID", 
                  "IdentityInfoValue": "DCIM:firmware:25227", 
                  "InstallationDate": "2017-06-03T23:05:47Z", 
                  "InstanceID": "DCIM:INSTALLED#iDRAC.Embedded.1-1#IDRACinfo", 
                  "IsEntity": "true",
                  "Key": "DCIM:INSTALLED#iDRAC.Embedded.1-1#IDRACinfo", 
                  "MajorVersion": "2", 
                  "MinorVersion": "41", 
                  "RevisionNumber": "40", 
                  "RevisionString": null, 
                  "Status": "Installed", 
                  "SubDeviceID": null, 
                  "SubVendorID": null, 
                  "Updateable": "true", 
                  "VendorID": null, 
                  "VersionString": "2.41.40.40", 
                  "impactsTPMmeasurements": "false" 
              }
              ...
          ]
'''

import traceback
from ansible.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
try:
    from omsdk.sdkfile import LocalFile
    from omsdk.catalog.sdkupdatemgr import UpdateManager
    from omdrivers.helpers.iDRAC.UpdateHelper import UpdateHelper
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False

def sw_inventory(idrac, module):
    """
    Get Firmware Inventory

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
        if module.params['choice'] == "all":
            msg['msg'] = idrac.update_mgr.get_swidentity()
        elif module.params['choice'] == "installed":
            msg['msg'] = idrac.update_mgr.InstalledFirmware

        if module.params['serialize']:
            fw_inv_path = LocalFile(local=module.params['share_mnt'],
                                    isFolder=True)

            if fw_inv_path.IsValid:
                UpdateManager.configure(fw_inv_path)
                msg['msg'] = UpdateHelper.save_firmware_inventory(idrac)

                if "Status" in msg['msg'] and msg['msg']['Status'] != "Success":
                    msg['failed'] = True
            else:
                msg['msg'] = "Error: Network share is not valid"
                msg['failed'] = True

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
            share_mnt=dict(required=False, default=None, type='path'),
            choice=dict(required=False, choices=['all', 'installed'],
                        default='installed'),
            serialize=dict(required=False, default=False, type='bool')
        ),

        required_if=[
            ["serialize", True, ["share_mnt"]]
        ],
        supports_check_mode=True)

    if not HAS_OMSDK:
        module.fail_json(msg="Dell EMC OpenManage Python SDK required for this module")

    # Connect to iDRAC
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    (msg, err) = sw_inventory(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()
