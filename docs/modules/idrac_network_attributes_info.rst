.. _idrac_network_attributes_info_module:


idrac_network_attributes_info -- Query and validate iDRAC Network Attribute Registry for a specific NIC
=======================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Query the Dell OEM DellNetworkAttributes endpoint and NetworkAttributesRegistry for a specific network device function (NIC).

Returns full attribute schema with current values, supporting attribute name filtering and OEM vs. standard attribute classification.

Supports both iDRAC9 (16G) and iDRAC10 (17G) via dynamic URI resolution.

When :literal:`validate=true` and :literal:`attributes` is provided, validates each user\-supplied attribute name\-value pair against the registry and returns a consolidated report with fuzzy match suggestions for misspelled attribute names.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  network_device_function_id (True, str, None)
    FQDD of the network device function to query attributes for.

    Example: :literal:`NIC.Embedded.1\-1\-1`.

    If the specified ID does not exist, the module returns an error including a list of valid NIC IDs discovered on the iDRAC.


  attribute_name (False, str, None)
    Pattern to filter attributes by name (supports glob patterns via fnmatch).


  attribute_source (False, str, all)
    Filter attributes by source type.


  force_refresh (False, bool, False)
    Force refresh of attribute registry data, bypassing the in\-memory cache.


  validate (False, bool, False)
    When set to :literal:`true`\ , validates the attribute name\-value pairs provided in :emphasis:`attributes` against the attribute registry for the specified NIC.

    Returns a consolidated validation report with per\-attribute status.

    Requires :emphasis:`attributes` to be provided.


  attributes (False, dict, None)
    Dictionary of attribute name\-value pairs to validate against the registry.

    Required when :emphasis:`validate=true`.

    Example: :literal:`{VLanMode: Enabled, VLanId: 100}`.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.

    If the username is not provided, then the environment variable :envvar:`IDRAC\_USERNAME` is used.

    Example: export IDRAC\_USERNAME=username


  idrac_password (True, str, None)
    iDRAC user password.

    If the password is not provided, then the environment variable :envvar:`IDRAC\_PASSWORD` is used.

    Example: export IDRAC\_PASSWORD=password


  idrac_port (optional, int, 443)
    iDRAC port.


  validate_certs (optional, bool, True)
    If :literal:`false`\ , the SSL certificates will not be validated.

    Configure :literal:`false` only on personally controlled sites where self\-signed certificates are used.

    Prior to collection version :literal:`5.0.0`\ , the :emphasis:`validate\_certs` is :literal:`false` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports both IPv4 and IPv6 address for :emphasis:`idrac\_ip`.
   - This module is read\-only and always returns changed=false.
   - Use idrac\_network\_info to discover valid NIC IDs before calling this module.




Examples
--------

.. code-block:: yaml+jinja

    
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

    - name: Validate attribute values before applying
      dellemc.openmanage.idrac_network_attributes_info:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        network_device_function_id: "NIC.Embedded.1-1-1"
        validate: true
        attributes:
          VLanMode: "Enabled"
          VLanId: "100"

    - name: Batch validate with fuzzy match suggestions for misspelled names
      dellemc.openmanage.idrac_network_attributes_info:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        network_device_function_id: "NIC.Embedded.1-1-1"
        validate: true
        attributes:
          VLanMoed: "Enabled"
          VLanId: "99999"

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



Return Values
-------------

msg (always, str, Successfully queried network attribute registry.)
  Overall status message.


network_attributes (success, list, [{'name': 'VLanMode', 'type': 'Enumeration', 'current_value': 'Disabled', 'default_value': 'Disabled', 'valid_values': ['Disabled', 'Enabled'], 'description': 'Enable or disable VLAN mode.', 'is_oem': True, 'read_only': False, 'requires_reboot': False, 'dependencies': []}])
  List of network attributes with complete metadata.


network_device_function_id (success, str, NIC.Embedded.1-1-1)
  The NIC FQDD that was queried.


attribute_registry (success, str, NetworkAttributesRegistry_NIC.Embedded.1-1-1)
  Name of the attribute registry used.


attribute_count (success, int, 85)
  Total number of attributes returned (after filtering).


idrac_generation (success, int, 16)
  PowerEdge server generation (14G\-16G for iDRAC9, 17G+ for iDRAC10).


idrac_firmware_version (success, str, 7.30.30.50)
  iDRAC firmware version.


idrac_model (success, str, iDRAC 9)
  iDRAC model identifier.


valid (when validate=true, bool, False)
  Whether all submitted attributes passed validation.


valid_count (when validate=true, int, 1)
  Number of attributes that passed validation.


invalid_count (when validate=true, int, 1)
  Number of attributes that failed validation.


validation_results (when validate=true, list, [{'attribute': 'VLanMode', 'status': 'valid', 'reason': "Value 'Enabled' is valid for enumeration attribute.", 'suggestions': []}, {'attribute': 'VLanMoed', 'status': 'invalid', 'reason': 'Attribute not found.', 'suggestions': ['VLanMode', 'VLanId']}])
  Per\-attribute validation results.


redfish_error (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred.'}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Mangirish Kenkare(@MangirishK)

