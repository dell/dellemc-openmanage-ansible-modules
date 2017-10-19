#! /usr/bin/python
# _*_ coding: utf-8 _*_

#
# Dell EMC OpenManage Ansible Modules
#
# Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved.
# Dell, EMC, and other trademarks are trademarks of Dell Inc. or its
# subsidiaries. Other trademarks may be trademarks of their respective owners.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: dellemc_idrac_system
short_description: Configure System attributes
version_added: "2.3"
description:
    - Configure following System attributes:
      - System Topology
options:
  idrac_ip:
    required: False
    description:
      - iDRAC IP Address
    default: None
  idrac_user:
    required: False
    description:
      - iDRAC user name
    default: None
  idrac_pwd:
    required: False
    description:
      - iDRAC user password
    default: None
  idrac_port:
    required: False
    description:
      - iDRAC port
    default: None
  share_name:
    required: True
    description:
      - Network file share
  share_user:
    required: True
    description:
      - Network share user in the format 'user@domain' if user is part of a domain else 'user'
  share_pwd:
    required: True
    description:
      - Network share user password
  share_mnt:
    required: True
    description:
      - Local mount path of the network file share with read-write permission for ansible user
  system_topology:
    required: False
    description:
      - Dictionary of all the topology variables for the system:
          "data_center_name" (Data Center Name)
          "aisle_name" (Aisle Name)
          "rack_name" (Rack Name)
          "rack_slot" (Rack Slot)
          "slot_name" (Slot Name)
          "room_name" (Room Name)
    default: None
    type: 'dict'

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
'''

EXAMPLES = '''
# Configure System Topology
- name: Configure System Topology such as DC name, Rack name, Slot name etc.
    dellemc_idrac_location:
      idrac_ip:     "192.168.1.1"
      idrac_user:   "root"
      idrac_pwd:    "calvin"
      share_name:   "\\\\192.168.10.10\\share\\"
      share_user:   "user1"
      share_pwd:    "password"
      share_mnt:    "/mnt/share"
      system_topology:
        data_center_name: "Data Center 1"
        aisle_name:   "Aisle 1"
        rack_name:    "Rack 1"
        rack_slot:    "Slot 1"
        room_name:    "Room 1"
'''

RETURN = '''
ElapsedTimeSinceCompletion:
  type: str
  description: Time elapsed since completion of the JOB
  returned: always
  sample: "0"
InstanceID:
  type: str
  description: 
  returned: always
  sample: "JID_064113236770"
JobStartTime:
  type: str
  description: Start time of the lifecycle controller JOB
  returned: always
  sample: "NA"
JobStatus:
  type: str
  description:
  returned: always
  sample: "Completed"
JobUntilTime:
  type: str
  description: Until time of the job
  returned: always
  sample: "NA"
Message:
  type: str
  description: The message text that is displayed to the user or logged as a result of the event
  returned: always
  sample: "Successfully imported and applied system configuration XML file"
MessageArguments:
  type: str
  description: Message arguments for the lifecycle job
  returned: always
  sample: "NA"
MessageID:
  type: str
  description: Unique alphanumeric identifier of the event 
  returned: always
  sample: "SYS053"
Name:
  type: str
  description: 
  returned: always
  sample: "Import Configurtion"
PercentComplete:
  type: str
  description: Percent completion of the JOB
  returned: always
  sample: "100"
Status:
  type: str
  description: Status
  returned: always
  sample: "Success"
file:
  type: str
  description: Server configuration profile (SCP) file path 
  returned: always
  sample: "\\\\192.168.10.10\\Share\\scpO3ZxL1.xml1"
retval:
  type: bool
  description: Return value
  returned: always
  sample: true

'''

import traceback
from ansible.module_utils.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule


def setup_idrac_server_topology(idrac, module):
    """
    Setup iDRAC System Location

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    idrac.config_mgr._sysconfig.System.ServerTopology.\
        DataCenterName_ServerTopology = module.params['server_topology'].get('data_center_name')
    idrac.config_mgr._sysconfig.System.ServerTopology.\
        AisleName_ServerTopology = module.params['server_topology'].get('aisle_name')
    idrac.config_mgr._sysconfig.System.ServerTopology.\
        RackName_ServerTopology = module.params['server_topology'].get('rack_name')
    idrac.config_mgr._sysconfig.System.ServerTopology.\
        RackSlot_ServerTopology = module.params['server_topology'].get('rack_slot')
    idrac.config_mgr._sysconfig.System.ServerTopology.\
        RoomName_ServerTopology = module.params['server_topology'].get('room_name')


def setup_idrac_system_attr(idrac, module):
    """
    Setup iDRAC system attributes

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    error = False

    try:
        if module.params.get('server_topology'):
            setup_idrac_server_topology(idrac, module)

        msg['changed'] = idrac.config_mgr._sysconfig.is_changed()

        if module.check_mode:
            # since it is running in check mode, reject the changes
            idrac.config_mgr._sysconfig.reject()
        else:
            msg['msg'] = idrac.config_mgr.apply_changes()

            if "Status" in msg['msg'] and msg['msg']['Status'] != "Success":
                msg['failed'] = True
                msg['changed'] = False

    except Exception as err:
        error = True
        msg['msg'] = "Error: %s" % str(err)
        msg['exception'] = traceback.format_exc()
        msg['failed'] = True

    return msg, error

# Main
def main():

    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC handle
            idrac=dict(required=False, type='dict'),

            # iDRAC Credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_pwd=dict(required=True, type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Network File Share
            share_name=dict(required=True, type='str'),
            share_user=dict(required=True, type='str'),
            share_pwd=dict(required=True, type='str', no_log=True),
            share_mnt=dict(required=True, type='path'),

            server_topology=dict(required=False, default=None, type='dict'),
            data_center_name=dict(required=False, default=None, type='str'),
            aisle_name=dict(required=False, default=None, type='str'),
            rack_name=dict(required=False, default=None, type='str'),
            rack_slot=dict(required=False, default=None, type='str'),
            room_name=dict(required=False, default=None, type='str')
        ),
        supports_check_mode=True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    # Setup network share as local mount
    if not idrac_conn.setup_nw_share_mount():
        module.fail_json(msg="Failed to setup network share local mount point")

    # Setup iDRAC system attributes
    msg, error = setup_idrac_system_attr(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if error:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()
