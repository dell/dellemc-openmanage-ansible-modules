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
from builtins import *

import os
import sys
import logging
import logging.config

log_root = '/var/log'
dell_emc_log_path = log_root + '/dellemc'

# create log directory in the log root var/log
if not os.path.isdir(dell_emc_log_path):
    os.makedirs(dell_emc_log_path)

logging.config.fileConfig('dellemc_log.conf',
                          defaults={'logfilename': dell_emc_log_path + '/dellemc_ansible_install.log'})

# create logger
logger = logging.getLogger('ansible')

print("Dell EMC OpenManage Ansible Modules v1.0 installation has started.")
logger.info('Dell EMC OpenManage Ansible Modules v1.0 installation has started.')
print("Checking prerequisites...")
print("")
logger.info('Checking prerequisites...')
# Check for Ansible installlisation with version
try:
    import ansible

    logger.info('Ansible is installed')
except:
    logger.info('Ansible is not installed.')
    sys.exit(1)

# check for ansible verson
required_version = '2.2.0'
installed_version = ansible.__version__
logger.info('Ansible v' + installed_version + ' is installed.')


def version_check(installed_version, required_version):
    installed_version_tuple = tuple([int(x) for x in installed_version.split('.')])
    required_version_tuple = tuple([int(x) for x in required_version.split('.')])
    return all(map(lambda x, y: x >= y, installed_version_tuple, required_version_tuple))


if version_check(installed_version, required_version):
    print("	Ansible version 2.2 or later is installed.")
else:
    print("Ansible version 2.2 or later is not installed.")
    print('Dell EMC OpenManage Ansible Modules v1.0 installation has failed.')
    logger.info('The Installed Ansible version is lesser than the required Ansible version.')
    sys.exit(1)

# check for omsdk installization

try:
    from omsdk.sdkinfra import sdkinfra

    print("	OpenManage Software Development Kit version 1.0 or later is installed.")
    logger.info('OpenManage Software Development Kit v1.0 is installed.')
except:
    print('OpenManage Software Development Kit version 1.0 or later is not installed.')
    print('Dell EMC OpenManage Ansible Modules v1.0 installation has failed.')
    sys.exit(1)

ansible_path = ansible.__path__[0]
# print("Ansible config path :" + ansible_path)
module_utils_path = ansible_path + '/module_utils/'
extras_path = ansible_path + '/modules/extras'
server_path = extras_path + '/dellemc'
dellemc_idrac_path = server_path + '/server'
log_root = '/var/log'
dell_emc_log_path = log_root + '/dellemc'

warning_message = "Dell EMC OpenManage Ansible Module 1.0 is already present. Do you want to overwrite? (y/n)  "


def update_check(message):
    yes = {'y', ''}
    print(" ")
    print(message)
    print("Press `y` to overwrite the Dell EMC OpenManage Ansible Modules specific folders and files...")
    print("Press any other key to exit installation (default: 'y'):")
    choice = input()
    if choice in yes:
        return True
    else:
        return False


if os.path.isdir(server_path):
    checking = update_check(warning_message)
    if not checking:
        sys.exit(1)

print("Installing Dell EMC OpenManage Ansible Modules specific folders and files...")
logger.info('Installing Dell EMC OpenManage Ansible Modules specific folders and files...')


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


def copy_files(src, dest):
    import shutil

    src_files = os.listdir(src)

    for file_name in src_files:
        src_file = os.path.join(src, file_name)
        dst_file = os.path.join(dest, file_name)
        if file_name != "install.py" and file_name != "uninstall.py" and file_name != "dellemc_log.conf":
            if (os.path.isfile(src_file)):
                shutil.copy(src_file, dst_file)
        elif file_name == "dellemc_log.conf":
            shutil.copy(src_file, os.path.join(dell_emc_log_path, file_name))


# Create the directory for the main module under extras/server/dellemc repo
if not os.path.isdir(dellemc_idrac_path):
    os.makedirs(dellemc_idrac_path)

touch(server_path + '/__init__.py')
touch(dellemc_idrac_path + '/__init__.py')

# Copy files from parent folder to dellemc_idrac_path
copy_files(os.getcwd(), dellemc_idrac_path)

# Copy files from library folder to dellemc_idrac_path
copy_files(os.getcwd() + '/library', dellemc_idrac_path)

# Copy common files to module_util
copy_files(os.getcwd() + '/utils', module_utils_path)
print("SUCCESS: Dell EMC OpenManage Ansible Modules v1.0 is installed successfully.")
logger.info("SUCCESS: Dell EMC OpenManage Ansible Modules v1.0 is installed successfully.")
