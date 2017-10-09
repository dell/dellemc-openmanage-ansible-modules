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
  timeout:
    required: False
    description:
      - Time (in seconds) that a connection is allowed to remain idle
      - Changes to the timeout settings do not affect the current session
      - If you change the timeout value, you must log out and log in again for the new settings to take effect
      - Timeout range is 60 to 10800 seconds
    default: 1800
  http_port:
    required: False
    description:
      - HTTP port
    default: 80
  https_port:
    required: False
    description:
      - HTTPS port
    default: 443
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
  state:
    required: False
    description:
      - if C(present), will enable the Web Server and configure the Web Server parameters
      - if C(absent), will disable the Web Server. Please note that you will not be able to use the iDRAC Web Interface if you disable the Web server.
    choices: ['present', 'absent']
    default: 'present'

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

from ansible.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule

try:
    from omsdk.sdkcenum import TypeHelper
    from omdrivers.enums.iDRAC.iDRAC import (
        Enable_WebServerTypes, SSLEncryptionBitLength_WebServerTypes,
        TLSProtocol_WebServerTypes
    )
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False


def setup_idrac_webserver(idrac, module):
    """
    Setup iDRAC Webserver services

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
        tls_protocol = TypeHelper.convert_to_enum(module.params['tls_protocol'],
                                                  TLSProtocol_WebServerTypes)
        ssl_bits = TypeHelper.convert_to_enum(module.params['ssl_bits'],
                                              SSLEncryptionBitLength_WebServerTypes)

        if module.params['state'] == 'present':
            idrac.config_mgr._sysconfig.iDRAC.WebServer.\
                    Enable_WebServer = Enable_WebServerTypes.Enabled
            idrac.config_mgr._sysconfig.iDRAC.WebServer.\
                    Timeout_WebServer = module.params['timeout']
            idrac.config_mgr._sysconfig.iDRAC.WebServer.\
                    HttpPort_WebServer = module.params['http_port']
            idrac.config_mgr._sysconfig.iDRAC.WebServer.\
                    HttpsPort_WebServer = module.params['https_port']
            idrac.config_mgr._sysconfig.iDRAC.WebServer.\
                    TLSProtocol_WebServer = tls_protocol
            idrac.config_mgr._sysconfig.iDRAC.WebServer.\
                    SSLEncryptionBitLength_WebServer = ssl_bits
        else:
            idrac.config_mgr._sysconfig.iDRAC.WebServer.\
                    Enable_WebServer = Enable_WebServerTypes.Disabled

        msg['changed'] = idrac.config_mgr._sysconfig.is_changed()

        if module.check_mode:
            # Since it is running in check mode, reject the changes
            idrac.config_mgr._sysconfig.reject()
        else:
            msg['msg'] = idrac.config_mgr.apply_changes(reboot=False)

            if "Status" in msg['msg'] and msg['msg']['Status'] != "Success":
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

            # Web Server Service paramaters
            timeout=dict(required=False, default=1800, type='int'),
            http_port=dict(required=False, default=80, type='int'),
            https_port=dict(required=False, default=443, type='int'),
            tls_protocol=dict(required=False,
                              choices=['TLS 1.0 and Higher', 'TLS 1.1 and Higher', 'TLS 1.2 Only'],
                              default='TLS 1.1 and Higher'),
            ssl_bits=dict(required=False,
                          choices=['Auto-Negotiate', '128-Bit or higher',
                                   '168-Bit or higher', '256-Bit or higher'],
                          default='128-Bit or higher'),
            state=dict(required=False, choices=['present', 'absent'], default='present')
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

    # Setup web server parameters
    msg, err = setup_idrac_webserver(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()
