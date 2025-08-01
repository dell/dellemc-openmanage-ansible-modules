.. _ome_firmware_catalog_module:


ome_firmware_catalog -- Create, modify, or delete a firmware catalog on OpenManage Enterprise or OpenManage Enterprise Modular
==============================================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to create, modify, or delete a firmware catalog on OpenManage Enterprise or OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  state (optional, str, present)
    \ :literal:`present`\  creates or modifies a catalog.

    \ :literal:`absent`\  deletes an existing catalog.


  catalog_name (optional, list, None)
    Name of the firmware catalog to be created.

    This option is mutually exclusive with \ :emphasis:`catalog\_id`\ .

    Provide the list of firmware catalog names that are supported when \ :emphasis:`state`\  is \ :literal:`absent`\ .


  new_catalog_name (optional, str, None)
    New name of the firmware catalog.


  catalog_id (optional, list, None)
    ID of the catalog.

    This option is mutually exclusive with \ :emphasis:`catalog\_name`\ .

    Provide the list of firmware catalog IDs that are supported when \ :emphasis:`state`\  is \ :literal:`absent`\ .


  catalog_description (optional, str, None)
    Description for the catalog.


  source (optional, str, None)
    The IP address of the system where the firmware catalog is stored on the local network.

    By default, this option is set to downloads.dell.com when \ :emphasis:`repository\_type`\  is \ :literal:`DELL\_ONLINE`\ .


  source_path (optional, str, None)
    Specify the complete path of the catalog file location without the file name.

    This is option ignored when \ :emphasis:`repository\_type`\  is \ :literal:`DELL\_ONLINE`\ .


  file_name (optional, str, None)
    Catalog file name associated with the \ :emphasis:`source\_path`\ .

    This option is ignored when \ :emphasis:`repository\_type`\  is \ :literal:`DELL\_ONLINE`\ .


  repository_type (optional, str, None)
    Type of repository. The supported types are NFS, CIFS, HTTP, HTTPS,and DELL\_ONLINE.


  repository_username (optional, str, None)
    User name of the repository where the catalog is stored.

    This option is mandatory when \ :emphasis:`repository\_type`\  is CIFS.

    This option is ignored when \ :emphasis:`repository\_type`\  is \ :literal:`DELL\_ONLINE`\ .


  repository_password (optional, str, None)
    Password to access the repository.

    This option is mandatory when \ :emphasis:`repository\_type`\  is CIFS.

    This option is ignored when \ :emphasis:`repository\_type`\  is \ :literal:`DELL\_ONLINE`\ .

    \ :literal:`NOTE`\  The module always reports the changed status, when this is provided.


  repository_domain (optional, str, None)
    Domain name of the repository.

    This option is ignored when \ :emphasis:`repository\_type`\  is \ :literal:`DELL\_ONLINE`\ .


  check_certificate (optional, bool, False)
    The certificate warnings are ignored when \ :emphasis:`repository\_type`\  is HTTPS. If \ :literal:`true`\ . If not, certificate warnings are not ignored.


  job_wait (optional, bool, True)
    Provides the option to wait for job completion.

    This option is applicable when \ :emphasis:`state`\  is \ :literal:`present`\ .


  job_wait_timeout (optional, int, 600)
    The maximum wait time of \ :emphasis:`job\_wait`\  in seconds. The job is tracked only for this duration.

    This option is applicable when \ :emphasis:`job\_wait`\  is \ :literal:`true`\ .


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
   - If \ :emphasis:`repository\_password`\  is provided, then the module always reports the changed status.
   - Run this module from a system that has direct access to Dell OpenManage Enterprise or OpenManage Enterprise Modular.
   - This module supports IPv4 and IPv6 addresses.
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create a catalog from HTTPS repository
      dellemc.openmanage.ome_firmware_catalog:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        catalog_name: "catalog_name"
        catalog_description: "catalog_description"
        repository_type: "HTTPS"
        source: "downloads.dell.com"
        source_path: "catalog"
        file_name: "catalog.gz"
        check_certificate: true

    - name: Create a catalog from HTTP repository
      dellemc.openmanage.ome_firmware_catalog:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        catalog_name: "catalog_name"
        catalog_description: "catalog_description"
        repository_type: "HTTP"
        source: "downloads.dell.com"
        source_path: "catalog"
        file_name: "catalog.gz"

    - name: Create a catalog using CIFS share
      dellemc.openmanage.ome_firmware_catalog:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        catalog_name: "catalog_name"
        catalog_description: "catalog_description"
        repository_type: "CIFS"
        source: "192.167.0.1"
        source_path: "cifs/R940"
        file_name: "catalog.gz"
        repository_username: "repository_username"
        repository_password: "repository_password"
        repository_domain: "repository_domain"

    - name: Create a catalog using NFS share
      dellemc.openmanage.ome_firmware_catalog:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        catalog_name: "catalog_name"
        catalog_description: "catalog_description"
        repository_type: "NFS"
        source: "192.166.0.2"
        source_path: "/nfs/R940"
        file_name: "catalog.xml"

    - name: Create a catalog using repository from Dell.com
      dellemc.openmanage.ome_firmware_catalog:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        catalog_name: "catalog_name"
        catalog_description: "catalog_description"
        repository_type: "DELL_ONLINE"
        check_certificate: true

    - name: Modify a catalog using a repository from CIFS share
      dellemc.openmanage.ome_firmware_catalog:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        catalog_name: "catalog_name"
        catalog_description: "new catalog_description"
        repository_type: "CIFS"
        source: "192.167.0.2"
        source_path: "cifs/R941"
        file_name: "catalog1.gz"
        repository_username: "repository_username"
        repository_password: "repository_password"
        repository_domain: "repository_domain"

    - name: Modify a catalog using a repository from Dell.com
      dellemc.openmanage.ome_firmware_catalog:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        catalog_id: 10
        new_catalog_name: "new_catalog_name"
        repository_type: "DELL_ONLINE"
        catalog_description: "catalog_description"

    - name: Delete catalog using catalog name
      dellemc.openmanage.ome_firmware_catalog:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: absent
        catalog_name: ["catalog_name1", "catalog_name2"]

    - name: Delete catalog using catalog id
      dellemc.openmanage.ome_firmware_catalog:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: absent
        catalog_id: [11, 34]



Return Values
-------------

msg (always, str, Successfully triggered the job to create a catalog with Task ID : 10094)
  Overall status of the firmware catalog operation.


catalog_status (When I(state) is C(present), dict, {'AssociatedBaselines': [], 'BaseLocation': None, 'BundlesCount': 0, 'Filename': 'catalog.gz', 'Id': 12, 'LastUpdated': None, 'ManifestIdentifier': None, 'ManifestVersion': None, 'NextUpdate': None, 'PredecessorIdentifier': None, 'ReleaseDate': None, 'ReleaseIdentifier': None, 'Repository': {'CheckCertificate': True, 'Description': 'HTTPS Desc', 'DomainName': None, 'Id': None, 'Name': 'catalog4', 'Password': None, 'RepositoryType': 'HTTPS', 'Source': 'company.com', 'Username': None}, 'Schedule': None, 'SourcePath': 'catalog', 'Status': None, 'TaskId': 10094})
  Details of the catalog operation.


job_id (When catalog job is in a running state, int, 10123)
  Job ID of the catalog task.


catalog_id (When I(state) is C(absent), int, 10123)
  IDs of the deleted catalog.


associated_baselines (When I(state) is C(absent), list, [{'BaselineId': 24, 'BaselineName': 'new'}, {'BaselineId': 25, 'BaselineName': 'c7'}, {'BaselineId': 27, 'BaselineName': 'c4'}])
  IDs of the baselines associated with catalog.


error_info (on http error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to create or update the catalog because a repository with the same name already exists.', 'Resolution': 'Enter a different name and retry the operation.', 'Severity': 'Critical'}], 'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.'}})
  Details of the http error.





Status
------





Authors
~~~~~~~

- Sajna Shetty(@Sajna-Shetty)
- Jagadeesh N V(@jagadeeshnv)
- Krunal Thakkar(@Krunal-Thakkar)

