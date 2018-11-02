#!/usr/bin/python
# _*_ coding: utf-8 _*_

#
# Dell EMC OpenManage Ansible Modules
# Version 1.0
# Copyright (C) 2018 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#


import os
import sys
import shutil


try:
    import ansible

except:
    print('Dell EMC OpenManage Ansible Modules is not installed.')
    sys.exit(1)
try:
    ansible_path = ansible.__path__[0]
    module_utils_path = ansible_path + '/module_utils/'

    remote_mgmt_path = ansible_path + '/modules/remote_management'
    remote_mgmt_dellemc = remote_mgmt_path + '/dellemc'
    remote_mgmt_dellemc_idrac = remote_mgmt_dellemc + '/idrac'

    if not os.path.isfile(module_utils_path + 'dellemc_idrac.py'):
        print('Dell EMC OpenManage Ansible Modules is not installed.')
        sys.exit(1)
except:
    sys.exit(1)

print("Dell EMC OpenManage Ansible Modules uninstallation has started.")

print("Uninstalling Dell EMC OpenManage Ansible Modules specific folders and files...")


def remove_files(src):

    src_files = os.listdir(src)

    for file_name in src_files:
        src_file = os.path.join(src, file_name)

        if (os.path.isfile(src_file)):
            os.remove(src_file)


if os.path.isdir(remote_mgmt_dellemc_idrac):
    remove_files(remote_mgmt_dellemc_idrac)

if os.path.isdir(remote_mgmt_dellemc):
    shutil.rmtree(remote_mgmt_dellemc)


if os.path.isfile(module_utils_path + 'dellemc_idrac.py'):
    os.remove(module_utils_path + 'dellemc_idrac.py')
    print("SUCCESS: Dell EMC OpenManage Ansible Modules is uninstalled successfully.")
else:
    print("SUCCESS: Dell EMC OpenManage Ansible Modules is uninstalled successfully.")

