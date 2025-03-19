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

- python \>= 3.9.6



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


  username (False, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.

    If the username is not provided, then the environment variable \ :envvar:`OME\_USERNAME`\  is used.

    Example: export OME\_USERNAME=username


  password (False, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.

    If the password is not provided, then the environment variable \ :envvar:`OME\_PASSWORD`\  is used.

    Example: export OME\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`OME\_X\_AUTH\_TOKEN`\  is used.

    Example: export OME\_X\_AUTH\_TOKEN=x\_auth\_token


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.


  validate_certs (optional, bool, True)
    If \ :literal:`false`\ , the SSL certificates will not be validated.

    Configure \ :literal:`false`\  only on personally controlled sites where self-signed certificates are used.

    Prior to collection version \ :literal:`5.0.0`\ , the \ :emphasis:`validate\_certs`\  is \ :literal:`false`\  by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Retrieve basic details of all templates
      dellemc.openmanage.ome_template_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"

    - name: Retrieve details of a specific template identified by its template ID
      dellemc.openmanage.ome_template_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        template_id: 1

    - name: Get filtered template info based on name
      dellemc.openmanage.ome_template_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
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

