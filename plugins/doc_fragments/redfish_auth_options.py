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
  baseuri:
    description: "IP address of the target out-of-band controller. For example- <ipaddress>:<port>."
    type: str
    required: True
  username:
    description: Username of the target out-of-band controller.
    type: str
    required: True
  password:
    description: Password of the target out-of-band controller.
    type: str
    required: True
'''
