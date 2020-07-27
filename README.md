# Dell EMC OpenManage Ansible Modules

Dell EMC OpenManage Ansible Modules allows data center and IT administrators to use RedHat Ansible to automate and orchestrate the configuration, deployment, and update of Dell EMC PowerEdge Servers and modular infrastructure by leveraging the management automation capabilities in-built into the Integrated Dell Remote Access Controller (iDRAC) and OpenManage Enterprise.

OpenManage Ansible Modules simplifies and automates provisioning, deployment, and updates of PowerEdge servers and modular infrastructure. It allows system administrators and software developers to introduce the physical infrastructure provisioning into their software provisioning stack, integrate with existing DevOps pipelines and manage their infrastructure using version-controlled playbooks, server configuration profiles, and templates in line with the Infrastructure-as-Code (IaC) principles.

## Supported Platforms
  * iDRAC 7 and 8 based Dell EMC PowerEdge Servers with Firmware versions 2.60.60.60 and above.
  * iDRAC 9 based Dell EMC PowerEdge Servers with Firmware versions 3.34.34.34 and above.
  * Dell EMC OpenManage Enterprise versions 3.2.1 and above.

## Prerequisites
  * [Ansible = 2.9.10](https://github.com/ansible/ansible)
  * Python >=2.7.17 and >=3.6.5
  * To run the iDRAC modules, install OpenManage Python Software Development
   Kit (OMSDK) using ``` pip install omsdk --upgrade``` or from 
   [Dell EMC OpenManage Python SDK](https://github.com/dell/omsdk)

## Installation
Install the latest dellemc openmanage collection from this branch:
```
ansible-galaxy collection install git+https://github.com/dell/dellemc-openmanage-ansible-modules.git,collections
```


## Documentation
See the OpenManage Ansible Modules User Guide [gitpages](https://dell.github.io/dellemc-openmanage-ansible-modules).

## Playbooks
Sample playbooks and examples are available at [playbooks](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections/playbooks).

## LICENSE
This project is licensed under GPL-3.0 License. See the [COPYING](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/COPYING.md) for more information.

## Contributing
We welcome your contributions to OpenManage Ansible Modules. See [Coding Guidelines](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/devel/CODING_GUIDELINES.md) for more details.

## Testing
See [here](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections/tests/README.md) for further information on testing.

## Support
  * To report any issue, create an issue [here](https://github.com/dell/dellemc-openmanage-ansible-modules/issues).
  * If any requirements have not been addressed, then create an issue [here](https://github.com/dell/dellemc-openmanage-ansible-modules/issues).
  * To provide feedback to the development team, send an email to **OpenManageAnsible@Dell.com**.

## Authors
  * OpenManageAnsible (OpenManageAnsible@dell.com)
