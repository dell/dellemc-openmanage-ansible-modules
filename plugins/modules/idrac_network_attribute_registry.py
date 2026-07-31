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
  - This module queries the iDRAC Redfish network attribute registry to discover available
    network attributes with their schemas (data types, valid values, descriptions, read-only
    vs read-write status).
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
"""

EXAMPLES = """
---
- name: Query all network attributes
  dellemc.openmanage.idrac_network_attribute_registry:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    query_type: "all"

- name: Query only standard Redfish attributes
  dellemc.openmanage.idrac_network_attribute_registry:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    query_type: "redfish"

- name: Query only Dell OEM attributes
  dellemc.openmanage.idrac_network_attribute_registry:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    query_type: "oem"

- name: Filter VLAN-related attributes using wildcard
  dellemc.openmanage.idrac_network_attribute_registry:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    attribute_pattern: "VLAN*"

- name: Validate attribute name-value pairs
  dellemc.openmanage.idrac_network_attribute_registry:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    query_type: "validate"
    validate_attributes:
      VLanMode: "Enabled"
      LinkSpeed: "1Gbps"

- name: Query attributes with YAML output format
  dellemc.openmanage.idrac_network_attribute_registry:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    output_format: "yaml"

- name: Query attributes with table output format
  dellemc.openmanage.idrac_network_attribute_registry:
    idrac_ip: "192.168.0.1"
    idrac_user: "user_name"
    idrac_password: "user_password"
    output_format: "table"

- name: Query using X-Auth token for session reuse
  dellemc.openmanage.idrac_network_attribute_registry:
    idrac_ip: "192.168.0.1"
    x_auth_token: "{{ auth_token }}"
    query_type: "all"
"""

RETURN = """
---
msg:
  description: Status message for the operation.
  returned: always
  type: str
  sample: "Successfully retrieved network attribute registry."
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

REGISTRY_URI = "/redfish/v1/Registries/NetworkAttributeRegistry"
MANAGER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"
IDRAC_ATTRIBUTES_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/iDRAC.Embedded.1"

MIN_FW_IDRAC9 = "7.30.30.50"
MIN_FW_IDRAC10 = "1.30.30.50"
ODATA_ID = "(.*?)@odata"

SUCCESS_QUERY_MSG = "Successfully retrieved network attribute registry."
SUCCESS_VALIDATE_MSG = "Attribute validation completed."
FIRMWARE_TOO_OLD_MSG = (
    "iDRAC firmware version {fw_version} does not support attribute registry endpoints. "
    "Minimum required version: {min_version}. "
    "Please upgrade firmware or use manual attribute configuration."
)
NO_REGISTRY_MSG = "No network attribute registry data found on the target."
VALIDATE_REQUIRES_ATTRS_MSG = "The 'validate_attributes' parameter is required when query_type is 'validate'."
RETRY_TRANSIENT_MSG = "Transient error on attempt {attempt}/{max_retries}: {error}. Retrying in {delay}s..."
MAX_RETRIES = 3
RETRY_BASE_DELAY = 1


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


def fetch_registry_attributes(idrac, module=None):
    """Fetch raw attribute registry data from iDRAC Redfish endpoint with retry."""
    response = _invoke_with_retry(idrac, REGISTRY_URI, 'GET', module=module)
    if response.status_code != 200:
        return None

    registry_data = response.json_data
    members = registry_data.get("Members", registry_data.get("RegistryEntries", {}))

    if isinstance(members, list) and len(members) > 0:
        location = members[0] if isinstance(members[0], dict) else {}
        registry_uri = location.get("@odata.id")
        if registry_uri:
            if module:
                module.log("Fetching registry detail from: {0}".format(registry_uri))
            detail_resp = _invoke_with_retry(idrac, registry_uri, 'GET', module=module)
            if detail_resp.status_code == 200:
                return detail_resp.json_data
    elif isinstance(members, dict):
        return registry_data

    return registry_data


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
        }

        module = IdracAnsibleModule(
            argument_spec=specs,
            supports_check_mode=True,
            required_if=[["query_type", "validate", ("validate_attributes",)]],
        )

        query_type = module.params.get("query_type")
        attribute_pattern = module.params.get("attribute_pattern")
        validate_attrs = module.params.get("validate_attributes")
        output_format = module.params.get("output_format")

        idrac_ip = module.params.get("idrac_ip")
        module.log("Starting network attribute registry query on iDRAC {0}, "
                   "query_type={1}, attribute_pattern={2}, output_format={3}".format(
                       idrac_ip, query_type, attribute_pattern, output_format))

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
                )

            registry_data = fetch_registry_attributes(idrac, module=module)
            if not registry_data:
                module.fail_json(msg=NO_REGISTRY_MSG)

            all_attributes = parse_registry_attributes(registry_data)
            query_duration = round(time.time() - start_time, 2)
            module.log("Registry query completed in {0}s, {1} attributes parsed".format(
                query_duration, len(all_attributes)))

            if query_type == "validate":
                module.log("Validating {0} attribute(s)".format(len(validate_attrs)))
                validation_results = validate_attributes_against_registry(all_attributes, validate_attrs)
                module.exit_json(
                    msg=SUCCESS_VALIDATE_MSG,
                    changed=False,
                    validation_results=validation_results,
                    firmware_version=firmware_version,
                    idrac_model=hw_model,
                    output_format=output_format,
                )
            else:
                filtered = filter_by_query_type(all_attributes, query_type)
                filtered = filter_by_pattern(filtered, attribute_pattern)
                formatted = format_output(filtered, output_format)
                module.log("Query completed: {0} attributes returned (query_type={1}, "
                           "pattern={2}, duration={3}s)".format(
                               len(filtered), query_type, attribute_pattern, query_duration))

                module.exit_json(
                    msg=SUCCESS_QUERY_MSG,
                    changed=False,
                    attributes=filtered if output_format == "json" else [],
                    attribute_count=len(filtered),
                    firmware_version=firmware_version,
                    idrac_model=hw_model,
                    output_format=output_format,
                    formatted_output=formatted,
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
