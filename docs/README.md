<!--
Copyright (c) 2023-2025 Dell Inc., or its subsidiaries. All Rights Reserved.

Licensed under the GPL, Version 3.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.gnu.org/licenses/gpl-3.0.txt
-->
# OpenManage Ansible Modules Documentation

### iDRAC Modules
| Module Name                                                                                          | iDRAC9 | iDRAC10 |
| ---------------------------------------------------------------------------------------------------- | ------ | ------  |
| [dellemc_configure_idrac_eventing](modules/dellemc_configure_idrac_eventing.rst)                     | ✓      | ✗      |
| [dellemc_configure_idrac_services](modules/dellemc_configure_idrac_services.rst)                     | ✓      | ✗      |
| [dellemc_idrac_lc_attributes](modules/dellemc_idrac_lc_attributes.rst)                               | ✓      | ✗      |
| [dellemc_idrac_storage_volume](modules/dellemc_idrac_storage_volume.rst)                             | ✓      | ✗      |
| [dellemc_system_lockdown_mode](modules/dellemc_system_lockdown_mode.rst)                             | ✓      | ✗      |
| [idrac_attributes](modules/idrac_attributes.rst)                                                     | ✓      | ✓      |
| [idrac_bios](modules/idrac_bios.rst)                                                                 | ✓      | ✓      |
| [idrac_boot](modules/idrac_boot.rst)                                                                 | ✓      | ✓      |
| [idrac_certificates](modules/idrac_certificates.rst)                                                 | ✓      | ✓      |
| [idrac_diagnostics](modules/idrac_diagnostics.rst)                                                   | ✓      | ✓      |
| [idrac_firmware](modules/idrac_firmware.rst)                                                         | ✓      | ✓      |
| [idrac_firmware_info](modules/idrac_firmware_info.rst)                                               | ✓      | ✓      |
| [idrac_license](modules/idrac_license.rst)                                                           | ✓      | ✗      |
| [idrac_lifecycle_controller_job_status_info](modules/idrac_lifecycle_controller_job_status_info.rst) | ✓      | ✓      |
| [idrac_lifecycle_controller_jobs](modules/idrac_lifecycle_controller_jobs.rst)                       | ✓      | ✓      |
| [idrac_lifecycle_controller_logs](modules/idrac_lifecycle_controller_logs.rst)                       | ✓      | ✓      |
| [idrac_lifecycle_controller_status_info](modules/idrac_lifecycle_controller_status_info.rst)         | ✓      | ✓      |
| [idrac_network](modules/idrac_network.rst)                                                           | ✓      | ✗      |
| [idrac_network_attributes](modules/idrac_network_attributes.rst)                                     | ✓      | ✓      |
| [idrac_os_deployment](modules/idrac_os_deployment.rst)                                               | ✓      | ✗      |
| [idrac_redfish_storage_controller](modules/idrac_redfish_storage_controller.rst)                     | ✓      | ✗      |
| [idrac_reset](modules/idrac_reset.rst)                                                               | ✓      | ✓      |
| [idrac_secure_boot](modules/idrac_secure_boot.rst)                                                   | ✓      | ✓      |
| [idrac_server_config_profile](modules/idrac_server_config_profile.rst)                               | ✓      | ✗      |
| [idrac_session](modules/idrac_session.rst)                                                           | ✓      | ✓      |
| [idrac_storage_volume](modules/idrac_storage_volume.rst)                                             | ✓      | ✗      |
| [idrac_support_assist](modules/idrac_support_assists.rst)                                            | ✓      | ✓      |
| [idrac_syslog](modules/idrac_syslog.rst)                                                             | ✓      | ✗      |
| [idrac_system_erase](modules/idrac_system_erase.rst)                                                 | ✓      | ✓      |  
| [idrac_system_info](modules/idrac_system_info.rst)                                                   | ✓      | ✓      |
| [idrac_timezone_ntp](modules/idrac_timezone_ntp.rst)                                                 | ✓      | ✗      |
| [idrac_user](modules/idrac_user.rst)                                                                 | ✓      | ✓      |
| [idrac_user_info](modules/idrac_user_info.rst)                                                       | ✓      | ✓      |
| [idrac_virtual_media](modules/idrac_virtual_media.rst)                                               | ✓      | ✓      |
| [redfish_event_subscription](modules/redfish_event_subscription.rst)                                 | ✓      | ✓      |
| [redfish_firmware](modules/redfish_firmware.rst)                                                     | ✓      | ✓      |
| [redfish_firmware_rollback](modules/redfish_firmware_rollback.rst)                                   | ✓      | ✗      |
| [redfish_powerstate](modules/redfish_powerstate.rst)                                                 | ✓      | ✓      |
| [redfish_storage_volume](modules/redfish_storage_volume.rst)                                         | ✓      | ✗      |

### iDRAC Roles
| Role Name                                                                                          | iDRAC9 | iDRAC10 |
| ---------------------------------------------------------------------------------------------------- | ------ | ------  |
| [idrac_attributes](../roles/idrac_attributes/README.md)                                                     | ✓      | ✓      |
| [idrac_bios](../roles/idrac_bios/README.md)                                                                 | ✓      | ✓     |
| [idrac_boot](../roles/idrac_boot/README.md)                                                                 | ✓      | ✓      |
| [idrac_certificate](../roles/idrac_certificate/README.md)                                                   | ✓      | ✗      |
| [idrac_export_server_config_profile](../roles/idrac_export_server_config_profile/README.md)                 | ✓      | ✗      |
| [idrac_firmware](../roles/idrac_firmware/README.md)                                                         | ✓      | ✗      |
| [idrac_gather_facts](../roles/idrac_gather_facts/README.md)                                                 | ✓      | ✓      |
| [idrac_import_server_config_profile](../roles/idrac_import_server_config_profile/README.md)                 | ✓      | ✗      |
| [idrac_job_queue](../roles/idrac_job_queue/README.md)                                                       | ✓      | ✓      | 
| [idrac_os_deployment](../roles/idrac_os_deployment/README.md)                                               | ✓      | ✗      |
| [idrac_reset](../roles/idrac_reset/README.md)                                                               | ✓      | ✓      |
| [idrac_server_powerstate](../roles/idrac_server_powerstate/README.md)                                       | ✓      | ✓      |
| [idrac_storage_controller](../roles/idrac_storage_controller/README.md)                                     | ✓      | ✗      |
| [idrac_user](../roles/idrac_user/README.md)                                                                 | ✓      | ✓      |
| [redfish_firmware](../roles/redfish_firmware/README.md)                                                     | ✓      | ✗      |
| [redfish_storage_volume](../roles/redfish_storage_volume/README.md)                                         | ✓      | ✗      |

### OpenManage Enterprise Modules

|  Module Name                                                                               |
| ------------------------------------------------------------------------------------------ |
| [ome_active_directory](modules/ome_active_directory.rst)                                   |
| [ome_alert_policies](modules/ome_alert_policies.rst)                                       |
| [ome_alert_policies_message_id_info](modules/ome_alert_policies_message_id_info.rst)       |
| [ome_alert_policies_info](modules/ome_alert_policies_info.rst)                             |
| [ome_alert_policies_actions_info](modules/ome_alert_policies_actions_info.rst)             |
| [ome_alert_policies_category_info](modules/ome_alert_policies_category_info.rst)           |
| [ome_application_alerts_smtp](modules/ome_application_alerts_smtp.rst)                     |
| [ome_application_alerts_syslog](modules/ome_application_alerts_syslog.rst)                 |
| [ome_application_certificate](modules/ome_application_certificate.rst)                     |
| [ome_application_console_preferences](modules/ome_application_console_preferences.rst)     |
| [ome_application_network_address](modules/ome_application_network_address.rst)             |
| [ome_application_network_proxy](modules/ome_application_network_proxy.rst)                 |
| [ome_application_network_settings](modules/ome_application_network_settings.rst)           |
| [ome_application_network_time](modules/ome_application_network_time.rst)                   |
| [ome_application_network_webserver](modules/ome_application_network_webserver.rst)         |
| [ome_application_security_settings](modules/ome_application_security_settings.rst)         |
| [ome_chassis_slots](modules/ome_chassis_slots.rst)                                         |
| [ome_configuration_compliance_baseline](modules/ome_configuration_compliance_baseline.rst) |
| [ome_configuration_compliance_info](modules/ome_configuration_compliance_info.rst)         |
| [ome_device_group](modules/ome_device_group.rst)                                           |
| [ome_device_info](modules/ome_device_info.rst)                                             |
| [ome_device_local_access_configuration](modules/ome_device_local_access_configuration.rst) |
| [ome_device_location](modules/ome_device_location.rst)                                     |
| [ome_device_mgmt_network](modules/ome_device_mgmt_network.rst)                             |
| [ome_device_network_services](modules/ome_device_network_services.rst)                     |
| [ome_device_power_settings](modules/ome_device_power_settings.rst)                         |
| [ome_device_quick_deploy](modules/ome_device_quick_deploy.rst)                             |
| [ome_devices](modules/ome_devices.rst)                                                     |
| [ome_diagnostics](modules/ome_diagnostics.rst)                                             |
| [ome_discovery](modules/ome_discovery.rst)                                                 |
| [ome_domain_user_groups](modules/ome_domain_user_groups.rst)                               |
| [ome_firmware](modules/ome_firmware.rst)                                                   |
| [ome_firmware_baseline](modules/ome_firmware_baseline.rst)                                 |
| [ome_firmware_baseline_compliance_info](modules/ome_firmware_baseline_compliance_info.rst) |
| [ome_firmware_baseline_info](modules/ome_firmware_baseline_info.rst)                       |
| [ome_firmware_catalog](modules/ome_firmware_catalog.rst)                                   |
| [ome_groups](modules/ome_groups.rst)                                                       |
| [ome_identity_pool](modules/ome_identity_pool.rst)                                         |
| [ome_job_info](modules/ome_job_info.rst)                                                   |
| [ome_network_port_breakout](modules/ome_network_port_breakout.rst)                         |
| [ome_network_vlan](modules/ome_network_vlan.rst)                                           |
| [ome_network_vlan_info](modules/ome_network_vlan_info.rst)                                 |
| [ome_powerstate](modules/ome_powerstate.rst)                                               |
| [ome_profile](modules/ome_profile.rst)                                                     |
| [ome_profile_info](modules/ome_profile_info.rst)                                           |
| [ome_server_interface_profile_info](modules/ome_server_interface_profile_info.rst)         |
| [ome_server_interface_profiles](modules/ome_server_interface_profiles.rst)                 |
| [ome_session](modules/ome_session.rst)                                                     |
| [ome_smart_fabric_info](modules/ome_smart_fabric_info.rst)                                 |
| [ome_smart_fabric](modules/ome_smart_fabric.rst)                                           |
| [ome_smart_fabric_uplink_info](modules/ome_smart_fabric_uplink_info.rst)                   |
| [ome_smart_fabric_uplink](modules/ome_smart_fabric_uplink.rst)                             |
| [ome_template](modules/ome_template.rst)                                                   |
| [ome_template_identity_pool](modules/ome_template_identity_pool.rst)                       |
| [ome_template_info](modules/ome_template_info.rst)                                         |
| [ome_template_network_vlan](modules/ome_template_network_vlan.rst)                         |
| [ome_template_network_vlan_info](modules/ome_template_network_vlan_info.rst)               |
| [ome_user](modules/ome_user.rst)                                                           |
| [ome_user_info](modules/ome_user_info.rst)                                                 |

### OpenManage Enterprise Integration for VMWare vCenter Plug-in Modules

|  Module Name                                                                                 |
| -------------------------------------------------------------------------------------------- |
| [omevv_baseline_profile](modules/omevv_baseline_profile.rst)                                 |
| [omevv_baseline_profile_info](modules/omevv_baseline_profile_info.rst)                       |
| [omevv_firmware](modules/omevv_firmware.rst)                                                 |
| [omevv_firmware_compliance_info](modules/omevv_firmware_compliance_info.rst)                 |
| [omevv_firmware_repository_profile](modules/omevv_firmware_repository_profile.rst)           |
| [omevv_firmware_repository_profile_info](modules/omevv_firmware_repository_profile_info.rst) |
| [omevv_vcenter_info](modules/omevv_vcenter_info.rst)                                         |