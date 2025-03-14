# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.10.0
# Copyright (C) 2022-2024 Dell Inc. or its subsidiaries. All Rights Reserved.

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
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_certificates
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from unittest.mock import MagicMock

IMPORT_SSL_CERTIFICATE = "#DelliDRACCardService.ImportSSLCertificate"
EXPORT_SSL_CERTIFICATE = "#DelliDRACCardService.ExportSSLCertificate"
IDRAC_CARD_SERVICE_ACTION_URI = "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions"
IDRAC_CARD_SERVICE_ACTION_URI_RES_ID = "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DelliDRACCardService/Actions"

NOT_SUPPORTED_ACTION = "Certificate '{operation}' not supported for the specified certificate type '{cert_type}'."
SUCCESS_MSG = "Successfully performed the '{command}' certificate operation."
SUCCESS_MSG_SSL = "Successfully performed the SSL key upload and '{command}' certificate operation."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_MSG = "Changes found to be applied."
WAIT_NEGATIVE_OR_ZERO_MSG = "The value for the `wait` parameter cannot be negative or zero."
SSL_KEY_MSG = "Unable to locate the SSL key file at {ssl_key}."
SSK_KEY_NOT_SUPPORTED = "Upload of SSL key not supported"
NO_RESET = "Reset iDRAC to apply the new certificate. Until the iDRAC is reset, the old certificate will remain active."
RESET_UNTRACK = " iDRAC reset is in progress. Until the iDRAC is reset, the changes would not apply."
RESET_SUCCESS = "iDRAC has been reset successfully."
RESET_FAIL = " Unable to reset the iDRAC. For changes to reflect, manually reset the iDRAC."
SYSTEM_ID = "System.Embedded.1"
MANAGER_ID = "iDRAC.Embedded.1"
SYSTEMS_URI = "/redfish/v1/Systems"
MANAGERS_URI = "/redfish/v1/Managers"
IDRAC_SERVICE = "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService"
CSR_SSL = "/redfish/v1/CertificateService/Actions/CertificateService.GenerateCSR"
IMPORT_SSL = f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.ImportSSLCertificate"
UPLOAD_SSL = f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.UploadSSLKey"
EXPORT_SSL = f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.ExportSSLCertificate"
RESET_SSL = f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.SSLResetCfg"
IDRAC_RESET = "/redfish/v1/Managers/{res_id}/Actions/Manager.Reset"
idrac_service_actions = {
    "#DelliDRACCardService.DeleteCertificate": f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.DeleteCertificate",
    "#DelliDRACCardService.ExportCertificate": f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.ExportCertificate",
    EXPORT_SSL_CERTIFICATE: EXPORT_SSL,
    "#DelliDRACCardService.FactoryIdentityCertificateGenerateCSR":
        f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.FactoryIdentityCertificateGenerateCSR",
    "#DelliDRACCardService.FactoryIdentityExportCertificate":
        f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.FactoryIdentityExportCertificate",
    "#DelliDRACCardService.FactoryIdentityImportCertificate":
        f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.FactoryIdentityImportCertificate",
    "#DelliDRACCardService.GenerateSEKMCSR": f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.GenerateSEKMCSR",
    "#DelliDRACCardService.ImportCertificate": f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.ImportCertificate",
    IMPORT_SSL_CERTIFICATE: IMPORT_SSL,
    "#DelliDRACCardService.UploadSSLKey": UPLOAD_SSL,
    "#DelliDRACCardService.SSLResetCfg": f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.SSLResetCfg",
    "#DelliDRACCardService.iDRACReset": f"{IDRAC_CARD_SERVICE_ACTION_URI}/DelliDRACCardService.iDRACReset"
}
MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.idrac_certificates.'


@pytest.fixture
def idrac_redfish_mock_for_certs(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestIdracCertificates(FakeAnsibleModule):
    module = idrac_certificates

    @pytest.fixture
    def idrac_certificates_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_connection_certificates_mock(
            self, mocker, idrac_certificates_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'iDRACRedfishAPI',
                                       return_value=idrac_certificates_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_certificates_mock
        return idrac_conn_mock

    @pytest.mark.parametrize("params", [
        {"json_data": {"CertificateFile": b'Hello world!', "@Message.ExtendedInfo": [
            {
                "Message": "Successfully exported SSL Certificate.",
                "MessageId": "IDRAC.2.5.LC067",
                "Resolution": "No response action is required.",
                "Severity": "Informational"
            }]}, 'message': SUCCESS_MSG.format(command="export"), "success": True,
         "reset_idrac": (True, False, RESET_SUCCESS),
         'mparams': {'command': 'export', 'certificate_type': "HTTPS", 'certificate_path': tempfile.gettempdir(),
                     'reset': False}},
        {"json_data": {"CertificateFile": b'Hello world!'}, 'message': CHANGES_MSG, "success": True,
         "reset_idrac": (True, False, RESET_SUCCESS), 'check_mode': True,
         'mparams': {'command': 'import', 'certificate_type': "HTTPS", 'certificate_path': '.pem', 'reset': False}},
        {"json_data": {"CertificateFile": b'Hello world!', "ssl_key": b'Hello world!'}, 'message': CHANGES_MSG, "success": True,
         "reset_idrac": (True, False, RESET_SUCCESS), 'check_mode': True,
         'mparams': {'command': 'import', 'certificate_type': "HTTPS", 'certificate_path': '.pem', "ssl_key": '.pem', 'reset': False}},
        {"json_data": {}, 'message': "{0}{1}".format(SUCCESS_MSG.format(command="import"), NO_RESET), "success": True,
         "reset_idrac": (True, False, RESET_SUCCESS),
         'mparams': {'command': 'import', 'certificate_type': "HTTPS", 'certificate_path': '.pem', 'reset': False}},
        {"json_data": {}, 'message': "{0} {1}".format(SUCCESS_MSG_SSL.format(command="import"), NO_RESET), "success": True,
         "reset_idrac": (True, False, RESET_SUCCESS),
         'mparams': {'command': 'import', 'certificate_type': "HTTPS", 'certificate_path': '.pem', "ssl_key": '.pem', 'reset': False}},
        {"json_data": {}, 'message': SUCCESS_MSG.format(command="generate_csr"),
         "success": True,
         "get_cert_url": "url", "reset_idrac": (True, False, RESET_SUCCESS),
         'mparams': {'command': 'generate_csr', 'certificate_type': "HTTPS", 'certificate_path': tempfile.gettempdir(),
                     'cert_params': {
                         "common_name": "dell",
                         "country_code": "IN",
                         "email_address": "dell@dell.com",
                         "locality_name": "Bangalore",
                         "organization_name": "Dell",
                         "organization_unit": "ansible",
                         "state_name": "Karnataka",
                         "subject_alt_name": [
                             "emc"
                         ]}}},
        {"json_data": {}, 'message': NOT_SUPPORTED_ACTION.format(operation="generate_csr", cert_type="CA"),
         "success": True,
         "get_cert_url": "url", "reset_idrac": (True, False, RESET_SUCCESS),
         'mparams': {'command': 'generate_csr', 'certificate_type': "CA", 'certificate_path': tempfile.gettempdir(),
                     'cert_params': {
                         "common_name": "dell",
                         "country_code": "IN",
                         "email_address": "dell@dell.com",
                         "locality_name": "Bangalore",
                         "organization_name": "Dell",
                         "organization_unit": "ansible",
                         "state_name": "Karnataka",
                         "subject_alt_name": [
                             "emc"
                         ]}}},
        {"json_data": {}, 'message': "{0}{1}".format(SUCCESS_MSG.format(command="import"), RESET_SUCCESS),
         "success": True,
         "get_cert_url": "url", "reset_idrac": (True, False, RESET_SUCCESS),
         'mparams': {'command': 'import', 'certificate_type': "CA", 'passphrase': 'myphrase',
                     'certificate_path': '.p12'}},
        {"json_data": {}, 'message': "{0}{1}".format(SUCCESS_MSG.format(command="import"), RESET_SUCCESS),
         "success": True,
         "get_cert_url": "url", "reset_idrac": (True, False, RESET_SUCCESS),
         'mparams': {'command': 'import', 'certificate_type': "HTTPS", 'certificate_path': '.pem'}},
        {"json_data": {}, 'message': "{0} {1}".format(SUCCESS_MSG_SSL.format(command="import"), RESET_SUCCESS),
         "success": True,
         "get_cert_url": "url", "reset_idrac": (True, False, RESET_SUCCESS),
         'mparams': {'command': 'import', 'certificate_type': "HTTPS", 'certificate_path': '.pem', 'ssl_key': '.pem'}},
        {"json_data": {}, 'message': "{0}{1}".format(SUCCESS_MSG.format(command="import"), RESET_SUCCESS),
         "success": True,
         "reset_idrac": (True, False, RESET_SUCCESS),
         'mparams': {'command': 'import', 'certificate_type': "HTTPS", 'certificate_path': '.pem'}},
        {"json_data": {}, 'message': "{0} {1}".format(SUCCESS_MSG_SSL.format(command="import"), RESET_SUCCESS),
         "success": True,
         "reset_idrac": (True, False, RESET_SUCCESS),
         'mparams': {'command': 'import', 'certificate_type': "HTTPS", 'certificate_path': '.pem', "ssl_key": '.pem'}},
        {"json_data": {}, 'message': SUCCESS_MSG.format(command="export"), "success": True, "get_cert_url": "url",
         'mparams': {'command': 'export', 'certificate_type': "HTTPS", 'certificate_path': tempfile.gettempdir()}},
        {"json_data": {}, 'message': "{0}{1}".format(SUCCESS_MSG.format(command="reset"), RESET_SUCCESS),
         "success": True, "get_cert_url": "url", "reset_idrac": (True, False, RESET_SUCCESS),
         'mparams': {'command': 'reset', 'certificate_type': "HTTPS"}
         },
        {"json_data": {}, 'message': WAIT_NEGATIVE_OR_ZERO_MSG, "success": True,
         'mparams': {'command': 'import', 'certificate_type': "HTTPS", 'certificate_path': '.pem', 'wait': -1}},
        {"json_data": {}, 'message': WAIT_NEGATIVE_OR_ZERO_MSG, "success": True,
         'mparams': {'command': 'reset', 'certificate_type': "HTTPS", 'wait': 0}},
        {"json_data": {}, 'message': f"{SSL_KEY_MSG.format(ssl_key='/invalid/path')}", "success": True,
         'mparams': {'command': 'import', 'certificate_type': "HTTPS", 'certificate_path': '.pem', 'ssl_key': '/invalid/path'}}
    ])
    def test_idrac_certificates(
            self, params, idrac_connection_certificates_mock, idrac_default_args, mocker):
        idrac_connection_certificates_mock.success = params.get(
            "success", True)
        idrac_connection_certificates_mock.json_data = params.get('json_data')
        if params.get('mparams').get('certificate_path') and params.get(
                'mparams').get('command') == 'import':
            sfx = params.get('mparams').get('certificate_path')
            temp = tempfile.NamedTemporaryFile(suffix=sfx, delete=False)
            temp.write(b'Hello')
            temp.close()
            params.get('mparams')['certificate_path'] = temp.name
            if params.get('mparams').get('ssl_key') == '.pem':
                temp = tempfile.NamedTemporaryFile(suffix=sfx, delete=False)
                temp.write(b'Hello')
                temp.close()
                params.get('mparams')['ssl_key'] = temp.name
        mocker.patch(MODULE_PATH + 'get_res_id', return_value=MANAGER_ID)
        mocker.patch(
            MODULE_PATH + 'get_idrac_service',
            return_value=IDRAC_SERVICE.format(
                res_id=MANAGER_ID))
        mocker.patch(
            MODULE_PATH + 'get_actions_map',
            return_value=idrac_service_actions)
        # mocker.patch(MODULE_PATH + 'get_cert_url', return_value=params.get('get_cert_url'))
        # mocker.patch(MODULE_PATH + 'write_to_file', return_value=params.get('write_to_file'))
        mocker.patch(
            MODULE_PATH + 'reset_idrac',
            return_value=params.get('reset_idrac'))
        idrac_default_args.update(params.get('mparams'))
        result = self._run_module(
            idrac_default_args,
            check_mode=params.get(
                'check_mode',
                False))
        if params.get('mparams').get('command') == 'import' and params.get('mparams').get(
                'certificate_path') and os.path.exists(temp.name):
            os.remove(temp.name)
        assert result['msg'] == params['message']

    @pytest.mark.parametrize("params", [{"json_data": {"Members": [{"@odata.id": '/redfish/v1/Mangers/iDRAC.1'}]},
                                         "cert_type": 'Server', "res_id": "iDRAC.1"},
                                        {"json_data": {"Members": []},
                                         "cert_type": 'Server', "res_id": MANAGER_ID}
                                        ])
    def test_res_id(
            self, params, idrac_redfish_mock_for_certs, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        res_id = self.module.get_res_id(
            idrac_redfish_mock_for_certs,
            params.get('cert_type'))
        assert res_id == params['res_id']

    @pytest.mark.parametrize("params", [{"json_data": {
        "Links": {
            "Oem": {
                "Dell": {
                    "DelliDRACCardService": {
                        "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DelliDRACCardService"
                    }}}},
        "VirtualMedia": {
            "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia"}
    },
        "idrac_srv": '/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DelliDRACCardService', "res_id": "iDRAC.1"}
    ])
    def test_get_idrac_service(
            self, params, idrac_redfish_mock_for_certs, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        idrac_srv = self.module.get_idrac_service(
            idrac_redfish_mock_for_certs, params.get('res_id'))
        assert idrac_srv == params['idrac_srv']

    def test_write_to_file(self, idrac_default_args, mocker):
        temp_dir = 'XX/YY/'
        inv_dir = "invalid_temp_dir"
        idrac_default_args.update({"certificate_path": inv_dir})
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as ex:
            self.module.write_to_file(f_module, {}, "dkey")
        assert ex.value.args[0] == f"Provided directory path '{inv_dir}' is not valid."
        mocker.patch('os.path.exists', return_value=True)
        mocker.patch('os.access', return_value=False)
        idrac_default_args.update({"certificate_path": temp_dir})
        with pytest.raises(Exception) as ex:
            self.module.write_to_file(f_module, {}, "dkey")
        assert ex.value.args[0] == f"Provided directory path '{temp_dir}' is not writable. Please check if you have appropriate permissions."

    def test_upload_ssl_key(self, idrac_default_args, mocker):
        temp_ssl = tempfile.NamedTemporaryFile(delete=False)
        temp_ssl.write(b'ssl_key')
        temp_ssl.close()
        f_module = self.get_module_mock(params=idrac_default_args)
        with pytest.raises(Exception) as ex:
            self.module.upload_ssl_key(f_module, {}, {}, temp_ssl.name, "res_id")
        assert ex.value.args[0] == "Upload of SSL key not supported"
        mocker.patch('builtins.open', side_effect=OSError(0, "Permission denied"))
        with pytest.raises(Exception) as ex:
            self.module.upload_ssl_key(f_module, {}, {}, temp_ssl.name, "res_id")
        assert "Permission denied" in ex.value.args[0]
        os.remove(temp_ssl.name)

    def test_build_generate_csr_payload(self, idrac_default_args):
        cert_params_data = {
            "cert_params": {
                "subject_alt_name": ['192.198.2.1,192.198.2.2', 'X.X.X.X']
            }
        }
        idrac_default_args.update(cert_params_data)
        f_module = self.get_module_mock(params=idrac_default_args)
        payload = self.module._build_generate_csr_payload(f_module, None)
        assert payload["AlternativeNames"] == ['192.198.2.1,192.198.2.2,X.X.X.X']

    def test_perform_operation_and_download_csr(self, idrac_default_args):
        idrac, value = MagicMock(), MagicMock()
        value.json_data = {"CSRString": "value"}
        idrac.invoke_request = MagicMock(return_value=value)
        idrac_default_args.update({"timeout": 120})
        f_module = self.get_module_mock(params=idrac_default_args)
        payload = self.module.perform_operation_and_download_csr(idrac, None, None, None, f_module)
        assert "CSRString" in payload.json_data

    def test_check_csr_generated(self, mocker):
        idrac, value = MagicMock(), MagicMock()
        value.json_data = {"Attributes": {"Security.1.ConfigCertStatus": 2}}
        idrac.invoke_request = MagicMock(return_value=value)
        mocker.patch(MODULE_PATH + 'time.sleep', return_value=None)
        payload = self.module.check_csr_generated(idrac)
        assert payload is True

    def test_perform_operation_and_download_csr_with_HTTPError(self, idrac_default_args, mocker):
        idrac, value = MagicMock(), MagicMock()
        value.json_data = {"CSRString": "value"}
        err_info = '{"error":{"@Message.ExtendedInfo":[{"MessageId": "IDRAC.2.9.SYS537"}]}}'

        def mock_invoke_request(*args, **kwargs):
            if args[1] == 'POST':
                return value
            else:
                raise HTTPError('https://testhost.com', 503, "http error message",
                                {"accept-type": "application/json"}, StringIO(err_info))
        idrac.invoke_request = MagicMock(side_effect=mock_invoke_request)
        mocker.patch(MODULE_PATH + 'time.sleep', return_value=None)
        mocker.patch(MODULE_PATH + 'check_csr_generated', return_value=True)
        idrac_default_args.update({"timeout": 120})
        f_module = self.get_module_mock(params=idrac_default_args)
        payload = self.module.perform_operation_and_download_csr(idrac, None, "GET", None, f_module)
        assert payload.json_data["CSRString"] == "value"

    @pytest.mark.parametrize("params", [{"json_data": {
        "Actions": {
            EXPORT_SSL_CERTIFICATE: {
                "SSLCertType@Redfish.AllowableValues": ["CA", "CSC", "CustomCertificate", "ClientTrustCertificate", "Server"],
                "target":
                    f"{IDRAC_CARD_SERVICE_ACTION_URI_RES_ID}/DelliDRACCardService.ExportSSLCertificate"
            },
            IMPORT_SSL_CERTIFICATE: {
                "CertificateType@Redfish.AllowableValues": ["CA", "CSC", "CustomCertificate", "ClientTrustCertificate", "Server"],
                "target":
                    f"{IDRAC_CARD_SERVICE_ACTION_URI_RES_ID}/DelliDRACCardService.ImportSSLCertificate"
            },
            "#DelliDRACCardService.SSLResetCfg": {
                "target": f"{IDRAC_CARD_SERVICE_ACTION_URI_RES_ID}/DelliDRACCardService.SSLResetCfg"
            },
            "#DelliDRACCardService.UploadSSLKey": {
                "target": f"{IDRAC_CARD_SERVICE_ACTION_URI_RES_ID}/DelliDRACCardService.UploadSSLKey"}
        },
    },
        "idrac_service_uri": '/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DelliDRACCardService',
        "actions": {
            EXPORT_SSL_CERTIFICATE:
                f"{IDRAC_CARD_SERVICE_ACTION_URI_RES_ID}/DelliDRACCardService.ExportSSLCertificate",
            IMPORT_SSL_CERTIFICATE:
                f"{IDRAC_CARD_SERVICE_ACTION_URI_RES_ID}/DelliDRACCardService.ImportSSLCertificate",
            '#DelliDRACCardService.SSLResetCfg':
                f"{IDRAC_CARD_SERVICE_ACTION_URI_RES_ID}/DelliDRACCardService.SSLResetCfg",
            '#DelliDRACCardService.UploadSSLKey':
                f"{IDRAC_CARD_SERVICE_ACTION_URI_RES_ID}/DelliDRACCardService.UploadSSLKey"}},
        {"json_data": {"Members": []},
         "idrac_service_uri": '/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DelliDRACCardService',
         "actions": idrac_service_actions}
    ])
    def test_get_actions_map(
            self, params, idrac_redfish_mock_for_certs, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        actions = self.module.get_actions_map(
            idrac_redfish_mock_for_certs,
            params.get('idrac_service_uri'))
        assert actions == params['actions']

    @pytest.mark.parametrize("params", [{"actions": {}, "operation": "generate_csr",
                                         "cert_type": 'Server', "res_id": "iDRAC.1",
                                         "dynurl": "/redfish/v1/CertificateService/Actions/CertificateService.GenerateCSR"},
                                        {"actions": {}, "operation": "import",
                                         "cert_type": 'Server', "res_id": "iDRAC.1",
                                         "dynurl": "/redfish/v1/Managers/iDRAC.1/Oem/Dell/DelliDRACCardService/Actions/"
                                         "DelliDRACCardService.ImportSSLCertificate"}
                                        ])
    def test_get_cert_url(self, params):
        dynurl = self.module.get_cert_url(params.get('actions'), params.get('operation'), params.get('cert_type'),
                                          params.get('res_id'))
        assert dynurl == params['dynurl']

    @pytest.mark.parametrize("params", [
        {"cert_data": {"CertificateFile": 'Hello world!',
                       "@Message.ExtendedInfo": [{
                           "Message": "Successfully exported SSL Certificate.",
                           "MessageId": "IDRAC.2.5.LC067",
                           "Resolution": "No response action is required.",
                           "Severity": "Informational"}
                       ]},
         "result": {'@Message.ExtendedInfo': [
             {'Message': 'Successfully exported SSL Certificate.',
              'MessageId': 'IDRAC.2.5.LC067',
              'Resolution': 'No response action is required.',
              'Severity': 'Informational'}]},
         "mparams": {'command': 'export', 'certificate_type': "HTTPS",
                     'certificate_path': tempfile.gettempdir(), 'reset': False}
         },
        {"cert_data": {"CertificateFile": 'Hello world!',
                       "@Message.ExtendedInfo": [{
                           "Message": "Successfully exported SSL Certificate.",
                           "MessageId": "IDRAC.2.5.LC067",
                                        "Resolution": "No response action is required.",
                                        "Severity": "Informational"}
                       ]},
         "result": {'@Message.ExtendedInfo': [
             {'Message': 'Successfully exported SSL Certificate.',
              'MessageId': 'IDRAC.2.5.LC067',
                           'Resolution': 'No response action is required.',
                           'Severity': 'Informational'}]},
         "mparams": {'command': 'generate_csr', 'certificate_type': "HTTPS",
                     'certificate_path': tempfile.gettempdir(), 'reset': False}}])
    def test_format_output(self, params, idrac_default_args):
        idrac_default_args.update(params.get('mparams'))
        f_module = self.get_module_mock(params=idrac_default_args)
        result = self.module.format_output(f_module, params.get('cert_data'))
        if os.path.exists(result.get('certificate_path')):
            os.remove(result.get('certificate_path'))
        assert 'result' not in result

    @pytest.mark.parametrize("exc_type", [SSLValidationError, URLError, ValueError, TypeError,
                                          ConnectionError, HTTPError, ImportError, RuntimeError])
    def test_main_exceptions(
            self, exc_type, idrac_connection_certificates_mock, idrac_default_args, mocker):
        idrac_default_args.update(
            {"command": "export", "certificate_path": "mypath"})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + "get_res_id",
                         side_effect=exc_type('test'))
        else:
            mocker.patch(MODULE_PATH + "get_res_id",
                         side_effect=exc_type('https://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
        if not exc_type == URLError:
            result = self._run_module(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result
