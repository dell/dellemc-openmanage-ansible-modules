# -*- coding: utf-8 -*-
#
# Dell OpenManage Ansible Modules
# Version 8.6.0
# Copyright (C) 2023 Dell Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import config_ipv6


class TestUtils(object):
    def test_valid_ipv6_address_with_port(self):
        hostname = "[2001:db8::1]:80"
        expected_hostname = "[2001:db8::1]:80"
        result = config_ipv6(hostname)
        assert result == expected_hostname

    def test_valid_ipv6_address_without_port(self):
        hostname = "2001:db8::1"
        expected_hostname = "[2001:db8::1]"
        result = config_ipv6(hostname)
        assert result == expected_hostname

    def test_valid_ipv6_address_with_square_brackets(self):
        hostname = "[2001:0db8:0000:0000:0000:8a2e:0370:7334]"
        expected_hostname = "[2001:0db8:0000:0000:0000:8a2e:0370:7334]"
        result = config_ipv6(hostname)
        assert result == expected_hostname

    def test_valid_ipv6_address_case01(self):
        hostname = "2001:db8::8a2e:370:7334"
        expected_hostname = "[2001:db8::8a2e:370:7334]"
        result = config_ipv6(hostname)
        assert result == expected_hostname

    def test_invalid_ipv6_address_case02(self):
        hostname = "[2001:0db8:0:0:0:8a2e:0370:7334]:80"
        expected_hostname = "[2001:0db8:0:0:0:8a2e:0370:7334]:80"
        result = config_ipv6(hostname)
        assert result == expected_hostname

    def test_invalid_ipv6_address_case03(self):
        hostname = "2001:db8:0:0:0:8a2e:370:7334"
        expected_hostname = "[2001:db8:0:0:0:8a2e:370:7334]"
        result = config_ipv6(hostname)
        assert result == expected_hostname

    def test_invalid_ipv6_address_case04(self):
        hostname = "ff06::c3"
        expected_hostname = "[ff06::c3]"
        result = config_ipv6(hostname)
        assert result == expected_hostname

    def test_valid_ipv4(self):
        hostname = "192.168.24.15"
        expected_hostname = "192.168.24.15"
        result = config_ipv6(hostname)
        assert result == expected_hostname

    def test_valid_ipv4_with_port(self):
        hostname = "192.168.24.15:80"
        expected_hostname = "192.168.24.15:80"
        result = config_ipv6(hostname)
        assert result == expected_hostname

    def test_valid_hostname_case01(self):
        hostname = "abcd123"
        expected_hostname = "abcd123"
        result = config_ipv6(hostname)
        assert result == expected_hostname

    def test_valid_hostname_case02(self):
        hostname = "redfish123"
        expected_hostname = "redfish123"
        result = config_ipv6(hostname)
        assert result == expected_hostname

    def test_valid_hostname_case03(self):
        hostname = "redfish-domain.com"
        expected_hostname = "redfish-domain.com"
        result = config_ipv6(hostname)
        assert result == expected_hostname

    def test_valid_hostname_with_port(self):
        hostname = "abcd123:443"
        expected_hostname = "abcd123:443"
        result = config_ipv6(hostname)
        assert result == expected_hostname

    def test_invalid_ipv4(self):
        hostname = "192.168.1"
        expected_hostname = "192.168.1"
        result = config_ipv6(hostname)
        assert result == expected_hostname

    def test_invalid_ipv4_with_port(self):
        hostname = "192.168.1:22"
        expected_hostname = "192.168.1:22"
        result = config_ipv6(hostname)
        assert result == expected_hostname

    def test_invalid_ipv6_cas01(self):
        hostname = "2001:db8::8a2e::370:7334"
        expected_hostname = "[2001:db8::8a2e::370:7334]"
        result = config_ipv6(hostname)
        assert result == expected_hostname

    def test_invalid_ipv6_cas02(self):
        hostname = "2001:db8::1:"
        expected_hostname = "[2001:db8::1:]"
        result = config_ipv6(hostname)
        assert result == expected_hostname

    def test_invalid_ipv6_cas03(self):
        hostname = "2001:0db8:85a3:0000:0000:8a2e:0370:7334:"
        expected_hostname = "[2001:0db8:85a3:0000:0000:8a2e:0370:7334:]"
        result = config_ipv6(hostname)
        assert result == expected_hostname

    def test_invalid_ipv6_with_port(self):
        hostname = "[2001:db8::8a2e::370:7334]:180"
        expected_hostname = "[2001:db8::8a2e::370:7334]:180"
        result = config_ipv6(hostname)
        assert result == expected_hostname

    def test_invalid_hostname_cas01(self):
        hostname = "invalid:address"
        expected_hostname = "invalid:address"
        result = config_ipv6(hostname)
        assert result == expected_hostname
