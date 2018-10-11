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
import logging.config
import shutil
try:
    log_root = '.'
    dell_emc_log_path = log_root + '/dellemc'
    dell_emc_log_file = dell_emc_log_path + '/dellemc_log.conf'
    logging.config.fileConfig(dell_emc_log_file, defaults={'logfilename': dell_emc_log_path + '/dellemc_ansible_uninstall.log'})
except Exception as e:
    print('Dell EMC OpenManage Ansible Modules v1.0 is not installed.')
    sys.exit(1)

# create logger
logger = logging.getLogger('ansible')


try:
    import ansible

except:
    logger.error('Ansible is not installed')
    sys.exit(1)
try:
    logger.info('Finding Dell EMC OpenManage Ansible Modules specific folders and files path details....')
    ansible_path = ansible.__path__[0]
    module_utils_path = ansible_path + '/module_utils/'
    extras_path = ansible_path + '/modules/extras'
    server_path = extras_path + '/dellemc'
    dellemc_idrac_path = server_path + '/server'

    if not os.path.isfile(module_utils_path + 'dellemc_idrac.py'):
        sys.exit(1)
except:
    logger.error(" Dell EMC OpenManage Ansible Modules v1.0 is not installed.")
    sys.exit(1)

print("Dell EMC OpenManage Ansible Modules v1.0 uninstallation has started.")
logger.info('Dell EMC OpenManage Ansible Modules v1.0 uninstallation has started.')

print("Uninstalling Dell EMC OpenManage Ansible Modules specific folders and files...")
logger.info('Uninstalling Dell EMC OpenManage Ansible Modules specific folders and files...')


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

if os.path.isfile(module_utils_path + 'dellemc_idrac.py'):
    os.remove(module_utils_path + 'dellemc_idrac.py')
    print("SUCCESS: Dell EMC OpenManage Ansible Modules v1.0 is uninstalled successfully.")
else:
    print("SUCCESS: Dell EMC OpenManage Ansible Modules v1.0 is uninstalled successfully.")

