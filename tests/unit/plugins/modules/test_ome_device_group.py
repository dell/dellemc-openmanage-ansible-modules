# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.3.0
# Copyright (C) 2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible_collections.dellemc.openmanage.plugins.modules import ome_device_group
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants, \
    AnsibleFailJSonException

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_device_group.'


@pytest.fixture
def ome_connection_mock_for_device_group(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    ome_connection_mock_obj.get_all_report_details.return_value = {"report_list": []}
    return ome_connection_mock_obj


class TestOMEDeviceGroup(FakeAnsibleModule):
    module = ome_device_group

    def test_get_group_id(self, ome_connection_mock_for_device_group, ome_response_mock):
        f_module = self.get_module_mock(params={"name": "Storage Services",
                                                "device_ids": [25011], "device_service_tags": []})
        ome_response_mock.json_data = {"value": []}
        with pytest.raises(Exception) as exc:
            self.module.get_group_id(ome_connection_mock_for_device_group, f_module)
        assert exc.value.args[0] == "Unable to complete the operation because the entered " \
                                    "target group name 'Storage Services' is invalid."
        ome_response_mock.json_data = {"value": [{"Id": 25011, "CreatedBy": "user"}]}
        resp = self.module.get_group_id(ome_connection_mock_for_device_group, f_module)
        assert resp == 25011

    def test_get_device_id(self, ome_connection_mock_for_device_group):
        report_list = [{"Id": 25011, "DeviceServiceTag": "SEFRG2"}, {"Id": 25012, "DeviceServiceTag": "SEFRG3"}]
        ome_connection_mock_for_device_group.get_all_report_details.return_value = {"report_list": report_list}
        f_module = self.get_module_mock(params={"name": "Storage Services",
                                                "device_ids": [25011, 25012]})
        device_list, key = self.module.get_device_id(ome_connection_mock_for_device_group, f_module)
        assert device_list == [25011, 25012]
        assert key == "Id"
        f_module = self.get_module_mock(params={"name": "Storage Services",
                                                "device_service_tags": ["SEFRG2", "SEFRG3"]})
        device_list, key = self.module.get_device_id(ome_connection_mock_for_device_group, f_module)
        assert device_list == [25011, 25012]
        assert key == "DeviceServiceTag"

        f_module = self.get_module_mock(params={"name": "Storage Services",
                                                "device_ids": [25011, 25000]})
        with pytest.raises(Exception) as exc:
            self.module.get_device_id(ome_connection_mock_for_device_group, f_module)
        assert exc.value.args[0] == "Unable to complete the operation because the entered target " \
                                    "device id(s) '25000' are invalid."

    def test_add_member_to_group(self, ome_connection_mock_for_device_group, ome_response_mock):
        report_list = [{"Id": 25011, "DeviceServiceTag": "SEFRG2"}]
        ome_connection_mock_for_device_group.get_all_report_details.return_value = {"report_list": report_list}
        f_module = self.get_module_mock(params={"name": "Storage Services",
                                                "device_ids": [25011]})
        ome_response_mock.status_code = 204
        ome_response_mock.success = True
        with pytest.raises(Exception) as exc:
            self.module.add_member_to_group(f_module, ome_connection_mock_for_device_group,
                                            1, [25011], "Id")
        assert exc.value.args[0] == "Requested device(s) '25011' are already present in the group."

        f_module.check_mode = True
        with pytest.raises(Exception) as exc:
            self.module.add_member_to_group(f_module, ome_connection_mock_for_device_group,
                                            1, [25011], "Id")
        assert exc.value.args[0] == "No changes found to commit!"

        f_module.check_mode = False
        report_list = [{"Id": 25013, "DeviceServiceTag": "SEFRG4"}, {"Id": 25014, "DeviceServiceTag": "SEFRG5"}]
        ome_connection_mock_for_device_group.get_all_report_details.return_value = {"report_list": report_list}
        resp = self.module.add_member_to_group(f_module, ome_connection_mock_for_device_group,
                                               1, [25011, 25012], "Id")
        assert resp.status_code == 204

        f_module.check_mode = True
        with pytest.raises(Exception) as exc:
            self.module.add_member_to_group(f_module, ome_connection_mock_for_device_group,
                                            1, [25011, 25012], "Id")
        assert exc.value.args[0] == "Changes found to commit!"

    def test_main_exception(self, ome_connection_mock_for_device_group, mocker,
                            ome_response_mock, ome_default_args):
        ome_default_args.update({"name": "Storage Services", "device_ids": [25011, 25012]})
        ome_response_mock.status_code = 204
        ome_response_mock.success = True
        mocker.patch(MODULE_PATH + 'get_group_id', return_value=1)
        mocker.patch(MODULE_PATH + 'get_device_id', return_value=[25011, 25012])
        mocker.patch(MODULE_PATH + 'add_member_to_group', return_value=ome_response_mock)
        result = self._run_module(ome_default_args)
        assert result['msg'] == "Successfully added member(s) to the device group."
        # with pytest.raises(Exception) as exc:
        #     self._run_module(ome_default_args)
        # assert exc.value.args[0]['msg'] == "state is present but the device_service_tags value is missing."
        # self._run_module(ome_default_args)
        # assert report["msg"] == "Successfully added member(s) to the device group."
        # assert report["changed"] is True

        # ome_default_args.update({"name": "Storage Services", "state": "absent"})
        # with pytest.raises(Exception) as exc:
        #     self._run_module(ome_default_args)
        # assert exc.value.args[0]['msg'] == "Currently, this feature is not supported."
