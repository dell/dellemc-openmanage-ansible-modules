.. _idrac_network_attributes_module:


idrac_network_attributes -- Configures the iDRAC network attributes
===================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows you to configure the port and partition network attributes on the network interface cards.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  network_adapter_id (True, str, None)
    FQDD of the network adapter device that represents the physical network adapter capable of connecting to a computer network.

    An example of FQDD of the network adapter is 'NIC.Mezzanine.1A'


  network_device_function_id (True, str, None)
    FQDD of the network adapter device function that represents a logical interface exposed by the network adapter.

    An example of FQDD of the network adapter device function is 'NIC.Mezzanine.1A-1-1'


  network_attributes (optional, dict, None)
    Dictionary of network attributes and value. To view the list of attributes and its structure, see the below API \ `https://I(idrac\_ip <https://I(idrac_ip>`__\ /redfish/v1/Systems/System.Embedded.1/NetworkAdapters/\<network\_adapter\_id\>/NetworkDeviceFunctions/ \<network\_device\_function\_id\>/Settings) and \ `https://\<idrac\_ip\>/redfish/v1/Schemas/NetworkDeviceFunction.v1\_8\_0.json <https://%3Cidrac_ip%3E/redfish/v1/Schemas/NetworkDeviceFunction.v1_8_0.json>`__.

    :emphasis:`network\_attributes` is mutually exclusive with :emphasis:`oem\_network\_attributes`.


  oem_network_attributes (optional, dict, None)
    The attributes must be part of the Integrated Dell Remote Access Controller Attribute Registry. To view the list of attributes in Attribute Registry for iDRAC9 and newer versions. For more information, see, \ `https://I(idrac\_ip <https://I(idrac_ip>`__\ /redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/\<network\_adapter\_id\>/NetworkDeviceFunctions/ \<network\_device\_function\_id\>/Oem/Dell/DellNetworkAttributes/\<network\_device\_function\_id\>) and \ `https://I(idrac\_ip <https://I(idrac_ip>`__\ /redfish/v1/Registries/NetworkAttributesRegistry\_\<network\_device\_function\_id\>/ NetworkAttributesRegistry\_network\_port\_id.json).

    For iDRAC8 based servers, derive the network attribute name from Server Configuration Profile.

    :emphasis:`oem\_network\_attributes` is mutually exclusive with :emphasis:`network\_attributes`.


  resource_id (optional, str, None)
    Id of the resource.

    If the value for resource ID is not provided, the module picks the first resource ID available from the list of system resources returned by the iDRAC.


  clear_pending (optional, bool, False)
    This parameter allows you to clear all the pending OEM network attributes changes.

    :literal:`false` does not perform any operation.

    :literal:`true` discards any pending changes to network attributes, or if a job is in scheduled state, removes the job.

    :emphasis:`apply\_time` value will be ignored and will not have any impact for :emphasis:`clear\_pending` operation.

    This operation is not supported for iDRAC8.


  apply_time (True, str, None)
    Apply time of the :emphasis:`network\_attributes` and :emphasis:`oem\_network\_attributes`.

    This is applicable only to :emphasis:`network\_attributes` and :emphasis:`oem\_network\_attributes`.

    :literal:`Immediate` allows the user to immediately reboot the host and apply the changes. :emphasis:`job\_wait` is applicable. This is applicable for :emphasis:`oem\_network\_attributes` and :emphasis:`job\_wait`.

    :literal:`OnReset` allows the user to apply the changes on the next reboot of the host server.

    :literal:`AtMaintenanceWindowStart` allows the user to apply at the start of a maintenance window as specified in :emphasis:`maintenance\_window`. A reboot job is scheduled.

    :literal:`InMaintenanceWindowOnReset` allows to apply after a manual reset but within the maintenance window as specified in :emphasis:`maintenance\_window`.

    This is not applicable for iDRAC8 and value will be ignored and will not have any impact for configuring :emphasis:`oem\_network\_attributes`.

    For iDRAC10, only :literal:`OnReset` is supported.


  maintenance_window (optional, dict, None)
    This option allows you to schedule the maintenance window.

    This is required when :emphasis:`apply\_time` is :literal:`AtMaintenanceWindowStart` or :literal:`InMaintenanceWindowOnReset`.


    start_time (True, str, None)
      The start time for the maintenance window to be scheduled.

      The format is YYYY-MM-DDThh:mm:ss\<offset\>

      \<offset\> is the time offset from UTC that the current timezone set in iDRAC in the format: +05:30 for IST.


    duration (True, int, None)
      The duration in seconds for the maintenance window.



  job_wait (optional, bool, True)
    Provides the option to wait for job completion.

    This is applicable when :emphasis:`apply\_time` is :literal:`Immediate` for :emphasis:`oem\_network\_attributes`.


  job_wait_timeout (optional, int, 1200)
    The maximum wait time of :emphasis:`job\_wait` in seconds. The job is tracked only for this duration.

    This option is applicable when :emphasis:`job\_wait` is :literal:`true`.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (False, str, None)
    iDRAC username.

    If the username is not provided, then the environment variable :envvar:`IDRAC\_USERNAME` is used.

    Example: export IDRAC\_USERNAME=username


  idrac_password (False, str, None)
    iDRAC user password.

    If the password is not provided, then the environment variable :envvar:`IDRAC\_PASSWORD` is used.

    Example: export IDRAC\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable :envvar:`IDRAC\_X\_AUTH\_TOKEN` is used.

    Example: export IDRAC\_X\_AUTH\_TOKEN=x\_auth\_token


  idrac_port (optional, int, 443)
    iDRAC port.


  validate_certs (optional, bool, True)
    If :literal:`false`\ , the SSL certificates will not be validated.

    Configure :literal:`false` only on personally controlled sites where self-signed certificates are used.

    Prior to collection version :literal:`5.0.0`\ , the :emphasis:`validate\_certs` is :literal:`false` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports both IPv4 and IPv6 address.
   - This module supports :literal:`check\_mode`.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Configure OEM network attributes
      dellemc.openmanage.idrac_network_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        network_adapter_id: "NIC.Integrated.1"
        network_device_function_id: "NIC.Integrated.1-1-1"
        apply_time: "Immediate"
        oem_network_attributes:
          BannerMessageTimeout: "4"

    - name: Configure OEM network attributes to apply on reset
      dellemc.openmanage.idrac_network_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        network_adapter_id: NIC.Integrated.1
        network_device_function_id: "NIC.Integrated.1-1-1"
        oem_network_attributes:
          BannerMessageTimeout: "4"
        apply_time: OnReset

    - name: Configure OEM network attributes to apply at maintainance window
      dellemc.openmanage.idrac_network_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        network_adapter_id: NIC.Integrated.1
        network_device_function_id: "NIC.Integrated.1-1-1"
        oem_network_attributes:
          BannerMessageTimeout: "4"
        apply_time: AtMaintenanceWindowStart
        maintenance_window:
          start_time: "2022-09-30T05:15:40-05:00"
          duration: 600

    - name: Clearing the pending attributes
      dellemc.openmanage.idrac_network_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        network_adapter_id: NIC.Integrated.1
        network_device_function_id: "NIC.Integrated.1-1-1"
        apply_time: "Immediate"
        clear_pending: true

    - name: Clearing the OEM pending attributes and apply the OEM network attributes
      dellemc.openmanage.idrac_network_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        network_adapter_id: NIC.Integrated.1
        network_device_function_id: "NIC.Integrated.1-1-1"
        apply_time: "Immediate"
        clear_pending: true
        oem_network_attributes:
          BannerMessageTimeout: "4"

    - name: Configure OEM network attributes and wait for the job
      dellemc.openmanage.idrac_network_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        network_adapter_id: NIC.Integrated.1
        network_device_function_id: "NIC.Integrated.1-1-1"
        apply_time: "Immediate"
        oem_network_attributes:
          LnkSpeed: "10MbpsHalf"
          WakeOnLan: "Enabled"
          VLanMode: "Enabled"
        job_wait: true
        job_wait_timeout: 2000

    - name: Configure redfish network attributes to update fiber channel on reset
      dellemc.openmanage.idrac_network_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        network_adapter_id: NIC.Integrated.1
        network_device_function_id: "NIC.Integrated.1-1-1"
        apply_time: OnReset
        network_attributes:
          Ethernet:
            VLAN:
              VLANEnable: true

    - name: Configure redfish network attributes to apply on reset
      dellemc.openmanage.idrac_network_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        network_adapter_id: NIC.Integrated.1
        network_device_function_id: "NIC.Integrated.1-1-1"
        network_attributes:
          Ethernet:
            VLAN:
              VLANEnable: true
        apply_time: OnReset

    - name: Configure redfish network attributes of iscsi to apply at maintainance window start
      dellemc.openmanage.idrac_network_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        network_adapter_id: NIC.Integrated.1
        network_device_function_id: "NIC.Integrated.1-1-1"
        network_attributes:
          iSCSIBoot:
            InitiatorIPAddress: 1.0.0.1
        apply_time: AtMaintenanceWindowStart
        maintenance_window:
          start_time: "2022-09-30T05:15:40-05:00"
          duration: 600

    - name: Configure redfish network attributes to apply at maintainance window on reset
      dellemc.openmanage.idrac_network_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        network_adapter_id: NIC.Integrated.1
        network_device_function_id: "NIC.Integrated.1-1-1"
        network_attributes:
          Ethernet:
            VLAN:
              VLANEnable: false
              VLANId: 1
        apply_time: AtMaintenanceWindowStart
        maintenance_window:
          start_time: "2022-09-30T05:15:40-05:00"
          duration: 600



Return Values
-------------

msg (when network attributes is applied, str, Successfully updated the network attributes.)
  Status of the attribute update operation.


invalid_attributes (On invalid attributes or values, dict, {'IscsiInitiatorIpAddr': 'Attribute is not valid.', 'IscsiInitiatorSubnet': 'Attribute is not valid.'})
  Dictionary of invalid attributes provided that cannot be applied.


job_status (always, dict, {'ActualRunningStartTime': None, 'ActualRunningStopTime': None, 'CompletionTime': None, 'Description': 'Job Instance', 'EndTime': 'TIME_NA', 'Id': 'JID_XXXXXXXXX', 'JobState': 'Scheduled', 'JobType': 'NICConfiguration', 'Message': 'Task successfully scheduled.', 'MessageArgs': [], 'MessageId': 'JCP001', 'Name': 'Configure: NIC.Integrated.1-1-1', 'PercentComplete': 0, 'StartTime': '2023-08-07T06:21:24', 'TargetSettingsURI': None})
  Returns the output for status of the job.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Abhishek Sinha(@ABHISHEK-SINHA10)
- Kritika Bhateja (@Kritika-Bhateja-03)

