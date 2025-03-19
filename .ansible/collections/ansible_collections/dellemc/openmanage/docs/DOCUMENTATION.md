<!--
Copyright (c) 2022 Dell Inc., or its subsidiaries. All Rights Reserved.

Licensed under the GPL, Version 3.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.gnu.org/licenses/gpl-3.0.txt
-->
## Playbooks and Tutorials
* For the latest sample playbooks and example for idrac, see [idrac playbooks](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections/playbooks/idrac).
* For the latest sample playbooks and examples for redfish, see [redfish playbooks](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections/playbooks/redfish).
* For the latest sample playbooks and examples for ome, see [ome playbooks](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections/playbooks/ome).
* For the latest sample playbooks and examples for roles, see [roles playbooks](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections/playbooks/roles).
* For the tutorials and sample use cases, see the tutorials available at [developer.dell.com](https://developer.dell.com/).

## Module documentations
- For the OpenManage Ansible collection documentation, see [Documentation](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections/docs). This documentation page is updated for every major and minor (patch release) and has the latest collection documentation.
- OpenManage Ansible collection is an Ansible certified collection and also available as part of the Ansible Community Releases version v3.0.0 and later. Consequently, the documentation can also be accessed at [Ansible Collection Documentation](https://docs.ansible.com/ansible/latest/collections/dellemc/openmanage/index.html#plugins-in-dellemc-openmanage).
> **_NOTE_**: There might be a scenario where the documentation available at [Ansible Collection Documentation](https://docs.ansible.com/ansible/latest/collections/dellemc/openmanage/index.html#plugins-in-dellemc-openmanage) is not the latest version. And, this is due to differences in the release timelines for Ansible community release and OpenManage Ansible collection. 
- To view the documentation for a module, use the command ```ansible-doc```. For example,
    ```$ ansible-doc dellemc.openmanage.<module-name>```

## SSL Certificate Validation
**By default, SSL certificate validation is enabled in all modules to enforce secure communication.**

### Enable SSL certificate validation
  - Generate and upload the custom or organizational CA signed certificates on the iDRACs, OpenManage Enterprise, and OpenManage Enterprise-Modular, as required. 
    - For iDRAC, see the section `SSL server certificates` in the `Integrated Dell Remote Access Controller Users Guide`. 
    - For OpenManage Enterprise, see the section `Security Certificates` in the `OpenManage Enterprise Users Guide`. 
    - For OpenManage Enterprise Modular, see the section `Managing certificates` in the `OpenManage Enterprise Modular for PowerEdge MX7000 Chassis Users Guide`. 
  - After you have uploaded the custom or organizational CA signed certificate to iDRAC or OME or OME-M, you must have the CA file or bundle available on your Ansible controller. For example, copy the CA file or bundle in the following path: /usr/share/ssl-certs/
   > **_NOTE_**: Ensure that the user running the Ansible modules has permission to access the certificate file or bundle. 
   - You can then use either of the following methods to specify the custom or organization CA certificate file or bundle path to the module:
     - In your playbook tasks, set the `ca_path` argument to the file path of your custom or organization CA certificate file or bundle.
   ```ca_path: /usr/share/ssl-certs/ca-cert.pem```
     - Use any of the following environment variables to specify the custom or organization CA certificate file or bundle path. The modules reads the environment variable in the following order of preference: ```REQUESTS_CA_BUNDLE```, ```CURL_CA_BUNDLE```, ```OMAM_CA_BUNDLE```. 
   > **_NOTE_**: Use the following command to set the environment variable with the custom or organization CA certificate file or bundle:
       ```export REQUESTS_CA_BUNDLE=/usr/share/ssl-certs/ca-cert.pem```

### Ignore SSL certificate validation
It is common to run a test environment without a proper SSL certificate configuration. To disable the certificate validation for a module, set the validate_certs module argument to ```false``` in the playbook.

