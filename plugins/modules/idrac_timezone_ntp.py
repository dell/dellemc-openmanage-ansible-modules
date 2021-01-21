#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.0.0
# Copyright (C) 2018-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_timezone_ntp
short_description: Configures time zone and NTP on iDRAC
version_added: "2.1.0"
description:
    - This module allows to configure time zone and NTP on iDRAC.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
  - dellemc.openmanage.network_share_options
options:
    setup_idrac_timezone:
        type: str
        description: Allows to configure time zone on iDRAC.
    enable_ntp:
        type: str
        description: Allows to enable or disable NTP on iDRAC.
        choices: [Enabled, Disabled]
    ntp_server_1:
        type: str
        description: The IP address of the NTP server 1.
    ntp_server_2:
        type: str
        description: The IP address of the NTP server 2.
    ntp_server_3:
        type: str
        description: The IP address of the NTP server 3.

requirements:
    - "omsdk"
    - "python >= 2.7.5"
author:
    - "Felix Stephen (@felixs88)"
    - "Anooja Vardhineni (@anooja-vardhineni)"
notes:
    - Run this module from a system that has direct access to DellEMC iDRAC.
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Configure time zone and NTP on iDRAC
  dellemc.openmanage.idrac_timezone_ntp:
       idrac_ip:   "190.168.0.1"
       idrac_user: "user_name"
       idrac_password:  "user_password"
       share_name: "user_name:/share"
       share_password:  "share_password"
       share_user: "user_name"
       share_mnt: "/mnt/share"
       setup_idrac_timezone: "UTC"
       enable_ntp: Enabled
       ntp_server_1: "190.168.0.1"
       ntp_server_2: "190.168.0.2"
       ntp_server_3: "190.168.0.3"
"""

RETURN = r'''
---
msg:
  description: Overall status of the timezone and ntp configuration.
  returned: always
  type: str
  sample: "Successfully configured the iDRAC time settings."
timezone_ntp_status:
    description: Job details of the time zone setting operation.
    returned: success
    type: dict
    sample: {
        "@odata.context": "/redfish/v1/$metadata#DellJob.DellJob",
        "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_861801613971",
        "@odata.type": "#DellJob.v1_0_0.DellJob",
        "CompletionTime": "2020-04-06T19:06:01",
        "Description": "Job Instance",
        "EndTime": null,
        "Id": "JID_861801613971",
        "JobState": "Completed",
        "JobType": "ImportConfiguration",
        "Message": "Successfully imported and applied Server Configuration Profile.",
        "MessageArgs": [],
        "MessageId": "SYS053",
        "Name": "Import Configuration",
        "PercentComplete": 100,
        "StartTime": "TIME_NOW",
        "Status": "Success",
        "TargetSettingsURI": null,
        "retval": true
}
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
'''


from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
import json
try:
    from omdrivers.enums.iDRAC.iDRAC import NTPEnable_NTPConfigGroupTypes
    from omsdk.sdkfile import file_share_manager
    from omsdk.sdkcreds import UserCredentials
except ImportError:
    pass


def run_idrac_timezone_config(idrac, module):
    """
    Get Lifecycle Controller status

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    idrac.use_redfish = True
    upd_share = file_share_manager.create_share_obj(share_path=module.params['share_name'],
                                                    mount_point=module.params['share_mnt'],
                                                    isFolder=True,
                                                    creds=UserCredentials(
                                                    module.params['share_user'],
                                                    module.params['share_password']))

    idrac.config_mgr.set_liason_share(upd_share)

    if module.params['setup_idrac_timezone'] is not None:
        idrac.config_mgr.configure_timezone(module.params['setup_idrac_timezone'])

    if module.params['enable_ntp'] is not None:
        idrac.config_mgr.configure_ntp(
            enable_ntp=NTPEnable_NTPConfigGroupTypes[module.params['enable_ntp']]
        )
    if module.params['ntp_server_1'] is not None:
        idrac.config_mgr.configure_ntp(
            ntp_server_1=module.params['ntp_server_1']
        )
    if module.params['ntp_server_2'] is not None:
        idrac.config_mgr.configure_ntp(
            ntp_server_2=module.params['ntp_server_2']
        )
    if module.params['ntp_server_3'] is not None:
        idrac.config_mgr.configure_ntp(
            ntp_server_3=module.params['ntp_server_3']
        )

    if module.check_mode:
        msg = idrac.config_mgr.is_change_applicable()
    else:
        msg = idrac.config_mgr.apply_changes(reboot=False)
    return msg


# Main
def main():
    module = AnsibleModule(
        argument_spec={

            # iDRAC credentials
            "idrac_ip": {"required": True, "type": 'str'},
            "idrac_user": {"required": True, "type": 'str'},
            "idrac_password": {"required": True, "type": 'str', "aliases": ['idrac_pwd'], "no_log": True},
            "idrac_port": {"required": False, "default": 443, "type": 'int'},

            # Export Destination
            "share_name": {"required": True, "type": 'str'},
            "share_password": {"required": False, "type": 'str', "aliases": ['share_pwd'], "no_log": True},
            "share_user": {"required": False, "type": 'str'},
            "share_mnt": {"required": False, "type": 'str'},

            # setup NTP
            "enable_ntp": {"required": False, "choices": ['Enabled', 'Disabled']},
            "ntp_server_1": {"required": False},
            "ntp_server_2": {"required": False},
            "ntp_server_3": {"required": False},

            # set up timezone
            "setup_idrac_timezone": {"required": False, "type": 'str'},

        },
        supports_check_mode=True)

    try:
        with iDRACConnection(module.params) as idrac:
            changed = False
            msg = run_idrac_timezone_config(idrac, module)
            if "Status" in msg:
                if msg['Status'] == "Success":
                    changed = True
                    if "Message" in msg:
                        if msg['Message'] == "No changes found to commit!":
                            changed = False
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError) as e:
        module.fail_json(msg=str(e))
    module.exit_json(msg="Successfully configured the iDRAC time settings.",
                     timezone_ntp_status=msg, changed=changed)


if __name__ == '__main__':
    main()
