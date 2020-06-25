#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0.11
# Copyright (C) 2019-2020 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of
# Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

"""
Installation of DellEMC OpenManage Ansible Module.
"""

from __future__ import (absolute_import, division, print_function)
import os
import sys
import glob
import shutil

print("\n-------------------------------------------------------------"
      "------------------------------------")
print("Dell EMC OpenManage Ansible Modules installation has started.")
print("\nChecking prerequisites...\n")

# checking prerequisites..
FAIL_MESSAGE = "\nFAILED: Dell EMC OpenManage Ansible Modules " \
               "installation failed."

# print colors
FAIL = "\033[91m"  # RED
SUCCESS = "\033[92m"  # GREEN
NORMAL = "\033[00m"  # DEFAULT

try:
    import ansible
    from ansible.module_utils.six.moves import input
except ImportError:
    print("\tAnsible is not installed.")
    print(FAIL + " {0}".format(FAIL_MESSAGE) + NORMAL)
    print("---------------------------------------------------------"
          "----------------------------------------\n")
    sys.exit(1)

# required path to check
if 'ANSIBLE_LIBRARY' in os.environ:
    ANSIBLE_INSTALLED_PATH = os.environ['ANSIBLE_LIBRARY']
else:
    ANSIBLE_INSTALLED_PATH = ansible.__path__[0]

# master contribution details:
CONTRIB_FILES = {
    "module_utils/remote_management/dellemc/__init__.py": "ansible 2.8.0",
    "module_utils/remote_management/dellemc/dellemc_idrac.py": "ansible 2.8.0",
    "modules/remote_management/dellemc/__init__.py": "ansible 2.8.0",
    "modules/remote_management/dellemc/idrac/idrac_firmware.py":
        "ansible 2.8.0",
    "modules/remote_management/dellemc/idrac/idrac_server_config_profile.py":
        "ansible 2.8.0",
    "modules/remote_management/dellemc/idrac/__init__.py": "ansible 2.8.0",
    "modules/remote_management/dellemc/ome_device_info.py": "ansible 2.9.0",
    "module_utils/remote_management/dellemc/ome.py": "ansible 2.9.0",
    "modules/remote_management/dellemc/idrac_firmware.py": "ansible 2.9.0",
    "modules/remote_management/dellemc/idrac_server_config_profile.py":
        "ansible 2.9.0",
}

# ansible module path
DELLEMC_PATH = os.path.join(ANSIBLE_INSTALLED_PATH, "modules",
                            "remote_management", "dellemc")
DELLEMC_IDRAC_PATH = os.path.join(ANSIBLE_INSTALLED_PATH, "modules",
                                  "remote_management", "dellemc", "idrac")
DELLEMC_OME_PATH = os.path.join(ANSIBLE_INSTALLED_PATH, "modules",
                                "remote_management", "dellemc", "ome")
DELLEMC_REDFISH_PATH = os.path.join(ANSIBLE_INSTALLED_PATH, "modules",
                                    "remote_management", "dellemc", "redfish")

# ansible util path
DELLEMC_UTIL_PATH = os.path.join(ANSIBLE_INSTALLED_PATH, "module_utils",
                                 "remote_management", "dellemc")
OLD_UTIL_PATH = os.path.join(ANSIBLE_INSTALLED_PATH, "module_utils",
                             "dellemc_idrac.py")
OLD_OME_FILE = os.path.join(ANSIBLE_INSTALLED_PATH, "module_utils",
                            "remote_management", "dellemc", "dellemc_ome.py")

# dellemc local path
BASE_LOCAL_PATH = os.getcwd()
SRC_IDRAC_PATH = os.path.join(BASE_LOCAL_PATH, "library", "dellemc", "idrac")
SRC_OME_PATH = os.path.join(BASE_LOCAL_PATH, "library", "dellemc", "ome")
SRC_REDFISH_PATH = os.path.join(BASE_LOCAL_PATH, "library", "dellemc",
                                "redfish")
SRC_UTIL_PATH = os.path.join(BASE_LOCAL_PATH, "utils")
IDRAC_UTIL_EXISTS = os.path.exists(
    os.path.join(DELLEMC_UTIL_PATH, "dellemc_idrac.py"))
PROPERTY_JSON = os.path.join(DELLEMC_PATH, "properties.json")
INSTALLATION_MESSAGE = "\n\tInstalling Dell EMC OpenManage Ansible " \
                       "Modules specific folders and files..."
INIT_FILE = os.path.join(ANSIBLE_INSTALLED_PATH, "module_utils",
                         "remote_management", "__init__.py")
EXTRAS = os.path.join(ANSIBLE_INSTALLED_PATH, "modules", "extras")
DEPRECATED_SRC_PATH = os.path.join(BASE_LOCAL_PATH, "deprecated")
DELLEMC_OME_FIRMWARE = os.path.join(ANSIBLE_INSTALLED_PATH, "modules",
                                    "remote_management",
                                    "dellemc", "dellemc_ome_firmware.py")
DELLEMC_OME_JOB_FACTS = os.path.join(ANSIBLE_INSTALLED_PATH, "modules",
                                     "remote_management",
                                     "dellemc", "dellemc_ome_job_facts.py")


def copy_files(src, dest):
    """
    Copying all files from one directory to ansible directory.
    """
    srclst = os.listdir(src)
    for fle in srclst:
        if fle.endswith(".py"):
            srcfile, destfile = os.path.join(src, fle), os.path.join(dest, fle)
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
    message = "\tDell EMC OpenManage Ansible Modules is already present." \
              " Do you want to upgrade? (y/n)?"
    yes = {'y', '', 'Y'}
    print(message)
    print("\tPress `y` to update the Dell EMC OpenManage Ansible Modules"
          " specific folders and files...")
    choice = input("\tPress any other key to exit installation "
                   "(default: 'y'):")
    return choice in yes


def update_cleanup(*args):
    """
    update_cleanup
    """
    for fle in args:
        if os.path.isdir(fle):
            shutil.rmtree(fle)
        if os.path.isfile(fle):
            os.remove(fle)


def complete_installation():
    """
    Creating directory and copying files to ansible location.
    """
    if os.path.exists(DELLEMC_PATH):
        copy_files(SRC_IDRAC_PATH, DELLEMC_PATH)
        copy_files(SRC_OME_PATH, DELLEMC_PATH)
        copy_files(SRC_REDFISH_PATH, DELLEMC_PATH)
        copy_files(SRC_UTIL_PATH, DELLEMC_UTIL_PATH)
    if not os.path.exists(DELLEMC_PATH):
        shutil.copytree(os.path.join("library", "dellemc", "idrac"),
                        DELLEMC_PATH)
        copy_files(SRC_OME_PATH, DELLEMC_PATH)
        copy_files(SRC_REDFISH_PATH, DELLEMC_PATH)
    if not os.path.exists(DELLEMC_UTIL_PATH):
        shutil.copytree(SRC_UTIL_PATH, DELLEMC_UTIL_PATH)
        if not os.path.isfile(INIT_FILE):
            touch(INIT_FILE)
    else:
        copy_files(SRC_UTIL_PATH, DELLEMC_UTIL_PATH)

    copy_files(DEPRECATED_SRC_PATH, DELLEMC_PATH)


def install():
    """
    Creating module directory in Ansible location.
    """
    # Step 0: Upgrading dellemc modules with new directory structure.
    operation_message = 'installed'
    if os.path.exists(DELLEMC_PATH) or (os.path.exists(EXTRAS)):
        # Upgrade checking if dellemc modules are present.
        module_files = [f for f in
                        glob.glob(os.path.join(DELLEMC_PATH, "*.py"))]
        if os.path.exists(OLD_UTIL_PATH) or len(module_files) > len(
                CONTRIB_FILES) or (os.path.exists(EXTRAS)) or \
                os.path.exists(DELLEMC_OME_PATH):
            checking = update_check()
            if not checking:
                print(FAIL + "\n{0}".format("Aborting upgrade...") + NORMAL)
                print("----------------------------------------------------"
                      "---------------------------------------------\n")
                return
            operation_message = 'upgraded'
        print(INSTALLATION_MESSAGE)
        # Cleaning up dellemc modules.
        if os.path.exists(DELLEMC_IDRAC_PATH) and os.path.exists(
                DELLEMC_OME_PATH):
            update_cleanup(DELLEMC_IDRAC_PATH, DELLEMC_OME_PATH)
        if os.path.exists(DELLEMC_IDRAC_PATH) and not os.path.exists(
                DELLEMC_OME_PATH):
            # Solve case
            # when OMAM 1.1 to 2.1 upgrade is done with ansible version
            # lesser than 2.8.4
            # where idrac folder exists with contributed_file_lst.
            # in this case upgrade is not removing other than contributed
            # files inside idrac folder
            contributed_file_lst = {DELLEMC_IDRAC_PATH + '/idrac_firmware.py',
                                    DELLEMC_IDRAC_PATH +
                                    '/idrac_server_config_profile.py'}
            old_module_idrac_files = [f for f in glob.glob(
                os.path.join(DELLEMC_IDRAC_PATH, "*.py"))]
            removed_module = list(
                set(old_module_idrac_files) - contributed_file_lst)
            if len(old_module_idrac_files) == len(removed_module):
                update_cleanup(DELLEMC_IDRAC_PATH)
            else:
                update_cleanup(*removed_module)
        update_cleanup(OLD_UTIL_PATH, PROPERTY_JSON, EXTRAS, OLD_OME_FILE,
                       DELLEMC_OME_FIRMWARE, DELLEMC_OME_JOB_FACTS)
    # Step 1: Installing complete dellemc modules if not present.
    elif not os.path.exists(DELLEMC_PATH):
        print(INSTALLATION_MESSAGE)
    # Complete installation with new directory structure, dellemc modules
    # version 2.0.
    complete_installation()
    print("\nDell EMC OpenMange Ansible Modules are present in: {0} \n"
          "".format(DELLEMC_PATH))
    print(SUCCESS + "SUCCESS: Dell EMC OpenManage Ansible Modules - {0} "
                    "successfully.".format(operation_message) + NORMAL)
    print("-----------------------------------------------------------"
          "--------------------------------------\n")


if __name__ == "__main__":
    try:
        install()
    except (IOError, OSError) as err:
        print(str(err))
        print(FAIL + " {0}".format(FAIL_MESSAGE) + NORMAL)
        sys.exit(1)
