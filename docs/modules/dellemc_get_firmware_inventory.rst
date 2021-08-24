.. _dellemc_get_firmware_inventory_module:


dellemc_get_firmware_inventory -- Get Firmware Inventory
========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get Firmware Inventory.



Requirements
------------
The below requirements are needed on the host that executes this module.

- omsdk
- python >= 2.7.5



Parameters
----------

  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.


  idrac_password (True, str, None)
    iDRAC user password.


  idrac_port (optional, int, 443)
    iDRAC port.





Notes
-----

.. note::
   - Run this module from a system that has direct access to DellEMC iDRAC.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Get Installed Firmware Inventory
      dellemc.openmanage.dellemc_get_firmware_inventory:
          idrac_ip:   "192.168.0.1"
          idrac_user: "user_name"
          idrac_password:  "user_password"





Status
------


- This module will be removed in version
  .
  *[deprecated]*


Authors
~~~~~~~

- Rajeev Arakkal (@rajeevarakkal)

