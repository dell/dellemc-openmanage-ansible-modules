.. _omevv_firmware_compliance_info_module:


omevv_firmware_compliance_info -- Retrieve firmware compliance report.
======================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows you to retrieve firmware compliance reports of all the hosts of the cluster, a specific host of the cluster, or multiple clusters.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  clusters (optional, list, None)
    Cluster details to retrieve the firmware compliance report.


    cluster_name (True, str, None)
      Cluster name of the hosts for which the firmware compliance report should be retrieved.

      If \ :emphasis:`servicetags`\  or \ :emphasis:`hosts`\  is provided, then the firmware compliance report of only the specified hosts is retrieved and displayed.


    servicetags (optional, list, None)
      The service tag of the hosts for which the firmware compliance reports must be retrieved.


    hosts (optional, list, None)
      The IP address or hostname of the hosts for which the firmware compliance reports must be retrieved.



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




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Retrieve a firmware compliance report of all the clusters
      dellemc.openmanage.omevv_firmware_compliance_info:
        hostname: "192.168.0.1"
        vcenter_uuid: "xxxxx"
        vcenter_username: "username"
        vcenter_password: "password"
        ca_path: "path/to/ca_file"

    - name: Retrieve a firmware compliance report of all the hosts in a specific cluster
      dellemc.openmanage.omevv_firmware_compliance_info:
        hostname: "192.168.0.1"
        vcenter_uuid: "xxxxx"
        vcenter_username: "username"
        vcenter_password: "password"
        ca_path: "path/to/ca_file"
        clusters:
          - cluster_name: cluster_a

    - name: Retrieve a firmware compliance report of specific hosts in the cluster
      dellemc.openmanage.omevv_firmware_compliance_info:
        hostname: "192.168.0.1"
        vcenter_uuid: "xxxxx"
        vcenter_username: "username"
        vcenter_password: "password"
        ca_path: "path/to/ca_file"
        clusters:
          - cluster_name: cluster_a
            servicetags:
              - SVCTAG1
              - SVCTAG2
            hosts:
              - host1
              - xx.xx.xx.xx

    - name: Retrieve a firmware compliance report of multiple clusters
      dellemc.openmanage.omevv_firmware_compliance_info:
        hostname: "192.168.0.1"
        vcenter_uuid: "xxxxx"
        vcenter_username: "username"
        vcenter_password: "password"
        ca_path: "path/to/ca_file"
        clusters:
          - cluster_name: cluster_a
          - cluster_name: cluster_b



Return Values
-------------

msg (always, str, Successfully fetched the firmware compliance report.)
  Retrive the firmware compliance report.


firmware_compliance_info (on HTTP error, list, [{'complianceStatus': 'NonCompliant', 'cluster': 'cluster_a', 'hostComplianceReports': [{'hostId': 1002, 'hostAddress': 'XX.XX.XX.XX', 'serviceTag': 'SVCTAG', 'deviceModel': 'PowerEdge R660xs', 'complianceStatus': 'WARNING', 'componentCompliances': [{'driftStatus': 'NonCompliant', 'componentName': 'Enterprise UEFI Diagnostics', 'currentValue': '4303A15', 'baselineValue': '4303A19', 'criticality': 'Optional', 'updateAction': 'UPGRADE', 'sourceName': 'DCIM:INSTALLED#802__Diagnostics.Embedded.1:LC.Embedded.1', 'complianceStatus': 'WARNING', 'rebootRequired': False}]}]}])
  Details of the compliance report.





Status
------





Authors
~~~~~~~

- Abhishek Sinha(@ABHISHEK-SINHA10)

