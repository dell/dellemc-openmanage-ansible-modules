.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.24.0

.. Anchors

.. _ansible_collections.dellemc.openmanage.idrac_session_module:

.. Anchors: short name for ansible.builtin

.. Title

dellemc.openmanage.idrac_session module -- Manage iDRAC sessions
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `dellemc.openmanage collection <https://galaxy.ansible.com/ui/repo/published/dellemc/openmanage/>`_ (version 7.6.1).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible\-galaxy collection install dellemc.openmanage`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.dellemc.openmanage.idrac_session_module_requirements>` for details.

    To use it in a playbook, specify: :code:`dellemc.openmanage.idrac_session`.

.. version_added

.. rst-class:: ansible-version-added

New in dellemc.openmanage 9.2.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- This module allows the creation and deletion of sessions on iDRAC.


.. Aliases


.. Requirements

.. _ansible_collections.dellemc.openmanage.idrac_session_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9.6






.. Options

Parameters
----------

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ca_path"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_module__parameter-ca_path:

      .. rst-class:: ansible-option-title

      **ca_path**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ca_path" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`path`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-hostname"></div>
        <div class="ansibleOptionAnchor" id="parameter-idrac_ip"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_module__parameter-hostname:
      .. _ansible_collections.dellemc.openmanage.idrac_session_module__parameter-idrac_ip:

      .. rst-class:: ansible-option-title

      **hostname**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-hostname" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: idrac_ip`

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      IP address or hostname of the iDRAC.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password"></div>
        <div class="ansibleOptionAnchor" id="parameter-idrac_password"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_module__parameter-idrac_password:
      .. _ansible_collections.dellemc.openmanage.idrac_session_module__parameter-password:

      .. rst-class:: ansible-option-title

      **password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-password" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: idrac_password`

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Password of the iDRAC. If the password is not provided, then the environment variable :ansenvvar:`IDRAC\_PASSWORD` is used.

      :emphasis:`password` is required when :emphasis:`state` is :literal:`present`.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-port"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_module__parameter-port:

      .. rst-class:: ansible-option-title

      **port**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-port" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Port of the iDRAC.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`443`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-session_id"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_module__parameter-session_id:

      .. rst-class:: ansible-option-title

      **session_id**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-session_id" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Session ID of the iDRAC.

      :emphasis:`session\_id` is required when :emphasis:`state` is :literal:`absent`.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_module__parameter-state:

      .. rst-class:: ansible-option-title

      **state**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The state of the session in an iDRAC.

      :literal:`present` creates a session.

      :literal:`absent` deletes a session.

      Module will always report changes found to be applied when :emphasis:`state` is :literal:`present`.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"present"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"absent"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-timeout"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_module__parameter-timeout:

      .. rst-class:: ansible-option-title

      **timeout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-timeout" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The https socket level timeout in seconds.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`30`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-username"></div>
        <div class="ansibleOptionAnchor" id="parameter-idrac_user"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_module__parameter-idrac_user:
      .. _ansible_collections.dellemc.openmanage.idrac_session_module__parameter-username:

      .. rst-class:: ansible-option-title

      **username**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-username" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: idrac_user`

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Username of the iDRAC. If the username is not provided, then the environment variable :ansenvvar:`IDRAC\_USERNAME` is used.

      :emphasis:`username` is required when :emphasis:`state` is :literal:`present`.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_module__parameter-validate_certs:

      .. rst-class:: ansible-option-title

      **validate_certs**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-validate_certs" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If :literal:`false`\ , the SSL certificates will not be validated.

      Configure :literal:`false` only on personally controlled sites where self\-signed certificates are used.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-x_auth_token"></div>
        <div class="ansibleOptionAnchor" id="parameter-auth_token"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_module__parameter-auth_token:
      .. _ansible_collections.dellemc.openmanage.idrac_session_module__parameter-x_auth_token:

      .. rst-class:: ansible-option-title

      **x_auth_token**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-x_auth_token" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: auth_token`

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Authentication token.

      :emphasis:`x\_auth\_token` is required when :emphasis:`state` is :literal:`absent`.


      .. raw:: html

        </div>


.. Attributes


.. Notes

Notes
-----

.. note::
   - Run this module from a system that has direct access to Dell iDRAC.
   - This module supports IPv4 and IPv6 addresses.
   - This module supports :literal:`check\_mode`.
   - This module will always report changes found to be applied when :emphasis:`state` is :literal:`present`.
   - When :emphasis:`state` is :literal:`absent`\ , self\-session termination protection is applied. If the target :emphasis:`session\_id` is determined to be the caller's own auth session, the deletion is rejected to prevent accidental lockout.
   - Self\-session protection is skipped when using :emphasis:`x\_auth\_token` because the caller's auth session ID cannot be determined from the token alone.

.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    ---
    - name: Create a session
      dellemc.openmanage.idrac_session:
        hostname: 198.162.0.1
        username: username
        password: password
        ca_path: "/path/to/ca_cert.pem"
        state: present

    - name: Delete a session
      dellemc.openmanage.idrac_session:
        hostname: 198.162.0.1
        ca_path: "/path/to/ca_cert.pem"
        state: absent
        x_auth_token: aed4aa802b748d2f3b31deec00a6b28a
        session_id: 2

    - name: Create a session and execute other modules
      block:
        - name: Create a session
          dellemc.openmanage.idrac_session:
            hostname: 198.162.0.1
            username: username
            password: password
            ca_path: "/path/to/ca_cert.pem"
            state: present
            register: authData

        - name: Call idrac_firmware_info module
          dellemc.openmanage.idrac_firmware_info:
            idrac_ip: 198.162.0.1
            ca_path: "/path/to/ca_cert.pem"
            x_auth_token: "{{ authData.x_auth_token }}"

        - name: Call idrac_user_info module
          dellemc.openmanage.idrac_user_info:
            idrac_ip: 198.162.0.1
            ca_path: "/path/to/ca_cert.pem"
            x_auth_token: "{{ authData.x_auth_token }}"
      always:
        - name: Destroy a session
          dellemc.openmanage.idrac_session:
            hostname: 198.162.0.1
            ca_path: "/path/to/ca_cert.pem"
            state: absent
            x_auth_token: "{{ authData.x_auth_token }}"
            session_id: "{{ authData.session_data.Id }}"



.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-error_info"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_module__return-error_info:

      .. rst-class:: ansible-option-title

      **error_info**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-error_info" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Details of the HTTP Error.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` On HTTP error

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`{"error": {"@Message.ExtendedInfo": [{"Message": "Unable to complete the operation because an invalid username and/or password is entered, and therefore authentication failed.", "MessageArgs": [], "MessageId": "IDRAC.2.9.SYS415", "RelatedProperties": [], "Resolution": "Enter valid user name and password and retry the operation.", "Severity": "Warning"}], "code": "Base.1.12.GeneralError", "message": "A general error has occurred. See ExtendedInfo for more information"}}`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-msg"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_module__return-msg:

      .. rst-class:: ansible-option-title

      **msg**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-msg" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Status of the session operation.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"The session has been created successfully."`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-session_data"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_module__return-session_data:

      .. rst-class:: ansible-option-title

      **session_data**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-session_data" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The session details.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` For session creation operation

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`{"@Message.ExtendedInfo": [{"Message": "The resource has been created successfully.", "MessageArgs": [], "MessageId": "Base.1.12.Created", "RelatedProperties": [], "Resolution": "None.", "Severity": "OK"}, {"Message": "A new resource is successfully created.", "MessageArgs": [], "MessageId": "IDRAC.2.9.SYS414", "RelatedProperties": [], "Resolution": "No response action is required.", "Severity": "Informational"}], "ClientOriginIPAddress": "100.96.37.58", "CreatedTime": "2024\-04\-05T01:14:01\-05:00", "Description": "User Session", "Id": "74", "Name": "User Session", "Password": null, "SessionType": "Redfish", "UserName": "root"}`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-x_auth_token"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_module__return-x_auth_token:

      .. rst-class:: ansible-option-title

      **x_auth_token**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-x_auth_token" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Authentication token.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` For session creation operation

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"d15f17f01cd627c30173b1582642497d"`


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Rajshekar P(@rajshekarp87)
- Kritika Bhateja (@Kritika-Bhateja-03)
- Saksham Nautiyal (@Saksham-Nautiyal)


.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. ansible-links::

  - title: "Issue Tracker"
    url: "https://github.com/dell/dellemc-openmanage-ansible-modules/issues"
    external: true
  - title: "Homepage"
    url: "https://github.com/dell/dellemc-openmanage-ansible-modules"
    external: true
  - title: "Repository (Sources)"
    url: "https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections"
    external: true


.. Parsing errors
