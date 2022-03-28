# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.2.0
# Copyright (C) 2020-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
import pytest
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_firmware
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from mock import MagicMock, patch, Mock
from io import StringIO
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.parse import urlparse, ParseResult
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


class TestidracFirmware(FakeAnsibleModule):
    module = idrac_firmware

    @pytest.fixture
    def idrac_firmware_update_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.update_mgr = idrac_obj
        idrac_obj.update_from_repo = Mock(return_value={
            "update_status": {
                "job_details": {
                    "Data": {
                        "StatusCode": 200,
                        "body": {
                            "PackageList": [{}]
                        }
                    }
                }
            }
        })
        idrac_obj.update_from_repo_url = Mock(return_value={"job_details": {"Data": {"StatusCode": 200,
                                                                                     "body": {"PackageList": [
                                                                                         {}]
                                                                                     }
                                                                                     }
                                                                            }
                                                            })
        return idrac_obj

    @pytest.fixture
    def idrac_firmware_job_mock(self, mocker):
        omsdk_mock = MagicMock()
        idrac_obj = MagicMock()
        omsdk_mock.job_mgr = idrac_obj
        idrac_obj.get_job_status_redfish = Mock(return_value={
            "update_status": {
                "job_details": {
                    "Data": {
                        "StatusCode": 200,
                        "body": {
                            "PackageList": [{}]
                        }
                    }
                }
            }
        })
        idrac_obj.job_wait = Mock(return_value="21543")
        return idrac_obj

    @pytest.fixture
    def re_match_mock(self, mocker):
        try:
            re_mock = mocker.patch(
                MODULE_PATH + 'idrac_firmware.re')
        except AttributeError:
            re_mock = MagicMock()
        obj = MagicMock()
        re_mock.match.group.return_value = obj
        return "3.30"

    @pytest.fixture
    def ET_convert_mock(self, mocker):
        try:
            ET_mock = mocker.patch(
                MODULE_PATH + 'idrac_firmware.ET')
        except AttributeError:
            ET_mock = MagicMock()
        obj = MagicMock()
        ET_mock.fromstring.return_value = obj
        return ET_mock

    @pytest.fixture
    def fileonshare_idrac_firmware_mock(self, mocker):
        share_mock = mocker.patch(MODULE_PATH + 'idrac_firmware.FileOnShare',
                                  return_value=MagicMock())
        return share_mock

    @pytest.fixture
    def idrac_connection_firmware_mock(self, mocker, idrac_firmware_update_mock):
        idrac_conn_class_mock = mocker.patch(MODULE_PATH +
                                             'idrac_firmware.iDRACConnection',
                                             return_value=idrac_firmware_update_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_firmware_update_mock
        return idrac_firmware_update_mock

    @pytest.fixture
    def idrac_connection_firmware_redfish_mock(self, mocker, idrac_firmware_job_mock):
        idrac_conn_class_mock = mocker.patch(MODULE_PATH +
                                             'idrac_firmware.iDRACRedfishAPI',
                                             return_value=idrac_firmware_job_mock)
        idrac_conn_class_mock.return_value.__enter__.return_value = idrac_firmware_job_mock
        return idrac_firmware_job_mock

    def test_main_idrac_firmware_success_case(self, idrac_connection_firmware_mock,
                                              idrac_connection_firmware_redfish_mock,
                                              idrac_default_args, mocker):
        idrac_default_args.update({"share_name": "sharename", "catalog_file_name": "Catalog.xml",
                                   "share_user": "sharename", "share_password": "sharepswd",
                                   "share_mnt": "sharmnt",
                                   "reboot": True, "job_wait": True
                                   })
        message = {"Status": "Success", "update_msg": "Successfully updated the firmware.",
                   "update_status": "Success", 'changed': False, 'failed': False}
        idrac_connection_firmware_redfish_mock.success = True
        idrac_connection_firmware_redfish_mock.json_data = {}
        mocker.patch(MODULE_PATH + 'idrac_firmware.update_firmware_redfish', return_value=message)
        result = self._run_module(idrac_default_args)
        assert result == {'msg': 'Successfully updated the firmware.', 'update_status': 'Success',
                          'changed': False, 'failed': False}

    @pytest.mark.parametrize("exc_type", [RuntimeError, URLError, SSLValidationError, ConnectionError, KeyError,
                                          ImportError, ValueError, TypeError])
    def test_main_idrac_firmware_exception_handling_case(self, exc_type, mocker, idrac_default_args,
                                                         idrac_connection_firmware_redfish_mock,
                                                         idrac_connection_firmware_mock):
        idrac_default_args.update({"share_name": "sharename", "catalog_file_name": "Catalog.xml",
                                   "share_user": "sharename", "share_password": "sharepswd",
                                   "share_mnt": "sharmnt",
                                   "reboot": True, "job_wait": True
                                   })
        idrac_connection_firmware_redfish_mock.success = True
        idrac_connection_firmware_redfish_mock.json_data = {"FirmwareVersion": "2.70"}
        mocker.patch(MODULE_PATH +
                     'idrac_firmware._validate_catalog_file', return_value="catalog_file_name")
        mocker.patch(MODULE_PATH +
                     'idrac_firmware.update_firmware_omsdk', side_effect=exc_type('test'))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True

    def test_main_HTTPError_case(self, idrac_connection_firmware_mock, idrac_default_args,
                                 idrac_connection_firmware_redfish_mock, mocker):
        idrac_default_args.update({"share_name": "sharename", "catalog_file_name": "Catalog.xml",
                                   "share_user": "sharename", "share_password": "sharepswd",
                                   "share_mnt": "sharmnt",
                                   "reboot": True, "job_wait": True
                                   })
        json_str = to_text(json.dumps({"data": "out"}))
        idrac_connection_firmware_redfish_mock.success = True
        idrac_connection_firmware_redfish_mock.json_data = {"FirmwareVersion": "2.70"}
        mocker.patch(MODULE_PATH + 'idrac_firmware.update_firmware_omsdk',
                     side_effect=HTTPError('http://testhost.com', 400, 'http error message',
                                           {"accept-type": "application/json"},
                                           StringIO(json_str)))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True

    def test_update_firmware_omsdk_success_case01(self, idrac_connection_firmware_mock,
                                                  idrac_connection_firmware_redfish_mock, idrac_default_args, mocker,
                                                  re_match_mock):
        idrac_default_args.update({"share_name": "https://downloads.dell.com", "catalog_file_name": "Catalog.xml",
                                   "share_user": "UserName", "share_password": "sharepswd",
                                   "share_mnt": "shrmnt",
                                   "reboot": True, "job_wait": True, "ignore_cert_warning": True,
                                   "apply_update": True})
        mocker.patch(MODULE_PATH + "idrac_firmware.update_firmware_url_omsdk",
                     return_value=({"update_status": {"job_details": {"Data": {"StatusCode": 200,
                                                                               "body": {"PackageList": [{}]}}}}},
                                   {"Data": {"StatusCode": 200, "body": {"PackageList": [{}]}}}))

        mocker.patch(MODULE_PATH + "idrac_firmware._convert_xmltojson",
                     return_value=({"BaseLocation": None,
                                    "ComponentID": "18981",
                                    "ComponentType": "APAC",
                                    "Criticality": "3",
                                    "DisplayName": "Dell OS Driver Pack",
                                    "JobID": None,
                                    "PackageName": "Drivers-for-OS-Deployment_Application_X0DW6_WN64"
                                                   "_19.10.12_A00.EXE",
                                    "PackagePath": "FOLDER05902898M/1/Drivers-for-"
                                                   "OS-Deployment_Application_X0DW6_WN64_19.10.12_A00.EXE",
                                    "PackageVersion": "19.10.12",
                                    "RebootType": "NONE",
                                    "Target": "DCIM:INSTALLED#802__DriverPack.Embedded.1:LC.Embedded.1"
                                    }, True, False))
        f_module = self.get_module_mock(params=idrac_default_args)
        idrac_connection_firmware_mock.match.return_value = "2.70"
        idrac_connection_firmware_redfish_mock.success = True
        idrac_connection_firmware_redfish_mock.json_data = {"FirmwareVersion": "2.70"}
        idrac_connection_firmware_mock.ServerGeneration.return_value = "13"
        idrac_connection_firmware_mock.update_mgr.update_from_repo.return_value = {
            "job_details": {"Data": {"StatusCode": 200, "GetRepoBasedUpdateList_OUTPUT": {},
                                     "body": {"PackageList1": [{}]}}}
        }
        result = self.module.update_firmware_omsdk(idrac_connection_firmware_mock, f_module)
        assert result["update_status"]["job_details"]["Data"]["StatusCode"] == 200

    def test_update_firmware_omsdk_success_case02(self, idrac_connection_firmware_mock,
                                                  idrac_connection_firmware_redfish_mock, idrac_default_args, mocker,
                                                  re_match_mock, fileonshare_idrac_firmware_mock):
        idrac_default_args.update({"share_name": "mhttps://downloads.dell.com", "catalog_file_name": "Catalog.xml",
                                   "share_user": "UserName", "share_password": "sharepswd",
                                   "share_mnt": "shrmnt",
                                   "reboot": True, "job_wait": True, "ignore_cert_warning": True,
                                   "apply_update": True
                                   })
        mocker.patch(MODULE_PATH + "idrac_firmware.update_firmware_url_omsdk",
                     return_value=({"update_status": {"job_details": {"data": {"StatusCode": 200,
                                                                               "body": {"PackageList": [{}]}}}}},
                                   {"Data": {"StatusCode": 200, "body": {"PackageList": [{}]}}}))

        mocker.patch(MODULE_PATH + "idrac_firmware._convert_xmltojson",
                     return_value=({"BaseLocation": None,
                                    "ComponentID": "18981",
                                    "ComponentType": "APAC",
                                    "Criticality": "3",
                                    "DisplayName": "Dell OS Driver Pack",
                                    "JobID": None,
                                    "PackageName": "Drivers-for-OS-Deployment_Application_X0DW6_WN64"
                                                   "_19.10.12_A00.EXE",
                                    "PackagePath": "FOLDER05902898M/1/Drivers-for-"
                                                   "OS-Deployment_Application_X0DW6_WN64_19.10.12_A00.EXE",
                                    "PackageVersion": "19.10.12",
                                    "RebootType": "NONE",
                                    "Target": "DCIM:INSTALLED#802__DriverPack.Embedded.1:LC.Embedded.1"
                                    }, True))

        f_module = self.get_module_mock(params=idrac_default_args)
        idrac_connection_firmware_mock.match.return_value = "2.70"
        idrac_connection_firmware_mock.ServerGeneration.return_value = "13"
        idrac_connection_firmware_redfish_mock.success = True
        idrac_connection_firmware_redfish_mock.json_data = {"FirmwareVersion": "2.70"}
        mocker.patch(MODULE_PATH + "idrac_firmware._convert_xmltojson", return_value=("INSTANCENAME", False, False))
        idrac_connection_firmware_mock.update_mgr.update_from_repo.return_value = {
            "job_details": {"Data": {"StatusCode": 200, "GetRepoBasedUpdateList_OUTPUT": {},
                                     "body": {"PackageList": [{}]}}}}
        upd_share = fileonshare_idrac_firmware_mock
        upd_share.IsValid = True
        result = self.module.update_firmware_omsdk(idrac_connection_firmware_mock, f_module)
        assert result["update_status"]["job_details"]["Data"]["StatusCode"] == 200

    def test_update_firmware_redfish_success_case03(self, idrac_connection_firmware_mock,
                                                    idrac_connection_firmware_redfish_mock,
                                                    idrac_default_args, mocker, re_match_mock):
        idrac_default_args.update({"share_name": "https://downloads.dell.com", "catalog_file_name": "Catalog.xml",
                                   "share_user": "UserName", "share_password": "sharepswd",
                                   "share_mnt": "shrmnt",
                                   "reboot": True, "job_wait": False, "ignore_cert_warning": True,
                                   "apply_update": True
                                   })
        mocker.patch(MODULE_PATH + "idrac_firmware.update_firmware_url_redfish",
                     return_value=(
                         {"job_details": {"Data": {"StatusCode": 200, "body": {"PackageList": [{}]}}}},
                         {"Data": {"StatusCode": 200, "body": {"PackageList": [{}]}}}))

        mocker.patch(MODULE_PATH + "idrac_firmware._convert_xmltojson",
                     return_value=({"BaseLocation": None,
                                    "ComponentID": "18981",
                                    "ComponentType": "APAC",
                                    "Criticality": "3",
                                    "DisplayName": "Dell OS Driver Pack",
                                    "JobID": None,
                                    "PackageName": "Drivers-for-OS-Deployment_Application_X0DW6_WN64_"
                                                   "19.10.12_A00.EXE",
                                    "PackagePath": "FOLDER05902898M/1/Drivers-for-OS-"
                                                   "Deployment_Application_X0DW6_WN64_19.10.12_A00.EXE",
                                    "PackageVersion": "19.10.12",
                                    "RebootType": "NONE",
                                    "Target": "DCIM:INSTALLED#802__DriverPack.Embedded.1:LC.Embedded.1"
                                    }, True))
        f_module = self.get_module_mock(params=idrac_default_args)
        idrac_connection_firmware_mock.re_match_mock.group = Mock(return_value="3.30")
        idrac_connection_firmware_redfish_mock.success = True
        idrac_connection_firmware_redfish_mock.json_data = {"FirmwareVersion": "3.30"}
        mocker.patch(MODULE_PATH + "idrac_firmware._convert_xmltojson", return_value=("INSTANCENAME", False, False))
        idrac_connection_firmware_mock.ServerGeneration = "14"
        result = self.module.update_firmware_redfish(idrac_connection_firmware_mock, f_module, {})
        assert result["changed"] is False
        assert result["update_msg"] == "Successfully triggered the job to update the firmware."

    def test_update_firmware_omsdk_status_success_case01(self, idrac_connection_firmware_mock,
                                                         idrac_connection_firmware_redfish_mock, idrac_default_args,
                                                         mocker, re_match_mock, fileonshare_idrac_firmware_mock):
        idrac_default_args.update({"share_name": "mhttps://downloads.dell.com", "catalog_file_name": "Catalog.xml",
                                   "share_user": "UserName", "share_password": "sharepswd",
                                   "share_mnt": "sharemnt",
                                   "reboot": True, "job_wait": True, "ignore_cert_warning": True,
                                   "apply_update": True
                                   })
        mocker.patch(MODULE_PATH + "idrac_firmware.update_firmware_url_omsdk",
                     return_value=({"update_status": {"job_details": {"data": {"StatusCode": 200,
                                                                               "body": {"PackageList": [{}]}}}}},
                                   {"job_details": {"Data": {"StatusCode": 200, "body": {"PackageList": [{}]}}}}))

        mocker.patch(MODULE_PATH + "idrac_firmware._convert_xmltojson",
                     return_value={
                         "BaseLocation": None,
                         "ComponentID": "18981",
                         "ComponentType": "APAC",
                         "Criticality": "3",
                         "DisplayName": "Dell OS Driver Pack",
                         "JobID": None,
                         "PackageName": "Drivers-for-OS-Deployment_Application_X0DW6_WN64_19.10.12_A00.EXE",
                         "PackagePath": "FOLDER05902898M/1/Drivers-for-OS-Deployment_"
                                        "Application_X0DW6_WN64_19.10.12_A00.EXE",
                         "PackageVersion": "19.10.12",
                         "RebootType": "NONE",
                         "Target": "DCIM:INSTALLED#802__DriverPack.Embedded.1:LC.Embedded.1"
                     })
        f_module = self.get_module_mock(params=idrac_default_args, check_mode=False)
        idrac_connection_firmware_mock.match.return_value = "2.70"
        idrac_connection_firmware_mock.ServerGeneration.return_value = "13"
        idrac_connection_firmware_redfish_mock.success = True
        idrac_connection_firmware_redfish_mock.json_data = {"FirmwareVersion": "2.70"}
        idrac_connection_firmware_mock.update_mgr.update_from_repo.return_value = {"job_details": {
            "Data": {"StatusCode": 200, "body": {}, "GetRepoBasedUpdateList_OUTPUT": {}}, "Status": "Success"},
            "Status": "Success"}
        upd_share = fileonshare_idrac_firmware_mock
        upd_share.IsValid = True
        result = self.module.update_firmware_omsdk(idrac_connection_firmware_mock, f_module)
        assert result == {'changed': False, 'failed': False,
                          'update_msg': 'Successfully triggered the job to update the firmware.',
                          'update_status': {'Status': 'Success',
                                            'job_details': {'Data': {'StatusCode': 200, 'body': {},
                                                                     "GetRepoBasedUpdateList_OUTPUT": {}},
                                                            'Status': 'Success'}}}

    def test_update_firmware_omsdk_status_failed_case01(self, idrac_connection_firmware_mock,
                                                        idrac_connection_firmware_redfish_mock,
                                                        idrac_default_args, mocker, re_match_mock):
        idrac_default_args.update({"share_name": "mhttps://downloads.dell.com", "catalog_file_name": "Catalog.xml",
                                   "share_user": "UserName", "share_password": "sharepswd",
                                   "share_mnt": "sharemnt",
                                   "reboot": True, "job_wait": True, "ignore_cert_warning": True,
                                   "apply_update": True})
        mocker.patch(MODULE_PATH + "idrac_firmware.update_firmware_url_omsdk",
                     return_value=({"update_status": {"job_details": {"data": {"StatusCode": 200,
                                                                               "body": {"PackageList": [{}]}}}}},
                                   {"job_details": {"Data": {"StatusCode": 200, "body": {"PackageList": [{}]}}}}))

        mocker.patch(MODULE_PATH + "idrac_firmware._convert_xmltojson",
                     return_value={
                         "BaseLocation": None,
                         "ComponentID": "18981",
                         "ComponentType": "APAC",
                         "Criticality": "3",
                         "DisplayName": "Dell OS Driver Pack",
                         "JobID": None,
                         "PackageName": "Drivers-for-OS-Deployment_Application_X0DW6_WN64_19.10.12_A00.EXE",
                         "PackagePath": "FOLDER05902898M/1/Drivers-for-OS-Deployment_"
                                        "Application_X0DW6_WN64_19.10.12_A00.EXE",
                         "PackageVersion": "19.10.12",
                         "RebootType": "NONE",
                         "Target": "DCIM:INSTALLED#802__DriverPack.Embedded.1:LC.Embedded.1"
                     })

        f_module = self.get_module_mock(params=idrac_default_args)
        idrac_connection_firmware_mock.match.return_value = "2.70"
        idrac_connection_firmware_mock.ServerGeneration.return_value = "13"
        idrac_connection_firmware_redfish_mock.success = True
        idrac_connection_firmware_redfish_mock.json_data = {"FirmwareVersion": "2.70"}
        idrac_connection_firmware_mock.update_mgr.update_from_repo.return_value = {"job_details": {"Data": {
            "StatusCode": 200, "body": {}, "GetRepoBasedUpdateList_OUTPUT": {}}, "Status": "Failed"},
            "Status": "Failed"}
        with pytest.raises(Exception) as ex:
            self.module.update_firmware_omsdk(idrac_connection_firmware_mock, f_module)
        assert ex.value.args[0] == "Firmware update failed."

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

    def test_convert_xmltojson_case01(self, mocker, idrac_connection_firmware_mock,
                                      idrac_default_args, ET_convert_mock):
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
        mocker.patch(MODULE_PATH + "idrac_firmware.get_job_status", return_value=("Component", False))
        mocker.patch(MODULE_PATH + 'idrac_firmware.ET')
        result = self.module._convert_xmltojson({"PackageList": [{"INSTANCENAME": {"PROPERTY": {"NAME": "abc"}}}]},
                                                MagicMock(), None)
        assert result == ([], True, False)

    def test_convert_xmltojson_case02(self, mocker, idrac_connection_firmware_mock, idrac_default_args):
        idrac_default_args.update({"Data": {"StatusCode": 200, "body": {"PackageList": [{}]}}})
        packagelist = {"PackageList": "INSTANCENAME"}
        mocker.patch(MODULE_PATH + "idrac_firmware.get_job_status", return_value=("Component", False))
        mocker.patch(MODULE_PATH + 'idrac_firmware.ET')
        result = self.module._convert_xmltojson(packagelist, MagicMock(), None)
        assert result == ([], True, False)

    def test_get_jobid_success_case01(self, idrac_connection_firmware_mock, idrac_default_args,
                                      idrac_firmware_job_mock,
                                      idrac_connection_firmware_redfish_mock):
        idrac_default_args.update({"Location": "https://jobmnager/jid123"})
        idrac_firmware_job_mock.status_code = 202
        idrac_firmware_job_mock.Success = True
        idrac_connection_firmware_redfish_mock.update_mgr.headers.get().split().__getitem__().return_value = "jid123"
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.get_jobid(f_module, idrac_firmware_job_mock)
        assert result == idrac_connection_firmware_redfish_mock.headers.get().split().__getitem__()

    def test_get_jobid_fail_case01(self, idrac_connection_firmware_mock, idrac_default_args,
                                   idrac_firmware_job_mock):
        idrac_firmware_job_mock.status_code = 202
        idrac_firmware_job_mock.headers = {"Location": None}
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as exc:
            self.module.get_jobid(f_module, idrac_firmware_job_mock)
        assert exc.value.args[0] == "Failed to update firmware."

    def test_get_jobid_fail_case02(self, idrac_connection_firmware_mock, idrac_default_args,
                                   idrac_firmware_job_mock):
        idrac_firmware_job_mock.status_code = 400
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as exc:
            self.module.get_jobid(f_module, idrac_firmware_job_mock)
        assert exc.value.args[0] == "Failed to update firmware."

    def test_update_firmware_url_omsdk_success_case02(self, idrac_connection_firmware_mock, idrac_default_args,
                                                      mocker, idrac_connection_firmware_redfish_mock):
        idrac_default_args.update({"share_name": "http://downloads.dell.com", "catalog_file_name": "catalog.xml",
                                   "share_user": "shareuser", "share_password": "sharepswd",
                                   "share_mnt": "sharmnt",
                                   "reboot": True, "job_wait": False, "ignore_cert_warning": True,
                                   "share_type": "http", "idrac_ip": "idrac_ip", "idrac_user": "idrac_user",
                                   "idrac_password": "idrac_password", "idrac_port": 443
                                   })
        mocker.patch(MODULE_PATH + "idrac_firmware.get_jobid",
                     return_value="23451")

        mocker.patch(MODULE_PATH + "idrac_firmware.urlparse",
                     return_value=ParseResult(scheme='http', netloc='downloads.dell.com',
                                              path='/%7Eguido/Python.html',
                                              params='', query='', fragment=''))
        mocker.patch("socket.gethostbyname", return_value="downloads.dell.com")
        f_module = self.get_module_mock(params=idrac_default_args)
        idrac_connection_firmware_mock.use_redfish = False
        idrac_connection_firmware_redfish_mock.get_job_status_redfish = "Status"
        idrac_connection_firmware_redfish_mock.update_mgr.job_mgr.job_wait.return_value = "12345"
        idrac_connection_firmware_mock.update_mgr.update_from_repo_url.return_value = {
            "update_status": {"job_details": {"data": {
                "StatusCode": 200,
                "body": {
                    "PackageList": [
                        {}]
                }
            }
            }
            }
        }
        idrac_connection_firmware_mock.update_mgr.update_from_dell_repo_url.return_value = {"job_details": {"Data": {
            "GetRepoBasedUpdateList_OUTPUT": {
                "Message": [
                    {}]
            }
        }
        }
        }
        payload = {"ApplyUpdate": "True",
                   "CatalogFile": "Catalog.xml",
                   "IgnoreCertWarning": "On",
                   "RebootNeeded": True,
                   "UserName": "username",
                   "Password": "psw"
                   }
        result = self.module.update_firmware_url_omsdk(f_module, idrac_connection_firmware_mock,
                                                       "http://downloads.dell.com", "catalog.xml", True, True, True,
                                                       False, payload)
        assert result == (
            {'job_details': {'Data': {'GetRepoBasedUpdateList_OUTPUT': {'Message': [{}]}}}}, {})

    def test_update_firmware_url_omsdk(self, idrac_connection_firmware_mock, idrac_default_args, mocker,
                                       idrac_connection_firmware_redfish_mock):
        idrac_default_args.update({"share_name": "http://downloads.dell.com", "catalog_file_name": "catalog.xml",
                                   "share_user": "shareuser", "share_password": "sharepswd",
                                   "share_mnt": "sharmnt",
                                   "reboot": True, "job_wait": False, "ignore_cert_warning": True,
                                   "share_type": "http", "idrac_ip": "idrac_ip", "idrac_user": "idrac_user",
                                   "idrac_password": "idrac_password", "idrac_port": 443
                                   })
        mocker.patch(MODULE_PATH + "idrac_firmware.get_jobid",
                     return_value="23451")
        mocker.patch(MODULE_PATH + "idrac_firmware.get_check_mode_status")
        idrac_connection_firmware_mock.use_redfish = True
        idrac_connection_firmware_mock.job_mgr.get_job_status_redfish.return_value = "23451"
        idrac_connection_firmware_mock.update_mgr.update_from_dell_repo_url.return_value = {
            "InstanceID": "JID_12345678"}
        f_module = self.get_module_mock(params=idrac_default_args)
        payload = {"ApplyUpdate": "True", "CatalogFile": "Catalog.xml", "IgnoreCertWarning": "On",
                   "RebootNeeded": True, "UserName": "username", "Password": "psw"}
        result = self.module.update_firmware_url_omsdk(f_module, idrac_connection_firmware_mock,
                                                       "http://downloads.dell.com/repo",
                                                       "catalog.xml", True, True, True, True, payload)
        assert result[0] == {"InstanceID": "JID_12345678"}

    def _test_update_firmware_redfish(self, idrac_connection_firmware_mock, idrac_default_args, re_match_mock,
                                      mocker, idrac_connection_firmware_redfish_mock,
                                      fileonshare_idrac_firmware_mock):
        idrac_default_args.update({"share_name": "192.168.0.1:/share_name", "catalog_file_name": "catalog.xml",
                                   "share_user": "shareuser", "share_password": "sharepswd",
                                   "share_mnt": "sharmnt",
                                   "reboot": True, "job_wait": False, "ignore_cert_warning": True,
                                   "share_type": "http", "idrac_ip": "idrac_ip", "idrac_user": "idrac_user",
                                   "idrac_password": "idrac_password", "idrac_port": 443, 'apply_update': True
                                   })
        mocker.patch(MODULE_PATH + "idrac_firmware.SHARE_TYPE",
                     return_value={"NFS": "NFS"})
        mocker.patch(MODULE_PATH + "idrac_firmware.eval",
                     return_value={"PackageList": []})
        mocker.patch(MODULE_PATH + "idrac_firmware.wait_for_job_completion", return_value=({}, None))
        f_module = self.get_module_mock(params=idrac_default_args)
        re_mock = mocker.patch(MODULE_PATH + "idrac_firmware.re",
                               return_value=MagicMock())
        re_mock.match(MagicMock(), MagicMock()).group.return_value = "3.60"
        mocker.patch(MODULE_PATH + "idrac_firmware.get_jobid",
                     return_value="23451")
        idrac_connection_firmware_mock.idrac.update_mgr.job_mgr.get_job_status_redfish.return_value = "23451"
        idrac_connection_firmware_mock.ServerGeneration = "14"
        upd_share = fileonshare_idrac_firmware_mock
        upd_share.remote_addr.return_value = "192.168.0.1"
        upd_share.remote.share_name.return_value = "share_name"
        upd_share.remote_share_type.name.lower.return_value = "NFS"
        result = self.module.update_firmware_redfish(idrac_connection_firmware_mock, f_module)
        assert result['update_msg'] == "Successfully triggered the job to update the firmware."

    def _test_get_job_status(self, idrac_connection_firmware_mock, idrac_default_args,
                             mocker, idrac_connection_firmware_redfish_mock):
        idrac_default_args.update({"share_name": "http://downloads.dell.com", "catalog_file_name": "catalog.xml",
                                   "share_user": "shareuser", "share_password": "sharepswd",
                                   "share_mnt": "sharmnt", "apply_update": False,
                                   "reboot": True, "job_wait": False, "ignore_cert_warning": True,
                                   "share_type": "http", "idrac_ip": "idrac_ip", "idrac_user": "idrac_user",
                                   "idrac_password": "idrac_password", "idrac_port": 443})
        f_module = self.get_module_mock(params=idrac_default_args)
        idrac_connection_firmware_redfish_mock.success = True
        idrac_connection_firmware_redfish_mock.json_data = {"JobStatus": "OK"}
        each_comp = {"JobID": "JID_1234567", "Messages": [{"Message": "test_message"}], "JobStatus": "Completed"}
        result = self.module.get_job_status(f_module, each_comp, None)
        assert result[1] is False

    def test_message_verification(self, idrac_connection_firmware_mock, idrac_connection_firmware_redfish_mock,
                                  idrac_default_args, mocker):
        idrac_default_args.update({"share_name": "http://downloads.dell.com", "catalog_file_name": "catalog.xml",
                                   "share_user": "shareuser", "share_password": "sharepswd",
                                   "share_mnt": "sharmnt", "apply_update": False,
                                   "reboot": False, "job_wait": True, "ignore_cert_warning": True,
                                   "idrac_ip": "idrac_ip", "idrac_user": "idrac_user",
                                   "idrac_password": "idrac_password", "idrac_port": 443})
        mocker.patch(MODULE_PATH + "idrac_firmware._convert_xmltojson", return_value=("INSTANCENAME", False, False))
        # mocker.patch(MODULE_PATH + "idrac_firmware.re")
        idrac_connection_firmware_redfish_mock.success = True
        idrac_connection_firmware_redfish_mock.json_data = {"FirmwareVersion": "2.70"}
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.update_firmware_omsdk(idrac_connection_firmware_mock, f_module)
        assert result['update_msg'] == "Successfully fetched the applicable firmware update package list."

        idrac_default_args.update({"apply_update": True, "reboot": False, "job_wait": False})
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.update_firmware_omsdk(idrac_connection_firmware_mock, f_module)
        assert result['update_msg'] == "Successfully triggered the job to stage the firmware."

        idrac_default_args.update({"apply_update": True, "reboot": False, "job_wait": True})
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.update_firmware_omsdk(idrac_connection_firmware_mock, f_module)
        assert result['update_msg'] == "Successfully staged the applicable firmware update packages."

        idrac_default_args.update({"apply_update": True, "reboot": False, "job_wait": True})
        mocker.patch(MODULE_PATH + "idrac_firmware.update_firmware_url_omsdk",
                     return_value=({"Status": "Success"}, {"PackageList": []}))
        mocker.patch(MODULE_PATH + "idrac_firmware._convert_xmltojson", return_value=({}, True, True))
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.update_firmware_omsdk(idrac_connection_firmware_mock, f_module)
        assert result['update_msg'] == "Successfully staged the applicable firmware update packages with error(s)."

        idrac_default_args.update({"apply_update": True, "reboot": True, "job_wait": True})
        mocker.patch(MODULE_PATH + "idrac_firmware._convert_xmltojson", return_value=({}, True, False))
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.update_firmware_omsdk(idrac_connection_firmware_mock, f_module)
        assert result['update_msg'] == "Successfully updated the firmware."

        idrac_default_args.update({"apply_update": True, "reboot": True, "job_wait": True})
        mocker.patch(MODULE_PATH + "idrac_firmware._convert_xmltojson", return_value=({}, True, True))
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.update_firmware_omsdk(idrac_connection_firmware_mock, f_module)
        assert result['update_msg'] == "Firmware update failed."
