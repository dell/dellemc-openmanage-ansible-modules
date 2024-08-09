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
    platform_key: /user/name/certificates/pk.crt
    key_exchange_key:
      - /user/name/certificates/kek1.crt
      - /user/name/certificates/kek2.crt  
    database:
      - /user/name/certificates/db1.crt
      - /user/name/certificates/db2.crt
    disallow_database:
      - /user/name/certificates/dbx1.crt
      - /user/name/certificates/dbx2.crt
"""

RETURN = r'''
---
msg:
  description: Status of the attribute update operation.
  returned: when network attributes is applied
  type: str
  sample: "Successfully updated the network attributes."
invalid_attributes:
    description: Dictionary of invalid attributes provided that cannot be applied.
    returned: On invalid attributes or values
    type: dict
    sample: {
        "IscsiInitiatorIpAddr": "Attribute is not valid.",
        "IscsiInitiatorSubnet": "Attribute is not valid."
    }
job_status:
    description: Returns the output for status of the job.
    returned: always
    type: dict
    sample: {
        "ActualRunningStartTime": null,
        "ActualRunningStopTime": null,
        "CompletionTime": null,
        "Description": "Job Instance",
        "EndTime": "TIME_NA",
        "Id": "JID_XXXXXXXXX",
        "JobState": "Scheduled",
        "JobType": "NICConfiguration",
        "Message": "Task successfully scheduled.",
        "MessageArgs": [],
        "MessageId": "JCP001",
        "Name": "Configure: NIC.Integrated.1-1-1",
        "PercentComplete": 0,
        "StartTime": "2023-08-07T06:21:24",
        "TargetSettingsURI": null
    }
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
import base64
import time
from urllib.error import HTTPError, URLError
from ansible.module_utils.compat.version import LooseVersion
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, IdracAnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    delete_job, get_current_time, get_dynamic_uri, get_idrac_firmware_version,
    get_scheduled_job_resp, remove_key, validate_and_get_first_resource_id_uri,
    idrac_redfish_job_tracking, xml_data_conversion, trigger_restart_operation)

SYSTEMS_URI = "/redfish/v1/Systems"
iDRAC_JOB_URI = "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/{job_id}"
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The value for the `job_wait_timeout` parameter cannot be negative or zero."
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
                self.module.warn(f"Please provide absolute path of the certificate file {path}.")
                invalid_paths.add(path)
            if path and not os.path.isfile(path):
                self.module.warn(f"Unable to read the certificate file {path}.")
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
  
    def construct_payload(self):
        """
        Construct payload
        """
        payload = {}
        if self.platform_key:
            payload['platform_key'] = self.read_certificate_file(self.platform_key[0])
        if self.key_exchange_key:
            payload['key_exchange_key'] = [self.read_certificate_file(path) for path in self.key_exchange_key]
            payload['key_exchange_key'] = "".join(payload['key_exchange_key'])
        if self.database:
            payload['database'] = [str(self.read_certificate_file(path)) for path in self.database]
            payload['database'] = "".join(payload['database'])
        if self.disallow_database:
            payload['disallow_database'] = [str(self.read_certificate_file(path)) for path in self.disallow_database]
            payload['disallow_database'] = "".join(payload['disallow_database'])
        return payload

    def perform_operation(self):
        """
        Perform operation
        """
        # self.filter_invalid_paths()
        # self.validate_job_wait()
        # payload_values = self.construct_payload()
        # if not payload_values:
        #     return False
        # uri = self.mapping_secure_boot_database_uri()
        # for each_label in payload_values:
        #     payload = {"CertificateString": payload_values[each_label],
        #                "CertificateType": "PEM"}
        #     certificates_uri = get_dynamic_uri(self.idrac, uri[each_label], 'Certificates')[odata]
        #     self.idrac.invoke_request(method='POST', uri=certificates_uri, data=payload)
        if self.module.params.get('restart'):
          restart_triggered, msg = trigger_restart_operation(self.module, self.idrac,
                                                             self.module.params.get('restart_type'))
          if not restart_triggered and msg != '':
            self.module.exit_json(msg=msg, failed=True)
          self.module.exit_json(msg=restart_triggered)


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
