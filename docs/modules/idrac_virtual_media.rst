.. _idrac_virtual_media_module:


idrac_virtual_media -- Configure the Remote File Share settings.
================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module allows to configure Remote File Share settings.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.8.6



Parameters
----------

  virtual_media (True, list, None)
    Details of the Remote File Share.


    insert (True, bool, None)
      ``True`` connects the remote image file.

      ``False`` ejects the remote image file if connected.


    image (optional, path, None)
      The path of the image file. The supported file types are .img and .iso.

      The file name with .img extension is redirected as a virtual floppy and a file name with .iso extension is redirected as a virtual CDROM.

      This option is required when *insert* is ``True``.

      The following are the examples of the share location: CIFS share: //192.168.0.1/file_path/image_name.iso, NFS share: 192.168.0.2:/file_path/image_name.img, HTTP share: http://192.168.0.3/file_path/image_name.iso, HTTPS share: https://192.168.0.4/file_path/image_name.img

      CIFS share is not supported by iDRAC7 and iDRAC8.

      HTTPS share with credentials is not supported by iDRAC7 and iDRAC8.


    index (optional, int, None)
      Index of the Remote File Share. For example, to specify the Remote File Share 1, the value of *index* should be 1. If *index* is not specified, the order of *virtual_media* list will be considered.


    domain (optional, str, None)
      Domain name of network share. This option is applicable for CIFS and HTTPS share.


    username (optional, str, None)
      Network share username. This option is applicable for CIFS and HTTPS share.


    password (optional, str, None)
      Network share password. This option is applicable for CIFS and HTTPS share.

      This module always reports as the changes found when *password* is provided.


    media_type (optional, str, None)
      Type of the image file. This is applicable when *insert* is ``True``.



  force (optional, bool, False)
    ``True`` ejects the image file if already connected and inserts the file provided in *image*. This is applicable when *insert* is ``True``.


  resource_id (optional, str, None)
    Resource id of the iDRAC, if not specified manager collection id will be used.


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
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports ``check_mode``.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Insert image file to Remote File Share 1 using CIFS share.
      dellemc.openmanage.idrac_virtual_media:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        virtual_media:
          - insert: true
            image: "//192.168.0.2/file_path/file.iso"
            username: "username"
            password: "password"

    - name: Insert image file to Remote File Share 2 using NFS share.
      dellemc.openmanage.idrac_virtual_media:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        virtual_media:
          - index: 2
            insert: true
            image: "192.168.0.4:/file_path/file.iso"

    - name: Insert image file to Remote File Share 1 and 2 using HTTP.
      dellemc.openmanage.idrac_virtual_media:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        force: true
        virtual_media:
          - index: 1
            insert: true
            image: "http://192.168.0.4/file_path/file.img"
          - index: 2
            insert: true
            image: "http://192.168.0.4/file_path/file.img"

    - name: Insert image file using HTTPS.
      dellemc.openmanage.idrac_virtual_media:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        force: true
        virtual_media:
          - index: 1
            insert: true
            image: "https://192.168.0.5/file_path/file.img"
            username: username
            password: password

    - name: Eject multiple virtual media.
      dellemc.openmanage.idrac_virtual_media:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        force: true
        virtual_media:
          - index: 1
            insert: false
          - index: 2
            insert: false

    - name: Ejection of image file from Remote File Share 1.
      dellemc.openmanage.idrac_virtual_media:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        force: true
        virtual_media:
            insert: false

    - name: Insertion and ejection of image file in single task.
      dellemc.openmanage.idrac_virtual_media:
        idrac_ip: "192.168.0.1"
        idrac_user: "user_name"
        idrac_password: "user_password"
        ca_path: "/path/to/ca_cert.pem"
        force: true
        virtual_media:
          - index: 1
            insert: true
            image: https://192.168.0.5/file/file.iso
            username: username
            password: password
          - index: 2
            insert: false



Return Values
-------------

msg (success, str, Successfully performed the virtual media operation.)
  Successfully performed the virtual media operation.


error_info (on HTTP error, dict, {'error': {'code': 'Base.1.0.GeneralError', 'message': 'A general error has occurred. See ExtendedInfo for more information.', '@Message.ExtendedInfo': [{'MessageId': 'GEN1234', 'RelatedProperties': [], 'Message': 'Unable to process the request because an error occurred.', 'MessageArgs': [], 'Severity': 'Critical', 'Resolution': 'Retry the operation. If the issue persists, contact your system administrator.'}]}})
  Details of the HTTP Error.





Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88)

