#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.3.0
# Copyright (C) 2021-2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+
# see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: redfish_event_subscription
short_description: Manage Redfish Subscriptions
version_added: "4.1.0"
description:
    This module allows to add or delete Redfish Event subscriptions.
extends_documentation_fragment:
  - dellemc.openmanage.redfish_auth_options
options:
    destination:
        description:
          - The HTTPS URI of the destination to send events.
          - HTTPS is required.
        type: str
        required: true
    event_type:
        description:
          - Specifies the event type to be subscribed.
          - C(Alert) used to subscribe for alert.
          - C(MetricReport) used to subscribe for the metrics report.
        type: str
        default: Alert
        choices: [Alert, MetricReport]
    event_format_type:
        description:
          - Specifies the format type of the event to be subscribed.
          - C(Event) used to subscribe for Event format type.
          - C(MetricReport) used to subscribe for the metrics report format type.
        type: str
        default: Event
        choices: [Event, MetricReport]
    state:
        description:
          - C(present) adds new event subscription.
          - C(absent) deletes event subscription with the specified I(destination).
        type: str
        default: present
        choices: ["present", "absent"]
requirements:
    - "python >= 3.9.6"
author:
    - "Trevor Squillario (@TrevorSquillario)"
    - "Sachin Apagundi (@sachin-apa)"
notes:
    - I(event_type) needs to be C(MetricReport) and I(event_format_type) needs to be C(MetricReport) for metrics
      subscription.
    - I(event_type) needs to be C(Alert) and I(event_format_type) needs to be C(Event) for event subscription.
    - Modifying a subscription is not supported.
    - Context is always set to RedfishEvent.
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Add Redfish metric subscription
  redfish_event_subscription:
    baseuri: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    destination: "https://192.168.1.100:8188"
    event_type: MetricReport
    event_format_type: MetricReport
    state: present

- name: Add Redfish alert subscription
  redfish_event_subscription:
    baseuri: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    destination: "https://server01.example.com:8188"
    event_type: Alert
    event_format_type: Event
    state: present

- name: Delete Redfish subscription with a specified destination
  redfish_event_subscription:
    baseuri: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    ca_path: "/path/to/ca_cert.pem"
    destination: "https://server01.example.com:8188"
    state: absent
"""

RETURN = """
---
msg:
  description: Overall status of the task.
  returned: always
  type: str
  sample: Successfully added the subscription.
status:
  description: Returns subscription object created
  returned: on adding subscription successfully
  type: dict
  sample: {
        "@Message.ExtendedInfo": [
            {
                "Message": "The resource has been created successfully",
                "MessageArgs": [],
                "MessageArgs@odata.count": 0,
                "MessageId": "Base.1.7.Created",
                "RelatedProperties": [],
                "RelatedProperties@odata.count": 0,
                "Resolution": "None",
                "Severity": "OK"
            },
            {
                "Message": "A new resource is successfully created.",
                "MessageArgs": [],
                "MessageArgs@odata.count": 0,
                "MessageId": "IDRAC.2.2.SYS414",
                "RelatedProperties": [],
                "RelatedProperties@odata.count": 0,
                "Resolution": "No response action is required.",
                "Severity": "Informational"
            }
        ],
        "Actions": {
            "#EventDestination.ResumeSubscription": {
                "target": "/redfish/v1/EventService/Subscriptions/5d432f36-81f4-11eb-9dc0-2cea7ff7ff9a/Actions/EventDestination.ResumeSubscription"
            }
        },
        "Context": "RedfishEvent",
        "DeliveryRetryPolicy": "RetryForever",
        "Description": "Event Subscription Details",
        "Destination": "https://192.168.1.100:8188",
        "EventFormatType": "Event",
        "EventTypes": [
            "Alert"
        ],
        "EventTypes@odata.count": 1,
        "HttpHeaders": [],
        "HttpHeaders@odata.count": 0,
        "Id": "5d432f36-81f4-11eb-9dc0-2cea7ff7ff9a",
        "MetricReportDefinitions": [],
        "MetricReportDefinitions@odata.count": 0,
        "Name": "EventSubscription 5d432f36-81f4-11eb-9dc0-2cea7ff7ff9a",
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
error_info:
  type: dict
  description: Details of http error.
  returned: on http error
  sample:  {
        "error": {
            "@Message.ExtendedInfo": [
                {
                    "Message": "Unable to complete the operation because the JSON data format entered is invalid.",
                    "Resolution": "Do the following and the retry the operation:
                        1) Enter the correct JSON data format and retry the operation.
                        2) Make sure that no syntax error is present in JSON data format.
                        3) Make sure that a duplicate key is not present in JSON data format.",
                    "Severity": "Critical"
                },
                {
                    "Message": "The request body submitted was malformed JSON and
                        could not be parsed by the receiving service.",
                    "Resolution": "Ensure that the request body is valid JSON and resubmit the request.",
                    "Severity": "Critical"
                }
            ],
            "code": "Base.1.2.GeneralError",
            "message": "A general error has occurred. See ExtendedInfo for more information."
        }
    }
"""

import json
import os
from ssl import SSLError
from ansible_collections.dellemc.openmanage.plugins.module_utils.redfish import Redfish, RedfishAnsibleModule
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError

DESTINATION_INVALID = "The Parameter destination must have an HTTPS destination. The HTTP destination is not allowed"
SUBSCRIPTION_EXISTS = "No changes found to be applied."
SUBSCRIPTION_DELETED = "Successfully deleted the subscription."
SUBSCRIPTION_UNABLE_DEL = "Unable to delete the subscription."
SUBSCRIPTION_UNABLE_ADD = "Unable to add a subscription."
SUBSCRIPTION_ADDED = "Successfully added the subscription."
DESTINATION_MISMATCH = "No changes found to be applied."
CHANGES_FOUND = "Changes found to be applied."


def get_subscription_payload():
    payload = {
        "Destination": "https://192.168.1.100:8188",
        "EventFormatType": "MetricReport",
        "Context": "RedfishEvent",
        "Protocol": "Redfish",
        "EventTypes": ["MetricReport"],
        "SubscriptionType": "RedfishEvent"
    }
    return payload


def get_subscription(obj, destination):
    url = "{0}{1}".format(obj.root_uri, "EventService/Subscriptions")
    list_resp = obj.invoke_request("GET", url)
    list_subscriptions = list_resp.json_data["Members"]
    for list_subscription in list_subscriptions:
        id = os.path.basename(list_subscription.get('@odata.id'))
        detail_json = get_subscription_details(obj, id)
        subscription = get_subscription_payload()
        if detail_json and detail_json["Destination"] == destination:
            subscription["Id"] = detail_json["Id"]
            subscription["Destination"] = detail_json["Destination"]
            subscription["EventFormatType"] = detail_json["EventFormatType"]
            subscription["Context"] = detail_json["Context"]
            subscription["Protocol"] = detail_json["Protocol"]
            subscription["EventTypes"] = detail_json["EventTypes"]
            subscription["SubscriptionType"] = detail_json["SubscriptionType"]
            return subscription
    return None


def get_subscription_details(obj, id):
    detail_url = "{0}{1}".format(obj.root_uri, "EventService/Subscriptions/%s" % id)
    detail_resp = obj.invoke_request("GET", detail_url)
    detail_json = detail_resp.json_data
    if detail_resp.success:
        return detail_json
    else:
        return None


def create_subscription(obj, module):
    payload = get_subscription_payload()
    payload["Destination"] = module.params["destination"]
    payload["EventFormatType"] = module.params["event_format_type"]
    payload["EventTypes"] = [module.params["event_type"]]
    if module.check_mode:
        module.exit_json(changed=True, msg=CHANGES_FOUND)
    resp = obj.invoke_request("POST", "{0}{1}".format(obj.root_uri, "EventService/Subscriptions"), data=payload)
    return resp


def delete_subscription(obj, id):
    resp = obj.invoke_request("DELETE", "{0}{1}".format(obj.root_uri, "EventService/Subscriptions/%s" % id))
    return resp


def _validate_inputs(module):
    """validates that destination has https instead of http"""
    inp_destination = module.params['destination']
    if not inp_destination.startswith("https"):
        module.fail_json(msg=DESTINATION_INVALID)


def _get_formatted_payload(obj, existing_payload):
    """get the payload after removing unwanted tags"""
    existing_payload = obj.strip_substr_dict(existing_payload)
    return existing_payload


def main():
    specs = {
        "destination": {"required": True, "type": "str"},
        "event_type": {"type": "str", "default": "Alert", "choices": ['Alert', 'MetricReport']},
        "event_format_type": {"type": "str", "default": "Event",
                              "choices": ['Event', 'MetricReport']},
        "state": {"type": "str", "default": "present", "choices": ['present', 'absent']},
    }

    module = RedfishAnsibleModule(
        argument_spec=specs,
        supports_check_mode=True)

    try:
        _validate_inputs(module)
        with Redfish(module.params, req_session=True) as obj:
            subscription = get_subscription(obj, module.params["destination"])
            if subscription:
                if module.params["state"] == "present":
                    module.exit_json(msg=SUBSCRIPTION_EXISTS, changed=False)
                else:
                    if module.check_mode:
                        module.exit_json(changed=True, msg=CHANGES_FOUND)
                    delete_resp = delete_subscription(obj, subscription["Id"])
                    if delete_resp.success:
                        module.exit_json(msg=SUBSCRIPTION_DELETED, changed=True)
                    else:
                        module.fail_json(msg=SUBSCRIPTION_UNABLE_DEL)
            else:
                if module.params["state"] == "present":
                    create_resp = create_subscription(obj, module)
                    if create_resp.success:
                        module.exit_json(msg=SUBSCRIPTION_ADDED, changed=True,
                                         status=_get_formatted_payload(obj, create_resp.json_data))
                    else:
                        module.fail_json(msg=SUBSCRIPTION_UNABLE_ADD)
                else:
                    module.exit_json(msg=DESTINATION_MISMATCH, changed=False)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, URLError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError, IOError, AssertionError, OSError, SSLError) as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
