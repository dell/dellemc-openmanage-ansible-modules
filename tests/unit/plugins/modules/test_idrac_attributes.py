# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 8.1.0
# Copyright (C) 2022-2023 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
from io import StringIO

import pytest
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_attributes
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from unittest.mock import MagicMock

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
SNMP_ADDRESS = "SNMP.1.IPAddress"


@pytest.fixture
def idrac_redfish_mock_for_attr(mocker, redfish_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI')
    idrac_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    idrac_connection_mock_obj.invoke_request.return_value = redfish_response_mock
    return idrac_connection_mock_obj


class TestIdracAttributes(FakeAnsibleModule):
    module = idrac_attributes

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

    @pytest.mark.parametrize("exc_type", [HTTPError, URLError, IOError, ValueError, TypeError, ConnectionError,
                                          AttributeError, IndexError, KeyError])
    def test_main_idrac_attributes_exception_handling_case(self, exc_type, idrac_redfish_mock_for_attr,
                                                           idrac_default_args, mocker):
        idrac_default_args.update({'lifecycle_controller_attributes': {"LCAttributes.1.AutoUpdate": "Enabled"}})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError]:
            mocker.patch(MODULE_PATH + 'update_idrac_attributes', side_effect=exc_type('test'))
        else:
            mocker.patch(MODULE_PATH + 'update_idrac_attributes',
                         side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
        if exc_type != URLError:
            result = self._run_module(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result

    def test_xml_data_conversion(self, idrac_redfish_mock_for_attr, idrac_default_args):
        attribute = {"Time.1.Timezone": "CST6CDT", "SNMP.1.SNMPProtocol": "All",
                     "LCAttributes.1.AutoUpdate": "Disabled"}
        result = self.module.xml_data_conversion(attribute, "System.Embedded.1")
        assert isinstance(result[0], str)
        assert isinstance(result[1], dict)

    def test_validate_attr_name(self, idrac_redfish_mock_for_attr, idrac_default_args):
        attribute = [{"Name": "Time.1.Timezone", "Value": "CST6CDT"}, {"Name": "SNMP.1.SNMPProtocol", "Value": "All"},
                     {"Name": "LCAttributes.1.AutoUpdate", "Value": "Disabled"}]
        req_data = {"Time.1.Timezone": "CST6CDT", "SNMP.1.SNMPProtocol": "All",
                    "LCAttributes.1.AutoUpdate": "Disabled"}
        result = self.module.validate_attr_name(attribute, req_data)
        assert result[0] == {'Time.1.Timezone': 'CST6CDT', 'SNMP.1.SNMPProtocol': 'All',
                             'LCAttributes.1.AutoUpdate': 'Disabled'}
        assert result[1] == {}
        req_data = {"Time.2.Timezone": "CST6CDT", "SNMP.2.SNMPProtocol": "All"}
        result = self.module.validate_attr_name(attribute, req_data)
        assert result[0] == {}
        assert result[1] == {'Time.2.Timezone': 'Attribute does not exist.',
                             'SNMP.2.SNMPProtocol': 'Attribute does not exist.'}

    def test_process_check_mode(self, idrac_redfish_mock_for_attr, idrac_default_args):
        idrac_default_args.update({'lifecycle_controller_attributes': {"LCAttributes.1.AutoUpdate": "Enabled"}})
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as exc:
            self.module.process_check_mode(f_module, False)
        assert exc.value.args[0] == "No changes found to be applied."
        f_module.check_mode = True
        with pytest.raises(Exception) as exc:
            self.module.process_check_mode(f_module, True)
        assert exc.value.args[0] == "Changes found to be applied."

    def test_scp_idrac_attributes(self, idrac_redfish_mock_for_attr, redfish_response_mock, idrac_default_args, mocker):
        idrac_default_args.update({'lifecycle_controller_attributes': {"LCAttributes.1.AutoUpdate": "Enabled"}})
        f_module = self.get_module_mock(params=idrac_default_args)
        mocker.patch(MODULE_PATH + 'get_check_mode', return_value=None)
        mocker.patch(MODULE_PATH + 'xml_data_conversion', return_value=("<components></components>",
                                                                        {"LCAttributes.1.AutoUpdate": "Enabled"}))
        idrac_redfish_mock_for_attr.wait_for_job_completion.return_value = {"JobStatus": "Success"}
        result = self.module.scp_idrac_attributes(f_module, idrac_redfish_mock_for_attr, "LC.Embedded.1")
        assert result["JobStatus"] == "Success"
        idrac_default_args.update({'idrac_attributes': {"User.1.UserName": "username"}})
        f_module = self.get_module_mock(params=idrac_default_args)
        mocker.patch(MODULE_PATH + 'xml_data_conversion', return_value=("<components></components>",
                                                                        {"User.1.UserName": "username"}))
        idrac_redfish_mock_for_attr.wait_for_job_completion.return_value = {"JobStatus": "Success"}
        result = self.module.scp_idrac_attributes(f_module, idrac_redfish_mock_for_attr, MANAGER_ID)
        assert result["JobStatus"] == "Success"
        idrac_default_args.update({'system_attributes': {SNMP_ADDRESS: "XX.XX.XX.XX"}})
        f_module = self.get_module_mock(params=idrac_default_args)
        mocker.patch(MODULE_PATH + 'xml_data_conversion', return_value=("<components></components>",
                                                                        {SNMP_ADDRESS: "XX.XX.XX.XX"}))
        idrac_redfish_mock_for_attr.wait_for_job_completion.return_value = {"JobStatus": "Success"}
        result = self.module.scp_idrac_attributes(f_module, idrac_redfish_mock_for_attr, "System.Embedded.1")
        assert result["JobStatus"] == "Success"

    def test_get_check_mode(self, idrac_redfish_mock_for_attr, redfish_response_mock, idrac_default_args, mocker):
        idrac_json = {SNMP_ADDRESS: "XX.XX.XX.XX"}
        idrac_default_args.update({'idrac_attributes': idrac_json})
        f_module = self.get_module_mock(params=idrac_default_args)
        response_obj = MagicMock()
        idrac_redfish_mock_for_attr.export_scp.return_value = response_obj
        response_obj.json_data = {
            "SystemConfiguration": {"Components": [
                {"FQDD": MANAGER_ID, "Attributes": {"Name": SNMP_ADDRESS, "Value": "XX.XX.XX.XX"}}
            ]}}
        mocker.patch(MODULE_PATH + 'validate_attr_name', return_value=(
            idrac_json, {"SNMP.10.IPAddress": "Attribute does not exists."}))
        with pytest.raises(Exception) as exc:
            self.module.get_check_mode(f_module, idrac_redfish_mock_for_attr, idrac_json, {}, {})
        assert exc.value.args[0] == "Attributes have invalid values."
        system_json = {"System.1.Attr": "Value"}
        idrac_default_args.update({'system_attributes': system_json})
        f_module = self.get_module_mock(params=idrac_default_args)
        response_obj.json_data = {
            "SystemConfiguration": {"Components": [
                {"FQDD": "System.Embedded.1", "Attributes": {"Name": "System.1.Attr", "Value": "Value"}}
            ]}}
        mocker.patch(MODULE_PATH + 'validate_attr_name', return_value=(
            system_json, {"System.10.Attr": "Attribute does not exists."}))
        with pytest.raises(Exception) as exc:
            self.module.get_check_mode(f_module, idrac_redfish_mock_for_attr, {}, system_json, {})
        assert exc.value.args[0] == "Attributes have invalid values."
        lc_json = {"LCAttributes.1.AutoUpdate": "Enabled"}
        idrac_default_args.update({'lifecycle_controller_attributes': lc_json})
        f_module = self.get_module_mock(params=idrac_default_args)
        response_obj.json_data = {
            "SystemConfiguration": {"Components": [
                {"FQDD": "LifecycleController.Embedded.1", "Attributes": {"Name": "LCAttributes.1.AutoUpdate",
                                                                          "Value": "Enabled"}}
            ]}}
        mocker.patch(MODULE_PATH + 'validate_attr_name', return_value=(
            lc_json, {"LCAttributes.10.AutoUpdate": "Attribute does not exists."}))
        with pytest.raises(Exception) as exc:
            self.module.get_check_mode(f_module, idrac_redfish_mock_for_attr, {}, {}, lc_json)
        assert exc.value.args[0] == "Attributes have invalid values."
        lc_json = {"LCAttributes.1.AutoUpdate": "Enabled"}
        idrac_default_args.update({'lifecycle_controller_attributes': lc_json})
        f_module = self.get_module_mock(params=idrac_default_args)
        f_module.check_mode = True
        mocker.patch(MODULE_PATH + 'validate_attr_name', return_value=(lc_json, None))
        with pytest.raises(Exception) as exc:
            self.module.get_check_mode(f_module, idrac_redfish_mock_for_attr, {}, {}, lc_json)
        assert exc.value.args[0] == "No changes found to be applied."
        mocker.patch(MODULE_PATH + 'validate_attr_name', return_value=({"LCAttributes.1.AutoUpdate": "Disabled"}, None))
        with pytest.raises(Exception) as exc:
            self.module.get_check_mode(f_module, idrac_redfish_mock_for_attr, {}, {}, lc_json)
        assert exc.value.args[0] == "Changes found to be applied."

    def test_fetch_idrac_uri_attr(self, idrac_redfish_mock_for_attr, redfish_response_mock, idrac_default_args, mocker):
        idrac_json = {SNMP_ADDRESS: "XX.XX.XX.XX"}
        idrac_default_args.update({'idrac_attributes': idrac_json})
        f_module = self.get_module_mock(params=idrac_default_args)
        response_obj = MagicMock()
        idrac_redfish_mock_for_attr.invoke_request.return_value = response_obj
        response_obj.json_data = {"Links": {"Oem": {"Dell": {"DellAttributes": {}}}},
                                  "Message": "None", "MessageId": "SYS069"}
        response_obj.status_code = 200
        mocker.patch(MODULE_PATH + "scp_idrac_attributes", return_value=response_obj)
        with pytest.raises(Exception) as exc:
            self.module.fetch_idrac_uri_attr(idrac_redfish_mock_for_attr, f_module, MANAGER_ID)
        assert exc.value.args[0] == "No changes found to be applied."
        response_obj.json_data = {"Links": {"Oem": {"Dell": {"DellAttributes": {}}}},
                                  "Message": "None", "MessageId": "SYS053"}
        mocker.patch(MODULE_PATH + "scp_idrac_attributes", return_value=response_obj)
        with pytest.raises(Exception) as exc:
            self.module.fetch_idrac_uri_attr(idrac_redfish_mock_for_attr, f_module, MANAGER_ID)
        assert exc.value.args[0] == "Successfully updated the attributes."
        response_obj.json_data = {"Links": {"Oem": {"Dell": {"DellAttributes": {}}}},
                                  "Message": "Unable to complete application of configuration profile values.",
                                  "MessageId": "SYS080"}
        mocker.patch(MODULE_PATH + "scp_idrac_attributes", return_value=response_obj)
        with pytest.raises(Exception) as exc:
            self.module.fetch_idrac_uri_attr(idrac_redfish_mock_for_attr, f_module, MANAGER_ID)
        assert exc.value.args[0] == "Application of some of the attributes failed due to invalid value or enumeration."

        response_obj.json_data = {"Links": {"Oem": {"Dell": {"DellAttributes": {}}}},
                                  "Message": "Unable to complete the task.", "MessageId": "SYS080"}
        mocker.patch(MODULE_PATH + "scp_idrac_attributes", return_value=response_obj)
        with pytest.raises(Exception) as exc:
            self.module.fetch_idrac_uri_attr(idrac_redfish_mock_for_attr, f_module, MANAGER_ID)
        assert exc.value.args[0] == "Unable to complete the task."

    def test_main_success(self, idrac_redfish_mock_for_attr, redfish_response_mock, idrac_default_args, mocker):
        idrac_default_args.update({"resource_id": "System.Embedded.1", "idrac_attributes": {"Attr": "Value"}})
        mocker.patch(MODULE_PATH + "fetch_idrac_uri_attr", return_value=(None, None, None, None, None))
        mocker.patch(MODULE_PATH + "process_check_mode", return_value=None)
        mocker.patch(MODULE_PATH + "update_idrac_attributes", return_value=None)
        result = self._run_module(idrac_default_args)
        assert result["changed"]
        assert result["msg"] == "Successfully updated the attributes."

    def test_validate_vs_registry(self, idrac_redfish_mock_for_attr, redfish_response_mock, idrac_default_args):
        idrac_default_args.update({"resource_id": "System.Embedded.1", "idrac_attributes": {"Attr": "Value"}})
        attr_dict = {"attr": "value", "attr1": "value1", "attr2": 3}
        registry = {"attr": {"Readonly": True},
                    "attr1": {"Type": "Enumeration", "Value": [{"ValueDisplayName": "Attr"}]},
                    "attr2": {"Type": "Integer", "LowerBound": 1, "UpperBound": 2}}
        result = self.module.validate_vs_registry(registry, attr_dict)
        assert result["attr"] == "Read only Attribute cannot be modified."
        assert result["attr1"] == "Invalid value for Enumeration."
        assert result["attr2"] == "Integer out of valid range."

    def test_fetch_idrac_uri_attr_dell_attr(self, idrac_redfish_mock_for_attr, redfish_response_mock,
                                            idrac_default_args, mocker):
        idrac_default_args.update({"resource_id": "System.Embedded.1", "idrac_attributes": {"Attr": "Value"}})
        f_module = self.get_module_mock(params=idrac_default_args)
        mocker.patch(MODULE_PATH + "get_response_attr", return_value=(1, None))
        mocker.patch(MODULE_PATH + "validate_vs_registry", return_value={"Attr": "Attribute does not exists"})
        response_obj = MagicMock()
        idrac_redfish_mock_for_attr.invoke_request.return_value = response_obj
        response_obj.json_data = {"Links": {"Oem": {"Dell": {
            "DellAttributes": [
                {"@odata.id": "/api/services/"}
            ]
        }}}}
        with pytest.raises(Exception) as exc:
            self.module.fetch_idrac_uri_attr(idrac_redfish_mock_for_attr, f_module, "System.Embedded.1")
        assert exc.value.args[0] == "Attributes have invalid values."

        idrac_default_args.update({"resource_id": "System.Embedded.1", "system_attributes": {"Attr": "Value"}})
        f_module = self.get_module_mock(params=idrac_default_args)
        mocker.patch(MODULE_PATH + "get_response_attr", return_value=(1, None))
        mocker.patch(MODULE_PATH + "validate_vs_registry", return_value={"Attr": "Attribute does not exists"})
        response_obj = MagicMock()
        idrac_redfish_mock_for_attr.invoke_request.return_value = response_obj
        response_obj.json_data = {"Links": {"Oem": {"Dell": {
            "DellAttributes": [
                {"@odata.id": "/api/services/"}
            ]
        }}}}
        with pytest.raises(Exception) as exc:
            self.module.fetch_idrac_uri_attr(idrac_redfish_mock_for_attr, f_module, "System.Embedded.1")
        assert exc.value.args[0] == "Attributes have invalid values."
