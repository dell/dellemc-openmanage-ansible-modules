# -*- coding: utf-8 -*-
# Dell OpenManage Ansible Modules
# Version 10.0.0
# Copyright (C) 2018-2025 Dell Inc. or its subsidiaries. All Rights Reserved.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from io import StringIO

import pytest
from ansible.module_utils._text import to_text
from urllib.error import HTTPError, URLError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.modules import \
    idrac_os_deployment
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import \
    FakeAnsibleModule, AnsibleFailJSonException
from unittest.mock import MagicMock

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
MODULE_UTIL_PATH = 'ansible_collections.dellemc.openmanage.plugins.module_utils.utils.'
JOB_NOT_FOUND = "No matching job found following the BootToNetworkISO operation."
INVALID_EXPOSEDURATION = "Invalid value for ExposeDuration."


class TestiDRACOSDeployment(FakeAnsibleModule):
    module = idrac_os_deployment

    @pytest.fixture
    def idrac_osd_mock(self):
        idrac_obj = MagicMock()
        return idrac_obj

    @pytest.fixture
    def idrac_osd_connection_mock(self, mocker, idrac_osd_mock):
        idrac_conn_mock = mocker.patch(MODULE_PATH + 'idrac_os_deployment.iDRACRedfishAPI',
                                       return_value=idrac_osd_mock)
        idrac_conn_mock.return_value.__enter__.return_value = idrac_osd_mock
        return idrac_conn_mock

    def test_minutes_to_iso_format_positive_scenario(self, idrac_default_args):
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        resp = self.module.minutes_to_iso_format(f_module, 10)
        assert resp == "0000-00-00T00:10:00-00:00"

    def test_minutes_to_iso_format_negative_scenario(self, idrac_default_args):
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        with pytest.raises(AnsibleFailJSonException, match=INVALID_EXPOSEDURATION):
            self.module.minutes_to_iso_format(f_module, -10)

    def test_get_current_time_from_iDRAC(self, idrac_osd_connection_mock):
        obj = MagicMock()
        obj.json_data = {"DateTime": "2022-09-14T05:59:35-05:00"}
        idrac_osd_connection_mock.invoke_request.return_value = obj
        resp = self.module.get_current_time_from_idrac(
            idrac_osd_connection_mock)
        assert resp == "2022-09-14T05:59:35-05:00"

    def test_construct_payload(self, idrac_default_args):
        _params = {'expose_duration': 5,
                   'iso_image': '/path/to/image.iso',
                   'share_password': 'password',
                   'share_user': 'username'}
        # Scenario 1: For CIFS
        idrac_default_args.update(_params)
        idrac_default_args.update({'share_name': '\\\\192.168.0.1\\sharename'})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        resp = self.module.construct_payload(
            f_module)
        assert resp == {'ExposeDuration': '0000-00-00T00:05:00-00:00', 'IPAddress': '192.168.0.1', 'ShareName': 'sharename',
                        'ShareType': 'CIFS', 'ImageName': '/path/to/image.iso', 'Password': 'password', 'UserName': 'username'}

        # Scenario 2: For NFS
        idrac_default_args.update({'share_name': "192.168.0.0:/nfsfileshare"})
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)
        resp = self.module.construct_payload(
            f_module)
        assert resp == {'ExposeDuration': '0000-00-00T00:05:00-00:00', 'IPAddress': '192.168.0.0', 'ShareName': 'nfsfileshare',
                        'ShareType': 'NFS', 'ImageName': '/path/to/image.iso', 'Password': 'password', 'UserName': 'username'}

    def test_getting_top_osd_job_and_tracking(self, idrac_default_args, idrac_osd_connection_mock,
                                              idrac_osd_mock, mocker):
        job_detail = MagicMock()
        job_detail.json_data = {
            "JobState": "Passed",
            "StartTime": "2025-04-07T12:15:12",
            "Id": "JID_440458720416"
        }
        obj = MagicMock()
        obj.json_data = {
            "Members": [
                job_detail
            ]
        }
        idrac_osd_connection_mock.invoke_request.return_value = obj
        mocker.patch(MODULE_PATH + 'idrac_os_deployment.' +
                     'time.sleep', return_value=None)
        mocker.patch(MODULE_PATH + 'idrac_os_deployment.wait_for_idrac_job_completion',
                     return_value=(job_detail, ""))
        mocker.patch(
            MODULE_PATH + 'idrac_os_deployment.filter_job_from_members',
            return_value=job_detail)
        f_module = self.get_module_mock(
            params=idrac_default_args, check_mode=False)

        # Scenario 1: Searching job before Start time
        resp = self.module.getting_top_osd_job_and_tracking(
            idrac_osd_connection_mock, f_module, "2025-04-07T12:10:12")
        assert resp == job_detail.json_data

        # Scenario 2: Searching job after Start time so no job will be found
        no_job = MagicMock()
        no_job.json_data = {"Members": []}
        idrac_osd_connection_mock.invoke_request.return_value = no_job
        mocker.patch(
            MODULE_PATH + 'idrac_os_deployment.filter_job_from_members',
            return_value={})
        with pytest.raises(AnsibleFailJSonException, match=JOB_NOT_FOUND) as excinfo:
            self.module.getting_top_osd_job_and_tracking(
                idrac_osd_connection_mock, f_module, "2025-04-07T12:20:12")
        assert excinfo.value.args[0] == "No matching job found following the BootToNetworkISO operation."

    def test_filter_job_from_members(self, idrac_osd_connection_mock):
        job_name = 'OSD: BootTONetworkISO'
        members = [
            {"@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/JID_001"}
        ]
        job_detail = MagicMock()
        job_detail.json_data = {
            "JobState": "Passed",
            "StartTime": "2025-04-07T12:15:12",
            "Id": "JID_001",
            "Name": job_name
        }
        idrac_osd_connection_mock.invoke_request.return_value = job_detail

        result = self.module.filter_job_from_members(idrac_osd_connection_mock, members, "2025-04-07T12:14:12")

        assert result["Name"] == job_name
        assert result["StartTime"] == "2025-04-07T12:15:12"

    def test_idrac_os_deployment_main(self, idrac_default_args, idrac_osd_connection_mock, idrac_osd_mock, mocker):
        idrac_default_args.update({"iso_image": "/path/to/image.iso", "share_name": "192.168.10.1:/nfsfileshare"})
        mocker.patch(MODULE_PATH + 'idrac_os_deployment.get_current_time_from_idrac', return_value="2025-04-07T12:20:12")
        mocker.patch(MODULE_PATH + 'idrac_os_deployment.construct_payload', return_value={})
        idrac_osd_connection_mock.invoke_request.return_value = None

        # Scenario 1: Job failed
        job_detail = {'JobState': 'Failed', 'Message': "IP Address format is invalid."}
        mocker.patch(MODULE_PATH + 'idrac_os_deployment.getting_top_osd_job_and_tracking', return_value=job_detail)
        resp = self._run_module(idrac_default_args)
        assert resp['failed'] is True

        # Scenario 2: Job passed
        job_detail = {'JobState': 'Passed', 'Message': "The command was successful."}
        mocker.patch(MODULE_PATH + 'idrac_os_deployment.getting_top_osd_job_and_tracking', return_value=job_detail)
        resp = self._run_module(idrac_default_args)
        assert resp['changed'] is True

    @pytest.mark.parametrize("exc_type",
                             [URLError, HTTPError, SSLValidationError, ConnectionError, TypeError, ValueError])
    def test_idrac_os_deployment_main_exception_handling_case(self, exc_type, mocker, idrac_default_args,
                                                              idrac_osd_connection_mock, idrac_osd_mock):
        json_str = to_text(json.dumps({"data": "out"}))
        if exc_type in [HTTPError, SSLValidationError]:
            mocker.patch(MODULE_PATH + "idrac_os_deployment.get_current_time_from_idrac",
                         side_effect=exc_type('https://testhost.com', 400,
                                              'http error message',
                                              {"accept-type": "application/json"},
                                              StringIO(json_str)))
        else:
            mocker.patch(MODULE_PATH + "idrac_os_deployment.get_current_time_from_idrac",
                         side_effect=exc_type('test'))
        idrac_default_args.update(
            {"iso_image": "/path/to/image.iso", "share_name": "192.168.10.1:/nfsfileshare"})
        result = self._run_module(idrac_default_args)
        if exc_type == URLError:
            assert result['unreachable'] is True
        else:
            assert result['failed'] is True
        assert 'msg' in result
