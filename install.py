#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0.5
# Copyright (C) 2019 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#


from __future__ import (absolute_import, division, print_function)
import os
import sys
import glob
import shutil


print("\nDell EMC OpenManage Ansible Modules installation has started.")
print("\nChecking prerequisites...\n")

# checking prerequisites..
fail_message = "\nFAILED: Dell EMC OpenManage Ansible Modules installation failed.\n"
try:
    import ansible
    from ansible.module_utils.six.moves import input
except ImportError as e:
    print("\tAnsible is not installed.")
    print(fail_message)
    sys.exit(1)

# required path to check
if 'ANSIBLE_LIBRARY' in os.environ:
    ansible_installed_path = os.environ['ANSIBLE_LIBRARY']
else:
    ansible_installed_path = ansible.__path__[0]

# master contribution details:
contrib_files = {
    "module_utils/remote_management/dellemc/__init__.py": "ansible 2.8.0",
    "module_utils/remote_management/dellemc/dellemc_idrac.py": "ansible 2.8.0",
    "modules/remote_management/dellemc/__init__.py": "ansible 2.8.0",
    "modules/remote_management/dellemc/idrac/idrac_firmware.py": "ansible 2.8.0",
    "modules/remote_management/dellemc/idrac/idrac_server_config_profile.py": "ansible 2.8.0",
    "modules/remote_management/dellemc/idrac/__init__.py": "ansible 2.8.0",
    "modules/remote_management/dellemc/ome_device_info.py": "ansible 2.9.0",
    "module_utils/remote_management/dellemc/ome.py": "ansible 2.9.0",
    "modules/remote_management/dellemc/idrac_firmware.py": "ansible 2.9.0",
    "modules/remote_management/dellemc/idrac_server_config_profile.py": "ansible 2.9.0",
}

# ansible module path
dellemc_path = os.path.join(ansible_installed_path, "modules", "remote_management", "dellemc")
dellemc_idrac_path = os.path.join(ansible_installed_path, "modules", "remote_management", "dellemc", "idrac")
dellemc_ome_path = os.path.join(ansible_installed_path, "modules", "remote_management", "dellemc", "ome")
dellemc_redfish_path = os.path.join(ansible_installed_path, "modules", "remote_management", "dellemc", "redfish")

# ansible util path
dellemc_util_path = os.path.join(ansible_installed_path, "module_utils", "remote_management", "dellemc")
old_util_file = os.path.join(ansible_installed_path, "module_utils", "dellemc_idrac.py")
old_ome_file = os.path.join(ansible_installed_path, "module_utils", "remote_management", "dellemc", "dellemc_ome.py")

# dellemc local path
base_local_path = os.getcwd()
src_idrac_path = os.path.join(base_local_path, "library", "dellemc", "idrac")
src_ome_path = os.path.join(base_local_path, "library", "dellemc", "ome")
src_redfish_path = os.path.join(base_local_path, "library", "dellemc", "redfish")
src_util_path = os.path.join(base_local_path, "utils")
idrac_util_exists = os.path.exists(os.path.join(dellemc_util_path, "dellemc_idrac.py"))
property_json = os.path.join(dellemc_path, "properties.json")
installation_message = "\tInstalling Dell EMC OpenManage Ansible Modules specific folders and files..."
init_file = os.path.join(ansible_installed_path, "module_utils", "remote_management", "__init__.py")
extras = os.path.join(ansible_installed_path, "modules", "extras")
deprecated_src_path = os.path.join(base_local_path, "deprecated")


def copy_files(src, dest):
    """
    Copying all files from one directory to ansible directory.
    """
    srclst = os.listdir(src)
    for f in srclst:
        if f.endswith(".py"):
            srcfile, destfile = os.path.join(src, f), os.path.join(dest, f)
            shutil.copy(srcfile, destfile)



def touch(fname, times=None):
    """
    Creating empty file in a directory.
    """
    with open(fname, 'a'):
        os.utime(fname, times)


def update_check():
    """
    checking whenever upgrade is required.
    """
    message = "\tDell EMC OpenManage Ansible Modules is already present. Do you want to upgrade? (y/n)?"
    yes = {'y', ''}
    print(message)
    print("\tPress `y` to update the Dell EMC OpenManage Ansible Modules specific folders and files...")
    print("\tPress any other key to exit installation (default: 'y'):")
    choice = input()
    if choice in yes:
        return True
    else:
        return False


def update_cleanup(*args):
    for f in args:
        if os.path.isdir(f):
            shutil.rmtree(f)
        if os.path.isfile(f):
            os.remove(f)


def complete_installation():
    """
    Creating directory and copying files to ansible location.
    """
    if os.path.exists(dellemc_path):
        copy_files(src_idrac_path, dellemc_path)
        copy_files(src_ome_path, dellemc_path)
        copy_files(src_redfish_path, dellemc_path)
        copy_files(src_util_path, dellemc_util_path)
    if not os.path.exists(dellemc_path):
        shutil.copytree(os.path.join("library", "dellemc", "idrac"), dellemc_path)
        copy_files(src_ome_path, dellemc_path)
        copy_files(src_redfish_path, dellemc_path)
    if not os.path.exists(dellemc_util_path):
        shutil.copytree(src_util_path, dellemc_util_path)
        if not os.path.isfile(init_file):
            touch(init_file)
    else:
        copy_files(src_util_path, dellemc_util_path)

    copy_files(deprecated_src_path, dellemc_path)


def install():
    """
    Creating module directory in Ansible location.
    """
    # Step 0: Upgrading dellemc modules with new directory structure.
    if os.path.exists(dellemc_path) or (os.path.exists(extras)):
        # Upgrade checking if dellemc modules are present.
        module_files = [f for f in glob.glob(os.path.join(dellemc_path, "*.py"))]
        if os.path.exists(old_util_file) or len(module_files) > len(contrib_files) or (os.path.exists(extras)) or \
                os.path.exists(dellemc_ome_path):
            checking = update_check()
            if not checking:
                return
        print(installation_message)
        # Cleaning up dellemc modules.
        if os.path.exists(dellemc_idrac_path) and os.path.exists(dellemc_ome_path):
            update_cleanup(dellemc_idrac_path, dellemc_ome_path)
        if os.path.exists(dellemc_idrac_path) and not os.path.exists(dellemc_ome_path):
            # Solve case
            # when OMAM 1.1 to 2.1 upgrade is done with ansible version lesser than 2.8.4
            # where idrac folder exists with contributed_file_lst.
            #in this case upgrade is not removing other than contributed files inside idrac folder
            contributed_file_lst = { dellemc_idrac_path+'/idrac_firmware.py',
                                     dellemc_idrac_path+'/idrac_server_config_profile.py'}
            old_module_idrac_files = [f for f in glob.glob(os.path.join(dellemc_idrac_path, "*.py"))]
            removed_module = list(set(old_module_idrac_files) - contributed_file_lst)
            if len(old_module_idrac_files) == len(removed_module):
                update_cleanup(dellemc_idrac_path)
            else:
                update_cleanup(*removed_module)
        update_cleanup(old_util_file, property_json, extras, old_ome_file)
    # Step 1: Installing complete dellemc modules if not present.
    elif not os.path.exists(dellemc_path):
        print(installation_message)
    # Complete installation with new directory structure, dellemc modules version 2.0.
    complete_installation()

    print("\nSUCCESS: Dell EMC OpenManage Ansible Modules is installed successfully.\n")


if __name__ == "__main__":
    try:
        install()
    except (IOError, OSError) as e:
        print(str(e))
        print(fail_message)
        sys.exit(1)
