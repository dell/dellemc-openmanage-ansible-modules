#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 1.2
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


print("Dell EMC OpenManage Ansible Modules installation has started.")
print("Checking prerequisites...")

# checking prerequisites..
fail_message = "FAILED: Dell EMC OpenManage Ansible Modules installation failed."
try:
    import ansible
    from ansible.module_utils.six.moves import input
except ImportError as e:
    print("")
    print("Ansible is not installed.")
    print(fail_message)
    sys.exit(1)

# required path to check
ansible_installed_path = ansible.__path__[0]

# master contribution details:
contrib_files = {
    "module_utils/remote_management/dellemc/__init__.py": "ansible 2.8.0",
    "module_utils/remote_management/dellemc/dellemc_idrac.py": "ansible 2.8.0",
    "modules/remote_management/dellemc/__init__.py": "ansible 2.8.0",
    "modules/remote_management/dellemc/idrac/dellemc_idrac_firmware.py": "ansible 2.8.0",
    "modules/remote_management/dellemc/idrac/__init__.py": "ansible 2.8.0",
}

# ansible module path
dellemc_path = os.path.join(ansible_installed_path, "modules", "remote_management", "dellemc")
dellemc_idrac_path = os.path.join(ansible_installed_path, "modules", "remote_management", "dellemc", "idrac")
dellemc_ome_path = os.path.join(ansible_installed_path, "modules", "remote_management", "dellemc", "ome")

# ansible util path
dellemc_util_path = os.path.join(ansible_installed_path, "module_utils", "remote_management", "dellemc")
old_util_file = os.path.join(ansible_installed_path, "module_utils", "dellemc_idrac.py")

# dellemc local path
base_local_path = os.getcwd()
src_idrac_path = os.path.join(base_local_path, "library", "dellemc", "idrac")
src_ome_path = os.path.join(base_local_path, "library", "dellemc", "ome")
src_util_path = os.path.join(base_local_path, "utils")
idrac_util_exists = os.path.exists(os.path.join(dellemc_util_path, "dellemc_idrac.py"))
property_json = os.path.join(dellemc_path, "properties.json")
existing_files = set([k.split("/")[-1] for k, v in contrib_files.items()])
installation_message = "Installing Dell EMC OpenManage Ansible Modules specific folders and files..."
init_file = os.path.join(ansible_installed_path, "module_utils", "remote_management", "__init__.py")
extras = os.path.join(ansible_installed_path, "modules", "extras")


def copy_files(src, dest, keep_util=False):
    """
    Copying all files from one directory to ansible directory.
    """
    srclst = os.listdir(src)
    for f in srclst:
        if f.endswith(".py") and not (f in existing_files and keep_util):
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
    message = "Dell EMC OpenManage Ansible Modules is already present. Do you want to upgrade? (y/n)  "
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


def update_cleanup(*args):
    for f in args:
        if os.path.isdir(f):
            shutil.rmtree(f)
        if os.path.isfile(f):
            os.remove(f)


def complete_installation(keep_util=False):
    """
    Creating directory and copying files to ansible location.
    """
    if os.path.exists(dellemc_path) and os.path.exists(dellemc_util_path):
        if not os.path.exists(dellemc_idrac_path):
            shutil.copytree(os.path.join("library", "dellemc", "idrac"), dellemc_idrac_path)
        copy_files(src_idrac_path, dellemc_idrac_path, keep_util=keep_util)
        copy_files(src_util_path, dellemc_util_path, keep_util=keep_util)
        if not os.path.exists(dellemc_ome_path):
            shutil.copytree(os.path.join("library", "dellemc", "ome"), dellemc_ome_path)
        copy_files(src_ome_path, dellemc_ome_path)
    if not os.path.exists(dellemc_path):
        shutil.copytree(os.path.join("library", "dellemc"), dellemc_path)
    if not os.path.exists(dellemc_util_path):
        shutil.copytree("utils", dellemc_util_path)
        if not os.path.isfile(init_file):
            touch(init_file)


def install():
    """
    Creating module directory in Ansible location.
    """
    # Step 0: Upgrading dellemc modules with new directory structure.
    if os.path.exists(dellemc_path) or (os.path.exists(extras)):
        # Upgrade checking if dellemc modules are present.
        module_files = [f for f in glob.glob(os.path.join(dellemc_path, "idrac", "*.py"))]
        if os.path.exists(old_util_file) or len(module_files) > len(contrib_files) or (os.path.exists(extras)):
            checking = update_check()
            if not checking:
                return
        print(installation_message)
        # Cleaning up dellemc modules.
        if os.path.exists(dellemc_util_path):
            update_cleanup(old_util_file, property_json, extras)
            keep_util = True
        else:
            update_cleanup(dellemc_path, old_util_file, property_json, extras)
            keep_util = False
        # Complete installation with new directory structure, dellemc modules version 2.0.
        complete_installation(keep_util=keep_util)

    # Step 1: Installing complete dellemc modules if not present.
    elif not os.path.exists(dellemc_path):
        print(installation_message)
        # Complete installation with new directory structure, dellemc modules version 2.0.
        complete_installation(keep_util=False)

    print("SUCCESS: Dell EMC OpenManage Ansible Modules is installed successfully.")


if __name__ == "__main__":
    try:
        install()
    except (IOError, OSError) as e:
        print(str(e))
        print(fail_message)
        sys.exit(1)
