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

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import sys
import shutil
import glob

print("Dell EMC OpenManage Ansible Modules installation has started.")
print("Checking prerequisites...")
print("")
# Check for Ansible installlisation with version
try:
    import ansible

except ImportError:
    print('Ansible is not installed.')
    print('Dell EMC OpenManage Ansible Modules installation has failed.')
    sys.exit(1)

# check for ansible verson
required_version = '2.2.0'
installed_version = ansible.__version__

# check for omsdk installization

try:
    from omsdk.sdkinfra import sdkinfra
    from builtins import input
    print("	OpenManage Software Development Kit is installed.")
except ImportError:
    print('OpenManage Software Development Kit is not installed.')
    print('Dell EMC OpenManage Ansible Modules installation has failed.')
    sys.exit(1)

ansible_path = ansible.__path__[0]
# print("Ansible config path :" + ansible_path)
module_utils_path = ansible_path + '/module_utils/'
extras_path = ansible_path + '/modules/extras'
server_path = extras_path + '/dellemc'
dellemc_idrac_path = server_path + '/server'

remote_mgmt_path = ansible_path + '/modules/remote_management'
remote_mgmt_dellemc = remote_mgmt_path + '/dellemc'
remote_mgmt_dellemc_idrac = remote_mgmt_dellemc + '/idrac'

log_root = '/var/log'
dell_emc_log_path = log_root + '/dellemc'
dell_emc_log_file = dell_emc_log_path + '/dellemc_log.conf'
dell_emc_json = remote_mgmt_dellemc_idrac + '/properties.json'
dell_emc_depr = remote_mgmt_dellemc_idrac + '/dellemc_configure_raid.py'

warning_message = "Dell EMC OpenManage Ansible Modules is already present. Do you want to upgrade? (y/n)  "


def update_check(message):
    yes = {'y', ''}
    print(" ")
    print(message)
    print("Press `y` to update the Dell EMC OpenManage Ansible Modules specific folders and files...")
    print("Press any other key to exit installation (default: 'y'):")
    choice = input()
    if choice in yes:
        return True
    else:
        return False


if os.path.isdir(server_path) or os.path.isdir(remote_mgmt_dellemc):
    checking = update_check(warning_message)
    if not checking:
        sys.exit(1)

print("Installing Dell EMC OpenManage Ansible Modules specific folders and files...")


# Cleaning up old installation content from /modules/extras/dellemc and log config files
def remove_files(src):
    src_files = os.listdir(src)

    for file_name in src_files:
        src_file = os.path.join(src, file_name)

        if (os.path.isfile(src_file)):
            os.remove(src_file)


if os.path.isdir(dellemc_idrac_path):
    remove_files(dellemc_idrac_path)

if os.path.isdir(server_path):
    shutil.rmtree(server_path)

if os.path.isfile(dell_emc_log_file):
    os.remove(dell_emc_log_file)


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


# Removing COPYING.txt and README.txt files.
for f in glob.glob(os.path.join(remote_mgmt_dellemc_idrac, "*.txt")):
    os.remove(f)

# Removing properties.json file.
if os.path.isfile(dell_emc_json):
    os.remove(dell_emc_json)

# Removing deprecated raid module
if os.path.isfile(dell_emc_depr):
    os.remove(dell_emc_depr)

def copy_files(src, dest):
    import shutil

    src_files = os.listdir(src)

    for file_name in src_files:
        src_file, dst_file = '', ''
        if not file_name.endswith(".txt") and not file_name.endswith(".md"):
            src_file = os.path.join(src, file_name)
            dst_file = os.path.join(dest, file_name)
        if file_name != "install.py" and file_name != "uninstall.py":
            if (os.path.isfile(src_file)):
                shutil.copy(src_file, dst_file)


# Create the directory for the main module under remote_management/dellemc/idrac repo
if not os.path.isdir(remote_mgmt_dellemc_idrac):
    os.makedirs(remote_mgmt_dellemc_idrac)
touch(remote_mgmt_dellemc + '/__init__.py')
touch(remote_mgmt_dellemc_idrac + '/__init__.py')

# Copy files from parent folder to dellemc_idrac_path
copy_files(os.getcwd(), remote_mgmt_dellemc)

# Copy files from library folder to dellemc_idrac_path
copy_files(os.getcwd() + '/library', remote_mgmt_dellemc_idrac)

# Copy common files to module_util
copy_files(os.getcwd() + '/utils', module_utils_path)
print("SUCCESS: Dell EMC OpenManage Ansible Modules is installed successfully.")
