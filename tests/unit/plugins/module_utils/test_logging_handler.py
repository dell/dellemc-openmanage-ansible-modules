# -*- coding: utf-8 -*-


# Dell OpenManage Ansible Modules
# Version 9.12.2
# Copyright (C) 2025 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.

import pytest
from datetime import datetime
from unittest.mock import patch
from ansible_collections.dellemc.openmanage.plugins.module_utils.logging_handler import CustomRotatingFileHandler


@pytest.fixture
def mock_datetime():
    with patch('ansible_collections.dellemc.openmanage.plugins.module_utils.logging_handler.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2025, 6, 6)
        yield mock_dt


def test_rotation_filename(mock_datetime):
    handler = CustomRotatingFileHandler('test.log', maxBytes=1000, backupCount=3)
    default_name = 'test.log.1'
    expected_name = 'test_20250606.log.1'
    actual_name = handler.rotation_filename(default_name)
    assert actual_name == expected_name
