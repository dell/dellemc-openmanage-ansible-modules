#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.9.0
# Copyright (C) 2024-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: omevv_baseline_profile_info
short_description: Retrieve OMEVV baseline profile information.
version_added: "9.9.0"
description:
  - This module allows you to retrieve all or the specific OMEVV baseline profile information.
extends_documentation_fragment:
  - dellemc.openmanage.omevv_auth_options
options:
  name:
    description:
      - Name of the baseline profile.
      - If I(name) is provided, the module retrieves only specified baseline profile information.
    type: str
requirements:
  - "python >= 3.9.6"
author:
  - "Kritika Bhateja (@Kritika-Bhateja-03)"
attributes:
    check_mode:
        description: Runs task to validate without performing action on the target machine.
        support: full
notes:
  - Run this module from a system that has direct access to Dell OpenManage Enterprise.
"""


EXAMPLES = r"""
---
- name: Retrieve all baseline profile information.
  dellemc.openmanage.omevv_baseline_profile_info:
    hostname: "192.168.0.1"
    vcenter_uuid: "xxxxxx"
    vcenter_username: "username"
    vcenter_password: "password"
    ca_path: "path/to/ca_file"

- name: Retrieve specific baseline profile information using profile name.
  dellemc.openmanage.omevv_baseline_profile_info:
    hostname: "192.168.0.1"
    vcenter_uuid: "xxxxxx"
    vcenter_username: "username"
    vcenter_password: "password"
    ca_path: "path/to/ca_file"
    name: profile-1
"""

RETURN = r"""
---
msg:
  description: Status of the baseline profile information for the retrieve operation.
  returned: always
  type: str
  sample: "Successfully retrieved the baseline profile information."
baseline_profile_info:
  description: Information on the vCenter.
  returned: success
  type: list
  elements: dict
  sample:
    [
        {
            "id": 1000,
            "name": "Baseline-1",
            "description": "Baseline-1 desc",
            "consoleId": "xxxxx",
            "consoleAddress": "xx.xx.xx.xx",
            "firmwareRepoId": 1000,
            "firmwareRepoName": "Dell Default Catalog",
            "configurationRepoId": null,
            "configurationRepoName": null,
            "driverRepoId": null,
            "driverRepoName": null,
            "driftJobId": 1743,
            "driftJobName": "BP-Baseline-1-Host-Firmware-Drift-Detection",
            "dateCreated": "2024-10-16T10:25:29.786Z",
            "dateModified": null,
            "lastmodifiedBy": "Administrator@VSPHERE.LOCAL",
            "version": "1.0.0-0",
            "lastSuccessfulUpdatedTime": "2024-10-16T10:27:35.212Z",
            "clusterGroups": [],
            "datacenter_standAloneHostsGroups": [],
            "baselineType": null,
            "status": "SUCCESSFUL"
        },
        {
            "id": 1001,
            "name": "Baseline - 2",
            "description": "Baseline - 2 description",
            "consoleId": "xxxxx",
            "consoleAddress": "xx.xx.xx.xx",
            "firmwareRepoId": 1000,
            "firmwareRepoName": "Dell Default Catalog",
            "configurationRepoId": null,
            "configurationRepoName": null,
            "driverRepoId": null,
            "driverRepoName": null,
            "driftJobId": 1812,
            "driftJobName": "BP-Baseline - 2-Host-Firmware-Drift-Detection",
            "dateCreated": "2024-10-16T12:38:56.581Z",
            "dateModified": null,
            "lastmodifiedBy": "Administrator@VSPHERE.LOCAL",
            "version": "1.0.0-0",
            "lastSuccessfulUpdatedTime": "2024-10-16T12:41:02.641Z",
            "clusterGroups": [],
            "datacenter_standAloneHostsGroups": [
                {
                    "associated_datacenterID": "datacenter-1001",
                    "associated_datacenterName": "Standalone Hosts-Test-DC",
                    "omevv_groupID": 1002
                }
            ],
            "baselineType": "DATACENTER_NONCLUSTER",
            "status": "SUCCESSFUL"
        }
    ]
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
      "code": "Base.1.0.GeneralError",
      "message": "A general error has occurred. See ExtendedInfo for more information.",
      "@Message.ExtendedInfo": [
        {
          "MessageId": "GEN1234",
          "RelatedProperties": [],
          "Message": "Unable to process the request because an error occurred.",
          "MessageArgs": [],
          "Severity": "Critical",
          "Resolution": "Retry the operation. If the issue persists, contact your system administrator."
        }
      ]
    }
  }
"""

import json
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv import RestOMEVV, OMEVVAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv_utils.omevv_firmware_utils import OMEVVBaselineProfile

SUCCESS_MSG = "Successfully retrieved the baseline profile information."
NO_PROFILE_MSG = "'{profile_name}' baseline profile name does not exist in OMEVV."
ERROR_CODES = ["12027"]


class OMEVVBaselineProfileInfo:

    def __init__(self, module, rest_obj) -> None:
        """
        Initializes a new instance of the class.
        Args:
            module (object): The module object.
            rest_obj (object): The REST object.
        Returns:
            None
        """
        self.module = module
        self.obj = rest_obj

    def perform_module_operation(self) -> dict:
        """
        Retrieves the baseline profile information.
        Returns:
            dict: A dictionary containing the message and the baseline profile information.
                - msg (str): The success message or the error message.
                - profile_info (list): The list of baseline profile information.
        """
        profile_name = self.module.params.get("name")
        uuid = self.module.params.get("vcenter_uuid")
        self.omevv_utils_obj = OMEVVBaselineProfile(self.obj)
        if profile_name:
            resp = self.omevv_utils_obj.get_baseline_profile_by_name(profile_name, uuid)
        else:
            resp = self.omevv_utils_obj.get_baseline_profiles(uuid)
        result = {'msg': SUCCESS_MSG, 'profile_info': resp}
        if not resp:
            result['msg'] = NO_PROFILE_MSG.format(profile_name=profile_name)
        return result


def main():
    """
    Retrieves the baseline profile information.

    Returns:
        dict: A dictionary containing the message and the baseline profile information.
            - msg (str): The success message or the error message.
            - profile_info (list): The list of baseline profile information.

    Error Codes:
        - 12027: The specified vCenter UUID is not registered in OME.
    """
    argument_spec = {
        "name": {"type": 'str'}
    }
    module = OMEVVAnsibleModule(argument_spec=argument_spec,
                                supports_check_mode=True)
    try:
        with RestOMEVV(module.params) as rest_obj:
            omevv_obj = OMEVVBaselineProfileInfo(module, rest_obj)
            resp = omevv_obj.perform_module_operation()
            module.exit_json(msg=resp['msg'], profile_info=resp['profile_info'])
    except HTTPError as err:
        error_info = json.load(err)
        message = error_info.get('message')
        code = error_info.get('errorCode')
        if code in ERROR_CODES:
            module.exit_json(msg=message, skipped=True)
        module.exit_json(msg=str(err), error_info=error_info, failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, TypeError, ConnectionError, IOError, ValueError,
            AttributeError, OSError, IndexError, KeyError,) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
