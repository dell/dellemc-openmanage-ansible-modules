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

import os
import sys
import shutil

try:
    import ansible
except:
    print "Ansible is not installed"
    sys.exit(1)

ansible_path = ansible.__path__[0]
module_utils_path = ansible_path + '/module_utils/'
extras_path = ansible_path + '/modules/extras'
server_path = extras_path + '/server'
dellemc_idrac_path = server_path + '/dellemc'

if os.path.isdir(server_path):
    shutil.rmtree(server_path)

if os.path.isfile(module_utils_path + 'dellemc_idrac.py'):
    os.remove(module_utils_path + 'dellemc_idrac.py')
