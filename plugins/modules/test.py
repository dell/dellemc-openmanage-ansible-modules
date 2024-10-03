from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
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
