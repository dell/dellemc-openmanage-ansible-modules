# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.4.0
# Copyright (C) 2020-2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
import pytest
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_firmware
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from unittest.mock import MagicMock, Mock
from io import StringIO
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.parse import ParseResult
from pytest import importorskip

importorskip("omsdk.sdkfile")
importorskip("omsdk.sdkcreds")

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
CATALOG = "Catalog.xml"
DELL_SHARE = "https://downloads.dell.com"
GET_JOBID = "idrac_firmware.get_jobid"
CONVERT_XML_JSON = "idrac_firmware._convert_xmltojson"
SUCCESS_MSG = "Successfully updated the firmware."
UPDATE_URL = "idrac_firmware.update_firmware_url_redfish"
WAIT_FOR_JOB = "idrac_firmware.wait_for_job_completion"
TIME_SLEEP = "idrac_firmware.time.sleep"
VALIDATE_CATALOG = "idrac_firmware._validate_catalog_file"
SHARE_PWD = "share_pwd"
USER_PWD = "user_pwd"
TEST_HOST = "'https://testhost.com'"


class TestidracFirmware(FakeAnsibleModule):
    module = idrac_firmware

    @pytest.fixture
    def idrac_firmware_update_mock(self):
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

    @pytest.fixture
    def idrac_connection_firm_mock(self, mocker, redfish_response_mock):

        connection_class_mock = mocker.patch(MODULE_PATH + 'idrac_firmware.iDRACRedfishAPI')
        redfish_connection_obj = connection_class_mock.return_value.__enter__.return_value
        redfish_connection_obj.invoke_request.return_value = redfish_response_mock
        return redfish_connection_obj

    def test__validate_catalog_file_case01(self, idrac_default_args):
        idrac_default_args.update({"catalog_file_name": ""})
        with pytest.raises(ValueError) as exc:
            self.module._validate_catalog_file("")
        assert exc.value.args[0] == 'catalog_file_name should be a non-empty string.'

    def test__validate_catalog_file_case02(self, idrac_default_args):
        idrac_default_args.update({"catalog_file_name": "Catalog.json"})
        with pytest.raises(ValueError) as exc:
            self.module._validate_catalog_file("Catalog.json")
        assert exc.value.args[0] == 'catalog_file_name should be an XML file.'

    def test_convert_xmltojson(self, mocker, idrac_default_args, idrac_connection_firmware_redfish_mock):
        idrac_default_args.update({"share_name": "sharename", "catalog_file_name": CATALOG,
                                   "share_user": "sharename", "share_password": SHARE_PWD,
                                   "share_mnt": "sharmnt", "reboot": True, "job_wait": True, "apply_update": True})
        f_module = self.get_module_mock(params=idrac_default_args)
        mocker.patch(MODULE_PATH + "idrac_firmware.get_job_status", return_value=("Component", False))
        job_details = {"PackageList": """<?xml version="1.0" encoding="UTF-8" ?><root><BaseLocation /><ComponentID>18981</ComponentID></root>"""}
        result = self.module._convert_xmltojson(f_module, job_details, idrac_connection_firmware_redfish_mock)
        assert result == ([], True, False)
        et_mock = MagicMock()
        et_mock.iter.return_value = [et_mock, et_mock]
        mocker.patch(MODULE_PATH + "idrac_firmware.ET.fromstring", return_value=et_mock)
        mocker.patch(MODULE_PATH + "idrac_firmware.get_job_status", return_value=("Component", True))
        result = self.module._convert_xmltojson(f_module, job_details, idrac_connection_firmware_redfish_mock)
        assert result[0] == ['Component', 'Component']
        assert result[1]
        assert result[2]

    def test_update_firmware_url_omsdk(self, idrac_connection_firmware_mock, idrac_default_args, mocker):
        idrac_default_args.update({"share_name": DELL_SHARE, "catalog_file_name": CATALOG,
                                   "share_user": "shareuser", "share_password": SHARE_PWD,
                                   "share_mnt": "sharmnt", "reboot": True, "job_wait": False, "ignore_cert_warning": True,
                                   "share_type": "http", "idrac_ip": "idrac_ip", "idrac_user": "idrac_user",
                                   "idrac_password": "idrac_password", "idrac_port": 443, "proxy_support": "Off"})
        mocker.patch(MODULE_PATH + GET_JOBID, return_value="23451")
        mocker.patch(MODULE_PATH + "idrac_firmware.get_check_mode_status")
        idrac_connection_firmware_mock.use_redfish = True
        idrac_connection_firmware_mock.job_mgr.get_job_status_redfish.return_value = "23451"
        idrac_connection_firmware_mock.update_mgr.update_from_dell_repo_url.return_value = {"InstanceID": "JID_12345678"}
        f_module = self.get_module_mock(params=idrac_default_args)
        payload = {"ApplyUpdate": "True", "CatalogFile": CATALOG, "IgnoreCertWarning": "On",
                   "RebootNeeded": True, "UserName": "username", "Password": USER_PWD}
        result = self.module.update_firmware_url_omsdk(f_module, idrac_connection_firmware_mock,
                                                       DELL_SHARE, CATALOG, True, True, True, True, payload)
        assert result[0] == {"InstanceID": "JID_12345678"}

    def test_update_firmware_url_omsdk_success_case02(self, idrac_connection_firmware_mock, idrac_default_args,
                                                      mocker, idrac_connection_firmware_redfish_mock):
        idrac_default_args.update({"share_name": DELL_SHARE, "catalog_file_name": CATALOG,
                                   "share_user": "shareuser", "share_password": SHARE_PWD,
                                   "share_mnt": "sharmnt",
                                   "reboot": True, "job_wait": False, "ignore_cert_warning": True,
                                   "share_type": "http", "idrac_ip": "idrac_ip", "idrac_user": "idrac_user",
                                   "idrac_password": "idrac_password", "idrac_port": 443, "proxy_support": "Off",
                                   })
        mocker.patch(MODULE_PATH + GET_JOBID, return_value="23451")
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
            "update_status": {"job_details": {"data": {"StatusCode": 200, "body": {"PackageList": [{}]}}}}
        }
        idrac_connection_firmware_mock.update_mgr.update_from_dell_repo_url.return_value = {"job_details": {"Data": {
            "GetRepoBasedUpdateList_OUTPUT": {"Message": [{}]}}}
        }
        payload = {"ApplyUpdate": "True", "CatalogFile": CATALOG, "IgnoreCertWarning": "On", "RebootNeeded": True,
                   "UserName": "username", "Password": USER_PWD}
        result = self.module.update_firmware_url_omsdk(f_module, idrac_connection_firmware_mock,
                                                       DELL_SHARE, CATALOG, True, True, True,
                                                       False, payload)
        assert result == ({'job_details': {'Data': {'GetRepoBasedUpdateList_OUTPUT': {'Message': [{}]}}}}, {})

    def test_message_verification(self, idrac_connection_firmware_mock, idrac_connection_firmware_redfish_mock,
                                  idrac_default_args, mocker):
        idrac_default_args.update({"share_name": DELL_SHARE, "catalog_file_name": CATALOG,
                                   "share_user": "shareuser", "share_password": SHARE_PWD,
                                   "share_mnt": "sharmnt", "apply_update": False,
                                   "reboot": False, "job_wait": True, "ignore_cert_warning": True,
                                   "idrac_ip": "idrac_ip", "idrac_user": "idrac_user",
                                   "idrac_password": "idrac_password", "idrac_port": 443, "proxy_support": "Off", })
        mocker.patch(MODULE_PATH + CONVERT_XML_JSON, return_value=("INSTANCENAME", False, False))
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
        mocker.patch(MODULE_PATH + CONVERT_XML_JSON, return_value=({}, True, True))
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.update_firmware_omsdk(idrac_connection_firmware_mock, f_module)
        assert result['update_msg'] == "Successfully staged the applicable firmware update packages with error(s)."
        idrac_default_args.update({"apply_update": True, "reboot": True, "job_wait": True})
        mocker.patch(MODULE_PATH + CONVERT_XML_JSON, return_value=({}, True, False))
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.update_firmware_omsdk(idrac_connection_firmware_mock, f_module)
        assert result['update_msg'] == SUCCESS_MSG
        idrac_default_args.update({"apply_update": True, "reboot": True, "job_wait": True})
        mocker.patch(MODULE_PATH + CONVERT_XML_JSON, return_value=({}, True, True))
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.update_firmware_omsdk(idrac_connection_firmware_mock, f_module)
        assert result['update_msg'] == "Firmware update failed."

    def test_update_firmware_redfish_success_case03(self, idrac_connection_firmware_mock,
                                                    idrac_connection_firmware_redfish_mock,
                                                    idrac_default_args, mocker):
        idrac_default_args.update({"share_name": DELL_SHARE, "catalog_file_name": CATALOG,
                                   "share_user": "UserName", "share_password": SHARE_PWD, "share_mnt": "shrmnt",
                                   "reboot": True, "job_wait": False, "ignore_cert_warning": True, "apply_update": True})
        mocker.patch(MODULE_PATH + UPDATE_URL,
                     return_value=({"job_details": {"Data": {"StatusCode": 200, "body": {"PackageList": [{}]}}}},
                                   {"Data": {"StatusCode": 200, "body": {"PackageList": [{}]}}}))
        mocker.patch(MODULE_PATH + CONVERT_XML_JSON,
                     return_value=({"BaseLocation": None, "ComponentID": "18981", "ComponentType": "APAC", "Criticality": "3",
                                    "DisplayName": "Dell OS Driver Pack", "JobID": None,
                                    "PackageName": "Drivers-for-OS-Deployment_Application_X0DW6_WN64_19.10.12_A00.EXE",
                                    "PackagePath": "FOLDER05902898M/1/Drivers-for-OS-Deployment_Application_X0DW6_WN64_19.10.12_A00.EXE",
                                    "PackageVersion": "19.10.12", "RebootType": "NONE",
                                    "Target": "DCIM:INSTALLED#802__DriverPack.Embedded.1:LC.Embedded.1"}, True))
        f_module = self.get_module_mock(params=idrac_default_args)
        idrac_connection_firmware_mock.re_match_mock.group = Mock(return_value="3.30")
        idrac_connection_firmware_redfish_mock.success = True
        idrac_connection_firmware_redfish_mock.json_data = {"FirmwareVersion": "3.30"}
        mocker.patch(MODULE_PATH + CONVERT_XML_JSON, return_value=("INSTANCENAME", False, False))
        idrac_connection_firmware_mock.ServerGeneration = "14"
        result = self.module.update_firmware_redfish(idrac_connection_firmware_mock, f_module, {})
        assert result["changed"] is False
        assert result["update_msg"] == "Successfully triggered the job to update the firmware."
        idrac_default_args.update({"proxy_support": "ParametersProxy", "proxy_server": "127.0.0.2", "proxy_port": 3128,
                                   "proxy_type": "HTTP", "proxy_uname": "username", "proxy_passwd": "pwd", "apply_update": False})
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = True
        mocker.patch(MODULE_PATH + WAIT_FOR_JOB, return_value=({"JobStatus": "Ok"}, ""))
        mocker.patch(MODULE_PATH + CONVERT_XML_JSON, return_value=({"PackageList": []}, False, False))
        mocker.patch(MODULE_PATH + UPDATE_URL,
                     return_value=({"JobStatus": "Ok"}, {"Status": "Success", "JobStatus": "Ok",
                                                         "Data": {"GetRepoBasedUpdateList_OUTPUT": {}}}))
        with pytest.raises(Exception) as exc:
            self.module.update_firmware_redfish(idrac_connection_firmware_mock, f_module, {})
        assert exc.value.args[0] == 'Unable to complete the firmware repository download.'
        idrac_default_args.update({"share_name": "\\\\127.0.0.1\\cifsshare"})
        idrac_connection_firmware_mock.json_data = {"Status": "Success"}
        mocker.patch(MODULE_PATH + GET_JOBID, return_value=None)
        mocker.patch(MODULE_PATH + WAIT_FOR_JOB,
                     return_value=({"JobStatus": "Ok"}, {"job_details": "", "JobStatus": "Ok"}))
        with pytest.raises(Exception) as exc:
            self.module.update_firmware_redfish(idrac_connection_firmware_mock, f_module, {})
        assert exc.value.args[0] == 'Unable to complete the firmware repository download.'
        idrac_default_args.update({"apply_update": True, "reboot": False, "job_wait": True})
        mocker.patch(MODULE_PATH + WAIT_FOR_JOB,
                     return_value=({"JobStatus": "OK"}, {"job_details": "", "JobStatus": "OK"}))
        with pytest.raises(Exception) as exc:
            self.module.update_firmware_redfish(idrac_connection_firmware_mock, f_module, {})
        assert exc.value.args[0] == 'Changes found to commit!'
        f_module.check_mode = False
        idrac_default_args.update({"apply_update": True, "reboot": True, "job_wait": True, "share_name": "https://127.0.0.2/httpshare"})
        mocker.patch(MODULE_PATH + CONVERT_XML_JSON, return_value=({"PackageList": []}, True, False))
        mocker.patch(MODULE_PATH + UPDATE_URL, return_value=(
            {"JobStatus": "Ok"}, {"Status": "Success", "JobStatus": "Ok", "PackageList": [],
                                  "Data": {"GetRepoBasedUpdateList_OUTPUT": {}}}))
        result = self.module.update_firmware_redfish(idrac_connection_firmware_mock, f_module, {})
        assert result["update_msg"] == SUCCESS_MSG
        mocker.patch(MODULE_PATH + CONVERT_XML_JSON, return_value=({"PackageList": []}, True, True))
        result = self.module.update_firmware_redfish(idrac_connection_firmware_mock, f_module, {})
        assert result["update_msg"] == "Firmware update failed."
        idrac_default_args.update({"apply_update": False})
        mocker.patch(MODULE_PATH + UPDATE_URL,
                     return_value=({"JobStatus": "Critical"}, {"Status": "Success", "JobStatus": "Critical", "PackageList": [],
                                                               "Data": {"GetRepoBasedUpdateList_OUTPUT": {}}}))
        with pytest.raises(Exception) as exc:
            self.module.update_firmware_redfish(idrac_connection_firmware_mock, f_module, {})
        assert exc.value.args[0] == 'Unable to complete the repository update.'
        idrac_default_args.update({"apply_update": True, "reboot": False, "job_wait": True, "share_name": "https://127.0.0.3/httpshare"})
        with pytest.raises(Exception) as exc:
            self.module.update_firmware_redfish(idrac_connection_firmware_mock, f_module, {})
        assert exc.value.args[0] == 'Firmware update failed.'
        idrac_default_args.update({"apply_update": True, "reboot": False, "job_wait": False, "share_name": "https://127.0.0.4/httpshare"})
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = True
        mocker.patch(MODULE_PATH + CONVERT_XML_JSON, return_value=({"PackageList": []}, True, False))
        mocker.patch(MODULE_PATH + UPDATE_URL,
                     return_value=({"JobStatus": "OK"}, {"Status": "Success", "JobStatus": "OK", "PackageList": ['test'],
                                                         "Data": {"key": "value"}}))
        with pytest.raises(Exception) as exc:
            self.module.update_firmware_redfish(idrac_connection_firmware_mock, f_module, {})
        assert exc.value.args[0] == 'Changes found to commit!'

    def test_main_idrac_firmware_success_case(self, idrac_connection_firmware_redfish_mock, idrac_default_args, mocker):
        idrac_default_args.update({"share_name": "sharename", "catalog_file_name": CATALOG,
                                   "share_user": "sharename", "share_password": SHARE_PWD,
                                   "share_mnt": "sharmnt", "reboot": True, "job_wait": True})
        message = {"Status": "Success", "update_msg": SUCCESS_MSG,
                   "update_status": "Success", 'changed': False, 'failed': False}
        idrac_connection_firmware_redfish_mock.success = True
        idrac_connection_firmware_redfish_mock.json_data = {}
        mocker.patch(MODULE_PATH + 'idrac_firmware.update_firmware_redfish', return_value=message)
        result = self._run_module(idrac_default_args)
        assert result == {'msg': 'Successfully updated the firmware.', 'update_status': 'Success',
                          'changed': False, 'failed': False}

    def test_main_HTTPError_case(self, idrac_default_args, idrac_connection_firmware_redfish_mock, mocker):
        idrac_default_args.update({"share_name": "sharename", "catalog_file_name": CATALOG,
                                   "share_user": "sharename", "share_password": SHARE_PWD,
                                   "share_mnt": "sharmnt",
                                   "reboot": True, "job_wait": True})
        json_str = to_text(json.dumps({"data": "out"}))
        idrac_connection_firmware_redfish_mock.success = True
        idrac_connection_firmware_redfish_mock.json_data = {"FirmwareVersion": "2.70"}
        mocker.patch(MODULE_PATH + 'idrac_firmware.update_firmware_omsdk',
                     side_effect=HTTPError('https://testhost.com', 400, 'http error message',
                                           {"accept-type": "application/json"},
                                           StringIO(json_str)))
        result = self._run_module_with_fail_json(idrac_default_args)
        assert 'msg' in result
        assert result['failed'] is True

    def test_get_jobid(self, idrac_connection_firmware_mock, idrac_default_args):
        idrac_default_args.update({"share_name": "sharename", "catalog_file_name": CATALOG,
                                   "share_user": "sharename", "share_password": SHARE_PWD,
                                   "share_mnt": "sharmnt", "reboot": True, "job_wait": True})
        f_module = self.get_module_mock(params=idrac_default_args)
        idrac_connection_firmware_mock.status_code = 202
        idrac_connection_firmware_mock.headers = {"Location": "/uri/JID_123456789"}
        result = self.module.get_jobid(f_module, idrac_connection_firmware_mock)
        assert result == "JID_123456789"
        idrac_connection_firmware_mock.headers = {"Location": None}
        with pytest.raises(Exception) as exc:
            self.module.get_jobid(f_module, idrac_connection_firmware_mock)
        assert exc.value.args[0] == 'Failed to update firmware.'
        idrac_connection_firmware_mock.status_code = 200
        with pytest.raises(Exception) as exc:
            self.module.get_jobid(f_module, idrac_connection_firmware_mock)
        assert exc.value.args[0] == 'Failed to update firmware.'

    def test_handle_HTTP_error(self, idrac_default_args, mocker):
        error_message = {"error": {"@Message.ExtendedInfo": [{"Message": "Http error message", "MessageId": "SUP029"}]}}
        idrac_default_args.update({"share_name": "sharename", "catalog_file_name": CATALOG,
                                   "share_user": "sharename", "share_password": SHARE_PWD,
                                   "share_mnt": "sharmnt", "reboot": True, "job_wait": True})
        f_module = self.get_module_mock(params=idrac_default_args)
        mocker.patch(MODULE_PATH + 'idrac_firmware.json.load', return_value=error_message)
        with pytest.raises(Exception) as exc:
            self.module.handle_HTTP_error(f_module, error_message)
        assert exc.value.args[0] == 'Http error message'

    def test_get_job_status(self, idrac_default_args, idrac_connection_firmware_redfish_mock, mocker):
        idrac_default_args.update({"share_name": "sharename", "catalog_file_name": CATALOG,
                                   "share_user": "sharename", "share_password": SHARE_PWD,
                                   "share_mnt": "sharmnt", "reboot": True, "job_wait": True, "apply_update": True})
        f_module = self.get_module_mock(params=idrac_default_args)
        each_comp = {"JobID": "JID_123456789", "Message": "Invalid", "JobStatus": "Ok"}
        idrac_connection_firmware_redfish_mock.job_mgr.job_wait.return_value = {"JobStatus": "Completed", "Message": "Invalid"}
        comp, failed = self.module.get_job_status(f_module, each_comp, idrac_connection_firmware_redfish_mock)
        assert comp == {'JobID': 'JID_123456789', 'Message': 'Invalid', 'JobStatus': 'Critical'}
        assert failed
        mocker.patch(MODULE_PATH + WAIT_FOR_JOB,
                     return_value=(idrac_connection_firmware_redfish_mock, ""))
        each_comp = {"JobID": "JID_123456789", "Message": "Invalid", "JobStatus": "Critical"}
        idrac_connection_firmware_redfish_mock.json_data = {"Messages": [{"Message": "Success"}], "JobStatus": "Critical"}
        comp, failed = self.module.get_job_status(f_module, each_comp, None)
        assert comp == {'JobID': 'JID_123456789', 'Message': 'Success', 'JobStatus': 'Critical'}
        assert failed

    def test_wait_for_job_completion(self, idrac_default_args, idrac_connection_firm_mock, redfish_response_mock):
        idrac_default_args.update({"share_name": "sharename", "catalog_file_name": CATALOG,
                                   "share_user": "sharename", "share_password": SHARE_PWD,
                                   "share_mnt": "sharmnt", "reboot": True, "job_wait": True, "apply_update": True})
        f_module = self.get_module_mock(params=idrac_default_args)
        result, msg = self.module.wait_for_job_completion(f_module, "JobService/Jobs/JID_1234567890")
        assert msg is None
        redfish_response_mock.json_data = {"Members": {}, "JobState": "Completed", "PercentComplete": 100}
        result, msg = self.module.wait_for_job_completion(f_module, "JobService/Jobs/JID_12345678", job_wait=True)
        assert result.json_data["JobState"] == "Completed"
        redfish_response_mock.json_data = {"Members": {}, "JobState": "New", "PercentComplete": 0}
        result, msg = self.module.wait_for_job_completion(f_module, "JobService/Jobs/JID_123456789", job_wait=True, apply_update=True)
        assert result.json_data["JobState"] == "New"

    @pytest.mark.parametrize("exc_type", [TypeError])
    def test_wait_for_job_completion_exception(self, exc_type, idrac_default_args, idrac_connection_firmware_redfish_mock, mocker):
        idrac_default_args.update({"share_name": "sharename", "catalog_file_name": CATALOG,
                                   "share_user": "sharename", "share_password": SHARE_PWD,
                                   "share_mnt": "sharmnt", "reboot": True, "job_wait": True, "apply_update": True})
        f_module = self.get_module_mock(params=idrac_default_args)
        mocker.patch(MODULE_PATH + TIME_SLEEP, return_value=None)
        if exc_type == TypeError:
            idrac_connection_firmware_redfish_mock.invoke_request.side_effect = exc_type("exception message")
            result, msg = self.module.wait_for_job_completion(f_module, "JobService/Jobs/JID_123456789", job_wait=True)
            assert msg == "Job wait timed out after 120.0 minutes"

    def test_get_check_mode_status_check_mode(self, idrac_default_args):
        idrac_default_args.update({"share_name": "sharename", "catalog_file_name": CATALOG,
                                   "share_user": "sharename", "share_password": SHARE_PWD,
                                   "share_mnt": "sharmnt", "reboot": True, "job_wait": True, "apply_update": True})
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = True
        status = {"job_details": {"Data": {"GetRepoBasedUpdateList_OUTPUT": {
            "Message": "Firmware versions on server match catalog, applicable updates are not present in the repository"}}},
            "JobStatus": "Completed"}
        with pytest.raises(Exception) as ex:
            self.module.get_check_mode_status(status, f_module)
        assert ex.value.args[0] == "No changes found to commit!"
        f_module.check_mode = False
        with pytest.raises(Exception) as ex:
            self.module.get_check_mode_status(status, f_module)
        assert ex.value.args[0] == "The catalog in the repository specified in the operation has the same firmware versions as currently present on the server."

    def test_update_firmware_url_redfish(self, idrac_default_args, idrac_connection_firmware_redfish_mock, mocker):
        idrac_default_args.update({"share_name": "sharename", "catalog_file_name": CATALOG,
                                   "share_user": "sharename", "share_password": SHARE_PWD,
                                   "share_mnt": "sharmnt", "reboot": True, "job_wait": True, "apply_update": True})
        f_module = self.get_module_mock(params=idrac_default_args)
        mocker.patch(MODULE_PATH + TIME_SLEEP, return_value=None)
        mocker.patch(MODULE_PATH + 'idrac_firmware.get_error_syslog', return_value=(True, "Failed to update firmware."))
        mocker.patch(MODULE_PATH + WAIT_FOR_JOB, return_value=None)
        mocker.patch(MODULE_PATH + 'idrac_firmware.get_jobid', return_value="JID_123456789")
        mocker.patch(MODULE_PATH + 'idrac_firmware.handle_HTTP_error', return_value=None)
        actions = {"Actions": {"#DellSoftwareInstallationService.InstallFromRepository": {"target": "/api/installRepository"},
                               "#DellSoftwareInstallationService.GetRepoBasedUpdateList": {"target": "/api/getRepoBasedUpdateList"}}}
        idrac_connection_firmware_redfish_mock.json_data = {"Entries": {"@odata.id": "/api/log"}, "DateTime": "2023-10-05"}
        with pytest.raises(Exception) as ex:
            self.module.update_firmware_url_redfish(f_module, idrac_connection_firmware_redfish_mock,
                                                    "https://127.0.0.1/httpshare", True, True, True, {}, actions)
        assert ex.value.args[0] == "Failed to update firmware."
        mocker.patch(MODULE_PATH + 'idrac_firmware.get_error_syslog', return_value=(False, ""))
        mocker.patch(MODULE_PATH + WAIT_FOR_JOB, return_value=(None, "Successfully updated."))
        result, msg = self.module.update_firmware_url_redfish(f_module, idrac_connection_firmware_redfish_mock,
                                                              "https://127.0.0.1/httpshare", True, True, True, {}, actions)
        assert result["update_msg"] == "Successfully updated."

    def test_get_error_syslog(self, idrac_default_args, idrac_connection_firm_mock, redfish_response_mock, mocker):
        idrac_default_args.update({"share_name": "sharename", "catalog_file_name": CATALOG,
                                   "share_user": "sharename", "share_password": SHARE_PWD,
                                   "share_mnt": "sharmnt", "reboot": True, "job_wait": True, "apply_update": True})
        self.get_module_mock(params=idrac_default_args)
        redfish_response_mock.json_data = {"Members": [{"MessageId": "SYS229"}], "Entries": {"@odata.id": "/api/log"}}
        mocker.patch(MODULE_PATH + TIME_SLEEP, return_value=None)
        result = self.module.get_error_syslog(idrac_connection_firm_mock, "", "/api/service")
        assert result[0]

    def test_update_firmware_omsdk(self, idrac_default_args, idrac_connection_firmware_redfish_mock, mocker):
        idrac_default_args.update({"share_name": "sharename", "catalog_file_name": CATALOG,
                                   "share_user": "sharename", "share_password": SHARE_PWD, "ignore_cert_warning": False,
                                   "share_mnt": "sharmnt", "reboot": True, "job_wait": True, "apply_update": True})
        f_module = self.get_module_mock(params=idrac_default_args)
        mocker.patch(MODULE_PATH + 'idrac_firmware.FileOnShare', return_value=None)
        mocker.patch(MODULE_PATH + 'idrac_firmware.get_check_mode_status', return_value=None)
        mocker.patch(MODULE_PATH + 'idrac_firmware._convert_xmltojson', return_value=([], True, False))
        status = {"job_details": {"Data": {"GetRepoBasedUpdateList_OUTPUT": {"PackageList": []}}}, "JobStatus": "Completed"}
        idrac_connection_firmware_redfish_mock.update_mgr.update_from_repo.return_value = status
        result = self.module.update_firmware_omsdk(idrac_connection_firmware_redfish_mock, f_module)
        assert result['update_msg'] == 'Successfully triggered the job to update the firmware.'
        f_module.check_mode = True
        with pytest.raises(Exception) as ex:
            self.module.update_firmware_omsdk(idrac_connection_firmware_redfish_mock, f_module)
        assert ex.value.args[0] == "Changes found to commit!"
        status.update({"JobStatus": "InProgress"})
        with pytest.raises(Exception) as ex:
            self.module.update_firmware_omsdk(idrac_connection_firmware_redfish_mock, f_module)
        assert ex.value.args[0] == "Unable to complete the firmware repository download."
        status = {"job_details": {"Data": {}, "PackageList": []}, "JobStatus": "Completed", "Status": "Failed"}
        idrac_connection_firmware_redfish_mock.update_mgr.update_from_repo.return_value = status
        with pytest.raises(Exception) as ex:
            self.module.update_firmware_omsdk(idrac_connection_firmware_redfish_mock, f_module)
        assert ex.value.args[0] == "No changes found to commit!"
        idrac_default_args.update({"apply_update": False})
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = False
        with pytest.raises(Exception) as ex:
            self.module.update_firmware_omsdk(idrac_connection_firmware_redfish_mock, f_module)
        assert ex.value.args[0] == "Unable to complete the repository update."

    @pytest.mark.parametrize("exc_type", [RuntimeError, URLError, SSLValidationError, ConnectionError, KeyError,
                                          ImportError, ValueError, TypeError, IOError, AssertionError, OSError])
    def test_main(self, idrac_default_args, idrac_connection_firmware_redfish_mock, mocker, exc_type):
        idrac_default_args.update({"share_name": "sharename", "catalog_file_name": CATALOG,
                                   "share_user": "sharename", "share_password": SHARE_PWD, "ignore_cert_warning": False,
                                   "share_mnt": "sharmnt", "reboot": True, "job_wait": True, "apply_update": True})
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = True
        idrac_connection_firmware_redfish_mock.status_code = 400
        idrac_connection_firmware_redfish_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + VALIDATE_CATALOG,
                         side_effect=exc_type('test'))
        else:
            mocker.patch(MODULE_PATH + VALIDATE_CATALOG,
                         side_effect=exc_type(TEST_HOST, 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
        if exc_type == HTTPError:
            result = self._run_module(idrac_default_args)
            assert result['failed'] is True
        elif exc_type == URLError:
            result = self._run_module(idrac_default_args)
            assert result['unreachable'] is True
        else:
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        if exc_type == HTTPError:
            assert 'error_info' in result
        assert 'msg' in result
