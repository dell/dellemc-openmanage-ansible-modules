#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.0
# Copyright (C) 2025-2026 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_network_attribute_registry
short_description: Queries and validates iDRAC network attribute registry
version_added: "9.12.0"
description:
  - This module queries the iDRAC Redfish network attribute registry for a specific NIC
    to discover available network attributes with their schemas (data types, valid values,
    descriptions, read-only vs read-write status).
  - Requires I(network_device_function_id) to target a specific NIC. To discover available
    NIC IDs, first query C(/redfish/v1/Registries) or use I(dellemc.openmanage.idrac_network_attributes)
    with the desired network adapter and device function.
  - Supports querying all attributes, standard Redfish-only attributes, or Dell OEM-only attributes.
  - Supports wildcard pattern filtering to narrow results to specific attribute categories.
  - Supports batch validation of attribute name-value pairs against the registry schema with
    actionable error messages and suggested corrections.
  - Supports three output formats - JSON (default), YAML, and table (human-readable).
  - Performs an upfront firmware version check and fails with a descriptive error if firmware
    is below the minimum required version.
  - This module is read-only and does not modify any iDRAC configuration.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_x_auth_options
options:
  network_device_function_id:
    type: str
    required: true
    description:
      - FQDD of the network device function whose attribute registry to query.
      - "An example of FQDD of the network device function is C(NIC.Integrated.1-1-1) or C(NIC.Slot.2-1-1)."
      - "To discover available NIC IDs, query the iDRAC Registries endpoint at
        C(/redfish/v1/Registries) and look for members whose name starts with
        C(NetworkAttributesRegistry_)."
  query_type:
    type: str
    description:
      - The type of query to perform against the attribute registry.
      - C(all) returns both standard Redfish and Dell OEM attributes.
      - C(redfish) returns only standard Redfish attributes.
      - C(oem) returns only Dell OEM-specific attributes.
      - C(validate) validates the attribute name-value pairs provided via I(validate_attributes).
    default: all
    choices: [all, redfish, oem, validate]
  attribute_pattern:
    type: str
    description:
      - Wildcard pattern for filtering attributes by name.
      - Uses standard wildcard matching (e.g., C(VLAN*), C(Link*), C(*Speed*)).
      - Only attributes whose names match the pattern are returned.
      - This parameter is applied after the I(query_type) filter.
    default: '*'
  validate_attributes:
    type: dict
    description:
      - Dictionary of attribute name-value pairs to validate against the registry schema.
      - Each key is an attribute name and each value is the proposed attribute value.
      - The module returns per-attribute pass/fail validation results.
      - For invalid attribute names, the module suggests corrections (fuzzy matching).
      - For invalid attribute values, the module lists the valid values.
      - This parameter is required when I(query_type) is C(validate).
  output_format:
    type: str
    description:
      - The output format for the query results.
      - C(json) returns a structured dictionary (default).
      - C(yaml) returns a YAML-formatted string.
      - C(table) returns a human-readable table string.
    default: json
    choices: [json, yaml, table]
  force_refresh:
    type: bool
    description:
      - Force refresh of registry data from iDRAC, bypassing the within-playbook cache.
      - When C(false), the module caches registry data per iDRAC target for the duration
        of the playbook run. Subsequent queries to the same target return cached data.
      - When C(true), the module always queries the iDRAC Redfish API directly and
        updates the cache with the fresh data.
    default: false
requirements:
  - "python >= 3.9.6"
author:
  - "Dell OpenManage Ansible Team"
notes:
  - Run this module from a system that has direct access to Dell iDRAC.
  - This module supports both IPv4 and IPv6 addresses.
  - This module supports C(check_mode).
  - This module is read-only and does not make any configuration changes.
  - Minimum firmware required - iDRAC9 7.30.30.50 or iDRAC10 1.30.30.50.
  - I(network_device_function_id) is required to target a specific NIC for performance reasons.
    Querying all NICs simultaneously can result in 10+ minute response times.
  - Registry data is cached per iDRAC target and NIC within a playbook run. Use I(force_refresh) to bypass.
  - When used with C(x_auth_token), authentication overhead is reduced by reusing an existing session.
"""

EXAMPLES = """
---
- name: Query all network attributes for a specific NIC
  dellemc.openmanage.idrac_network_attribute_registry:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_device_function_id: "NIC.Integrated.1-1-1"
    query_type: "all"

- name: Query only standard Redfish attributes for a NIC
  dellemc.openmanage.idrac_network_attribute_registry:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_device_function_id: "NIC.Integrated.1-1-1"
    query_type: "redfish"

- name: Query only Dell OEM attributes for a NIC
  dellemc.openmanage.idrac_network_attribute_registry:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_device_function_id: "NIC.Integrated.1-1-1"
    query_type: "oem"

- name: Filter VLAN-related attributes using wildcard
  dellemc.openmanage.idrac_network_attribute_registry:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_device_function_id: "NIC.Integrated.1-1-1"
    attribute_pattern: "VLan*"

- name: Validate attribute name-value pairs for a NIC
  dellemc.openmanage.idrac_network_attribute_registry:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_device_function_id: "NIC.Integrated.1-1-1"
    query_type: "validate"
    validate_attributes:
      VLanMode: "Enabled"
      LnkSpeed: "AutoNeg"

- name: Query attributes with YAML output format
  dellemc.openmanage.idrac_network_attribute_registry:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_device_function_id: "NIC.Integrated.1-1-1"
    output_format: "yaml"

- name: Query attributes with table output format
  dellemc.openmanage.idrac_network_attribute_registry:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_device_function_id: "NIC.Integrated.1-1-1"
    output_format: "table"

- name: Query using X-Auth token for session reuse
  dellemc.openmanage.idrac_network_attribute_registry:
    idrac_ip: "192.168.0.1"
    x_auth_token: "{{ auth_token }}"
    network_device_function_id: "NIC.Integrated.1-1-1"
    query_type: "all"

- name: Establish session and query with token reuse
  block:
    - name: Create iDRAC session
      dellemc.openmanage.idrac_session:
        hostname: "192.168.0.1"
        username: "user_name"
        password: "user_password"
        state: "present"
      register: session_result

    - name: Query registry using session token
      dellemc.openmanage.idrac_network_attribute_registry:
        idrac_ip: "192.168.0.1"
        x_auth_token: "{{ session_result.x_auth_token }}"
        network_device_function_id: "NIC.Integrated.1-1-1"
        query_type: "all"

- name: Force refresh to bypass cache
  dellemc.openmanage.idrac_network_attribute_registry:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_device_function_id: "NIC.Integrated.1-1-1"
    force_refresh: true

- name: Multi-target query using loop
  dellemc.openmanage.idrac_network_attribute_registry:
    idrac_ip: "{{ item }}"
    idrac_user: "user_name"
    idrac_password: "user_password"
    network_device_function_id: "NIC.Integrated.1-1-1"
    query_type: "all"
  loop:
    - "192.168.0.1"
    - "192.168.0.2"
    - "192.168.0.3"
  register: multi_target_results
  ignore_errors: true
"""

RETURN = """
---
msg:
  description: Status message for the operation.
  returned: always
  type: str
  sample: "Successfully retrieved network attribute registry for NIC.Integrated.1-1-1."
network_device_function_id:
  description: The NIC ID that was queried.
  returned: always
  type: str
  sample: "NIC.Integrated.1-1-1"
available_nics:
  description: List of available NIC IDs with network attribute registries on the target iDRAC.
  returned: on failure when NIC ID is not found
  type: list
  elements: str
  sample: ["NIC.Integrated.1-1-1", "NIC.Integrated.1-2-1", "NIC.Slot.2-1-1"]
attributes:
  description:
    - List of network attributes from the registry.
    - Each attribute contains name, data_type, valid_values (if enumerated),
      description, read_only status, and oem_vendor (for OEM attributes).
  returned: when I(query_type) is C(all), C(redfish), or C(oem)
  type: list
  elements: dict
  sample: [
    {
      "name": "VLanMode",
      "data_type": "Enumeration",
      "valid_values": ["Enabled", "Disabled"],
      "description": "Enables or disables VLAN mode.",
      "read_only": false,
      "oem_vendor": "Dell"
    }
  ]
attribute_count:
  description: Number of attributes returned.
  returned: when I(query_type) is C(all), C(redfish), or C(oem)
  type: int
  sample: 42
validation_results:
  description:
    - Per-attribute validation results.
    - Each entry contains attribute_name, attribute_value, status (pass/fail),
      error_message (if failed), and suggested_corrections (if applicable).
  returned: when I(query_type) is C(validate)
  type: list
  elements: dict
  sample: [
    {
      "attribute_name": "VLanMode",
      "attribute_value": "Enabled",
      "status": "pass",
      "error_message": null,
      "suggested_corrections": null
    },
    {
      "attribute_name": "VLanMod",
      "attribute_value": "Enabled",
      "status": "fail",
      "error_message": "Attribute 'VLanMod' does not exist in registry. Did you mean 'VLanMode'?",
      "suggested_corrections": ["VLanMode"]
    }
  ]
firmware_version:
  description: iDRAC firmware version detected on the target.
  returned: always
  type: str
  sample: "7.30.30.50"
idrac_model:
  description: iDRAC hardware model detected on the target.
  returned: always
  type: str
  sample: "iDRAC 9"
output_format:
  description: The output format used for the response.
  returned: always
  type: str
  sample: "json"
formatted_output:
  description:
    - The attribute data formatted according to I(output_format).
    - For C(json), this is a list of attribute dictionaries.
    - For C(yaml), this is a YAML-formatted string.
    - For C(table), this is a human-readable table string.
  returned: when I(query_type) is C(all), C(redfish), or C(oem)
  type: raw
  sample: "| Name | Type | Read Only | Description |\\n|------|------|-----------|-------------|"
error_info:
  description:
    - Error details from the iDRAC Redfish API when an HTTP error occurs.
    - Contains the structured error response body with OData keys removed.
    - Useful for programmatic error handling in multi-target loop playbooks.
  returned: on HTTP error
  type: dict
  sample: {"error": {"@Message.ExtendedInfo": [{"Message": "Access denied"}]}}
"""

import json
import re
import time
import yaml
from fnmatch import fnmatch
from difflib import get_close_matches
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import (
    iDRACRedfishAPI, IdracAnsibleModule
)
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import remove_key

REGISTRIES_URI = "/redfish/v1/Registries"
MANAGER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"
IDRAC_ATTRIBUTES_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/iDRAC.Embedded.1"

MIN_FW_IDRAC9 = "7.30.30.50"
MIN_FW_IDRAC10 = "1.30.30.50"
ODATA_ID = "(.*?)@odata"

SUCCESS_QUERY_MSG = "Successfully retrieved network attribute registry for {nic_id}."
SUCCESS_VALIDATE_MSG = "Attribute validation completed for {nic_id}."
FIRMWARE_TOO_OLD_MSG = (
    "iDRAC firmware version {fw_version} does not support attribute registry endpoints. "
    "Minimum required version: {min_version}. "
    "Please upgrade firmware or use manual attribute configuration."
)
NO_REGISTRY_MSG = (
    "No network attribute registry found for '{nic_id}' on iDRAC {idrac_ip}. "
    "Available NICs with registries: {available_nics}. "
    "To discover available NICs, query /redfish/v1/Registries on the target iDRAC."
)
VALIDATE_REQUIRES_ATTRS_MSG = "The 'validate_attributes' parameter is required when query_type is 'validate'."
RETRY_TRANSIENT_MSG = "Transient error on attempt {attempt}/{max_retries}: {error}. Retrying in {delay}s..."
MAX_RETRIES = 3
RETRY_BASE_DELAY = 1
NETWORK_REGISTRY_PREFIX = "NetworkAttributesRegistry_"

# In-memory cache for registry data (per-process, within a playbook run)
_registry_cache = {}


def get_cache_key(idrac_ip, port, nic_id):
    """Generate cache key based on iDRAC IP, port, and NIC ID."""
    return "{0}:{1}:{2}".format(idrac_ip, port, nic_id)


def get_from_cache(cache_key):
    """Retrieve data from cache if available."""
    return _registry_cache.get(cache_key)


def store_in_cache(cache_key, data):
    """Store data in cache."""
    _registry_cache[cache_key] = data


def _invoke_with_retry(idrac, uri, method, module=None, max_retries=MAX_RETRIES):
    """Invoke a Redfish request with exponential backoff retry for transient failures.

    Only transient errors (URLError excluding HTTPError, ConnectionError, OSError)
    are retried. HTTPError (4xx/5xx) is raised immediately.
    """
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            return idrac.invoke_request(uri, method)
        except HTTPError:
            raise
        except (URLError, ConnectionError, OSError) as err:
            last_error = err
            if attempt < max_retries:
                delay = RETRY_BASE_DELAY * (2 ** (attempt - 1))
                if module:
                    module.log(RETRY_TRANSIENT_MSG.format(
                        attempt=attempt, max_retries=max_retries,
                        error=str(err), delay=delay
                    ))
                time.sleep(delay)
    raise last_error


def get_idrac_firmware_info(idrac):
    """Query iDRAC Manager endpoint to get generation, firmware version, and model."""
    response = idrac.invoke_request(MANAGER_URI, 'GET')
    generation = 0
    firmware_version = None
    if response.status_code == 200:
        data = response.json_data
        model_match = re.search(r"\d+(?=G)", data.get("Model", ""))
        if model_match:
            generation = int(model_match.group())
        firmware_version = data.get("FirmwareVersion")

    hw_model = "iDRAC 9"
    try:
        hw_resp = idrac.invoke_request(IDRAC_ATTRIBUTES_URI, 'GET')
        if hw_resp.status_code == 200:
            hw_model = hw_resp.json_data.get('Attributes', {}).get('Info.1.HWModel', "iDRAC 9")
    except HTTPError:
        hw_model = "iDRAC 8"

    return generation, firmware_version, hw_model


def check_firmware_version(firmware_version, hw_model):
    """Check if firmware meets minimum requirements for attribute registry support."""
    if "10" in hw_model:
        min_version = MIN_FW_IDRAC10
    else:
        min_version = MIN_FW_IDRAC9

    fw_parts = [int(x) for x in firmware_version.split('.')]
    min_parts = [int(x) for x in min_version.split('.')]
    for fw, min_v in zip(fw_parts, min_parts):
        if fw > min_v:
            return True, min_version
        if fw < min_v:
            return False, min_version
    return len(fw_parts) >= len(min_parts), min_version


def discover_available_nics(idrac, module=None):
    """Discover available NIC IDs from the Registries endpoint.

    Returns a list of NIC ID strings (e.g. ['NIC.Integrated.1-1-1', 'NIC.Slot.2-1-1']).
    """
    response = _invoke_with_retry(idrac, REGISTRIES_URI, 'GET', module=module)
    if response.status_code != 200:
        return []

    members = response.json_data.get("Members", [])
    nics = []
    for member in members:
        odata_id = member.get("@odata.id", "")
        # Extract NIC ID from registry names like NetworkAttributesRegistry_NIC.Slot.10-2-1
        if NETWORK_REGISTRY_PREFIX in odata_id:
            nic_id = odata_id.rsplit("/", 1)[-1].replace(NETWORK_REGISTRY_PREFIX, "")
            nics.append(nic_id)
    return nics


def fetch_registry_attributes(idrac, nic_id, module=None):
    """Fetch raw attribute registry data for a specific NIC from iDRAC Redfish endpoint.

    Discovery flow:
    1. GET /redfish/v1/Registries — list all registry members
    2. Find the member whose @odata.id contains the nic_id
    3. GET the member URI to retrieve the Location array
    4. GET Location[0].Uri to retrieve the actual AttributeRegistry JSON
    """
    response = _invoke_with_retry(idrac, REGISTRIES_URI, 'GET', module=module)
    if response.status_code != 200:
        return None, []

    members = response.json_data.get("Members", [])
    available_nics = []
    matching_member_uri = None

    for member in members:
        odata_id = member.get("@odata.id", "")
        if NETWORK_REGISTRY_PREFIX in odata_id:
            member_nic_id = odata_id.rsplit("/", 1)[-1].replace(NETWORK_REGISTRY_PREFIX, "")
            available_nics.append(member_nic_id)
            if nic_id == member_nic_id:
                matching_member_uri = odata_id

    if not matching_member_uri:
        return None, available_nics

    if module:
        module.log("Found registry member for {0}: {1}".format(nic_id, matching_member_uri))

    # Step 2: GET the registry member to find Location URI
    member_resp = _invoke_with_retry(idrac, matching_member_uri, 'GET', module=module)
    if member_resp.status_code != 200:
        return None, available_nics

    location = member_resp.json_data.get("Location", [])
    if not location:
        return None, available_nics

    registry_json_uri = location[0].get("Uri")
    if not registry_json_uri:
        return None, available_nics

    if module:
        module.log("Fetching registry JSON from: {0}".format(registry_json_uri))

    # Step 3: GET the actual AttributeRegistry JSON
    detail_resp = _invoke_with_retry(idrac, registry_json_uri, 'GET', module=module)
    if detail_resp.status_code == 200:
        return detail_resp.json_data, available_nics

    return None, available_nics


def parse_registry_attributes(registry_data):
    """Parse raw registry data into a structured list of attributes."""
    attributes = []
    if not registry_data:
        return attributes

    registry_entries = registry_data.get("RegistryEntries", {})
    attr_list = registry_entries.get("Attributes", [])

    for attr in attr_list:
        parsed = {
            "name": attr.get("AttributeName", attr.get("Id", "")),
            "data_type": attr.get("Type", "Unknown"),
            "valid_values": attr.get("Value", []),
            "description": attr.get("HelpText", attr.get("Description", "")),
            "read_only": attr.get("ReadOnly", False),
            "oem_vendor": None,
        }

        if isinstance(parsed["valid_values"], list):
            parsed["valid_values"] = [
                v.get("ValueName", v) if isinstance(v, dict) else v
                for v in parsed["valid_values"]
            ]
        else:
            parsed["valid_values"] = []

        if attr.get("Oem") or "Dell" in str(attr.get("AttributeName", "")):
            parsed["oem_vendor"] = "Dell"

        attributes.append(parsed)

    return attributes


def filter_by_query_type(attributes, query_type):
    """Filter attributes based on query type (all, redfish, oem)."""
    if query_type == "all":
        return attributes
    elif query_type == "oem":
        return [a for a in attributes if a.get("oem_vendor") == "Dell"]
    elif query_type == "redfish":
        return [a for a in attributes if a.get("oem_vendor") is None]
    return attributes


def filter_by_pattern(attributes, pattern):
    """Filter attributes by wildcard pattern."""
    if pattern == "*":
        return attributes
    return [a for a in attributes if fnmatch(a["name"], pattern)]


def validate_attributes_against_registry(attributes, validate_attrs):
    """Validate attribute name-value pairs against the registry."""
    attr_map = {a["name"]: a for a in attributes}
    attr_names = list(attr_map.keys())
    results = []

    for attr_name, attr_value in validate_attrs.items():
        result = {
            "attribute_name": attr_name,
            "attribute_value": attr_value,
            "status": "pass",
            "error_message": None,
            "suggested_corrections": None,
        }

        if attr_name not in attr_map:
            suggestions = get_close_matches(attr_name, attr_names, n=3, cutoff=0.6)
            suggestion_text = ""
            if suggestions:
                suggestion_text = " Did you mean '{0}'?".format(suggestions[0])
                result["suggested_corrections"] = suggestions
            result["status"] = "fail"
            result["error_message"] = (
                "Attribute '{0}' does not exist in registry.{1}".format(
                    attr_name, suggestion_text
                )
            )
        else:
            registry_attr = attr_map[attr_name]
            valid_values = registry_attr.get("valid_values", [])
            if valid_values and str(attr_value) not in [str(v) for v in valid_values]:
                result["status"] = "fail"
                result["error_message"] = (
                    "{0} value '{1}' is invalid. Valid values: {2}".format(
                        attr_name, attr_value, ", ".join(str(v) for v in valid_values)
                    )
                )
                close_vals = get_close_matches(str(attr_value), [str(v) for v in valid_values], n=1, cutoff=0.4)
                if close_vals:
                    result["suggested_corrections"] = close_vals

        results.append(result)

    return results


def format_output(attributes, output_format):
    """Format attributes according to the requested output format."""
    if output_format == "json":
        return attributes
    elif output_format == "yaml":
        return yaml.dump(attributes, default_flow_style=False, sort_keys=False)
    elif output_format == "table":
        if not attributes:
            return "No attributes found."
        header = "| {0} | {1} | {2} | {3} |".format(
            "Name".ljust(30), "Type".ljust(15), "Read Only".ljust(10), "Description".ljust(50)
        )
        separator = "| {0} | {1} | {2} | {3} |".format(
            "-" * 30, "-" * 15, "-" * 10, "-" * 50
        )
        rows = [header, separator]
        for attr in attributes:
            row = "| {0} | {1} | {2} | {3} |".format(
                str(attr.get("name", "")).ljust(30),
                str(attr.get("data_type", "")).ljust(15),
                str(attr.get("read_only", "")).ljust(10),
                str(attr.get("description", ""))[:50].ljust(50),
            )
            rows.append(row)
        return "\n".join(rows)
    return attributes


def main():
    try:
        specs = {
            "network_device_function_id": {
                "type": "str",
                "required": True,
            },
            "query_type": {
                "type": "str",
                "default": "all",
                "choices": ["all", "redfish", "oem", "validate"],
            },
            "attribute_pattern": {
                "type": "str",
                "default": "*",
            },
            "validate_attributes": {
                "type": "dict",
                "required": False,
            },
            "output_format": {
                "type": "str",
                "default": "json",
                "choices": ["json", "yaml", "table"],
            },
            "force_refresh": {
                "type": "bool",
                "default": False,
            },
        }

        module = IdracAnsibleModule(
            argument_spec=specs,
            supports_check_mode=True,
            required_if=[["query_type", "validate", ("validate_attributes",)]],
        )

        nic_id = module.params.get("network_device_function_id")
        query_type = module.params.get("query_type")
        attribute_pattern = module.params.get("attribute_pattern")
        validate_attrs = module.params.get("validate_attributes")
        output_format = module.params.get("output_format")
        force_refresh = module.params.get("force_refresh", False)

        idrac_ip = module.params.get("idrac_ip")
        idrac_port = module.params.get("idrac_port", 443)
        cache_key = get_cache_key(idrac_ip, idrac_port, nic_id)

        module.log("Starting network attribute registry query on iDRAC {0}, "
                   "nic_id={1}, query_type={2}, attribute_pattern={3}, output_format={4}".format(
                       idrac_ip, nic_id, query_type, attribute_pattern, output_format))

        with iDRACRedfishAPI(module.params, req_session=True) as idrac:
            start_time = time.time()
            generation, firmware_version, hw_model = get_idrac_firmware_info(idrac)
            module.log("iDRAC {0}: generation={1}, firmware={2}, model={3}".format(
                idrac_ip, generation, firmware_version, hw_model))

            if not firmware_version:
                module.fail_json(msg="Unable to determine iDRAC firmware version.")

            is_compliant, min_version = check_firmware_version(firmware_version, hw_model)
            if not is_compliant:
                module.fail_json(
                    msg=FIRMWARE_TOO_OLD_MSG.format(
                        fw_version=firmware_version, min_version=min_version
                    ),
                    firmware_version=firmware_version,
                    idrac_model=hw_model,
                )

            if module.check_mode:
                module.exit_json(
                    msg="Check mode: No changes would be made. Registry query would be performed.",
                    changed=False,
                    firmware_version=firmware_version,
                    idrac_model=hw_model,
                    network_device_function_id=nic_id,
                )

            cached_data = None
            if not force_refresh:
                cached_data = get_from_cache(cache_key)

            if cached_data:
                module.log("Cache hit for {0}".format(cache_key))
                registry_data = cached_data
            else:
                module.log("Cache miss for {0}, fetching from iDRAC".format(cache_key))
                registry_data, available_nics = fetch_registry_attributes(idrac, nic_id, module=module)
                if not registry_data:
                    module.fail_json(
                        msg=NO_REGISTRY_MSG.format(
                            nic_id=nic_id, idrac_ip=idrac_ip,
                            available_nics=available_nics if available_nics else "none found"
                        ),
                        network_device_function_id=nic_id,
                        available_nics=available_nics,
                    )
                store_in_cache(cache_key, registry_data)

            all_attributes = parse_registry_attributes(registry_data)
            query_duration = round(time.time() - start_time, 2)
            module.log("Registry query completed in {0}s, {1} attributes parsed for {2}".format(
                query_duration, len(all_attributes), nic_id))

            if query_type == "validate":
                module.log("Validating {0} attribute(s)".format(len(validate_attrs)))
                validation_results = validate_attributes_against_registry(all_attributes, validate_attrs)
                module.exit_json(
                    msg=SUCCESS_VALIDATE_MSG.format(nic_id=nic_id),
                    changed=False,
                    validation_results=validation_results,
                    firmware_version=firmware_version,
                    idrac_model=hw_model,
                    output_format=output_format,
                    network_device_function_id=nic_id,
                )
            else:
                filtered = filter_by_query_type(all_attributes, query_type)
                filtered = filter_by_pattern(filtered, attribute_pattern)
                formatted = format_output(filtered, output_format)
                module.log("Query completed: {0} attributes returned (nic_id={1}, query_type={2}, "
                           "pattern={3}, duration={4}s)".format(
                               len(filtered), nic_id, query_type, attribute_pattern, query_duration))

                module.exit_json(
                    msg=SUCCESS_QUERY_MSG.format(nic_id=nic_id),
                    changed=False,
                    attributes=filtered if output_format == "json" else [],
                    attribute_count=len(filtered),
                    firmware_version=firmware_version,
                    idrac_model=hw_model,
                    output_format=output_format,
                    formatted_output=formatted,
                    network_device_function_id=nic_id,
                )

    except HTTPError as err:
        filter_err = remove_key(json.load(err), regex_pattern=ODATA_ID)
        module.exit_json(msg=str(err), error_info=filter_err, failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
