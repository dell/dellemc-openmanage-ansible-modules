# Dell EMC OpenManage Ansible Modules

Dell EMC OpenManage Ansible Modules allows data center and IT administrators to use RedHat Ansible to automate and orchestrate the configuration, deployment, and update of Dell EMC PowerEdge Servers and modular infrastructure by leveraging the management automation capabilities in-built into the Integrated Dell Remote Access Controller (iDRAC), OpenManage Enterprise (OME) and OpenManage Enterprise Modular (OMEM).

OpenManage Ansible Modules simplifies and automates provisioning, deployment, and updates of PowerEdge servers and modular infrastructure. It allows system administrators and software developers to introduce the physical infrastructure provisioning into their software provisioning stack, integrate with existing DevOps pipelines and manage their infrastructure using version-controlled playbooks, server configuration profiles, and templates in line with the Infrastructure-as-Code (IaC) principles.

## Supported Platforms
  * iDRAC 7 based Dell EMC PowerEdge Servers with firmware versions 2.63.60.62 and above.
  * iDRAC 8 based Dell EMC PowerEdge Servers with firmware versions 2.81.81.81 and above.
  * iDRAC 9 based Dell EMC PowerEdge Servers with firmware versions 5.10.00.00 and above.
  * Dell EMC OpenManage Enterprise versions 3.8.2 and above.
  * Dell EMC OpenManage Enterprise Modular versions 1.40.00 and above.

## Prerequisites
  * [Ansible >= 2.10.0](https://github.com/ansible/ansible)
  * Python >= 3.8.6
  * To run the iDRAC modules, install OpenManage Python Software Development Kit (OMSDK) 
  using either ```pip install omsdk --upgrade``` or ```pip install -r requirements.txt```. 
  OMSDK can also be installed from [Dell EMC OpenManage Python SDK](https://github.com/dell/omsdk)
  * Operating System
    * Red Hat Enterprise Linux (RHEL) 8.5 and 8.4
    * SUSE Linux Enterprise Server (SLES) 15 SP2 and 15 SP1
    * Ubuntu 20.04.2 and 20.04.1

## Installation

* From [galaxy](https://galaxy.ansible.com/dellemc/openmanage):  
```ansible-galaxy collection install dellemc.openmanage```

    - For offline installation on the Ansible control machine, download the required tar archive version of the collection from [Dell EMC OpenManage collection](https://galaxy.ansible.com/dellemc/openmanage) and run the command given below:  
      ```ansible-galaxy collection install dellemc-openmanage-<version>.tar.gz```

* From [github](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections):  
Install the collection from the github repository using the latest commit on the branch 'collections'  
```ansible-galaxy collection install git+https://github.com/dell/dellemc-openmanage-ansible-modules.git,collections```

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
It is common to run a test environment without a proper SSL certificate configuration. To disable the certificate validation for a module, set the validate_certs module argument to ```False``` in the playbook.

## Playbooks and Tutorials
* For the latest sample playbooks and examples, see [playbooks](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections/playbooks).
* For the tutorials and sample use cases, see the tutorials available at [developer.dell.com](https://developer.dell.com/).

## Documentation
- For the OpenManage Ansible collection documentation, see [Documentation](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections/docs). This documentation page is updated for every major and minor (patch release) and has the latest collection documentation.
- OpenManage Ansible collection is an Ansible certified collection and also available as part of the Ansible Community Releases version v3.0.0 and later. Consequently, the documentation can also be accessed at [Ansible Collection Documentation](https://docs.ansible.com/ansible/latest/collections/dellemc/openmanage/index.html#plugins-in-dellemc-openmanage).
> **_NOTE_**: There might be a scenario where the documentation available at [Ansible Collection Documentation](https://docs.ansible.com/ansible/latest/collections/dellemc/openmanage/index.html#plugins-in-dellemc-openmanage) is not the latest version. And, this is due to differences in the release timelines for Ansible community release and OpenManage Ansible collection. 
- To view the documentation for a module, use the command ```ansible-doc```. For example,
    ```$ ansible-doc dellemc.openmanage.<module-name>```  

## LICENSE
This project is licensed under GPL-3.0 License. See the [COPYING](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections/COPYING.md) for more information.

## Contributing
We welcome your contributions to OpenManage Ansible Modules. See [Coding Guidelines](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections/CODING_GUIDELINES.md) for more details.
You can refer our [Code of Conduct](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections/CODE_OF_CONDUCT.md) here.

## Testing
See [here](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections/tests/README.md) for further information on testing.

## Debugging
To debug OpenManage Ansible Modules using IDE, see [here](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections/.github/debug.md)

## Maintenance
  * OpenManage Ansible Modules releases follows a monthly release cycle. On the last week of every month, 
  the updated modules are posted to this repository.
  * OpenManage Ansible Modules releases follow [semantic versioning](https://semver.org/).
  * OpenManage Ansible Modules deprecation cycle is aligned with [Ansible](https://docs.ansible.com/ansible/latest/dev_guide/module_lifecycle.html).

## Support
  * This branch corresponds to the release actively under development.
  * To report any issue, create an issue [here](https://github.com/dell/dellemc-openmanage-ansible-modules/issues).
  * If any requirements have not been addressed, then create an issue [here](https://github.com/dell/dellemc-openmanage-ansible-modules/issues).
  * To provide feedback to the development team, send an email to **OpenManageAnsible@Dell.com**.

## Authors
  * OpenManageAnsible (OpenManageAnsible@dell.com)