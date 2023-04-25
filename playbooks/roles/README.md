# Roles Playbooks

### Using the Example playbooks

1. Update the inventory
Update the idrac IP's, hostnames in the `inventory` file.

1. Update the varaibles required for a role under `vars_files` folder.

1. Run the following command to run the role
`ansible-playbook <role_folder>/<role_file>.yml -i inventory

### Folder Tree

```
.
├── idrac_certificate
│   └── idrac_certificate.yml
├── idrac_export_server_config_profile
│   └── idrac_export_server_config_profile.yml
├── idrac_firmware
│   └── idrac_firmware.yml
├── idrac_gather_facts
│   └── idrac_gather_facts.yml
├── idrac_import_server_config_profile
│   └── idrac_import_server_config_profile.yml
├── idrac_os_deployment
│   └── idrac_os_deployment.yml
├── idrac_server_powerstate
│   └── idrac_server_powerstate.yml
├── inventory
├── README.md
├── redfish_firmware
│   └── redfish_firmware.yml
├── redfish_storage_volume
│   └── redfish_storage_volume.yml
└── vars_files
    ├── certificates.yml
    ├── credentials.yml
    ├── export.yml
    ├── firmware.yml
    ├── import.yml
    ├── osd.yml
    └── storage.yml
```
