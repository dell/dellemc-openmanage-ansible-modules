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
module: dellemc_idrac_web_server
short_description: Configure iDRAC Web Server service interface settings
version_added: "2.3"
description:
    - Configure iDRAC Web Server Service interface settings such as minimum supprted levels of Transport Layer Security (TLS) protocol and levels of Secure Socket Layer (SSL) Encryption
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
      - Network file share
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
  tls_protocol:
    required: False
    description:
      - if C(TLS 1.0 and Higher), will set the TLS protocol to TLS 1.0 and higher
      - if C(TLS 1.1 and Higher), will set the TLS protocol to TLS 1.1 and higher
      - if C(TLS 1.2 Only), will set the TLS protocol option to TLS 1.2 Only
    choices: ['TLS 1.0 and Higher', 'TLS 1.1 and Higher', 'TLS 1.2 Only']
    default: 'TLS 1.1 and Higher'
  ssl_bits:
    required: False
    description:
      - if C(128-Bit or higher), will set the SSL Encryption Bits to 128-Bit or higher
      - if C(168-Bit or higher), will set the SSL Encryption Bits to 168-Bit or higher
      - if C(256-Bit or higher), will set the SSL Encryption Bits to 256-Bit or higher
      - if C(Auto-Negotiate), will set the SSL Encryption Bits to Auto-Negotiate
    choices: ['Auto-Negotiate', '128-Bit or higher', '168-Bit or higher', '256-Bit or higher']
    default: "128-Bit or higher"

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
'''

EXAMPLES = '''
- name: Configure Web Server TLS and SSL settings (using CIFS network share)
    dellemc_idrac_web_server:
      idrac_ip:     "192.168.1.1"
      idrac_user:   "root"
      idrac_pwd:    "calvin"
      share_name:   "\\\\192.168.10.10\\share"
      share_user:   "user1"
      share_pwd:    "password"
      share_mnt:    "/mnt/share"
      tls_protocol: "TLS 1.2 Only"
      ssl_bits:     "256-Bit or higher"

- name: Configure Web Server TLS and SSL settings (using NFS network share)
    dellemc_idrac_web_server:
      idrac_ip:     "192.168.1.1"
      idrac_user:   "root"
      idrac_pwd:    "calvin"
      share_name:   "192.168.10.10:/share"
      share_user:   "user1"
      share_pwd:    "password"
      share_mnt:    "/mnt/share"
      tls_protocol: "TLS 1.2 Only"
      ssl_bits:     "256-Bit or higher"
'''

RETURN = '''
'''

from ansible.module_utils.dellemc_idrac import *
from ansible.module_utils.basic import AnsibleModule

def _setup_idrac_nw_share (idrac, module):
    """
    Setup local mount point for Network file share

    Keyword arguments:
    iDRAC  -- iDRAC handle
    module -- Ansible module
    """

    myshare = FileOnShare(module.params['share_name'],
                          module.params['share_mnt'],
                          isFolder=True)

    myshare.addcreds(UserCredentials(module.params['share_user'],
                                     module.params['share_pwd']))

    return idrac.config_mgr.set_liason_share(myshare)

def setup_idrac_tls (idrac, module):
    """
    Setup iDRAC TLS settings

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    from omdrivers.enums.iDRAC.iDRACEnums import TLSOptions, SSLBits

    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    err = False

    try:
        # Check first whether local mount point for network share is setup
        if idrac.config_mgr.liason_share is None:
            if not  _setup_idrac_nw_share (idrac, module):
                msg['msg'] = "Failed to setup local mount point for network share"
                msg['failed'] = True
                return msg

        # Check if TLS and SSL settings already exists
        exists = False
        tls_protocol = TypeHelper.convert_to_enum(module.params['tls_protocol'], TLSOptions)
        ssl_bits = TypeHelper.convert_to_enum(module.params['ssl_bits'], SSLBits)
        curr_tls_protocol = idrac.config_mgr.TLSProtocol
        curr_ssl_bits = idrac.config_mgr.SSLEncryptionBits

        if curr_tls_protocol == tls_protocol and curr_ssl_bits == ssl_bits:
            exists = True

        if module.check_mode or exists:
            msg['changed'] = not exists
        else:
            msg['msg'] = idrac.config_mgr.configure_tls(tls_protocol, ssl_bits)

            if "Status" in msg['msg'] and msg['msg']['Status'] is "Success":
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

                tls_protocol = dict (required = False,
                                     choices = ['TLS 1.0 and Higher',
                                                'TLS 1.1 and Higher',
                                                'TLS 1.2 Only'],
                                     default = 'TLS 1.1 and Higher'),
                ssl_bits = dict (required = False,
                                 choices = ['Auto-Negotiate',
                                            '128-Bit or higher',
                                            '168-Bit or higher',
                                            '256-Bit or higher'],
                                 default = '128-Bit or higher')

                ),
            supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    msg, err = setup_idrac_tls (idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()
