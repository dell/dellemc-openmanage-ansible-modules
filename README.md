# Dell EMC OpenManage Ansible Modules for iDRAC
Dell EMC OpenManage Ansible Modules provide capabilities for out-of-band management of PowerEdge Servers using Integrated Dell Remote Access Controller (iDRAC).

# Supported Platforms
- iDRAC 7/8 with FW version 2.00.00.00 or above

# Prerequisites
- Dell EMC OpenManage SDK

# Installation
- Ansible must be installed
```
sudo pip install ansible
```
- You will need the latest Dell EMC OpenManage SDK
```
sudo pip install omsdk
```
- Clone this repository and install the ansible modules
```
git clone https://github.com/anupamaloke/Dell-EMC-Ansible-Modules-for-iDRAC.git
cd Dell-EMC-Ansible-Modules-for-iDRAC
sudo python install.py
```
# Uninstallation
```
cd Dell-EMC-Ansible-Modules-for-iDRAC
sudo python uninstall.py
```

# Support
Please note that this is still in development and therefore no support is provided at present. However, if you want to report any issues or provide any feedback, then please send an email to anupam.aloke@dell.com.
 
# Authors
- Anupam Aloke (anupam.aloke@dell.com)
