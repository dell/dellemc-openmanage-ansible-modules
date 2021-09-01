# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.4.0
# Copyright (C) 2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    DOCUMENTATION = r'''
options:
  hostname:
    description: OpenManage Enterprise Modular IP address or hostname.
    type: str
    required: True
  username:
    description: OpenManage Enterprise Modular username.
    type: str
    required: True
  password:
    description: OpenManage Enterprise Modular password.
    type: str
    required: True
  port:
    description: OpenManage Enterprise Modular HTTPS port.
    type: int
    default: 443
'''
