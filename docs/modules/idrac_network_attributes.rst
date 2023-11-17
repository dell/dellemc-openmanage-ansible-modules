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

- python >= 3.9.6



Parameters
----------

  network_adapter_id (True, str, None)
    FQDD of the network adapter device that represents the physical network adapter capable of connecting to a computer network.

    An example of FQDD of the network adapter is 'NIC.Mezzanine.1A'


  network_device_function_id (True, str, None)
    FQDD of the network adapter device function that represents a logical interface exposed by the network adapter.

    An example of FQDD of the network adapter device function is 'NIC.Mezzanine.1A-1-1'


  network_attributes (optional, dict, None)
    Dictionary of network attributes and value. To view the list of attributes and its structure, see the below API https://*idrac_ip*/redfish/v1/Systems/System.Embedded.1/NetworkAdapters/<network_id>/NetworkDeviceFunctions/ <network_port_id>/Settings and https://<idrac_ip>/redfish/v1/Schemas/NetworkDeviceFunction.v1_8_0.json.

    *network_attributes* is mutually exclusive with *oem_network_attributes*.


  oem_network_attributes (optional, dict, None)
    The attributes must be part of the Integrated Dell Remote Access Controller Attribute Registry. To view the list of attributes in Attribute Registry for iDRAC9 and newer versions. For more information, see, https://*idrac_ip*/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/<network_id>/NetworkDeviceFunctions/ <network_port_id>/Oem/Dell/DellNetworkAttributes/<network_port_id> and https://*idrac_ip*/redfish/v1/Registries/NetworkAttributesRegistry_<network_port_id>/ NetworkAttributesRegistry_network_port_id.json.

    For iDRAC8 based servers, derive the network attribute name from Server Configuration Profile.

    *oem_network_attributes* is mutually exclusive with *network_attributes*.


  resource_id (optional, str, None)
    Id of the resource.

    If the value for resource ID is not provided, the module picks the first resource ID available from the list of system resources returned by the iDRAC.


  clear_pending (optional, bool, False)
    This parameter allows you to clear all the pending OEM network attributes changes.

    ``false`` does not perform any operation.

    ``true`` discards any pending changes to network attributes, or if a job is in scheduled state, removes the job.

    *apply_time* value will be ignored and will not have any impact for *clear_pending* operation.

    This operation is not supported for iDRAC8.


  apply_time (True, str, None)
    Apply time of the *network_attributes* and *oem_network_attributes*.

    This is applicable only to *network_attributes* and *oem_network_attributes*.

    ``Immediate`` allows the user to immediately reboot the host and apply the changes. *job_wait* is applicable. This is applicable for *oem_network_attributes* and *job_wait*.

    ``OnReset`` allows the user to apply the changes on the next reboot of the host server.

    ``AtMaintenanceWindowStart`` allows the user to apply at the start of a maintenance window as specified in *maintenance_window*. A reboot job is scheduled.

    ``InMaintenanceWindowOnReset`` allows to apply after a manual reset but within the maintenance window as specified in *maintenance_window*.

    This is not applicable for iDRAC8 and value will be ignored and will not have any impact for configuring *oem_network_attributes*.


  maintenance_window (optional, dict, None)
    This option allows you to schedule the maintenance window.

    This is required when *apply_time* is ``AtMaintenanceWindowStart`` or ``InMaintenanceWindowOnReset``.


    start_time (True, str, None)
      The start time for the maintenance window to be scheduled.

      The format is YYYY-MM-DDThh:mm:ss<offset>

      <offset> is the time offset from UTC that the current timezone set in iDRAC in the format: +05:30 for IST.


    duration (True, int, None)
      The duration in seconds for the maintenance window.



  job_wait (optional, bool, True)
    Provides the option to wait for job completion.

    This is applicable when *apply_time* is ``Immediate`` for *oem_network_attributes*.


  job_wait_timeout (optional, int, 1200)
    The maximum wait time of *job_wait* in seconds. The job is tracked only for this duration.

    This option is applicable when *job_wait* is ``true``.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.


  idrac_password (True, str, None)
    iDRAC user password.


  idrac_port (optional, int, 443)
    iDRAC port.


  validate_certs (optional, bool, True)
    If ``false``, the SSL certificates will not be validated.

    Configure ``false`` only on personally controlled sites where self-signed certificates are used.

    Prior to collection version ``5.0.0``, the *validate_certs* is ``false`` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports both IPv4 and IPv6 address.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Configure OEM network attributes
      dellemc.openmanage.idrac_network_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        network_id: "NIC.Integrated.1"
        network_port_id: "NIC.Integrated.1-1-1"
        apply_time: "Immediate"
        oem_network_attributes:
          BannerMessageTimeout: "4"

    - name: Configure OEM network attributes to apply on reset
      dellemc.openmanage.idrac_network_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        network_id: NIC.Integrated.1
        network_port_id: "NIC.Integrated.1-1-1"
        oem_network_attributes:
          BannerMessageTimeout: "4"
        apply_time: OnReset

    - name: Configure OEM network attributes to apply at maintainance window
      dellemc.openmanage.idrac_network_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        network_id: NIC.Integrated.1
        network_port_id: "NIC.Integrated.1-1-1"
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
        network_id: NIC.Integrated.1
        network_port_id: "NIC.Integrated.1-1-1"
        apply_time: "Immediate"
        clear_pending: true

    - name: Clearing the OEM pending attributes and apply the OEM network attributes
      dellemc.openmanage.idrac_network_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        network_id: NIC.Integrated.1
        network_port_id: "NIC.Integrated.1-1-1"
        apply_time: "Immediate"
        clear_pending: true
        oem_network_attributes:
          BannerMessageTimeout: "4"

    - name: Configure OEM network attributes and wait for the job
      dellemc.openmanage.idrac_network_attributes:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        network_id: NIC.Integrated.1
        network_port_id: "NIC.Integrated.1-1-1"
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
        network_id: NIC.Integrated.1
        network_port_id: "NIC.Integrated.1-1-1"
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
        network_id: NIC.Integrated.1
        network_port_id: "NIC.Integrated.1-1-1"
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
        network_id: NIC.Integrated.1
        network_port_id: "NIC.Integrated.1-1-1"
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
        network_id: NIC.Integrated.1
        network_port_id: "NIC.Integrated.1-1-1"
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

