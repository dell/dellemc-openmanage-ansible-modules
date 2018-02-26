# Dell EMC OpenManage Ansible Modules

Dell EMC OpenManage Ansible Modules allows Data Center and IT administrators to use RedHat Ansible to automate and orchestrate the configuration, deployment, and update of Dell EMC PowerEdge Servers (12th generation of PowerEdge servers and later) by leveraging the management automation capabilities in-built into the integrated Dell Remote Access Controller (iDRAC).

## Supported Platforms
Dell EMC PowerEdge Servers with:
  * 12G and 13G PowerEdge Servers: iDRAC 7/8 with Firmware version 2.41.40.40 and above
  * 14G PowerEdge Servers: iDRAC 9 with Firmware version 3.00.00.00 and above

## Prerequisites
  * Ansible >= 2.2
  * Python >= 2.7
  * [Dell EMC OpenManage Python SDK](https://github.com/dell/omsdk)

## Documentation
Please refer to the [OpenManage Ansible Modules Documentation](./docs) 

## Examples
Sample playbooks and examples could be found under [examples](./examples) directory

## Results
Sample Results for the respective modules could be found under [samples](./samples) directory.

## Installation

  * Ansible must be installed

  ```
  yum install ansible
  ```

  * You will need the latest [Dell EMC OpenManage Python SDK](https://github.com/dell/omsdk)
  ```
  pip install omsdk
  ```

  * Clone this repository and install the ansible modules. 
  ```
  git clone https://github.com/dell/Dell-EMC-Ansible-Modules-for-iDRAC.git
  cd Dell-EMC-Ansible-Modules-for-iDRAC
  python install.py
  ```

## Uninstallation

```
cd Dell-EMC-Ansible-Modules-for-iDRAC
python uninstall.py
```

## LICENSE
This project is licensed under GPL-3.0 License. Please see the [COPYING](https://github.com/dell/Dell-EMC-Ansible-Modules-for-iDRAC/blob/master/COPYING.md) for more information

## Support
  * Dell EMC OpenManage Ansible Modules are supported by Dell support.
  * In addition, if you want to report any issue, then please report it by creating a new issue [here](https://github.com/dell/Dell-EMC-Ansible-Modules-for-iDRAC/issues)
  * If you have any requirements that is not currently addressed, then please let us know by creating a new issue [here](https://github.com/dell/Dell-EMC-Ansible-Modules-for-iDRAC/issues)
  * If you want to provide any feedback to the development team, then you can do so by sending an email to **OpenManageAnsibleEval@Dell.com**
  * We also have a **#openmanageansibleval** slack channel which you can use for reporting any issue, new feature request or for general discussion with development team.

## Authors
  * OpenManageAnsibleEval (OpenManageAnsibleEval@dell.com)
