# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.4.0
# Copyright (C) 2019-2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.modules import ome_template
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants, \
    AnsibleFailJSonException
from io import StringIO
from ansible.module_utils._text import to_text

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_template.'


@pytest.fixture
def ome_connection_mock_for_template(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    ome_connection_mock_obj.get_all_report_details.return_value = {"report_list": []}
    return ome_connection_mock_obj


TEMPLATE_RESOURCE = {"TEMPLATE_RESOURCE": "TemplateService/Templates"}


class TestOmeTemplate(FakeAnsibleModule):
    module = ome_template

    @pytest.fixture
    def get_template_resource_mock(self, mocker):
        response_class_mock = mocker.patch(
            MODULE_PATH + '_get_resource_parameters')
        return response_class_mock

    def test_get_service_tags_success_case(self, ome_connection_mock_for_template, ome_response_mock):
        ome_connection_mock_for_template.get_all_report_details.return_value = {
            "report_list": [{"Id": Constants.device_id1,
                             "DeviceServiceTag": Constants.service_tag1}]}
        f_module = self.get_module_mock({'device_id': [], 'device_service_tag': [Constants.service_tag1]})
        data = self.module.get_device_ids(f_module, ome_connection_mock_for_template)
        assert data == [Constants.device_id1]

    def test_get_device_ids_failure_case01(self, ome_connection_mock_for_template, ome_response_mock, ome_default_args):
        ome_response_mock.json_data = {'value': []}
        ome_response_mock.success = False
        f_module = self.get_module_mock(params={'device_id': ["#@!1"]})
        with pytest.raises(Exception) as exc:
            self.module.get_device_ids(f_module, ome_connection_mock_for_template)
        assert exc.value.args[0] == "Unable to complete the operation because the entered target device id(s) " \
                                    "'{0}' are invalid.".format("#@!1")

    def test_get_device_ids_failure_case_02(self, ome_connection_mock_for_template, ome_response_mock,
                                            ome_default_args):
        ome_connection_mock_for_template.get_all_report_details.return_value = {
            "report_list": [{"Id": Constants.device_id1,
                             "DeviceServiceTag": Constants.service_tag1},
                            {"Id": Constants.device_id2,
                             "DeviceServiceTag": "tag2"}
                            ]}
        f_module = self.get_module_mock(params={'device_id': [Constants.device_id2], 'device_service_tag': ["abcd"]})
        with pytest.raises(Exception) as exc:
            self.module.get_device_ids(f_module, ome_connection_mock_for_template)
        assert exc.value.args[0] == "Unable to complete the operation because the entered target service tag(s) " \
                                    "'{0}' are invalid.".format('abcd')

    def test_get_device_ids_for_no_device_failue_case_03(self, ome_connection_mock_for_template, ome_response_mock,
                                                         ome_default_args):
        ome_connection_mock_for_template.get_all_report_details.return_value = {
            "report_list": [{"Id": Constants.device_id1,
                             "DeviceServiceTag": Constants.service_tag1}
                            ], "resp_obj": ome_response_mock}
        f_module = self.get_module_mock(params={'device_service_tag': [Constants.service_tag1], 'device_id': []})
        with pytest.raises(Exception) as exc:
            device_ids = self.module.get_device_ids(f_module, ome_connection_mock_for_template)
            assert exc.value.args[0] == "Failed to fetch the device ids."

    def test_get_view_id_success_case(self, ome_connection_mock_for_template, ome_response_mock):
        ome_response_mock.json_data = {'value': [{"Description": "", 'Id': 2}]}
        ome_response_mock.status_code = 200
        ome_response_mock.success = True
        result = self.module.get_view_id(ome_response_mock, "Deployment")
        assert result == 2

    create_payload = {"Fqdds": "All",  # Mandatory for create
                      "ViewTypeId": 4, "attributes": {"Name": "create template name"}, "SourceDeviceId": 2224}

    @pytest.mark.parametrize("param", [create_payload])
    def test_get_create_payload(self, param, ome_response_mock):
        f_module = self.get_module_mock(params=param)
        data = self.module.get_create_payload(f_module, 2224, 4)
        assert data

    def test_get_template_by_id_success_case(self, ome_response_mock):
        ome_response_mock.json_data = {'value': []}
        ome_response_mock.status_code = 200
        ome_response_mock.success = True
        f_module = self.get_module_mock()
        data = self.module.get_template_by_id(f_module, ome_response_mock, 17)
        assert data

    def test_get_template_by_name_success_case(self, ome_response_mock, ome_connection_mock_for_template):
        ome_response_mock.json_data = {'value': [{"Name": "test Sample Template import1", "Id": 24}]}
        ome_response_mock.status_code = 200
        ome_response_mock.success = True
        f_module = self.get_module_mock()
        data = self.module.get_template_by_name("test Sample Template import1", f_module,
                                                ome_connection_mock_for_template)
        assert data[0]["Name"] == "test Sample Template import1"
        assert data[0]["Id"] == 24

    def test_get_group_devices_all(self, ome_response_mock, ome_connection_mock_for_template):
        ome_response_mock.json_data = {'value': [{"Name": "Device1", "Id": 24}]}
        ome_response_mock.status_code = 200
        ome_response_mock.success = True
        f_module = self.get_module_mock()
        data = self.module.get_group_devices_all(ome_connection_mock_for_template, "uri")
        assert data == [{"Name": "Device1", "Id": 24}]

    def test_get_template_by_name_fail_case(self, ome_response_mock):
        ome_response_mock.json_data = {'value': [{"Name": "template by name for template name", "Id": 12}]}
        ome_response_mock.status_code = 500
        ome_response_mock.success = False
        f_module = self.get_module_mock()
        with pytest.raises(Exception) as exc:
            self.module.get_template_by_name("template by name for template name", f_module, ome_response_mock)
        assert exc.value.args[0] == "Unable to complete the operation because the" \
                                    " requested template with name {0} is not present." \
            .format("template by name for template name")

    create_payload = {"command": "create", "device_id": [25007],
                      "ViewTypeId": 4, "attributes": {"Name": "texplate999", "Fqdds": "All"}, "template_view_type": 4}
    inter_payload = {
        "Name": "texplate999",
        "SourceDeviceId": 25007,
        "Fqdds": "All",
        "TypeId": 2,
        "ViewTypeId": 2
    }
    payload_out = ('TemplateService/Templates',
                   {
                       "Name": "texplate999",
                       "SourceDeviceId": 25007,
                       "Fqdds": "All",
                       "TypeId": 2,
                       "ViewTypeId": 2
                   }, "POST")

    @pytest.mark.parametrize("params", [{"inp": create_payload, "mid": inter_payload, "out": payload_out}])
    def test__get_resource_parameters_create_success_case(self, mocker, ome_response_mock,
                                                          ome_connection_mock_for_template, params):
        f_module = self.get_module_mock(params=params["inp"])
        mocker.patch(MODULE_PATH + 'get_device_ids',
                     return_value=[25007])
        mocker.patch(MODULE_PATH + 'get_view_id',
                     return_value=["Deployment"])
        mocker.patch(MODULE_PATH + 'get_create_payload',
                     return_value=params["mid"])
        data = self.module._get_resource_parameters(f_module, ome_connection_mock_for_template)
        assert data == params["out"]

    modify_payload = {"command": "modify", "device_id": [25007], "template_id": 1234,
                      "ViewTypeId": 4, "attributes": {"Name": "texplate999", "Fqdds": "All"}, "template_view_type": 4}
    inter_payload = {
        "Name": "texplate999",
        "SourceDeviceId": 25007,
        "Fqdds": "All",
        "TypeId": 2,
        "ViewTypeId": 2
    }
    payload_out = ('TemplateService/Templates(1234)',
                   {
                       "Name": "texplate999",
                       "SourceDeviceId": 25007,
                       "Fqdds": "All",
                       "TypeId": 2,
                       "ViewTypeId": 2
                   }, "PUT")

    @pytest.mark.parametrize("params", [{"inp": modify_payload, "mid": inter_payload, "out": payload_out}])
    def test__get_resource_parameters_modify_success_case(self, mocker, ome_response_mock,
                                                          ome_connection_mock_for_template, params):
        f_module = self.get_module_mock(params=params["inp"])
        mocker.patch(MODULE_PATH + 'get_template_by_id',
                     return_value={})
        mocker.patch(MODULE_PATH + 'get_modify_payload',
                     return_value={})
        data = self.module._get_resource_parameters(f_module, ome_connection_mock_for_template)
        assert data == ('TemplateService/Templates(1234)', {}, 'PUT')

    def test__get_resource_parameters_delete_success_case(self, mocker, ome_response_mock,
                                                          ome_connection_mock_for_template):
        f_module = self.get_module_mock({"command": "delete", "template_id": 1234})
        data = self.module._get_resource_parameters(f_module, ome_connection_mock_for_template)
        assert data == ('TemplateService/Templates(1234)', {}, 'DELETE')

    def test__get_resource_parameters_export_success_case(self, mocker, ome_response_mock,
                                                          ome_connection_mock_for_template):
        f_module = self.get_module_mock({"command": "export", "template_id": 1234})
        data = self.module._get_resource_parameters(f_module, ome_connection_mock_for_template)
        assert data == ('TemplateService/Actions/TemplateService.Export', {'TemplateId': 1234}, 'POST')

    def test__get_resource_parameters_deploy_success_case(self, mocker, ome_response_mock,
                                                          ome_connection_mock_for_template):
        f_module = self.get_module_mock({"command": "deploy", "template_id": 1234})
        mocker.patch(MODULE_PATH + 'get_device_ids',
                     return_value=[Constants.device_id1])
        mocker.patch(MODULE_PATH + 'get_deploy_payload',
                     return_value={"deploy_payload": "value"})
        data = self.module._get_resource_parameters(f_module, ome_connection_mock_for_template)
        assert data == ('TemplateService/Actions/TemplateService.Deploy', {"deploy_payload": "value"}, 'POST')

    def test__get_resource_parameters_clone_success_case(self, mocker, ome_response_mock,
                                                         ome_connection_mock_for_template):
        f_module = self.get_module_mock({"command": "clone", "template_id": 1234, "template_view_type": 2})
        mocker.patch(MODULE_PATH + 'get_view_id',
                     return_value=2)
        mocker.patch(MODULE_PATH + 'get_clone_payload',
                     return_value={"clone_payload": "value"})
        data = self.module._get_resource_parameters(f_module, ome_connection_mock_for_template)
        assert data == ('TemplateService/Actions/TemplateService.Clone', {"clone_payload": "value"}, 'POST')

    def test__get_resource_parameters_import_success_case(self, mocker, ome_response_mock,
                                                          ome_connection_mock_for_template):
        f_module = self.get_module_mock({"command": "import", "template_id": 1234, "template_view_type": 2})
        mocker.patch(MODULE_PATH + 'get_view_id',
                     return_value=2)
        mocker.patch(MODULE_PATH + 'get_import_payload',
                     return_value={"import_payload": "value"})
        data = self.module._get_resource_parameters(f_module, ome_connection_mock_for_template)
        assert data == ('TemplateService/Actions/TemplateService.Import', {"import_payload": "value"}, 'POST')

    @pytest.mark.parametrize("params", [{"inp": {"command": "modify"}, "mid": inter_payload, "out": payload_out}])
    def test__get_resource_parameters_modify_template_none_failure_case(self, mocker, ome_response_mock,
                                                                        ome_connection_mock_for_template, params):
        f_module = self.get_module_mock(params=params["inp"])
        with pytest.raises(Exception) as exc:
            data = self.module._get_resource_parameters(f_module, ome_connection_mock_for_template)
        assert exc.value.args[0] == "Enter a valid template_name or template_id"

    @pytest.mark.parametrize("params",
                             [{"success": True, "json_data": {"value": [{"Name": "template_name", "Id": 123}]},
                               "id": 123, "gtype": True},
                              {"success": True, "json_data": {}, "id": 0, "gtype": False},
                              {"success": False, "json_data": {"value": [{"Name": "template_name", "Id": 123}]},
                               "id": 0, "gtype": False},
                              {"success": True, "json_data": {"value": [{"Name": "template_name1", "Id": 123}]},
                               "id": 12, "gtype": False}])
    def test_get_type_id_valid(self, params, ome_connection_mock_for_template,
                               ome_response_mock):
        ome_response_mock.success = params["success"]
        ome_response_mock.json_data = params["json_data"]
        id = self.module.get_type_id_valid(ome_connection_mock_for_template, params["id"])
        assert id == params["gtype"]

    @pytest.mark.parametrize("params",
                             [{"success": True, "json_data": {"value": [{"Description": "Deployment", "Id": 2}]},
                               "view": "Deployment", "gtype": 2},
                              {"success": True, "json_data": {}, "view": "Compliance", "gtype": 1},
                              {"success": False, "json_data": {"value": [{"Description": "template_name", "Id": 1}]},
                               "view": "Deployment", "gtype": 2},
                              {"success": True, "json_data": {"value": [{"Description": "template_name1", "Id": 2}]},
                               "view": "Deployment", "gtype": 2}])
    def test_get_view_id(self, params, ome_connection_mock_for_template,
                         ome_response_mock):
        ome_response_mock.success = params["success"]
        ome_response_mock.json_data = params["json_data"]
        id = self.module.get_view_id(ome_connection_mock_for_template, params["view"])
        assert id == params["gtype"]

    @pytest.mark.parametrize("param",
                             [{"pin": {"NetworkBootIsoModel": {"ShareDetail": {"Password": "share_password"}}}},
                              {"pin": {"NetworkBootIsoModel": {"ShareDetail": {"Password1": "share_password"}}}},
                              {"pin": {"NetworkBootIsoModel": {"ShareDetail": [{"Password1": "share_password"}]}}}])
    def test_password_no_log(self, param):
        attributes = param["pin"]
        self.module.password_no_log(attributes)

    def test__get_resource_parameters_create_failure_case_02(self, mocker, ome_response_mock,
                                                             ome_connection_mock_for_template):
        f_module = self.get_module_mock({"command": "create", "template_name": "name"})
        mocker.patch(MODULE_PATH + 'get_device_ids',
                     return_value=[Constants.device_id1, Constants.device_id2])
        mocker.patch(MODULE_PATH + 'get_template_by_name',
                     return_value=("template", 1234))
        with pytest.raises(Exception) as exc:
            data = self.module._get_resource_parameters(f_module, ome_connection_mock_for_template)
        assert exc.value.args[0] == "Create template requires only one reference device"

    def test_main_template_success_case2(self, ome_default_args, mocker, module_mock, ome_connection_mock_for_template,
                                         get_template_resource_mock, ome_response_mock):
        ome_connection_mock_for_template.__enter__.return_value = ome_connection_mock_for_template
        ome_connection_mock_for_template.invoke_request.return_value = ome_response_mock
        ome_response_mock.json_data = {
            "value": [{"device_id": "1111", "command": "create", "attributes": {"Name": "new 1template name"}}]}
        ome_response_mock.status_code = 200
        ome_default_args.update(
            {"device_id": "1111", "command": "create", "attributes": {"Name": "new 1template name"}})
        ome_response_mock.success = True
        mocker.patch(MODULE_PATH + '_get_resource_parameters',
                     return_value=(TEMPLATE_RESOURCE, "template_payload", "POST"))
        result = self._run_module(ome_default_args)
        assert result['changed'] is True
        assert result['msg'] == "Successfully created a template with ID {0}".format(ome_response_mock.json_data)

    @pytest.mark.parametrize("param",
                             [{"attr": {"attributes": {}}, "template_id": 1234,
                               "template_dict": {"Name": "template1", "Description": "template description"}},
                              {"attr": {"attributes": {"Name": "1", "Description": "d1"}}, "template_id": 1234,
                               "template_dict": {"Name": "template1", "Description": "template description"}},
                              {"attr": {"attributes": []}, "template_id": 1234,
                               "template_dict": {"Name": "template1", "Description": "template description"}}
                              ])
    def test_get_modify_payload_success_case_01(self, param):
        self.module.get_modify_payload(param["attr"], param["template_id"],
                                       param["template_dict"])

    def test_get_import_payload_success_case_01(self, ome_connection_mock_for_template):
        f_module = self.get_module_mock(params={"attributes": {"Name": "template1", "Content": "Content"}})
        self.module.get_import_payload(f_module, ome_connection_mock_for_template, 2)

    def test_get_deploy_payload_success_case_01(self):
        module_params = {"attributes": {"Name": "template1"}}
        self.module.get_deploy_payload(module_params, [Constants.device_id1], 1234)

    @pytest.mark.parametrize("param",
                             [{"attr": {"attributes": {"Name": "template1"}}, "name": "template1"}])
    def test_get_clone_payload_success_case_01(self, param):
        module_params = param["attr"]
        self.module.get_clone_payload(module_params, 1234, 2)

    @pytest.mark.parametrize("param",
                             [{"inp": {"command": "create", "template_name": "name", "device_id": [None],
                                       "device_service_tag": [None]},
                               "msg": "Argument device_id or device_service_tag has null values"},
                              {"inp": {"command": "deploy", "template_name": "name", "device_id": [None],
                                       "device_service_tag": [None]},
                               "msg": "Argument device_id or device_service_tag has null values"},
                              {"inp": {"command": "import", "template_name": "name", "device_id": [],
                                       "device_service_tag": []},
                               "msg": "Argument 'Name' required in attributes for import operation"},
                              {"inp": {"command": "import", "attributes": {"Name": "name"}, "device_id": [],
                                       "device_service_tag": []},
                               "msg": "Argument 'Content' required in attributes for import operation"},
                              {"inp": {"command": "clone", "template_name": "name", "device_id": [],
                                       "device_service_tag": []},
                               "msg": "Argument 'Name' required in attributes for clone operation"}
                              ])
    def test_validate_inputs(self, param, mocker):
        f_module = self.get_module_mock(param["inp"])
        mocker.patch(MODULE_PATH + 'password_no_log')
        with pytest.raises(Exception) as exc:
            self.module._validate_inputs(f_module)
        assert exc.value.args[0] == param["msg"]

    @pytest.mark.parametrize("param", [
        {"inp": {"command": "deploy", "template_name": "name",
                 "device_group_names": ["mygroup"]},
         "group": {'Id': 23, "Name": "mygroup"},
         "dev_list": [1, 2, 3]}])
    def test_get_group_details(self, param, ome_connection_mock_for_template, mocker,
                               ome_response_mock):
        f_module = self.get_module_mock(param["inp"])
        ome_response_mock.json_data = {
            "value": [{'Id': 1, "Name": "mygroup3"}, {'Id': 2, "Name": "mygroup2"}, {'Id': 3, "Name": "mygroup"}]}
        ome_response_mock.status_code = 200
        mocker.patch(MODULE_PATH + 'get_group_devices_all', return_value=[{'Id': 1}, {'Id': 2}, {'Id': 3}])
        dev_list = self.module.get_group_details(ome_connection_mock_for_template, f_module)
        assert dev_list == param["dev_list"]

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, TypeError, ConnectionError,
                              HTTPError, URLError, SSLError])
    def test_main_template_exception_case(self, exc_type, mocker, ome_default_args,
                                          ome_connection_mock_for_template, ome_response_mock):
        ome_default_args.update({"command": "export", "template_name": "t1", 'attributes': {'Attributes': "myattr1"}})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'password_no_log')
            mocker.patch(MODULE_PATH + '_get_resource_parameters', side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + '_get_resource_parameters', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + '_get_resource_parameters',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result
