# -*- coding: utf-8 -*-

# Dell EMC OpenManage Ansible Modules
# Version 2.1.1
# Copyright (C) 2019-2020 Dell Inc. or its subsidiaries. All Rights Reserved.

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


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError


class iDRACRedfishAPI(object):
    """REST api for iDRAC modules."""

    def __init__(self, module_params):
        self.ipaddress = module_params['idrac_ip']
        self.username = module_params['idrac_user']
        self.password = module_params['idrac_password']
        self.port = module_params['idrac_port']
        self._headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def _get_url(self, uri):
        return "https://{0}:{1}{2}".format(self.ipaddress, self.port, uri)

    def _auth_kwargs(self):
        auth_kwargs = {}
        auth_kwargs['url_username'] = self.username
        auth_kwargs['url_password'] = self.password
        auth_kwargs['force_basic_auth'] = True
        auth_kwargs['validate_certs'] = False
        auth_kwargs['use_proxy'] = True
        auth_kwargs['follow_redirects'] = 'all'
        return auth_kwargs

    def invoke_request(self, uri, method, data=None):
        if data is None:
            data = {}
        kwargs = self._auth_kwargs()
        path = self._get_url(uri)
        payload = json.dumps(data)
        try:
            response = open_url(path, method=method, data=payload, headers=self._headers, **kwargs)
        except (HTTPError, URLError, SSLValidationError, ConnectionError) as error:
            raise error
        return response

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
