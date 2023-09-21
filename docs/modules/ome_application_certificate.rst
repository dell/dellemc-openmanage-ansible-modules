.. _ome_application_certificate_module:


ome_application_certificate -- This module allows to generate a CSR and upload the certificate
==============================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows the generation a new certificate signing request (CSR) and to upload the certificate on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.9.6



Parameters
----------

  command (optional, str, generate_csr)
    ``generate_csr`` allows the generation of a CSR and ``upload`` uploads the certificate.


  distinguished_name (optional, str, None)
    Name of the certificate issuer. This option is applicable for ``generate_csr``.


  department_name (optional, str, None)
    Name of the department that issued the certificate. This option is applicable for ``generate_csr``.


  business_name (optional, str, None)
    Name of the business that issued the certificate. This option is applicable for ``generate_csr``.


  locality (optional, str, None)
    Local address of the issuer of the certificate. This option is applicable for ``generate_csr``.


  country_state (optional, str, None)
    State in which the issuer resides. This option is applicable for ``generate_csr``.


  country (optional, str, None)
    Country in which the issuer resides. This option is applicable for ``generate_csr``.


  email (optional, str, None)
    Email associated with the issuer. This option is applicable for ``generate_csr``.


  subject_alternative_names (optional, str, None)
    Subject alternative name required for the certificate signing request generation.

    Supports up to 4 comma separated values starting from primary, secondary, Tertiary and Quaternary values.


  upload_file (optional, str, None)
    Local path of the certificate file to be uploaded. This option is applicable for ``upload``. Once the certificate is uploaded, OpenManage Enterprise cannot be accessed for a few seconds.


  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.


  password (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.


  validate_certs (optional, bool, True)
    If ``false``, the SSL certificates will not be validated.

    Configure ``false`` only on personally controlled sites where self-signed certificates are used.

    Prior to collection version ``5.0.0``, the *validate_certs* is ``false`` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - If a certificate is uploaded, which is identical to an already existing certificate, it is accepted by the module.
   - This module does not support ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Generate a certificate signing request
      dellemc.openmanage.ome_application_certificate:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: "generate_csr"
        distinguished_name: "hostname.com"
        department_name: "Remote Access Group"
        business_name: "Dell Inc."
        locality: "Round Rock"
        country_state: "Texas"
        country: "US"
        email: "support@dell.com"

    - name: Generate a certificate signing request with subject alternative names
      dellemc.openmanage.ome_application_certificate:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: "generate_csr"
        distinguished_name: "hostname.com"
        subject_alternative_names: "hostname1.chassis.com,hostname2.chassis.com"
        department_name: "Remote Access Group"
        business_name: "Dell Inc."
        locality: "Round Rock"
        country_state: "Texas"
        country: "US"
        email: "support@dell.com"

    - name: Upload the certificate
      dellemc.openmanage.ome_application_certificate:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        command: "upload"
        upload_file: "/path/certificate.cer"



Return Values
-------------

msg (always, str, Successfully generated certificate signing request.)
  Overall status of the certificate signing request.


csr_status (on success, dict, {'CertificateData': '-----BEGIN CERTIFICATE REQUEST-----GHFSUEKLELE af3u4h2rkdkfjasczjfefhkrr/frjrfrjfrxnvzklf/nbcvxmzvndlskmcvbmzkdk kafhaksksvklhfdjtrhhffgeth/tashdrfstkm@kdjFGD/sdlefrujjfvvsfeikdf yeufghdkatbavfdomehtdnske/tahndfavdtdfgeikjlagmdfbandfvfcrfgdtwxc qwgfrteyupojmnsbajdkdbfs/ujdfgthedsygtamnsuhakmanfuarweyuiwruefjr etwuwurefefgfgurkjkdmbvfmvfvfk==-----END CERTIFICATE REQUEST-----'})
  Details of the generated certificate.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'CSEC9002', 'RelatedProperties': [], 'Message': 'Unable to upload the certificate because the certificate file provided is invalid.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Make sure the CA certificate and private key are correct and retry the operation.'}]}})
  Details of the HTTP error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)
- Kritika Bhateja (@Kritika-Bhateja-03)
- Jennifer John (@Jennifer-John)

