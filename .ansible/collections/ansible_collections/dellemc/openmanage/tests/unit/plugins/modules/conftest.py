# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.0.0
# Copyright (C) 2019-2022 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible.module_utils import basic
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.utils import exit_json, \
    fail_json, AnsibleFailJson, AnsibleExitJson
from unittest.mock import MagicMock

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
MODULE_UTIL_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.'


@pytest.fixture(autouse=True)
def module_mock(mocker):
    return mocker.patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json)


@pytest.fixture
def ome_connection_mock(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'ome_device_info.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


@pytest.fixture
def ome_response_mock(mocker):
    set_method_result = {'json_data': {}}
    response_class_mock = mocker.patch(MODULE_UTIL_PATH + 'ome.OpenURLResponse', return_value=set_method_result)
    response_class_mock.success = True
    response_class_mock.status_code = 200
    return response_class_mock


@pytest.fixture
def redfish_response_mock(mocker):
    set_method_result = {'json_data': {}}
    response_class_mock = mocker.patch(MODULE_UTIL_PATH + 'redfish.OpenURLResponse', return_value=set_method_result)
    response_class_mock.success = True
    response_class_mock.status_code = 200
    return response_class_mock


@pytest.fixture
def ome_default_args():
    default_args = {'hostname': 'XX.XX.XX.XX', 'username': 'username', 'password': 'password', "ca_path": "/path/ca_bundle"}
    return default_args


@pytest.fixture
def omevv_default_args():
    default_args = {'hostname': 'XX.XX.XX.XX', 'vcenter_uuid': 'vcenter_uuid', 'vcenter_username': 'vcenter_username',
                    'vcenter_password': 'vcenter_password', "ca_path": "/path/ca_bundle"}
    return default_args


@pytest.fixture
def idrac_default_args():
    default_args = {"idrac_ip": "idrac_ip", "idrac_user": "idrac_user", "idrac_password": "idrac_password",
                    "ca_path": "/path/to/ca_cert.pem"}
    return default_args


@pytest.fixture
def redfish_default_args():
    default_args = {'baseuri': 'XX.XX.XX.XX', 'username': 'username', 'password': 'password',
                    "ca_path": "/path/to/ca_cert.pem"}
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
