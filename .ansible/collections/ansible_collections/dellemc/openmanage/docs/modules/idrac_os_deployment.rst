.. _idrac_os_deployment_module:


idrac_os_deployment -- Boot to a network ISO image
==================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Boot to a network ISO image.



Requirements
------------
The below requirements are needed on the host that executes this module.

- omsdk \>= 1.2.488
- python \>= 3.9.6



Parameters
----------

  share_name (True, str, None)
    CIFS or NFS Network share.


  share_user (optional, str, None)
    Network share user in the format 'user@domain' or 'domain\\\\user' if user is part of a domain else 'user'. This option is mandatory for CIFS Network Share.


  share_password (optional, str, None)
    Network share user password. This option is mandatory for CIFS Network Share.


  iso_image (True, str, None)
    Network ISO name.


  expose_duration (optional, int, 1080)
    It is the time taken in minutes for the ISO image file to be exposed as a local CD-ROM device to the host server. When the time expires, the ISO image gets automatically detached.


  idrac_ip (True, str, None)
    iDRAC IP Address.


  idrac_user (True, str, None)
    iDRAC username.

    If the username is not provided, then the environment variable \ :envvar:`IDRAC\_USERNAME`\  is used.

    Example: export IDRAC\_USERNAME=username


  idrac_password (True, str, None)
    iDRAC user password.

    If the password is not provided, then the environment variable \ :envvar:`IDRAC\_PASSWORD`\  is used.

    Example: export IDRAC\_PASSWORD=password


  idrac_port (optional, int, 443)
    iDRAC port.


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
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports both IPv4 and IPv6 address for \ :emphasis:`idrac\_ip`\ .
   - This module does not support \ :literal:`check\_mode`\ .




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Boot to Network ISO
      dellemc.openmanage.idrac_os_deployment:
          idrac_ip: "192.168.0.1"
          idrac_user: "user_name"
          idrac_password: "user_password"
          ca_path: "/path/to/ca_cert.pem"
          share_name: "192.168.0.0:/nfsfileshare"
          iso_image: "unattended_os_image.iso"
          expose_duration: 180



Return Values
-------------

msg (on error, str, Failed to boot to network iso)
  Over all device information status.


boot_status (always, dict, {'DeleteOnCompletion': 'false', 'InstanceID': 'DCIM_OSDConcreteJob:1', 'JobName': 'BootToNetworkISO', 'JobStatus': 'Success', 'Message': 'The command was successful.', 'MessageID': 'OSD1', 'Name': 'BootToNetworkISO', 'Status': 'Success', 'file': '192.168.0.0:/nfsfileshare/unattended_os_image.iso', 'retval': True})
  Details of the boot to network ISO image operation.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)
- Jagadeesh N V (@jagadeeshnv)

