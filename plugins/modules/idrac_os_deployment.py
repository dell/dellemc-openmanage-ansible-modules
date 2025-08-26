#!/usr/bin/python
# -*- coding: utf-8 -*-
# Dell OpenManage Ansible Modules
# Version 10.0.0
# Copyright (C) 2018-2025 Dell Inc. or its subsidiaries. All Rights Reserved.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: idrac_os_deployment
short_description: Boot to a network ISO image
version_added: "2.1.0"
description: Boot to a network ISO image.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_x_auth_options
options:
    share_name:
        required: true
        description: CIFS or NFS Network share.
        type: str
    share_user:
        description:
          - Network share user in the format 'user@domain' or 'domain\\user'
            if user is part of a domain else 'user'. This option is mandatory
            for CIFS Network Share.
        type: str
    share_password:
        description:
          - Network share user password. This option is mandatory for CIFS
            Network Share.
        type: str
        aliases: ['share_pwd']
    iso_image:
        required: true
        description: Network ISO name.
        type: str
    expose_duration:
        description:
          - It is the time taken in minutes for the ISO image file to be exposed
            as a local CD-ROM device to the host server. When the time expires,
            the ISO image gets automatically detached.
        type: int
        default: 1080
requirements:
    - "python >= 3.9.6"
author:
    - "Felix Stephen (@felixs88)"
    - "Jagadeesh N V (@jagadeeshnv)"
    - "Abhishek Sinha (@ABHISHEK-SINHA10)"
    - "Bhavneet Sharma (@Bhavneet-Sharma)"
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports both IPv4 and IPv6 address for I(idrac_ip).
    - This module does not support C(check_mode).
'''

EXAMPLES = r'''
---
- name: Boot to Network ISO
  dellemc.openmanage.idrac_os_deployment:
      idrac_ip: "192.168.0.1"
      idrac_user: "user_name"
      idrac_password: "user_password"
      ca_path: "/path/to/ca_cert.pem"
      share_name: "192.168.0.0:/nfsfileshare"
      iso_image: "unattended_os_image.iso"
      expose_duration: 180
'''

RETURN = r'''
---
msg:
  type: str
  description: Over all device information status.
  returned: on error
  sample: "Failed to boot to network iso"
boot_status:
    description: Details of the boot to network ISO image operation.
    returned: always
    type: dict
    sample: {
        "DeleteOnCompletion": "false",
        "InstanceID": "DCIM_OSDConcreteJob:1",
        "JobName": "BootToNetworkISO",
        "JobStatus": "Success",
        "Message": "The command was successful.",
        "MessageID": "OSD1",
        "Name": "BootToNetworkISO",
        "Status": "Success",
        "file": "192.168.0.0:/nfsfileshare/unattended_os_image.iso",
        "retval": true
    }
'''


import json
import time
from ansible.module_utils.six.moves.urllib.parse import urlparse
from urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import idrac_auth_params, \
    iDRACRedfishAPI, IdracAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import \
    remove_key, wait_for_idrac_job_completion

MANAGER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"
JOB_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/Jobs"
SINGLE_JOB_URI = JOB_URI + "/{jobId}"
BootTONetworkISOURI = "/redfish/v1/Systems/System.Embedded.1/Oem/Dell/DellOSDeploymentService/Actions/DellOSDeploymentService.BootToNetworkISO"
ODATA_ID = "(.*?)@odata"
JOB_NOT_FOUND = "No matching job found following the BootToNetworkISO operation."
INVALID_EXPOSEDURATION = "Invalid value for ExposeDuration."


def minutes_to_iso_format(module, dur_minutes):
    """Convert minutes to iso format"""
    if dur_minutes < 0:
        module.exit_json(msg=INVALID_EXPOSEDURATION, failed=True)
    sample_time_str = '0000-00-00T00:00:00-00:00'
    time_part = sample_time_str.split('T')[1].split('-')[0]
    h, m, s = map(int, time_part.split(':'))
    # Add minutes
    m += dur_minutes
    h += m // 60
    m = m % 60
    h = h % 24

    new_time = f"{h:02}:{m:02}:{s:02}"
    formatted_time = sample_time_str.replace(time_part, new_time)
    return formatted_time


def get_current_time_from_idrac(idrac):
    """Get current time from iDRAC"""
    resp = idrac.invoke_request(MANAGER_URI, "GET")
    date_time = resp.json_data.get("DateTime")
    return date_time


def construct_payload(module):
    """Construct payload"""
    shr_name = module.params.get('share_name')
    ip_addr, share_name, share_type = '', '', ''
    if shr_name.startswith('\\\\'):
        cifs = shr_name.split('\\')
        ip_addr = cifs[2]
        share_name = '\\'.join(cifs[3:])
        share_type = 'CIFS'
    else:
        nfs = urlparse("nfs://" + shr_name)
        ip_addr = nfs.netloc.strip(':')
        share_name = nfs.path.strip('/')
        share_type = 'NFS'
    payload = {
        "ExposeDuration": minutes_to_iso_format(
            module, module.params.get('expose_duration')),
        "IPAddress": ip_addr,
        "ShareName": share_name,
        "ShareType": share_type,
        "ImageName": module.params.get('iso_image'),
    }

    if module.params.get('share_user'):
        payload["UserName"] = module.params['share_user']
    if module.params.get('share_password'):
        payload["Password"] = module.params['share_password']
    return payload


def filter_job_from_members(idrac, members, idrac_time):
    job_type = 'OSD: BootTONetworkISO'
    jid_list = []
    for membr in members:
        split_job_oid = membr.get("@odata.id").split("/")
        jid_list.append(split_job_oid[-1])

    for jid in jid_list:
        job_uri = SINGLE_JOB_URI.format(jobId=jid)
        resp = idrac.invoke_request(job_uri, "GET")
        job = resp.json_data
        art_time = job.get('StartTime')
        if job.get("Name") == job_type and art_time > idrac_time:
            return job
    return None


def getting_top_osd_job_and_tracking(idrac, module, idrac_time_str):
    job_id = None
    _out = {'msg': JOB_NOT_FOUND, 'failed': True}
    time.sleep(20)

    resp = idrac.invoke_request(JOB_URI, "GET")
    filtered_job = filter_job_from_members(
        idrac, resp.json_data.get("Members", []), idrac_time_str)
    if filtered_job:
        job_id = filtered_job.get("Id")
    if job_id:
        job_uri = SINGLE_JOB_URI.format(jobId=job_id)
        job_details, msg = wait_for_idrac_job_completion(
            idrac, job_uri, wait_timeout=1800)
        if job_details:
            return remove_key(job_details.json_data, regex_pattern=ODATA_ID)
        _out = {'msg': msg}
    module.exit_json(**_out)


def main():
    specs = {
        "share_name": {"required": True, "type": 'str'},
        "share_user": {"required": False, "type": 'str'},
        "share_password": {
            "required": False, "type": 'str', "aliases": ['share_pwd'],
            "no_log": True},
        "iso_image": {"required": True, "type": 'str'},
        "expose_duration": {"required": False, "type": 'int', "default": 1080}
    }
    specs.update(idrac_auth_params)
    module = IdracAnsibleModule(
        argument_spec=specs,
        supports_check_mode=False)

    try:
        with iDRACRedfishAPI(module.params) as idrac:
            idrac_time_str = get_current_time_from_idrac(idrac)
            payload = construct_payload(module)
            idrac.invoke_request(BootTONetworkISOURI, "POST", data=payload)
            resp = getting_top_osd_job_and_tracking(idrac, module,
                                                    idrac_time_str)
            boot_status = {'Message': resp.get("Message"),
                           'Status': resp.get("JobState")}
            if resp.get("JobState") == "Failed":
                module.exit_json(msg=boot_status, failed=True)
            module.exit_json(boot_status=boot_status, changed=True)
    except HTTPError as err:
        filter_err = remove_key(json.load(err), regex_pattern=ODATA_ID)
        module.exit_json(msg=str(err), error_info=filter_err, failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
