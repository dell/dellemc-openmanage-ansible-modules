#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.4.0
# Copyright (C) 2018-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

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
        required: true
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
        default: true
    catalog_file_name:
        description: Catalog file name relative to the I(share_name).
        type: str
        default: 'Catalog.xml'
    ignore_cert_warning:
        description: Specifies if certificate warnings are ignored when HTTPS share is used.
            If C(true) option is set, then the certificate warnings are ignored.
        type: bool
        default: true
    apply_update:
        description:
          - If I(apply_update) is set to C(true), then the packages are applied.
          - If I(apply_update) is set to C(false), no updates are applied, and a catalog report
            of packages is generated and returned.
        type: bool
        default: true
    reboot:
        description:
          - Provides the option to apply the update packages immediately or in the next reboot.
          - If I(reboot) is set to C(true),  then the packages  are applied immediately.
          - If I(reboot) is set to C(false), then the packages are staged and applied in the next reboot.
          - Packages that do not require a reboot are applied immediately irrespective of I (reboot).
        type: bool
        default: false
    proxy_support:
        description:
          - Specifies if a proxy should be used.
          - Proxy parameters are applicable on C(HTTP), C(HTTPS), and C(FTP) share type of repositories.
          - C(ParametersProxy), sets the proxy parameters for the current firmware operation.
          - C(DefaultProxy), iDRAC uses the proxy values set by default.
          - Default Proxy can be set in the Lifecycle Controller attributes using M(dellemc.openmanage.idrac_attributes).
          - C(Off), will not use the proxy.
          - For iDRAC8 based servers, use proxy server with basic authentication.
          - "For iDRAC9 based servers, ensure that you use digest authentication for the proxy server,
          basic authentication is not supported."
        choices: ["ParametersProxy", "DefaultProxy", "Off"]
        type: str
        default: "Off"
    proxy_server:
        description:
          - The IP address of the proxy server.
          - "This IP will not be validated. The download job will be created even for invalid I(proxy_server).
          Please check the results of the job for error details."
          - This is required when I(proxy_support) is C(ParametersProxy).
        type: str
    proxy_port:
        description:
          - The Port for the proxy server.
          - This is required when I(proxy_support) is C(ParametersProxy).
        type: int
    proxy_type:
        description:
          - The proxy type of the proxy server.
          - This is required when I(proxy_support) is C(ParametersProxy).
          - "Note: SOCKS4 proxy does not support IPv6 address."
        choices: [HTTP, SOCKS]
        type: str
    proxy_uname:
        description: The user name for the proxy server.
        type: str
    proxy_passwd:
        description: The password for the proxy server.
        type: str

requirements:
    - "omsdk >= 1.2.503"
    - "python >= 3.9.6"
author:
    - "Rajeev Arakkal (@rajeevarakkal)"
    - "Felix Stephen (@felixs88)"
    - "Jagadeesh N V (@jagadeeshnv)"
    - "Sakshi Makkar (@Sakshi-dell)"
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - Module will report success based on the iDRAC firmware update parent job status if there are no individual
        component jobs present.
    - For server with iDRAC firmware 5.00.00.00 and later, if the repository contains unsupported packages, then the
        module will return success with a proper message.
    - This module supports both IPv4 and IPv6 address for I(idrac_ip) and I(share_name).
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
       reboot: true
       job_wait: true
       apply_update: true
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
       reboot: true
       job_wait: true
       apply_update: true
       catalog_file_name: "Catalog.xml"

- name: Update firmware from repository on a HTTP
  dellemc.openmanage.idrac_firmware:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       ca_path: "/path/to/ca_cert.pem"
       share_name: "http://downloads.dell.com"
       reboot: true
       job_wait: true
       apply_update: true

- name: Update firmware from repository on a HTTPS
  dellemc.openmanage.idrac_firmware:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       ca_path: "/path/to/ca_cert.pem"
       share_name: "https://downloads.dell.com"
       reboot: true
       job_wait: true
       apply_update: true

- name: Update firmware from repository on a HTTPS via proxy
  dellemc.openmanage.idrac_firmware:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       ca_path: "/path/to/ca_cert.pem"
       share_name: "https://downloads.dell.com"
       reboot: true
       job_wait: true
       apply_update: true
       proxy_support: ParametersProxy
       proxy_server: 192.168.1.10
       proxy_type: HTTP
       proxy_port: 80
       proxy_uname: "proxy_user"
       proxy_passwd: "proxy_pwd"

- name: Update firmware from repository on a FTP
  dellemc.openmanage.idrac_firmware:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       ca_path: "/path/to/ca_cert.pem"
       share_name: "ftp://ftp.mydomain.com"
       reboot: true
       job_wait: true
       apply_update: true
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
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
try:
    from omsdk.sdkcreds import UserCredentials
    from omsdk.sdkfile import FileOnShare
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False

SHARE_TYPE = {'nfs': 'NFS', 'cifs': 'CIFS', 'ftp': 'FTP',
              'http': 'HTTP', 'https': 'HTTPS', 'tftp': 'TFTP'}
CERT_WARN = {True: 'On', False: 'Off'}
PROXY_SUPPORT = {"DefaultProxy": "Use_Default_Settings", "Off": "Off", "ParametersProxy": "Use_Custom_Settings"}
IDRAC_PATH = "/redfish/v1/Systems/System.Embedded.1/Oem/Dell/DellSoftwareInstallationService"
PATH = "/redfish/v1/Systems/System.Embedded.1/Oem/Dell/DellSoftwareInstallationService/Actions/" \
       "DellSoftwareInstallationService.InstallFromRepository"
GET_REPO_BASED_UPDATE_LIST_PATH = "/redfish/v1/Systems/System.Embedded.1/Oem/Dell/DellSoftwareInstallationService/" \
                                  "Actions/DellSoftwareInstallationService.GetRepoBasedUpdateList"
JOB_URI = "/redfish/v1/JobService/Jobs/{job_id}"
iDRAC_JOB_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs/{job_id}"
LOG_SERVICE_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Lclog"
iDRAC9_LC_LOG = "/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Lclog/Entries"
iDRAC8_LC_LOG = "/redfish/v1/Managers/iDRAC.Embedded.1/Logs/Lclog"
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
                job_status = response.json_data.get("JobStatus")
            msg = None
        except Exception as error_message:
            msg = str(error_message)
            track_counter += 2
            time.sleep(INTERVAL)
        else:
            if job_status == "Critical":
                msg = response.json_data.get("Messages")[0]["Message"]
                module.exit_json(msg=msg)
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


def get_error_syslog(idrac, curr_time, uri):
    error_log_found = False
    msg = None
    # 'SYS226' Unable to transfer a file, Catalog/Catalog.xml, because of the
    # reason described by the code 404 sent by the HTTP remote host server.
    # 'SYS252' Unable to transfer a file, Catalog/Catalog.xml, because the file is
    # not available at the remote host location.
    # 'SYS261' Unable to transfer the file, Catalog/catalog.xml, because initial network
    # connection to the remote host server is not successfully started.
    error_log_ids = ['SYS229', 'SYS227', 'RED132', 'JCP042', 'RED068', 'RED137']
    intrvl = 5
    retries = 60 // intrvl
    try:
        if not curr_time:
            resp = idrac.invoke_request(LOG_SERVICE_URI, "GET")
            uri = resp.json_data.get('Entries').get('@odata.id')
            curr_time = resp.json_data.get('DateTime')
        fltr = "?$filter=Created%20ge%20'{0}'".format(curr_time)
        fltr_uri = "{0}{1}".format(uri, fltr)
        while retries:
            resp = idrac.invoke_request(fltr_uri, "GET")
            logs_list = resp.json_data.get("Members")
            for log in logs_list:
                for err_id in error_log_ids:
                    if err_id in log.get('MessageId'):
                        error_log_found = True
                        msg = log.get('Message')
                        break
                if msg or error_log_found:
                    break
            if msg or error_log_found:
                break
            retries = retries - 1
            time.sleep(intrvl)
        else:
            msg = "No Error log found."
            error_log_found = False
    except Exception:
        msg = "No Error log found."
        error_log_found = False
    return error_log_found, msg


def update_firmware_url_redfish(module, idrac, share_path, apply_update, reboot, job_wait, payload, repo_urls):
    """Update firmware through HTTP/HTTPS/FTP and return the job details."""
    repo_url = urlparse(share_path)
    job_details, status = {}, {}
    ipaddr = repo_url.netloc
    share_type = repo_url.scheme
    sharename = repo_url.path.strip('/')
    if repo_url.path:
        payload['ShareName'] = sharename
    payload['IPAddress'] = ipaddr
    payload['ShareType'] = SHARE_TYPE[share_type]
    install_url = PATH
    get_repo_url = GET_REPO_BASED_UPDATE_LIST_PATH
    actions = repo_urls.get('Actions')
    if actions:
        install_url = actions.get("#DellSoftwareInstallationService.InstallFromRepository", {}).get("target", PATH)
        get_repo_url = actions.get("#DellSoftwareInstallationService.GetRepoBasedUpdateList", {}).\
            get("target", GET_REPO_BASED_UPDATE_LIST_PATH)
    try:
        log_resp = idrac.invoke_request(LOG_SERVICE_URI, "GET")
        log_uri = log_resp.json_data.get('Entries').get('@odata.id')
        curr_time = log_resp.json_data.get('DateTime')
    except Exception:
        log_uri = iDRAC9_LC_LOG
        curr_time = None
    resp = idrac.invoke_request(install_url, method="POST", data=payload)
    error_log_found, msg = get_error_syslog(idrac, curr_time, log_uri)
    job_id = get_jobid(module, resp)
    if error_log_found:
        module.exit_json(msg=msg, failed=True, job_id=job_id)
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
    proxy_support = PROXY_SUPPORT[module.params["proxy_support"]]
    proxy_type = module.params.get("proxy_type") if module.params.get("proxy_type") is not None else "HTTP"
    proxy_server = module.params.get("proxy_server") if module.params.get("proxy_server") is not None else ""
    proxy_port = module.params.get("proxy_port") if module.params.get("proxy_port") is not None else 80
    proxy_uname = module.params.get("proxy_uname")
    proxy_passwd = module.params.get("proxy_passwd")
    if ipaddr == "downloads.dell.com":
        status = idrac.update_mgr.update_from_dell_repo_url(
            ipaddress=ipaddr, share_type=share_type, share_name=sharename, catalog_file=catalog_file_name,
            apply_update=apply_update, reboot_needed=reboot, ignore_cert_warning=ignore_cert_warning, job_wait=job_wait,
            proxy_support=proxy_support, proxy_type=proxy_type, proxy_server=proxy_server, proxy_port=proxy_port,
            proxy_uname=proxy_uname, proxy_passwd=proxy_passwd)
        get_check_mode_status(status, module)
    else:
        status = idrac.update_mgr.update_from_repo_url(
            ipaddress=ipaddr, share_type=share_type, share_name=sharename, catalog_file=catalog_file_name,
            apply_update=apply_update, reboot_needed=reboot, ignore_cert_warning=ignore_cert_warning, job_wait=job_wait,
            proxy_support=proxy_support, proxy_type=proxy_type, proxy_server=proxy_server,
            proxy_port=proxy_port, proxy_uname=proxy_uname, proxy_passwd=proxy_passwd)
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
            msg['update_status'] = idrac.update_mgr.update_from_repo(
                upd_share, apply_update=apply_update, reboot_needed=reboot, job_wait=job_wait,)
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
            proxy = module.params.get("proxy_support")
            if proxy == "ParametersProxy":
                proxy_dict = {"proxy_server": "ProxyServer",
                              "proxy_port": "ProxyPort",
                              "proxy_support": "ProxySupport",
                              "proxy_type": "ProxyType",
                              "proxy_uname": "ProxyUname",
                              "proxy_passwd": "ProxyPasswd"}
                for pk, pv in proxy_dict.items():
                    prm = module.params.get(pk)
                    if prm is not None:
                        payload[pv] = prm
            elif proxy == "DefaultProxy":
                payload["ProxySupport"] = module.params.get("proxy_support")
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
                nfs = urlparse("nfs://" + share_name)
                payload['IPAddress'] = nfs.netloc.strip(':')
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
        "share_user": {"type": 'str'},
        "share_password": {"type": 'str', "aliases": ['share_pwd'], "no_log": True},
        "share_mnt": {"type": 'str'},

        "catalog_file_name": {"type": 'str', "default": "Catalog.xml"},
        "reboot": {"type": 'bool', "default": False},
        "job_wait": {"type": 'bool', "default": True},
        "ignore_cert_warning": {"type": 'bool', "default": True},
        "apply_update": {"type": 'bool', "default": True},
        # proxy params
        "proxy_support": {"default": 'Off', "type": 'str', "choices": ["Off", "ParametersProxy", "DefaultProxy"]},
        "proxy_type": {"type": 'str', "choices": ["HTTP", "SOCKS"]},
        "proxy_server": {"type": 'str'},
        "proxy_port": {"type": 'int'},
        "proxy_uname": {"type": 'str'},
        "proxy_passwd": {"type": 'str', "no_log": True},
    }
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        required_if=[
            # ['proxy_type', 'SOCKS', ('proxy_port',)],
            ['proxy_support', 'ParametersProxy', ('proxy_server', 'proxy_type', 'proxy_port',)],
        ],
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
    except URLError as err:
        message = err.reason if err.reason else err(str)
        module.exit_json(msg=message, unreachable=True)
    except (RuntimeError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError, SSLError) as e:
        module.fail_json(msg=str(e))
    except Exception as exc:
        module.fail_json(msg="Unhandled Exception {0}".format(exc))

    module.exit_json(msg=status['update_msg'], update_status=status['update_status'],
                     changed=status['changed'], failed=status['failed'])


if __name__ == '__main__':
    main()
