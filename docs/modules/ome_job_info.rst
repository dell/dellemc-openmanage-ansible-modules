.. _ome_job_info_module:


ome_job_info -- Get job details for a given job ID or an entire job queue on OpenMange Enterprise
=================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves job details for a given job ID or an entire job queue on OpenMange Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  job_id (optional, int, None)
    Unique ID of the job.


  system_query_options (optional, dict, None)
    Options for pagination of the output.


    top (optional, int, None)
      Number of records to return. Default value is 100.


    skip (optional, int, None)
      Number of records to skip. Default value is 0.


    filter (optional, str, None)
      Filter records by the values supported.



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
    - name: Get all jobs details
      dellemc.openmanage.ome_job_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"

    - name: Get job details for id
      dellemc.openmanage.ome_job_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        job_id: 12345

    - name: Get filtered job details
      dellemc.openmanage.ome_job_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        system_query_options:
          top: 2
          skip: 1
          filter: "JobType/Id eq 8"




Return Values
-------------

msg (always, str, Successfully fetched the job info)
  Overall status of the job facts operation.


job_info (success, dict, {'value': [{'Builtin': False, 'CreatedBy': 'system', 'Editable': True, 'EndTime': None, 'Id': 12345, 'JobDescription': 'Refresh Inventory for Device', 'JobName': 'Refresh Inventory for Device', 'JobStatus': {'Id': 2080, 'Name': 'New'}, 'JobType': {'Id': 8, 'Internal': False, 'Name': 'Inventory_Task'}, 'LastRun': '2000-01-29 10:51:34.776', 'LastRunStatus': {'Id': 2060, 'Name': 'Completed'}, 'NextRun': None, 'Params': [], 'Schedule': '', 'StartTime': None, 'State': 'Enabled', 'Targets': [{'Data': "''", 'Id': 123123, 'JobId': 12345, 'TargetType': {'Id': 1000, 'Name': 'DEVICE'}}], 'UpdatedBy': None, 'Visible': True}]})
  Details of the OpenManage Enterprise jobs.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

