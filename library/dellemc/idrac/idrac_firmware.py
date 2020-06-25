#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1
# Copyright (C) 2018-2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: idrac_firmware
short_description: Firmware update from a repository on a network share (CIFS, NFS, HTTP, HTTPS, FTP).
version_added: "2.8"
description:
    - Update the Firmware by connecting to a network share (CIFS, NFS, HTTP, HTTPS, FTP) that contains a catalog of
        available updates.
    - Network share should contain a valid repository of Update Packages (DUPs) and a catalog file describing the DUPs.
    - All applicable updates contained in the repository are applied to the system.
    - This feature is available only with iDRAC Enterprise License.
options:
    idrac_ip:
        description: iDRAC IP Address.
        type: str
        required: True
    idrac_user:
        description: iDRAC username.
        type: str
        required: True
    idrac_password:
        description: iDRAC user password.
        type: str
        required: True
        aliases: ['idrac_pwd']
    idrac_port:
        description: iDRAC port.
        type: int
        default: 443
    share_name:
        description: Network share path of update repository. CIFS, NFS, HTTP, HTTPS and FTP share types are supported.
        type: str
        required: True
    share_user:
        description: Network share user in the format 'user@domain' or 'domain\\user' if user is
            part of a domain else 'user'. This option is mandatory for CIFS Network Share.
        type: str
    share_password:
        description: Network share user password. This option is mandatory for CIFS Network Share.
        type: str
        aliases: ['share_pwd']
    share_mnt:
        description:
          - Local mount path of the network share with read-write permission for ansible user.
          - This option is not applicable for HTTP, HTTPS, and FTP shares.
        type: str
        required: False
    reboot:
        description:
          - Whether to reboot for applying the updates or not.
          - If I(reboot) is C(False), updates take effect after the system is rebooted. If update packages
            in the repository require a reboot, ensure that I(reboot) is C(False) and I(job_wait) is C(True).
            If not, the module will continue to wait for a system reboot and eventually time out.
        type: bool
        default: False
    job_wait:
        description: Whether to wait for job completion or not.
        type: bool
        default: True
    catalog_file_name:
        required: False
        description: Catalog file name relative to the I(share_name).
        type: str
        default: 'Catalog.xml'
    ignore_cert_warning:
        required: False
        description: Specifies if certificate warnings are ignored when HTTPS share is used.
            If C(True) option is set, then the certificate warnings are ignored.
        type: bool
        default: True
    apply_update:
        required: False
        description: If I(apply_update) is set to C(True), then the packages are applied.
            If it is set to C(False), packages are not applied.
        type: bool
        default: True

requirements:
    - "omsdk"
    - "python >= 2.7.5"
author:
    - "Rajeev Arakkal (@rajeevarakkal)"
    - "Felix Stephen (@felixs88)"
'''

EXAMPLES = """
---
- name: Update firmware from repository on a NFS Share
  idrac_firmware:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       share_name: "192.168.0.0:/share"
       reboot: True
       job_wait: True
       apply_update: True
       catalog_file_name: "Catalog.xml"

- name: Update firmware from repository on a CIFS Share
  idrac_firmware:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       share_name: "full_cifs_path"
       share_user: "share_user"
       share_password: "share_password"
       reboot: True
       job_wait: True
       apply_update: True
       catalog_file_name: "Catalog.xml"

- name: Update firmware from repository on a HTTP
  idrac_firmware:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       share_name: "http://downloads.dell.com"
       reboot: True
       job_wait: True
       apply_update: True

- name: Update firmware from repository on a HTTPS
  idrac_firmware:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       share_name: "https://downloads.dell.com"
       reboot: True
       job_wait: True
       apply_update: True

- name: Update firmware from repository on a FTP
  idrac_firmware:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       share_name: "ftp://ftp.dell.com"
       reboot: True
       job_wait: True
       apply_update: True
"""

RETURN = """
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
        'InstanceID': 'JID_XXXXXXXXXXXX',
        'JobState': 'Completed',
        'Message': 'Job completed successfully.',
        'MessageId': 'REDXXX',
        'Name': 'Repository Update',
        'JobStartTime': 'NA',
        'Status': 'Success',
    }
"""


import os
import re
import json
from xml.etree import ElementTree as ET
from ansible.module_utils.remote_management.dellemc.dellemc_idrac import iDRACConnection
from ansible.module_utils.remote_management.dellemc.idrac_redfish import iDRACRedfishAPI
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.parse import urlparse
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
try:
    from omsdk.sdkcreds import UserCredentials
    from omsdk.sdkfile import FileOnShare
    from omsdk.http.sdkwsmanbase import WsManProtocolBase
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False

SHARE_TYPE = {'nfs': 'NFS', 'cifs': 'CIFS', 'ftp': 'FTP',
              'http': 'HTTP', 'https': 'HTTPS', 'tftp': 'TFTP'}
CERT_WARN = {True: 'On', False: 'Off'}
PATH = "/redfish/v1/Dell/Systems/System.Embedded.1/DellSoftwareInstallationService/Actions/DellSoftwareInstallationService.InstallFromRepository"
GET_REPO_BASED_UPDATE_LIST_PATH = "/redfish/v1/Dell/Systems/System.Embedded.1/DellSoftwareInstallationService/Actions/" \
                                  "DellSoftwareInstallationService.GetRepoBasedUpdateList"


def _validate_catalog_file(catalog_file_name):
    normilized_file_name = catalog_file_name.lower()
    if not normilized_file_name:
        raise ValueError('catalog_file_name should be a non-empty string.')
    elif not normilized_file_name.endswith("xml"):
        raise ValueError('catalog_file_name should be an XML file.')


def _convert_xmltojson(job_details):
    """get all the xml data from PackageList and returns as valid json."""
    data, repo_status = [], False
    try:
        xmldata = ET.fromstring(job_details['PackageList'])
        for iname in xmldata.iter('INSTANCENAME'):
            data.append({attr.attrib['NAME']: txt.text for attr in iname.iter("PROPERTY") for txt in attr})
        repo_status = True
    except ET.ParseError:
        data = job_details['PackageList']
    return data, repo_status


def get_jobid(module, resp):
    """Get the Job ID from the response header."""
    jobid = None
    if resp.code == 202:
        joburi = resp.headers.get('Location')
        if joburi is None:
            module.fail_json(msg="Failed to update firmware.")
        jobid = joburi.split("/")[-1]
    else:
        module.fail_json(msg="Failed to update firmware.")
    return jobid


def update_firmware_url(module, idrac, share_name, catalog_file_name, apply_update, reboot,
                        ignore_cert_warning, job_wait, payload):
    """Update firmware through HTTP/HTTPS/FTP and return the job details."""
    repo_url = urlparse(share_name)
    job_details, status = {}, {}
    ipaddr = repo_url.netloc
    share_type = repo_url.scheme
    sharename = repo_url.path.strip('/')
    message = "Firmware versions on server match catalog, applicable updates are not present in the repository."
    exit_message = "The catalog in the repository specified in the operation has the same firmware versions" \
                   " as currently present on the server."
    if idrac.use_redfish:
        payload['IPAddress'] = ipaddr
        if repo_url.path:
            payload['ShareName'] = sharename
        payload['ShareType'] = SHARE_TYPE[share_type]
        with iDRACRedfishAPI(module.params) as obj:
            resp = obj.invoke_request(PATH, method="POST", data=payload)
            job_id = get_jobid(module, resp)
            status = idrac.job_mgr.get_job_status_redfish(job_id)
            if job_wait:
                status = idrac.job_mgr.job_wait(job_id)
            try:
                resp_repo_based_update_list = obj.invoke_request(GET_REPO_BASED_UPDATE_LIST_PATH, method="POST", data={})
                job_details = eval(resp_repo_based_update_list.read())
            except HTTPError as err:
                err_message = json.load(err)
                if err_message['error']['@Message.ExtendedInfo'][0]['Message'] == message:
                    module.exit_json(msg=exit_message)
                raise err
    elif not idrac.use_redfish and ipaddr == "downloads.dell.com":
        status = idrac.update_mgr.update_from_dell_repo_url(ipaddress=ipaddr, share_type=share_type,
                                                            share_name=sharename, catalog_file=catalog_file_name,
                                                            apply_update=apply_update, reboot_needed=reboot,
                                                            ignore_cert_warning=ignore_cert_warning, job_wait=job_wait)
        if status["job_details"]["Data"]["GetRepoBasedUpdateList_OUTPUT"].get("Message") == message.rstrip("."):
            module.exit_json(msg=exit_message)
    else:
        status = idrac.update_mgr.update_from_repo_url(ipaddress=ipaddr, share_type=share_type,
                                                       share_name=sharename, catalog_file=catalog_file_name,
                                                       apply_update=apply_update, reboot_needed=reboot,
                                                       ignore_cert_warning=ignore_cert_warning, job_wait=job_wait)
        if status["job_details"]["Data"]["GetRepoBasedUpdateList_OUTPUT"].get("Message") == message.rstrip("."):
            module.exit_json(msg=exit_message)
    return status, job_details


def update_firmware(idrac, module):
    """Update firmware from a network share and return the job details."""
    msg = {}
    msg['changed'] = False
    msg['update_msg'] = "Successfully triggered the job to update the firmware."
    try:
        share_name = module.params['share_name']
        catalog_file_name = module.params['catalog_file_name']
        share_user = module.params['share_user']
        share_pwd = module.params['share_password']
        reboot = module.params['reboot']
        job_wait = module.params['job_wait']
        ignore_cert_warning = module.params['ignore_cert_warning']
        apply_update = module.params['apply_update']
        payload = {"RebootNeeded": reboot, "CatalogFile": catalog_file_name, "ApplyUpdate": str(apply_update),
                   "IgnoreCertWarning": CERT_WARN[ignore_cert_warning]}
        if share_user is not None:
            payload['UserName'] = share_user
        if share_pwd is not None:
            payload['Password'] = share_pwd

        firmware_version = re.match(r"^\d.\d{2}", idrac.entityjson['System'][0]['LifecycleControllerVersion']).group()
        idrac.use_redfish = False
        if '14' in idrac.ServerGeneration and float(firmware_version) >= float('3.30'):
            idrac.use_redfish = True
        if share_name.lower().startswith(('http://', 'https://', 'ftp://')):
            msg['update_status'], job_details = update_firmware_url(module, idrac, share_name, catalog_file_name,
                                                                    apply_update, reboot, ignore_cert_warning,
                                                                    job_wait, payload)
            if job_details:
                msg['update_status']['job_details'] = job_details
        else:
            upd_share = FileOnShare(remote="{0}{1}{2}".format(share_name, os.sep, catalog_file_name),
                                    mount_point=module.params['share_mnt'], isFolder=False,
                                    creds=UserCredentials(share_user, share_pwd))
            payload['IPAddress'] = upd_share.remote_ipaddr
            payload['ShareName'] = upd_share.remote.share_name
            payload['ShareType'] = SHARE_TYPE[upd_share.remote_share_type.name.lower()]
            if idrac.use_redfish:
                with iDRACRedfishAPI(module.params) as obj:
                    resp = obj.invoke_request(PATH, method="POST", data=payload)
                    job_id = get_jobid(module, resp)
                    msg['update_status'] = idrac.job_mgr.get_job_status_redfish(job_id)
                    if job_wait:
                        msg['update_status'] = idrac.job_mgr.job_wait(job_id)
                    repo_based_update_list = obj.invoke_request(GET_REPO_BASED_UPDATE_LIST_PATH,
                                                                method="POST", data={})
                    msg['update_status']['job_details'] = eval(repo_based_update_list.read())
            else:
                msg['update_status'] = idrac.update_mgr.update_from_repo(upd_share, apply_update=apply_update,
                                                                         reboot_needed=reboot, job_wait=job_wait)
        json_data, repo_status = msg['update_status']['job_details'], False
        if "PackageList" not in json_data:
            job_data = json_data.get('Data')
            pkglst = job_data['body'] if 'body' in job_data else job_data.get('GetRepoBasedUpdateList_OUTPUT')
            if 'PackageList' in pkglst:
                pkglst['PackageList'], repo_status = _convert_xmltojson(pkglst)
        else:
            json_data['PackageList'], repo_status = _convert_xmltojson(json_data)
    except RuntimeError as e:
        module.fail_json(msg=str(e))
    if "Status" in msg['update_status']:
        if msg['update_status']['Status'] in ["Success", "InProgress"]:
            if module.params['job_wait'] and module.params['apply_update'] and \
                    ('job_details' in msg['update_status'] and repo_status):
                msg['changed'] = True
                msg['update_msg'] = "Successfully updated the firmware."
        else:
            module.fail_json(msg='Failed to update firmware.', update_status=msg['update_status'])
    return msg


def main():
    module = AnsibleModule(
        argument_spec={
            "idrac_ip": {"required": True, "type": 'str'},
            "idrac_user": {"required": True, "type": 'str'},
            "idrac_password": {"required": True, "type": 'str', "aliases": ['idrac_pwd'], "no_log": True},
            "idrac_port": {"required": False, "default": 443, "type": 'int'},

            "share_name": {"required": True, "type": 'str'},
            "share_user": {"required": False, "type": 'str'},
            "share_password": {"required": False, "type": 'str', "aliases": ['share_pwd'], "no_log": True},
            "share_mnt": {"required": False, "type": 'str'},

            "catalog_file_name": {"required": False, "type": 'str', "default": "Catalog.xml"},
            "reboot": {"required": False, "type": 'bool', "default": False},
            "job_wait": {"required": False, "type": 'bool', "default": True},
            "ignore_cert_warning": {"required": False, "type": 'bool', "default": True},
            "apply_update": {"required": False, "type": 'bool', "default": True},
        },

        supports_check_mode=False)

    try:
        # Validate the catalog file
        _validate_catalog_file(module.params['catalog_file_name'])
        # Connect to iDRAC and update firmware
        with iDRACConnection(module.params) as idrac:
            status = update_firmware(idrac, module)
    except HTTPError as err:
        module.fail_json(msg=str(err), update_status=json.load(err))
    except (RuntimeError, URLError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError) as e:
        module.fail_json(msg=str(e))

    module.exit_json(msg=status['update_msg'], update_status=status['update_status'],
                     changed=status['changed'])


if __name__ == '__main__':
    main()
