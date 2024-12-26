.. _omevv_firmware_module:


omevv_firmware -- Update the firmware of a specific host in the cluster
=======================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows you to update the firmware of a specific host in the cluster.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  check_vSAN_health (optional, bool, None)
    Check vSAN health while updating the firmware.

    \ :literal:`true`\  checks the vSAN health while updating the firmware.

    \ :literal:`false`\  does not check the vSAN health while updating the firmware.


  date_time (optional, str, None)
    Date and time when the job must run. This is applicable when \ :emphasis:`run\_now`\  is \ :literal:`false`\ .

    The supported format is YYYY-MM-DDThh:mm:ss\<offset\>.


  delete_job_queue (optional, bool, None)
    Whether to delete the job queue in iDRAC while updating firmware.

    \ :literal:`true`\  deletes the job queue in iDRAC while updating firmware.

    \ :literal:`false`\  does not delete the job queue in iDRAC while updating firmware.


  drs_check (optional, bool, False)
    Allows you to check if DRS of the cluster is enabled or not.

    \ :literal:`true`\  checks if Distributed Resource Scheduler (DRS) of the cluster is enabled.

    \ :literal:`false`\  does not check if DRS of the cluster is enabled.


  enter_maintenance_mode_options (optional, str, None)
    VM migration policy during management mode.

    \ :literal:`FULL\_DATA\_MIGRATION`\  for full data migration.

    \ :literal:`ENSURE\_ACCESSIBILITY`\  for ensuring accessibility.

    \ :literal:`NO\_DATA\_MIGRATION`\  does not migrate any data.


  enter_maintenance_mode_timeout (optional, int, 60)
    Time out value during maintenance mode in minutes.


  evacuate_VMs (optional, bool, False)
    Allows to move the virtual machine (VM) to other host when current host is powered off.

    \ :literal:`true`\  moves the VM to another host when the current host is powered off.

    \ :literal:`false`\  does not move the VM to another host when the current host is powered off.


  exit_maintenance_mode (optional, bool, False)
    Whether to exit management mode after Update.

    \ :literal:`true`\  exits the management mode after Update.

    \ :literal:`false`\  does not exit the management mode after Update.


  job_description (optional, str, None)
    Update job description.


  job_name (optional, str, None)
    Update job name.


  job_wait (optional, bool, True)
    Whether to wait till completion of the job. This is applicable when \ :emphasis:`power\_on`\  is \ :literal:`true`\ .

    \ :literal:`true`\  waits for job completion.

    \ :literal:`false`\  does not wait for job completion.


  job_wait_timeout (optional, int, 1200)
    The maximum wait time of \ :emphasis:`job\_wait`\  in seconds. The job is tracked only for this duration.

    This option is applicable when \ :emphasis:`job\_wait`\  is \ :literal:`true`\ .


  maintenance_mode_count_check (optional, bool, None)
    Allows to check if any host in cluster is in management mode.

    \ :literal:`true`\  checks if any host in cluster is in management mode.

    \ :literal:`false`\  does not check if any host in cluster is in management mode.


  reboot_options (optional, str, SAFEREBOOT)
    Host reboot option for firmware update.

    \ :literal:`FORCEREBOOT`\  will force reboot the server.

    \ :literal:`SAFEREBOOT`\  reboots the server in safe mode.

    \ :literal:`NEXTREBOOT`\  does not reboot the server.


  reset_idrac (optional, bool, None)
    Whether to reset the iDRAC while performing firmware update.

    \ :literal:`true`\  resets the iDRAC while performing firmware update.

    \ :literal:`false`\  does not reset the iDRAC while performing firmware update.


  run_now (True, bool, None)
    Whether to run the update job now or later.

    \ :literal:`true`\  runs the update job instantly.

    \ :literal:`false`\  runs the update at the specified \ :emphasis:`date\_time`\ .


  targets (True, list, None)
    The target details for the firmware update operation.

    Either \ :emphasis:`cluster`\ , \ :emphasis:`servicetag`\  or \ :emphasis:`host`\  is required for the firmware update operation.


    cluster (False, str, None)
      Name of the cluster to which firmware needs to updated.

      \ :emphasis:`cluster`\  is mutually exclusive with \ :emphasis:`servicetag`\  and \ :emphasis:`host`\ .

      This module supports only single cluster update.


    firmware_components (True, list, None)
      List of host firmware components to update.

      \ :ref:`dellemc.openmanage.omevv\_firmware\_compliance\_info <ansible_collections.dellemc.openmanage.omevv_firmware_compliance_info_module>`\  module can be used to fetch the supported firmware components.


    host (optional, str, None)
      The IP address or hostname of the host.

      \ :emphasis:`host`\  is mutually exclusive with \ :emphasis:`servicetag`\  and \ :emphasis:`cluster`\ .

      \ :ref:`dellemc.openmanage.omevv\_device\_info <ansible_collections.dellemc.openmanage.omevv_device_info_module>`\  module can be used to fetch the device information.


    servicetag (optional, str, None)
      The service tag of the host.

      \ :emphasis:`servicetag`\  is mutually exclusive with \ :emphasis:`host`\  and \ :emphasis:`cluster`\ .

      \ :ref:`dellemc.openmanage.omevv\_device\_info <ansible_collections.dellemc.openmanage.omevv_device_info_module>`\  module can be used to fetch the device information.



  hostname (True, str, None)
    IP address or hostname of the OpenManage Enterprise Modular.


  vcenter_username (False, str, None)
    Username for OpenManage Enterprise Integration for VMware vCenter (OMEVV).

    If the username is not provided, then the environment variable \ :envvar:`OMEVV\_VCENTER\_USERNAME`\  is used.

    Example: export OMEVV\_VCENTER\_USERNAME=username


  vcenter_password (False, str, None)
    Password for OpenManage Enterprise Integration for VMware vCenter (OMEVV).

    If the password is not provided, then the environment variable \ :envvar:`OMEVV\_VCENTER\_PASSWORD`\  is used.

    Example: export OMEVV\_VCENTER\_PASSWORD=password


  vcenter_uuid (False, str, None)
    Universally Unique Identifier (UUID) of vCenter.

    vCenter UUID details can be retrieved using \ :ref:`dellemc.openmanage.omevv\_vcenter\_info <ansible_collections.dellemc.openmanage.omevv_vcenter_info_module>`\  module.

    If UUID is not provided, then the environment variable \ :envvar:`OMEVV\_VCENTER\_UUID`\  is used.

    Example: export OMEVV\_VCENTER\_UUID=uuid


  port (optional, int, 443)
    OpenManage Enterprise HTTPS port.


  validate_certs (optional, bool, True)
    Whether to check SSL certificate. - If \ :literal:`true`\ , the SSL certificates will be validated. - If \ :literal:`false`\ , the SSL certificates will not be validated.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.
   - This module supports IPv4 and IPv6 addresses.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Immediately update the firmware of a single component for a specific host
      dellemc.openmanage.omevv.omevv_firmware:
        hostname: "XXX.XXX.XXX.XX"
        vcenter_uuid: "xxxxx"
        vcenter_username: "username"
        vcenter_password: "password"
        ca_path: "path/to/ca_file"
        run_now: false
        date_time: "2024-09-10T20:50:00Z"
        enter_maintenance_mode_timeout: 60
        enter_maintenance_mode_options: FULL_DATA_MIGRATION
        drs_check: true
        evacuate_VMs: true
        exit_maintenance_mode: true
        reboot_options: NEXTREBOOT
        maintenance_mode_count_check: true
        check_vSAN_health: true
        reset_idrac: true
        delete_job_queue: true
        targets:
          - servicetag: SVCTAG1
            firmware_components:
              - "DCIM:INSTALLED#802__Diagnostics.Embedded.1:LC.Embedded.1"

    - name: Update the firmware of multiple components at scheduled time for a specific host
      dellemc.openmanage.omevv.omevv_firmware:
        hostname: "XXX.XXX.XXX.XY"
        vcenter_uuid: "xxxxx"
        vcenter_username: "username"
        vcenter_password: "password"
        ca_path: "path/to/ca_file"
        run_now: false
        date_time: "2024-09-10T20:50:00+05:30"
        enter_maintenance_mode_timeout: 60
        enter_maintenance_mode_options: ENSURE_ACCESSIBILITY
        drs_check: true
        evacuate_VMs: true
        exit_maintenance_mode: true
        reboot_options: FORCEREBOOT
        maintenance_mode_count_check: true
        check_vSAN_health: true
        reset_idrac: false
        delete_job_queue: false
        targets:
          - host: "XXX.XXX.XXX.XZ"
            firmware_components:
              - "DCIM:INSTALLED#iDRAC.Embedded.1-1#IDRACinfo"
              - "DCIM:INSTALLED#301_C_BOSS.SL.14-1"
              - "DCIM:INSTALLED#807__TPM.Integrated.1-1"

    - name: Update the firmware of multiple components at scheduled time for a cluster
      dellemc.openmanage.omevv.omevv_firmware:
        hostname: "XXX.XXX.XXX.XX"
        vcenter_uuid: "xxxxx"
        vcenter_username: "username"
        vcenter_password: "password"
        ca_path: "path/to/ca_file"
        run_now: false
        date_time: "2024-09-10T20:50:00+05:30"
        enter_maintenance_mode_timeout: 60
        enter_maintenance_mode_options: ENSURE_ACCESSIBILITY
        drs_check: true
        evacuate_VMs: true
        exit_maintenance_mode: true
        reboot_options: SAFEREBOOT
        maintenance_mode_count_check: true
        check_vSAN_health: true
        reset_idrac: false
        delete_job_queue: false
        targets:
          - cluster: cluster_a
            firmware_components:
              - "DCIM:INSTALLED#iDRAC.Embedded.1-1#IDRACinfo"
              - "DCIM:INSTALLED#301_C_BOSS.SL.14-1"
              - "DCIM:INSTALLED#807__TPM.Integrated.1-1"

    - name: Retrieve firmware compliance report of all hosts in the specific cluster
      dellemc.openmanage.omevv_firmware_compliance_info:
        hostname: "XXX.XXX.XXX.XX"
        vcenter_uuid: "xxxxx"
        vcenter_username: "username"
        vcenter_password: "password"
        ca_path: "path/to/ca_file"
        clusters:
          - cluster_name: cluster_a
      register: compliance_data

    - name: Initialize compliance status results
      ansible.builtin.set_fact:
        source_names: []
        service_tag: ""

    - name: Flatten host compliance reports
      ansible.builtin.set_fact:
        host_reports: "{{
            compliance_data.firmware_compliance_info |
            map(attribute='hostComplianceReports') |
            flatten(levels=1) }}"

    - name: Flatten and filter concompliant components
      ansible.builtin.set_fact:
        non_compliant_components: >-
            {{
              host_reports
              | map(attribute='componentCompliances')
              | flatten(levels=1)
              | selectattr('driftStatus', 'equalto', 'NonCompliant')
            }}

    - name: Gather components source name and set service tag
      ansible.builtin.set_fact:
        source_names: "{{ source_names + [item.sourceName] }}"
        service_tag: "{{ host_report.serviceTag }}"
      loop: "{{ non_compliant_components }}"
      vars:
        host_report: >-
            {{
              host_reports
              | selectattr('componentCompliances', 'contains', item)
              | first
            }}

    - name: Combine the final non compliance report
      ansible.builtin.set_fact:
        noncompliance_report:
          sourceNames: "{{ source_names }}"
          serviceTag: "{{ service_tag }}"

    - name: Update firmware at the scheduled time for a specific host
      dellemc.openmanage.omevv.omevv_firmware:
        hostname: "192.168.0.1"
        vcenter_uuid: "{{ vcenter_uuid }}"
        vcenter_username: "username"
        vcenter_password: "password"
        ca_path: "path/to/ca_file"
        run_now: false
        date_time: "2024-09-10T20:50:00Z"
        enter_maintenance_mode_timeout: 60
        enter_maintenance_mode_options: NO_DATA_MIGRATION
        drs_check: true
        evacuate_VMs: false
        exit_maintenance_mode: true
        reboot_options: SAFEREBOOT
        maintenance_mode_count_check: true
        check_vSAN_health: true
        reset_idrac: true
        delete_job_queue: true
        targets:
          - servicetag: "{{ noncompliance_report.serviceTag }}"
            firmware_components: "{{ noncompliance_report.sourceNames }}"



Return Values
-------------

msg (always, str, Successfully created the OMEVV baseline profile.)
  Status of the firmware update operation.


error_info (on HTTP error, dict, {'errorCode': '20058', 'message': 'Update Job already running for group id 1004 corresponding to cluster OMAM-Cluster-1. Wait for its completion and trigger.'})
  Details of the module HTTP Error.





Status
------





Authors
~~~~~~~

- Rajshekar P(@rajshekarp87)

