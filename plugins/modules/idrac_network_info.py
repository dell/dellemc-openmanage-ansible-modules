# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.0
# Copyright (C) 2026 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""Ansible module for discovering network device functions (NICs) on iDRAC.

This module discovers all network device functions on an iDRAC via the
chassis-scoped Redfish NetworkAdapters endpoint, returning rich metadata
per NIC including ID, link status, MAC address, NIC type, speed capability,
and media type.
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_network_info
short_description: Discover network device functions (NICs) on iDRAC
version_added: "10.0.0"
description:
    - Discover all network device functions (NICs) on an iDRAC via the
      chassis-scoped Redfish NetworkAdapters endpoint.
    - Returns rich metadata per NIC including ID, link status, MAC address,
      NIC type, speed capability, and media type.
    - Supports both iDRAC9 (16G) and iDRAC10 (17G) via dynamic URI resolution.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options

options:
    force_refresh:
        description: Force refresh of NIC discovery results, bypassing the in-memory cache.
        type: bool
        required: false
        default: false

requirements:
    - "python >= 3.9.6"
author: "Mangirish Kenkare(@MangirishK)"
notes:
    - "Run this module from a system that has direct access to Dell iDRAC."
    - "This module supports both IPv4 and IPv6 address for I(idrac_ip)."
    - "This module is read-only and always returns changed=false."
"""

EXAMPLES = """
---
- name: Discover all NICs on iDRAC
  dellemc.openmanage.idrac_network_info:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"

- name: Discover NICs with forced cache refresh
  dellemc.openmanage.idrac_network_info:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    force_refresh: true

- name: Discover NICs and use results in subsequent tasks
  hosts: idrac_hosts
  tasks:
    - name: Get all NICs
      dellemc.openmanage.idrac_network_info:
        idrac_ip: "{{ idrac_ip }}"
        idrac_user: "{{ idrac_user }}"
        idrac_password: "{{ idrac_password }}"
      register: nic_result

    - name: Display NIC IDs
      ansible.builtin.debug:
        msg: "Found NIC: {{ item.id }}"
      loop: "{{ nic_result.network_device_functions }}"
"""

RETURN = r'''
---
msg:
  description: Overall status message.
  returned: always
  type: str
  sample: "Successfully discovered network device functions."
network_device_functions:
  type: list
  description: List of network device functions with rich metadata.
  returned: success
  sample: [
    {
      "id": "NIC.Embedded.1-1-1",
      "net_dev_func_type": "Ethernet",
      "mac_address": "B0:26:28:E4:95:60",
      "link_status": "LinkUp",
      "device_description": "Embedded NIC 1 Port 1 Partition 1",
      "link_speed": "10000 Mbps",
      "media_type": "Base-T"
    }
  ]
idrac_generation:
  type: int
  description: PowerEdge server generation (14G-16G for iDRAC9, 17G+ for iDRAC10).
  returned: success
  sample: 16
idrac_firmware_version:
  type: str
  description: iDRAC firmware version.
  returned: success
  sample: "7.30.30.50"
idrac_model:
  type: str
  description: iDRAC model identifier.
  returned: success
  sample: "iDRAC 9"
redfish_error:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
      "code": "Base.1.0.GeneralError",
      "message": "A general error has occurred."
    }
  }
'''

import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import (
    iDRACRedfishAPI, idrac_auth_params
)


# In-memory cache for NIC discovery data
_NIC_CACHE = {}

CHASSIS_URI = "/redfish/v1/Chassis"
ODATA_ID = "@odata.id"
ODATA_NEXT_LINK = "Members@odata.nextLink"


def get_collection_members(idrac, collection_uri):
    """Return all members of a Redfish collection, following nextLink pagination."""
    members = []
    next_uri = collection_uri
    while next_uri:
        resp = idrac.invoke_request(next_uri, 'GET').json_data
        members.extend(resp.get('Members', []))
        next_uri = resp.get(ODATA_NEXT_LINK) or resp.get('@odata.nextLink')
    return members


def get_cache_key(idrac_ip, idrac_port):
    """Generate cache key based on iDRAC IP and port."""
    return f"{idrac_ip}:{idrac_port}"


def get_from_cache(cache_key):
    """Retrieve data from cache if available."""
    return _NIC_CACHE.get(cache_key)


def store_in_cache(cache_key, data):
    """Store data in cache."""
    _NIC_CACHE[cache_key] = data


def _get_network_adapters_uri(idrac, chassis_members):
    """Return the first chassis member that exposes a NetworkAdapters link."""
    for member in chassis_members:
        chassis_uri = member.get(ODATA_ID, '')
        if not chassis_uri:
            continue
        try:
            chassis_detail = idrac.invoke_request(chassis_uri, 'GET').json_data
        except (HTTPError, URLError, ConnectionError, SSLValidationError):
            continue
        network_adapters_link = chassis_detail.get('NetworkAdapters', {}).get(ODATA_ID)
        if network_adapters_link:
            return network_adapters_link
    return None


def _get_ndf_members(idrac, adapter_detail):
    """Return NetworkDeviceFunctions members from inline array or collection link."""
    ndf = adapter_detail.get('NetworkDeviceFunctions')
    if isinstance(ndf, list):
        return ndf
    if isinstance(ndf, dict):
        ndf_link = ndf.get(ODATA_ID)
        if ndf_link:
            return get_collection_members(idrac, ndf_link)
    return []


def discover_network_device_functions(idrac):
    """Discover all network device functions via chassis-scoped NetworkAdapters.

    Walks the Redfish tree:
    /redfish/v1/Chassis/{ChassisId}/NetworkAdapters/{AdapterId}/NetworkDeviceFunctions/{FuncId}

    Returns a list of dicts with rich metadata per NIC.
    """
    network_device_functions = []

    # Find the chassis member that exposes network adapters
    chassis_resp = idrac.invoke_request(CHASSIS_URI, 'GET').json_data
    chassis_members = chassis_resp.get('Members', [])
    network_adapters_link = _get_network_adapters_uri(idrac, chassis_members)
    if not network_adapters_link:
        return network_device_functions

    adapter_members = get_collection_members(idrac, network_adapters_link)

    for adapter_ref in adapter_members:
        adapter_uri = adapter_ref.get(ODATA_ID, '')
        if not adapter_uri:
            continue

        adapter_detail = idrac.invoke_request(adapter_uri, 'GET').json_data

        for ndf_ref in _get_ndf_members(idrac, adapter_detail):
            ndf_uri = ndf_ref.get(ODATA_ID, '')
            if not ndf_uri:
                continue

            ndf_detail = idrac.invoke_request(ndf_uri, 'GET').json_data

            # Extract Dell OEM DellNIC extension for link_status and media metadata
            dell_nic = ndf_detail.get('Oem', {}).get('Dell', {}).get('DellNIC', {})

            func_data = {
                'id': ndf_detail.get('Id', ndf_uri.split('/')[-1]),
                'net_dev_func_type': ndf_detail.get('NetDevFuncType', ''),
                'mac_address': ndf_detail.get('Ethernet', {}).get('MACAddress', ''),
                'link_status': (
                    dell_nic.get('LinkStatus') or
                    ndf_detail.get('Status', {}).get('State', '') or
                    ndf_detail.get('Status', {}).get('Health', '')
                ),
                'device_description': dell_nic.get('DeviceDescription', ''),
                'link_speed': dell_nic.get('LinkSpeed', ''),
                'media_type': dell_nic.get('MediaType', ''),
            }
            network_device_functions.append(func_data)

    return network_device_functions


def main():
    """Main entry point for the idrac_network_info module."""
    argument_spec = idrac_auth_params.copy()
    argument_spec.update({
        'force_refresh': {'type': 'bool', 'required': False, 'default': False},
    })

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        with iDRACRedfishAPI(module.params) as idrac:
            # Fetch server generation info
            generation, firmware_version, hw_model = idrac.get_server_generation

            # Check firmware version requirements
            is_compliant, min_fw_version, error_msg = iDRACRedfishAPI.check_minimum_firmware_requirement(  # pylint: disable=unused-variable
                hw_model, firmware_version
            )
            if not is_compliant:
                module.fail_json(msg=error_msg)

            # Check cache first (unless force_refresh is True)
            force_refresh = module.params.get('force_refresh')
            cache_key = get_cache_key(module.params['idrac_ip'], module.params['idrac_port'])
            cached_data = None

            if not force_refresh:
                cached_data = get_from_cache(cache_key)

            if cached_data:
                network_device_functions = cached_data['network_device_functions']
            else:
                try:
                    network_device_functions = discover_network_device_functions(idrac)
                except HTTPError as e:
                    redfish_error = {}
                    try:
                        redfish_error = json.load(e)
                    except Exception:
                        pass
                    if e.code == 404:
                        module.fail_json(
                            msg="NetworkAdapters endpoint not supported on this firmware. "
                                "Please update iDRAC firmware.",
                            redfish_error=redfish_error
                        )
                    raise

                # Store in cache
                store_in_cache(cache_key, {
                    'network_device_functions': network_device_functions,
                })

            module.exit_json(
                msg="Successfully discovered network device functions.",
                changed=False,
                network_device_functions=network_device_functions,
                idrac_generation=generation,
                idrac_firmware_version=firmware_version,
                idrac_model=hw_model
            )
    except HTTPError as e:
        redfish_error = {}
        try:
            redfish_error = json.load(e)
        except Exception:
            pass
        if e.code in [401, 403]:
            module.fail_json(msg=f"Authentication failed: {e.msg}", redfish_error=redfish_error)
        else:
            module.fail_json(msg=f"HTTP error {e.code}: {e.msg}", redfish_error=redfish_error)
    except SSLValidationError as e:
        module.fail_json(msg=f"SSL validation error: {str(e)}")
    except ConnectionError as e:
        module.fail_json(msg=f"Connection error: {str(e)}")
    except URLError as e:
        module.fail_json(msg=f"Network error: {str(e)}")
    except Exception as e:  # pylint: disable=broad-except
        if type(e).__name__ in ['AnsibleExitJson', 'AnsibleFailJson']:
            raise
        module.fail_json(msg=f"Unexpected error: {str(e)}")


if __name__ == '__main__':
    main()
