# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 6.0.0
# Copyright (C) 2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
import os
import tempfile
from io import StringIO

import pytest
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_attributes
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from mock import MagicMock

SUCCESS_MSG = "Successfully updated the attributes."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_MSG = "Changes found to be applied."
SYSTEM_ID = "System.Embedded.1"
MANAGER_ID = "iDRAC.Embedded.1"
LC_ID = "LifecycleController.Embedded.1"
IDRAC_URI = "/redfish/v1/Managers/{res_id}/Oem/Dell/DellAttributes/{attr_id}"
MANAGERS_URI = "/redfish/v1/Managers"
MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_attributes.'
UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.'


@pytest.fixture
def idrac_redfish_mock_for_attr(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestIdracAttributes(FakeAnsibleModule):
    module = idrac_attributes

    @pytest.fixture
    def idrac_attributes_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_attributes_mock(self, mocker, idrac_attributes_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_attributes_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_attributes_mock
        return idrac_conn_mock

    @pytest.mark.parametrize("params", [{"id": "iDRAC.Embedded.1", "attr": {'SNMP.1.AgentCommunity': 'Disabled'},
                                         "uri_dict":
                                             {"iDRAC.Embedded.1": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/iDRAC.Embedded.1",
                                              "System.Embedded.1": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/System.Embedded.1",
                                              "LifecycleController.Embedded.1":
                                                  "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/LifecycleController.Embedded.1"},
                                         "response_attr": {"SNMP.1.AgentCommunity": "Disabled"}}])
    def test_get_response_attr(self, params, idrac_redfish_mock_for_attr, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        diff, response_attr = self.module.get_response_attr(idrac_redfish_mock_for_attr, params["id"], params["attr"], params["uri_dict"])
        assert response_attr.keys() == params["response_attr"].keys()

    @pytest.mark.parametrize("params", [{"res_id": "iDRAC.Embedded.1", "attr": {'SNMP.1.AgentCommunity': 'public'},
                                         "uri_dict": {
                                             "iDRAC.Embedded.1": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/iDRAC.Embedded.1",
                                             "System.Embedded.1": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/System.Embedded.1",
                                             "LifecycleController.Embedded.1":
                                                 "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/LifecycleController.Embedded.1"},
                                         "response_attr": {"SNMP.1.AgentCommunity": "public"},
                                         "mparams": {'idrac_attributes': {"SNMP.1.AgentCommunity": "public"}
                                                     }
                                         }])
    def _test_fetch_idrac_uri_attr(self, params, idrac_redfish_mock_for_attr, idrac_default_args):
        idrac_default_args.update(params.get('mparams'))
        f_module = self.get_module_mock(params=idrac_default_args)
        diff, uri_dict, idrac_response_attr, system_response_attr, lc_response_attr =\
            self.module.fetch_idrac_uri_attr(idrac_redfish_mock_for_attr, f_module, params["res_id"])
        assert idrac_response_attr.keys() == params["response_attr"].keys()

    @pytest.mark.parametrize("params", [{"res_id": "iDRAC.Embedded.1", "attr": {'SNMP.1.AgentCommunity': 'Disabled'},
                                         "uri_dict": {
                                             "iDRAC.Embedded.1": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/iDRAC.Embedded.1",
                                             "System.Embedded.1": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/System.Embedded.1",
                                             "LifecycleController.Embedded.1":
                                                 "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/LifecycleController.Embedded.1"},
                                         "response_attr": {"ThermalSettings.1.ThermalProfile": "Sound Cap"},
                                         "mparams": {'system_attributes': {"ThermalSettings.1.ThermalProfile": "Sound Cap"}
                                                     }}])
    def _test_fetch_idrac_uri_attr_succes_case01(self, params, idrac_redfish_mock_for_attr, idrac_default_args):
        idrac_default_args.update(params.get('mparams'))
        f_module = self.get_module_mock(params=idrac_default_args)
        diff, uri_dict, idrac_response_attr, system_response_attr, lc_response_attr = self.module.fetch_idrac_uri_attr(
            idrac_redfish_mock_for_attr, f_module, params["res_id"])
        assert system_response_attr.keys() == params["response_attr"].keys()

    @pytest.mark.parametrize("params", [{"res_id": "iDRAC.Embedded.1", "attr": {'SNMP.1.AgentCommunity': 'Disabled'},
                                         "uri_dict": {
                                             "iDRAC.Embedded.1": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/iDRAC.Embedded.1",
                                             "System.Embedded.1": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/System.Embedded.1",
                                             "LifecycleController.Embedded.1":
                                                 "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/LifecycleController.Embedded.1"},
                                         "response_attr": {"LCAttributes.1.AutoUpdate": "Enabled"},
                                         "mparams": {'lifecycle_controller_attributes': {"LCAttributes.1.AutoUpdate": "Enabled"}
                                                     }}])
    def _test_fetch_idrac_uri_attr_succes_case02(self, params, idrac_redfish_mock_for_attr, idrac_default_args):
        idrac_default_args.update(params.get('mparams'))
        f_module = self.get_module_mock(params=idrac_default_args)
        diff, uri_dict, idrac_response_attr, system_response_attr, lc_response_attr = self.module.fetch_idrac_uri_attr(
            idrac_redfish_mock_for_attr, f_module, params["res_id"])
        assert lc_response_attr.keys() == params["response_attr"].keys()

    @pytest.mark.parametrize("params", [{"res_id": "iDRAC.Embedded.1", "attr": {'SNMP.1.AgentCommunity': 'Disabled'},
                                         "uri_dict": {
                                             "iDRAC.Embedded.1": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/iDRAC.Embedded.1",
                                             "System.Embedded.1": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/System.Embedded.1",
                                             "LifecycleController.Embedded.1":
                                                 "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/LifecycleController.Embedded.1"},
                                         "response_attr": {"SNMP.1.AgentCommunity": "Disabled"},
                                         "mparams": {'idrac_attributes': {"SNMP.1.AgentCommunity": "Enabled"}
                                                     },
                                         "system_response_attr": {},
                                         "lc_response_attr": {},
                                         "resp": {
        "iDRAC": {
            "@Message.ExtendedInfo": [
                {
                    "Message": "The request completed successfully.",
                    "MessageArgs": [],
                    "MessageArgs@odata.count": 0,
                    "MessageId": "Base.1.12.Success",
                    "RelatedProperties": [],
                    "RelatedProperties@odata.count": 0,
                    "Resolution": "None",
                    "Severity": "OK"
                },
                {
                    "Message": "The operation successfully completed.",
                    "MessageArgs": [],
                    "MessageArgs@odata.count": 0,
                    "MessageId": "IDRAC.2.7.SYS413",
                    "RelatedProperties": [],
                    "RelatedProperties@odata.count": 0,
                    "Resolution": "No response action is required.",
                    "Severity": "Informational"
                }
            ]
        }
    }}])
    def test_update_idrac_attributes(self, params, idrac_redfish_mock_for_attr, idrac_default_args):
        idrac_default_args.update(params.get('mparams'))
        f_module = self.get_module_mock(params=idrac_default_args)
        resp = self.module.update_idrac_attributes(idrac_redfish_mock_for_attr, f_module, params["uri_dict"],
                                                   params["response_attr"], params["system_response_attr"],
                                                   params["lc_response_attr"])
        assert resp.keys() == params["resp"].keys()

    @pytest.mark.parametrize("params", [{"res_id": "iDRAC.Embedded.1",
                                         "uri_dict": {
                                             "iDRAC.Embedded.1": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/iDRAC.Embedded.1",
                                             "System.Embedded.1": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/System.Embedded.1",
                                             "LifecycleController.Embedded.1":
                                                 "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/LifecycleController.Embedded.1"},
                                         "system_response_attr": {"ThermalSettings.1.ThermalProfile": "Sound Cap"},
                                         "mparams": {'system_attributes': {"ThermalSettings.1.ThermalProfile": "Sound Cap"}
                                                     },
                                         "idrac_response_attr": {},
                                         "lc_response_attr": {},
                                         "resp": {
                                             "System": {
                                                 "@Message.ExtendedInfo": [
                                                     {
                                                         "Message": "The request completed successfully.",
                                                         "MessageArgs": [],
                                                         "MessageArgs@odata.count": 0,
                                                         "MessageId": "Base.1.12.Success",
                                                         "RelatedProperties": [],
                                                         "RelatedProperties@odata.count": 0,
                                                         "Resolution": "None",
                                                         "Severity": "OK"
                                                     },
                                                     {
                                                         "Message": "The operation successfully completed.",
                                                         "MessageArgs": [],
                                                         "MessageArgs@odata.count": 0,
                                                         "MessageId": "IDRAC.2.7.SYS413",
                                                         "RelatedProperties": [],
                                                         "RelatedProperties@odata.count": 0,
                                                         "Resolution": "No response action is required.",
                                                         "Severity": "Informational"
                                                     }
                                                 ]
                                             }
                                         }}])
    def test_update_idrac_attributes_case01(self, params, idrac_redfish_mock_for_attr, idrac_default_args):
        idrac_default_args.update(params.get('mparams'))
        f_module = self.get_module_mock(params=idrac_default_args)
        resp = self.module.update_idrac_attributes(idrac_redfish_mock_for_attr, f_module, params["uri_dict"],
                                                   params["idrac_response_attr"], params["system_response_attr"],
                                                   params["lc_response_attr"])
        assert resp.keys() == params["resp"].keys()

    @pytest.mark.parametrize("params", [{"res_id": "iDRAC.Embedded.1",
                                         "uri_dict": {
                                             "iDRAC.Embedded.1": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/iDRAC.Embedded.1",
                                             "System.Embedded.1": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/System.Embedded.1",
                                             "LifecycleController.Embedded.1":
                                                 "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/LifecycleController.Embedded.1"},
                                         "lc_response_attr": {"LCAttributes.1.AutoUpdate": "Enabled"},
                                         "mparams": {
                                             'lifecycle_controller_attributes': {"LCAttributes.1.AutoUpdate": "Enabled"}
                                         },
                                         "idrac_response_attr": {},
                                         "system_response_attr": {},
                                         "resp": {
                                             "Lifecycle Controller": {
                                                 "@Message.ExtendedInfo": [
                                                     {
                                                         "Message": "The request completed successfully.",
                                                         "MessageArgs": [],
                                                         "MessageArgs@odata.count": 0,
                                                         "MessageId": "Base.1.12.Success",
                                                         "RelatedProperties": [],
                                                         "RelatedProperties@odata.count": 0,
                                                         "Resolution": "None",
                                                         "Severity": "OK"
                                                     },
                                                     {
                                                         "Message": "The operation successfully completed.",
                                                         "MessageArgs": [],
                                                         "MessageArgs@odata.count": 0,
                                                         "MessageId": "IDRAC.2.7.SYS413",
                                                         "RelatedProperties": [],
                                                         "RelatedProperties@odata.count": 0,
                                                         "Resolution": "No response action is required.",
                                                         "Severity": "Informational"
                                                     }
                                                 ]
                                             }
                                         }}])
    def test_update_idrac_attributes_case02(self, params, idrac_redfish_mock_for_attr, idrac_default_args):
        idrac_default_args.update(params.get('mparams'))
        f_module = self.get_module_mock(params=idrac_default_args)
        resp = self.module.update_idrac_attributes(idrac_redfish_mock_for_attr, f_module, params["uri_dict"],
                                                   params["idrac_response_attr"], params["system_response_attr"],
                                                   params["lc_response_attr"])
        assert resp.keys() == params["resp"].keys()

    @pytest.mark.parametrize("params",
                             [{"json_data": {},
                               "diff": 1,
                               "uri_dict": {
                                   "iDRAC.Embedded.1": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/iDRAC.Embedded.1",
                                   "System.Embedded.1": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/System.Embedded.1",
                                   "LifecycleController.Embedded.1":
                                       "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DellAttributes/LifecycleController.Embedded.1"},
                               "system_response_attr": {"ThermalSettings.1.ThermalProfile": "Sound Cap"},
                               "mparams": {'system_attributes': {"ThermalSettings.1.ThermalProfile": "Sound Cap"}},
                               "idrac_response_attr": {},
                               "lc_response_attr": {},
                               "message": "Successfully updated the attributes."
                               }])
    def _test_idrac_attributes(self, params, idrac_connection_attributes_mock, idrac_default_args, mocker):
        idrac_connection_attributes_mock.success = params.get("success", True)
        idrac_connection_attributes_mock.json_data = params.get('json_data')
        idrac_default_args.update(params.get('mparams'))
        f_module = self.get_module_mock(params=idrac_default_args)
        mocker.patch(UTILS_PATH + 'get_manager_res_id', return_value=MANAGER_ID)
        mocker.patch(MODULE_PATH + 'fetch_idrac_uri_attr', return_value=(params["diff"],
                                                                         params["uri_dict"],
                                                                         params["idrac_response_attr"],
                                                                         params["system_response_attr"],
                                                                         params["lc_response_attr"]))
        mocker.patch(MODULE_PATH + 'update_idrac_attributes', return_value=params["resp"])
        result = self._run_module(idrac_default_args, check_mode=params.get('check_mode', False))
        assert result['msg'] == params['message']

    @pytest.mark.parametrize("exc_type", [HTTPError, URLError])
    def _test_main_idrac_attributes_exception_handling_case(self, exc_type, idrac_connection_attributes_mock, idrac_default_args, mocker):
        idrac_default_args.update({'lifecycle_controller_attributes': {"LCAttributes.1.AutoUpdate": "Enabled"}})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError]:
            mocker.patch(
                MODULE_PATH + 'update_idrac_attributes',
                side_effect=exc_type('test'))
        else:
            mocker.patch(
                MODULE_PATH + 'update_idrac_attributes',
                side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                     {"accept-type": "application/json"}, StringIO(json_str)))
        if not exc_type == URLError:
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result
