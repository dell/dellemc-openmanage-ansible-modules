.. _ome_server_interface_profiles_module:


ome_server_interface_profiles -- Configure server interface profiles
====================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to configure server interface profiles on OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  device_id (optional, list, None)
    Device id of the Server under chassis fabric.

    \ :emphasis:`device\_id`\  and \ :emphasis:`device\_service\_tag`\  is mutually exclusive.


  device_service_tag (optional, list, None)
    Service tag of the Server under chassis fabric.

    \ :emphasis:`device\_service\_tag`\  and \ :emphasis:`device\_id`\  is mutually exclusive.


  nic_teaming (optional, str, None)
    NIC teaming options.

    \ :literal:`NoTeaming`\  the NICs are not bonded and provide no load balancing or redundancy.

    \ :literal:`LACP`\  use LACP for NIC teaming.

    \ :literal:`Other`\  use other technology for NIC teaming.


  nic_configuration (optional, list, None)
    NIC configuration for the Servers to be applied.


    nic_identifier (True, str, None)
      ID of the NIC or port number.

      \ :literal:`Note`\  This will not be validated.


    team (optional, bool, None)
      Group two or more ports. The ports must be connected to the same pair of Ethernet switches.

      \ :emphasis:`team`\  is applicable only if \ :emphasis:`nic\_teaming`\  is \ :literal:`LACP`\ .


    untagged_network (optional, int, None)
      The maximum or minimum VLAN id of the network to be untagged.

      The \ :emphasis:`untagged\_network`\  can be retrieved using the \ :ref:`dellemc.openmanage.ome\_network\_vlan\_info <ansible_collections.dellemc.openmanage.ome_network_vlan_info_module>`\ 

      If \ :emphasis:`untagged\_network`\  needs to be unset this needs to be sent as \ :literal:`0`\ 

      \ :literal:`Note`\  The network cannot be added as a untagged network if it is already assigned to a tagged network.


    tagged_networks (optional, dict, None)
      List of tagged networks

      Network cannot be added as a tagged network if it is already assigned to untagged network


      state (optional, str, present)
        Indicates if a list of networks needs to be added or deleted.

        \ :literal:`present`\  to add the network to the tagged list

        \ :literal:`absent`\  to delete the Network from the tagged list


      names (True, list, None)
        List of network name to be marked as tagged networks

        The \ :emphasis:`names`\  can be retrieved using the \ :ref:`dellemc.openmanage.ome\_network\_vlan\_info <ansible_collections.dellemc.openmanage.ome_network_vlan_info_module>`\ 




  job_wait (optional, bool, True)
    Provides the option to wait for job completion.


  job_wait_timeout (optional, int, 120)
    The maximum wait time of \ :emphasis:`job\_wait`\  in seconds. The job is  tracked only for this duration.

    This option is applicable when \ :emphasis:`job\_wait`\  is \ :literal:`true`\ .


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
   - This module supports \ :literal:`check\_mode`\ .
   - Run this module from a system that has direct access to Dell OpenManage Enterprise Modular.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Modify Server Interface Profile for the server using the service tag
      dellemc.openmanage.ome_server_interface_profiles:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_service_tag:
          - SVCTAG1
          - SVCTAG2
        nic_teaming: LACP
        nic_configuration:
          - nic_identifier: NIC.Mezzanine.1A-1-1
            team: false
            untagged_network: 2
            tagged_networks:
              names:
                - vlan1
          - nic_identifier: NIC.Mezzanine.1A-2-1
            team: true
            untagged_network: 3
            tagged_networks:
              names:
                - range120-125

    - name: Modify Server Interface Profile for the server using the device id
      dellemc.openmanage.ome_server_interface_profiles:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_id:
          - 34523
          - 48999
        nic_teaming: NoTeaming
        nic_configuration:
          - nic_identifier: NIC.Mezzanine.1A-1-1
            team: false
            untagged_network: 2
            tagged_networks:
              names:
                - vlan2
          - nic_identifier: NIC.Mezzanine.1A-2-1
            team: true
            untagged_network: 3
            tagged_networks:
              names:
                - range120-125



Return Values
-------------

msg (always, str, Successfully triggered apply server profiles job.)
  Status of the overall server interface operation.


job_id (on applying the Interface profiles, int, 14123)
  Job ID of the task to apply the server interface profiles.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V (@jagadeeshnv)

