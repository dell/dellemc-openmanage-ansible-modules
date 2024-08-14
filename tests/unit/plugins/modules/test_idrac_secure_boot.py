# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.6.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ast import arg
import json
from io import StringIO

import pytest
import tempfile
import os
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
SUCCESS_MSG = "The Secure Boot Certificate Import operation has completed successfully."
SCHEDULE_MSG = "The SecureBoot Certificate Import operation is successfully scheduled. Restart the host server for the changes to take effect."
NO_OPERATION_SKIP = "Task is skipped as import is 'false'."
PROVIDE_ABSOLUTE_PATH = "Please provide absolute path of the certificate file {path}"
NO_READ_PERMISSION_PATH = "Unable to read the certificate file {path}."
NO_VALID_PATHS = "No valid absolute path found for certificate(s)."
CHANGES_FOUND = 'Changes found to be applied.'
FAILED_IMPORT = "Failed to import certificate file {path}."
NO_IMPORT_SUCCESS = "The Secure Boot Certificate Import operation was not successful."
odata = '@odata.id'


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

    def test_import_certificates(self, idrac_default_args, idrac_connection_secure_boot,
                                                     idrac_secure_boot_mock, mocker):
        secure_boot = {"@odata.id": "/redfish/v1/Systems/System.Embedded.1/SecureBoot"}
        secure_boot_databases = {"@odata.id": "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases"}
        secure_boot_database_members = [
            {
            "@odata.id": "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/db"
            },
            {
            "@odata.id": "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/dbx"
            },
            {
            "@odata.id": "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/KEK"
            },
            {
            "@odata.id": "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/PK"
            }
            ]
        certificates = {
                "@odata.id": "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/db/Certificates"
                }
        curr_time = "2024-08-13T17:15:06-05:00"

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
            if args[2]:
                return True, SUCCESS_MSG
            return curr_time

        mocker.patch(MODULE_PATH + "idrac_secure_boot.get_dynamic_uri",
                     side_effect=mock_get_dynamic_uri_request)
        mocker.patch(MODULE_PATH + "idrac_secure_boot.validate_and_get_first_resource_id_uri",
                     return_value=(self.uri, ''))
        
        # Scenario 1: When import_certificates is false
        idrac_default_args.update({'import_certificates': False})
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == NO_OPERATION_SKIP
        assert resp['skipped'] == True

        # Scenario 2: When import_certificates is True, other parameters is empty
        idrac_default_args.update({'import_certificates': True})
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == NO_VALID_PATHS
        assert resp['skipped'] == True

        # Scenario 3: When import_certificates is True, invalid path is given
        idrac_default_args.update({'import_certificates': True,
                                   'database': ['/tmp/invalid_path.pem']})
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == NO_VALID_PATHS
        assert resp['skipped'] == True

        # Scenaro 4: When import_certificates is True, path doesn't have read permission
        mocker.patch(MODULE_PATH + "idrac_secure_boot.get_lc_log_or_current_log_time",
                     side_effect=mock_get_lc_log_scheduled)
        mocker.patch("os.path.isabs", return_value=True)
        mocker.patch("os.access", return_value=False)
        idrac_default_args.update({'import_certificates': True,
                                    'database': ['/tmp/invalid_path.pem']})
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == NO_VALID_PATHS
        assert resp['changed'] == False

        # # Scenaro 5: When import_certificates is True, valid path is given
        # mocker.patch(MODULE_PATH + "idrac_secure_boot.get_lc_log_or_current_log_time",
        #              side_effect=mock_get_lc_log_scheduled)
        # mocker.patch("os.path.isabs", return_value=True)
        # mocker.patch("os.access", return_value=True)
        # mocker.patch("os.path.isfile", return_value=True)
        # idrac_default_args.update({'import_certificates': True,
        #                             'database': ['/tmp/invalid_path.pem']})
        # resp = self._run_module(idrac_default_args)
        # assert resp['msg'] == SCHEDULE_MSG
        # assert resp['changed'] == False

    # @pytest.mark.parametrize("exc_type",
    #                          [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    # def test_idrac_secure_boot_main_exception_handling_case(self, exc_type, mocker, idrac_default_args,
    #                                                                idrac_connection_secure_boot, idrac_secure_boot_mock):
    #     obj = MagicMock()
    #     obj.perform_validation_for_network_adapter_id.return_value = None
    #     obj.perform_validation_for_network_device_function_id.return_value = None
    #     obj.get_diff_between_current_and_module_input.return_value = (
    #         None, None)
    #     obj.validate_job_timeout.return_value = None
    #     obj.clear_pending.return_value = None
    #     idrac_default_args.update({'apply_time': "Immediate",
    #                                'network_adapter_id': 'Some_adapter_id',
    #                                'network_device_function_id': 'some_device_id',
    #                                'clear_pending': True if exec == 'URLError' else False})
    #     json_str = to_text(json.dumps({"data": "out"}))
    #     if exc_type in [HTTPError, SSLValidationError]:
    #         tmp = {'network_attributes': {'VlanId': 10}}
    #         mocker.patch(MODULE_PATH + "idrac_secure_boot.IDRACNetworkAttributes.set_dynamic_base_uri_and_validate_ids",
    #                      side_effect=exc_type('https://testhost.com', 400,
    #                                           'http error message',
    #                                           {"accept-type": "application/json"},
    #                                           StringIO(json_str)))
    #     else:

    #         tmp = {'oem_network_attributes': {'VlanId': 10}}
    #         mocker.patch(MODULE_PATH + "idrac_secure_boot.IDRACNetworkAttributes.set_dynamic_base_uri_and_validate_ids",
    #                      side_effect=exc_type('test'))
    #     idrac_default_args.update(tmp)
    #     result = self._run_module(idrac_default_args)
    #     if exc_type == URLError:
    #         assert result['unreachable'] is True
    #     else:
    #         assert result['failed'] is True
    #     assert 'msg' in result
