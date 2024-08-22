# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.6.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from io import StringIO

import pytest
from ansible.module_utils._text import to_text
from urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import \
    idrac_secure_boot
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import \
    FakeAnsibleModule
from mock import MagicMock

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'

TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The value for the 'job_wait_timeout' parameter cannot be negative or zero."
SUCCESS_MSG = "Successfully imported the SecureBoot certificate."
SCHEDULE_MSG = "The SecureBoot Certificate Import operation is successfully scheduled. Restart the host server for the changes to take effect."
NO_OPERATION_SKIP = "Task is skipped as import_certificates is 'false'."
PROVIDE_ABSOLUTE_PATH = "Please provide absolute path of the certificate file {path}"
NO_READ_PERMISSION_PATH = "Unable to read the certificate file {path}."
NO_VALID_PATHS = "No valid absolute path found for certificate(s)."
CHANGES_FOUND = 'Changes found to be applied.'
FAILED_IMPORT = "Failed to import certificate file {path} for {parameter}."
NO_IMPORT_SUCCESS = "The Secure Boot Certificate Import operation was not successful."
IMPORT_REQUIRED_IF = "import_certificates is True but any of the following are missing: \
platform_key, KEK, database, disallow_database"
odata = '@odata.id'
get_log_function = "idrac_secure_boot.get_lc_log_or_current_log_time"
OS_ABS_FN = "os.path.isabs"
OS_ACCESS_FN = "os.access"


class TestIDRACSecureBoot(FakeAnsibleModule):
    module = idrac_secure_boot
    uri = '/redfish/v1/api'

    @pytest.fixture
    def idrac_secure_boot_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_secure_boot(self, mocker, idrac_secure_boot_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'idrac_secure_boot.iDRACRedfishAPI',
                                       return_value=idrac_secure_boot_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_secure_boot_mock
        return idrac_conn_mock

    def test_import_secure_boot(self, idrac_default_args, idrac_connection_secure_boot,
                                idrac_secure_boot_mock, mocker):
        secure_boot = {
            odata: "/redfish/v1/Systems/System.Embedded.1/SecureBoot"}
        secure_boot_databases = {
            odata: "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases"}
        secure_boot_database_members = [{odata: "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/db"},
                                        {odata: "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/dbx"},
                                        {odata: "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/KEK"},
                                        {odata: "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/PK"}
                                        ]
        certificates = {
            odata: "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/db/Certificates"}
        curr_time = "2024-08-13T17:15:06-05:00"
        invalid_pem_file_path = '/XX/YY/ZZ.pem'

        def mock_get_dynamic_uri_request(*args, **kwargs):
            if args[2] == 'SecureBoot':
                return secure_boot
            elif args[2] == 'SecureBootDatabases':
                return secure_boot_databases
            elif args[2] == 'Members':
                return secure_boot_database_members
            elif args[2] == 'Certificates':
                return certificates
            else:
                return {}

        def mock_get_lc_log_scheduled(*args, **kwargs):
            if args[0]:
                return True, SCHEDULE_MSG
            return curr_time

        def mock_get_lc_log_success(*args, **kwargs):
            if args[0]:
                return True, SUCCESS_MSG
            return curr_time

        def mock_get_no_lc_log(*args, **kwargs):
            if args[0]:
                return False, 'some msg'
            return curr_time

        mocker.patch(MODULE_PATH + "idrac_secure_boot.get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)
        mocker.patch(MODULE_PATH + "idrac_secure_boot.validate_and_get_first_resource_id_uri",
                     return_value=(self.uri, ''))

        # Scenario 1: When import_certificates is false
        idrac_default_args.update({'import_certificates': False})
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == NO_OPERATION_SKIP
        assert resp['skipped'] is True

        # Scenario 2: When import_certificates is True, other parameters is empty
        idrac_default_args.update({'import_certificates': True})
        with pytest.raises(Exception) as ex:
            self._run_module(idrac_default_args)
        assert ex.value.args[0]["msg"] == IMPORT_REQUIRED_IF
        assert ex.value.args[0]["failed"] is True

        # Scenario 3: When import_certificates is True, invalid path is given
        idrac_default_args.update({'import_certificates': True,
                                   'database': [invalid_pem_file_path]})
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == NO_VALID_PATHS
        assert resp['skipped'] is True

        # Scenaro 4: When import_certificates is True, path doesn't have read permission
        mocker.patch(MODULE_PATH + get_log_function,
                     side_effect=mock_get_lc_log_scheduled)
        mocker.patch(OS_ABS_FN, return_value=False)
        mocker.patch(OS_ACCESS_FN, return_value=False)
        idrac_default_args.update({'import_certificates': True,
                                   'database': [invalid_pem_file_path]})
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == NO_VALID_PATHS
        assert resp['changed'] is False

        # Scenario 5: When No LC log found after import operation
        mocker.patch(MODULE_PATH + get_log_function,
                     side_effect=mock_get_no_lc_log)
        mocker.patch(MODULE_PATH + "idrac_secure_boot.IDRACImportSecureBoot.read_certificate_file",
                     return_value='some data in file')
        mocker.patch(OS_ABS_FN, return_value=True)
        mocker.patch(OS_ACCESS_FN, return_value=True)
        mocker.patch("os.path.isfile", return_value=True)
        idrac_default_args.update({'import_certificates': True,
                                   'platform_key': invalid_pem_file_path,
                                   'KEK': [invalid_pem_file_path],
                                   'database': [invalid_pem_file_path],
                                   'disallow_database': [invalid_pem_file_path]})
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == NO_IMPORT_SUCCESS
        assert resp['skipped'] is True

        # Scenario 6: When import_certificates is True, valid path is given
        mocker.patch(MODULE_PATH + get_log_function,
                     side_effect=mock_get_lc_log_scheduled)
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == SCHEDULE_MSG
        assert resp['changed'] is False

        # Scenario 7: When above scenario is running in check mode
        resp = self._run_module(idrac_default_args, check_mode=True)
        assert resp['msg'] == CHANGES_FOUND
        assert resp['changed'] is True

        # Scenario 8: When job_wait_timeout is negative
        idrac_default_args.update({'import_certificates': True,
                                   'database': [invalid_pem_file_path],
                                   'job_wait_timeout': -11})
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == TIMEOUT_NEGATIVE_OR_ZERO_MSG
        assert resp['failed'] is True

        # Scenario 9: When restart is True
        obj = MagicMock()
        obj.success = 'OK'
        mocker.patch(MODULE_PATH + "idrac_secure_boot.trigger_restart_operation",
                     return_value=(obj, 'Error in triggering restart'))
        mocker.patch(MODULE_PATH + "idrac_secure_boot.wait_for_lc_status",
                     return_value=(True, 'some msg'))
        mocker.patch(MODULE_PATH + get_log_function,
                     side_effect=mock_get_lc_log_success)
        idrac_default_args.update({'import_certificates': True,
                                   'database': [invalid_pem_file_path],
                                   'restart': True,
                                   'job_wait_timeout': 300})
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == SUCCESS_MSG
        assert resp['changed'] is True

        # Sceneario 10: When got error during LC status waiting
        error_msg = 'Timeout during LC status'
        mocker.patch(MODULE_PATH + "idrac_secure_boot.wait_for_lc_status",
                     return_value=(False, error_msg))
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == error_msg
        assert resp['failed'] is True

        # Scenario 11: When invalid certificate is given
        obj.success = False
        mocker.patch(MODULE_PATH + "idrac_secure_boot.trigger_restart_operation",
                     return_value=(obj, 'Error in triggering restart'))
        idrac_secure_boot_mock.invoke_request.side_effect = HTTPError('https://testhost.com', 400,
                                                                      'http error message',
                                                                      {"accept-type": "application/json"},
                                                                      StringIO('HTTP 400: Bad Request'))
        mocker.patch(MODULE_PATH + get_log_function,
                     side_effect=mock_get_lc_log_scheduled)
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == SCHEDULE_MSG
        assert resp['changed'] is False

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_idrac_secure_boot_main_exception_handling_case(self, exc_type, mocker, idrac_default_args,
                                                            idrac_connection_secure_boot, idrac_secure_boot_mock):
        obj = MagicMock()
        invalid_pem_file_path = '/XX/YY/ZZ.pem'
        obj.perform_operation.return_value = None
        obj.validate_job_timeout.return_value = None
        mocker.patch(OS_ABS_FN, return_value=True)
        mocker.patch(OS_ACCESS_FN, return_value=True)
        mocker.patch("os.path.isfile", return_value=True)
        idrac_default_args.update({'import_certificates': True,
                                   'database': [invalid_pem_file_path]})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + "idrac_secure_boot.IDRACImportSecureBoot.perform_operation",
                         side_effect=exc_type('https://testhost.com', 400,
                                              'http error message',
                                              {"accept-type": "application/json"},
                                              StringIO(json_str)))
        else:
            mocker.patch(MODULE_PATH + "idrac_secure_boot.IDRACImportSecureBoot.perform_operation",
                         side_effect=exc_type('test'))
        result = self._run_module(idrac_default_args)
        if exc_type == URLError:
            assert result['unreachable'] is True
        else:
            assert result['failed'] is True
        assert 'msg' in result
