# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2020-2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    DOCUMENTATION = r'''
options:
  hostname:
    description: OpenManage Enterprise IP address or hostname.
    type: str
    required: true
  username:
    description:
      - OpenManage Enterprise username.
      - If the username is not provided, then the environment variable E(OME_USERNAME) is used.
      - "Example: export OME_USERNAME=username"
    type: str
    required: false
  password:
    description:
      - OpenManage Enterprise password.
      - If the password is not provided, then the environment variable E(OME_PASSWORD) is used.
      - "Example: export OME_PASSWORD=password"
    type: str
    required: false
  x_auth_token:
    description:
     - Authentication token.
     - If the x_auth_token is not provided, then the environment variable E(OME_X_AUTH_TOKEN) is used.
     - "Example: export OME_X_AUTH_TOKEN=x_auth_token"
    type: str
    required: false
    version_added: 9.3.0
  port:
    description: OpenManage Enterprise HTTPS port.
    type: int
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
