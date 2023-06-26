# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.0.0
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    DOCUMENTATION = r'''
options:
    share_name:
        required: true
        type: str
        description: Network share or a local path.
    share_user:
        type: str
        description: Network share user name. Use the format 'user@domain' or 'domain\\user' if user is part of a domain.
            This option is mandatory for CIFS share.
    share_password:
        type: str
        description: Network share user password. This option is mandatory for CIFS share.
        aliases: ['share_pwd']
    share_mnt:
        type: str
        description: Local mount path of the network share with read-write permission for ansible user.
            This option is mandatory for network shares.
'''
