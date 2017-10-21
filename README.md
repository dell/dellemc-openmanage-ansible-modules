# Dell EMC OpenManage Ansible Modules (BETA)

Dell EMC OpenManage Ansible Modules provide customers the ability to automate the Out-of-Band configuration management, deployment and updates for Dell EMC PowerEdge Servers using Ansible by leveraging the management automation built into the iDRAC with Lifecycle Controller. iDRAC provides both REST APIs based on DMTF RedFish industry standard and WS-Management (WS-MAN) based on DMTF's Web Services management standard for management automation of PowerEdge Servers.

## Supported Platforms
Dell EMC PowerEdge Servers with:
  * iDRAC 7/8 with Firmware version 2.00.00.00 or above
  * iDRAC 9 with Firmware version 3.00.00.00

## Prerequisites
  * Ansible >= 2.3
  * Python >= 2.7.9
  * [Dell EMC OpenManage Python SDK](https://github.com/vaideesg/omsdk)

## Documentation

Please refer to the [OpenManage Ansible Modules Documentation](docs/Dell-EMC-OpenManage-Ansible-Modules.md)

## Examples

Sample playbooks and examples could be found under [examples](./examples) directory

## Installation

  * Ansible must be installed

  ```
  pip install ansible
  ```

  * You will need the latest [Dell EMC OpenManage Python SDK](https://github.com/vaideesg/omsdk)
  ```
  pip install omsdk
  ```

  * Clone this repository and install the ansible modules. This will copy the OpenManage Ansible modules in ```ansible/modules/remote_management/dellemc/idrac``` directory and ```utils/dellemc_idrac.py``` in ```ansible/module_utils/``` directory.

  ```
  git clone https://github.com/anupamaloke/Dell-EMC-Ansible-Modules-for-iDRAC.git
  cd Dell-EMC-Ansible-Modules-for-iDRAC
  python install.py
  ```

## Uninstallation

```
cd Dell-EMC-Ansible-Modules-for-iDRAC
python uninstall.py
```

## LICENSE
This project is licensed under GPL-3.0 License. Please see the [LICENSE](https://github.com/anupamaloke/Dell-EMC-Ansible-Modules-for-iDRAC/blob/master/LICENSE) for more information

## Support
Please note that OpenManage Ansible Modules is in **BETA** development stage and therefore **not ready for production**. However, if you want to report any issues or provide any feedback, then please send an email to OpenManageAnsibleEval@dell.com.
 
## Authors
  * OpenManageAnsibleEval (OpenManageAnsibleEval@dell.com)
