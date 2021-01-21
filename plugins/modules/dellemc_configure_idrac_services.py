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
module: dellemc_configure_idrac_services
short_description: Configures the iDRAC services related attributes
version_added: "1.0.0"
description:
    - This module allows to configure the iDRAC services related attributes.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
    share_name:
        required: True
        type: str
        description: Network share or a local path.
    share_user:
        type: str
        description: Network share user in the format 'user@domain' or 'domain\\user' if user is
            part of a domain else 'user'. This option is mandatory for CIFS Network Share.
    share_password:
        type: str
        description: Network share user password. This option is mandatory for CIFS Network Share.
        aliases: ['share_pwd']
    share_mnt:
        type: str
        description: Local mount path of the network share with read-write permission for ansible user.
            This option is mandatory for Network Share.
    enable_web_server:
        type: str
        description: Whether to Enable or Disable webserver configuration for iDRAC.
        choices: [Enabled, Disabled]
    ssl_encryption:
        type: str
        description: Secure Socket Layer encryption for webserver.
        choices: [Auto_Negotiate, T_128_Bit_or_higher, T_168_Bit_or_higher, T_256_Bit_or_higher]
    tls_protocol:
        type: str
        description: Transport Layer Security for webserver.
        choices: [TLS_1_0_and_Higher, TLS_1_1_and_Higher, TLS_1_2_Only]
    https_port:
        type: int
        description: HTTPS access port.
    http_port:
        type: int
        description: HTTP access port.
    timeout:
        type: str
        description: Timeout value.
    snmp_enable:
        type: str
        description: Whether to Enable or Disable SNMP protocol for iDRAC.
        choices: [Enabled, Disabled]
    snmp_protocol:
        type: str
        description: Type of the SNMP protocol.
        choices: [All, SNMPv3]
    community_name:
        type: str
        description: SNMP community name for iDRAC. It is used by iDRAC to validate SNMP queries
            received from remote systems requesting SNMP data access.
    alert_port:
        type: int
        description: The iDRAC port number that must be used for SNMP traps.
            The default value is 162, and the acceptable range is between 1 to 65535.
        default: 162
    discovery_port:
        type: int
        description: The SNMP agent port on the iDRAC. The default value is 161,
            and the acceptable range is between 1 to 65535.
        default: 161
    trap_format:
        type: str
        description: SNMP trap format for iDRAC.
        choices: [SNMPv1, SNMPv2, SNMPv3]
    ipmi_lan:
        type: dict
        description: Community name set on iDRAC for SNMP settings.
        suboptions:
            community_name:
                type: str
                description: This option is used by iDRAC when it sends out SNMP and IPMI traps.
                    The community name is checked by the remote system to which the traps are sent.
requirements:
    - "omsdk"
    - "python >= 2.7.5"
author: "Felix Stephen (@felixs88)"
notes:
    - Run this module from a system that has direct access to DellEMC iDRAC.
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Configure the iDRAC services attributes
  dellemc.openmanage.dellemc_configure_idrac_services:
       idrac_ip:   "192.168.0.1"
       idrac_user: "user_name"
       idrac_password:  "user_password"
       share_name: "192.168.0.1:/share"
       share_mnt: "/mnt/share"
       enable_web_server: "Enabled"
       http_port: 80
       https_port: 443
       ssl_encryption: "Auto_Negotiate"
       tls_protocol: "TLS_1_2_Only"
       timeout: "1800"
       snmp_enable: "Enabled"
       snmp_protocol: "SNMPv3"
       community_name: "public"
       alert_port: 162
       discovery_port: 161
       trap_format: "SNMPv3"
       ipmi_lan:
         community_name: "public"
"""

RETURN = r'''
---
msg:
  description: Overall status of iDRAC service attributes configuration.
  returned: always
  type: str
  sample: Successfully configured the iDRAC services settings.
service_status:
    description: Details of iDRAC services attributes configuration.
    returned: success
    type: dict
    sample: {
        "CompletionTime": "2020-04-02T02:43:28",
        "Description": "Job Instance",
        "EndTime": null,
        "Id": "JID_12345123456",
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

import json
from ansible_collections.dellemc.openmanage.plugins.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError

try:
    from omdrivers.enums.iDRAC.iDRAC import (Enable_WebServerTypes,
                                             SSLEncryptionBitLength_WebServerTypes,
                                             TLSProtocol_WebServerTypes,
                                             AgentEnable_SNMPTypes,
                                             SNMPProtocol_SNMPTypes)
    from omsdk.sdkfile import file_share_manager
    from omsdk.sdkcreds import UserCredentials
except ImportError:
    pass


def run_idrac_services_config(idrac, module):
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
                                                        module.params['share_password'])
                                                    )

    set_liason = idrac.config_mgr.set_liason_share(upd_share)
    if set_liason['Status'] == "Failed":
        try:
            message = set_liason['Data']['Message']
        except (IndexError, KeyError):
            message = set_liason['Message']
        module.fail_json(msg=message)

    if module.params['enable_web_server'] is not None:
        idrac.config_mgr.configure_web_server(
            enable_web_server=Enable_WebServerTypes[module.params['enable_web_server']]
        )
    if module.params['http_port'] is not None:
        idrac.config_mgr.configure_web_server(
            http_port=module.params['http_port']
        )
    if module.params['https_port'] is not None:
        idrac.config_mgr.configure_web_server(
            https_port=module.params['https_port']
        )
    if module.params['timeout'] is not None:
        idrac.config_mgr.configure_web_server(
            timeout=module.params['timeout']
        )
    if module.params['ssl_encryption'] is not None:
        idrac.config_mgr.configure_web_server(
            ssl_encryption=SSLEncryptionBitLength_WebServerTypes[module.params['ssl_encryption']]
        )
    if module.params['tls_protocol'] is not None:
        idrac.config_mgr.configure_web_server(
            tls_protocol=TLSProtocol_WebServerTypes[module.params['tls_protocol']]
        )

    if module.params['snmp_enable'] is not None:
        idrac.config_mgr.configure_snmp(
            snmp_enable=AgentEnable_SNMPTypes[module.params['snmp_enable']]
        )
    if module.params['community_name'] is not None:
        idrac.config_mgr.configure_snmp(
            community_name=module.params['community_name']
        )
    if module.params['snmp_protocol'] is not None:
        idrac.config_mgr.configure_snmp(
            snmp_protocol=SNMPProtocol_SNMPTypes[module.params['snmp_protocol']]
        )
    if module.params['alert_port'] is not None:
        idrac.config_mgr.configure_snmp(
            alert_port=module.params['alert_port']
        )
    if module.params['discovery_port'] is not None:
        idrac.config_mgr.configure_snmp(
            discovery_port=module.params['discovery_port']
        )
    if module.params['trap_format'] is not None:
        idrac.config_mgr.configure_snmp(
            trap_format=module.params['trap_format']
        )
    if module.params['ipmi_lan'] is not None:
        ipmi_option = module.params.get('ipmi_lan')
        community_name = ipmi_option.get('community_name')
        if community_name is not None:
            idrac.config_mgr.configure_snmp(ipmi_community=community_name)

    if module.check_mode:
        status = idrac.config_mgr.is_change_applicable()
        if status.get('changes_applicable'):
            module.exit_json(msg="Changes found to commit!", changed=True)
        else:
            module.exit_json(msg="No changes found to commit!")
    else:
        return idrac.config_mgr.apply_changes(reboot=False)


# Main
def main():
    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_password=dict(required=True, type='str', aliases=['idrac_pwd'], no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Export Destination
            share_name=dict(required=True, type='str'),
            share_password=dict(required=False, type='str', aliases=['share_pwd'], no_log=True),
            share_user=dict(required=False, type='str'),
            share_mnt=dict(required=False, type='str'),

            # setup Webserver
            enable_web_server=dict(required=False, choices=['Enabled', 'Disabled'], default=None),
            http_port=dict(required=False, default=None, type='int'),
            https_port=dict(required=False, default=None, type='int'),
            ssl_encryption=dict(required=False, choices=['Auto_Negotiate', 'T_128_Bit_or_higher',
                                                         'T_168_Bit_or_higher', 'T_256_Bit_or_higher'],
                                default=None),
            tls_protocol=dict(required=False, choices=['TLS_1_0_and_Higher',
                                                       'TLS_1_1_and_Higher', 'TLS_1_2_Only'], default=None),
            timeout=dict(required=False, default=None, type="str"),

            # set up SNMP settings
            snmp_enable=dict(required=False, choices=['Enabled', 'Disabled'], default=None),
            community_name=dict(required=False, type='str'),
            snmp_protocol=dict(required=False, choices=['All', 'SNMPv3'], default=None),
            discovery_port=dict(required=False, type="int", default=161),

            # set up SNMP settings
            ipmi_lan=dict(required=False, type='dict', options=dict(community_name=dict(required=False, type='str'))),
            alert_port=dict(required=False, type='int', default=162),
            trap_format=dict(required=False, choices=['SNMPv1', 'SNMPv2', 'SNMPv3'], default=None),

        ),

        supports_check_mode=True)

    try:
        with iDRACConnection(module.params) as idrac:
            status = run_idrac_services_config(idrac, module)
            if status.get('Status') == "Success":
                changed = True
                msg = "Successfully configured the iDRAC services settings."
                if status.get('Message') and (status.get('Message') == "No changes found to commit!" or
                                              "No changes were applied" in status.get('Message')):
                    msg = status.get('Message')
                    changed = False
                elif status.get('Status') == "Failed":
                    module.fail_json(msg="Failed to configure the iDRAC services.")
                module.exit_json(msg=msg, service_status=status, changed=changed)
            else:
                module.fail_json(msg="Failed to configure the iDRAC services.")
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, ImportError, SSLValidationError, IOError, ValueError, TypeError, ConnectionError) as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
