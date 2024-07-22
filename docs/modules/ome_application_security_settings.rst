.. _ome_application_security_settings_module:


ome_application_security_settings -- Configure the login security properties
============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows you to configure the login security properties on OpenManage Enterprise or OpenManage Enterprise Modular



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  restrict_allowed_ip_range (optional, dict, None)
    Restrict to allow inbound connections only from the specified IP address range.

    This is mutually exclusive with \ :emphasis:`fips\_mode\_enable`\ .

    \ :literal:`NOTE`\  When \ :emphasis:`restrict\_allowed\_ip\_range`\  is configured on the appliance, any inbound connection to the appliance, such as alert reception, firmware update, and network identities are blocked from the devices that are outside the specified IP address range. However, any outbound connection from the appliance will work on all devices.


    enable_ip_range (True, bool, None)
      Allow connections based on the IP address range.


    ip_range (optional, str, None)
      The IP address range in Classless Inter-Domain Routing (CIDR) format. For example: 192.168.100.14/24 or 2001:db8::/24



  login_lockout_policy (optional, dict, None)
    Locks the application after multiple unsuccessful login attempts.

    This is mutually exclusive with \ :emphasis:`fips\_mode\_enable`\ .


    by_user_name (optional, bool, None)
      Enable or disable lockout policy settings based on the user name. This restricts the number of unsuccessful login attempts from a specific user for a specific time interval.


    by_ip_address (optional, bool, None)
      Enable or disable lockout policy settings based on the IP address. This restricts the number of unsuccessful login attempts from a specific IP address for a specific time interval.


    lockout_fail_count (optional, int, None)
      The number of unsuccessful login attempts that are allowed after which the appliance prevents log in from the specific  username or IP Address.


    lockout_fail_window (optional, int, None)
      Lockout fail window is the time in seconds within which the lockout fail count event must occur to trigger the lockout penalty time. Enter the duration for which OpenManage Enterprise must display information about a failed attempt.


    lockout_penalty_time (optional, int, None)
      The duration of time, in seconds, that login attempts from the specific user or IP address must not be allowed.



  job_wait (optional, bool, True)
    Provides an option to wait for job completion.


  job_wait_timeout (optional, int, 120)
    The maximum wait time of \ :emphasis:`job\_wait`\  in seconds. The job is tracked only for this duration.

    This option is applicable when \ :emphasis:`job\_wait`\  is \ :literal:`true`\ .


  fips_mode_enable (optional, bool, None)
    The FIPS mode is intended to meet the requirements of FIPS 140-2 level 1. For more information refer to the FIPS user guide

    This is applicable only for OpenManage Enterprise Modular only

    This is mutually exclusive with \ :emphasis:`restrict\_allowed\_ip\_range`\  and \ :emphasis:`login\_lockout\_policy`\ .

    \ :literal:`WARNING`\  Enabling or Disabling this option resets your chassis to default settings. This may cause change in IP settings and loss of network connectivity.

    \ :literal:`WARNING`\  The FIPS mode cannot be enabled on a lead chassis in a multi-chassis management configuration. To toggle enable FIPS on a lead chassis, delete the chassis group, enable FIPS and recreate the group.

    \ :literal:`WARNING`\  For a Standalone or member chassis, enabling the FIPS mode deletes any fabrics created. This may cause loss of network connectivity and data paths to the compute sleds.


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
   - Run this module from a system that has direct access to Dell OpenManage Enterprise or OpenManage Enterprise Modular.
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Configure restricted allowed IP range
      dellemc.openmanage.ome_application_security_settings:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        restrict_allowed_ip_range:
          enable_ip_range: true
          ip_range: 192.1.2.3/24

    - name: Configure login lockout policy
      dellemc.openmanage.ome_application_security_settings:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        login_lockout_policy:
          by_user_name: true
          by_ip_address: true
          lockout_fail_count: 3
          lockout_fail_window: 30
          lockout_penalty_time: 900

    - name: Configure restricted allowed IP range and login lockout policy with job wait time out of 60 seconds
      dellemc.openmanage.ome_application_security_settings:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        restrict_allowed_ip_range:
          enable_ip_range: true
          ip_range: 192.1.2.3/24
        login_lockout_policy:
          by_user_name: true
          by_ip_address: true
          lockout_fail_count: 3
          lockout_fail_window: 30
          lockout_penalty_time: 900
        job_wait_timeout: 60

    - name: Enable FIPS mode
      dellemc.openmanage.ome_application_security_settings:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        fips_mode_enable: true



Return Values
-------------

msg (always, str, Successfully applied the security settings.)
  Overall status of the login security configuration.


job_id (When security configuration properties are provided, int, 10123)
  Job ID of the security configuration task.


error_info (on http error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to process the request because the domain information cannot be retrieved.', 'MessageArgs': [], 'MessageId': 'CGEN8007', 'RelatedProperties': [], 'Resolution': 'Verify the status of the database and domain configuration, and then retry the operation.', 'Severity': 'Critical'}], 'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.'}})
  Details of http error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

