.. _idrac_bios_registry_info_module:


idrac_bios_registry_info -- Query iDRAC BIOS Attribute Registry and validate configurations
===========================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Query the iDRAC Redfish BIOS Attribute Registry endpoint to retrieve complete BIOS attribute metadata.
- Validate proposed BIOS configurations against the registry with actionable error messages.
- Filter attributes by name pattern, OEM/standard classification, and category.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  attribute_name (optional, str, None)
    Pattern to filter BIOS attributes by name (supports glob patterns).


  attribute_source (optional, str, all)
    Filter attributes by source type.

    :literal:`all` includes all attributes.

    :literal:`oem` includes OEM-specific attributes only.

    :literal:`standard` includes standard Redfish attributes only.


  category (optional, str, None)
    Filter attributes by category (e.g., 'Processor', 'Memory', 'Security').


  validate (optional, bool, False)
    Validate proposed BIOS configuration against the registry.


  attributes (optional, dict, None)
    Dictionary of attribute names and proposed values to validate.


  force_refresh (optional, bool, False)
    Force refresh of BIOS attribute registry from iDRAC, bypassing cache.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (False, str, None)
    iDRAC username.

    If the username is not provided, then the environment variable :envvar:`IDRAC\_USERNAME`\  is used.

    Example: export IDRAC\_USERNAME=username


  idrac_password (False, str, None)
    iDRAC user password.

    If the password is not provided, then the environment variable :envvar:`IDRAC\_PASSWORD`\  is used.

    Example: export IDRAC\_PASSWORD=password


  idrac_port (optional, int, 443)
    iDRAC port.


  validate_certs (optional, bool, True)
    If :literal:`false`\ , the SSL certificates will not be validated.

    Configure :literal:`false` only on personally controlled sites where self\-signed certificates are used.

    Prior to collection version :literal:`5.0.0`\ , the :emphasis:`validate\_certs`\ is :literal:`false`\ by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports IPv4 and IPv6 addresses.
   - Minimum firmware requirement: iDRAC9 >= 7.10.90.00 or iDRAC10 >= 1.20.50.50.



Examples
--------

.. code-block:: yaml+jinja

    
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



Return Values
-------------

msg (always, str, Successfully queried BIOS attribute registry.)
  Overall status message.


bios_attributes (success, list, [{'name': 'ProcVirtualization', 'display_name': 'Virtualization Technology', 'type': 'Enumeration', 'current_value': 'Enabled', 'default_value': 'Enabled', 'valid_values': ['Enabled', 'Disabled'], 'description': 'Enable or disable virtualization technology.', 'is_oem': true, 'read_only': false, 'immutable': false, 'write_only': false, 'gray_out': false, 'hidden': false, 'group': 'Processor Settings', 'menu_path': './ProcSettingsRef', 'lower_bound': None, 'upper_bound': None, 'min_length': None, 'max_length': None, 'scalar_increment': None, 'regex': None, 'value_expression': None, 'warning_text': None, 'display_order': 1, 'is_system_unique_property': False}])
  List of BIOS attributes with complete metadata.


registry_version (success, str, 1.0.0)
  Version of the BIOS attribute registry.


attribute_count (success, int, 150)
  Total number of attributes in the registry.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Sapana Gupta(@sapana05)
