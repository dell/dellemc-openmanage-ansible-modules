# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.2.0
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
extends_documentation_fragment:
  - dellemc.openmanage.ome_auth_options
options:
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

EXAMPLES = """
---
# To retrieve all the groups host details.
plugin: dellemc.openmanage.ome_inventory
hostname: "192.168.0.1"
username: username
password: password

# To retrieve specific group host details.
plugin: dellemc.openmanage.ome_inventory
hostname: "192.168.0.1"
username: username
password: password
ome_group_name: group_name

# To set host variables to specific group host.
plugin: dellemc.openmanage.ome_inventory
hostname: "192.168.0.1"
username: username
password: password
ome_group_name: group_name
host_vars:
  idrac_user: username
  idrac_password: password

# To set host variables and multiple group variables.
plugin: dellemc.openmanage.ome_inventory
hostname: "192.168.0.1"
username: username
password: password
host_vars:
  idrac_user: username
  idrac_password: password
group_vars:
  group_name:
    attribute: value
  group_name_one:
    new_attribute: new_value
"""

from ansible.plugins.inventory import BaseInventoryPlugin
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME

GROUP_API = "GroupService/Groups"


class InventoryModule(BaseInventoryPlugin):

    NAME = "dellemc.openmanage.ome_inventory"

    def __init__(self):
        super(InventoryModule, self).__init__()
        self.config = None

    def _get_connection_resp(self):
        port = self.config.get("port") if "port" in self.config else 443
        validate_certs = self.config.get("validate_certs") if "validate_certs" in self.config else False
        module_params = {"hostname": self.config.get("hostname"), "username": self.config.get("username"),
                         "password": self.config.get("password"), "port": port, "validate_certs": validate_certs}
        if "ca_path" in self.config:
            module_params.update({"ca_path": self.config.get("ca_path")})
        with RestOME(module_params, req_session=False) as ome:
            resp = ome.invoke_request("GET", GROUP_API)
        return resp.json_data

    def _set_host_vars(self, host):
        self.inventory.set_variable(host, "idrac_ip", host)
        self.inventory.set_variable(host, "baseuri", host)
        self.inventory.set_variable(host, "hostname", host)
        if "host_vars" in self.config:
            host_vars = self.config.get("host_vars")
            for key, val in dict(host_vars).items():
                self.inventory.set_variable(host, key, val)

    def _set_group_vars(self, group):
        self.inventory.add_group(group)
        if "group_vars" in self.config:
            group_vars = self.config.get("group_vars")
            if group in dict(group_vars):
                for key, val in dict(dict(group_vars)[group]).items():
                    self.inventory.set_variable(group, key, val)

    def _get_all_devices(self, device_uri):
        device_host = []
        device_host_uri = device_uri.strip("/api/")
        port = self.config.get("port") if "port" in self.config else 443
        validate_certs = self.config.get("validate_certs") if "validate_certs" in self.config else False
        module_params = {"hostname": self.config.get("hostname"), "username": self.config.get("username"),
                         "password": self.config.get("password"), "port": port, "validate_certs": validate_certs}
        if "ca_path" in self.config:
            module_params.update({"ca_path": self.config.get("ca_path")})
        with RestOME(module_params, req_session=False) as ome:
            device_resp = ome.invoke_request("GET", device_host_uri)
            device_data = device_resp.json_data.get("value")
            if device_data is not None:
                for mgmt in device_data:
                    if len(mgmt["DeviceManagement"]) == 1:
                        if mgmt["DeviceManagement"][0]["NetworkAddress"].startswith("["):
                            device_host.append(mgmt["DeviceManagement"][0]["NetworkAddress"][1:-1])
                        else:
                            device_host.append(mgmt["DeviceManagement"][0]["NetworkAddress"])
                    elif len(mgmt["DeviceManagement"]) == 2:
                        if mgmt["DeviceManagement"][0]["NetworkAddress"].startswith("["):
                            device_host.append(mgmt["DeviceManagement"][1]["NetworkAddress"])
                        else:
                            device_host.append(mgmt["DeviceManagement"][0]["NetworkAddress"])
        return device_host

    def _set_child_group(self, group_data):
        port = self.config.get("port") if "port" in self.config else 443
        validate_certs = self.config.get("validate_certs") if "validate_certs" in self.config else False
        module_params = {"hostname": self.config.get("hostname"), "username": self.config.get("username"),
                         "password": self.config.get("password"), "port": port, "validate_certs": validate_certs}
        if "ca_path" in self.config:
            module_params.update({"ca_path": self.config.get("ca_path")})
        with RestOME(module_params, req_session=False) as ome:
            for gdata in group_data:
                group_name = gdata["Name"]
                subgroup_uri = gdata["SubGroups@odata.navigationLink"].strip("/api/")
                sub_group = ome.invoke_request("GET", subgroup_uri)
                gdata = sub_group.json_data.get("value")
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
            device_ip = self._get_all_devices(gdata["Devices@odata.navigationLink"])
            for hst in device_ip:
                self.inventory.add_host(host=hst, group=gdata["Name"])
                self._set_host_vars(hst)
        self._set_child_group(group_data)

    def _populate(self, inventory_data):
        group_data = inventory_data.get("value")
        group_name = str(self.config.get("ome_group_name")) if "ome_group_name" in self.config else None
        if group_name is not None:
            group_data = list(filter(lambda d: d.get("Name").lower() in [group_name.lower()], group_data))
        elif group_name is None:
            group_data = list(filter(lambda d: d.get("Name") in ["All Devices"], group_data))
        self._add_group_data(group_data)

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        self.config = self._read_config_data(path)
        resp_data = self._get_connection_resp()
        self._populate(resp_data)
