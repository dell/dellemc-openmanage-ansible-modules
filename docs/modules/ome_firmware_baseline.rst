.. _ome_firmware_baseline_module:


ome_firmware_baseline -- Create, modify, or delete a firmware baseline on OpenManage Enterprise or OpenManage Enterprise Modular
================================================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to create, modify, or delete a firmware baseline on OpenManage Enterprise or OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7.5



Parameters
----------

  state (optional, str, present)
    ``present`` creates or modifies a baseline.

    ``absent`` deletes an existing baseline.


  baseline_name (optional, str, None)
    Name of the the baseline.

    This option is mutually exclusive with *baseline_id*.


  baseline_id (optional, int, None)
    ID of the existing baseline.

    This option is mutually exclusive with *baseline_name*.


  new_baseline_name (optional, str, None)
    New name of the baseline.


  baseline_description (optional, str, None)
    Description for the baseline being created.


  catalog_name (optional, str, None)
    Name of the catalog to be associated with the baseline.


  downgrade_enabled (optional, bool, None)
    Indicates whether firmware downgrade is allowed for the devices in the baseline.

    This value will be set to ``True`` by default, if not provided during baseline creation.


  is_64_bit (optional, bool, None)
    Indicates if the repository contains 64-bit DUPs.

    This value will be set to ``True`` by default, if not provided during baseline creation.


  device_ids (optional, list, None)
    List of device IDs.

    This option is mutually exclusive with *device_service_tags* and *device_group_names*.


  device_service_tags (optional, list, None)
    List of device service tags.

    This option is mutually exclusive with *device_ids* and *device_group_names*.


  device_group_names (optional, list, None)
    List of group names.

    This option is mutually exclusive with *device_ids* and *device_service_tags*.


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
   - Run this module from a system that has direct access to DellEMC OpenManage Enterprise or OpenManage Enterprise Modular.
   - *device_group_names* option is not applicable for OpenManage Enterprise Modular.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create baseline for device IDs
      dellemc.openmanage.ome_firmware_baseline:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        baseline_name: "baseline_name"
        baseline_description: "baseline_description"
        catalog_name: "catalog_name"
        device_ids:
          - 1010
          - 2020

    - name: Create baseline for servicetags
      dellemc.openmanage.ome_firmware_baseline:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        baseline_name: "baseline_name"
        baseline_description: "baseline_description"
        catalog_name: "catalog_name"
        device_service_tags:
          - "SVCTAG1"
          - "SVCTAG2"

    - name: Create baseline for device groups without job tracking
      dellemc.openmanage.ome_firmware_baseline:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        baseline_name: "baseline_name"
        baseline_description: "baseline_description"
        catalog_name: "catalog_name"
        device_group_names:
          - "Group1"
          - "Group2"
        job_wait: no

    - name: Modify an existing baseline
      dellemc.openmanage.ome_firmware_baseline:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        baseline_name: "existing_baseline_name"
        new_baseline_name: "new_baseline_name"
        baseline_description: "new baseline_description"
        catalog_name: "catalog_other"
        device_group_names:
          - "Group3"
          - "Group4"
          - "Group5"
        downgrade_enabled: no
        is_64_bit: yes

    - name: Delete a baseline
      dellemc.openmanage.ome_firmware_baseline:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        state: absent
        baseline_name: "baseline_name"



Return Values
-------------

msg (always, str, Successfully created the firmware baseline.)
  Overall status of the firmware baseline operation.


baseline_status (success, dict, {'CatalogId': 123, 'Description': 'BASELINE DESCRIPTION', 'DeviceComplianceReports': [], 'DowngradeEnabled': True, 'Id': 23, 'Is64Bit': True, 'Name': 'my_baseline', 'RepositoryId': 123, 'RepositoryName': 'catalog123', 'RepositoryType': 'HTTP', 'Targets': [{'Id': 10083, 'Type': {'Id': 1000, 'Name': 'DEVICE'}}, {'Id': 10076, 'Type': {'Id': 1000, 'Name': 'DEVICE'}}], 'TaskId': 11235, 'TaskStatusId': 2060})
  Details of the baseline status.


job_id (When baseline job is in running state, int, 10123)
  Job ID of the baseline task.


baseline_id (When I(state) is C(absent), int, 10123)
  ID of the deleted baseline.


error_info (on http error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to retrieve baseline list either because the device ID(s) entered are invalid', 'Resolution': 'Make sure the entered device ID(s) are valid and retry the operation.', 'Severity': 'Critical'}], 'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.'}})
  Details of http error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

