.. _ome_active_directory_module:


ome_active_directory -- Configure Active Directory groups to be used with Directory Services
============================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to add, modify, and delete OpenManage Enterprise connection with Active Directory Service.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  domain_server (optional, list, None)
    Enter the domain name or FQDN or IP address of the domain controller.

    If *domain_controller_lookup* is ``DNS``, enter the domain name to query DNS for the domain controllers.

    If *domain_controller_lookup* is ``MANUAL``, enter the FQDN or the IP address of the domain controller. The maximum number of Active Directory servers that can be added is three.


  domain_controller_lookup (optional, str, DNS)
    Select the Domain Controller Lookup method.


  domain_controller_port (optional, int, 3269)
    Domain controller port.

    By default, Global Catalog Address port number 3269 is populated.

    For the Domain Controller Access, enter 636 as the port number.

    ``NOTE``, Only LDAPS ports are supported.


  group_domain (optional, str, None)
    Provide the group domain in the format ``example.com`` or ``ou=org, dc=example, dc=com``.


  id (optional, int, None)
    Provide the ID of the existing Active Directory service connection.

    This is applicable for modification and deletion.

    This is mutually exclusive with *name*.


  name (optional, str, None)
    Provide a name for the Active Directory connection.

    This is applicable for creation and deletion.

    This is mutually exclusive with *name*.


  network_timeout (optional, int, 120)
    Enter the network timeout duration in seconds.

    The supported timeout duration range is 15 to 300 seconds.


  search_timeout (optional, int, 120)
    Enter the search timeout duration in seconds.

    The supported timeout duration range is 15 to 300 seconds.


  state (optional, str, present)
    ``present`` allows to create or modify an Active Directory service.

    ``absent`` allows to delete a Active Directory service.


  test_connection (optional, bool, False)
    Enables testing the connection to the domain controller.

    The connection to the domain controller is tested with the provided Active Directory service details.

    If test fails, module will error out.

    If ``yes``, *domain_username* and *domain_password* has to be provided.


  domain_password (optional, str, None)
    Provide the domain password.

    This is applicable when *test_connection* is ``yes``.


  domain_username (optional, str, None)
    Provide the domain username either in the UPN (username@domain) or NetBIOS (domain\\username) format.

    This is applicable when *test_connection* is ``yes``.


  validate_certificate (optional, bool, False)
    Enables validation of SSL certificate of the domain controller.

    The module will always report change when this is ``yes``.


  certificate_file (optional, path, None)
    Provide the full path of the SSL certificate.

    The certificate should be a Root CA Certificate encoded in Base64 format.

    This is applicable when *validate_certificate* is ``yes``.


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
   - The module will always report change when *validate_certificate* is ``yes``.
   - Run this module from a system that has direct access to OpenManage Enterprise.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Add Active Directory service using DNS lookup along with the test connection
      dellemc.openmanage.ome_active_directory:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        name: my_ad1
        domain_server:
          - domainname.com
        group_domain: domainname.com
        test_connection: yes
        domain_username: user@domainname
        domain_password: domain_password

    - name: Add Active Directory service using IP address of the domain controller with certificate validation
      dellemc.openmanage.ome_active_directory:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        name: my_ad2
        domain_controller_lookup: MANUAL
        domain_server:
          - 192.68.20.181
        group_domain: domainname.com
        validate_certificate: yes
        certificate_file: "/path/to/certificate/file.cer"

    - name: Modify domain controller IP address, network_timeout and group_domain
      dellemc.openmanage.ome_active_directory:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        name: my_ad2
        domain_controller_lookup: MANUAL
        domain_server:
          - 192.68.20.189
        group_domain: newdomain.in
        network_timeout: 150

    - name: Delete Active Directory service
      dellemc.openmanage.ome_active_directory:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        name: my_ad2
        state: absent

    - name: Test connection to existing Active Directory service with certificate validation
      dellemc.openmanage.ome_active_directory:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        name: my_ad2
        test_connection: yes
        domain_username: user@domainname
        domain_password: domain_password
        validate_certificate: yes
        certificate_file: "/path/to/certificate/file.cer"



Return Values
-------------

msg (always, str, Successfully renamed the slot(s).)
  Overall status of the Active Directory operation.


active_directory (on change, dict, {'Name': 'ad_test', 'Id': 21789, 'ServerType': 'MANUAL', 'ServerName': ['192.168.20.181'], 'DnsServer': [], 'GroupDomain': 'dellemcdomain.com', 'NetworkTimeOut': 120, 'Password': None, 'SearchTimeOut': 120, 'ServerPort': 3269, 'CertificateValidation': False})
  The Active Directory that was added, modified or deleted by this module.


error_info (on HTTP error, dict, {'error_info': {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to connect to the LDAP or AD server because the entered credentials are invalid.', 'MessageArgs': [], 'MessageId': 'CSEC5002', 'RelatedProperties': [], 'Resolution': 'Make sure the server input configuration are valid and retry the operation.', 'Severity': 'Critical'}], 'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.'}}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

