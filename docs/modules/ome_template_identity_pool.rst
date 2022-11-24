.. _ome_template_identity_pool_module:


ome_template_identity_pool -- Attach or detach an identity pool to a requested template on OpenManage Enterprise
================================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to- - Attach an identity pool to a requested template on OpenManage Enterprise. - Detach an identity pool from a requested template on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  template_name (True, str, None)
    Name of the template to which an identity pool is attached or detached.


  identity_pool_name (optional, str, None)
    Name of the identity pool. - To attach an identity pool to a template, provide the name of the identity pool. - This option is not applicable when detaching an identity pool from a template.


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
    - name: Attach an identity pool to a template
      dellemc.openmanage.ome_template_identity_pool:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        template_name: template_name
        identity_pool_name: identity_pool_name

    - name: Detach an identity pool from a template
      dellemc.openmanage.ome_template_identity_pool:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        template_name: template_name



Return Values
-------------

msg (always, str, Successfully attached identity pool to template.)
  Overall identity pool status of the attach or detach operation.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)

