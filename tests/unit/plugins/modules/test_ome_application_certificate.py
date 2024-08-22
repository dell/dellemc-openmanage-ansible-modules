# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.6.0
# Copyright (C) 2019-2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json

import pytest
from urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.modules import ome_application_certificate
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
MODULE_UTILS_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.'
EMAIL_ADDRESS = "support@dell.com"


@pytest.fixture
def ome_connection_mock_for_application_certificate(mocker, ome_response_mock):
    connection_class_mock = mocker.patch(
        MODULE_PATH + 'ome_application_certificate.RestOME')
    ome_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    ome_connection_mock_obj.invoke_request.return_value = ome_response_mock
    return ome_connection_mock_obj


class TestOmeAppCSR(FakeAnsibleModule):
    module = ome_application_certificate

    @pytest.mark.parametrize("exc_type",
                             [ValueError, SSLError, TypeError, ConnectionError, HTTPError, URLError])
    def test_ome_application_certificate_main_error_cases(self, exc_type, mocker, ome_default_args,
                                                          ome_connection_mock_for_application_certificate,
                                                          ome_response_mock):
        json_str = to_text(json.dumps({"info": "error_details"}))
        args = {"command": "generate_csr", "distinguished_name": "hostname.com",
                "department_name": "Remote Access Group", "business_name": "Dell Inc.",
                "locality": "Round Rock", "country_state": "Texas", "country": "US",
                "email": EMAIL_ADDRESS, "subject_alternative_names": "XX.XX.XX.XX"}
        ome_default_args.update(args)
        if exc_type == URLError:
            mocker.patch(MODULE_PATH + 'ome_application_certificate.get_resource_parameters',
                         side_effect=exc_type("TEST"))
            result = self._run_module(ome_default_args)
            assert result["unreachable"] is True
        elif exc_type not in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + 'ome_application_certificate.get_resource_parameters',
                         side_effect=exc_type("exception message"))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        else:
            mocker.patch(MODULE_PATH + 'ome_application_certificate.get_resource_parameters',
                         side_effect=exc_type('https://testhost.com', 400,
                                              'http error message',
                                              {"accept-type": "application/json"},
                                              StringIO(json_str)))
            result = self._run_module_with_fail_json(ome_default_args)
            assert result['failed'] is True
        assert 'csr_status' not in result
        assert 'msg' in result

    def test_get_resource_parameters_generate(self, mocker, ome_default_args,
                                              ome_connection_mock_for_application_certificate,
                                              ome_response_mock):
        args = {"command": "generate_csr", "distinguished_name": "hostname.com",
                "department_name": "Remote Access Group", "business_name": "Dell Inc.",
                "locality": "Round Rock", "country_state": "Texas", "country": "US",
                "email": EMAIL_ADDRESS, "subject_alternative_names": "XX.XX.XX.XX"}
        f_module = self.get_module_mock(params=args)
        result = self.module.get_resource_parameters(f_module)
        assert result[0] == "POST"
        assert result[1] == "ApplicationService/Actions/ApplicationService.GenerateCSR"
        assert result[2] == {'DistinguishedName': 'hostname.com', 'Locality': 'Round Rock',
                             'DepartmentName': 'Remote Access Group', 'BusinessName': 'Dell Inc.',
                             'State': 'Texas', 'Country': 'US', 'Email': 'support@dell.com',
                             'San': 'XX.XX.XX.XX'}

    def test_upload_csr_fail01(self, mocker, ome_default_args, ome_connection_mock_for_application_certificate,
                               ome_response_mock):
        args = {"command": "upload", "upload_file": "/path/certificate.cer"}
        f_module = self.get_module_mock(params=args)
        with pytest.raises(Exception) as exc:
            self.module.get_resource_parameters(f_module)
        assert exc.value.args[0] == "No such file or directory."

    def test_upload_csr_success(self, mocker, ome_default_args, ome_connection_mock_for_application_certificate,
                                ome_response_mock):
        payload = "--BEGIN-REQUEST--"
        mocker.patch(MODULE_PATH + 'ome_application_certificate.get_resource_parameters',
                     return_value=("POST", "ApplicationService/Actions/ApplicationService.UploadCertificate", payload))
        ome_default_args.update({"command": "upload", "upload_file": "/path/certificate.cer"})
        ome_response_mock.success = True
        result = self.execute_module(ome_default_args)
        assert result['msg'] == "Successfully uploaded application certificate."

    def test_upload_cert_chain_fail(self, mocker, ome_default_args, ome_connection_mock_for_application_certificate,
                                    ome_response_mock):
        args = {"command": "upload_cert_chain", "upload_file": "/path/nonexistent_certificate_chain.p7b"}
        f_module = self.get_module_mock(params=args)
        with pytest.raises(Exception) as exc:
            self.module.get_resource_parameters(f_module)
        assert exc.value.args[0] == "No such file or directory."

    def test_upload_cert_chain_success(self, mocker, ome_default_args, ome_connection_mock_for_application_certificate,
                                       ome_response_mock):
        payload = "--BEGIN-CERT-CHAIN--"
        mocker.patch(MODULE_PATH + 'ome_application_certificate.get_resource_parameters',
                     return_value=("POST", "ApplicationService/Actions/ApplicationService.UploadCertChain", payload))
        mocker.patch(MODULE_PATH + 'ome_application_certificate.get_ome_version', return_value="4.1.0")
        ome_default_args.update({"command": "upload_cert_chain", "upload_file": "/path/certificate_chain.cer"})
        result = self.execute_module(ome_default_args)
        assert result['msg'] == "Successfully uploaded application certificate."

    def test_generate_csr(self, mocker, ome_default_args, ome_connection_mock_for_application_certificate,
                          ome_response_mock):
        csr_data = "-----BEGIN CERTIFICATE REQUEST-----MIIFMDCCAxgCAQAwgbAxCzAJBgNVBAYTAlVTMREwDwYDVQQIDAhWaXJnaW5pYTES-----END CERTIFICATE REQUEST-----"
        csr_json = {"CertificateData": csr_data}
        payload = {"DistinguishedName": "hostname.com", "DepartmentName": "Remote Access Group",
                   "BusinessName": "Dell Inc.", "Locality": "Round Rock", "State": "Texas",
                   "Country": "US", "Email": EMAIL_ADDRESS, "subject_alternative_names": "XX.XX.XX.XX"}
        mocker.patch(MODULE_PATH + 'ome_application_certificate.get_resource_parameters',
                     return_value=("POST", "ApplicationService/Actions/ApplicationService.GenerateCSR", payload))
        ome_default_args.update({"command": "generate_csr", "distinguished_name": "hostname.com",
                                 "department_name": "Remote Access Group", "business_name": "Dell Inc.",
                                 "locality": "Round Rock", "country_state": "Texas", "country": "US",
                                 "email": EMAIL_ADDRESS, "subject_alternative_names": "XX.XX.XX.XX, YY.YY.YY.YY"})
        ome_response_mock.success = True
        ome_response_mock.json_data = csr_json
        result = self.execute_module(ome_default_args)
        assert result['msg'] == "Successfully generated certificate signing request."
        data = '''-----BEGIN CERTIFICATE REQUEST-----\nMIIFMDCCAxgCAQAwgbAxCzAJBgNVBAYTAlVTMREwDwYDVQQIDAhWaXJnaW5pYTES\n-----END CERTIFICATE REQUEST-----'''
        assert result['csr_status']['CertificateData'] == data
