#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.6.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_secure_boot
short_description: Configures the iDRAC secure boot
version_added: "9.6.0"
description:
  - This module allows you to configure the secure boot.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_x_auth_options
options:
  import_certificates:
    type: bool
    description:
        - Import all the specified key certificates.
        - I(import_certificates) is C(true) either of I(platform_key) or i(key_exchange_key) or I(database) or I(disallow_database) is required.
  platform_key:
    type: path
    description:
      - Platform Key policy certificate path for UEFI Secure Boot.
      - Absolute path of the certificate file I(import_certificates) is C(true).
  key_exchange_key:
    type: list
    elements: path
    description:
      - Key exchange key policy certificate paths for UEFI Secure Boot.
      - Absolute path of the certificate file if I(import_certificates) is C(import).
  database:
    type: list
    elements: path
    description:
      - Databases certificate paths for UEFI Secure Boot.
      - Absolute path of the certificate file if I(import_certificates) is C(import).
  disallow_database:
    type: list
    elements: path
    description:
      - Disallow database certificate paths for UEFI Secure Boot.
      - Absolute path of the certificate file if I(import_certificates) is C(import).
  restart:
    type: bool
    default: false
    description:
      -  Restart the server to apply the secure boot settings.
      - I(restart) will be ignored only when I(export_certificates) is C(true).
  restart_type:
    type: str
    default: GracefulRestart
    choices: [GracefulRestart, ForceRestart]
    description:
      - Reset type
      - C(ForceRestart) Forcefully reboot the host system.
      - C(GracefulRestart) Gracefully reboot the host system.
      - C(GracefulRestart) Gracefully reboot the host system.
      - I(restart_type) is applicable when i(restart) is C(true).
  job_wait:
    type: bool
    default: true
    description:
      - Provides the option to wait for job completion.
  job_wait_timeout:
    type: int
    default: 1200
    description:
      - The maximum wait time of I(job_wait) in seconds. The job is tracked only for this duration.
      - This option is applicable when I(job_wait) is C(true).
requirements:
    - "python >= 3.9.6"
author:
    - "Abhishek Sinha(@ABHISHEK-SINHA10)"
notes:
    - This module reports changes found when ran in check_mode for I(import_certificates).
    - This module does not support idempotency when I(import_certificates) is provided.
    - This module supports both IPv4 and IPv6 address.
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Import a SecureBoot certificate.
  dellemc.openmanage.idrac_secureboot:
    import: true
    platform_key: /user/name/certificates/pk.pem
    key_exchange_key:
      - /user/name/certificates/kek1.pem
      - /user/name/certificates/kek2.pem
    database:
      - /user/name/certificates/db1.pem
      - /user/name/certificates/db2.pem
    disallow_database:
      - /user/name/certificates/dbx1.pem
      - /user/name/certificates/dbx2.pem
"""

RETURN = r'''
---
msg:
  description: Status of the secure boot operation.
  returned: always
  type: str
  sample: "The Secure Boot Certificate Import operation has completed successfully."
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
      "code": "Base.1.0.GeneralError",
      "message": "A general error has occurred. See ExtendedInfo for more information.",
      "@Message.ExtendedInfo": [
        {
          "MessageId": "GEN1234",
          "RelatedProperties": [],
          "Message": "Unable to process the request because an error occurred.",
          "MessageArgs": [],
          "Severity": "Critical",
          "Resolution": "Retry the operation. If the issue persists, contact your system administrator."
        }
      ]
    }
  }
'''

import json
import os
from urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, IdracAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    get_dynamic_uri, remove_key, validate_and_get_first_resource_id_uri,
    trigger_restart_operation, wait_for_LCStatus, get_lc_log_or_current_log_time)

SYSTEMS_URI = "/redfish/v1/Systems"
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The value for the 'job_wait_timeout' parameter cannot be negative or zero."
SUCCESS_MSG = "The Secure Boot Certificate Import operation has completed successfully."
NO_OPERATION_SKIP = "Task is skipped as import is 'false'."
PROVIDE_ABSOLUTE_PATH = "Please provide absolute path of the certificate file {path}"
NO_READ_PERMISSION_PATH = "Unable to read the certificate file {path}."
NO_VALID_PATHS = "No valid absolute path found for certificate(s)."
CHANGES_FOUND = 'Changes found to be applied.'
FAILED_IMPORT = "Failed to import certificate file {path}."
NO_IMPORT_SUCCESS = "The Secure Boot Certificate Import operation was not successful."
odata = '@odata.id'

class IDRACSecureBoot:

    def __init__(self, idrac, module):
        self.module = module
        self.idrac = idrac
        self.uri_mapping = {'database': 'db',
                            'key_exchange_key': 'KEK',
                            'disallow_database': 'dbx',
                            'platform_key': 'PK'}

    def validate_job_wait(self):
        """
        Validates job_wait and job_wait_timeout parameters.
        """
        if self.module.params.get('job_wait') and self.module.params.get('job_wait_timeout') == 0:
            self.module.exit_json(msg=TIMEOUT_NEGATIVE_OR_ZERO_MSG)

    def get_dynamic_secure_boot_database_uri(self):
        uri, error_msg = validate_and_get_first_resource_id_uri(
            self.module, self.idrac, SYSTEMS_URI)
        if error_msg:
            self.module.exit_json(msg=error_msg, failed=True)
        secure_boot_uri = get_dynamic_uri(
            self.idrac, uri, 'SecureBoot')[odata]
        secure_boot_database_uri = get_dynamic_uri(
            self.idrac, secure_boot_uri, 'SecureBootDatabases')[odata]
        return secure_boot_database_uri

    def mapping_secure_boot_database_uri(self):
        mapped_value = {}
        secure_boot_database_uri = self.get_dynamic_secure_boot_database_uri()
        secure_boot_database_members = get_dynamic_uri(self.idrac, secure_boot_database_uri, 'Members')
        for each_member in secure_boot_database_members:
            for label, last_uri_leaf in self.uri_mapping.items():
                uri = each_member.get(odata)
                if last_uri_leaf == uri.split('/')[-1]:
                    mapped_value.update({label: uri})
                    break
        return mapped_value


class IDRACImportSecureBoot(IDRACSecureBoot):

    def __init__(self, idrac, module):
        super().__init__(idrac, module)
        plt_key = self.module.params.get('platform_key')
        self.platform_key = [plt_key] if plt_key else [] 
        self.key_exchange_key = self.module.params.get('key_exchange_key') or []
        self.database = self.module.params.get('database') or []
        self.disallow_database = self.module.params.get('disallow_database') or []

    def validate_certificate_paths(self, paths):
        """
        Validate certificate paths
        """
        invalid_paths = set()
        for path in paths:
            if path and not os.path.isabs(path):
                self.module.warn(PROVIDE_ABSOLUTE_PATH.format(path=path))
                invalid_paths.add(path)
            if path and not os.path.isfile(path):
                self.module.warn(NO_READ_PERMISSION_PATH.format(path=path))
                invalid_paths.add(path)
        return list(set(paths) - invalid_paths)

    def filter_invalid_paths(self):
        """
        Filter invalid paths
        """
        self.platform_key = self.validate_certificate_paths(self.platform_key)
        self.key_exchange_key = self.validate_certificate_paths(self.key_exchange_key)
        self.database = self.validate_certificate_paths(self.database)
        self.disallow_database = self.validate_certificate_paths(self.disallow_database)

    def read_certificate_file(self, path):
        with open(path, 'r') as f:
            return f.read()

    def create_dictionary_payload(self, paths):
        result = []
        for each_path in paths:
            tmp = {'cert_data': self.read_certificate_file(each_path),
                   'path': each_path}
            result.append(tmp)
        return result

    def construct_payload(self):
        """
        Construct payload
        """
        payload = {}
        if self.platform_key:
            payload['platform_key'] = self.create_dictionary_payload(self.platform_key)
        if self.key_exchange_key:
            payload['key_exchange_key'] = self.create_dictionary_payload(self.key_exchange_key)
        if self.database:
            payload['database'] = self.create_dictionary_payload(self.database)
        if self.disallow_database:
            payload['disallow_database'] = self.create_dictionary_payload(self.disallow_database)
        return payload

    def perform_operation(self):
        """
        Perform operation
        """
        SUCCESS_CODE = ["SWC9010", "UEFI0286"]
        current_time = get_lc_log_or_current_log_time(self.idrac)
        self.filter_invalid_paths()
        self.validate_job_wait()
        payload_values = self.construct_payload()
        if not payload_values:
            self.module.exit_json(msg=NO_VALID_PATHS, skipped=True)
        if self.module.check_mode:
            self.module.exit_json(msg=CHANGES_FOUND, changed=True)
        uri = self.mapping_secure_boot_database_uri()
        for parameter, payload_list in payload_values.items():
            for each_payload in payload_list:
                payload = {"CertificateString": each_payload['cert_data'],
                           "CertificateType": "PEM"}
                certificates_uri = get_dynamic_uri(self.idrac, uri[parameter], 'Certificates')[odata]
                try:
                    self.idrac.invoke_request(method='POST', uri=certificates_uri, data=payload)
                except HTTPError:
                    self.module.warn(FAILED_IMPORT.format(parameter=parameter,
                                                          path=each_payload['path']))
        lc_log, msg = get_lc_log_or_current_log_time(self.idrac, current_time, SUCCESS_CODE)
        if not lc_log:
            self.module.exit_json(msg=NO_IMPORT_SUCCESS, skipped=True)
        if self.module.params.get('restart'):
            resp, err_msg = trigger_restart_operation(self.idrac, self.module.params.get('restart_type'))
            if resp.success:
                if self.module.params.get('job_wait'):
                    lc_completed, error_msg = wait_for_LCStatus(self.idrac, self.module.params.get('job_wait_timeout'))
                    if lc_completed:
                        lc_log, msg = get_lc_log_or_current_log_time(self.idrac, current_time, SUCCESS_CODE)
                        self.module.exit_json(msg=SUCCESS_MSG, changed=True)
                    else:
                        self.module.exit_json(msg=error_msg, failed=True)
        self.module.exit_json(msg=msg)


def main():
    try:
        specs = {
            "import_certificates": {"type": 'bool'},
            "platform_key": {"type": 'path'},
            "key_exchange_key": {"type": 'list', "elements": 'path'},
            "database": {"type": 'list', "elements": 'path'},
            "disallow_database": {"type": 'list', "elements": 'path'},
            "restart": {"type": 'bool', "default": False},
            "restart_type": {"type": 'str', "default": "GracefulRestart",
                             "choices": ['ForceRestart', 'GracefulRestart']},
            "job_wait": {"type": 'bool', "default": True},
            "job_wait_timeout": {"type": 'int', "default": 1200},
        }

        module = IdracAnsibleModule(argument_spec=specs,
                                    supports_check_mode=True)
        with iDRACRedfishAPI(module.params, req_session=True) as idrac:
            obj = None
            if module.params.get('import_certificates'):
                obj = IDRACImportSecureBoot(idrac, module)
            else:
                module.exit_json(msg=NO_OPERATION_SKIP, skipped=True)
            obj.perform_operation()
    except HTTPError as err:
        filter_err = remove_key(json.load(err), regex_pattern='(.*?)@odata')
        module.exit_json(msg=str(err), error_info=filter_err, failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
