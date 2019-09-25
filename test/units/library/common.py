# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0
# Copyright (C) 2019 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

import pytest
from units.modules.utils import set_module_args
from units.modules.utils import AnsibleFailJson, AnsibleExitJson

class Constants:
    device_id1 = 1234
    device_id2 = 4321
    service_tag1 = "MXL1234"


class FakeAnsibleModule:

    def _run_module(self, module_args):
        set_module_args(module_args)
        with pytest.raises(AnsibleExitJson) as ex:
            self.module.main()
        return ex.value.args[0]

    def _run_module_with_fail_json(self, module_args):
        set_module_args(module_args)
        with pytest.raises(AnsibleFailJson) as exc:
            self.module.main()
        result = exc.value.args[0]
        return result
