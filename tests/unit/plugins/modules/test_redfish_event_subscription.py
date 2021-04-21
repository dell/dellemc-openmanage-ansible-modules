# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.3
# Copyright (C) 2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import json
from ansible_collections.dellemc.openmanage.plugins.modules import redfish_event_subscription
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule, Constants
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from io import StringIO
from ansible.module_utils._text import to_text

tarrget_error_msg = "The target device does not support the system reset" \
                    " feature using Redfish API."
MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'


@pytest.fixture
def redfish_connection_mock(mocker, redfish_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'redfish_event_subscription.Redfish')
    redfish_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    redfish_connection_mock_obj.invoke_request.return_value = redfish_response_mock
    return redfish_connection_mock_obj

class TestRedfishSubscription(FakeAnsibleModule):
    module = redfish_event_subscription

    @pytest.mark.parametrize("val", [{"destination": "https://192.168.1.100:8188"},
                                    {"destination": "https://192.168.1.100:8189"}])
    def test_function_get_subscription_success(self, mocker, redfish_connection_mock, redfish_response_mock, redfish_default_args, val):
        redfish_default_args.update({"state": "absent"})
        redfish_default_args.update({"destination": val["destination"]})
        redfish_default_args.update({"type": "metric"})
        json_data1 = {
            "@odata.context": "/redfish/v1/$metadata#EventDestination.EventDestination",
            "@odata.id": "/redfish/v1/EventService/Subscriptions/c7e5c3fc-8204-11eb-bd10-2cea7ff7fe80",
            "@odata.type": "#EventDestination.v1_6_0.EventDestination",
            "Context": "RedfishEvent",
            "DeliveryRetryPolicy": "RetryForever",
            "Description": "Event Subscription Details",
            "Destination": "https://192.168.1.100:8189",
            "EventFormatType": "Event",
            "EventTypes": [
                "Alert"
            ],
            "EventTypes@odata.count": 1,
            "HttpHeaders": [],
            "HttpHeaders@odata.count": 0,
            "Id": "c7e5c3fc-8204-11eb-bd10-2cea7ff7fe80",
            "MetricReportDefinitions": [],
            "MetricReportDefinitions@odata.count": 0,
            "Name": "EventSubscription c7e5c3fc-8204-11eb-bd10-2cea7ff7fe80",
            "OriginResources": [],
            "OriginResources@odata.count": 0,
            "Protocol": "Redfish",
            "Status": {
                "Health": "OK",
                "HealthRollup": "OK",
                "State": "Enabled"
            },
            "SubscriptionType": "RedfishEvent"
        }
        json_data2 = {
            "@odata.context": "/redfish/v1/$metadata#EventDestination.EventDestination",
            "@odata.id": "/redfish/v1/EventService/Subscriptions/c6ff37fc-8204-11eb-b08f-2cea7ff7fe80",
            "@odata.type": "#EventDestination.v1_6_0.EventDestination",
            "Context": "RedfishEvent",
            "DeliveryRetryPolicy": "RetryForever",
            "Description": "Event Subscription Details",
            "Destination": "https://192.168.1.100:8188",
            "EventFormatType": "MetricReport",
            "EventTypes": [
                "MetricReport"
            ],
            "EventTypes@odata.count": 1,
            "HttpHeaders": [],
            "HttpHeaders@odata.count": 0,
            "Id": "c6ff37fc-8204-11eb-b08f-2cea7ff7fe80",
            "MetricReportDefinitions": [],
            "MetricReportDefinitions@odata.count": 0,
            "Name": "EventSubscription c6ff37fc-8204-11eb-b08f-2cea7ff7fe80",
            "OriginResources": [],
            "OriginResources@odata.count": 0,
            "Protocol": "Redfish",
            "Status": {
                "Health": "OK",
                "HealthRollup": "OK",
                "State": "Enabled"
            },
            "SubscriptionType": "RedfishEvent"
        }

        mocker.patch(MODULE_PATH + 'redfish_event_subscription.get_subscription_details', side_effect=[json_data1, json_data2])

        redfish_response_mock.json_data = {
            "@odata.context": "/redfish/v1/$metadata#EventDestinationCollection.EventDestinationCollection",
            "@odata.id": "/redfish/v1/EventService/Subscriptions",
            "@odata.type": "#EventDestinationCollection.EventDestinationCollection",
            "Description": "List of Event subscriptions",
            "Members": [
                {
                    "@odata.id": "/redfish/v1/EventService/Subscriptions/c6ff37fc-8204-11eb-b08f-2cea7ff7fe80"
                },
                {
                    "@odata.id": "/redfish/v1/EventService/Subscriptions/c7e5c3fc-8204-11eb-bd10-2cea7ff7fe80"
                }
            ],
            "Members@odata.count": 2,
            "Name": "Event Subscriptions Collection"
        }
        redfish_response_mock.success = True
        f_module = self.get_module_mock(params=redfish_default_args)
        result = self.module.get_subscription(redfish_connection_mock, val["destination"])
        assert result["Destination"] == val["destination"]

    @pytest.mark.parametrize("val", [{"destination": "https://192.168.1.100:8188", "type": "metric", "event_format_type": "MetricReport"},
                                    {"destination": "https://192.168.1.100:8188", "type": "alert", "event_format_type": "Event"}])
    def test_function_create_subscription(self, mocker, redfish_connection_mock, redfish_response_mock, redfish_default_args, val):
        redfish_default_args.update({"state": "absent"})
        redfish_default_args.update({"destination": val["destination"]})
        redfish_default_args.update({"type":  val["type"]})

        redfish_response_mock.json_data = {
            "Id": "c6ff37fc-8204-11eb-b08f-2cea7ff7fe80",
            "Destination": val["destination"],
            "EventFormatType": val["event_format_type"],
            "Context": "RedfishEvent",
            "Protocol": "Redfish",
            "EventTypes": ["MetricReport"],
            "SubscriptionType": "RedfishEvent"
        }
        redfish_response_mock.success = True
        f_module = self.get_module_mock(params=redfish_default_args)
        result = self.module.create_subscription(redfish_connection_mock, f_module)
        assert result.json_data["Destination"] == val["destination"]
        assert result.json_data["EventFormatType"] == val["event_format_type"]

    def test_module_absent_does_not_exist(self, mocker, redfish_connection_mock, redfish_response_mock, redfish_default_args):
        redfish_default_args.update({"state": "absent"})
        redfish_default_args.update({"destination": "https://192.168.1.100:8188"})
        redfish_default_args.update({"type": "metric"})

        redfish_connection_mock.patch(MODULE_PATH + 'redfish_event_subscription.get_subscription',
                     return_value=None)
        redfish_response_mock.success = True
        result = self._run_module(redfish_default_args)
        assert result["msg"] == "No changes made."

    def test_module_absent_does_exist(self, mocker, redfish_connection_mock, redfish_response_mock, redfish_default_args):
        redfish_default_args.update({"state": "absent"})
        redfish_default_args.update({"destination": "https://192.168.1.100:8188"})
        redfish_default_args.update({"type": "metric"})

        json_data = {
            "Id": "c6ff37fc-8204-11eb-b08f-2cea7ff7fe80",
            "Destination": "https://192.168.1.100:8188",
            "EventFormatType": "MetricReport",
            "Context": "RedfishEvent",
            "Protocol": "Redfish",
            "EventTypes": ["MetricReport"],
            "SubscriptionType": "RedfishEvent"
        } 
        redfish_response_mock.success = True
        mocker.patch(MODULE_PATH + 'redfish_event_subscription.get_subscription', return_value=json_data)
        mocker.patch(MODULE_PATH + 'redfish_event_subscription.delete_subscription', return_value=redfish_response_mock)
        f_module = self.get_module_mock()
        result = self._run_module(redfish_default_args)
        print(result)
        assert result["msg"] == "Successfully deleted subscription."

    def test_module_present_does_not_exist(self, mocker, redfish_connection_mock, redfish_response_mock, redfish_default_args):
        redfish_default_args.update({"state": "present"})
        redfish_default_args.update({"destination": "https://192.168.1.100:8188"})
        redfish_default_args.update({"type": "metric"})

        json_data = {
            "Destination": "https://192.168.1.100:8188",
            "EventFormatType": "MetricReport",
            "Context": "RedfishEvent",
            "Protocol": "Redfish",
            "EventTypes": ["MetricReport"],
            "SubscriptionType": "RedfishEvent"
        }
        mocker.patch(MODULE_PATH + 'redfish_event_subscription.get_subscription', return_value=None)
        create_subscription_response_mock = redfish_response_mock
        create_subscription_response_mock.json_data = json_data
        mocker.patch(MODULE_PATH + 'redfish_event_subscription.create_subscription', return_value=create_subscription_response_mock)
        f_module = self.get_module_mock()
        redfish_response_mock.success = True
        result = self._run_module(redfish_default_args)
        print(result)
        assert result["msg"] == "Successfully created subscription."

    def test_module_present_does_exist(self, mocker, redfish_connection_mock, redfish_response_mock, redfish_default_args):
        redfish_default_args.update({"state": "present"})
        redfish_default_args.update({"destination": "https://192.168.1.100:8188"})
        redfish_default_args.update({"type": "metric"})

        json_data = {
            "Id": "c6ff37fc-8204-11eb-b08f-2cea7ff7fe80",
            "Destination": "https://192.168.1.100:8188",
            "EventFormatType": "MetricReport",
            "Context": "RedfishEvent",
            "Protocol": "Redfish",
            "EventTypes": ["MetricReport"],
            "SubscriptionType": "RedfishEvent"
        } 
        mocker.patch(MODULE_PATH + 'redfish_event_subscription.get_subscription', return_value=json_data)
        f_module = self.get_module_mock()
        redfish_response_mock.success = True
        result = self._run_module(redfish_default_args)
        print(result)
        assert result["msg"] == "Subscription exists. No changes made."

