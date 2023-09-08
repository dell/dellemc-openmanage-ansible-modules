.. _ome_alert_policies_module:


ome_alert_policies -- Manage OME alert policies.
================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows you to create, modify, or delete alert policies on OpenManage Enterprise or OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  name (True, list, None)
    Name for the alert policy.

    This is applicable only when \ :emphasis:`state`\  is \ :literal:`present`\  and first one is picked if multiple values is provided.

    More than one policy name is applicable when \ :emphasis:`state`\  is \ :literal:`absent`\  and \ :emphasis:`state`\  is \ :literal:`present`\  with only \ :emphasis:`enable`\  provided.


  state (optional, str, present)
    \ :literal:`present`\  allows to create an alert policy or update if the policy name already exists.

    \ :literal:`absent`\  allows to delete an alert policy.


  enable (optional, bool, None)
    \ :literal:`true`\  allows to enable an alert policy.

    \ :literal:`false`\  allows to disable an alert policy.

    This is applicable only when \ :emphasis:`state`\  is \ :literal:`present`\ .


  new_name (optional, str, None)
    New name for the alert policy.

    This is applicable only when \ :emphasis:`state`\  is \ :literal:`present`\  and a policy exists.


  description (optional, str, None)
    Description for the alert policy.

    This is applicable only when \ :emphasis:`state`\  is \ :literal:`present`\ 


  device_service_tag (optional, list, None)
    List of device service tags on which the alert policy will be applicable.

    This option is mutually exclusive with \ :emphasis:`device\_group`\ , \ :emphasis:`specific\_undiscovered\_devices`\ , \ :emphasis:`any\_undiscovered\_devices`\  and \ :emphasis:`all\_devices`\ .

    This is applicable only when \ :emphasis:`state`\  is \ :literal:`present`\ 


  device_group (optional, list, None)
    List of Group name on which the alert policy will be applicable.

    This option is mutually exclusive with \ :emphasis:`device\_service\_tag`\ , \ :emphasis:`specific\_undiscovered\_devices`\ , \ :emphasis:`any\_undiscovered\_devices`\  and \ :emphasis:`all\_devices`\  .

    This is applicable only when \ :emphasis:`state`\  is \ :literal:`present`\ 


  specific_undiscovered_devices (optional, list, None)
    Undiscovered IP's, hostnames or range of IP's of a devices on which the alert policy will be applicable.

    This option is mutually exclusive with \ :emphasis:`device\_service\_tag`\ , \ :emphasis:`device\_group`\ , \ :emphasis:`any\_undiscovered\_devices`\  and \ :emphasis:`all\_devices`\  .

    This is applicable only when \ :emphasis:`state`\  is \ :literal:`present`\ 

    Sample Valid IP Range Format:

         10.35.0.0

         10.36.0.0-10.36.0.255

         10.37.0.0/24

         2607:f2b1:f083:135::5500/118

         2607:f2b1:f083:135::a500-2607:f2b1:f083:135::a600

         hostname.domain.com

    Sample Invalid IP Range Format:

         10.35.0.\*

         10.36.0.0-255

         10.35.0.0/255.255.255.0


  any_undiscovered_devices (optional, bool, None)
    Any Undiscovered devices on which the alert policy will be applicable.

    This option is mutually exclusive with \ :emphasis:`device\_service\_tag`\ , \ :emphasis:`specific\_undiscovered\_devices`\ , \ :emphasis:`device\_group`\  and \ :emphasis:`all\_devices`\ .

    This is applicable only when \ :emphasis:`state`\  is \ :literal:`present`\ .


  all_devices (optional, bool, None)
    All the discovered and undiscovered devices on which the alert policy will be applicable.

    This option is mutually exclusive with \ :emphasis:`device\_service\_tag`\ , \ :emphasis:`specific\_undiscovered\_devices`\ , \ :emphasis:`any\_undiscovered\_devices`\  and \ :emphasis:`device\_group`\ .

    This is applicable only when \ :emphasis:`state`\  is \ :literal:`present`\ .


  category (optional, list, None)
    Category of the alerts received.

    This is mutually exclusive with the \ :emphasis:`message\_ids`\ , \ :emphasis:`message\_file`\ .

    To be fetch from the \ :ref:`dellemc.openmanage.ome\_alert\_policies\_category\_info <ansible_collections.dellemc.openmanage.ome_alert_policies_category_info_module>`\ .

    This is applicable only when \ :emphasis:`state`\  is \ :literal:`present`\ .


    catalog_name (True, str, None)
      Name of the catalog.


    catalog_category (optional, list, None)
      Category of the catalog.


      category_name (optional, str, None)
        Name of the category.


      sub_category_names (optional, list, None)
        List of sub categories.




  message_ids (optional, list, None)
    List of Message ids

    This is mutually exclusive with the \ :emphasis:`category`\ , \ :emphasis:`message\_file`\ 

    This is applicable only when \ :emphasis:`state`\  is \ :literal:`present`\ 

    To be fetched from the \ :ref:`dellemc.openmanage.ome\_alert\_policies\_message\_id\_info <ansible_collections.dellemc.openmanage.ome_alert_policies_message_id_info_module>`\ 


  message_file (optional, path, None)
    Local path of a CSV formatted file with message ids

    This is mutually exclusive with the \ :emphasis:`category`\ , \ :emphasis:`message\_ids`\ 

    This is applicable only when \ :emphasis:`state`\  is \ :literal:`present`\ 

    To be fetched from the \ :ref:`dellemc.openmanage.ome\_alert\_policies\_message\_id\_info <ansible_collections.dellemc.openmanage.ome_alert_policies_message_id_info_module>`\ 


  date_and_time (optional, dict, None)
    Specify the schedule for when the alert policy is applicable.

    \ :emphasis:`date\_and\_time`\  is mandatory for creating a policy and optional when updating a poicy.

    This is applicable only when \ :emphasis:`state`\  is \ :literal:`present`\ 


    date_from (True, str, None)
      Start date in the format YYYY-MM-DD.


    date_to (optional, str, None)
      End date in the format YYYY-MM-DD.


    time_from (optional, str, None)
      Interval start time in the format HH:MM

      This is mandatory when \ :emphasis:`time\_interval`\  is \ :literal:`true`\ 


    time_to (optional, str, None)
      Interval end time in the format HH:MM

      This is mandatory when \ :emphasis:`time\_interval`\  is \ :literal:`true`\ 


    days (optional, list, None)
      Days of the week to be scheduled.


    time_interval (optional, bool, None)
      Enable time interval to be scheduled.



  severity (optional, list, None)
    Severity of the alert.

    This is mandatory when creating a policy and optional updating a policy.

    This is applicable only when \ :emphasis:`state`\  is \ :literal:`present`\ .


  actions (optional, list, None)
    Actions to be triggered for the policy.

    This parameter is case-sensitive.

    This is mandatory when creating a policy and optional updating a policy.

    This is applicable only when \ :emphasis:`state`\  is \ :literal:`present`\ 


    action_name (True, str, None)
      Name of the action.

      To be fetched from the \ :ref:`dellemc.openmanage.ome\_alert\_policies\_action\_info <ansible_collections.dellemc.openmanage.ome_alert_policies_action_info_module>`\ 

      This is mandatory when creating a policy and optional updating a policy.

      This parameter is case-sensitive.


    parameters (optional, list, [])
      Predefined parameters to be set for the \ :emphasis:`action\_name`\ .


      name (optional, str, None)
        Name of the parameter.

        To be fetched from the \ :ref:`dellemc.openmanage.ome\_alert\_policies\_action\_info <ansible_collections.dellemc.openmanage.ome_alert_policies_action_info_module>`\ 


      value (optional, str, None)
        Value of the parameter.




  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.


  password (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.


  validate_certs (optional, bool, True)
    If \ :literal:`False`\ , the SSL certificates will not be validated.

    Configure \ :literal:`False`\  only on personally controlled sites where self-signed certificates are used.

    Prior to collection version \ :literal:`5.0.0`\ , the \ :emphasis:`validate\_certs`\  is \ :literal:`False`\  by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell OpenManage Enterprise or OpenManage Enterprise Modular.
   - This module supports both IPv4 and IPv6 addresses.
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: "Create a Alert Policy"
      dellemc.openamanage.ome_alert_policies:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        name: "Alert Policy One"
        device_service_tag:
          - ABCD123
          - SVC7845
        category:
          - catalog_name: Application
            catalog_category:
              - category_name: Audit
                sub_category_names:
                  - Generic
                  - Devices
          - catalog_name: iDRAC
            catalog_category:
              - category_name: Audit
                sub_category_names:
                  - BIOS Management
                  - iDRAC Service Module
        date_and_time:
          date_from: 2023-10-10
          date_to: 2023-10-11
          time_from: "11:00"
          time_to: "12:00"
        severity:
          - unknown
          - critical
        actions:
          - action_name: Trap
            parameters:
              - name: "192.1.2.3:162"
                value: true
              - name: "traphostname.domain.com:162"
                value: true
      tags: create_alert_policy

    - name: "Update a Alert Policy"
      dellemc.openamanage.ome_alert_policies:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        new_name: "Update Policy Name"
        device_group: "Group Name"
        message_ids:
          - AMP400
          - CTL201
          - BIOS101
        date_and_time:
          date_from: 2023-10-10
          date_to: 2023-10-11
          time_from: "11:00"
          time_to: "12:00"
          time_interval: true
        actions:
          - action_name: Trap
            parameters:
              - name: "192.1.2.3:162"
                value: true
      tags: update_alert_policy

    - name: "Enable a Policy"
      dellemc.openamanage.ome_alert_policies:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        name: "Policy Name"
        enable: true
      tags: enable_alert_policy

    - name: "Disable multiple Policies"
      dellemc.openamanage.ome_alert_policies:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        name:
          - "Policy Name 1"
          - "Policy Name 2"
        enable: false
      tags: disable_alert_policy

    - name: "Delete a Policy"
      dellemc.openamanage.ome_alert_policies:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        name: "Policy Name"
        state: absent
      tags: delete_alert_policy



Return Values
-------------

msg (always, str, Successfully performed the create policy operation.)
  Status of the alert policies operation.


status (when state is present, dict, {'Id': 12345, 'Name': 'Policy', 'Description': 'Details of the Policy', 'Enabled': True, 'DefaultPolicy': False, 'Editable': True, 'Visible': True, 'PolicyData': {'Catalogs': [{'CatalogName': 'iDRAC', 'Categories': [4], 'SubCategories': [41]}, {'CatalogName': 'Application', 'Categories': [0], 'SubCategories': [0]}], 'Severities': [16, 1, 2, 4, 8], 'Devices': [10086, 10088], 'DeviceTypes': [1000, 2000], 'Groups': [], 'Schedule': {'StartTime': '2023-06-06 15:02:46.000', 'EndTime': '2023-06-06 15:02:46.000', 'CronString': '* * * ? * * *'}, 'Actions': [{'Id': 8, 'Name': 'Email', 'ParameterDetails': [{'Id': 1, 'Name': 'subject', 'Value': 'Device Name: $name,  Device IP Address: $ip,  Severity: $severity', 'Type': 'string', 'TypeParams': [{'Name': 'maxLength', 'Value': '255'}]}, {'Id': 1, 'Name': 'to', 'Value': 'test@org.com', 'Type': 'string', 'TypeParams': [{'Name': 'maxLength', 'Value': '255'}]}, {'Id': 1, 'Name': 'from', 'Value': 'abc@corp.com', 'Type': 'string', 'TypeParams': [{'Name': 'maxLength', 'Value': '255'}]}, {'Id': 1, 'Name': 'message', 'Value': 'Event occurred for Device Name: $name, Device IP Address: $ip', 'Type': 'string', 'TypeParams': [{'Name': 'maxLength', 'Value': '255'}]}]}], 'UndiscoveredTargets': [], 'State': True, 'Owner': 10069}})
  The policy which was created or modified.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'CMON7011', 'RelatedProperties': [], 'Message': 'Unable to create or modify the alert policy because an invalid value [To Email] is entered for the action Email.', 'MessageArgs': ['[To Email]', 'Email'], 'Severity': 'Warning', 'Resolution': 'Enter a valid value for the action identified in the message and retry the operation.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

