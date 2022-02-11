# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.0.1
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    DOCUMENTATION = r'''
options:
  idrac_ip:
    required: True
    type: str
    description: iDRAC IP Address.
  idrac_user:
    required: True
    type: str
    description: iDRAC username.
  idrac_password:
    required: True
    type: str
    description: iDRAC user password.
    aliases: ['idrac_pwd']
  idrac_port:
    type: int
    description: iDRAC port.
    default: 443
  validate_certs:
    description:
     - If C(False), the SSL certificates will not be validated.
     - Configure C(False) only on personally controlled sites where self-signed certificates are used.
     - Prior to collection version C(5.0.0), the I(validate_certs) is C(False) by default.
    type: bool
    default: True
    version_added: 5.0.0
  ca_path:
    description:
     - The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.
    type: path
    version_added: 5.0.0
  timeout:
    description: The socket level timeout in seconds.
    type: int
    default: 30
    version_added: 5.0.0
'''
