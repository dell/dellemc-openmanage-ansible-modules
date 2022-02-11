.. _dellemc_get_system_inventory_module:


dellemc_get_system_inventory -- Get the PowerEdge Server System Inventory
=========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get the PowerEdge Server System Inventory.



Requirements
------------
The below requirements are needed on the host that executes this module.

- omsdk >= 1.2.488
- python >= 3.8.6



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
   - Run this module from a system that has direct access to DellEMC iDRAC.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Get System Inventory
      dellemc.openmanage.dellemc_get_system_inventory:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"





Status
------


- This module will be removed in version
  .
  *[deprecated]*


Authors
~~~~~~~

- Rajeev Arakkal (@rajeevarakkal)

