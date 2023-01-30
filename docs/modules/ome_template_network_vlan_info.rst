.. _ome_template_network_vlan_info_module:


ome_template_network_vlan_info -- Retrieves network configuration of template.
==============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves the network configuration of a template on OpenManage Enterprise or OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.9.6



Parameters
----------

  template_id (optional, int, None)
    Id of the template.

    This is mutually exclusive with *template_name*.


  template_name (optional, str, None)
    Name of the template.

    This is mutually exclusive with *template_id*.

    ``Note`` If *template_id* or *template_name* option is not provided, the module retrieves network VLAN info of all templates.


  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.


  password (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.


  validate_certs (optional, bool, True)
    If ``False``, the SSL certificates will not be validated.

    Configure ``False`` only on personally controlled sites where self-signed certificates are used.

    Prior to collection version ``5.0.0``, the *validate_certs* is ``False`` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module on a system that has direct access to Dell OpenManage Enterprise.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Retrieve network details of all templates.
      dellemc.openmanage.ome_template_network_vlan_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"

    - name: Retrieve network details using template ID
      dellemc.openmanage.ome_template_network_vlan_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        template_id: 1234

    - name: Retrieve network details using template name
      dellemc.openmanage.ome_template_network_vlan_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        template_name: template1



Return Values
-------------

msg (always, str, Successfully retrieved the template network VLAN information.)
  Status of template VLAN information retrieval.


vlan_info (success, list, [{'TemplateId': 58, 'TemplateName': 't2', 'NicBondingTechnology': 'LACP', 'NicModel': {'NIC in Mezzanine 1B': {'1': {'Port': 1, 'Vlan Tagged': ['25367', '32656', '32658', '26898'], 'Vlan UnTagged': '21474', 'NICBondingEnabled': 'false'}, '2': {'Port': 2, 'Vlan Tagged': [], 'Vlan UnTagged': '32658', 'NIC Bonding Enabled': 'true'}}, 'NIC in Mezzanine 1A': {'1': {'Port': 1, 'Vlan Tagged': ['32656', '32658'], 'Vlan UnTagged': '25367', 'NIC Bonding Enabled': 'true'}, '2': {'Port': 2, 'Vlan Tagged': ['21474'], 'Vlan UnTagged': '32656', 'NIC Bonding Enabled': 'false'}}}}])
  Information about the template network VLAN.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

