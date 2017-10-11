#! /usr/bin/python
# _*_ coding: utf-8 _*_

#
# Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved.
# Dell, EMC, and other trademarks are trademarks of Dell Inc. or its
# subsidiaries. Other trademarks may be trademarks of their respective owners.

import os
import sys

try:
    import ansible
except ImportError:
    print "Error: Ansible is not installed"
    sys.exit(1)

ansible_path = ansible.__path__[0]
module_utils_path = ansible_path + '/module_utils/'
remote_management__path = ansible_path + '/modules/remote_management'
dellemc_idrac_path = remote_management__path + '/dellemc_idrac'


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


def copy_files(src, dest):

    import shutil

    src_files = os.listdir(src)

    for file_name in src_files:
        src_file = os.path.join(src, file_name)
        dst_file = os.path.join(dest, file_name)

        if (os.path.isfile(src_file)):
            print(src_file, "===>", dst_file)
            shutil.copy(src_file, dst_file)

# Create the directory for the main module under remote_management/dellemc_idrac repo
if not os.path.isdir(dellemc_idrac_path):
    os.makedirs(dellemc_idrac_path)

touch(dellemc_idrac_path + '/__init__.py')

# Copy files from library folder to dellemc_idrac_path
copy_files(os.getcwd() + '/library', dellemc_idrac_path)

# Copy common files to module_util
copy_files(os.getcwd() + '/utils', module_utils_path)
