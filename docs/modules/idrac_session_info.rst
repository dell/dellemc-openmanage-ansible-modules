.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.24.0

.. Anchors

.. _ansible_collections.dellemc.openmanage.idrac_session_info_module:

.. Anchors: short name for ansible.builtin

.. Title

dellemc.openmanage.idrac_session_info module -- Query iDRAC session information
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `dellemc.openmanage collection <https://galaxy.ansible.com/ui/repo/published/dellemc/openmanage/>`_ (version 7.6.1).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible\-galaxy collection install dellemc.openmanage`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.dellemc.openmanage.idrac_session_info_module_requirements>` for details.

    To use it in a playbook, specify: :code:`dellemc.openmanage.idrac_session_info`.

.. version_added

.. rst-class:: ansible-version-added

New in dellemc.openmanage 10.0.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- This module retrieves information about active sessions on a Dell iDRAC.
- It can query active sessions, session service configuration, and session limits.
- Supports client\-side filtering by session type, username, and stale session detection.
- This module is read\-only and does not modify any sessions.


.. Aliases


.. Requirements

.. _ansible_collections.dellemc.openmanage.idrac_session_info_module_requirements:

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

      .. _ansible_collections.dellemc.openmanage.idrac_session_info_module__parameter-ca_path:

      .. rst-class:: ansible-option-title

      **ca_path**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ca_path" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`path`

      :ansible-option-versionadded:`added in dellemc.openmanage 5.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-idrac_ip"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_info_module__parameter-idrac_ip:

      .. rst-class:: ansible-option-title

      **idrac_ip**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-idrac_ip" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      iDRAC IP Address.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-idrac_password"></div>
        <div class="ansibleOptionAnchor" id="parameter-idrac_pwd"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_info_module__parameter-idrac_password:
      .. _ansible_collections.dellemc.openmanage.idrac_session_info_module__parameter-idrac_pwd:

      .. rst-class:: ansible-option-title

      **idrac_password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-idrac_password" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: idrac_pwd`

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      iDRAC user password.

      If the password is not provided, then the environment variable :ansenvvar:`IDRAC\_PASSWORD` is used.

      Example: export IDRAC\_PASSWORD=password


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-idrac_port"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_info_module__parameter-idrac_port:

      .. rst-class:: ansible-option-title

      **idrac_port**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-idrac_port" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      iDRAC port.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`443`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-idrac_user"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_info_module__parameter-idrac_user:

      .. rst-class:: ansible-option-title

      **idrac_user**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-idrac_user" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      iDRAC username.

      If the username is not provided, then the environment variable :ansenvvar:`IDRAC\_USERNAME` is used.

      Example: export IDRAC\_USERNAME=username


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-session_type"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_info_module__parameter-session_type:

      .. rst-class:: ansible-option-title

      **session_type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-session_type" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Filter sessions by DMTF session type.

      Case\-insensitive exact match against the :literal:`SessionType` field.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Redfish"`
      - :ansible-option-choices-entry:`"WebUI"`
      - :ansible-option-choices-entry:`"IPMI"`
      - :ansible-option-choices-entry:`"KVMS"`
      - :ansible-option-choices-entry:`"VirtualMedia"`
      - :ansible-option-choices-entry:`"OEM"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-stale_threshold_minutes"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_info_module__parameter-stale_threshold_minutes:

      .. rst-class:: ansible-option-title

      **stale_threshold_minutes**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-stale_threshold_minutes" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Flag sessions as stale if their age exceeds this threshold in minutes.

      Sessions older than this value will have :literal:`is\_stale` set to :literal:`true`.

      Must be a positive integer.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-timeout"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_info_module__parameter-timeout:

      .. rst-class:: ansible-option-title

      **timeout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-timeout" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in dellemc.openmanage 5.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The socket level timeout in seconds.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`30`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-username_filter"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_info_module__parameter-username_filter:

      .. rst-class:: ansible-option-title

      **username_filter**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-username_filter" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Filter sessions by username.

      Case\-insensitive substring match against the :literal:`UserName` field.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_info_module__parameter-validate_certs:

      .. rst-class:: ansible-option-title

      **validate_certs**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-validate_certs" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in dellemc.openmanage 5.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If :literal:`false`\ , the SSL certificates will not be validated.

      Configure :literal:`false` only on personally controlled sites where self\-signed certificates are used.

      Prior to collection version :literal:`5.0.0`\ , the :emphasis:`validate\_certs` is :literal:`false` by default.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


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
   - Minimum firmware versions \- iDRAC9 \>= 7.10.90.00, iDRAC10 \>= 1.20.50.50.
   - Session age is computed from :literal:`CreatedTime`\ , which reflects session creation time, not last activity. For true idle time detection, use iDRAC OEM Redfish extensions (future enhancement).
   - For fleet operations, use Ansible :literal:`forks` to parallelize queries across multiple iDRAC instances.
   - Administrator privileges are required to query all sessions. Non\-admin users may only see their own sessions.

.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    ---
    - name: Query all active sessions
      dellemc.openmanage.idrac_session_info:
        idrac_ip: 198.162.0.1
        idrac_user: username
        idrac_password: password
        ca_path: "/path/to/ca_cert.pem"

    - name: Filter sessions by type
      dellemc.openmanage.idrac_session_info:
        idrac_ip: 198.162.0.1
        idrac_user: username
        idrac_password: password
        ca_path: "/path/to/ca_cert.pem"
        session_type: Redfish

    - name: Find stale sessions older than 24 hours
      dellemc.openmanage.idrac_session_info:
        idrac_ip: 198.162.0.1
        idrac_user: username
        idrac_password: password
        ca_path: "/path/to/ca_cert.pem"
        stale_threshold_minutes: 1440

    - name: Filter by username and session type
      dellemc.openmanage.idrac_session_info:
        idrac_ip: 198.162.0.1
        idrac_user: username
        idrac_password: password
        ca_path: "/path/to/ca_cert.pem"
        session_type: Redfish
        username_filter: admin

    - name: Query sessions using token authentication
      dellemc.openmanage.idrac_session_info:
        idrac_ip: 198.162.0.1
        ca_path: "/path/to/ca_cert.pem"
        x_auth_token: "aed4aa802b748d2f3b31deec00a6b28a"

    - name: Troubleshoot Max Sessions Reached (UC-1)
      block:
        - name: Create a session
          dellemc.openmanage.idrac_session:
            hostname: 198.162.0.1
            username: "{{ vault_idrac_user }}"
            password: "{{ vault_idrac_password }}"
            ca_path: "/path/to/ca_cert.pem"
            state: present
          register: auth_data

        - name: Query session utilization
          dellemc.openmanage.idrac_session_info:
            idrac_ip: 198.162.0.1
            idrac_user: "{{ vault_idrac_user }}"
            idrac_password: "{{ vault_idrac_password }}"
            ca_path: "/path/to/ca_cert.pem"
          register: session_info

        - name: Display utilization
          ansible.builtin.debug:
            msg: "Session utilization: {{ session_info.session_limits.utilization_percent }}%"
      always:
        - name: Destroy the session
          dellemc.openmanage.idrac_session:
            hostname: 198.162.0.1
            ca_path: "/path/to/ca_cert.pem"
            state: absent
            x_auth_token: "{{ auth_data.x_auth_token }}"
            session_id: "{{ auth_data.session_data.Id }}"

    - name: Fleet-wide session monitoring (UC-2)
      hosts: idrac_fleet
      gather_facts: false
      tasks:
        - name: Query sessions on each iDRAC
          dellemc.openmanage.idrac_session_info:
            idrac_ip: "{{ inventory_hostname }}"
            idrac_user: "{{ vault_idrac_user }}"
            idrac_password: "{{ vault_idrac_password }}"
            ca_path: "/path/to/ca_cert.pem"
          register: session_info

        - name: Report high utilization
          ansible.builtin.debug:
            msg: "WARNING: {{ inventory_hostname }} at {{ session_info.session_limits.utilization_percent }}% utilization"
          when: session_info.session_limits.utilization_percent | default(0) > 80

    - name: Nightly stale session cleanup (UC-3)
      hosts: idrac_fleet
      gather_facts: false
      tasks:
        - name: Find stale sessions
          dellemc.openmanage.idrac_session_info:
            idrac_ip: "{{ inventory_hostname }}"
            idrac_user: "{{ vault_idrac_user }}"
            idrac_password: "{{ vault_idrac_password }}"
            ca_path: "/path/to/ca_cert.pem"
            stale_threshold_minutes: 1440
          register: session_info

        - name: Terminate stale sessions
          dellemc.openmanage.idrac_session:
            hostname: "{{ inventory_hostname }}"
            ca_path: "/path/to/ca_cert.pem"
            state: absent
            x_auth_token: "{{ vault_idrac_auth_token }}"
            session_id: "{{ item.id }}"
          loop: "{{ session_info.sessions | selectattr('is_stale', 'equalto', true) | list }}"
          when: session_info.sessions | selectattr('is_stale', 'equalto', true) | list | length > 0



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

      .. _ansible_collections.dellemc.openmanage.idrac_session_info_module__return-error_info:

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

      :ansible-option-returned-bold:`Returned:` on HTTP error

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`{"error": {"@Message.ExtendedInfo": [{"Message": "Unable to complete the operation.", "MessageId": "IDRAC.2.9.SYS415", "Resolution": "Enter valid credentials.", "Severity": "Warning"}], "code": "Base.1.12.GeneralError", "message": "A general error has occurred."}}`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-idrac_firmware_version"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_info_module__return-idrac_firmware_version:

      .. rst-class:: ansible-option-title

      **idrac_firmware_version**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-idrac_firmware_version" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Detected iDRAC firmware version.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"7.10.90.00"`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-idrac_model"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_info_module__return-idrac_model:

      .. rst-class:: ansible-option-title

      **idrac_model**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-idrac_model" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Detected iDRAC model.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"iDRAC 9"`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-msg"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_info_module__return-msg:

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

      Status of the session query operation.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"Successfully retrieved session information."`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-session_count"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_info_module__return-session_count:

      .. rst-class:: ansible-option-title

      **session_count**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-session_count" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Number of sessions returned (after filtering).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`3`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-session_limits"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_info_module__return-session_limits:

      .. rst-class:: ansible-option-title

      **session_limits**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-session_limits" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Session limits and utilization.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`{"active\_count": 5, "max\_sessions": 64, "source": "idrac\_attributes", "utilization\_percent": 7.81}`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-session_service"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_info_module__return-session_service:

      .. rst-class:: ansible-option-title

      **session_service**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-session_service" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Session service configuration.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`{"service\_enabled": true, "session\_timeout": 1800}`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-sessions"></div>

      .. _ansible_collections.dellemc.openmanage.idrac_session_info_module__return-sessions:

      .. rst-class:: ansible-option-title

      **sessions**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-sessions" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      List of active sessions with details.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`[{"client\_origin\_ip": "100.96.37.58", "created\_time": "2024\-04\-05T01:14:01\-05:00", "description": "User Session", "id": "74", "is\_stale": false, "name": "User Session", "session\_age\_minutes": 120, "session\_type": "Redfish", "user\_name": "root"}]`


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

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
