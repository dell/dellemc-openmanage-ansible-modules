.. _ome_powerstate_module:


ome_powerstate -- Performs the power management operations on OpenManage Enterprise
===================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module performs the supported power management operations on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  power_state (True, str, None)
    Desired end power state.


  device_service_tag (optional, str, None)
    Targeted device service tag.

    \ :emphasis:`device\_service\_tag`\  is mutually exclusive with \ :emphasis:`device\_id`\ .


  device_id (optional, int, None)
    Targeted device id.

    \ :emphasis:`device\_id`\  is mutually exclusive with \ :emphasis:`device\_service\_tag`\ .


  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (False, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.

    If the username is not provided, then the environment variable \ :envvar:`OME\_USERNAME`\  is used.

    Example: export OME\_USERNAME=username


  password (False, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.

    If the password is not provided, then the environment variable \ :envvar:`OME\_PASSWORD`\  is used.

    Example: export OME\_PASSWORD=password


  x_auth_token (False, str, None)
    Authentication token.

    If the x\_auth\_token is not provided, then the environment variable \ :envvar:`OME\_X\_AUTH\_TOKEN`\  is used.

    Example: export OME\_X\_AUTH\_TOKEN=x\_auth\_token


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.


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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Power state operation based on device id
      dellemc.openmanage.ome_powerstate:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_id: 11111
        power_state: "off"

    - name: Power state operation based on device service tag
      dellemc.openmanage.ome_powerstate:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_service_tag: "KLBR111"
        power_state: "on"

    - name: Power state operation based on list of device ids
      dellemc.openmanage.ome_powerstate:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_id: "{{ item.device_id }}"
        power_state: "{{ item.state }}"
      with_items:
        - { "device_id": 11111, "state": "on" }
        - { "device_id": 22222, "state": "off" }

    - name: Power state operation based on list of device service tags
      dellemc.openmanage.ome_powerstate:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        device_service_tag: "{{ item.service_tag }}"
        power_state: "{{ item.state }}"
      with_items:
        - { "service_tag": "KLBR111", "state": "on" }
        - { "service_tag": "KLBR222", "state": "off" }



Return Values
-------------

msg (always, str, Power State operation job submitted successfully.)
  Overall power state operation job status.


job_status (success, dict, {'Builtin': False, 'CreatedBy': 'user', 'Editable': True, 'EndTime': None, 'Id': 11111, 'JobDescription': 'DeviceAction_Task', 'JobName': 'DeviceAction_Task_PowerState', 'JobStatus': {'Id': 1111, 'Name': 'New'}, 'JobType': {'Id': 1, 'Internal': False, 'Name': 'DeviceAction_Task'}, 'LastRun': '2019-04-01 06:39:02.69', 'LastRunStatus': {'Id': 1112, 'Name': 'Running'}, 'NextRun': None, 'Params': [{'JobId': 11111, 'Key': 'powerState', 'Value': '2'}, {'JobId': 11111, 'Key': 'operationName', 'Value': 'POWER_CONTROL'}], 'Schedule': '', 'StartTime': None, 'State': 'Enabled', 'Targets': [{'Data': '', 'Id': 11112, 'JobId': 11111, 'TargetType': {'Id': 1000, 'Name': 'DEVICE'}}], 'UpdatedBy': None, 'Visible': True})
  Power state operation job and progress details from the OME.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)

