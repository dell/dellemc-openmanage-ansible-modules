#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.7.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_secure_boot
short_description: Configure attributes, import or export secure boot certificate and Reset keys
version_added: "9.6.0"
description:
  - This module allows to import/export the secure boot certificates.
  - This module allows to enable/disable secure boot, boot mode.
  - This modules also allows to configure Policies PK, KEK and configure DB, DBX certificates.
  - This module allows to reset the UEFI Secure Boot keys..
extends_documentation_fragment:
  - dellemc.openmanage.idrac_x_auth_options
options:
  boot_mode:
    type: str
    choices: [Uefi, Bios]
    description:
      - Boot Mode of the idrac.
      - I(Uefi) Enables the secure boot in uefi mode.
      - I(Bios) Enables the secure boot in bios mode.
  secure_boot:
    type: str
    choices: [Enabled, Disabled]
    description:
      - UEFI Secure Boot.
      - The I(secure_boot_mode) can be C(Enabled) only if I(boot_mode) is C(Uefi) and I(force_int_10) is C(Disabled).
      - I(Enabled) enables the Secureboot mode.
      - I(Disabled) disables the Secureboot mode.
  secure_boot_mode:
    type: str
    choices: [UserMode, DeployedMode, AuditMode]
    description:
      - The UEFI Secure Boot Mode configures how the Secure Boot Policy are used.
      - I(UserMode) set the secure boot mode into an user mode where PK must be installed, and BIOS performs signature verification on programmatic attempts
        to update policy objects.
      - I(DeployedMode) set the secure boot mode into an deployed mode where PK is present, and BIOS performs signature verification on programmatic attempts
        to update policy objects
      - I(AuditMode) set the secure boot mode into an audit mode where PK is not present. The BIOS does not authenticate programmatic updates to the policy
        objects, and transitions between modes. The BIOS performs a signature verification on pre-boot images and logs the results in the image Execution
        Information Table, but executes the images whether they pass or fail verification.
  secure_boot_policy:
    type: str
    choices: [Standard, Custom]
    description:
      - Following are the secure boot policy.
      - C (Standard) indicates that the system has default certificates and image digests, or hash loaded from the factory.
      - C(Custom) inherits the standard certificates and image digests that are loaded in the system by default, which you can modify.
      - Secure Boot Policy configured as Custom allows you to perform operations such as View, Export, Import, Delete, Delete All, Reset, and Reset.
  force_int_10:
    type: str
    choices: [Enabled, Disabled]
    description:
      - Determines whether the system BIOS will load the legacy video (INT 10h) option ROM from the video controller.
      - This field is supported only in UEFI boot mode. This field cannot be set to Enabled if UEFI SecureBoot is enabled.
      - C(Enabled) if the operating system does not support UEFI video output standards.
      - C(Disabled) if the operating system support UEFI video output standards.
  export_certificates:
    type: bool
    description:
      - Export all the available certificates in the specified directory for the given keys.
      - I(export_cetificates) is mutually exclusive with I(import).
      - I(export_cetificates) is C(true) either of I(platform_key) or i(key_exchange_key) or I(database) - or I(disallow_database) is required.
  import_certificates:
    type: bool
    description:
      - Import all the specified key certificates.
      - When I(import_certificates) is C(true), then either I(platform_key), I(KEK), I(database), or I(disallow_database) is required.
  platform_key:
    type: path
    description:
      - The absolute path of the Platform key certificate file for UEFI secure boot.
      - Directory path with write permissions if I(export_certificates) is C(true).
  KEK:
    type: list
    elements: path
    description:
      - A list of absolute paths of the Key Exchange Key (KEK) certificate file for UEFI secure boot.
      - Directory path with write permissions if I(export_certificates) is C(true).
  database:
    type: list
    elements: path
    description:
      - A list of absolute paths of the Database certificate file for UEFI secure boot.
      - Directory path with write permissions if I(export_certificates) is C(true).
  disallow_database:
    type: list
    elements: path
    description:
      - A list of absolute paths of the Disallow Database certificate file for UEFI secure boot.
      - Directory path with write permissions if I(export_certificates) is C(true).
  reset_keys:
    type: str
    choices: [ResetAllKeysToDefault, DeleteAllKeys, DeletePK, ResetPK, ResetKEK, ResetDB, ResetDBX]
    description:
      - Resets the UEFI Secure Boot keys.
      - C(ResetAllKeysToDefault) - Reset the content of all UEFI Secure Boot key databases (PK, KEK, DB, DBX) to their default values.
      - C(DeletePK) - Delete the content of the PK UEFI Secure Boot database. This puts the system in Setup Mode.
      - C(DeleteAllKeys) - Delete the content of all UEFI Secure Boot key databases (PK, KEK, DB, DBX). This puts the system in Setup Mode
      - C(ResetPK) - Reset the content of PK UEFI Secure Boot database to their default values.
      - C(ResetKEK)- Reset the content of KEK UEFI Secure Boot database to their default values.
      - C(ResetDB)- Reset the content of DB UEFI Secure Boot database to their default values.
      - C(ResetDBX)- Reset the content of DBX UEFI Secure Boot database to their default values.
  restart:
    type: bool
    default: false
    description:
      - Secure boot certificate import operation requires a server restart. This parameter provides an option to restart the server.
      - C(true) restarts the server.
      - C(false) does not restart the server.
      - I(restart) is applicable when I(import_certificates) is C(true).
      - I(restart) will be ignored only when I(export_certificates) is C(true).
  restart_type:
    type: str
    default: GracefulRestart
    choices: [GracefulRestart, ForceRestart]
    description:
      - Restart type of the server.
      - C(ForceRestart) forcefully restarts the server.
      - C(GracefulRestart) gracefully restarts the server.
      - I(restart_type) is applicable when I(restart) is C(true).
  job_wait:
    type: bool
    default: true
    description:
      - Whether to wait till completion of the secure boot certificate operation. This is applicable when I(restart) is C(true).
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
    - "Lovepreet Singh (@singh-lovepreet1)"
attributes:
    check_mode:
        description: Runs task to validate without performing action on the target machine.
        support: full
    diff_mode:
        description: Runs the task to report the changes made or to be made.
        support: none
notes:
    - This module will always report changes found to be applied when run in C(check mode).
    - This module does not support idempotency when I(reset_type) or I(export_certificates)
      or I(import_certificates) is provided.
    - The order of operations set secure boot settings (boot_mode, secure_boot, secure_boot_mode,
      secure_boot_policy, force_int_10),  export,  certificate reset,  import, idrac reset.
    - I(export_certificate) will export all the certificates of the key defined in the playbook.
    - This module supports IPv4 and IPv6 addresses.
"""

EXAMPLES = """
---
- name: Enable Secureboot.
  dellemc.openmanage.idrac_secure_boot:
    idrac_ip: "192.168.1.2"
    idrac_user: "user"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    secure_boot: "Enabled"

- name: Set SecureBootMode and SecureBootPolicy and reset iDRAC.
  dellemc.openmanage.idrac_secure_boot:
    idrac_ip: "192.168.1.2"
    idrac_user: "user"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    secure_boot: "Enabled"
    secure_boot_mode: "UserMode"
    secure_boot_policy: "Custom"
    restart: true
    restart_type: "GracefulRestart"

- name: Reset Secure Boot certificates.
  dellemc.openmanage.idrac_secure_boot:
    idrac_ip: "192.168.1.2"
    idrac_user: "user"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    reset_keys: "ResetAllKeysToDefault"

- name: Export multiple SecureBoot certificate.
  dellemc.openmanage.idrac_secure_boot:
    idrac_ip: "192.168.1.2"
    idrac_user: "user"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    export_certificates: true
    platform_key: /user/name/export_cert/pk
    KEK:
      - /user/name/export_cert/kek
    database:
      - /user/name/export_cert/db
    disallow_database:
      - /user/name/export_cert/dbx

- name: Import multiple SecureBoot certificate without applying to iDRAC.
  dellemc.openmanage.idrac_secure_boot:
    idrac_ip: "192.168.1.2"
    idrac_user: "user"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    import_certificates: true
    platform_key: /user/name/certificates/pk.pem
    KEK:
      - /user/name/certificates/kek1.pem
      - /user/name/certificates/kek2.pem
    database:
      - /user/name/certificates/db1.pem
      - /user/name/certificates/db2.pem
    disallow_database:
      - /user/name/certificates/dbx1.pem
      - /user/name/certificates/dbx2.pem

- name: Import a SecureBoot certificate and restart the server to apply it.
  dellemc.openmanage.idrac_secure_boot:
    idrac_ip: "192.168.1.2"
    idrac_user: "user"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    import_certificates: true
    platform_key: /user/name/certificates/pk.pem
    restart: true
    job_wait_timeout: 600
"""

RETURN = r'''
---
msg:
  description: Status of the secure boot operation.
  returned: always
  type: str
  sample: "Successfully imported the SecureBoot certificate."
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
    trigger_restart_operation, wait_for_lc_status, get_lc_log_or_current_log_time,
    cert_file_format_string)

SYSTEMS_URI = "/redfish/v1/Systems"
TIME_FORMAT = "%Y%m%d_%H%M%S"
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The value for the 'job_wait_timeout' parameter cannot be negative or zero."
SUCCESS_MSG = "Successfully imported the SecureBoot certificate."
NO_OPERATION_SKIP = "Task is skipped as import_certificates is 'false'."
PROVIDE_ABSOLUTE_PATH = "Please provide absolute path of the certificate file {path}."
NO_READ_PERMISSION_PATH = "Unable to read the certificate file {path}."
NO_FILE_FOUND = "Unable to find the certificate file {path}."
NO_VALID_PATHS = "No valid absolute path found for certificate(s)."
CHANGES_FOUND = 'Changes found to be applied.'
SCHEDULED_AND_RESTARTED = "Successfully scheduled the boot certificate import operation and restarted the server."
FAILED_IMPORT = "Failed to import certificate file {path} for {parameter}."
NO_IMPORT_SUCCESS = "The Secure Boot Certificate Import operation was not successful."
NO_DIRECTORY_FOUND = "Unable to find the directory {path}."
NO_WRITE_PERMISSION_PATH = 'Unable to write to the directory {path}.'
TOO_MANY_DIRECTORIES = 'More than one directory found for parameter {key}.'
CERT_IS_EMPTY = 'Certificate string is empty in {file_name} for {parameter}.'
SUCCESS_EXPORT_MSG = 'Successfully exported the SecureBoot certificate.'
odata = '@odata.id'


class IDRACSecureBoot:

    def __init__(self, idrac, module):
        self.module = module
        self.idrac = idrac
        plt_key = self.module.params.get('platform_key')
        self.platform_key = [plt_key] if plt_key else []
        self.KEK = self.module.params.get(
            'KEK') or []
        self.database = self.module.params.get('database') or []
        self.disallow_database = self.module.params.get(
            'disallow_database') or []
        self.uri_mapping = {'database': 'db',
                            'KEK': 'KEK',
                            'disallow_database': 'dbx',
                            'platform_key': 'PK'}

    def validate_job_wait(self):
        """
        Validates job_wait and job_wait_timeout parameters.
        """
        if self.module.params.get('job_wait') and self.module.params.get('job_wait_timeout') <= 0:
            self.module.exit_json(
                msg=TIMEOUT_NEGATIVE_OR_ZERO_MSG, failed=True)

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
        secure_boot_database_members = get_dynamic_uri(
            self.idrac, secure_boot_database_uri, 'Members')
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

    def validate_certificate_paths(self, paths):
        """
        Validate certificate paths
        """
        invalid_paths = set()
        for path in paths:
            if path and not os.path.isabs(path):
                self.module.warn(PROVIDE_ABSOLUTE_PATH.format(path=path))
                invalid_paths.add(path)
            if path and not os.access(path=path, mode=os.R_OK):
                self.module.warn(NO_READ_PERMISSION_PATH.format(path=path))
                invalid_paths.add(path)
            if path and not os.path.isfile(path):
                self.module.warn(NO_FILE_FOUND.format(path=path))
                invalid_paths.add(path)
        return list(set(paths) - invalid_paths)

    def filter_invalid_paths(self):
        """
        Filter invalid paths
        """
        self.platform_key = self.validate_certificate_paths(self.platform_key)
        self.KEK = self.validate_certificate_paths(
            self.KEK)
        self.database = self.validate_certificate_paths(self.database)
        self.disallow_database = self.validate_certificate_paths(
            self.disallow_database)

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
            payload['platform_key'] = self.create_dictionary_payload(
                self.platform_key)
        if self.KEK:
            payload['KEK'] = self.create_dictionary_payload(
                self.KEK)
        if self.database:
            payload['database'] = self.create_dictionary_payload(self.database)
        if self.disallow_database:
            payload['disallow_database'] = self.create_dictionary_payload(
                self.disallow_database)
        return payload

    def looping_over_parameters(self, payload_values, uri):
        for parameter, payload_list in payload_values.items():
            for each_payload in payload_list:
                payload = {"CertificateString": each_payload['cert_data'],
                           "CertificateType": "PEM"}
                cert_uri = get_dynamic_uri(
                    self.idrac, uri[parameter], 'Certificates')[odata]

                try:
                    self.idrac.invoke_request(
                        method='POST', uri=cert_uri, data=payload)
                except HTTPError:
                    self.module.warn(FAILED_IMPORT.format(
                        parameter=parameter, path=each_payload['path']))

    def perform_restart(self, success_codes, current_time):
        resp, err_msg = trigger_restart_operation(
            self.idrac, self.module.params.get('restart_type'))

        if resp.success:
            if self.module.params.get('job_wait'):
                lc_completed, error_msg = wait_for_lc_status(
                    self.idrac, self.module.params.get('job_wait_timeout'))

                self.operation_after_lc_status_check(success_codes, current_time, lc_completed, error_msg)
            else:
                self.module.exit_json(msg=SCHEDULED_AND_RESTARTED)

    def operation_after_lc_status_check(self, success_codes, current_time, lc_completed, error_msg):
        if lc_completed:
            lc_log, msg = get_lc_log_or_current_log_time(self.idrac, current_time, success_codes)
            if lc_log:
                self.module.exit_json(msg=SUCCESS_MSG, changed=True)
            else:
                self.module.exit_json(msg=NO_IMPORT_SUCCESS,
                                      skipped=True)
        else:
            self.module.exit_json(msg=error_msg, failed=True)

    def perform_operation(self):
        """
        Perform operation
        """
        success_codes = ["UEFI0286"]
        scheduled_code = ["SWC9010"]
        self.filter_invalid_paths()
        self.validate_job_wait()
        payload_values = self.construct_payload()
        if not payload_values:
            self.module.exit_json(msg=NO_VALID_PATHS, skipped=True)

        if self.module.check_mode:
            self.module.exit_json(msg=CHANGES_FOUND, changed=True)

        uri = self.mapping_secure_boot_database_uri()
        current_time = get_lc_log_or_current_log_time(self.idrac)

        self.looping_over_parameters(payload_values, uri)

        lc_log, scheduled_msg = get_lc_log_or_current_log_time(
            self.idrac, current_time, scheduled_code)

        if not lc_log:
            self.module.exit_json(msg=NO_IMPORT_SUCCESS, skipped=True)

        if self.module.params.get('restart'):
            self.perform_restart(success_codes, current_time)
        self.module.exit_json(msg=scheduled_msg)


class IDRACExportSecureBoot(IDRACSecureBoot):

    def __init__(self, idrac, module):
        super().__init__(idrac, module)

    def verify_path_is_directory_and_has_write_permission(self, path):
        flag = True
        is_dir_path = os.path.isdir(path)
        if path and not is_dir_path:
            self.module.warn(NO_DIRECTORY_FOUND.format(path=path))
            flag = False
        if path and is_dir_path and not os.access(path=path, mode=os.W_OK):
            self.module.warn(NO_WRITE_PERMISSION_PATH.format(path=path))
            flag = False
        return path if flag is True else ''

    def validate_key_directory(self, parameter, directories):
        resp = ''
        length_directories = len(directories)
        if length_directories > 1:
            self.module.warn(TOO_MANY_DIRECTORIES.format(key=parameter))
        if length_directories == 1:
            resp = self.verify_path_is_directory_and_has_write_permission(directories[0])
        return resp

    def filter_invalid_directory(self):
        self.platform_key = self.validate_key_directory('platform_key', self.platform_key)
        self.KEK = self.validate_key_directory('KEK', self.KEK)
        self.database = self.validate_key_directory('database', self.database)
        self.disallow_database = self.validate_key_directory('disallow_database', self.disallow_database)

    def fetch_certificate_file_and_write(self, uri, path, parameter):
        certificates_uri = get_dynamic_uri(self.idrac, uri, 'Certificates')[odata]
        members = get_dynamic_uri(self.idrac, certificates_uri, 'Members')
        for each_member in members:
            tmp_uri = each_member.get(odata)
            file_name = tmp_uri.split('/')[-1]
            resp = get_dynamic_uri(self.idrac, tmp_uri)
            cert_type = resp.get('CertificateType').lower()
            cert_string = resp.get('CertificateString')
            hostname = self.module.params.get('idrac_ip')
            updated_file_name = cert_file_format_string(hostname, postfix=f"_{file_name}")
            file_path = os.path.join(path, f"{updated_file_name}.{cert_type}")
            if cert_string:
                with open(file_path, 'w') as f:
                    f.write(cert_string)
            else:
                self.module.warn(CERT_IS_EMPTY.format(file_name=file_name,
                                                      parameter=parameter))

    def perform_operation(self):
        """
        Perform operation
        """
        self.validate_job_wait()
        self.filter_invalid_directory()
        if self.module.check_mode:
            self.module.exit_json(msg=CHANGES_FOUND, changed=True)
        uri = self.mapping_secure_boot_database_uri()
        data_map = {
            'platform_key': self.platform_key,
            'KEK': self.KEK,
            'database': self.database,
            'disallow_database': self.disallow_database
        }
        for parameter, path in data_map.items():
            if path:
                self.fetch_certificate_file_and_write(uri[parameter], path,
                                                      parameter)
        self.module.exit_json(msg=SUCCESS_EXPORT_MSG)


def main():
    try:
        specs = {
            "boot_mode": {"type": 'str', "choices": ['Uefi', 'Bios']},
            "secure_boot": {"type": 'str', "choices": ['Enabled', 'Disabled']},
            "secure_boot_mode": {"type": 'str', "choices": ['UserMode', 'DeployedMode', 'AuditMode']},
            "secure_boot_policy": {"type": 'str', "choices": ['Standard', 'Custom']},
            "force_int_10": {"type": 'str', "choices": ['Enabled', 'Disabled']},
            "export_certificates": {"type": 'bool'},
            "import_certificates": {"type": 'bool'},
            "platform_key": {"type": 'path'},
            "KEK": {"type": 'list', "elements": 'path'},
            "database": {"type": 'list', "elements": 'path'},
            "disallow_database": {"type": 'list', "elements": 'path'},
            "restart": {"type": 'bool', "default": False},
            "restart_type": {"type": 'str', "default": "GracefulRestart",
                             "choices": ['ForceRestart', 'GracefulRestart']},
            "reset_keys": {"type": 'str', "choices": ['ResetAllKeysToDefault', 'DeleteAllKeys', 'DeletePK',
                                                      'ResetPK', 'ResetKEK', 'ResetDB', 'ResetDBX']},
            "job_wait": {"type": 'bool', "default": True},
            "job_wait_timeout": {"type": 'int', "default": 1200},
        }
        mutually_exclusive_val = [("import_certificates", "export_certificates")]
        required_if_val = [("import_certificates", True, ("platform_key", "KEK",
                            "database", "disallow_database"), True),
                           ("export_certificates", True, ("platform_key", "KEK",
                            "database", "disallow_database"), True)]

        module = IdracAnsibleModule(argument_spec=specs,
                                    required_if=required_if_val,
                                    mutually_exclusive=mutually_exclusive_val,
                                    supports_check_mode=True)
        with iDRACRedfishAPI(module.params, req_session=True) as idrac:
            obj = None
            if module.params.get('import_certificates'):
                obj = IDRACImportSecureBoot(idrac, module)
            elif module.params.get('export_certificates'):
                obj = IDRACExportSecureBoot(idrac, module)
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
