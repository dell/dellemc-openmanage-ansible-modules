=================================================
Dell EMC OpenManage Ansible Modules Release Notes
=================================================

.. contents:: Topics


v6.3.0
======

Release Summary
---------------

Support for LockVirtualDisk operation and to configure Remote File Share settings using idrac_virtual_media module.

Major Changes
-------------

- idrac_redfish_storage_controller - This module is enhanced to support LockVirtualDisk operation.
- idrac_virtual_media - This module allows to configure Remote File Share settings.

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.idrac_virtual_media - Configure the virtual media settings.

v6.2.0
======

Release Summary
---------------

Added clear pending BIOS attributes, reset BIOS to default settings, and configure BIOS attribute using Redfish enhancements for idrac_bios.

Major Changes
-------------

- idrac_bios - The module is enhanced to support clear pending BIOS attributes, reset BIOS to default settings, and configure BIOS attribute using Redfish.

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

v6.1.0
======

Release Summary
---------------

Support for device-specific operations on OpenManage Enterprise and configuring boot settings on iDRAC.

Major Changes
-------------

- idrac_boot - Support for configuring the boot settings on iDRAC.
- ome_device_group - The module is enhanced to support the removal of devices from a static device group.
- ome_devices - Support for performing device-specific operations on OpenManage Enterprise.

Minor Changes
-------------

- ome_configuration_compliance_info - The module is enhanced to report single device compliance information.

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_local_access_configuration - Issue(215035) - The module reports ``Successfully updated the local access setting`` if an unsupported value is provided for the parameter timeout_limit. However, this value is not actually applied on OpenManage Enterprise Modular.
- ome_device_local_access_configuration - Issue(217865) - The module does not display a proper error message if an unsupported value is provided for the user_defined and lcd_language parameters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_device_quick_deploy - Issue(216352) - The module does not display a proper error message if an unsupported value is provided for the ipv6_prefix_length and vlan_id parameters.
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.idrac_boot - Configure the boot order settings.
- dellemc.openmanage.ome_devices - Perform device-specific operations on target devices

v6.0.0
======

Release Summary
---------------

Added collection metadata for creating execution environments, deprecation of share parameters, and support for configuring iDRAC attributes using idrac_attributes module.

Major Changes
-------------

- Added collection metadata for creating execution environments.
- Refactored the Markdown (MD) files and content for better readability.
- The share parameters are deprecated from the following modules - idrac_network, idrac_timezone_ntp, dellemc_configure_idrac_eventing, dellemc_configure_idrac_services, dellemc_idrac_lc_attributes, dellemc_system_lockdown_mode.

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_local_access_configuration - Issue(215035) - The module reports ``Successfully updated the local access setting`` if an unsupported value is provided for the parameter timeout_limit. However, this value is not actually applied on OpenManage Enterprise Modular.
- ome_device_local_access_configuration - Issue(217865) - The module does not display a proper error message if an unsupported value is provided for the user_defined and lcd_language parameters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_device_quick_deploy - Issue(216352) - The module does not display a proper error message if an unsupported value is provided for the ipv6_prefix_length and vlan_id parameters.
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.idrac_attributes - Configure the iDRAC attributes

v5.5.0
======

Release Summary
---------------

Support to generate certificate signing request, import, and export certificates on iDRAC.

Minor Changes
-------------

- idrac_redfish_storage_controller - This module is updated to use the Job Service URL instead of Task Service URL for job tracking.
- idrac_server_config_profile - This module is updated to use the Job Service URL instead of Task Service URL for job tracking.
- redfish_firmware - This module is updated to use the Job Service URL instead of Task Service URL for job tracking.

Bugfixes
--------

- idrac_server_config_profile - Issue(234817) – When an XML format is exported using the SCP, the module breaks while waiting for the job completion.
- ome_application_console_preferences - Issue(224690) - The module does not display a proper error message when an unsupported value is provided for the parameters report_row_limit, email_sender_settings, and metric_collection_settings, and the value is applied on OpenManage Enterprise

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_local_access_configuration - Issue(215035) - The module reports ``Successfully updated the local access setting`` if an unsupported value is provided for the parameter timeout_limit. However, this value is not actually applied on OpenManage Enterprise Modular.
- ome_device_local_access_configuration - Issue(217865) - The module does not display a proper error message if an unsupported value is provided for the user_defined and lcd_language parameters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_device_quick_deploy - Issue(216352) - The module does not display a proper error message if an unsupported value is provided for the ipv6_prefix_length and vlan_id parameters.
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.idrac_certificates - Configure certificates for iDRAC.

v5.4.0
======

Release Summary
---------------

Support for export, import, and preview the Server Configuration Profile (SCP) configuration using Redfish and added support for check mode.

Major Changes
-------------

- idrac_server_config_profile - The module is enhanced to support export, import, and preview the SCP configuration using Redfish and added support for check mode.

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_console_preferences - Issue(224690) - The module does not display a proper error message when an unsupported value is provided for the parameters report_row_limit, email_sender_settings, and metric_collection_settings, and the value is applied on OpenManage Enterprise.
- ome_device_local_access_configuration - Issue(215035) - The module reports ``Successfully updated the local access setting`` if an unsupported value is provided for the parameter timeout_limit. However, this value is not actually applied on OpenManage Enterprise Modular.
- ome_device_local_access_configuration - Issue(217865) - The module does not display a proper error message if an unsupported value is provided for the user_defined and lcd_language parameters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_device_quick_deploy - Issue(216352) - The module does not display a proper error message if an unsupported value is provided for the ipv6_prefix_length and vlan_id parameters.
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

v5.3.0
======

Release Summary
---------------

Added check mode and idempotency support for redfish_storage_volume and idempotency support for ome_smart_fabric_uplink. For ome_diagnostics, added support for debug logs and added supportassist_collection as a choice for the log_type argument to export SupportAssist logs.

Minor Changes
-------------

- ome_diagnostics - Added "supportassist_collection" as a choice for the log_type argument to export SupportAssist logs. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/309)
- ome_diagnostics - The module is enhanced to support debug logs. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/308)
- ome_smart_fabric_uplink - The module is enhanced to support idempotency. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/253)
- redfish_storage_volume - The module is enhanced to support check mode and idempotency. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/245)

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_console_preferences - Issue(224690) - The module does not display a proper error message when an unsupported value is provided for the parameters report_row_limit, email_sender_settings, and metric_collection_settings, and the value is applied on OpenManage Enterprise.
- ome_device_local_access_configuration - Issue(215035) - The module reports ``Successfully updated the local access setting`` if an unsupported value is provided for the parameter timeout_limit. However, this value is not actually applied on OpenManage Enterprise Modular.
- ome_device_local_access_configuration - Issue(217865) - The module does not display a proper error message if an unsupported value is provided for the user_defined and lcd_language parameters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_device_quick_deploy - Issue(216352) - The module does not display a proper error message if an unsupported value is provided for the ipv6_prefix_length and vlan_id parameters.
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

v5.2.0
======

Release Summary
---------------

Support to configure console preferences on OpenManage Enterprise.

Minor Changes
-------------

- idrac_redfish_storage_controller - This module is enhanced to support the following settings with check mode and idempotency - UnassignSpare, EnableControllerEncryption, BlinkTarget, UnBlinkTarget,  ConvertToRAID, ConvertToNonRAID, ChangePDStateToOnline, ChangePDStateToOffline.
- ome_diagnostics - The module is enhanced to support check mode and idempotency. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/345)
- ome_diagnostics - This module is enhanced to extract log from lead chassis. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/310)
- ome_profile - The module is enhanced to support check mode and idempotency.
- ome_profile - The module is enhanced to support modifying a profile based on the attribute names instead of the ID.
- ome_template - The module is enhanced to support check mode and idempotency. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/255)
- ome_template - The module is enhanced to support modifying a template based on the attribute names instead of the ID. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/358)

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_console_preferences - Issue(224690) - The module does not display a proper error message when an unsupported value is provided for the parameters report_row_limit, email_sender_settings, and metric_collection_settings, and the value is applied on OpenManage Enterprise.
- ome_device_local_access_configuration - Issue(215035) - The module reports ``Successfully updated the local access setting`` if an unsupported value is provided for the parameter timeout_limit. However, this value is not actually applied on OpenManage Enterprise Modular.
- ome_device_local_access_configuration - Issue(217865) - The module does not display a proper error message if an unsupported value is provided for the user_defined and lcd_language parameters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module displays the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_device_quick_deploy - Issue(216352) - The module does not display a proper error message if an unsupported value is provided for the ipv6_prefix_length and vlan_id parameters.
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_application_console_preferences - Configures console preferences on OpenManage Enterprise.

v5.1.0
======

Release Summary
---------------

Support for OpenManage Enterprise Modular server interface management.

Minor Changes
-------------

- ome_application_network_address - The module is enhanced to support check mode and idempotency.
- ome_device_info - The module is enhanced to return a blank list when devices or baselines are not present in the system.
- ome_firmware_baseline_compliance_info - The module is enhanced to return a blank list when devices or baselines are not present in the system.
- ome_firmware_baseline_info - The module is enhanced to return a blank list when devices or baselines are not present in the system.
- ome_identity_pool - The iSCSI Initiator and Initiator IP Pool attributes are not mandatory to create an identity pool. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/329)
- ome_identity_pool - The module is enhanced to support check mode and idempotency. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/328)
- ome_template_identity_pool - The module is enhanced to support check mode and idempotency.
- redfish_event_subscription - The module is enhanced to support check mode and idempotency.

Bugfixes
--------

- idrac_firmware - Issue (220130) The socket.timout issue that occurs during the wait_for_job_completion() job is fixed.

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_local_access_configuration - Issue(215035) - The module reports ``Successfully updated the local access setting`` if an unsupported value is provided for the parameter timeout_limit. However, this value is not actually applied on OpenManage Enterprise Modular.
- ome_device_local_access_configuration - Issue(217865) - The module does not display a proper error message if an unsupported value is provided for the user_defined and lcd_language parameters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module errors out with the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_server_interface_profile_info - Retrieves the information of server interface profile on OpenManage Enterprise Modular.
- dellemc.openmanage.ome_server_interface_profiles - Configures server interface profiles on OpenManage Enterprise Modular.

v5.0.1
======

Release Summary
---------------

Support to provide custom or organizational CA signed certificate for SSL validation from the environment variable.

Major Changes
-------------

- All modules can read custom or organizational CA signed certificate from the environment variables. Please refer to `SSL Certificate Validation <https://github.com/dell/dellemc-openmanage-ansible-modules#ssl-certificate-validation>`_ section in the `README.md <https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/README.md#SSL-Certificate-Validation>`_ for modification to existing playbooks or setting environment variable.

Bugfixes
--------

- All playbooks require modification because the validate_certs argument is set to True by default (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/357)
- The ome_application_network_time and ome_application_network_proxy modules are breaking due to the changes introduced for SSL validation.(https://github.com/dell/dellemc-openmanage-ansible-modules/issues/360)

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_local_access_configuration - Issue(215035) - The module reports ``Successfully updated the local access setting`` if an unsupported value is provided for the parameter timeout_limit. However, this value is not actually applied on OpenManage Enterprise Modular.
- ome_device_local_access_configuration - Issue(217865) - The module does not display a proper error message if an unsupported value is provided for the user_defined and lcd_language parameters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module errors out with the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not  exist or is not applicable for the resource URI.``
- ome_device_quick_deploy - Issue(216352) - The module does not display a proper error message if an unsupported value is provided for the ipv6_prefix_length and vlan_id parameters.
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

v5.0.0
======

Release Summary
---------------

HTTPS SSL support for all modules and quick deploy settings.

Major Changes
-------------

- All modules now support SSL over HTTPS and socket level timeout.

Breaking Changes / Porting Guide
--------------------------------

- HTTPS SSL certificate validation is a **breaking change** and will require modification in the existing playbooks. Please refer to `SSL Certificate Validation <https://github.com/dell/dellemc-openmanage-ansible-modules#ssl-certificate-validation>`_ section in the `README.md <https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/README.md#SSL-Certificate-Validation>`_ for modification to existing playbooks.

Bugfixes
--------

- idrac_bios - The issue while configuring boot sources is fixed (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/347)

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_local_access_configuration - Issue(215035) - The module reports ``Successfully updated the local access setting`` if an unsupported value is provided for the parameter timeout_limit. However, this value is not actually applied on OpenManage Enterprise Modular.
- ome_device_local_access_configuration - Issue(217865) - The module does not display a proper error message if an unsupported value is provided for the user_defined and lcd_language parameters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module errors out with the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not  exist or is not applicable for the resource URI.``
- ome_device_quick_deploy - Issue(216352) - The module does not display a proper error message if an unsupported value is provided for the ipv6_prefix_length and vlan_id parameters.
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_device_quick_deploy - Configure Quick Deploy settings on OpenManage Enterprise Modular

v4.4.0
======

Release Summary
---------------

Support to configure login security, session inactivity timeout, and local access settings.

Minor Changes
-------------

- ome_firmware - The module is enhanced to support check mode and idempotency (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/274)
- ome_template - An example task is added to create a compliance template from reference device (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/339)

Bugfixes
--------

- ome_device_location - The issue that applies values of the location settings only in lowercase is fixed (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/341)

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_local_access_configuration - Issue(215035) - The module reports ``Successfully updated the local access setting`` if an unsupported value is provided for the parameter timeout_limit. However, this value is not actually applied on OpenManage Enterprise Modular.
- ome_device_local_access_configuration - Issue(217865) - The module does not display a proper error message if an unsupported value is provided for the user_defined and lcd_language parameters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module errors out with the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not  exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_application_network_settings - This module allows you to configure the session inactivity timeout settings
- dellemc.openmanage.ome_application_security_settings - Configure the login security properties
- dellemc.openmanage.ome_device_local_access_configuration - Configure local access settings on OpenManage Enterprise Modular

v4.3.0
======

Release Summary
---------------

Support to configure network services, syslog forwarding, and SMTP settings.

Known Issues
------------

- idrac_user - Issue(192043) The module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_application_alerts_smtp - Issue(212310) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_application_alerts_syslog - Issue(215374) - The module does not provide a proper error message if the destination_address is more than 255 characters.
- ome_device_network_services - Issue(212681) - The module does not provide a proper error message if unsupported values are provided for the parameters- port_number, community_name, max_sessions, max_auth_retries, and idle_timeout.
- ome_device_power_settings - Issue(212679) - The module errors out with the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not  exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) - The module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_application_alerts_smtp - This module allows to configure SMTP or email configurations
- dellemc.openmanage.ome_application_alerts_syslog - Configure syslog forwarding settings on OpenManage Enterprise and OpenManage Enterprise Modular
- dellemc.openmanage.ome_device_network_services - Configure chassis network services settings on OpenManage Enterprise Modular

v4.2.0
======

Release Summary
---------------

Support to configure OME Modular devices network, power, and location settings.

Known Issues
------------

- idrac_user - Issue(192043) Module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_device_power_settings - Issue(212679) The ome_device_power_settings module errors out with the following message if the value provided for the parameter ``power_cap`` is not within the supported range of 0 to 32767, ``Unable to complete the request because PowerCap does not  exist or is not applicable for the resource URI.``
- ome_smart_fabric_uplink - Issue(186024) ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_device_location - Configure device location settings on OpenManage Enterprise Modular
- dellemc.openmanage.ome_device_mgmt_network - Configure network settings of devices on OpenManage Enterprise Modular
- dellemc.openmanage.ome_device_power_settings - Configure chassis power settings on OpenManage Enterprise Modular

v4.1.0
======

Release Summary
---------------

Support for Redfish event subscriptions and enhancements to ome_firmware module.

Major Changes
-------------

- ome_firmware - Added option to stage the firmware update and support for selecting components and devices for baseline-based firmware update.

Minor Changes
-------------

- ome_template_network_vlan - Enabled check_mode support.

Known Issues
------------

- idrac_user - Issue(192043) Module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_smart_fabric_uplink - Issue(186024) ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though it is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.redfish_event_subscription - Manage Redfish Subscriptions

v4.0.0
======

Release Summary
---------------

Support for configuring active directory user group on OpenManage Enterprise and OpenManage Enterprise Modular.

Known Issues
------------

- idrac_user - Issue(192043) Module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_smart_fabric_uplink - Issue(186024) ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though this is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_active_directory - Configure Active Directory groups to be used with Directory Services on OpenManage Enterprise and OpenManage Enterprise Modular
- dellemc.openmanage.ome_domain_user_groups - Create, modify, or delete an Active Directory user group on OpenManage Enterprise and OpenManage Enterprise Modular

v3.6.0
======

Release Summary
---------------

Support for configuring device slot name and export SupportAssist device collections from OpenManage Enterprise and OpenManage Enterprise Modular.

Bugfixes
--------

- dellemc_idrac_storage_volume - Module fails if the BlockSize, FreeSize, or Size state of the physical disk is set to "Not Available".

Known Issues
------------

- idrac_user - Issue(192043) Module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_smart_fabric_uplink - Issue(186024) ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though this is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_chassis_slots - Rename sled slots on OpenManage Enterprise Modular
- dellemc.openmanage.ome_diagnostics - Export technical support logs(TSR) to network share location

v3.5.0
======

Release Summary
---------------

Support for managing static device groups on OpenManage Enterprise.

Major Changes
-------------

- idrac_server_config_profile - Added support for exporting and importing Server Configuration Profile through HTTP/HTTPS share.
- ome_device_group - Added support for adding devices to a group using the IP addresses of the devices and group ID.

Bugfixes
--------

- Handled invalid share and unused imports cleanup for iDRAC modules (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/268)

Known Issues
------------

- idrac_user - Issue(192043) Module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_smart_fabric_uplink - Issue(186024) ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though this is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_groups - Manages static device groups on OpenManage Enterprise

v3.4.0
======

Release Summary
---------------

OpenManage Enterprise firmware baseline and firmware catalog modules updated to support checkmode.

Major Changes
-------------

- ome_firmware_baseline - Module supports check mode, and allows the modification and deletion of firmware baselines.
- ome_firmware_catalog - Module supports check mode, and allows the modification and deletion of firmware catalogs.

Minor Changes
-------------

- ome_firmware_catalog - Added support for repositories available on the Dell support site.
- ome_template_network_vlan - Added the input option which allows to apply the modified VLAN settings immediately on the associated modular-system servers.

Known Issues
------------

- idrac_user - Issue(192043) Module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_smart_fabric_uplink - Issue(186024) ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though this is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

v3.3.0
======

Release Summary
---------------

OpenManage Enterprise device group and device discovery support added

Minor Changes
-------------

- ome_firmware_baseline - Allows to retrieve the device even if it not in the first 50 device IDs

Known Issues
------------

- idrac_user - Issue(192043) Module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_configuration_compliance_info - Issue(195592) Module may error out with the message ``unable to process the request because an error occurred``. If the issue persists, report it to the system administrator.
- ome_smart_fabric - Issue(185322) Only three design types are supported by OpenManage Enterprise Modular but the module successfully creates a fabric when the design type is not supported.
- ome_smart_fabric_uplink - Issue(186024) ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though this is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_device_group - Add devices to a static device group on OpenManage Enterprise
- dellemc.openmanage.ome_discovery - Create, modify, or delete a discovery job on OpenManage Enterprise

v3.2.0
======

Release Summary
---------------

Configuration compliance related modules added

Minor Changes
-------------

- ome_template - Allows to deploy a template on device groups.

Known Issues
------------

- idrac_user - Issue(192043) Module may error out with the message ``unable to perform the import or export operation because there are pending attribute changes or a configuration job is in progress``. Wait for the job to complete and run the task again.
- ome_configuration_compliance_info - Issue(195592) Module may error out with the message ``unable to process the request because an error occurred``. If the issue persists, report it to the system administrator.
- ome_smart_fabric - Issue(185322) Only three design types are supported by OpenManage Enterprise Modular but the module successfully creates a fabric when the design type is not supported.
- ome_smart_fabric_uplink - Issue(186024) ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though this is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_configuration_compliance_baseline - Create, modify, and delete a configuration compliance baseline and remediate non-compliant devices on OpenManage Enterprise
- dellemc.openmanage.ome_configuration_compliance_info - Device compliance report for devices managed in OpenManage Enterprise

v3.1.0
======

Release Summary
---------------

OpenManage Enterprise profiles management support added.

Bugfixes
--------

- ome_firmware_baseline_compliance_info - OMEnt firmware baseline compliance info pagination support added (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/171)
- ome_network_proxy - OMEnt network proxy check mode support added (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/187)

Known Issues
------------

- ome_smart_fabric - Issue(185322) Only three design types are supported by OpenManage Enterprise Modular but the module successfully creates a fabric when the design type is not supported.
- ome_smart_fabric_uplink - Issue(186024) ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though this is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_profile - Create, modify, delete, assign, unassign and migrate a profile on OpenManage Enterprise

v3.0.0
======

Release Summary
---------------

Deprecations, issue fixes, and standardization of modules as per ansible guidelines.

Major Changes
-------------

- Removed the existing deprecated modules.

Minor Changes
-------------

- Coding Guidelines, Contributor Agreement, and Code of Conduct files are added to the collection.
- New deprecation changes for ``dellemc_get_system_inventory`` and ``dellemc_get_firmware_inventory`` ignored for ansible 2.9 sanity test.
- The modules are standardized as per ansible guidelines.

Deprecated Features
-------------------

- The ``dellemc_get_firmware_inventory`` module is deprecated and replaced with ``idrac_firmware_info``.
- The ``dellemc_get_system_inventory`` module is deprecated and replaced with ``idrac_system_info``.

Bugfixes
--------

- GitHub issue fix - Module dellemc_idrac_storage_volume.py broken. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/212)
- GitHub issue fix - ome_smart_fabric Fabric management is not supported on the specified system. (https://github.com/dell/dellemc-openmanage-ansible-modules/issues/179)
- Known issue fix #187956: If an invalid job_id is provided, the idrac_lifecycle_controller_job_status_info module returns an error message with the description of the issue.
- Known issue fix #188267: No error message is displayed when the target iDRAC with firmware version less than 3.30.30.30 is updated.
- Sanity fixes as per ansible guidelines to all modules.

Known Issues
------------

- Issue 1(186024): ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though this is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

v2.1.5
======

Release Summary
---------------

The idrac_firmware module is enhanced to include checkmode support and job tracking.

Minor Changes
-------------

- The idrac_server_config_profile module supports IPv6 address format.

Bugfixes
--------

- Identity pool does not reset when a network VLAN is added to a template in the ome_template_network_vlan module. `#169 <https://github.com/dell/dellemc-openmanage-ansible-modules/issues /169>`_
- Missing parameter added in ome_smart_fabric_uplink module documenation. `#181 <https://github.com/dell/dellemc-openmanage-ansible-modules/issues/181>`_

Known Issues
------------

- Issue 1(186024): ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though this is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.
- Issue 2(187956): If an invalid job_id is provided, idrac_lifecycle_controller_job_status_info returns an error message. This error message does not contain information about the exact issue with the invalid job_id.
- Issue 3(188267): While updating the iDRAC firmware, the idrac_firmware module completes execution before the firmware update job is completed. An incorrect message is displayed in the task output as 'DRAC WSMAN endpoint returned HTTP code '400' Reason 'Bad Request''. This issue may occur if the target iDRAC firmware version is less than 3.30.30.30

v2.1.4
======

Release Summary
---------------

Fabric management related modules ome_smart_fabric and ome_smart_fabric_uplink are added.

Known Issues
------------

- Issue 1(186024): ome_smart_fabric_uplink module does not allow the creation of multiple uplinks of the same name even though this is supported by OpenManage Enterprise Modular. If an uplink is created using the same name as an existing uplink, the existing uplink is modified.

New Modules
-----------

- dellemc.openmanage.ome_smart_fabric - Create, modify or delete a fabric on OpenManage Enterprise Modular
- dellemc.openmanage.ome_smart_fabric_uplink - Create, modify or delete a uplink for a fabric on OpenManage Enterprise Modular

v2.1.3
======

Release Summary
---------------

Network configuration service related modules ome_network_vlan, ome_network_port_breakout and ome_network_vlan_info are added.

New Modules
-----------

- dellemc.openmanage.ome_network_port_breakout - This module allows to automate the port portioning or port breakout to logical sub ports
- dellemc.openmanage.ome_network_vlan - Create, modify & delete a VLAN
- dellemc.openmanage.ome_network_vlan_info - Retrieves the information about networks VLAN(s) present in OpenManage Enterprise

v2.1.2
======

Release Summary
---------------

The dellemc_change_power_state and dellemc_configure_idrac_users modules are standardized as per ansible guidelines. 8 GitHub issues are fixed.

Minor Changes
-------------

- The idrac_server_config_profile module supports a user provided file name for an export operation.

Deprecated Features
-------------------

- The dellemc_change_power_state module is deprecated and replaced with the redfish_powerstate module.
- The dellemc_configure_idrac_users module is deprecated and replaced with the idrac_user module.

Bugfixes
--------

- Documentation improvement request `#140 <https://github.com/dell/dellemc-openmanage-ansible-modules/issues/140>`_
- Executing dellemc_configure_idrac_users twice fails the second attempt `#100 <https://github.com/dell/dellemc-openmanage-ansible-modules/issues/100>`_
- dellemc_change_power_state fails if host is already on `#132 <https://github.com/dell/dellemc-openmanage-ansible-modules/issues/132>`_
- dellemc_change_power_state not idempotent `#115 <https://github.com/dell/dellemc-openmanage-ansible-modules/issues/115>`_
- dellemc_configure_idrac_users error `#26 <https://github.com/dell/dellemc-openmanage-ansible-modules/issues/26>`_
- dellemc_configure_idrac_users is unreliable - errors `#113 <https://github.com/dell/dellemc-openmanage-ansible-modules/issues/113>`_
- idrac_server_config_profile improvement requested (request) `#137 <https://github.com/dell/dellemc-openmanage-ansible-modules/issues/137>`_
- ome_firmware_catalog.yml example errors `#145 <https://github.com/dell/dellemc-openmanage-ansible-modules/issues/145>`_

New Modules
-----------

- dellemc.openmanage.idrac_user - Configure settings for user accounts
- dellemc.openmanage.redfish_powerstate - Manage device power state

v2.1.1
======

Release Summary
---------------

Support for OpenManage Enterprise Modular and other enhancements.

Major Changes
-------------

- Standardization of ten iDRAC ansible modules based on ansible guidelines.
- Support for OpenManage Enterprise Modular.

Deprecated Features
-------------------

- The dellemc_configure_bios module is deprecated and replaced with the idrac_bios module.
- The dellemc_configure_idrac_network module is deprecated and replaced with the idrac_network module.
- The dellemc_configure_idrac_timezone module is deprecated and replaced with the idrac_timezone_ntp module.
- The dellemc_delete_lc_job and dellemc_delete_lc_job_queue modules are deprecated and replaced with the idrac_lifecycle_controller_jobs module.
- The dellemc_export_lc_logs module is deprecated and replaced with the idrac_lifecycle_controller_logs module.
- The dellemc_get_lc_job_status module is deprecated and replaced with the idrac_lifecycle_controller_job_status_info module.
- The dellemc_get_lcstatus module is deprecated and replaced with the idrac_lifecycle_controller_status_info module.
- The dellemc_idrac_reset module is deprecated and replaced with the idrac_reset module.
- The dellemc_setup_idrac_syslog module is deprecated and replaced  with the idrac_syslog module.

New Modules
-----------

- dellemc.openmanage.idrac_bios - Configure the BIOS attributes
- dellemc.openmanage.idrac_lifecycle_controller_job_status_info - Get the status of a Lifecycle Controller job
- dellemc.openmanage.idrac_lifecycle_controller_jobs - Delete the Lifecycle Controller Jobs
- dellemc.openmanage.idrac_lifecycle_controller_logs - Export Lifecycle Controller logs to a network share or local path.
- dellemc.openmanage.idrac_lifecycle_controller_status_info - Get the status of the Lifecycle Controller
- dellemc.openmanage.idrac_network - Configures the iDRAC network attributes
- dellemc.openmanage.idrac_reset - Reset iDRAC
- dellemc.openmanage.idrac_syslog - Enable or disable the syslog on iDRAC
- dellemc.openmanage.idrac_timezone_ntp - Configures time zone and NTP on iDRAC

v2.1.0
======

Release Summary
---------------

The `Dell EMC OpenManage Ansible Modules <https://github.com/dell/dellemc-openmanage-ansible-modules>`_ are available on Ansible Galaxy as a collection.
