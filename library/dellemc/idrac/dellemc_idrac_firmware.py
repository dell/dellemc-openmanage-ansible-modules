#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 1.3
# Copyright (C) 2019 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: dellemc_idrac_firmware
short_description: Firmware update from a repository on a remote network share (CIFS, NFS) or a URL (HTTP, HTTPS, FTP)
version_added: "2.8"
description:
  - Update the Firmware by connecting to a network repository (CIFS, NFS, HTTP, HTTPS, FTP) that contains a catalog of available updates.
  - Remote network share or URL should contain a valid repository of Update Packages (DUPs) and a catalog file describing the DUPs.
  - All applicable updates contained in the repository is applied to the system.
  - This feature is only available with iDRAC Enterprise License.
options:
  idrac_ip:
    description:
      - iDRAC IP Address
    required: True
    type: 'str'
  idrac_user:
    description:
      - iDRAC user name
    required: True
    type: 'str'
  idrac_pwd:
    description:
      - iDRAC user password
    required: True
    type: 'str'
  idrac_port:
    description:
      - iDRAC port
    required: False
    default: 443
    type: 'int'
  share_name:
    description:
      - Network share (CIFS, NFS, HTTP, HTTPS, FTP) containing the Catalog file and Update Packages (DUPs)
    required: True
    type: 'str'
  share_user:
    description:
      - Network share user in the format 'user@domain' or 'domain\\user' if
        user is part of a domain else 'user'. This option is mandatory if
        I(share_name) is a CIFS share.
    required: False
    type: 'str'
  share_pwd:
    description:
      - Network share user password
    required: False
    type: 'str'
  share_mnt:
    description:
      - Local mount path on the ansible controller machine for the remote
        network share (CIFS, NFS) provided in I(share_name). This is not
        applicable for HTTP, HTTPS and FTP share.
      - This option is mandatory only when using firmware update from a network
        repository using Server Configuration Profiles (SCP).
      - SCP based firmware update is only supported for 14G PowerEdge servers
        (iDRAC firmware version >=3.00.00.00).
    required: False
    type: 'path'
  catalog_file_name:
    description:
      - Catalog file name relative to the I(share_name)
    required: False
    type: 'str'
    default: 'Catalog.xml'
  apply_update:
    description:
      - if C(True), the updatable packages from Catalog XML are staged
      - if C(False), do not Install Updates
    required: False
    type: 'bool'
    default: True
  reboot:
    description:
      - if C(True), reboot server for applying the updates
      - if C(False), updates take effect after the system is rebooted the next time
    required: False
    type: 'bool'
    default: False
  job_wait:
    description:
      - if C(True), will wait for update JOB to get completed
      - if C(False), return immediately after creating the update job in job queue
    required: False
    type: 'bool'
    default: True
  ignore_cert_warning:
    description:
      - Specifies if certificate warnings should be ignored when HTTPS share is used
      - if C(True), certificate warnings are ignored
      - if C(False), certificate warnings are not ignored
    required: False
    type: 'bool'
    default: True

requirements:
  - "omsdk"
  - "python >= 2.7.5"
author:
  - "Anupam Aloke (@anupamaloke)"
  - "Rajeev Arakkal (@rajeevarakkal)"
'''

EXAMPLES = '''
---
# Update firmware from repository on a CIFS Share. '\\\\192.168.20.10\\share' is
# locally mounted to '/mnt/cifs_share' in a read-write mode on the Ansible
# controller machine. 'share_mnt' is required argument only for 14G servers

- name: Update firmware from repository on a CIFS Share
  dellemc_idrac_firmware:
      idrac_ip: "192.168.10.1"
      idrac_user: "user_name"
      idrac_pwd: "user_pwd"
      share_name: '\\\\192.168.20.10\\share'
      share_user: "share_user_name"
      share_pwd: "share_user_pwd"
      share_mnt: "/mnt/cifs_share"
      catalog_file_name: "Catalog.xml"
      apply_update: True
      reboot: False
      job_wait: True
  delegate_to: localhost

# Update firmware from repository on a NFS Share. '192.168.20.10:/share' is
# locally mounted to '/mnt/nfs_share' in a read-write mode on the Ansible
# controller machine. 'share_mnt' is required argument only for 14G servers

- name: Update firmware from repository on a NFS Share
  dellemc_idrac_firmware:
    idrac_ip: "192.168.10.1"
    idrac_user: "user_name"
    idrac_pwd: "user_pwd"
    share_name: "192.168.20.10:/share"
    share_mnt: "/mnt/nfs_share"
    catalog_file_name: "Catalog.xml"
    apply_update: True
    reboot: False
    job_wait: True
  delegate_to: localhost

# Update firmware from repository on a HTTP Share.
# In this example, http://<ipaddress>/firmware contains the Catalog file and
# the DUPs

- name: Update firmware from repository on a HTTP Share
  dellemc_install_firmware:
    idrac_ip: "192.168.10.1"
    idrac_user: "user_name"
    idrac_pwd: "user_pwd"
    share_name: "http://<ipaddress>/firmware"
    catalog_file_name: "Catalog.xml"
    apply_update: True
    reboot: False
    job_wait: True
  delegate_to: localhost

'''

RETURN = '''
---
msg:
  type: str
  description: Over all firmware update status.
  returned: always
  sample: "Successfully updated the firmware."
update_status:
  type: dict
  description: Firmware Update job and progress details from the iDRAC.
  returned: success
  sample: {
        "ElapsedTimeSinceCompletion": "0",
        "InstanceID": "JID_396919089508",
        "JobStartTime": "NA",
        "JobStatus": "Completed",
        "JobUntilTime": "NA",
        "Message": "Job completed successfully.",
        "MessageArguments": "NA",
        "MessageID": "RED001",
        "Name": "Repository Update",
        "PercentComplete": "100",
        "Status": "Success",
        "file": "http://<ipaddress>/firmware/Catalog.xml",
        "retval": true
    }

'''

import re
from ansible.module_utils.remote_management.dellemc.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.parse import urlparse

try:
    from omsdk.sdkcreds import UserCredentials
    from omsdk.sdkfile import FileOnShare
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False


def update_firmware_from_url(idrac, share_name, share_user, share_pwd,
                             catalog_file_name, apply_update=True,
                             reboot=False, job_wait=True,
                             ignore_cert_warning=True):
    """
    Update firmware from a ftp/http/https URL

    :param share_name: ftp/http/https url for downloading the catalog file and DUPs
    :type share_name: ``str``

    :param share_user: user name for the URL
    :type share_user: ``str``

    :param share_pwd: password for the URL
    :type share_pwd: ``str``

    :param catalog_file_name: Name of the Catalog file on the repository
    :type catalog_file_name: ``str``

    :param apply_update: If apply_update is set to True, the updatable packages from Catalog XML are staged. If it is set to False, no updates are applied.
    :type apply_update: ``bool``

    :param reboot: True if the server needs to be rebooted during the update
    process. False if the updates take effect after the server is rebooted the
    next time.
    :type reboot: ``bool``

    :param job_wait: True if need to wait for firmware job to be completed. False if need to return immediately after staging the job in LC queue
    :type job_wait: ``bool``

    :returns: A dict containing the return value from the Update Job
    :rtype: ``dict``
    """

    # IPv4 address with an optional port number, for e.g. 192.168.10.20:80
    ipv4_re = re.compile(r'(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}(?=$|(?::(\d{2,5})))')

    # URL scheme
    schemes = ["ftp", "http", "https"]

    # Validate URL
    p = urlparse(share_name)
    if not p:
        result = "Invalid url: {0}".format(share_name)
    else:
        path = p.path
        if p.scheme not in schemes:
            error_str = "URL scheme must be one of " + str(schemes)
            result = "Invalid url: {0}. {1}".format(share_name, error_str)
        elif not (p.netloc and re.match(ipv4_re, p.netloc)):
            error_str = "URL netloc must be a valid IPv4 address."
            result = "Invalid url: {0}. {1}".format(share_name, error_str)
        else:
            if not p.path:
                # if path is empty (for e.g. in "http://192.168.10.10"), then
                # use "/" as path
                path += "/"

            result = idrac.update_mgr.update_from_repo_url(
                ipaddress=p.netloc, share_type=p.scheme, share_name=path,
                share_user=share_user, share_pwd=share_pwd,
                catalog_file=catalog_file_name, apply_update=apply_update,
                reboot_needed=reboot, ignore_cert_warning=ignore_cert_warning,
                job_wait=job_wait)

    return result


def update_firmware_from_net_share(idrac, share_name, share_user, share_pwd,
                                   share_mnt, catalog_file_name,
                                   apply_update=True, reboot=False,
                                   job_wait=True):
    """
    Update firmware from a repository on a remote network share (CIFS, NFS)

    :param idrac: iDRAC connection object
    :type idrac: iDRAC connection object

    :param share_name: CIFS or NFS network share
    :type share_name: ``str``

    :param share_user: username for the remote network share
    :type share_user: ``str``

    :param share_pwd: password for the remote network share
    :type share_pwd: ``str``

    :param share_mnt: local mount point for the remote network share
    :type share_mnt: ``str``

    :param catalog_file_name: Name of Catalog file on the repository
    :type catalog_file_name: ``str``

    :param apply_update: Apply update
    :type apply_update: ``bool``

    :param reboot: Reboot system
    :type reboot: ``bool``

    :param job_wait: Wait for JOB to be completed
    :type job_wait: ``bool``

    :returns: A dict containing the return value for the Update Job
    :rtype: ``dict``
    """

    net_share_repo = FileOnShare(remote=share_name,
                                 mount_point=share_mnt,
                                 creds=UserCredentials(share_user, share_pwd),
                                 isFolder=True)
    catalog_path = net_share_repo.new_file(catalog_file_name)

    result = idrac.update_mgr.update_from_repo(catalog_path=catalog_path,
                                               apply_update=apply_update,
                                               reboot_needed=reboot,
                                               job_wait=job_wait)

    return result


def update_firmware(idrac, module):
    """
    Update firmware from a repository (CIFS, NFS, HTTP, HTTPS, FTP)

    :param idrac: iDRAC handle
    :type idrac: ``iDRAC Connection Object``

    :param module: Ansible module
    :type module: ``class AnsibleModule``

    :returns: A tuple containing a result dict and error flag
    :rtype: ``tuple``
    """

    result = {}
    result['changed'] = False
    result['update_status'] = {}
    err = False

    try:
        share_name = module.params['share_name']
        share_user = module.params.get('share_user')
        share_pwd = module.params.get('share_pwd')
        share_mnt = module.params.get('share_mnt')
        catalog_file_name = module.params['catalog_file_name']
        apply_update = module.params['apply_update']
        reboot = module.params['reboot']
        job_wait = module.params['job_wait']
        ignore_cert_warning = module.params['ignore_cert_warning']

        # check if valid catalog file
        if not catalog_file_name.lower().endswith('.xml'):
            module.fail_json(msg="Invalid catalog file: {0}. Must end with \'.xml\' or \'.XML\' extension".format(catalog_file_name))

        # Temporary Fix for 12G and 13G iDRAC - Use WS-Man API for Firmware
        # update from a network repository
        idrac.use_redfish = True
        if any(gen in idrac.ServerGeneration for gen in ['12', '13']):
            idrac.use_redfish = False

        # check if HTTP/HTTPS share
        if share_name.lower().startswith(('http://', 'https://', 'ftp://')):
            # Update from http/https/ftp repo is currently supported using
            # only WS-Man
            idrac.use_redfish = False
            result['update_status'] = update_firmware_from_url(idrac,
                                                               share_name,
                                                               share_user,
                                                               share_pwd,
                                                               catalog_file_name,
                                                               apply_update,
                                                               reboot, job_wait,
                                                               ignore_cert_warning)
        else:
            # local mount point is required for SCP based firmware update
            if idrac.use_redfish and not share_mnt:
                module.fail_json(msg="Error: \'share_mnt\' is a mandatory argument for firmware update using Server Configuration Profile")

            result['update_status'] = update_firmware_from_net_share(idrac,
                                                                     share_name,
                                                                     share_user,
                                                                     share_pwd,
                                                                     share_mnt,
                                                                     catalog_file_name,
                                                                     apply_update,
                                                                     reboot,
                                                                     job_wait)

    except RuntimeError as e:
        module.fail_json(msg=str(e))

    if "Status" in result['update_status']:
        if result['update_status']['Status'] == "Success":
            result['msg'] = 'Successfully created the repository update job.'
            if module.params['job_wait']:
                remote['msg'] = 'Succesfully completed the repository update job.'
                result['changed'] = True
        else:
            result['msg'] = 'Failed to update firmware.'
            module.fail_json(**result)
    else:
        result['msg'] = 'Failed to update firmware.'
        module.fail_json(**result)

    return result


def main():

    module = AnsibleModule(
        argument_spec={
            # iDRAC Credentials
            "idrac_ip": {"required": True, "type": 'str'},
            "idrac_user": {"required": True, "type": 'str'},
            "idrac_pwd": {"required": True, "type": 'str', "no_log": True},
            "idrac_port": {"required": False, "default": 443, "type": 'int'},

            # Network File Share
            "share_name": {"required": True, "type": 'str'},
            "share_user": {"required": False, "type": 'str', "default": None},
            "share_pwd": {"required": False, "type": 'str', "default": None, "no_log": True},
            "share_mnt": {"required": False, "type": 'path', "default": None},

            # Firmware update parameters
            "catalog_file_name": {"required": False, "default": 'Catalog.xml', "type": 'str'},
            "apply_update": {"required": False, "default": True, "type": 'bool'},
            "reboot": {"required": False, "default": False, "type": 'bool'},
            "job_wait": {"required": False, "default": True, "type": 'bool'},
            "ignore_cert_warning": {"required": False, "default": True, "type": 'bool'}
        },

        supports_check_mode=False)

    try:
        # Connect to iDRAC and update firmware
        with iDRACConnection(module.params) as idrac:
            result = update_firmware(idrac, module)

    except (ImportError, ValueError, RuntimeError) as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
