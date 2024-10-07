from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: test file
short_description: test file
version_added: "9.8.0"
description:
  - This module allows to manage the different power states of the specified device.
extends_documentation_fragment:
  - dellemc.openmanage.omevv_auth_options
options:
  uri:
    description: Need to pass the URI
    required: true
    type: str
  filter:
    description: Filter to pass
    required: false
    type: dict
requirements:
    - "python >= 3.9.6"
author:
    - "Abhishek Sinha (@ABHISHEK-SINHA10)
notes:
    - Run this module from a system that has direct access to Redfish APIs.
    - This module supports C(check_mode).
'''

EXAMPLES = r'''
---
- name: Test
  dellemc.openmanage.test:
    baseuri: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    uri: "/Consoles"
'''

RETURN = r'''
---
msg:
  description: Overall status of the reset operation.
  returned: always
  type: str
  sample: "Successfully performed the reset type operation 'On'."
error_info:
  type: dict
  description: Details of the HTTP error.
  returned: on http error
  sample:  {
    "error": {
        "@Message.ExtendedInfo": [
            {
                "Message": "Unable to complete the operation because the resource
                 /redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset entered in not found.",
                "MessageArgs": [
                    "/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset"
                ],
                "MessageArgs@odata.count": 1,
                "MessageId": "IDRAC.2.1.SYS403",
                "RelatedProperties": [],
                "RelatedProperties@odata.count": 0,
                "Resolution": "Enter the correct resource and retry the operation.
                 For information about valid resource,
                 see the Redfish Users Guide available on the support site.",
                "Severity": "Critical"
            },
        ],
        "code": "Base.1.5.GeneralError",
        "message": "A general error has occurred. See ExtendedInfo for more information"
    }
}
'''

from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.omevv import RestOMEVV, OMEVVAnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


def main():
    specs = {
        "uri": {"required": True, "type": 'str'},
        "filter": {"required": False, "type": 'dict'}
    }

    module = OMEVVAnsibleModule(argument_spec=specs)
    try:
        with RestOMEVV(module.params) as rest_obj:
            qp = module.params.get("filter")
            resp = rest_obj.invoke_request("GET", module.params.get("uri"), query_param=qp)
            module.exit_json(msg=resp.json_data)
    except HTTPError as err:
        module.exit_json(msg=str(err))
    except (URLError, SSLValidationError, ConnectionError, TypeError, ValueError, OSError, SSLError) as err:
        module.exit_json(msg=str(err))


if __name__ == '__main__':
    main()
