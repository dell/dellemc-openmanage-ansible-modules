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

from ansible.module_utils.dellemc_idrac import *
from ansible.module_utils.basic import AnsibleModule

def _setup_idrac_nw_share (idrac, module):
    """
    Setup local mount point for network file share

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    myshare = FileOnShare(module.params['share_name'],
                          module.params['share_mnt'],
                          isFolder=True)

    myshare.addcreds(UserCredentials(module.params['share_user'],
                                    module.params['share_pwd']))

    return idrac.config_mgr.set_liason_share(myshare)

def _timezone_exists (idrac, module):
    """
    Check whether a given timezone is already configured

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    if module.params['timezone']:
        if module.params['timezone'] == idrac.config_mgr.TimeZone:
            return True
        else:
            return False

    return True

def _setup_timezone(idrac, module):
    """
    Setup timezone settings on iDRAC

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    changed = False
    failed = False
    msg = {}

    # Check if the timezone settings exists
    exists = _timezone_exists(idrac, module)

    if module.check_mode or exists:
        changed = not exists
    else:
        msg = idrac.config_mgr.configure_time_zone(module.params["timezone"])

        if 'Status' in msg and msg['Status'] == "Success":
            changed = True
        else:
            failed = True

    return changed, failed, msg


def _ntp_exists(idrac, module):
    """
    Check whether NTP configuration settings already exists on iDRAC

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    if not idrac.config_mgr.NTPEnabled:
        return False
    elif module.params['ntp_servers']:
        # filter out the empty addresses
        ntp_servers = [server for server in module.params['ntp_servers'] if server]
        if set(idrac.config_mgr.NTPServers) != set(ntp_servers):
            return False

    return True

def _setup_ntp(idrac, module):
    """
    Setup NTP settings on iDRAC

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    msg = {}
    changed = False
    failed = False

    # Check whether NTP settings already exist
    exists = _ntp_exists(idrac, module)

    if module.params['state'] == 'present':
        if module.check_mode or exists:
            changed = not exists
        else:
            ntp_servers = []

            if module.params['ntp_servers']:
                ntp_servers = module.params['ntp_servers']
                ntp_servers.extend(["", "", ""])

                msg = idrac.config_mgr.enable_ntp(server1=ntp_servers[0],
                                                  server2=ntp_servers[1],
                                                  server3=ntp_servers[2])
    elif module.params['state'] == 'absent':
        if module.check_mode or not exists:
            changed = exists
        else:
            msg = idrac.config_mgr.disable_ntp()

    if 'Status' in msg:
        if msg['Status'] == "Success":
            changed = True
        else:
            failed = True

    return changed, failed, msg


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
    changed = {"timezone" : False, "ntp" : False}
    failed = {"timezone" : False, "ntp" : False}

    try:
        # Check first whether local mount point for network share is setup
        if idrac.config_mgr.liason_share is None:
            if not  _setup_idrac_nw_share (idrac, module):
                msg['msg'] = "Failed to setup local mount point for network share"
                msg['failed'] = True
                return msg


        changed['timezone'], failed['timezone'], msg['msg'] = _setup_timezone(idrac, module)

        if not failed['timezone']:
            changed['ntp'], failed['ntp'], msg['msg'] = _setup_ntp(idrac, module)

        for key,value in changed.iteritems():
            if value:
                msg['changed'] = True
                break

        for key, value in failed.iteritems():
            if value:
                msg['failed'] = True
                break

    except Exception as e:
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True

    return msg, err

# Main
def main():

    module = AnsibleModule (
            argument_spec = dict (
                # iDRAC handle
                idrac = dict (required = False, type = 'dict'),

                # iDRAC Credentials
                idrac_ip   = dict (required = False, default = None, type = 'str'),
                idrac_user = dict (required = False, default = None, type = 'str'),
                idrac_pwd  = dict (required = False, default = None,
                                   type = 'str', no_log = True),
                idrac_port = dict (required = False, default = None, type = 'int'),

                # Network File Share
                share_name = dict (required = True, type = 'str'),
                share_user = dict (required = True, type = 'str'),
                share_pwd  = dict (required = True, type = 'str', no_log = True),
                share_mnt  = dict (required = True, type = 'path'),

                # Time Zone
                timezone = dict (required = False, default = None, type = 'str'),
                # NTP parameters
                ntp_servers = dict (required = False, default = None, type = 'list'),
                state = dict (required = False,
                              choices = ['present', 'absent'],
                              default = 'present')

                ),
            supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    (msg, err) = setup_idrac_timezone_ntp (idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()
