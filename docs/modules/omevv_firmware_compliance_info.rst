.. _omevv_firmware_compliance_info_module:


omevv_firmware_compliance_info -- Fetch the firmware compliance report
======================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to fetch the firmware compliance report of all the hosts of the cluster, or a specific host of the cluster, or multiple clusters.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  clusters (optional, list, None)
    The cluster details to retrieve the firmware compliance report.


    cluster_name (True, str, None)
      The cluster name of the hosts for which the firmware compliance report needs to be fetched.

      If \ :emphasis:`servicetags`\  or \ :emphasis:`hosts`\  is provided, then firmware compliance report of only the specified hosts will be fetched and shown.


    servicetags (optional, list, None)
      The service tag of the hosts.

      The hosts for which the firmware compliance reports needs to be fetched.


    hosts (optional, list, None)
      The IP address or hostname of the hosts.

      The hosts for which the firmware compliance reports needs to be fetched.



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
    - name: Fetch firmware compliance report of all the cluster
      dellemc.openmanage.omevv_firmware_compliance_info:
        hostname: "192.168.0.1"
        vcenter_uuid: "xxxxx"
        vcenter_username: "username"
        vcenter_password: "password"
        ca_path: "path/to/ca_file"

    - name: Fetch firmware compliance report of all the hosts in the specific cluster
      dellemc.openmanage.omevv_firmware_compliance_info:
        hostname: "192.168.0.1"
        vcenter_uuid: "xxxxx"
        vcenter_username: "username"
        vcenter_password: "password"
        ca_path: "path/to/ca_file"
        clusters:
          - cluster_name: cluster_a

    - name: Fetch firmware compliance report of a specific hosts in the cluster
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

    - name: Fetch firmware compliance report of multiple cluster
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

msg (always, str, Successfully created the OMEVV firmware repository profile.)
  Status of the profile operation.


error_info (on HTTP error, dict, {'errorCode': '18001', 'message': 'Repository profile with name Test already exists.'})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Abhishek Sinha(@ABHISHEK-SINHA10)

