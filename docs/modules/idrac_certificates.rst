.. _idrac_certificates_module:


idrac_certificates -- Configure certificates for iDRAC
======================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to generate certificate signing request, import, and export certificates on iDRAC.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  command (optional, str, generate_csr)
    ``generate_csr``, generate CSR. This requires *cert_params* and *certificate_path*. This is applicable only for ``HTTPS``

    ``import``, import the certificate file. This requires *certificate_path*.

    ``export``, export the certificate. This requires *certificate_path*.

    ``reset``, reset the certificate to default settings. This is applicable only for ``HTTPS``.


  certificate_type (optional, str, HTTPS)
    Type of the iDRAC certificate.

    ``HTTPS`` The Dell self-signed SSL certificate.

    ``CA`` Certificate Authority(CA) signed SSL certificate.

    ``CSC`` The custom signed SSL certificate.

    ``CLIENT_TRUST_CERTIFICATE`` Client trust certificate.


  certificate_path (optional, path, None)
    Absolute path of the certificate file if *command* is ``import``.

    Directory path with write permissions if *command* is ``generate_csr`` or ``export``.


  passphrase (optional, str, None)
    The passphrase string if the certificate to be imported is passphrase protected.


  cert_params (optional, dict, None)
    Certificate parameters to generate signing request.


    common_name (True, str, None)
      The common name of the certificate.


    organization_unit (True, str, None)
      The name associated with an organizational unit. For example department name.


    locality_name (True, str, None)
      The city or other location where the entity applying for certification is located.


    state_name (True, str, None)
      The state where the entity applying for certification is located.


    country_code (True, str, None)
      The country code of the country where the entity applying for certification is located.


    email_address (True, str, None)
      The email associated with the CSR.


    organization_name (True, str, None)
      The name associated with an organization.


    subject_alt_name (optional, list, [])
      The alternative domain names associated with the request.



  resource_id (optional, str, None)
    Redfish ID of the resource.


  reset (optional, bool, True)
    To reset the iDRAC after the certificate operation.

    This is applicable when *command* is ``import`` or ``reset``.


  wait (optional, int, 300)
    Maximum wait time for iDRAC to start after the reset, in seconds.

    This is applicable when *command* is ``import`` or ``reset`` and *reset* is ``True``.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.


  idrac_password (True, str, None)
    iDRAC user password.


  idrac_port (optional, int, 443)
    iDRAC port.


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
   - The certificate operations are supported on iDRAC firmware 5.10.10.00 and above.
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Generate HTTPS certificate signing request
      dellemc.openmanage.idrac_certificates:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        command: "generate_csr"
        certificate_type: "HTTPS"
        certificate_path: "/home/omam/mycerts"
        cert_params:
          common_name: "sample.domain.com"
          organization_unit: "OrgUnit"
          locality_name: "Bangalore"
          state_name: "Karnataka"
          country_code: "IN"
          email_address: "admin@domain.com"
          organization_name: "OrgName"
          subject_alt_name:
            - 192.198.2.1

    - name: Import a HTTPS certificate.
      dellemc.openmanage.idrac_certificates:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        command: "import"
        certificate_type: "HTTPS"
        certificate_path: "/path/to/cert.pem"

    - name: Export a HTTPS certificate.
      dellemc.openmanage.idrac_certificates:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        command: "export"
        certificate_type: "HTTPS"
        certificate_path: "/home/omam/mycert_dir"

    - name: Import a CSC certificate.
      dellemc.openmanage.idrac_certificates:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        command: "import"
        certificate_type: "CSC"
        certificate_path: "/path/to/cert.pem"

    - name: Export a Client trust certificate.
      dellemc.openmanage.idrac_certificates:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        command: "export"
        certificate_type: "CLIENT_TRUST_CERTIFICATE"
        certificate_path: "/home/omam/mycert_dir"



Return Values
-------------

msg (always, str, Successfully performed the operation generate_csr.)
  Status of the certificate configuration operation.


certificate_path (when I(command) is C(export) or C(generate_csr), str, /home/ansible/myfiles/cert.pem)
  The csr or exported certificate file path


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

