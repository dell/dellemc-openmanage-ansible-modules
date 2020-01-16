# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0
# Copyright (C) 2019 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from ansible.module_utils import basic
from units.modules.utils import set_module_args, exit_json, fail_json
from units.modules.utils import AnsibleFailJson, AnsibleExitJson
from units.compat.mock import MagicMock
import json


@pytest.fixture(autouse=True)
def module_mock(mocker):
    return mocker.patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json)


@pytest.fixture
def ome_connection_mock(mocker, ome_response_mock):
    connection_class_mock = mocker.patch('ansible.modules.remote_management.dellemc.ome_device_info.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


@pytest.fixture
def ome_response_mock(mocker):
    set_method_result = {'json_data': {}}
    response_class_mock = mocker.patch('ansible.module_utils.remote_management.dellemc.ome.OpenURLResponse', return_value=set_method_result)
    response_class_mock.success = True
    response_class_mock.status_code = 200
    return response_class_mock


@pytest.fixture
def redfish_response_mock(mocker):
    set_method_result = {'json_data': {}}
    response_class_mock = mocker.patch('ansible.module_utils.remote_management.dellemc.redfish.OpenURLResponse', return_value=set_method_result)
    response_class_mock.success = True
    response_class_mock.status_code = 200
    return response_class_mock


@pytest.fixture
def ome_default_args():
    default_args = {'hostname': '192.168.0.1', 'username': 'username', 'password': 'password'}
    return default_args


@pytest.fixture
def redfish_default_args():
    default_args = {'baseuri': '192.168.0.1', 'username': 'username', 'password': 'password'}
    return default_args


@pytest.fixture
def fake_ansible_module_mock():
    module = MagicMock()
    module.params = {}
    module.fail_json = AnsibleFailJson()
    module.exit_json = AnsibleExitJson()
    return module


@pytest.fixture
def default_ome_args():
    return {"hostname": "hostname", "username": "username", "password": "password"}
