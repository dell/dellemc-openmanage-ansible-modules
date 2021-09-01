# -*- coding: utf-8 -*-

# Dell EMC OpenManage Ansible Modules
# Version 4.0.0
# Copyright (C) 2019-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:

#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.

#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    from omsdk.sdkinfra import sdkinfra
    from omsdk.sdkcreds import UserCredentials
    from omsdk.sdkfile import FileOnShare, file_share_manager
    from omsdk.sdkprotopref import ProtoPreference, ProtocolEnum
    from omsdk.http.sdkwsmanbase import WsManOptions
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False


class iDRACConnection:

    def __init__(self, module_params):
        if not HAS_OMSDK:
            raise ImportError("Dell EMC OMSDK library is required for this module")
        self.idrac_ip = module_params['idrac_ip']
        self.idrac_user = module_params['idrac_user']
        self.idrac_pwd = module_params['idrac_password']
        self.idrac_port = module_params['idrac_port']
        if not all((self.idrac_ip, self.idrac_user, self.idrac_pwd)):
            raise ValueError("hostname, username and password required")
        self.handle = None
        self.creds = UserCredentials(self.idrac_user, self.idrac_pwd)
        self.pOp = WsManOptions(port=self.idrac_port)
        self.sdk = sdkinfra()
        if self.sdk is None:
            msg = "Could not initialize iDRAC drivers."
            raise RuntimeError(msg)

    def __enter__(self):
        self.sdk.importPath()
        self.handle = self.sdk.get_driver(self.sdk.driver_enum.iDRAC, self.idrac_ip, self.creds, pOptions=self.pOp)
        if self.handle is None:
            msg = "Unable to communicate with iDRAC {0}. This may be due to one of the following: " \
                  "Incorrect username or password, unreachable iDRAC IP or " \
                  "a failure in TLS/SSL handshake.".format(self.idrac_ip)
            raise RuntimeError(msg)
        return self.handle

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.handle.disconnect()
        return False
