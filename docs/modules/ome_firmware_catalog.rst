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

- python >= 2.7.5



Parameters
----------

  state (optional, str, present)
    ``present`` creates or modifies a catalog.

    ``absent`` deletes an existing catalog.


  catalog_name (optional, list, None)
    Name of the firmware catalog to be created.

    This option is mutually exclusive with *catalog_id*.

    Provide the list of firmware catalog names that are supported when *state* is ``absent``.


  new_catalog_name (optional, str, None)
    New name of the firmware catalog.


  catalog_id (optional, list, None)
    ID of the catalog.

    This option is mutually exclusive with *catalog_name*.

    Provide the list of firmware catalog IDs that are supported when *state* is ``absent``.


  catalog_description (optional, str, None)
    Description for the catalog.


  source (optional, str, None)
    The IP address of the system where the firmware catalog is stored on the local network.

    By default, this option is set to downloads.dell.com when *repository_type* is ``DELL_ONLINE``.


  source_path (optional, str, None)
    Specify the complete path of the catalog file location without the file name.

    This is option ignored when *repository_type* is ``DELL_ONLINE``.


  file_name (optional, str, None)
    Catalog file name associated with the *source_path*.

    This option is ignored when *repository_type* is ``DELL_ONLINE``.


  repository_type (optional, str, None)
    Type of repository. The supported types are NFS, CIFS, HTTP, HTTPS,and DELL_ONLINE.


  repository_username (optional, str, None)
    User name of the repository where the catalog is stored.

    This option is mandatory when *repository_type* is CIFS.

    This option is ignored when *repository_type* is ``DELL_ONLINE``.


  repository_password (optional, str, None)
    Password to access the repository.

    This option is mandatory when *repository_type* is CIFS.

    This option is ignored when *repository_type* is ``DELL_ONLINE``.

    ``NOTE`` The module always reports the changed status, when this is provided.


  repository_domain (optional, str, None)
    Domain name of the repository.

    This option is ignored when *repository_type* is ``DELL_ONLINE``.


  check_certificate (optional, bool, False)
    The certificate warnings are ignored when *repository_type* is HTTPS. If ``True``. If not, certificate warnings are not ignored.


  job_wait (optional, bool, True)
    Provides the option to wait for job completion.

    This option is applicable when *state* is ``present``.


  job_wait_timeout (optional, int, 600)
    The maximum wait time of *job_wait* in seconds. The job is tracked only for this duration.

    This option is applicable when *job_wait* is ``True``.


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
   - If *repository_password* is provided, then the module always reports the changed status.
   - Run this module from a system that has direct access to DellEMC OpenManage Enterprise or OpenManage Enterprise Modular.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create a catalog from HTTPS repository
      dellemc.openmanage.ome_firmware_catalog:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        catalog_name: "catalog_name"
        catalog_description: "catalog_description"
        repository_type: "HTTPS"
        source: "downloads.dell.com"
        source_path: "catalog"
        file_name: "catalog.gz"
        check_certificate: True

    - name: Create a catalog from HTTP repository
      dellemc.openmanage.ome_firmware_catalog:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
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
        catalog_name: "catalog_name"
        catalog_description: "catalog_description"
        repository_type: "DELL_ONLINE"
        check_certificate: True

    - name: Modify a catalog using a repository from CIFS share
      dellemc.openmanage.ome_firmware_catalog:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
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
        catalog_id: 10
        new_catalog_name: "new_catalog_name"
        repository_type: "DELL_ONLINE"
        catalog_description: "catalog_description"

    - name: Delete catalog using catalog name
      dellemc.openmanage.ome_firmware_catalog:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        state: absent
        catalog_name: ["catalog_name1", "catalog_name2"]

    - name: Delete catalog using catalog id
      dellemc.openmanage.ome_firmware_catalog:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        state: absent
        catalog_id: [11, 34]



Return Values
-------------

msg (always, str, Successfully triggered the job to create a catalog with Task ID : 10094)
  Overall status of the firmware catalog operation.


catalog_status (When I(state) is C(present), dict, {'AssociatedBaselines': [], 'BaseLocation': None, 'BundlesCount': 0, 'Filename': 'catalog.gz', 'Id': 0, 'LastUpdated': None, 'ManifestIdentifier': None, 'ManifestVersion': None, 'NextUpdate': None, 'PredecessorIdentifier': None, 'ReleaseDate': None, 'ReleaseIdentifier': None, 'Repository': {'CheckCertificate': True, 'Description': 'HTTPS Desc', 'DomainName': None, 'Id': None, 'Name': 'catalog4', 'Password': None, 'RepositoryType': 'HTTPS', 'Source': 'company.com', 'Username': None}, 'Schedule': None, 'SourcePath': 'catalog', 'Status': None, 'TaskId': 10094})
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

