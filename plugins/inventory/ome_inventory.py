# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.4.0
# Copyright (C) 2022-2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = """
---
name: ome_inventory
short_description: Group inventory plugin on OpenManage Enterprise.
description: This plugin allows to retrieve inventory hosts from groups on OpenManage Enterprise.
version_added: "7.1.0"
options:
  hostname:
    description:
    - OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.
    - If the value is not specified in the task, the value of environment variable C(OME_HOSTNAME) will be used instead.
    env:
     - name: OME_HOSTNAME
    type: str
    required: true
  username:
    description:
    - OpenManage Enterprise or OpenManage Enterprise Modular username.
    - If the value is not specified in the task, the value of environment variable C(OME_USERNAME) will be used instead.
    env:
     - name: OME_USERNAME
    type: str
    required: true
  password:
    description:
    - OpenManage Enterprise or OpenManage Enterprise Modular password.
    - If the value is not specified in the task, the value of environment variable C(OME_PASSWORD) will be used instead.
    env:
    - name: OME_PASSWORD
    type: str
    required: true
  port:
    description:
    - OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.
    - If the value is not specified in the task, the value of environment variable C(OME_PORT) will be used instead.
    type: int
    default: 443
  validate_certs:
    description:
    - If C(false), the SSL certificates will not be validated.
    - Configure C(false) only on personally controlled sites where self-signed certificates are used.
    - Prior to collection version C(5.0.0), the I(validate_certs) is C(false) by default.
    type: bool
    default: true
  ca_path:
    description:
    - The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.
    type: path
  timeout:
    description: The socket level timeout in seconds.
    type: int
    default: 30
  ome_group_name:
    description: Group name.
    type: str
    required: false
  host_vars:
    description: To include host related variables in the inventory source.
    type: dict
    required: false
  group_vars:
    description: To include group variables in the inventory source.
    type: dict
    required: false
requirements:
  - "python >= 3.9.6"
author:
  - "Felix Stephen (@felixs88)"
notes:
  - Run this plugin on a system that has direct access to Dell OpenManage Enterprise.
"""

from ansible.plugins.inventory import BaseInventoryPlugin
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import get_all_data_with_pagination

GROUP_API = "GroupService/Groups"


class InventoryModule(BaseInventoryPlugin):

    NAME = "dellemc.openmanage.ome_inventory"

    def __init__(self):
        super(InventoryModule, self).__init__()
        self.config = None

    def _get_connection_resp(self):
        port = self.get_option("port") if "port" in self.config else 443
        validate_certs = self.get_option("validate_certs") if "validate_certs" in self.config else False
        module_params = {"hostname": self.get_option("hostname"), "username": self.get_option("username"),
                         "password": self.get_option("password"), "port": port, "validate_certs": validate_certs}
        if "ca_path" in self.config:
            module_params.update({"ca_path": self.get_option("ca_path")})
        with RestOME(module_params, req_session=False) as ome:
            all_group_data = get_all_data_with_pagination(ome, GROUP_API)
        return all_group_data

    def _set_host_vars(self, host):
        self.inventory.set_variable(host, "idrac_ip", host)
        self.inventory.set_variable(host, "baseuri", host)
        self.inventory.set_variable(host, "hostname", host)
        if "host_vars" in self.config:
            host_vars = self.get_option("host_vars")
            for key, val in dict(host_vars).items():
                self.inventory.set_variable(host, key, val)

    def _set_group_vars(self, group):
        self.inventory.add_group(group)
        if "group_vars" in self.config:
            group_vars = self.get_option("group_vars")
            if group in dict(group_vars):
                for key, val in dict(dict(group_vars)[group]).items():
                    self.inventory.set_variable(group, key, val)

    def _get_device_host(self, mgmt):
        if len(mgmt["DeviceManagement"]) == 1 and mgmt["DeviceManagement"][0]["NetworkAddress"].startswith("["):
            dev_host = mgmt["DeviceManagement"][0]["NetworkAddress"][1:-1]
        elif len(mgmt["DeviceManagement"]) == 2 and mgmt["DeviceManagement"][0]["NetworkAddress"].startswith("["):
            dev_host = mgmt["DeviceManagement"][1]["NetworkAddress"]
        else:
            dev_host = mgmt["DeviceManagement"][0]["NetworkAddress"]
        return dev_host

    def _get_all_devices(self, device_uri):
        device_host = []
        device_host_uri = device_uri.strip("/api/")
        port = self.get_option("port") if "port" in self.config else 443
        validate_certs = self.get_option("validate_certs") if "validate_certs" in self.config else False
        module_params = {
            "hostname": self.get_option("hostname"),
            "username": self.get_option("username"),
            "password": self.get_option("password"),
            "port": port,
            "validate_certs": validate_certs}
        if "ca_path" in self.config:
            module_params.update({"ca_path": self.get_option("ca_path")})
        with RestOME(module_params, req_session=False) as ome:
            device_resp = get_all_data_with_pagination(ome, device_host_uri)
            device_data = device_resp.get("report_list", [])
            if device_data is not None:
                for mgmt in device_data:
                    if (len(mgmt["DeviceManagement"]) != 0):
                        device_host.append(self._get_device_host(mgmt))
        return device_host

    def _set_child_group(self, group_data):
        port = self.get_option("port") if "port" in self.config else 443
        validate_certs = self.get_option("validate_certs") if "validate_certs" in self.config else False
        module_params = {"hostname": self.get_option("hostname"), "username": self.get_option("username"),
                         "password": self.get_option("password"), "port": port, "validate_certs": validate_certs}
        if "ca_path" in self.config:
            module_params.update({"ca_path": self.get_option("ca_path")})
        with RestOME(module_params, req_session=False) as ome:
            for gdata in group_data:
                group_name = gdata["Name"]
                subgroup_uri = gdata["SubGroups@odata.navigationLink"].strip("/api/")
                sub_group = get_all_data_with_pagination(ome, subgroup_uri)
                gdata = sub_group.get("report_list", [])
                if gdata:
                    self._add_group_data(gdata)
                    self._add_child_group_data(group_name, gdata)

    def _add_child_group_data(self, group_name, gdata):
        for child_name in gdata:
            self.inventory.add_child(group_name, child_name["Name"])

    def _add_group_data(self, group_data):
        visible_gdata = list(filter(lambda d: d.get("Visible") in [False], group_data))
        if visible_gdata:
            for gp in visible_gdata:
                group_data.remove(gp)
        for gdata in group_data:
            self._set_group_vars(gdata["Name"])
            device_ip = self._get_all_devices(gdata["AllLeafDevices@odata.navigationLink"])
            for hst in device_ip:
                self.inventory.add_host(host=hst, group=gdata["Name"])
                self._set_host_vars(hst)
        self._set_child_group(group_data)

    def _populate(self, all_group_data):
        group_data = all_group_data.get("report_list", [])
        group_name = str(self.get_option("ome_group_name")) if "ome_group_name" in self.config else None
        if group_name is not None:
            group_data = list(filter(lambda d: d.get("Name").lower() in [group_name.lower()], group_data))
        elif group_name is None:
            group_data = list(filter(lambda d: d.get("Name") in ["All Devices"], group_data))
        self._add_group_data(group_data)

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        self.config = self._read_config_data(path)
        all_group_data = self._get_connection_resp()
        self._populate(all_group_data)
