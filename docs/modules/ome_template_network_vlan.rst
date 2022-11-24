.. _ome_template_network_vlan_module:


ome_template_network_vlan -- Set tagged and untagged vlans to native network card supported by a template on OpenManage Enterprise
==================================================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to set tagged and untagged vlans to native network card supported by a template on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  template_name (optional, str, None)
    Name of the template.

    It is mutually exclusive with *template_id*.


  template_id (optional, int, None)
    Id of the template.

    It is mutually exclusive with *template_name*.


  nic_identifier (True, str, None)
    Display name of NIC port in the template for VLAN configuration.


  propagate_vlan (optional, bool, True)
    To deploy the modified VLAN settings immediately without rebooting the server.

    This option will be applied only when there are changes to the VLAN configuration.


  untagged_networks (optional, list, None)
    List of untagged networks and their corresponding NIC ports.


    port (True, int, None)
      NIC port number of the untagged VLAN.


    untagged_network_id (optional, int, None)
      ID of the untagged VLAN

      Enter 0 to clear the untagged VLAN from the port.

      This option is mutually exclusive with *untagged_network_name*

      To get the VLAN network ID use the API  https://*hostname*/api/NetworkConfigurationService/Networks


    untagged_network_name (optional, str, None)
      name of the vlan for untagging

      provide 0 for clearing the untagging for this *port*

      This parameter is mutually exclusive with *untagged_network_id*



  tagged_networks (optional, list, None)
    List of tagged VLANs and their corresponding NIC ports.


    port (True, int, None)
      NIC port number of the tagged VLAN


    tagged_network_ids (optional, list, None)
      List of IDs of the tagged VLANs

      Enter [] to remove the tagged VLAN from a port.

      List of *tagged_network_ids* is combined with list of *tagged_network_names* when adding tagged VLANs to a port.

      To get the VLAN network ID use the API  https://*hostname*/api/NetworkConfigurationService/Networks


    tagged_network_names (optional, list, None)
      List of names of tagged VLANs

      Enter [] to remove the tagged VLAN from a port.

      List of *tagged_network_names* is combined with list of *tagged_network_ids* when adding tagged VLANs to a port.



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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Add tagged or untagged VLANs to a template using VLAN ID and name
      dellemc.openmanage.ome_template_network_vlan:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        template_id: 78
        nic_identifier: NIC Slot 4
        untagged_networks:
          - port: 1
            untagged_network_id: 127656
          - port: 2
            untagged_network_name: vlan2
        tagged_networks:
          - port: 1
            tagged_network_ids:
              - 12767
              - 12768
          - port: 4
            tagged_network_ids:
              - 12767
              - 12768
            tagged_network_names:
              - vlan3
          - port: 2
            tagged_network_names:
              - vlan4
              - vlan1

    - name: Clear the tagged and untagged VLANs from a template
      dellemc.openmanage.ome_template_network_vlan:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        template_id: 78
        nic_identifier: NIC Slot 4
        untagged_networks:
          # For removing the untagged VLANs for the port 1 and 2
          - port: 1
            untagged_network_id: 0
          - port: 2
            untagged_network_name: 0
        tagged_networks:
          # For removing the tagged VLANs for port 1, 4 and 2
          - port: 1
            tagged_network_ids: []
          - port: 4
            tagged_network_ids: []
            tagged_network_names: []
          - port: 2
            tagged_network_names: []



Return Values
-------------

msg (always, str, Successfully applied the network settings to template.)
  Overall status of the template vlan operation.


error_info (on HTTP error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to complete the request because TemplateId  does not exist or is not applicable for the resource URI.', 'MessageArgs': ['TemplateId'], 'MessageId': 'CGEN1004', 'RelatedProperties': [], 'Resolution': "Check the request resource URI. Refer to the OpenManage Enterprise-Modular User's Guide for more information about resource URI and its properties.", 'Severity': 'Critical'}], 'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.'}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

