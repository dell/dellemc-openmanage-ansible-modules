#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 3.0.1
# Copyright (C) 2019 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+
# see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r"""
---
module: redfish_event_subscription
short_description: Manage Redfish Subscriptions
version_added: "3.3.0"
description: >
    This module allows you to create or delete Redfish Subscriptions.
    HTTPS is required for the destination listening server. Example: Logstash HTTP Input Plugin.
    The maximum number of subscriptions a user can create is 2.
options:
    baseuri:
        description: "IP Address of the target out-of-band controller."
        type: str
        required: True
    username:
        description: Username of the target out-of-band controller.
        type: str
        required: True
    password:
        description: Password of the target out of-band controller.
        type: str
        required: True
    destination:
        description:
            - URL of server that is listening for events.
            - HTTPS is required.
            - The maximum number of subscriptions a user can create is 2.
        type: str
        required: True
    type:
        description: Type of Redfish subscription to create.
        type: str
        default: metric
        choices: ["metric", "alert"]
        required: False
    state:
        description: Whether the subscription should exist or not.
        type: str
        default: present
        choices: ["present", "absent"]
        required: False
requirements:
    - "python >= 2.7.5"
author:
    - "Trevor Squillario (@TrevorSquillario)"
"""

EXAMPLES = """
---
- name: Create redfish metric subscription
  redfish_event_subscription:
    baseuri: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    destination: "https://192.168.1.100:8188"
    type: metric
    state: present

- name: Create redfish alert subscription
  redfish_event_subscription:
    baseuri: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    destination: "https://server01.example.com:8188"
    type: alert
    state: present

- name: Delete redfish subscription
  redfish_event_subscription:
    baseuri: "192.168.0.1"
    username: "user_name"
    password: "user_password"
    destination: "https://server01.example.com:8188"
    state: absent
"""

RETURN = """
---
msg:
  description: Overall status of the task.
  returned: always
  type: str
  sample: Successfully submitted the task.
status:
  description: Returns subscription object createdq
  returned: success
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
        "@odata.context": "/redfish/v1/$metadata#EventDestination.EventDestination",
        "@odata.id": "/redfish/v1/EventService/Subscriptions/5d432f36-81f4-11eb-9dc0-2cea7ff7ff9a",
        "@odata.type": "#EventDestination.v1_9_0.EventDestination",
        "Actions": {
            "#EventDestination.ResumeSubscription": {
                "target": "/redfish/v1/EventService/Subscriptions/5d432f36-81f4-11eb-9dc0-2cea7ff7ff9a/Actions/EventDestination.ResumeSubscription"
            }
        },
        "Context": "RedfishEvent",
        "DeliveryRetryPolicy": "RetryForever",
        "Description": "Event Subscription Details",
        "Destination": "https://100.77.11.5:8189",
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
from ansible_collections.dellemc.openmanage.plugins.module_utils.redfish import Redfish
from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError


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
    if module.params["type"] == "metric":
        payload["EventFormatType"] = "MetricReport"
        payload["EventTypes"] = ["MetricReport"]
    if module.params["type"] == "alert":
        payload["EventFormatType"] = "Event"
        payload["EventTypes"] = ["Alert"]
    resp = obj.invoke_request("POST", "{0}{1}".format(obj.root_uri, "EventService/Subscriptions"), data=payload)
    return resp


def delete_subscription(obj, id):
    resp = obj.invoke_request("DELETE", "{0}{1}".format(obj.root_uri, "EventService/Subscriptions/%s" % id))
    return resp


def main():
    module = AnsibleModule(
        argument_spec={
            "baseuri": {"required": True, "type": "str"},
            "username": {"required": True, "type": "str"},
            "password": {"required": True, "type": "str", "no_log": True},
            "destination": {"required": True, "type": "str"},
            "type": {
                "required": False,
                "type": "str",
                "default": "metric",
                "choices": ["alert", "metric"]},
            "state": {
                "required": False,
                "default": "present",
                "choices": ['present', 'absent']},
        },
        supports_check_mode=False)
    try:
        with Redfish(module.params, req_session=True) as obj:
            subscription = get_subscription(obj, module.params["destination"])
            if subscription:
                if module.params["state"] == "present":
                    module.exit_json(msg="Subscription exists. No changes made.", changed=False)
                if module.params["state"] == "absent":
                    delete_resp = delete_subscription(obj, subscription["Id"])
                    if delete_resp.success:
                        module.exit_json(msg="Successfully deleted subscription.", changed=True)
                    else:
                        module.exit_json(msg="Module failed.", changed=True)
            else:
                if module.params["state"] == "present":
                    create_resp = create_subscription(obj, module)
                    if create_resp.success:
                        module.exit_json(msg="Successfully created subscription.", changed=True, status=create_resp.json_data)
                    else:
                        module.exit_json(msg="Module failed.", changed=True)
                else:
                    module.exit_json(msg="No changes made.", changed=False)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except (RuntimeError, URLError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError, IOError, AssertionError) as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
