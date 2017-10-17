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
module: dellemc_idrac_timezone_ntp
short_description: Configure Time Zone and NTP settings
version_added: "2.3"
description:
    - Configure Time Zone and NTP settings
options:
  idrac_ip:
    required: False
    description:
      - iDRAC IP Address
    default: None
  idrac_user:
    required: False
    description:
      - iDRAC user name
    default: None
  idrac_pwd:
    required: False
    description:
      - iDRAC user password
    default: None
  idrac_port:
    required: False
    description:
      - iDRAC port
    default: None
  share_name:
    required: True
    description:
      - CIFS or NFS Network share
  share_user:
    required: True
    description:
      - Network share user in the format user@domain
  share_pwd:
    required: True
    description:
      - Network share user password
  share_mnt:
    required: True
    description:
      - Local mount path of the network file share with read-write permission for ansible user
  timezone:
    required: False
    description:
      - time zone e.g. "Asia/Kolkata"
    default: None
  ntp_servers:
    required: False
    description:
      - List of IP Addresses of the NTP Servers
    default: None
  state:
    required: False
    description:
      - if C(present), will enable the NTP option and add the NTP servers
      - if C(absent), will disable the NTP option
    default: 'present'


requirements: ['omsdk']
author: "anupam.aloke@dell.com"
'''

EXAMPLES = '''
# Set Timezone, Enable NTP and add NTP Servers
- name: Configure TimeZone and NTP
    dellemc_idrac_timezone_ntp:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      timezone:   "Asia/Kolkata"
      ntp_servers: ["10.10.10.10", "10.10.10.11"]
      state:      "present"

# Disable NTP
- name: Configure TimeZone and NTP
    dellemc_idrac_timezone_ntp:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      share_name: "\\\\192.168.10.10\\share"
      share_user: "user1"
      share_pwd:  "password"
      share_mnt:  "/mnt/share"
      state:      "absent"
'''

RETURN = '''
'''

from ansible.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule


def _setup_timezone(idrac, module):
    """
    Setup timezone settings on iDRAC

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    if module.params['timezone']:
        idrac.config_mgr.TimeZone.set_value(module.params["timezone"])


def _setup_ntp(idrac, module):
    """
    Setup NTP settings on iDRAC

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    if module.params['state'] == 'present':
        idrac.config_mgr._sysconfig.iDRAC.NTPConfigGroup.NTPEnable_NTPConfigGroup = 'Enabled'

        if module.params['ntp_servers']:
            ntp_servers = [server for server in module.params['ntp_servers'] \
                           if server.strip()]
            ntp_servers.extend(["", "", ""])

            if ntp_servers[0]:
                idrac.config_mgr._sysconfig.iDRAC.NTPConfigGroup.\
                    NTP1_NTPConfigGroup = ntp_servers[0]

            if ntp_servers[1]:
                idrac.config_mgr._sysconfig.iDRAC.NTPConfigGroup.\
                    NTP2_NTPConfigGroup = ntp_servers[1]

            if ntp_servers[2]:
                idrac.config_mgr._sysconfig.iDRAC.NTPConfigGroup.\
                    NTP3_NTPConfigGroup = ntp_servers[2]

    elif module.params['state'] == 'absent':
        idrac.config_mgr._sysconfig.iDRAC.NTPConfigGroup.NTPEnable_NTPConfigGroup = 'Disabled'


def setup_idrac_timezone_ntp(idrac, module):
    """
    Setup iDRAC Time Zone

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
        _setup_timezone(idrac, module)
        _setup_ntp(idrac, module)

        msg['changed'] = idrac.config_mgr._sysconfig.is_changed()

        if module.check_mode:
            # since it is running in check mode, reject the changes
            idrac.config_mgr._sysconfig.reject()
        else:
            msg['msg'] = idrac.config_mgr.apply_changes(reboot=False)

            if 'Status' in msg['msg'] and msg['msg']['Status'] != "Success":
                msg['failed'] = True
                msg['changed'] = False

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
            share_mnt=dict(required=True, type='path'),

            # Time Zone
            timezone=dict(required=False, default=None, type='str'),

            # NTP parameters
            ntp_servers=dict(required=False, default=None, type='list'),

            state=dict(required=False, choices=['present', 'absent'], default='present')
        ),

        supports_check_mode=True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    # Setup network share as local mount
    if not idrac_conn.setup_nw_share_mount():
        module.fail_json(msg="Failed to setup network share local mount point")

    # Setup TZ and NTP
    (msg, err) = setup_idrac_timezone_ntp(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()
