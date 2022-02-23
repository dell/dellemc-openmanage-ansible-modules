#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.1.0
# Copyright (C) 2018-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: idrac_firmware
short_description: Firmware update from a repository on a network share (CIFS, NFS, HTTP, HTTPS, FTP)
version_added: "2.1.0"
description:
    - Update the Firmware by connecting to a network share (CIFS, NFS, HTTP, HTTPS, FTP) that contains a catalog of
        available updates.
    - Network share should contain a valid repository of Update Packages (DUPs) and a catalog file describing the DUPs.
    - All applicable updates contained in the repository are applied to the system.
    - This feature is available only with iDRAC Enterprise License.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
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
    job_wait:
        description: Whether to wait for job completion or not.
        type: bool
        default: True
    catalog_file_name:
        description: Catalog file name relative to the I(share_name).
        type: str
        default: 'Catalog.xml'
    ignore_cert_warning:
        description: Specifies if certificate warnings are ignored when HTTPS share is used.
            If C(True) option is set, then the certificate warnings are ignored.
        type: bool
        default: True
    apply_update:
        description:
          - If I(apply_update) is set to C(True), then the packages are applied.
          - If I(apply_update) is set to C(False), no updates are applied, and a catalog report
            of packages is generated and returned.
        type: bool
        default: True
    reboot:
        description:
          - Provides the option to apply the update packages immediately or in the next reboot.
          - If I(reboot) is set to C(True),  then the packages  are applied immediately.
          - If I(reboot) is set to C(False), then the packages are staged and applied in the next reboot.
          - Packages that do not require a reboot are applied immediately irrespective of I (reboot).
        type: bool
        default: False

requirements:
    - "omsdk >= 1.2.488"
    - "python >= 3.8.6"
author:
    - "Rajeev Arakkal (@rajeevarakkal)"
    - "Felix Stephen (@felixs88)"
notes:
    - Run this module from a system that has direct access to DellEMC iDRAC.
    - Module will report success based on the iDRAC firmware update parent job status if there are no individual
        component jobs present.
    - For server with iDRAC firmware 5.00.00.00 and later, if the repository contains unsupported packages, then the
        module will return success with a proper message.
    - This module supports C(check_mode).
'''

EXAMPLES = """
---
- name: Update firmware from repository on a NFS Share
  dellemc.openmanage.idrac_firmware:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       ca_path: "/path/to/ca_cert.pem"
       share_name: "192.168.0.0:/share"
       reboot: True
       job_wait: True
       apply_update: True
       catalog_file_name: "Catalog.xml"

- name: Update firmware from repository on a CIFS Share
  dellemc.openmanage.idrac_firmware:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       ca_path: "/path/to/ca_cert.pem"
       share_name: "full_cifs_path"
       share_user: "share_user"
       share_password: "share_password"
       reboot: True
       job_wait: True
       apply_update: True
       catalog_file_name: "Catalog.xml"

- name: Update firmware from repository on a HTTP
  dellemc.openmanage.idrac_firmware:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       ca_path: "/path/to/ca_cert.pem"
       share_name: "http://downloads.dell.com"
       reboot: True
       job_wait: True
       apply_update: True

- name: Update firmware from repository on a HTTPS
  dellemc.openmanage.idrac_firmware:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       ca_path: "/path/to/ca_cert.pem"
       share_name: "https://downloads.dell.com"
       reboot: True
       job_wait: True
       apply_update: True

- name: Update firmware from repository on a FTP
  dellemc.openmanage.idrac_firmware:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       ca_path: "/path/to/ca_cert.pem"
       share_name: "ftp://ftp.dell.com"
       reboot: True
       job_wait: True
       apply_update: True
"""

RETURN = """
---
msg:
  type: str
  description: Overall firmware update status.
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
import json
import time
from ssl import SSLError
from xml.etree import ElementTree as ET
from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection, idrac_auth_params
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI
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
IDRAC_PATH = "/redfish/v1/Dell/Systems/System.Embedded.1/DellSoftwareInstallationService"
PATH = "/redfish/v1/Dell/Systems/System.Embedded.1/DellSoftwareInstallationService/Actions/" \
       "DellSoftwareInstallationService.InstallFromRepository"
GET_REPO_BASED_UPDATE_LIST_PATH = "/redfish/v1/Dell/Systems/System.Embedded.1/DellSoftwareInstallationService/" \
                                  "Actions/DellSoftwareInstallationService.GetRepoBasedUpdateList"
JOB_URI = "/redfish/v1/JobService/Jobs/{job_id}"
iDRAC_JOB_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/{job_id}"
MESSAGE = "Firmware versions on server match catalog, applicable updates are not present in the repository."
EXIT_MESSAGE = "The catalog in the repository specified in the operation has the same firmware versions " \
               "as currently present on the server."
IDEM_MSG_ID = "SUP029"
REDFISH_VERSION = "3.30"
INTERVAL = 30  # polling interval
WAIT_COUNT = 240
JOB_WAIT_MSG = 'Job wait timed out after {0} minutes'


def wait_for_job_completion(module, job_uri, job_wait=False, reboot=False, apply_update=False):
    track_counter = 0
    response = {}
    msg = None
    while track_counter < 5:
        try:
            # For job_wait False return a valid response, try 5 times
            with iDRACRedfishAPI(module.params) as redfish:
                response = redfish.invoke_request(job_uri, "GET")
            track_counter += 5
            msg = None
        except Exception as error_message:
            msg = str(error_message)
            track_counter += 1
            time.sleep(10)
    if track_counter < 5:
        msg = None
    #  reset track counter
    track_counter = 0
    while job_wait and track_counter <= WAIT_COUNT:
        try:
            with iDRACRedfishAPI(module.params) as redfish:
                response = redfish.invoke_request(job_uri, "GET")
                job_state = response.json_data.get("JobState")
            msg = None
        except Exception as error_message:
            msg = str(error_message)
            track_counter += 2
            time.sleep(INTERVAL)
        else:
            if response.json_data.get("PercentComplete") == 100 and job_state == "Completed":  # apply now
                break
            if job_state in ["Starting", "Running", "Pending", "New"] and not reboot and apply_update:  # apply on
                break
            track_counter += 1
            time.sleep(INTERVAL)
    if track_counter > WAIT_COUNT:
        # TIMED OUT
        msg = JOB_WAIT_MSG.format((WAIT_COUNT * INTERVAL) / 60)
    return response, msg


def _validate_catalog_file(catalog_file_name):
    normilized_file_name = catalog_file_name.lower()
    if not normilized_file_name:
        raise ValueError('catalog_file_name should be a non-empty string.')
    elif not normilized_file_name.endswith("xml"):
        raise ValueError('catalog_file_name should be an XML file.')


def get_check_mode_status(status, module):
    if status['job_details']["Data"]["GetRepoBasedUpdateList_OUTPUT"].get("Message") == MESSAGE.rstrip(".") and \
            status.get('JobStatus') == "Completed":
        if module.check_mode:
            module.exit_json(msg="No changes found to commit!")
        module.exit_json(msg=EXIT_MESSAGE)


def get_job_status(module, each_comp, idrac):
    failed, each_comp['JobStatus'], each_comp['Message'] = False, None, None
    job_wait = module.params['job_wait']
    reboot = module.params['reboot']
    apply_update = module.params['apply_update']
    if each_comp.get("JobID") is not None:
        if idrac:
            resp = idrac.job_mgr.job_wait(each_comp.get("JobID"))
            while reboot and apply_update:
                resp = idrac.job_mgr.job_wait(each_comp.get("JobID"))
                if resp.get("JobStatus") is not None and (not resp.get('JobStatus') == "Scheduled"):
                    break
            each_comp['Message'] = resp.get('Message')
            each_comp['JobStatus'] = "OK"
            fail_words_lower = ['fail', 'invalid', 'unable', 'not', 'cancel']
            if any(x in resp.get('Message').lower() for x in fail_words_lower):
                each_comp['JobStatus'] = "Critical"
                failed = True
        else:
            resp, msg = wait_for_job_completion(module, JOB_URI.format(job_id=each_comp.get("JobID")), job_wait, reboot,
                                                apply_update)
            if not msg:
                resp_data = resp.json_data
                if resp_data.get('Messages'):
                    each_comp['Message'] = resp_data.get('Messages')[0]['Message']
                each_comp['JobStatus'] = resp_data.get('JobStatus')
                if each_comp['JobStatus'] == "Critical":
                    failed = True
            else:
                failed = True
    return each_comp, failed


def _convert_xmltojson(module, job_details, idrac):
    """get all the xml data from PackageList and returns as valid json."""
    data, repo_status, failed_status = [], False, False
    try:
        xmldata = ET.fromstring(job_details['PackageList'])
        for iname in xmldata.iter('INSTANCENAME'):
            comp_data = dict([(attr.attrib['NAME'], txt.text) for attr in iname.iter("PROPERTY") for txt in attr])
            component, failed = get_job_status(module, comp_data, idrac)
            # get the any single component update failure and record the only very first failure on failed_status True
            if not failed_status and failed:
                failed_status = True
            data.append(component)
        repo_status = True
    except ET.ParseError:
        data = job_details['PackageList']
    return data, repo_status, failed_status


def get_jobid(module, resp):
    """Get the Job ID from the response header."""
    jobid = None
    if resp.status_code == 202:
        joburi = resp.headers.get('Location')
        if joburi is None:
            module.fail_json(msg="Failed to update firmware.")
        jobid = joburi.split("/")[-1]
    else:
        module.fail_json(msg="Failed to update firmware.")
    return jobid


def handle_HTTP_error(module, httperr):
    err_message = json.load(httperr)
    err_list = err_message.get('error', {}).get('@Message.ExtendedInfo', [{"Message": EXIT_MESSAGE}])
    if err_list:
        err_reason = err_list[0].get("Message", EXIT_MESSAGE)
        if IDEM_MSG_ID in err_list[0].get('MessageId'):
            module.exit_json(msg=err_reason)
    if "error" in err_message:
        module.fail_json(msg=err_message)


def update_firmware_url_redfish(module, idrac, share_name, apply_update, reboot, job_wait, payload, repo_urls):
    """Update firmware through HTTP/HTTPS/FTP and return the job details."""
    repo_url = urlparse(share_name)
    job_details, status = {}, {}
    ipaddr = repo_url.netloc
    share_type = repo_url.scheme
    sharename = repo_url.path.strip('/')
    payload['IPAddress'] = ipaddr
    if repo_url.path:
        payload['ShareName'] = sharename
    payload['ShareType'] = SHARE_TYPE[share_type]
    install_url = PATH
    get_repo_url = GET_REPO_BASED_UPDATE_LIST_PATH
    actions = repo_urls.get('Actions')
    if actions:
        install_url = actions.get("#DellSoftwareInstallationService.InstallFromRepository", {}).get("target", PATH)
        get_repo_url = actions.get("#DellSoftwareInstallationService.GetRepoBasedUpdateList", {}).\
            get("target", GET_REPO_BASED_UPDATE_LIST_PATH)
    resp = idrac.invoke_request(install_url, method="POST", data=payload)
    job_id = get_jobid(module, resp)
    resp, msg = wait_for_job_completion(module, JOB_URI.format(job_id=job_id), job_wait, reboot, apply_update)
    if not msg:
        status = resp.json_data
    else:
        status['update_msg'] = msg
    try:
        resp_repo_based_update_list = idrac.invoke_request(get_repo_url, method="POST", data="{}",
                                                           dump=False)
        job_details = resp_repo_based_update_list.json_data
    except HTTPError as err:
        handle_HTTP_error(module, err)
        raise err
    return status, job_details


def update_firmware_url_omsdk(module, idrac, share_name, catalog_file_name, apply_update, reboot,
                              ignore_cert_warning, job_wait, payload):
    """Update firmware through HTTP/HTTPS/FTP and return the job details."""
    repo_url = urlparse(share_name)
    job_details, status = {}, {}
    ipaddr = repo_url.netloc
    share_type = repo_url.scheme
    sharename = repo_url.path.strip('/')
    if ipaddr == "downloads.dell.com":
        status = idrac.update_mgr.update_from_dell_repo_url(ipaddress=ipaddr, share_type=share_type,
                                                            share_name=sharename, catalog_file=catalog_file_name,
                                                            apply_update=apply_update, reboot_needed=reboot,
                                                            ignore_cert_warning=ignore_cert_warning, job_wait=job_wait)
        get_check_mode_status(status, module)
    else:
        status = idrac.update_mgr.update_from_repo_url(ipaddress=ipaddr, share_type=share_type,
                                                       share_name=sharename, catalog_file=catalog_file_name,
                                                       apply_update=apply_update, reboot_needed=reboot,
                                                       ignore_cert_warning=ignore_cert_warning, job_wait=job_wait)
        get_check_mode_status(status, module)
    return status, job_details


def update_firmware_omsdk(idrac, module):
    """Update firmware from a network share and return the job details."""
    msg = {}
    msg['changed'], msg['failed'], msg['update_status'] = False, False, {}
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

        if share_name.lower().startswith(('http://', 'https://', 'ftp://')):
            msg['update_status'], job_details = update_firmware_url_omsdk(module, idrac, share_name, catalog_file_name,
                                                                          apply_update, reboot, ignore_cert_warning,
                                                                          job_wait, payload)
            if job_details:
                msg['update_status']['job_details'] = job_details
        else:
            upd_share = FileOnShare(remote="{0}{1}{2}".format(share_name, os.sep, catalog_file_name),
                                    mount_point=module.params['share_mnt'], isFolder=False,
                                    creds=UserCredentials(share_user, share_pwd))
            msg['update_status'] = idrac.update_mgr.update_from_repo(upd_share, apply_update=apply_update,
                                                                     reboot_needed=reboot, job_wait=job_wait)
            get_check_mode_status(msg['update_status'], module)

        json_data, repo_status, failed = msg['update_status']['job_details'], False, False
        if "PackageList" not in json_data:
            job_data = json_data.get('Data')
            pkglst = job_data['body'] if 'body' in job_data else job_data.get('GetRepoBasedUpdateList_OUTPUT')
            if 'PackageList' in pkglst:  # Returns from OMSDK
                pkglst['PackageList'], repo_status, failed = _convert_xmltojson(module, pkglst, idrac)
        else:  # Redfish
            json_data['PackageList'], repo_status, failed = _convert_xmltojson(module, json_data, None)

        if not apply_update and not failed:
            msg['update_msg'] = "Successfully fetched the applicable firmware update package list."
        elif apply_update and not reboot and not job_wait and not failed:
            msg['update_msg'] = "Successfully triggered the job to stage the firmware."
        elif apply_update and job_wait and not reboot and not failed:
            msg['update_msg'] = "Successfully staged the applicable firmware update packages."
            msg['changed'] = True
        elif apply_update and job_wait and not reboot and failed:
            msg['update_msg'] = "Successfully staged the applicable firmware update packages with error(s)."
            msg['failed'] = True

    except RuntimeError as e:
        module.fail_json(msg=str(e))

    if module.check_mode and not (json_data.get('PackageList') or json_data.get('Data')) and \
            msg['update_status']['JobStatus'] == 'Completed':
        module.exit_json(msg="No changes found to commit!")
    elif module.check_mode and (json_data.get('PackageList') or json_data.get('Data')) and \
            msg['update_status']['JobStatus'] == 'Completed':
        module.exit_json(msg="Changes found to commit!", changed=True,
                         update_status=msg['update_status'])
    elif module.check_mode and not msg['update_status']['JobStatus'] == 'Completed':
        msg['update_status'].pop('job_details')
        module.fail_json(msg="Unable to complete the firmware repository download.",
                         update_status=msg['update_status'])
    elif not module.check_mode and "Status" in msg['update_status']:
        if msg['update_status']['Status'] in ["Success", "InProgress"]:
            if module.params['job_wait'] and module.params['apply_update'] and module.params['reboot'] and (
                    'job_details' in msg['update_status'] and repo_status) and not failed:
                msg['changed'] = True
                msg['update_msg'] = "Successfully updated the firmware."
            elif module.params['job_wait'] and module.params['apply_update'] and module.params['reboot'] and (
                    'job_details' in msg['update_status'] and repo_status) and failed:
                msg['failed'], msg['changed'] = True, False
                msg['update_msg'] = "Firmware update failed."
        else:
            failed_msg = "Firmware update failed."
            if not apply_update:
                failed_msg = "Unable to complete the repository update."
            module.fail_json(msg=failed_msg, update_status=msg['update_status'])
    return msg


def update_firmware_redfish(idrac, module, repo_urls):
    """Update firmware from a network share and return the job details."""
    msg = {}
    msg['changed'], msg['failed'] = False, False
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

        if share_name.lower().startswith(('http://', 'https://', 'ftp://')):
            msg['update_status'], job_details = update_firmware_url_redfish(
                module, idrac, share_name, apply_update, reboot, job_wait, payload, repo_urls)
            if job_details:
                msg['update_status']['job_details'] = job_details
        else:
            if share_name.startswith('\\\\'):
                cifs = share_name.split('\\')
                payload['IPAddress'] = cifs[2]
                payload['ShareName'] = '\\'.join(cifs[3:])
                payload['ShareType'] = 'CIFS'
            else:
                nfs = urlparse(share_name)
                payload['IPAddress'] = nfs.scheme
                payload['ShareName'] = nfs.path.strip('/')
                payload['ShareType'] = 'NFS'
            resp = idrac.invoke_request(PATH, method="POST", data=payload)
            job_id = get_jobid(module, resp)
            resp, mesg = wait_for_job_completion(module, JOB_URI.format(job_id=job_id), job_wait, reboot, apply_update)
            if not mesg:
                msg['update_status'] = resp.json_data
            else:
                msg['update_status'] = mesg
            try:
                repo_based_update_list = idrac.invoke_request(GET_REPO_BASED_UPDATE_LIST_PATH, method="POST",
                                                              data="{}", dump=False)
                msg['update_status']['job_details'] = repo_based_update_list.json_data
            except HTTPError as err:
                handle_HTTP_error(module, err)
                raise err
        json_data, repo_status, failed = msg['update_status']['job_details'], False, False
        if "PackageList" not in json_data:
            job_data = json_data.get('Data')
            pkglst = job_data['body'] if 'body' in job_data else job_data.get('GetRepoBasedUpdateList_OUTPUT')
            if 'PackageList' in pkglst:
                pkglst['PackageList'], repo_status, failed = _convert_xmltojson(module, pkglst, idrac)
        else:
            json_data['PackageList'], repo_status, failed = _convert_xmltojson(module, json_data, None)

        if not apply_update and not failed:
            msg['update_msg'] = "Successfully fetched the applicable firmware update package list."
        elif apply_update and not reboot and not job_wait and not failed:
            msg['update_msg'] = "Successfully triggered the job to stage the firmware."
        elif apply_update and job_wait and not reboot and not failed:
            msg['update_msg'] = "Successfully staged the applicable firmware update packages."
            msg['changed'] = True
        elif apply_update and job_wait and not reboot and failed:
            msg['update_msg'] = "Successfully staged the applicable firmware update packages with error(s)."
            msg['failed'] = True

    except RuntimeError as e:
        module.fail_json(msg=str(e))

    if module.check_mode and not (json_data.get('PackageList') or json_data.get('Data')) and \
            msg['update_status']['JobStatus'] == 'OK':
        module.exit_json(msg="No changes found to commit!")
    elif module.check_mode and (json_data.get('PackageList') or json_data.get('Data')) and \
            msg['update_status']['JobStatus'] == 'OK':
        module.exit_json(msg="Changes found to commit!", changed=True,
                         update_status=msg['update_status'])
    elif module.check_mode and not msg['update_status']['JobStatus'] == 'OK':
        msg['update_status'].pop('job_details')
        module.fail_json(msg="Unable to complete the firmware repository download.",
                         update_status=msg['update_status'])
    elif not module.check_mode and "JobStatus" in msg['update_status']:
        if not msg['update_status']['JobStatus'] == "Critical":
            if module.params['job_wait'] and module.params['apply_update'] and module.params['reboot'] and \
                    ('job_details' in msg['update_status'] and repo_status) and not failed:
                msg['changed'] = True
                msg['update_msg'] = "Successfully updated the firmware."
            elif module.params['job_wait'] and module.params['apply_update'] and module.params['reboot'] and \
                    ('job_details' in msg['update_status'] and repo_status) and failed:
                msg['failed'], msg['changed'] = True, False
                msg['update_msg'] = "Firmware update failed."
        else:
            failed_msg = "Firmware update failed."
            if not apply_update:
                failed_msg = "Unable to complete the repository update."
            module.fail_json(msg=failed_msg, update_status=msg['update_status'])
    return msg


def main():
    specs = {
        "share_name": {"required": True, "type": 'str'},
        "share_user": {"required": False, "type": 'str'},
        "share_password": {"required": False, "type": 'str', "aliases": ['share_pwd'], "no_log": True},
        "share_mnt": {"required": False, "type": 'str'},

        "catalog_file_name": {"required": False, "type": 'str', "default": "Catalog.xml"},
        "reboot": {"required": False, "type": 'bool', "default": False},
        "job_wait": {"required": False, "type": 'bool', "default": True},
        "ignore_cert_warning": {"required": False, "type": 'bool', "default": True},
        "apply_update": {"required": False, "type": 'bool', "default": True},
    }
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        supports_check_mode=True)

    redfish_check = False
    try:
        with iDRACRedfishAPI(module.params) as obj:
            resp = obj.invoke_request(IDRAC_PATH, method="GET")
            software_service_data = resp.json_data
            redfish_check = True
    except Exception:
        software_service_data = {}
        redfish_check = False

    try:
        # Validate the catalog file
        _validate_catalog_file(module.params['catalog_file_name'])
        if module.check_mode:
            module.params['apply_update'] = False
            module.params['reboot'] = False
            module.params['job_wait'] = True
        # Connect to iDRAC and update firmware
        if redfish_check:
            with iDRACRedfishAPI(module.params) as redfish_obj:
                status = update_firmware_redfish(redfish_obj, module, software_service_data)
        else:
            with iDRACConnection(module.params) as idrac:
                status = update_firmware_omsdk(idrac, module)
    except HTTPError as err:
        module.fail_json(msg=str(err), update_status=json.load(err))
    except (RuntimeError, URLError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError, SSLError) as e:
        module.fail_json(msg=str(e))
    except Exception as exc:
        module.fail_json(msg="Unhandled Exception {0}".format(exc))

    module.exit_json(msg=status['update_msg'], update_status=status['update_status'],
                     changed=status['changed'], failed=status['failed'])


if __name__ == '__main__':
    main()
