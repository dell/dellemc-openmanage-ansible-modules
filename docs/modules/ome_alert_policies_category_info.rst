.. _ome_alert_policies_category_info_module:


ome_alert_policies_category_info -- Retrieves information of all OME alert policy categories.
=============================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to retrieve all the OME alert policy categories.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.9.6



Parameters
----------

  hostname (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular IP address or hostname.


  username (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular username.


  password (True, str, None)
    OpenManage Enterprise or OpenManage Enterprise Modular password.


  port (optional, int, 443)
    OpenManage Enterprise or OpenManage Enterprise Modular HTTPS port.


  validate_certs (optional, bool, True)
    If ``false``, the SSL certificates will not be validated.

    Configure ``false`` only on personally controlled sites where self-signed certificates are used.

    Prior to collection version ``5.0.0``, the *validate_certs* is ``false`` by default.


  ca_path (optional, path, None)
    The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


  timeout (optional, int, 30)
    The socket level timeout in seconds.





Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell OpenManage Enterprise.
   - This module supports both IPv4 and IPv6 address.
   - This module supports ``check_mode``.




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

msg (on error, str, HTTP Error 501: 501)
  Error description in case of error.


categories (always, list, [{'CategoriesDetails': [{'CatalogName': 'Application', 'Id': 4, 'Name': 'Audit', 'SubCategoryDetails': [{'Description': 'Devices', 'Id': 90, 'Name': 'Devices'}, {'Description': 'Generic', 'Id': 10, 'Name': 'Generic'}, {'Description': 'Power Configuration', 'Id': 151, 'Name': 'Power Configuration'}, {'Description': 'Users', 'Id': 35, 'Name': 'Users'}]}, {'CatalogName': 'Application', 'Id': 5, 'Name': 'Configuration', 'SubCategoryDetails': [{'Description': 'Application', 'Id': 85, 'Name': 'Application'}, {'Description': 'Users', 'Id': 35, 'Name': 'Users'}]}, {'CatalogName': 'Application', 'Id': 7, 'Name': 'Miscellaneous', 'SubCategoryDetails': [{'Description': 'Miscellaneous', 'Id': 20, 'Name': 'Miscellaneous'}]}, {'CatalogName': 'Application', 'Id': 2, 'Name': 'Storage', 'SubCategoryDetails': [{'Description': 'Devices', 'Id': 90, 'Name': 'Devices'}]}, {'CatalogName': 'Application', 'Id': 1, 'Name': 'System Health', 'SubCategoryDetails': [{'Description': 'Devices', 'Id': 90, 'Name': 'Devices'}, {'Description': 'Health Status of Managed device', 'Id': 7400, 'Name': 'Health Status of Managed device'}, {'Description': 'Job', 'Id': 47, 'Name': 'Job'}, {'Description': 'Metrics', 'Id': 118, 'Name': 'Metrics'}, {'Description': 'Power Configuration', 'Id': 151, 'Name': 'Power Configuration'}]}, {'CatalogName': 'Application', 'Id': 3, 'Name': 'Updates', 'SubCategoryDetails': [{'Description': 'Application', 'Id': 85, 'Name': 'Application'}, {'Description': 'Firmware', 'Id': 112, 'Name': 'Firmware'}]}], 'IsBuiltIn': True, 'Name': 'Application'}, {'CategoriesDetails': [{'CatalogName': 'Dell Storage', 'Id': 2, 'Name': 'Storage', 'SubCategoryDetails': [{'Description': 'Other', 'Id': 7700, 'Name': 'Other'}]}, {'CatalogName': 'Dell Storage', 'Id': 1, 'Name': 'System Health', 'SubCategoryDetails': [{'Description': 'Other', 'Id': 7700, 'Name': 'Other'}, {'Description': 'Storage', 'Id': 18, 'Name': 'Storage'}]}], 'IsBuiltIn': True, 'Name': 'Dell Storage'}, {'CategoriesDetails': [{'CatalogName': 'iDRAC', 'Id': 4, 'Name': 'Audit', 'SubCategoryDetails': [{'Description': 'Auto System Reset', 'Id': 41, 'Name': 'Auto System Reset'}, {'Description': 'UEFI Event', 'Id': 55, 'Name': 'UEFI Event'}, {'Description': 'User Tracking', 'Id': 56, 'Name': 'User Tracking'}]}, {'CatalogName': 'iDRAC', 'Id': 5, 'Name': 'Configuration', 'SubCategoryDetails': [{'Description': 'Auto-Discovery', 'Id': 49, 'Name': 'Auto-Discovery'}, {'Description': 'vFlash Event', 'Id': 66, 'Name': 'vFlash Event'}, {'Description': 'Virtual Console', 'Id': 7, 'Name': 'Virtual Console'}]}, {'CatalogName': 'iDRAC', 'Id': 2, 'Name': 'Storage', 'SubCategoryDetails': [{'Description': 'Battery Event', 'Id': 108, 'Name': 'Battery Event'}, {'Description': 'Virtual Disk', 'Id': 46, 'Name': 'Virtual Disk'}]}, {'CatalogName': 'iDRAC', 'Id': 1, 'Name': 'System Health', 'SubCategoryDetails': [{'Description': 'Amperage', 'Id': 67, 'Name': 'Amperage'}, {'Description': 'Auto System Reset', 'Id': 41, 'Name': 'Auto System Reset'}, {'Description': 'Voltage', 'Id': 40, 'Name': 'Voltage'}]}, {'CatalogName': 'iDRAC', 'Id': 3, 'Name': 'Updates', 'SubCategoryDetails': [{'Description': 'Firmware Download', 'Id': 51, 'Name': 'Firmware Download'}, {'Description': 'Firmware Update Job', 'Id': 24, 'Name': 'Firmware Update Job'}, {'Description': 'Group Manager', 'Id': 53, 'Name': 'Group Manager'}, {'Description': 'UEFI Event', 'Id': 55, 'Name': 'UEFI Event'}]}, {'CatalogName': 'iDRAC', 'Id': 6, 'Name': 'Work Notes', 'SubCategoryDetails': [{'Description': 'BIOS Management', 'Id': 54, 'Name': 'BIOS Management'}]}], 'IsBuiltIn': True, 'Name': 'iDRAC'}, {'CategoriesDetails': [{'CatalogName': 'IF-MIB', 'Id': 4, 'Name': 'Audit', 'SubCategoryDetails': [{'Description': 'Interface', 'Id': 101, 'Name': 'Interface'}]}], 'IsBuiltIn': True, 'Name': 'IF-MIB'}, {'CategoriesDetails': [{'CatalogName': 'Internal Events Catalog', 'Id': 4, 'Name': 'Audit', 'SubCategoryDetails': [{'Description': 'BIOS Management', 'Id': 54, 'Name': 'BIOS Management'}, {'Description': 'Debug', 'Id': 12, 'Name': 'Debug'}, {'Description': 'Support Assist', 'Id': 92, 'Name': 'Support Assist'}, {'Description': 'Virtual Media', 'Id': 50, 'Name': 'Virtual Media'}]}, {'CatalogName': 'Internal Events Catalog', 'Id': 5, 'Name': 'Configuration', 'SubCategoryDetails': [{'Description': 'Auto-Discovery', 'Id': 49, 'Name': 'Auto-Discovery'}, {'Description': 'Backup/Restore', 'Id': 107, 'Name': 'Backup/Restore'}, {'Description': 'UEFI Event', 'Id': 55, 'Name': 'UEFI Event'}, {'Description': 'vFlash Event', 'Id': 66, 'Name': 'vFlash Event'}, {'Description': 'vFlash Media', 'Id': 74, 'Name': 'vFlash Media'}]}, {'CatalogName': 'Internal Events Catalog', 'Id': 7, 'Name': 'Miscellaneous', 'SubCategoryDetails': [{'Description': 'Application', 'Id': 85, 'Name': 'Application'}]}, {'CatalogName': 'Internal Events Catalog', 'Id': 2, 'Name': 'Storage', 'SubCategoryDetails': [{'Description': 'Battery Event', 'Id': 108, 'Name': 'Battery Event'}, {'Description': 'Virtual Disk', 'Id': 46, 'Name': 'Virtual Disk'}]}, {'CatalogName': 'Internal Events Catalog', 'Id': 1, 'Name': 'System Health', 'SubCategoryDetails': [{'Description': 'Amperage', 'Id': 67, 'Name': 'Amperage'}, {'Description': 'Auto System Reset', 'Id': 41, 'Name': 'Auto System Reset'}, {'Description': 'System Info', 'Id': 71, 'Name': 'System Info'}]}, {'CatalogName': 'Internal Events Catalog', 'Id': 6, 'Name': 'Work Notes', 'SubCategoryDetails': [{'Description': 'User Tracking', 'Id': 56, 'Name': 'User Tracking'}]}], 'IsBuiltIn': True, 'Name': 'Internal Events Catalog'}, {'CategoriesDetails': [{'CatalogName': 'Networking', 'Id': 1, 'Name': 'System Health', 'SubCategoryDetails': [{'Description': 'Other', 'Id': 7700, 'Name': 'Other'}]}], 'IsBuiltIn': True, 'Name': 'Networking'}, {'CategoriesDetails': [{'CatalogName': 'OMSA', 'Id': 4, 'Name': 'Audit', 'SubCategoryDetails': [{'Description': 'Log Event', 'Id': 19, 'Name': 'Log Event'}]}, {'CatalogName': 'OMSA', 'Id': 5, 'Name': 'Configuration', 'SubCategoryDetails': [{'Description': 'Auto System Reset', 'Id': 41, 'Name': 'Auto System Reset'}, {'Description': 'Processor', 'Id': 61, 'Name': 'Processor'}, {'Description': 'Security Event', 'Id': 25, 'Name': 'Security Event'}, {'Description': 'System Info', 'Id': 71, 'Name': 'System Info'}]}, {'CatalogName': 'OMSA', 'Id': 1, 'Name': 'System Health', 'SubCategoryDetails': [{'Description': 'Amperage', 'Id': 67, 'Name': 'Amperage'}, {'Description': 'Voltage', 'Id': 40, 'Name': 'Voltage'}]}], 'IsBuiltIn': True, 'Name': 'OMSA'}, {'CategoriesDetails': [{'CatalogName': 'OpenManage Enterprise', 'Id': 1, 'Name': 'System Health', 'SubCategoryDetails': [{'Description': 'Health Status of Managed device', 'Id': 7400, 'Name': 'Health Status of Managed device'}, {'Description': 'Metrics', 'Id': 118, 'Name': 'Metrics'}, {'Description': 'System Info', 'Id': 71, 'Name': 'System Info'}]}], 'IsBuiltIn': True, 'Name': 'OpenManage Enterprise'}, {'CategoriesDetails': [{'CatalogName': 'OpenManage Essentials', 'Id': 1, 'Name': 'System Health', 'SubCategoryDetails': [{'Description': 'Health Status of Managed device', 'Id': 7400, 'Name': 'Health Status of Managed device'}, {'Description': 'Other', 'Id': 7700, 'Name': 'Other'}]}, {'CatalogName': 'OpenManage Essentials', 'Id': 6, 'Name': 'Work Notes', 'SubCategoryDetails': []}], 'IsBuiltIn': True, 'Name': 'OpenManage Essentials'}, {'CategoriesDetails': [{'CatalogName': 'Power Manager', 'Id': 1, 'Name': 'System Health', 'SubCategoryDetails': [{'Description': 'Power Configuration', 'Id': 151, 'Name': 'Power Configuration'}]}], 'IsBuiltIn': True, 'Name': 'Power Manager'}, {'CategoriesDetails': [{'CatalogName': 'RFC1215', 'Id': 1, 'Name': 'System Health', 'SubCategoryDetails': [{'Description': 'Other', 'Id': 7700, 'Name': 'Other'}]}], 'IsBuiltIn': True, 'Name': 'RFC1215'}, {'CategoriesDetails': [{'CatalogName': 'SNMPv2-MIB', 'Id': 1, 'Name': 'System Health', 'SubCategoryDetails': [{'Description': 'Other', 'Id': 7700, 'Name': 'Other'}]}], 'IsBuiltIn': True, 'Name': 'SNMPv2-MIB'}, {'CategoriesDetails': [{'CatalogName': 'VMWare', 'Id': 1, 'Name': 'System Health', 'SubCategoryDetails': [{'Description': 'Other', 'Id': 7700, 'Name': 'Other'}]}], 'IsBuiltIn': True, 'Name': 'VMWare'}])
  Information about the alert categories.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'CGEN1234', 'RelatedProperties': [], 'Message': 'Unable to complete the request because the resource URI does not exist or is not implemented.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': "Check the request resource URI. Refer to the OpenManage Enterprise-Modular User's Guide for more information about resource URI and its properties."}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Jagadeesh N V(@jagadeeshnv)

