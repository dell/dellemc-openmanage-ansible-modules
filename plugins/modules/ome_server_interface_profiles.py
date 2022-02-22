#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.1.0
# Copyright (C) 2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ome_server_interface_profiles
short_description: Configure server interface profiles
version_added: "5.1.0"
description: This module allows to configure server interface profiles on OpenManage Enterprise Modular.
extends_documentation_fragment:
  - dellemc.openmanage.omem_auth_options
options:
  device_id:
    description:
      - Device id of the Server under chassis fabric.
      - I(device_id) and I(device_service_tag) is mutually exclusive.
    type: list
    elements: int
  device_service_tag:
    description:
      - Service tag of the Server under chassis fabric.
      - I(device_service_tag) and I(device_id) is mutually exclusive.
    type: list
    elements: str
  nic_teaming:
    description:
      - NIC teaming options.
      - C(NoTeaming) the NICs are not bonded and provide no load balancing or redundancy.
      - C(LACP) use LACP for NIC teaming.
      - C(Other) use other technology for NIC teaming.
    choices: ['LACP', 'NoTeaming', 'Other']
    type: str
  nic_configuration:
    description: NIC configuration for the Servers to be applied.
    type: list
    elements: dict
    suboptions:
      nic_identifier:
        description:
          - ID of the NIC or port number.
          - C(Note) This will not be validated.
        type: str
        required: True
      team:
        description:
          - Group two or more ports. The ports must be connected to the same pair of Ethernet switches.
          - I(team) is applicable only if I(nic_teaming) is C(LACP).
        type: bool
      untagged_network:
        description:
          - The maximum or minimum VLAN id of the network to be untagged.
          - The I(untagged_network) can be retrieved using the M(dellemc.openmanage.ome_network_vlan_info)
          - If I(untagged_network) needs to be unset this needs to be sent as C(0)
          - C(Note) The network cannot be added as a untagged network if it is already assigned to a tagged network.
        type: int
      tagged_networks:
        description:
          - List of tagged networks
          - Network cannot be added as a tagged network if it is already assigned to untagged network
        type: dict
        suboptions:
          state:
            description:
              - Indicates if a list of networks needs to be added or deleted.
              - C(present) to add the network to the tagged list
              - C(absent) to delete the Network from the tagged list
            choices: [present, absent]
            type: str
            default: present
          names:
            description:
              - List of network name to be marked as tagged networks
              - The I(names) can be retrieved using the M(dellemc.openmanage.ome_network_vlan_info)
            type: list
            elements: str
            required: True
  job_wait:
    description:
      - Provides the option to wait for job completion.
    type: bool
    default: true
  job_wait_timeout:
    description:
      - The maximum wait time of I(job_wait) in seconds. The job is  tracked only for this duration.
      - This option is applicable when I(job_wait) is C(True).
    type: int
    default: 120
requirements:
    - "python >= 3.8.6"
author: "Jagadeesh N V (@jagadeeshnv)"
notes:
    - This module supports C(check_mode).
    - Run this module from a system that has direct access to Dell EMC OpenManage Enterprise Modular.
'''

EXAMPLES = r'''
---
- name: Modify Server Interface Profile for the server using the service tag
  dellemc.openmanage.ome_server_interface_profiles:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_service_tag:
      - SVCTAG1
      - SVCTAG2
    nic_teaming: LACP
    nic_configuration:
      - nic_identifier: NIC.Mezzanine.1A-1-1
        team: no
        untagged_network: 2
        tagged_networks:
          names:
            - vlan1
      - nic_identifier: NIC.Mezzanine.1A-2-1
        team: yes
        untagged_network: 3
        tagged_networks:
          names:
            - range120-125

- name: Modify Server Interface Profile for the server using the device id
  dellemc.openmanage.ome_server_interface_profiles:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    device_id:
      - 34523
      - 48999
    nic_teaming: NoTeaming
    nic_configuration:
      - nic_identifier: NIC.Mezzanine.1A-1-1
        team: no
        untagged_network: 2
        tagged_networks:
          names:
            - vlan2
      - nic_identifier: NIC.Mezzanine.1A-2-1
        team: yes
        untagged_network: 3
        tagged_networks:
          names:
            - range120-125
'''

RETURN = r'''
---
msg:
  description: Status of the overall server interface operation.
  returned: always
  type: str
  sample: Successfully triggered apply server profiles job.
job_id:
  description: Job ID of the task to apply the server interface profiles.
  returned: on applying the Interface profiles
  type: int
  sample: 14123
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
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME, ome_auth_params
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import \
    get_rest_items, strip_substr_dict, job_tracking, apply_diff_key

SERVER_PROFILE = "NetworkService/ServerProfiles('{service_tag}')"
SERVER_INTERFACE = "NetworkService/ServerProfiles('{service_tag}')/ServerInterfaceProfiles"
VLANS = "NetworkConfigurationService/Networks"
DEVICE_URI = "DeviceService/Devices"
APPLY_SERVER_PROFILES = "NetworkService/Actions/NetworkService.ApplyServersInterfaceProfiles"
JOB_URI = "JobService/Jobs({job_id})"
LAST_EXEC = "JobService/Jobs({job_id})/LastExecutionDetail"
APPLY_TRIGGERED = "Successfully initiated the apply server profiles job."
NO_STAG = "No profile found for service tag {service_tag}."
CHANGES_MSG = "Changes found to be applied."
NO_CHANGES_MSG = "No changes found to be applied."
VLAN_NOT_FOUND = "The VLAN with a name {vlan_name} not found."
DUPLICATE_NIC_IDENTIFIED = "Duplicate NIC identfiers provided."
INVALID_UNTAGGED = "The untagged VLAN {id} provided for the NIC ID {nic_id} is not valid."
NW_OVERLAP = "Network profiles of {service_tag} provided for tagged or untagged VLANs of {nic_id} overlaps."
INVALID_DEV_ST = "Unable to complete the operation because the entered target device service tag(s) '{0}' are invalid."
INVALID_DEV_ID = "Unable to complete the operation because the entered target device ids '{0}' are invalid."


def get_valid_service_tags(module, rest_obj):
    service_tags = []
    nic_configs = module.params.get('nic_configuration')
    if nic_configs:
        nic_ids = [(nic.get('nic_identifier')) for nic in nic_configs]
        if len(nic_ids) > len(set(nic_ids)):
            module.exit_json(failed=True, msg=DUPLICATE_NIC_IDENTIFIED)
    dev_map = get_rest_items(rest_obj, uri=DEVICE_URI)
    if module.params.get('device_service_tag'):
        cmp_set = set(module.params.get('device_service_tag')) - set(dict(dev_map).values())
        if cmp_set:
            module.exit_json(failed=True, msg=INVALID_DEV_ST.format(",".join(cmp_set)))
        service_tags = list(set(module.params.get('device_service_tag')))
    if module.params.get('device_id'):
        cmp_set = set(module.params.get('device_id')) - set(dict(dev_map).keys())
        if cmp_set:
            module.exit_json(failed=True, msg=INVALID_DEV_ID.format(",".join(map(str, cmp_set))))
        service_tags = [(dev_map.get(id)) for id in set(module.params.get('device_id'))]
    return service_tags


def _get_profile(module, rest_obj, stag):
    prof = {}
    try:
        resp = rest_obj.invoke_request("GET", SERVER_PROFILE.format(service_tag=stag))
        prof = resp.json_data
    except HTTPError:
        module.exit_json(failed=True, msg=NO_STAG.format(service_tag=stag))
    return prof


def _get_interface(module, rest_obj, stag):
    intrfc_dict = {}
    try:
        intrfc = rest_obj.invoke_request("GET", SERVER_INTERFACE.format(service_tag=stag))
        intrfc_list = intrfc.json_data.get("value")
        intrfc_dict = dict((sip['Id'], {"NativeVLAN": sip['NativeVLAN'],
                                        "NicBonded": sip["NicBonded"],
                                        "Networks": set([(ntw['Id']) for ntw in sip['Networks']])
                                        }) for sip in intrfc_list)
    except HTTPError:
        module.exit_json(failed=True, msg=NO_STAG.format(service_tag=stag))
    return intrfc_dict


def get_server_profiles(module, rest_obj, service_tags):
    profile_dict = {}
    for stag in service_tags:
        prof = _get_profile(module, rest_obj, stag)
        intrfc = _get_interface(module, rest_obj, stag)
        prof["ServerInterfaceProfiles"] = intrfc
        prof = strip_substr_dict(prof)
        profile_dict[stag] = prof
    return profile_dict


def get_vlan_ids(rest_obj):
    resp = rest_obj.invoke_request("GET", VLANS)
    vlans = resp.json_data.get('value')
    vlan_map = {}
    natives = {}
    for vlan in vlans:
        vlan_map[vlan['Name']] = vlan['Id']
        if vlan['VlanMaximum'] == vlan['VlanMinimum']:
            natives[vlan['VlanMaximum']] = vlan['Id']
    natives.update({0: 0})
    return vlan_map, natives


def compare_profile(template, profile):
    diff = 0
    diff = diff + apply_diff_key(template, profile, ["BondingTechnology"])
    # bond_tex = profile["BondingTechnology"]
    # ignore_bond = 0 if profile['BondingTechnology'] == 'LACP' else -1
    sip = profile.get('ServerInterfaceProfiles')
    for nic, ntw in sip.items():
        tmp = template.get(nic, {})
        diff = diff + apply_diff_key(tmp, ntw, ["NativeVLAN"])
        diff = diff + apply_diff_key(tmp, ntw, ["NicBonded"])
        untags = ntw.get("Networks")
        s = set(untags) | set(tmp.get('present', set()))
        s = s - set(tmp.get('absent', set()))
        if s.symmetric_difference(set(untags)):
            ntw["Networks"] = s
            diff = diff + 1
    return diff


def get_template(module, vlan_dict, natives):
    template = {"ServerInterfaceProfiles": {}}
    mparams = module.params
    ignore_teaming = True
    if mparams.get('nic_teaming'):
        template['BondingTechnology'] = mparams.get('nic_teaming')
        if mparams.get('nic_teaming') != "LACP":
            ignore_teaming = False
    if mparams.get('nic_configuration'):
        for nic in mparams.get('nic_configuration'):
            nic_data = {}
            if nic.get('team') is not None and ignore_teaming:
                nic_data['NicBonded'] = nic.get('team')  # if ignore_teaming else False
            ntvlan = nic.get('untagged_network')
            if ntvlan is not None:
                if ntvlan not in natives:
                    module.exit_json(failed=True, msg=INVALID_UNTAGGED.format(id=ntvlan, nic_id=nic['nic_identifier']),
                                     natives=natives)
                nic_data['NativeVLAN'] = ntvlan
            if nic.get('tagged_networks'):
                tg = nic.get('tagged_networks')
                nic_data[tg.get('state')] = set()
                for vlan_name in tg.get('names'):
                    if vlan_name in vlan_dict:
                        nic_data[tg.get('state')].add(vlan_dict[vlan_name])
                    else:
                        module.exit_json(failed=True, msg=VLAN_NOT_FOUND.format(vlan_name=vlan_name))
            template[nic['nic_identifier']] = nic_data
    return template


def get_payload(module, rest_obj, profile_dict):
    vlan_dict, natives = get_vlan_ids(rest_obj)
    template = get_template(module, vlan_dict, natives)
    diff = 0
    payload = []
    for stag, prof in profile_dict.items():
        df = compare_profile(template, prof)
        if df:
            sip_list = []
            for k, v in prof["ServerInterfaceProfiles"].items():
                if natives.get(v['NativeVLAN']) in set(v['Networks']):
                    module.exit_json(failed=True, msg=NW_OVERLAP.format(service_tag=stag, nic_id=k))
                sips = {"Id": k, "NativeVLAN": v['NativeVLAN'], "NicBonded": v["NicBonded"],
                        "Networks": [({'Id': ntw}) for ntw in v['Networks']]}
                sip_list.append(sips)
            prof["ServerInterfaceProfiles"] = sip_list
            payload.append(prof)
        diff = diff + df
    if not diff:
        module.exit_json(msg=NO_CHANGES_MSG)
    if module.check_mode:
        module.exit_json(msg=CHANGES_MSG, changed=True)  # , payload=payload)
    return payload


def handle_job(module, rest_obj, job_id):
    if module.params.get("job_wait"):
        job_failed, msg, job_dict, wait_time = job_tracking(
            rest_obj, JOB_URI.format(job_id=job_id), max_job_wait_sec=module.params.get('job_wait_timeout'))
        try:
            job_resp = rest_obj.invoke_request('GET', LAST_EXEC.format(job_id=job_id))
            msg = job_resp.json_data.get("Value")
            msg = msg.replace('\n', ' ')
        except Exception:
            msg = job_dict.get('JobDescription', msg)
        module.exit_json(failed=job_failed, msg=msg, job_id=job_id, changed=True)
    else:
        module.exit_json(changed=True, msg=APPLY_TRIGGERED, job_id=job_id)


def main():
    specs = {"device_id": {"type": 'list', "elements": 'int'},
             "device_service_tag": {"type": 'list', "elements": 'str'},
             "nic_teaming": {"choices": ['LACP', 'NoTeaming', 'Other']},
             "nic_configuration": {
                 "type": 'list', "elements": 'dict',
                 "options": {
                     "nic_identifier": {"type": 'str', "required": True},
                     "team": {"type": 'bool'},
                     "untagged_network": {"type": 'int'},
                     "tagged_networks": {
                         "type": 'dict', "options": {
                             "state": {"choices": ['present', 'absent'], "default": 'present'},
                             "names": {"type": 'list', "elements": 'str', 'required': True}
                         },
                     }
                 }},
             "job_wait": {"type": 'bool', "default": True},
             "job_wait_timeout": {"type": 'int', "default": 120}}
    specs.update(ome_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        mutually_exclusive=[
            ('device_id', 'device_service_tag',)],
        required_one_of=[('device_id', 'device_service_tag',),
                         ('nic_teaming', 'nic_configuration')],
        supports_check_mode=True)
    try:
        with RestOME(module.params, req_session=True) as rest_obj:
            service_tags = get_valid_service_tags(module, rest_obj)
            profiles = get_server_profiles(module, rest_obj, service_tags)
            apply_data = get_payload(module, rest_obj, profiles)
            resp = rest_obj.invoke_request("POST", APPLY_SERVER_PROFILES, data=apply_data)
            jobid = resp.json_data.get("JobId")
            handle_job(module, rest_obj, jobid)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, TypeError, SSLError, ConnectionError, SSLValidationError, OSError) as err:
        module.fail_json(msg=str(err))


if __name__ == '__main__':
    main()
