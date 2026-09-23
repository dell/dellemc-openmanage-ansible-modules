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

- python \>= 3.9.6
- urllib3



Parameters
----------

  image_uri (True, str, None)
    Firmware Image location URI or local path.

    For example- \ http://%3Cweb_address%3E/components.exe\  or /home/firmware\_repo/component.exe.


  transfer_protocol (optional, str, HTTP)
    Protocol used to transfer the firmware image file. Applicable for URI based update.


  job_wait (optional, bool, True)
    Provides the option to wait for job completion.


  job_wait_timeout (optional, int, 3600)
    The maximum wait time of \ :emphasis:`job\_wait`\  in seconds. The job is tracked only for this duration.

    This option is applicable when \ :emphasis:`job\_wait`\  is \ :literal:`true`\ .

    Note: If a firmware update needs a reboot, the job will get scheduled and waits for no of seconds specfied in \ :emphasis:`job\_wait\_time`\ . to reduce the wait time either give \ :emphasis:`job\_wait\_time`\  minimum or make \ :emphasis:`job\_wait`\ as false and retrigger.


  image_checksum (optional, dict, None)
    Optional checksum to verify a local firmware image before uploading.

    When specified, the module computes the digest of the local file and fails if it does not match.

    Not applicable for URI-based transfers (iDRAC fetches the image directly).

    \ :sub:`algorithm` (optional, str, sha256)
      Hash algorithm to use.

    \ :sub:`value` (True, str, None)
      Expected hex digest of the firmware image.


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


  cert_fingerprint (optional, str, None)
    SHA-256 fingerprint of the expected TLS certificate (hex digest, with or without colons).

    When supplied together with \ :literal:`validate\_certs=false`\ , the module verifies the remote certificate's fingerprint instead of performing full CA validation.


  enforce_validate_certs (optional, bool, False)
    If \ :literal:`true`\  and \ :literal:`validate\_certs`\  is \ :literal:`false`\ , the module will fail with an error instead of just emitting a warning.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Redfish APIs.
   - This module supports both IPv4 and IPv6 addresses.
   - This module supports only iDRAC9 and above.
   - This module does not support \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Update the firmware from a single executable file available over HTTPS (recommended)
      dellemc.openmanage.redfish_firmware:
        baseuri: "192.168.0.1"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        image_uri: "https://192.168.0.2/firmware_repo/component.exe"
        transfer_protocol: "HTTPS"

    - name: Update the firmware from a single executable file available in a HTTP protocol
      dellemc.openmanage.redfish_firmware:
        baseuri: "192.168.0.1"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        image_uri: "http://192.168.0.2/firmware_repo/component.exe"
        transfer_protocol: "HTTP"

    - name: Update the firmware from a single executable file available in a HTTP protocol with job_Wait
      dellemc.openmanage.redfish_firmware:
        baseuri: "192.168.0.1"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        image_uri: "http://192.168.0.2/firmware_repo/component.exe"
        transfer_protocol: "HTTP"
        job_wait: true
        job_wait_timeout: 600

    - name: Update the firmware from a single executable file available in a local path
      dellemc.openmanage.redfish_firmware:
        baseuri: "192.168.0.1"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        image_uri: "/home/firmware_repo/component.exe"

    - name: Update the firmware from a local file, verifying its checksum before upload
      dellemc.openmanage.redfish_firmware:
        baseuri: "192.168.0.1"
        username: "user_name"
        password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        image_uri: "/home/firmware_repo/component.exe"
        image_checksum:
          algorithm: "sha256"
          value: "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"



Return Values
-------------

msg (always, str, Successfully updated the firmware.)
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
- Husniya Hameed (@husniya_hameed)
- Shivam Sharma (@Shivam-Sharma)
- Kritika Bhateja (@Kritika_Bhateja)
- Abhishek Sinha (@ABHISHEK-SINHA10)

