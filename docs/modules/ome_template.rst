.. _ome_template_module:


ome_template -- Create, modify, deploy, delete, export, import and clone a template on OpenManage Enterprise
============================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module creates, modifies, deploys, deletes, exports, imports and clones a template on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7.5



Parameters
----------

  command (optional, str, create)
    ``create`` creates a new template.

    ``modify`` modifies an existing template.

    ``deploy`` creates a template-deployment job.

    ``delete`` deletes an existing template.

    ``export`` exports an existing template.

    ``import`` creates a template from a specified configuration text in SCP XML format.

    ``clone`` creates a clone of a existing template.


  template_id (optional, int, None)
    ID of the existing template.

    This option is applicable when *command* is ``modify``, ``deploy``, ``delete`` and ``export``.

    This option is mutually exclusive with *template_name*.


  template_name (optional, str, None)
    Name of the existing template.

    This option is applicable when *command* is ``modify``, ``deploy``, ``delete`` and ``export``.

    This option is mutually exclusive with *template_id*.


  device_id (optional, list, [])
    Specify the list of targeted device ID(s) when *command* is ``deploy``. When I (command) is ``create``, specify the ID of a single device.

    Either *device_id* or *device_service_tag* is mandatory or both can be applicable.


  device_service_tag (optional, list, [])
    Specify the list of targeted device service tags when I (command) is ``deploy``. When *command* is ``create``, specify the service tag of a single device.

    Either *device_id* or *device_service_tag* is mandatory or both can be applicable.


  device_group_names (optional, list, [])
    Specify the list of groups when I (command) is ``deploy``.

    Provide at least one of the mandatory options *device_id*, *device_service_tag*, or *device_group_names*.


  template_view_type (optional, str, Deployment)
    Select the type of view of the OME template.

    This is applicable when *command* is ``create``,``clone`` and ``import``.


  attributes (optional, dict, None)
    Payload data for the template operations. All the variables in this option are added as payload for ``create``, ``modify``, ``deploy``, ``import``, and ``clone`` operations. It takes the following attributes.

    Attributes: List of dictionaries of attributes (if any) to be modified in the deployment template. This is applicable when *command* is ``deploy`` and ``modify``.

    Name: Name of the template. This is mandatory when *command* is ``create``, ``import``, ``clone``, and optional when *command* is ``modify``.

    Description: Description for the template. This is applicable when *command* is ``create`` or ``modify``.

    Fqdds: This allows to create a template using components from a specified reference server. One or more, of the following values must be specified in a comma-separated string: iDRAC, System, BIOS, NIC, LifeCycleController, RAID, and EventFilters. If none of the values are specified, the default value 'All' is selected. This is applicable when I (command) is ``create``.

    Options: Options to control device shutdown or end power state post template deployment. This is applicable for ``deploy`` operation.

    Schedule: Provides options to schedule the deployment task immediately, or at a specified time. This is applicable when *command* is ``deploy``.

    NetworkBootIsoModel: Payload to specify the ISO deployment details. This is applicable when *command* is ``deploy``.

    Content: The XML content of template. This is applicable when *command* is ``import``.

    Type: Template type ID, indicating the type of device for which configuration is supported, such as chassis and servers. This is applicable when *command* is ``import``.

    TypeId: Template type ID, indicating the type of device for which configuration is supported, such as chassis and servers. This is applicable when *command* is ``create``.

    Refer OpenManage Enterprise API Reference Guide for more details.


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
   - Run this module from a system that has direct access to DellEMC OpenManage Enterprise.
   - This module does not support ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create a template from a reference device
      dellemc.openmanage.ome_template:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        device_id: 25123
        attributes:
          Name: "New Template"
          Description: "New Template description"

    - name: Modify template name, description, and attribute value
      dellemc.openmanage.ome_template:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        command: "modify"
        template_id: 12
        attributes:
          Name: "New Custom Template"
          Description: "Custom Template Description"
          # Attributes to be modified in the template.
          # For information on any attribute id, use API /TemplateService/Templates(Id)/Views(Id)/AttributeViewDetails
          # This section is optional
          Attributes:
            - Id: 1234
              Value: "Test Attribute"
              IsIgnored: false

    - name: Deploy template on multiple devices
      dellemc.openmanage.ome_template:
        hostname:  "192.168.0.1"
        username: "username"
        password: "password"
        command: "deploy"
        template_id: 12
        device_id:
          - 12765
          - 10173
        device_service_tag:
          - 'SVTG123'
          - 'SVTG456'

    - name: Deploy template on groups
      dellemc.openmanage.ome_template:
        hostname:  "192.168.0.1"
        username: "username"
        password: "password"
        command: "deploy"
        template_id: 12
        device_group_names:
          - server_group_1
          - server_group_2

    - name: Deploy template on multiple devices along with the attributes values to be modified on the target devices
      dellemc.openmanage.ome_template:
        hostname:  "192.168.0.1"
        username: "username"
        password: "password"
        command: "deploy"
        template_id: 12
        device_id:
          - 12765
          - 10173
        device_service_tag:
          - 'SVTG123'
        attributes:
          # Device specific attributes to be modified during deployment.
          # For information on any attribute id, use API /TemplateService/Templates(Id)/Views(Id)/AttributeViewDetails
          # This section is optional
          Attributes:
            # specific device where attribute to be modified at deployment run-time.
            # The DeviceId should be mentioned above in the 'device_id' section.
            # Service tags not allowed.
            - DeviceId: 12765
              Attributes:
                - Id : 15645
                  Value : "0.0.0.0"
                  IsIgnored : false
            - DeviceId: 10173
              Attributes:
                - Id : 18968,
                  Value : "hostname-1"
                  IsIgnored : false

    - name: Deploy template and Operating System (OS) on multiple devices
      dellemc.openmanage.ome_template:
        hostname:  "192.168.0.1"
        username: "username"
        password: "password"
        command: "deploy"
        template_id: 12
        device_id:
          - 12765
        device_service_tag:
          - 'SVTG123'
        attributes:
          # Include this to install OS on the devices.
          # This section is optional
          NetworkBootIsoModel:
            BootToNetwork: true
            ShareType: "NFS"
            IsoTimeout: 1 # allowable values(1,2,4,8,16) in hours
            IsoPath: "/home/iso_path/filename.iso"
            ShareDetail:
              IpAddress: "192.168.0.2"
              ShareName: "sharename"
              User: "share_user"
              Password: "share_password"
          Options:
            EndHostPowerState: 1
            ShutdownType: 0
            TimeToWaitBeforeShutdown: 300
          Schedule:
            RunLater: true
            RunNow: false

    - name: "Deploy template on multiple devices and changes the device-level attributes. After the template is deployed,
    install OS using its image"
      dellemc.openmanage.ome_template:
        hostname:  "192.168.0.1"
        username: "username"
        password: "password"
        command: "deploy"
        template_id: 12
        device_id:
          - 12765
          - 10173
        device_service_tag:
          - 'SVTG123'
          - 'SVTG456'
        attributes:
          Attributes:
            - DeviceId: 12765
              Attributes:
                - Id : 15645
                  Value : "0.0.0.0"
                  IsIgnored : false
            - DeviceId: 10173
              Attributes:
                - Id : 18968,
                  Value : "hostname-1"
                  IsIgnored : false
          NetworkBootIsoModel:
            BootToNetwork: true
            ShareType: "NFS"
            IsoTimeout: 1 # allowable values(1,2,4,8,16) in hours
            IsoPath: "/home/iso_path/filename.iso"
            ShareDetail:
              IpAddress: "192.168.0.2"
              ShareName: "sharename"
              User: "share_user"
              Password: "share_password"
          Options:
            EndHostPowerState: 1
            ShutdownType: 0
            TimeToWaitBeforeShutdown: 300
          Schedule:
            RunLater: true
            RunNow: false

    - name: Delete template
      dellemc.openmanage.ome_template:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        command: "delete"
        template_id: 12

    - name: Export a template
      dellemc.openmanage.ome_template:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        command: "export"
        template_id: 12

    # Start of example to export template to a local xml file
    - name: Export template to a local xml file
      dellemc.openmanage.ome_template:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        command: "export"
        template_name: "my_template"
      register: result
    - name: Save template into a file
      ansible.builtin.copy:
        content: "{{ result.Content}}"
        dest: "/path/to/exported_template.xml"
    # End of example to export template to a local xml file

    - name: Clone a template
      dellemc.openmanage.ome_template:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        command: "clone"
        template_id: 12
        attributes:
          Name: "New Cloned Template Name"

    - name: Import template from XML content
      dellemc.openmanage.ome_template:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        command: "import"
        attributes:
          Name: "Imported Template Name"
          # Template Type from TemplateService/TemplateTypes
          Type: 2
          # xml string content
          Content: "<SystemConfiguration Model=\"PowerEdge R940\" ServiceTag=\"SVCTAG1\"
          TimeStamp=\"Tue Sep 24 09:20:57.872551 2019\">\n<Component FQDD=\"AHCI.Slot.6-1\">\n<Attribute
          Name=\"RAIDresetConfig\">True</Attribute>\n<Attribute Name=\"RAIDforeignConfig\">Clear</Attribute>\n
          </Component>\n<Component FQDD=\"Disk.Direct.0-0:AHCI.Slot.6-1\">\n<Attribute Name=\"RAIDPDState\">Ready
          </Attribute>\n<Attribute Name=\"RAIDHotSpareStatus\">No</Attribute>\n</Component>\n
          <Component FQDD=\"Disk.Direct.1-1:AHCI.Slot.6-1\">\n<Attribute Name=\"RAIDPDState\">Ready</Attribute>\n
          <Attribute Name=\"RAIDHotSpareStatus\">No</Attribute>\n</Component>\n</SystemConfiguration>\n"

    - name: Import template from local XML file
      dellemc.openmanage.ome_template:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        command: "import"
        attributes:
          Name: "Imported Template Name"
          Type: 2
          Content: "{{ lookup('ansible.builtin.file.', '/path/to/xmlfile') }}"

    - name: "Deploy template and Operating System (OS) on multiple devices."
      dellemc.openmanage.ome_template:
        hostname: "192.168.0.1"
        username: "username"
        password: "{{password}}"
        command: "deploy"
        template_id: 12
        device_id:
          - 12765
        device_service_tag:
          - 'SVTG123'
        attributes:
          # Include this to install OS on the devices.
          # This section is optional
          NetworkBootIsoModel:
            BootToNetwork: true
            ShareType: "CIFS"
            IsoTimeout: 1 # allowable values(1,2,4,8,16) in hours
            IsoPath: "/home/iso_path/filename.iso"
            ShareDetail:
              IpAddress: "192.168.0.2"
              ShareName: "sharename"
              User: "share_user"
              Password: "share_password"
          Options:
            EndHostPowerState: 1
            ShutdownType: 0
            TimeToWaitBeforeShutdown: 300
          Schedule:
            RunLater: true
            RunNow: false



Return Values
-------------

msg (always, str, Successfully created a template with ID 23)
  Overall status of the template operation.


return_id (success, when I(command) is C(create), C(modify), C(import), C(clone) and C(deploy), int, 12)
  ID of the template for ``create``, ``modify``, ``import`` and ``clone`` or task created in case of ``deploy``.


TemplateId (success, when I(command) is C(export), int, 13)
  ID of the template for ``export``.


Content (success, when I(command) is C(export), str, <SystemConfiguration Model="PowerEdge R940" ServiceTag="DG22TR2" TimeStamp="Tue Sep 24 09:20:57.872551 2019">
<Component FQDD="AHCI.Slot.6-1">
<Attribute Name="RAIDresetConfig">True</Attribute>
<Attribute Name="RAIDforeignConfig">Clear</Attribute>
</Component>
<Component FQDD="Disk.Direct.0-0:AHCI.Slot.6-1">
<Attribute Name="RAIDPDState">Ready</Attribute>
<Attribute Name="RAIDHotSpareStatus">No</Attribute>
</Component>
<Component FQDD="Disk.Direct.1-1:AHCI.Slot.6-1">
<Attribute Name="RAIDPDState">Ready </Attribute>
<Attribute Name="RAIDHotSpareStatus">No</Attribute>
</Component>
</SystemConfiguration>
) XML content of the exported template. This content can be written to a xml file.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V (@jagadeeshnv)

