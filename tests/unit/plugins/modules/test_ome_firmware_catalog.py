# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.4.0
# Copyright (C) 2019-2021 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.modules import ome_firmware_catalog
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from io import StringIO
from ansible.module_utils._text import to_text
from ansible.module_utils.urls import ConnectionError, SSLValidationError
import json
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.ome_firmware_catalog.'

NO_CHANGES_MSG = "No changes found to be applied."
INVALID_CATALOG_ID = "Invalid catalog ID provided."
CATALOG_DEL_SUCCESS = "Successfully deleted the firmware catalog."
CATALOG_BASELINE_ATTACHED = "Unable to delete as catalog is associated with baseline(s)."
CATALOG_JOB_RUNNING = "Catalog job '{name}' with ID {id} is running.Retry after job completion."
CHECK_MODE_CHANGE_FOUND_MSG = "Changes found to be applied."
CHECK_MODE_CHANGE_NOT_FOUND_MSG = "No changes found to be applied."
INVALID_CATALOG_ID = "Invalid catalog ID provided."
CATALOG_DEL_SUCCESS = "Successfully deleted the firmware catalog(s)."
CATALOG_BASELINE_ATTACHED = "Unable to delete the catalog as it is with baseline(s)."
CATALOG_EXISTS = "The catalog with the name '{new_name}' already exists in the system."
DELL_ONLINE_EXISTS = "Catalog with 'DELL_ONLINE' repository already exists with the name '{catalog_name}'."
NAMES_ERROR = "Only delete operations accept multiple catalog names or IDs."
CATALOG_ID_NOT_FOUND = "Catalog with ID '{catalog_id}' not found."
CATALOG_NAME_NOT_FOUND = "Catalog '{catalog_name}' not found."
CATALOG_UPDATED = "Successfully {operation} the firmware catalog."

catalog_info = {
    "@odata.context": "/api/$metadata#Collection(UpdateService.Catalogs)",
    "@odata.count": 3,
    "value": [
        {
            "@odata.type": "#UpdateService.Catalogs",
            "@odata.id": "/api/UpdateService/Catalogs(29)",
            "Id": 29,
            "Filename": "catalog.gz",
            "SourcePath": "catalog/catalog.gz",
            "Status": "Failed",
            "TaskId": 21448,
            "BaseLocation": None,
            "Schedule": {
                "StartTime": None,
                "EndTime": None,
                "Cron": "startnow"
            },
            "AssociatedBaselines": ["abc"],
            "Repository": {
                "@odata.type": "#UpdateService.Repository",
                "Id": 19,
                "Name": "catalog_http3",
                "Description": "catalog desc3",
                "Source": "downloads.dell.com",
                "DomainName": None,
                "Username": None,
                "Password": None,
                "CheckCertificate": False,
                "RepositoryType": "HTTP"
            }
        },
        {
            "@odata.type": "#UpdateService.Catalogs",
            "@odata.id": "/api/UpdateService/Catalogs(30)",
            "Id": 30,
            "Filename": "catalog.gz",
            "SourcePath": "catalog/catalog.gz",
            "Status": "Failed",
            "BaseLocation": None,
            "TaskId": 21449,
            "Schedule": {
                "StartTime": None,
                "EndTime": None,
                "Cron": "startnow"
            },
            "AssociatedBaselines": [],
            "Repository": {
                "@odata.type": "#UpdateService.Repository",
                "Id": 20,
                "Name": "catalog_http4",
                "Description": "catalog desc4",
                "Source": "downloads.dell.com",
                "DomainName": None,
                "Username": None,
                "Password": None,
                "CheckCertificate": False,
                "RepositoryType": "HTTP"
            }
        },
        {
            "@odata.type": "#UpdateService.Catalogs",
            "@odata.id": "/api/UpdateService/Catalogs(34)",
            "Id": 34,
            "Filename": "catalog.xml",
            "SourcePath": "catalog/catalog.gz",
            "Status": "Completed",
            "TaskId": 21453,
            "BaseLocation": "downloads.dell.com",
            "Schedule": {
                "StartTime": None,
                "EndTime": None,
                "Cron": "startnow"
            },
            "BundlesCount": 173,
            "PredecessorIdentifier": "aaaaaa",
            "AssociatedBaselines": [],
            "Repository": {
                "@odata.type": "#UpdateService.Repository",
                "Id": 24,
                "Name": "catalog_online2",
                "Description": "catalog desc4",
                "Source": "downloads.dell.com",
                "DomainName": None,
                "Username": None,
                "Password": None,
                "CheckCertificate": False,
                "RepositoryType": "DELL_ONLINE"
            }
        }
    ]
}

catalog_resp = {
    "@odata.type": "#UpdateService.Catalogs",
    "@odata.id": "/api/UpdateService/Catalogs(34)",
    "Id": 34,
    "Filename": "catalog.xml",
    "SourcePath": "catalog/catalog.gz",
    "Status": "Completed",
    "TaskId": 21453,
    "BaseLocation": "downloads.dell.com",
    "Schedule": {
        "StartTime": None,
        "EndTime": None,
        "Cron": "startnow"
    },
    "BundlesCount": 173,
    "PredecessorIdentifier": "aaaaaa",
    "AssociatedBaselines": [],
    "Repository": {
        "@odata.type": "#UpdateService.Repository",
        "Id": 24,
        "Name": "catalog_online2",
        "Description": "catalog desc4",
        "Source": "downloads.dell.com",
        "DomainName": None,
        "Username": None,
        "Password": None,
        "CheckCertificate": False,
        "RepositoryType": "DELL_ONLINE"
    }
}


@pytest.fixture
def ome_connection_catalog_mock(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeFirmwareCatalog(FakeAnsibleModule):
    module = ome_firmware_catalog

    @pytest.fixture
    def mock__get_catalog_payload(self, mocker):
        mock_payload = mocker.patch(
            MODULE_PATH + '_get_catalog_payload',
            return_value={"Repistory": "Dummy val"})
        return mock_payload

    def test_ome_catalog_firmware_main_ome_firmware_catalog_no_mandatory_arg_passed_failuer_case(self, ome_default_args,
                                                                                                 module_mock,
                                                                                                 mock__get_catalog_payload,
                                                                                                 ome_connection_catalog_mock):
        result = self._run_module_with_fail_json(ome_default_args)
        assert 'catalog_status' not in result

    inp_param1 = {"hostname": "host ip", "username": "username",
                  "password": "password", "port": 443, "catalog_name": ["catalog_name"]}
    inp_param2 = {"hostname": "host ip", "username": "username",
                  "password": "password", "port": 443, "catalog_name": ["catalog_name"], "catalog_description": "desc",
                  "source": "10.255.2.128:2607", "source_path": "source_path", "file_name": "file_name",
                  "repository_type": "HTTPS",
                  "repository_username": "repository_username",
                  "repository_password": "repository_password",
                  "repository_domain": "repository_domain",
                  "check_certificate": True}
    inp_param3 = {"hostname": "host ip", "username": "username",
                  "password": "password", "port": 443, "catalog_name": " ", "catalog_description": None}
    inp_param4 = {"hostname": "host ip", "username": "username",
                  "password": "password", "port": 443, "catalog_name": ["catalog_name"], "catalog_description": "desc",
                  "source": "10.255.2.128:2607", "source_path": "source_path", "file_name": "file_name",
                  "repository_type": "DELL_ONLINE",
                  "repository_username": "repository_username",
                  "repository_password": "repository_password",
                  "repository_domain": "repository_domain",
                  "check_certificate": True}
    inp_param5 = {"hostname": "host ip", "username": "username",
                  "password": "password", "port": 443, "catalog_name": ["catalog_name"], "catalog_description": "desc",
                  "source_path": "source_path", "file_name": "file_name",
                  "repository_type": "DELL_ONLINE",
                  "repository_username": "repository_username",
                  "repository_password": "repository_password",
                  "repository_domain": "repository_domain",
                  "check_certificate": True}
    out1 = {"Repository": {"Name": "catalog_name"}}
    out2 = {'Filename': 'file_name', 'SourcePath': 'source_path',
            'Repository': {'Name': 'catalog_name', 'Description': 'desc',
                           'Source': '10.255.2.128:2607', 'RepositoryType': 'HTTPS', 'Username': 'repository_username',
                           'Password': 'repository_password', 'DomainName': 'repository_domain',
                           'CheckCertificate': True}}

    out3 = {"Repository": {"Name": " "}}
    out4 = {'Filename': 'file_name', 'SourcePath': 'source_path',
            'Repository': {'Name': 'catalog_name', 'Description': 'desc',
                           'Source': '10.255.2.128:2607', 'RepositoryType': 'DELL_ONLINE',
                           'CheckCertificate': True}}
    out5 = {'Filename': 'file_name', 'SourcePath': 'source_path',
            'Repository': {'Name': 'catalog_name', 'Description': 'desc',
                           'Source': 'downloads.dell.com', 'RepositoryType': 'DELL_ONLINE',
                           'CheckCertificate': True}}

    @pytest.mark.parametrize("params", [{"inp": inp_param1, "out": out1},
                                        {"inp": inp_param2, "out": out2},
                                        {"inp": inp_param3, "out": out3}
                                        ])
    def test_ome_catalog_firmware__get_catalog_payload_success_case(self, params):
        payload = self.module._get_catalog_payload(params["inp"], params["inp"]["catalog_name"][0])
        assert payload == params["out"]

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_catalog_firmware_ome_catalog_main_exception_failure_case(self, exc_type, mocker, ome_default_args,
                                                                          ome_connection_catalog_mock,
                                                                          ome_response_mock):
        ome_default_args.update({"state": "absent", "catalog_name": "t1"})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'check_existing_catalog', side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'check_existing_catalog', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'check_existing_catalog',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result

    @pytest.mark.parametrize("params", [{"state": "present", "catalog_name": ["catalog_online2"]},
                                        {"state": "present", "catalog_id": [34]}])
    def test_ome_catalog_firmware_check_existing_catalog_case01(self, params, ome_connection_catalog_mock):
        ome_connection_catalog_mock.get_all_items_with_pagination.return_value = {"value": catalog_info["value"]}
        f_module = self.get_module_mock(params=params)
        catalog, all_catalog = self.module.check_existing_catalog(f_module, ome_connection_catalog_mock,
                                                                  params["state"])
        assert catalog[0] == {
            "@odata.type": "#UpdateService.Catalogs",
            "@odata.id": "/api/UpdateService/Catalogs(34)",
            "Id": 34,
            "Filename": "catalog.xml",
            "SourcePath": "catalog/catalog.gz",
            "Status": "Completed",
            "TaskId": 21453,
            "BaseLocation": "downloads.dell.com",
            "Schedule": {
                "StartTime": None,
                "EndTime": None,
                "Cron": "startnow"
            },
            "BundlesCount": 173,
            "PredecessorIdentifier": "aaaaaa",
            "AssociatedBaselines": [],
            "Repository": {
                "@odata.type": "#UpdateService.Repository",
                "Id": 24,
                "Name": "catalog_online2",
                "Description": "catalog desc4",
                "Source": "downloads.dell.com",
                "DomainName": None,
                "Username": None,
                "Password": None,
                "CheckCertificate": False,
                "RepositoryType": "DELL_ONLINE"
            }
        }
        assert all_catalog == {"catalog_online2": "DELL_ONLINE", "catalog_http4": "HTTP",
                               "catalog_http3": "HTTP"}

    @pytest.mark.parametrize("params",
                             [{"state": "absent", "catalog_name": ["catalog_online2", "catalog_http4"]},
                              {"state": "absent", "catalog_id": [34, 30]}])
    def test_ome_catalog_firmware_check_existing_catalog_case02(self, params, ome_connection_catalog_mock):
        ome_connection_catalog_mock.get_all_items_with_pagination.return_value = {"value": catalog_info["value"]}
        f_module = self.get_module_mock(params=params)
        catalog, all_catalog = self.module.check_existing_catalog(f_module, ome_connection_catalog_mock,
                                                                  params["state"])
        assert catalog == [
            {
                "@odata.type": "#UpdateService.Catalogs",
                "@odata.id": "/api/UpdateService/Catalogs(30)",
                "Id": 30,
                "Filename": "catalog.gz",
                "SourcePath": "catalog/catalog.gz",
                "Status": "Failed",
                "BaseLocation": None,
                "TaskId": 21449,
                "Schedule": {
                    "StartTime": None,
                    "EndTime": None,
                    "Cron": "startnow"
                },
                "AssociatedBaselines": [],
                "Repository": {
                    "@odata.type": "#UpdateService.Repository",
                    "Id": 20,
                    "Name": "catalog_http4",
                    "Description": "catalog desc4",
                    "Source": "downloads.dell.com",
                    "DomainName": None,
                    "Username": None,
                    "Password": None,
                    "CheckCertificate": False,
                    "RepositoryType": "HTTP"
                }
            },
            {
                "@odata.type": "#UpdateService.Catalogs",
                "@odata.id": "/api/UpdateService/Catalogs(34)",
                "Id": 34,
                "Filename": "catalog.xml",
                "SourcePath": "catalog/catalog.gz",
                "Status": "Completed",
                "TaskId": 21453,
                "BaseLocation": "downloads.dell.com",
                "Schedule": {
                    "StartTime": None,
                    "EndTime": None,
                    "Cron": "startnow"
                },
                "BundlesCount": 173,
                "PredecessorIdentifier": "aaaaaa",
                "AssociatedBaselines": [],
                "Repository": {
                    "@odata.type": "#UpdateService.Repository",
                    "Id": 24,
                    "Name": "catalog_online2",
                    "Description": "catalog desc4",
                    "Source": "downloads.dell.com",
                    "DomainName": None,
                    "Username": None,
                    "Password": None,
                    "CheckCertificate": False,
                    "RepositoryType": "DELL_ONLINE"
                }
            }
        ]
        assert all_catalog == {}

    @pytest.mark.parametrize("params", [{"state": "present", "catalog_name": ["catalog_online2"]}])
    def test_ome_catalog_firmware_check_existing_catalog_case03(self, params, ome_connection_catalog_mock):
        ome_connection_catalog_mock.get_all_items_with_pagination.return_value = {"value": catalog_info["value"]}
        f_module = self.get_module_mock(params=params)
        catalog, all_catalog = self.module.check_existing_catalog(f_module, ome_connection_catalog_mock,
                                                                  params["state"],
                                                                  "catalog_online2")
        assert catalog[0] == {
            "@odata.type": "#UpdateService.Catalogs",
            "@odata.id": "/api/UpdateService/Catalogs(34)",
            "Id": 34,
            "Filename": "catalog.xml",
            "SourcePath": "catalog/catalog.gz",
            "Status": "Completed",
            "TaskId": 21453,
            "BaseLocation": "downloads.dell.com",
            "Schedule": {
                "StartTime": None,
                "EndTime": None,
                "Cron": "startnow"
            },
            "BundlesCount": 173,
            "PredecessorIdentifier": "aaaaaa",
            "AssociatedBaselines": [],
            "Repository": {
                "@odata.type": "#UpdateService.Repository",
                "Id": 24,
                "Name": "catalog_online2",
                "Description": "catalog desc4",
                "Source": "downloads.dell.com",
                "DomainName": None,
                "Username": None,
                "Password": None,
                "CheckCertificate": False,
                "RepositoryType": "DELL_ONLINE"
            }
        }
        assert all_catalog == {"catalog_online2": "DELL_ONLINE", "catalog_http4": "HTTP",
                               "catalog_http3": "HTTP"}

    def test_ome_catalog_firmware_get_updated_catalog_info(self, ome_connection_catalog_mock):
        resp = {
            "@odata.type": "#UpdateService.Catalogs",
            "@odata.id": "/api/UpdateService/Catalogs(34)",
            "Id": 34,
            "Filename": "catalog.xml",
            "SourcePath": "catalog/catalog.gz",
            "Status": "Completed",
            "TaskId": 21453,
            "BaseLocation": "downloads.dell.com",
            "Schedule": {
                "StartTime": None,
                "EndTime": None,
                "Cron": "startnow"
            },
            "BundlesCount": 173,
            "PredecessorIdentifier": "aaaaaa",
            "AssociatedBaselines": [],
            "Repository": {
                "@odata.type": "#UpdateService.Repository",
                "Id": 24,
                "Name": "catalog_online2",
                "Description": "catalog desc4",
                "Source": "downloads.dell.com",
                "DomainName": None,
                "Username": None,
                "Password": None,
                "CheckCertificate": False,
                "RepositoryType": "DELL_ONLINE"
            }
        }
        f_module = self.get_module_mock(params={"state": "present", "catalog_name": "catalog_online2"})
        ome_connection_catalog_mock.get_all_items_with_pagination.return_value = {"value": catalog_info["value"]}
        catalog = self.module.get_updated_catalog_info(f_module, ome_connection_catalog_mock, resp)
        assert catalog == resp

    @pytest.mark.parametrize("params",
                             [{"mparams": {"state": "present", "job_wait_timeout": 10, "job_wait": True,
                                           "catalog_name": ["catalog_online2"]}}])
    @pytest.mark.parametrize("action",
                             ["created", "modified"])
    def test_ome_catalog_firmware_exit_catalog(self, mocker, ome_connection_catalog_mock, params, action):
        ome_connection_catalog_mock.job_tracking.return_value = False, "message"
        mocker.patch(MODULE_PATH + 'time.sleep', return_value=None)
        f_module = self.get_module_mock(params=params["mparams"])
        mocker.patch(MODULE_PATH + 'get_updated_catalog_info', return_value=catalog_resp)
        msg = CATALOG_UPDATED.format(operation=action)
        with pytest.raises(Exception) as err:
            self.module.exit_catalog(f_module, ome_connection_catalog_mock, catalog_resp, action, msg)
        assert err.value.args[0] == msg

    @pytest.mark.parametrize("params",
                             [{"mparams": {"state": "present", "job_wait_timeout": 10, "job_wait": False,
                                           "catalog_name": ["catalog_online2"]}}])
    @pytest.mark.parametrize("action",
                             ["created", "modified"])
    def test_ome_catalog_firmware_exit_catalog2(self, mocker, ome_connection_catalog_mock, params, action):
        mocker.patch(MODULE_PATH + 'time.sleep', return_value=None)
        f_module = self.get_module_mock(params=params["mparams"])
        mocker.patch(MODULE_PATH + 'get_updated_catalog_info', return_value=catalog_resp)
        msg = CATALOG_UPDATED.format(operation=action)
        with pytest.raises(Exception) as err:
            self.module.exit_catalog(f_module, ome_connection_catalog_mock, catalog_resp, action, msg)
        assert err.value.args[0] == msg

    def test_ome_catalog_firmware_validate_dell_online_case01(self):
        all_catalog = {"catalog_online2": "DELL_ONLINE", "catalog_http4": "HTTP",
                       "catalog_http3": "HTTP"}
        f_module = self.get_module_mock(params={"catalog_name": ["catalog_online2"]})
        self.module.validate_dell_online(all_catalog, f_module)

    def test_ome_catalog_firmware_validate_dell_online_case02(self):
        all_catalog = {"catalog_http4": "HTTP",
                       "catalog_http3": "HTTP"}
        f_module = self.get_module_mock(params={"catalog_name": ["catalog_online2"]})
        self.module.validate_dell_online(all_catalog, f_module)

    def test_ome_catalog_firmware_validate_dell_online_case03(self):
        all_catalog = {"catalog_online3": "DELL_ONLINE", "catalog_http4": "HTTP",
                       "catalog_http3": "HTTP"}
        f_module = self.get_module_mock(params={"catalog_name": ["catalog_online2"]})
        with pytest.raises(Exception) as err:
            self.module.validate_dell_online(all_catalog, f_module)
        assert err.value.args[0] == DELL_ONLINE_EXISTS.format(catalog_name="catalog_online3")

    def test_ome_catalog_firmware_create_catalog(self, mocker, ome_response_mock, ome_connection_catalog_mock):
        f_module = self.get_module_mock(params={"catalog_name": ["catalog_name"]})
        ome_response_mock.json_data = catalog_resp
        mocker.patch(MODULE_PATH + 'exit_catalog', return_value=catalog_resp)
        self.module.create_catalog(f_module, ome_connection_catalog_mock)

    def test_ome_catalog_firmware_get_current_catalog_settings(self):
        payload = self.module.get_current_catalog_settings(catalog_resp)
        assert payload == {'Filename': 'catalog.xml', 'SourcePath': 'catalog/catalog.gz',
                           'Repository': {'Name': 'catalog_online2', 'Id': 24, 'Description': 'catalog desc4',
                                          'RepositoryType': 'DELL_ONLINE', 'Source': 'downloads.dell.com',
                                          'CheckCertificate': False}}

    def test_ome_catalog_firmware_modify_catalog_case01(self, mocker, ome_connection_catalog_mock):
        f_module = self.get_module_mock(
            params={"catalog_name": ["catalog_online2"], "new_catalog_name": "catalog_http3"})
        modify_payload = {
            "Id": 34,
            "Filename": "catalog.xml",
            "SourcePath": "catalog/catalog.gz",
            "Repository": {
                "Name": "catalog_online2",
                "Description": "catalog desc4",
                "CheckCertificate": False,
            }
        }
        mocker.patch(MODULE_PATH + '_get_catalog_payload', return_value=modify_payload)
        with pytest.raises(Exception) as err:
            self.module.modify_catalog(f_module, ome_connection_catalog_mock, [catalog_resp],
                                       {"catalog_online2": "DELL_ONLINE", "catalog_http4": "HTTP",
                                        "catalog_http3": "HTTP"})
        assert err.value.args[0] == CATALOG_EXISTS.format(new_name="catalog_http3")

    def test_ome_catalog_firmware_modify_catalog_case02(self, mocker, ome_connection_catalog_mock):
        f_module = self.get_module_mock(
            params={"catalog_name": ["catalog_online2"], "new_catalog_name": "catalog_http10"})
        modify_payload = {
            "Id": 34,
            "Filename": "catalog.xml",
            "SourcePath": "catalog/catalog.gz",
            "Repository": {
                "Name": "catalog_online2",
                "Description": "catalog desc4",
                "CheckCertificate": False,
                "RepositoryType": "NFS"
            }
        }
        current_payload = {
            "Id": 34,
            "Filename": "catalog.xml",
            "SourcePath": "catalog/catalog.gz",
            "Repository": {
                "Id": 11,
                "Name": "catalog_online2",
                "Description": "catalog desc4",
                "CheckCertificate": False,
                "RepositoryType": "DELL_ONLINE"
            }
        }
        mocker.patch(MODULE_PATH + '_get_catalog_payload', return_value=modify_payload)
        mocker.patch(MODULE_PATH + 'get_current_catalog_settings', return_value=current_payload)
        with pytest.raises(Exception) as err:
            self.module.modify_catalog(f_module, ome_connection_catalog_mock, [catalog_resp],
                                       {"catalog_online2": "DELL_ONLINE", "catalog_http4": "HTTP",
                                        "catalog_http3": "HTTP"})
        assert err.value.args[0] == "Repository type cannot be changed to another repository type."

    def test_ome_catalog_firmware_modify_catalog_case03(self, mocker, ome_connection_catalog_mock):
        f_module = self.get_module_mock(
            params={"catalog_name": ["catalog_online2"], "new_catalog_name": "catalog_http10"}, check_mode=True)
        modify_payload = {
            "Id": 34,
            "Filename": "catalog.xml",
            "SourcePath": "catalog/catalog.gz",
            "Repository": {
                "Name": "catalog_online2",
                "Description": "catalog desc4",
                "CheckCertificate": True,
                "RepositoryType": "DELL_ONLINE"
            }
        }
        # current_payload = {
        #     "Id": 34,
        #     "Filename": "catalog.xml",
        #     "SourcePath": "catalog/catalog.gz",
        #     "Repository": {
        #         "Id": 11,
        #         "Name": "catalog_online2",
        #         "Description": "catalog desc4",
        #         "CheckCertificate": True,
        #         "RepositoryType": "DELL_ONLINE"
        #     }
        # }
        mocker.patch(MODULE_PATH + '_get_catalog_payload', return_value=modify_payload)
        with pytest.raises(Exception) as err:
            self.module.modify_catalog(f_module, ome_connection_catalog_mock, [catalog_resp],
                                       {"catalog_online2": "DELL_ONLINE", "catalog_http4": "HTTP",
                                        "catalog_http3": "HTTP"})
        assert err.value.args[0] == CHECK_MODE_CHANGE_FOUND_MSG

    @pytest.mark.parametrize("check_mode", [True, False])
    def test_ome_catalog_firmware_modify_catalog_case04(self, check_mode, mocker, ome_connection_catalog_mock):
        f_module = self.get_module_mock(
            params={"catalog_name": ["catalog_online2"], "new_catalog_name": "catalog_online2"}, check_mode=check_mode)
        modify_payload = {
            "Filename": "catalog.xml",
            "SourcePath": "catalog/catalog.gz",
            "Repository": {
                "Name": "catalog_online2",
                "Description": "catalog desc4",
                "CheckCertificate": False,
                "RepositoryType": "DELL_ONLINE"
            }
        }
        current_payload = {
            "Filename": "catalog.xml",
            "SourcePath": "catalog/catalog.gz",
            "Repository": {
                "Id": 11,
                "Name": "catalog_online2",
                "Description": "catalog desc4",
                "CheckCertificate": False,
                "RepositoryType": "DELL_ONLINE"
            }
        }
        mocker.patch(MODULE_PATH + '_get_catalog_payload', return_value=modify_payload)
        mocker.patch(MODULE_PATH + 'get_current_catalog_settings', return_value=current_payload)
        with pytest.raises(Exception) as err:
            self.module.modify_catalog(f_module, ome_connection_catalog_mock, [catalog_resp],
                                       {"catalog_online2": "DELL_ONLINE", "catalog_http4": "HTTP",
                                        "catalog_http3": "HTTP"})
        assert err.value.args[0] == CHECK_MODE_CHANGE_NOT_FOUND_MSG

    def test_ome_catalog_firmware_modify_catalog_case05(self, mocker, ome_connection_catalog_mock, ome_response_mock):
        f_module = self.get_module_mock(
            params={"catalog_name": ["catalog_online2"], "new_catalog_name": "catalog_http10"}, check_mode=False)
        modify_payload = {
            "Id": 34,
            "Filename": "catalog.xml",
            "SourcePath": "catalog/catalog.gz",
            "Repository": {
                "Name": "catalog_online2",
                "Description": "catalog desc4",
                "CheckCertificate": False,
                "RepositoryType": "DELL_ONLINE"
            }
        }
        mocker.patch(MODULE_PATH + '_get_catalog_payload', return_value=modify_payload)
        ome_response_mock.json_data = catalog_resp
        mocker.patch(MODULE_PATH + 'exit_catalog', return_value=None)
        self.module.modify_catalog(f_module, ome_connection_catalog_mock, [catalog_resp],
                                   {"catalog_online2": "DELL_ONLINE", "catalog_http4": "HTTP",
                                    "catalog_http3": "HTTP"})

    def test_ome_catalog_firmware_validate_delete_operation_case1(self, ome_response_mock, ome_connection_catalog_mock):
        f_module = self.get_module_mock(
            params={"catalog_name": ["catalog_http3", "catalog_online2"]}, check_mode=False)
        ome_response_mock.json_data = {
            "@odata.context": "/api/$metadata#JobService.Job",
            "@odata.type": "#JobService.Job",
            "@odata.id": "/api/JobService/Jobs(10025)",
            "Id": 10025,
            "JobName": "Default Console Update Execution Task",
            "JobDescription": "Default Console Update Execution Task",
            "State": "Enabled",
            "CreatedBy": "system",
            "Targets": [],
            "Params": [],
            "LastRunStatus": {
                "@odata.type": "#JobService.JobStatus",
                "Id": 2051,
                "Name": "NotRun"
            },
            "JobType": {
                "@odata.type": "#JobService.JobType",
                "Id": 124,
                "Name": "ConsoleUpdateExecution_Task",
                "Internal": False
            },
            "JobStatus": {
                "@odata.type": "#JobService.JobStatus",
                "Id": 2080,
                "Name": "New"
            },
        }
        with pytest.raises(Exception) as err:
            self.module.validate_delete_operation(ome_connection_catalog_mock, f_module, catalog_info["value"], [1, 2])
        assert err.value.args[0] == CATALOG_BASELINE_ATTACHED

    def test_ome_catalog_firmware_validate_delete_operation_case2(self, ome_response_mock, ome_connection_catalog_mock):
        f_module = self.get_module_mock(
            params={"catalog_name": ["catalog_http3", "catalog_online2"]}, check_mode=True)
        ome_response_mock.json_data = {
            "@odata.context": "/api/$metadata#JobService.Job",
            "@odata.type": "#JobService.Job",
            "@odata.id": "/api/JobService/Jobs(10025)",
            "Id": 10025,
            "JobName": "Default Console Update Execution Task",
            "JobDescription": "Default Console Update Execution Task",
            "State": "Enabled",
            "CreatedBy": "system",
            "Targets": [],
            "Params": [],
            "LastRunStatus": {
                "@odata.type": "#JobService.JobStatus",
                "Id": 2051,
                "Name": "NotRun"
            },
            "JobType": {
                "@odata.type": "#JobService.JobType",
                "Id": 124,
                "Name": "ConsoleUpdateExecution_Task",
                "Internal": False
            },
            "JobStatus": {
                "@odata.type": "#JobService.JobStatus",
                "Id": 2080,
                "Name": "New"
            },
        }
        catalog_info1 = [catalog_resp]
        with pytest.raises(Exception) as err:
            self.module.validate_delete_operation(ome_connection_catalog_mock, f_module, catalog_info1, [34])
        assert err.value.args[0] == CHECK_MODE_CHANGE_FOUND_MSG

    def test_ome_catalog_firmware_validate_delete_operation_case3(self, ome_response_mock, ome_connection_catalog_mock):
        f_module = self.get_module_mock(
            params={"catalog_name": ["catalog_http3", "catalog_online2"]}, check_mode=False)
        ome_response_mock.json_data = {
            "@odata.context": "/api/$metadata#JobService.Job",
            "@odata.type": "#JobService.Job",
            "@odata.id": "/api/JobService/Jobs(10025)",
            "Id": 10025,
            "JobName": "Default Console Update Execution Task",
            "JobDescription": "Default Console Update Execution Task",
            "State": "Enabled",
            "CreatedBy": "system",
            "Targets": [],
            "Params": [],
            "LastRunStatus": {
                "@odata.type": "#JobService.JobStatus",
                "Id": 2051,
                "Name": "NotRun"
            },
            "JobType": {
                "@odata.type": "#JobService.JobType",
                "Id": 124,
                "Name": "ConsoleUpdateExecution_Task",
                "Internal": False
            },
            "JobStatus": {
                "@odata.type": "#JobService.JobStatus",
                "Id": 2080,
                "Name": "New"
            },
        }
        catalog_info1 = [catalog_resp]
        self.module.validate_delete_operation(ome_connection_catalog_mock, f_module, catalog_info1, [34])

    @pytest.mark.parametrize("check_mode", [True, False])
    def test_ome_catalog_firmware_validate_delete_operation_case4(self, check_mode, ome_response_mock,
                                                                  ome_connection_catalog_mock):
        f_module = self.get_module_mock(
            params={"catalog_name": ["catalog_http3", "catalog_online2"]}, check_mode=check_mode)
        with pytest.raises(Exception) as err:
            self.module.validate_delete_operation(ome_connection_catalog_mock, f_module, [], [])
        assert err.value.args[0] == CHECK_MODE_CHANGE_NOT_FOUND_MSG

    def test_ome_catalog_firmware_delete_catalog(self, mocker, ome_connection_catalog_mock, ome_response_mock):
        mocker.patch(MODULE_PATH + 'validate_delete_operation', return_value=None)
        ome_response_mock.json_data = [1, 2]
        f_module = self.get_module_mock(params={"state": "absent", "catalog_id": [1, 2]})
        with pytest.raises(Exception) as err:
            self.module.delete_catalog(f_module, ome_connection_catalog_mock, catalog_info["value"])
        assert err.value.args[0] == CATALOG_DEL_SUCCESS

    @pytest.mark.parametrize("exc_type",
                             [IOError, ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_catalog_firmware_main_exception_failure_case(self, exc_type, mocker, ome_default_args,
                                                              ome_connection_catalog_mock, ome_response_mock):
        ome_default_args.update({"catalog_name": "catalog1", "repository_type": "HTTPS"})
        ome_response_mock.status_code = 400
        ome_response_mock.success = False
        json_str = to_text(json.dumps({"info": "error_details"}))
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'validate_names', side_effect=exc_type("url open error"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'validate_names', side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'validate_names',
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'msg' in result

    @pytest.mark.parametrize("param", [{"state": "absent", "catalog_id": [1, 2]},
                                       {"state": "absent", "catalog_name": ["abc", "xyz"]}])
    def test_ome_catalog_firmware_validate_names(self, param):
        f_module = self.get_module_mock(params=param)
        self.module.validate_names("absent", f_module)

    @pytest.mark.parametrize("param", [{"state": "present", "catalog_id": [1, 2]},
                                       {"state": "present", "catalog_name": ["abc", "xyz"]}])
    def test_ome_catalog_firmware_validate_names_exception_case(self, param):
        f_module = self.get_module_mock(params=param)
        with pytest.raises(Exception) as err:
            self.module.validate_names("present", f_module)
        assert err.value.args[0] == NAMES_ERROR

    def test_ome_catalog_firmware_argument_exception_case1(self, ome_default_args):
        ome_default_args.update({"catalog_name": "t1"})
        result = self._run_module_with_fail_json(ome_default_args)
        assert result["msg"] == "state is present but all of the following are missing: repository_type"

    def test_ome_catalog_firmware_argument_exception_case2(self, ome_default_args):
        ome_default_args.update({"catalog_id": 1})
        result = self._run_module_with_fail_json(ome_default_args)
        assert result["msg"] == "state is present but all of the following are missing: repository_type"

    def test_ome_catalog_firmware_argument_exception_case3(self, ome_default_args):
        result = self._run_module_with_fail_json(ome_default_args)
        assert result["msg"] == "one of the following is required: catalog_name, catalog_id"

    def test_ome_catalog_firmware_argument_exception_case4(self, ome_default_args):
        ome_default_args.update({"repository_type": "HTTPS", "catalog_name": "t1", "catalog_id": 1})
        result = self._run_module_with_fail_json(ome_default_args)
        assert result["msg"] == "parameters are mutually exclusive: catalog_name|catalog_id"
