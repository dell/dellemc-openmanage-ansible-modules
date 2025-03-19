.. _ome_smart_fabric_module:


ome_smart_fabric -- Create, modify or delete a fabric on OpenManage Enterprise Modular
======================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to create a fabric, and modify or delete an existing fabric on OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  state (optional, str, present)
    \ :literal:`present`\  creates a new fabric or modifies an existing fabric.

    \ :literal:`absent`\  deletes an existing fabric.

    Notes: The create, modify, or delete fabric operation takes around 15-20 minutes to complete. It is recommended not to start an another operation until the current operation is completed.


  name (True, str, None)
    Provide the \ :emphasis:`name`\  of the fabric to be created, deleted or modified.


  new_name (optional, str, None)
    Provide the \ :emphasis:`name`\  of the fabric to be modified.


  description (optional, str, None)
    Provide a short description of the fabric to be created or modified.


  fabric_design (optional, str, None)
    Specify the fabric topology.See the use API \ https://www.dell.com/support/manuals/en-in/poweredge-mx7000/omem_1_20_10_ug/smartfabric-network-topologies\  to know why its topology.

    \ :emphasis:`fabric\_design`\  is mandatory for fabric creation.


  primary_switch_service_tag (optional, str, None)
    Service tag of the first switch.

    \ :emphasis:`primary\_switch\_service\_tag`\  is mandatory for fabric creation.

    \ :emphasis:`primary\_switch\_service\_tag`\  must belong to the model selected in \ :emphasis:`fabric\_design`\ .


  secondary_switch_service_tag (optional, str, None)
    Service tag of the second switch.

    \ :emphasis:`secondary\_switch\_service\_tag`\  is mandatory for fabric creation.

    \ :emphasis:`secondary\_switch\_service\_tag`\  must belong to the model selected in \ :emphasis:`fabric\_design`\ .


  override_LLDP_configuration (optional, str, None)
    Enable this configuration to allow Fabric Management Address to be included in LLDP messages.

    Notes: OpenManage Enterprise Modular 1.0 does not support this option. Some software networking solutions require a single management address to be transmitted by all Ethernet switches to represent the entire fabric. Enable this feature only when connecting to such a solution.


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
    - name: Create a fabric
      dellemc.openmanage.ome_smart_fabric:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: present
        name: "fabric1"
        description: "fabric desc"
        fabric_design: "2xMX9116n_Fabric_Switching_Engines_in_different_chassis"
        primary_switch_service_tag: "SVTG123"
        secondary_switch_service_tag: "PXYT456"
        override_LLDP_configuration: "Enabled"

    - name: Modify a fabric
      dellemc.openmanage.ome_smart_fabric:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: present
        name: "fabric1"
        new_name: "fabric_gold1"
        description: "new description"

    - name: Delete a fabric
      dellemc.openmanage.ome_smart_fabric:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        state: "absent"
        name: "fabric1"



Return Values
-------------

msg (always, str, Fabric creation operation is initiated.)
  Overall status of the fabric operation.


fabric_id (success, str, 1312cceb-c3dd-4348-95c1-d8541a17d776)
  Returns the ID when an fabric is created, modified or deleted.


additional_info (when I(state=present) and additional information present in response., dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'RelatedProperties': [], 'Message': 'Fabric update is successful. The OverrideLLDPConfiguration attribute is not provided in the payload, so it preserves the previous value.', 'MessageArgs': [], 'Severity': 'Informational', 'Resolution': 'Please update the Fabric with the OverrideLLDPConfiguration as Disabled or Enabled if necessary.'}]}})
  Additional details of the fabric operation.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'RelatedProperties': [], 'Message': 'Unable to perform operation, because the fabric manager was not reachable.', 'MessageArgs': [], 'Severity': 'Warning', 'Resolution': 'Make sure of the following and retry the operation: 1) There is at least one advanced I/O Module in power-on mode. For example, MX9116n Ethernet Switch and MX5108n Ethernet Switch. However, if an advanced I/O Module is available in the power-on mode, make sure that the network profile is not set when the fabric manager is in the switch-over mode. 2) If the issue persists, wait for few minutes and retry the operation.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Sajna Shetty(@Sajna-Shetty)

