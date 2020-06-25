#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0.14
# Copyright (C) 2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import

import json
import pytest
from ansible.modules.remote_management.dellemc import idrac_firmware
from units.modules.remote_management.dellemc.common import FakeAnsibleModule, Constants
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from units.compat.mock import MagicMock, patch, Mock
from ansible.module_utils.six.moves.urllib.parse import urlparse
from units.modules.utils import set_module_args, exit_json, fail_json, AnsibleFailJson, AnsibleExitJson
from units.compat.mock import PropertyMock
from io import StringIO
from ansible.module_utils._text import to_text
from units.compat.mock import patch, mock_open
from ansible.module_utils.six.moves.urllib.parse import urlparse, ParseResult
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")


class TestidracFirmware(FakeAnsibleModule):
    module = idrac_firmware

    @pytest.fixture
    def idrac_firmware_update_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.update_mgr = idrac_obj
        idrac_obj.update_from_repo = Mock(return_value={"update_status": {"job_details": {"Data":
                                                                                {"StatusCode": 200,
                                                                               "body": {"PackageList": [{}]}}}}})
        idrac_obj.update_from_repo_url = Mock(return_value={"job_details": {"Data": {"StatusCode": 200,
                                                                               "body": {"PackageList": [{}]}}}})
        return idrac_obj

    @pytest.fixture
    def idrac_firmware_job_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.job_mgr = idrac_obj
        idrac_obj.get_job_status_redfish = Mock(return_value={"update_status": {"job_details": {"Data":
                                                                                                {"StatusCode": 200,
                                                                                                "body": {
                                                                                                "PackageList": [
                                                                                                {}]}}}}})
        idrac_obj.job_wait = Mock(return_value="21543")
        return idrac_obj

    @pytest.fixture
    def re_match_mock(self, mocker):
        try:
            re_mock = mocker.patch(
                'ansible.modules.remote_management.dellemc.idrac_firmware.re')
        except AttributeError:
            re_mock = MagicMock()
        obj = MagicMock()
        re_mock.match.group.return_value = obj
        return "3.30"

    @pytest.fixture
    def ET_convert_mock(self, mocker):
        try:
            ET_mock = mocker.patch(
                'ansible.modules.remote_management.dellemc.idrac_firmware.ET')
        except AttributeError:
            ET_mock = MagicMock()
        obj = MagicMock()
        ET_mock.fromstring.return_value = obj
        return ET_mock

    @pytest.fixture
    def fileonshare_idrac_firmware_mock(self, mocker):
        share_mock = mocker.patch('ansible.modules.remote_management.dellemc.idrac_firmware.FileOnShare',
                                  return_value=MagicMock())
        return share_mock

    @pytest.fixture
    def idrac_connection_firmware_mock(self, mocker, idrac_firmware_update_mock):
        idrac_conn_class_mock = mocker.patch('ansible.modules.remote_management.dellemc.'
                                             'idrac_firmware.iDRACConnection',
                                             return_value=idrac_firmware_update_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_firmware_update_mock
        return idrac_firmware_update_mock

    @pytest.fixture
    def idrac_connection_firmware_redfish_mock(self, mocker, idrac_firmware_job_mock):
        idrac_conn_class_mock = mocker.patch('ansible.modules.remote_management.dellemc.'
                                             'idrac_firmware.iDRACRedfishAPI',
                                             return_value=idrac_firmware_job_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_firmware_job_mock
        return idrac_firmware_job_mock

    def test_main_idrac_firmware_success_Case(self, idrac_connection_firmware_mock,idrac_default_args, mocker):
        idrac_default_args.update({"share_name": "sharename", "catalog_file_name": "Catalog.xml",
                                   "share_user": "sharename", "share_password": "sharepswd", "share_mnt": "sharmnt",
                                   "reboot": True, "job_wait": True})
        message = {"Status": "Success", "update_msg": "Successfully updated the firmware.", "update_status": "Success",
                   'changed': False}
        mocker.patch('ansible.modules.remote_management.dellemc.idrac_firmware.update_firmware',
                     return_value=message)
        result = self._run_module(idrac_default_args)
        assert result == {'msg': 'Successfully updated the firmware.', 'update_status': 'Success', 'changed': False}

    @pytest.mark.parametrize("exc_type", [RuntimeError, URLError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError])
    def test_main_idrac_firmware_exception_handling_case(self, exc_type, mocker, idrac_default_args,
                                                         idrac_connection_firmware_mock):
        idrac_default_args.update({"share_name": "sharename", "catalog_file_name": "Catalog.xml",
                                   "share_user": "sharename", "share_password": "sharepswd", "share_mnt": "sharmnt",
                                   "reboot": True, "job_wait": True})
        mocker.patch('ansible.modules.remote_management.dellemc.'
                     'idrac_firmware._validate_catalog_file', return_value="catalog_file_name")
        mocker.patch('ansible.modules.remote_management.dellemc.'
                     'idrac_firmware.update_firmware', side_effect=exc_type('test'))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True

    def test_main_HTTPError_case(self, idrac_connection_firmware_mock, idrac_default_args, mocker):
        idrac_default_args.update({"share_name": "sharename", "catalog_file_name": "Catalog.xml",
                                   "share_user": "sharename", "share_password": "sharepswd", "share_mnt": "sharmnt",
                                   "reboot": True, "job_wait": True})
        json_str = to_text(json.dumps({"data": "out"}))
        mocker.patch('ansible.modules.remote_management.dellemc.'
                     'idrac_firmware.update_firmware', side_effect=HTTPError('http://testhost.com',
                                                                             400, 'http error message',
                                     {"accept-type": "application/json"}, StringIO(json_str)))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True

    def test_update_firmware_success_case01(self, idrac_connection_firmware_mock, idrac_default_args, mocker,
                                          re_match_mock):
        idrac_default_args.update({"share_name": "mhttps://downloads.dell.com", "catalog_file_name": "Catalog.xml",
                                   "share_user": "UserName", "share_password": "sharepswd", "share_mnt": "shrmnt",
                                   "reboot": True, "job_wait": True, "ignore_cert_warning": True, "apply_update": True})
        mocker.patch("ansible.modules.remote_management.dellemc.idrac_firmware.update_firmware_url",
                     return_value=({"update_status": {"job_details": {"Data": {"StatusCode": 200,
                                                                               "body": {"PackageList": [{}]}}}}},
                                   {"job_details": {"Data": {"StatusCode": 200,
                                   "body": {"PackageList": [{}]}}}}))

        f_module = self.get_module_mock(params=idrac_default_args)
        idrac_connection_firmware_mock.match.return_value = "2.70"
        idrac_connection_firmware_mock.ServerGeneration.return_value = "13"
        idrac_connection_firmware_mock.update_mgr.update_from_repo.return_value = {"job_details": {"Data": {"StatusCode": 200,
                                   "body": {"PackageList1": [{}]}}}}
        result = self.module.update_firmware(idrac_connection_firmware_mock, f_module)
        assert result == {'update_status': {'job_details':
                            {'Data': {'body': {'PackageList1': [{}]}, 'StatusCode': 200}}},
                          'changed': False, 'update_msg': 'Successfully triggered the job to update the firmware.'}

    def test_update_firmware_success_case02(self, idrac_connection_firmware_mock, idrac_default_args, mocker,
                                          re_match_mock):
        idrac_default_args.update({"share_name": "mhttps://downloads.dell.com", "catalog_file_name": "Catalog.xml",
                                   "share_user": "UserName", "share_password": "sharepswd", "share_mnt": "shrmnt",
                                   "reboot": True, "job_wait": True, "ignore_cert_warning": True, "apply_update": True})
        mocker.patch("ansible.modules.remote_management.dellemc.idrac_firmware.update_firmware_url",
                     return_value=({"update_status": {"job_details": {"data": {"StatusCode": 200,
                                                                               "body": {"PackageList": [{}]}}}}},
                                   {"job_details": {"Data": {"StatusCode": 200,
                                   "body": {"PackageList": [{}]}}}}))

        mocker.patch("ansible.modules.remote_management.dellemc.idrac_firmware._convert_xmltojson", return_value=
        ({
            "BaseLocation": None,
            "ComponentID": "18981",
            "ComponentType": "APAC",
            "Criticality": "3",
            "DisplayName": "Dell OS Driver Pack",
            "JobID": None,
            "PackageName": "Drivers-for-OS-Deployment_Application_X0DW6_WN64_19.10.12_A00.EXE",
            "PackagePath": "FOLDER05902898M/1/Drivers-for-OS-Deployment_Application_X0DW6_WN64_19.10.12_A00.EXE",
            "PackageVersion": "19.10.12",
            "RebootType": "NONE",
            "Target": "DCIM:INSTALLED#802__DriverPack.Embedded.1:LC.Embedded.1"
        }, True))

        f_module = self.get_module_mock(params=idrac_default_args)
        idrac_connection_firmware_mock.match.return_value = "2.70"
        idrac_connection_firmware_mock.ServerGeneration.return_value = "13"
        idrac_connection_firmware_mock.update_mgr.update_from_repo.return_value = {"job_details": {"Data":
                                                                                    {"StatusCode": 200,
                                                                                   "body": {"PackageList": [{}]}}}}
        result = self.module.update_firmware(idrac_connection_firmware_mock, f_module)
        assert result == {'changed': False, 'update_msg': 'Successfully triggered the job to update the firmware.',
                          'update_status': {'job_details': {'Data': {'StatusCode': 200,
                          'body': {'PackageList': {'BaseLocation': None, 'ComponentID': '18981',
                          'ComponentType': 'APAC', 'Criticality': '3', 'DisplayName': 'Dell OS Driver Pack',
                          'JobID': None, 'PackageName':
                          'Drivers-for-OS-Deployment_Application_X0DW6_WN64_19.10.12_A00.EXE',
                          'PackagePath':
                        'FOLDER05902898M/1/Drivers-for-OS-Deployment_Application_X0DW6_WN64_19.10.12_A00.EXE',
                        'PackageVersion': '19.10.12', 'RebootType': 'NONE',
                        'Target': 'DCIM:INSTALLED#802__DriverPack.Embedded.1:LC.Embedded.1'}}}}}}

    def test_update_firmware_success_case03(self, idrac_connection_firmware_mock, idrac_default_args, mocker,
                                           re_match_mock):
        idrac_default_args.update({"share_name": "https://downloads.dell.com", "catalog_file_name": "Catalog.xml",
                                   "share_user": "UserName", "share_password": "sharepswd", "share_mnt": "shrmnt",
                                   "reboot": True, "job_wait": False, "ignore_cert_warning": True, "apply_update": True})
        mocker.patch("ansible.modules.remote_management.dellemc.idrac_firmware.update_firmware_url",
                     return_value=({"job_details": {"Data": {"StatusCode": 200, "body": {"PackageList": [{}]}}}},
                                   {"Data": {"StatusCode": 200,
                                   "body": {"PackageList": [{}]}}}))

        mocker.patch("ansible.modules.remote_management.dellemc.idrac_firmware._convert_xmltojson", return_value=
        ({
            "BaseLocation": None,
            "ComponentID": "18981",
            "ComponentType": "APAC",
            "Criticality": "3",
            "DisplayName": "Dell OS Driver Pack",
            "JobID": None,
            "PackageName": "Drivers-for-OS-Deployment_Application_X0DW6_WN64_19.10.12_A00.EXE",
            "PackagePath": "FOLDER05902898M/1/Drivers-for-OS-Deployment_Application_X0DW6_WN64_19.10.12_A00.EXE",
            "PackageVersion": "19.10.12",
            "RebootType": "NONE",
            "Target": "DCIM:INSTALLED#802__DriverPack.Embedded.1:LC.Embedded.1"
        }, True))

        f_module = self.get_module_mock(params=idrac_default_args)
        idrac_connection_firmware_mock.re_match_mock.group = Mock(return_value="3.30")
        idrac_connection_firmware_mock.ServerGeneration = "14"
        result = self.module.update_firmware(idrac_connection_firmware_mock, f_module)
        assert result["changed"] is False
        assert result["update_msg"] == "Successfully triggered the job to update the firmware."

    def test_update_firmware_status_success_case01(self, idrac_connection_firmware_mock, idrac_default_args, mocker,
                                           re_match_mock):
        idrac_default_args.update({"share_name": "mhttps://downloads.dell.com", "catalog_file_name": "Catalog.xml",
                                   "share_user": "UserName", "share_password": "sharepswd", "share_mnt": "sharemnt",
                                   "reboot": True, "job_wait": True, "ignore_cert_warning": True, "apply_update": True})
        mocker.patch("ansible.modules.remote_management.dellemc.idrac_firmware.update_firmware_url",
                     return_value=({"update_status": {"job_details": {"data": {"StatusCode": 200,
                                                                               "body": {"PackageList": [{}]}}}}},
                                   {"job_details": {"Data": {"StatusCode": 200,
                                                             "body": {"PackageList": [{}]}}}}))

        mocker.patch("ansible.modules.remote_management.dellemc.idrac_firmware._convert_xmltojson", return_value=
        {
            "BaseLocation": None,
            "ComponentID": "18981",
            "ComponentType": "APAC",
            "Criticality": "3",
            "DisplayName": "Dell OS Driver Pack",
            "JobID": None,
            "PackageName": "Drivers-for-OS-Deployment_Application_X0DW6_WN64_19.10.12_A00.EXE",
            "PackagePath": "FOLDER05902898M/1/Drivers-for-OS-Deployment_Application_X0DW6_WN64_19.10.12_A00.EXE",
            "PackageVersion": "19.10.12",
            "RebootType": "NONE",
            "Target": "DCIM:INSTALLED#802__DriverPack.Embedded.1:LC.Embedded.1"
        })

        f_module = self.get_module_mock(params=idrac_default_args)
        idrac_connection_firmware_mock.match.return_value = "2.70"
        idrac_connection_firmware_mock.ServerGeneration.return_value = "13"
        idrac_connection_firmware_mock.update_mgr.update_from_repo.return_value = {"job_details": {"Data": {
                                                                                    "StatusCode": 200,
                                                                                    "body": {}}, "Status": "Success"},
                                                                                   "Status": "Success"}
        result = self.module.update_firmware(idrac_connection_firmware_mock, f_module)
        assert result == {'changed': False,
           'update_msg': 'Successfully triggered the job to update the firmware.',
           'update_status': {'Status': 'Success',
                             'job_details': {'Data': {'StatusCode': 200, 'body': {}},
                                             'Status': 'Success'}}}

    def test_update_firmware_status_failed_case01(self, idrac_connection_firmware_mock, idrac_default_args, mocker,
                                           re_match_mock):
        idrac_default_args.update({"share_name": "mhttps://downloads.dell.com", "catalog_file_name": "Catalog.xml",
                                   "share_user": "UserName", "share_password": "sharepswd", "share_mnt": "sharemnt",
                                   "reboot": True, "job_wait": True, "ignore_cert_warning": True, "apply_update": True})
        mocker.patch("ansible.modules.remote_management.dellemc.idrac_firmware.update_firmware_url",
                     return_value=({"update_status": {"job_details": {"data": {"StatusCode": 200,
                                                                               "body": {"PackageList": [{}]}}}}},
                                   {"job_details": {"Data": {"StatusCode": 200,
                                                             "body": {"PackageList": [{}]}}}}))

        mocker.patch("ansible.modules.remote_management.dellemc.idrac_firmware._convert_xmltojson", return_value=
        {
            "BaseLocation": None,
            "ComponentID": "18981",
            "ComponentType": "APAC",
            "Criticality": "3",
            "DisplayName": "Dell OS Driver Pack",
            "JobID": None,
            "PackageName": "Drivers-for-OS-Deployment_Application_X0DW6_WN64_19.10.12_A00.EXE",
            "PackagePath": "FOLDER05902898M/1/Drivers-for-OS-Deployment_Application_X0DW6_WN64_19.10.12_A00.EXE",
            "PackageVersion": "19.10.12",
            "RebootType": "NONE",
            "Target": "DCIM:INSTALLED#802__DriverPack.Embedded.1:LC.Embedded.1"
        })

        f_module = self.get_module_mock(params=idrac_default_args)
        idrac_connection_firmware_mock.match.return_value = "2.70"
        idrac_connection_firmware_mock.ServerGeneration.return_value = "13"
        idrac_connection_firmware_mock.update_mgr.update_from_repo.return_value = {"job_details": {"Data": {
                                                                                    "StatusCode": 200,
                                                                                    "body": {}}, "Status": "Failed"},
                                                                                   "Status": "Failed"}
        with pytest.raises(Exception) as ex:
            self.module.update_firmware(idrac_connection_firmware_mock, f_module)
        assert "Failed to update firmware." == str(ex.value)

    def test__validate_catalog_file_case01(self, idrac_connection_firmware_mock, idrac_default_args):
        idrac_default_args.update({"catalog_file_name": ""})
        with pytest.raises(ValueError) as exc:
            self.module._validate_catalog_file("")
        assert exc.value.args[0] == 'catalog_file_name should be a non-empty string.'

    def test__validate_catalog_file_case02(self, idrac_connection_firmware_mock, idrac_default_args):
        idrac_default_args.update({"catalog_file_name": "Catalog.json"})
        with pytest.raises(ValueError) as exc:
            self.module._validate_catalog_file("Catalog.json")
        assert exc.value.args[0] == 'catalog_file_name should be an XML file.'

    def test__convert_xmltojson_case01(self, idrac_connection_firmware_mock, idrac_default_args, ET_convert_mock):
        idrac_default_args.update({"PackageList": [{
                     "BaseLocation": None,
                     "ComponentID": "18981",
                     "ComponentType": "APAC",
                     "Criticality": "3",
                     "DisplayName": "Dell OS Driver Pack",
                     "JobID": None,
                     "PackageName": "Drivers-for-OS-Deployment_Application_X0DW6_WN64_19.10.12_A00.EXE",
                     "PackagePath":
                                  "FOLDER05902898M/1/Drivers-for-OS-Deployment_Application_X0DW6_WN64_19.10.12_A00.EXE",
                     "PackageVersion": "19.10.12"}]})
        result = self.module._convert_xmltojson({"PackageList": [{"INSTANCENAME": {"PROPERTY": {"NAME": "abc"}}}]})
        assert result == ([], True)

    def test__convert_xmltojson_case02(self, idrac_connection_firmware_mock, idrac_default_args):
        idrac_default_args.update({"Data": {"StatusCode": 200, "body": {"PackageList": [{}]}}})
        packagelist = {"PackageList": "INSTANCENAME"}
        result = self.module._convert_xmltojson(packagelist)
        assert result == ('INSTANCENAME', False)

    def test__convert_xmltojson_case03(self, idrac_connection_firmware_mock, idrac_default_args):
        idrac_default_args.update({"Data": {"StatusCode": 200, "body": {"PackageList": [{}]}}})
        packagelist = {"PackageList": "INSTANCENAME"}
        result = self.module._convert_xmltojson(packagelist)
        assert result == ('INSTANCENAME', False)

    def test_get_jobid_success_case01(self, idrac_connection_firmware_mock, idrac_default_args, idrac_firmware_job_mock,
                                      idrac_connection_firmware_redfish_mock):
        idrac_default_args.update({"Location": "https://jobmnager/jid123"})
        idrac_firmware_job_mock.code = 202
        idrac_firmware_job_mock.Success = True
        idrac_connection_firmware_redfish_mock.update_mgr.headers.get().split().__getitem__().return_value = "jid123"
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.get_jobid(f_module, idrac_firmware_job_mock)
        assert result == idrac_connection_firmware_redfish_mock.headers.get().split().__getitem__()

    def test_get_jobid_fail_case01(self, idrac_connection_firmware_mock, idrac_default_args, idrac_firmware_job_mock):
        idrac_default_args.update({"Location": None})
        idrac_firmware_job_mock.code = 400
        idrac_firmware_job_mock.Success = False
        idrac_connection_firmware_mock.header.get().split().__getitem__().side_effects = "Location"
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as exc:
            self.module.get_jobid(f_module, idrac_firmware_job_mock)
        assert exc.value.args[0] == "Failed to update firmware."

    def test_update_firmware_url_success_case02(self, idrac_connection_firmware_mock, idrac_default_args,
                                              mocker, idrac_connection_firmware_redfish_mock):
        idrac_default_args.update({"share_name": "http://downloads.dell.com", "catalog_file_name": "catalog.xml",
                                   "share_user": "shareuser", "share_password": "sharepswd", "share_mnt": "sharmnt",
                                   "reboot": True, "job_wait": False, "ignore_cert_warning": True,
                                   "share_type": "http", "idrac_ip": "idrac_ip", "idrac_user": "idrac_user",
                                   "idrac_password": "idrac_password", "idrac_port": 443})
        mocker.patch("ansible.modules.remote_management.dellemc.idrac_firmware.get_jobid", return_value="23451")

        mocker.patch("ansible.modules.remote_management.dellemc.idrac_firmware.urlparse",
                     return_value=ParseResult(scheme='http', netloc='downloads.dell.com', path='/%7Eguido/Python.html',
                     params='', query='', fragment=''))
        mocker.patch("socket.gethostbyname", return_value="downloads.dell.com")
        f_module = self.get_module_mock(params=idrac_default_args)
        idrac_connection_firmware_mock.use_redfish = False
        idrac_connection_firmware_redfish_mock.get_job_status_redfish = "Status"
        idrac_connection_firmware_redfish_mock.update_mgr.job_mgr.job_wait.return_value = "12345"
        idrac_connection_firmware_mock.update_mgr.update_from_repo_url.return_value = {"update_status": {"job_details":
                                                                                    {"data": {"StatusCode": 200,
                                                                               "body": {"PackageList": [{}]}}}}}
        idrac_connection_firmware_mock.update_mgr.update_from_dell_repo_url.return_value = {"job_details":
                                                                                    {"Data":
                                                                                {"GetRepoBasedUpdateList_OUTPUT":
                                                                                     {"Message": [{}]}}}}
        payload = {"ApplyUpdate": "True",
            "CatalogFile": "Catalog.xml",
            "IgnoreCertWarning": "On",
            "RebootNeeded": True,
            "UserName": "username",
            "Password": "psw"}
        result = self.module.update_firmware_url(f_module, idrac_connection_firmware_mock,
                                                 "http://downloads.dell.com",
                                                 "catalog.xml",
                                                 True, True, True, False, payload)
        assert result == ({'job_details': {'Data': {'GetRepoBasedUpdateList_OUTPUT': {'Message': [{}]}}}}, {})

    def test_update_firmware_url(self, idrac_connection_firmware_mock, idrac_default_args,
                                 mocker, idrac_connection_firmware_redfish_mock):
        idrac_default_args.update({"share_name": "http://downloads.dell.com", "catalog_file_name": "catalog.xml",
                                   "share_user": "shareuser", "share_password": "sharepswd", "share_mnt": "sharmnt",
                                   "reboot": True, "job_wait": False, "ignore_cert_warning": True,
                                   "share_type": "http", "idrac_ip": "idrac_ip", "idrac_user": "idrac_user",
                                   "idrac_password": "idrac_password", "idrac_port": 443})
        mocker.patch("ansible.modules.remote_management.dellemc.idrac_firmware.get_jobid", return_value="23451")
        mocker.patch("ansible.modules.remote_management.dellemc.idrac_firmware.eval", return_value={"PackageList": []})
        idrac_connection_firmware_mock.use_redfish = True
        idrac_connection_firmware_mock.idrac.update_mgr.job_mgr.get_job_status_redfish.return_value = "23451"
        f_module = self.get_module_mock(params=idrac_default_args)
        payload = {"ApplyUpdate": "True", "CatalogFile": "Catalog.xml", "IgnoreCertWarning": "On",
                   "RebootNeeded": True, "UserName": "username", "Password": "psw"}
        result = self.module.update_firmware_url(f_module, idrac_connection_firmware_mock, "http://downloads.dell.com/repo",
                                                 "catalog.xml", True, True, True, True, payload)
        assert result[1] == {"PackageList": []}

    def test_update_firmware_redfish(self, idrac_connection_firmware_mock, idrac_default_args, re_match_mock,
                                     mocker, idrac_connection_firmware_redfish_mock, fileonshare_idrac_firmware_mock):
        idrac_default_args.update({"share_name": "192.168.0.1:/share_name", "catalog_file_name": "catalog.xml",
                                   "share_user": "shareuser", "share_password": "sharepswd", "share_mnt": "sharmnt",
                                   "reboot": True, "job_wait": False, "ignore_cert_warning": True,
                                   "share_type": "http", "idrac_ip": "idrac_ip", "idrac_user": "idrac_user",
                                   "idrac_password": "idrac_password", "idrac_port": 443, 'apply_update': True})
        mocker.patch("ansible.modules.remote_management.dellemc.idrac_firmware.SHARE_TYPE", return_value={"NFS": "NFS"})
        mocker.patch("ansible.modules.remote_management.dellemc.idrac_firmware.eval", return_value={"PackageList": []})
        f_module = self.get_module_mock(params=idrac_default_args)
        re_mock = mocker.patch("ansible.modules.remote_management.dellemc.idrac_firmware.re", return_value=MagicMock())
        re_mock.match(MagicMock(), MagicMock()).group.return_value = "3.60"
        mocker.patch("ansible.modules.remote_management.dellemc.idrac_firmware.get_jobid", return_value="23451")
        idrac_connection_firmware_mock.idrac.update_mgr.job_mgr.get_job_status_redfish.return_value = "23451"
        idrac_connection_firmware_mock.ServerGeneration = "14"
        upd_share = fileonshare_idrac_firmware_mock
        upd_share.remote_addr.return_value = "192.168.0.1"
        upd_share.remote.share_name.return_value = "share_name"
        upd_share.remote_share_type.name.lower.return_value = "NFS"
        result = self.module.update_firmware(idrac_connection_firmware_mock, f_module)
        assert result['update_msg'] == "Successfully triggered the job to update the firmware."
