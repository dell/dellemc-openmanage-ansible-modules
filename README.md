# Dell EMC OpenManage Ansible Modules (BETA)

Dell EMC OpenManage Ansible Modules provide customers the ability to automate the Out-of-Band configuration management, deployment and updates for Dell EMC PowerEdge Servers using Ansible by leveraging the management automation built into the iDRAC with Lifecycle Controller. iDRAC provides both REST APIs based on DMTF RedFish industry standard and WS-Management (WS-MAN) based on DMTF's Web Services management standard for management automation of PowerEdge Servers.

# Supported Platforms
Dell EMC PowerEdge Servers with:
  * iDRAC 7/8 with FW version 2.00.00.00 or above
  * iDRAC 9 with FW version 3.00.00.00

# Prerequisites
  * [Dell EMC OpenManage Python SDK](https://github.com/vaideesg/omsdk)

# Documentation

Please refer to the [OpenManage Ansible Modules Documentation](doc/Dell-EMC-OpenManage-Ansible-Modules.md)

# Installation

  * Ansible must be installed

  ```
  pip install ansible
  ```

  * You will need the latest [Dell EMC OpenManage Python SDK](https://github.com/vaideesg/omsdk)
  ```
  git clone https://github.com/vaideesg/omsdk.git
  cd omsdk
  sh build.bat
  cd dist
  pip install omsdk
  ```

  * Clone this repository and install the ansible modules
  ```
  git clone https://github.com/anupamaloke/Dell-EMC-Ansible-Modules-for-iDRAC.git
  cd Dell-EMC-Ansible-Modules-for-iDRAC
  python install.py
  ```

# Uninstallation

```
cd Dell-EMC-Ansible-Modules-for-iDRAC
python uninstall.py
```

# Support
Please note that OpenManage Ansible Modules is still in development and therefore no support is provided at present. However, if you want to report any issues or provide any feedback, then please send an email to OpenManageAnsibleEval@dell.com.
 
# Authors
  * Anupam Aloke (anupam.aloke@dell.com)
