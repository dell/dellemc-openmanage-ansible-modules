# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.1
# Copyright (C) 2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    DOCUMENTATION = r'''
options:
  hostname:
    description: Target IP address or hostname.
    type: str
    required: True
  username:
    description: Target username.
    type: str
    required: True
  password:
    description: Target user password.
    type: str
    required: True
  port:
    description: Target HTTPS port.
    type: int
    default: 443
'''
