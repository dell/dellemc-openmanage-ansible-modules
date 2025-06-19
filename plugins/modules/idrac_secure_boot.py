#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.12.2
# Copyright (C) 2024-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: idrac_secure_boot
short_description: Configure attributes, import, or export secure boot certificate, and reset keys.
version_added: "9.6.0"
description:
  - This module allows you to perform the following operations.`
  - Import or Export Secure Boot certificate.
  - Enable or disable Secure Boot mode.
  - Configure Platform Key (PK) and Key Exchange Key (KEK) policies
  - Configure Allow Database (DB) and Disallow Database (DBX) certificates.
  - Reset UEFI Secure Boot keys.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_x_auth_options
options:
  boot_mode:
    type: str
    choices: [Uefi, Bios]
    description:
      - Boot mode of the iDRAC. Not supported for 17G iDRAC10 and later.
      - C(Uefi) enables the secure boot in UEFI mode.
      - C(Bios) enables the secure boot in BIOS mode.
  secure_boot:
    type: str
    choices: [Disabled, Enabled]
    description:
      - UEFI Secure Boot.
      - The I(secure_boot) can be C(Enabled) only if I(boot_mode) is C(UEFI) and I(force_int_10) is C(Disabled).
      - C(Disabled) disables the secure boot mode.
      - C(Enabled) enables the secure boot mode.
  secure_boot_mode:
    type: str
    choices: [AuditMode, DeployedMode, UserMode]
    description:
      - The UEFI Secure Boot mode configures how to use the Secure Boot Policy.
      - C(AuditMode) sets the Secure Boot mode to an Audit mode when Platform Key is not installed on the system. The BIOS does not authenticate
        updates to the policy objects and transition between modes. BIOS performs a signature verification on pre-boot images and logs the results in the Image
        Execution Information table, where it processes the images whether the status of verification is pass or fail.
      - C(DeployedMode) sets the Secure Boot mode to a Deployed mode when Platform Key is installed on the system, and then BIOS performs a signature
        verification to update the policy objects.
      - C(UserMode) sets the Secure Boot mode to a User mode when Platform Key is installed on the system, and then BIOS performs signature
        verification to update policy objects.
  secure_boot_policy:
    type: str
    choices: [Custom, Standard]
    description:
      - The following are the types of Secure Boot policy.
      - C(Custom) inherits the standard certificates and image digests that are loaded in the system by default.
        You can modify the certificates and image digests.
      - C(Standard) indicates that the system has default certificates, image digests, or hash loaded from the factory.
      - When the Secure Boot Policy is set to Custom, you can perform following operations such as viewing, exporting,
        importing, deleting, deleting all, and resetting policies.
  force_int_10:
    type: str
    choices: [Disabled, Enabled]
    description:
      - Determines whether the system BIOS loads the legacy video (INT 10h) option ROM from the video controller.
      - This parameter is supported only in UEFI boot mode. If UEFI Secure Boot mode is enabled, you cannot enable this parameter.
      - This parameter is not supported for 17G iDRAC10 and later.
      - C(Disabled) if the operating system supports UEFI video output standards.
      - C(Enabled) if the operating system does not support UEFI video output standards.
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
      - Directory path with write permission when I(export_certificates) is C(true).
  KEK:
    type: list
    elements: path
    description:
      - A list of absolute paths of the Key Exchange Key (KEK) certificate file for UEFI secure boot.
      - Directory path with write permission when I(export_certificates) is C(true).
  database:
    type: list
    elements: path
    description:
      - A list of absolute paths of the Allow Database(DB) certificate file for UEFI secure boot.
      - Directory path with write permission when I(export_certificates) is C(true).
  disallow_database:
    type: list
    elements: path
    description:
      - A list of absolute paths of the Disallow Database(DBX) certificate file for UEFI secure boot.
      - Directory path with write permission when I(export_certificates) is C(true).
  reset_keys:
    type: str
    choices: [DeleteAllKeys, DeletePK, ResetAllKeysToDefault, ResetDB, ResetDBX, ResetKEK, ResetPK]
    description:
      - Resets the UEFI Secure Boot keys.
      - C(DeleteAllKeys) deletes the content of all UEFI Secure Boot key databases (PK, KEK, DB, and DBX). This choice configures the system in Setup Mode.
      - C(DeletePK) deletes the content of the PK UEFI Secure Boot database. This choice configures the system in Setup Mode.
      - C(ResetAllKeysToDefault) resets the content of all UEFI Secure Boot key databases (PK, KEK, DB, and DBX) to their default values.
      - C(ResetDB) resets the content of the DB UEFI Secure Boot database to its default values.
      - C(ResetDBX) resets the content of the DBX UEFI Secure Boot database to its default values.
      - C(ResetKEK) resets the content of the KEK UEFI Secure Boot database to its default values.
      - C(ResetPK) resets the content of the PK UEFI Secure Boot database to its default values.
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
    - "Rounak Adhikary (@rounak-adhikary)"
attributes:
    check_mode:
        description: Runs task to validate without performing action on the target machine.
        support: full
    diff_mode:
        description: Runs the task to report the changes made or to be made.
        support: none
notes:
    - This module will always report changes found to be applied for I(import_certificates) when run in C(check mode).
    - This module does not support idempotency when I(reset_type) or I(export_certificates)
      or I(import_certificates) is provided.
    - To configure the secure boot settings, the idrac_secure_boot module performs the following order of operations
      set attributes, export certificate, reset keys, import certificate, and restart iDRAC.
    - I(export_certificate) will export all the certificates of the key defined in the playbook.
    - This module considers values of I(restart) and I(job_wait) only for the last operation in the sequence.
    - This module supports IPv4 and IPv6 addresses.
    - Only I(reset_keys) is supported on iDRAC8.
"""

EXAMPLES = """
---
- name: Enable Secure Boot.
  dellemc.openmanage.idrac_secure_boot:
    idrac_ip: "192.168.1.2"
    idrac_user: "user"
    idrac_password: "password"
    ca_path: "/path/to/ca_cert.pem"
    secure_boot: "Enabled"

- name: Set Secure Boot mode, Secure Boot policy, and restart iDRAC.
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

- name: Export multiple Secure Boot certificate.
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

- name: Import multiple Secure Boot certificate without applying to iDRAC.
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

- name: Import a Secure Boot certificate and restart the server to apply it.
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

import os
import json
from ansible.module_utils.common.dict_transformations import recursive_diff
from urllib.error import HTTPError, URLError
from ansible.module_utils.compat.version import LooseVersion
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, IdracAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    get_dynamic_uri, remove_key, validate_and_get_first_resource_id_uri,
    trigger_restart_operation, wait_for_lc_status, get_lc_log_or_current_log_time,
    cert_file_format_string, strip_substr_dict, idrac_redfish_job_tracking, reset_host)

SYSTEMS_URI = "/redfish/v1/Systems"
IDRAC_MANAGER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"
IDRAC_JOBS_URI = IDRAC_MANAGER_URI + "/Oem/Dell/Jobs"
iDRAC_JOB_URI = IDRAC_JOBS_URI + "/{job_id}"
iDRAC_JOBS_EXP = IDRAC_JOBS_URI + "?$expand=*($levels=1)"
BIOS_JOB_EXISTS = "BIOS Configuration job already exists."
TIME_FORMAT = "%Y%m%d_%H%M%S"
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The value for the 'job_wait_timeout' parameter cannot be negative or zero."
SUCCESS_MSG = "Successfully imported the SecureBoot certificate."
NO_OPERATION_SKIP = "Task is skipped because no operation is selected."
PROVIDE_ABSOLUTE_PATH = "Please provide absolute path of the certificate file {path}."
NO_READ_PERMISSION_PATH = "Unable to read the certificate file {path}."
NO_FILE_FOUND = "Unable to find the certificate file {path}."
NO_VALID_PATHS = "No valid absolute path found for certificate(s)."
HOST_RESTART_FAILED = "Unable to restart the host system. Check the host status and restart the host system manually."
SUCCESS_COMPLETE = "Successfully updated the {partial} iDRAC Secure Boot settings."
SCHEDULED_SUCCESS = "Successfully scheduled the job and initiated the restart operation for {partial} iDRAC Secure Boot settings update."
COMMITTED_SUCCESS = "Successfully committed {partial} changes. The job is in pending state, and changes will be effective at the next reboot."
RESET_TRIGGERRED = "Reset BIOS action triggered successfully."
CHANGES_FOUND = 'Changes found to be applied.'
SCHEDULED_AND_RESTARTED = "Successfully scheduled the boot certificate import operation and restarted the server."
FAILED_IMPORT = "Failed to import certificate file {path} for {parameter}."
NO_IMPORT_SUCCESS = "The Secure Boot Certificate Import operation was not successful."
NO_RESET_KEYS_SUCCESS = "The Secure Boot Reset Certificates operation was not successful."
NO_DIRECTORY_FOUND = "Unable to find the directory {path}."
NO_WRITE_PERMISSION_PATH = 'Unable to write to the directory {path}.'
TOO_MANY_DIRECTORIES = 'More than one directory found for parameter {key}.'
CERT_IS_EMPTY = 'Certificate string is empty in {file_name} for {parameter}.'
SUCCESS_EXPORT_MSG = 'Successfully exported the SecureBoot certificate.'
UNSUCCESSFUL_EXPORT_MSG = 'Failed to export the SecureBoot certificate.'
NO_CHANGES_FOUND = 'No changes found to be applied.'
INVALID_RESET_KEY = "The Reset key {reset_key_op} entered is not applicable. The supported values are {supported_values}. " \
    "Enter a valid Reset key and retry the operation."
SUCCESS_MSG_RESET = "The {reset_key_op} operation is successfully completed and restarted the host system."
SUCCESS_RESET_KEYS_RESTARTED = "The {reset_key_op} operation is successfully completed and initiated the restart operation for the host system. " \
    "Ensure to wait for the host system to be available."
SCHEDULED_RESET_KEYS = "The {reset_key_op} operation is successfully completed. To apply the updates, restart the host system manually."
odata = '@odata.id'
OPERATION_NOT_SUPPORTED = "{op} is not supported on this firmware version of iDRAC."
SECURE_BOOT_NOT_FOUND = "Secure Boot operations are not supported on this iDRAC."
NO_KEY_FOUND = "The entered {secure_boot_key} is not supported on this host."
LEGACY_BIOS_UNSUPPORTED_MSG = "boot mode and Force int 10 are not supported for 17G and later."
FAILED_RESET_KEYS = "Failed to complete the Reset Certificates operation using {reset_key_op}. Retry the operation."
MESSAGE_EXTENDED_INFO = "@Message.ExtendedInfo"
NO_SECURE_BOOT_SUCCESS = "Unable to update the iDRAC Secure Boot settings because the entered parameter is not supported."
FAILED_BIOS_JOB = "Failed to update the iDRAC Secure Boot settings. Retry the operation."
NOT_UPDATED_ATTRIBUTES = "Unable to update the following BIOS attributes: {attribute_list}. This may be because the attribute is in " \
    "read-only mode, its value depends on other attributes, or an incorrect value was provided."
SYS_CODES = ["SYS410", "SYS409"]


class IDRACSecureBoot:

    def __init__(self, idrac: iDRACRedfishAPI, module: IdracAnsibleModule):
        self.module: IdracAnsibleModule = module
        self.idrac: iDRACRedfishAPI = idrac
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
        secure_boot_database_uri = None
        uri, error_msg = validate_and_get_first_resource_id_uri(
            self.module, self.idrac, SYSTEMS_URI)
        if error_msg:
            self.module.exit_json(msg=error_msg, failed=True)
        resp_secure_boot_uri = get_dynamic_uri(
            self.idrac, uri, 'SecureBoot')
        if not resp_secure_boot_uri:
            self.module.exit_json(msg=SECURE_BOOT_NOT_FOUND, skipped=True)
        self.secure_boot_uri = resp_secure_boot_uri[odata]
        resp_secure_boot = get_dynamic_uri(
            self.idrac, self.secure_boot_uri, 'SecureBootDatabases')
        if resp_secure_boot:
            secure_boot_database_uri = resp_secure_boot[odata]
        return secure_boot_database_uri

    def mapping_secure_boot_database_uri(self):
        mapped_value = {}
        secure_boot_database_uri = self.get_dynamic_secure_boot_database_uri()
        if secure_boot_database_uri:
            secure_boot_database_members = get_dynamic_uri(
                self.idrac, secure_boot_database_uri, 'Members')
            for each_member in secure_boot_database_members:
                for label, last_uri_leaf in self.uri_mapping.items():
                    uri = each_member.get(odata)
                    if last_uri_leaf == uri.split('/')[-1]:
                        mapped_value.update({label: uri})
                        break
        return mapped_value

    def get_dynamic_attribute_uri(self):
        self.uri, error_msg = validate_and_get_first_resource_id_uri(
            self.module, self.idrac, SYSTEMS_URI)
        if error_msg:
            self.module.exit_json(msg=error_msg, failed=True)
        self.bios_uri = get_dynamic_uri(
            self.idrac, self.uri, 'Bios')[odata]

    def get_current_attributes(self):
        self.get_dynamic_attribute_uri()
        curr_attributes_res = get_dynamic_uri(
            self.idrac, self.bios_uri)
        self.curr_attributes_val = curr_attributes_res.get("Attributes", {})
        self.bios_setting_uri = curr_attributes_res.get("@Redfish.Settings").get('SettingsObject').get(odata)

    def perform_restart(self, success_codes, current_time, op, unsuccessful_codes=None):
        resp, _err_msg = trigger_restart_operation(self.idrac,
                                                   self.module.params.get('restart_type'))
        job_wait = self.module.params.get('job_wait')
        if self.module.params.get('import_certificates') and op != 'import_certificates':
            job_wait = True
        if resp.success:
            if job_wait:
                lc_completed, error_msg = wait_for_lc_status(
                    self.idrac, self.module.params.get('job_wait_timeout'))
                self.operation_after_lc_status_check(success_codes, current_time, lc_completed, error_msg, op, unsuccessful_codes)
            else:
                scheduled_msg = {
                    'import_certificates': SCHEDULED_AND_RESTARTED,
                    'reset_keys': SUCCESS_RESET_KEYS_RESTARTED.format(reset_key_op=self.module.params.get('reset_keys'))
                }
                self.module.exit_json(msg=scheduled_msg.get(op))
        else:
            self.module.exit_json(msg=HOST_RESTART_FAILED, skipped=True)

    def operation_after_lc_status_check(self, success_codes, current_time, lc_completed, error_msg, op, unsuccessful_codes):
        success_msgs = {
            'import_certificates': SUCCESS_MSG,
            'reset_keys': SUCCESS_MSG_RESET.format(reset_key_op=self.module.params.get('reset_keys'))
        }
        no_success = {
            'import_certificates': NO_IMPORT_SUCCESS,
            'reset_keys': NO_RESET_KEYS_SUCCESS
        }
        if lc_completed:
            if unsuccessful_codes:
                lc_log, _msg = get_lc_log_or_current_log_time(self.idrac, current_time, unsuccessful_codes)
                if lc_log:
                    self.module.exit_json(msg=NO_RESET_KEYS_SUCCESS, failed=True)
            lc_log, _msg = get_lc_log_or_current_log_time(self.idrac, current_time, success_codes)
            if lc_log:
                if not (op == "reset_keys" and self.module.params.get('import_certificates')) or op == "import_certificates":
                    self.module.exit_json(msg=success_msgs.get(op), changed=True)
            else:
                self.module.exit_json(msg=no_success.get(op),
                                      skipped=True)
        else:
            self.module.exit_json(msg=error_msg, failed=True)


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
        if uri:
            current_time = get_lc_log_or_current_log_time(self.idrac)
            self.looping_over_parameters(payload_values, uri)
            lc_log, scheduled_msg = get_lc_log_or_current_log_time(
                self.idrac, current_time, scheduled_code)
            if not lc_log:
                self.module.exit_json(msg=NO_IMPORT_SUCCESS, skipped=True)
            if self.module.params.get('restart'):
                self.perform_restart(success_codes, current_time, 'import_certificates')
            self.module.exit_json(msg=scheduled_msg)
        self.module.exit_json(msg=OPERATION_NOT_SUPPORTED.format(op='import_certificates'), skipped=True)


class IDRACResetCertificates(IDRACSecureBoot):

    def __init__(self, idrac, module):
        super().__init__(idrac, module)
        self.reset_keys = self.module.params.get('reset_keys')
        self.import_op = self.module.params.get('import_certificates')

    def validate_allowed_reset_keys(self, allowed_values):
        if self.reset_keys not in allowed_values:
            self.module.exit_json(msg=INVALID_RESET_KEY.format(reset_key_op=self.reset_keys,
                                                               supported_values=', '.join(map(str, allowed_values))), skipped=True)

    def fetch_allowed_values_reset_uri(self):
        self.get_dynamic_secure_boot_database_uri()
        resp = get_dynamic_uri(
            self.idrac, self.secure_boot_uri, 'Actions')
        secure_boot_resp = resp.get("#SecureBoot.ResetKeys")
        reset_allowable_values = secure_boot_resp.get("ResetKeysType@Redfish.AllowableValues")
        reset_key_uri = secure_boot_resp.get("target")
        self.validate_allowed_reset_keys(reset_allowable_values)
        return reset_key_uri

    def perform_operation(self):
        """
        Perform operation
        """
        success_codes = ["UEFI0074", "UEFI0286"]
        unsuccessful_codes = ["UEFI0285", "UEFI0423"]
        scheduled_code = ["SWC9007", "SWC9008", "SWC9009", "SWC9012"]
        self.validate_job_wait()
        reset_key_uri = self.fetch_allowed_values_reset_uri()
        payload = {"ResetKeysType": self.reset_keys}
        self.get_current_attributes()
        secure_boot_policy = self.curr_attributes_val.get("SecureBootPolicy")
        if self.module.check_mode:
            if secure_boot_policy == 'Standard':
                self.module.exit_json(msg=NO_CHANGES_FOUND)
            self.module.exit_json(msg=CHANGES_FOUND, changed=True)
        current_time = get_lc_log_or_current_log_time(self.idrac)
        resp = self.idrac.invoke_request(reset_key_uri, "POST", data=payload)
        if resp.success:
            lc_log, _scheduled_msg = get_lc_log_or_current_log_time(
                self.idrac, current_time, unsuccessful_codes)
            if lc_log:
                self.module.exit_json(msg=NO_RESET_KEYS_SUCCESS, skipped=True)
            lc_log, _scheduled_msg = get_lc_log_or_current_log_time(
                self.idrac, current_time, scheduled_code)
            if not lc_log:
                self.module.exit_json(msg=NO_RESET_KEYS_SUCCESS, skipped=True)
            reboot_required = self.module.params.get('restart')
            if self.import_op:
                reboot_required = True
            current_time = get_lc_log_or_current_log_time(self.idrac)
            if reboot_required:
                self.perform_restart(success_codes, current_time, 'reset_keys', unsuccessful_codes)
            else:
                self.module.exit_json(msg=SCHEDULED_RESET_KEYS.format(reset_key_op=self.reset_keys), changed=True)
        else:
            self.module.exit_json(msg=FAILED_RESET_KEYS.format(reset_key_op=self.reset_keys), failed=True)


def get_server_generation(idrac: iDRACRedfishAPI):
    """
    Function wrapping idrac.get_server_generation. Helps with mocked testing.

    Args:
        idrac (iDRACRedfishAPI): iDRACRedfishAPI object.

    Returns:
        Tuple[int, str, str]: A tuple containing the server generation, firmware version, and hardware model.
    """
    return idrac.get_server_generation


class IDRACAttributes(IDRACSecureBoot):

    def __init__(self, idrac: iDRACRedfishAPI, module: IdracAnsibleModule):
        super().__init__(idrac, module)
        self.boot_mode = self.module.params.get('boot_mode')
        self.secure_boot = self.module.params.get('secure_boot')
        self.secure_boot_mode = self.module.params.get('secure_boot_mode')
        self.secure_boot_policy = self.module.params.get('secure_boot_policy')
        self.force_int_10 = self.module.params.get('force_int_10')

        server_generation_op = get_server_generation(self.idrac)
        self.generation, self.idrac_firmware_version = server_generation_op[0], server_generation_op[1]

    def check_scheduled_bios_job(self):
        job_resp = self.idrac.invoke_request(iDRAC_JOBS_EXP, "GET")
        job_list = job_resp.json_data.get('Members', [])
        sch_jb = None
        for jb in job_list:
            if jb.get("JobType") == "BIOSConfiguration" and jb.get("JobState") in ["Scheduled", "Running", "Starting"]:
                sch_jb = jb['Id']
                break
        return sch_jb

    def get_pending_attributes(self):
        try:
            resp = self.idrac.invoke_request(self.bios_setting_uri, "GET")
            attr = resp.json_data.get("Attributes")
        except Exception:
            attr = {}
        return attr

    def trigger_bios_job(self):
        job_id = None
        payload = {"TargetSettingsURI": self.bios_setting_uri}
        resp = self.idrac.invoke_request(IDRAC_JOBS_URI, "POST", data=payload)
        job_id = resp.headers["Location"].split("/")[-1]
        return job_id

    def apply_attributes(self, pending):
        payload = {"Attributes": pending}
        reboot_required = False
        partial_update = False
        resp = self.idrac.invoke_request(self.bios_setting_uri, "PATCH", data=payload)
        if resp.success:
            resp_body = resp.json_data.get(MESSAGE_EXTENDED_INFO)
            filtered_data = [item.get("MessageArgs") for item in resp_body
                             if any(code in item.get("MessageId", "") for code in SYS_CODES)]
            if filtered_data:
                self.module.warn(NOT_UPDATED_ATTRIBUTES.format(attribute_list=', '.join(map(str, filtered_data))))
                partial_update = True
            if self.module.params.get('restart'):
                reboot_required = True
            job_id = self.trigger_bios_job()
            return job_id, reboot_required, partial_update
        self.module.exit_json(msg=FAILED_BIOS_JOB, failed=True)

    def compare_attr_val(self, curr_attr):
        """
        Compare the current attributes with the new attributes.

        Parameters:
            curr_attr (dict): The current attributes.

        Returns:
            dict: A dictionary containing the attributes that are different.
        """
        new_payload = {"BootMode": self.boot_mode, "SecureBoot": self.secure_boot,
                       "SecureBootMode": self.secure_boot_mode, "SecureBootPolicy": self.secure_boot_policy,
                       "ForceInt10": self.force_int_10}
        new_attr = {k: v for k, v in new_payload.items() if v is not None}
        fetched_dict = {}
        attributes = list(new_attr.keys())
        for key in attributes:
            if key in curr_attr:
                fetched_dict[key] = curr_attr[key]
            else:
                new_attr.pop(key)
                self.module.warn(NO_KEY_FOUND.format(secure_boot_key=key))
        if not fetched_dict:
            self.module.exit_json(msg=NO_SECURE_BOOT_SUCCESS, skipped=True)
        diff_tuple = recursive_diff(new_attr, fetched_dict)
        attr = {}
        if diff_tuple and diff_tuple[0]:
            attr = diff_tuple[0]
        return attr

    def attributes_config(self):
        curr_attr = self.curr_attributes_val
        attr = self.compare_attr_val(curr_attr)
        self.import_op = self.module.params.get('import_certificates')
        self.export_op = self.module.params.get('export_certificates')
        self.reset_keys = self.module.params.get('reset_keys')
        if not attr:
            if self.import_op or self.export_op or self.reset_keys:
                return
            elif self.module.check_mode:
                self.module.exit_json(msg=NO_CHANGES_FOUND, changed=False)
            self.module.exit_json(msg=NO_CHANGES_FOUND)
        if self.module.check_mode:
            self.module.exit_json(msg=CHANGES_FOUND, changed=True)
        self.update_pending_attributes(attr)

    def update_pending_attributes(self, attr):
        pending = self.get_pending_attributes()
        pending.update(attr)
        if pending:
            self.handle_scheduled_bios_job()
        self.apply_attributes_and_exit_json(attr)

    def handle_scheduled_bios_job(self):
        job_id = self.check_scheduled_bios_job()
        if job_id:
            self.module.exit_json(msg=BIOS_JOB_EXISTS, job_id=job_id,
                                  skipped=True)

    def apply_attributes_and_exit_json(self, attr):
        reboot_required = False
        job_id, reboot_required, partial_update = self.apply_attributes(attr)
        job_wait = self.module.params.get("job_wait")
        job_resp = self.idrac.invoke_request(iDRAC_JOB_URI.format(job_id=job_id), 'GET')
        job_dict = job_resp.json_data
        if self.import_op or self.export_op or self.reset_keys:
            reboot_required = True
            job_wait = True
        if reboot_required and job_id:
            restart_type = self.module.params.get('restart_type')
            reset_success = reset_host(self.idrac, restart_type, SYSTEMS_URI, self.uri)
            if not reset_success:
                self.module.exit_json(msg=HOST_RESTART_FAILED,
                                      failed=True)
            if job_wait:
                self.handle_job_wait(job_id, partial_update)
                return
            else:
                resp_msg = SCHEDULED_SUCCESS.format(partial='partial' if partial_update
                                                    else '').replace("  ", " ")
                self.module.exit_json(msg=resp_msg, job_status=strip_substr_dict(job_dict), changed=True)
        resp_msg = COMMITTED_SUCCESS.format(partial='partial' if partial_update
                                            else '').replace("  ", " ")
        self.module.exit_json(msg=resp_msg,
                              job_status=strip_substr_dict(job_dict), changed=True)

    def handle_job_wait(self, job_id, partial_update):
        job_failed, msg, job_dict, _wait_time = idrac_redfish_job_tracking(
            self.idrac, iDRAC_JOB_URI.format(job_id=job_id),
            max_job_wait_sec=self.module.params.get('job_wait_timeout'))
        if job_failed:
            self.module.exit_json(failed=True, msg=msg, job_id=job_id)
        if self.import_op or self.export_op or self.reset_keys:
            return
        resp_msg = SUCCESS_COMPLETE.format(partial='partial' if partial_update
                                           else '').replace("  ", " ")
        self.module.exit_json(msg=resp_msg, job_status=strip_substr_dict(job_dict), changed=True)

    def perform_operation(self):
        """
        Perform operation
        """
        self.validate_job_wait()
        if self.generation < 17 and LooseVersion(self.idrac_firmware_version) < '3.0':
            self.module.exit_json(msg=OPERATION_NOT_SUPPORTED.format(op='Secure Boot settings update'), skipped=True)
        if self.generation >= 17:
            # Legacy BIOS boot mode and Force int 10 are not supported from 17G onwards
            # boot mode is a readonly attribute and Force int 10 is not an attribute in 17G
            if self.boot_mode is not None or self.force_int_10 is not None:
                self.module.exit_json(msg=LEGACY_BIOS_UNSUPPORTED_MSG, failed=True, changed=False)
        self.get_current_attributes()
        self.attributes_config()


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
        return any([self.platform_key, self.KEK, self.database, self.disallow_database])

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
        valid_directory = self.filter_invalid_directory()
        if self.module.check_mode:
            if valid_directory:
                self.module.exit_json(msg=CHANGES_FOUND, changed=True)
            elif self.module.params.get('reset_keys') or self.module.params.get('import_certificates'):
                return
            self.module.exit_json(msg=NO_CHANGES_FOUND)

        if not valid_directory:
            self.module.exit_json(msg=UNSUCCESSFUL_EXPORT_MSG, failed=True)

        uri = self.mapping_secure_boot_database_uri()
        if uri:
            parameter_map = {
                'platform_key': self.platform_key,
                'KEK': self.KEK,
                'database': self.database,
                'disallow_database': self.disallow_database
            }
            for parameter, path in parameter_map.items():
                if path:
                    self.fetch_certificate_file_and_write(uri[parameter], path,
                                                          parameter)
            if self.module.params.get('reset_keys') or self.module.params.get('import_certificates'):
                return
            self.module.exit_json(msg=SUCCESS_EXPORT_MSG)
        self.module.exit_json(msg=OPERATION_NOT_SUPPORTED.format(op='export_certificates'), skipped=True)


def main():
    try:
        specs = {
            "boot_mode": {"type": 'str', "choices": ['Uefi', 'Bios']},
            "secure_boot": {"type": 'str', "choices": ['Disabled', 'Enabled']},
            "secure_boot_mode": {"type": 'str', "choices": ['AuditMode', 'DeployedMode', 'UserMode']},
            "secure_boot_policy": {"type": 'str', "choices": ['Custom', 'Standard']},
            "force_int_10": {"type": 'str', "choices": ['Disabled', 'Enabled']},
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
            boot_mode = module.params.get('boot_mode')
            secure_boot = module.params.get('secure_boot')
            secure_boot_mode = module.params.get('secure_boot_mode')
            secure_boot_policy = module.params.get('secure_boot_policy')
            force_int_10 = module.params.get('force_int_10')
            class_mapping = {
                'export_certificates': IDRACExportSecureBoot,
                'reset_keys': IDRACResetCertificates,
                'import_certificates': IDRACImportSecureBoot
            }
            if not all(p is None for p in [boot_mode, secure_boot, secure_boot_mode,
                                           secure_boot_policy, force_int_10]):
                obj = IDRACAttributes(idrac, module)
                obj.perform_operation()
            if any(module.params.get(param) is not None for param in class_mapping.keys()):
                for param, op_class in class_mapping.items():
                    if module.params.get(param):
                        obj = op_class(idrac, module)
                        obj.perform_operation()
            if obj is None:
                module.exit_json(msg=NO_OPERATION_SKIP, skipped=True)
    except HTTPError as err:
        filter_err = remove_key(json.load(err), regex_pattern='(.*?)@odata')
        message_details = filter_err.get('error').get(MESSAGE_EXTENDED_INFO)[0]
        message_id = message_details.get('MessageId').split(".")[-1]
        skippable_messages = {
            'SYS011': message_details.get('Message'),
            'SYS409': message_details.get('Message'),
            'SYS410': message_details.get('Message'),
            'SYS439': message_details.get('Message')
        }
        if message_id in skippable_messages:
            module.exit_json(msg=skippable_messages[message_id], skipped=True)
        module.exit_json(msg=str(err), error_info=filter_err, failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (SSLValidationError, ConnectionError, TypeError, ValueError, OSError) as err:
        module.exit_json(msg=str(err), failed=True)


if __name__ == '__main__':
    main()
