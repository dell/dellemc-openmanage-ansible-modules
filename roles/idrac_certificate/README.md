# idrac_certificate

Role to manage the iDRAC certificates - Generate Certificate Signing Request, Import/Export certificates, and Reset configuration - for PowerEdge servers.

## Requirements

---

Requirements to develop and contribute to the role.

### Development

```
ansible
docker
molecule
python
```

### Production

Requirements to use the role.

```
ansible
python
```

## Ansible collections

Collections required to use the role.

```
dellemc.openmanage
```

## Role Variables

---

<table>
<thead>
  <tr>
    <th>Name</th>
    <th>Required</th>
    <th>Default Value</th>
    <th>Choices</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>hostname</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- iDRAC IP Address</td>
  </tr>
  <tr>
    <td>username</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- iDRAC username</td>
  </tr>
  <tr>
    <td>password</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- iDRAC user password.</td>
  </tr>
  <tr>
    <td>https_port</td>
    <td>false</td>
    <td>443</td>
    <td></td>
    <td>int</td>
    <td>- iDRAC port.</td>
  </tr>
  <tr>
    <td>validate_certs</td>
    <td>false</td>
    <td>true</td>
    <td></td>
    <td>bool</td>
    <td>- If C(false), the SSL certificates will not be validated.<br>- Configure C(false) only on personally controlled sites where self-signed certificates are used.</td>
  </tr>
  <tr>
    <td>ca_path</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>path</td>
    <td>- The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.</td>
  </tr>
  <tr>
    <td>https_timeout</td>
    <td>false</td>
    <td>30</td>
    <td></td>
    <td>int</td>
    <td>- The socket level timeout in seconds.</td>
  </tr>
    <tr>
    <td>command</td>
    <td>false</td>
    <td>generate_csr</td>
    <td>'import', 'export', 'generate_csr', 'reset'</td>
    <td>str</td>
    <td>- C(generate_csr), generate CSR. This requires I(cert_params) and I(certificate_path).
    <br>- C(import), import the certificate file. This requires I(certificate_path).
    <br>- C(export), export the certificate. This requires I(certificate_path).
    <br>- C(reset), reset the certificate to default settings. This is applicable only for C(HTTPS).
    </td>
  </tr>
  <tr>
    <td>certificate_type</td>
    <td>false</td>
    <td>HTTPS</td>
    <td>'HTTPS', 'CA', 'CSC', 'CLIENT_TRUST_CERTIFICATE', 'CUSTOMCERTIFICATE'</td>
    <td>str</td>
    <td>-Type of the iDRAC certificate:
      <br>- C(HTTPS) The Dell self-signed SSL certificate.
      <br>- C(CA) Certificate Authority(CA) signed SSL certificate.
      <br>- C(CSC) The custom signed SSL certificate.
      <br>- C(CLIENT_TRUST_CERTIFICATE) Client trust certificate.
      <br>- C(CUSTOMCERTIFICATE) The custom PKCS12 certificate and private key. Export of custom certificate is supported only on iDRAC firmware version 7.00.00.00 and above.</td>
  </tr>
  <tr>
    <td>certificate_path</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>path</td>
    <td>- Absolute path of the certificate file if I(command) is C(import).
    <br>- Directory path with write permissions if I(command) is C(generate_csr) or C(export).<br></td>
  </tr>
  <tr>
    <td>passpharse</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- The passphrase string if the certificate to be imported is passphrase protected.</td>
  </tr>
  <tr>
    <td>ssl_key</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>path</td>
    <td>- Absolute path of the private or SSL key file.
    <br>- This is applicable only when I(command) is C(import) and I(certificate_type) is C(HTTPS).
    <br>- Uploading the SSL key on iDRAC is supported on version 6.00.02.00 and newer versions.<br></td>
  </tr>
  <tr>
    <td>cert_params</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>dict</td>
    <td></td>
  </tr>
    <tr>
      <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;common_name</td>
      <td>false</td>
      <td></td>
      <td></td>
      <td>str</td>
      <td>- The common name of the certificate.</td>
    </tr>
    <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;organization_unit</td>
    <td>false</td>
    <td>true</td>
    <td></td>
    <td>str</td>
    <td>- The name associated with an organizational unit. For example, department name.</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;locality_name</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- The city or other location where the entity applying for certification is located.</td>
    </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;state_name</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- The state where the entity applying for certification is located.</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;country_code</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td> - The country code of the country where the entity applying for certification is located.</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;email_address</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- The email associated with the CSR.</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;organization_name</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- The name associated with an organization.</td>
    </tr>
     <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;subject_alt_name</td>
    <td>false</td>
    <td>[]</td>
    <td></td>
    <td>list</td>
    <td>- The alternative domain names associated with the request.</td>
  </tr>
    <tr>
    <td>resource_id</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Redfish ID of the resource.</td>
  </tr>
  <tr>
    <td>reset</td>
    <td>false</td>
    <td>true</td>
    <td></td>
    <td>bool</td>
    <td>- To reset the iDRAC after the certificate operation.<br>- This is applicable when I(command) is C(import) or C(reset).<br></td>
  </tr>
  <tr>
    <td>wait</td>
    <td>false</td>
    <td>300</td>
    <td></td>
    <td>bool</td>
    <td>- Maximum wait time for iDRAC to start after the reset, in seconds.<br>- This is applicable when I(command) is C(import) or C(reset) and I(reset) is C(True).<br></td>
  </tr>
</tbody>
</table>

## Fact variables

<table>
<thead>
  <tr>
    <th>Name</th>
    <th>Sample</th>
    <th>Description</th>
  </tr>
</thead>
  <tbody>
    <tr>
      <td>idrac_certificate_out</td>
      <td>{
"certificate_path": "/root/Certs/192.168.0.1_202333_4130_HTTPS.pem",
    "changed": false,
    "msg": "Successfully performed the 'export' operation."
}</td>
      <td>Module output of the cerificate export job.</td>
    </tr>
  </tbody>
</table>

## Examples

---

```
- name: Generate HTTPS certificate signing request
  ansible.builtin.import_role:
    name: idrac_certificate
  vars:
    hostname: "192.168.0.1"
    username: "user_name"
    password: "user_password"
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
```

```
- name: Importing certificate.
  ansible.builtin.import_role:
    name: idrac_certificate
  vars:
    hostname: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "import"
    certificate_type: "HTTPS"
    certificate_path: "/path/to/cert.pem"
```

```
- name: Exporting certificate.
  ansible.builtin.import_role:
    name: idrac_certificate
  vars:
    hostname: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "export"
    certificate_type: "HTTPS"
    certificate_path: "/home/omam/mycert_dir"
```

```
- name: Importing Custom Signing Certificate.
  ansible.builtin.import_role:
    name: idrac_certificate
  vars:
    hostname: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "import"
    certificate_type: "CSC"
    certificate_path: "/path/to/cert.pem"
```

```
- name: Import an HTTPS certificate with private key.
  ansible.builtin.import_role:
    name: idrac_certificate
  vars:
    hostname: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "import"
    certificate_type: "HTTPS"
    certificate_path: "/path/to/cert.pem"
    ssl_key: "/path/to/ssl_key"
```

```
- name: Exporting certificate.
  ansible.builtin.import_role:
    name: idrac_certificate
  vars:
    hostname: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    command: "export"
    certificate_type: "CLIENT_TRUST_CERTIFICATE"
    certificate_path: "/home/omam/mycert_dir"
```

## Author Information
---
Dell Technologies <br>
Shivam Sharma (Shivam.Sharma3@Dell.com) 2023<br>
Jagadeesh N V (Jagadeesh.N.V@Dell.com) 2023
