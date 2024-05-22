.. _ome_smart_fabric_uplink_module:


ome_smart_fabric_uplink -- Create, modify or delete a uplink for a fabric on OpenManage Enterprise Modular
==========================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to create, modify or delete an uplink for a fabric.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  state (optional, str, present)
    \ :literal:`present`\  - Creates a new uplink with the provided \ :emphasis:`name`\ . - Modifies an existing uplink with the provided \ :emphasis:`name`\ .

    \ :literal:`absent`\  – Deletes the uplink with the provided \ :emphasis:`name`\ .

    \ :emphasis:`WARNING`\  Delete operation can impact the network infrastructure.


  fabric_name (True, str, None)
    Provide the \ :emphasis:`fabric\_name`\  of the fabric for which the uplink is to be configured.


  name (True, str, None)
    Provide the \ :emphasis:`name`\  of the uplink to be created, modified or deleted.


  new_name (optional, str, None)
    Provide the new \ :emphasis:`new\_name`\  for the uplink.


  description (optional, str, None)
    Provide a short description for the uplink to be created or modified.


  uplink_type (optional, str, None)
    Specify the uplink type.

    \ :emphasis:`NOTE`\  The uplink type cannot be changed for an existing uplink.


  ufd_enable (optional, str, None)
    Add or Remove the uplink to the Uplink Failure Detection (UFD) group. The UFD group identifies the loss of connectivity to the upstream switch and notifies the servers that are connected to the switch. During an uplink failure, the switch disables the corresponding downstream server ports. The downstream servers can then select alternate connectivity routes, if available.

    \ :emphasis:`WARNING`\  The firmware version of the I/O Module running the Fabric Manager must support this configuration feature. If not, uplink creation will be successful with an appropriate error message in response.


  primary_switch_service_tag (optional, str, None)
    Service tag of the primary switch.


  primary_switch_ports (optional, list, None)
    The IOM slots to be connected to the primary switch.

    \ :emphasis:`primary\_switch\_service\_tag`\  is mandatory for this option.


  secondary_switch_service_tag (optional, str, None)
    Service tag of the secondary switch.


  secondary_switch_ports (optional, list, None)
    The IOM slots to be connected to the secondary switch.

    \ :emphasis:`secondary\_switch\_service\_tag`\  is mandatory for this option.


  tagged_networks (optional, list, None)
    VLANs to be associated with the uplink \ :emphasis:`name`\ .


  untagged_network (optional, str, None)
    Specify the name of the VLAN to be added as untagged to the uplink.


  hostname (True, str, None)
    OpenManage Enterprise Modular IP address or hostname.


  username (False, str, None)
    OpenManage Enterprise Modular username.

    If the username is not provided, then the environment variable \ :envvar:`OME\_USERNAME`\  is used.

    Example: export OME\_USERNAME=username


  password (False, str, None)
    OpenManage Enterprise Modular password.

    If the password is not provided, then the environment variable \ :envvar:`OME\_PASSWORD`\  is used.

    Example: export OME\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`OME\_X\_AUTH\_TOKEN`\  is used.

    Example: export OME\_X\_AUTH\_TOKEN=x\_auth\_token


  port (optional, int, 443)
    OpenManage Enterprise Modular HTTPS port.


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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise Modular.
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Create an Uplink
      dellemc.openmanage.ome_smart_fabric_uplink:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "present"
        fabric_name: "fabric1"
        name: "uplink1"
        description: "CREATED from OMAM"
        uplink_type: "Ethernet"
        ufd_enable: "Enabled"
        primary_switch_service_tag: "ABC1234"
        primary_switch_ports:
          - ethernet1/1/13
          - ethernet1/1/14
        secondary_switch_service_tag: "XYZ1234"
        secondary_switch_ports:
          - ethernet1/1/13
          - ethernet1/1/14
        tagged_networks:
          - vlan1
          - vlan3
        untagged_network: vlan2
      tags: create_uplink

    - name: Modify an existing uplink
      dellemc.openmanage.ome_smart_fabric_uplink:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "present"
        fabric_name: "fabric1"
        name: "uplink1"
        new_name: "uplink2"
        description: "Modified from OMAM"
        uplink_type: "Ethernet"
        ufd_enable: "Disabled"
        primary_switch_service_tag: "DEF1234"
        primary_switch_ports:
          - ethernet1/2/13
          - ethernet1/2/14
        secondary_switch_service_tag: "TUV1234"
        secondary_switch_ports:
          - ethernet1/2/13
          - ethernet1/2/14
        tagged_networks:
          - vlan11
          - vlan33
        untagged_network: vlan22
      tags: modify_uplink

    - name: Delete an Uplink
      dellemc.openmanage.ome_smart_fabric_uplink:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "absent"
        fabric_name: "fabric1"
        name: "uplink1"
      tags: delete_uplink

    - name: Modify an Uplink name
      dellemc.openmanage.ome_smart_fabric_uplink:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "present"
        fabric_name: "fabric1"
        name: "uplink1"
        new_name: "uplink2"
      tags: modify_uplink_name

    - name: Modify Uplink ports
      dellemc.openmanage.ome_smart_fabric_uplink:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "present"
        fabric_name: "fabric1"
        name: "uplink1"
        description: "uplink ports modified"
        primary_switch_service_tag: "ABC1234"
        primary_switch_ports:
          - ethernet1/1/6
          - ethernet1/1/7
        secondary_switch_service_tag: "XYZ1234"
        secondary_switch_ports:
          - ethernet1/1/9
          - ethernet1/1/10
      tags: modify_ports

    - name: Modify Uplink networks
      dellemc.openmanage.ome_smart_fabric_uplink:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "present"
        fabric_name: "fabric1"
        name: "create1"
        description: "uplink networks modified"
        tagged_networks:
          - vlan4
      tags: modify_networks



Return Values
-------------

msg (always, str, Successfully modified the uplink.)
  Overall status of the uplink operation.


uplink_id (when I(state=present), str, ddc3d260-fd71-46a1-97f9-708e12345678)
  Returns the ID when an uplink is created or modified.


additional_info (when I(state=present) and additional information present in response., dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to configure the Uplink Failure Detection mode on the uplink because the firmware version of the I/O Module running the Fabric Manager does not support the configuration feature.', 'MessageArgs': [], 'MessageId': 'CDEV7151', 'RelatedProperties': [], 'Resolution': "Update the firmware version of the I/O Module running the Fabric Manager and retry the operation. For information about the recommended I/O Module firmware versions, see the OpenManage Enterprise-Modular User's Guide available on the support site.", 'Severity': 'Informational'}], 'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.'}})
  Additional details of the fabric operation.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'CGEN1006', 'RelatedProperties': [], 'Message': 'Unable to complete the request because the resource URI does not exist or is not implemented.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': "Check the request resource URI. Refer to the OpenManage Enterprise-Modular User's Guide for more information about resource URI and its properties."}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

