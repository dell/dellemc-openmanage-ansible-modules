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
  idrac_ip:
    required: true
    type: str
    description: iDRAC IP Address.
  idrac_user:
    required: true
    type: str
    description:
      - iDRAC username.
      - If the username is not provided, then the environment variable E(IDRAC_USERNAME) is used.
      - "Example: export IDRAC_USERNAME=username"
  idrac_password:
    required: true
    type: str
    description:
      - iDRAC user password.
      - If the password is not provided, then the environment variable E(IDRAC_PASSWORD) is used.
      - "Example: export IDRAC_PASSWORD=password"
    aliases: ['idrac_pwd']
  idrac_port:
    type: int
    description: iDRAC port.
    default: 443
  validate_certs:
    description:
     - If C(false), the SSL certificates will not be validated.
     - Configure C(false) only on personally controlled sites where self-signed certificates are used.
     - Prior to collection version C(5.0.0), the I(validate_certs) is C(false) by default.
    type: bool
    default: true
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
