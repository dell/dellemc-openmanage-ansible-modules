# Dell EMC OpenManage Ansible Modules

Dell EMC OpenManage Ansible Modules allows data center and IT administrators to use RedHat Ansible to automate and orchestrate the configuration, deployment, and update of Dell EMC PowerEdge Servers and modular infrastructure by leveraging the management automation capabilities in-built into the Integrated Dell Remote Access Controller (iDRAC), OpenManage Enterprise and OpenManage Enterprise Modular.

OpenManage Ansible Modules simplifies and automates provisioning, deployment, and updates of PowerEdge servers and modular infrastructure. It allows system administrators and software developers to introduce the physical infrastructure provisioning into their software provisioning stack, integrate with existing DevOps pipelines and manage their infrastructure using version-controlled playbooks, server configuration profiles, and templates in line with the Infrastructure-as-Code (IaC) principles.

## Supported Platforms
  * iDRAC 7 and 8 based Dell EMC PowerEdge Servers with Firmware versions 2.60.60.60 and above.
  * iDRAC 9 based Dell EMC PowerEdge Servers with Firmware versions 3.34.34.34 and above.
  * Dell EMC OpenManage Enterprise versions 3.2.1 and above.
  * Dell EMC OpenManage Enterprise-Modular versions 1.20.00 and above.

## Prerequisites
  * [Ansible](https://github.com/ansible/ansible) versions: 2.8.4 to 2.9.15
  * Python >=2.7.17 or >=3.6.5
  * To run the iDRAC modules, install OpenManage Python Software Development
   Kit (OMSDK) using ``` pip install omsdk --upgrade``` or from 
   [Dell EMC OpenManage Python SDK](https://github.com/dell/omsdk)

## Documentation
Please refer to the [OpenManage Ansible Modules Documentation](./guides)

## Examples
Latest sample playbooks and examples are available under [playbooks](./playbooks) directory

## Results
Latest sample results for the respective modules are available under [output](./output) directory.

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

## Building a Docker image of OpenManage Ansible Modules
Refer the following [document](./docker/README.md) for detailed instructions on how to build a docker image of OpenManage Ansible Modules.

## LICENSE
This project is licensed under GPL-3.0 License. Please see the [COPYING](
./COPYING.md) for more information


## Contributing
We welcome your contributions to OpenManage Ansible Modules. See [Coding Guidelines](./CODING_GUIDELINES.md) for more details.
You can refer our [Code of Conduct](./CODE_OF_CONDUCT.md) here.

## Testing
See [here](test/README.md) for further information on testing.

## Maintenance
  * OpenManage Ansible Modules releases follows a monthly release cycle. On the last week of every month, 
  the updated modules are posted to this repository.
  * OpenManage Ansible Modules releases follow [semantic versioning](https://semver.org/).
  * OpenManage Ansible Modules deprecation cycle is aligned with [Ansible](https://docs.ansible.com/ansible/latest/dev_guide/module_lifecycle.html).


## Support
  * This branch only supports maintenance changes such as bug fixes and security fixes.
  * If you want to report any issue, then please report it by creating a new issue [here](https://github.com/dell/dellemc-openmanage-ansible-modules/issues)
  * If you want to provide any feedback to the development team, then you can do so by sending an email to **OpenManageAnsible@Dell.com**

## Authors
  * OpenManageAnsible (OpenManageAnsible@dell.com)
