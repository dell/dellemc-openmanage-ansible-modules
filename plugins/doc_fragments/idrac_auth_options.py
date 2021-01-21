# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.0.0
# Copyright (C) 2020-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

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
'''
