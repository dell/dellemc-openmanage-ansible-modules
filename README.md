# Dell OpenManage Ansible Modules

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.1%20adopted-ff69b4.svg)](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/docs/CODE_OF_CONDUCT.md)
[![License](https://img.shields.io/github/license/dell/dellemc-openmanage-ansible-modules)](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/LICENSE)
[![Python version](https://img.shields.io/badge/python-3.9.6+-blue.svg)](https://www.python.org/downloads/)
[![Ansible version](https://img.shields.io/badge/ansible-2.15.6+-blue.svg)](https://pypi.org/project/ansible/)
[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/dell/dellemc-openmanage-ansible-modules?include_prereleases&label=latest&style=flat-square)](https://github.com/dell/dellemc-openmanage-ansible-modules/releases)
[![codecov](https://codecov.io/gh/dell/dellemc-openmanage-ansible-modules/branch/collections/graph/badge.svg)](https://app.codecov.io/gh/dell/dellemc-openmanage-ansible-modules)

Dell OpenManage Ansible Modules allows data center and IT administrators to use RedHat Ansible to automate and orchestrate the configuration, deployment, and update of Dell PowerEdge Servers and modular infrastructure by leveraging the management automation capabilities in-built into the Integrated Dell Remote Access Controller (iDRAC), OpenManage Enterprise (OME), OpenManage Enterprise Modular (OMEM) and OpenManage Enterprise Integration for VMWare vCenter Plug-in.

OpenManage Ansible Modules simplifies and automates provisioning, deployment, and updates of PowerEdge servers and modular infrastructure. It allows system administrators and software developers to introduce the physical infrastructure provisioning into their software provisioning stack, integrate with existing DevOps pipelines and manage their infrastructure using version-controlled playbooks, server configuration profiles, and templates in line with the Infrastructure-as-Code (IaC) principles.

## Table of Contents

  * [Code of Conduct](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/docs/CODE_OF_CONDUCT.md)
  * [Committer Guide](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/docs/COMMITTER_GUIDE.md)
  * [Contributing Guide](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/docs/CONTRIBUTING.md)
  * [Maintainers](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/docs/MAINTAINERS.md)
  * [Support](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/docs/SUPPORT.md)
  * [Security](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/docs/SECURITY.md)
  * [Documentation](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/docs/DOCUMENTATION.md)
  * [Execution Environment](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/docs/EXECUTION_ENVIRONMENT.md)
  * [Attribution](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/docs/ATTRIBUTION.md)
  * [Additional Information](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/docs/ADDITIONAL_INFORMATION.md)

## Supported Platforms
  * iDRAC9 based Dell PowerEdge Servers with firmware versions 7.10.90.00 and above.
  * iDRAC10 based Dell PowerEdge Servers with firmware versions 1.20.50.50 and above (for supported modules refer [here](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/docs/README.md)).
  * Dell OpenManage Enterprise versions 3.10 and 4.2.
  * Dell OpenManage Enterprise Modular versions 2.10.10 and above.

## Requirements
  * [Ansible Core >= 2.18.7 and 2.17.13](https://github.com/ansible/ansible)
  * Python >= 3.9.6
  * To run the iDRAC modules, install OpenManage Python Software Development Kit (OMSDK) 
  using either ```pip install omsdk --upgrade``` or ```pip install -r requirements.txt```. 
  OMSDK can also be installed from [Dell OpenManage Python SDK](https://github.com/dell/omsdk)
  * Operating System
    * Red Hat Enterprise Linux (RHEL) 9.5 and 8.10
    * SUSE Linux Enterprise Server (SLES) 15 SP5 and 15 SP4
    * Ubuntu 24.04.1 and 24.04

## Installation

* From [Galaxy](https://galaxy.ansible.com/dellemc/openmanage) or [Automation Hub](https://console.redhat.com/ansible/automation-hub/repo/published/dellemc/openmanage):  
Install the latest Ansible collection from the Ansible Galaxy or Automation hub 
  ```
  ansible-galaxy collection install dellemc.openmanage
  ```

* From [GitHub](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections):  
Install the Ansible collection from the GitHub repository using the latest commit with the branch name 'collections'  
  ```
  ansible-galaxy collection install git+https://github.com/dell/dellemc-openmanage-ansible-modules.git,collections
  ```

* To Upgrade:
Update the `dellemc.openmanage` collection to the latest version available on [Galaxy](https://galaxy.ansible.com/dellemc/openmanage) and [Automation Hub](https://console.redhat.com/ansible/automation-hub/repo/published/dellemc/openmanage)
  ```
  ansible-galaxy collection install dellemc.openmanage --upgrade
  ```

* To specific version:  
Install a specifc version of the collection from the [Galaxy](https://galaxy.ansible.com/dellemc/openmanage) and [Automation Hub](https://console.redhat.com/ansible/automation-hub/repo/published/dellemc/openmanage)
  ```
  ansible-galaxy collection install dellemc.openmanage:==<version>
  ```

* Offline Installation:  
For offline installation on the Ansible control machine, download the required tar archive version of the collection from [Dell OpenManage collection](https://galaxy.ansible.com/dellemc/openmanage) and run the command given below:  
    ```
    ansible-galaxy collection install dellemc-openmanage-<version>.tar.gz
    ```

For more details, see [Using Ansible collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html)

## Use Cases
For more information about how to use the collection, refer to [OME modules](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections/playbooks/ome), [iDRAC modules](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections/playbooks/idrac), [Redfish modules](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections/playbooks/redfish) and [roles](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections/playbooks/roles). 

## Testing

For more information about Unit testing, see [Unit testing](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/tests/README.md).

For more information about Integration testing, see [Integration testing](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/tests/integration/README.md).

## Support

For support, see [SUPPORT.md](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/docs/SUPPORT.md).

## Release Notes

For release notes, see [CHANGELOG.rst](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/CHANGELOG.rst).

## Related Information
Refer the [Table of Contents](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/README.md#table-of-contents) for any other information on the Dell OpenManage Ansible Modules documentations.

## License Information
Dell OpenManage Ansible Modules is 100% open source and community-driven. All components are available under [GPL-3.0-only](https://www.gnu.org/licenses/gpl-3.0.html) on GitHub.
