#! /usr/bin/python
# _*_ coding: utf-8 _*_

#
# Copyright (c) 2017 Dell Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#


try:
    from omsdk.sdkinfra import sdkinfra
    from omsdk.sdkcreds import UserCredentials,ProtocolCredentialsFactory

    HAS_OMSDK = True

except ImportError:

    HAS_OMSDK = False

class iDRACConnection():

    def __init__(self, module):
        if HAS_OMSDK is False:
            results = {}
            results['msg']="Dell EMC OMSDK library is required for this module"
            module.fail_json(**results)

        self.module = module
        self.handle = None

    def connect(self):
        results = {}

        ansible_module_params = self.module.params

        idrac = ansible_module_params.get('idrac')
        idrac_ipv4 = ansible_module_params.get('idrac_ipv4')
        idrac_user = ansible_module_params.get('idrac_user')
        idrac_pwd = ansible_module_params.get('idrac_pwd')
        idrac_port = ansible_module_params.get('idrac_port')

        if idrac:
            return idrac

        try:
            sd = sdkinfra()
            sd.importPath()
        except Exception as e:
            results['msg'] = "Could not initialize drivers"
            results['exception'] = str(e)
            self.module.fail_json(**results)

        # Connect to iDRAC
        if idrac_ipv4 == '' or idrac_user == '' or idrac_pwd == '':
            results['msg'] = "hostname, username and password required for this name"
            self.module.fail_json(**results)
        else:
            creds = UserCredentials(idrac_user, idrac_pwd)
            idrac = sd.find_driver(idrac_ipv4, creds)

            if idrac is None:
                results['msg'] = "Could not find device driver for iDRAC with IP Address: " + idrac_ipv4 + " User: " + idrac_user + " Pwd: " + idrac_pwd
                self.module.fail_json(**results)

        self.handle = idrac
        return idrac

    def disconnect(self):
        idrac = self.module.params.get('idrac')

        if idrac:
            # pre-existing handle from a task
            return False

        if self.handle:
            self.handle.disconnect()
            return True

        return True
