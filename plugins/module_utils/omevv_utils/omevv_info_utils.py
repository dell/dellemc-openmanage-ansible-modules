# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 9.10.0
# Copyright (C) 2024-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:

#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.

#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

VCENTER_INFO_URI = "/Consoles"
CLUSTER_INFO_URI = "/Consoles/{uuid}/Clusters"
GROUP_ID_CLUSTER_INFO_URI = "/Consoles/{uuid}/Groups/getGroupsForClusters"
MANAGED_HOST_INFO_URI = "/Consoles/{uuid}/ManagedHosts"
CLUSTER_MANAGED_HOST_INFO_URI = "/Consoles/{uuid}/Groups/{groupId}/ManagedHosts"
HOST_FIRMWARE_DRIFT_INFO_URI = "/Consoles/{uuid}/Groups/{groupId}/ManagedHosts/{hostId}/FirmwareDriftReport"
CLUSTER_FIRMWARE_DRIFT_INFO_URI = "/Consoles/{uuid}/Groups/{groupId}/FirmwareDriftReport"


class OMEVVInfo:
    def __init__(self, omevv_obj):
        self.omevv_obj = omevv_obj

    def get_vcenter_info(self, vcenter_id=None):
        """
        Retrieves the vCenter information.
        Parameters:
            vcenter_id (str, optional): The hostname of the vCenter. If provided, retrieves the information for the specified vCenter.
        Returns:
            list: A list of vCenter information when `vcenter_id` is not provided
            dict: A dict containing the information for the specified vCenter when `vcenter_id` is provided. If no match is found, the empty dict is returned.
        """
        resp = self.omevv_obj.invoke_request('GET', VCENTER_INFO_URI)
        vcenter_info = []
        if resp.success:
            vcenter_info = resp.json_data
            if vcenter_id and vcenter_info:
                for each_vcenter in vcenter_info:
                    if each_vcenter.get('consoleAddress') == vcenter_id:
                        return each_vcenter
                return {}
        return vcenter_info

    def get_cluster_info(self, uuid, cluster_name=""):
        uri = CLUSTER_INFO_URI.format(uuid=uuid)
        resp = self.omevv_obj.invoke_request('GET', uri)
        cluster_info = []
        if resp.success:
            cluster_info = resp.json_data
            if cluster_name and cluster_info:
                for each_cluster in cluster_info:
                    if each_cluster.get('name') == cluster_name:
                        return each_cluster
                return {}
        return cluster_info

    def get_group_id_of_cluster(self, uuid, cluster_name):
        group_id = -1
        uri = GROUP_ID_CLUSTER_INFO_URI.format(uuid=uuid)
        cluster_info = self.get_cluster_info(uuid, cluster_name)
        if cluster_info:
            entity_id = cluster_info.get('entityId')
            payload = {"clustIds": [entity_id]}
            resp = self.omevv_obj.invoke_request('POST', uri, data=payload)
            if resp.success:
                group_id = resp.json_data[0].get('groupId')
        return group_id

    def get_managed_host_details(self, uuid, servicetags=None, hostnames=None):
        servicetags = [] if servicetags is None else servicetags
        hostnames = [] if hostnames is None else hostnames
        uri = MANAGED_HOST_INFO_URI.format(uuid=uuid)
        resp = self.omevv_obj.invoke_request('GET', uri)
        managed_hosts = resp.json_data
        if not (servicetags or hostnames):
            return managed_hosts, {}

        if servicetags:
            managed_hosts = [
                host for host in managed_hosts
                if host.get("serviceTag") in servicetags
            ]

        if hostnames:
            managed_hosts = [
                host for host in managed_hosts
                if host.get("hostName") in hostnames
            ]

        invalid_result = {
            "servicetags": [
                tag for tag in servicetags
                if not any(host.get("serviceTag") == tag for host in managed_hosts)
            ],
            "hostnames": [
                name for name in hostnames
                if not any(host.get("hostName") == name for host in managed_hosts)
            ]
        }
        return managed_hosts, invalid_result

    def get_firmware_drift_info_for_single_host(self, uuid, groupid, hostid):
        result = []
        uri = HOST_FIRMWARE_DRIFT_INFO_URI.format(uuid=uuid,
                                                  groupId=str(groupid),
                                                  hostId=str(hostid))
        resp = self.omevv_obj.invoke_request('GET', uri)
        if resp.success:
            result = resp.json_data
        return result

    def get_firmware_drift_info_for_multiple_host(self, uuid, groupid, hostidlist):
        result = []
        for each_host in hostidlist:
            output = self.get_firmware_drift_info_for_single_host(uuid, groupid, each_host)
            result.append(output)
        return result

    def get_firmware_drift_info_for_single_cluster(self, uuid, groupid):
        result = []
        uri = CLUSTER_FIRMWARE_DRIFT_INFO_URI.format(uuid=uuid,
                                                     groupId=str(groupid))
        resp = self.omevv_obj.invoke_request('GET', uri)
        if resp.success:
            result = resp.json_data
        return result

    def get_firmware_drift_info_for_multiple_cluster(self, uuid, groupidlist):
        result = []
        for each_group in groupidlist:
            output = self.get_firmware_drift_info_for_single_cluster(uuid=uuid,
                                                                     groupid=each_group)
            result.append(output)
        return result

    def get_cluster_name(self, uuid, host_id):
        uri = MANAGED_HOST_INFO_URI.format(uuid=uuid)
        resp = self.omevv_obj.invoke_request('GET', uri)
        managed_hosts = resp.json_data
        for host in managed_hosts:
            if host['id'] == host_id:
                return host['clusterName']
        return ""

    def get_host_id_either_host_or_service_tag(self, uuid, hostname=None, servicetag=None):
        uri = MANAGED_HOST_INFO_URI.format(uuid=uuid)
        resp = self.omevv_obj.invoke_request('GET', uri)
        managed_hosts = resp.json_data
        for host in managed_hosts:
            if hostname and host['hostName'] == hostname:
                return host['id'], host['serviceTag']
            if servicetag and host['serviceTag'] == servicetag:
                return host['id'], host['serviceTag']
        return None, None

    def get_cluster_managed_host_details(self, uuid, cluster_group_id):
        uri = CLUSTER_MANAGED_HOST_INFO_URI.format(uuid=uuid, groupId=cluster_group_id)
        resp = self.omevv_obj.invoke_request('GET', uri)
        managed_hosts = resp.json_data

        host_ids = []
        host_service_tags = []

        for host in managed_hosts:
            host_ids.append(host.get('id'))
            host_service_tags.append(host.get('serviceTag'))

        return host_ids, host_service_tags
