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


from __future__ import (absolute_import, division, print_function)


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_install_firmware
short_description: Firmware update from a repository on a network share (CIFS, NFS).
version_added: "2.3"
description:
    - Update the Firmware by connecting to a network share (either CIFS or NFS) that contains a catalog of
        available updates.
    - Network share should contain a valid repository of Update Packages (DUPs) and a catalog file describing the DUPs.
    - All applicable updates contained in the repository are applied to the system.
    - This feature is available only with iDRAC Enterprise License.
options:
    idrac_ip:
        required: True
        description: iDRAC IP Address.
    idrac_user:
        required: True
        description: iDRAC username.
    idrac_pwd:
        required: True
        description: iDRAC user password.
    idrac_port:
        required: False
        description: iDRAC port.
        default: 443
    share_name:
        required: True
        description: CIFS or NFS Network share.
    share_user:
        required: True
        description: Network share user in the format 'user@domain' if user is part of a domain else 'user'.
    share_pwd:
        required: True
        description: Network share user password.
    share_mnt:
        required: True
        description: Local mount path of the network share with read-write permission for ansible user.
    reboot:
        required: False
        description: Whether to reboots after applying the updates or not.
        default: False
        choices: [True,  False]
    job_wait:
        required:  True
        description: Whether to wait for job completion or not.
        choices: [True,  False]

requirements:
    - "omsdk"
    - "python >= 2.7.5"
author: "Rajeev Arakkal (@rajeevarakkal)"
"""

EXAMPLES = """
---
- name: Update firmware from repository on a Network Share
  dellemc_install_firmware:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_pwd:  "xxxxxxxx"
       share_name: "xx.xx.xx.xx:/share"
       share_user: "xxxx"
       share_pwd:  "xxxxxxxx"
       share_mnt: "/mnt/share"
       reboot:     True
       job_wait:   True
"""

RETURN = """
dest:
    description: Updates firmware from a repository on a network share (CIFS, NFS).
    returned: success
    type: string
"""


from ansible.module_utils.dellemc_idrac import iDRACConnection, logger
from ansible.module_utils.basic import AnsibleModule
try:
    from omsdk.sdkcreds import UserCredentials
    from omsdk.sdkfile import FileOnShare
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False


def run_update_fw_from_nw_share(idrac, module):
    """
    Update firmware from a network share
    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    logger.info(module.params['idrac_ip'] + ': STARTING: Update Firmware From Network Share Method')
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    err = False

    try:
        if module.check_mode:
            msg['changed'] = True
        else:

            logger.info(module.params['idrac_ip'] + ': CALLING: File on share OMSDK API')
            upd_share = FileOnShare(remote=module.params['share_name'] + "/Catalog.xml",
                                    mount_point=module.params['share_mnt'],
                                    isFolder=False,
                                    creds=UserCredentials(
                                        module.params['share_user'],
                                        module.params['share_pwd'])
                                    )
            logger.info(module.params['idrac_ip'] + ': FINISHED: File on share OMSDK API')

            idrac.use_redfish = True
            if '12' in idrac.ServerGeneration or '13' in idrac.ServerGeneration:
                idrac.use_redfish = False

            # upd_share_file_path = upd_share.new_file("Catalog.xml")

            apply_update = True
            logger.info(module.params['idrac_ip'] + ': STARTING: Update Firmware From Network Share Method:'
                                                    ' Invoking OMSDK Firmware update API')
            msg['msg'] = idrac.update_mgr.update_from_repo(upd_share,
                                                           apply_update,
                                                           module.params['reboot'],
                                                           module.params['job_wait'])

            logger.info(module.params['idrac_ip'] + ': FINISHED: Update Firmware From Network Share Method:'
                                                    ' Invoking OMSDK Firmware update API')
            if "Status" in msg['msg']:
                if msg['msg']['Status'] == "Success":
                    if module.params['job_wait'] == True:
                        msg['changed'] = True
                else:
                    msg['failed'] = True

    except Exception as e:
        logger.error(module.params['idrac_ip'] + ': EXCEPTION: Update Firmware From Network Share Method: ' + str(e))
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True

    logger.info(module.params['idrac_ip'] + ': FINISHED: Update Firmware From Network Share Method')
    return msg, err


# Main
def main():
    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC handle
            idrac=dict(required=False, type='dict'),

            # iDRAC Credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_pwd=dict(required=True, type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Network File Share
            share_name=dict(required=True, type='str'),
            share_user=dict(required=True, type='str'),
            share_pwd=dict(required=True, type='str', no_log=True),
            share_mnt=dict(required=True, type='str'),

            # Firmware update parameters
            reboot=dict(required=False, default=False, type='bool'),
            job_wait=dict(required=False, default=True, type='bool')
        ),

        supports_check_mode=True)

    if not HAS_OMSDK:
        module.fail_json(msg="Dell EMC OpenManage Python SDK required for this module")

    logger.info(module.params['idrac_ip'] + ': STARTING: Firmware Update')
    # Connect to iDRAC
    logger.info(module.params['idrac_ip'] + ': CALLING: iDRAC Connection')
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()
    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Connection is successful')

    msg, err = run_update_fw_from_nw_share(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)
    logger.info(module.params['idrac_ip'] + ': FINISHED: Firmware Update')


if __name__ == '__main__':
    main()
