# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.5.0
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
from ansible_collections.dellemc.openmanage.plugins.modules import idrac_certificates
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule
from mock import MagicMock

NOT_SUPPORTED_ACTION = "Certificate {op} not supported for the specified certificate type {certype}."
SUCCESS_MSG = "Successfully performed the '{command}' operation."
NO_CHANGES_MSG = "No changes found to be applied."
CHANGES_MSG = "Changes found to be applied."
NO_RESET = " Reset iDRAC to apply new certificate. Until iDRAC is reset, the old certificate will be active."
RESET_UNTRACK = " iDRAC reset is in progress. Until the iDRAC is reset, the changes would not apply."
RESET_SUCCESS = " iDRAC has been reset successfully."
RESET_FAIL = " Unable to reset the iDRAC. For changes to reflect, manually reset the iDRAC."
SYSTEM_ID = "System.Embedded.1"
MANAGER_ID = "iDRAC.Embedded.1"
SYSTEMS_URI = "/redfish/v1/Systems"
MANAGERS_URI = "/redfish/v1/Managers"
IDRAC_SERVICE = "/redfish/v1/Dell/Managers/{res_id}/DelliDRACCardService"
CSR_SSL = "/redfish/v1/CertificateService/Actions/CertificateService.GenerateCSR"
IMPORT_SSL = "/redfish/v1/Dell/Managers/{res_id}/DelliDRACCardService/Actions/DelliDRACCardService.ImportSSLCertificate"
EXPORT_SSL = "/redfish/v1/Dell/Managers/{res_id}/DelliDRACCardService/Actions/DelliDRACCardService.ExportSSLCertificate"
RESET_SSL = "/redfish/v1/Dell/Managers/{res_id}/DelliDRACCardService/Actions/DelliDRACCardService.SSLResetCfg"
IDRAC_RESET = "/redfish/v1/Managers/{res_id}/Actions/Manager.Reset"
idrac_service_actions = {
    "#DelliDRACCardService.DeleteCertificate": "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.DeleteCertificate",
    "#DelliDRACCardService.ExportCertificate": "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.ExportCertificate",
    "#DelliDRACCardService.ExportSSLCertificate": EXPORT_SSL,
    "#DelliDRACCardService.FactoryIdentityCertificateGenerateCSR":
        "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.FactoryIdentityCertificateGenerateCSR",
    "#DelliDRACCardService.FactoryIdentityExportCertificate":
        "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.FactoryIdentityExportCertificate",
    "#DelliDRACCardService.FactoryIdentityImportCertificate":
        "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.FactoryIdentityImportCertificate",
    "#DelliDRACCardService.GenerateSEKMCSR": "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.GenerateSEKMCSR",
    "#DelliDRACCardService.ImportCertificate": "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.ImportCertificate",
    "#DelliDRACCardService.ImportSSLCertificate": IMPORT_SSL,
    "#DelliDRACCardService.SSLResetCfg": "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.SSLResetCfg",
    "#DelliDRACCardService.iDRACReset": "/redfish/v1/Managers/{res_id}/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.iDRACReset"
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
    def idrac_connection_certificates_mock(self, mocker, idrac_certificates_mock):
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
        {"json_data": {}, 'message': "{0}{1}".format(SUCCESS_MSG.format(command="import"), NO_RESET), "success": True,
         "reset_idrac": (True, False, RESET_SUCCESS),
         'mparams': {'command': 'import', 'certificate_type': "HTTPS", 'certificate_path': '.pem', 'reset': False}},
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
        {"json_data": {}, 'message': NOT_SUPPORTED_ACTION.format(op="generate_csr", certype="CA"),
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
        {"json_data": {}, 'message': "{0}{1}".format(SUCCESS_MSG.format(command="import"), RESET_SUCCESS),
         "success": True,
         "reset_idrac": (True, False, RESET_SUCCESS),
         'mparams': {'command': 'import', 'certificate_type': "HTTPS", 'certificate_path': '.pem'}},
        {"json_data": {}, 'message': SUCCESS_MSG.format(command="export"), "success": True, "get_cert_url": "url",
         'mparams': {'command': 'export', 'certificate_type': "HTTPS", 'certificate_path': tempfile.gettempdir()}},
        {"json_data": {}, 'message': "{0}{1}".format(SUCCESS_MSG.format(command="reset"), RESET_SUCCESS),
         "success": True, "get_cert_url": "url", "reset_idrac": (True, False, RESET_SUCCESS),
         'mparams': {'command': 'reset', 'certificate_type': "HTTPS"}
         }
    ])
    def test_idrac_certificates(self, params, idrac_connection_certificates_mock, idrac_default_args, mocker):
        idrac_connection_certificates_mock.success = params.get("success", True)
        idrac_connection_certificates_mock.json_data = params.get('json_data')
        if params.get('mparams').get('certificate_path') and params.get('mparams').get('command') == 'import':
            sfx = params.get('mparams').get('certificate_path')
            temp = tempfile.NamedTemporaryFile(suffix=sfx, delete=False)
            temp.write(b'Hello')
            temp.close()
            params.get('mparams')['certificate_path'] = temp.name
        mocker.patch(MODULE_PATH + 'get_res_id', return_value=MANAGER_ID)
        mocker.patch(MODULE_PATH + 'get_idrac_service', return_value=IDRAC_SERVICE.format(res_id=MANAGER_ID))
        mocker.patch(MODULE_PATH + 'get_actions_map', return_value=idrac_service_actions)
        # mocker.patch(MODULE_PATH + 'get_cert_url', return_value=params.get('get_cert_url'))
        # mocker.patch(MODULE_PATH + 'write_to_file', return_value=params.get('write_to_file'))
        mocker.patch(MODULE_PATH + 'reset_idrac', return_value=params.get('reset_idrac'))
        idrac_default_args.update(params.get('mparams'))
        result = self._run_module(idrac_default_args, check_mode=params.get('check_mode', False))
        if params.get('mparams').get('command') == 'import' and params.get('mparams').get(
                'certificate_path') and os.path.exists(temp.name):
            os.remove(temp.name)
        assert result['msg'] == params['message']

    @pytest.mark.parametrize("params", [{"json_data": {"Members": [{"@odata.id": '/redfish/v1/Mangers/iDRAC.1'}]},
                                         "certype": 'Server', "res_id": "iDRAC.1"},
                                        {"json_data": {"Members": []},
                                         "certype": 'Server', "res_id": MANAGER_ID}
                                        ])
    def test_res_id(
            self, params, idrac_redfish_mock_for_certs, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        res_id = self.module.get_res_id(idrac_redfish_mock_for_certs, params.get('certype'))
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
        "idrac_srv": '/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DelliDRACCardService', "res_id": "iDRAC.1"},
        {"json_data": {"Members": []},
         "idrac_srv": '/redfish/v1/Dell/Managers/iDRAC.Embedded.1/DelliDRACCardService', "res_id": MANAGER_ID}
    ])
    def test_get_idrac_service(
            self, params, idrac_redfish_mock_for_certs, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        idrac_srv = self.module.get_idrac_service(idrac_redfish_mock_for_certs, params.get('res_id'))
        assert idrac_srv == params['idrac_srv']

    @pytest.mark.parametrize("params", [{"json_data": {
        "Actions": {
            "#DelliDRACCardService.ExportSSLCertificate": {
                "SSLCertType@Redfish.AllowableValues": ["CA", "CSC", "ClientTrustCertificate", "Server"],
                "target":
                    "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.ExportSSLCertificate"
            },
            "#DelliDRACCardService.ImportSSLCertificate": {
                "CertificateType@Redfish.AllowableValues": ["CA", "CSC", "ClientTrustCertificate", "Server"],
                "target":
                    "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.ImportSSLCertificate"
            },
            "#DelliDRACCardService.SSLResetCfg": {
                "target": "/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.SSLResetCfg"
            },
        },
    },
        "idrac_service_uri": '/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DelliDRACCardService',
        "actions": {
            '#DelliDRACCardService.ExportSSLCertificate':
                '/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.ExportSSLCertificate',
            '#DelliDRACCardService.ImportSSLCertificate':
                '/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.ImportSSLCertificate',
            '#DelliDRACCardService.SSLResetCfg':
                '/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/DelliDRACCardService/Actions/DelliDRACCardService.SSLResetCfg'}},
        {"json_data": {"Members": []},
         "idrac_service_uri": '/redfish/v1/Dell/Managers/iDRAC.Embedded.1/DelliDRACCardService',
         "actions": idrac_service_actions}
    ])
    def test_get_actions_map(
            self, params, idrac_redfish_mock_for_certs, ome_response_mock):
        ome_response_mock.success = params.get("success", True)
        ome_response_mock.json_data = params["json_data"]
        actions = self.module.get_actions_map(idrac_redfish_mock_for_certs, params.get('idrac_service_uri'))
        assert actions == params['actions']

    @pytest.mark.parametrize("params", [{"actions": {}, "op": "generate_csr",
                                         "certype": 'Server', "res_id": "iDRAC.1",
                                         "dynurl": "/redfish/v1/CertificateService/Actions/CertificateService.GenerateCSR"},
                                        {"actions": {}, "op": "import",
                                         "certype": 'Server', "res_id": "iDRAC.1",
                                         "dynurl": "/redfish/v1/Dell/Managers/iDRAC.1/DelliDRACCardService/Actions/DelliDRACCardService.ImportSSLCertificate"}
                                        ])
    def test_get_cert_url(self, params):
        dynurl = self.module.get_cert_url(params.get('actions'), params.get('op'), params.get('certype'),
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
    def test_main_exceptions(self, exc_type, idrac_connection_certificates_mock, idrac_default_args, mocker):
        idrac_default_args.update({"command": "export", "certificate_path": "mypath"})
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + "get_res_id",
                         side_effect=exc_type('test'))
        else:
            mocker.patch(MODULE_PATH + "get_res_id",
                         side_effect=exc_type('http://testhost.com', 400, 'http error message',
                                              {"accept-type": "application/json"}, StringIO(json_str)))
        if not exc_type == URLError:
            result = self._run_module_with_fail_json(idrac_default_args)
            assert result['failed'] is True
        else:
            result = self._run_module(idrac_default_args)
        assert 'msg' in result
