# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.0
# Copyright (C) 2026 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""Ansible module for querying iDRAC Network Attribute Registry.

This module queries the Dell OEM DellNetworkAttributes endpoint and
NetworkAttributesRegistry for a specific NIC, returning full attribute
schema with current values. Supports attribute name filtering and
OEM vs. standard attribute classification.
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_network_attributes_info
short_description: Query iDRAC Network Attribute Registry for a specific NIC
version_added: "10.0.0"
description:
    - Query the Dell OEM DellNetworkAttributes endpoint and NetworkAttributesRegistry
      for a specific network device function (NIC).
    - Returns full attribute schema with current values, supporting attribute name
      filtering and OEM vs. standard attribute classification.
    - Supports both iDRAC9 (16G) and iDRAC10 (17G) via dynamic URI resolution.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options

options:
    network_device_function_id:
        description:
            - FQDD of the network device function to query attributes for.
            - "Example: C(NIC.Embedded.1-1-1)."
            - If the specified ID does not exist, the module returns an error
              including a list of valid NIC IDs discovered on the iDRAC.
        type: str
        required: true
    attribute_name:
        description: Pattern to filter attributes by name (supports glob patterns via fnmatch).
        type: str
        required: false
    attribute_source:
        description: Filter attributes by source type.
        type: str
        required: false
        default: 'all'
        choices: ['all', 'oem', 'standard']
    force_refresh:
        description: Force refresh of attribute registry data, bypassing the in-memory cache.
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
    - "Use idrac_network_info to discover valid NIC IDs before calling this module."
"""

EXAMPLES = """
---
- name: Query all network attributes for a specific NIC
  dellemc.openmanage.idrac_network_attributes_info:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    network_device_function_id: "NIC.Embedded.1-1-1"

- name: Filter attributes by glob pattern
  dellemc.openmanage.idrac_network_attributes_info:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_device_function_id: "NIC.Embedded.1-1-1"
    attribute_name: "VLan*"

- name: Query only OEM attributes
  dellemc.openmanage.idrac_network_attributes_info:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_device_function_id: "NIC.Embedded.1-1-1"
    attribute_source: "oem"

- name: Two-step workflow - discover NICs then query attributes
  hosts: idrac_hosts
  tasks:
    - name: Discover all NICs
      dellemc.openmanage.idrac_network_info:
        idrac_ip: "{{ idrac_ip }}"
        idrac_user: "{{ idrac_user }}"
        idrac_password: "{{ idrac_password }}"
      register: nic_result

    - name: Query attributes for first NIC
      dellemc.openmanage.idrac_network_attributes_info:
        idrac_ip: "{{ idrac_ip }}"
        idrac_user: "{{ idrac_user }}"
        idrac_password: "{{ idrac_password }}"
        network_device_function_id: "{{ nic_result.network_device_functions[0].id }}"
      register: attr_result

    - name: Display attribute count
      ansible.builtin.debug:
        msg: "Found {{ attr_result.attribute_count }} attributes"
"""

RETURN = r'''
---
msg:
  description: Overall status message.
  returned: always
  type: str
  sample: "Successfully queried network attribute registry."
network_attributes:
  type: list
  description: List of network attributes with complete metadata.
  returned: success
  sample: [
    {
      "name": "VLanMode",
      "type": "Enumeration",
      "current_value": "Disabled",
      "default_value": "Disabled",
      "valid_values": ["Disabled", "Enabled"],
      "description": "Enable or disable VLAN mode.",
      "is_oem": true,
      "read_only": false,
      "requires_reboot": false,
      "dependencies": []
    }
  ]
network_device_function_id:
  type: str
  description: The NIC FQDD that was queried.
  returned: success
  sample: "NIC.Embedded.1-1-1"
attribute_registry:
  type: str
  description: Name of the attribute registry used.
  returned: success
  sample: "NetworkAttributesRegistry_NIC.Embedded.1-1-1"
attribute_count:
  type: int
  description: Total number of attributes returned (after filtering).
  returned: success
  sample: 85
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

import fnmatch
import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import (
    iDRACRedfishAPI, idrac_auth_params
)


# In-memory cache for registry data
_REGISTRY_CACHE = {}

CHASSIS_URI = "/redfish/v1/Chassis"
REGISTRIES_URI = "/redfish/v1/Registries"
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


def get_cache_key(idrac_ip, idrac_port, ndf_id):
    """Generate cache key based on iDRAC IP, port, and NIC ID."""
    return f"{idrac_ip}:{idrac_port}:{ndf_id}"


def get_from_cache(cache_key):
    """Retrieve data from cache if available."""
    return _REGISTRY_CACHE.get(cache_key)


def store_in_cache(cache_key, data):
    """Store data in cache."""
    _REGISTRY_CACHE[cache_key] = data


def discover_valid_nic_ids(idrac):
    """Discover all valid NIC IDs on the iDRAC for error messages.

    Returns a list of NIC FQDD strings. Discovery errors are intentionally
    swallowed so that the primary "NIC not found" error is surfaced.
    """
    nic_ids = []
    try:
        chassis_resp = idrac.invoke_request(CHASSIS_URI, 'GET').json_data
        chassis_members = chassis_resp.get('Members', [])
        if not chassis_members:
            return nic_ids

        chassis_uri = chassis_members[0].get(ODATA_ID, '')
        chassis_detail = idrac.invoke_request(chassis_uri, 'GET').json_data
        network_adapters_link = chassis_detail.get('NetworkAdapters', {}).get(ODATA_ID)
        if not network_adapters_link:
            return nic_ids

        for adapter_ref in get_collection_members(idrac, network_adapters_link):
            adapter_uri = adapter_ref.get(ODATA_ID, '')
            if not adapter_uri:
                continue
            adapter_detail = idrac.invoke_request(adapter_uri, 'GET').json_data
            ndf_link = adapter_detail.get('NetworkDeviceFunctions', {}).get(ODATA_ID)
            if not ndf_link:
                continue
            for ndf_ref in get_collection_members(idrac, ndf_link):
                ndf_uri = ndf_ref.get(ODATA_ID, '')
                if ndf_uri:
                    nic_ids.append(ndf_uri.split('/')[-1])
    except (HTTPError, URLError, ConnectionError, SSLValidationError):
        pass
    return nic_ids


def find_network_device_function_uri(idrac, target_ndf_id):
    """Find the Redfish URI for a specific network device function ID.

    Walks the chassis-scoped NetworkAdapters tree to find the matching NIC.
    Returns the URI string or None if not found.
    """
    chassis_resp = idrac.invoke_request(CHASSIS_URI, 'GET').json_data
    chassis_members = chassis_resp.get('Members', [])
    if not chassis_members:
        return None

    chassis_uri = chassis_members[0].get(ODATA_ID, '')
    chassis_detail = idrac.invoke_request(chassis_uri, 'GET').json_data
    network_adapters_link = chassis_detail.get('NetworkAdapters', {}).get(ODATA_ID)
    if not network_adapters_link:
        return None

    for adapter_ref in get_collection_members(idrac, network_adapters_link):
        adapter_uri = adapter_ref.get(ODATA_ID, '')
        if not adapter_uri:
            continue
        adapter_detail = idrac.invoke_request(adapter_uri, 'GET').json_data
        ndf_link = adapter_detail.get('NetworkDeviceFunctions', {}).get(ODATA_ID)
        if not ndf_link:
            continue
        for ndf_ref in get_collection_members(idrac, ndf_link):
            ndf_uri = ndf_ref.get(ODATA_ID, '')
            if ndf_uri and ndf_uri.split('/')[-1] == target_ndf_id:
                return ndf_uri

    return None


def get_registry_attributes(idrac, ndf_detail, module=None):
    """Resolve and fetch the attribute registry for a NIC.

    Follows the AttributeRegistry field from the OEM DellNetworkAttributes
    response to locate the full registry via /redfish/v1/Registries.

    Returns a tuple of (registry_name, registry_attributes_list).
    """
    # Get OEM link to DellNetworkAttributes
    oem_link = ndf_detail.get('Links', {}).get('Oem', {}).get(
        'Dell', {}).get('DellNetworkAttributes', {}).get(ODATA_ID)

    if not oem_link:
        return None, []

    # Read the DellNetworkAttributes resource
    try:
        oem_resp = idrac.invoke_request(oem_link, 'GET').json_data
    except HTTPError as e:
        if e.code == 404 and module is not None:
            module.fail_json(
                msg="DellNetworkAttributes endpoint not supported on this firmware. "
                    "Minimum required firmware: iDRAC9 >= 7.30.30.50, "
                    "iDRAC10 >= 1.30.30.50."
            )
        raise

    current_attributes = oem_resp.get('Attributes', {})
    registry_name = oem_resp.get('AttributeRegistry', '')

    # Resolve the registry from /redfish/v1/Registries
    registry_attributes = []
    if registry_name:
        for member in get_collection_members(idrac, REGISTRIES_URI):
            member_uri = member.get(ODATA_ID, '')
            if registry_name in member_uri:
                registry_detail = idrac.invoke_request(member_uri, 'GET').json_data
                locations = registry_detail.get('Location', [])
                if locations:
                    registry_uri = locations[0].get('Uri', '')
                    if registry_uri:
                        full_registry = idrac.invoke_request(registry_uri, 'GET').json_data
                        registry_attributes = full_registry.get(
                            'RegistryEntries', {}).get('Attributes', [])
                break

    return registry_name, merge_attributes(registry_attributes, current_attributes)


def merge_attributes(registry_attributes, current_attributes):
    """Merge registry schema with current attribute values.

    Returns a list of attribute dicts with combined registry metadata and
    current values from the iDRAC.
    """
    merged = []
    for attr in registry_attributes:
        attr_name = attr.get('AttributeName', '')
        merged.append({
            'name': attr_name,
            'type': attr.get('Type', ''),
            'current_value': current_attributes.get(attr_name),
            'default_value': attr.get('DefaultValue'),
            'valid_values': [v.get('ValueName', v) if isinstance(v, dict) else v
                             for v in attr.get('Value', [])],
            'description': attr.get('HelpText', ''),
            'is_oem': bool(attr.get('Oem', {}).get('Dell')),
            'read_only': attr.get('ReadOnly', False),
            'requires_reboot': bool(attr.get('Oem', {}).get('Dell', {}).get('RequiresReboot')),
            'dependencies': attr.get('Dependency', []),
            'lower_bound': attr.get('LowerBound'),
            'upper_bound': attr.get('UpperBound'),
            'min_length': attr.get('MinLength'),
            'max_length': attr.get('MaxLength'),
        })
    return merged


def filter_attributes_by_name(attributes, pattern):
    """Filter attributes by name using glob pattern matching."""
    if not pattern:
        return attributes
    return [attr for attr in attributes if fnmatch.fnmatch(attr['name'], pattern)]


def filter_attributes_by_source(attributes, source):
    """Filter attributes by OEM/standard classification."""
    if source == 'all':
        return attributes
    return [attr for attr in attributes if attr['is_oem'] == (source == 'oem')]


def main():
    """Main entry point for the idrac_network_attributes_info module."""
    argument_spec = idrac_auth_params.copy()
    argument_spec.update({
        'network_device_function_id': {'type': 'str', 'required': True},
        'attribute_name': {'type': 'str', 'required': False},
        'attribute_source': {
            'type': 'str',
            'required': False,
            'default': 'all',
            'choices': ['all', 'oem', 'standard']
        },
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

            ndf_id = module.params['network_device_function_id']
            force_refresh = module.params.get('force_refresh')
            cache_key = get_cache_key(
                module.params['idrac_ip'], module.params['idrac_port'], ndf_id)
            cached_data = None

            if not force_refresh:
                cached_data = get_from_cache(cache_key)

            if cached_data:
                network_attributes = cached_data['network_attributes']
                registry_name = cached_data['attribute_registry']
            else:
                # Find the NIC URI
                ndf_uri = find_network_device_function_uri(idrac, ndf_id)
                if not ndf_uri:
                    valid_ids = discover_valid_nic_ids(idrac)
                    valid_ids_str = ', '.join(valid_ids) if valid_ids else 'none discovered'
                    module.fail_json(
                        msg=f"Network device function '{ndf_id}' not found. "
                            f"Valid NIC IDs on this iDRAC: {valid_ids_str}"
                    )

                # Read the NDF detail to get OEM links
                ndf_detail = idrac.invoke_request(ndf_uri, 'GET').json_data

                # Query the registry
                registry_name, network_attributes = get_registry_attributes(idrac, ndf_detail, module)
                if not registry_name:
                    module.fail_json(
                        msg=f"Dell OEM network attributes link not found for NIC '{ndf_id}'. "
                            "This NIC may not support OEM attribute registry queries."
                    )

                # Store in cache
                store_in_cache(cache_key, {
                    'network_attributes': network_attributes,
                    'attribute_registry': registry_name,
                })

            # Apply filters
            attribute_name = module.params.get('attribute_name')
            attribute_source = module.params.get('attribute_source')

            if attribute_name:
                network_attributes = filter_attributes_by_name(network_attributes, attribute_name)
            if attribute_source:
                network_attributes = filter_attributes_by_source(network_attributes, attribute_source)

            attribute_count = len(network_attributes)

            module.exit_json(
                msg="Successfully queried network attribute registry.",
                changed=False,
                network_attributes=network_attributes,
                network_device_function_id=ndf_id,
                attribute_registry=registry_name,
                attribute_count=attribute_count,
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
