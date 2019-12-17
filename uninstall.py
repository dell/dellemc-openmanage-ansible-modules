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


import os
import re
import sys
import glob
import shutil


no_ansible_message = "Dell EMC OpenManage Ansible Modules is not installed."
# if any one of them are present proceeding with further process.
started_message = "Dell EMC OpenManage Ansible Modules uninstallation has started."
folder_message = "Uninstalling Dell EMC OpenManage Ansible Modules specific folders and files..."
success_message = "SUCCESS: Dell EMC OpenManage Ansible Modules is uninstalled successfully."
failed_message = "FAILED: Dell EMC OpenManage Ansible Modules uninstallation failed."

try:
    import ansible
except ImportError:
    print(no_ansible_message)
    sys.exit(1)

# Ansible and dellemc installed location path.
if 'ANSIBLE_LIBRARY' in os.environ:
    ansible_installed_path = os.environ['ANSIBLE_LIBRARY']
else:
    ansible_installed_path = ansible.__path__[0]
ansible_version = ansible.__version__

# dellemc module path
dellemc_path = os.path.join(ansible_installed_path, "modules", "remote_management", "dellemc")
dellemc_idrac_path = os.path.join(ansible_installed_path, "modules", "remote_management", "dellemc", "idrac")
dellemc_ome_path = os.path.join(ansible_installed_path, "modules", "remote_management", "dellemc", "ome")
dellemc_redfish_path = os.path.join(ansible_installed_path, "modules", "remote_management", "dellemc", "redfish")

# dellemc util path
dellemc_util_path = os.path.join(ansible_installed_path, "module_utils", "remote_management", "dellemc")
old_util_file = os.path.join(ansible_installed_path, "module_utils", "dellemc_idrac.py")

# contributed module details for skipping if ansible 2.8 or more than exists.
contrib_module_files = {
    os.path.join(ansible_installed_path,
                 "modules/remote_management/dellemc/idrac/idrac_firmware.py"): "ansible 2.8.0",
    os.path.join(ansible_installed_path,
                 "modules/remote_management/dellemc/idrac/idrac_server_config_profile.py"): "ansible 2.8.0",
    os.path.join(ansible_installed_path,
                 "modules/remote_management/dellemc/idrac/__init__.py"): "ansible 2.8.0",
    os.path.join(ansible_installed_path,
                 "modules/remote_management/dellemc/__init__.py"): "ansible 2.8.0",
    os.path.join(ansible_installed_path,
                 "modules/remote_management/dellemc/ome_device_info.py"): "ansible 2.9.0",
    os.path.join(ansible_installed_path,
                 "modules/remote_management/dellemc/__init__.py"): "ansible 2.8.4",
    os.path.join(ansible_installed_path,
                 "modules/remote_management/dellemc/idrac_firmware.py"): "ansible 2.8.4",
    os.path.join(ansible_installed_path,
                 "modules/remote_management/dellemc/idrac_server_config_profile.py"): "ansible 2.8.4",
}
contrib_util_files = {
    os.path.join(ansible_installed_path,
                 "module_utils/remote_management/dellemc/dellemc_idrac.py"): "ansible 2.8.0",
    os.path.join(ansible_installed_path,
                 "module_utils/remote_management/dellemc/__init__.py"): "ansible 2.8.0",
    os.path.join(ansible_installed_path,
                 "module_utils/remote_management/dellemc/ome.py"): "ansible 2.9.0",
}

# Any of the path is not present exit with message.
if not any(os.path.exists(exists) for exists in (dellemc_path, dellemc_util_path, old_util_file)):
    print(no_ansible_message)
    sys.exit(1)


def complete_remove(*args):
    """Completely removing folders, except contributed files or folders."""
    for arg in args:
        if os.path.isdir(arg):
            shutil.rmtree(arg)
        if os.path.isfile(arg):
            os.remove(arg)
    return


def check_ome_contributed():
    is_contributed = False
    if not os.path.exists(dellemc_idrac_path):
        is_contributed = True
    return is_contributed


def version_check(v):
    return tuple(map(int, (v.split("."))))


def uninstall():
    """Uninstalling Dell EMC ansible modules from ansible core repository."""
    version = re.match(r"(\d.\d)", ansible_version).group()
    # listing out all the installed modules from the location.
    module_files = [f for f in glob.glob(os.path.join(dellemc_path, "*.py"))]
    # listing out all the utility files from the installed location.
    util_files = [f for f in glob.glob(os.path.join(dellemc_util_path, "*.py"))]
    # Step 1: checking the installed ansible version,
    # if it's more than 2.8 or equal skipping contributed modules.
    if all(map(lambda x, y: x <= y, (2, 8), tuple(map(int, version.split("."))))):
        if len(module_files) > len(contrib_module_files):
            # skipping contributed modules/utility files from installed location.
            removed_module = list(set(module_files) - set(contrib_module_files.keys()))
            removed_util = list(set(util_files) - set(contrib_util_files.keys()))
            removed_module.extend(removed_util)
            removed_module.append(dellemc_ome_path)
            removed_module.append(dellemc_redfish_path)
            if version_check(ansible_version) < version_check("2.9.0"):
                # remove ome modules if ansible version is lower than 2.9
                remove_module_list, remove_modules_dict = [], {}
                remove_modules_dict.update(contrib_module_files)
                remove_modules_dict.update(contrib_util_files)
                for key, val in remove_modules_dict.items():
                    if (val == "ansible 2.9.0" or (val == "ansible 2.8.4" and
                                                   version_check(ansible_version) < version_check("2.8.4"))) \
                            and not "__init__" in key:
                        remove_module_list.append(key)
                removed_module.extend(remove_module_list)
            print(started_message)
            print(folder_message)
            # removing installed files.
            complete_remove(*removed_module)
            print(success_message)
        elif os.path.exists(dellemc_idrac_path) and not os.path.exists(dellemc_ome_path):
            # Solve case
            # when OMAM 1.1 to 2.1 upgrade is done with ansible version lesser than 2.8.4
            # where idrac folder exists with contributed_file_lst.
            #in this case upgrade is not removing other than contributed files inside idrac folder
            idrac_util_exists = os.path.exists(os.path.join(dellemc_util_path, "dellemc_idrac.py"))
            property_json = os.path.join(dellemc_path, "properties.json")
            extras = os.path.join(ansible_installed_path, "modules", "extras")
            old_ome_file = os.path.join(ansible_installed_path, "module_utils", "remote_management", "dellemc", "dellemc_ome.py")
            contributed_file_lst = { dellemc_idrac_path+'/idrac_firmware.py',
                                     dellemc_idrac_path+'/idrac_server_config_profile.py'}
            old_module_idrac_files = [f for f in glob.glob(os.path.join(dellemc_idrac_path, "*.py"))]
            removed_module = list(set(old_module_idrac_files) - contributed_file_lst)
            if len(old_module_idrac_files) == len(removed_module):
                complete_remove(dellemc_idrac_path)
            else:
                complete_remove(*removed_module)
            print(started_message)
            print(folder_message)
            complete_remove(old_util_file, property_json, extras, old_ome_file)
            print(success_message)
        else:
            print(no_ansible_message)
    # Step 2: installed ansible version is less than 2.8,
    # removing all the files from installed location.
    elif any(map(lambda x, y: x <= y, tuple(map(int, version.split("."))), (2, 8))):
        print(started_message)
        print(folder_message)
        complete_remove(dellemc_path, dellemc_util_path, old_util_file)
        print(success_message)
    # Step 3: If ansible is not installed showing error message.
    else:
        print(no_ansible_message)


if __name__ == "__main__":
    try:
        uninstall()
    except (IOError, OSError) as err:
        print(str(err))
        print(failed_message)
        sys.exit(1)
