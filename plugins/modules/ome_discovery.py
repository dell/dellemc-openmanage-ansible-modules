#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2021-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_discovery
short_description: Create, modify, or delete a discovery job on OpenManage Enterprise
version_added: "3.3.0"
description: This module allows to create, modify, or delete a discovery job.
extends_documentation_fragment:
  - dellemc.openmanage.oment_auth_options
options:
  state:
    description:
      - C(present) creates a discovery job or modifies an existing discovery job.
      - I(discovery_job_name) is mandatory for the creation of a new discovery job.
      - If multiple discoveries of the same I(discovery_job_name) exist, then the new discovery job will not be created.
      - C(absent) deletes an existing discovery job(s) with the specified I(discovery_job_name).
    choices: [present, absent]
    default: present
    type: str
  discovery_job_name:
    description:
      - Name of the discovery configuration job.
      - It is mutually exclusive with I(discovery_id).
    type: str
  discovery_id:
    description:
      - ID of the discovery configuration group.
      - This value is DiscoveryConfigGroupId in the return values under discovery_status.
      - It is mutually exclusive with I(discovery_job_name).
    type: int
  new_name:
    description: New name of the discovery configuration job.
    type: str
  schedule:
    description:
      - Provides the option to schedule the discovery job.
      - If C(RunLater) is selected, then I(cron) must be specified.
    choices: [RunNow, RunLater]
    default: RunNow
    type: str
  cron:
    description:
      - Provide a cron expression based on Quartz cron format.
    type: str
  trap_destination:
    description:
      - Enable OpenManage Enterprise to receive the incoming SNMP traps from the discovered devices.
      - This is effective only for servers discovered by using their iDRAC interface.
    type: bool
    default: false
  community_string:
    description: "Enable the use of SNMP community strings to receive SNMP traps using Application Settings in
    OpenManage Enterprise. This option is available only for the discovered iDRAC servers and MX7000 chassis."
    type: bool
    default: false
  email_recipient:
    description: "Enter the email address to which notifications are to be sent about the discovery job status.
    Configure the SMTP settings to allow sending notifications to an email address."
    type: str
  job_wait:
    description:
      - Provides the option to wait for job completion.
      - This option is applicable when I(state) is C(present).
    type: bool
    default: true
  job_wait_timeout:
    description:
      - The maximum wait time of I(job_wait) in seconds. The job is tracked only for this duration.
      - This option is applicable when I(job_wait) is C(true).
    type: int
    default: 10800
  ignore_partial_failure:
    description:
      - "Provides the option to ignore partial failures. Partial failures occur when there is a combination of both
      discovered and undiscovered IPs."
      - If C(false), then the partial failure is not ignored, and the module will error out.
      - If C(true), then the partial failure is ignored.
      - This option is only applicable if I(job_wait) is C(true).
    type: bool
    default: false
  discovery_config_targets:
    description:
      - Provide the list of discovery targets.
      - "Each discovery target is a set of I(network_address_detail), I(device_types), and one or more protocol
      credentials."
      - This is mandatory when I(state) is C(present).
      - "C(WARNING) Modification of this field is not supported, this field is overwritten every time. Ensure to provide
      all the required details for this field."
    type: list
    elements: dict
    suboptions:
      network_address_detail:
        description:
          - "Provide the list of IP addresses, host names, or the range of IP addresses of the devices to be discovered
          or included."
          - "Sample Valid IP Range Formats"
          - "   192.35.0.0"
          - "   192.36.0.0-10.36.0.255"
          - "   192.37.0.0/24"
          - "   2345:f2b1:f083:135::5500/118"
          - "   2345:f2b1:f083:135::a500-2607:f2b1:f083:135::a600"
          - "   hostname.domain.tld"
          - "   hostname"
          - "   2345:f2b1:f083:139::22a"
          - "Sample Invalid IP Range Formats"
          - "   192.35.0.*"
          - "   192.36.0.0-255"
          - "   192.35.0.0/255.255.255.0"
          - C(NOTE) The range size for the number of IP addresses is limited to 16,385 (0x4001).
          - C(NOTE) Both IPv6 and IPv6 CIDR formats are supported.
        type: list
        elements: str
        required: true
      device_types:
        description:
          - Provide the type of devices to be discovered.
          - The accepted types are SERVER, CHASSIS, NETWORK SWITCH, and STORAGE.
          - A combination or all of the above can be provided.
          - "Supported protocols for each device type are:"
          - SERVER - I(wsman), I(redfish), I(snmp), I(ipmi), I(ssh), and I(vmware).
          - CHASSIS - I(wsman), and I(redfish).
          - NETWORK SWITCH - I(snmp).
          - STORAGE - I(storage), and I(snmp).
        type: list
        elements: str
        required: true
      wsman:
        description: Web Services-Management (WS-Man).
        type: dict
        suboptions:
          username:
            description: Provide a username for the protocol.
            type: str
            required: true
          password:
            description: Provide a password for the protocol.
            type: str
            required: true
          domain:
            description: Provide a domain for the protocol.
            type: str
          port:
            description: Enter the port number that the job must use to discover the devices.
            type: int
            default: 443
          retries:
            description: Enter the number of repeated attempts required to discover a device.
            type: int
            default: 3
          timeout:
            description: Enter the time in seconds after which a job must stop running.
            type: int
            default: 60
          cn_check:
            description: Enable the Common Name (CN) check.
            type: bool
            default: false
          ca_check:
            description: Enable the Certificate Authority (CA) check.
            type: bool
            default: false
          certificate_data:
            description: Provide certificate data for the CA check.
            type: str
      redfish:
        description: REDFISH protocol.
        type: dict
        suboptions:
          username:
            description: Provide a username for the protocol.
            type: str
            required: true
          password:
            description: Provide a password for the protocol.
            type: str
            required: true
          domain:
            description: Provide a domain for the protocol.
            type: str
          port:
            description: Enter the port number that the job must use to discover the devices.
            type: int
            default: 443
          retries:
            description: Enter the number of repeated attempts required to discover a device.
            type: int
            default: 3
          timeout:
            description: Enter the time in seconds after which a job must stop running.
            type: int
            default: 60
          cn_check:
            description: Enable the Common Name (CN) check.
            type: bool
            default: false
          ca_check:
            description: Enable the Certificate Authority (CA) check.
            type: bool
            default: false
          certificate_data:
            description: Provide certificate data for the CA check.
            type: str
      snmp:
        description: Simple Network Management Protocol (SNMP).
        type: dict
        suboptions:
          community:
            description: Community string for the SNMP protocol.
            type: str
            required: true
          port:
            description: Enter the port number that the job must use to discover the devices.
            type: int
            default: 161
          retries:
            description: Enter the number of repeated attempts required to discover a device.
            type: int
            default: 3
          timeout:
            description: Enter the time in seconds after which a job must stop running.
            type: int
            default: 3
      storage:
        description: HTTPS Storage protocol.
        type: dict
        suboptions:
          username:
            description: Provide a username for the protocol.
            type: str
            required: true
          password:
            description: Provide a password for the protocol.
            type: str
            required: true
          domain:
            description: Provide a domain for the protocol.
            type: str
          port:
            description: Enter the port number that the job must use to discover the devices.
            type: int
            default: 443
          retries:
            description: Enter the number of repeated attempts required to discover a device.
            type: int
            default: 3
          timeout:
            description: Enter the time in seconds after which a job must stop running.
            type: int
            default: 60
          cn_check:
            description: Enable the Common Name (CN) check.
            type: bool
            default: false
          ca_check:
            description: Enable the Certificate Authority (CA) check.
            type: bool
            default: false
          certificate_data:
            description: Provide certificate data for the CA check.
            type: str
      vmware:
        description: VMWARE protocol.
        type: dict
        suboptions:
          username:
            description: Provide a username for the protocol.
            type: str
            required: true
          password:
            description: Provide a password for the protocol.
            type: str
            required: true
          domain:
            description: Provide a domain for the protocol.
            type: str
          port:
            description: Enter the port number that the job must use to discover the devices.
            type: int
            default: 443
          retries:
            description: Enter the number of repeated attempts required to discover a device.
            type: int
            default: 3
          timeout:
            description: Enter the time in seconds after which a job must stop running.
            type: int
            default: 60
          cn_check:
            description: Enable the Common Name (CN) check.
            type: bool
            default: false
          ca_check:
            description: Enable the Certificate Authority (CA) check.
            type: bool
            default: false
          certificate_data:
            description: Provide certificate data for the CA check.
            type: str
      ssh:
        description: Secure Shell (SSH).
        type: dict
        suboptions:
          username:
            description: Provide a username for the protocol.
            type: str
            required: true
          password:
            description: Provide a password for the protocol.
            type: str
            required: true
          port:
            description: Enter the port number that the job must use to discover the devices.
            type: int
            default: 22
          retries:
            description: Enter the number of repeated attempts required to discover a device.
            type: int
            default: 3
          timeout:
            description: Enter the time in seconds after which a job must stop running.
            type: int
            default: 60
          check_known_hosts:
            description: Verify the known host key.
            type: bool
            default: false
          is_sudo_user:
            description: Use the SUDO option.
            type: bool
            default: false
      ipmi:
        description: Intelligent Platform Management Interface (IPMI)
        type: dict
        suboptions:
          username:
            description: Provide a username for the protocol.
            type: str
            required: true
          password:
            description: Provide a password for the protocol.
            type: str
            required: true
          retries:
            description: Enter the number of repeated attempts required to discover a device.
            type: int
            default: 3
          timeout:
            description: Enter the time in seconds after which a job must stop running.
            type: int
            default: 60
          kgkey:
            description: KgKey for the IPMI protocol.
            type: str
requirements:
    - "python >= 3.9.6"
author:
    - "Jagadeesh N V (@jagadeeshnv)"
    - "Sajna Shetty (@Sajna-Shetty)"
    - "Abhishek Sinha (@Abhishek-Dell)"
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
    - This module does not support C(check_mode).
    - If I(state) is C(present), then Idempotency is not supported.
'''

EXAMPLES = r'''
---
- name: Discover servers in a range
  dellemc.openmanage.ome_discovery:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    discovery_job_name: "Discovery_server_1"
    discovery_config_targets:
      - network_address_detail:
          - 192.96.24.1-192.96.24.255
        device_types:
          - SERVER
        wsman:
          username: user
          password: password

- name: Discover chassis in a range
  dellemc.openmanage.ome_discovery:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    discovery_job_name: "Discovery_chassis_1"
    discovery_config_targets:
      - network_address_detail:
          - 192.96.24.1-192.96.24.255
        device_types:
          - CHASSIS
        wsman:
          username: user
          password: password

- name: Discover switches in a range
  dellemc.openmanage.ome_discovery:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    discovery_job_name: "Discover_switch_1"
    discovery_config_targets:
      - network_address_detail:
          - 192.96.24.1-192.96.24.255
        device_types:
          - NETWORK SWITCH
        snmp:
          community: snmp_creds

- name: Discover storage in a range
  dellemc.openmanage.ome_discovery:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    discovery_job_name: "Discover_storage_1"
    discovery_config_targets:
      - network_address_detail:
          - 192.96.24.1-192.96.24.255
        device_types:
          - STORAGE
        storage:
          username: user
          password: password
        snmp:
          community: snmp_creds

- name: Delete a discovery job
  dellemc.openmanage.ome_discovery:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "absent"
    discovery_job_name: "Discovery-123"

- name: Schedule the discovery of multiple devices ignoring partial failure and enable trap to receive alerts
  dellemc.openmanage.ome_discovery:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    state: "present"
    discovery_job_name: "Discovery-123"
    discovery_config_targets:
      - network_address_detail:
          - 192.96.24.1-192.96.24.255
          - 192.96.0.0/24
          - 192.96.26.108
        device_types:
          - SERVER
          - CHASSIS
          - STORAGE
          - NETWORK SWITCH
        wsman:
          username: wsman_user
          password: wsman_pwd
        redfish:
          username: redfish_user
          password: redfish_pwd
        snmp:
          community: snmp_community
      - network_address_detail:
          - 192.96.25.1-192.96.25.255
          - ipmihost
          - esxiserver
          - sshserver
        device_types:
          - SERVER
        ssh:
          username: ssh_user
          password: ssh_pwd
        vmware:
          username: vm_user
          password: vmware_pwd
        ipmi:
          username: ipmi_user
          password: ipmi_pwd
    schedule: RunLater
    cron: "0 0 9 ? * MON,WED,FRI *"
    ignore_partial_failure: true
    trap_destination: true
    community_string: true
    email_recipient: test_email@company.com

- name: Discover servers with ca check enabled
  dellemc.openmanage.ome_discovery:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    discovery_job_name: "Discovery_server_ca1"
    discovery_config_targets:
      - network_address_detail:
          - 192.96.24.108
        device_types:
          - SERVER
        wsman:
          username: user
          password: password
          ca_check: true
          certificate_data: "{{ lookup('ansible.builtin.file', '/path/to/certificate_data_file') }}"

- name: Discover chassis with ca check enabled data
  dellemc.openmanage.ome_discovery:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    discovery_job_name: "Discovery_chassis_ca1"
    discovery_config_targets:
      - network_address_detail:
          - 192.96.24.108
        device_types:
          - CHASSIS
        redfish:
          username: user
          password: password
          ca_check: true
          certificate_data: "-----BEGIN CERTIFICATE-----\r\n
          ABCDEFGHIJKLMNOPQRSTUVWXYZaqwertyuiopasdfghjklzxcvbnmasdasagasvv\r\n
          ABCDEFGHIJKLMNOPQRSTUVWXYZaqwertyuiopasdfghjklzxcvbnmasdasagasvv\r\n
          ABCDEFGHIJKLMNOPQRSTUVWXYZaqwertyuiopasdfghjklzxcvbnmasdasagasvv\r\n
          aqwertyuiopasdfghjklzxcvbnmasdasagasvv=\r\n
          -----END CERTIFICATE-----"
'''

RETURN = r'''
---
msg:
  description: Overall status of the discovery operation.
  returned: always
  type: str
  sample: "Successfully deleted 1 discovery job(s)."
discovery_status:
  description:
    - Details of the discovery job created or modified.
    - If I(job_wait) is true, Completed and Failed IPs are also listed.
  returned: when I(state) is C(present)
  type: dict
  sample: {
    "Completed": [
      "192.168.24.17",
      "192.168.24.20",
      "192.168.24.22"
    ],
    "Failed": [
      "192.168.24.15",
      "192.168.24.16",
      "192.168.24.18",
      "192.168.24.19",
      "192.168.24.21",
      "host123"
    ],
    "DiscoveredDevicesByType": [
      {
        "Count": 3,
        "DeviceType": "SERVER"
      }
    ],
    "DiscoveryConfigDiscoveredDeviceCount": 3,
    "DiscoveryConfigEmailRecipient": "myemail@dell.com",
    "DiscoveryConfigExpectedDeviceCount": 9,
    "DiscoveryConfigGroupId": 125,
    "JobDescription": "D1",
    "JobEnabled": true,
    "JobEndTime": "2021-01-01 06:27:29.99",
    "JobId": 12666,
    "JobName": "D1",
    "JobNextRun": null,
    "JobProgress": "100",
    "JobSchedule": "startnow",
    "JobStartTime": "2021-01-01 06:24:10.071",
    "JobStatusId": 2090,
    "LastUpdateTime": "2021-01-01 06:27:30.001",
    "UpdatedBy": "admin"
  }
discovery_ids:
  description: IDs of the discoveries with duplicate names.
  returned: when discoveries with duplicate name exist for I(state) is C(present)
  type: list
  sample: [1234, 5678]
job_detailed_status:
  description: Detailed last execution history of a job.
  returned: All time.
  type: list
  sample: [
        {
            "ElapsedTime": "00:00:00",
            "EndTime": null,
            "ExecutionHistoryId": 564873,
            "Id": 656893,
            "IdBaseEntity": 0,
            "JobStatus": {
                "Id": 2050,
                "Name": "Running"
            },
            "Key": "192.96.24.1",
            "Progress": "0",
            "StartTime": "2023-07-04 06:23:54.008",
            "Value": "Running\nDiscovery of target 192.96.24.1 started.\nDiscovery target resolved to IP  192.96.24.1 ."
        }
    ]
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
      "code": "Base.1.0.GeneralError",
      "message": "A general error has occurred. See ExtendedInfo for more information.",
      "@Message.ExtendedInfo": [
        {
          "MessageId": "GEN1234",
          "RelatedProperties": [],
          "Message": "Unable to process the request because an error occurred.",
          "MessageArgs": [],
          "Severity": "Critical",
          "Resolution": "Retry the operation. If the issue persists, contact your system administrator."
        }
      ]
    }
  }
'''

import json
import time
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, OmeAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import strip_substr_dict
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.common.dict_transformations import snake_dict_to_camel_dict

CONFIG_GROUPS_URI = "DiscoveryConfigService/DiscoveryConfigGroups"
DISCOVERY_JOBS_URI = "DiscoveryConfigService/Jobs"
DELETE_JOB_URI = "DiscoveryConfigService/Actions/DiscoveryConfigService.RemoveDiscoveryGroup"
PROTOCOL_DEVICE = "DiscoveryConfigService/ProtocolToDeviceType"
JOB_EXEC_HISTORY = "JobService/Jobs({job_id})/ExecutionHistories"
CONFIG_GROUPS_ID_URI = "DiscoveryConfigService/DiscoveryConfigGroups({group_id})"
NO_CHANGES_MSG = "No changes found to be applied."
DISC_JOB_RUNNING = "Discovery job '{name}' with ID {id} is running. Please retry after job completion."
DISC_DEL_JOBS_SUCCESS = "Successfully deleted {n} discovery job(s)."
MULTI_DISCOVERY = "Multiple discoveries present. Run the job again using a specific ID."
DISCOVERY_SCHEDULED = "Successfully scheduled the Discovery job."
DISCOVER_JOB_COMPLETE = "Successfully completed the Discovery job."
JOB_TRACK_SUCCESS = "Discovery job has {0}."
JOB_TRACK_FAIL = "No devices discovered, job is in {0} state."
JOB_TRACK_UNABLE = "Unable to track discovery job status of {0}."
JOB_TRACK_INCOMPLETE = "Discovery job {0} incomplete after polling {1} times."
INVALID_DEVICES = "Invalid device types found - {0}."
DISCOVERY_PARTIAL = "Some IPs are not discovered."
ATLEAST_ONE_PROTOCOL = "Protocol not applicable for given device types."
INVALID_DISCOVERY_ID = "Invalid discovery ID provided."
SETTLING_TIME = 5
JOB_STATUS_MAP = {
    2020: "Scheduled", 2030: "Queued", 2040: "Starting", 2050: "Running", 2060: "completed successfully",
    2070: "Failed", 2090: "completed with errors", 2080: "New", 2100: "Aborted", 2101: "Paused", 2102: "Stopped",
    2103: "Canceled"
}


def check_existing_discovery(module, rest_obj):
    discovery_cfgs = []
    discovery_id = module.params.get("discovery_id")
    srch_key = "DiscoveryConfigGroupName"
    srch_val = module.params.get("discovery_job_name")
    if discovery_id:
        srch_key = "DiscoveryConfigGroupId"
        srch_val = module.params.get("discovery_id")
    resp = rest_obj.invoke_request('GET', CONFIG_GROUPS_URI + "?$top=9999")
    discovs = resp.json_data.get("value")
    for d in discovs:
        if d[srch_key] == srch_val:
            discovery_cfgs.append(d)
            if discovery_id:
                break
    return discovery_cfgs


def get_discovery_states(rest_obj, key="JobStatusId"):
    resp = rest_obj.invoke_request('GET', DISCOVERY_JOBS_URI)
    disc_jobs = resp.json_data.get("value")
    job_state_dict = dict([(item["DiscoveryConfigGroupId"], item[key]) for item in disc_jobs])
    return job_state_dict


def get_protocol_device_map(rest_obj):
    prot_dev_map = {}
    dev_id_map = {}
    resp = rest_obj.invoke_request('GET', PROTOCOL_DEVICE)
    prot_dev = resp.json_data.get('value')
    for item in prot_dev:
        dname = item["DeviceTypeName"]
        dlist = prot_dev_map.get(dname, [])
        dlist.append(item["ProtocolName"])
        prot_dev_map[dname] = dlist
        dev_id_map[dname] = item["DeviceTypeId"]
        if dname == "DELL STORAGE":
            prot_dev_map['STORAGE'] = dlist
            dev_id_map['STORAGE'] = item["DeviceTypeId"]
    return prot_dev_map, dev_id_map


def get_other_discovery_payload(module):
    trans_dict = {'discovery_job_name': "DiscoveryConfigGroupName",
                  'trap_destination': "TrapDestination",
                  'community_string': "CommunityString",
                  'email_recipient': "DiscoveryStatusEmailRecipient"}
    other_dict = {}
    for key, val in trans_dict.items():
        if module.params.get(key) is not None:
            other_dict[val] = module.params.get(key)
    return other_dict


def get_schedule(module):
    schedule_payload = {}
    schedule = module.params.get('schedule')
    if not schedule or schedule == 'RunNow':
        schedule_payload['RunNow'] = True
        schedule_payload['RunLater'] = False
        schedule_payload['Cron'] = 'startnow'
    else:
        schedule_payload['RunNow'] = False
        schedule_payload['RunLater'] = True
        schedule_payload['Cron'] = module.params.get('cron')
    return schedule_payload


def get_execution_details(rest_obj, job_id):
    try:
        ips = {"Completed": [], "Failed": []}
        job_detail_status = []
        resp = rest_obj.invoke_request('GET', JOB_EXEC_HISTORY.format(job_id=job_id))
        ex_hist = resp.json_data.get('value')
        # Sorting based on startTime and to get latest execution instance.
        tmp_dict = dict((x["StartTime"], x["Id"]) for x in ex_hist)
        sorted_dates = sorted(tmp_dict.keys())
        ex_url = JOB_EXEC_HISTORY.format(job_id=job_id) + "({0})/ExecutionHistoryDetails".format(tmp_dict[sorted_dates[-1]])
        all_exec = rest_obj.get_all_items_with_pagination(ex_url)
        for jb_ip in all_exec.get('value'):
            jb_ip = strip_substr_dict(jb_ip)
            jb_ip.get('JobStatus', {}).pop('@odata.type', None)
            job_detail_status.append(jb_ip)
            jobstatus = jb_ip.get('JobStatus', {}).get('Name', 'Unknown')
            jlist = ips.get(jobstatus, [])
            jlist.append(jb_ip.get('Key'))
            ips[jobstatus] = jlist
    except Exception:
        pass
    return ips, job_detail_status


def discovery_job_tracking(rest_obj, job_id, job_wait_sec):
    sleep_interval = 30
    max_retries = job_wait_sec // sleep_interval
    failed_job_status = [2070, 2100, 2101, 2102, 2103]
    success_job_status = [2060, 2020, 2090]
    job_url = (DISCOVERY_JOBS_URI + "({job_id})").format(job_id=job_id)
    loop_ctr = 0
    time.sleep(SETTLING_TIME)
    while loop_ctr < max_retries:
        loop_ctr += 1
        try:
            job_resp = rest_obj.invoke_request('GET', job_url)
            job_dict = job_resp.json_data
            job_status = job_dict['JobStatusId']
            if job_status in success_job_status:
                return JOB_TRACK_SUCCESS.format(JOB_STATUS_MAP[job_status])
            elif job_status in failed_job_status:
                return JOB_TRACK_FAIL.format(JOB_STATUS_MAP[job_status])
            time.sleep(sleep_interval)
        except HTTPError:
            return JOB_TRACK_UNABLE.format(job_id)
        except Exception as err:
            return str(err)
    return JOB_TRACK_INCOMPLETE.format(job_id, max_retries)


def get_job_data(discovery_json, rest_obj):
    job_list = discovery_json['DiscoveryConfigTaskParam']
    if len(job_list) == 1:
        job_id = job_list[0].get('TaskId')
    else:
        srch_key = 'DiscoveryConfigGroupId'
        srch_val = discovery_json[srch_key]
        resp = rest_obj.invoke_request('GET', DISCOVERY_JOBS_URI + "?$top=9999")
        discovs = resp.json_data.get("value")
        for d in discovs:
            if d[srch_key] == srch_val:
                job_id = d['JobId']
                break
    return job_id


def get_connection_profile(disc_config):
    proto_add_dict = {
        'wsman': {
            'certificateDetail': None,
            'isHttp': False,
            'keepAlive': True,
            # 'version': None
        },
        'redfish': {'certificateDetail': None, 'isHttp': False, 'keepAlive': True},
        'snmp': {
            # 'authenticationPassphrase': None,
            # 'authenticationProtocol': None,
            'enableV1V2': True,
            'enableV3': False,
            # 'localizationEngineID': None,
            # 'privacyPassphrase': None,
            # 'privacyProtocol': None,
            # 'securityName': None
        },
        'vmware': {'certificateDetail': None, 'isHttp': False, 'keepAlive': False},
        'ssh': {'useKey': False, 'key': None, 'knownHostKey': None, 'passphrase': None},
        'ipmi': {'privilege': 2},
        'storage': {
            'certificateDetail': None,
            'isHttp': False,
            'keepAlive': True,
            # 'version': None
        }
    }
    proto_list = ['wsman', 'snmp', 'vmware', 'ssh', 'ipmi', 'redfish', 'storage']
    conn_profile = {"profileId": 0, "profileName": "", "profileDescription": "", "type": "DISCOVERY"}
    creds_dict = {}
    for p in proto_list:
        if disc_config.get(p):
            xproto = {"type": p.upper(),
                      "authType": "Basic",
                      "modified": False}
            xproto['credentials'] = snake_dict_to_camel_dict(disc_config[p])
            (xproto['credentials']).update(proto_add_dict.get(p, {}))
            creds_dict[p] = xproto
            # Special handling, duplicating wsman to redfish as in GUI
            if p == 'wsman':
                rf = xproto.copy()
                rf['type'] = 'REDFISH'
                creds_dict['redfish'] = rf
    conn_profile['credentials'] = list(creds_dict.values())
    return conn_profile


def get_discovery_config(module, rest_obj):
    disc_cfg_list = []
    proto_dev_map, dev_id_map = get_protocol_device_map(rest_obj)
    discovery_config_list = module.params.get("discovery_config_targets")
    for disc_config in discovery_config_list:
        disc_cfg = {}
        disc_cfg['DeviceType'] = list(
            dev_id_map[dev] for dev in disc_config.get('device_types') if dev in dev_id_map.keys())
        devices = list(set(disc_config.get('device_types')))
        if len(devices) != len(disc_cfg['DeviceType']):
            invalid_dev = set(devices) - set(dev_id_map.keys())
            module.fail_json(msg=INVALID_DEVICES.format(','.join(invalid_dev)))
        disc_cfg["DiscoveryConfigTargets"] = list({"NetworkAddressDetail": ip} for ip in disc_config["network_address_detail"])
        conn_profile = get_connection_profile(disc_config)
        given_protos = list(x["type"] for x in conn_profile['credentials'])
        req_protos = []
        for dev in disc_config.get('device_types'):
            proto_dev_value = proto_dev_map.get(dev, [])
            req_protos.extend(proto_dev_value)
        if not (set(req_protos) & set(given_protos)):
            module.fail_json(msg=ATLEAST_ONE_PROTOCOL, discovery_status=proto_dev_map)
        disc_cfg["ConnectionProfile"] = json.dumps(conn_profile)
        disc_cfg_list.append(disc_cfg)
    return disc_cfg_list


def get_discovery_job(rest_obj, job_id):
    resp = rest_obj.invoke_request('GET', DISCOVERY_JOBS_URI + "({0})".format(job_id))
    djob = resp.json_data
    nlist = list(djob)
    for k in nlist:
        if str(k).lower().startswith('@odata'):
            djob.pop(k)
    return djob


def exit_discovery(module, rest_obj, job_id):
    msg = DISCOVERY_SCHEDULED
    time.sleep(SETTLING_TIME)
    djob = get_discovery_job(rest_obj, job_id)
    detailed_job = []
    if module.params.get("job_wait") and module.params.get('schedule') == 'RunNow':
        job_message = discovery_job_tracking(rest_obj, job_id, job_wait_sec=module.params["job_wait_timeout"])
        msg = job_message
        ip_details, detailed_job = get_execution_details(rest_obj, job_id)
        djob = get_discovery_job(rest_obj, job_id)
        djob.update(ip_details)
        if djob["JobStatusId"] == 2090 and not module.params.get("ignore_partial_failure"):
            module.fail_json(msg=DISCOVERY_PARTIAL, discovery_status=djob, job_detailed_status=detailed_job)
        if djob["JobStatusId"] == 2090 and module.params.get("ignore_partial_failure"):
            module.exit_json(msg=JOB_TRACK_SUCCESS.format(JOB_STATUS_MAP[djob["JobStatusId"]]), discovery_status=djob,
                             job_detailed_status=detailed_job, changed=True)
        if ip_details.get("Failed"):
            module.fail_json(msg=JOB_TRACK_FAIL.format(JOB_STATUS_MAP[djob["JobStatusId"]]), discovery_status=djob,
                             job_detailed_status=detailed_job)
    module.exit_json(msg=msg, discovery_status=djob, job_detailed_status=detailed_job, changed=True)


def create_discovery(module, rest_obj):
    discovery_payload = {}
    discovery_payload['DiscoveryConfigModels'] = get_discovery_config(module, rest_obj)
    discovery_payload['Schedule'] = get_schedule(module)
    other_params = get_other_discovery_payload(module)
    discovery_payload.update(other_params)
    resp = rest_obj.invoke_request("POST", CONFIG_GROUPS_URI, data=discovery_payload)
    job_id = get_job_data(resp.json_data, rest_obj)
    exit_discovery(module, rest_obj, job_id)


def update_modify_payload(discovery_modify_payload, current_payload, new_name=None):
    parent_items = ["DiscoveryConfigGroupName",
                    "TrapDestination",
                    "CommunityString",
                    "DiscoveryStatusEmailRecipient",
                    "CreateGroup",
                    "UseAllProfiles"]
    for key in parent_items:
        if key not in discovery_modify_payload and key in current_payload:
            discovery_modify_payload[key] = current_payload[key]
    if not discovery_modify_payload.get("Schedule"):
        exist_schedule = current_payload.get("Schedule", {})
        schedule_payload = {}
        if exist_schedule.get('Cron') == 'startnow':
            schedule_payload['RunNow'] = True
            schedule_payload['RunLater'] = False
            schedule_payload['Cron'] = 'startnow'
        else:
            schedule_payload['RunNow'] = False
            schedule_payload['RunLater'] = True
            schedule_payload['Cron'] = exist_schedule.get('Cron')
        discovery_modify_payload['Schedule'] = schedule_payload
    discovery_modify_payload["DiscoveryConfigGroupId"] = current_payload["DiscoveryConfigGroupId"]
    if new_name:
        discovery_modify_payload["DiscoveryConfigGroupName"] = new_name


def modify_discovery(module, rest_obj, discov_list):
    if len(discov_list) > 1:
        dup_discovery = list(item["DiscoveryConfigGroupId"] for item in discov_list)
        module.fail_json(msg=MULTI_DISCOVERY, discovery_ids=dup_discovery)
    job_state_dict = get_discovery_states(rest_obj)
    for d in discov_list:
        if job_state_dict.get(d["DiscoveryConfigGroupId"]) == 2050:
            module.fail_json(
                msg=DISC_JOB_RUNNING.format(name=d["DiscoveryConfigGroupName"], id=d["DiscoveryConfigGroupId"]))
    discovery_payload = {'DiscoveryConfigModels': get_discovery_config(module, rest_obj),
                         'Schedule': get_schedule(module)}
    other_params = get_other_discovery_payload(module)
    discovery_payload.update(other_params)
    update_modify_payload(discovery_payload, discov_list[0], module.params.get("new_name"))
    resp = rest_obj.invoke_request("PUT",
                                   CONFIG_GROUPS_ID_URI.format(group_id=discovery_payload["DiscoveryConfigGroupId"]),
                                   data=discovery_payload)
    job_id = get_job_data(resp.json_data, rest_obj)
    exit_discovery(module, rest_obj, job_id)


def delete_discovery(module, rest_obj, discov_list):
    job_state_dict = get_discovery_states(rest_obj)
    delete_ids = []
    for d in discov_list:
        if job_state_dict.get(d["DiscoveryConfigGroupId"]) == 2050:
            module.fail_json(msg=DISC_JOB_RUNNING.format(name=d["DiscoveryConfigGroupName"],
                                                         id=d["DiscoveryConfigGroupId"]))
        else:
            delete_ids.append(d["DiscoveryConfigGroupId"])
    delete_payload = {"DiscoveryGroupIds": delete_ids}
    rest_obj.invoke_request('POST', DELETE_JOB_URI, data=delete_payload)
    module.exit_json(msg=DISC_DEL_JOBS_SUCCESS.format(n=len(delete_ids)), changed=True)


def main():
    http_creds = {"username": {"type": 'str', "required": True},
                  "password": {"type": 'str', "required": True, "no_log": True},
                  "domain": {"type": 'str'},
                  "retries": {"type": 'int', "default": 3},
                  "timeout": {"type": 'int', "default": 60},
                  "port": {"type": 'int', "default": 443},
                  "cn_check": {"type": 'bool', "default": False},
                  "ca_check": {"type": 'bool', "default": False},
                  "certificate_data": {"type": 'str', "no_log": True}
                  }
    snmp_creds = {"community": {"type": 'str', "required": True},
                  "retries": {"type": 'int', "default": 3},
                  "timeout": {"type": 'int', "default": 3},
                  "port": {"type": 'int', "default": 161},
                  }
    ssh_creds = {"username": {"type": 'str', "required": True},
                 "password": {"type": 'str', "required": True, "no_log": True},
                 "retries": {"type": 'int', "default": 3},
                 "timeout": {"type": 'int', "default": 60},
                 "port": {"type": 'int', "default": 22},
                 "check_known_hosts": {"type": 'bool', "default": False},
                 "is_sudo_user": {"type": 'bool', "default": False}
                 }
    ipmi_creds = {"username": {"type": 'str', "required": True},
                  "password": {"type": 'str', "required": True, "no_log": True},
                  "retries": {"type": 'int', "default": 3},
                  "timeout": {"type": 'int', "default": 60},
                  "kgkey": {"type": 'str', "no_log": True}
                  }
    discovery_config_model = {"device_types": {"required": True, 'type': 'list', "elements": 'str'},
                              "network_address_detail": {"required": True, "type": 'list', "elements": 'str'},
                              "wsman": {"type": 'dict', "options": http_creds,
                                        "required_if": [['ca_check', True, ('certificate_data',)]]},
                              "storage": {"type": 'dict', "options": http_creds,
                                          "required_if": [['ca_check', True, ('certificate_data',)]]},
                              "redfish": {"type": 'dict', "options": http_creds,
                                          "required_if": [['ca_check', True, ('certificate_data',)]]},
                              "vmware": {"type": 'dict', "options": http_creds,
                                         "required_if": [['ca_check', True, ('certificate_data',)]]},
                              "snmp": {"type": 'dict', "options": snmp_creds},
                              "ssh": {"type": 'dict', "options": ssh_creds},
                              "ipmi": {"type": 'dict', "options": ipmi_creds},
                              }
    specs = {
        "discovery_job_name": {"type": 'str'},
        "discovery_id": {"type": 'int'},
        "state": {"default": "present", "choices": ['present', 'absent']},
        "new_name": {"type": 'str'},
        "discovery_config_targets":
            {"type": 'list', "elements": 'dict', "options": discovery_config_model,
             "required_one_of": [
                 ('wsman', 'storage', 'redfish', 'vmware', 'snmp', 'ssh', 'ipmi')
             ]},
        "schedule": {"default": 'RunNow', "choices": ['RunNow', 'RunLater']},
        "cron": {"type": 'str'},
        "job_wait": {"type": 'bool', "default": True},
        "job_wait_timeout": {"type": 'int', "default": 10800},
        "trap_destination": {"type": 'bool', "default": False},
        "community_string": {"type": 'bool', "default": False},
        "email_recipient": {"type": 'str'},
        "ignore_partial_failure": {"type": 'bool', "default": False}
    }

    module = OmeAnsibleModule(
        argument_spec=specs,
        required_if=[
            ['state', 'present', ('discovery_config_targets',)],
            ['schedule', 'RunLater', ('cron',)]
        ],
        required_one_of=[('discovery_job_name', 'discovery_id')],
        mutually_exclusive=[('discovery_job_name', 'discovery_id')],
        supports_check_mode=False
    )
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            discov_list = check_existing_discovery(module, rest_obj)
            if module.params.get('state') == 'absent':
                if discov_list:
                    delete_discovery(module, rest_obj, discov_list)
                module.exit_json(msg=NO_CHANGES_MSG)
            else:
                if discov_list:
                    modify_discovery(module, rest_obj, discov_list)
                else:
                    if module.params.get('discovery_id'):
                        module.fail_json(msg=INVALID_DISCOVERY_ID)
                    create_discovery(module, rest_obj)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, TypeError, ConnectionError, SSLValidationError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == "__main__":
    main()
