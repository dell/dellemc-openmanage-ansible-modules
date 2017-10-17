#! /usr/bin/python
# _*_ coding: utf-8 _*_

#
# Dell EMC OpenManage Ansible Modules
#
# Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved.
# Dell, EMC, and other trademarks are trademarks of Dell Inc. or its
# subsidiaries. Other trademarks may be trademarks of their respective owners.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: dellemc_idrac_firmware_update
short_description: Firmware update from a repository on a network share (CIFS, NFS)
version_added: "2.3"
description:
    - Update the Firmware by connecting to a network repository (either CIFS or NFS) that contains a catalog of available updates
    - Network share should contain a valid repository of Update Packages (DUPs) and a catalog file describing the DUPs
    - All applicable updates contained in the repository is applied to the system
    - This feature is only available with iDRAC Enterprise License
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
      - Network file share (either CIFS or NFS) containing the Catalog file and Update Packages (DUPs)
    type: 'str'
  share_user:
    required: True
    description:
      - Network share user in the format 'user@domain' if user is part of a domain else 'user'
    type: 'str'
  share_pwd:
    required: True
    description:
      - Network share user password
    type: 'str'
  catalog_file_name:
    required: False
    description:
      - Catalog file name relative to the I(share_name)
    default: 'Catalog.xml'
    type: 'str'
  apply_updates:
    required: False
    description: 
      - if C(True), Install Updates
      - if C(False), do not Install Updates
    default: True
    type: 'bool'
  reboot:
    required: False
    description:
      - if C(True), reboot for applying the updates
      - if C(False), do not reboot for applying the update
    default: False
    type: 'bool'
  job_wait:
    required: False
    description:
      - if C(True), will wait for update JOB to get completed
      - if C(False), return immediately after creating the update job in job queue
    default: True
    type: 'bool'
    
requirements: ['Dell EMC OpenManage Python SDK']
author: "anupam.aloke@dell.com"
'''

EXAMPLES = '''
---
- name: Update firmware from repository on a Network Share
    dellemc_idrac_virtual_drive:
       idrac_ip:   "192.168.1.1"
       idrac_user: "root"
       idrac_pwd:  "calvin"
       share_name: "\\\\192.168.10.10\\share"
       share_user: "user1"
       share_pwd:  "password"
       catalog_file_name:  "Catalog.xml"
       apply_updates:   True
       reboot:     False
       job_wait:   True

'''

RETURN = '''
---
'''

from ansible.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
try:
    from omsdk.sdkcreds import UserCredentials
    from omsdk.sdkfile import FileOnShare
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False


def update_fw_from_nw_share(idrac, module):
    """
    Update firmware from a network share

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    err = False

    try:
        if module.check_mode:
            msg['changed'] = True
        else:
            upd_share = FileOnShare(remote=module.params['share_name'],
                                    isFolder=True)
            upd_share.addcreds(UserCredentials(module.params['share_user'],
                                               module.params['share_pwd']))
            upd_share_file_path = upd_share.new_file(module.params['catalog_file_name'])

            msg['msg'] = idrac.update_mgr.update_from_repo(upd_share_file_path,
                                                           module.params['apply_update'],
                                                           module.params['reboot'],
                                                           module.params['job_wait'])

            if "Status" in msg['msg']:
                if msg['msg']['Status'] == "Success":
                    msg['changed'] = True
                else:
                    msg['failed'] = True

    except Exception as e:
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True

    return msg, err

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

            # Firmware update parameters
            catalog_file_name=dict(required=False, default='Catalog.xml', type='str'),
            apply_update=dict(required=False, default=True, type='bool'),
            reboot=dict(required=False, default=False, type='bool'),
            job_wait=dict(required=False, default=True, type='bool')
        ),

        supports_check_mode=True)

    if not HAS_OMSDK:
        module.fail_json(msg="Dell EMC OpenManage Python SDK required for this module")

    # Connect to iDRAC
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    msg, err = update_fw_from_nw_share(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()
