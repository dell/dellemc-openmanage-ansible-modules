# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 10.0.0
# Copyright (C) 2021-2026 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""Ansible module for querying iDRAC BIOS Attribute Registry and validating configurations.

This module enables administrators to query the iDRAC Redfish BIOS Attribute Registry endpoint,
validate proposed BIOS configurations against the registry, and filter attributes by name pattern,
OEM/standard classification, and category.
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_bios_registry_info
short_description: Query iDRAC BIOS Attribute Registry and validate configurations
version_added: "10.0.0"
description:
    - Query the iDRAC Redfish BIOS Attribute Registry endpoint to retrieve complete BIOS attribute metadata.
    - Validate proposed BIOS configurations against the registry with actionable error messages.
    - Filter attributes by name pattern, OEM/standard classification, and category.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options

options:
    attribute_name:
        description: Pattern to filter BIOS attributes by name (supports glob patterns).
        type: str
        required: false
    attribute_source:
        description: Filter attributes by source type.
        type: str
        required: false
        default: 'all'
        choices: ['all', 'oem', 'standard']
    category:
        description: Filter attributes by category (e.g., 'Processor', 'Memory', 'Security').
        type: str
        required: false
    validate:
        description: Validate proposed BIOS configuration against the registry.
        type: bool
        required: false
        default: false
    attributes:
        description: Dictionary of attribute names and proposed values to validate.
        type: dict
        required: false
    force_refresh:
        description: Force refresh of BIOS attribute registry from iDRAC, bypassing cache.
        type: bool
        required: false
        default: false

requirements:
    - "python >= 3.9.6"
author: "Sapana Gupta(@sapana05)"
notes:
    - "Run this module from a system that has direct access to Dell iDRAC."
    - "This module supports both IPv4 and IPv6 address for I(idrac_ip)."
    - "Minimum firmware requirement: iDRAC9 >= 7.10.90.00 or iDRAC10 >= 1.20.50.50."
"""

EXAMPLES = """
---
- name: Query all BIOS attributes
  dellemc.openmanage.idrac_bios_registry_info:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    ca_path: "/path/to/ca_cert.pem"

- name: Query BIOS attributes with filtering
  dellemc.openmanage.idrac_bios_registry_info:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    attribute_name: "Proc*"
    attribute_source: "oem"
    category: "Processor"

- name: Validate BIOS configuration
  dellemc.openmanage.idrac_bios_registry_info:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    validate: true
    attributes:
      ProcVirtualization: "Enabled"
      MemTest: "Disabled"
"""

RETURN = r'''
---
msg:
  description: Overall status message.
  returned: always
  type: str
  sample: "Successfully queried BIOS attribute registry."
bios_attributes:
  type: list
  description: List of BIOS attributes with complete metadata.
  returned: success
  sample: [
    {
      "name": "ProcVirtualization",
      "display_name": "Virtualization Technology",
      "type": "Enumeration",
      "current_value": "Enabled",
      "default_value": "Enabled",
      "valid_values": ["Enabled", "Disabled"],
      "description": "Enable or disable virtualization technology.",
      "is_oem": true,
      "read_only": false,
      "immutable": false,
      "write_only": false,
      "gray_out": false,
      "hidden": false,
      "group": "Processor Settings",
      "menu_path": "./ProcSettingsRef",
      "lower_bound": null,
      "upper_bound": null,
      "min_length": null,
      "max_length": null,
      "scalar_increment": null,
      "regex": null,
      "value_expression": null,
      "warning_text": null,
      "display_order": 1,
      "is_system_unique_property": false
    }
  ]
registry_version:
  type: str
  description: Version of the BIOS attribute registry.
  returned: success
  sample: "1.0.0"
attribute_count:
  type: int
  description: Total number of attributes in the registry.
  returned: success
  sample: 150
language:
  type: str
  description: Language of the registry.
  returned: success
  sample: "en"
owning_entity:
  type: str
  description: Entity that owns the registry.
  returned: success
  sample: "Dell"
idrac_generation:
  type: int
  description: PowerEdge server generation (14G-16G for iDRAC9, 17G+ for iDRAC10).
  returned: success
  sample: 15
idrac_firmware_version:
  type: str
  description: iDRAC firmware version.
  returned: success
  sample: "7.10.90.00"
idrac_model:
  type: str
  description: iDRAC model.
  returned: success
  sample: "iDRAC 9"
validation_results:
  type: list
  description: Validation results for each attribute when validate=true.
  returned: when validate=true
  sample: [
    {
      "attribute": "ProcVirtualization",
      "status": "valid",
      "reason": "Value is valid",
      "suggestions": []
    }
  ]
valid:
  type: bool
  description: Overall validation status when validate=true.
  returned: when validate=true
  sample: true
valid_count:
  type: int
  description: Count of valid attributes when validate=true.
  returned: when validate=true
  sample: 2
invalid_count:
  type: int
  description: Count of invalid attributes when validate=true.
  returned: when validate=true
  sample: 0
error_info:
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

import difflib
import fnmatch
import re
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import (
    iDRACRedfishAPI, idrac_auth_params
)


# In-memory cache for BIOS registry data
_REGISTRY_CACHE = {}


def map_attribute_to_dict(attr_data):
    """Map DellAttributeRegistry_v1_2_0_Attributes schema to Python dict."""
    return {
        'name': attr_data.get('AttributeName'),
        'display_name': attr_data.get('DisplayName'),
        'type': attr_data.get('Type'),
        'current_value': attr_data.get('CurrentValue'),
        'default_value': attr_data.get('DefaultValue'),
        'valid_values': [v.get('ValueName', v) if isinstance(v, dict) else v
                         for v in attr_data.get('Value', [])],
        'description': attr_data.get('HelpText'),
        'is_oem': bool(attr_data.get('Oem', {}).get('Dell')),
        'read_only': attr_data.get('ReadOnly', False),
        'immutable': attr_data.get('Immutable', False),
        'write_only': attr_data.get('WriteOnly', False),
        'gray_out': attr_data.get('GrayOut', False),
        'hidden': attr_data.get('Hidden', False),
        'group': (attr_data.get('Oem', {}).get('Dell', {}).get('GroupDisplayName', '')
                  or (attr_data.get('MenuPath', '').split('/')[-1] if attr_data.get('MenuPath') else '')),
        'menu_path': attr_data.get('MenuPath'),
        'lower_bound': attr_data.get('LowerBound'),
        'upper_bound': attr_data.get('UpperBound'),
        'min_length': attr_data.get('MinLength'),
        'max_length': attr_data.get('MaxLength'),
        'scalar_increment': attr_data.get('ScalarIncrement'),
        'regex': attr_data.get('Regex'),
        'value_expression': attr_data.get('ValueExpression'),
        'warning_text': attr_data.get('WarningText'),
        'display_order': attr_data.get('DisplayOrder'),
        'is_system_unique_property': attr_data.get('IsSystemUniqueProperty', False)
    }


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


def filter_attributes_by_category(attributes, category):
    """Filter attributes by category matching group display name or MenuPath.

    Supports both exact category names (e.g., 'Processor') and iDRAC-specific
    MenuPath naming conventions (e.g., './ProcSettingsRef' for 'Processor',
    './SysSecurityRef' for 'Security', './MemSettingsRef' for 'Memory').
    """
    if not category:
        return attributes
    cat_lower = category.lower()
    # Map common category names to MenuPath prefixes used by iDRAC
    _CATEGORY_MENU_PATH_MAP = {
        'processor': ['Proc', 'Processor'],
        'security': ['SysSecurity', 'Security'],
        'memory': ['MemSettings', 'Memory'],
        'boot': ['BootSettings', 'Boot'],
        'network': ['NetworkSettings', 'Network'],
        'integrated devices': ['IntegratedDevices'],
        'serial communication': ['SerialCommSettings', 'SerialComm'],
        'system profile': ['SysProfileSettings', 'SysProfile'],
        'miscellaneous': ['MiscSettings', 'Misc'],
        'system information': ['SysInformation', 'SysInfo'],
        'sata': ['SataSettings', 'Sata'],
        'nvme': ['NvmeSettings', 'Nvme'],
        'redundant os': ['RedundantOsControl', 'RedundantOs'],
    }
    menu_prefixes = _CATEGORY_MENU_PATH_MAP.get(cat_lower, [category])
    return [attr for attr in attributes
            if cat_lower in attr.get('group', '').lower()
            or any(attr.get('menu_path', '').startswith(f'./{prefix}')
                   for prefix in menu_prefixes)]


def _validation_result(attr, status, reason, suggestions=None):
    """Build a validation result dict."""
    return {
        'attribute': attr,
        'status': status,
        'reason': reason,
        'suggestions': suggestions or []
    }


def _fuzzy_attr_suggestions(attr, bios_attributes, n=3, cutoff=0.6):
    """Return close-match attribute names using difflib."""
    all_names = [a['name'] for a in bios_attributes]
    return difflib.get_close_matches(attr, all_names, n=n, cutoff=cutoff)


def validate_attribute(attr, value, bios_attributes):
    """Validate a single attribute value against the registry."""
    attr_def = next((a for a in bios_attributes if a['name'] == attr), None)
    if not attr_def:
        suggestions = _fuzzy_attr_suggestions(attr, bios_attributes)
        return _validation_result(
            attr, 'invalid',
            f"Attribute '{attr}' not found in BIOS registry",
            suggestions)

    if attr_def['read_only']:
        return _validation_result(attr, 'invalid',
                                  f"Attribute '{attr}' is read-only and cannot be modified")

    if attr_def['type'] == 'Enumeration':
        if value not in attr_def['valid_values']:
            suggestions = [v for v in attr_def['valid_values']
                           if value.lower() in v.lower() or v.lower() in value.lower()]
            return _validation_result(attr, 'invalid',
                                      f"Value '{value}' is not a valid enumeration value",
                                      suggestions[:3])
    elif attr_def['type'] == 'Integer':
        try:
            int_value = int(value)
            if attr_def['lower_bound'] is not None and int_value < attr_def['lower_bound']:
                return _validation_result(attr, 'invalid',
                                          f"Value {int_value} is below minimum {attr_def['lower_bound']}")
            if attr_def['upper_bound'] is not None and int_value > attr_def['upper_bound']:
                return _validation_result(attr, 'invalid',
                                          f"Value {int_value} exceeds maximum {attr_def['upper_bound']}")
        except (ValueError, TypeError):
            return _validation_result(attr, 'invalid',
                                      f"Value '{value}' is not a valid integer")
    elif attr_def['type'] == 'String':
        str_value = str(value)
        if attr_def['min_length'] is not None and len(str_value) < attr_def['min_length']:
            return _validation_result(attr, 'invalid',
                                      f"Value length {len(str_value)} is below minimum {attr_def['min_length']}")
        if attr_def['max_length'] is not None and len(str_value) > attr_def['max_length']:
            return _validation_result(attr, 'invalid',
                                      f"Value length {len(str_value)} exceeds maximum {attr_def['max_length']}")
        if attr_def['regex'] and not re.match(attr_def['regex'], str_value):
            return _validation_result(attr, 'invalid',
                                      f"Value '{value}' does not match required pattern")

    return _validation_result(attr, 'valid', 'Value is valid')


def validate_attributes(attributes_to_validate, bios_attributes):
    """Validate multiple attribute-value pairs."""
    validation_results = []
    valid_count = 0
    invalid_count = 0

    for attr, value in attributes_to_validate.items():
        result = validate_attribute(attr, value, bios_attributes)
        validation_results.append(result)
        if result['status'] == 'valid':
            valid_count += 1
        else:
            invalid_count += 1

    return {
        'validation_results': validation_results,
        'valid': invalid_count == 0,
        'valid_count': valid_count,
        'invalid_count': invalid_count
    }


def get_cache_key(idrac_ip, firmware_version):
    """Generate cache key based on iDRAC IP and firmware version."""
    return f"{idrac_ip}:{firmware_version}"


def get_from_cache(cache_key):
    """Retrieve data from cache if available."""
    return _REGISTRY_CACHE.get(cache_key)


def store_in_cache(cache_key, data):
    """Store data in cache."""
    _REGISTRY_CACHE[cache_key] = data


def main():
    """Main entry point for the idrac_bios_registry_info module.

    This function initializes the Ansible module, connects to iDRAC,
    queries the BIOS attribute registry, applies filters and validation,
    and returns the results.
    """
    argument_spec = idrac_auth_params.copy()
    argument_spec.update({
        'attribute_name': {'type': 'str', 'required': False},
        'attribute_source': {
            'type': 'str',
            'required': False,
            'default': 'all',
            'choices': ['all', 'oem', 'standard']
        },
        'category': {'type': 'str', 'required': False},
        'validate': {'type': 'bool', 'required': False, 'default': False},
        'attributes': {'type': 'dict', 'required': False},
        'force_refresh': {'type': 'bool', 'required': False, 'default': False},
    })

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    # Initialize iDRAC connection
    try:
        with iDRACRedfishAPI(module.params) as idrac:
            # Fetch firmware version and generation
            generation, firmware_version, hw_model = idrac.get_server_generation

            # Check firmware version requirements using centralized utility
            is_compliant, min_fw_version, error_msg = iDRACRedfishAPI.check_minimum_firmware_requirement(  # pylint: disable=unused-variable
                hw_model, firmware_version
            )
            if not is_compliant:
                module.fail_json(msg=error_msg)

            # Query BIOS attribute registry
            registry_uri = "/redfish/v1/Systems/System.Embedded.1/Bios/BiosRegistry"

            # Check cache first (unless force_refresh is True)
            force_refresh = module.params.get('force_refresh')
            cache_key = get_cache_key(module.params['idrac_ip'], firmware_version)
            cached_data = None

            if not force_refresh:
                cached_data = get_from_cache(cache_key)

            if cached_data:
                bios_attributes = cached_data['bios_attributes']
                registry_version = cached_data['registry_version']
                attribute_count = cached_data['attribute_count']
                language = cached_data.get('language', 'en')
                owning_entity = cached_data.get('owning_entity', 'Dell')
            else:
                try:
                    response = idrac.invoke_request(registry_uri, 'GET')
                except HTTPError as e:
                    if e.code == 404:
                        module.fail_json(
                            msg="BIOS attribute registry endpoint not supported on this system."
                        )
                    else:
                        module.fail_json(
                            msg=f"HTTP error {e.code} when querying registry: {e.msg}"
                        )

                # Parse registry response
                registry_data = response.json_data

                # Extract registry metadata
                registry_version = registry_data.get('RegistryVersion', '')
                language = registry_data.get('Language', 'en')
                owning_entity = registry_data.get('OwningEntity', 'Dell')
                registry_entries = registry_data.get('RegistryEntries', {})
                attributes_list = registry_entries.get('Attributes', [])
                attribute_count = len(attributes_list)

                # Map attributes to flat list
                bios_attributes = [map_attribute_to_dict(attr) for attr in attributes_list]

                # Store in cache
                store_in_cache(cache_key, {
                    'bios_attributes': bios_attributes,
                    'registry_version': registry_version,
                    'attribute_count': attribute_count,
                    'language': language,
                    'owning_entity': owning_entity
                })

            # Apply filters
            attribute_name = module.params.get('attribute_name')
            attribute_source = module.params.get('attribute_source')
            category = module.params.get('category')

            if attribute_name:
                bios_attributes = filter_attributes_by_name(bios_attributes, attribute_name)

            if attribute_source:
                bios_attributes = filter_attributes_by_source(bios_attributes, attribute_source)

            if category:
                bios_attributes = filter_attributes_by_category(bios_attributes, category)

            # Update attribute count after filtering
            attribute_count = len(bios_attributes)

            # Handle validation if requested
            validate = module.params.get('validate')
            attributes_to_validate = module.params.get('attributes')
            validation_results = None
            valid = None
            valid_count = None
            invalid_count = None

            if validate and attributes_to_validate:
                validation_data = validate_attributes(attributes_to_validate, bios_attributes)
                validation_results = validation_data['validation_results']
                valid = validation_data['valid']
                valid_count = validation_data['valid_count']
                invalid_count = validation_data['invalid_count']
            module.exit_json(
                msg="Successfully queried BIOS attribute registry.",
                changed=False,
                bios_attributes=bios_attributes,
                registry_version=registry_version,
                attribute_count=attribute_count,
                language=language,
                owning_entity=owning_entity,
                idrac_generation=generation,
                idrac_firmware_version=firmware_version,
                idrac_model=hw_model,
                validation_results=validation_results,
                valid=valid,
                valid_count=valid_count,
                invalid_count=invalid_count
            )
    except HTTPError as e:
        if e.code in [401, 403]:
            module.fail_json(msg=f"Authentication failed: {e.msg}")
        else:
            module.fail_json(msg=f"HTTP error {e.code}: {e.msg}")
    except SSLValidationError as e:
        module.fail_json(msg=f"SSL validation error: {str(e)}")
    except ConnectionError as e:
        module.fail_json(msg=f"Connection error: {str(e)}")
    except URLError as e:
        module.fail_json(msg=f"Network error: {str(e)}")
    except Exception as e:  # pylint: disable=broad-except
        # Re-raise AnsibleExitJson and AnsibleFailJson for test framework
        if type(e).__name__ in ['AnsibleExitJson', 'AnsibleFailJson']:
            raise
        module.fail_json(msg=f"Unexpected error: {str(e)}")


if __name__ == '__main__':
    main()
