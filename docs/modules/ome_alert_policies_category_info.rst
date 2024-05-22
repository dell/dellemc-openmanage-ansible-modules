.. _ome_alert_policies_category_info_module:


ome_alert_policies_category_info -- Retrieves information of all OME alert policy categories.
=============================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to retrieve all the alert policy categories for OpenManage Enterprise and OpenManage Enterprise Modular.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6



Parameters
----------

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
   - This module supports IPv4 and IPv6 addresses.
   - This module supports \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Retrieve information about all the OME alert policy categories
      dellemc.openmanage.ome_alert_policies_category_info:
        hostname: "192.168.0.1"
        username: "username"
        password: "password"
        ca_path: "/path/to/ca_cert.pem"



Return Values
-------------

msg (always, str, Successfully retrieved alert policies category information.)
  Status of the alert policies category fetch operation.


categories (always, list, [{'CategoriesDetails': [{'CatalogName': 'Application', 'Id': 5, 'Name': 'Configuration', 'SubCategoryDetails': [{'Description': 'Application', 'Id': 85, 'Name': 'Application'}, {'Description': 'Users', 'Id': 35, 'Name': 'Users'}]}, {'CatalogName': 'Application', 'Id': 7, 'Name': 'Miscellaneous', 'SubCategoryDetails': [{'Description': 'Miscellaneous', 'Id': 20, 'Name': 'Miscellaneous'}]}, {'CatalogName': 'Application', 'Id': 2, 'Name': 'Storage', 'SubCategoryDetails': [{'Description': 'Devices', 'Id': 90, 'Name': 'Devices'}]}, {'CatalogName': 'Application', 'Id': 3, 'Name': 'Updates', 'SubCategoryDetails': [{'Description': 'Application', 'Id': 85, 'Name': 'Application'}, {'Description': 'Firmware', 'Id': 112, 'Name': 'Firmware'}]}], 'IsBuiltIn': True, 'Name': 'Application'}, {'CategoriesDetails': [{'CatalogName': 'Dell Storage', 'Id': 2, 'Name': 'Storage', 'SubCategoryDetails': [{'Description': 'Other', 'Id': 7700, 'Name': 'Other'}]}, {'CatalogName': 'Dell Storage', 'Id': 1, 'Name': 'System Health', 'SubCategoryDetails': [{'Description': 'Other', 'Id': 7700, 'Name': 'Other'}, {'Description': 'Storage', 'Id': 18, 'Name': 'Storage'}]}], 'IsBuiltIn': True, 'Name': 'Dell Storage'}, {'CategoriesDetails': [{'CatalogName': 'iDRAC', 'Id': 4, 'Name': 'Audit', 'SubCategoryDetails': [{'Description': 'Auto System Reset', 'Id': 41, 'Name': 'Auto System Reset'}, {'Description': 'UEFI Event', 'Id': 55, 'Name': 'UEFI Event'}, {'Description': 'User Tracking', 'Id': 56, 'Name': 'User Tracking'}]}, {'CatalogName': 'iDRAC', 'Id': 5, 'Name': 'Configuration', 'SubCategoryDetails': [{'Description': 'Auto-Discovery', 'Id': 49, 'Name': 'Auto-Discovery'}, {'Description': 'vFlash Event', 'Id': 66, 'Name': 'vFlash Event'}, {'Description': 'Virtual Console', 'Id': 7, 'Name': 'Virtual Console'}]}, {'CatalogName': 'iDRAC', 'Id': 2, 'Name': 'Storage', 'SubCategoryDetails': [{'Description': 'Battery Event', 'Id': 108, 'Name': 'Battery Event'}, {'Description': 'Virtual Disk', 'Id': 46, 'Name': 'Virtual Disk'}]}, {'CatalogName': 'iDRAC', 'Id': 1, 'Name': 'System Health', 'SubCategoryDetails': [{'Description': 'Amperage', 'Id': 67, 'Name': 'Amperage'}, {'Description': 'Auto System Reset', 'Id': 41, 'Name': 'Auto System Reset'}, {'Description': 'Voltage', 'Id': 40, 'Name': 'Voltage'}]}, {'CatalogName': 'iDRAC', 'Id': 6, 'Name': 'Work Notes', 'SubCategoryDetails': [{'Description': 'BIOS Management', 'Id': 54, 'Name': 'BIOS Management'}]}], 'IsBuiltIn': True, 'Name': 'iDRAC'}])
  Information about the alert categories.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'CGEN1234', 'RelatedProperties': [], 'Message': 'Unable to complete the request because the resource URI does not exist or is not implemented.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': "Check the request resource URI. Refer to the OpenManage Enterprise-Modular User's Guide for more information about resource URI and its properties."}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

