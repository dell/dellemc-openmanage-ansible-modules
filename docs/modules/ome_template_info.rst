.. _ome_template_info_module:


ome_template_info -- Retrieves template details from OpenManage Enterprise
==========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves the list and details of all the templates on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7.5



Parameters
----------

  template_id (optional, int, None)
    Unique Id of the template.


  system_query_options (optional, dict, None)
    Options for pagination of the output.


    filter (optional, str, None)
      Filter records by the supported values.



  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.


  password (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.





Notes
-----

.. note::
   - Run this module from a system that has direct access to DellEMC OpenManage Enterprise.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Retrieve basic details of all templates
      dellemc.openmanage.ome_template_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"

    - name: Retrieve details of a specific template identified by its template ID
      dellemc.openmanage.ome_template_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        template_id: 1

    - name: Get filtered template info based on name
      dellemc.openmanage.ome_template_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        system_query_options:
          filter: "Name eq 'new template'"



Return Values
-------------

msg (on error, str, Failed to fetch the template facts)
  Overall template facts status.


template_info (success, dict, {'192.168.0.1': {'CreatedBy': 'system', 'CreationTime': '1970-01-31 00:00:56.372144', 'Description': 'Tune workload for Performance Optimized Virtualization', 'HasIdentityAttributes': False, 'Id': 1, 'IdentityPoolId': 0, 'IsBuiltIn': True, 'IsPersistencePolicyValid': False, 'IsStatelessAvailable': False, 'LastUpdatedBy': None, 'LastUpdatedTime': '1970-01-31 00:00:56.372144', 'Name': 'iDRAC Enable Performance Profile for Virtualization', 'SourceDeviceId': 0, 'Status': 0, 'TaskId': 0, 'TypeId': 2, 'ViewTypeId': 4}})
  Details of the templates.





Status
------





Authors
~~~~~~~

- Sajna Shetty(@Sajna-Shetty)

