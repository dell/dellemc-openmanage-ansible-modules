#! /usr/bin/python
# _*_ coding: utf-8 _*_

#
# Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved.
# Dell, EMC, and other trademarks are trademarks of Dell Inc. or its
# subsidiaries. Other trademarks may be trademarks of their respective owners.

import os
import sys
import shutil

try:
    import ansible
except ImportError:
    print "Error: Ansible is not installed"
    sys.exit(1)

ansible_path = ansible.__path__[0]
module_utils_path = ansible_path + '/module_utils/'
remote_management_path = ansible_path + '/modules/remote_management'
dellemc_idrac_path = remote_management_path + '/dellemc_idrac'

if os.path.isdir(dellemc_idrac_path):
    shutil.rmtree(dellemc_idrac_path)

if os.path.isfile(module_utils_path + 'dellemc_idrac.py'):
    os.remove(module_utils_path + 'dellemc_idrac.py')
