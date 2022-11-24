.. _redfish_event_subscription_module:


redfish_event_subscription -- Manage Redfish Subscriptions
==========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to add or delete Redfish Event subscriptions.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  destination (True, str, None)
    The HTTPS URI of the destination to send events.

    HTTPS is required.


  event_type (optional, str, Alert)
    Specifies the event type to be subscribed.

    ``Alert`` used to subscribe for alert.

    ``MetricReport`` used to subscribe for the metrics report.


  event_format_type (optional, str, Event)
    Specifies the format type of the event to be subscribed.

    ``Event`` used to subscribe for Event format type.

    ``MetricReport`` used to subscribe for the metrics report format type.


  state (optional, str, present)
    ``present`` adds new event subscription.

    ``absent`` deletes event subscription with the specified *destination*.


  baseuri (True, str, None)
    IP address of the target out-of-band controller. For example- <ipaddress>:<port>.


  username (True, str, None)
    Username of the target out-of-band controller.


  password (True, str, None)
    Password of the target out-of-band controller.


  validate_certs (optional, bool, True)
    If ``False``, the SSL certificates will not be validated.

    Configure ``False`` only on personally controlled sites where self-signed certificates are used.

    Prior to collection version ``5.0.0``, the *validate_certs* is ``False`` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - *event_type* needs to be ``MetricReport`` and *event_format_type* needs to be ``MetricReport`` for metrics subscription.
   - *event_type* needs to be ``Alert`` and *event_format_type* needs to be ``Event`` for event subscription.
   - Modifying a subscription is not supported.
   - Context is always set to RedfishEvent.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
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



Return Values
-------------

msg (always, str, Successfully added the subscription.)
  Overall status of the task.


status (on adding subscription successfully, dict, {'@Message.ExtendedInfo': [{'Message': 'The resource has been created successfully', 'MessageArgs': [], 'MessageArgs@odata.count': 0, 'MessageId': 'Base.1.7.Created', 'RelatedProperties': [], 'RelatedProperties@odata.count': 0, 'Resolution': 'None', 'Severity': 'OK'}, {'Message': 'A new resource is successfully created.', 'MessageArgs': [], 'MessageArgs@odata.count': 0, 'MessageId': 'IDRAC.2.2.SYS414', 'RelatedProperties': [], 'RelatedProperties@odata.count': 0, 'Resolution': 'No response action is required.', 'Severity': 'Informational'}], 'Actions': {'#EventDestination.ResumeSubscription': {'target': '/redfish/v1/EventService/Subscriptions/5d432f36-81f4-11eb-9dc0-2cea7ff7ff9a/Actions/EventDestination.ResumeSubscription'}}, 'Context': 'RedfishEvent', 'DeliveryRetryPolicy': 'RetryForever', 'Description': 'Event Subscription Details', 'Destination': 'https://192.168.1.100:8188', 'EventFormatType': 'Event', 'EventTypes': ['Alert'], 'EventTypes@odata.count': 1, 'HttpHeaders': [], 'HttpHeaders@odata.count': 0, 'Id': '5d432f36-81f4-11eb-9dc0-2cea7ff7ff9a', 'MetricReportDefinitions': [], 'MetricReportDefinitions@odata.count': 0, 'Name': 'EventSubscription 5d432f36-81f4-11eb-9dc0-2cea7ff7ff9a', 'OriginResources': [], 'OriginResources@odata.count': 0, 'Protocol': 'Redfish', 'Status': {'Health': 'OK', 'HealthRollup': 'OK', 'State': 'Enabled'}, 'SubscriptionType': 'RedfishEvent'})
  Returns subscription object created


error_info (on http error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to complete the operation because the JSON data format entered is invalid.', 'Resolution': 'Do the following and the retry the operation: 1) Enter the correct JSON data format and retry the operation. 2) Make sure that no syntax error is present in JSON data format. 3) Make sure that a duplicate key is not present in JSON data format.', 'Severity': 'Critical'}, {'Message': 'The request body submitted was malformed JSON and could not be parsed by the receiving service.', 'Resolution': 'Ensure that the request body is valid JSON and resubmit the request.', 'Severity': 'Critical'}], 'code': 'Base.1.2.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.'}})
  Details of http error.





Status
------





Authors
~~~~~~~

- Trevor Squillario (@TrevorSquillario)
- Sachin Apagundi (@sachin-apa)

