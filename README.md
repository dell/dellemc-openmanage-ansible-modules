# Dell EMC OpenManage Ansible Modules Version: 1.0

Dell EMC OpenManage Ansible Modules allows Data Center and IT administrators to use RedHat Ansible to automate and orchestrate the configuration, deployment, and update of Dell EMC PowerEdge Servers (12th generation of PowerEdge servers and later) by leveraging the management automation capabilities in-built into the integrated Dell Remote Access Controller (iDRAC).

## Supported Platforms
Dell EMC PowerEdge Servers with:
  * iDRAC 7/8 with Firmware version 2.41.40.40 and above
  * iDRAC 9 with Firmware version 3.00.00.00 and above

## Prerequisites
  * Ansible >= 2.2
  * Python >= 2.7
  * [Dell EMC OpenManage Python SDK](https://github.com/dell/omsdk)

## Documentation

Please refer to the [OpenManage Ansible Modules Documentation](./docs) 

## Examples

Sample playbooks and examples could be found under [examples](./examples) directory

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
If you want to report any issues or provide any feedback, then please send an email to OpenManageAnsibleEval@dell.com.

We also have a **#openmanageansible** slack channel. You can get an invite by requesting one at http://community.codedellemc.com. 

 
## Authors
  * OpenManageAnsibleEval (OpenManageAnsibleEval@dell.com)
