.. _redfish_firmware_module:


redfish_firmware -- To perform a component firmware update using the image file available on the local or remote system
=======================================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows the firmware update of only one component at a time. If the module is run for more than one component, an error message is returned.

Depending on the component, the firmware update is applied after an automatic or manual reboot.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6
- urllib3



Parameters
----------

  image_uri (True, str, None)
    Firmware Image location URI or local path.

    For example- http://<web_address>/components.exe or /home/firmware_repo/component.exe.


  transfer_protocol (optional, str, HTTP)
    Protocol used to transfer the firmware image file. Applicable for URI based update.


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
   - Run this module from a system that has direct access to Redfish APIs.
   - This module does not support ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Update the firmware from a single executable file available in a HTTP protocol
      dellemc.openmanage.redfish_firmware:
        baseuri: "192.168.0.1"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        image_uri: "http://192.168.0.2/firmware_repo/component.exe"
        transfer_protocol: "HTTP"

    - name: Update the firmware from a single executable file available in a local path
      dellemc.openmanage.redfish_firmware:
        baseuri: "192.168.0.1"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        image_uri: "/home/firmware_repo/component.exe"



Return Values
-------------

msg (always, str, Successfully submitted the firmware update task.)
  Overall status of the firmware update task.


task (success, dict, {'id': 'JID_XXXXXXXXXXXX', 'uri': '/redfish/v1/TaskService/Tasks/JID_XXXXXXXXXXXX'})
  Returns ID and URI of the created task.


error_info (on http error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to complete the operation because the JSON data format entered is invalid.', 'Resolution': 'Do the following and the retry the operation: 1) Enter the correct JSON data format and retry the operation. 2) Make sure that no syntax error is present in JSON data format. 3) Make sure that a duplicate key is not present in JSON data format.', 'Severity': 'Critical'}, {'Message': 'The request body submitted was malformed JSON and could not be parsed by the receiving service.', 'Resolution': 'Ensure that the request body is valid JSON and resubmit the request.', 'Severity': 'Critical'}], 'code': 'Base.1.2.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.'}})
  Details of http error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)
- Shivam Sharma (@Shivam-Sharma)

