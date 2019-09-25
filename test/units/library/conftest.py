# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0
# Copyright (C) 2019 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

import pytest
from ansible.module_utils import basic
from units.modules.utils import set_module_args, exit_json, fail_json
from units.modules.utils import AnsibleFailJson, AnsibleExitJson
from units.compat.mock import MagicMock


@pytest.fixture(autouse=True)
def module_mock(mocker):
    return mocker.patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json)


@pytest.fixture
def ome_connection_mock(mocker,ome_response_mock):
    connection_class_mock = mocker.patch('ansible.modules.remote_management.dellemc.ome_device_info.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return connection_class_mock


@pytest.fixture
def ome_response_mock(mocker):
    response_class_mock = mocker.patch('ansible.module_utils.remote_management.dellemc.ome.OpenURLResponse')
    return response_class_mock


@pytest.fixture
def ome_default_args():
    default_args = {'hostname': '192.168.0.1', 'username': 'username', 'password': 'password'}
    return default_args

@pytest.fixture
def fake_ansible_module_mock():
    module = MagicMock()
    module.params = {}
    module.fail_json = AnsibleFailJson()
    module.exit_json = AnsibleExitJson()
    return module