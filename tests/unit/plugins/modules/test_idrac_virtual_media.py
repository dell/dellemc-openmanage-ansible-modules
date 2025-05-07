# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 6.3.0
# Copyright (C) 2022-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_virtual_media
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from io import StringIO
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import AnsibleFailJSonException

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
ISO_PATH = "//XX.XX.XX.XX/path/file.iso"
ISO_IMAGE_PATH = "//XX.XX.XX.XX/path/image_file.iso"
SLEEP = 'idrac_virtual_media.time.sleep'
PAYLOAD_DATA = 'idrac_virtual_media.get_payload_data'
GET_INFO = 'idrac_virtual_media.get_virtual_media_info'
SAMPLE_IMAGE = "\\\\XX.XX.XX.XX\\path\\image.iso"


@pytest.fixture
def virtual_media_conn_mock(mocker, redfish_response_mock):
    idrac_conn_mock = mocker.patch(MODULE_PATH + 'idrac_virtual_media.iDRACRedfishAPI')
    idrac_conn_mock_obj = idrac_conn_mock.return_value.__enter__.return_value
    idrac_conn_mock_obj.invoke_request.return_value = redfish_response_mock
    return idrac_conn_mock_obj


class TestVirtualMedia(FakeAnsibleModule):

    module = idrac_virtual_media

    def test_validate_params(self, virtual_media_conn_mock, redfish_response_mock, idrac_default_args):
        idrac_default_args.update(
            {"virtual_media": [{"index": 1, "insert": True, "image": "//XX.XX.XX.XX/path/image.iso"}]})
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as err:
            self.module._validate_params(f_module, {"index": 1, "insert": True,
                                                    "image": "//XX.XX.XX.XX/path/image.iso"}, "140")
        assert err.value.args[0] == "CIFS share required username and password."
        idrac_default_args.update({"virtual_media": [{"index": 1, "insert": True, "username": "user", "password": "pwd",
                                                      "image": SAMPLE_IMAGE}]})
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module._validate_params(f_module, {"password": "pwd", "insert": True, "username": "usr",
                                                         "image": SAMPLE_IMAGE, "index": 1},
                                              "141")
        assert result is None
        with pytest.raises(AnsibleFailJSonException) as exc:
            idrac_default_args.update({"virtual_media": [{"index": 1, "insert": True, "username": "user", "password": "pwd",
                                                          "image": SAMPLE_IMAGE}]})
            f_module = self.get_module_mock(params=idrac_default_args)
            self.module._validate_params(f_module, {"password": "pwd", "insert": True, "username": "usr",
                                                    "image": SAMPLE_IMAGE, "index": 1},
                                         "139")
        assert exc.value.args[0] == "The system does not support the CIFS network share feature."
        with pytest.raises(AnsibleFailJSonException) as exc:
            idrac_default_args.update({"virtual_media": [{"index": 1, "insert": True, "username": "user", "password": "pwd",
                                                          "image": SAMPLE_IMAGE}]})
            f_module = self.get_module_mock(params=idrac_default_args)
            self.module._validate_params(f_module, {"password": "pwd", "insert": True, "username": "usr",
                                                    "image": "https://XX.XX.XX.XX//path//image.iso", "index": 1},
                                         "139")

        assert exc.value.args[0] == "The system does not support the HTTPS network share feature with credentials."

    def test_get_virtual_media_info(self, virtual_media_conn_mock, redfish_response_mock, idrac_default_args):
        redfish_response_mock.json_data = {
            "RedfishVersion": "1.13.1",
            "VirtualMedia": {"@odata.id": "/redfish/v1/Systems/System.Embedded.1/VirtualMedia"},
            "Members": [{"Inserted": False, "Image": None},
                        {"Inserted": True, "Image": "//XX.XX.XX.XX/file_path/file.iso"}]
        }
        resp, vr_id, rd_version = self.module.get_virtual_media_info(virtual_media_conn_mock)
        assert vr_id == "system"
        redfish_response_mock.json_data.update({"RedfishVersion": "1.11.1"})
        resp, vr_id, rd_version = self.module.get_virtual_media_info(virtual_media_conn_mock)
        assert vr_id == "manager"

    def test_get_payload_data(self, virtual_media_conn_mock, redfish_response_mock, idrac_default_args):
        idrac_default_args.update({"virtual_media": [{"insert": True, "image": ISO_PATH}]})
        each = {"insert": True, "image": ISO_PATH, "index": 1, "media_type": "CD"}
        vr_member = [{"Inserted": True, "Image": ISO_IMAGE_PATH,
                      "UserName": "username", "Password": "password", "Id": "CD", "MediaTypes": ["CD", "DVD"]}]
        is_change, input_vr_mem, vr_mem, unsup_media = self.module.get_payload_data(each, vr_member, "manager")
        assert is_change is True
        assert input_vr_mem == {'Inserted': True, 'Image': '//XX.XX.XX.XX/path/file.iso'}
        assert vr_mem == {'Inserted': True, 'Image': '//XX.XX.XX.XX/path/image_file.iso', 'UserName': 'username',
                          'Password': 'password', 'Id': 'CD', 'MediaTypes': ['CD', 'DVD']}
        each.update({"username": "user_name", "password": "password", "domain": "domain",
                     "image": "XX.XX.XX.XX:/file_path/image.iso"})
        is_change, input_vr_mem, vr_mem, unsup_media = self.module.get_payload_data(each, vr_member, "manager")
        assert is_change is True
        each.update({"media_type": "USBStick"})
        is_change, input_vr_mem, vr_mem, unsup_media = self.module.get_payload_data(each, vr_member, "manager")
        assert unsup_media == 1
        each = {"insert": False, "index": 1}
        is_change, input_vr_mem, vr_mem, unsup_media = self.module.get_payload_data(each, vr_member, "manager")
        assert is_change is True
        is_change, input_vr_mem, vr_mem, unsup_media = self.module.get_payload_data(each, vr_member, "system")
        assert is_change is True
        each.update({"username": "user_name", "password": "password", "domain": "domain", "media_type": "CD",
                     "image": "XX.XX.XX.XX:/file_path/image.img", "insert": True})
        is_change, input_vr_mem, vr_mem, unsup_media = self.module.get_payload_data(each, vr_member, "manager")
        assert unsup_media == 1
        each.update({"username": "user_name", "password": "password", "domain": "domain", "media_type": "DVD",
                     "image": "XX.XX.XX.XX:/file_path/image.img", "insert": True})
        is_change, input_vr_mem, vr_mem, unsup_media = self.module.get_payload_data(each, vr_member, "manager")
        assert unsup_media == 1

    def test_domain_name(self, virtual_media_conn_mock, redfish_response_mock, idrac_default_args):
        idrac_default_args.update({"virtual_media": [{"insert": True, "image": ISO_PATH}]})
        each = {"insert": True, "image": ISO_PATH, "index": 1, "media_type": "CD",
                "domain": "domain", "username": "user", "password": "pwd"}
        vr_member = [{"Inserted": True, "Image": ISO_IMAGE_PATH, "domain": "domain",
                      "UserName": "username", "Password": "password", "Id": "CD", "MediaTypes": ["CD", "DVD"]}]
        is_change, input_vr_mem, vr_mem, unsup_media = self.module.get_payload_data(each, vr_member, "manager")
        assert is_change is True

    def test_virtual_media_operation(self, virtual_media_conn_mock, redfish_response_mock, idrac_default_args, mocker):
        idrac_default_args.update({"virtual_media": [{"insert": True, "image": ISO_PATH}],
                                   "force": True})
        f_module = self.get_module_mock(params=idrac_default_args)
        mocker.patch(MODULE_PATH + SLEEP, return_value=None)
        payload = [{
            "vr_mem": {"Inserted": True, "Actions": {
                "#VirtualMedia.EjectMedia": {
                    "target": "/redfish/v1/Systems/System.Embedded.1/VirtualMedia/1/Actions/VirtualMedia.EjectMedia"},
                "#VirtualMedia.InsertMedia": {
                    "target": "/redfish/v1/Systems/System.Embedded.1/VirtualMedia/1/Actions/VirtualMedia.InsertMedia"}
            }},
            "payload": {"Inserted": True, "Image": "https://XX.XX.XX.XX/file_path/file.iso"},
            "input": {"index": 1, "insert": True, "image": ISO_PATH, "force": True}
        }]
        result = self.module.virtual_media_operation(virtual_media_conn_mock, f_module, payload, "manager")
        assert result == []
        idrac_default_args.update({"force": False})
        result = self.module.virtual_media_operation(virtual_media_conn_mock, f_module, payload, "manager")
        assert result == []
        payload[0]["vr_mem"].update({"Inserted": False})
        result = self.module.virtual_media_operation(virtual_media_conn_mock, f_module, payload, "manager")
        assert result == []
        payload[0]["vr_mem"].update({"Inserted": True})
        payload[0]["payload"].update({"Inserted": False})
        result = self.module.virtual_media_operation(virtual_media_conn_mock, f_module, payload, "manager")
        assert result == []

    @pytest.mark.parametrize("exc_type", [HTTPError])
    def test_virtual_media_operation_http(self, virtual_media_conn_mock, redfish_response_mock,
                                          idrac_default_args, mocker, exc_type):
        idrac_default_args.update({"virtual_media": [{"insert": True, "image": ISO_PATH}],
                                   "force": True})
        f_module = self.get_module_mock(params=idrac_default_args)
        mocker.patch(MODULE_PATH + SLEEP, return_value=None)
        payload = [{
            "vr_mem": {"Inserted": True, "Actions": {
                "#VirtualMedia.EjectMedia": {
                    "target": "/redfish/v1/Systems/System.Embedded.1/VirtualMedia/CD/Actions/VirtualMedia.EjectMedia"},
                "#VirtualMedia.InsertMedia": {
                    "target": "/redfish/v1/Systems/System.Embedded.1/VirtualMedia/CD/Actions/VirtualMedia.InsertMedia"}
            }},
            "payload": {"Inserted": True, "Image": "https://XX.XX.XX.XX/file_path/file.iso"},
            "input": {"index": 1, "insert": True, "image": ISO_PATH, "force": True}
        }]
        if exc_type == HTTPError:
            mocker.patch(MODULE_PATH + 'idrac_virtual_media.json.load', return_value={
                "error": {"@Message.ExtendedInfo": [{"MessageId": "VRM0012"}]}
            })
            json_str = to_text(json.dumps({"data": "out"}))
            mocker.patch(
                MODULE_PATH + SLEEP,
                side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                     {"accept-type": "application/json"}, StringIO(json_str)))
            result = self.module.virtual_media_operation(virtual_media_conn_mock, f_module, payload, "system")
            assert result == [{'@Message.ExtendedInfo': [{'MessageId': 'VRM0012'}]}]

    def test_virtual_media(self, virtual_media_conn_mock, redfish_response_mock, idrac_default_args, mocker):
        vr_member = [{"Inserted": True, "Image": ISO_IMAGE_PATH,
                      "UserName": "username", "Password": "password", "Id": "CD", "MediaTypes": ["CD", "DVD"]}]
        mocker.patch(MODULE_PATH + 'idrac_virtual_media.virtual_media_operation', return_value=[])
        mocker.patch(MODULE_PATH + 'idrac_virtual_media._validate_params', return_value=None)
        mocker.patch(MODULE_PATH + PAYLOAD_DATA, return_value=(True, {}, {}, 1))
        idrac_default_args.update({"virtual_media": [{"insert": True, "image": ISO_PATH}],
                                   "force": True})
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as ex:
            self.module.virtual_media(virtual_media_conn_mock, f_module, vr_member, "manager", "141")
        assert ex.value.args[0] == "Unable to complete the virtual media operation because unsupported " \
                                   "media type provided for index 1"
        idrac_default_args.update({"virtual_media": [{"insert": True, "image": "//XX.XX.XX.XX/path/file.img"}],
                                   "force": True})
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as ex:
            self.module.virtual_media(virtual_media_conn_mock, f_module, vr_member, "manager", "141")
        assert ex.value.args[0] == "Unable to complete the virtual media operation because " \
                                   "unsupported media type provided for index 1"
        with pytest.raises(Exception) as ex:
            self.module.virtual_media(virtual_media_conn_mock, f_module, vr_member, "system", "141")
        assert ex.value.args[0] == "Unable to complete the virtual media operation because " \
                                   "unsupported media type provided for index 1"
        idrac_default_args.update({"virtual_media": [{"insert": True, "image": ISO_PATH,
                                                      "index": 1, "media_type": "CD"}], "force": True})
        f_module = self.get_module_mock(params=idrac_default_args)
        mocker.patch(MODULE_PATH + PAYLOAD_DATA, return_value=(True, {}, {}, None))
        result = self.module.virtual_media(virtual_media_conn_mock, f_module, vr_member, "manager", "141")
        assert result == []
        result = self.module.virtual_media(virtual_media_conn_mock, f_module, vr_member, "system", "141")
        assert result == []
        idrac_default_args.update({"virtual_media": [{"insert": False, "image": None,
                                                      "index": None, "media_type": "CD"}], "force": True})
        f_module = self.get_module_mock(params=idrac_default_args)
        mocker.patch(MODULE_PATH + PAYLOAD_DATA, return_value=(True, {}, {}, None))
        result = self.module.virtual_media(virtual_media_conn_mock, f_module, vr_member, "manager", "141")
        assert result == []
        f_module.check_mode = True
        mocker.patch(MODULE_PATH + PAYLOAD_DATA,
                     return_value=(True, {"Insert": True}, {}, None))
        with pytest.raises(Exception) as ex:
            self.module.virtual_media(virtual_media_conn_mock, f_module, vr_member, "manager", "141")
        assert ex.value.args[0] == "Changes found to be applied."
        idrac_default_args.update({"virtual_media": [{"insert": True, "image": ISO_PATH,
                                                      "index": 1, "media_type": "CD"}], "force": False})
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = True
        mocker.patch(MODULE_PATH + PAYLOAD_DATA, return_value=(False, {}, {}, None))
        with pytest.raises(Exception) as ex:
            self.module.virtual_media(virtual_media_conn_mock, f_module, vr_member, "manager", "141")
        assert ex.value.args[0] == "No changes found to be applied."

    def test_main_success(self, virtual_media_conn_mock, redfish_response_mock, idrac_default_args, mocker):
        idrac_default_args.update({"virtual_media": [
            {"insert": True, "image": "https://XX.XX.XX.XX/path/file.iso"},
            {"insert": True, "image": "YY.YY.YY.YY:/file/file.iso"}], "force": True})
        mocker.patch(MODULE_PATH + GET_INFO,
                     return_value=([{"Insert": True}, {"Insert": True}], "manager", "141"))
        with pytest.raises(Exception) as ex:
            self._run_module(idrac_default_args)
        assert ex.value.args[0]["msg"] == "Unable to complete the operation because the virtual media settings " \
                                          "provided exceeded the maximum limit."
        mocker.patch(MODULE_PATH + 'idrac_virtual_media.virtual_media', return_value=[])
        idrac_default_args.update({"virtual_media": [{"insert": True, "image": "https://XX.XX.XX.XX/path/file.iso"}],
                                   "force": True})
        result = self._run_module(idrac_default_args)
        assert result == {'changed': True, 'msg': 'Successfully performed the virtual media operation.'}
        mocker.patch(MODULE_PATH + 'idrac_virtual_media.virtual_media', return_value=["error"])
        with pytest.raises(Exception) as ex:
            self._run_module(idrac_default_args)
        assert ex.value.args[0]["msg"] == "Unable to complete the virtual media operation."

    @pytest.mark.parametrize("exc_type", [HTTPError, URLError, ValueError, RuntimeError, SSLValidationError,
                                          ConnectionError, KeyError, ImportError, ValueError, TypeError])
    def test_main_exception(self, virtual_media_conn_mock, redfish_response_mock, idrac_default_args, mocker, exc_type):
        idrac_default_args.update({"virtual_media": [{"index": 1, "insert": False}]})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError]:
            mocker.patch(MODULE_PATH + GET_INFO, side_effect=exc_type('test'))
        else:
            mocker.patch(
                MODULE_PATH + GET_INFO,
                side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                     {"accept-type": "application/json"}, StringIO(json_str)))
        if not exc_type == URLError:
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result
