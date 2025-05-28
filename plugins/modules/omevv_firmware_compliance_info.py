#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.9.0
# Copyright (C) 2024-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: omevv_firmware_compliance_info
short_description: Retrieve firmware compliance report.
version_added: "9.9.0"
description:
  - This module allows you to retrieve firmware compliance reports of all the
    hosts of the cluster, a specific host of the cluster, or multiple clusters.
extends_documentation_fragment:
  - dellemc.openmanage.omevv_auth_options
options:
  clusters:
    description:
      - Cluster details to retrieve the firmware compliance report.
    type: list
    elements: dict
    suboptions:
      cluster_name:
        description:
          - Cluster name of the hosts for which the firmware compliance report should be retrieved.
          - If I(servicetags) or I(hosts) is provided, then the firmware compliance report of only the specified hosts
            is retrieved and displayed.
        required: true
        type: str
      servicetags:
        description:
          - The service tag of the hosts for which the firmware compliance
            reports must be retrieved.
        type: list
        elements: str
      hosts:
        description:
          - The IP address or hostname of the hosts for which the firmware
            compliance reports must be retrieved.
        type: list
        elements: str
requirements:
  - "python >= 3.9.6"
author:
  - "Abhishek Sinha(@ABHISHEK-SINHA10)"
attributes:
  check_mode:
    description: Runs task to validate without performing action on the target machine.
    support: full
  diff_mode:
    description: Runs the task to report the changes that are made or the changes that must be applied.
    support: full
notes:
    - Run this module from a system that has direct access to Dell OpenManage Enterprise.
"""

EXAMPLES = r"""
---
- name: Retrieve a firmware compliance report of all the clusters
  dellemc.openmanage.omevv_firmware_compliance_info:
    hostname: "192.168.0.1"
    vcenter_uuid: "xxxxx"
    vcenter_username: "username"
    vcenter_password: "password"
    ca_path: "path/to/ca_file"

- name: Retrieve a firmware compliance report of all the hosts in a specific cluster
  dellemc.openmanage.omevv_firmware_compliance_info:
    hostname: "192.168.0.1"
    vcenter_uuid: "xxxxx"
    vcenter_username: "username"
    vcenter_password: "password"
    ca_path: "path/to/ca_file"
    clusters:
      - cluster_name: cluster_a

- name: Retrieve a firmware compliance report of specific hosts in the cluster
  dellemc.openmanage.omevv_firmware_compliance_info:
    hostname: "192.168.0.1"
    vcenter_uuid: "xxxxx"
    vcenter_username: "username"
    vcenter_password: "password"
    ca_path: "path/to/ca_file"
    clusters:
      - cluster_name: cluster_a
        servicetags:
          - SVCTAG1
          - SVCTAG2
        hosts:
          - host1
          - xx.xx.xx.xx

- name: Retrieve a firmware compliance report of multiple clusters
  dellemc.openmanage.omevv_firmware_compliance_info:
    hostname: "192.168.0.1"
    vcenter_uuid: "xxxxx"
    vcenter_username: "username"
    vcenter_password: "password"
    ca_path: "path/to/ca_file"
    clusters:
      - cluster_name: cluster_a
      - cluster_name: cluster_b
"""

RETURN = r'''
---
msg:
  type: str
  description: Retrive the firmware compliance report.
  returned: always
  sample: "Successfully fetched the firmware compliance report."
firmware_compliance_info:
  description: Details of the compliance report.
  returned: on HTTP error
  type: list
  elements: dict
  sample:
    [{
      "complianceStatus": "NonCompliant",
      "cluster": "cluster_a",
      "hostComplianceReports": [
    {
      "hostId": 1002,
      "hostAddress": "XX.XX.XX.XX",
      "serviceTag": "SVCTAG",
      "deviceModel": "PowerEdge R660xs",
      "complianceStatus": "WARNING",
      "componentCompliances": [
        {
          "driftStatus": "NonCompliant",
          "componentName": "Enterprise UEFI Diagnostics",
          "currentValue": "4303A15",
          "baselineValue": "4303A19",
          "criticality": "Optional",
          "updateAction": "UPGRADE",
          "sourceName": "DCIM:INSTALLED#802__Diagnostics.Embedded.1:LC.Embedded.1",
          "complianceStatus": "WARNING",
          "rebootRequired": false
        }]
      }]
    }]
'''
import json
from copy import deepcopy
from urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv import RestOMEVV, OMEVVAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv_utils.omevv_info_utils import OMEVVInfo

PARTIAL_HOST_WARN_MSG = "Unable to fetch the firmware compliance report of few of the host(s) - {0}"
PARTIAL_CLUSTER_WARN_MSG = "Unable to fetch the firmware compliance report of few of the cluster(s) - {0}"
CLUSTER_NOT_VALID_MSG = "Unable to complete the operation because the {cluster_name} is not valid."
ALL_HOST_CLUSTER_NOT_VALID_MSG = "Unable to complete the operation because none of clusters and hosts are valid."
SUCCESS_FETCHED_MSG = "Successfully fetched the firmware compliance report."


class FirmwareComplianceInfo:

    def __init__(self, module, rest_obj):
        self.module = module
        self.info = OMEVVInfo(rest_obj)

    def extract_host_id(self, svctag, hostname, cluster_name):
        host_id = []
        uuid = self.module.params.get("vcenter_uuid")
        managed_hosts, invalid_result = self.info.get_managed_host_details(uuid=uuid,
                                                                           servicetags=svctag,
                                                                           hostnames=hostname)
        if invalid_result:
            hostnames = invalid_result["hostnames"]
            servicetags = invalid_result["servicetags"]
            if hostnames or servicetags:
                host_invalid_list = ', '.join(hostnames + servicetags)
                self.module.warn(PARTIAL_HOST_WARN_MSG.format(host_invalid_list))

        for each_host in managed_hosts:
            if each_host.get("clusterName") == cluster_name:
                host_id.append(each_host.get('id'))
        return host_id

    def get_hostid_groupid_and_cluster_name(self):
        flatten_data = {}
        clusters = self.module.params.get("clusters")
        uuid = self.module.params.get("vcenter_uuid")
        invalid_cluster_name = []
        if clusters:
            for cluster in clusters:
                cluster_name = cluster.get("cluster_name")
                svctag = cluster.get("servicetags")
                hostname = cluster.get("hosts")
                group_id = self.info.get_group_id_of_cluster(uuid, cluster_name)
                if group_id == -1:
                    invalid_cluster_name.append(cluster_name)
                    continue
                host_id_list = self.extract_host_id(svctag, hostname, cluster_name)
                for each_host_id in host_id_list:
                    if cluster_name not in flatten_data:
                        flatten_data[cluster_name] = {"hostId": [each_host_id],
                                                      "groupId": group_id}
                    else:
                        flatten_data[cluster_name]["hostId"].append(each_host_id)
        return flatten_data, invalid_cluster_name

    def execute(self):
        output = None
        uuid = self.module.params.get("vcenter_uuid")
        clusters = self.module.params.get("clusters")
        flattend_data, invalid_cluster_name = self.get_hostid_groupid_and_cluster_name()
        if invalid_cluster_name:
            inv_cls = ', '.join(invalid_cluster_name)
            self.module.warn(PARTIAL_CLUSTER_WARN_MSG.format(inv_cls))
        if not flattend_data:
            if clusters is None:
                output = self.get_all_cluster_drift_info(uuid)
        else:
            output = self.get_host_drift_info(uuid, flattend_data)
        if output:
            self.module.exit_json(msg=SUCCESS_FETCHED_MSG, firmware_compliance_info=output)
        else:
            self.module.exit_json(msg=ALL_HOST_CLUSTER_NOT_VALID_MSG, skipped=True)

    def get_host_drift_info(self, uuid, flattend_data):
        output = []
        for each_cluster, each_value in flattend_data.items():
            try:
                drift_info = deepcopy(self.info.get_firmware_drift_info_for_multiple_host(uuid=uuid,
                                                                                          groupid=each_value["groupId"],
                                                                                          hostidlist=each_value["hostId"]))
                drift_info[0]["cluster"] = each_cluster
                output.append(drift_info[0])
            except HTTPError as err:
                error_info = json.load(err)
                msg = error_info.get("message")
                self.module.warn(msg)
        return output

    def get_all_cluster_drift_info(self, uuid):
        output = []
        all_cluster = self.info.get_cluster_info(uuid=uuid)
        cluster_names = [each_cluster.get("name") for each_cluster in all_cluster]
        group_id_cluster_name = [{"groupId": self.info.get_group_id_of_cluster(uuid, each_name),
                                  "cluster_name": each_name} for each_name in cluster_names]
        for each_group in group_id_cluster_name:
            try:
                drift_info = deepcopy(self.info.get_firmware_drift_info_for_single_cluster(uuid=uuid,
                                                                                           groupid=each_group["groupId"]))
                drift_info["cluster"] = each_group["cluster_name"]
                output.append(drift_info)
            except HTTPError as err:
                error_info = json.load(err)
                msg = error_info.get("message")
                self.module.warn(msg)
        return output


def main():
    argument_spec = {
        "clusters": {"type": "list", "elements": "dict",
                     "options": {"cluster_name": {"type": "str", "required": True},
                                 "servicetags": {"type": "list", "elements": "str"},
                                 "hosts": {"type": "list", "elements": "str"}}}}

    module = OMEVVAnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True)
    try:
        with RestOMEVV(module.params) as rest_obj:
            obj = FirmwareComplianceInfo(module, rest_obj)
            obj.execute()
    except HTTPError as err:
        msg = json.load(err) if isinstance(err, dict) else err
        module.exit_json(msg=str(msg), failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (IOError, ValueError, TypeError, ConnectionError,
            AttributeError, IndexError, KeyError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
