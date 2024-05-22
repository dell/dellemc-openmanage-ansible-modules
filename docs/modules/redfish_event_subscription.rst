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

- python \>= 3.9.6



Parameters
----------

  destination (True, str, None)
    The HTTPS URI of the destination to send events.

    HTTPS is required.


  event_type (optional, str, Alert)
    Specifies the event type to be subscribed.

    \ :literal:`Alert`\  used to subscribe for alert.

    \ :literal:`MetricReport`\  used to subscribe for the metrics report.


  event_format_type (optional, str, Event)
    Specifies the format type of the event to be subscribed.

    \ :literal:`Event`\  used to subscribe for Event format type.

    \ :literal:`MetricReport`\  used to subscribe for the metrics report format type.


  state (optional, str, present)
    \ :literal:`present`\  adds new event subscription.

    \ :literal:`absent`\  deletes event subscription with the specified \ :emphasis:`destination`\ .


  baseuri (True, str, None)
    IP address of the target out-of-band controller. For example- \<ipaddress\>:\<port\>.


  username (False, str, None)
    Username of the target out-of-band controller.

    If the username is not provided, then the environment variable \ :envvar:`IDRAC\_USERNAME`\  is used.

    Example: export IDRAC\_USERNAME=username


  password (False, str, None)
    Password of the target out-of-band controller.

    If the password is not provided, then the environment variable \ :envvar:`IDRAC\_PASSWORD`\  is used.

    Example: export IDRAC\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`IDRAC\_X\_AUTH\_TOKEN`\  is used.

    Example: export IDRAC\_X\_AUTH\_TOKEN=x\_auth\_token


  validate_certs (optional, bool, True)
    If \ :literal:`false`\ , the SSL certificates will not be validated.

    Configure \ :literal:`false`\  only on personally controlled sites where self-signed certificates are used.

    Prior to collection version \ :literal:`5.0.0`\ , the \ :emphasis:`validate\_certs`\  is \ :literal:`false`\  by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - \ :emphasis:`event\_type`\  needs to be \ :literal:`MetricReport`\  and \ :emphasis:`event\_format\_type`\  needs to be \ :literal:`MetricReport`\  for metrics subscription.
   - \ :emphasis:`event\_type`\  needs to be \ :literal:`Alert`\  and \ :emphasis:`event\_format\_type`\  needs to be \ :literal:`Event`\  for event subscription.
   - Modifying a subscription is not supported.
   - Context is always set to RedfishEvent.
   - This module supports \ :literal:`check\_mode`\ .




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

