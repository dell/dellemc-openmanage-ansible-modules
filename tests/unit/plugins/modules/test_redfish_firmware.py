# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.2.0
# Copyright (C) 2020-2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

import sys

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import redfish_firmware
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from unittest.mock import MagicMock
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO, BytesIO
from ansible.module_utils._text import to_text
from unittest.mock import patch, mock_open

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
JOB_URI = "JobService/Jobs/{job_id}"
FIRMWARE_DATA = "multipart/form-data"
HTTPS_IMAGE_URI = "https://home/firmware_repo/component.exe"
HTTPS_ADDRESS_DELL = "https://dell.com"
LOCAL_IMAGE_URI = "/home/firmware_repo/component.exe"


@pytest.fixture
def redfish_firmware_connection_mock(mocker, redfish_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'redfish_firmware.Redfish')
    redfish_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    redfish_connection_mock_obj.invoke_request.return_value = redfish_response_mock
    return redfish_connection_mock_obj


class TestRedfishFirmware(FakeAnsibleModule):
    module = redfish_firmware

    @pytest.fixture
    def os_mock(self, mocker):
        try:
            fi_mock = mocker.patch(
                MODULE_PATH + 'redfish_firmware.payload_file.get("file")')
        except AttributeError:
            fi_mock = MagicMock()
        obj = MagicMock()
        fi_mock.read.return_value = obj
        return fi_mock

    update_status = {
        "@odata.context": "/redfish/v1/$metadata#DellJob.DellJob",
        "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_824742691385",
        "@odata.type": "#DellJob.v1_0_2.DellJob",
        "CompletionTime": "2020-02-23T21:51:30",
        "Description": "Job Instance",
        "EndTime": None,
        "Id": "JID_824742691385",
        "JobState": "Completed",
        "JobType": "RepositoryUpdate",
        "Message": "Job completed successfully.",
        "MessageArgs": [
            "NA"
        ],
        "MessageArgs@odata.count": 1,
        "MessageId": "RED001",
        "Name": "Repository Update",
        "PercentComplete": 100,
        "StartTime": "TIME_NOW",
        "Status": "Success",
        "TargetSettingsURI": None,
        "job_details": {
            "Data": {
                "StatusCode": 200,
                "body": {
                    "@Message.ExtendedInfo": [
                        {
                            "Message": "Successfully Completed Request",
                            "MessageArgs": [],
                            "MessageArgs@odata.count": 0,
                            "MessageId": "Base.1.5.Success",
                            "RelatedProperties": [],
                            "RelatedProperties@odata.count": 0,
                            "Resolution": "None",
                            "Severity": "OK"
                        }
                    ],
                    "PackageList": [
                        {
                            "BaseLocation": None,
                            "ComponentID": "18981",
                            "ComponentType": "APAC",
                            "Criticality": "3",
                            "DisplayName": "Dell OS Driver Pack",
                            "JobID": "JID_824746139010",
                            "PackageName": "Drivers-for-OS-Deployment_Application_X0DW6_WN64_19.10.12_A00.EXE",
                            "PackageVersion": "19.10.12",
                            "RebootType": "NONE",
                            "Target": "DCIM:INSTALLED#802__DriverPack.Embedded.1:LC.Embedded.1"
                        }]

                }
            }
        }
    }

    def test_main_redfish_firmware_success_case(self, redfish_firmware_connection_mock, redfish_default_args, mocker,
                                                redfish_response_mock):
        redfish_default_args.update({"image_uri": "/home/firmware_repo/component.exe", "job_wait": False})
        redfish_firmware_connection_mock.headers.get("Location").return_value = "https://multipart/form-data"
        redfish_firmware_connection_mock.headers.get("Location").split().return_value = FIRMWARE_DATA
        mocker.patch(MODULE_PATH + 'redfish_firmware.firmware_update',
                     return_value=redfish_response_mock)
        redfish_response_mock.json_data = {"image_uri": HTTPS_IMAGE_URI}
        redfish_response_mock.status_code = 201
        redfish_response_mock.success = True
        result = self._run_module(redfish_default_args)
        assert result['changed'] is True
        assert result['msg'] == 'Successfully submitted the firmware update task.'
        assert result['task']['id'] == redfish_response_mock.headers.get().split().__getitem__()
        assert result['task']['uri'] == JOB_URI.format(job_id=redfish_response_mock.headers.get().split().__getitem__())

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_main_redfish_firmware_exception_handling_case(self, exc_type, mocker, redfish_default_args,
                                                           redfish_firmware_connection_mock,
                                                           redfish_response_mock):
        redfish_default_args.update({"image_uri": "/home/firmware_repo/component.exe", "job_wait_timeout": 0})
        redfish_response_mock.json_data = {"value": [{"image_uri": "/home/firmware_repo/component.exe"}]}
        redfish_response_mock.status_code = 400
        redfish_response_mock.success = False
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'redfish_firmware.firmware_update',
                         side_effect=exc_type('test'))
        else:
            mocker.patch(MODULE_PATH + 'redfish_firmware.firmware_update',
                         side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
        if exc_type == HTTPError:
            result = self._run_module(redfish_default_args)
        else:
            result = self._run_module_with_fail_json(redfish_default_args)
        assert 'task' not in result
        assert 'msg' in result
        assert result['failed'] is True
        if exc_type == HTTPError:
            assert 'error_info' in result

    @pytest.mark.parametrize("generation", [16, 17])
    def test_get_update_service_target_success_case(self, redfish_default_args, redfish_firmware_connection_mock,
                                                    redfish_response_mock, generation):
        redfish_default_args.update({"transfer_protocol": "HTTP", "job_wait_timeout": 0})
        f_module = self.get_module_mock(params=redfish_default_args)
        redfish_response_mock.status_code = 200
        redfish_response_mock.success = True
        redfish_response_mock.json_data = {
            "Actions": {
                "#UpdateService.SimpleUpdate": {
                    "TransferProtocol@Redfish.AllowableValues": ["HTTP"],
                    "target": ""
                }
            },
            "transfer_protocol": "HTTP",
            "HttpPushUri": HTTPS_ADDRESS_DELL,
            "MultipartHttpPushUri": HTTPS_ADDRESS_DELL,
            "FirmwareInventory": {
                "@odata.id": "2134"
            }
        }
        result = self.module._get_update_service_target(redfish_firmware_connection_mock, f_module, generation)
        assert result == ('2134', HTTPS_ADDRESS_DELL, '')

    @pytest.mark.parametrize("generation", [16, 17])
    def test_get_update_service_target_uri_none_case(self, redfish_default_args, redfish_firmware_connection_mock,
                                                     redfish_response_mock, generation):
        redfish_default_args.update({"transfer_protocol": "HTTP", "job_wait_timeout": 0})
        f_module = self.get_module_mock(params=redfish_default_args)
        redfish_response_mock.status_code = 200
        redfish_response_mock.success = True
        redfish_response_mock.json_data = {
            "Actions": {
                "#UpdateService.SimpleUpdate": {
                    "TransferProtocol@Redfish.AllowableValues": ["HTTP"],
                    "target": None
                }
            },
            "transfer_protocol": "HTTP",
            "HttpPushUri": None,
            "MultipartHttpPushUri": None,
            "FirmwareInventory": {
                "@odata.id": None
            }
        }
        with pytest.raises(Exception) as ex:
            self.module._get_update_service_target(redfish_firmware_connection_mock, f_module, generation)
        assert ex.value.args[0] == "Target firmware version does not support redfish firmware update."

    @pytest.mark.parametrize("generation", [16, 17])
    def test_get_update_service_target_failed_case(self, redfish_default_args, redfish_firmware_connection_mock,
                                                   redfish_response_mock, generation):
        redfish_default_args.update({"transfer_protocol": "HTTP", "job_wait_timeout": 0})
        f_module = self.get_module_mock(params=redfish_default_args)
        redfish_response_mock.status_code = 200
        redfish_response_mock.success = True
        redfish_response_mock.json_data = {
            "Actions": {
                "#UpdateService.SimpleUpdate": {
                    "TransferProtocol@Redfish.AllowableValues": [""]
                }
            },
            "transfer_protocol": "HTTP",
            "HttpPushUri": HTTPS_ADDRESS_DELL,
            "MultipartHttpPushUri": HTTPS_ADDRESS_DELL,
            "FirmwareInventory": {
                "@odata.id": "2134"
            }
        }
        with pytest.raises(Exception) as ex:
            self.module._get_update_service_target(redfish_firmware_connection_mock, f_module, generation)
        assert ex.value.args[0] == "Target firmware version does not support {0} protocol.".format("HTTP")

    def test_firmware_update_success_case01(self, redfish_default_args, redfish_firmware_connection_mock,
                                            redfish_response_mock, mocker):
        mocker.patch(MODULE_PATH + 'redfish_firmware._get_update_service_target',
                     return_value=('2134', HTTPS_ADDRESS_DELL, 'redfish'))
        redfish_default_args.update({"image_uri": HTTPS_IMAGE_URI,
                                     "transfer_protocol": "HTTP", "timeout": 0, "job_wait_timeout": 0})
        f_module = self.get_module_mock(params=redfish_default_args)
        redfish_response_mock.status_code = 200
        redfish_response_mock.success = True
        redfish_response_mock.json_data = {"image_uri": HTTPS_IMAGE_URI,
                                           "transfer_protocol": "HTTP"}
        result = self.module.firmware_update(redfish_firmware_connection_mock, f_module)
        assert result == redfish_response_mock

    def test_firmware_update_success_case02(self, redfish_default_args, redfish_firmware_connection_mock,
                                            redfish_response_mock, mocker):
        mocker.patch(MODULE_PATH + "redfish_firmware._get_update_service_target",
                     return_value=('2134', HTTPS_ADDRESS_DELL, 'multipart/form-data'))
        mocker.patch("ansible_collections.dellemc.openmanage.plugins.modules.redfish_firmware._encode_form_data",
                     return_value=({"file": (3, HTTPS_ADDRESS_DELL, FIRMWARE_DATA)}, FIRMWARE_DATA))
        redfish_default_args.update({"image_uri": HTTPS_IMAGE_URI,
                                     "transfer_protocol": "HTTP", "timeout": 0, "job_wait_timeout": 0})
        f_module = self.get_module_mock(params=redfish_default_args)
        redfish_response_mock.status_code = 200
        redfish_response_mock.success = True
        redfish_response_mock.json_data = {"image_uri": HTTPS_IMAGE_URI,
                                           "transfer_protocol": "HTTP"}
        if sys.version_info.major == 3:
            builtin_module_name = 'builtins'
        else:
            builtin_module_name = '__builtin__'
        with patch("{0}.open".format(builtin_module_name), mock_open(read_data="data")) as mock_file:
            result = self.module.firmware_update(redfish_firmware_connection_mock, f_module)
        assert result == redfish_response_mock

    @pytest.mark.parametrize("params", [{"ip": "192.161.1.1:443"}, {"ip": "192.161.1.1"},
                                        {"ip": "82f5:d985:a2d5:f0c3:5392:cc52:27d1:4da6"},
                                        {"ip": "[82f5:d985:a2d5:f0c3:5392:cc52:27d1:4da6]"},
                                        {"ip": "[82f5:d985:a2d5:f0c3:5392:cc52:27d1:4da6]:443"}])
    def test_firmware_update_success_case03(self, params, redfish_default_args, redfish_firmware_connection_mock,
                                            redfish_response_mock, mocker):
        mocker.patch(MODULE_PATH + "redfish_firmware._get_update_service_target",
                     return_value=('2134', HTTPS_ADDRESS_DELL, 'multipart/form-data'))
        mocker.patch(MODULE_PATH + "redfish_firmware._encode_form_data",
                     return_value=({"file": (3, HTTPS_ADDRESS_DELL, FIRMWARE_DATA)}, FIRMWARE_DATA))
        redfish_default_args.update({"baseuri": params["ip"], "image_uri": HTTPS_IMAGE_URI,
                                     "transfer_protocol": "HTTP", "timeout": 0, "job_wait_timeout": 0})
        f_module = self.get_module_mock(params=redfish_default_args)
        redfish_response_mock.status_code = 201
        redfish_response_mock.success = True
        redfish_response_mock.json_data = {"image_uri": HTTPS_IMAGE_URI,
                                           "transfer_protocol": "HTTP"}
        if sys.version_info.major == 3:
            builtin_module_name = 'builtins'
        else:
            builtin_module_name = '__builtin__'
        with patch("{0}.open".format(builtin_module_name), mock_open(read_data="data")) as mock_file:
            result = self.module.firmware_update(redfish_firmware_connection_mock, f_module)
        assert result == redfish_response_mock

    def test_encode_form_data(self, mocker):
        payload_file = {'UpdateFile': ('image.exe', BytesIO(b'example data'), 'application/octet-stream')}
        payload_file_header = 'UpdateFile'
        mocker.patch('urllib3.filepost.encode_multipart_formdata', return_value=(b'example data', 'multipart/form-data'))
        result = redfish_firmware._encode_form_data(payload_file, payload_file_header)
        assert b'example data' in result[0]
        assert 'multipart/form-data' in result[1]

    @pytest.mark.parametrize("generation", [16, 17])
    def test_firmware_update_success_case04(self, redfish_default_args, redfish_firmware_connection_mock,
                                            redfish_response_mock, mocker, generation):
        mocker.patch(MODULE_PATH + "redfish_firmware._get_update_service_target",
                     return_value=('2134', HTTPS_ADDRESS_DELL, 'multipart/form-data'))
        mocker.patch(MODULE_PATH + "redfish_firmware._encode_form_data",
                     return_value=({"file": (3, HTTPS_ADDRESS_DELL, FIRMWARE_DATA)}, FIRMWARE_DATA))
        redfish_default_args.update({"image_uri": LOCAL_IMAGE_URI,
                                    "transfer_protocol": "HTTP", "timeout": 0, "job_wait_timeout": 0})
        f_module = self.get_module_mock(params=redfish_default_args)
        redfish_response_mock.status_code = 201
        redfish_response_mock.success = True
        redfish_response_mock.json_data = {"image_uri": LOCAL_IMAGE_URI,
                                           "transfer_protocol": "HTTP"}
        if sys.version_info.major == 3:
            builtin_module_name = 'builtins'
        else:
            builtin_module_name = '__builtin__'
        with patch("{0}.open".format(builtin_module_name), mock_open(read_data="data")):
            redfish_firmware_connection_mock.get_server_generation = (generation, "firm_ver", "hw_model")
            result = self.module.firmware_update(redfish_firmware_connection_mock, f_module)
        assert result == redfish_response_mock
