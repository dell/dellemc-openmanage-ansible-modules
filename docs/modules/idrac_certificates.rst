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

- python \>= 3.9.6



Parameters
----------

  command (optional, str, generate_csr)
    \ :literal:`generate\_csr`\ , generate CSR. This requires \ :emphasis:`cert\_params`\  and \ :emphasis:`certificate\_path`\ . This is applicable only for \ :literal:`HTTPS`\ 

    \ :literal:`import`\ , import the certificate file. This requires \ :emphasis:`certificate\_path`\ .

    \ :literal:`export`\ , export the certificate. This requires \ :emphasis:`certificate\_path`\ .

    \ :literal:`reset`\ , reset the certificate to default settings. This is applicable only for \ :literal:`HTTPS`\ .


  certificate_type (optional, str, HTTPS)
    Type of the iDRAC certificate.

    \ :literal:`HTTPS`\  The Dell self-signed SSL certificate.

    \ :literal:`CA`\  Certificate Authority(CA) signed SSL certificate.

    \ :literal:`CUSTOMCERTIFICATE`\  The custom PKCS12 certificate and private key. Export of custom certificate is supported only on iDRAC firmware version 7.00.00.00 and above.

    \ :literal:`CSC`\  The custom signing SSL certificate.

    \ :literal:`CLIENT\_TRUST\_CERTIFICATE`\  Client trust certificate.


  certificate_path (optional, path, None)
    Absolute path of the certificate file if \ :emphasis:`command`\  is \ :literal:`import`\ .

    Directory path with write permissions if \ :emphasis:`command`\  is \ :literal:`generate\_csr`\  or \ :literal:`export`\ .


  passphrase (optional, str, None)
    The passphrase string if the certificate to be imported is passphrase protected.


  ssl_key (optional, path, None)
    Absolute path of the private or SSL key file.

    This is applicable only when \ :emphasis:`command`\  is \ :literal:`import`\  and \ :emphasis:`certificate\_type`\  is \ :literal:`HTTPS`\ .

    Uploading the SSL key to iDRAC is supported on firmware version 6.00.02.00 and above.


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


    email_address (optional, str, None)
      The email associated with the CSR.


    organization_name (True, str, None)
      The name associated with an organization.


    subject_alt_name (optional, list, [])
      The alternative domain names associated with the request.



  resource_id (optional, str, None)
    Redfish ID of the resource.


  reset (optional, bool, True)
    To reset the iDRAC after the certificate operation.

    This is applicable when \ :emphasis:`command`\  is \ :literal:`import`\  or \ :literal:`reset`\ .


  wait (optional, int, 600)
    Maximum wait time for iDRAC to start after the reset, in seconds.

    This is applicable when \ :emphasis:`command`\  is \ :literal:`import`\  or \ :literal:`reset`\  and \ :emphasis:`reset`\  is \ :literal:`true`\ .


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (False, str, None)
    iDRAC username.

    If the username is not provided, then the environment variable \ :envvar:`IDRAC\_USERNAME`\  is used.

    Example: export IDRAC\_USERNAME=username


  idrac_password (False, str, None)
    iDRAC user password.

    If the password is not provided, then the environment variable \ :envvar:`IDRAC\_PASSWORD`\  is used.

    Example: export IDRAC\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`IDRAC\_X\_AUTH\_TOKEN`\  is used.

    Example: export IDRAC\_X\_AUTH\_TOKEN=x\_auth\_token


  idrac_port (optional, int, 443)
    iDRAC port.


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
   - The certificate operations are supported on iDRAC firmware version 6.10.80.00 and above.
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports \ :literal:`check\_mode`\ .
   - This module supports IPv4 and IPv6 addresses.




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

    - name: Import an HTTPS certificate along with its private key.
      dellemc.openmanage.idrac_certificates:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        command: "import"
        certificate_type: "HTTPS"
        certificate_path: "/path/to/cert.pem"
        ssl_key: "/path/to/private_key.pem"

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

    - name: Import a custom certificate with a passphrase.
      dellemc.openmanage.idrac_certificates:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        command: "import"
        certificate_type: "CUSTOMCERTIFICATE"
        certificate_path: "/path/to/idrac_cert.p12"
        passphrase: "cert_passphrase"
        reset: false

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

msg (always, str, Successfully performed the 'generate_csr' certificate operation.)
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
- Rajshekar P(@rajshekarp87)
- Kristian Lamb V(@kristian_lamb)

