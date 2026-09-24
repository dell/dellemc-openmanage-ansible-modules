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
  baseuri:
    description: "IP address of the target out-of-band controller. For example- <ipaddress>:<port>."
    type: str
    required: true
  username:
    description:
      - Username of the target out-of-band controller.
      - If the username is not provided, then the environment variable E(IDRAC_USERNAME) is used.
      - "Example: export IDRAC_USERNAME=username"
    type: str
    required: false
  password:
    description:
      - Password of the target out-of-band controller.
      - If the password is not provided, then the environment variable E(IDRAC_PASSWORD) is used.
      - "Example: export IDRAC_PASSWORD=password"
    type: str
    required: false
  x_auth_token:
    description:
     - Authentication token.
     - If the x_auth_token is not provided, then the environment variable E(IDRAC_X_AUTH_TOKEN) is used.
     - "Example: export IDRAC_X_AUTH_TOKEN=x_auth_token"
    type: str
    required: false
    version_added: 9.3.0
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
  cert_fingerprint:
    description:
     - SHA-256 fingerprint of the expected TLS certificate (hex digest, with or without colons).
     - When supplied together with C(validate_certs=false), the module verifies the remote
       certificate's fingerprint instead of performing full CA validation. This allows secure
       connections to hosts with self-signed certificates without trusting any arbitrary certificate.
     - Obtain the fingerprint with C(openssl s_client -connect <host>:<port> </dev/null 2>/dev/null
       | openssl x509 -noout -fingerprint -sha256).
    type: str
    required: false
  enforce_validate_certs:
    description:
     - If C(true) and C(validate_certs) is C(false), the module will fail with an error instead
       of just emitting a warning. Use this in CI/CD pipelines or production inventories to
       enforce certificate validation as a hard requirement.
    type: bool
    default: false
'''
