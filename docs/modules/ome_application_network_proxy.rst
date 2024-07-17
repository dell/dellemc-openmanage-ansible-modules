.. _ome_application_network_proxy_module:


ome_application_network_proxy -- Updates the proxy configuration on OpenManage Enterprise
=========================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to configure a network proxy on OpenManage Enterprise.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

  enable_proxy (True, bool, None)
    Enables or disables the HTTP proxy configuration.

    If \ :emphasis:`enable proxy`\  is false, then the HTTP proxy configuration is set to its default value.


  ip_address (optional, str, None)
    Proxy server address.

    This option is mandatory when \ :emphasis:`enable\_proxy`\  is true.


  proxy_port (optional, int, None)
    Proxy server's port number.

    This option is mandatory when \ :emphasis:`enable\_proxy`\  is true.


  enable_authentication (optional, bool, None)
    Enable or disable proxy authentication.

    If \ :emphasis:`enable\_authentication`\  is true, \ :emphasis:`proxy\_username`\  and \ :emphasis:`proxy\_password`\  must be provided.

    If \ :emphasis:`enable\_authentication`\  is false, the proxy username and password are set to its default values.


  proxy_username (optional, str, None)
    Proxy server username.

    This option is mandatory when \ :emphasis:`enable\_authentication`\  is true.


  proxy_password (optional, str, None)
    Proxy server password.

    This option is mandatory when \ :emphasis:`enable\_authentication`\  is true.


  ignore_certificate_validation (optional, bool, False)
    This option will ignore the integrated certificate checks like those used for the warranty and catalog updates.

    \ :literal:`true`\  ignores the certificate validation.

    \ :literal:`false`\  does not ignore the certificate validation.


  proxy_exclusion_list (optional, list, None)
    The list of IPv4 addresses, IPv6 addresses or the domain names of the devices that can bypass the proxy server to directly access the appliance.


  update_password (optional, bool, False)
    This flag is used to update the \ :emphasis:`proxy\_password`\ .

    This is applicable only when \ :emphasis:`enable\_authentication`\  is \ :literal:`true`\ .

    \ :literal:`true`\  will update the \ :emphasis:`proxy\_password`\ .

    \ :literal:`false`\  will not update the \ :emphasis:`proxy\_password`\ .


  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.


  password (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.


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
   - This module supports IPv4 and IPv6 addresses.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Update proxy configuration and enable authentication
      dellemc.openmanage.ome_application_network_proxy:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        enable_proxy: true
        ip_address: "192.168.0.2"
        proxy_port: 444
        enable_authentication: true
        proxy_username: "proxy_username"
        proxy_password: "proxy_password"

    - name: Reset proxy authentication
      dellemc.openmanage.ome_application_network_proxy:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        enable_proxy: true
        ip_address: "192.168.0.2"
        proxy_port: 444
        enable_authentication: false

    - name: Reset proxy configuration
      dellemc.openmanage.ome_application_network_proxy:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        enable_proxy: false

    - name: Add IPv4, IPv6 and domain names of devices in proxy exclusion list
      dellemc.openmanage.ome_application_network_proxy:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        enable_proxy: true
        ip_address: "192.168.0.2"
        proxy_port: 444
        enable_authentication: false
        proxy_exclusion_list:
          - 192.168.1.0
          - 191.187.2.0
          - www.*.com
          - 191.1.168.1/24

    - name: Clear the proxy exclusion list
      dellemc.openmanage.ome_application_network_proxy:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        enable_proxy: true
        ip_address: "192.168.0.2"
        proxy_port: 444
        proxy_exclusion_list: []

    - name: Ignore the certificate validation
      dellemc.openmanage.ome_application_network_proxy:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"
        enable_proxy: true
        ip_address: "192.168.0.2"
        proxy_port: 444
        ignore_certificate_validation: true



Return Values
-------------

msg (always, str, Successfully updated network proxy configuration.)
  Overall status of the network proxy configuration change.


proxy_configuration (On successful configuration of network proxy settings, dict, {'EnableAuthentication': True, 'EnableProxy': True, 'IpAddress': '192.168.0.2', 'Password': None, 'PortNumber': 444, 'ProxyExclusionList': ['192.168.0.1', 'www.*.com', '172.1.1.1/24'], 'SslCheckDisabled': False, 'Username': 'root'})
  Updated application network proxy configuration.


error_info (On HTTP error, dict, {'error': {'@Message.ExtendedInfo': [{'Message': 'Unable to complete the request because the input value for  PortNumber  is missing or an invalid value is entered.', 'MessageArgs': ['PortNumber'], 'MessageId': 'CGEN6002', 'RelatedProperties': [], 'Resolution': 'Enter a valid value and retry the operation.', 'Severity': 'Critical'}], 'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.'}})
  Details of the HTTP error.





Status
------





Authors
~~~~~~~

- Sajna Shetty(@Sajna-Shetty)
- Rajshekar P(@rajshekarp87)

