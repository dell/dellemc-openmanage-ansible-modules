# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 7.0.0
# Copyright (C) 2021-2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from ansible_collections.dellemc.openmanage.plugins.modules import redfish_event_subscription
from ansible_collections.dellemc.openmanage.tests.unit.plugins.modules.common import FakeAnsibleModule

MODULE_PATH = 'ansible_collections.dellemc.openmanage.plugins.modules.'
DESTINATION_INVALID = "The Parameter destination must have an HTTPS destination. The HTTP destination is not allowed"
SUBSCRIPTION_EXISTS = "No changes found to be applied."
SUBSCRIPTION_DELETED = "Successfully deleted the subscription."
SUBSCRIPTION_UNABLE_DEL = "Unable to delete the subscription."
SUBSCRIPTION_UNABLE_ADD = "Unable to add a subscription."
SUBSCRIPTION_ADDED = "Successfully added the subscription."
DESTINATION_MISMATCH = "No changes found to be applied."
EVENT_TYPE_INVALID = "value of event_type must be one of: Alert, MetricReport, got: Metricreport"
PARAM_DESTINATION = "https://XX.XX.XX.XX:8188"


@pytest.fixture
def redfish_connection_mock(mocker, redfish_response_mock):
    connection_class_mock = mocker.patch(MODULE_PATH + 'redfish_event_subscription.Redfish')
    redfish_connection_mock_obj = connection_class_mock.return_value.__enter__.return_value
    redfish_connection_mock_obj.invoke_request.return_value = redfish_response_mock
    return redfish_connection_mock_obj


class TestRedfishSubscription(FakeAnsibleModule):
    module = redfish_event_subscription

    @pytest.mark.parametrize("val", [{"destination": PARAM_DESTINATION},
                                     {"destination": "https://XX.XX.XX.XX:8189"}])
    def test_function_get_subscription_success(self, mocker, redfish_connection_mock, redfish_response_mock,
                                               redfish_default_args, val):
        redfish_default_args.update({"state": "absent"})
        redfish_default_args.update({"destination": val["destination"]})
        redfish_default_args.update({"event_type": "MetricReport"})
        redfish_default_args.update({"event_format_type": "MetricReport"})
        json_data1 = {
            "@odata.context": "/redfish/v1/$metadata#EventDestination.EventDestination",
            "@odata.id": "/redfish/v1/EventService/Subscriptions/c7e5c3fc-8204-11eb-bd10-2cea7ff7fe80",
            "@odata.type": "#EventDestination.v1_6_0.EventDestination",
            "Context": "RedfishEvent",
            "DeliveryRetryPolicy": "RetryForever",
            "Description": "Event Subscription Details",
            "Destination": "https://XX.XX.XX.XX:8189",
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
            "Destination": PARAM_DESTINATION,
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

        mocker.patch(MODULE_PATH + 'redfish_event_subscription.get_subscription_details',
                     side_effect=[json_data1, json_data2])

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

    @pytest.mark.parametrize("val", [
        {"destination": PARAM_DESTINATION, "event_type": "MetricReport",
         "event_format_type": "MetricReport"},
        {"destination": PARAM_DESTINATION, "event_type": "Alert", "event_format_type": "Event"}])
    def test_function_create_subscription(self, mocker, redfish_connection_mock, redfish_response_mock,
                                          redfish_default_args, val):
        redfish_default_args.update({"state": "absent"})
        redfish_default_args.update({"destination": val["destination"]})
        redfish_default_args.update({"event_type": val["event_type"]})
        redfish_default_args.update({"event_format_type": val["event_format_type"]})

        redfish_response_mock.json_data = {
            "Id": "c6ff37fc-8204-11eb-b08f-2cea7ff7fe80",
            "Destination": val["destination"],
            "EventFormatType": val["event_format_type"],
            "Context": "RedfishEvent",
            "Protocol": "Redfish",
            "EventTypes": [val["event_type"]],
            "SubscriptionType": "RedfishEvent"
        }
        redfish_response_mock.success = True
        f_module = self.get_module_mock(params=redfish_default_args)
        result = self.module.create_subscription(redfish_connection_mock, f_module)
        assert result.json_data["Destination"] == val["destination"]
        assert result.json_data["EventFormatType"] == val["event_format_type"]
        assert result.json_data["EventTypes"] == [val["event_type"]]

    @pytest.mark.parametrize("val", [
        {"destination": "https://XX.XX.XX.XX:161", "event_type": "MetricReport",
         "event_format_type": "MetricReport"},
        {"destination": "https://XX.XX.XX.XX:161", "event_type": "Alert", "event_format_type": "Event"}])
    def test_function_get_subscription_details(self, mocker, redfish_connection_mock, redfish_response_mock,
                                               redfish_default_args, val):
        redfish_default_args.update({"state": "absent"})
        redfish_default_args.update({"destination": val["destination"]})
        redfish_default_args.update({"event_type": val["event_type"]})
        redfish_default_args.update({"event_format_type": val["event_format_type"]})

        redfish_response_mock.json_data = {
            "@odata.context": "/redfish/v1/$metadata#EventDestination.EventDestination",
            "@odata.id": "/redfish/v1/EventService/Subscriptions/087b9026-0afa-11ec-8120-4cd98f5fc5a6",
            "@odata.type": "#EventDestination.v1_9_0.EventDestination",
            "Actions": {
                "#EventDestination.ResumeSubscription": {
                    "target": "/redfish/v1/EventService/Subscriptions/087b9026-0afa-11ec-8120-4cd98f5fc5a6/Actions/EventDestination.ResumeSubscription"
                }
            },
            "Context": "RedfishEvent",
            "DeliveryRetryPolicy": "RetryForever",
            "Description": "Event Subscription Details",
            "Destination": val['destination'],
            "EventFormatType": val["event_format_type"],
            "EventTypes": [val["event_type"]],
            "EventTypes@odata.count": 1,
            "HttpHeaders": [],
            "HttpHeaders@odata.count": 0,
            "Id": "087b9026-0afa-11ec-8120-4cd98f5fc5a6",
            "Name": "EventSubscription 087b9026-0afa-11ec-8120-4cd98f5fc5a6",
            "Protocol": "Redfish",
            "Status": {
                "Health": "OK",
                "HealthRollup": "OK",
                "State": "Enabled"
            },
            "SubscriptionType": "RedfishEvent"
        }
        redfish_response_mock.success = True
        result = self.module.get_subscription_details(redfish_connection_mock, "c6ff37fc-8204-11eb-b08f-2cea7ff7fe80")
        assert result["Destination"] == val["destination"]
        assert result["EventFormatType"] == val["event_format_type"]
        assert result["EventTypes"] == [val["event_type"]]

    @pytest.mark.parametrize("val", [
        {"destination": "https://XX.XX.XX.XX:161", "event_type": "MetricReport",
         "event_format_type": "MetricReport"},
        {"destination": "https://XX.XX.XX.XX:161", "event_type": "Alert", "event_format_type": "Event"}])
    def test_function_get_subscription_details_None(self, mocker, redfish_connection_mock, redfish_response_mock,
                                                    redfish_default_args, val):
        redfish_default_args.update({"state": "absent"})
        redfish_default_args.update({"destination": val["destination"]})
        redfish_default_args.update({"event_type": val["event_type"]})
        redfish_default_args.update({"event_format_type": val["event_format_type"]})

        redfish_response_mock.json_data = {
            "@odata.context": "/redfish/v1/$metadata#EventDestination.EventDestination",
            "@odata.id": "/redfish/v1/EventService/Subscriptions/087b9026-0afa-11ec-8120-4cd98f5fc5a6",
            "@odata.type": "#EventDestination.v1_9_0.EventDestination",
            "Actions": {
                "#EventDestination.ResumeSubscription": {
                    "target": "/redfish/v1/EventService/Subscriptions/087b9026-0afa-11ec-8120-4cd98f5fc5a6/Actions/EventDestination.ResumeSubscription"
                }
            },
            "Context": "RedfishEvent",
            "DeliveryRetryPolicy": "RetryForever",
            "Description": "Event Subscription Details",
            "Destination": val['destination'],
            "EventFormatType": val["event_format_type"],
            "EventTypes": [val["event_type"]],
            "EventTypes@odata.count": 1,
            "HttpHeaders": [],
            "HttpHeaders@odata.count": 0,
            "Id": "087b9026-0afa-11ec-8120-4cd98f5fc5a6",
            "Name": "EventSubscription 087b9026-0afa-11ec-8120-4cd98f5fc5a6",
            "Protocol": "Redfish",
            "Status": {
                "Health": "OK",
                "HealthRollup": "OK",
                "State": "Enabled"
            },
            "SubscriptionType": "RedfishEvent"
        }
        redfish_response_mock.success = False
        result = self.module.get_subscription_details(redfish_connection_mock, "c6ff37fc-8204-11eb-b08f-2cea7ff7fe80")
        assert result is None

    @pytest.mark.parametrize("val", [
        {"destination": "https://XX.XX.XX.XX:161"},
        {"destination": "https://XX.XX.XX.XX:161"}])
    def test_function_delete_subscription(self, mocker, redfish_connection_mock, redfish_response_mock,
                                          redfish_default_args, val):
        redfish_default_args.update({"state": "absent"})
        redfish_default_args.update({"destination": val["destination"]})

        redfish_response_mock.json_data = {
            "@Message.ExtendedInfo": [
                {
                    "Message": "Successfully Completed Request",
                    "MessageArgs": [],
                    "MessageArgs@odata.count": 0,
                    "MessageId": "Base.1.7.Success",
                    "RelatedProperties": [],
                    "RelatedProperties@odata.count": 0,
                    "Resolution": "None",
                    "Severity": "OK"
                },
                {
                    "Message": "The operation successfully completed.",
                    "MessageArgs": [],
                    "MessageArgs@odata.count": 0,
                    "MessageId": "IDRAC.2.4.SYS413",
                    "RelatedProperties": [],
                    "RelatedProperties@odata.count": 0,
                    "Resolution": "No response action is required.",
                    "Severity": "Informational"
                }
            ]
        }
        redfish_response_mock.success = True
        result = self.module.delete_subscription(redfish_connection_mock, "c6ff37fc-8204-11eb-b08f-2cea7ff7fe80")
        assert result.json_data["@Message.ExtendedInfo"][0]["Message"] == "Successfully Completed Request"
        assert result.json_data["@Message.ExtendedInfo"][1]["Message"] == "The operation successfully completed."

    def test_module_validation_input_params(self, mocker, redfish_connection_mock, redfish_response_mock,
                                            redfish_default_args):
        redfish_default_args.update({"state": "absent"})
        http_str = "http"
        redfish_default_args.update({"destination": http_str + "://XX.XX.XX.XX:8188"})
        redfish_default_args.update({"event_type": "MetricReport"})
        redfish_default_args.update({"event_format_type": "MetricReport"})
        with pytest.raises(Exception) as err:
            self._run_module(redfish_default_args)
        assert err.value.args[0]['msg'] == DESTINATION_INVALID

    def test_module_absent_does_not_exist(self, mocker, redfish_connection_mock, redfish_response_mock,
                                          redfish_default_args):
        redfish_default_args.update({"state": "absent"})
        redfish_default_args.update({"destination": PARAM_DESTINATION})
        redfish_default_args.update({"event_type": "MetricReport"})
        redfish_default_args.update({"event_format_type": "MetricReport"})

        redfish_connection_mock.patch(
            MODULE_PATH + 'redfish_event_subscription.get_subscription', return_value=None)
        redfish_response_mock.success = True
        result = self._run_module(redfish_default_args)
        assert result["msg"] == DESTINATION_MISMATCH

    def test_module_absent_does_exist(self, mocker, redfish_connection_mock, redfish_response_mock,
                                      redfish_default_args):
        redfish_default_args.update({"state": "absent"})
        redfish_default_args.update({"destination": PARAM_DESTINATION})
        redfish_default_args.update({"event_type": "MetricReport"})
        redfish_default_args.update({"event_format_type": "MetricReport"})

        json_data = {
            "Id": "c6ff37fc-8204-11eb-b08f-2cea7ff7fe80",
            "Destination": PARAM_DESTINATION,
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
        assert result["msg"] == SUBSCRIPTION_DELETED

    def test_module_absent_does_exist_error(self, mocker, redfish_connection_mock, redfish_response_mock,
                                            redfish_default_args):
        redfish_default_args.update({"state": "absent"})
        redfish_default_args.update({"destination": PARAM_DESTINATION})
        redfish_default_args.update({"event_type": "MetricReport"})
        redfish_default_args.update({"event_format_type": "MetricReport"})

        json_data = {
            "Id": "c6ff37fc-8204-11eb-b08f-2cea7ff7fe80",
            "Destination": PARAM_DESTINATION,
            "EventFormatType": "MetricReport",
            "Context": "RedfishEvent",
            "Protocol": "Redfish",
            "EventTypes": ["MetricReport"],
            "SubscriptionType": "RedfishEvent"
        }
        redfish_response_mock.success = False
        mocker.patch(MODULE_PATH + 'redfish_event_subscription.get_subscription', return_value=json_data)
        mocker.patch(MODULE_PATH + 'redfish_event_subscription.delete_subscription', return_value=redfish_response_mock)
        with pytest.raises(Exception) as err:
            self._run_module(redfish_default_args)
        assert err.value.args[0]['msg'] == SUBSCRIPTION_UNABLE_DEL

    def test_module_present_does_not_exist(self, mocker, redfish_connection_mock, redfish_response_mock,
                                           redfish_default_args):
        redfish_default_args.update({"state": "present"})
        redfish_default_args.update({"destination": PARAM_DESTINATION})
        redfish_default_args.update({"event_type": "MetricReport"})
        redfish_default_args.update({"event_format_type": "MetricReport"})

        json_data = {
            "Destination": PARAM_DESTINATION,
            "EventFormatType": "MetricReport",
            "Context": "RedfishEvent",
            "Protocol": "Redfish",
            "EventTypes": ["MetricReport"],
            "SubscriptionType": "RedfishEvent"
        }
        mocker.patch(MODULE_PATH + 'redfish_event_subscription.get_subscription', return_value=None)
        create_subscription_response_mock = redfish_response_mock
        create_subscription_response_mock.json_data = json_data
        mocker.patch(MODULE_PATH + 'redfish_event_subscription.create_subscription',
                     return_value=create_subscription_response_mock)
        f_module = self.get_module_mock()
        redfish_response_mock.success = True
        result = self._run_module(redfish_default_args)
        print(result)
        assert result["msg"] == SUBSCRIPTION_ADDED

    def test_module_present_does_not_exist_error(self, mocker, redfish_connection_mock, redfish_response_mock,
                                                 redfish_default_args):
        redfish_default_args.update({"state": "present"})
        redfish_default_args.update({"destination": PARAM_DESTINATION})
        redfish_default_args.update({"event_type": "MetricReport"})
        redfish_default_args.update({"event_format_type": "MetricReport"})

        json_data = {
            "Destination": PARAM_DESTINATION,
            "EventFormatType": "MetricReport",
            "Context": "RedfishEvent",
            "Protocol": "Redfish",
            "EventTypes": ["MetricReport"],
            "SubscriptionType": "RedfishEvent"
        }
        mocker.patch(MODULE_PATH + 'redfish_event_subscription.get_subscription', return_value=None)
        create_subscription_response_mock = redfish_response_mock
        create_subscription_response_mock.json_data = json_data
        mocker.patch(MODULE_PATH + 'redfish_event_subscription.create_subscription',
                     return_value=create_subscription_response_mock)
        redfish_response_mock.success = False
        with pytest.raises(Exception) as err:
            self._run_module(redfish_default_args)
        assert err.value.args[0]['msg'] == SUBSCRIPTION_UNABLE_ADD

    def test_module_present_does_not_exist_error_wrong_input(self, mocker, redfish_connection_mock,
                                                             redfish_response_mock,
                                                             redfish_default_args):
        redfish_default_args.update({"state": "present"})
        redfish_default_args.update({"destination": PARAM_DESTINATION})
        redfish_default_args.update({"event_type": "Metricreport"})
        redfish_default_args.update({"event_format_type": "MetricReport"})

        json_data = {
            "Destination": PARAM_DESTINATION,
            "EventFormatType": "MetricReport",
            "Context": "RedfishEvent",
            "Protocol": "Redfish",
            "EventTypes": ["MetricReport"],
            "SubscriptionType": "RedfishEvent"
        }
        mocker.patch(MODULE_PATH + 'redfish_event_subscription.get_subscription', return_value=None)
        create_subscription_response_mock = redfish_response_mock
        create_subscription_response_mock.json_data = json_data
        mocker.patch(MODULE_PATH + 'redfish_event_subscription.create_subscription',
                     return_value=create_subscription_response_mock)
        f_module = self.get_module_mock()
        redfish_response_mock.success = True
        with pytest.raises(Exception) as err:
            self._run_module(redfish_default_args)
        print(err)
        assert err.value.args[0]['msg'] == EVENT_TYPE_INVALID

    def test_module_present_does_exist(self, mocker, redfish_connection_mock, redfish_response_mock,
                                       redfish_default_args):
        redfish_default_args.update({"state": "present"})
        redfish_default_args.update({"destination": PARAM_DESTINATION})
        redfish_default_args.update({"event_type": "MetricReport"})
        redfish_default_args.update({"event_format_type": "MetricReport"})

        json_data = {
            "Id": "c6ff37fc-8204-11eb-b08f-2cea7ff7fe80",
            "Destination": PARAM_DESTINATION,
            "EventFormatType": "MetricReport",
            "Context": "RedfishEvent",
            "Protocol": "Redfish",
            "EventTypes": ["MetricReport"],
            "SubscriptionType": "RedfishEvent"
        }
        mocker.patch(MODULE_PATH + 'redfish_event_subscription.get_subscription', return_value=json_data)
        redfish_response_mock.success = True
        result = self._run_module(redfish_default_args)
        assert result["msg"] == SUBSCRIPTION_EXISTS
