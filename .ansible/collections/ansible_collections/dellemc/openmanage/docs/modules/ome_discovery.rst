.. _ome_discovery_module:


ome_discovery -- Create, modify, or delete a discovery job on OpenManage Enterprise
===================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to create, modify, or delete a discovery job.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  state (optional, str, present)
    \ :literal:`present`\  creates a discovery job or modifies an existing discovery job.

    \ :emphasis:`discovery\_job\_name`\  is mandatory for the creation of a new discovery job.

    If multiple discoveries of the same \ :emphasis:`discovery\_job\_name`\  exist, then the new discovery job will not be created.

    \ :literal:`absent`\  deletes an existing discovery job(s) with the specified \ :emphasis:`discovery\_job\_name`\ .


  discovery_job_name (optional, str, None)
    Name of the discovery configuration job.

    It is mutually exclusive with \ :emphasis:`discovery\_id`\ .


  discovery_id (optional, int, None)
    ID of the discovery configuration group.

    This value is DiscoveryConfigGroupId in the return values under discovery\_status.

    It is mutually exclusive with \ :emphasis:`discovery\_job\_name`\ .


  new_name (optional, str, None)
    New name of the discovery configuration job.


  schedule (optional, str, RunNow)
    Provides the option to schedule the discovery job.

    If \ :literal:`RunLater`\  is selected, then \ :emphasis:`cron`\  must be specified.


  cron (optional, str, None)
    Provide a cron expression based on Quartz cron format.


  trap_destination (optional, bool, False)
    Enable OpenManage Enterprise to receive the incoming SNMP traps from the discovered devices.

    This is effective only for servers discovered by using their iDRAC interface.


  community_string (optional, bool, False)
    Enable the use of SNMP community strings to receive SNMP traps using Application Settings in OpenManage Enterprise. This option is available only for the discovered iDRAC servers and MX7000 chassis.


  email_recipient (optional, str, None)
    Enter the email address to which notifications are to be sent about the discovery job status. Configure the SMTP settings to allow sending notifications to an email address.


  job_wait (optional, bool, True)
    Provides the option to wait for job completion.

    This option is applicable when \ :emphasis:`state`\  is \ :literal:`present`\ .


  job_wait_timeout (optional, int, 10800)
    The maximum wait time of \ :emphasis:`job\_wait`\  in seconds. The job is tracked only for this duration.

    This option is applicable when \ :emphasis:`job\_wait`\  is \ :literal:`true`\ .


  ignore_partial_failure (optional, bool, False)
    Provides the option to ignore partial failures. Partial failures occur when there is a combination of both discovered and undiscovered IPs.

    If \ :literal:`false`\ , then the partial failure is not ignored, and the module will error out.

    If \ :literal:`true`\ , then the partial failure is ignored.

    This option is only applicable if \ :emphasis:`job\_wait`\  is \ :literal:`true`\ .


  discovery_config_targets (optional, list, None)
    Provide the list of discovery targets.

    Each discovery target is a set of \ :emphasis:`network\_address\_detail`\ , \ :emphasis:`device\_types`\ , and one or more protocol credentials.

    This is mandatory when \ :emphasis:`state`\  is \ :literal:`present`\ .

    \ :literal:`WARNING`\  Modification of this field is not supported, this field is overwritten every time. Ensure to provide all the required details for this field.


    network_address_detail (True, list, None)
      Provide the list of IP addresses, host names, or the range of IP addresses of the devices to be discovered or included.

      Sample Valid IP Range Formats

         192.35.0.0

         192.36.0.0-10.36.0.255

         192.37.0.0/24

         2345:f2b1:f083:135::5500/118

         2345:f2b1:f083:135::a500-2607:f2b1:f083:135::a600

         hostname.domain.tld

         hostname

         2345:f2b1:f083:139::22a

      Sample Invalid IP Range Formats

         192.35.0.\*

         192.36.0.0-255

         192.35.0.0/255.255.255.0

      \ :literal:`NOTE`\  The range size for the number of IP addresses is limited to 16,385 (0x4001).

      \ :literal:`NOTE`\  Both IPv6 and IPv6 CIDR formats are supported.


    device_types (True, list, None)
      Provide the type of devices to be discovered.

      The accepted types are SERVER, CHASSIS, NETWORK SWITCH, and STORAGE.

      A combination or all of the above can be provided.

      Supported protocols for each device type are:

      SERVER - \ :emphasis:`wsman`\ , \ :emphasis:`redfish`\ , \ :emphasis:`snmp`\ , \ :emphasis:`ipmi`\ , \ :emphasis:`ssh`\ , and \ :emphasis:`vmware`\ .

      CHASSIS - \ :emphasis:`wsman`\ , and \ :emphasis:`redfish`\ .

      NETWORK SWITCH - \ :emphasis:`snmp`\ .

      STORAGE - \ :emphasis:`storage`\ , and \ :emphasis:`snmp`\ .


    wsman (optional, dict, None)
      Web Services-Management (WS-Man).


      username (True, str, None)
        Provide a username for the protocol.


      password (True, str, None)
        Provide a password for the protocol.


      domain (optional, str, None)
        Provide a domain for the protocol.


      port (optional, int, 443)
        Enter the port number that the job must use to discover the devices.


      retries (optional, int, 3)
        Enter the number of repeated attempts required to discover a device.


      timeout (optional, int, 60)
        Enter the time in seconds after which a job must stop running.


      cn_check (optional, bool, False)
        Enable the Common Name (CN) check.


      ca_check (optional, bool, False)
        Enable the Certificate Authority (CA) check.


      certificate_data (optional, str, None)
        Provide certificate data for the CA check.



    redfish (optional, dict, None)
      REDFISH protocol.


      username (True, str, None)
        Provide a username for the protocol.


      password (True, str, None)
        Provide a password for the protocol.


      domain (optional, str, None)
        Provide a domain for the protocol.


      port (optional, int, 443)
        Enter the port number that the job must use to discover the devices.


      retries (optional, int, 3)
        Enter the number of repeated attempts required to discover a device.


      timeout (optional, int, 60)
        Enter the time in seconds after which a job must stop running.


      cn_check (optional, bool, False)
        Enable the Common Name (CN) check.


      ca_check (optional, bool, False)
        Enable the Certificate Authority (CA) check.


      certificate_data (optional, str, None)
        Provide certificate data for the CA check.



    snmp (optional, dict, None)
      Simple Network Management Protocol (SNMP).


      community (True, str, None)
        Community string for the SNMP protocol.


      port (optional, int, 161)
        Enter the port number that the job must use to discover the devices.


      retries (optional, int, 3)
        Enter the number of repeated attempts required to discover a device.


      timeout (optional, int, 3)
        Enter the time in seconds after which a job must stop running.



    storage (optional, dict, None)
      HTTPS Storage protocol.


      username (True, str, None)
        Provide a username for the protocol.


      password (True, str, None)
        Provide a password for the protocol.


      domain (optional, str, None)
        Provide a domain for the protocol.


      port (optional, int, 443)
        Enter the port number that the job must use to discover the devices.


      retries (optional, int, 3)
        Enter the number of repeated attempts required to discover a device.


      timeout (optional, int, 60)
        Enter the time in seconds after which a job must stop running.


      cn_check (optional, bool, False)
        Enable the Common Name (CN) check.


      ca_check (optional, bool, False)
        Enable the Certificate Authority (CA) check.


      certificate_data (optional, str, None)
        Provide certificate data for the CA check.



    vmware (optional, dict, None)
      VMWARE protocol.


      username (True, str, None)
        Provide a username for the protocol.


      password (True, str, None)
        Provide a password for the protocol.


      domain (optional, str, None)
        Provide a domain for the protocol.


      port (optional, int, 443)
        Enter the port number that the job must use to discover the devices.


      retries (optional, int, 3)
        Enter the number of repeated attempts required to discover a device.


      timeout (optional, int, 60)
        Enter the time in seconds after which a job must stop running.


      cn_check (optional, bool, False)
        Enable the Common Name (CN) check.


      ca_check (optional, bool, False)
        Enable the Certificate Authority (CA) check.


      certificate_data (optional, str, None)
        Provide certificate data for the CA check.



    ssh (optional, dict, None)
      Secure Shell (SSH).


      username (True, str, None)
        Provide a username for the protocol.


      password (True, str, None)
        Provide a password for the protocol.


      port (optional, int, 22)
        Enter the port number that the job must use to discover the devices.


      retries (optional, int, 3)
        Enter the number of repeated attempts required to discover a device.


      timeout (optional, int, 60)
        Enter the time in seconds after which a job must stop running.


      check_known_hosts (optional, bool, False)
        Verify the known host key.


      is_sudo_user (optional, bool, False)
        Use the SUDO option.



    ipmi (optional, dict, None)
      Intelligent Platform Management Interface (IPMI)


      username (True, str, None)
        Provide a username for the protocol.


      password (True, str, None)
        Provide a password for the protocol.


      retries (optional, int, 3)
        Enter the number of repeated attempts required to discover a device.


      timeout (optional, int, 60)
        Enter the time in seconds after which a job must stop running.


      kgkey (optional, str, None)
        KgKey for the IPMI protocol.




  hostname (True, str, None)
    OpenManage Enterprise IP address or hostname.


  username (False, str, None)
    OpenManage Enterprise username.

    If the username is not provided, then the environment variable \ :envvar:`OME\_USERNAME`\  is used.

    Example: export OME\_USERNAME=username


  password (False, str, None)
    OpenManage Enterprise password.

    If the password is not provided, then the environment variable \ :envvar:`OME\_PASSWORD`\  is used.

    Example: export OME\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`OME\_X\_AUTH\_TOKEN`\  is used.

    Example: export OME\_X\_AUTH\_TOKEN=x\_auth\_token


  port (optional, int, 443)
    OpenManage Enterprise HTTPS port.


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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.
   - This module does not support \ :literal:`check\_mode`\ .
   - If \ :emphasis:`state`\  is \ :literal:`present`\ , then Idempotency is not supported.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Discover servers in a range
      dellemc.openmanage.ome_discovery:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        discovery_job_name: "Discovery_server_1"
        discovery_config_targets:
          - network_address_detail:
              - 192.96.24.1-192.96.24.255
            device_types:
              - SERVER
            wsman:
              username: user
              password: password

    - name: Discover chassis in a range
      dellemc.openmanage.ome_discovery:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        discovery_job_name: "Discovery_chassis_1"
        discovery_config_targets:
          - network_address_detail:
              - 192.96.24.1-192.96.24.255
            device_types:
              - CHASSIS
            wsman:
              username: user
              password: password

    - name: Discover switches in a range
      dellemc.openmanage.ome_discovery:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        discovery_job_name: "Discover_switch_1"
        discovery_config_targets:
          - network_address_detail:
              - 192.96.24.1-192.96.24.255
            device_types:
              - NETWORK SWITCH
            snmp:
              community: snmp_creds

    - name: Discover storage in a range
      dellemc.openmanage.ome_discovery:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        discovery_job_name: "Discover_storage_1"
        discovery_config_targets:
          - network_address_detail:
              - 192.96.24.1-192.96.24.255
            device_types:
              - STORAGE
            storage:
              username: user
              password: password
            snmp:
              community: snmp_creds

    - name: Delete a discovery job
      dellemc.openmanage.ome_discovery:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "absent"
        discovery_job_name: "Discovery-123"

    - name: Schedule the discovery of multiple devices ignoring partial failure and enable trap to receive alerts
      dellemc.openmanage.ome_discovery:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "present"
        discovery_job_name: "Discovery-123"
        discovery_config_targets:
          - network_address_detail:
              - 192.96.24.1-192.96.24.255
              - 192.96.0.0/24
              - 192.96.26.108
            device_types:
              - SERVER
              - CHASSIS
              - STORAGE
              - NETWORK SWITCH
            wsman:
              username: wsman_user
              password: wsman_pwd
            redfish:
              username: redfish_user
              password: redfish_pwd
            snmp:
              community: snmp_community
          - network_address_detail:
              - 192.96.25.1-192.96.25.255
              - ipmihost
              - esxiserver
              - sshserver
            device_types:
              - SERVER
            ssh:
              username: ssh_user
              password: ssh_pwd
            vmware:
              username: vm_user
              password: vmware_pwd
            ipmi:
              username: ipmi_user
              password: ipmi_pwd
        schedule: RunLater
        cron: "0 0 9 ? * MON,WED,FRI *"
        ignore_partial_failure: true
        trap_destination: true
        community_string: true
        email_recipient: test_email@company.com

    - name: Discover servers with ca check enabled
      dellemc.openmanage.ome_discovery:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        discovery_job_name: "Discovery_server_ca1"
        discovery_config_targets:
          - network_address_detail:
              - 192.96.24.108
            device_types:
              - SERVER
            wsman:
              username: user
              password: password
              ca_check: true
              certificate_data: "{{ lookup('ansible.builtin.file', '/path/to/certificate_data_file') }}"

    - name: Discover chassis with ca check enabled data
      dellemc.openmanage.ome_discovery:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        discovery_job_name: "Discovery_chassis_ca1"
        discovery_config_targets:
          - network_address_detail:
              - 192.96.24.108
            device_types:
              - CHASSIS
            redfish:
              username: user
              password: password
              ca_check: true
              certificate_data: "-----BEGIN CERTIFICATE-----\r\n
              ABCDEFGHIJKLMNOPQRSTUVWXYZaqwertyuiopasdfghjklzxcvbnmasdasagasvv\r\n
              ABCDEFGHIJKLMNOPQRSTUVWXYZaqwertyuiopasdfghjklzxcvbnmasdasagasvv\r\n
              ABCDEFGHIJKLMNOPQRSTUVWXYZaqwertyuiopasdfghjklzxcvbnmasdasagasvv\r\n
              aqwertyuiopasdfghjklzxcvbnmasdasagasvv=\r\n
              -----END CERTIFICATE-----"



Return Values
-------------

msg (always, str, Successfully deleted 1 discovery job(s).)
  Overall status of the discovery operation.


discovery_status (when I(state) is C(present), dict, {'Completed': ['192.168.24.17', '192.168.24.20', '192.168.24.22'], 'Failed': ['192.168.24.15', '192.168.24.16', '192.168.24.18', '192.168.24.19', '192.168.24.21', 'host123'], 'DiscoveredDevicesByType': [{'Count': 3, 'DeviceType': 'SERVER'}], 'DiscoveryConfigDiscoveredDeviceCount': 3, 'DiscoveryConfigEmailRecipient': 'myemail@dell.com', 'DiscoveryConfigExpectedDeviceCount': 9, 'DiscoveryConfigGroupId': 125, 'JobDescription': 'D1', 'JobEnabled': True, 'JobEndTime': '2021-01-01 06:27:29.99', 'JobId': 12666, 'JobName': 'D1', 'JobNextRun': None, 'JobProgress': '100', 'JobSchedule': 'startnow', 'JobStartTime': '2021-01-01 06:24:10.071', 'JobStatusId': 2090, 'LastUpdateTime': '2021-01-01 06:27:30.001', 'UpdatedBy': 'admin'})
  Details of the discovery job created or modified.

  If \ :emphasis:`job\_wait`\  is true, Completed and Failed IPs are also listed.


discovery_ids (when discoveries with duplicate name exist for I(state) is C(present), list, [1234, 5678])
  IDs of the discoveries with duplicate names.


job_detailed_status (All time., list, [{'ElapsedTime': '00:00:00', 'EndTime': None, 'ExecutionHistoryId': 564873, 'Id': 656893, 'IdBaseEntity': 0, 'JobStatus': {'Id': 2050, 'Name': 'Running'}, 'Key': '192.96.24.1', 'Progress': '0', 'StartTime': '2023-07-04 06:23:54.008', 'Value': 'Running\nDiscovery of target 192.96.24.1 started.\nDiscovery target resolved to IP  192.96.24.1 .'}])
  Detailed last execution history of a job.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V (@jagadeeshnv)
- Sajna Shetty (@Sajna-Shetty)
- Abhishek Sinha (@Abhishek-Dell)

