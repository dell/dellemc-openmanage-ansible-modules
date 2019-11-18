# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1
# Copyright (C) 2019 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

from __future__ import absolute_import

import pytest
from ansible.modules.remote_management.dellemc import idrac_os_deployment
from units.modules.remote_management.dellemc.common import FakeAnsibleModule, Constants
from ansible.module_utils.remote_management.dellemc.dellemc_idrac import iDRACConnection
from units.compat.mock import MagicMock
from units.modules.utils import set_module_args

from units.modules.utils import set_module_args, exit_json, fail_json, AnsibleFailJson, AnsibleExitJson
from ansible.module_utils import basic
from units.compat.mock import PropertyMock
import json


class TestOsDeployment(FakeAnsibleModule):
    module = idrac_os_deployment

    @pytest.fixture
    def default_idrac_args(self):
        return {"idrac_ip":"idrac_ip", "idrac_user":"idrac_user", "idrac_password":"idrac_password"}

    @pytest.fixture
    def idrac_connection_mock(self, mocker,idrac_mock):
        idrac_connection_class_mock = mocker.patch('ansible.modules.remote_management.dellemc.idrac_os_deployment.iDRACConnection')
        #idrac_connection_class_mock.return_value = idrac_mock
        idrac_connection_class_mock.return_value.__enter__.return_value = idrac_mock
        return idrac_connection_class_mock

    @pytest.fixture
    def idrac_mock(self, mocker):
        sdkinfra_obj = mocker.patch('ansible.module_utils.remote_management.dellemc.dellemc_idrac.sdkinfra')
        obj = MagicMock()
        sdkinfra_obj.get_driver.return_value = obj
        return sdkinfra_obj

    @pytest.fixture
    def omsdk_mock(self, mocker):
        mocker.patch('ansible.module_utils.remote_management.dellemc.dellemc_idrac.UserCredentials')
        mocker.patch('ansible.module_utils.remote_management.dellemc.dellemc_idrac.WsManOptions')

    @pytest.fixture
    def fileonshare_mock(self, mocker):
        share_mock = mocker.patch('ansible.modules.remote_management.dellemc.idrac_os_deployment.FileOnShare',return_value=MagicMock())
        return share_mock


    @pytest.fixture
    def minutes_to_cim_format_mock(self, mocker):
        validate_device_inputs_mock = mocker.patch('ansible.modules.remote_management.dellemc.idrac_os_deployment.minutes_to_cim_format')
        validate_device_inputs_mock.return_value = "time"


    @pytest.mark.parametrize("expose_duration_val", ["abc",None,"",1.5,{"abc":1},[110,210,300],[120]])
    def test_main_failure_case_01(self,expose_duration_val,default_idrac_args, module_mock):
        """when invalid value for expose_durationis given """
        default_idrac_args.update({"iso_image":"iso_image"})
        default_idrac_args.update({"expose_duration": expose_duration_val})
        result = self._run_module_with_fail_json(default_idrac_args)

    def test_main_failure_case_02(self, module_mock,default_idrac_args):
        """when required arg iso_image is not passed"""
        default_idrac_args.update({"iso_image":"iso_image"})
        result = self._run_module_with_fail_json(default_idrac_args)

    def test_main_failure_case_03(self, module_mock,default_idrac_args):
        """when invalid ansible option is given"""
        default_idrac_args.update({"iso_image":"iso_image", "invalid_key":"val"})
        result = self._run_module_with_fail_json(default_idrac_args)

    def test_main_run_boot_to_network_iso_success_case(self, idrac_connection_mock,idrac_mock, module_mock, fileonshare_mock, omsdk_mock,minutes_to_cim_format_mock):
        idrac_connection_mock.return_value.__enter__.return_value = idrac_mock
        idrac_mock.config_mgr.boot_to_network_iso.return_value = {"Status": "Success"}
        params = {"idrac_ip":"idrac_ip", "idrac_user":"idrac_user", "idrac_password":"idrac_password",
                  "share_name" : "dummy_share_name", "share_password":"dummy_share_password",
                                   "iso_image":"dummy_iso_image","expose_duration":"100"}
        set_module_args(params)
        result = self._run_module(params)
        assert result == {'changed': True, 'msg': {'Status': 'Success'}}

    def test_main_run_boot_to_network_iso_fleonshare_failure_case(self, idrac_connection_mock, idrac_mock, module_mock, fileonshare_mock, omsdk_mock,
                                                       minutes_to_cim_format_mock):
        idrac_connection_mock.return_value.__enter__.return_value = idrac_mock
        fileonshare_mock.side_effect = RuntimeError("Error in Runtime")
        params = {"idrac_ip": "idrac_ip", "idrac_user": "idrac_user", "idrac_password": "idrac_password",
                  "share_name": "invalid_share_name", "share_password": "dummy_share_password",
                  "iso_image": "dummy_iso_image", "expose_duration": "100"}
        set_module_args(params)
        result = self._run_module_with_fail_json(params)
        assert result == {'failed': True, 'msg': 'Error in Runtime'}

    def test_main_run_boot_to_network_iso_failure_case(self, idrac_connection_mock,idrac_mock, module_mock, fileonshare_mock, omsdk_mock,minutes_to_cim_format_mock):
        idrac_mock.config_mgr.boot_to_network_iso.return_value = {"Status": "Failure"}
        params = {"idrac_ip":"idrac_ip", "idrac_user":"idrac_user", "idrac_password":"idrac_password",
                  "share_name" : "dummy_share_name", "share_password":"dummy_share_password",
                                   "iso_image":"dummy_iso_image","expose_duration":"100"}
        set_module_args(params)
        result = self._run_module_with_fail_json(params)
        assert result['failed'] is True

    def test_minutes_to_cim_format_success_case_01(self, module_mock):
        result = self.module.minutes_to_cim_format(module_mock, 180)
        assert result == '00000000030000.000000:000'

    def test_minutes_to_cim_format_success_case_02(self, module_mock):
        result = self.module.minutes_to_cim_format(module_mock, 0)
        assert result == '00000000000000.000000:000'

    def test_minutes_to_cim_format_failure_case(self):
        fmodule = self.get_module_mock()
        with pytest.raises(Exception) as exc:
            set_module_args({})
            self.module.minutes_to_cim_format(fmodule, -1)
        assert exc.value.args[0] == "Invalid value for ExposeDuration."

    # def test_minutes_to_cim_format_success_case_03(self,fake_ansible_module_mock):
    #     with pytest.raises(Exception) as exc:
    #         self.module.minutes_to_cim_format(fake_ansible_module_mock, -1)
    #     pdb.set_trace()
    #     assert exc.value.args[0] == "Unable to parse the expose duration."








