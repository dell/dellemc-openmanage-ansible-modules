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
from mock import mock_open
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
NO_OPERATION_SKIP = "Task is skipped as operation is not specified."
SUCCESS_COMPLETE = "Successfully applied the BIOS attributes update."
BIOS_JOB_RUNNING = "BIOS Config job is already running. Wait for the job to complete."
SCHEDULED_SUCCESS = "Successfully scheduled the job for the BIOS attributes update."
COMMITTED_SUCCESS = "Successfully committed changes. The job is in pending state. The changes will be applied ay next reboot."
PROVIDE_ABSOLUTE_PATH = "Please provide absolute path of the certificate file {path}"
NO_READ_PERMISSION_PATH = "Unable to read the certificate file {path}."
NO_VALID_PATHS = "No valid absolute path found for certificate(s)."
HOST_RESTART_FAILED = "Unable to restart the host. Check the host status and restart the host manually."
CHANGES_FOUND = 'Changes found to be applied.'
FAILED_IMPORT = "Failed to import certificate file {path} for {parameter}."
NO_IMPORT_SUCCESS = "The Secure Boot Certificate Import operation was not successful."
IMPORT_REQUIRED_IF = "import_certificates is True but any of the following are missing: \
platform_key, KEK, database, disallow_database"
EXPORT_REQUIRED_IF = "export_certificates is True but any of the following are missing: \
platform_key, KEK, database, disallow_database"
IMPORT_EXPORT_MUTUALLY_EXCLUSIVE = "parameters are mutually exclusive: import_certificates|export_certificates"
SUCCESS_EXPORT_MSG = 'Successfully exported the SecureBoot certificate.'
UNSUCCESSFUL_EXPORT_MSG = 'Failed to export the SecureBoot certificate.'
NO_CHANGES_FOUND = 'No changes found to be applied.'
odata = '@odata.id'
INVOKE_REQ_KEY = "idrac_secure_boot.iDRACRedfishAPI.invoke_request"
get_log_function = "idrac_secure_boot.get_lc_log_or_current_log_time"
OS_ABS_FN = "os.path.isabs"
OS_ACCESS_FN = "os.access"
HTTP_ERROR_MSG = 'Http error message'
RETURN_TYPE = "application/json"
GET_DYNAMIC_URI = "idrac_secure_boot.get_dynamic_uri"
HTTP_ERROR_URL = 'https://testhost.com'
RESET_HOST_KEY = 'idrac_secure_boot.IDRACAttributes.reset_host'
JOB_RACKING_KEY = "idrac_secure_boot.idrac_redfish_job_tracking"
VALIDATE_RESOURCE_KEY = 'idrac_secure_boot.validate_and_get_first_resource_id_uri'
JOB_FAILED_MSG = 'Job Failed'


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

        mocker.patch(MODULE_PATH + GET_DYNAMIC_URI,
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
        idrac_secure_boot_mock.invoke_request.side_effect = HTTPError(HTTP_ERROR_URL, 400,
                                                                      HTTP_ERROR_MSG,
                                                                      {"accept-type": RETURN_TYPE},
                                                                      StringIO('HTTP 400: Bad Request'))
        mocker.patch(MODULE_PATH + get_log_function,
                     side_effect=mock_get_lc_log_scheduled)
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == SCHEDULE_MSG
        assert resp['changed'] is False

    def test_attributes_secure_boot(self, idrac_default_args, idrac_connection_secure_boot,
                                    idrac_secure_boot_mock, mocker):
        uri = '/redfish/v1/Systems/System.Embedded.1'
        atttr_resp = {
            "Attributes": {
                "BootMode": "Uefi",
                "SecureBoot": "Enabled",
                "SecureBootMode": "UserMode",
                "SecureBootPolicy": "Standard",
                "force_int_10": "Disabled"
            },
            "@Redfish.Settings": {
                "SettingsObject": {
                    odata: "/redfish/v1/Systems/System.Embedded.1/Bios/Settings"
                }
            }
        }
        bios = {
            odata: "/redfish/v1/Systems/System.Embedded.1/Bios"}
        reset_idrac = {
            "#ComputerSystem.Reset": {
                "target": "/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset"
            }
        }
        job_dict = {
            "Id": "job_1", "JobType": "BIOSConfiguration", "JobState": "Completed"
        }

        def mock_get_dynamic_uri_request(*args, **kwargs):
            length = len(args)
            if length > 2:
                if args[2] == 'Bios':
                    return bios
                elif args[2] == 'SecureBoot':
                    return reset_idrac
            else:
                return atttr_resp

        mocker.patch(MODULE_PATH + GET_DYNAMIC_URI,
                     side_effect=mock_get_dynamic_uri_request)
        mocker.patch(MODULE_PATH + "idrac_secure_boot.validate_and_get_first_resource_id_uri",
                     return_value=(uri, ''))

        # Scenario 1: When secure_boot is enabled when already enabled in check_mode
        idrac_default_args.update({'secure_boot': 'Enabled'})
        resp = self._run_module(idrac_default_args, check_mode=True)
        assert resp['msg'] == NO_CHANGES_FOUND
        assert resp['changed'] is False

        # Scenario 2: When secure_boot is enabled when already enabled in normal mode
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == NO_CHANGES_FOUND
        assert resp['skipped'] is True

        # Scenario 3: When secure_boot_policy is Custom, update happens in check_mode
        idrac_default_args.update({'secure_boot_policy': 'Custom'})
        resp = self._run_module(idrac_default_args, check_mode=True)
        assert resp['msg'] == CHANGES_FOUND
        assert resp['changed'] is True

        # Scenario 4: When secure_boot_policy is Custom, update happens in normal mode and restart is False
        obj = MagicMock()
        obj2 = MagicMock()
        obj.status_code = 200
        obj.json_data = {'Attributes': {}, 'PowerState': 'On'}
        obj.headers = {'Location': '/redfish/v1/TaskService/Tasks/Job_ID'}
        obj2.status_code = 204
        obj2.json_data = {'Members': [{'JobType': 'BIOSConfiguration', 'JobState': 'Scheduled', 'Id': 'Job_ID'}],
                          'PowerState': 'Off'}
        idrac_default_args.update({'secure_boot_policy': 'Custom'})
        idrac_default_args.update({'restart': False})
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, side_effect=[obj, obj2, obj, obj, obj, obj, obj2, obj2, obj2, obj])
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == COMMITTED_SUCCESS
        assert resp['changed'] is True

        # Scenario 5: When secure_boot_policy is Custom, update happens in normal mode and restart is True but job_wait false
        idrac_default_args.update({'restart': True, 'job_wait': False})
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, side_effect=[obj, obj2, obj, obj])
        mocker.patch(MODULE_PATH + RESET_HOST_KEY, return_value=True)
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == SCHEDULED_SUCCESS
        assert resp['changed'] is True

        # Scenario 6: When secure_boot_policy is Custom, update happens in normal mode and restart is True and job_wait True
        idrac_default_args.update({'restart': True, 'job_wait': True})
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, side_effect=[obj, obj2, obj, obj])
        mocker.patch(MODULE_PATH + RESET_HOST_KEY, return_value=True)
        mocker.patch(MODULE_PATH + JOB_RACKING_KEY,
                     return_value=(False, 'successfull', job_dict, 10))
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == SUCCESS_COMPLETE
        assert resp['changed'] is True
        assert resp['job_status'] == job_dict

        # Scenario 7: When boot_mode is Bios, validate_and_get_first_resource_id_uri givess error
        del idrac_default_args['secure_boot_policy']
        atttr_resp['Attributes']['SecureBoot'] = 'Disabled'
        idrac_default_args.update({'boot_mode': 'Bios'})
        mocker.patch(MODULE_PATH + VALIDATE_RESOURCE_KEY, return_value=(uri, "Error"))
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == "Error"
        assert resp['failed'] is True

        # Scenario 8: When boot_mode is Bios, already a BIOS job is running
        mocker.patch(MODULE_PATH + VALIDATE_RESOURCE_KEY, return_value=(uri, ""))
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, side_effect=[obj, obj2, obj, obj])
        mocker.patch(MODULE_PATH + 'idrac_secure_boot.IDRACAttributes.check_scheduled_bios_job', return_value="Job_ID")
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == BIOS_JOB_RUNNING
        assert resp['failed'] is True

        # Scenario 9: When boot_mode is Bios, restart fails
        obj2.json_data = {'Members': [],
                          'PowerState': 'Off'}
        mocker.patch(MODULE_PATH + VALIDATE_RESOURCE_KEY, return_value=(uri, ""))
        mocker.patch(MODULE_PATH + 'idrac_secure_boot.IDRACAttributes.check_scheduled_bios_job', return_value="")
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, side_effect=[obj, obj, obj])
        mocker.patch(MODULE_PATH + RESET_HOST_KEY, return_value=False)
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == HOST_RESTART_FAILED
        assert resp['failed'] is True

        # Scenario 10: When force_int_10 is Enabled, Job tracking fails
        del idrac_default_args['boot_mode']
        idrac_default_args.update({'force_int_10': 'Enabled'})
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, side_effect=[obj, obj2, obj, obj])
        mocker.patch(MODULE_PATH + RESET_HOST_KEY, return_value=True)
        mocker.patch(MODULE_PATH + JOB_RACKING_KEY,
                     return_value=(True, JOB_FAILED_MSG, job_dict, 10))
        resp = self._run_module(idrac_default_args)
        assert resp['msg'] == JOB_FAILED_MSG
        assert resp['failed'] is True

        # Scenario 11: When Secure_boot is Enabled, but force_int_10 is Enabled
        del idrac_default_args['force_int_10']
        json_str = to_text(json.dumps({"data": "out"}))
        atttr_resp['Attributes']['secure_boot'] = 'Disabled'
        idrac_default_args.update({'secure_boot': 'Enabled'})
        atttr_resp['Attributes']['force_int_10'] = 'Enabled'
        mocker.patch(MODULE_PATH + INVOKE_REQ_KEY, side_effect=[obj])
        mocker.patch(MODULE_PATH + RESET_HOST_KEY, return_value=True)
        mocker.patch(MODULE_PATH + "idrac_secure_boot.IDRACAttributes.apply_attributes",
                     side_effect=HTTPError(HTTP_ERROR_URL, 400,
                                           HTTP_ERROR_MSG,
                                           {"accept-type": RETURN_TYPE},
                                           StringIO(json_str)))
        mocker.patch(MODULE_PATH + JOB_RACKING_KEY,
                     return_value=(False, 'Success', job_dict, 10))
        try:
            self._run_module(idrac_default_args)
        except Exception as ex:
            assert isinstance(ex, HTTPError)
            assert ex.value.args[0]["msg"] == "HTTP Error 400: Bad Request"
            assert ex.value.args[0]["failed"] is True

    def test_export_secure_boot(self, idrac_default_args, idrac_connection_secure_boot,
                                idrac_secure_boot_mock, mocker):
        mapping_uri_resp = {'database': "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/db",
                                        'disallow_database': "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/dbx",
                                        'KEK': "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/KEK",
                                        'platform_key': "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/PK"}

        members = [
            {
                "@odata.id": "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/dbx/Certificates/CustSecbootpolicy.222"},
            {
                "@odata.id": "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/dbx/Certificates/CustSecbootpolicy.278"}]
        certificates = {
            odata: "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/db/Certificates"}

        resp_idrac = {'CertificateType': 'PEM',
                      'CertificateString': '---BEGIN CERT---'}

        # Scenario 1: When import and export both is given
        idrac_default_args.update({'import_certificates': True,
                                   'export_certificates': True,
                                   'database': '/XYZ/export/db'
                                   })
        with pytest.raises(Exception) as ex:
            self._run_module(idrac_default_args)
        assert ex.value.args[0]["msg"] == IMPORT_EXPORT_MUTUALLY_EXCLUSIVE
        assert ex.value.args[0]["failed"] is True

        # Scenario 2: When export is given but other parameters are missing
        del idrac_default_args['import_certificates']
        del idrac_default_args['database']
        idrac_default_args.update({'export_certificates': True})
        with pytest.raises(Exception) as ex:
            self._run_module(idrac_default_args)
        assert ex.value.args[0]["msg"] == EXPORT_REQUIRED_IF
        assert ex.value.args[0]["failed"] is True

        # Scenario 3: when multiple path is given
        idrac_default_args.update({'database': ['/XYZ/db1', '/XYZ/db2']})
        data = self._run_module(idrac_default_args)
        assert data['msg'] == UNSUCCESSFUL_EXPORT_MSG
        assert data['failed'] is True

        def mock_get_dynamic_uri_request(*args, **kwargs):
            length = len(args)
            if length > 2:
                if args[2] == 'Members':
                    return members
                elif args[2] == 'Certificates':
                    return certificates
            else:
                return resp_idrac

        # Scenario 4: When file path is given
        idrac_default_args.update({'database': ['/XYZ/abc.txt']})
        data = self._run_module(idrac_default_args)
        assert data['msg'] == UNSUCCESSFUL_EXPORT_MSG
        assert data['failed'] is True

        # Scenario 5: when single path is given
        mocker.patch("os.path.isdir", return_value=True)
        mocker.patch(OS_ACCESS_FN, return_value=True)
        mocker.patch("builtins.open", side_effect=mock_open(read_data="data"), create=True)
        mocker.patch(MODULE_PATH + GET_DYNAMIC_URI,
                     side_effect=mock_get_dynamic_uri_request)
        mocker.patch(MODULE_PATH + "idrac_secure_boot.IDRACSecureBoot.mapping_secure_boot_database_uri",
                     return_value=mapping_uri_resp)
        del idrac_default_args['database']
        idrac_default_args.update({'database': ['/XYZ/']})
        data = self._run_module(idrac_default_args)
        assert data['msg'] == SUCCESS_EXPORT_MSG
        assert data['changed'] is False

        # Scenario 6: When single path is given in check mode
        data = self._run_module(idrac_default_args, check_mode=True)
        assert data['msg'] == CHANGES_FOUND
        assert data['changed'] is True

        # Scenario 7: When no path is given in check mode
        idrac_default_args.update({'database': []})
        data = self._run_module(idrac_default_args, check_mode=True)
        assert data['msg'] == NO_CHANGES_FOUND
        assert data['changed'] is False

        # Scenario 8: Directory does not have write permission
        mocker.patch(OS_ACCESS_FN, return_value=False)
        idrac_default_args.update({'database': ['/XYZ/']})
        data = self._run_module(idrac_default_args)
        assert data['msg'] == UNSUCCESSFUL_EXPORT_MSG
        assert data['failed'] is True

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
                         side_effect=exc_type(HTTP_ERROR_URL, 400,
                                              HTTP_ERROR_MSG,
                                              {"accept-type": RETURN_TYPE},
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
