#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0.8
# Copyright (C) 2019-2020 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of
# Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

"""
Un-installation of DellEMC OpenManage Ansible Module.
"""

import os
import re
import sys
import glob
import shutil

# print colors
FAIL = "\033[91m"  # RED
SUCCESS = "\033[92m"  # GREEN
NORMAL = "\033[00m"  # DEFAULT

NO_ANSIBLE_MESSAGE = "\nDell EMC OpenManage Ansible Modules is not " \
                     "installed.\n"
# if any one of them are present proceeding with further process.
STARTED_MESSAGE = "Dell EMC OpenManage Ansible Modules uninstallation has " \
                  "started."
FOLDER_MESSAGE = "\n\tUninstalling Dell EMC OpenManage Ansible Modules " \
                 "specific folders and files...\n"
SUCCESS_MESSAGE = "SUCCESS: Dell EMC OpenManage Ansible Modules is " \
                  "uninstalled successfully."
FAILED_MESSAGE = "FAILED: Dell EMC OpenManage Ansible Modules uninstallation" \
                 " failed."
START_END = "-------------------------------------------------------------" \
            "------------------------------------"

try:
    import ansible
except ImportError:
    print("\n" + START_END)
    print(FAIL + "{0}".format(NO_ANSIBLE_MESSAGE) + NORMAL)
    print(START_END + "\n")
    sys.exit(1)

try:
    # Ansible and dellemc installed location path.
    if 'ANSIBLE_LIBRARY' in os.environ:
        ANSIBLE_INSTALLED_PATH = os.environ['ANSIBLE_LIBRARY']
    else:
        ANSIBLE_INSTALLED_PATH = ansible.__path__[0]
        ANSIBLE_VERSION = ansible.__version__
except (AttributeError, TypeError):
    print("\n" + START_END)
    print(FAIL + "{0}".format(NO_ANSIBLE_MESSAGE) + NORMAL)
    print(START_END + "\n")
    sys.exit(1)

# dellemc module path
DELLEMC_PATH = os.path.join(ANSIBLE_INSTALLED_PATH, "modules",
                            "remote_management", "dellemc")
DELLEMC_IDRAC_PATH = os.path.join(ANSIBLE_INSTALLED_PATH, "modules",
                                  "remote_management", "dellemc", "idrac")
DELLEMC_OME_PATH = os.path.join(ANSIBLE_INSTALLED_PATH, "modules",
                                "remote_management", "dellemc", "ome")
DELLEMC_REDFISH_PATH = os.path.join(ANSIBLE_INSTALLED_PATH, "modules",
                                    "remote_management", "dellemc", "redfish")

# dellemc util path
DELLEMC_UTIL_PATH = os.path.join(ANSIBLE_INSTALLED_PATH, "module_utils",
                                 "remote_management", "dellemc")
OLD_UTIL_FILE = os.path.join(ANSIBLE_INSTALLED_PATH, "module_utils",
                             "dellemc_idrac.py")

# contributed module details for skipping if ansible 2.8 or more than exists.
CONTRIB_MODULE_FILES = {
    os.path.join(ANSIBLE_INSTALLED_PATH,
                 "modules/remote_management/dellemc/idrac/"
                 "idrac_firmware.py"): "ansible 2.8.0",
    os.path.join(ANSIBLE_INSTALLED_PATH,
                 "modules/remote_management/dellemc/idrac"
                 "/idrac_server_config_profile.py"): "ansible 2.8.0",
    os.path.join(ANSIBLE_INSTALLED_PATH,
                 "modules/remote_management/dellemc/idrac"
                 "/__init__.py"): "ansible 2.8.0",
    os.path.join(ANSIBLE_INSTALLED_PATH,
                 "modules/remote_management/dellemc/"
                 "__init__.py"): "ansible 2.8.0",
    os.path.join(ANSIBLE_INSTALLED_PATH,
                 "modules/remote_management/dellemc/"
                 "ome_device_info.py"): "ansible 2.9.0",
    os.path.join(ANSIBLE_INSTALLED_PATH,
                 "modules/remote_management/dellemc/"
                 "__init__.py"): "ansible 2.8.4",
    os.path.join(ANSIBLE_INSTALLED_PATH,
                 "modules/remote_management/dellemc/"
                 "idrac_firmware.py"): "ansible 2.8.4",
    os.path.join(ANSIBLE_INSTALLED_PATH,
                 "modules/remote_management/dellemc"
                 "/idrac_server_config_profile.py"): "ansible 2.8.4",
}
CONTRIB_UTIL_FILES = {
    os.path.join(ANSIBLE_INSTALLED_PATH,
                 "module_utils/remote_management/dellemc/"
                 "dellemc_idrac.py"): "ansible 2.8.0",
    os.path.join(ANSIBLE_INSTALLED_PATH,
                 "module_utils/remote_management/dellemc/"
                 "__init__.py"): "ansible 2.8.0",
    os.path.join(ANSIBLE_INSTALLED_PATH,
                 "module_utils/remote_management/dellemc/"
                 "ome.py"): "ansible 2.9.0",
}

# Any of the path is not present exit with message.
if not any(os.path.exists(exists) for exists in
           (DELLEMC_PATH, DELLEMC_UTIL_PATH, OLD_UTIL_FILE)):
    print("\n" + START_END)
    print(FAIL + "{0}".format(NO_ANSIBLE_MESSAGE) + NORMAL)
    print(START_END + "\n")
    sys.exit(1)


def complete_remove(*args):
    """Completely removing folders, except contributed files or folders."""
    for arg in args:
        if os.path.isdir(arg):
            shutil.rmtree(arg)
        if os.path.isfile(arg):
            os.remove(arg)


def check_ome_contributed():
    """Checks if contributed files present or not."""
    is_contributed = False
    if not os.path.exists(DELLEMC_IDRAC_PATH):
        is_contributed = True
    return is_contributed


def version_check(version):
    """Data type conversion of ansible version."""
    return tuple(map(int, (version.split("."))))


def uninstall():
    """Uninstalling Dell EMC ansible modules from ansible core repository."""
    version = re.match(r"(\d.\d)", ANSIBLE_VERSION).group()
    # listing out all the installed modules from the location.
    module_files = [f for f in glob.glob(os.path.join(DELLEMC_PATH, "*.py"))]
    # listing out all the utility files from the installed location.
    util_files = [f for f in
                  glob.glob(os.path.join(DELLEMC_UTIL_PATH, "*.py"))]
    # Step 1: checking the installed ansible version,
    # if it's more than 2.8 or equal skipping contributed modules.
    if all(map(lambda x, y: x <= y, (2, 8),
               tuple(map(int, version.split("."))))):
        if len(module_files) > len(CONTRIB_MODULE_FILES):
            # skipping contributed modules/utility files from installed
            # location.
            removed_module = list(
                set(module_files) - set(CONTRIB_MODULE_FILES.keys()))
            removed_util = list(
                set(util_files) - set(CONTRIB_UTIL_FILES.keys()))
            removed_module.extend(removed_util)
            removed_module.append(DELLEMC_OME_PATH)
            removed_module.append(DELLEMC_REDFISH_PATH)
            if version_check(ANSIBLE_VERSION) < version_check("2.9.0"):
                # remove ome modules if ansible version is lower than 2.9
                remove_module_list, remove_modules_dict = [], {}
                remove_modules_dict.update(CONTRIB_MODULE_FILES)
                remove_modules_dict.update(CONTRIB_UTIL_FILES)
                for key, val in remove_modules_dict.items():
                    if val == "ansible 2.9.0" or \
                            (val == "ansible 2.8.4" and
                             version_check(ANSIBLE_VERSION) <
                             version_check("2.8.4")) and \
                            "__init__" not in key:
                        remove_module_list.append(key)
                removed_module.extend(remove_module_list)
            print("\n" + START_END)
            print(STARTED_MESSAGE)
            print(FOLDER_MESSAGE)
            # removing installed files.
            complete_remove(*removed_module)
            print(SUCCESS + "{0}".format(SUCCESS_MESSAGE) + NORMAL)
            print(START_END + "\n")
        elif os.path.exists(DELLEMC_IDRAC_PATH) and not os.path.exists(
                DELLEMC_OME_PATH):
            # Solve case
            # when OMAM 1.1 to 2.1 upgrade is done with ansible version
            # lesser than 2.8.4
            # where idrac folder exists with contributed_file_lst.
            # in this case upgrade is not removing other than contributed
            # files inside idrac folder
            # idrac_util_exists = os.path.exists(os.path.join(
            # DELLEMC_UTIL_PATH, "dellemc_idrac.py"))
            property_json = os.path.join(DELLEMC_PATH, "properties.json")
            extras = os.path.join(ANSIBLE_INSTALLED_PATH, "modules", "extras")
            old_ome_file = os.path.join(ANSIBLE_INSTALLED_PATH, "module_utils",
                                        "remote_management", "dellemc",
                                        "dellemc_ome.py")
            contributed_file_lst = {DELLEMC_IDRAC_PATH + '/idrac_firmware.py',
                                    DELLEMC_IDRAC_PATH +
                                    '/idrac_server_config_profile.py'}
            old_module_idrac_files = [f for f in glob.glob(
                os.path.join(DELLEMC_IDRAC_PATH, "*.py"))]
            removed_module = list(
                set(old_module_idrac_files) - contributed_file_lst)
            if len(old_module_idrac_files) == len(removed_module):
                complete_remove(DELLEMC_IDRAC_PATH)
            else:
                complete_remove(*removed_module)
            print("\n" + START_END)
            print(STARTED_MESSAGE)
            print(FOLDER_MESSAGE)
            complete_remove(OLD_UTIL_FILE, property_json, extras, old_ome_file)
            print(SUCCESS + "{0}".format(SUCCESS_MESSAGE) + NORMAL)
            print(START_END + "\n")
        else:
            print("\n" + START_END)
            print(FAIL + "{0}".format(NO_ANSIBLE_MESSAGE) + NORMAL)
            print(START_END + "\n")
    # Step 2: installed ansible version is less than 2.8,
    # removing all the files from installed location.
    elif any(map(lambda x, y: x <= y, tuple(map(int, version.split("."))),
                 (2, 8))):
        print("\n" + START_END)
        print(STARTED_MESSAGE)
        print(FOLDER_MESSAGE)
        complete_remove(DELLEMC_PATH, DELLEMC_UTIL_PATH, OLD_UTIL_FILE)
        print(SUCCESS + "{0}".format(SUCCESS_MESSAGE) + NORMAL)
        print(START_END + "\n")
    # Step 3: If ansible is not installed showing error message.
    else:
        print("\n" + START_END)
        print(FAIL + "{0}".format(NO_ANSIBLE_MESSAGE) + NORMAL)
        print(START_END + "\n")


if __name__ == "__main__":
    try:
        uninstall()
    except (IOError, OSError) as err:
        print(str(err))
        print("\n" + START_END)
        print(FAIL + "{0}".format(FAILED_MESSAGE) + NORMAL)
        print(START_END + "\n")
        sys.exit(1)
