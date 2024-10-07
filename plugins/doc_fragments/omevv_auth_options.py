# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.8.0
# Copyright (C) 2020-2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    DOCUMENTATION = r'''
options:
  hostname:
    description: OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.
    type: str
    required: true
  vcenter_username:
    description:
      - OpenManage Enterprise Integration for VMware vCenter username.
      - If the username is not provided, then the environment variable E(OMEVV_VCENTER_USERNAME) is used.
      - "Example: export OMEVV_VCENTER_USERNAME=username"
    type: str
    required: false
  vcenter_password:
    description:
      - OpenManage Enterprise Integration for VMware vCenter password.
      - If the password is not provided, then the environment variable E(OMEVV_VCENTER_PASSWORD) is used.
      - "Example: export OMEVV_VCENTER_PASSWORD=password"
    type: str
    required: false
  vcenter_uuid:
    description:
     - Universally unique identifier (uuid) of vCenter.
     - vCenter uuid details can be fetched using M(omevv_vcenter_info) module.
     - If the uuid is not provided, then the environment variable E(OMEVV_VCENTER_UUID) is used.
     - "Example: export OMEVV_VCENTER_UUID=uuid"
    type: str
    required: false
  port:
    description: OpenManage Enterprise HTTPS port.
    type: int
    default: 443
  validate_certs:
    description: Whether to check SSL certificate.
     - If C(true), the SSL certificates will be validated.
     - If C(false), the SSL certificates will not be validated.
    type: bool
    default: true
  ca_path:
    description:
     - The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.
    type: path
  timeout:
    description: The socket level timeout in seconds.
    type: int
    default: 30
'''
