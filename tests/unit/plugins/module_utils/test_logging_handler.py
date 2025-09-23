# -*- coding: utf-8 -*-


# Dell OpenManage Ansible Modules
# Version 10.0.1
# Copyright (C) 2025 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.


from datetime import datetime
from ansible_collections.dellemc.openmanage.plugins.module_utils.logging_handler import CustomRotatingFileHandler
import tempfile
import os


def test_rotation_filename_format():
    with tempfile.TemporaryDirectory() as tmpdir:
        log_path = os.path.join(tmpdir, "test.log")
        handler = CustomRotatingFileHandler(log_path, maxBytes=1000, backupCount=1)
        default_name = "test.log.1"

        rotated_name = handler.rotation_filename(default_name)

        expected_date = datetime.now().strftime("%Y%m%d")
        assert rotated_name.startswith(f"test_{expected_date}.log.1")
