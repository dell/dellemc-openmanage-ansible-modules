# Dell EMC OpenManage Ansible Modules

Dell EMC OpenManage Ansible Modules allows data center and IT administrators to use RedHat Ansible to automate and orchestrate the configuration, deployment, and update of Dell EMC PowerEdge Servers and modular infrastructure by leveraging the management automation capabilities in-built into the Integrated Dell Remote Access Controller (iDRAC) and OpenManage Enterprise.

OpenManage Ansible Modules simplifies and automates provisioning, deployment, and updates of PowerEdge servers and modular infrastructure. It allows system administrators and software developers to introduce the physical infrastructure provisioning into their software provisioning stack, integrate with existing DevOps pipelines and manage their infrastructure using version-controlled playbooks, server configuration profiles, and templates in line with the Infrastructure-as-Code (IaC) principles.

## Supported Platforms
  * iDRAC 7/8 based Dell EMC PowerEdge Servers with Firmware
   version 2.60.60.60 and above.
  * iDRAC 9 based Dell EMC PowerEdge Servers with Firmware version 3.34.34.34
   and above.
  * Dell EMC OpenManage Enterprise version 3.2.1 and above.

## Prerequisites
  * [Ansible](https://github.com/ansible/ansible)
  * Python >= 2.7.16
  * To run the iDRAC modules, install OpenManage Python Software Development
   Kit (OMSDK) using ``` pip install omsdk --upgrade``` or from 
   [Dell EMC OpenManage Python SDK](https://github.com/dell/omsdk)

## Documentation
Please refer to the [OpenManage Ansible Modules Documentation](./guides) or OpenManage Ansible Modules User Guide [gitpages](https://dell.github.io/dellemc-openmanage-ansible-modules/)

## Examples
Sample playbooks and examples could be found under [examples](./examples) directory

## Results
Sample Results for the respective modules could be found under [samples](./samples) directory.

## Installation

  * Clone the latest development repository and install the ansible modules.
  ```
  git clone -b devel --single-branch https://github.com/dell/dellemc-openmanage-ansible-modules.git
  cd dellemc-openmanage-ansible-modules
  python install.py
  ```

  * It is recommended to update the ansible configuration setting environment variables to point to the current module paths, if any.

  * If using an alternative python interpreter, i.e. virtualenv, you must set the Ansible variable ansible_python_interpreter to that path.

## Uninstallation

```
cd dellemc-openmanage-ansible-modules
python uninstall.py
```

## Ansible Galaxy Collections
The latest Dell EMC OpenManage Ansible Modules are available on Ansible
 Galaxy as a collection. Please see [dellemc.openmanage](https://galaxy.ansible.com/dellemc/openmanage)
 for more information. The collection branch is available [here.](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections)
 
## Build Docker image for OpenManage Ansible Modules
Refer following [how-to guide](./docker/README.md) for detailed instructions on how to create and run containerized version of OpenManage Ansible Modules.


## LICENSE
This project is licensed under GPL-3.0 License. Please see the [COPYING](
./COPYING.md) for more information


## Contributing
We welcome your contributions to OpenManage Ansible Modules. See [Coding Guidelines](./CODING_GUIDELINES.md) for more details.

## Testing
See [here](test/README.md) for further information on testing.

## Support
  * This devel branch corresponds to the release actively under development.
  * If you want to report any issue, then please report it by creating a new issue [here](https://github.com/dell/dellemc-openmanage-ansible-modules/issues)
  * If you have any requirements that is not currently addressed, then please let us know by creating a new issue [here](https://github.com/dell/dellemc-openmanage-ansible-modules/issues)
  * If you want to provide any feedback to the development team, then you can do so by sending an email to **OpenManageAnsible@Dell.com**

## Authors
  * OpenManageAnsible (OpenManageAnsible@dell.com)
